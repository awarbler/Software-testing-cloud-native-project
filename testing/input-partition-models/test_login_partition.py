"""
Partition-based test suite for login() — POST /api/auth/login
Coverage criterion: Base Choice Coverage (BCC)
IDM reference: testing/input-partition-models/login_idm.md
Base choice reference: testing/input-partition-models/login_base_choice.md

Characteristics:
  C1 — userId field value   : b1=non-empty string, b2=omitted, b3=empty string, b4=null
  C2 — password field value : b1=non-empty string, b2=omitted, b3=empty string, b4=null
  C3 — credential validity  : b1=correct match, b2=wrong password, b3=userId not found

Base choice: C1:b1, C2:b1, C3:b1
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "backend"))

import pytest
from unittest.mock import MagicMock, patch
from bson import ObjectId
from app import create_app

REGISTER_URL = "/api/auth/register"
LOGIN_URL = "/api/auth/login"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

class FakeCollection:
    def __init__(self):
        self._docs = []

    def find_one(self, query: dict):
        for doc in self._docs:
            if all(doc.get(k) == v for k, v in query.items()):
                return doc
        return None

    def insert_one(self, data: dict):
        doc = {**data, "_id": ObjectId()}
        self._docs.append(doc)
        result = MagicMock()
        result.inserted_id = doc["_id"]
        return result

    def clear(self):
        self._docs.clear()


@pytest.fixture()
def fake_users():
    col = FakeCollection()
    yield col
    col.clear()


@pytest.fixture()
def client(fake_users):
    fake_db = MagicMock()
    fake_db.__getitem__ = MagicMock(return_value=fake_users)

    def _noop_init_mongo(app):
        app.extensions["mongo_client"] = MagicMock()

    with (
        patch("app.init_mongo", side_effect=_noop_init_mongo),
        patch("app.seed_hardware"),
        patch("app.get_db", return_value=fake_db),
        patch("app.routes.auth.get_db", return_value=fake_db),
        patch("app.routes.auth.users_col", return_value=fake_users),
    ):
        flask_app = create_app()
        flask_app.config["TESTING"] = True
        flask_app.config["PROPAGATE_EXCEPTIONS"] = False
        with flask_app.test_client() as c:
            yield c


# ---------------------------------------------------------------------------
# BT — Base test (C1:b1, C2:b1, C3:b1)
# ---------------------------------------------------------------------------

def test_login_bt_valid_credentials(client):
    """BT (C1:b1, C2:b1, C3:b1): registered user with correct password returns 200."""
    client.post(REGISTER_URL, json={"userId": "carol", "password": "mypassword"})

    response = client.post(LOGIN_URL, json={"userId": "carol", "password": "mypassword"})

    assert response.status_code == 200
    body = response.get_json()
    assert body["ok"] is True
    assert body["user"]["userId"] == "carol"


# ---------------------------------------------------------------------------
# Varying C1 — userId field value
# ---------------------------------------------------------------------------

def test_login_t1_userid_omitted(client):
    """T1 (C1:b2, C2:b1, C3:b1): omitting userId is caught by the None guard."""
    response = client.post(LOGIN_URL, json={"password": "mypassword"})

    assert response.status_code == 400
    body = response.get_json()
    assert body["ok"] is False


def test_login_t2_userid_empty_string(client):
    """T2 (C1:b3, C2:b1, C3:b1): empty string userId bypasses the None guard.

    DEFECT: data.get("userId") returns "" which is not None, so the guard passes.
    The DB is queried for userId="" and finds no match, returning 401 instead of
    400. An empty string is misclassified as an invalid credential rather than a
    malformed input.
    """
    response = client.post(LOGIN_URL, json={"userId": "", "password": "mypassword"})

    assert response.status_code == 401  # actual behavior — misclassification
    body = response.get_json()
    assert body["ok"] is False


def test_login_t3_userid_null(client):
    """T3 (C1:b4, C2:b1, C3:b1): null userId is caught by the None guard.

    data.get("userId") returns None for an explicit null value, identical to a
    missing key — both collapse to None through dict.get().
    """
    response = client.post(LOGIN_URL, json={"userId": None, "password": "mypassword"})

    assert response.status_code == 400
    body = response.get_json()
    assert body["ok"] is False


# ---------------------------------------------------------------------------
# Varying C2 — password field value
# ---------------------------------------------------------------------------

def test_login_t4_password_omitted(client):
    """T4 (C1:b1, C2:b2, C3:b1): omitting password is caught by the None guard."""
    response = client.post(LOGIN_URL, json={"userId": "carol"})

    assert response.status_code == 400
    body = response.get_json()
    assert body["ok"] is False


def test_login_t5_password_empty_string(client):
    """T5 (C1:b1, C2:b3, C3:b1): empty string password bypasses the None guard.

    DEFECT: data.get("password") returns "" which is not None, so the guard passes.
    _encrypt("") returns "". The DB is queried with the encrypted empty string and
    finds no match, returning 401 instead of 400. Same misclassification as T2.
    """
    client.post(REGISTER_URL, json={"userId": "carol", "password": "mypassword"})

    response = client.post(LOGIN_URL, json={"userId": "carol", "password": ""})

    assert response.status_code == 401  # actual behavior — misclassification
    body = response.get_json()
    assert body["ok"] is False


def test_login_t6_password_null(client):
    """T6 (C1:b1, C2:b4, C3:b1): null password is caught by the None guard.

    data.get("password") returns None for an explicit null value, identical to a
    missing key — both collapse to None through dict.get().
    """
    response = client.post(LOGIN_URL, json={"userId": "carol", "password": None})

    assert response.status_code == 400
    body = response.get_json()
    assert body["ok"] is False


# ---------------------------------------------------------------------------
# Varying C3 — credential validity
# ---------------------------------------------------------------------------

def test_login_t7_wrong_password(client):
    """T7 (C1:b1, C2:b1, C3:b2): correct userId but wrong password returns 401."""
    client.post(REGISTER_URL, json={"userId": "carol", "password": "rightpass"})

    response = client.post(LOGIN_URL, json={"userId": "carol", "password": "wrongpass"})

    assert response.status_code == 401
    body = response.get_json()
    assert body["ok"] is False


def test_login_t8_userid_not_found(client):
    """T8 (C1:b1, C2:b1, C3:b3): userId that was never registered returns 401."""
    response = client.post(LOGIN_URL, json={"userId": "ghost", "password": "anypass"})

    assert response.status_code == 401
    body = response.get_json()
    assert body["ok"] is False
