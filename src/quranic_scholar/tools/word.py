"""Word-level MCP tools: analyze_word, find_root_occurrences, get_root_stats."""

from __future__ import annotations

from typing import Annotated

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from quranic_scholar.db import query_all, query_one
from quranic_scholar.models import AyahReference, WordAnalysis

_ANNOTATIONS = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
)

_DEFAULT_ASPECTS = ("meaning", "irab", "sarf")


def get_word_analysis(
    surah: int,
    ayah: int,
    word_no: Annotated[int, Field(ge=1, description="رقم الكلمة في الآية (يبدأ من 1)")],
    aspects: list[str] | None = None,
) -> dict:
    """تحليل كلمة قرآنية على مستوى: المعنى، الإعراب، الصرف، الإحصاء، القراءات.

    aspects: قائمة اختيارية من ['meaning','irab','sarf','statistics','qeraat']
    default: ['meaning','irab','sarf']
    """
    ref = AyahReference(surah=surah, ayah=ayah)
    active = set(aspects or _DEFAULT_ASPECTS)

    row = query_one(
        "SELECT r.word, r.rasm,"
        "       m.meaning,"
        "       i.irabMushakkal,"
        "       s.sarf,"
        "       ws.root, ws.repeatitionCount, ws.rootRepeatitionCount"
        " FROM word_content_rasm r"
        " LEFT JOIN word_content_meaning m"
        "   ON m.surahNo=r.surahNo AND m.ayahNo=r.ayahNo AND m.wordNo=r.wordNo"
        " LEFT JOIN word_content_irab i"
        "   ON i.surahNo=r.surahNo AND i.ayahNo=r.ayahNo AND i.wordNo=r.wordNo"
        " LEFT JOIN word_content_sarf s"
        "   ON s.surahNo=r.surahNo AND s.ayahNo=r.ayahNo AND s.wordNo=r.wordNo"
        " LEFT JOIN word_statistics ws"
        "   ON ws.surahNo=r.surahNo AND ws.ayahNo=r.ayahNo AND ws.wordNo=r.wordNo"
        " WHERE r.surahNo = ? AND r.ayahNo = ? AND r.wordNo = ?",
        (ref.surah, ref.ayah, word_no),
    )

    if not row:
        return {
            "error": f"لم تُوجد الكلمة رقم {word_no} في الآية {surah}:{ayah}",
            "surah": surah, "ayah": ayah, "word_no": word_no,
        }

    # rasm note: DB stores '-' when there is no note
    rasm_note = row["rasm"] if row["rasm"] and row["rasm"] != "-" else None

    result = WordAnalysis(
        word_no=word_no,
        word=row["word"],
        meaning=row["meaning"] if "meaning" in active else None,
        irab=row["irabMushakkal"] if "irab" in active else None,
        sarf=row["sarf"] if "sarf" in active else None,
        root=row["root"] if "statistics" in active else None,
        # DB has typo 'repeatitionCount' — exposed as clean field 'frequency'
        frequency=row["repeatitionCount"] if "statistics" in active else None,
    ).model_dump()

    if rasm_note:
        result["rasm_note"] = rasm_note

    if "statistics" in active and row["rootRepeatitionCount"] is not None:
        result["root_repetition_count"] = row["rootRepeatitionCount"]

    if "qeraat" in active:
        qeraat_rows = query_all(
            "SELECT content, note FROM qeraat_info"
            " WHERE surahNo = ? AND ayahNo = ? AND wordNo = ?",
            (ref.surah, ref.ayah, word_no),
        )
        result["qeraat"] = [
            {"content": r["content"], "note": r["note"]}
            for r in qeraat_rows
        ]

    return result


def search_by_root(
    root: str,
    limit: Annotated[int, Field(ge=1, le=500)] = 50,
) -> list[dict]:
    """جلب كل مواضع ورود جذر معين في القرآن.

    root: الجذر الثلاثي أو الرباعي (مثال: 'رحم', 'كتب', 'علم')
    limit: الحد الأقصى للنتائج (افتراضي 50، أقصاه 500)
    يُرجع قائمة بالسورة والآية ورقم الكلمة وعدد تكراراتها في القرآن.
    """
    rows = query_all(
        "SELECT ws.surahNo, ws.ayahNo, ws.wordNo, r.word, ws.repeatitionCount"
        " FROM word_statistics ws"
        " JOIN word_content_rasm r"
        "   ON r.surahNo=ws.surahNo AND r.ayahNo=ws.ayahNo AND r.wordNo=ws.wordNo"
        " WHERE ws.root = ?"
        " ORDER BY ws.surahNo, ws.ayahNo, ws.wordNo"
        " LIMIT ?",
        (root, limit),
    )
    return [
        {
            "surah": r["surahNo"],
            "ayah": r["ayahNo"],
            "word_no": r["wordNo"],
            "word": r["word"],
            "total_occurrences_in_quran": r["repeatitionCount"],
        }
        for r in rows
    ]


def get_root_statistics(root: str) -> dict:
    """إحصاءات شاملة لجذر معين: عدد الأوزان، السور، الآيات.

    root: الجذر (مثال: 'رحم')
    يُرجع: عدد الكلمات الكلي، عدد السور التي وردت فيها، عدد الآيات.
    """
    row = query_one(
        "SELECT COUNT(*) AS occurrences,"
        "       COUNT(DISTINCT surahNo) AS surahs_count,"
        "       COUNT(DISTINCT surahNo||':'||ayahNo) AS ayahs_count,"
        "       COUNT(DISTINCT wordText) AS distinct_forms"
        " FROM word_statistics WHERE root = ?",
        (root,),
    )
    if not row or row["occurrences"] == 0:
        return {"root": root, "found": False}
    return {
        "root": root,
        "found": True,
        "occurrences": row["occurrences"],
        "surahs_count": row["surahs_count"],
        "ayahs_count": row["ayahs_count"],
        "distinct_forms": row["distinct_forms"],
    }


def register(mcp: FastMCP) -> None:
    mcp.tool(name="analyze_word", annotations=_ANNOTATIONS)(get_word_analysis)
    mcp.tool(name="find_root_occurrences", annotations=_ANNOTATIONS)(search_by_root)
    mcp.tool(name="get_root_stats", annotations=_ANNOTATIONS)(get_root_statistics)
