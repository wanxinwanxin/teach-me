"""Tiny SQLite store for the hosted instance: users and jobs.

The BYO API key is NEVER stored. It lives in process memory for the
duration of the job only.
"""

from __future__ import annotations

import sqlite3
import threading
import time
import uuid
from pathlib import Path

_lock = threading.Lock()


class Db:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        with _lock:
            self.conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    email TEXT PRIMARY KEY,
                    name TEXT,
                    trial_used INTEGER DEFAULT 0,
                    created REAL
                );
                CREATE TABLE IF NOT EXISTS jobs (
                    id TEXT PRIMARY KEY,
                    email TEXT,
                    topic TEXT,
                    status TEXT,          -- queued | running | done | failed
                    used_shared_key INTEGER DEFAULT 0,
                    error TEXT DEFAULT '',
                    created REAL
                );
                """
            )
            self.conn.commit()

    def upsert_user(self, email: str, name: str) -> None:
        with _lock:
            self.conn.execute(
                "INSERT INTO users(email, name, created) VALUES(?,?,?) "
                "ON CONFLICT(email) DO UPDATE SET name=excluded.name",
                (email, name, time.time()),
            )
            self.conn.commit()

    def trial_used(self, email: str) -> bool:
        row = self.conn.execute(
            "SELECT trial_used FROM users WHERE email=?", (email,)
        ).fetchone()
        return bool(row and row["trial_used"])

    def mark_trial_used(self, email: str) -> None:
        with _lock:
            self.conn.execute(
                "UPDATE users SET trial_used=1 WHERE email=?", (email,)
            )
            self.conn.commit()

    def create_job(self, email: str, topic: str, used_shared_key: bool) -> str:
        job_id = uuid.uuid4().hex[:12]
        with _lock:
            self.conn.execute(
                "INSERT INTO jobs(id, email, topic, status, used_shared_key, created) "
                "VALUES(?,?,?,?,?,?)",
                (job_id, email, topic, "queued", int(used_shared_key), time.time()),
            )
            self.conn.commit()
        return job_id

    def set_status(self, job_id: str, status: str, error: str = "") -> None:
        with _lock:
            self.conn.execute(
                "UPDATE jobs SET status=?, error=? WHERE id=?",
                (status, error, job_id),
            )
            self.conn.commit()

    def get_job(self, job_id: str) -> sqlite3.Row | None:
        return self.conn.execute(
            "SELECT * FROM jobs WHERE id=?", (job_id,)
        ).fetchone()

    def jobs_for(self, email: str) -> list[sqlite3.Row]:
        return self.conn.execute(
            "SELECT * FROM jobs WHERE email=? ORDER BY created DESC", (email,)
        ).fetchall()

    def queue_position(self, job_id: str) -> int:
        row = self.conn.execute(
            "SELECT COUNT(*) AS n FROM jobs WHERE status='queued' AND created < "
            "(SELECT created FROM jobs WHERE id=?)",
            (job_id,),
        ).fetchone()
        return int(row["n"]) if row else 0
