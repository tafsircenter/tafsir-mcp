"""SQLite read-only connection management for quran.db."""

import sqlite3
from pathlib import Path

from tafsir.data_loader import get_db_path

# Tafsir tables use (sura, aya); all other tables use (surahNo, ayahNo)
TAFSIR_KEYS = ("sura", "aya")
STANDARD_KEYS = ("surahNo", "ayahNo")


class QuranDataError(Exception):
    """يُرفع عند خطأ في قاعدة بيانات القرآن."""


def get_connection(path: Path | None = None) -> sqlite3.Connection:
    db_path = path or get_db_path()
    if not db_path.exists():
        raise FileNotFoundError(f"ملف قاعدة البيانات غير موجود: {db_path}")
    uri = f"file:{db_path}?mode=ro"
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
