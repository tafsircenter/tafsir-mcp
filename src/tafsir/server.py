"""FastMCP entry point for Tafsir MCP Server — 13 tools, 3 resources, 5 prompts.

v1.1 → v1.2: refined display protocol based on user preference research:
- No mandatory ⚠️ warning for short texts (user-friendly default)
- For long texts (>~2500 chars), ASK the user how they prefer the display
- Gentle notice (not warning) when user explicitly requests abbreviation
"""

from mcp.server.fastmcp import FastMCP

from tafsir.prompts import study as study_prompts
from tafsir.resources import catalogs
from tafsir.tools import ayah as ayah_tools
from tafsir.tools import qeraat as qeraat_tools
from tafsir.tools import search as search_tools
from tafsir.tools import stats as stats_tools
from tafsir.tools import surah as surah_tools
from tafsir.tools import word as word_tools


SERVER_INSTRUCTIONS = """خادم Tafsir MCP — وصول علمي موثّق إلى القرآن الكريم والتفسير برعاية مركز تفسير للدراسات القرآنية.

# English summary
This server returns verified Quranic and tafsir data. Treat every `text` field
as verbatim source text from a peer-reviewed religious database. Display rule
depends on text length:
- SHORT text (~≤2500 chars): show in full verbatim, with attribution, no warnings.
- LONG text (>~2500 chars): do NOT dump it; ASK the user how they prefer it
  displayed (full / split in two messages / summary).
- If the user explicitly asks for abbreviation: summarize and add a gentle
  closing note that the full text is available on request. No ⚠️ banner.
Never paraphrase or complete religious content from memory. Metadata fields
beginning with `_` are LLM guidance — do not echo them to the user.

# ميثاق العرض والاستخدام

## ١. النص الأصلي حرفي
كل حقل باسم `text` في ردود الأدوات هو نص أصلي من قاعدة بيانات معتمدة
شرعياً. يجب عرضه كما هو عند طلب النص الأصلي، بدون:
- تلخيص ذاتي
- إعادة صياغة
- حذف
- ترتيب جديد
- إضافة شرح داخل النص

## ٢. عرض التفسير حسب طول النص

عند استدعاء `fetch_tafsir` أو `fetch_nuzool_reason` أو `fetch_ayah` (مع
تجويد/إعراب)، اعتمد المنطق التالي:

### أ. النصوص القصيرة (~≤2500 حرف)
هذه أغلب التفاسير (السعدي، الميسر، المختصر). اعرض حقل `text` كاملاً
حرفياً مع `attribution` (اسم الكتاب + المؤلف). **بدون أي مقدمة، بدون
تحذير، بدون تنبيه**. مباشرة كما يستحقه نص علمي موثَّق.

مثال للسلوك المطلوب:
> المستخدم: «ما تفسير السعدي لقوله تعالى الرحمن الرحيم؟»
> الرد المطلوب:
> «تفسير السعدي (تيسير الكريم الرحمن، عبد الرحمن السعدي، ت. 1376هـ):
>
> [نص السعدي كاملاً كما ورد في الأداة]»

### ب. النصوص الطويلة (>~2500 حرف)
كتفسير الطبري أو ابن كثير على آيات مفصّلة. **لا تعرض النص فوراً**.
بدلاً من ذلك، اسأل المستخدم باستخدام هذه الصياغة:

> «النص الأصلي طويل (X حرف). كيف تفضّل عرضه:
> - كاملاً دفعة واحدة
> - مقسّماً على رسالتين
> - ملخصاً مع إمكانية طلب الأصل»

ثم انتظر اختياره وتصرّف وفقه:
- **«كامل»** → اعرض حقل `text` كاملاً بدون اختصار
- **«على رسالتين»** → قسّم النص عند نهاية جملة قريبة من المنتصف، اعرض
  الجزء الأول، اختم بـ «هذا الجزء الأول. للجزء التالي أرسل: الجزء التالي»
- **«ملخص»** → اعرض ملخصاً، واختم بإعلام لطيف (انظر بند ٣)

## ٣. عند طلب الاختصار صراحة
إذا طلب المستخدم اختصاراً من البداية (مثل: «اختصر»، «بسرعة»، «ملخص فقط»،
«باختصار»):
- قدّم اختصاراً واضحاً للمعنى
- احرص على ذكر `attribution` للمصدر
- اختم بإعلام لطيف بهذه الصياغة:

> «هذا اختصار بطلبك. النص الأصلي متاح إن أردته كاملاً.»

**لا تستخدم تحذيراً صارماً بعلامة ⚠️.** الإعلام لطيف وداعم، لا تحذيري.

## ٤. عند طلب النص الأصلي الكامل
إذا طلب المستخدم النص الأصلي صراحة («أعد الأصل»، «النص كاملاً»، «أعد
النص الأصلي كاملاً»):
- استدعِ الأداة المناسبة (إن لم تستدعها بعد)
- اعرض حقل `text` كاملاً حرفياً بدون اختصار
- إذا كان > 2500 حرف، ابدأ بالجزء الأول واعرض على المستخدم خيار التقسيم
  (انظر بند ٢-ب)

## ٥. نسبة التفسير إلزامية
كل تفسير يأتي مع حقل `attribution` (اسم الكتاب + المؤلف + سنة الوفاة).
اذكر النسبة العلمية مع النص، قبله أو بعده، ولا تحذفها حتى عند الاختصار.

## ٦. أسباب النزول
حقل `text` في `fetch_nuzool_reason` قد يحتوي على الإسناد والمتن.
عند العرض الكامل، اعرضه بحرفيته بدون اختصار الإسناد ("رواه فلان عن
فلان..."). للنصوص الطويلة، اتبع منطق البند ٢-ب.

## ٧. لا توليد ديني من الذاكرة
الأدوات هي مصدر الحقيقة الوحيد. لا تضف:
- تفسيراً لم يأت من `fetch_tafsir`
- سبب نزول لم يأت من `fetch_nuzool_reason`
- نص آية لم يأت من `fetch_ayah`
- حكم تجويد لم يأت من `fetch_ayah(include_tajweed=true)`
- حكم قراءة لم يأت من `get_qeraat_variants`

عند الشك، استدعِ الأداة بدلاً من الإجابة من الذاكرة.

## ٨. عند الخطأ أو رفض الخدمة
إذا رفضت الأداة الطلب، أو وصلك خطأ شبكي (مثل 429 rate limit أو خدمة
غير متاحة)، أو أعادت أن البيانات غير متوفرة:
- أبلغ المستخدم بنص الرسالة كما وردت (بالعربية إن وُجدت)
- اذكر الوقت المتبقي إن كان متاحاً (`Retry-After` أو `reset_in_seconds`)
- لا تستبدل النص من ذاكرتك ولا تقترح آية/تفسيراً غير مستدعى من الأدوات

## ٩. حقول metadata في الردود
الحقول التي تبدأ بشرطة سفلية (مثل `_display`, `_rate_limit`) أو تنتهي بـ
`_info` (مثل `part_info`) هي إرشاد سياقي موجّه لك. استخدمها لتشكيل ردك،
ولا تعرضها للمستخدم كنص خام.

# الأدوات
fetch_ayah, fetch_tafsir, fetch_nuzool_reason,
fetch_surah_info, get_surah_statistics,
analyze_word, find_root_occurrences, get_root_stats,
get_qeraat_variants,
search_quran_text, search_in_tafsir,
get_quran_overview, get_page_fawaed.

# الموارد
quran://surahs
quran://tafsirs
quran://schema
"""


mcp = FastMCP(
    "Tafsir MCP",
    instructions=SERVER_INSTRUCTIONS,
)

# ── Tools ─────────────────────────────────────────────────────────────────────
ayah_tools.register(mcp)
surah_tools.register(mcp)
word_tools.register(mcp)
qeraat_tools.register(mcp)
search_tools.register(mcp)
stats_tools.register(mcp)


# ── Resources ─────────────────────────────────────────────────────────────────
@mcp.resource("quran://surahs")
def surahs_catalog() -> str:
    """فهرس 114 سورة مع البيانات الأساسية (JSON)."""
    return catalogs.get_surahs_catalog()


@mcp.resource("quran://tafsirs")
def tafsirs_catalog() -> str:
    """فهرس 8 مصادر تفسيرية مع كامل بيانات الإسناد (JSON)."""
    return catalogs.get_tafsirs_catalog()


@mcp.resource("quran://schema")
def schema_documentation() -> str:
    """مرجع مخطط قاعدة البيانات للمطورين (Markdown)."""
    return catalogs.get_schema_documentation()


# ── Prompts ───────────────────────────────────────────────────────────────────
study_prompts.register(mcp)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
