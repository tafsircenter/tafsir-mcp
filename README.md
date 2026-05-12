# Quranic Scholar MCP Server

خادم MCP يمنح Claude Desktop وصولاً علمياً وحرفياً إلى القرآن الكريم بلا اتصال بالإنترنت.

An MCP server giving Claude Desktop offline scholarly access to the Holy Quran.

---

## المحتوى / Contents

| | العربية | English |
|---|---|---|
| **التفاسير** | الطبري، ابن كثير، البغوي، السعدي، الميسر، المختصر (ع/ن/بنغالية) | 5 classical Arabic tafsirs + trilingual Mukhtasar |
| **التحليل اللغوي** | إعراب ومعنى وصرف لكل كلمة (77,432 كلمة) | Word-level i'rab, meaning, sarf (77,432 words) |
| **البحث** | FTS5 بدون تشكيل + بحث في متون التفاسير | Diacritic-free FTS5 + tafsir LIKE search |
| **القراءات** | قراءات القرآن العشر (مخزّنة بصيغة @قارئ/نص@) | Qira'at variants in @reader/text@ format |
| **الإحصاءات** | إحصاءات السور، الجذور، الصفحات | Surah stats, root stats, page fawaed |
| **أسباب النزول** | 201 آية لها بيانات | Asbab al-nuzool for 201 ayahs |

---

## المتطلبات / Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- Claude Desktop (for MCP integration)
- قاعدة البيانات `data/quran.db` (~224 MB) — غير مضمّنة في المستودع

---

## التثبيت / Installation

```bash
git clone https://github.com/your-username/quranic-scholar-mcp
cd quranic-scholar-mcp

# ضع قاعدة البيانات في مجلد data/
cp /path/to/quran.db data/quran.db

# ثبّت المتطلبات
uv sync
```

---

## ربط Claude Desktop / Claude Desktop Setup

أضف الخادم إلى ملف إعدادات Claude Desktop:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "quranic-scholar": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/YOUR_USERNAME/projects/quranic-scholar-mcp",
        "run",
        "quranic-scholar-mcp"
      ]
    }
  }
}
```

استبدل `YOUR_USERNAME` باسم المستخدم الفعلي، ثم أعد تشغيل Claude Desktop.

---

## الأدوات / Tools (13)

### نصوص الآيات / Ayah Text

| الأداة | الوصف |
|--------|-------|
| `fetch_ayah` | نص الآية بالرسم العثماني، مع تجويد/إعراب اختياري |
| `fetch_tafsir` | تفسير آية من مصدر محدد |
| `fetch_nuzool_reason` | سبب نزول الآية (إن وُجد) |

### السور / Surahs

| الأداة | الوصف |
|--------|-------|
| `fetch_surah_info` | معلومات كاملة عن السورة |

### تحليل الكلمات / Word Analysis

| الأداة | الوصف |
|--------|-------|
| `analyze_word` | تحليل كلمة: معنى، إعراب، صرف، إحصاء، قراءات |
| `find_root_occurrences` | جميع مواضع جذر في القرآن |
| `get_root_stats` | إحصاءات جذر: سور، آيات، أوزان |

### القراءات / Qira'at

| الأداة | الوصف |
|--------|-------|
| `get_qeraat_variants` | القراءات المختلفة لآية أو كلمة |

### البحث / Search

| الأداة | الوصف |
|--------|-------|
| `search_quran_text` | بحث نصي FTS5 بدون تشكيل |
| `search_in_tafsir` | بحث LIKE في متن تفسير محدد |

### الإحصاءات / Statistics

| الأداة | الوصف |
|--------|-------|
| `get_quran_overview` | إحصاءات عامة (سور، آيات، كلمات، جذور) |
| `get_page_fawaed` | فوائد صفحة من المصحف |
| `get_surah_statistics` | إحصاءات مفصّلة لسورة |

---

## الموارد / Resources (3)

| المورد | الوصف |
|--------|-------|
| `quran://surahs` | فهرس 114 سورة (JSON) |
| `quran://tafsirs` | فهرس 8 مصادر تفسيرية مع الإسناد (JSON) |
| `quran://schema` | توثيق مخطط قاعدة البيانات (Markdown) |

---

## قوالب الدراسة / Study Prompts (5)

| القالب | الوصف |
|--------|-------|
| `study_ayah(surah, ayah)` | دراسة شاملة لآية: نص + تفسير + إعراب + كلمات |
| `compare_tafsirs(surah, ayah)` | مقارنة التفاسير الخمسة لآية |
| `root_study(root)` | دراسة جذر: إحصاء + مواضع + سياقات |
| `surah_overview(surah)` | نظرة شاملة على سورة |
| `tajweed_lesson(surah, ayah)` | درس تجويد: أحكام + قراءات |

---

## مصادر التفسير / Tafsir Sources

| المعرّف | الكتاب | المؤلف | سنة الوفاة |
|---------|--------|--------|------------|
| `tabary` | جامع البيان | أبو جعفر الطبري | 310هـ |
| `katheer` | تفسير ابن كثير | أبو الفداء إسماعيل بن كثير | 774هـ |
| `baghawy` | معالم التنزيل | الحسين بن مسعود البغوي | 510هـ |
| `saadi` | تيسير الكريم الرحمن | عبد الرحمن بن ناصر السعدي | 1376هـ |
| `moyassar` | التفسير الميسر | مجمع الملك فهد | — |
| `mukhtasar_ar` | المختصر (عربي) | مجمع الملك فهد | — |
| `mukhtasar_en` | Concise Commentary (English) | King Fahd Complex | — |
| `mukhtasar_bn` | সংক্ষিপ্ত তাফসীর (Bengali) | King Fahd Complex | — |

---

## البنية / Project Structure

```
src/quranic_scholar/
├── server.py          # FastMCP entry point
├── db.py              # SQLite read-only connection
├── models.py          # Pydantic models + attributions
├── normalize.py       # Arabic text normalization
├── tools/
│   ├── ayah.py        # fetch_ayah, fetch_tafsir, fetch_nuzool_reason
│   ├── surah.py       # fetch_surah_info
│   ├── word.py        # analyze_word, find_root_occurrences, get_root_stats
│   ├── qeraat.py      # get_qeraat_variants
│   ├── search.py      # search_quran_text, search_in_tafsir
│   └── stats.py       # get_quran_overview, get_page_fawaed, get_surah_statistics
├── resources/
│   └── catalogs.py    # quran://surahs, quran://tafsirs, quran://schema
└── prompts/
    └── study.py       # 5 study prompt templates
```

---

## الاختبارات / Tests

```bash
uv run pytest tests/ -v
# 35 tests — all pass
```

---

## ملاحظات أمان / Security Notes

- قاعدة البيانات تُفتح للقراءة فقط: `mode=ro` + `PRAGMA query_only=ON`
- جميع مدخلات المستخدم تمر عبر `?` placeholders — لا SQL injection
- الخادم لا يستخدم الشبكة (`openWorldHint=False`)

---

## الترخيص / License

See [DATA_SOURCES.md](DATA_SOURCES.md) for attribution and usage terms of the Quranic data.
