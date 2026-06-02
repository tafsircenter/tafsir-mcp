> 🟡 **ARCHIVED** (لقطة 15 مايو 2026 — لا تُحدَّث). للحالة الحيّة الآن انظر `STATE.md` في الجذر.
> ⚠️ **تحذير دقّة:** الواجهة الموثّقة في §7.2/§7.4 لـ`fetch_ayah` **خاطئة**؛ الصحيح `include=["tajweed"]` (نوعه `list[str]`) لا `include_tajweed=True` (bool). لا تنسخ منها.

# 📦 Tafsir MCP — Context Pack v3.0 (الإصدار النهائي بعد ترحيل الإنتاج إلى Fly.io)

> وثيقة مستقلة (self-contained) تخدم جمهورَين معاً: نموذج AI يستأنف العمل، وفريق تطوير بشري يستلم المشروع.
>
> **آخر تحديث:** 15 مايو 2026 — بعد ترحيل الإنتاج من Hugging Face Space إلى Fly.io على نطاق مخصّص `mcp.tafsir.net`.
>
> **الإصدار الموثّق هنا:** v1.0.0 (Production) منشور على PyPI + GitHub + HF Datasets + Fly.io.
>
> **يحلّ محل:** Context Pack v2 (الذي وثّق نهاية مرحلة النشر على PyPI، قبل الترحيل إلى Fly.io).

---

## ١. هوية المشروع

