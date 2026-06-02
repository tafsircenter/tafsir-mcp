# Rules — عند لمس `src/tafsir/tools/`

- أسماء أدوات MCP الـ13 ثابتة. تغيير أيّ منها = كسر كل عميل مربوط.
- حقول `text` تُعاد حرفيًّا. لا تلخيص، لا إعادة صياغة، لا حذف.
- خرائط المفاتيح: `(sura, aya)` للتفاسير الخمسة الكلاسيكية، `(surahNo, ayahNo)` للباقي (و`QuranTafseer`). الخلط = خطأ صامت كارثي.
- استخدم `Annotated[int, Field(ge=..., le=...)]` لا `Field()` كقيمة افتراضية (يُنتج FieldInfo).
- كل أداة تُسجَّل عبر `register(mcp)` لا `@mcp.tool` decorator. اسم Python ≠ اسم MCP (متعمد).
- موضع اصطلاح المفتاح لكل مصدر تفسير: `_TAFSIR_SQL` (ayah.py) و`_SEARCH_TAFSIR_SQL` (search.py).
