"""Qira'at (recitation variants) MCP tools."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from tafsir.db import query_all, query_one
from tafsir.models import AyahReference

_ANNOTATIONS = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
)

_NO_VARIANT_PREFIX = "لا خلاف بين القراء"
_FORMAT_NOTE = (
    "تنسيق القراءات: @اسم القارئ أو مجموعة القراء/نص القراءة@. "
    "يحتاج تفسير من قارئ مختص. "
    "كل مقطع بين @ يمثل رواية واحدة."
)


def compare_qeraat(
    surah: int,
    ayah: int,
    word_no: int | None = None,
) -> dict:
    """قراءات الكلمات المختلف فيها في آية معينة.

    surah, ayah: الآية المطلوبة.
    word_no: رقم الكلمة (اختياري). إذا لم يُحدَّد، تُرجع كل الكلمات ذات الخلاف.
    البيانات خام بتنسيق @قارئ/قراءة@ — لا يُحلَّل برمجياً.
    """
    ref = AyahReference(surah=surah, ayah=ayah)

    if word_no is not None:
        rows = query_all(
            "SELECT wordNo, content, note FROM qeraat_info"
            " WHERE surahNo = ? AND ayahNo = ? AND wordNo = ?"
            " ORDER BY wordNo",
            (ref.surah, ref.ayah, word_no),
        )
        # Fetch word text for context
        word_row = query_one(
            "SELECT word FROM word_content_rasm"
            " WHERE surahNo = ? AND ayahNo = ? AND wordNo = ?",
            (ref.surah, ref.ayah, word_no),
        )
        word_text = word_row["word"] if word_row else None
    else:
        # Only return words that actually have qira'at differences
        rows = query_all(
            "SELECT q.wordNo, q.content, q.note, r.word"
            " FROM qeraat_info q"
            " JOIN word_content_rasm r"
            "   ON r.surahNo=q.surahNo AND r.ayahNo=q.ayahNo AND r.wordNo=q.wordNo"
            " WHERE q.surahNo = ? AND q.ayahNo = ?"
            "   AND q.content LIKE '@%'"
            " ORDER BY q.wordNo",
            (ref.surah, ref.ayah),
        )
        word_text = None

    entries = []
    for r in rows:
        # Skip "no difference" entries when filtering by variant content
        if r["content"].startswith(_NO_VARIANT_PREFIX):
            continue
        entry = {
            "word_no": r["wordNo"],
            "qeraat_raw": r["content"],
        }
        if r.get("note"):
            entry["note"] = r["note"]
        # Include word text if available in row (from join query) or from separate lookup
        w = r.get("word") or (word_text if word_no is not None else None)
        if w:
            entry["word"] = w
        entries.append(entry)

    return {
        "surah": ref.surah,
        "ayah": ref.ayah,
        "word_no_filter": word_no,
        "qeraat_entries": entries,
        "has_variants": len(entries) > 0,
        "format_note": _FORMAT_NOTE,
    }


def register(mcp: FastMCP) -> None:
    mcp.tool(name="get_qeraat_variants", annotations=_ANNOTATIONS)(compare_qeraat)
