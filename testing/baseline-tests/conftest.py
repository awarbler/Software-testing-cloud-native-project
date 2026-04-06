import sys
import os

# Ensure the backend package root is on the path when running pytest from any directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "backend"))

import pytest
from unittest.mock import MagicMock, patch
from bson import ObjectId

from app import create_app


class FakeCollection:
    """In-memory pymongo Collection replacement used across auth tests."""

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
    """Flask test client with MongoDB replaced by an in-memory FakeCollection."""
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
