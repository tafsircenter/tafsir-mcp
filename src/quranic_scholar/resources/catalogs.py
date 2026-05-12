"""MCP Resources: static catalogs and schema documentation."""

import json

from quranic_scholar.db import query_all
from quranic_scholar.models import TAFSIR_ATTRIBUTIONS, TafsirSource

# ── Tafsir catalog (static) ───────────────────────────────────────────────────

_TAFSIR_CATALOG = [
    {
        "id": "tabary",
        "name_ar": "تفسير الإمام الطبري (جامع البيان)",
        "author": "أبو جعفر الطبري",
        "death_year_hijri": 310,
        "db_table": "tafsir_tabary",
        "db_keys": "sura, aya",
        "coverage": "كامل القرآن (6236 آية)",
        "language": "ar",
        "attribution": TAFSIR_ATTRIBUTIONS[TafsirSource.tabary],
    },
    {
        "id": "katheer",
        "name_ar": "تفسير ابن كثير",
        "author": "أبو الفداء إسماعيل بن كثير",
        "death_year_hijri": 774,
        "db_table": "tafsir_katheer",
        "db_keys": "sura, aya",
        "coverage": "كامل القرآن (6236 آية)",
        "language": "ar",
        "attribution": TAFSIR_ATTRIBUTIONS[TafsirSource.katheer],
    },
    {
        "id": "baghawy",
        "name_ar": "تفسير البغوي (معالم التنزيل)",
        "author": "الحسين بن مسعود البغوي",
        "death_year_hijri": 510,
        "db_table": "tafsir_baghawy",
        "db_keys": "sura, aya",
        "coverage": "كامل القرآن (6236 آية)",
        "language": "ar",
        "attribution": TAFSIR_ATTRIBUTIONS[TafsirSource.baghawy],
    },
    {
        "id": "saadi",
        "name_ar": "تيسير الكريم الرحمن (تفسير السعدي)",
        "author": "عبد الرحمن بن ناصر السعدي",
        "death_year_hijri": 1376,
        "db_table": "tafsir_saadi",
        "db_keys": "sura, aya",
        "coverage": "كامل القرآن (6236 آية) — لا قيم فارغة",
        "language": "ar",
        "attribution": TAFSIR_ATTRIBUTIONS[TafsirSource.saadi],
    },
    {
        "id": "moyassar",
        "name_ar": "التفسير الميسر",
        "author": "مجمع الملك فهد لطباعة المصحف الشريف",
        "death_year_hijri": None,
        "db_table": "tafsir_moyassar",
        "db_keys": "sura, aya",
        "coverage": "كامل القرآن (6236 آية)",
        "language": "ar",
        "attribution": TAFSIR_ATTRIBUTIONS[TafsirSource.moyassar],
    },
    {
        "id": "mukhtasar_ar",
        "name_ar": "المختصر في تفسير القرآن الكريم",
        "author": "مجمع الملك فهد لطباعة المصحف الشريف",
        "death_year_hijri": None,
        "db_table": "QuranTafseer",
        "db_column": "Mukhtasarar",
        "db_keys": "surahNo, ayahNo",
        "coverage": "كامل القرآن (6236 آية) — لا قيم فارغة",
        "language": "ar",
        "attribution": TAFSIR_ATTRIBUTIONS[TafsirSource.mukhtasar_ar],
    },
    {
        "id": "mukhtasar_en",
        "name_ar": "المختصر — ترجمة إنجليزية",
        "name_en": "Concise Quran Commentary (English)",
        "author": "King Fahd Complex for the Printing of the Holy Quran",
        "death_year_hijri": None,
        "db_table": "QuranTafseer",
        "db_column": "Mukhtasaren",
        "db_keys": "surahNo, ayahNo",
        "coverage": "Full Quran (6236 ayahs) — no nulls",
        "language": "en",
        "attribution": TAFSIR_ATTRIBUTIONS[TafsirSource.mukhtasar_en],
    },
    {
        "id": "mukhtasar_bn",
        "name_ar": "المختصر — ترجمة بنغالية",
        "name_bn": "সংক্ষিপ্ত তাফসীর (Bengali)",
        "author": "King Fahd Complex for the Printing of the Holy Quran",
        "death_year_hijri": None,
        "db_table": "QuranTafseer",
        "db_column": "Mukhtasarbn",
        "db_keys": "surahNo, ayahNo",
        "coverage": "Full Quran (6236 ayahs) — no nulls",
        "language": "bn",
        "attribution": TAFSIR_ATTRIBUTIONS[TafsirSource.mukhtasar_bn],
    },
]


