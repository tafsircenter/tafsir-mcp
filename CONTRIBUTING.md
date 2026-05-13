# المساهمة | Contributing

نرحب بالمساهمات من المطوّرين والباحثين.

## أنواع المساهمات المرحب بها

- 🐛 تقارير الأخطاء (tool bugs, edge cases, validation gaps)
- 📝 تحسين الوثائق والترجمات
- 🧪 إضافة اختبارات (أدوات غير مغطاة، حالات حدية)
- ⚡ تحسين الأداء (استعلامات SQL، تخزين مؤقت)

## ما لا نقبله بدون تنسيق مسبق

- ❌ تعديل محتوى التفاسير أو النصوص القرآنية — يتطلب مراجعة علماء المركز
- ❌ إضافة تفاسير جديدة — يجب اعتمادها أولاً من المركز
- ❌ تغيير نمط نسب المصادر (`TAFSIR_ATTRIBUTIONS`) بدون موافقة

## خطوات المساهمة

```bash
# 1. Fork المستودع وانسخه محلياً
git clone https://github.com/YOUR_USERNAME/tafsir-mcp
cd tafsir-mcp

# 2. ضع قاعدة البيانات (أو اضبط متغير البيئة)
export TAFSIR_DB_PATH=/path/to/quran.db

# 3. ثبّت المتطلبات
uv sync

# 4. أنشئ branch جديداً
git checkout -b feat/your-feature

# 5. أجرِ تغييراتك مع اختبارات
uv run pytest tests/ -v     # يجب: 35/35
uv run ruff check src/      # يجب: no errors

# 6. افتح Pull Request
```

## تنسيق رسائل الـ Commit

نتبع [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: ميزة جديدة
fix: إصلاح خطأ
docs: توثيق فقط
test: اختبارات فقط
refactor: إعادة هيكلة بدون تغيير وظيفي
perf: تحسين أداء
```

## القواعد الصارمة (CLAUDE.md)

راجع [CLAUDE.md](CLAUDE.md) — لا سيما:
- لا توليد محتوى ديني — البيانات تُعاد حرفياً
- `Annotated[T, Field()]` لا `T = Field(default=...)` في معاملات الأدوات
- SQL بـ `?` placeholders فقط — لا f-strings

## التواصل

- المشاكل التقنية: [GitHub Issues](https://github.com/ah-vb-cod/tafsir-mcp/issues)
- الاستفسارات العلمية: cloud@tafsir.net
