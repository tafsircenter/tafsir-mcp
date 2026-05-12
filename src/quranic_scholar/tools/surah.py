"""Surah-level MCP tools: get_surah_info."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from quranic_scholar.db import query_one
from quranic_scholar.models import SurahInfo

_ANNOTATIONS = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
)

# Stat columns to include in SurahInfo.statistics
_STAT_COLS = (
    "wordCount", "charCount", "uniqueAyahCount", "repeatedAyahs",
    "sujud", "beginType", "longestWord", "mostFreqWord", "mostFreqChar",
    "haraqaCount", "charNotOccured",
)


def get_surah_info(
    surah: int = Field(ge=1, le=114, description="رقم السورة (1-114)"),
) -> dict:
    """معلومات شاملة عن سورة: الأسماء، نوع النزول، الفضائل، الأهداف، الإحصاءات."""
    content = query_one(
        "SELECT surahNameInfo, surahNujoolInfo, surahFadael, surahGoals"
        " FROM surah_content WHERE surahNo = ?",
        (surah,),
    )
    stats = query_one(
        "SELECT * FROM surah_stats WHERE surahNo = ?",
        (surah,),
    )

    if not stats:
        return {"error": f"لم يُوجد بيانات للسورة رقم {surah}"}

    statistics = {col: stats[col] for col in _STAT_COLS if col in stats}

    return SurahInfo(
        surah_no=surah,
        names=[stats["surahName"]],
        revelation_type=stats["makkiMadani"],
        ayah_count=stats["ayahCount"],
        revelation_order=stats["revelationSeq"],
        virtues=content["surahFadael"] if content else None,
        objectives=content["surahGoals"] if content else None,
        statistics=statistics,
    ).model_dump()


def register(mcp: FastMCP) -> None:
    mcp.tool(annotations=_ANNOTATIONS)(get_surah_info)
