import sys
import os

# Ensure the backend package root is on the path when running pytest from any directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "backend"))

import pytest
from unittest.mock import MagicMock, patch
from bson import ObjectId

from app import create_app


class FakeCollection:
    """In-memory pymongo Collection replacement for testing auth and hardware operations."""

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

    def update_one(self, query: dict, update: dict):
        """Update first matching document with $set, $inc, $addToSet, $pull, $push operators."""
        for doc in self._docs:
            if not self._matches_query(doc, query):
                continue
            self._apply_updates(doc, update, query)
            result = MagicMock()
            result.matched_count = 1
            return result
        result = MagicMock()
        result.matched_count = 0
        return result

    def _matches_query(self, doc: dict, query: dict) -> bool:
        """Check if document matches all query conditions (supports nested queries)."""
        for q_key, q_value in query.items():
            if "." in q_key:
                if not self._matches_nested_query(doc, q_key, q_value):
                    return False
            else:
                if doc.get(q_key) != q_value:
                    return False
        return True

    def _matches_nested_query(self, doc: dict, q_key: str, q_value) -> bool:
        """Check if document matches a nested query like 'assignedHardware.hardwareId'."""
        parts = q_key.split(".")
        current = doc
        for part in parts:
            if isinstance(current, list):
                for item in current:
                    if item.get(part) == q_value:
                        return True
                return False
            elif part in current:
                current = current[part]
            else:
                return False
        return current == q_value

    def _apply_updates(self, doc: dict, update: dict, query: dict) -> None:
        """Apply MongoDB-style update operators to a document."""
        if "$set" in update:
            doc.update(update["$set"])
        if "$inc" in update:
            for key, value in update["$inc"].items():
                if "." in key:
                    self._increment_nested(doc, key, value, query)
                else:
                    doc[key] = doc.get(key, 0) + value
        if "$addToSet" in update:
            for key, value in update["$addToSet"].items():
                if key not in doc:
                    doc[key] = []
                if isinstance(value, list):
                    doc[key].extend(value)
                elif value not in doc[key]:
                    doc[key].append(value)
        if "$pull" in update:
            for key, value in update["$pull"].items():
                if key in doc and value in doc[key]:
                    doc[key].remove(value)
        if "$push" in update:
            for key, value in update["$push"].items():
                if key not in doc:
                    doc[key] = []
                doc[key].append(value)

    def _increment_nested(self, doc: dict, key: str, value: int, query: dict) -> None:
        """Handle positional increment like 'assignedHardware.$.amount'."""
        parts = key.split(".")
        if parts[1] == "$":
            # Positional operator: find and increment matching array element
            array_key = parts[0]
            field_key = parts[2]
            query_key = f"{array_key}.hardwareId"
            if array_key in doc and isinstance(doc[array_key], list) and query_key in query:
                hw_id = query[query_key]
                for item in doc[array_key]:
                    if item.get("hardwareId") == hw_id:
                        item[field_key] = item.get(field_key, 0) + value
                        break
        else:
            # Regular nested key
            current = doc
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = current.get(parts[-1], 0) + value

    def update_many(self, query: dict, update: dict):
        """Update all matching documents."""
        count = 0
        for doc in self._docs:
            if self._matches_query(doc, query):
                self._apply_updates(doc, update, query)
                count += 1
        result = MagicMock()
        result.matched_count = count
        return result

    def clear(self):
        """Clear all documents from the collection."""
        self._docs.clear()


class FakeDB:
    """Mock MongoDB database that routes collection requests to FakeCollections."""

    def __init__(self, collections: dict[str, FakeCollection]):
        self._collections = collections

    def __getitem__(self, key: str) -> FakeCollection:
        """Return the FakeCollection for the given collection name."""
        return self._collections[key]


# ============================================================================
# Base Fixtures: Raw collections for fine-grained test control
# ============================================================================


@pytest.fixture()
def fake_users():
    col = FakeCollection()
    yield col
    col.clear()


@pytest.fixture()
def fake_hardware():
    col = FakeCollection()
    yield col
    col.clear()


@pytest.fixture()
def fake_projects():
    col = FakeCollection()
    yield col
    col.clear()


# ============================================================================
# Flask Client Fixture: Mocks MongoDB for API testing
# ============================================================================


