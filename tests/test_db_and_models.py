"""Tests for db.py and models.py."""

import pytest
from pydantic import ValidationError

from quranic_scholar.db import QuranDataError, get_connection, query_all, query_one
from quranic_scholar.models import (
    SURAH_AYAH_COUNTS,
    TAFSIR_ATTRIBUTIONS,
    AyahReference,
    TafsirSource,
)

# ── db.py tests ────────────────────────────────────────────────────────────────

def test_get_connection_opens_readonly():
    conn = get_connection()
    with pytest.raises(Exception):
        conn.execute("INSERT INTO surah_stats (id) VALUES (999)")
    conn.close()


def test_query_one_returns_dict():
    row = query_one("SELECT surahNo, ayahCount FROM surah_stats WHERE surahNo = ?", (1,))
    assert isinstance(row, dict)
    assert row["surahNo"] == 1
    assert row["ayahCount"] == 7


def test_query_all_returns_list():
    rows = query_all("SELECT surahNo FROM surah_stats ORDER BY surahNo LIMIT 5")
    assert isinstance(rows, list)
    assert len(rows) == 5
    assert rows[0]["surahNo"] == 1


def test_query_with_invalid_sql_raises_quran_data_error():
    with pytest.raises(QuranDataError):
        query_one("SELECT * FROM nonexistent_table_xyz")


# ── models.py — AyahReference validation ──────────────────────────────────────

def test_ayah_reference_rejects_surah_zero():
    with pytest.raises(ValidationError):
        AyahReference(surah=0, ayah=1)


def test_ayah_reference_rejects_surah_115():
    with pytest.raises(ValidationError):
        AyahReference(surah=115, ayah=1)


def test_ayah_reference_rejects_ayah_exceeding_surah_length():
    # الفاتحة 7 آيات — الآية 8 خارج النطاق
    with pytest.raises(ValidationError):
        AyahReference(surah=1, ayah=8)


def test_ayah_reference_accepts_valid():
    ref = AyahReference(surah=2, ayah=255)  # آية الكرسي
    assert ref.surah == 2
    assert ref.ayah == 255


# ── models.py — TAFSIR_ATTRIBUTIONS ───────────────────────────────────────────

def test_tafsir_attribution_strings_match_claude_md():
    assert TAFSIR_ATTRIBUTIONS[TafsirSource.tabary] == (
        "تفسير الإمام الطبري (جامع البيان)، أبو جعفر الطبري (ت. 310هـ)"
    )
    assert TAFSIR_ATTRIBUTIONS[TafsirSource.katheer] == (
        "تفسير ابن كثير، أبو الفداء إسماعيل بن كثير (ت. 774هـ)"
    )
    assert TAFSIR_ATTRIBUTIONS[TafsirSource.baghawy] == (
        "تفسير البغوي (معالم التنزيل)، الحسين بن مسعود البغوي (ت. 510هـ)"
    )
    assert TAFSIR_ATTRIBUTIONS[TafsirSource.saadi] == (
        "تيسير الكريم الرحمن، عبد الرحمن بن ناصر السعدي (ت. 1376هـ)"
    )
    assert TAFSIR_ATTRIBUTIONS[TafsirSource.moyassar] == (
        "التفسير الميسر، مجمع الملك فهد لطباعة المصحف الشريف"
    )


def test_all_114_surahs_in_ayah_counts_dict():
    assert len(SURAH_AYAH_COUNTS) == 114
    assert set(SURAH_AYAH_COUNTS.keys()) == set(range(1, 115))
    assert sum(SURAH_AYAH_COUNTS.values()) == 6236
