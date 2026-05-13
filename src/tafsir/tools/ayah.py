"""Ayah-level MCP tools: get_ayah, get_ayah_tafsir, get_ayah_nuzool."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from tafsir.db import query_all, query_one
from tafsir.models import (
    TAFSIR_ATTRIBUTIONS,
    AyahReference,
    AyahResponse,
    TafsirEntry,
    TafsirResponse,
    TafsirSource,
)
from tafsir.normalize import reconstruct_ayah

_ANNOTATIONS = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
)

# SQL literals — no f-strings per CLAUDE.md rule #4
_TAFSIR_SQL: dict[TafsirSource, tuple[str, str]] = {
    TafsirSource.tabary: (
        "SELECT tafsir FROM tafsir_tabary WHERE sura = ? AND aya = ?",
        "tafsir",
    ),
    TafsirSource.katheer: (
        "SELECT tafsir FROM tafsir_katheer WHERE sura = ? AND aya = ?",
        "tafsir",
    ),
    TafsirSource.baghawy: (
        "SELECT tafsir FROM tafsir_baghawy WHERE sura = ? AND aya = ?",
        "tafsir",
    ),
    TafsirSource.saadi: (
        "SELECT tafsir FROM tafsir_saadi WHERE sura = ? AND aya = ?",
        "tafsir",
    ),
    TafsirSource.moyassar: (
        "SELECT tafsir FROM tafsir_moyassar WHERE sura = ? AND aya = ?",
        "tafsir",
    ),
    TafsirSource.mukhtasar_ar: (
        "SELECT Mukhtasarar FROM QuranTafseer WHERE surahNo = ? AND ayahNo = ?",
        "Mukhtasarar",
    ),
    TafsirSource.mukhtasar_en: (
        "SELECT Mukhtasaren FROM QuranTafseer WHERE surahNo = ? AND ayahNo = ?",
        "Mukhtasaren",
    ),
    TafsirSource.mukhtasar_bn: (
        "SELECT Mukhtasarbn FROM QuranTafseer WHERE surahNo = ? AND ayahNo = ?",
        "Mukhtasarbn",
    ),
}


def get_ayah(
    surah: int,
    ayah: int,
    include: list[str] | None = None,
) -> dict:
    """جلب نص آية قرآنية بالرسم العثماني.

    include: حقول اختيارية — قائمة تحتوي أي من: 'tajweed', 'irab'
    """
    ref = AyahReference(surah=surah, ayah=ayah)
    include = include or []

    rasm_rows = query_all(
        "SELECT word, wordNo FROM word_content_rasm"
        " WHERE surahNo = ? AND ayahNo = ? ORDER BY wordNo",
        (ref.surah, ref.ayah),
    )
    text = reconstruct_ayah(rasm_rows)

    tajweed = None
    if "tajweed" in include:
        row = query_one(
            "SELECT tajweed FROM ayah_content_tajweed WHERE surahNo = ? AND ayahNo = ?",
            (ref.surah, ref.ayah),
        )
        tajweed = row["tajweed"] if row else None

    irab = None
    if "irab" in include:
        row = query_one(
            "SELECT irabAyah1 FROM ayah_content_irab WHERE surahNo = ? AND ayahNo = ?",
            (ref.surah, ref.ayah),
        )
        irab = row["irabAyah1"] if row else None

    return AyahResponse(
        surah=ref.surah,
        ayah=ref.ayah,
        text=text,
        tajweed=tajweed,
        irab=irab,
        word_count=len(rasm_rows),
    ).model_dump()


def get_ayah_tafsir(
    surah: int,
    ayah: int,
    sources: list[str] | None = None,
) -> dict:
    """جلب تفسير آية من مصدر أو أكثر.

    sources: قائمة المصادر المطلوبة (default: ['saadi']).
    القيم المتاحة: tabary, katheer, baghawy, saadi, moyassar,
                   mukhtasar_ar, mukhtasar_en, mukhtasar_bn
    """
    ref = AyahReference(surah=surah, ayah=ayah)
    requested = [TafsirSource(s) for s in (sources or ["saadi"])]

    tafsirs: list[TafsirEntry] = []
    for src in requested:
        sql, col = _TAFSIR_SQL[src]
        row = query_one(sql, (ref.surah, ref.ayah))
        if row and row[col]:
            tafsirs.append(
                TafsirEntry(
                    source=src,
                    attribution=TAFSIR_ATTRIBUTIONS[src],
                    text=row[col],
                )
            )

    return TafsirResponse(
        surah=ref.surah,
        ayah=ref.ayah,
        tafsirs=tafsirs,
    ).model_dump()


def get_ayah_nuzool(surah: int, ayah: int) -> dict:
    """سبب نزول الآية إن ثبت في المصادر المعتمدة.

    201 آية فقط لها أسباب نزول موثقة في القاعدة.
    النص يُعاد كما هو بإسناده الكامل — لا تلخيص.
    """
    ref = AyahReference(surah=surah, ayah=ayah)
    row = query_one(
        "SELECT nozoolInfo FROM ayah_content_nozool WHERE surahNo = ? AND ayahNo = ?",
        (ref.surah, ref.ayah),
    )
    if not row or not row["nozoolInfo"]:
        return {
            "surah": ref.surah,
            "ayah": ref.ayah,
            "available": False,
            "reason": "لم يثبت سبب نزول لهذه الآية في المصادر المعتمدة",
        }
    return {
        "surah": ref.surah,
        "ayah": ref.ayah,
        "available": True,
        "text": row["nozoolInfo"],
    }


def register(mcp: FastMCP) -> None:
    mcp.tool(name="fetch_ayah", annotations=_ANNOTATIONS)(get_ayah)
    mcp.tool(name="fetch_tafsir", annotations=_ANNOTATIONS)(get_ayah_tafsir)
    mcp.tool(name="fetch_nuzool_reason", annotations=_ANNOTATIONS)(get_ayah_nuzool)
