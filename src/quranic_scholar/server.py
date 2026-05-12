"""FastMCP entry point for Quranic Scholar MCP Server."""

from mcp.server.fastmcp import FastMCP

from quranic_scholar.tools import ayah as ayah_tools
from quranic_scholar.tools import surah as surah_tools

mcp = FastMCP(
    "Quranic Scholar",
    instructions=(
        "خادم MCP للوصول العلمي إلى القرآن الكريم بلا اتصال بالإنترنت. "
        "يوفر: نصوص الآيات بالرسم العثماني، التفاسير الكلاسيكية الخمسة "
        "(الطبري، ابن كثير، البغوي، السعدي، الميسر)، التجويد، الإعراب، "
        "أسباب النزول، وإحصاءات السور. "
        "جميع النصوص تُعاد حرفياً من قاعدة البيانات بدون تلخيص أو تعديل."
    ),
)

ayah_tools.register(mcp)
surah_tools.register(mcp)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
