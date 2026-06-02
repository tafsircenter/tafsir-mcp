# Skill — Stabilize (ميكرو-دورة الطور 3)

إصلاح بندٍ **واحد** في كل مرة، يمرّ بدورة كاملة كأنه ميزة. لا تجمّع إصلاحَين في commit/نشر واحد.

1. **plan (5):** الملفات بالضبط · الاختبارات (وحدة + حُرّاس) · أمر النشر · rollback · آخر image ناجح · معيار النجاح. اعرضها وانتظر ACK.
2. **implement (6):** فرع `fix/<slug>` من main نظيف · تعديل ذرّي · Conventional Commit.
3. **test (7):** `uv run pytest tests/ -q` + ruff + mypy + smoke محلي (`/health` 200، `/mcp` 406).
4. **review (8):** self-diff → PR → انتظار CI → مراجعة المالك.
5. **refactor (9):** تنظيف الأسماء/التعليقات/الكود الميت قبل الدمج.
6. **document (10):** سجلّ `sessions/YYYY-MM-DD_<slug>.md` + تحديث `STATE.md`.
7. **deploy (11):** `flyctl deploy --remote-only` + تحقّق.
8. **monitor (12):** `flyctl logs` + health، **24 ساعة** قبل الإصلاح التالي.

قواعد: أمر واحد كل مرة · `git add <مسار محدّد>` لا `-A` · لا تلمس منطقة «لا تلمس» (انظر `STATE.md`).
