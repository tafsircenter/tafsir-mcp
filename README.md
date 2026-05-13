<div align="center">

# 🕌 Tafsir MCP

**خادم MCP العلمي للقرآن الكريم — برعاية مركز تفسير للدراسات القرآنية**

[![PyPI](https://img.shields.io/pypi/v/tafsir-mcp.svg)](https://pypi.org/project/tafsir-mcp/)
[![License](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Data License](https://img.shields.io/badge/data-CC%20BY%204.0-green.svg)](LICENSE-DATA)
[![MCP](https://img.shields.io/badge/MCP-2025--11--25-purple.svg)](https://modelcontextprotocol.io)
[![Tafsir Center](https://img.shields.io/badge/sponsor-Markaz%20Tafsir-darkgreen.svg)](https://tafsir.net)

[العربية](#arabic) · [English](#english)

</div>

---

<a id="arabic"></a>

## 🌙 نبذة

خادم **Model Context Protocol (MCP)** يوفّر وصولاً علمياً موثّقاً للقرآن الكريم لأي مساعد ذكي يدعم MCP (Claude Code، Claude Desktop، VS Code، وغيرها).

كل البيانات مراجعة ومعتمدة من **[مركز تفسير للدراسات القرآنية](https://tafsir.net)**.

---

## ✨ المميزات

- 📖 **6,236 آية** كاملة بالرسم العثماني
- 📚 **5 تفاسير كلاسيكية**: الطبري · ابن كثير · البغوي · السعدي · الميسر
- 🌍 **المختصر في التفسير** بـ3 لغات (عربي، إنجليزي، بنغالي)
- 🔤 **77,432 كلمة** بتحليل لغوي شامل (إعراب، صرف، جذر، رسم)
- 🔍 **1,891 جذر** قابل للبحث والإحصاء
- ⚡ **بحث FTS5** سريع مع تطبيع عربي كامل (بدون تشكيل)
- 🎵 **اختلاف القراءات** لكل آية وكلمة
- 📜 **أسباب النزول** بالإسناد الكامل (201 آية)
- 📊 **إحصاءات تفصيلية** لكل سورة وصفحة مصحف
- 🛡️ **حماية صارمة** من الهلوسة (Pydantic v2 validation)
- 📴 **يعمل دون إنترنت** بعد التثبيت

---

## 🚀 التثبيت السريع

### لمستخدمي Claude Code:
```bash
claude mcp add tafsir --scope user -- uvx tafsir-mcp
```

### للتثبيت اليدوي:
```bash
pip install tafsir-mcp
# أو
uvx tafsir-mcp
```

عند أول تشغيل، سيُحمَّل ملف البيانات (~214 MB) من Hugging Face تلقائياً ويُخزَّن في `~/.cache/tafsir-mcp/`.

### للمطوّرين (من المصدر):
```bash
git clone https://github.com/ah-vb-cod/tafsir-mcp
cd tafsir-mcp
cp /path/to/quran.db data/quran.db   # أو: export TAFSIR_DB_PATH=/path/to/quran.db
uv sync
uv run tafsir-mcp
```

---

## 🔧 ربط Claude Desktop

أضف إلى `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "tafsir": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/YOUR_USERNAME/projects/quranic-scholar-mcp",
        "run",
        "tafsir-mcp"
      ]
    }
  }
}
```

---

## 🧰 الأدوات المتاحة (13 أداة)

| الفئة | الأداة | الوصف |
|---|---|---|
| **الآية** | `fetch_ayah` | نص آية بالرسم العثماني، مع تجويد/إعراب اختياري |
| | `fetch_tafsir` | تفسير من 8 مصادر (تفاسير متعددة بطلب واحد) |
| | `fetch_nuzool_reason` | سبب النزول بالإسناد الكامل |
| **السورة** | `fetch_surah_info` | معلومات شاملة: أهداف، فضائل، نزول |
| | `get_surah_statistics` | إحصاءات: كلمات، حروف، أطول كلمة... |
| **الكلمة** | `analyze_word` | إعراب، صرف، معنى، جذر، قراءات |
| | `find_root_occurrences` | كل مواضع جذر في القرآن |
| | `get_root_stats` | إحصاءات جذر: سور، آيات، أوزان |
| **البحث** | `search_quran_text` | بحث FTS5 بدون تشكيل |
| | `search_in_tafsir` | بحث LIKE في متن تفسير محدد |
| **القراءات** | `get_qeraat_variants` | اختلاف القراءات لآية أو كلمة |
| **عام** | `get_quran_overview` | إحصاءات شاملة للقرآن |
| | `get_page_fawaed` | فوائد صفحة من المصحف |

---

## 📋 الموارد والقوالب

### الموارد (Resources)
| المورد | الوصف |
|--------|-------|
| `quran://surahs` | فهرس 114 سورة (JSON) |
| `quran://tafsirs` | فهرس 8 مصادر تفسيرية مع الإسناد (JSON) |
| `quran://schema` | توثيق مخطط قاعدة البيانات (Markdown) |

### قوالب الدراسة (Prompts)
| القالب | الوصف |
|--------|-------|
| `study_ayah(surah, ayah)` | دراسة شاملة: نص + تفسير + إعراب + كلمات |
| `compare_tafsirs(surah, ayah)` | مقارنة التفاسير الخمسة |
| `root_study(root)` | دراسة جذر: إحصاء + مواضع + سياقات |
| `surah_overview(surah)` | نظرة شاملة على سورة |
| `tajweed_lesson(surah, ayah)` | درس تجويد: أحكام + قراءات |

---

## 📚 مصادر التفسير

| المعرّف | الكتاب | المؤلف | الوفاة |
|---------|--------|--------|--------|
| `tabary` | جامع البيان | أبو جعفر الطبري | 310هـ |
| `katheer` | تفسير ابن كثير | أبو الفداء إسماعيل بن كثير | 774هـ |
| `baghawy` | معالم التنزيل | الحسين بن مسعود البغوي | 510هـ |
| `saadi` | تيسير الكريم الرحمن | عبد الرحمن بن ناصر السعدي | 1376هـ |
| `moyassar` | التفسير الميسر | مجمع الملك فهد | — |
| `mukhtasar_ar` | المختصر (عربي) | مجمع الملك فهد | — |
| `mukhtasar_en` | Concise Commentary (English) | King Fahd Complex | — |
| `mukhtasar_bn` | সংক্ষিপ্ত তাফসীর (Bengali) | King Fahd Complex | — |

---

## 🗂️ بنية المشروع

```
src/tafsir/
├── server.py          # FastMCP entry point
├── db.py              # SQLite read-only connection
├── data_loader.py     # DB path resolver + auto-download
├── models.py          # Pydantic models + attributions
├── normalize.py       # Arabic text normalization
├── tools/             # 13 MCP tools
├── resources/         # 3 MCP resources
└── prompts/           # 5 study prompt templates
```

---

## 🧪 الاختبارات

```bash
uv run pytest tests/ -v
# 35 tests — all pass
```

---

## 🔒 الأمان

- قاعدة البيانات تُفتح للقراءة فقط: `mode=ro` + `PRAGMA query_only=ON`
- جميع مدخلات المستخدم عبر `?` placeholders — لا SQL injection
- الأدوات لا تصل للشبكة (`openWorldHint=False`)

---

## 📜 الترخيص

- **الكود**: [MIT License](LICENSE) — Ahmed Eid, Markaz Tafsir for Quranic Studies
- **قاعدة البيانات**: [CC BY 4.0](LICENSE-DATA) — يجب نسبة المصدر لمركز تفسير

---

## 🏛️ الجهة الراعية

هذا المشروع رعاية ودعم **[مركز تفسير للدراسات القرآنية](https://tafsir.net)**.
البيانات القرآنية مراجعة وموثّقة من قِبل الباحثين العلميين في المركز.

📧 cloud@tafsir.net

---

<a id="english"></a>

## 🌙 About

A **Model Context Protocol (MCP)** server providing scholarly, certified access to the Holy Quran for any MCP-compatible AI assistant (Claude Code, Claude Desktop, VS Code, etc.).

All data is reviewed and certified by **[Markaz Tafsir for Quranic Studies](https://tafsir.net)**.

## ✨ Features

- 📖 **6,236 ayahs** in Uthmani script
- 📚 **5 classical Arabic tafsirs**: Tabari · Ibn Kathir · Baghawi · Saadi · Muyassar
- 🌍 **Trilingual Mukhtasar** (Arabic, English, Bengali)
- 🔤 **77,432 words** with full linguistic analysis (i'rab, sarf, root, rasm)
- 🔍 **1,891 roots** searchable with statistics
- ⚡ **FTS5 search** with full Arabic normalization (diacritic-free)
- 🎵 **Qira'at variants** per ayah and word
- 📜 **Asbab al-nuzool** with full isnad (201 ayahs)
- 📊 **Detailed statistics** per surah and mushaf page
- 🛡️ **Hallucination protection** (strict Pydantic v2 validation)
- 📴 **Fully offline** after installation

## 🚀 Quick Install

```bash
# Claude Code
claude mcp add tafsir --scope user -- uvx tafsir-mcp

# pip / uvx
pip install tafsir-mcp
uvx tafsir-mcp
```

On first run, the database (~214 MB) is downloaded automatically from Hugging Face and cached at `~/.cache/tafsir-mcp/`.

## 🧰 Available Tools (13)

| Category | Tool | Description |
|---|---|---|
| **Ayah** | `fetch_ayah` | Ayah text with optional tajweed/i'rab |
| | `fetch_tafsir` | Tafsir from up to 8 sources in one call |
| | `fetch_nuzool_reason` | Asbab al-nuzool with full isnad |
| **Surah** | `fetch_surah_info` | Full surah info: goals, virtues, revelation |
| | `get_surah_statistics` | Word count, char count, longest word... |
| **Word** | `analyze_word` | I'rab, sarf, meaning, root, qira'at |
| | `find_root_occurrences` | All occurrences of a root in the Quran |
| | `get_root_stats` | Root stats: surahs, ayahs, distinct forms |
| **Search** | `search_quran_text` | FTS5 diacritic-free search |
| | `search_in_tafsir` | LIKE search in a tafsir text |
| **Qira'at** | `get_qeraat_variants` | Reading variants for ayah or word |
| **General** | `get_quran_overview` | Quran-wide statistics |
| | `get_page_fawaed` | Fawaed for a mushaf page |

## 📜 License

- **Code**: [MIT](LICENSE) — Ahmed Eid, Markaz Tafsir for Quranic Studies
- **Quranic Data**: [CC BY 4.0](LICENSE-DATA) — attribution to "Markaz Tafsir for Quranic Studies" required

## 🏛️ Sponsor

Sponsored by **[Markaz Tafsir for Quranic Studies](https://tafsir.net)**.

📧 cloud@tafsir.net · [GitHub Issues](https://github.com/ah-vb-cod/tafsir-mcp/issues)
