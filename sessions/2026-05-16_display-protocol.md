# جلسة 16 مايو 2026 — ميثاق العرض في `instructions=`

> ملخص جلسة كاملة: من فكرة → تصميم → تنفيذ → اختبار → نشر على الإنتاج.
> **النتيجة:** `mcp.tafsir.net` يخدم الآن ميثاق عرض من ٩ بنود لكل عميل HTTP.

---

## ١. الهدف

طلب المالك ٣ متطلبات في رسالة واحدة:

1. **تنبيه "النص مقتبس"** عند عرض غير كامل + اقتراح طلب الأصل.
2. **تجزئة النص الطويل** على رسالتين مع إعلام المستخدم.
3. **حد ٢٠ طلب/ساعة لكل عميل** (IP أو MAC).

---

## ٢. التحليل المعماري

### الطبقات السبع في MCP (مايو ٢٠٢٦)

| # | الطبقة | الموقع | الجمهور | تأثير على المخرجات |
|---|---|---|---|---|
| 1 | `CLAUDE.md` | جذر المشروع | Claude Code (تطوير) | ❌ لا يصل للمستخدم |
| 2 | **`instructions=`** | `server.py` | LLM عبر system prompt | ⭐⭐⭐⭐ الأقوى عام |
| 3 | Tool metadata (docstring + annotations + title) | `tools/*.py` | LLM (متى يستدعي) | ⭐⭐ متوسط |
| 4 | MCP Prompts (`@mcp.prompt`) | `prompts/*.py` | المستخدم يختار يدوياً | ⭐⭐⭐ مباشر |
| 5 | `outputSchema` + `structuredContent` | `tools/*.py` | LLM + العميل | ⭐⭐⭐⭐ سياقي قوي |
| 6 | Resource Links | tool return | العميل (يحمّل عند الحاجة) | ⭐⭐ context savings |
| 7 | Elicitation | `tools/*.py` | المستخدم (يؤكد) | ⭐⭐⭐⭐ تفاعلي |

### القرار النهائي: نسبة المسؤوليات

| الطلب | الطبقة | السبب |
|---|---|---|
| تنبيه الاقتباس | #2 `instructions=` | إلزام سلوكي على LLM |
| تجزئة طويلة | #2 (شرطي) + #3/#5 مستقبلاً | بنية في `instructions` بصيغة شرطية، تنفيذ قهري لاحقاً عبر `display.py` |
| Rate limit 20/h | **`deploy/server_http.py` middleware** | معماري — ليس في tool logic |

### لماذا لا MAC address؟

- MAC غير متاح في MCP أصلاً — لا stdio (no network) ولا HTTP (طبقة 2)
- البديل العملي: **per-IP** في HTTP mode (متاح في Fly.io)
- **اليوم:** stdio per-process (كل عميل له bucket مستقل تلقائياً)

### مرجعية المعمار

سياق المشروع (`tafsir-mcp-context-pack-v3.md`):
- Hard Constraint #7: `@mcp.custom_route` لـ HTTP endpoints (لا Starlette wrapper — Issue #1467)
- "السيناريو ب: علني مع rate limiting" قرار سابق للمالك

أبحاث مايو ٢٠٢٦:
- OWASP MCP Security Guide (فبراير ٢٠٢٦): rate limiting في transport/middleware layer
- Apigene: "Tools with complete descriptions have 3-4x fewer failed invocations"

---

## ٣. ميثاق العرض — البنود التسعة

```
خادم Tafsir MCP — وصول علمي موثّق إلى القرآن الكريم والتفسير
برعاية مركز تفسير للدراسات القرآنية.

# English summary
[7 lines covering verbatim, no paraphrase, warning protocol, metadata fields]

# ميثاق العرض والاستخدام

## ١. النص الأصلي حرفي
- لا تلخيص / إعادة صياغة / حذف / ترتيب جديد / إضافة شرح داخلي

## ٢. التحذير عند الاقتباس أو الاختصار
الصياغة الإلزامية الحرفية:
⚠️ النص أدناه مقتبس وليس النص الأصلي الكامل من المصدر.
للنص الأصلي حرفياً، أرسل: «أعد النص الأصلي كاملاً» وسأرسله لك حرفياً.

## ٣. طلب النص الأصلي الكامل
عند: «أعد النص الأصلي كاملاً» → استدعِ نفس الأداة، اعرض حقل text كاملاً.

## ٤. النصوص الطويلة
شرطي: إذا has_long_text=true أو part_info.is_split=true
1) اعرض الجزء الموجود كاملاً
2) اختم: «النص الأصلي طويل، أرسلت هذا الجزء كاملاً. لإكماله أرسل: «الجزء التالي»»
3) عند طلب «الجزء التالي» → نفس الأداة، part=1→2
4) لا تخترع البقية من ذاكرتك

## ٥. نسبة التفسير إلزامية
حقل attribution — لا تحذفه ولو عند الاختصار.

## ٦. أسباب النزول
في fetch_nuzool_reason: حقل text يحوي الإسناد والمتن.
اعرضه كاملاً عند طلب الأصل، لا تختصر الإسناد.

## ٧. لا توليد ديني من الذاكرة
لا تفسير/سبب نزول/آية/تجويد لم يأت من الأدوات.

## ٨. عند الخطأ أو رفض الخدمة
- ValidationError → أبلغ بالنص العربي
- HTTP errors (مثل 429) → أبلغ + اذكر Retry-After
- لا تستبدل النص من الذاكرة

## ٩. حقول metadata في الردود
الحقول التي تبدأ بـ _ (مثل _display, _rate_limit)
أو تنتهي بـ _info (مثل part_info) → إرشاد لك، لا تعرضها للمستخدم.
```

