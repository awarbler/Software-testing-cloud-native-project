"""
Partition-based test suite for register() — POST /api/auth/register
Coverage criterion: Base Choice Coverage (BCC)
IDM reference: testing/input-partition-models/register_idm.md
Base choice reference: testing/input-partition-models/register_base_choice.md

Characteristics:
  C1 — userId field value   : b1=non-empty string, b2=omitted, b3=empty string, b4=null
  C2 — password field value : b1=non-empty string, b2=omitted, b3=empty string, b4=null
  C3 — userId uniqueness    : b1=new user, b2=duplicate

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

def test_register_bt_valid_new_user(client):
    """BT (C1:b1, C2:b1, C3:b1): well-formed request for a new userId returns 201."""
    response = client.post(REGISTER_URL, json={"userId": "alice", "password": "secure123"})

    assert response.status_code == 201
    body = response.get_json()
    assert body["user"]["userId"] == "alice"


# ---------------------------------------------------------------------------
# Varying C1 — userId field value
# ---------------------------------------------------------------------------

def test_register_t1_userid_omitted(client):
    """T1 (C1:b2, C2:b1, C3:b1): omitting userId is caught as a missing field."""
    response = client.post(REGISTER_URL, json={"password": "secure123"})

    assert response.status_code == 400
    body = response.get_json()
    assert "userId" in body["error"]


@pytest.mark.xfail(reason="D-1: empty string userId bypasses field guard (field in data checks key presence only); returns 201 instead of 400")
def test_register_t2_userid_empty_string(client):
    """T2 (C1:b3, C2:b1, C3:b1): empty string userId should be rejected as malformed input.

    DEFECT: the field guard only checks key presence (`field in data`), not value
    validity. An empty string passes and is stored as the userId, producing 201.
    """
    response = client.post(REGISTER_URL, json={"userId": "", "password": "secure123"})

    assert response.status_code == 400


@pytest.mark.xfail(reason="D-2: null userId bypasses field guard (field in data checks key presence only); null stored in DB, returns 201 instead of 400")
def test_register_t3_userid_null(client):
    """T3 (C1:b4, C2:b1, C3:b1): null userId should be rejected as malformed input.

    DEFECT: the field guard only checks key presence. A null value passes and
    is stored as None in the DB, producing 201.
    """
    response = client.post(REGISTER_URL, json={"userId": None, "password": "secure123"})

    assert response.status_code == 400


# ---------------------------------------------------------------------------
# Varying C2 — password field value
# ---------------------------------------------------------------------------

def test_register_t4_password_omitted(client):
    """T4 (C1:b1, C2:b2, C3:b1): omitting password is caught as a missing field."""
    response = client.post(REGISTER_URL, json={"userId": "alice"})

    assert response.status_code == 400
    body = response.get_json()
    assert "password" in body["error"]


@pytest.mark.xfail(reason="D-3: empty string password bypasses field guard; _encrypt('') stored as password, returns 201 instead of 400")
def test_register_t5_password_empty_string(client):
    """T5 (C1:b1, C2:b3, C3:b1): empty string password should be rejected as malformed input.

    DEFECT: the field guard only checks key presence. An empty string passes,
    _encrypt("") returns "", and the user is stored with an empty password,
    producing 201.
    """
    response = client.post(REGISTER_URL, json={"userId": "alice", "password": ""})

    assert response.status_code == 400


@pytest.mark.xfail(reason="D-4: null password bypasses field guard; _encrypt(None) calls None.isascii() raising AttributeError; returns 500 crash instead of 400")
def test_register_t6_password_null(client):
    """T6 (C1:b1, C2:b4, C3:b1): null password should be rejected as malformed input.

    DEFECT: the field guard only checks key presence. A null value passes to
    _encrypt(None), which calls None.isascii() and raises AttributeError, crashing
    with 500.
    """
    response = client.post(REGISTER_URL, json={"userId": "alice", "password": None})

    assert response.status_code == 400


# ---------------------------------------------------------------------------
# Varying C3 — userId uniqueness
# ---------------------------------------------------------------------------

def test_register_t7_duplicate_userid(client):
    """T7 (C1:b1, C2:b1, C3:b2): registering an existing userId returns 409."""
    client.post(REGISTER_URL, json={"userId": "alice", "password": "secure123"})

    response = client.post(REGISTER_URL, json={"userId": "alice", "password": "secure123"})

    assert response.status_code == 409
    body = response.get_json()
    assert "already exists" in body["error"]