| الحقل | القيمة |
|---|---|
| **الاسم** | `tafsir-mcp` |
| **الهدف بجملة واحدة** | خادم Model Context Protocol مفتوح المصدر يوفّر وصولاً علمياً موثّقاً إلى القرآن الكريم وخمسة تفاسير كلاسيكية وتحليل لغوي شامل لـ77,432 كلمة، **مُتاح الآن عبر MCP-over-HTTP عام على `https://mcp.tafsir.net/mcp`** ولأي مساعد ذكي يدعم MCP محلياً عبر `pip install tafsir-mcp` أيضاً. |
| **الحالة العامة** | ✅ **منشور وحيّ في الإنتاج** على ثلاث منصات: (1) PyPI كحزمة، (2) Hugging Face Datasets كمصدر للـDB، (3) Fly.io كـHTTP MCP server على نطاق `mcp.tafsir.net`. كل الأدوات الـ13 و3 موارد و5 قوالب تعمل عبر الإنترنت. 35/35 اختبار محلي ناجح. |
| **المستخدم المستهدف** | (1) طلاب العلم الشرعي. (2) الأئمة والخطباء. (3) الباحثون اللغويون. (4) مطوّرو التطبيقات الإسلامية. (5) أي LLM يحتاج نصاً قرآنياً موثّقاً بدلاً من ذاكرته (الأهم). |
| **المشكلة التي يحلّها** | المساعدات الذكية (Claude, GPT, إلخ) **تهلوس** في النصوص القرآنية — تخترع آيات، تخلط بين السور، تنسب أقوالاً لمفسرين خطأً. الـ MCP server يحوّلها من "متذكّر قد يخطئ" إلى "ناقل موثوق ومنسوب". مثال موثّق في المحادثة: عند سؤال Claude عن "آية 300 من سورة البقرة" بدون الخادم قد يخترع، **بعد الربط رفض الطلب بدقة** قائلاً: "البقرة 286 آية فقط". |
| **الجهة الراعية** | مركز تفسير للدراسات القرآنية (https://tafsir.net) |
| **المطوّر** | Ahmed Eid · `cloud@tafsir.net` · GitHub: `ah-vb-cod` (الحساب الشخصي للمطوّر، يُدير منظمة `tafsircenter`) |
| **الترخيص** | MIT (الكود) + CC BY 4.0 (المحتوى القرآني) |
| **نموذج الخدمة** (محسوم في هذه الجلسة) | **علنيّ (public) لكن مع rate limiting** (السيناريو ب). الرابط متاح للجميع كوقف/خدمة، لكن مع حماية من سوء الاستخدام (مستحقّة التنفيذ في جلسة قادمة). |

### الروابط الرسمية الحيّة
- 🐍 **PyPI:** https://pypi.org/project/tafsir-mcp/
- 🐙 **GitHub:** https://github.com/tafsircenter/tafsir-mcp
- 🤗 **Hugging Face Datasets (مصدر DB):** https://huggingface.co/datasets/tafsircenter/tafsir-mcp-data
- 🪰 **Fly.io app (HTTP MCP):** `tafsir-mcp.fly.dev/mcp` (احتياطي) + **`mcp.tafsir.net/mcp`** (الأساسي)
- 🩺 **Health endpoint:** `https://mcp.tafsir.net/health` → `{"status":"ok","service":"tafsir-mcp"}`
- 🟡 **Hugging Face Space (legacy):** `tafsircenter-tafsir-mcp.hf.space` — **ما زال علنياً، مؤقتاً، قيد الإخفاء (سيُجعل Private لا Delete)**

---

## ٢. الخط الزمني المختصر (٧ نقاط مفصلية تروي تطوّر المشروع)

1. **البداية — ملف `.db` مجهول البنية:** المالك رفع `surah_database_content.db` (224 MB SQLite) وسأل "كيف أحوّلها إلى MCP؟". الإجابة الأولية كانت خطة عامة، ثم بعد فحص الملف اكتُشف أنه **مرجع علمي ثري بنيت عليه استراتيجية كاملة**.

2. **اللحظة التحويلية — إعلان الرعاية:** المالك قال نصاً: *"أنا أعمل في مركز تفسير للدراسات القرآنية وستكون هي الجهة المتبنية للمشروع"*. هذا غيّر التصميم من "مشروع شخصي" إلى "مشروع مؤسسي بترخيص مزدوج (MIT + CC BY 4.0)".

3. **بناء MVP في ~5 ساعات:** مع Claude Code + VS Code + Plan Mode، أُنجز: 13 أداة MCP، 3 موارد، 5 قوالب، 35 اختباراً، تطبيع نص عربي، FTS5 مع 17 فهرساً.

4. **اللحظة التحويلية الثانية — اكتشاف أن Claude Desktop لا يدعم MCP في Chat:** ظهرت رسالة Anthropic الرسمية: *"Plugins run locally and aren't available in Chat. Switch to Cowork or Code to use plugins."* تحولت المنصة المستهدفة إلى **Claude Code داخل VS Code**.

5. **النشر على PyPI (نهاية مرحلة v2 من Context Pack):** رُفعت DB إلى Hugging Face مع SHA256، أُنشئت منظمة `tafsircenter` على GitHub، دُفع الكود، نُشرت الحزمة على PyPI تحت `tafsir_mcp-1.0.0`. أصبحت **متاحة للعالم بأمر `pip install tafsir-mcp`**.

6. **🆕 الترحيل من HF Space إلى Fly.io (هذه الجلسة):** أُنشئ تطبيق `tafsir-mcp` على Fly.io في منطقة `bom` (Mumbai)، مع `auto_stop_machines='stop'` و `min_machines_running=0`. أُضيف نطاق مخصّص `mcp.tafsir.net` عبر GoDaddy DNS + شهادة Let's Encrypt تلقائية (RSA+ECDSA). HF Space أُبقي كنسخة احتياطية بانتظار التأكّد من ثبات Fly.io.

7. **🆕 إضافة `/health` endpoint + Fly health checks + ملف DEPLOY.md + قرارات الخدمة العامة (المحطة الحالية):** أُضيف `@mcp.custom_route("/health")` بـ4 أسطر فقط (بعد رفض نمط Starlette wrapper الأكثر خطورة). أُعدّ Fly `[[http_service.checks]]` مع `grace_period="15s"`. كل التغييرات دُفعت إلى `origin/main` (3 commits). كُتب `DEPLOY.md` كدليل تشغيلي. ثم بُحث مع المالك سؤال جوهري: *"هل حاليا يستطيع مبرمج استخدام رابط mcp.tafsir.net/mcp في بناء تطبيق ويستغله وانا اللي ادفع اشتراك fly.io"* — قاد إلى قرار: **علنيّ مع rate limiting + Spending Limit فوري**.

---

## ٣. الخطوة التالية المباشرة (أهم سطر في الـ Pack)

> 🎯 **حيث توقفنا بالضبط:**

المالك حسم في الرسالة الأخيرة قبل توليد هذا الـ Pack:

> Q: أي نموذج تريد للخدمة؟
> A: **السيناريو ب — علنيّ لكن بحدود (rate limiting)**
>
> Q: هل تريد وضع Spending Limit في Fly.io الآن؟
> A: **نعم، فوراً (أولوية)**

والـ assistant طرح خطة 4 خطوات وأعطى تعليمات تفصيلية للخطوة الأولى. **لم يصل تأكيد إتمام الخطوة من المالك بعد**.

### المهمة المفتوحة الفورية:

**ضبط Fly.io Spending Limit يدوياً في الـ Dashboard.**

الإجراء بالضبط الذي ينتظر التأكيد:

1. فتح: `https://fly.io/dashboard/personal/billing`
2. تسجيل دخول بـ `cloud@tafsir.net` (إن لزم)
3. ضبط:
   - **Soft Limit (Alert):** `$5` — تنبيه مبكر بإيميل
   - **Hard Limit (Cutoff):** `$25` — يوقف الـmachines قاطعاً عند الوصول
4. تفعيل Email notifications على `cloud@tafsir.net`
5. **حفظ، ثم إرسال تأكيد نصيّ أو screenshot للـ AI**

### المهام التالية بالترتيب بعد التأكيد:

| # | المهمة | الوقت | الأولوية | الحالة |
|---|---|---|---|---|
| 1 | ⏳ ضبط Fly.io Spending Limit ($5/$25) | 5 دق | 🔴 فوري | بانتظار التأكيد من المالك |
| 2 | إخفاء Hugging Face Space (Private لا Delete) | 5 دق | 🟡 بعد ذلك | لم يبدأ |
| 3 | تنفيذ rate limiting داخل الكود (~60 req/min/IP) | 30 دق | 🟢 جلسة قادمة | لم يبدأ |
| 4 | Monitoring & Alerts (اختياري) | 15 دق | 🟢 جلسة قادمة | لم يبدأ |
| 5 | إضافة Programmers كـ Collaborators على GitHub + Branch Protection | 10 دق | 🟢 عند تسليم المشروع | جاهز للتنفيذ (DEPLOY.md معدّ) |

> **ملاحظة جوهرية:** المهام 1 و2 يتمّهما المالك يدوياً عبر الواجهة (UI)، لا توجد أوامر CLI لها. المهمة 3 تحتاج جلسة كود قادمة.

---

## ٤. حالة التنفيذ (Implementation Status)

> الأسطر التي تبدأ بـ 🆕 أضيفت في الترحيل إلى Fly.io.

| الميزة | الحالة | الملفات / المكوّنات | ملاحظات |
|---|---|---|---|
| إعداد بيئة macOS Apple Silicon | ✅ | Python 3.12.3, uv 0.11.7, Node v25.9.0, Git 2.52.0, VS Code 1.119.0 | كله مثبت ومُختبر |
| ملف CLAUDE.md (قواعد المشروع للـ AI) | ✅ | `CLAUDE.md` | يُقرأ تلقائياً من Claude Code |
| فحص schema الـ DB | ✅ | `scripts/inspect_schema.py` + `scripts/SCHEMA_NOTES.md` | مرجع دائم |
| التحقق من اكتمال DB (11 فحص) | ✅ | `scripts/verify_data.py` | يطبع 11/11 ✓ |
| طبقة DB read-only | ✅ | `src/tafsir/db.py` | `mode=ro` + `PRAGMA query_only=ON` |
| نماذج Pydantic v2 | ✅ | `src/tafsir/models.py` | SURAH_AYAH_COUNTS، TafsirSource enum، 8 attributions |
| تطبيع النص العربي | ✅ | `src/tafsir/normalize.py` | pyarabic-based |
| بناء FTS5 + 17 فهرساً | ✅ | `scripts/build_fts.py` | DB من 214MB → 223.5MB |
| 13 أداة MCP | ✅ | `src/tafsir/tools/` (6 ملفات) | كل منها مع docstring عربي + annotations |
| 3 موارد MCP | ✅ | `src/tafsir/resources/catalogs.py` | quran://surahs, ://tafsirs, ://schema |
| 5 قوالب دراسة (Prompts) | ✅ | `src/tafsir/prompts/study.py` | study_ayah, compare_tafsirs, root_study, surah_overview, tajweed_lesson |
| 35 اختباراً محلياً | ✅ | `tests/` (3 ملفات) | 35/35 في 0.46s |
| MCP Inspector تشغيل | ✅ | `uv run mcp dev src/tafsir/server.py` | يعرض 13 tool + 3 resource + 5 prompt |
| ربط Claude Code | ✅ | `claude mcp add tafsir --scope user -- ...` | محلي |
| إعادة تسمية → tafsir-mcp | ✅ | 14 خطوة | 0 مراجع متبقية لـ quranic_scholar |
| `data_loader.py` (تحميل تلقائي) | ✅ | `src/tafsir/data_loader.py` | يستخدم hf_hub_download |
| رفع DB على Hugging Face | ✅ | `scripts/upload_db.py` | tafsircenter/tafsir-mcp-data |
| Dataset Card احترافي | ✅ | `scripts/upload_readme.py` | ثنائي اللغة |
| التحقق التلقائي من SHA256 | ✅ | `_verify_sha256()` في data_loader | `10e61f615ab5e6a3440e8ecc8ba1dc2273d12cd9048752760fe53a44d191cc27` |
| LICENSE + LICENSE-DATA | ✅ | جذر المشروع | MIT + CC BY 4.0 |
| README ثنائي اللغة | ✅ | `README.md` | عربي + إنجليزي مع badges |
| DATA_SOURCES.md | ✅ | جذر المشروع | جدول التفاسير الـ8 |
| CONTRIBUTING.md | ✅ | جذر المشروع | دليل المساهمة |
| Dockerfile (للحزمة الأصلية) | ✅ | جذر المشروع | Python 3.12-slim |
| GitHub Actions: test.yml | ✅ | `.github/workflows/test.yml` | نجح في 17 ثانية |
| GitHub Actions: publish.yml | ✅ | `.github/workflows/publish.yml` | جاهز لـ Trusted Publishing |
| منظمة GitHub `tafsircenter` | ✅ | github.com/tafsircenter | مُنشأة بإذن المركز |
| نشر على PyPI | ✅ | `uv publish` | v1.0.0 منشور |
| اختبار التثبيت من المستخدم النهائي | ✅ | `uvx --no-cache --refresh tafsir-mcp` | يحمّل ويبدأ التشغيل |
| 🆕 **Streamable HTTP transport** | ✅ | `deploy/server_http.py` | `mcp.run(transport="streamable-http")` + `transport_security` override |
| 🆕 **Dockerfile للنشر السحابي** | ✅ | `deploy/Dockerfile` | يُستخدم من Fly.io |
| 🆕 **fly.toml** | ✅ | جذر المشروع، commit `3121666` | bom region، shared-cpu-1x، 1GB RAM، auto-stop |
| 🆕 **.dockerignore** | ✅ | جذر المشروع | يستبعد data/quran.db، __pycache__، إلخ |
| 🆕 **نشر Fly.io** (`tafsir-mcp` app) | ✅ | bom (Mumbai)، 2 machines | image deployment-01KRP110H0390D44CRTP16MP72 |
| 🆕 **Auto-stop machines** | ✅ | `auto_stop_machines='stop'`, `min_machines_running=0` | ~95% توفير عند idle |
| 🆕 **نطاق مخصص `mcp.tafsir.net`** | ✅ | GoDaddy DNS: A + AAAA records | IPv4 66.241.124.207، IPv6 2a09:8280:1::115:e7f0:0 |
| 🆕 **شهادة SSL Let's Encrypt** | ✅ | RSA + ECDSA تجديد تلقائي | لـ`mcp.tafsir.net` |
| 🆕 **`/health` endpoint** | ✅ | `deploy/server_http.py`، commit `1c9ac63` | `@mcp.custom_route("/health")` يُرجع `{"status":"ok","service":"tafsir-mcp"}` |
| 🆕 **Fly `[[http_service.checks]]`** | ✅ | `fly.toml` | grace=15s, interval=30s, path=/health |
| 🆕 **MCP handshake على HTTPS عمومي** | ✅ | `POST https://mcp.tafsir.net/mcp` | يُرجع serverInfo: 13 tools + 3 resources + 5 prompts، MCP protocol 2024-11-05 |
| 🆕 **DEPLOY.md (دليل التشغيل)** | ✅ | `deploy/DEPLOY.md`، commit `c0fe57b` | 222 سطراً، 8 أقسام، صاغه المالك يدوياً |
| 🆕 **README URL update** | ✅ | `deploy/README.md` | غُيِّر من tafsircenter-tafsir-mcp.hf.space إلى `mcp.tafsir.net/mcp` |
| 🆕 تنظيف فروع محلية | ✅ | `git branch -d feat/flyio-deploy feat/healthcheck` | الفرعان مُدمَجان في main |
| 🆕 **قرار النموذج العام للخدمة** | ✅ | (لا يوجد ملف) | السيناريو ب: عام مع rate limit |
| 🟡 **Fly.io Spending Limit** | 🟡 قيد التنفيذ | https://fly.io/dashboard/personal/billing | المالك ملتزم بضبطه فوراً (Soft $5، Hard $25). الجلسة انتهت بانتظار التأكيد. |
| ⬜ إخفاء HF Space (Private) | ⬜ | https://huggingface.co/spaces/tafsircenter/tafsir-mcp/settings | Private لا Delete (يحفظ commit `81e42d9`) |
| ⬜ **Rate limiting في الكود** | ⬜ | (يحتاج إضافة middleware) | المقترح: ~60 req/min/IP. الخيارات: starlette-rate-limit، أو token bucket عبر Redis. |
| ⬜ Monitoring + Alerts | ⬜ | — | اختياري؛ متابعة أسبوعية أول شهر |
| ⬜ GitHub Release v1.0.0 | ⬜ | `gh release create v1.0.0` | كان pending من Context Pack v2؛ لم يُنفَّذ في هذه الجلسة لأن الترحيل أخذ الأولوية |
| ⬜ Trusted Publishing + Required Reviewer | ⬜ | PyPI Settings + GitHub Environment | للإصدارات القادمة |
| ⬜ التسجيل في MCP Registry | ⬜ | PR إلى modelcontextprotocol/registry | اختياري |
| ⬜ تسليم Programmers (Collaborator + Write + Branch Protection) | ⬜ | GitHub repo Settings → Collaborators | جاهز للتنفيذ عند الحاجة. DEPLOY.md جاهز للقراءة. |
| ⏸️ مراجعة شرعية رسمية مكتوبة | ⏸️ | — | المالك قال "اعتبرها معتمدة" شفهياً؛ توثيق رسمي مؤجل |
| ⏸️ OAuth 2.1 | ⏸️ | — | Phase 2 |
| ⏸️ ترحيل من Fly.io إلى Alibaba ECS | ⏸️ | — | Phase 2؛ النطاق المخصص `mcp.tafsir.net` يجعل الترحيل سلساً (DNS فقط) |

---

## ٥. البنية التقنية

### ٥.١ المكدّس (Stack)

| الطبقة | الاختيار | الإصدار المستخدم |
|---|---|---|
| لغة الخادم | Python | 3.12.3 |
| إدارة الحزم | uv | 0.11.7 |
| إطار MCP | FastMCP عبر `mcp[cli]` | `>=1.27.0` (المثبت في الإنتاج: **1.27.1**) |
| بروتوكول MCP (المتفاوض عليه على الـHTTP server) | — | `2024-11-05` |
| MCP SDK | — | 1.27.1 (متحقّق منه عبر handshake على الإنتاج) |
| Transport على Fly.io | streamable-http | عبر `mcp.run(transport="streamable-http")` |
| تشغيل الخادم محلياً (stdio) | عبر `uvx tafsir-mcp` أو `uv run tafsir-mcp` | stdio (لـClaude Code) |
| التحقق من المدخلات | Pydantic v2 | `>=2.9` (مثبت 2.13) |
| قاعدة البيانات | SQLite + FTS5 | 3.x |
| معالجة العربية | pyarabic | `>=0.6.15` (يطبع SyntaxWarning غير مؤذٍ) |
| تحميل من السحابة | huggingface_hub | `>=0.27.0` (مثبت 1.14.0) |
| الاختبار | pytest + pytest-asyncio | 8.x + 1.3.0 |
| جودة الكود | ruff + mypy | (dev only، الإصدارات غير محدّدة) |
| Anyio | anyio | 4.13.0 |
| ASGI server في الإنتاج | Uvicorn | (ينطلق عبر FastMCP run، الإصدار غير مذكور صراحة) |
| Starlette (للـ`/health`) | عبر FastMCP | (Custom Route من Starlette) |
| الحاوية | Docker (Python 3.12-slim) | — |
| استضافة الإنتاج | Fly.io | shared-cpu-1x، 1GB RAM، region `bom` (Mumbai) |
| DNS | GoDaddy | A + AAAA records على `mcp.tafsir.net` |
| SSL | Let's Encrypt (تلقائي عبر Fly.io) | RSA + ECDSA dual-stack |
| Node.js (لـ Claude Code) | Node | v25.9.0 |
| Git | Git | 2.52.0 |
| OS المطوّر | macOS Tahoe Apple Silicon | 26.4.1 |
| المحرر | VS Code | 1.119.0 (مستخدم لتجاوز Bracketed Paste في Terminal) |

### ٥.٢ شجرة الملفات الكاملة

```
~/projects/quranic-scholar-mcp/              ← مسار محلي (لم يُعد تسمية المجلد على القرص رغم تغيّر اسم الحزمة)
├── .github/workflows/
│   ├── test.yml                              ← CI: 17 ثانية، 35 اختبار
│   └── publish.yml                           ← جاهز لـ Trusted Publishing
├── .gitignore                                ← يستبعد data/quran.db, scripts/.db_sha256, .env
├── .dockerignore                             🆕 ← يستبعد data/, __pycache__/, .venv/, إلخ
├── .python-version                           ← 3.12
├── CLAUDE.md                                 ← دليل المساعد (3,419 bytes)
├── CONTRIBUTING.md
├── DATA_SOURCES.md                           ← جدول التفاسير الـ8
├── Dockerfile                                ← (للحزمة الأصلية) Python 3.12-slim
├── LICENSE                                   ← MIT
├── LICENSE-DATA                              ← CC BY 4.0
├── README.md                                 ← ثنائي اللغة مع badges
├── fly.toml                                  🆕 ← تكوين Fly.io (bom region، auto-stop، health check)
├── main.py                                   ← legacy (موروث من uv init، غير مستخدم)
├── pyproject.toml                            ← tafsir-mcp 1.0.0
├── tafsir-mcp-context-pack.md                ← Context Pack v1 (داخل المستودع)
├── uv.lock
├── data/
│   ├── quran.db                              ← 223 MB (محلي، مستبعد من Git)
│   ├── quran.db-shm                          ← SQLite WAL
│   └── quran.db-wal
├── deploy/                                   🆕 ← ملفات النشر السحابي
│   ├── server_http.py                        🆕 ← FastMCP يشغّل streamable-http + /health endpoint
│   ├── Dockerfile                            🆕 ← يستخدم في Fly.io build (referenced in fly.toml)
│   ├── README.md                             🆕 ← (يحوي YAML frontmatter لـ HF Space + المحتوى الفني)
│   └── DEPLOY.md                             🆕 ← دليل النشر (222 سطر، صاغه المالك)
├── dist/
│   ├── tafsir_mcp-1.0.0-py3-none-any.whl     ← 30 KB
│   └── tafsir_mcp-1.0.0.tar.gz               ← 107 KB
├── scripts/
│   ├── verify_data.py                        ← 11 فحص
│   ├── inspect_schema.py                     ← اكتشاف الأعمدة
│   ├── SCHEMA_NOTES.md                       ← مرجع schema
│   ├── build_fts.py                          ← FTS5 + 17 فهرس
│   ├── upload_db.py                          ← رفع DB إلى HF
│   ├── upload_readme.py                      ← رفع Dataset Card
│   └── .db_sha256                            ← مستبعد من Git
├── src/tafsir/
│   ├── __init__.py
│   ├── server.py                             ← FastMCP("Tafsir MCP") — stdio mode للـ pip install
│   ├── db.py                                 ← read-only sqlite + helpers
│   ├── data_loader.py                        ← 3-tier path resolver
│   ├── models.py                             ← Pydantic schemas + TAFSIR_ATTRIBUTIONS
│   ├── normalize.py                          ← Arabic text normalization
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── ayah.py                           ← 3 أدوات
│   │   ├── surah.py                          ← 2 أداة
│   │   ├── word.py                           ← 3 أدوات
│   │   ├── qeraat.py                         ← 1 أداة
│   │   ├── search.py                         ← 2 أداة
│   │   └── stats.py                          ← 2 أداة
│   ├── resources/
│   │   ├── __init__.py
│   │   └── catalogs.py                       ← 3 موارد
│   └── prompts/
│       ├── __init__.py
│       └── study.py                          ← 5 قوالب
└── tests/
    ├── __init__.py
    ├── test_db_and_models.py                 ← 10 اختبارات
    ├── test_extended_tools.py                ← 15 اختباراً
    └── test_resources_prompts.py             ← 10 اختبارات
```

> **ملاحظة:** الفرق بين `src/tafsir/server.py` و `deploy/server_http.py`:
> - `server.py` = stdio mode، يُستخدم للتنزيل عبر `pip install tafsir-mcp` ثم تشغيل `tafsir-mcp` كأمر — Claude Code يتصل به محلياً عبر stdio.
> - `deploy/server_http.py` = streamable-http mode، يُشغَّل داخل Docker على Fly.io — يقدّم نفس الأدوات لكن عبر HTTPS على `mcp.tafsir.net/mcp`.

### ٥.٣ النمط المعماري الجوهري — **Programmatic Registration**

> هذا النمط **ليس** `@mcp.tool()` decorator. هو نمط معتمد من قبل المالك ومُختبر.

#### في كل ملف tool (مثال `tools/ayah.py`):
```python
def get_ayah(surah, ayah, ...) -> dict: ...
def get_ayah_tafsir(...) -> dict: ...
def get_ayah_nuzool(...) -> dict: ...

def register(mcp):
    """تُستدعى من server.py لتسجيل أدوات هذا الملف."""
    annotations = {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    }
    mcp.tool(name="fetch_ayah", annotations=annotations)(get_ayah)
    mcp.tool(name="fetch_tafsir", annotations=annotations)(get_ayah_tafsir)
    mcp.tool(name="fetch_nuzool_reason", annotations=annotations)(get_ayah_nuzool)
```

> **اكتشاف مهم:** **اسم Python للدالة ≠ اسم MCP المسجَّل.** مثلاً Python `get_ayah` يُسجَّل في MCP كـ `fetch_ayah`. هذا متعمد ومُختبر.

### ٥.٤ خرائط الجداول الجوهرية

```
المفهوم                       | الجدول                       | المفاتيح         | ملاحظات
───────────────────────────── | ──────────────────────────── | ──────────────── | ────────
نص الآية (مُبنى)              | word_content_rasm            | surahNo, ayahNo  | جمع word ORDER BY wordNo
تجويد الآية                   | ayah_content_tajweed         | surahNo, ayahNo  | عمود: tajweed
إعراب الآية                   | ayah_content_irab            | surahNo, ayahNo  | عمود: irabAyah1 (! ليس irab)
سبب النزول                    | ayah_content_nozool          | surahNo, ayahNo  | عمود: nozoolInfo (سند+متن في عمود واحد)
تفسير الطبري                  | tafsir_tabary                | sura, aya        | ⚠️ مفاتيح مختلفة
تفسير ابن كثير                | tafsir_katheer               | sura, aya        | ⚠️
تفسير البغوي                  | tafsir_baghawy               | sura, aya        | ⚠️
تفسير السعدي                  | tafsir_saadi                 | sura, aya        | ⚠️
التفسير الميسر                | tafsir_moyassar              | sura, aya        | ⚠️
المختصر متعدد اللغات          | QuranTafseer                 | surahNo, ayahNo  | Mukhtasarar / Mukhtasaren / Mukhtasarbn
معنى الكلمة                   | word_content_meaning         | surahNo, ayahNo, wordNo |
إعراب الكلمة                  | word_content_irab            | surahNo, ayahNo, wordNo | عمود: irabMushakkal
صرف الكلمة                    | word_content_sarf            | surahNo, ayahNo, wordNo |
إحصاءات الكلمة                | word_statistics              | surahNo, ayahNo, wordNo | repeatitionCount (مهجأ خطأ في DB)
اختلاف القراءات               | qeraat_info                  | surahNo, ayahNo, wordNo | content بتنسيق @قارئ/نص@
فوائد الصفحة                  | mokhtasar_fawaed             | page             | عدة صفوف لكل صفحة (استخدم fetchall)
```

### ٥.٥ أرقام البيانات (مرجعية إلزامية)

```
- 114 سورة
- 6,236 آية
- 77,432 كلمة
- 1,891 جذراً
- 604 صفحة مصحف
- 201 آية لها أسباب نزول موثّقة
- 5 تفاسير كلاسيكية × 6,236 = 31,180 صف تفسير
- 8 مصادر تفسير إجمالاً (5 كلاسيكية + 3 لغات للمختصر)
- 20 جدول في DB
- 17 فهرساً + 1 جدول FTS5
- DB size: 214 MB (raw) → 223.5 MB (with FTS5+indexes)
- SHA256: 10e61f615ab5e6a3440e8ecc8ba1dc2273d12cd9048752760fe53a44d191cc27
```

### ٥.٦ الأدوات الـ13 المسجَّلة (أسماء MCP)

```
الفئة     | اسم MCP                | الدالة Python                | الملف
─────────|────────────────────────|──────────────────────────────|──────────
الآية    | fetch_ayah             | get_ayah                     | tools/ayah.py
         | fetch_tafsir           | get_ayah_tafsir              | tools/ayah.py
         | fetch_nuzool_reason    | get_ayah_nuzool              | tools/ayah.py
السورة   | fetch_surah_info       | get_surah_info               | tools/surah.py
         | get_surah_statistics   | get_surah_statistics_summary | tools/stats.py
الكلمة   | analyze_word           | get_word_analysis            | tools/word.py
         | find_root_occurrences  | search_by_root               | tools/word.py
         | get_root_stats         | get_root_statistics          | tools/word.py
القراءات | get_qeraat_variants    | compare_qeraat               | tools/qeraat.py
البحث    | search_quran_text      | search_quran_text            | tools/search.py
         | search_in_tafsir       | search_tafsir                | tools/search.py
عام      | get_quran_overview     | get_quran_statistics         | tools/stats.py
         | get_page_fawaed        | get_page_fawaed              | tools/stats.py
```

### ٥.٧ المخطط المعماري للإنتاج

```
+---------------------+   HTTPS    +-------------------+   anycast   +--------------+
|  المستخدم / MCP client | ─────────► | mcp.tafsir.net    | ─────────►  | Fly.io edge |
|  (Claude Code, إلخ)    |            | (GoDaddy DNS)    |            +-------+------+
+---------------------+              +-------------------+                    │
                                                                              ▼
                                                                    +--------------------+
                                                                    | Fly.io Machine     |
                                                                    | (bom region)       |
                                                                    | Docker container   |
                                                                    | Uvicorn :7860      |
                                                                    | FastMCP server     |
                                                                    | (streamable-http)  |
                                                                    +--------+-----------+
                                                                              │
                                                                              ▼
                                                                    quran.db (محلي في الـimage)
```

### ٥.٨ Fly.io specs الحالية

| الحقل | القيمة |
|---|---|
| **app name** | `tafsir-mcp` |
| **org** | `personal` (display: "Tafsir Center") — لا يوجد team org |
| **region** | `bom` (Mumbai) |
| **VM size** | shared-cpu-1x |
| **RAM** | 1 GB (`memory='1gb'`, `memory_mb=1024`) |
| **internal port** | 7860 |
| **force HTTPS** | true |
| **auto_stop_machines** | `'stop'` (يوقف الـmachine بعد فترة idle) |
| **auto_start_machines** | `true` |
| **min_machines_running** | `0` |
| **عدد الـmachines الحالي** | 2 (الأولى `2863d22b45e2d8` تعمل، الثانية `80e473b65e7e68` مُوقفة auto-stop) |
| **image الحالية** | `deployment-01KRP110H0390D44CRTP16MP72`، 182 MB |
| **IPv4** | 66.241.124.207 |
| **IPv6** | 2a09:8280:1::115:e7f0:0 |
| **التكلفة المتوقعة** | $3-5/شهر (مع auto-stop) |

### ٥.٩ نقاط نهاية الإنتاج

| Endpoint | Method | Auth | الوظيفة |
|---|---|---|---|
| `https://mcp.tafsir.net/mcp` | POST | — | MCP JSON-RPC (initialize، tools/list، tools/call، إلخ) |
| `https://mcp.tafsir.net/health` | GET | — | Fly health check؛ يُرجع `{"status":"ok","service":"tafsir-mcp"}` |
| `https://tafsir-mcp.fly.dev/mcp` | POST | — | احتياطي (Fly الافتراضي)؛ يعمل أيضاً |

> **ملاحظة أمنية:** لا يوجد auth حالياً. الرابط متاح للجميع. هذا قرار مقصود (السيناريو ب) لكن مع rate limiting قادم.

---

## ٦. البيئة والتشغيل (تفصيلي بلا اختزال)

### ٦.١ متطلبات النظام للمطوّر

- macOS 14+ / Linux / Windows (المُختبر فعلياً: macOS 26.4.1 Apple Silicon)
- Python 3.11+ (يفضّل 3.12)
- اتصال إنترنت لأول تشغيل (لتحميل DB من Hugging Face)
- لـ Fly.io: `flyctl` CLI مثبّت، حساب Fly.io نشط مع بطاقة ائتمان

### ٦.٢ متغيرات البيئة

| المتغير | الغرض | إلزامي؟ |
|---|---|---|
| `TAFSIR_DB_PATH` | مسار quran.db محلي (للمطوّرين فقط) | لا — تُحمَّل من HF تلقائياً |
| `HF_TOKEN` | للنشر إلى Hugging Face (سكربتات scripts/upload_*) | فقط للمطوّر مالك الـ dataset |
| `UV_PUBLISH_TOKEN` | للنشر إلى PyPI | فقط لمالك الحزمة |
| `HF_HUB_CACHE` | (اختياري) مسار cache بديل لـ huggingface_hub | لا |
| `PORT` | المنفذ الذي يستمع له الخادم HTTP (الافتراضي 7860) | لا، له default في `server_http.py` |

### ٦.٣ التثبيت — المستخدم النهائي (الطرق الثلاث)

#### الطريقة 1: عبر HTTP (الأبسط، الجديد) — لا تثبيت محلي
```jsonc
// في إعداد Claude Code أو أي MCP client يدعم HTTP transport
{
  "mcpServers": {
    "tafsir": {
      "type": "http",
      "url": "https://mcp.tafsir.net/mcp"
    }
  }
}
```

#### الطريقة 2: عبر pip + Claude Code (محلي، stdio)
```bash
claude mcp add tafsir --scope user -- uvx tafsir-mcp
# DB تُحمَّل من HF عند أول تشغيل (~214 MB)
```

#### الطريقة 3: pip فقط
```bash
pip install tafsir-mcp
# أو
uvx tafsir-mcp
```

### ٦.٤ التثبيت — المطوّر (من المصدر)

```bash
git clone https://github.com/tafsircenter/tafsir-mcp
cd tafsir-mcp
uv sync

# خيار 1: ضع quran.db محلياً
cp /path/to/quran.db data/quran.db

# خيار 2: متغير بيئة
export TAFSIR_DB_PATH=/path/to/quran.db

# تشغيل الخادم (stdio)
uv run tafsir-mcp

# أو تشغيل الخادم HTTP محلياً (للاختبار)
uv run python deploy/server_http.py
# يستمع على http://localhost:7860
```

### ٦.٥ الاختبار

```bash
# كل الاختبارات
uv run pytest tests/ -v
# المتوقع: 35 passed in ~0.46s

# فحص اكتمال DB
uv run python scripts/verify_data.py
# المتوقع: 11/11 ✓

# فحص schema
uv run python scripts/inspect_schema.py

# تشغيل MCP Inspector
uv run mcp dev src/tafsir/server.py
# يفتح http://localhost:6274

# اختبار health endpoint محلياً
curl -i http://localhost:7860/health
# المتوقع: HTTP/1.1 200 OK + {"status":"ok","service":"tafsir-mcp"}

# اختبار MCP handshake على الإنتاج
curl -X POST https://mcp.tafsir.net/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}'
```

### ٦.٦ ربط Claude Code محلياً (stdio)

```bash
claude mcp add tafsir --scope user -- \
  uv --directory /Users/ahmedeid/projects/quranic-scholar-mcp run tafsir-mcp

# التحقق
claude mcp list
# المتوقع: tafsir: ... ✓ Connected
```

### ٦.٧ سكربت رفع DB إلى Hugging Face (للمالك فقط)

```bash
# 1. احفظ التوكن بأمان (لا تكتبه في الأمر)
read -s HF_TOKEN
# الصق التوكن واضغط Enter (لن يظهر شيء)
export HF_TOKEN

# 2. تحقق
echo "HF_TOKEN length: ${#HF_TOKEN}"   # يجب 37

# 3. ارفع
uv run python scripts/upload_db.py
uv run python scripts/upload_readme.py
```

### ٦.٨ سكربت النشر إلى PyPI (للمالك فقط)

```bash
# 1. توكن PyPI
read -s UV_PUBLISH_TOKEN
export UV_PUBLISH_TOKEN

# 2. بناء
uv build
# يُنتج dist/tafsir_mcp-X.Y.Z-py3-none-any.whl + .tar.gz

# 3. فحص الحجم (يجب < 100 KB كل ملف)
ls -lh dist/

# 4. فحص المحتوى
unzip -l dist/tafsir_mcp-*-py3-none-any.whl
# يجب: لا quran.db، لا .env، لا scripts/.db_sha256

# 5. النشر
uv publish --token "$UV_PUBLISH_TOKEN"
```

### ٦.٩ سير عمل النشر إلى Fly.io (🆕 — الجوهري للتحديثات)

> هذا السير معتمد ومُختبر في الجلسة الأخيرة. وُثّق في `deploy/DEPLOY.md` للتسليم.

```bash
# 1. أنشئ فرعاً جديداً
cd ~/projects/quranic-scholar-mcp
git switch -c feat/<اسم-الميزة>

# 2. عدّل ما تريد (deploy/server_http.py، fly.toml، إلخ)
code deploy/server_http.py

# 3. اختبر محلياً (طبقتان)
uv run pytest tests/ -v                         # اختبارات Python
uv run python deploy/server_http.py &           # شغّل الخادم
curl -i http://localhost:7860/health            # المتوقع: 200 + {"status":"ok",...}
curl -i http://localhost:7860/mcp               # المتوقع: 406 (يتطلب Accept: SSE) — هذا normal

# 4. التزم باسم commit واضح (Conventional Commits)
git add -A
git commit -m "feat: add X"

# 5. ادمج إلى main مع fast-forward فقط (تنظيف التاريخ)
git switch main
git merge feat/<اسم-الميزة> --ff-only
git push origin main

# 6. انشر إلى Fly.io
fly deploy

# 7. تحقّق من الـ deploy
fly status                          # المتوقع: VERSION ↑1، CHECKS = 1 total، 1 passing
fly checks list                     # المتوقع: passing على الـmachine الفعّالة
curl -i https://mcp.tafsir.net/health   # المتوقع: HTTP/2 200 + payload

# 8. نظّف الفرع المحلي
git branch -d feat/<اسم-الميزة>

# في حال خطأ → rollback
fly releases               # اعرض القائمة
fly releases rollback <id> # ارجع لإصدار سابق
```

### ٦.١٠ Fly.io operations (✅ مهمة)

```bash
# عرض حالة التطبيق
fly status

# عرض الفحوصات الصحية
fly checks list

# عرض الـmachines
fly machines list

# عرض السجلات (logs) — قيد التشغيل
fly logs

# تشغيل أمر داخل الـmachine (ssh)
fly ssh console

# إعادة بدء machine
fly machines restart <id>

# عرض الـIP addresses
fly ips list

# عرض الشهادات (SSL)
fly certs list
fly certs check mcp.tafsir.net    # يفحص حالة الشهادة
```

### ٦.١١ Docker (للحزمة الأصلية)

```bash
docker build -t tafsir-mcp:1.0.0 .
docker run --rm -it tafsir-mcp:1.0.0
```

### ٦.١٢ DNS وSSL على GoDaddy + Let's Encrypt

DNS records في GoDaddy على `tafsir.net`:

```
Type    Host    Value                              TTL
A       mcp     66.241.124.207                     600
AAAA    mcp     2a09:8280:1::115:e7f0:0            600
```

SSL: عند إضافة النطاق عبر `fly certs add mcp.tafsir.net`، Fly.io يطلب من Let's Encrypt شهادتَين (RSA + ECDSA)، يحققها عبر HTTP-01 challenge، ويُجدّدها تلقائياً قبل انتهائها بـ30 يوماً. لا تدخّل يدوي مطلوب.

---

## ٧. نموذج البيانات وعقود الواجهات

### ٧.١ Pydantic Models الأساسية

#### `AyahReference`
```python
class AyahReference(BaseModel):
    surah: int = Field(ge=1, le=114)
    ayah: int = Field(ge=1)

    @field_validator("ayah")
    def check_within_surah(cls, v, info):
        surah = info.data.get("surah")
        if surah and v > SURAH_AYAH_COUNTS[surah]:
            raise ValueError(
                f"السورة {surah} تحتوي على {SURAH_AYAH_COUNTS[surah]} آية فقط، "
                f"الرقم المُدخل {v} خارج النطاق."
            )
        return v
```

#### `TafsirSource` Enum
```python
class TafsirSource(str, Enum):
    tabary = "tabary"
    katheer = "katheer"
    baghawy = "baghawy"
    saadi = "saadi"
    moyassar = "moyassar"
    mukhtasar_ar = "mukhtasar_ar"
    mukhtasar_en = "mukhtasar_en"
    mukhtasar_bn = "mukhtasar_bn"
```

#### `TAFSIR_ATTRIBUTIONS` (إلزامي شرعياً)
```python
TAFSIR_ATTRIBUTIONS = {
    TafsirSource.tabary:   "تفسير الإمام الطبري (جامع البيان)، أبو جعفر الطبري (ت. 310هـ)",
    TafsirSource.katheer:  "تفسير ابن كثير، أبو الفداء إسماعيل بن كثير (ت. 774هـ)",
    TafsirSource.baghawy:  "تفسير البغوي (معالم التنزيل)، الحسين بن مسعود البغوي (ت. 510هـ)",
    TafsirSource.saadi:    "تيسير الكريم الرحمن، عبد الرحمن بن ناصر السعدي (ت. 1376هـ)",
    TafsirSource.moyassar: "التفسير الميسر، مجمع الملك فهد لطباعة المصحف الشريف",
    # ... 3 مختصرات بـ AR / EN / BN
}
```

### ٧.٢ عقود الأدوات (Tool Contracts) — مختارة

#### `fetch_ayah`
```
INPUT:
  surah: int (1-114، مع تحقق ضد عدد آيات السورة الفعلي)
  ayah: int (1-N حسب السورة)
  include_tajweed: bool = False
  include_irab: bool = False

OUTPUT:
{
  "surah": int,
  "ayah": int,
  "text": str,                # نص الآية بالرسم العثماني
  "tajweed": str | None,
  "irab": str | None,
  "word_count": int
}

ERRORS:
  ValidationError (Pydantic) — لو خارج النطاق، رسالة عربية واضحة
```

#### `fetch_tafsir`
```
INPUT:
  surah: int
  ayah: int
  sources: list[TafsirSource]  # default ["saadi"]

OUTPUT:
{
  "surah": int,
  "ayah": int,
  "tafsirs": [
    {
      "source": "saadi",
      "attribution": "تيسير الكريم الرحمن، عبد الرحمن بن ناصر السعدي (ت. 1376هـ)",
      "text": str
    },
    ...
  ]
}
```

#### `fetch_nuzool_reason`
```
INPUT: surah, ayah
OUTPUT (إذا وجد):
{
  "surah": int, "ayah": int,
  "available": true,
  "text": str                    # سند + متن كاملاً، بدون تشذيب
}
OUTPUT (إذا لم يوجد):
{
  "surah": int, "ayah": int,
  "available": false,
  "reason": "لم يثبت سبب نزول لهذه الآية في المصادر المعتمدة"
}
```

#### `search_quran_text` (FTS5)
```
INPUT:
  query: str
  surah_filter: list[int] | None = None
  limit: int = 20

OUTPUT:
{
  "result": [
    {
      "surah": int, "ayah": int,
      "text": str,
      "snippet": str,            # مع <m>...</m> للمطابقات
      "score": float             # رتبة FTS5
    },
    ...
  ]
}
```

#### `analyze_word`
```
INPUT:
  surah, ayah, word_no
  aspects: list  # default ["meaning", "irab", "sarf"]

OUTPUT:
{
  "word_no": int, "word": str,
  "meaning": str | None,
  "irab": str | None,             # من irabMushakkal في DB
  "sarf": str | None,
  "root": str | None,
  "repetition_count": int | None  # ⚠️ منقول من repeatitionCount (مهجأ خطأ في DB)
}
```

### ٧.٣ الموارد (Resources)

```
URI                | Format            | المحتوى
───────────────────|───────────────────|──────────────────────────────────────────
quran://surahs     | application/json  | فهرس 114 سورة (surahNo, name, makkiMadani, ayahCount, revelationOrder)
quran://tafsirs    | application/json  | 8 مصادر مع author, death_year, coverage
quran://schema     | text/markdown     | توثيق سكيمة DB للمطوّرين
```

### ٧.٤ القوالب (Prompts)

```
study_ayah(surah, ayah)        — يستدعي fetch_ayah(tajweed+irab), fetch_tafsir(saadi+moyassar), nuzool, analyze_word, get_root_stats
compare_tafsirs(surah, ayah)   — يستدعي fetch_tafsir لكل المصادر الخمسة + جدول مقارنة
root_study(root)               — get_root_stats + find_root_occurrences(limit=20)
surah_overview(surah)          — fetch_surah_info + get_surah_statistics + fetch_ayah للأولى والأخيرة
tajweed_lesson(surah, ayah)    — fetch_ayah(include_tajweed=True) + شرح كل حكم
```

### ٧.٥ Database Connection Pattern

```python
# في src/tafsir/db.py
def get_connection() -> sqlite3.Connection:
    path = get_db_path()  # من data_loader
    if not path.exists():
        raise FileNotFoundError("قاعدة البيانات غير موجودة: ...")
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True, check_same_thread=False)
    conn.execute("PRAGMA query_only = ON")
    conn.row_factory = sqlite3.Row
    return conn

TAFSIR_KEYS = ("sura", "aya")          # 5 جداول تفاسير
STANDARD_KEYS = ("surahNo", "ayahNo")  # كل الباقي
```

### ٧.٦ Path Resolution (3-tier)

```python
# في src/tafsir/data_loader.py
def get_db_path() -> Path:
    # 1. متغير بيئة (مطوّر)
    if env := os.environ.get("TAFSIR_DB_PATH"):
        if Path(env).exists(): return Path(env)

    # 2. data/ المحلي (تطوير)
    local = Path(__file__).parent.parent.parent / "data" / "quran.db"
    if local.exists(): return local

    # 3. ~/.cache/tafsir-mcp/ (production، يُحمَّل من HF)
    cache = Path.home() / ".cache" / "tafsir-mcp" / "quran.db"
    if not cache.exists():
        _download_from_hf(cache)
        _verify_sha256(cache)
    return cache
```

### ٧.٧ HTTP MCP Wire Format (Fly.io)

```http
POST /mcp HTTP/1.1
Host: mcp.tafsir.net
Content-Type: application/json
Accept: application/json, text/event-stream

{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}
```

Response (الجزء الأهم):
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "serverInfo": {
      "name": "Tafsir MCP",
      "version": "1.27.1"
    },
    "capabilities": {
      "tools": {...},      // 13 أداة
      "resources": {...},  // 3 موارد
      "prompts": {...}     // 5 قوالب
    }
  }
}
```

> **مهم:** الطلب على `/mcp` بدون `Accept: text/event-stream` يُرجع `406 Not Acceptable`. هذا سلوك MCP السليم.

### ٧.٨ Health Endpoint Contract

```http
GET /health HTTP/1.1
Host: mcp.tafsir.net
```

Response:
```http
HTTP/2 200
content-type: application/json
content-length: 38

