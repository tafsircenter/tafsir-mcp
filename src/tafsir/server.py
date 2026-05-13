"""FastMCP entry point for Tafsir MCP Server — 13 tools, 3 resources, 5 prompts."""

from mcp.server.fastmcp import FastMCP

from tafsir.prompts import study as study_prompts
from tafsir.resources import catalogs
from tafsir.tools import ayah as ayah_tools
from tafsir.tools import qeraat as qeraat_tools
from tafsir.tools import search as search_tools
from tafsir.tools import stats as stats_tools
from tafsir.tools import surah as surah_tools
from tafsir.tools import word as word_tools

mcp = FastMCP(
    "Tafsir MCP",
    instructions=(
        "خادم MCP للوصول العلمي الموثّق إلى القرآن الكريم — برعاية مركز تفسير للدراسات القرآنية. "
        "يوفر 13 أداة + 3 موارد + 5 قوالب دراسة.\n\n"
        "الأدوات:\n"
        "• fetch_ayah — نص آية بالرسم العثماني مع تجويد/إعراب اختياري\n"
        "• fetch_tafsir — تفاسير الطبري/ابن كثير/البغوي/السعدي/الميسر والمختصر\n"
        "• fetch_nuzool_reason — سبب نزول الآية إن ثبت\n"
        "• fetch_surah_info — معلومات السورة الكاملة\n"
        "• analyze_word — تحليل كلمة: معنى/إعراب/صرف/إحصاء/قراءات\n"
        "• find_root_occurrences — مواضع جذر في القرآن\n"
        "• get_root_stats — إحصاءات جذر\n"
        "• get_qeraat_variants — القراءات المختلفة لآية أو كلمة\n"
        "• search_quran_text — بحث FTS5 في نصوص الآيات\n"
        "• search_in_tafsir — بحث في متن تفسير محدد\n"
        "• get_quran_overview — إحصاءات عامة للقرآن\n"
        "• get_page_fawaed — فوائد صفحة من المصحف\n"
        "• get_surah_statistics — إحصاءات مفصّلة لسورة\n\n"
        "الموارد:\n"
        "• quran://surahs — فهرس 114 سورة\n"
        "• quran://tafsirs — فهرس 8 مصادر تفسيرية\n"
        "• quran://schema — توثيق مخطط قاعدة البيانات\n\n"
        "القوالب: study_ayah، compare_tafsirs، root_study، surah_overview، tajweed_lesson\n\n"
        "جميع النصوص تُعاد حرفياً من قاعدة البيانات بدون تلخيص أو تعديل."
    ),
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
