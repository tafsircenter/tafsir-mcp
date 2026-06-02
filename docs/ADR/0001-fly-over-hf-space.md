# ADR-0001: استضافة الإنتاج على Fly.io بدل Hugging Face Space

- Date: 2026-05-15
- Status: Accepted

## Context
كان الإنتاج الأوّلي على Hugging Face Space (`tafsircenter-tafsir-mcp.hf.space`).
احتاج المشروع عنوانًا رسميًّا مستقرًّا قابلًا للترحيل لاحقًا (إلى Alibaba ECS في Phase 2)
دون كسر العملاء المربوطين، مع تحكّم أدقّ في الـruntime والتكلفة، وتقليل vendor lock-in.
HF Space يربط العنوان بالبنية التحتية، ويصعّب التحكّم في auto-stop والـhealth checks.

## Decision
الترحيل إلى تطبيق Fly.io باسم `tafsir-mcp` (org: personal، region: `bom`/Mumbai)،
خلف نطاق مخصّص **`mcp.tafsir.net`** (GoDaddy DNS: A + AAAA) وشهادة Let's Encrypt
تلقائية (RSA+ECDSA). النشر عبر `deploy/Dockerfile` الذي يَخبز قاعدة البيانات في الصورة
(تُنزَّل من HF Datasets وقت البناء مع تحقّق SHA256). transport = `streamable-http`.
الإعدادات: `auto_stop_machines='stop'` + `min_machines_running=0` لتوفير ~95% عند idle،
و `[[http_service.checks]]` على `/health` بـ`grace_period=15s`.

## Consequences
- ✅ عنوان رسمي ثابت `mcp.tafsir.net` يفصل العنوان عن البنية التحتية (ترحيل مستقبلي = DNS فقط).
- ✅ تكلفة متوقّعة ~$0.07–5/شهر مع auto-stop.
- ✅ تحكّم كامل في الـhealth checks والـimage.
- ⚠️ cold-start ~5–10s بعد سكون طويل (مقبول بوعي مقابل التوفير).
- ⚠️ منطقة واحدة (`bom`) → latency أعلى لمستخدمي خارج آسيا (يُعالَج لاحقًا إن لزم).
- ⚠️ النقطة عامّة بلا auth — تتطلّب rate limiting (مؤجَّل) + Spending Limit.

## Alternatives Rejected
- **البقاء على HF Space فقط:** يربط العنوان بالبنية، يصعّب الترحيل ويزيد lock-in.
- **حذف HF Space:** يُفقد commit `81e42d9` (إصلاح `transport_security` الموجود على HF فقط)
  ويُلغي إمكانية الإحياء. القرار: **إبقاؤه Private (لا حذف)** كأرشيف/fallback نظري.
- **استخدام `tafsir-mcp.fly.dev` المباشر:** يربط العنوان بمزوّد بعينه؛ النطاق المخصّص أفضل.
- **انتظار Alibaba ECS:** يُعلّق المشروع؛ استراتيجية مرحلتين أسرع.
