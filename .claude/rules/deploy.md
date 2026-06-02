# Rules — عند لمس `deploy/`

- الإنتاج على Fly.io فقط. الـimage يَخبز DB كاملة (تُنزَّل من HF وقت البناء، لا تنزيل وقت التشغيل).
- استخدم `@mcp.custom_route` لـ HTTP endpoints (لا Starlette wrapper — GitHub Issue #1467).
- قبل أي `flyctl deploy`: حدّث `STATE.md` بـ«آخر image ناجح» كخطّ نجاة للـrollback.
- بعد النشر: تحقّق `/health` (200) + handshake، ثم **24 ساعة مراقبة** قبل أي نشر آخر.
- `mcp.tafsir.net` هو العنوان الرسمي؛ `tafsir-mcp.fly.dev` احتياطي خفي لا يُنشر علنًا.
- النشر بيد المالك (Model A) — المبرمجون يرسلون PRs فقط.
