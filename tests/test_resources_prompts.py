"""Tests for MCP resources and prompts."""

import json

import pytest

from quranic_scholar.prompts.study import (
    compare_tafsirs,
    root_study,
    study_ayah,
    surah_overview,
    tajweed_lesson,
)
from quranic_scholar.resources.catalogs import (
    get_schema_documentation,
    get_surahs_catalog,
    get_tafsirs_catalog,
)


# ── Resources ─────────────────────────────────────────────────────────────────

def test_surahs_catalog_returns_114():
    data = json.loads(get_surahs_catalog())
    assert len(data) == 114


def test_surahs_catalog_structure():
    data = json.loads(get_surahs_catalog())
    first = data[0]
    assert first["surah_no"] == 1
    assert "name" in first
    assert "ayah_count" in first
    assert "revelation_type" in first
    assert "revelation_order" in first


def test_tafsirs_catalog_returns_8():
    data = json.loads(get_tafsirs_catalog())
    assert len(data) == 8


def test_tafsirs_catalog_has_required_fields():
    data = json.loads(get_tafsirs_catalog())
    for entry in data:
        assert "id" in entry
        assert "name_ar" in entry
        assert "db_table" in entry
        assert "attribution" in entry
        assert "language" in entry


def test_schema_documentation_contains_key_sections():
    doc = get_schema_documentation()
    assert "surah_stats" in doc
    assert "tafsir_tabary" in doc
    assert "ayah_fts" in doc
    assert "word_content_rasm" in doc
    assert "sura" in doc  # key naming difference section


# ── Prompts ───────────────────────────────────────────────────────────────────

def test_study_ayah_prompt_contains_tool_calls():
    result = study_ayah(surah=1, ayah=1)
    assert "fetch_ayah" in result
    assert "fetch_tafsir" in result
    assert "analyze_word" in result
    assert "1:1" in result


def test_compare_tafsirs_prompt_mentions_all_five():
    result = compare_tafsirs(surah=2, ayah=255)
    assert "tabary" in result
    assert "katheer" in result
    assert "baghawy" in result
    assert "saadi" in result
    assert "moyassar" in result
    assert "2:255" in result


def test_root_study_prompt_contains_root():
    result = root_study(root="رحم")
    assert "رحم" in result
    assert "get_root_stats" in result
    assert "find_root_occurrences" in result


def test_surah_overview_prompt_references_tools():
    result = surah_overview(surah=36)
    assert "fetch_surah_info" in result
    assert "get_surah_statistics" in result
    assert "36" in result


def test_tajweed_lesson_prompt_references_qeraat():
    result = tajweed_lesson(surah=1, ayah=2)
    assert "get_qeraat_variants" in result
    assert "analyze_word" in result
    assert "1:2" in result
