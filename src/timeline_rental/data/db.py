"""SQLite persistence for collapsed timelines."""

from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[3]


def saves_dir() -> Path:
    path = Path(os.getenv("SAVES_DIR", PROJECT_ROOT / "saves"))
    path.mkdir(parents=True, exist_ok=True)
    return path


def db_path() -> Path:
    return saves_dir() / "timelines.db"


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                tape TEXT NOT NULL,
                choice_history TEXT NOT NULL,
                outcome_index INTEGER NOT NULL,
                measured_bitstring TEXT NOT NULL,
                narration TEXT NOT NULL,
                receipt_line TEXT NOT NULL,
                lost_timelines TEXT NOT NULL,
                photo_label TEXT NOT NULL,
                clerk_fragment TEXT NOT NULL DEFAULT '',
                ending_title TEXT NOT NULL DEFAULT ''
            )
            """
        )
        for col, typedef in (
            ("clerk_fragment", "TEXT NOT NULL DEFAULT ''"),
            ("ending_title", "TEXT NOT NULL DEFAULT ''"),
        ):
            try:
                conn.execute(f"ALTER TABLE runs ADD COLUMN {col} {typedef}")
            except sqlite3.OperationalError:
                pass
        conn.commit()


def save_run(record: dict[str, Any]) -> int:
    init_db()
    with connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO runs (
                created_at, tape, choice_history, outcome_index,
                measured_bitstring, narration, receipt_line, lost_timelines,
                photo_label, clerk_fragment, ending_title
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                record["tape"],
                json.dumps(record["choice_history"]),
                record["outcome_index"],
                record["measured_bitstring"],
                record["narration"],
                record["receipt_line"],
                json.dumps(record["lost_timelines"]),
                record["photo_label"],
                record.get("clerk_fragment", ""),
                record.get("ending_title", ""),
            ),
        )
        conn.commit()
        return int(cur.lastrowid)


def latest_run() -> dict[str, Any] | None:
    init_db()
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM runs ORDER BY id DESC LIMIT 1"
        ).fetchone()
    if row is None:
        return None
    return _row_to_dict(row)


def get_run(run_id: int) -> dict[str, Any] | None:
    init_db()
    with connect() as conn:
        row = conn.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone()
    if row is None:
        return None
    return _row_to_dict(row)


def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "created_at": row["created_at"],
        "tape": row["tape"],
        "choice_history": json.loads(row["choice_history"]),
        "outcome_index": row["outcome_index"],
        "measured_bitstring": row["measured_bitstring"],
        "narration": row["narration"],
        "receipt_line": row["receipt_line"],
        "lost_timelines": json.loads(row["lost_timelines"]),
        "photo_label": row["photo_label"],
        "clerk_fragment": row["clerk_fragment"] if "clerk_fragment" in row.keys() else "",
        "ending_title": row["ending_title"] if "ending_title" in row.keys() else "",
    }


def list_runs(limit: int = 10) -> list[dict[str, Any]]:
    init_db()
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT id, created_at, tape, receipt_line, outcome_index,
                   measured_bitstring, photo_label, clerk_fragment
            FROM runs ORDER BY id DESC LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def run_count() -> int:
    init_db()
    with connect() as conn:
        row = conn.execute("SELECT COUNT(*) AS c FROM runs").fetchone()
    return int(row["c"]) if row else 0
