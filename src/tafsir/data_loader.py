"""Database path resolver with automatic download from Hugging Face Datasets."""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path
from urllib.request import urlretrieve

DB_URL = (
    "https://huggingface.co/datasets/tafsircenter/tafsir-mcp-data"
    "/resolve/main/quran.db"
)
DB_SHA256 = "10e61f615ab5e6a3440e8ecc8ba1dc2273d12cd9048752760fe53a44d191cc27"
DB_SIZE_MB = 214


def _verify_sha256(path: Path) -> None:
    """تحقق من سلامة الملف بعد التحميل."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    actual = h.hexdigest()
    if actual != DB_SHA256:
        path.unlink()
        raise RuntimeError(
            f"تعارض في SHA256 لقاعدة البيانات المحمّلة!\n"
            f"  متوقع: {DB_SHA256}\n"
            f"  فعلي:  {actual}\n"
            f"المرجو إعادة المحاولة أو الإبلاغ عن المشكلة."
        )


def get_db_path() -> Path:
    """Return the database path, downloading on first production run if needed.

    Priority:
    1. TAFSIR_DB_PATH env var (developer override)
    2. data/quran.db next to the project root (development)
    3. ~/.cache/tafsir-mcp/quran.db (production install — auto-download)
    """
    if env_path := os.environ.get("TAFSIR_DB_PATH"):
        path = Path(env_path)
        if path.exists():
            return path
        raise FileNotFoundError(
            f"TAFSIR_DB_PATH is set to '{env_path}' but the file does not exist."
        )

    local = Path(__file__).parent.parent.parent / "data" / "quran.db"
    if local.exists():
        return local

    cache_dir = Path.home() / ".cache" / "tafsir-mcp"
    cache_db = cache_dir / "quran.db"

    if not cache_db.exists():
        print(
            f"📥 Downloading Tafsir database ({DB_SIZE_MB} MB) — first run only...",
            file=sys.stderr,
        )
        cache_dir.mkdir(parents=True, exist_ok=True)
        try:
            urlretrieve(DB_URL, cache_db)
        except Exception as exc:
            cache_db.unlink(missing_ok=True)
            raise RuntimeError(
                f"Failed to download database from {DB_URL}: {exc}\n"
                "Set TAFSIR_DB_PATH to point to a local quran.db file."
            ) from exc

        _verify_sha256(cache_db)
        print(f"✅ Database saved to {cache_db}", file=sys.stderr)

    return cache_db
