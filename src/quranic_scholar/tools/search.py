"""Full-text and tafsir search MCP tools."""

from __future__ import annotations

from typing import Annotated

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from quranic_scholar.db import QuranDataError, get_connection, query_all
from quranic_scholar.models import TAFSIR_ATTRIBUTIONS, TafsirSource
from quranic_scholar.normalize import normalize_arabic

_ANNOTATIONS = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
)

# Pre-built SQL literals per source — no f-strings for table/column names
_SEARCH_TAFSIR_SQL: dict[TafsirSource, tuple[str, str]] = {
    TafsirSource.tabary: (
        "SELECT sura AS s, aya AS a, tafsir AS t FROM tafsir_tabary"
        " WHERE tafsir LIKE ? ESCAPE '!'",
        "s",
    ),
    TafsirSource.katheer: (
        "SELECT sura AS s, aya AS a, tafsir AS t FROM tafsir_katheer"
        " WHERE tafsir LIKE ? ESCAPE '!'",
        "s",
    ),
    TafsirSource.baghawy: (
        "SELECT sura AS s, aya AS a, tafsir AS t FROM tafsir_baghawy"
        " WHERE tafsir LIKE ? ESCAPE '!'",
        "s",
    ),
    TafsirSource.saadi: (
        "SELECT sura AS s, aya AS a, tafsir AS t FROM tafsir_saadi"
        " WHERE tafsir LIKE ? ESCAPE '!'",
        "s",
    ),
    TafsirSource.moyassar: (
        "SELECT sura AS s, aya AS a, tafsir AS t FROM tafsir_moyassar"
        " WHERE tafsir LIKE ? ESCAPE '!'",
        "s",
    ),
    TafsirSource.mukhtasar_ar: (
        "SELECT surahNo AS s, ayahNo AS a, Mukhtasarar AS t FROM QuranTafseer"
        " WHERE Mukhtasarar LIKE ? ESCAPE '!'",
        "s",
    ),
    TafsirSource.mukhtasar_en: (
        "SELECT surahNo AS s, ayahNo AS a, Mukhtasaren AS t FROM QuranTafseer"
        " WHERE Mukhtasaren LIKE ? ESCAPE '!'",
        "s",
    ),
    TafsirSource.mukhtasar_bn: (
        "SELECT surahNo AS s, ayahNo AS a, Mukhtasarbn AS t FROM QuranTafseer"
        " WHERE Mukhtasarbn LIKE ? ESCAPE '!'",
        "s",
    ),
}


def _escape_like(text: str) -> str:
    return text.replace("!", "!!").replace("%", "!%").replace("_", "!_")


def search_quran_text(
    query: str,
    surah_filter: list[int] | None = None,
    limit: Annotated[int, Field(ge=1, le=100)] = 20,
) -> list[dict]:
    """بحث نصي في آيات القرآن باستخدام FTS5 (يدعم البحث بدون تشكيل).

    query: نص البحث — يُطبَّع تلقائياً (تُزال التشكيلات، تُوحَّد الألفات).
    surah_filter: قائمة أرقام سور لتضييق البحث (اختياري).
    limit: أقصى عدد نتائج (1-100، افتراضي 20).
    يُرجع: [{surah, ayah, text, snippet, score}]
    """
    if not query or not query.strip():
        return []

    normalized = normalize_arabic(query.strip())
    if not normalized:
        return []

    conn = get_connection()
    try:
        if surah_filter:
            # Dynamic IN clause — only ? placeholders, not values
            placeholders = ",".join("?" * len(surah_filter))
            sql = (
                f"SELECT surahNo, ayahNo, text_original,"
                f" snippet(ayah_fts,2,'<m>','</m>','…',15) AS snip,"
                f" rank AS score"
                f" FROM ayah_fts"
                f" WHERE text_normalized MATCH ?"
                f" AND surahNo IN ({placeholders})"
                f" ORDER BY rank LIMIT ?"
            )
            params = (normalized, *surah_filter, limit)
        else:
            sql = (
                "SELECT surahNo, ayahNo, text_original,"
                " snippet(ayah_fts,2,'<m>','</m>','…',15) AS snip,"
                " rank AS score"
                " FROM ayah_fts"
                " WHERE text_normalized MATCH ?"
                " ORDER BY rank LIMIT ?"
            )
            params = (normalized, limit)

        try:
            rows = conn.execute(sql, params).fetchall()
        except Exception:
            return []

        return [
            {
                "surah": r["surahNo"],
                "ayah": r["ayahNo"],
                "text": r["text_original"],
                "snippet": r["snip"],
                "score": r["score"],
            }
            for r in rows
        ]
    finally:
        conn.close()


def search_tafsir(
    query: str,
    source: str = "saadi",
    surah_filter: list[int] | None = None,
    limit: Annotated[int, Field(ge=1, le=100)] = 20,
) -> list[dict]:
    """بحث LIKE في تفسير معين.

    query: نص البحث (بحث تضمين — لا يُطبَّع تلقائياً لأن التفاسير تحوي تشكيلاً).
    source: مصدر التفسير (tabary/katheer/baghawy/saadi/moyassar/
                          mukhtasar_ar/mukhtasar_en/mukhtasar_bn).
    surah_filter: قائمة أرقام سور (اختياري).
    limit: أقصى عدد نتائج (افتراضي 20).
    يُرجع: [{surah, ayah, tafsir_excerpt, source_attribution}]
    """
    if not query or not query.strip():
        return []

    try:
        src = TafsirSource(source)
    except ValueError:
        return []

    base_sql, sura_alias = _SEARCH_TAFSIR_SQL[src]
    escaped = _escape_like(query.strip())
    like_param = f"%{escaped}%"

    if surah_filter:
        # Only ? placeholders interpolated — no user values in SQL string
        placeholders = ",".join("?" * len(surah_filter))
        sql = f"{base_sql} AND {sura_alias} IN ({placeholders}) LIMIT ?"
        params = (like_param, *surah_filter, limit)
    else:
        sql = f"{base_sql} LIMIT ?"
        params = (like_param, limit)

    try:
        rows = query_all(sql, params)
    except QuranDataError:
        return []

    attribution = TAFSIR_ATTRIBUTIONS[src]
    return [
        {
            "surah": r["s"],
            "ayah": r["a"],
            "tafsir_excerpt": r["t"][:300] + ("…" if len(r["t"]) > 300 else ""),
            "source_attribution": attribution,
        }
        for r in rows
    ]


def register(mcp: FastMCP) -> None:
    mcp.tool(name="search_quran_text", annotations=_ANNOTATIONS)(search_quran_text)
    mcp.tool(name="search_in_tafsir", annotations=_ANNOTATIONS)(search_tafsir)
