# Rules — عند لمس `SERVER_INSTRUCTIONS` (server.py)

- الميثاق نصّ حسّاس يحكم سلوك LLM. لا تعدّله بدون جلسة تصميم منفصلة.
- أيّ تعديل يستوجب تحديث `docs/ADR/0003-display-protocol-v1.2.md` (أو ADR جديد إن كان تغييرًا جوهريًّا).
- تحقّق بعد النشر: `curl … initialize | grep 'كيف تفضّل عرضه'` يجب أن يطبع (توقيع بقاء v1.2).
- الطول الحالي مرجعيًّا: 4384 codepoint. عُدّ codepoints (Python `len()`) لا bytes (`wc -c`).