@pytest.fixture()
def client(fake_users, fake_hardware, fake_projects):
    """Flask test client with MongoDB replaced by in-memory FakeCollections."""
    fake_db = FakeDB({
        "users": fake_users,
        "hardware": fake_hardware,
        "projects": fake_projects,
    })

    def _noop_init_mongo(app):
        app.extensions["mongo_client"] = MagicMock()

    with (
        patch("app.init_mongo", side_effect=_noop_init_mongo),
        patch("app.seed_hardware"),
        patch("app.get_db", return_value=fake_db),
        # Auth routes
        patch("app.routes.auth.get_db", return_value=fake_db),
        patch("app.routes.auth.users_col", return_value=fake_users),
        # Hardware routes
        patch("app.routes.hardware.get_db", return_value=fake_db),
        patch("app.routes.hardware.hardware_col", return_value=fake_hardware),
        patch("app.routes.hardware.projects_col", return_value=fake_projects),
        # Projects routes
        patch("app.routes.projects.get_db", return_value=fake_db),
        patch("app.routes.projects.hardware_col", return_value=fake_hardware),
        patch("app.routes.projects.projects_col", return_value=fake_projects),
        # Users routes
        patch("app.routes.users.get_db", return_value=fake_db),
        patch("app.routes.users.users_col", return_value=fake_users),
    ):
        flask_app = create_app()
        flask_app.config["TESTING"] = True
        flask_app.config["PROPAGATE_EXCEPTIONS"] = False
        with flask_app.test_client() as c:
            yield c


# ============================================================================
# Hardware Test Fixtures: Pre-configured data for checkout/checkin tests
# ============================================================================


@pytest.fixture()
def valid_user(fake_users):
    """Fixture: Create a valid test user and return the user ID."""
    result = fake_users.insert_one({"userId": "test-user", "password": "test-password"})
    return "test-user"


@pytest.fixture()
def valid_hardware(fake_hardware):
    """Fixture: Create a valid hardware item with capacity=10 and return the hardware ID."""
    result = fake_hardware.insert_one({
        "hardwareName": "Test Hardware",
        "capacity": 10,
        "available": 10,
        "assignedProjects": []
    })
    return str(result.inserted_id)


@pytest.fixture()
def valid_project(fake_projects, valid_user):
    """Fixture: Create a valid project with the test user and return the project ID."""
    fake_projects.insert_one({
        "projectId": "test-project",
        "projectName": "Test Project",
        "description": "A test project",
        "ownerUserId": valid_user,
        "assignedUsers": [valid_user],
        "assignedHardware": []
    })
    return "test-project"


@pytest.fixture()
def checkout_test_data(fake_hardware, fake_projects, fake_users, valid_user, valid_project, valid_hardware):
    """Fixture: Set up complete data for checkout tests (hardware, project, user).
    
    Returns:
        tuple: (hardware_id, project_id, user_id)
    """
    return (valid_hardware, valid_project, valid_user)


@pytest.fixture()
def limited_hardware(fake_hardware):
    """Fixture: Create hardware with limited availability (5 units) for testing constraints."""
    result = fake_hardware.insert_one({
        "hardwareName": "Limited Hardware",
        "capacity": 10,
        "available": 5,
        "assignedProjects": []
    })
    return str(result.inserted_id)


@pytest.fixture()
def checkin_test_data(fake_hardware, fake_projects, fake_users, valid_user):
    """Fixture: Set up data for checkin tests (hardware with items checked out, project tracking them).
    
    Returns:
        tuple: (hardware_id, project_id, user_id)
    """
    # Create hardware with 7 available (3 checked out)
    hw_result = fake_hardware.insert_one({
        "hardwareName": "Checked Out Hardware",
        "capacity": 10,
        "available": 7,
        "assignedProjects": ["test-project"]
    })
    hw_id = str(hw_result.inserted_id)
    
    # Create project with tracked hardware
    fake_projects.insert_one({
        "projectId": "test-project",
        "projectName": "Test Project",
        "description": "A test project",
        "ownerUserId": valid_user,
        "assignedUsers": [valid_user],
        "assignedHardware": [{"hardwareId": hw_id, "amount": 3}]
    })
    
    return (hw_id, "test-project", valid_user)