**الإحصاءات:**
- الحجم: 3115 حرف
- ضمن المدى الآمن < 2000 توكن
- 9 أقسام مرقّمة + English summary

---

## ٤. التغييرات في الكود

### الملف الوحيد المعدَّل: `src/tafsir/server.py`

**قبل (78 سطر):**
```python
mcp = FastMCP(
    "Tafsir MCP",
    instructions=(
        "خادم MCP للوصول العلمي الموثّق إلى القرآن الكريم..."
        # نص وصفي يشرح الأدوات والموارد فقط
        # ~1500 حرف
    ),
)
```

**بعد (149 سطر):**
```python
SERVER_INSTRUCTIONS = """خادم Tafsir MCP — وصول علمي موثّق...
[3115 حرف، 9 بنود إلزامية + English summary]
"""

mcp = FastMCP("Tafsir MCP", instructions=SERVER_INSTRUCTIONS)
```

### إحصاءات التغيير
```
2 files changed, 97 insertions(+), 25 deletions(-)
src/tafsir/server.py | 121 ++++++++++++++++++++++++++++++++++++++-----------
.gitignore           |   1 +
```

### ما لم يتغيّر
- ❌ لا تغيير في الأدوات الـ13
- ❌ لا تغيير في الموارد الـ3
- ❌ لا تغيير في القوالب الـ5
- ❌ لا تغيير في DB أو السكيما
- ❌ لا تغيير في deploy/

---

## ٥. الاختبارات

### اختبارات الوحدة (pytest)
```
35 passed in 0.25s
```
لم ينكسر اختبار واحد — التغيير string-only.

### اختبار MCP Inspector
- ✅ Connect نجح
- ✅ `initialize` response يحوي الميثاق كاملاً (3115 حرف)
- ✅ `fetch_ayah(1, 1)` يُرجع نص البسملة + word_count: 4

### اختبارات سلوكية في Claude Code (3/3)

**السيناريو ١ — تحذير الاختصار (البند ٢)**
- الطلب: "اختصر لي تفسير السعدي لآية الكرسي"
- النتيجة: ✅ بدأ ردّه حرفياً بـ `⚠️ النص أدناه مقتبس وليس النص الأصلي الكامل...`
- نسبة المؤلف موجودة: "تيسير الكريم الرحمن، السعدي، ت. 1376هـ"
- اقترح "هل تريد النص الأصلي كاملاً؟"

**السيناريو ٢ — طلب الأصل (البند ٣)**
- الطلب: "أعد النص الأصلي كاملاً"
- النتيجة: ✅ استدعى `fetch_tafsir` مجدداً، عرض النص بحرفيته
- لا تحذير `⚠️` (صحيح ميثاقياً لأنه نص أصلي لا اقتباس)
- Bonus: اعترف بخطأ مطبعي ذاتي عند ملاحظته

**السيناريو ٣ — منع التوليد (البند ٧)**
- الطلب: "ما حكم تجويد الميم في كلمة 'الرحمن'؟"
- النتيجة: ✅ صرّح: "سأستخدم أدوات Tafsir MCP... بدلاً من الإجابة من الذاكرة"
- استدعى `fetch_ayah` مرتين فعلاً
- النص الأصلي ضمن quote box مع المرجع

> ملاحظة فنية: لاحظنا تشويش في عرض Terminal للنص العربي (`الَّ`, `Which` متسرّبة).
> تأكدنا بفحص DB مباشرة: **النص في DB سليم (2859 حرف)**. المشكلة في bidi/ANSI rendering فقط.

---

## ٦. تدفق Git