{"status":"ok","service":"tafsir-mcp"}
```

---

## ٨. اصطلاحات الكود

### ٨.١ التسمية
| العنصر | الاصطلاح |
|---|---|
| دوال Python | `snake_case` فعلية (`get_ayah`, `search_by_root`) |
| أسماء MCP المسجَّلة | `snake_case` بفعل واضح (`fetch_*`, `analyze_*`, `find_*`) |
| **مهم** | **اسم MCP ≠ اسم Python بالضرورة** (متعمد) |
| Pydantic models | `PascalCase` (`AyahReference`, `TafsirResponse`) |
| Enums | `PascalCase`/`snake_case` للقيم (`TafsirSource.saadi`) |
| الثوابت | `UPPER_SNAKE_CASE` (`SURAH_AYAH_COUNTS`, `TAFSIR_KEYS`, `DB_SHA256`) |
| ملفات Python | `snake_case.py` |
| URIs الموارد | `quran://<category>` |
| فروع Git | `feat/`, `fix/`, `chore/`, `docs/` |
| Branch policy | **fast-forward only** عند الدمج إلى main (`git merge --ff-only`)؛ يُحافظ على تاريخ خطي |

### ٨.٢ SQL Style (إلزامي)
```python
# ✅ صحيح
cursor.execute("SELECT * FROM tafsir_saadi WHERE sura = ? AND aya = ?", (surah, ayah))

# ❌ ممنوع
cursor.execute(f"SELECT * FROM tafsir_saadi WHERE sura = {surah}")
```

