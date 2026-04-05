"""
API's tested in hardware.py:
    - POST /api/hardware/<hardware_id>/checkout
    - POST /api/hardware/<hardware_id>/checkin

Baseline Rules:
    - 1 happy path
    - 1 invalid input
    - 1 boundary/guard case
    - 1 missing/unauthorized
"""

CHECKOUT_URL = "/api/hardware/{id}/checkout"
CHECKIN_URL = "/api/hardware/{id}/checkin"


# ---------------------------------------------------------------------------
# checkout_hardware()
# ---------------------------------------------------------------------------


def test_checkout_valid_base_case(client, checkout_test_data):
    """Happy path: successful hardware checkout updates global hardware sets."""
    hw_id, project_id, user_id = checkout_test_data

    response = client.post(
        CHECKOUT_URL.format(id=hw_id),
        json={
            "projectId": project_id,
            "amount": 3,
            "userId": user_id
        }
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["available"] == 7  # 10 - 3
    assert project_id in body["assignedProjects"]


def test_checkout_invalid_input_trigger_validation_err(client, valid_hardware):
    """Invalid input: non-positive integer entered in "amount" should trigger ValidationError."""
    response = client.post(
        CHECKOUT_URL.format(id=valid_hardware),
        json={
            "projectId": "test-project",
            "amount": 0,
            "userId": "test-user"
        }
    )

    assert response.status_code == 400
    body = response.get_json()
    assert "Validation failed" in body["error"]


def test_checkout_excessive_amount_trigger_error_handling(client, fake_projects, limited_hardware, valid_user):
    """Boundary/Guard Case: attempting to checkout more units than available should trigger manual error handling."""
    # Create project with user
    fake_projects.insert_one({
        "projectId": "test-project",
        "projectName": "Test Project",
        "description": "A test project",
        "ownerUserId": valid_user,
        "assignedUsers": [valid_user],
        "assignedHardware": []
    })

    # Try to checkout more than available
    response = client.post(
        CHECKOUT_URL.format(id=limited_hardware),
        json={
            "projectId": "test-project",
            "amount": 7,  # More than available (5)
            "userId": valid_user
        }
    )

    assert response.status_code == 400
    body = response.get_json()
    assert "Insufficient availability" in body["error"]


def test_checkout_unauthorized_trigger_validation_err(client, fake_projects, valid_hardware):
    """Unauthorized case: user not assigned to project should be rejected."""
    # Create project with different user
    fake_projects.insert_one({
        "projectId": "test-project",
        "projectName": "Test Project",
        "description": "A test project",
        "ownerUserId": "owner-user",
        "assignedUsers": ["owner-user"],
        "assignedHardware": []
    })

    # Try to checkout with user not assigned to project
    response = client.post(
        CHECKOUT_URL.format(id=valid_hardware),
        json={
            "projectId": "test-project",
            "amount": 3,
            "userId": "unauthorized-user"  # Not in assignedUsers
        }
    )

    assert response.status_code == 403
    body = response.get_json()
    assert "User is not assigned to this project" in body["error"]


# ---------------------------------------------------------------------------
# checkin_hardware()
# ---------------------------------------------------------------------------


def test_checkin_valid_base_case(client, checkin_test_data, fake_projects):
    """Happy Path: successful hardware checkin updates global hardware sets."""
    hw_id, project_id, user_id = checkin_test_data

    response = client.post(
        CHECKIN_URL.format(id=hw_id),
        json={
            "projectId": project_id,
            "amount": 2,  # Partial checkin
            "userId": user_id
        }
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["available"] == 9  # 7 + 2

    # Verify project was updated
    project = fake_projects.find_one({"projectId": project_id})
    assert len(project["assignedHardware"]) == 1
    assert project["assignedHardware"][0]["amount"] == 1  # 3 - 2


def test_checkin_invalid_input_trigger_validation_err(client, valid_hardware):
    """Invalid Input: non-positive integer entered in "amount" should trigger ValidationError."""
    response = client.post(
        CHECKIN_URL.format(id=valid_hardware),
        json={
            "projectId": "test-project",
            "amount": -1,
            "userId": "test-user"
        }
    )

    assert response.status_code == 400
    body = response.get_json()
    assert "Validation failed" in body["error"]


def test_checkin_excessive_amount_trigger_error_handling(client, checkin_test_data):
    """Boundary/Guard Case: attempting to checkin more units than checked out should trigger error."""
    hw_id, project_id, user_id = checkin_test_data

    # Try to checkin more than checked out (3)
    response = client.post(
        CHECKIN_URL.format(id=hw_id),
        json={
            "projectId": project_id,
            "amount": 5,
            "userId": user_id
        }
    )

    assert response.status_code == 400
    body = response.get_json()
    assert "Cannot check in 5 units" in body["error"]


def test_checkin_missing_user_id_trigger_validation_err(client, valid_hardware):
    """Missing Case: attempting to checkin without "userId" should trigger ValidationError."""
    response = client.post(
        CHECKIN_URL.format(id=valid_hardware),
        json={
            "projectId": "test-project",
            "amount": 2
            # Missing userId
        }
    )

    assert response.status_code == 400
    body = response.get_json()
    assert "Validation failed" in body["error"]