# Quranic Scholar MCP Server

## Project Overview
MCP server providing scholarly, offline-first access to the Quran with 5 classical Arabic tafsirs (Tabari, Ibn Kathir, Baghawi, Saadi, Muyassar), word-level grammatical analysis (i'rab, sarf, root), qira'at variants, asbab al-nuzool, and surah statistics. Religious content — accuracy is paramount.

## Tech Stack
- Python 3.12 with FastMCP (mcp[cli] >= 1.27.0)
- SQLite 3 + FTS5 for full-text search
- Pydantic v2 for input validation (strict mode)
- pyarabic for Arabic text normalization

## Critical Rules (NEVER VIOLATE)
1. No content generation. Tools return data verbatim from the database. Never summarize, paraphrase, or "improve" religious text.
2. Always attribute. Every tafsir response includes a `source` field with author name, book title, death year.
3. Strict input validation. Every tool parameter uses Pydantic Field with constraints (e.g., surah: int = Field(ge=1, le=114)).
4. Parametrized SQL only. Use ? placeholders. Never f-string SQL.
5. All Quranic ayah counts MUST validate against 6236 total ayahs and 114 surahs.

## FastMCP Parameter Pattern (Critical Bug Avoidance)
**NEVER** write `param: int = Field(ge=1, le=114, default=1)` in tool/prompt functions.
The `Field()` object becomes the default value (FieldInfo) instead of the integer — silent bug.

**ALWAYS** use `Annotated` with a separate Python default:
```python
# ✅ CORRECT
from typing import Annotated
param: Annotated[int, Field(ge=1, le=114)] = 1

# ❌ WRONG — passes FieldInfo to SQLite, causes ProgrammingError
param: int = Field(ge=1, le=114, default=1)
```
Required params (no default): `param: Annotated[int, Field(ge=1, le=114)]` — no `= value`.

## Database Schema
File: data/quran.db (read-only, SQLite 3.x, ~215 MB)

Tables:
- surah_content, surah_stats (114 rows each, surah-level)
- tafsir_tabary, tafsir_katheer, tafsir_baghawy, tafsir_saadi, tafsir_moyassar (6236 rows each; columns: sura, aya, tafsir)
- QuranTafseer (multilingual mukhtasar; columns: surahNo, ayahNo, Mukhtasaren, Mukhtasarar, Mukhtasarbn)
- ayah_content_irab, ayah_content_tajweed (6236 rows each)
- ayah_content_nozool (201 rows — not every ayah has it)
- word_content_rasm, word_content_meaning, word_content_irab, word_content_sarf, word_statistics, qeraat_info (77432 rows each)
- mokhtasar_fawaed (2212 rows, per mushaf page)

Note: full ayah text is reconstructed by concatenating word_content_rasm.word ordered by wordNo for a given (surahNo, ayahNo).

## Tafsir Source Attribution (use these strings exactly)
- tafsir_tabary → "تفسير الإمام الطبري (جامع البيان)، أبو جعفر الطبري (ت. 310هـ)"
- tafsir_katheer → "تفسير ابن كثير، أبو الفداء إسماعيل بن كثير (ت. 774هـ)"
- tafsir_baghawy → "تفسير البغوي (معالم التنزيل)، الحسين بن مسعود البغوي (ت. 510هـ)"
- tafsir_saadi → "تيسير الكريم الرحمن، عبد الرحمن بن ناصر السعدي (ت. 1376هـ)"
- tafsir_moyassar → "التفسير الميسر، مجمع الملك فهد لطباعة المصحف الشريف"

## Project Structure (target)
src/quranic_scholar/
├── __init__.py
├── server.py          # FastMCP entry point
├── db.py              # SQLite connection management
├── models.py          # Pydantic response models
├── normalize.py       # Arabic text normalization
├── tools/
│   ├── ayah.py
│   ├── surah.py
│   ├── word.py
│   ├── search.py
│   ├── qeraat.py
│   └── stats.py
├── resources/
│   └── catalogs.py
└── prompts/
    └── study.py

## MCP Tool Annotations (apply to all tools)
- readOnlyHint: True
- destructiveHint: False
- idempotentHint: True
- openWorldHint: False (no external network calls)

## Testing Requirements
- All 6236 ayahs queryable
- Input validation (out-of-range rejected)
- At least one happy-path test per tool
