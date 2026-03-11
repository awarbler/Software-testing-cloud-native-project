"""
Tests for POST /api/auth/register and POST /api/auth/login.

Coverage template per endpoint:
  - 1 happy path
  - 1 common invalid input
  - 1 missing/unauthorized case
  - 1 boundary/duplicate-request case (stateful)
"""

REGISTER_URL = "/api/auth/register"
LOGIN_URL = "/api/auth/login"


# ---------------------------------------------------------------------------
# register()
# ---------------------------------------------------------------------------


def test_register_valid_user_returns_201(client):
    """Happy path: new user with valid credentials is created."""
    response = client.post(REGISTER_URL, json={"userId": "alice", "password": "secure123"})

    assert response.status_code == 201
    body = response.get_json()
    assert body["user"]["userId"] == "alice"


def test_register_missing_required_field_returns_400(client):
    """Invalid input: required field 'password' is absent."""
    response = client.post(REGISTER_URL, json={"userId": "alice"})

    assert response.status_code == 400
    body = response.get_json()
    assert "password" in body["error"]


def test_register_empty_body_returns_400(client):
    """Missing input: an empty JSON object is not a valid registration payload."""
    response = client.post(REGISTER_URL, json={})

    assert response.status_code == 400
    body = response.get_json()
    assert "error" in body


def test_register_duplicate_userId_returns_409(client):
    """Boundary/stateful: registering the same userId a second time is rejected."""
    payload = {"userId": "bob", "password": "pass1"}
    first = client.post(REGISTER_URL, json=payload)
    assert first.status_code == 201

    second = client.post(REGISTER_URL, json=payload)

    assert second.status_code == 409
    body = second.get_json()
    assert "already exists" in body["error"]


# ---------------------------------------------------------------------------
# login()
# ---------------------------------------------------------------------------


def test_login_valid_credentials_returns_200(client):
    """Happy path: registered user logs in with the correct password."""
    client.post(REGISTER_URL, json={"userId": "carol", "password": "mypassword"})

    response = client.post(LOGIN_URL, json={"userId": "carol", "password": "mypassword"})

    assert response.status_code == 200
    body = response.get_json()
    assert body["ok"] is True
    assert body["user"]["userId"] == "carol"


def test_login_wrong_password_returns_401(client):
    """Unauthorized: correct userId but wrong password is rejected."""
    client.post(REGISTER_URL, json={"userId": "dave", "password": "rightpass"})

    response = client.post(LOGIN_URL, json={"userId": "dave", "password": "wrongpass"})

    assert response.status_code == 401
    body = response.get_json()
    assert body["ok"] is False


def test_login_missing_password_field_returns_400(client):
    """Invalid input: 'password' field is omitted from the login request."""
    response = client.post(LOGIN_URL, json={"userId": "eve"})

    assert response.status_code == 400
    body = response.get_json()
    assert body["ok"] is False


def test_login_nonexistent_user_returns_401(client):
    """Unauthorized: userId was never registered."""
    response = client.post(LOGIN_URL, json={"userId": "ghost", "password": "anypass"})

    assert response.status_code == 401
    body = response.get_json()
    assert body["ok"] is False
