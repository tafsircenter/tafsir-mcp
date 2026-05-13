# 📦 Tafsir MCP — Context Pack
> وثيقة مستقلة (self-contained) لتأهيل أي نموذج/مساعد جديد على المشروع دون الحاجة للرجوع لتاريخ المحادثة.
> آخر تحديث: 12 مايو 2026

---

## 1. هوية المشروع

| الحقل | القيمة |
|---|---|
| **الاسم الرسمي** | `tafsir-mcp` |
| **الاسم القديم** (مهجور) | `quranic-scholar-mcp` |
| **الإصدار الحالي** | v1.0.0 (قيد إعادة التسمية والنشر) |
| **الهدف بجملة** | خادم MCP يوفّر وصولاً علمياً موثّقاً (offline-first) للقرآن الكريم وخمسة تفاسير كلاسيكية وتحليل لغوي شامل لـ77,432 كلمة، لأي مساعد ذكي يدعم Model Context Protocol. |
| **الحالة الحالية** | جاهز تقنياً ومُختبر. 35/35 اختبار ناجح. مُتصل ومُجرَّب فعلياً عبر Claude Code. **متبقٍ:** إعادة تسمية الحزمة + رفع DB على Hugging Face + نشر على PyPI + GitHub. |
| **الجهة الراعية** | مركز تفسير للدراسات القرآنية (Markaz Tafsir for Quranic Studies, https://tafsir.net) |
| **المطوّر** | Ahmed Eid (GitHub: `ah-vb-cod`) |
| **البريد الرسمي** | cloud@tafsir.net |
| **الترخيص** | MIT للكود + CC BY 4.0 للمحتوى القرآني |
| **المستخدم المستهدف** | (1) طلاب العلم الشرعي — بحث في 5 تفاسير دفعة واحدة. (2) الأئمة والخطباء — إعداد خطب بمصادر موثقة. (3) الباحثون اللغويون — تحليل 77,432 كلمة و1,891 جذراً. (4) مطوّرو التطبيقات الإسلامية — API علمي مفتوح المصدر. (5) أي LLM يحتاج نصوصاً قرآنية موثوقة بدلاً من ذاكرته. |

### بيان النية الذي قاله المالك حرفياً
> "نعم سيتم نشره مجاناً لجميع المسلمين - اريد افضل الية لنشره وسرعة الاستجابة والدقة"
> "أنا أعمل في مركز تفسير للدراسات القرآنية وستكون هي الجهة المتبنية للمشروع"
> "الداتا المرفوعة كلها مراجعة بالفعل ومستخدمة في تطبيقات المركز — اعتبرها معتمدة"

---

## 2. البنية التقنية

### 2.1 المكدّس (Stack)

| الطبقة | الاختيار | السبب |
|---|---|---|
| لغة الخادم | **Python 3.12** | MCP Python SDK الأنضج |
| إدارة الحزم | **uv 0.11.7+** (Astral) | الأسرع، المعيار في 2026 |
| إطار MCP | **FastMCP** عبر `mcp[cli] >= 1.27.0` | الرسمي من Anthropic |
| بروتوكول MCP | **2025-11-25** | الإصدار الثابت حتى مايو 2026 |
| التحقق من المدخلات | **Pydantic v2** (strict) | حماية من هلوسة الـLLM |
| قاعدة البيانات | **SQLite 3.x + FTS5** | بدون خادم، يونيكود كامل |
| معالجة العربية | **pyarabic >= 0.6.15** | تطبيع الألف/الهمزة/التشكيل |
| الاختبار | **pytest + pytest-asyncio** | — |
| الجودة | **ruff + mypy** | تنسيق + فحص أنواع |
| الحاوية | **Docker** (Python 3.12-slim) | للنشر السحابي |
| Transports المدعومة | **stdio** (محلي) + **Streamable HTTP** (سحابي مستقبلاً) | — |

### 2.2 شجرة الملفات (Layout الحالي قبل إعادة التسمية النهائية)

```
~/projects/quranic-scholar-mcp/   ← سيُعاد لـ tafsir-mcp
├── CLAUDE.md                     ← دليل المساعد (قواعد المشروع للـAI)
├── README.md                     ← ثنائي اللغة
├── DATA_SOURCES.md               ← مصادر التفاسير والإسناد العلمي
├── LICENSE                       ← MIT (للكود)
├── LICENSE-DATA                  ← CC BY 4.0 (للمحتوى)
├── CONTRIBUTING.md               
├── pyproject.toml                ← uv-managed
├── .gitignore                    ← يتجاهل data/quran.db
├── Dockerfile                    
├── .github/workflows/
│   ├── test.yml                  ← CI
│   └── publish.yml               ← نشر PyPI تلقائياً عند release
├── data/
│   └── quran.db                  ← 214 MB، يُستبعد من Git
├── src/quranic_scholar/           ← سيُعاد لـ src/tafsir/
│   ├── __init__.py
│   ├── server.py                  ← نقطة دخول FastMCP
│   ├── db.py                      ← read-only sqlite + helpers
│   ├── data_loader.py             ← (مخطط) تحميل DB من HF
│   ├── models.py                  ← Pydantic schemas
│   ├── normalize.py               ← تطبيع النص العربي
│   ├── tools/
│   │   ├── ayah.py                ← 3 أدوات
│   │   ├── surah.py               ← 1 أداة
│   │   ├── word.py                ← 3 أدوات
│   │   ├── qeraat.py              ← 1 أداة
│   │   ├── search.py              ← 2 أداة
│   │   └── stats.py               ← 3 أدوات
│   ├── resources/
│   │   └── catalogs.py            ← 3 موارد
│   └── prompts/
│       └── study.py               ← 5 قوالب
├── tests/
│   ├── test_db_and_models.py      ← 10 اختبارات
│   ├── test_tools.py              ← 10 اختبارات
│   ├── test_extended_tools.py     ← 15 اختباراً (شامل FTS5)
│   └── test_resources_prompts.py  ← 10 اختبارات
└── scripts/
    ├── verify_data.py             ← فحص اكتمال DB (11 فحص)
    ├── inspect_schema.py          ← اكتشاف schema
    ├── SCHEMA_NOTES.md            ← مرجع الأعمدة الفعلية
    ├── build_fts.py               ← بناء FTS5 + 17 فهرساً
    └── build_indexes.py           ← (مدمج في build_fts.py)
```

### 2.3 النمط المعماري

#### نمط التسجيل المعتمد: **Programmatic Registration** (وليس Decorators)
الأدوات والقوالب **تُسجّل برمجياً** داخل دالة `register(mcp)` في كل ملف، **وليس** عبر `@mcp.tool()` decorator مباشرة. السبب: مرونة في تسمية أدوات MCP بأسماء مختلفة عن أسماء دوال Python الداخلية.

```python
# في tools/ayah.py:
def get_ayah(surah: int, ayah: int, ...) -> dict: ...
def get_ayah_tafsir(...) -> dict: ...
def get_ayah_nuzool(...) -> dict: ...

def register(mcp):
    mcp.tool(name="fetch_ayah")(get_ayah)
    mcp.tool(name="fetch_tafsir")(get_ayah_tafsir)
    mcp.tool(name="fetch_nuzool_reason")(get_ayah_nuzool)
```

#### في server.py:
```python
from tafsir.tools import ayah as ayah_tools, surah as surah_tools, ...
from tafsir.prompts import study as study_prompts

mcp = FastMCP("Tafsir MCP")

ayah_tools.register(mcp)
surah_tools.register(mcp)
word_tools.register(mcp)
qeraat_tools.register(mcp)
search_tools.register(mcp)
stats_tools.register(mcp)
study_prompts.register(mcp)

# الموارد تُعرّف هنا مباشرة بـ @mcp.resource
@mcp.resource("quran://surahs")
def surahs_catalog() -> str: ...
```

### 2.4 خرائط الجداول (من DB → الأدوات)

| المفهوم | الجدول | المفاتيح |
|---|---|---|
| نص الآية | `word_content_rasm.word` (مُجمَّع بـ `ORDER BY wordNo`) | `surahNo, ayahNo` |
| تجويد الآية | `ayah_content_tajweed.tajweed` | `surahNo, ayahNo` |
| إعراب الآية | `ayah_content_irab.irabAyah1` | `surahNo, ayahNo` |
| سبب النزول | `ayah_content_nozool.nozoolInfo` (سند + متن في عمود واحد) | `surahNo, ayahNo` |
| تفسير الطبري/ابن كثير/البغوي/السعدي/الميسر | `tafsir_<name>.tafsir` | **`sura, aya`** (مختلف!) |
| المختصر متعدد اللغات | `QuranTafseer.{Mukhtasarar, Mukhtasaren, Mukhtasarbn}` | `surahNo, ayahNo` |
| معنى الكلمة | `word_content_meaning` | `surahNo, ayahNo, wordNo` |
| إعراب الكلمة | `word_content_irab.irabMushakkal` | `surahNo, ayahNo, wordNo` |
| صرف الكلمة | `word_content_sarf` | `surahNo, ayahNo, wordNo` |
| إحصاءات الكلمة (الجذر، التكرار) | `word_statistics.{root, repeatitionCount}` ⚠️ مهجأ خطأ في DB | `surahNo, ayahNo, wordNo` |
| اختلاف القراءات | `qeraat_info.content` بتنسيق `@قارئ/نص@` | `surahNo, ayahNo, wordNo` |
| فوائد الصفحة | `mokhtasar_fawaed` (عدة صفوف لكل صفحة!) | `page` |

### 2.5 الأدوات الـ13 المسجَّلة (أسماء MCP، ليس أسماء Python)

```
fetch_ayah, fetch_tafsir, fetch_nuzool_reason,
fetch_surah_info,
analyze_word, find_root_occurrences, get_root_stats,
get_qeraat_variants,
search_quran_text, search_in_tafsir,
get_quran_overview, get_page_fawaed, get_surah_statistics
```

### 2.6 الموارد الـ3
```
quran://surahs    — قائمة الـ114 سورة بالأسماء والإحصاءات
quran://tafsirs   — فهرس المراجع الـ8 (الطبري إلى المختصر بثلاث لغات)
quran://schema    — توثيق سكيمة DB للمطوّرين
```

### 2.7 القوالب الـ5
```
study_ayah(surah, ayah)        — دراسة شاملة لآية
compare_tafsirs(surah, ayah)   — مقارنة 5 تفاسير لآية
root_study(root)               — دراسة جذر عبر القرآن
surah_overview(surah)          — نظرة شاملة على سورة
tajweed_lesson(surah, ayah)    — درس تجويد لآية
```

### 2.8 إحصاءات قاعدة البيانات

| القياس | القيمة |
|---|---|
| السور | 114 |
| الآيات | 6,236 |
| الكلمات | 77,432 |
| الجذور الفريدة | 1,891 |
| صفحات المصحف | 604 |
| آيات لها أسباب نزول موثّقة | 201 |
| إجمالي صفوف التفاسير | ~37,416 (6 مصادر × 6,236) |
| حجم DB قبل الفهارس | 214 MB |
| حجم DB بعد FTS5 + 17 فهرساً | 223.5 MB |

---

## 3. اصطلاحات الكود

### 3.1 التسمية

| العنصر | الاصطلاح | مثال |
|---|---|---|
| دوال Python | `snake_case` فعلي/وصفي | `get_ayah`, `search_by_root` |
| أسماء أدوات MCP المسجَّلة | `snake_case` بفعل واضح | `fetch_ayah`, `analyze_word` |
| ⚠️ ملاحظة | اسم MCP قد يختلف عن اسم Python | Python `get_ayah` → MCP `fetch_ayah` |
| Pydantic models | `PascalCase` | `AyahReference`, `TafsirResponse` |
| Enums | `PascalCase` للاسم، `snake_case` للقيم | `TafsirSource.saadi` |
| الثوابت | `UPPER_SNAKE_CASE` | `TAFSIR_KEYS`, `STANDARD_KEYS`, `SURAH_AYAH_COUNTS` |
| ملفات Python | `snake_case.py` | `ayah.py`, `data_loader.py` |
| موارد URI | `quran://<category>` | `quran://surahs` |
| فروع Git | `feat/`, `fix/`, `docs/` | `feat/add-fts5` |

### 3.2 المفاتيح المزدوجة في SQL (⚠️ فخّ كلاسيكي)

```python
# في db.py:
TAFSIR_KEYS = ("sura", "aya")        # tafsir_tabary/katheer/baghawy/saadi/moyassar
STANDARD_KEYS = ("surahNo", "ayahNo")  # كل الجداول الأخرى
```

**كل استعلام SQL يلامس التفاسير لازم يستخدم `sura, aya`. الباقي `surahNo, ayahNo`.**

### 3.3 نمط Pydantic v2 الصحيح في FastMCP

⚠️ **درس مكتشف:** `Field()` كقيمة افتراضية في دالة عادية يُنتج `FieldInfo` بدل القيمة.

```python
# ❌ خطأ — ينتج FieldInfo:
def get_ayah(surah: int = Field(ge=1, le=114, default=1), ...): ...

# ✅ صحيح — Annotated pattern:
from typing import Annotated
def get_ayah(
    surah: Annotated[int, Field(ge=1, le=114)] = 1,
    ...
): ...
```

### 3.4 معايير الأدوات

كل أداة MCP يجب أن تحوي:

```python
@mcp.tool(
    name="fetch_ayah",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,   # لا اتصال خارجي
    }
)
def get_ayah(...) -> dict:
    """جلب نص آية محددة من القرآن الكريم مع خيارات إضافية.

    Args:
        surah: رقم السورة (1-114)
        ayah: رقم الآية داخل السورة
        ...
    """
```

- Docstring **بالعربية** للوصف الرئيسي (الـLLM يقرؤها ليقرر متى يستدعي الأداة)
- Args **بالإنجليزية** الفنية
- نوع الإرجاع: `dict` دائماً (JSON-serializable)

### 3.5 SQL parametrized (إلزامي)

```python
# ❌ خطر:
cursor.execute(f"SELECT * FROM tafsir_saadi WHERE sura = {surah}")

# ✅ صحيح:
cursor.execute("SELECT * FROM tafsir_saadi WHERE sura = ? AND aya = ?", (surah, ayah))
```

### 3.6 طول الدوال
غير محدد رسمياً، لكن النمط الملاحظ: كل دالة تركّز على مسؤولية واحدة، 10-40 سطراً عادة. تقسيم بـ helper functions عند الحاجة.

### 3.7 التعليقات
- بالعربية للسياق الديني/الشرعي
- بالإنجليزية للتعليقات التقنية البحتة
- تعليقات `# sic` لأخطاء DB المحفوظة عمداً (مثل `repeatitionCount`)

---

## 4. أسلوب التواصل المتّبع مع المالك

| البُعد | التفضيل |
|---|---|
| **اللغة الأساسية** | العربية، مع مصطلحات تقنية بالإنجليزية كما هي |
| **طول الرد** | متوسط إلى طويل — يُقدِّر التفصيل لكن يكره الحشو |
| **مستوى الشرح** | يفضّل خطوات قابلة للنسخ مباشرة (copy-pasteable) |
| **الترتيب** | **الكود/الإجراء أولاً، ثم الشرح**. يكره الشرح المطوّل قبل التنفيذ |
| **النبرة** | عملية، مباشرة، احترافية. يقدّر اللمسات الروحية المقتصدة (آية، دعاء قصير) في اللحظات المهمة |
| **الصياغة** | جداول مرتبة، ✅/❌، code blocks مع لغة محددة، عناوين Markdown واضحة |
| **التأكيدات** | يطلب "اعرض الخطة أولاً ثم نفّذ" — يحب Plan Mode |
| **التغذية الراجعة** | يردّ بجداول ملخّصة لما أنجز + commit hash |
| **منصة التشغيل** | macOS Apple Silicon (M-series). الأوامر المخصصة لـmacOS مفضّلة |
| **سرعة التقدم** | سريع جداً — أنجز إعداد بيئة + بناء الـMVP في ~5 ساعات |
| **التفاعل مع الأخطاء** | يرسل لقطات أو نص الخطأ كاملاً ويتوقع تشخيصاً دقيقاً |

### اقتباسات حرفية تعكس نبرته
> "كل شيء جاهز 100%"
> "10/10 ✅ كل الاختبارات نجحت"
> "اين اجد هذه الخطوات؟"
> "نعم سنبدأ مباشرة"
> "اعرض الخطة أولاً ثم نفّذ"

### عبارات وأنماط رد متكررة في تقاريره
```
المهمة مكتملة ✅
الملف          الحالة
---            ---
db.py          ✅
models.py      ✅
commit 2ba90e6 ✅
```

---

## 5. سجل القرارات

| القرار | السبب | البديل المرفوض |
|---|---|---|
| **Python** كلغة الخادم | MCP Python SDK الأنضج، أقصر للتطوير | TypeScript (أحدث وأقل نضجاً للحالة) |
| **uv** بدل pip/poetry | الأسرع 10-100×، المعيار الرسمي في 2026 | pip + venv التقليدي |
| **FastMCP** | الإطار الرسمي من Anthropic، 70% من خوادم MCP | بناء خادم MCP يدوياً |
| **SQLite + FTS5** | offline-first، بدون خادم، يونيكود | PostgreSQL (يتطلب خادماً) أو ملفات JSON |
| **Pydantic v2 strict** | حماية صارمة من هلوسة الـLLM | dataclasses أو dict عادي |
| **read-only DB** عبر `?mode=ro` | استحالة تعديل المحتوى الديني خطأً | اتصال عادي مع pragma |
| **اسم MCP ≠ اسم Python** | المرونة وقراءة الكود | تطابق إلزامي يُقيّد التسمية |
| **`Annotated[T, Field(...)] = d`** | تفادي bug FieldInfo في FastMCP | `Field(default=...)` (مكسور) |
| **`register(mcp)` بدل `@mcp.tool`** | مودولاريّة + قابلية إعادة التسمية | decorators مباشرة في tools/ |
| **MIT للكود + CC BY 4.0 للمحتوى** | الكود مفتوح، المحتوى ملك المركز ومحفوظ | ترخيص واحد (يضرّ بأحد الطرفين) |
| **Hugging Face Datasets للـDB** | حدّ PyPI 100MB، الـDB 214MB | تضمين DB في PyPI (مستحيل) |
| **بدون beta — مباشرة v1.0** | البيانات معتمدة سلفاً من المركز | إصدار v0.x للمراجعة |
| **النشر تحت حساب `ah-vb-cod`** | مرحلي حتى تُنشأ منظمة GitHub رسمية | الانتظار لإنشاء org |
| **اسم `tafsir-mcp`** | قصير، عام، يربط بالمركز ضمنياً | `quranic-scholar-mcp`, `tadabbur-mcp`, `mishkah-mcp`, `hadi-mcp` |
| **FTS5 للقرآن فقط، LIKE للتفاسير** | توفير مساحة، FTS5 على ~300MB من التفاسير غير ضروري | FTS5 شامل |
| **qeraat raw + parser منفصل** | الباحث يفضّل النص الأصلي، أي parser قد يخطئ | parsing داخل الأداة |
| **حفظ الإسناد كاملاً في nuzool** | أمانة شرعية، الإسناد جزء من العلم | تشذيب لاختصار الرد |
| **TAFSIR_KEYS مقابل STANDARD_KEYS** | ثابتان واضحان يمنعان الخلط بين `sura/aya` و`surahNo/ayahNo` | تذكّر الفرق يدوياً (عرضة للخطأ) |

---

## 6. المقاربات المرفوضة (تجربة فعلية في المشروع)

| ما جُرّب | لماذا رُفض | ماذا حلّ محله |
|---|---|---|
| ربط الخادم بـ **Claude Desktop (Chat)** | الإصدار الحالي (مايو 2026) لا يدعم MCP في Chat — يعرض رسالة "Switch to Cowork or Code" | الربط بـ **Claude Code داخل VS Code** |
| `Field(default=val)` مع type hints عادية | ينتج كائن `FieldInfo` بدلاً من القيمة → كسر أدوات FastMCP | `Annotated[T, Field(...)] = default` |
| `@mcp.tool` decorator مباشرة على دوال Python | يُجبر اسم MCP = اسم Python | `mcp.tool(name="...")(fn)` داخل `register()` |
| الاعتماد على ذاكرة Claude للنص القرآني | هلوسة (مثلاً يخترع آية رقم 300 في البقرة) | كل ردّ قرآني يمرّ عبر `fetch_ayah` مع validation |
| تضمين `quran.db` (214MB) في حزمة PyPI | حد PyPI 100MB | استبعاد DB من الحزمة + `data_loader.py` يحمّلها من Hugging Face عند أول تشغيل |
| اختبارات تختبر MCP layer كاملاً | بطيء ومعقد | اختبارات تختبر **دوال Python مباشرة** + اختبار MCP layer منفصل عبر `mcp.list_tools()` |
| كتابة SQL بـ f-strings | SQL injection + خطأ خفي | SQL parametrized بـ`?` placeholders حصرياً |
| إنشاء `claude_desktop_config.json` فارغاً ثم الإضافة يدوياً | الـUI لا يدعم MCP، لا فائدة | إضافة الخادم لـ Claude Code عبر `claude mcp add ...` |
| تخمين أسماء أعمدة DB | الاسم الفعلي قد يكون `irabAyah1` لا `irab`، `irabMushakkal` لا `irab`، `repeatitionCount` (مهجأ خطأ) لا `repetitionCount` | فحص استباقي عبر `scripts/inspect_schema.py` + توثيق في `scripts/SCHEMA_NOTES.md` |
| تشذيب الإسناد في أسباب النزول لاختصار الرد | يخل بالأمانة العلمية | إعادة النص حرفياً + ملاحظة في `available: true/false` |
| Parsing لتنسيق qeraat `@قارئ/نص@` داخل الأداة | parsers هشة، الباحث يفضّل النص الأصلي | إرجاع `qeraat_raw` + `format_note` يشرح التنسيق |

---

## 7. القيود الصارمة (Hard Constraints)

> **هذه القواعد موثّقة في `CLAUDE.md` ولا يجوز كسرها مطلقاً تحت أي ظرف.**

### 7.1 محتوى ديني — لا توليد، لا اجتهاد
1. **No content generation.** الأدوات تُرجع البيانات حرفياً من DB. لا تلخيص، لا إعادة صياغة، لا "تحسين" للنص الديني.
2. **Always attribute.** كل تفسير يُرجع مع `source` يحوي: اسم المؤلف + عنوان الكتاب + سنة الوفاة.
3. **حفظ الإسناد كاملاً** في أسباب النزول. لا تشذيب.

### 7.2 الأمان البرمجي
4. **Read-only DB** عبر URI: `file:{path}?mode=ro` + `PRAGMA query_only=ON`.
5. **Parametrized SQL only.** استخدم `?` placeholders. **ممنوع** `f"... {var} ..."` في SQL أبداً.

### 7.3 التحقق الصارم
6. **Pydantic validation** لكل معامل أداة: `Annotated[int, Field(ge=1, le=114)]`.
7. **الأرقام المرجعية الإلزامية:**
   - **114** سورة بالضبط
   - **6,236** آية بالضبط
   - **77,432** كلمة بالضبط
   - **1,891** جذراً
   - **604** صفحة في المصحف
   - **201** آية لها أسباب نزول
8. **التحقق من عدد آيات السورة:** `ayah ≤ SURAH_AYAH_COUNTS[surah]` (الفاتحة 7، البقرة 286، ...).

### 7.4 الحماية من الخطأ
9. **لا تُضِف تفاسير جديدة** بدون اعتماد المركز.
10. **لا تُعدّل النصوص الموجودة** بدون مراجعة شرعية.
11. **رسائل الخطأ بالعربية الفصحى** عند تجاوز الحدود ("السورة 1 تحوي 7 آيات فقط، الرقم 8 خارج النطاق").

### 7.5 نسبة المصدر إلزامية
نص النسبة لكل تفسير (يجب أن تظهر حرفياً في كل رد):
```
tabary    → "تفسير الإمام الطبري (جامع البيان)، أبو جعفر الطبري (ت. 310هـ)"
katheer   → "تفسير ابن كثير، أبو الفداء إسماعيل بن كثير (ت. 774هـ)"
baghawy   → "تفسير البغوي (معالم التنزيل)، الحسين بن مسعود البغوي (ت. 510هـ)"
saadi     → "تيسير الكريم الرحمن، عبد الرحمن بن ناصر السعدي (ت. 1376هـ)"
moyassar  → "التفسير الميسر، مجمع الملك فهد لطباعة المصحف الشريف"
```

---

## 8. أمثلة عملية (Few-shot examples)

### مثال 1: دالة أداة (style مرجعي)
```python
# في src/tafsir/tools/ayah.py
from typing import Annotated, Literal
from pydantic import Field, validate_call
from tafsir.db import query_one, query_all
from tafsir.models import AyahReference
from tafsir.normalize import reconstruct_ayah


@validate_call
def get_ayah(
    surah: Annotated[int, Field(ge=1, le=114, description="رقم السورة")],
    ayah: Annotated[int, Field(ge=1, description="رقم الآية")],
    include: list[Literal["text", "tajweed", "irab"]] = ["text"],
) -> dict:
    """جلب نص آية مع خيارات إضافية.
    
    Args:
        surah: Surah number (1-114).
        ayah: Ayah number within the surah.
        include: Which extras to fetch (tajweed/irab).
    """
    # validate via AyahReference (checks ayah <= surah length)
    AyahReference(surah=surah, ayah=ayah)
    
    rows = query_all(
        "SELECT word, wordNo FROM word_content_rasm "
        "WHERE surahNo = ? AND ayahNo = ? ORDER BY wordNo",
        (surah, ayah),
    )
    text = reconstruct_ayah(rows)
    
    result: dict = {
        "surah": surah,
        "ayah": ayah,
        "text": text,
        "tajweed": None,
        "irab": None,
        "word_count": len(rows),
    }
    
    if "tajweed" in include:
        row = query_one(
            "SELECT tajweed FROM ayah_content_tajweed "
            "WHERE surahNo = ? AND ayahNo = ?",
            (surah, ayah),
        )
        result["tajweed"] = row["tajweed"] if row else None
    
    if "irab" in include:
        row = query_one(
            "SELECT irabAyah1 FROM ayah_content_irab "
            "WHERE surahNo = ? AND ayahNo = ?",
            (surah, ayah),
        )
        result["irab"] = row["irabAyah1"] if row else None
    
    return result
```

### مثال 2: تسجيل أدوات (style معتمد)
```python
# في src/tafsir/tools/ayah.py — نهاية الملف
def register(mcp):
    """Register all ayah-level tools with the MCP server."""
    annotations = {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    }
    mcp.tool(name="fetch_ayah", annotations=annotations)(get_ayah)
    mcp.tool(name="fetch_tafsir", annotations=annotations)(get_ayah_tafsir)
    mcp.tool(name="fetch_nuzool_reason", annotations=annotations)(get_ayah_nuzool)
```

### مثال 3: db.py (read-only + parametrized)
```python
# في src/tafsir/db.py
import os
import sqlite3
from pathlib import Path

TAFSIR_KEYS = ("sura", "aya")          # tafsir_* tables
STANDARD_KEYS = ("surahNo", "ayahNo")  # everything else


class QuranDataError(Exception):
    """يُرفع عند خطأ في قراءة قاعدة بيانات القرآن."""


def get_connection() -> sqlite3.Connection:
    path = Path(os.environ.get("TAFSIR_DB_PATH", "data/quran.db"))
    if not path.exists():
        raise FileNotFoundError(
            f"قاعدة البيانات غير موجودة: {path}. "
            "ضع quran.db في data/ أو حدّد TAFSIR_DB_PATH."
        )
    conn = sqlite3.connect(
        f"file:{path}?mode=ro",
        uri=True,
        check_same_thread=False,
    )
    conn.execute("PRAGMA query_only = ON")
    conn.row_factory = sqlite3.Row
    return conn


def query_one(sql: str, params: tuple = ()) -> dict | None:
    conn = get_connection()
    try:
        row = conn.execute(sql, params).fetchone()
        return dict(row) if row else None
    except sqlite3.DatabaseError as e:
        raise QuranDataError(f"خطأ في الاستعلام: {e}") from e
    finally:
        conn.close()
```

### مثال 4: قالب Pydantic
```python
# في src/tafsir/models.py
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field, field_validator

SURAH_AYAH_COUNTS = {1: 7, 2: 286, 3: 200, ...}  # 114 entries


class AyahReference(BaseModel):
    surah: int = Field(ge=1, le=114, description="رقم السورة")
    ayah: int = Field(ge=1, description="رقم الآية")

    @field_validator("ayah")
    @classmethod
    def check_within_surah(cls, v: int, info) -> int:
        surah = info.data.get("surah")
        if surah and v > SURAH_AYAH_COUNTS[surah]:
            raise ValueError(
                f"السورة {surah} تحتوي على {SURAH_AYAH_COUNTS[surah]} آية فقط، "
                f"الرقم المُدخل {v} خارج النطاق."
            )
        return v


class TafsirSource(str, Enum):
    tabary = "tabary"
    katheer = "katheer"
    baghawy = "baghawy"
    saadi = "saadi"
    moyassar = "moyassar"
    mukhtasar_ar = "mukhtasar_ar"
    mukhtasar_en = "mukhtasar_en"
    mukhtasar_bn = "mukhtasar_bn"


TAFSIR_ATTRIBUTIONS: dict[TafsirSource, str] = {
    TafsirSource.tabary: "تفسير الإمام الطبري (جامع البيان)، أبو جعفر الطبري (ت. 310هـ)",
    TafsirSource.saadi: "تيسير الكريم الرحمن، عبد الرحمن بن ناصر السعدي (ت. 1376هـ)",
    # ... باقي الستة
}
```

### مثال 5: اختبار style معتمد
```python
# في tests/test_db_and_models.py
import pytest
from pydantic import ValidationError
from tafsir.models import AyahReference


def test_ayah_reference_rejects_surah_zero():
    with pytest.raises(ValidationError):
        AyahReference(surah=0, ayah=1)


def test_ayah_reference_rejects_ayah_exceeding_surah_length():
    """الفاتحة 7 آيات، فالرقم 8 يجب أن يُرفض."""
    with pytest.raises(ValidationError) as exc:
        AyahReference(surah=1, ayah=8)
    assert "7 آية فقط" in str(exc.value)


def test_ayah_reference_accepts_valid():
    ref = AyahReference(surah=2, ayah=255)  # آية الكرسي
    assert ref.surah == 2
    assert ref.ayah == 255
```

---

## 9. مفردات وتعابير متّفق عليها

### 9.1 مصطلحات قرآنية (تظهر في الكود والوثائق)

| العربية | الإنجليزية (في الكود) | المعنى |
|---|---|---|
| سورة | surah | الفصل (114 منها) |
| آية | ayah | الوحدة الأصغر (6,236 منها) |
| كلمة | word | كل كلمة في الرسم العثماني (77,432) |
| رسم عثماني | rasm | شكل كتابة المصحف |
| تجويد | tajweed | أحكام تلاوة |
| إعراب | irab | تحليل نحوي |
| صرف | sarf | تحليل صرفي |
| جذر | root | الجذر اللغوي (1,891 جذراً) |
| تفسير | tafsir | شرح علمي للآية |
| سبب نزول | nuzool/nozool | الحدث الذي نزلت لأجله الآية |
| إسناد | isnad | سلسلة الرواة |
| متن | matn | النص بعد الإسناد |
| قراءات | qeraat | اختلاف القراء السبع/العشر |
| مكي | makki | نزل قبل الهجرة |
| مدني | madani | نزل بعد الهجرة |
| صفحة المصحف | mushaf page | (604 صفحة في الطبعة المدنية) |
| فوائد | fawaed | استنباطات علمية من الصفحة |

### 9.2 مصطلحات تقنية معتمدة

| المصطلح | الاستخدام |
|---|---|
| **MVP** | الإصدار الأدنى القابل للعمل (5 أدوات أساسية) |
| **Plan Mode** | وضع Claude Code (Shift+Tab) — يعرض الخطة قبل التنفيذ |
| **Checkpoint** | نقطة تحقق بعد كل خطوة (✅) |
| **Prompt N** | برومبت معدّ مسبقاً يُلصق في Claude Code (Prompt 1, 2, ...) |
| **schema-first** | فحص أعمدة DB الفعلية قبل كتابة استعلامات |
| **agentic test** | اختبار يستدعي عدة أدوات في تسلسل |
| **register pattern** | تسجيل برمجي للأدوات/القوالب |

### 9.3 العبارات الفنية المتكررة في المحادثة

- **"اعرض الخطة أولاً ثم نفّذ"** — قبل أي تعديل كبير
- **"35/35 ✓"** — صيغة الإبلاغ عن نجاح الاختبارات
- **"المهمة مكتملة ✅"** — صيغة الإبلاغ القياسية
- **"الحماية من الهلوسة"** — أهم اختبار شرعي للمشروع

---

## 10. الأسئلة المعلقة والمشكلات المعروفة

### 10.1 معلّق — يحتاج قراراً
| البند | الحالة | الإجراء المطلوب |
|---|---|---|
| **إنشاء منظمة GitHub `tafsir-center`** | لم تُنشأ بعد | نشر مرحلي تحت `ah-vb-cod`، نقل لاحقاً |
| **حساب Hugging Face للـDB** | لم يُحدد | الخيار الافتراضي: `huggingface.co/ah-vb-cod` مؤقتاً |
| **التحقق من توفر اسم `tafsir-mcp` على PyPI** | لم يُجرَ | فتح `https://pypi.org/project/tafsir-mcp/` للتأكد |
| **إجازة شرعية رسمية مكتوبة من المركز** | البيانات معتمدة شفهياً ("اعتبرها معتمدة") | الحصول على بيان رسمي للنشر |
| **شعار المشروع وألوان المركز** | غير محدد | الحصول على Brand kit من المركز |

### 10.2 مهام تقنية متبقية للوصول لـ v1.0 منشورة
1. ⏳ إعادة تسمية الحزمة: `quranic_scholar` → `tafsir`
2. ⏳ إنشاء `data_loader.py` للتحميل التلقائي من Hugging Face
3. ⏳ رفع `quran.db` على Hugging Face Datasets
4. ⏳ تحديث `pyproject.toml` (الاسم، الإصدار، scripts entry)
5. ⏳ كتابة `Dockerfile` متعدد المراحل
6. ⏳ إعداد `.github/workflows/test.yml` و `publish.yml`
7. ⏳ كتابة `LICENSE` + `LICENSE-DATA`
8. ⏳ كتابة `README.md` ثنائي اللغة احترافي
9. ⏳ النشر على PyPI
10. ⏳ PR للتسجيل في MCP Registry
11. ⏳ إنشاء GitHub Release v1.0.0

### 10.3 مشاكل معروفة في DB (محفوظة عمداً)
- ❗ `word_statistics.repeatitionCount` مهجأ خطأ — يُترك كما هو في SQL، يُطبَّع في Python output
- ❗ مفاتيح مزدوجة: `sura/aya` للتفاسير الخمسة، `surahNo/ayahNo` للباقي — يُحَلّ بثوابت `TAFSIR_KEYS` و `STANDARD_KEYS`
- ❗ `mokhtasar_fawaed` يحوي عدة صفوف لكل صفحة → استخدام `fetchall()` لا `fetchone()`
- ❗ `qeraat_info.content` بتنسيق `@قارئ/نص@` — يُرجع raw، parser منفصل لاحقاً
- ❗ أسباب النزول متاحة لـ201 آية فقط — `available: false` للباقي

### 10.4 ميزات مستقبلية (Phase 2+)
- 🔮 Streamable HTTP transport (للاستضافة السحابية)
- 🔮 OAuth 2.1 (لاستخدام مؤسسي)
- 🔮 استضافة عامة على fly.io/Railway
- 🔮 واجهة Mushaf Viewer (MCP Apps)
- 🔮 تكامل مع مصدر صوتي للتلاوة (everyayah.com)
- 🔮 parser قراءات منفصل (`parse_qeraat()`)
- 🔮 إضافة لغات إضافية للمختصر (تركي، فارسي، أوردو)

---

## 11. Onboarding Prompt (للصق في أي شات/نموذج جديد)

```markdown
أنت مساعد متخصص في مشروع `tafsir-mcp` — خادم Model Context Protocol مفتوح المصدر، 
يوفّر وصولاً علمياً موثقاً للقرآن الكريم برعاية مركز تفسير للدراسات القرآنية 
(https://tafsir.net).

## السياق الكامل

**أنا:** Ahmed Eid، باحث في مركز تفسير. GitHub: ah-vb-cod، البريد: cloud@tafsir.net.
**جهازي:** macOS Apple Silicon 26.4.1.
**لغتي:** عربية أساساً مع مصطلحات تقنية إنجليزية.

**حالة المشروع:** جاهز تقنياً 100% (35/35 اختبار ناجح، 13 أداة MCP مسجَّلة، 3 موارد، 
5 قوالب). متبقّي: إعادة التسمية من `quranic-scholar-mcp` إلى `tafsir-mcp`، رفع DB 
على Hugging Face، النشر على PyPI، التسجيل في MCP Registry.

## المكدّس
Python 3.12 + uv 0.11.7 + FastMCP (mcp[cli] >= 1.27.0) + SQLite/FTS5 + Pydantic v2 
+ pyarabic. اختبار: pytest. جودة: ruff + mypy.

## البيانات (224MB SQLite)
- 114 سورة، 6,236 آية، 77,432 كلمة، 1,891 جذراً
- 5 تفاسير كاملة: الطبري (310هـ)، ابن كثير (774هـ)، البغوي (510هـ)، السعدي (1376هـ)، 
  الميسر (مجمع الملك فهد) — كلٌّ 6,236 صف
- المختصر في التفسير بـ3 لغات (عربي/إنجليزي/بنغالي)
- إعراب وتجويد كل آية + إعراب وصرف وجذر كل كلمة
- 201 آية لها أسباب نزول بالإسناد الكامل
- اختلاف القراءات لكل كلمة

**مصدر البيانات:** مركز تفسير للدراسات القرآنية — معتمدة سلفاً.

## النمط المعماري الإلزامي

1. **التسجيل البرمجي** للأدوات (لا decorators مباشرة):
   - في tools/X.py: عرّف دوال Python عادية
   - في نهاية الملف: `def register(mcp): mcp.tool(name="...")(fn)`
   - server.py يستدعي `X.register(mcp)` لكل ملف
   
2. **اسم MCP قد يختلف عن اسم Python**: Python `get_ayah` → MCP `fetch_ayah`

3. **Pydantic v2 Annotated pattern** (لا تستخدم `Field(default=...)` لأنه ينتج 
   FieldInfo bug):
   ```python
   def fn(surah: Annotated[int, Field(ge=1, le=114)] = 1, ...): ...
   ```

4. **DB read-only**: `sqlite3.connect(f"file:{path}?mode=ro", uri=True)` + 
   `PRAGMA query_only = ON`

5. **مفاتيح SQL المزدوجة**:
   - `TAFSIR_KEYS = ("sura", "aya")` — للتفاسير الخمسة
   - `STANDARD_KEYS = ("surahNo", "ayahNo")` — لكل ما عداها

6. **Parametrized SQL إلزامي**: `?` placeholders، لا f-strings أبداً.

## القيود الصارمة (لا تُكسر)

1. **لا توليد محتوى ديني.** الأدوات تُرجع النصوص حرفياً من DB.
2. **نسبة كل تفسير لقائله** مع اسم الكتاب وسنة الوفاة (نصوص النسبة جاهزة في 
   `TAFSIR_ATTRIBUTIONS`).
3. **حفظ الإسناد كاملاً** في أسباب النزول — لا تشذيب.
4. **التحقق من 114 سورة و6,236 آية** — رفض أي رقم خارج النطاق.
5. **رسائل خطأ بالعربية الفصحى.**

## أسلوب التواصل المفضّل لديّ

- **الكود/الإجراء أولاً، الشرح ثانياً.**
- **جداول مرتبة + ✅/❌ + code blocks مع لغة محددة.**
- **خطوات قابلة للنسخ مباشرة** (copy-pasteable على macOS).
- **"اعرض الخطة أولاً ثم نفّذ"** قبل أي تعديل كبير.
- **سرعة + دقة** — أكره الحشو والتكرار.
- **macOS-specific commands** عند الحاجة (Apple Silicon paths، `~/.cache`، إلخ).

## مفردات أستخدمها

- "المهمة مكتملة ✅"
- "35/35 ✓"
- "Plan Mode"
- "Checkpoint"
- "register pattern"
- "الحماية من الهلوسة"
- مصطلحات قرآنية بالعربية: سورة، آية، كلمة، رسم، تجويد، إعراب، صرف، جذر، تفسير، 
  سبب نزول، إسناد، قراءات، مكي، مدني.

## ما يجب أن تفعله الآن

1. اقرأ هذا السياق كاملاً.
2. إذا طلبت مهمة، اعرض **الخطة أولاً** (مع الملفات التي ستُعدَّل والنتيجة المتوقعة).
3. التزم بكل **القيود الصارمة** والنمط المعماري.
4. لا تخمّن أسماء أعمدة DB — إن لزم، اقترح فحصاً عبر `PRAGMA table_info()`.
5. لكل أداة جديدة: docstring عربي + Args إنجليزية + annotations كاملة + 
   اختبار pytest واحد على الأقل.
6. أرجع التقرير في صيغة جدول `الملف | الحالة` + رقم commit.

تم. أبلغني بما تريد العمل عليه.
```

---

## 📌 ملحقات سريعة

### A. أوامر macOS التي يستخدمها صاحب المشروع
```bash
# تشغيل الخادم محلياً
cd ~/projects/quranic-scholar-mcp
uv run mcp dev src/quranic_scholar/server.py

# الاختبارات
uv run pytest tests/ -v

# تسجيل في Claude Code
claude mcp add quranic-scholar --scope user -- \
    uv --directory $(pwd) run quranic-scholar-mcp

# قائمة الخوادم
claude mcp list

# التحقق من أعمدة جدول
uv run python -c "
import sqlite3
conn = sqlite3.connect('data/quran.db')
for col in conn.execute('PRAGMA table_info(tafsir_saadi)').fetchall():
    print(col)
"
```

### B. ملف `CLAUDE.md` الحالي (مرجع كامل)
موجود في جذر المشروع. يحتوي على القواعد الصارمة، schema، نصوص نسبة التفاسير. **هذا الملف يُقرأ تلقائياً من Claude Code في كل جلسة.**

### C. الإحصاءات الناجحة من الاختبار النهائي
- آية الكرسي (2:255): استرجع 3 تفاسير بنسبة كاملة لكل مفسر
- جذر "صبر": 103 ورود، 45 سورة، 93 آية، 35 صيغة مختلفة
- اختبار الحماية: رفض "البقرة آية 300" بأمانة (البقرة 286 آية)
- اختبار agentic لـ"اليتامى": Claude استدعى 10 أدوات في تسلسل صحيح وأنتج تقريراً علمياً منظماً

---

> **ملاحظة ختامية:** هذا المستند يُحدَّث مع كل قرار جوهري جديد. عند تعديله، اذكر التاريخ في رأس الملف، واحفظ نسخة سابقة في `docs/context-pack-archive/`.