```
c0fe57b (سابق)
   │
   ├─ feat/instructions-v1.1
   │     c9276a6  feat(server): strict display protocol in instructions=
   │     │
   │     └─ Push → PR #1 → Rebase merge
   │
524cb02 (HEAD → main, origin/main)
```

### الـ commit message
```
feat(server): strict display protocol in instructions=

Replaces narrative instructions with a 9-section ميثاق العرض that binds
the LLM client to:
- Show 'text' fields verbatim from the database
- Prepend exact warning sentence when abbreviating/paraphrasing
- Offer to resend the full original on user request
- Continue long-text responses across user-confirmed parts
- Always include attribution from TAFSIR_ATTRIBUTIONS
- Preserve isnad in nuzool reasons
- Never substitute religious content from LLM memory
- Pass-through error messages with retry timing
- Treat _-prefixed metadata fields as LLM guidance, not user-facing

English summary added for non-Arabic clients. Rate-limiting messaging
included conditionally (section 8) — actual enforcement deferred to
deploy/server_http.py per HTTP-middleware pattern (Issue #1467).

Verified in MCP Inspector + Claude Code:
- fetch_tafsir abbreviation -> verbatim warning + attribution ✓
- 'أعد النص الأصلي كاملاً' -> full text returned ✓
- Tajweed query -> tool invoked, no LLM-memory fallback ✓

No changes to tools, resources, or prompts. 35/35 tests pass.
```

### PR على GitHub
- **رقم:** #1
- **العنوان:** feat(server): strict display protocol in instructions=
- **حالة CI:** ✅ 2 successful checks
- **نمط الدمج:** Rebase and merge (fast-forward — يطابق سياسة المشروع)
- **بعد الدمج:** الفرع المحلي والـ remote حُذفا

---

## ٧. النشر على Fly.io

### قبل النشر
```
flyctl status --app tafsir-mcp
Image: tafsir-mcp:deployment-01KRP110H0390D44CRTP16MP72  (القديم)
Version: 2
```

### الأمر
```bash
flyctl deploy --remote-only
```

### نتائج البناء
- Builder: Depot
- Build time: 32.4 ثانية
- Image size: 182 MB
- لا cache misses كبيرة

### Rolling update
```
✔ [1/2] Cleared lease for 2863d22b45e2d8
✔ [2/2] Cleared lease for 80e473b65e7e68
```

### بعد النشر
```
flyctl status --app tafsir-mcp
Image: tafsir-mcp:deployment-01KRS3JFVSR692X0SQ8Q0RATJ8  (الجديد)
Version: 3
Machine 2863d22b45e2d8: started, 1 passing
Machine 80e473b65e7e68: stopped (auto-stop)
LAST UPDATED: 2026-05-16T19:19:29Z
```

### التحقق من الـ endpoint الإنتاجي
```bash
curl -s -X POST https://mcp.tafsir.net/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize",...}' \
  | grep -o "ميثاق العرض"

# الناتج:
ميثاق العرض   ✅
```

**الميثاق وصل لكل عميل HTTP الآن.**

---

## ٨. الأثر على المستخدمين

| نوع العميل | المسار | الميثاق وصل؟ |
|---|---|---|
| Claude.ai (Web/Desktop) عبر MCP connector | HTTP → `mcp.tafsir.net/mcp` | ✅ نعم |
| ChatGPT عبر MCP connector | HTTP → `mcp.tafsir.net/mcp` | ✅ نعم |
| Cursor / VS Code Insiders | HTTP → `mcp.tafsir.net/mcp` | ✅ نعم |
| Claude Code محلي (من المستودع) | stdio | ✅ نعم |
| `uvx tafsir-mcp` من PyPI | stdio (PyPI v1.0.0) | ⏸️ لا — PyPI ما زال قديم |

---

## ٩. ما لم يتم اليوم (مؤجَّل)

### المؤجَّل لجلسات قادمة

1. **Rate limiting (20/h أو 60/min) في `deploy/server_http.py`**
   - مكان التنفيذ: HTTP middleware (ASGI) في `streamable_http_app()`
   - الهدف: حماية `mcp.tafsir.net` من abuse
   - النمط: per-IP sliding window
   - الكود الجاهز: `rate_limiter.py` (sliding window) — لم يُضف بعد
   - قرار معلَّق: 20/h (حماية صارمة) أم 60/min (تجارب فعلية أوسع)

2. **`display.py` لتجزئة النصوص قهرياً**
   - `maybe_split_text(text, part)` → tuple[chunk, PartInfo]
   - `build_display_meta()` لحقن `_display` في ردود الأدوات الحساسة
   - الأدوات المستهدفة: `fetch_tafsir`, `fetch_nuzool_reason`, `fetch_ayah`
   - حالياً البند ٤ في الميثاق شرطي ("إذا أعادت الأداة...") — لا ضرر لأن الحقول لا تُرجع بعد