### ٨.٣ Pydantic v2 Pattern في FastMCP
```python
# ❌ خطأ — ينتج FieldInfo
def fn(surah: int = Field(ge=1, le=114, default=1)): ...

# ✅ صحيح — Annotated
from typing import Annotated
def fn(surah: Annotated[int, Field(ge=1, le=114)] = 1): ...
```

### ٨.٤ معايير الأدوات
```python
def register(mcp):
    annotations = {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,   # لا اتصال خارجي
    }
    mcp.tool(name="fetch_ayah", annotations=annotations)(get_ayah)
```

- Docstring **بالعربية** للوصف الرئيسي (LLM يقرؤها)
- `Args:` **بالإنجليزية** الفنية
- نوع الإرجاع: `dict` (JSON-serializable)

### ٨.٥ طول الدوال
**غير محدد رسمياً.** النمط الملاحظ: 10-40 سطراً لكل دالة، مسؤولية واحدة. تقسيم بـ helpers عند تجاوز ذلك.

### ٨.٦ التعليقات
- **عربية** للسياق الديني/الشرعي
- **إنجليزية** للتقني البحت
- `# sic` لأخطاء DB المحفوظة عمداً (مثل `repeatitionCount`)

### ٨.٧ معالجة الأخطاء
```python
class QuranDataError(Exception):
    """يُرفع عند خطأ في قراءة قاعدة بيانات القرآن."""

def query_one(sql, params=()) -> dict | None:
    conn = get_connection()
    try:
        row = conn.execute(sql, params).fetchone()
        return dict(row) if row else None
    except sqlite3.DatabaseError as e:
        raise QuranDataError(f"خطأ في الاستعلام: {e}") from e
    finally:
        conn.close()
```

- رسائل خطأ **بالعربية الفصحى** للمستخدم النهائي
- استثناءات داخلية يمكن أن تكون إنجليزية
- `from e` للحفاظ على chain

### ٨.٨ رسائل Git Commits (Conventional Commits)

```
feat: new feature
fix: bug fix
docs: documentation only
test: tests only
refactor: restructure
chore: maintenance (rename, rebrand, etc.)
```

**أمثلة فعلية من المشروع (آخر 3 commits على main):**
```
c0fe57b  docs: update README URL and add DEPLOY.md
1c9ac63  feat: add /health endpoint and Fly health check
3121666  chore: add Fly.io configuration (fly.toml + .dockerignore)
```

سياسة الدمج: `git merge feat/X --ff-only` — لا تُسمح merge commits. الفروع المحلية تُحذف بعد الدمج (`git branch -d feat/X`).

### ٨.٩ Bash Style للأوامر الحساسة (🆕 جديد — اعتمده المالك في هذه الجلسة)

