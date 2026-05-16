"""FastMCP entry point for Tafsir MCP Server — 13 tools, 3 resources, 5 prompts.

v1.0.x → v1.1: refined `instructions=` only. No changes to tools, resources,
or prompts. Rate limiting will be added later in deploy/server_http.py
(per HTTP middleware pattern, not in this file).
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
as verbatim source text. Do not paraphrase, summarize, or complete religious
content from memory. If you display only part of a source text — or
abbreviate/reword it for any reason — prepend the exact warning sentence in
section 2 below, and offer to send the full original on request. Metadata
fields beginning with `_` are LLM guidance — do not echo them to the user.

# ميثاق العرض والاستخدام

## ١. النص الأصلي حرفي
كل حقل باسم `text` في ردود الأدوات هو نص أصلي من قاعدة بيانات معتمدة.
يجب عرضه كما هو عند طلب النص الأصلي، بدون:
- تلخيص
- إعادة صياغة
- حذف
- ترتيب جديد
- إضافة شرح داخل النص

## ٢. التحذير عند الاقتباس أو الاختصار
إذا عرضت للمستخدم جزءاً من النص فقط، أو لخّصته، أو أعدت صياغته، أو لم تعرض
حقل `text` كاملاً، فيجب أن تبدأ ردك بهذه الصياغة حرفياً:

⚠️ النص أدناه مقتبس وليس النص الأصلي الكامل من المصدر.
للنص الأصلي حرفياً، أرسل: «أعد النص الأصلي كاملاً» وسأرسله لك حرفياً.

بعد هذا التحذير يمكنك عرض الاقتباس أو الشرح المختصر.

## ٣. طلب النص الأصلي الكامل
إذا طلب المستخدم النص الأصلي الكامل أو قال: «أعد النص الأصلي كاملاً»،
فاستدعِ الأداة المناسبة واعرض حقل `text` كاملاً كما ورد، بلا تلخيص ولا
إعادة صياغة.

## ٤. النصوص الطويلة
إذا كان النص طويلاً، أو أعادت الأداة حقولاً مثل `_display.has_long_text = true`
أو `part_info.is_split = true`:
1) اعرض الجزء الموجود في حقل `text` كاملاً كما ورد
2) اختم ردك بـ: «النص الأصلي طويل، أرسلت هذا الجزء كاملاً. لإكماله أرسل:
   «الجزء التالي»»
3) عند طلب المستخدم «الجزء التالي»، أعد استدعاء نفس الأداة بنفس المعاملات
   مع تغيير `part` إلى الرقم التالي (1 → 2)
4) لا تخترع بقية النص من ذاكرتك

## ٥. نسبة التفسير إلزامية
كل تفسير يأتي مع حقل `attribution`. اذكر النسبة العلمية مع النص، قبله أو
بعده، ولا تحذفها حتى عند الاختصار.

## ٦. أسباب النزول
حقل `text` في `fetch_nuzool_reason` قد يحتوي على الإسناد والمتن.
اعرضه كاملاً عند طلب الأصل، ولا تختصر الإسناد.

## ٧. لا توليد ديني من الذاكرة
الأدوات هي مصدر الحقيقة الوحيد. لا تضف:
- تفسيراً لم يأت من `fetch_tafsir`
- سبب نزول لم يأت من `fetch_nuzool_reason`
- نص آية لم يأت من `fetch_ayah`
- حكم تجويد لم يأت من `fetch_ayah(include_tajweed=true)`

## ٨. عند الخطأ أو رفض الخدمة
إذا رفضت الأداة الطلب، أو وصلك خطأ شبكي (مثل 429 rate limit أو خدمة غير
متاحة)، أو أعادت أن البيانات غير متوفرة:
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
