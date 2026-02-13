"""Hardware management routes."""

from __future__ import annotations

from flask import Blueprint, jsonify, request
from pymongo import ReturnDocument
from pymongo.collection import Collection

from app.db import get_db
from app.mongo_utils import serialize_doc

bp = Blueprint("hardware", __name__)

DEFAULT_HARDWARE_SETS = [
    {
        "hardwareSetId": "HWSet1",
        "name": "HW Set 1",
        "capacity": 100,
        "available": 100,
    },
    {
        "hardwareSetId": "HWSet2",
        "name": "HW Set 2",
        "capacity": 100,
        "available": 100,
    },
]


def hardware_sets_col() -> Collection:
    return get_db()["Hardware_sets"]


def ensure_seeded() -> None:
    col = hardware_sets_col()
    for template in DEFAULT_HARDWARE_SETS:
        col.update_one(
            {"hardwareSetId": template["hardwareSetId"]},
            {"$setOnInsert": template},
            upsert=True,
        )


def _extract_units(data: dict) -> int | None:
    units = data.get("units")
    if units is None:
        return None
    if isinstance(units, int):
        return units
    try:
        return int(units)
    except (TypeError, ValueError):
        return None


@bp.get("")
def list_hardware_sets():
    ensure_seeded()
    docs = list(hardware_sets_col().find({}))
    return jsonify([serialize_doc(doc) for doc in docs])


@bp.post("/checkOut")
def checkout_units():
    data = request.get_json(silent=True) or {}
    hardware_set_id = data.get("hardwareSetId")
    units = _extract_units(data)

    if not hardware_set_id or not isinstance(hardware_set_id, str):
        return jsonify({"error": "Missing or invalid hardwareSetId"}), 400
    if units is None or units < 1:
        return jsonify({"error": "units must be a positive integer"}), 400

    filter_query = {"hardwareSetId": hardware_set_id.strip(), "available": {"$gte": units}}
    updated = hardware_sets_col().find_one_and_update(
        filter_query,
        {"$inc": {"available": -units}},
        return_document=ReturnDocument.AFTER,
    )

    if not updated:
        existing = hardware_sets_col().find_one({"hardwareSetId": hardware_set_id.strip()})
        if not existing:
            return jsonify({"error": "Hardware set not found"}), 404
        return (
            jsonify({"error": "Insufficient units available", "available": existing.get("available")}),
            409,
        )

    return jsonify(serialize_doc(updated))


@bp.post("/checkIn")
def checkin_units():
    data = request.get_json(silent=True) or {}
    hardware_set_id = data.get("hardwareSetId")
    units = _extract_units(data)

    if not hardware_set_id or not isinstance(hardware_set_id, str):
        return jsonify({"error": "Missing or invalid hardwareSetId"}), 400
    if units is None or units < 1:
        return jsonify({"error": "units must be a positive integer"}), 400

    filter_query = {
        "hardwareSetId": hardware_set_id.strip(),
        "$expr": {
            "$lte": ["$available", {"$subtract": ["$capacity", units]}],
        },
    }
    updated = hardware_sets_col().find_one_and_update(
        filter_query,
        {"$inc": {"available": units}},
        return_document=ReturnDocument.AFTER,
    )

    if not updated:
        existing = hardware_sets_col().find_one({"hardwareSetId": hardware_set_id.strip()})
        if not existing:
            return jsonify({"error": "Hardware set not found"}), 404
        return (
            jsonify({"error": "Check-in would exceed capacity", "available": existing.get("available")} ),
            409,
        )

    return jsonify(serialize_doc(updated))