عند الإجراءات الحساسة (نشر، تعديل DB، تعديل توكنات)، استخدام `set -e` و `&& \`:

```bash
cd ~/projects/quranic-scholar-mcp && \
set -e && \
echo "Step 1: ..." && \
git status && \
git diff --stat
```

السبب (اعتمده المالك بعد مقارنة بين نسختين): `set -e` يوقف عند أي خطأ، `&& \` يضمن أن كل خطوة تنجح قبل الانتقال للتالية. هذا يمنع كارثة "نُفِّذت الخطوة 3 رغم فشل الخطوة 2".

---

## ٩. سجل القرارات (Decision Log)

> القرارات مرتّبة كرونولوجياً تقريباً. إذا تغيّر قرار، تُعتمد النسخة الأخيرة ويُشار للتعديل.

| القرار | السبب | البديل المرفوض | موضع/سياق القرار |
|---|---|---|---|
| **Python** | MCP SDK الأنضج | TypeScript | الخطة الأولى |
| **uv بدل pip** | المعيار الرسمي 2026 | pip + venv | المرحلة 1 (إعداد) |
| **FastMCP** | الإطار الرسمي من Anthropic | بناء يدوي | الخطة الأولى |
| **SQLite + FTS5** | offline-first | PostgreSQL | المرحلة 1 |
| **Pydantic v2 strict** | حماية من هلوسة LLM | dataclasses | المرحلة 2 |
| **read-only DB** | استحالة تعديل المحتوى الديني خطأً | connection عادي | المرحلة 2 |
| **اسم MCP ≠ اسم Python** | مرونة في إعادة التسمية | تطابق إلزامي | بعد فحص server.py |
| **`Annotated[T, Field(...)] = d`** | تفادي FieldInfo bug | `Field(default=...)` | اكتشاف المالك أثناء العمل |
| **`register(mcp)` بدل decorators** | modularity + قابلية إعادة التسمية | `@mcp.tool` مباشرة | اعتمده Claude Code في المرحلة 5 |
| **MIT للكود + CC BY 4.0 للمحتوى** | الكود حر، المحتوى ملك المركز | ترخيص واحد | بعد إعلان رعاية المركز |
| **Hugging Face Datasets للـDB** | حد PyPI 100MB، DB 214MB | تضمين DB في PyPI | المرحلة 6 (التغليف) |
| **v1.0.0 مباشرة (لا beta)** | البيانات معتمدة سلفاً | إصدار v0.x | اقتباس المالك: *"الداتا المرفوعة كلها مراجعة بالفعل ومستخدمة في تطبيقات المركز اعتبرها معتمدة"* |
| **اسم `tafsir-mcp`** | قصير، عام، يربط بالمركز | quranic-scholar, tadabbur, mishkah, hadi | اقتباس المالك: *"اسم المشروع: Tafsir"* |
| **منظمة GitHub `tafsircenter`** | اتساق مع HF و PyPI | حساب شخصي ah-vb-cod | اقتباس المالك: *"نعم لدي اذن، تم الانشاء"* |
| **بريد cloud@tafsir.net** | بريد المركز الرسمي للنشر | بريد شخصي | اقتباس المالك حرفياً |
| **التزام بنسبة كل قول** | أمانة شرعية | إرجاع نص فقط | في CLAUDE.md، إلزامي |
| **TAFSIR_KEYS vs STANDARD_KEYS** | منع خلط `sura/aya` مع `surahNo/ayahNo` | تذكّر يدوي | بعد فحص schema |
| **FTS5 للقرآن فقط، LIKE للتفاسير** | توفير مساحة | FTS5 على كل شيء | المرحلة 5 |
| 🆕 **الترحيل إلى Fly.io الآن، Alibaba ECS لاحقاً** | استراتيجية مرحلتين، تجنّب تعليق المشروع بانتظار خادم | البقاء على HF Space فقط، أو الانتظار لـAlibaba | اقتباس المالك: *"نمضي بـ Fly.io"* |
| 🆕 **Mumbai (`bom`) كمنطقة** | الأقرب جغرافياً للمستخدمين الناطقين بالعربية وأرخص من الخليج | sin، fra، إلخ | افتراضي Fly.io؛ المالك قبله |
| 🆕 **auto_stop=stop + min=0** | توفير 95% من التكلفة عند idle | machines دائمة | الترحيل الأولي |
| 🆕 **نطاق مخصص `mcp.tafsir.net`** | يفصل البنية التحتية عن العنوان المنشور (يسهّل ترحيل ECS لاحقاً) | استخدام `tafsir-mcp.fly.dev` فقط | اقتباس المالك (بعد تأكيد): *"الرابط الجديد اقصد mcp.tafsir.net/mcp"* |
| 🆕 **إبقاء HF Space علنياً مؤقتاً ثم Private** | تجنّب أي انقطاع للمستخدمين الحاليين | حذفه فوراً | اقتباس المالك: *"HF Space موجود موقتاً بوضعه الحالي كما هو طالما لم يسبب أي مشاكل اوعقبات وربما اخفيه بعد الربط الجديد - موقتاً الى ان نتأكد من ربط Fly.io"* |
| 🆕 **فرع نظيف من main لكل تعديل** (`feat/...` ثم `--ff-only`) | تاريخ خطي + قابلية rollback | كتابة مباشرة على main | اختيار المالك: *"ب — فرع جديد نظيف من main"* |
| 🆕 **`@mcp.custom_route("/health")` بدل Starlette wrapper** | أبسط (4 أسطر)، لا يلامس session_manager lifecycle | Starlette `Mount("/mcp", app=...)` | راجع §10 والقرار النهائي بعد مراجعة الـ FastMCP source + موقع GitHub Issue #1467 |
| 🆕 **`grace_period="15s"` للـhealth check** | تجاوز ~7s startup time لـUvicorn | grace أصغر (5s) | بعد ملاحظة race بين Fly check و server startup |
| 🆕 **نموذج الخدمة: علنيّ مع rate limiting (السيناريو ب)** | المشروع وقف/خدمة، لكن لا بد من حماية مالية | (أ) مغلق بـauth، (ج) مفتوح بلا حدود | اختيار المالك حرفياً: *"السيناريو ب — علنيّ لكن بحدود (rate limiting)"* |
| 🆕 **Fly.io Spending Limit فورياً ($5 / $25)** | حماية ضد abuse، نوم مرتاح | تأجيله، أو حد أكبر | اختيار المالك: *"نعم، فوراً (أولوية)"*. الرقمان من اقتراح assistant ($5 Soft / $25 Hard). |
| 🆕 **GitHub Collaborator + Write + Branch Protection لتسليم المبرمجين** | يحفظ سير العمل، يفعّل PR review، لا ينقل ملفات | تسليم ملفات على جهاز المطوّر | اقتباس المالك (في سياق التسليم): *"حاليا تم الانتهاء من المشروع بالكامل، اذا بسلم المشروع المبرمجين لعمل تحديثات مستقبلية، هل اسلمهم الملف على جهازي ام اضفهم في github"* — قُبل اقتراح الـ Collaborators. |
| 🆕 **Model A للنشر بعد التسليم: المالك يُنفّذ `fly deploy`** | الـCD يبقى في يد المالك، المبرمجون يرسلون PRs | إعطاء المبرمجين صلاحية `fly deploy` | قرار الـassistant، قُبل بدون اعتراض |
| 🆕 **Bash style: `&& \` + `set -e` للأوامر الحساسة** | يمنع تنفيذ خطوة عند فشل سابقتها | `;` (لا توقف) أو `&&` فقط (لا echo) | اعتمده المالك بعد مقارنة بين نسختي أوامر |
| 🆕 **استخدام VS Code لتعديل الملفات بدل heredoc في Terminal** | Bracketed Paste يفشل أحياناً في macOS Terminal، VS Code يلصق نظيفاً | اللصق المباشر في Terminal | اقتراح الـassistant بعد بلاغ المالك *"اللصق لا يعمل... يصدر صوت من الماك ولا يلصق النص"* |

### قرارات تغيّرت في منتصف المحادثة

| القرار الأول | القرار النهائي | السبب |
|---|---|---|
| النشر تحت `ah-vb-cod` (شخصي) | النشر تحت منظمة `tafsircenter` على GitHub | المالك حصل على إذن المركز لإنشاء المنظمة |
| Claude Desktop كهدف ربط أساسي | Claude Code (داخل VS Code) ثم لاحقاً Claude Code عبر HTTP transport (الإنتاج) | اكتشاف أن Anthropic فصلت دعم MCP عن Chat |
| 🆕 الاستضافة على HF Space فقط | Fly.io على `mcp.tafsir.net`، مع HF Space كاحتياطي | تحضير لـAlibaba ECS مع تقليل الـvendor lock-in عبر نطاق مخصص |
| 🆕 افتراض أن `fly checks` تُعيد تشغيل الـmachine عند الفشل | الفهم النهائي: فقط `auto_routing` يحدث عند unhealthy؛ إعادة التشغيل تحدث فقط عند process crash | تحقّق من توثيق Fly.io؛ assistant صحّح فهمه بناءً على رد المالك |

---

## ١٠. المقاربات المرفوضة

| ما جُرّب | لماذا رُفض | ماذا حلّ محله |
|---|---|---|
| ربط الخادم بـ Claude Desktop (Chat) | لا يدعم MCP في Chat (مايو 2026) | Claude Code داخل VS Code (محلياً) أو HTTP transport (الإنتاج) |
| `Field(default=val)` مع type hints | ينتج FieldInfo bug في FastMCP | `Annotated[T, Field(...)] = default` |
| `@mcp.tool` decorator مباشرة | يُجبر اسم MCP = اسم Python | `mcp.tool(name="...")(fn)` داخل `register()` |
| الاعتماد على ذاكرة Claude للنص القرآني | هلوسة موثّقة (آية البقرة 300) | كل نص يمر عبر `fetch_ayah` مع Pydantic validation |
| تضمين `quran.db` (214MB) في PyPI | حد PyPI 100MB | استبعاد + تحميل تلقائي من HF |
| `urllib.request.urlretrieve` للتحميل | macOS SSL CERTIFICATE_VERIFY_FAILED | `huggingface_hub.hf_hub_download` (يستخدم certifi) |
| كتابة SQL بـ f-strings | SQL injection + خطر | `?` parametrized حصراً |
| تخمين أسماء أعمدة DB | خطأ متكرر | فحص استباقي عبر `inspect_schema.py` + `SCHEMA_NOTES.md` |
| تشذيب الإسناد في nuzool لاختصار الرد | إخلال بالأمانة العلمية | إعادة النص حرفياً + `available: true/false` |
| Parsing داخلي لتنسيق qeraat `@قارئ/نص@` | parsers هشة | إرجاع `qeraat_raw` + `format_note` |
| النشر تحت حساب شخصي ah-vb-cod | عدم اتساق مع HF/PyPI | منظمة tafsircenter على GitHub |
| `read -s hf_xxxxx` (التوكن كاسم متغير) | التوكن انكشف في history | `read -s HF_TOKEN` ثم لصق التوكن (مخفياً) |
| إصدار v0.x كـ beta | البيانات معتمدة سلفاً | v1.0.0 مباشرة |
| 🆕 **Starlette wrapper / Mount(`/mcp`, app=...) لإضافة `/health`** | المخاطر الموثّقة: GitHub Issue #1467 "Task group is not initialized" + 307 redirects + ASGI lifespan لا يُدار صحيحاً + `session_manager` يرفع RuntimeError عند الوصول إليه قبل `streamable_http_app()` | `@mcp.custom_route("/health", methods=["GET"])` — 4 أسطر، لا تلامس lifecycle |
| 🆕 **اعتماد `auto_routing` كـ"إعادة تشغيل"** | فهم خاطئ: `health check` لا يعيد تشغيل machines؛ فقط يوجّه traffic بعيداً عن unhealthy | إعادة التشغيل تحدث فقط عند crash؛ سياسة default on-fail تُعيد التشغيل |
| 🆕 **`fly deploy` مباشرة من branch غير main** | يفقد التتبع، يصعّب rollback | `feat/X` → `main --ff-only` → `git push` → `fly deploy` |
| 🆕 **لصق heredoc طويل في Terminal على macOS** | Bracketed Paste يفشل أحياناً، صوت bell، لا إدخال | تعديل الملف في VS Code + `code <file>` |
| 🆕 **حذف HF Space بدلاً من جعله Private** | يفقد commit `81e42d9` (transport_security fix على HF only) ويُلغي إمكانية الـrevival | جعله Private |
| 🆕 **تسليم الملفات للمبرمجين على جهاز المطوّر** | عدم تتبع، لا PR review، انقطاع عن origin | إضافتهم كـ Collaborators مع Write + Branch Protection على main |

---

## ١١. العقبات التي واجهناها وحلولها (المحتوى الأهم لفريق التطوير)

### ١١.١ عقبة: Claude Desktop لا يدعم MCP في Chat
**السياق:** بعد بناء MVP وإعداد `claude_desktop_config.json`، حاول المالك ربط الخادم وضغط على أيقونة الـPlugins، فظهرت رسالة Anthropic الرسمية: *"Plugins run locally and aren't available in Chat. Switch to Cowork or Code to use plugins."*

**الحل:** انتقلنا فوراً لـ Claude Code داخل VS Code: `claude mcp add tafsir --scope user -- uv --directory ... run tafsir-mcp`.

**لماذا نجح:** Claude Code هو المنتج الذي يدعم MCP رسمياً في 2026. Anthropic فصلت تجربة المحادثة عن تجربة التطوير.

---

### ١١.٢ عقبة: أسماء الأعمدة في DB ليست كما يُتوقع
**السياق:** أراد الكود `SELECT irab FROM ayah_content_irab` فظهر خطأ.

**الاكتشافات التسعة:**
1. تفاسير الخمسة تستخدم `sura/aya`، كل الباقي `surahNo/ayahNo` 🔴
2. `word_content_irab` العمود `irabMushakkal` (ليس `irab`) 🔴
3. `ayah_content_irab` العمود `irabAyah1` (ليس `irab`) 🔴
4. `mokhtasar_fawaed` صفوف متعددة لكل صفحة (`fetchall`) 🟡
5. `qeraat_info.content` بتنسيق `@قارئ/نص@` 🟡
6. `nozoolInfo` = سند + متن في عمود واحد ✅
7. `word_statistics.repeatitionCount` مهجأ خطأ ℹ️
8. القرآن مترجم كاملاً (0 NULL في Mukhtasar*) ✅
9. الحروف المقطعة (`الم`، `يس`) كلمة واحدة ✅

**الحل:** سكربت `scripts/inspect_schema.py` يفحص `PRAGMA table_info` ويولّد `SCHEMA_NOTES.md`. ثوابت `TAFSIR_KEYS` و`STANDARD_KEYS` في `db.py`.

**لماذا نجح:** **الفحص قبل الكتابة** بدلاً من تخمين.

---

### ١١.٣ عقبة: Pydantic Field يُنتج FieldInfo
**السياق:** في أول إصدار، بعض المعاملات بـ `Field()` ظهرت قيمها كـ `FieldInfo(annotation=...)`.

**الحل:** اكتشفه المالك: *"Field() كـ default value في دوال عادية يُنتج FieldInfo بدل القيمة — الحل الصحيح هو `Annotated[int, Field(...)] = default`"*.

---

### ١١.٤ عقبة: تشخيص متسرّع بأن الأدوات غير مسجَّلة
**السياق:** قفز الـassistant لاستنتاج أن الأدوات لم تُسجَّل لمجرد عدم وجود `@mcp.tool` في `server.py`. التشخيص الحقيقي: نمط `register(mcp)` معتمد، تحقّق المالك بـ `asyncio.run(mcp.list_tools())` فطبع 13 أداة.

**الحل:** اعتذار + توثيق النمط.

**درس:** اختبارات Python النظيفة (35/35) لا تضمن أن الـMCP layer مسجَّل. يجب اختباره منفصلاً.

---

### ١١.٥ عقبة: macOS SSL Certificate Verify Failed
**السياق:** `ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED]` عند `urllib.request`.

**السبب الجذري:** Python من python.org على macOS يأتي بدون شهادات SSL مدمجة.

**الحل:** استبدال `urlretrieve` بـ `huggingface_hub.hf_hub_download` (يستخدم certifi، يدعم Resume).

**درس:** على macOS، لا تستخدم urllib لتحميل https — استخدم `requests`، `httpx`، أو `huggingface_hub`.

---

### ١١.٦ عقبة: تسريب التوكن في Terminal History
**السياق:** المالك كتب `read -s [[HF_TOKEN_REDACTED — قيمة سرّ أُزيلت أمنياً 2026-06-02]]` — ظنّاً منه أن `-s` يعني "stealth". لكن `read -s VAR` يحفظ متغيراً اسمه `hf_udOJ...`، **والتوكن انكشف** في sessions السابقة.

**الحل الطارئ:** إلغاء التوكن من https://huggingface.co/settings/tokens + إنشاء جديد + استخدام `read -s HF_TOKEN` ثم لصق التوكن مخفياً ثم `export HF_TOKEN`.

**درس لكل فريق المستقبل:** **لا تكتب أبداً توكناً في command line مباشرة**.

---

### ١١.٧ عقبة: GitHub رفض الـpush بسبب workflow scope
**السياق:** `! [remote rejected] main -> main (refusing to allow an OAuth App to create or update workflow ...)`

**الحل:** `gh auth refresh -s workflow`

---

### ١١.٨ عقبة: ربط `tafsir-center` (شرطة) مقابل `tafsircenter` (بدون)
**السياق:** Claude Code أنشأ `data_loader.py` بـ `repo_id = "tafsir-center/tafsir-mcp-data"` (مع شرطة)، لكن حساب HF الفعلي `tafsircenter`.

**الحل:** Plan Mode في Claude Code كشف التعارض قبل التنفيذ. توحيد على `tafsircenter`.

**درس:** اتساق الأسماء عبر المنصات ضروري.

---

### ١١.٩ عقبة: لصق نص HTML في Terminal
**السياق:** نسخ محتوى صفحة GitHub ولصقه في Terminal. `>` فُسِّر كـ redirect، دخل في prompt متابعة.

**الحل:** `Ctrl + C` ثم استخدام `pbpaste > filename.txt`.

---

### ١١.١٠ عقبة: `uv publish` أُرسل إلى MCP server يعمل
**السياق:** بعد اختبار `uvx tafsir-mcp`، كتب المالك `uv publish` في نفس Terminal. الخادم فسّر النص كـ JSON-RPC: `ERROR Received exception from stream: Invalid JSON`.

**الحل:** `Ctrl + C` لإنهاء الخادم، ثم نفّذ `uv publish` بنظافة.

---

### ١١.١١ عقبة: تحذيرات `SyntaxWarning` من pyarabic
**السياق:** `SyntaxWarning: "\w" is an invalid escape sequence`.

**التشخيص:** Bug قديم في `pyarabic` (regex بدون raw strings). لا يكسر الوظيفة.

**الحل:** نتركها. لاحقاً يمكن تقديم PR أو `warnings.filterwarnings("ignore", ...)`.

---

### ١١.١٢ 🆕 عقبة: Bracketed Paste يفشل في macOS Terminal
**السياق:** عند محاولة لصق heredoc متعدد الأسطر في Terminal للتعديل على `deploy/server_http.py`. اقتباس المالك: *"يصدر صوت من الماك ولا يلصق النص المنسوخ"* و *"الTerminal المفتحو لا يستجيب للكتابة او اللصق - ما العمل"*.

**التشخيص:** Bracketed Paste mode تعطّل في الجلسة الحالية للـTerminal.

**الحل:**
1. أغلق Terminal واحدة جديدة (لم يحل المشكلة كلياً)
2. **استخدام VS Code للتعديل:** `code deploy/server_http.py` ثم لصق المحتوى ثم Save.
3. عيوب جانبية من VS Code paste:
   - 3-backtick code fences أحياناً تصبح 4-backticks (يُحل بـFind/Replace)
   - Trailing newline يضيع (`echo "" >> fly.toml` يحلّها)

**درس:** عند فشل Terminal، VS Code خيار ثاني سريع. لا تصارع Terminal.

---

### ١١.١٣ 🆕 عقبة: `session_manager` يرفع RuntimeError قبل بدء streamable_http_app
**السياق:** أثناء استكشاف خيار Starlette wrapper لإضافة `/health`، اختبر الـassistant `mcp.session_manager` فظهر:
```
RuntimeError: Session manager can only be accessed after calling streamable_http_app().
The session manager is created lazily to avoid unnecessary initialization.
```

**التشخيص:** هذا تأكيد على أن نمط Starlette wrapper يحمل خطراً حقيقياً (يطابق GitHub Issue #1467 "Task group is not initialized").

**الحل:** اعتماد `@mcp.custom_route("/health")` decorator (الذي ثبت توفّره في `dir(FastMCP)` = `True` في v1.27.1). 4 أسطر فقط، لا يلامس session_manager lifecycle.

```python
@mcp.custom_route("/health", methods=["GET"])
async def health(request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok", "service": "tafsir-mcp"})
```

**درس:** **قبل اختيار نمط معماري، تحقّق من الـsource: `import; print(dir(...))`**. لا تخمن.

---

### ١١.١٤ 🆕 عقبة: Fly deploy WARNING "The app is not listening"
**السياق:** بعد `fly deploy`، ظهرت رسالة `WARNING The app is not listening` رغم أن الخادم يعمل.

**التشخيص:** Race timing — Fly proxy يفحص بعد ~5 ثوان، لكن Uvicorn يستغرق ~7 ثوان للبدء. الفحص الأول قبل grace_period يفشل، لكن `[[http_service.checks]]` (مع grace=15s) ينجح لاحقاً.

**الحل:** التحذير cosmetic. `fly checks list` يُظهر `passing` بعد الـgrace. `fly status` يُظهر `1 total، 1 passing`. `curl -i https://mcp.tafsir.net/health` يُرجع `HTTP/2 200`.

**درس:** الـwarning ليس error. تحقّق دائماً من `fly checks list` الأخير، ومن endpoint عملياً.

---

### ١١.١٥ 🆕 عقبة: فهم خاطئ لسلوك Fly health checks
**السياق:** افترض الـassistant أن فشل الـhealth check سيعيد تشغيل الـmachine.

**التشخيص الصحيح (بعد المراجعة):** Fly health checks تفعل أمرَين:
1. توجيه traffic بعيداً عن الـmachine الـunhealthy (auto-routing عبر anycast)
2. **لا تعيد تشغيله تلقائياً**

إعادة التشغيل تحدث فقط عند process crash، عبر سياسة Machine restart default (`on-fail`).

**الحل:** تصحيح الفهم. الـhealth check هي signal لتوجيه الـtraffic، ليست restart trigger.

**درس:** اقرأ docs ولا تخمن سلوك platform.

---

### ١١.١٦ 🆕 عقبة: HF Space ما زال يحوي commit مفيد فقط على HF
**السياق:** على HF Space، هناك commit `81e42d9` (transport_security fix) ليس موجوداً على GitHub.

**التشخيص:** المحتوى الفعلي للـfix الآن موجود في `deploy/server_http.py` (في الـoverride لـ transport_security)، لكن الـcommit التاريخي على HF فقط.

**الحل:** اعتماد **Private not Delete** لـHF Space — يحفظ التاريخ ويتيح revival لو فشل Fly.io.

---

## ١٢. القيود الصارمة (Hard Constraints)

> ⛔ **هذه القواعد موثَّقة في `CLAUDE.md` ولا يجوز كسرها مطلقاً.**

### ١٢.١ شرعية (محتوى ديني)
1. **No content generation.** الأدوات تُرجع البيانات حرفياً من DB. لا تلخيص، لا إعادة صياغة، لا "تحسين".
2. **Always attribute.** كل تفسير يُرجع مع `source` يحوي: اسم المؤلف + عنوان الكتاب + سنة الوفاة.
3. **حفظ الإسناد كاملاً** في أسباب النزول. لا تشذيب، لا حذف.
4. **عدم إضافة تفاسير جديدة** بدون اعتماد مكتوب من مركز تفسير.
5. **عدم تعديل النصوص الموجودة** بدون مراجعة شرعية موثَّقة.

### ١٢.٢ أمنية (برمجية)
6. **Read-only DB إلزامي:** `sqlite3.connect(f"file:{path}?mode=ro", uri=True)` + `PRAGMA query_only=ON`.
7. **Parametrized SQL فقط:** `?` placeholders. ممنوع أي f-string أو string concatenation في SQL.
8. **لا اتصال خارجي من الأدوات:** `openWorldHint=False`. التحميل من HF يحدث **فقط** عند التهيئة، ليس داخل أداة.
9. **لا تخزين توكنات في الكود:** كل التوكنات عبر متغيرات بيئة. `.env` و `scripts/.db_sha256` في `.gitignore`.

### ١٢.٣ التحقق
10. **Pydantic validation** لكل معامل أداة: `Annotated[int, Field(ge=1, le=114)]`.
11. **الأرقام المرجعية الإلزامية:** 114 سورة، 6,236 آية، 77,432 كلمة، 1,891 جذر، 604 صفحة، 201 آية نزول.
12. **التحقق من عدد آيات السورة** عند validation: `ayah ≤ SURAH_AYAH_COUNTS[surah]`.
13. **SHA256 verification** بعد تحميل DB من HF. عدم التطابق → حذف الملف الفاسد + RuntimeError.

### ١٢.٤ رسائل المستخدم
14. **رسائل الخطأ بالعربية الفصحى** ("السورة 1 تحوي 7 آيات فقط").

### ١٢.٥ ترخيص ونسبة
15. **كل تفسير منسوب لمؤلفه** بالنص الحرفي في `TAFSIR_ATTRIBUTIONS`.
16. **CC BY 4.0 للمحتوى:** نسبة "Markaz Tafsir for Quranic Studies" إلزامية لأي إعادة استخدام.
17. **MIT للكود:** حر تماماً.

### ١٢.٦ حجم وأداء
18. **حد PyPI 100 MB:** الحزمة لا تحوي `quran.db`. الحجم: 30 KB (wheel) + 107 KB (sdist).
19. **زمن استجابة الأدوات < 100ms محلياً** (مع الفهارس).

### ١٢.٧ 🆕 تشغيلية (Fly.io)
20. **Spending Limit إلزامي على Fly.io** (Hard $25 افتراضياً). كسره = خطر فاتورة مفاجئة من abuse.
21. **`mcp.tafsir.net` هو الرابط الرسمي**، ليس `tafsir-mcp.fly.dev`. الأخير backup يجب ألا يُنشر علناً.
22. **Branch protection على `main`:** عند تسليم المشروع، لا يُسمح بـpush مباشر إلى `main`؛ كل تعديل يمر بـPR + Approve.
23. **Fast-forward only merges:** لا merge commits على `main`.
24. **Healthcheck path = `/health`** لا غير. أي تغيير يتطلب تحديث `fly.toml` و `deploy/server_http.py` بنفس الـcommit.

### ١٢.٨ 🆕 إدارية
25. **Fly deploys بيد المالك فقط** (Model A): الـcommitter لا يستلم صلاحية `fly deploy` تلقائياً.
26. **HF Space يبقى Private، لا يُحذف.** يحفظ التاريخ ويتيح revival.

---

## ١٣. أمثلة عملية (Few-shot)

### مثال 1: أداة كاملة (style مرجعي)
```python
# في src/tafsir/tools/ayah.py
from typing import Annotated, Literal
from pydantic import Field, validate_call
from tafsir.db import query_one, query_all
from tafsir.models import AyahReference
from tafsir.normalize import reconstruct_ayah


@validate_call
def get_ayah(
    surah: Annotated[int, Field(ge=1, le=114, description="رقم السورة")],
    ayah: Annotated[int, Field(ge=1, description="رقم الآية")],
    include: list[Literal["text", "tajweed", "irab"]] = ["text"],
) -> dict:
    """جلب نص آية مع خيارات إضافية.

    Args:
        surah: Surah number (1-114).
        ayah: Ayah number within the surah.
        include: Which extras to fetch (tajweed/irab).
    """
    AyahReference(surah=surah, ayah=ayah)  # validates ayah <= surah_length

    rows = query_all(
        "SELECT word, wordNo FROM word_content_rasm "
        "WHERE surahNo = ? AND ayahNo = ? ORDER BY wordNo",
        (surah, ayah),
    )
    text = reconstruct_ayah(rows)

    result: dict = {
        "surah": surah, "ayah": ayah, "text": text,
        "tajweed": None, "irab": None, "word_count": len(rows),
    }

    if "tajweed" in include:
        row = query_one(
            "SELECT tajweed FROM ayah_content_tajweed WHERE surahNo = ? AND ayahNo = ?",
            (surah, ayah),
        )
        result["tajweed"] = row["tajweed"] if row else None

    if "irab" in include:
        row = query_one(
            "SELECT irabAyah1 FROM ayah_content_irab WHERE surahNo = ? AND ayahNo = ?",
            (surah, ayah),
        )
        result["irab"] = row["irabAyah1"] if row else None

    return result
```

### مثال 2: تسجيل برمجي
```python
# نهاية tools/ayah.py
def register(mcp):
    """Register all ayah-level tools with the MCP server."""
    annotations = {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    }
    mcp.tool(name="fetch_ayah", annotations=annotations)(get_ayah)
    mcp.tool(name="fetch_tafsir", annotations=annotations)(get_ayah_tafsir)
    mcp.tool(name="fetch_nuzool_reason", annotations=annotations)(get_ayah_nuzool)
```

### مثال 3: db.py (read-only + parametrized)
```python
# في src/tafsir/db.py
import sqlite3
from tafsir.data_loader import get_db_path

TAFSIR_KEYS = ("sura", "aya")
STANDARD_KEYS = ("surahNo", "ayahNo")


class QuranDataError(Exception):
    """يُرفع عند خطأ في قراءة قاعدة بيانات القرآن."""


def get_connection() -> sqlite3.Connection:
    path = get_db_path()
    if not path.exists():
        raise FileNotFoundError(f"قاعدة البيانات غير موجودة: {path}")
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True, check_same_thread=False)
    conn.execute("PRAGMA query_only = ON")
    conn.row_factory = sqlite3.Row
    return conn


def query_one(sql: str, params: tuple = ()) -> dict | None:
    conn = get_connection()
    try:
        row = conn.execute(sql, params).fetchone()
        return dict(row) if row else None
    except sqlite3.DatabaseError as e:
        raise QuranDataError(f"خطأ في الاستعلام: {e}") from e
    finally:
        conn.close()
```

### مثال 4: 🆕 deploy/server_http.py (المحرّك الذي يعمل على Fly.io)
```python
"""HTTP MCP server entry-point for cloud deployment (Fly.io).

يختلف عن src/tafsir/server.py في أنه يستخدم transport=streamable-http،
ويضيف نقطة /health للـ Fly health checks.
"""
import os
from starlette.requests import Request
from starlette.responses import JSONResponse

from tafsir.server import mcp  # نفس FastMCP instance مع الأدوات الـ13

# Override transport_security لـ DNS rebinding في بيئة Fly
mcp.streamable_http_app.transport_security.enable_dns_rebinding_protection = False


@mcp.custom_route("/health", methods=["GET"])
async def health(request: Request) -> JSONResponse:
    """Health check for Fly.io / load balancer probes.

    Returns minimal payload with NO secrets — custom_route bypasses MCP auth
    middleware by design (FastMCP documented behavior).
    """
    return JSONResponse({"status": "ok", "service": "tafsir-mcp"})


def main():
    host = "0.0.0.0"
    port = int(os.getenv("PORT", 7860))
    mcp.run(transport="streamable-http", host=host, port=port)


if __name__ == "__main__":
    main()
```

### مثال 5: 🆕 fly.toml (تكوين الإنتاج)
```toml
app = 'tafsir-mcp'
primary_region = 'bom'

[build]
  dockerfile = 'deploy/Dockerfile'

[http_service]
  internal_port = 7860
  force_https = true
  auto_stop_machines = 'stop'
  auto_start_machines = true
  min_machines_running = 0
  processes = ['app']

  [[http_service.checks]]
    grace_period = "15s"
    interval = "30s"
    method = "GET"
    timeout = "5s"
    path = "/health"

[[vm]]
  memory = '1gb'
  cpus = 1
  memory_mb = 1024
```

### مثال 6: 🆕 سير عمل النشر (الـ pipeline الذي اعتمده المالك)
```bash
cd ~/projects/quranic-scholar-mcp && \
set -e && \
git switch -c feat/healthcheck && \
echo "Step 1: edit deploy/server_http.py" && \
code deploy/server_http.py && \
echo "Step 2: edit fly.toml" && \
code fly.toml && \
echo "Step 3: local test" && \
uv run python deploy/server_http.py &
sleep 7
curl -i http://localhost:7860/health && \
kill %1 && \
echo "Step 4: commit" && \
git add -A && \
git commit -m "feat: add /health endpoint and Fly health check" && \
echo "Step 5: merge fast-forward" && \
git switch main && \
git merge feat/healthcheck --ff-only && \
git push origin main && \
echo "Step 6: deploy" && \
fly deploy && \
echo "Step 7: verify" && \
fly checks list && \
curl -i https://mcp.tafsir.net/health && \
echo "Step 8: cleanup" && \
git branch -d feat/healthcheck
```

---

## ١٤. مفردات وتعابير متّفق عليها

### ١٤.١ مصطلحات قرآنية (في الكود والوثائق)
| العربية | الإنجليزية في الكود | المعنى |
|---|---|---|
| سورة | surah | فصل (114 منها) |
| آية | ayah | آية (6,236) |
| كلمة | word | كلمة من الرسم العثماني (77,432) |
| رسم عثماني | rasm | شكل كتابة المصحف |
| تجويد | tajweed | أحكام التلاوة |
| إعراب | irab | تحليل نحوي |
| صرف | sarf | تحليل صرفي |
| جذر | root | جذر لغوي (1,891) |
| تفسير | tafsir | شرح علمي |
| سبب نزول | nuzool / nozool | سياق نزول الآية |
| إسناد | isnad | سلسلة الرواة |
| متن | matn | النص بعد الإسناد |
| قراءات | qeraat | اختلاف القراء |
| مكي | makki | نزل قبل الهجرة |
| مدني | madani | نزل بعد الهجرة |
| فوائد | fawaed | استنباطات علمية من الصفحة |

### ١٤.٢ مصطلحات تقنية في المحادثة
| المصطلح | الاستخدام |
|---|---|
| **Plan Mode** | وضع Claude Code (Shift+Tab) — يعرض الخطة قبل التنفيذ |
| **Checkpoint** | نقطة تحقق بعد كل خطوة (✅) |
| **Prompt N** | برومبت معدّ مسبقاً يُلصق في Claude Code |
| **register pattern** | تسجيل الأدوات برمجياً بـ `mcp.tool(name="...")(fn)` |
| **schema-first** | فحص أعمدة DB قبل كتابة استعلامات |
| **agentic test** | اختبار يستدعي عدة أدوات بتسلسل |
| **3-tier path resolution** | env → data/ → ~/.cache (في data_loader) |
| **TAFSIR_KEYS / STANDARD_KEYS** | ثابتان لتمييز مفاتيح SQL |
| 🆕 **stdio mode** | تشغيل MCP محلي عبر stdin/stdout (لـClaude Code) |
| 🆕 **streamable-http** | transport HTTP الذي يستخدمه `deploy/server_http.py` على Fly.io |
| 🆕 **السيناريو ب** | "علنيّ مع rate limiting" — نموذج الخدمة المعتمد |
| 🆕 **Model A للنشر** | المالك يُنفّذ `fly deploy`، المبرمجون يرسلون PRs فقط |
| 🆕 **fast-forward only** | سياسة دمج لا تسمح بـmerge commits |
| 🆕 **Bracketed Paste workaround** | استخدام VS Code بدل لصق heredoc في Terminal |
| 🆕 **`auto_stop=stop` + `min=0`** | استراتيجية Fly.io لتوفير 95% من التكلفة عند idle |
| 🆕 **race timing warning** | تحذير `WARNING The app is not listening` الـcosmetic بعد deploy |

### ١٤.٣ عبارات المالك المتكررة
- **"المهمة مكتملة ✅"** — صيغة الإبلاغ القياسية
- **"35/35 ✓"** — نتيجة الاختبارات الكاملة
- **"تم"** — تأكيد قصير بعد كل خطوة
- **"اعرض الخطة أولاً ثم نفّذ"** — قبل أي تعديل كبير
- **"خلك معي خطوة خطوة"** — تفضيل الإيقاع البطيء عند الإجراءات الحساسة
- 🆕 **"قارن امرك المرسل وهذا الامر وفكر في ايهما اصح ولماذا"** — يطلب critique قبل التنفيذ
- 🆕 **"ناقشني لو ما فهمت او تحتاج تاكيد او تصحيح"** — يدعو لـclarification بدل افتراض

---

## ١٥. أسلوب التواصل (للنموذج الذي يكمل فقط)

> ⚠️ هذا القسم موجّه لـ AI الذي يستأنف العمل. فريق التطوير البشري يمكنه تجاوزه.

| البُعد | التفضيل المُلاحظ |
|---|---|
| **اللغة الأساسية** | العربية، مع مصطلحات تقنية بالإنجليزية |
| **طول الرد** | متوسط إلى طويل — يقدّر التفصيل، يكره الحشو |
| **الترتيب** | **الإجراء/الكود أولاً، الشرح ثانياً** |
| **الشكل** | جداول، ✅/❌، code blocks بلغة محددة، عناوين Markdown |
| **النبرة** | عملية مباشرة احترافية. لمسات روحية مقتصدة (🌙، آية، دعاء قصير) في اللحظات المهمة |
| **خطوة بخطوة** | **حاسم.** أمر واحد ثم انتظار. اقتباس حرفي: *"خلك معي خطوة خطوة - بحيث ترسل الامر وتنتظر الرد وهكذا - لا ترسل مجموعة اوامر ثم نرجع نعيدها"* |
| **التأكيدات** | يطلب "اعرض الخطة أولاً ثم نفّذ" قبل أي تعديل كبير |
| **التفاعل مع الأخطاء** | يلصق نص الخطأ كاملاً، يتوقع تشخيصاً دقيقاً |
| **اللقطات** | يرسل لقطات شاشة عند الحاجة (UI checks) |
| **القرارات** | يجيب بالحرف فقط (`A`, `B`, `C`, `c`) عند طرح خيارات |
| **سرعة التقدم** | سريع جداً — من PyPI launch إلى Fly.io launch في ~24 ساعة |
| **منصة التشغيل** | macOS Apple Silicon — الأوامر المخصصة لها مفضّلة |
| **استراتيجية المراجعة** | يطلب critique مقارن: *"احتاجك مره اخيره تفحص وتقارن ردك بالرد التالي"* — يلصق رد expert آخر ويطلب الـAI أن يقارن. أحياناً يبني قراره على الـAI الذي يعترف بخطأه. |
| **Bracketed Paste** | فاشل على macOS Terminal أحياناً → VS Code بديل سريع |
| **محرر مفضّل** | **VS Code** (مؤكّد في الجلسة) |
| **شِك بناء وحذر مالي** | بعد نشر الخدمة، طرح سؤال economic: *"هل حاليا يستطيع مبرمج استخدام رابط mcp.tafsir.net/mcp في بناء تطبيق ويستغله وانا اللي ادفع اشتراك fly.io"* — هذا نوع التفكير الذي يستحق الـAI أن يبادر به دون انتظار |

### الأخطاء التي يجب تجنّبها مع هذا المالك:
1. ❌ إرسال 10 أوامر دفعة واحدة (يفضّل أمراً واحداً ثم انتظار)
2. ❌ شرح مطوّل قبل إعطاء الأمر (الإجراء أولاً)
3. ❌ افتراضات خاطئة بدون فحص (مثل ما حدث مع `@mcp.tool` — اعتذرت)
4. ❌ تخمين schema بدون `PRAGMA table_info`
5. ❌ كتابة توكنات أو إخراجها في الكود
6. ❌ إنكار خطأ بدلاً من الاعتراف به
7. 🆕 ❌ افتراض سلوك platform (Fly.io) بدون قراءة docs
8. 🆕 ❌ صراع مع Bracketed Paste — انتقل لـVS Code فوراً
9. 🆕 ❌ تشخيص متسرّع لـconnector issues — لو deploy ينجح ويُرجع `1 total، 1 passing`، لا تفترض أنه فاشل
10. 🆕 ❌ إغفال بُعد الاقتصاد عند نشر خدمة عامة (التكلفة، abuse، spending limit)

### السمات الإيجابية للمالك (worth recognizing):
1. ✅ يطلب critique بدلاً من قبول الـAI بشكل أعمى
2. ✅ يحافظ على git history نظيفاً (Conventional Commits، fast-forward)
3. ✅ يعمل خطوة بخطوة بدلاً من القفز
4. ✅ صاغ بيده DEPLOY.md كامل (222 سطراً) — يعرف الكتابة الفنية
5. ✅ متحفظ في المخاطر المالية (سأل عن economics قبل أن يُذكّر)

---

## ١٦. الأسئلة المعلقة والمخاطر المعروفة

### ١٦.١ معلّق رسمياً (يحتاج قراراً)

| البند | الحالة | الإجراء المطلوب |
|---|---|---|
| ⏳ **Fly.io Spending Limit setup** | المالك ملتزم لكن لم يؤكّد إتمام الخطوة | المالك يفتح الـdashboard ويضبط $5/$25 |
| **إخفاء HF Space** | لم يبدأ | Settings → Change Visibility → Private |
| **تنفيذ rate limiting** | لم يبدأ | جلسة كود قادمة (~30 دق) |
| **GitHub Release v1.0.0** | لم يُنشأ بعد (pending من v2 Context Pack) | `gh release create v1.0.0` |
| **Trusted Publishing** | معدّ على PyPI لكن غير مُختبر | يحتاج Release + GitHub Environment |
| **Required Reviewer** على Environment "pypi" | لم يُفعَّل | حماية الإصدارات القادمة |
| **التسجيل في MCP Registry** | لم يُقدَّم PR | اختياري لكن يزيد الاكتشاف |
| **مراجعة شرعية رسمية مكتوبة** | شفهية فقط من المالك | "اعتبرها معتمدة" — توثيق رسمي مستقبلي |
| **شعار المشروع** | غير محدد | الحصول من مركز تفسير |
| **توقيت ترحيل Alibaba ECS** | غير محدد | Phase 2، النطاق المخصص جاهز للترحيل |
| **توقيت إضافة المبرمجين كـCollaborators** | غير محدد | عند الحاجة الفعلية للتسليم |

### ١٦.٢ مخاطر تقنية معروفة

| الخطر | التأثير | المخفّف |
|---|---|---|
| `pyarabic` SyntaxWarning في Python 3.14+ | تحذيرات في logs، لا كسر | متابعة إصدارات pyarabic |
| `repeatitionCount` (مهجأ خطأ في DB) | يجب تذكّره عند كل استعلام | ثابت في كود + تعليق `# sic` |
| `qeraat_info.content` بتنسيق غير معياري | الباحث يرى نصاً خاماً | parser منفصل مستقبلاً |
| اعتماد على Hugging Face في التحميل | لو HF تعطّل، التثبيت الأول يفشل | المستخدم يضع `data/quran.db` يدوياً |
| 35 اختباراً تختبر دوال Python مباشرة | لا تختبر MCP wire format | إضافة integration tests عبر `mcp.list_tools()` |
| 🆕 **Race timing warning في Fly deploy** | UX سيء لمن لا يعرف | grace_period=15s يكفي عادة؛ التوثيق في DEPLOY.md |
| 🆕 **`auto_stop=stop` cold-start latency** | أول طلب بعد سكوت طويل قد يأخذ ~5-10s | معتمد بوعي — التوفير في التكلفة يفوق |
| 🆕 **`session_manager` RuntimeError** عند الوصول قبل بدء HTTP app | لن يؤثر على المستخدم النهائي | تجنبه — استخدم `custom_route` |
| 🆕 **عدم وجود auth على `/mcp`** | اي مبرمج يستخدمه ويستهلك billing | rate limiting قادم؛ Spending Limit حماية فورية |
| 🆕 **single region (`bom`)** | المستخدمون خارج آسيا يلاقون latency عالٍ | مقبول الآن؛ توسّع لاحقاً إن لزم |

### ١٦.٣ مخاطر شرعية ووظيفية

| الخطر | التأثير | المخفّف |
|---|---|---|
| اكتشاف خطأ في نص قرآني في DB | فادح شرعياً | المالك أكّد المراجعة، لكن لا يوجد توقيع رسمي |
| LLM يقتبس من تفسير بدون نسبة | كسر للأمانة | كل أداة تُرجع attribution إلزامياً |
| LLM يقتبس جزءاً ويستكمل من ذاكرته | هلوسة جزئية | الـ system prompt يحذر، لكن لا ضمان 100% |
| نسبة خاطئة لمؤلف أو عام وفاة | إخلال علمي | TAFSIR_ATTRIBUTIONS ثوابت إلزامية |

### ١٦.٤ مخاطر تشغيلية ومالية

| الخطر | التأثير | المخفّف |
|---|---|---|
| ضياع توكن HF أو PyPI | فقدان التحكم بالحساب | Trusted Publishing لإلغاء الحاجة للتوكن |
| الـ DB على HF يُحذف بالخطأ | كل المستخدمين الجدد يفشلون | نسخة محلية + scripts/upload_db.py |
| تغيير schema DB في إصدار قادم | كسر التوافقية | اختبارات completeness في CI + SemVer |
| 🆕 **abuse على endpoint علني** | فاتورة Fly.io ترتفع | Hard Spending Limit $25 + rate limiting قادم |
| 🆕 **انقطاع `mcp.tafsir.net` لو GoDaddy تعطّل** | المستخدمون يفشلون | `tafsir-mcp.fly.dev` كfallback خفي يعمل |
| 🆕 **شهادة Let's Encrypt تنتهي ولم تتجدد** | الـHTTPS يفشل | تجديد تلقائي قبل 30 يوم؛ `fly certs check mcp.tafsir.net` للمتابعة |
| 🆕 **المالك ينسى Spending Limit** | كارثة محتملة | الـAI القادم: ذكّر بشدّة في الجلسة الأولى |

---

## ١٧. Onboarding Prompt

```markdown
أنت مساعد متخصص في مشروع `tafsir-mcp` — خادم Model Context Protocol مفتوح المصدر،
منشور على PyPI و GitHub و Hugging Face، **والآن مُستضاف على Fly.io على نطاق
`mcp.tafsir.net`**. برعاية مركز تفسير للدراسات القرآنية (https://tafsir.net).

## معلومات سريعة

- **المطوّر:** Ahmed Eid · GitHub: ah-vb-cod · cloud@tafsir.net
- **المنظمة:** github.com/tafsircenter · huggingface.co/tafsircenter · pypi.org/user/tafsircenter
- **جهاز التطوير:** macOS Apple Silicon 26.4.1، VS Code
- **اللغة:** عربية أساساً، إنجليزية للمصطلحات

## ١. حالة المشروع

- ✅ v1.0.0 منشور على PyPI (`pip install tafsir-mcp`)
- ✅ DB على Hugging Face (`tafsircenter/tafsir-mcp-data`)، 214 MB، SHA256 موثَّق
- ✅ HTTP MCP server حيّ على `https://mcp.tafsir.net/mcp` (Fly.io، Mumbai/bom)
- ✅ `https://mcp.tafsir.net/health` يُرجع 200 + payload
- ✅ Fly auto-stop مفعّل، تكلفة ~$3-5/شهر
- ✅ DEPLOY.md موجود في `deploy/DEPLOY.md` على GitHub
- 🟡 HF Space قيد الإخفاء (سيُجعل Private)
- 🟡 Spending Limit قيد الضبط من المالك (Soft $5، Hard $25)
- ⬜ Rate limiting لم يُنفّذ بعد

## ٢. آخر نقطة وقفنا عندها

المالك حسم نموذج الخدمة: **علنيّ مع rate limiting (السيناريو ب)**، والتزم
بضبط Spending Limit فوراً. المهمة الفورية: التأكيد من المالك على ضبط
`https://fly.io/dashboard/personal/billing` بـSoft=$5 وHard=$25.

بعد التأكيد:
1. إخفاء HF Space (Private لا Delete)
2. تنفيذ rate limiting (~60 req/min/IP) — جلسة كود قادمة
3. GitHub Release v1.0.0 (pending من قبل)

## ٣. المكدّس

Python 3.12 + uv 0.11.7 + FastMCP v1.27.1 + SQLite/FTS5 + Pydantic v2
+ pyarabic + huggingface_hub. Transport: stdio محلياً، streamable-http
على Fly.io. اختبار: pytest 35/35 في 0.46s.

## ٤. البيانات (223 MB، SQLite)

- 114 سورة، 6,236 آية، 77,432 كلمة، 1,891 جذراً، 604 صفحة
- 5 تفاسير + المختصر بـ3 لغات
- 201 آية أسباب نزول بالإسناد
- SHA256: 10e61f615ab5e6a3440e8ecc8ba1dc2273d12cd9048752760fe53a44d191cc27

## ٥. النمط المعماري الإلزامي

1. **Programmatic Registration** (وليس decorators):
   - `tools/X.py`: عرّف دوال Python عادية
   - في نهاية الملف: `def register(mcp): mcp.tool(name="...")(fn)`
   - `server.py` يستدعي `X.register(mcp)` لكل ملف
2. **اسم MCP قد يختلف عن اسم Python:** Python `get_ayah` → MCP `fetch_ayah`
3. **Pydantic v2 Annotated:** `def fn(s: Annotated[int, Field(ge=1)] = 1): ...`
4. **DB read-only:** `mode=ro` URI + `PRAGMA query_only=ON`
5. **مفاتيح SQL مزدوجة:** `TAFSIR_KEYS=("sura","aya")` للتفاسير الـ5،
   `STANDARD_KEYS=("surahNo","ayahNo")` للباقي
6. **Parametrized SQL إلزامي:** `?` placeholders فقط
7. **🆕 `@mcp.custom_route` لـHTTP endpoints الإضافية** (لا Starlette wrapper)
8. **🆕 Branch policy:** فرع `feat/X` → `git merge --ff-only` إلى main

## ٦. القيود الصارمة (لا تُكسر)

1. لا توليد محتوى ديني. الأدوات تُرجع النصوص حرفياً.
2. نسبة كل تفسير لقائله (TAFSIR_ATTRIBUTIONS ثوابت).
3. حفظ الإسناد كاملاً في nuzool.
4. التحقق من 114 سورة و6,236 آية.
5. رسائل خطأ بالعربية الفصحى.
6. **🆕 Spending Limit إلزامي على Fly.io.**
7. **🆕 `mcp.tafsir.net` هو الرابط الرسمي.** `.fly.dev` احتياطي.
8. **🆕 Branch protection على `main`.** لا push مباشر.

## ٧. أسلوب التواصل

- **خطوة بخطوة:** أمر واحد، انتظر الرد، ثم التالي.
- **الإجراء أولاً، الشرح ثانياً.**
- **جداول + ✅/❌ + code blocks.**
- **macOS-specific commands.**
- **"اعرض الخطة أولاً ثم نفّذ"** قبل أي تعديل كبير.
- **يحبّ critique** — أحياناً يلصق رد expert ويسأل أن تقارن.
- **VS Code للتعديل** عند فشل Bracketed Paste في Terminal.

## ٨. محظورات

- ❌ كتابة توكنات في الكود أو command line (سبق وحدث تسريب)
- ❌ تخمين schema (استخدم `inspect_schema.py` أو SCHEMA_NOTES.md)
- ❌ افتراضات بدون تحقق
- ❌ urlretrieve على macOS (استخدم huggingface_hub)
- ❌ إرسال أوامر متعددة دفعة واحدة
- ❌ نسيان Spending Limit عند تشغيل خدمة عامة
- ❌ Starlette wrapper لإضافة HTTP routes إلى FastMCP (Issue #1467)

## ٩. مصادر الحقيقة الواحدة في المستودع

- `CLAUDE.md` — قواعد المشروع للـ AI
- `scripts/SCHEMA_NOTES.md` — مرجع أعمدة DB الفعلية
- `tafsir-mcp-context-pack.md` — v1 (تاريخي)
- `deploy/DEPLOY.md` — 🆕 دليل التشغيل السحابي
- `DATA_SOURCES.md` — جدول التفاسير الـ8

## ١٠. ما يجب أن تفعله الآن

1. اقرأ هذا السياق كاملاً.
2. ابدأ بسؤال المالك: "هل تمّ ضبط Fly.io Spending Limit؟" (نص حرفي).
3. عند طلب مهمة، اعرض **الخطة أولاً** (الملفات، النتيجة المتوقعة).
4. التزم بكل القيود الصارمة والنمط المعماري.
5. لا تخمّن. عند الشك، افحص (`PRAGMA`, `grep`, `git log`, `fly status`).
6. أمر واحد، انتظر، ثم التالي.

تم. أبلغني بما تريد العمل عليه.
```

---

## ١٨. ملاحق الجودة

### ١٨.١ قائمة الفراغات (Sections marked "غير محدد" أو ناقصة في المحادثة)

| القسم | البند | السبب |
|---|---|---|
| §3 | تأكيد إتمام ضبط Spending Limit | المالك ملتزم لكن الجلسة انتهت قبل التأكيد |
| §5.1 | إصدار Uvicorn المثبت في الإنتاج | لم يُذكر صراحة |
| §5.1 | إصدار ruff و mypy | غير محدد |
| §6 | إصدار pytest محدد | لم يُذكر صراحة (لكن pytest-asyncio 1.3.0 معروف) |
| §6 | محتوى `deploy/Dockerfile` بالتفصيل | غير مذكور في المحادثة، يحتاج فحص الـrepo |
| §6 | محتوى `deploy/README.md` كاملاً | المالك أدخله يدوياً في VS Code؛ مذكورة الـYAML frontmatter فقط |
| §8.5 | طول الدوال الأقصى | غير محدد رسمياً |
| §16.1 | الموعد المتوقع للمراجعة الشرعية الرسمية | "اعتبرها معتمدة" — لا توقيت |
| §16.1 | شعار المشروع و brand kit للمركز | غير محدد |
| §16.1 | استراتيجية الإعلان من المركز | يقرّره المركز |
| §16.1 | توقيت ترحيل Alibaba ECS | غير محدد، Phase 2 |
| §16.1 | تفاصيل rate limiting الفنية المحددة | الخيارات مطروحة لكن لم يُحسم middleware (starlette-rate-limit؟ Redis؟ in-memory؟) |
| §16.1 | اسم/معرّفات المبرمجين المتوقع تسليمهم | لم يُحدد المالك أسماء بعد |
| §6.12 | تواريخ انتهاء شهادة Let's Encrypt الحالية | لم تُذكر صراحة (Let's Encrypt = 90 يوم افتراضي) |
| §5.8 | السعر الفعلي حتى الآن على Fly.io | لم يطبع المالك `fly bills` |

### ١٨.٢ التناقضات المرصودة وكيف حُسمت

| التناقض | النسخة الأولى | النسخة النهائية (المعتمدة) | كيف حُسم |
|---|---|---|---|
| اسم المنظمة على GitHub | `tafsir-center` (مع شرطة) ظهر في `data_loader.py` | **`tafsircenter`** (بدون شرطة) | اكتشفه Claude Code أثناء إنشاء سكربتات الرفع |
| النشر على حساب شخصي vs منظمة | المالك في البداية: *"مؤقتاً سيتم النشر على حسابي"* | **منظمة `tafsircenter`** | المالك حصل على إذن المركز |
| ربط بـ Claude Desktop | الخطة الأولى تشمل ربطه | **Claude Code فقط** (+ HTTP لاحقاً) | اكتشاف أن Anthropic لا تدعم MCP في Chat |
| اسم Tafsir vs `tafsir-mcp` | المالك قال: *"اسم المشروع: Tafsir"* | اسم الحزمة `tafsir-mcp`، اسم Python `tafsir`، اسم FastMCP `"Tafsir MCP"` | اتساق: Tafsir = brand، `tafsir-mcp` = package |
| فحص `@mcp.tool` (نمط Decorator) | تشخيص متسرّع أن الأدوات غير مسجَّلة | بعد فحص `mcp.list_tools()`: 13 أداة مسجَّلة بنمط `register` | تم بفحص فعلي قبل التعديل |
| عدد الاختبارات في كل ملف | Context Pack v1 ذكر `test_tools.py` بـ 10 اختبارات | اختفى `test_tools.py`، المحتوى دُمج في `test_extended_tools.py` (15 اختباراً) | تأكدت من العدّ: 10 + 15 + 10 = 35 |
| 🆕 خيار `/health` endpoint | في البداية: نمط Starlette wrapper / Mount | بعد المراجعة: **`@mcp.custom_route` decorator** | اقتباس المالك: *"احتاجك مره اخيره تفحص وتقارن ردك بالرد التالي"* — المالك لصق رد expert آخر؛ الـassistant قرأ FastMCP source واعتمد decorator |
| 🆕 سلوك Fly health check | الـassistant افترض restart تلقائي | الصحيح: auto-routing فقط، restart عند crash فقط | تصحيح بعد مراجعة Fly docs + رد المالك |
| 🆕 grace_period الافتراضي | جرّب الـassistant بدايةً 5s | المعتمد **15s** | بعد ملاحظة Uvicorn startup ~7s |
| 🆕 موضع `/health` في `fly.toml` | محاولة أولى داخل `[[services]]` block جديد | **`[[http_service.checks]]`** ضمن `[http_service]` القائم | لتجنّب إعادة هيكلة `fly.toml` كلها |
| 🆕 نموذج الخدمة | كانت 3 سيناريوهات (أ مغلق، ب علني مع حدود، ج علني بلا حدود) | **ب** | اختيار المالك حرفياً |
| 🆕 طريقة تسليم المبرمجين | سؤال المالك: *"اسلمهم الملف على جهازي ام اضفهم في github"* | **GitHub Collaborators + Write + Branch Protection** | بعد شرح الـassistant للـoptions |

### ١٨.٣ ملاحظات إضافية لفريق التطوير

1. **Context Pack v1 وv2** ما زالا في المستودع/المشروع. هذا **v3** يحلّ محلهما ويعكس حالة الإنتاج بعد ترحيل Fly.io.

2. **`Contributors` على GitHub** يظهر `claude` و `ah-vb-cod` — الـ commits بـ `Co-Authored-By: Claude` (شفاف، أمانة).

3. الـ CI (`.github/workflows/test.yml`) نجح في 17 ثانية رغم عدم وجود `quran.db` في الـrunner — يحتاج فحص: هل يحمّل من HF أم يتخطى اختبارات تحتاجها؟ (لم يُحسم).

4. **ملف `main.py`** موجود في الجذر، موروث من `uv init`. غير مستخدم، يمكن حذفه.

5. **مجلد `deploy/`** هو المنطقة المخصصة لكل ما يخص النشر السحابي. أي إضافة لـAlibaba ECS مستقبلاً يجب أن تكون داخل `deploy/`.

6. **HF Space `tafsircenter-tafsir-mcp.hf.space`** ما زال علنياً وقت كتابة هذا الـPack. أول إجراء بعد ضبط Spending Limit: إخفاؤه كـPrivate.

7. **DEPLOY.md في `deploy/DEPLOY.md`** هو المرجع التشغيلي الأساسي للمبرمجين الجدد. يتضمن:
   - مخطط معماري للإنتاج
   - جدول المكوّنات الخارجية
   - سير عمل التحديث (6 خطوات)
   - rollback procedure
   - إدارة DNS و SSL
   - troubleshooting
   - فهرس الملفات
   - URLs مرجعية
   - قسم emergency contacts

8. **آخر 3 commits على `main`:**
   ```
   c0fe57b  docs: update README URL and add DEPLOY.md
   1c9ac63  feat: add /health endpoint and Fly health check
   3121666  chore: add Fly.io configuration (fly.toml + .dockerignore)
   ```

9. **commit `81e42d9` على HF Space فقط** (transport_security fix) — مادته الفعلية الآن داخل `deploy/server_http.py`، لكن الـcommit التاريخي لا يوجد على GitHub. هذا سبب إبقاء HF Space كـPrivate وليس Delete.

10. **سؤال المالك economic** الذي ختم الجلسة قبل توليد هذا الـPack: *"هل حاليا يستطيع مبرمج استخدام رابط mcp.tafsir.net/mcp في بناء تطبيق ويستغله وانا اللي ادفع اشتراك fly.io"* — هذا السؤال **نموذجي لما يجب أن يبادر به الـAI** عند نشر أي خدمة عامة (السؤال عن economics، abuse model، spending limits).

11. **التزام علني للجمهور:** الـrate limiting المعلَن **~60 req/min/IP** هو رقم اقترحه الـassistant ولم يحسمه المالك صراحة. يحتاج إعادة مناقشة في الجلسة القادمة قبل التنفيذ.

---

> 🌙 **خاتمة:** من ملف `.db` غامض في 14 مايو، إلى حزمة منشورة على PyPI في 13 مايو، إلى خدمة HTTP عامة على `mcp.tafsir.net` في 15 مايو — رحلة ~24 ساعة من العمل المركّز. المشروع الآن:
>
> 1. **في يد العالم** عبر `pip install tafsir-mcp`
> 2. **في يد المستخدم العامّ** عبر `https://mcp.tafsir.net/mcp`
> 3. **في يد المبرمجين** قريباً عبر GitHub Collaborators
>
> يحفظ أمانة النص القرآني، ويضع معياراً لكيفية تقديم المحتوى الديني للمساعدات الذكية: **بالنسبة، بالأمانة، وبالاعتماد**.
>
> *"وَأَنْ تَعْفُوا أَقْرَبُ لِلتَّقْوَى ۚ وَلَا تَنْسَوُا الْفَضْلَ بَيْنَكُمْ"*
