"""
Input Space Partitioning (ISP) tests for checkout_hardware and checkin_hardware functions.

Test cases are designed based on the IDM partitions for checkout and checkin operations that take
into account the amount, user assignment, and project validity characteristics.
"""

CHECKOUT_URL = "/api/hardware/{id}/checkout"
CHECKIN_URL = "/api/hardware/{id}/checkin"


# -----------------------------------------------
# checkout_hardware — BCC Tests
# -----------------------------------------------


def test_isp_checkout_base_valid(client, checkout_test_data):
    """
    T-ISP-CO-BASE | BCC Base | Partition: C1=b3 (amount=1), C2=b1 (assigned), C3=b1 (valid project)
    Base case: all three characteristics at base choice — minimum valid amount, authorized user, existing project.
    Expected: 200; available==9 (10-1)
    """
    hw_id, project_id, user_id = checkout_test_data

    response = client.post(
        CHECKOUT_URL.format(id=hw_id),
        json={"projectId": project_id, "amount": 1, "userId": user_id}
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["available"] == 9  # 10 - 1
    assert project_id in body["assignedProjects"]


def test_isp_checkout_amount_negative(client, valid_hardware):
    """
    T-ISP-CO-C1-b1 | BCC Non-base | Partition: C1=b1 (amount<0), C2=b1, C3=b1
    Base case: negative amount; Pydantic rejects before any DB lookup (amount >= 1 required).
    Expected: 400 ValidationError
    """
    response = client.post(
        CHECKOUT_URL.format(id=valid_hardware),
        json={"projectId": "any-project", "amount": -2, "userId": "any-user"}
    )

    assert response.status_code == 400
    body = response.get_json()
    assert body["error"] == "Validation failed"


def test_isp_checkout_amount_zero(client, valid_hardware):
    """
    T-ISP-CO-C1-b2 | BCC Non-base | Partition: C1=b2 (amount==0), C2=b1, C3=b1
    Base case: zero amount at the lower domain boundary; Pydantic rejects before the DB guard.
    Expected: 400 ValidationError
    """
    response = client.post(
        CHECKOUT_URL.format(id=valid_hardware),
        json={"projectId": "any-project", "amount": 0, "userId": "any-user"}
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Validation failed"


def test_isp_checkout_amount_exact_capacity(client, fake_hardware, fake_projects, fake_users, valid_user):
    """
    T-ISP-CO-C1-b4 | BCC Non-base | Partition: C1=b4 (amount==available), C2=b1, C3=b1
    Base case: amount equals all available units (boundary of valid domain); guard (5<5) is False, checkout proceeds.
    Expected: 200; available==0
    """
    hw_result = fake_hardware.insert_one({
        "hardwareName": "Exact Capacity Hardware",
        "capacity": 5,
        "available": 5,
        "assignedProjects": []
    })
    hw_id = str(hw_result.inserted_id)

    fake_projects.insert_one({
        "projectId": "test-project",
        "projectName": "Test Project",
        "description": "A test project",
        "ownerUserId": valid_user,
        "assignedUsers": [valid_user],
        "assignedHardware": []
    })

    response = client.post(
        CHECKOUT_URL.format(id=hw_id),
        json={"projectId": "test-project", "amount": 5, "userId": valid_user}
    )

    assert response.status_code == 200
    assert response.get_json()["available"] == 0


def test_isp_checkout_amount_over_capacity(client, fake_hardware, fake_projects, fake_users, valid_user):
    """
    T-ISP-CO-C1-b5 | BCC Non-base | Partition: C1=b5 (amount>available), C2=b1, C3=b1
    Base case: requested amount exceeds available stock; availability guard (5<8) fires.
    Expected: 400 "Insufficient availability. Only 5 units available"
    """
    hw_result = fake_hardware.insert_one({
        "hardwareName": "Scarce Hardware",
        "capacity": 10,
        "available": 5,
        "assignedProjects": []
    })
    hw_id = str(hw_result.inserted_id)

    fake_projects.insert_one({
        "projectId": "test-project",
        "projectName": "Test Project",
        "description": "A test project",
        "ownerUserId": valid_user,
        "assignedUsers": [valid_user],
        "assignedHardware": []
    })

    response = client.post(
        CHECKOUT_URL.format(id=hw_id),
        json={"projectId": "test-project", "amount": 8, "userId": valid_user}
    )

    assert response.status_code == 400
    assert "Insufficient availability" in response.get_json()["error"]


def test_isp_checkout_user_not_assigned(client, fake_hardware, fake_projects, fake_users, valid_user):
    """
    T-ISP-CO-C2-b2 | BCC Non-base | Partition: C1=b3, C2=b2 (user not assigned), C3=b1
    Base case: valid project exists but the requesting user is not in assignedUsers.
    Expected: 403 "User is not assigned to this project"
    """
    hw_result = fake_hardware.insert_one({
        "hardwareName": "Test Hardware",
        "capacity": 10,
        "available": 10,
        "assignedProjects": []
    })
    hw_id = str(hw_result.inserted_id)

    fake_projects.insert_one({
        "projectId": "test-project",
        "projectName": "Test Project",
        "description": "A test project",
        "ownerUserId": valid_user,
        "assignedUsers": [valid_user],  # Only valid_user is assigned
        "assignedHardware": []
    })

    response = client.post(
        CHECKOUT_URL.format(id=hw_id),
        json={"projectId": "test-project", "amount": 1, "userId": "outsider-user"}
    )

    assert response.status_code == 403
    assert "User is not assigned to this project" in response.get_json()["error"]


def test_isp_checkout_project_invalid(client, valid_hardware):
    """
    T-ISP-CO-C3-b2 | BCC Non-base | Partition: C1=b3, C2=b1, C3=b2 (project not in DB)
    Base case: project ID does not match any document; C2 is unobservable (constraint: C2 irrelevant when C3=b2).
    Expected: 404 "Project not found"
    """
    response = client.post(
        CHECKOUT_URL.format(id=valid_hardware),
        json={"projectId": "ghost-project", "amount": 1, "userId": "any-user"}
    )

    assert response.status_code == 404
    assert response.get_json()["error"] == "Project not found"


# -----------------------------------------------
# checkin_hardware — BCC Base Test
# -----------------------------------------------


def test_isp_checkin_base_valid(client, checkin_test_data):
    """
    T-ISP-CI-BASE | BCC Base | Partition: C1=b3 (amount=1), C2=b1 (assigned), C3=b1 (valid project)
    Base case: partial checkin (1 of 3 checked-out units returned); $inc path runs, entry amount decremented.
    Expected: 200; available==8 (7+1)
    """
    hw_id, project_id, user_id = checkin_test_data

    response = client.post(
        CHECKIN_URL.format(id=hw_id),
        json={"projectId": project_id, "amount": 1, "userId": user_id}
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["available"] == 8  # 7 + 1
