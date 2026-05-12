"""FastMCP entry point for Quranic Scholar MCP Server — 12 tools."""

from mcp.server.fastmcp import FastMCP

from quranic_scholar.tools import ayah as ayah_tools
from quranic_scholar.tools import qeraat as qeraat_tools
from quranic_scholar.tools import search as search_tools
from quranic_scholar.tools import stats as stats_tools
from quranic_scholar.tools import surah as surah_tools
from quranic_scholar.tools import word as word_tools

mcp = FastMCP(
    "Quranic Scholar",
    instructions=(
        "خادم MCP للوصول العلمي إلى القرآن الكريم بلا اتصال بالإنترنت. "
        "يوفر 12 أداة:\n"
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
        "• get_surah_statistics — إحصاءات مفصّلة لسورة\n"
        "جميع النصوص تُعاد حرفياً من قاعدة البيانات بدون تلخيص أو تعديل."
    ),
)

ayah_tools.register(mcp)
surah_tools.register(mcp)
word_tools.register(mcp)
qeraat_tools.register(mcp)
search_tools.register(mcp)
stats_tools.register(mcp)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