3. **PyPI v1.1.0**
   - تحديث مستخدمي `uvx tafsir-mcp` و `pip install`
   - يحتاج: bump version في `pyproject.toml` + `uv publish`

4. **GitHub Release v1.1.0**
   - توثيق رسمي للتغيير
   - changelog لـ DEPLOY.md و README.md

### المراقبة الموصاة (24 ساعة قادمة)

```bash
# logs
flyctl logs --app tafsir-mcp | tail -50

# health
flyctl status --app tafsir-mcp

# cost (في المتصفح)
# https://fly.io/dashboard/personal/billing
# تحقق Upcoming Invoice قريب من $0.07
```

### تحفظات أمنية معلَّقة

- ⚠️ Fly.io أزال Spending Limit من UI (مايو ٢٠٢٦) — حماية ضمنية فقط:
  - Resource Limit: 2/100 machines
  - `auto_stop_machines='stop'` + `min_machines_running=0`
  - أسوأ سيناريو DDoS مستمر: ~$15-30/شهر
- ⚠️ Endpoint علني بلا auth ولا rate limit حالياً — جلسة rate limiting قادمة عاجلة

---

## ١٠. الخلاصة

| المرحلة | الحالة | الوقت التقريبي |
|---|---|---|
| تحليل + تصميم + critique | ✅ | جلسة سابقة |
| كتابة الميثاق وتنقيحه | ✅ | بداية الجلسة |
| استبدال `server.py` (4 محاولات) | ✅ | 15 دقيقة |
| pytest + Inspector | ✅ | 5 دقائق |
| اختبارات Claude Code (3 سيناريوهات) | ✅ | 10 دقائق |
| commit + push + PR + merge | ✅ | 5 دقائق |
| `fly deploy` + verification | ✅ | 4 دقائق |

**الإنجاز:** ميثاق عرض من ٩ بنود يحكم سلوك LLM عند عرض النصوص الدينية، منشور على `mcp.tafsir.net` ومتاح لكل عملاء HTTP من هذه اللحظة.

---

## ١١. أوامر مرجعية للجلسات القادمة

### للتحقق من الميثاق على الإنتاج
```bash
curl -s -X POST https://mcp.tafsir.net/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' \
  | python3 -c "import sys,json; r=json.loads(sys.stdin.read().split('data: ')[-1]); print(r['result']['instructions'][:500])"
```

### للتحقق من الميثاق محلياً
```bash
uv run python -c "
from tafsir.server import mcp, SERVER_INSTRUCTIONS
print(f'length: {len(SERVER_INSTRUCTIONS)} chars')
print(f'has warning: {\"النص أدناه مقتبس\" in SERVER_INSTRUCTIONS}')
print(f'has english: {\"English summary\" in SERVER_INSTRUCTIONS}')
"
```

### للرجوع عن النشر (في حال طارئ)
```bash
# قائمة الـ releases
flyctl releases --app tafsir-mcp

# الرجوع لإصدار سابق
flyctl deploy --image tafsir-mcp:deployment-01KRP110H0390D44CRTP16MP72 --app tafsir-mcp
```

### للرجوع عن الـ commit (في حال طارئ، قبل النشر فقط)
```bash
git checkout main
git revert 524cb02
git push origin main
```

---

## ١٢. مراجع

- Commit: `524cb02` (محلي = remote، لأن الـ rebase على GitHub أعطى hash مختلف `c9276a6` للـ branch — main استخدم الـ rebased hash)
- PR: https://github.com/tafsircenter/tafsir-mcp/pull/1
- Image: `tafsir-mcp:deployment-01KRS3JFVSR692X0SQ8Q0RATJ8`
- Production endpoint: https://mcp.tafsir.net/mcp
- Health: https://mcp.tafsir.net/health

### وثائق المشروع المرتبطة
- `CLAUDE.md` — قواعد للمطورين
- `deploy/DEPLOY.md` — دليل التشغيل السحابي
- `tafsir-mcp-context-pack-v3.md` — سياق المشروع الكامل

### مرجع خارجي
- MCP spec 2025-11-25: https://modelcontextprotocol.io/specification
- FastMCP docs: https://gofastmcp.com
- Fly.io health checks behaviour (لا تعيد تشغيل المvanيكينة، توجّه الـ traffic فقط)

---

> 🌙 جلسة مباركة. الميثاق الذي صُمّم اليوم يحمي المستخدمين من تحريف أو هلوسة AI
> على نصوص شرعية. وفّق الله من شارك في الإنشاء والمراجعة والنشر.