def get_surahs_catalog() -> str:
    """JSON catalog of all 114 surahs with key metadata."""
    rows = query_all(
        "SELECT surahNo, surahName, makkiMadani, ayahCount, revelationSeq"
        " FROM surah_stats ORDER BY surahNo"
    )
    data = [
        {
            "surah_no": r["surahNo"],
            "name": r["surahName"],
            "revelation_type": r["makkiMadani"],
            "ayah_count": r["ayahCount"],
            "revelation_order": r["revelationSeq"],
        }
        for r in rows
    ]
    return json.dumps(data, ensure_ascii=False, indent=2)


def get_tafsirs_catalog() -> str:
    """JSON catalog of all 8 available tafsir sources with full attribution."""
    return json.dumps(_TAFSIR_CATALOG, ensure_ascii=False, indent=2)


def get_schema_documentation() -> str:
    """Developer reference: DB schema, table mapping, key naming conventions."""
    return """\
# Quranic Scholar MCP — Database Schema Reference
> Read-only SQLite 3.x, ~224 MB (includes FTS5 index)

## Key Naming Difference ⚠️
| Tables | Surah column | Ayah column |
|--------|-------------|-------------|
| tafsir_tabary, tafsir_katheer, tafsir_baghawy, tafsir_saadi, tafsir_moyassar | `sura` | `aya` |
| ALL other tables | `surahNo` | `ayahNo` |

## Tables

### Surah-level (114 rows each)
- **surah_stats** — name, revelation type/order, ayah count, word count, statistics
  Columns: id, surahName, surahNo, revelationSeq, makkiMadani, surahClass,
           ayahCount, wordCount, charCount, beginType, longestWord, mostFreqWord, sujud
- **surah_content** — long-form Arabic content
  Columns: surahNo, surahNameInfo, surahNujoolInfo, surahFadael, surahGoals, surahAyahCount0/1

### Tafsir (6236 rows each — one per ayah)
- **tafsir_tabary** — keys: (sura, aya) + id column. Column: tafsir
- **tafsir_katheer** — keys: (sura, aya). Column: tafsir
- **tafsir_baghawy** — keys: (sura, aya). Column: tafsir
- **tafsir_saadi** — keys: (sura, aya). Column: tafsir. Zero NULLs.
- **tafsir_moyassar** — keys: (sura, aya). Column: tafsir
- **QuranTafseer** — keys: (surahNo, ayahNo). Columns: Mukhtasarar (ar), Mukhtasaren (en), Mukhtasarbn (bn). All zero NULLs.

### Ayah-level (6236 rows each)
- **ayah_content_irab** — keys: (surahNo, ayahNo). Column: **irabAyah1** (not 'irab')
- **ayah_content_tajweed** — keys: (surahNo, ayahNo). Column: tajweed
- **ayah_content_nozool** — keys: (surahNo, ayahNo). Column: nozoolInfo
  ⚠️ Only 201 rows (not all ayahs have nuzool info)

### Word-level (77,432 rows each — one per word)
Primary keys across all word tables: (surahNo, ayahNo, wordNo)

- **word_content_rasm** — Columns: id, word (Uthmani text), rasm (note, may be '-')
- **word_content_meaning** — Column: meaning
- **word_content_irab** — Column: **irabMushakkal** (not 'irab')
- **word_content_sarf** — Column: sarf
- **word_statistics** — Columns: root, repeatitionCount (⚠️ typo in DB), rootRepeatitionCount,
  wordNoInSurah, wordNoInAyah, surahCountWithWord, ayahCountWithWord
- **qeraat_info** — Columns: content (@reader/text@ format), note (nullable)
  Multiple rows per ayah; 'no-difference' entries start with 'لا خلاف'

### Page-level
- **mokhtasar_fawaed** — Columns: page (1-604), content
  ⚠️ Multiple rows per page (avg 3.7 per page, 2212 total rows)

### FTS5 (virtual)
- **ayah_fts** — Columns: surahNo UNINDEXED, ayahNo UNINDEXED, text_normalized, text_original
  Tokenizer: unicode61 remove_diacritics 2. Search via: WHERE text_normalized MATCH ?

## Ayah Text Reconstruction
Full ayah text = concatenate word_content_rasm.word ORDER BY wordNo for given (surahNo, ayahNo).
Includes disconnected letters (e.g., 'الم' is wordNo=1 only).

## Row Counts (verified)
| Table | Rows |
|-------|------|
| surah_stats / surah_content | 114 |
| all tafsir tables | 6236 each |
| QuranTafseer | 6236 |
| ayah_content_irab / tajweed | 6236 each |
| ayah_content_nozool | 201 |
| word_content_* / word_statistics / qeraat_info | 77,432 each |
| mokhtasar_fawaed | 2212 |
| ayah_fts | 6236 |
"""
