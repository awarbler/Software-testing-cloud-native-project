"""
Structural Test Cases for checkout_hardware and checkin_hardware functions.

Test cases are designed to achieve graph coverage of the control flow graphs for both functions
by applying node and edge coverage to the prime paths identified in the CFGs.
"""

CHECKOUT_URL = "/api/hardware/{id}/checkout"
CHECKIN_URL = "/api/hardware/{id}/checkin"


# ----------------------------------------------------------------------------------
# checkout_hardware  — Structural (Graph Coverage) Tests (PP2, PP3, PP4, PP8, PP9)
# ----------------------------------------------------------------------------------


def test_checkout_invalid_hardware_id(client):
    """
    T-CO-01 | Prime Path PP2: N1->N2(F)->N4(T)->N5 | Nodes: N1,N2,N4,N5 | New edge: E5 (N4 True)
    Base case: valid JSON body with an unparseable hardware_id string reaches N4.
    Expected: 400 {"error": "Invalid id"}
    """
    response = client.post(
        CHECKOUT_URL.format(id="not-a-valid-id"),
        json={"projectId": "proj", "amount": 1, "userId": "user"}
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid id"


def test_checkout_hardware_not_found(client, fake_projects):
    """
    T-CO-02 | Prime Path PP3: N1->N2(F)->N4(F)->N6(T)->N7 | Nodes: N4,N6,N7 | New edge: E7 (N6 True)
    Base case: valid ObjectId with no matching hardware document in the collection.
    Expected: 404 {"error": "Hardware not found"}
    """
    from bson import ObjectId
    nonexistent_id = str(ObjectId())

    response = client.post(
        CHECKOUT_URL.format(id=nonexistent_id),
        json={"projectId": "proj", "amount": 1, "userId": "user"}
    )
    assert response.status_code == 404
    assert response.get_json()["error"] == "Hardware not found"


def test_checkout_project_not_found(client, valid_hardware):
    """
    T-CO-03 | Prime Path PP4: N1->N2(F)->N4(F)->N6(F)->N8(T)->N9 | Nodes: N6,N8,N9 | New edge: E9 (N8 True)
    Base case: hardware found but project ID does not match any document.
    Expected: 404 {"error": "Project not found"}
    """
    response = client.post(
        CHECKOUT_URL.format(id=valid_hardware),
        json={"projectId": "nonexistent-project", "amount": 1, "userId": "user"}
    )
    assert response.status_code == 404
    assert response.get_json()["error"] == "Project not found"


def test_checkout_existing_entry_increments(client, fake_hardware, fake_projects, fake_users, valid_user):
    """
    T-CO-04 | Prime Path PP8: ...->N12->N13(T)->N14->N16(F)->N18 | Nodes: N12,N13,N14,N16,N18 | New edge: E14 (N13 True->$inc)
    Base case: project already has an assignedHardware entry for this hw_id; existing amount is incremented.
    Expected: 200; available==7; assignedHardware entry amount==5 (2+3)
    """
    # Create hardware
    hw_result = fake_hardware.insert_one({
        "hardwareName": "Shared Hardware",
        "capacity": 10,
        "available": 10,
        "assignedProjects": ["test-project"]
    })
    hw_id = str(hw_result.inserted_id)

    # Project already has 2 units of this hardware checked out
    fake_projects.insert_one({
        "projectId": "test-project",
        "projectName": "Test Project",
        "description": "A test project",
        "ownerUserId": valid_user,
        "assignedUsers": [valid_user],
        "assignedHardware": [{"hardwareId": hw_id, "amount": 2}]
    })

    response = client.post(
        CHECKOUT_URL.format(id=hw_id),
        json={"projectId": "test-project", "amount": 3, "userId": valid_user}
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["available"] == 7  # 10 - 3

    # Verify the $inc path updated the existing entry
    project = fake_projects.find_one({"projectId": "test-project"})
    entry = next(e for e in project["assignedHardware"] if e["hardwareId"] == hw_id)
    assert entry["amount"] == 5  # 2 + 3


def test_checkout_post_update_fetch_fails_500(client, fake_hardware, fake_projects, fake_users, valid_user):
    """
    T-CO-05 | Prime Path PP9: ...->N12->N13(F)->N15->N16(T)->N17exit | Nodes: N15,N16,N17exit | New edge: E18 (N16 True->500)
    Base case: no prior entry ($push path); counter-based mock forces second find_one to return None (infeasible without injection).
    Expected: 500 {"error": "Failed to retrieve hardware"}
    """
    hw_result = fake_hardware.insert_one({
        "hardwareName": "Fetch-Fail Hardware",
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
        "assignedUsers": [valid_user],
        "assignedHardware": []
    })

    # Counter-based mock: first find_one succeeds, second returns None
    call_count = [0]
    original_find_one = fake_hardware.find_one

    def find_one_fail_on_second(query):
        call_count[0] += 1
        if call_count[0] >= 2:
            return None
        return original_find_one(query)

    fake_hardware.find_one = find_one_fail_on_second

    response = client.post(
        CHECKOUT_URL.format(id=hw_id),
        json={"projectId": "test-project", "amount": 1, "userId": valid_user}
    )

    assert response.status_code == 500
    assert response.get_json()["error"] == "Failed to retrieve hardware"


# ----------------------------------------------------------------------------------
# checkin_hardware — Structural (Graph Coverage) Tests (PP2–PP6, PP8, PP9)
# ----------------------------------------------------------------------------------


def test_checkin_invalid_hardware_id(client):
    """
    T-CI-01 | Prime Path PP2: N1->N2(F)->N4(T)->N5 | Nodes: N1,N2,N4,N5 | New edge: E5 (N4 True)
    Base case: valid JSON body with an unparseable hardware_id string reaches N4.
    Expected: 400 {"error": "Invalid id"}
    """
    response = client.post(
        CHECKIN_URL.format(id="bad-id"),
        json={"projectId": "proj", "amount": 1, "userId": "user"}
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid id"


def test_checkin_hardware_not_found(client):
    """
    T-CI-02 | Prime Path PP3: N1->N2(F)->N4(F)->N6(T)->N7 | Nodes: N4,N6,N7 | New edge: E7 (N6 True)
    Base case: valid ObjectId with no matching hardware document in the collection.
    Expected: 404 {"error": "Hardware not found"}
    """
    from bson import ObjectId
    response = client.post(
        CHECKIN_URL.format(id=str(ObjectId())),
        json={"projectId": "proj", "amount": 1, "userId": "user"}
    )
    assert response.status_code == 404
    assert response.get_json()["error"] == "Hardware not found"


def test_checkin_project_not_found(client, valid_hardware):
    """
    T-CI-03 | Prime Path PP4: N1->N2(F)->N4(F)->N6(F)->N8(T)->N9 | Nodes: N6,N8,N9 | New edge: E9 (N8 True)
    Base case: hardware found but project ID does not match any document.
    Expected: 404 {"error": "Project not found"}
    """
    response = client.post(
        CHECKIN_URL.format(id=valid_hardware),
        json={"projectId": "nonexistent-project", "amount": 1, "userId": "user"}
    )
    assert response.status_code == 404
    assert response.get_json()["error"] == "Project not found"


def test_checkin_unauthorized_user(client, checkin_test_data):
    """
    T-CI-04 | Prime Path PP5: ...->N8(F)->N10(T)->N10exit | Nodes: N10,N10exit | New edge: E11 (N10 True)
    Base case: hw and project exist but the requesting userId is not in assignedUsers.
    Expected: 403 {"error": "User is not assigned to this project"}
    """
    hw_id, project_id, _ = checkin_test_data

    response = client.post(
        CHECKIN_URL.format(id=hw_id),
        json={"projectId": project_id, "amount": 1, "userId": "unauthorized-user"}
    )
    assert response.status_code == 403
    assert "User is not assigned to this project" in response.get_json()["error"]


def test_checkin_hardware_not_checked_out(client, fake_hardware, fake_projects, fake_users, valid_user):
    """
    T-CI-05 | Prime Path PP6: ...->N10(F)->N11(T)->N12exit | Nodes: N11,N12exit | New edge: E13 (N11 True)
    Base case: authorized user but project's assignedHardware has no entry for this hw_id.
    Expected: 400 {"error": "This hardware is not checked out for this project"}
    """
    hw_result = fake_hardware.insert_one({
        "hardwareName": "Uncheckd Hardware",
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
        "assignedUsers": [valid_user],
        "assignedHardware": []  # No entry for this hw_id
    })

    response = client.post(
        CHECKIN_URL.format(id=hw_id),
        json={"projectId": "test-project", "amount": 1, "userId": valid_user}
    )
    assert response.status_code == 400
    assert "not checked out" in response.get_json()["error"]


def test_checkin_full_checkin_removes_entries(client, fake_hardware, fake_projects, fake_users, valid_user):
    """
    T-CI-06 | Prime Path PP9: ...->N13(F)->N14->N15(T)->N15full->N17(F)->N19 | Nodes: N14,N15,N15full,N17,N19 | New edges: E16 (N15 True->$pull), E20 (N17 False->200)
    Base case: amount equals total checked-out units; both $pull operations fire, clearing assignedHardware and assignedProjects.
    Expected: 200; available==10; assignedHardware==[]; assignedProjects==[]
    """
    hw_result = fake_hardware.insert_one({
        "hardwareName": "Full Checkin Hardware",
        "capacity": 10,
        "available": 7,
        "assignedProjects": ["test-project"]
    })
    hw_id = str(hw_result.inserted_id)

    fake_projects.insert_one({
        "projectId": "test-project",
        "projectName": "Test Project",
        "description": "A test project",
        "ownerUserId": valid_user,
        "assignedUsers": [valid_user],
        "assignedHardware": [{"hardwareId": hw_id, "amount": 3}]
    })

    response = client.post(
        CHECKIN_URL.format(id=hw_id),
        json={"projectId": "test-project", "amount": 3, "userId": valid_user}
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["available"] == 10  # min(10, 7+3)
    assert body["assignedProjects"] == []  # $pull removed the project

    project = fake_projects.find_one({"projectId": "test-project"})
    assert project["assignedHardware"] == []  # $pull removed the entry


def test_checkin_post_update_fetch_fails_500(client, fake_hardware, fake_projects, fake_users, valid_user):
    """
    T-CI-07 | Prime Path PP8: ...->N14->N15(T)->N15full->N17(T)->N18exit | Nodes: N15full,N17,N18exit | New edge: E19 (N17 True->500)
    Base case: full checkin ($pull path); counter-based mock forces final find_one to return None (infeasible without injection).
    Expected: 500 {"error": "Failed to retrieve hardware"}
    """
    hw_result = fake_hardware.insert_one({
        "hardwareName": "Fetch-Fail Checkin",
        "capacity": 10,
        "available": 7,
        "assignedProjects": ["test-project"]
    })
    hw_id = str(hw_result.inserted_id)

    fake_projects.insert_one({
        "projectId": "test-project",
        "projectName": "Test Project",
        "description": "A test project",
        "ownerUserId": valid_user,
        "assignedUsers": [valid_user],
        "assignedHardware": [{"hardwareId": hw_id, "amount": 3}]
    })

    # Counter-based: first two find_one calls succeed (hw lookup + project lookup),
    # the final hardware re-fetch returns None
    call_count = [0]
    original_find_one = fake_hardware.find_one

    def find_one_fail_on_third(query):
        call_count[0] += 1
        if call_count[0] >= 2:
            return None
        return original_find_one(query)

    fake_hardware.find_one = find_one_fail_on_third

    response = client.post(
        CHECKIN_URL.format(id=hw_id),
        json={"projectId": "test-project", "amount": 3, "userId": valid_user}
    )

    assert response.status_code == 500
    assert response.get_json()["error"] == "Failed to retrieve hardware"
