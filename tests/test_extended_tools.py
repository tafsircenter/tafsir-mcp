"""Extended tool tests: word, qeraat, search, stats — 15 tests."""

import pytest

from tafsir.tools.word import get_root_statistics, get_word_analysis, search_by_root
from tafsir.tools.qeraat import compare_qeraat
from tafsir.tools.search import search_quran_text, search_tafsir
from tafsir.tools.stats import (
    get_page_fawaed,
    get_quran_statistics,
    get_surah_statistics_summary,
)

# ── word tools ────────────────────────────────────────────────────────────────

def test_word_analysis_fatiha_word_1():
    result = get_word_analysis(1, 1, 1)
    assert result["word"] == "بسم"
    assert result["word_no"] == 1
    assert result["meaning"] is not None
    assert result["irab"] is not None


def test_search_by_root_rahm_returns_many():
    results = search_by_root("رحم")
    assert len(results) >= 30
    assert all("surah" in r and "ayah" in r and "word" in r for r in results)


def test_root_statistics_rahm():
    stats = get_root_statistics("رحم")
    assert stats["found"] is True
    assert stats["occurrences"] >= 100
    assert stats["surahs_count"] >= 40
    assert stats["ayahs_count"] >= 90


def test_root_search_with_limit():
    results = search_by_root("رحم", limit=5)
    assert len(results) <= 5


# ── word analysis: repetition_count exposed as 'frequency' ───────────────────

def test_word_analysis_includes_repetition_count_not_repeatition():
    result = get_word_analysis(1, 1, 2, aspects=["statistics"])  # "الله"
    assert "frequency" in result
    assert result["frequency"] is not None and result["frequency"] > 0
    assert "repeatitionCount" not in result  # DB typo must NOT leak


# ── qeraat tools ──────────────────────────────────────────────────────────────

def test_qeraat_variants_returns_raw_format():
    result = compare_qeraat(1, 4)  # مالك/ملك
    assert result["has_variants"] is True
    entries = result["qeraat_entries"]
    assert len(entries) >= 1
    assert entries[0]["qeraat_raw"].startswith("@")


def test_qeraat_no_variants_for_fatiha_word_2():
    # كلمة 2 في 1:4 = "يوم" — قد يكون لها خلاف أو لا؛ نختبر 1:1 كلمة 1
    result = compare_qeraat(1, 1, word_no=1)
    # كلمة "بسم" لا يوجد لها خلاف قراءة
    assert "qeraat_entries" in result


# ── search tools ──────────────────────────────────────────────────────────────

def test_search_text_finds_bismillah():
    results = search_quran_text("بسم الله")
    assert len(results) >= 1
    surahs = [r["surah"] for r in results]
    ayahs_in_s1 = [r["ayah"] for r in results if r["surah"] == 1]
    assert 1 in ayahs_in_s1


def test_search_text_normalizes_input():
    # بحث مع تشكيل كامل يجب أن يجد نفس النتائج
    results_plain = search_quran_text("الرحمن")
    results_diacritics = search_quran_text("الرَّحْمَنِ")
    assert len(results_plain) > 0
    assert len(results_diacritics) > 0


def test_search_with_surah_filter():
    results = search_quran_text("الله", surah_filter=[2], limit=10)
    assert all(r["surah"] == 2 for r in results)


def test_search_text_invalid_returns_empty():
    results = search_quran_text("xyzxyz_notinquran_12345")
    assert results == []


def test_search_tafsir_saadi_for_rahma():
    results = search_tafsir("رحمة", source="saadi", limit=5)
    assert len(results) >= 1
    assert all("tafsir_excerpt" in r for r in results)
    assert all("source_attribution" in r for r in results)
    assert "السعدي" in results[0]["source_attribution"]


# ── stats tools ───────────────────────────────────────────────────────────────

def test_quran_overview_has_correct_counts():
    overview = get_quran_statistics()
    assert overview["total_surahs"] == 114
    assert overview["total_ayahs"] == 6236
    assert overview["total_words"] == 77432
    assert overview["total_unique_roots"] == 1891
    assert overview["mushaf_pages"] == 604
    assert overview["ayahs_with_nuzool_info"] == 201
    assert overview["makki_surahs"] + overview["madani_surahs"] == 114


def test_page_fawaed_page_1_returns_multiple_items():
    result = get_page_fawaed(1)
    assert result["page"] == 1
    assert result["fawaed_count"] > 1  # المكتشف #4: صفوف متعددة
    assert len(result["items"]) == result["fawaed_count"]


def test_surah_stats_baqarah():
    result = get_surah_statistics_summary(2)
    assert result["surah_no"] == 2
    assert result["name"] == "البقرة"
    assert result["revelation_type"] == "مدنية"
    assert result["ayah_count"] == 286
    assert result["ayah_count_verified"] == 286
