"""Statistics MCP tools: Quran overview, page fawaed, surah stats."""

from __future__ import annotations

from typing import Annotated

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from tafsir.db import query_all, query_one
from tafsir.models import SURAH_AYAH_COUNTS

_ANNOTATIONS = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
)


def get_quran_statistics() -> dict:
    """نظرة عامة شاملة على إحصاءات القرآن الكريم.

    يُرجع: عدد السور، الآيات، الكلمات، الجذور الفريدة،
    تصنيف مكي/مدني، عدد الصفحات، عدد آيات أسباب النزول.
    """
    # Makki / Madani counts
    type_rows = query_all(
        "SELECT makkiMadani, COUNT(*) AS cnt FROM surah_stats GROUP BY makkiMadani"
    )
    type_map = {r["makkiMadani"]: r["cnt"] for r in type_rows}

    unique_roots = query_one(
        "SELECT COUNT(DISTINCT root) AS cnt FROM word_statistics"
    )
    nozool_count = query_one("SELECT COUNT(*) AS cnt FROM ayah_content_nozool")
    pages = query_one(
        "SELECT COUNT(DISTINCT page) AS cnt FROM mokhtasar_fawaed"
    )
    words = query_one("SELECT COUNT(*) AS cnt FROM word_content_rasm")

    return {
        "total_surahs": 114,
        "total_ayahs": 6236,
        "total_words": words["cnt"] if words else 77432,
        "total_unique_roots": unique_roots["cnt"] if unique_roots else 1891,
        "makki_surahs": type_map.get("مكية", 0),
        "madani_surahs": type_map.get("مدنية", 0),
        "mushaf_pages": pages["cnt"] if pages else 604,
        "ayahs_with_nuzool_info": nozool_count["cnt"] if nozool_count else 201,
    }


def get_page_fawaed(
    page: Annotated[int, Field(ge=1, le=604, description="رقم صفحة المصحف (1-604)")],
) -> dict:
    """فوائد المختصر لصفحة من صفحات المصحف.

    page: رقم الصفحة (1-604).
    تحذير: الصفحة قد تحوي عدة فوائد — تُرجع كلها في قائمة items.
    """
    rows = query_all(
        "SELECT content FROM mokhtasar_fawaed WHERE page = ? ORDER BY rowid",
        (page,),
    )
    items = [r["content"] for r in rows if r["content"]]
    return {
        "page": page,
        "fawaed_count": len(items),
        "items": items,
    }


def get_surah_statistics_summary(
    surah: Annotated[int, Field(ge=1, le=114, description="رقم السورة (1-114)")],
) -> dict:
    """إحصاءات مفصّلة لسورة: كلمات، حروف، بدايات، أطول كلمة، الأكثر تكراراً.

    يجمع بيانات surah_stats و surah_content في استجابة واحدة.
    """
    row = query_one(
        "SELECT ss.*, sc.surahNameInfo, sc.surahFadael,"
        "       sc.surahGoals, sc.surahNujoolInfo"
        " FROM surah_stats ss"
        " JOIN surah_content sc ON sc.surahNo = ss.surahNo"
        " WHERE ss.surahNo = ?",
        (surah,),
    )
    if not row:
        return {"error": f"لم تُوجد بيانات للسورة {surah}"}

    return {
        "surah_no": surah,
        "name": row["surahName"],
        "revelation_type": row["makkiMadani"],
        "revelation_order": row["revelationSeq"],
        "surah_class": row["surahClass"],
        "ayah_count": row["ayahCount"],
        "unique_ayah_count": row["uniqueAyahCount"],
        "repeated_ayahs": row["repeatedAyahs"],
        "word_count": row["wordCount"],
        "char_count": row["charCount"],
        "haraka_count": row["haraqaCount"],
        "begin_type": row["beginType"],
        "longest_word": row["longestWord"],
        "most_freq_word": row["mostFreqWord"],
        "most_freq_char": row["mostFreqChar"],
        "sujud": row["sujud"],
        "chars_not_occurred": row["charNotOccured"],
        "chars_in_every_ayah": row["charOccuredInEveryAyah"],
        "names_info": row["surahNameInfo"],
        "virtues": row["surahFadael"],
        "objectives": row["surahGoals"],
        "nuzool_info": row["surahNujoolInfo"],
        "ayah_count_verified": SURAH_AYAH_COUNTS.get(surah),
    }


def register(mcp: FastMCP) -> None:
    mcp.tool(name="get_quran_overview", annotations=_ANNOTATIONS)(get_quran_statistics)
    mcp.tool(name="get_page_fawaed", annotations=_ANNOTATIONS)(get_page_fawaed)
    mcp.tool(name="get_surah_statistics", annotations=_ANNOTATIONS)(get_surah_statistics_summary)
