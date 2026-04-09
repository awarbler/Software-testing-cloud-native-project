"""
Logic Coverage (CACC) Test Cases for the checkout_hardware & checkin_hardware functions

Test cases are designed to achieve Correlated Active Clause Coverage (CACC) for the key predicates in the checkout 
and checkin logic, focusing on the availability guard in checkout and the checkin amount guard.
"""

CHECKOUT_URL = "/api/hardware/{id}/checkout"
CHECKIN_URL = "/api/hardware/{id}/checkin"


# ------------------------------------------------
# checkout_hardware — CACC Tests
# ------------------------------------------------


def test_cacc_checkout_predicate_true_c2_major(client, checkout_test_data):
    """
    T-CACC-CO-01 | PC: p=T | CC: c1=T, c2=T | CACC (c2 major): {c1=T, c2=T}→p=T — determination condition c1=T satisfied
    Base case: amount=3 ≤ available=10; availability guard (N11) takes False branch, checkout proceeds.
    Expected: 200; available==7 (10-3)
    """
    hw_id, project_id, user_id = checkout_test_data

    response = client.post(
        CHECKOUT_URL.format(id=hw_id),
        json={"projectId": project_id, "amount": 3, "userId": user_id}
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["available"] == 7
    assert project_id in body["assignedProjects"]


def test_cacc_checkout_predicate_false_c2_major(client, fake_hardware, fake_projects, fake_users, valid_user):
    """
    T-CACC-CO-02: p=F via c2=F | c2 as major clause (determination condition: c1=T)
    Base case: amount=7 > available=5; availability guard (N11) takes True branch, checkout blocked.
    Expected: 400 {"error": "Insufficient availability. Only 5 units available"}
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
        json={"projectId": "test-project", "amount": 7, "userId": valid_user}
    )

    assert response.status_code == 400
    assert "Insufficient availability" in response.get_json()["error"]


def test_cacc_checkout_c1_false_at_pydantic_boundary(client, valid_hardware):
    """
    T-CACC-CO-03: c1=F at Pydantic boundary (N2) | CACC (c1 major): {c1=F, c2=T}→p=F INFEASIBLE at N11
    Base case: amount=0 fails Pydantic amount>=1; c1=F only reachable at N2, never at guard node N11.
    Expected: 400 {"error": "Validation failed"}
    """
    response = client.post(
        CHECKOUT_URL.format(id=valid_hardware),
        json={"projectId": "test-project", "amount": 0, "userId": "test-user"}
    )

    assert response.status_code == 400
    body = response.get_json()
    assert body["error"] == "Validation failed"


def test_cacc_checkout_boundary_c2_equal(client, fake_hardware, fake_projects, fake_users, valid_user):
    """
    T-CACC-CO-04: p=T at c2 boundary | CACC (c2 major): {c1=T, c2=T}→p=T; c2=(5<=5)=True (off-by-one check)
    Base case: amount=5 == available=5; guard (N11) takes False branch, all units checked out.
    Expected: 200; available==0
    """
    hw_result = fake_hardware.insert_one({
        "hardwareName": "Boundary Hardware",
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


# ------------------------------------------------
# checkin_hardware — CACC Tests
# ------------------------------------------------


def test_cacc_checkin_predicate_true_c2_major(client, checkin_test_data):
    """
    T-CACC-CI-01 | PC: p=T | CC: c1=T, c2=T | CACC (c2 major): {c1=T, c2=T}→p=T; c2=(2<=3)=True
    Base case: amount=2 <= entry=3; checkin guard (N13) takes False branch, checkin proceeds.
    Expected: 200; available==9 (7+2)
    """
    hw_id, project_id, user_id = checkin_test_data

    response = client.post(
        CHECKIN_URL.format(id=hw_id),
        json={"projectId": project_id, "amount": 2, "userId": user_id}
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["available"] == 9  # 7 + 2


def test_cacc_checkin_predicate_false_c2_major(client, checkin_test_data):
    """
    T-CACC-CI-02 | PC: p=F | CC: c1=T, c2=F | CACC (c2 major): {c1=T, c2=F}→p=F; c2=(5<=3)=False
    Base case: amount=5 > entry=3; checkin guard (N13) takes True branch, checkin blocked.
    Expected: 400 {"error": "Cannot check in 5 units..."}
    """
    hw_id, project_id, user_id = checkin_test_data

    response = client.post(
        CHECKIN_URL.format(id=hw_id),
        json={"projectId": project_id, "amount": 5, "userId": user_id}
    )

    assert response.status_code == 400
    assert "Cannot check in 5 units" in response.get_json()["error"]


def test_cacc_checkin_c1_false_at_pydantic_boundary(client, valid_hardware):
    """
    T-CACC-CI-03: c1=F at Pydantic boundary (N2) | CACC (c1 major): {c1=F, c2=T}→p=F INFEASIBLE at N13
    Base case: amount=-1 fails Pydantic amount>=1; c1=F only reachable at N2, never at guard node N13.
    Expected: 400 {"error": "Validation failed"}
    """
    response = client.post(
        CHECKIN_URL.format(id=valid_hardware),
        json={"projectId": "test-project", "amount": -1, "userId": "test-user"}
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Validation failed"
