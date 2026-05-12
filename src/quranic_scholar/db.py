"""SQLite read-only connection management for data/quran.db."""

import os
import sqlite3
from pathlib import Path

DEFAULT_DB_PATH: str = os.environ.get("QURAN_DB_PATH", "data/quran.db")


class QuranDataError(Exception):
    """يُرفع عند خطأ في قاعدة بيانات القرآن."""


def get_connection(path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    if not Path(path).exists():
        raise FileNotFoundError(f"ملف قاعدة البيانات غير موجود: {path}")
    uri = f"file:{path}?mode=ro"
    conn = sqlite3.connect(uri, uri=True, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA query_only = ON")
    return conn


def query_one(sql: str, params: tuple = ()) -> dict | None:
    conn = get_connection()
    try:
        row = conn.execute(sql, params).fetchone()
        return dict(row) if row is not None else None
    except sqlite3.DatabaseError as exc:
        raise QuranDataError(f"خطأ في الاستعلام عن قاعدة البيانات: {exc}") from exc
    finally:
        conn.close()


def query_all(sql: str, params: tuple = ()) -> list[dict]:
    conn = get_connection()
    try:
        rows = conn.execute(sql, params).fetchall()
        return [dict(row) for row in rows]
    except sqlite3.DatabaseError as exc:
        raise QuranDataError(f"خطأ في الاستعلام عن قاعدة البيانات: {exc}") from exc
    finally:
        conn.close()
