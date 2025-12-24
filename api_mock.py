# api_mock.py
from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Optional

# In-memory store (reset when the Streamlit process restarts)
_RECORDS: Dict[int, Dict] = {
    1: {"id": 1, "title": "Record A", "status": "pending", "content": "Detail for Record A"},
    2: {"id": 2, "title": "Record B", "status": "pending", "content": "Detail for Record B"},
}

_AUDIT: List[Dict] = []


def fetch_records(status: Optional[str] = "pending") -> List[Dict]:
    """Return records (default: pending only)."""
    records = list(_RECORDS.values())
    if status is None:
        return records
    return [r for r in records if r["status"] == status]


def fetch_detail(record_id: int) -> Dict:
    r = _RECORDS[record_id]
    return {"id": r["id"], "title": r["title"], "status": r["status"], "content": r["content"]}


def approve_record(record_id: int, actor: str = "approver") -> bool:
    """Approve only if pending. Return True on success."""
    r = _RECORDS.get(record_id)
    if not r:
        return False
    if r["status"] != "pending":  # double-approval guard
        return False

    r["status"] = "approved"
    _AUDIT.append(
        {
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "actor": actor,
            "action": "approve",
            "record_id": record_id,
        }
    )
    return True


def fetch_audit(limit: int = 20) -> List[Dict]:
    return list(reversed(_AUDIT[-limit:]))
