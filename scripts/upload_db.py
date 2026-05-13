"""رفع quran.db إلى Hugging Face Datasets.

الاستخدام:
    export HF_TOKEN=hf_xxx
    uv run python scripts/upload_db.py
"""
import hashlib
import os
import sys
from pathlib import Path

from huggingface_hub import HfApi, login

DB_PATH = Path("data/quran.db")
REPO_ID = "tafsircenter/tafsir-mcp-data"


def compute_sha256(path: Path, chunk_size: int = 65536) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if not DB_PATH.exists():
        print(f"❌ القاعدة غير موجودة: {DB_PATH}", file=sys.stderr)
        return 1

    token = os.environ.get("HF_TOKEN")
    if not token:
        print("❌ ضع التوكن: export HF_TOKEN=hf_xxx", file=sys.stderr)
        return 1

    size_mb = DB_PATH.stat().st_size / (1024 * 1024)
    print(f"📦 الحجم: {size_mb:.1f} MB")

    print("🔒 حساب SHA256...")
    sha256 = compute_sha256(DB_PATH)
    print(f"   SHA256: {sha256}")

    print("🔐 تسجيل دخول Hugging Face...")
    login(token=token, add_to_git_credential=False)

    print(f"⬆️  رفع إلى {REPO_ID}...")
    api = HfApi()
    api.upload_file(
        path_or_fileobj=str(DB_PATH),
        path_in_repo="quran.db",
        repo_id=REPO_ID,
        repo_type="dataset",
        commit_message="feat: initial upload — Tafsir MCP Quranic database v1.0",
    )

    print()
    print("✅ تم الرفع بنجاح!")
    print(f"🔗 https://huggingface.co/datasets/{REPO_ID}")
    print()
    print("📝 احفظ هذه القيمة لتحديث data_loader.py:")
    print(f'   DB_SHA256 = "{sha256}"')

    Path("scripts/.db_sha256").write_text(sha256)
    print("   (محفوظة مؤقتاً في scripts/.db_sha256)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
