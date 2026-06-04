# جلسة 2026-06-03 — Deploy 1: تصحيح معامل التجويد في fetch_ayah

> إصلاح خطأ نقطيّ: القوالب والميثاق كانت تستدعي `fetch_ayah` بمعامل **غير موجود**
> (`include_tajweed=True/true`)، فيفشل مسار التجويد لأي عميل يتبعها.
> الصحيح هو توقيع الأداة `include: list[str]` ⇒ `include=["tajweed"]`.
> دورة TDD على فرع `fix/include-tajweed`. لم يُمَسّ منطق أي أداة ولا الـschema.

---

## ١. السياق
أوّل بنود stabilize (تقرير الـ9 محاور): القالبان `study_ayah`/`tajweed_lesson` وبند 7 من
`SERVER_INSTRUCTIONS` يضربون مثالًا بمعامل `include_tajweed` لا وجود له في توقيع `get_ayah`
(الموجود: `include: list[str]`، قيمه `'tajweed'`/`'irab'`). الاستدعاء كما هو موصوف يفشل ⇒
ميزة التجويد معطّلة عمليًّا عبر القوالب. اعتمد المالك Deploy 1 كأوّل إصلاح في دورة 5→12.

## ٢. القرارات المتخذة
| السؤال | القرار |
|---|---|
| الصيغة الصحيحة | `include=["tajweed"]` (مُحقَّقة من توقيع `ayah.py:66` واستهلاكها `ayah.py:83`، لا تخمين) |
| التحفّظ «(إن دعمتها الأداة)» في `study.py:179` | يُحذف — صار غير صحيح بعد التأكيد أن الأداة تدعمها |
| منطقة «لا تلمس» | تعديل `SERVER_INSTRUCTIONS` نقطيّ (مثال بند 7) ⇒ يستوجب ملاحظة في `docs/ADR/0003` (قاعدة `.claude/rules/instructions.md`) |
| نطاق التغيير | 3 مواضع فقط؛ لا منطق أداة، لا schema، لا أسماء MCP |

## ٣. التغييرات
| الملف | الموضع | قبل → بعد |
|---|---|---|
| `src/tafsir/server.py` | بند 7 (`SERVER_INSTRUCTIONS`) | `fetch_ayah(include_tajweed=true)` → `fetch_ayah(include=["tajweed"])` |
| `src/tafsir/prompts/study.py` | `study_ayah` خطوة 5 | `…, include_tajweed=True)` → `…, include=["tajweed"])` |
| `src/tafsir/prompts/study.py` | `tajweed_lesson` خطوة 1 | `include_tajweed=True\` (إن دعمتها الأداة)` → `include=["tajweed"]\`` |
| `docs/ADR/0003-display-protocol-v1.2.md` | إلحاق | ملاحظة تصحيح (تصحيح مثال لا سياسة؛ 4384→4383 cp) |
| `tests/test_resources_prompts.py` | استيراد + 3 حُرّاس | انظر §4 |

## ٤. الاختبارات (TDD)
ثلاثة حُرّاس جديدة في `test_resources_prompts.py`:
- `test_study_ayah_uses_correct_include_param` — `include=["tajweed"]` موجود · `include_tajweed` غائب
- `test_tajweed_lesson_uses_correct_include_param` — المثل
- `test_server_instructions_no_stale_include_param` — `include_tajweed` غائب من الميثاق · «كيف تفضّل عرضه» حاضر

| المرحلة | النتيجة |
|---|---|
| RED (قبل الإصلاح) | **3 failed**, 35 passed — الحُرّاس تُثبت الخلل |
| GREEN (بعد الإصلاح) | **38 passed** |

## ٥. التحقّق
- `grep -rn include_tajweed src/` → **فارغ** (regression).
- الميثاق: `charter_ok=True` · `4384 → 4383 codepoint` · `include_tajweed_present=False` — السياسة لم تتغيّر، توقيع v1.2 سليم.
- `ruff check src/` (نطاق CI) → نظيف. `mypy src/` → خطآن سابقان فقط (`pyarabic` بلا stubs).
- ℹ️ مصارحة: `ruff check tests/` يُظهر 3 مخالفات **سابقة وخارج نطاق CI** (استيراد `pytest` غير مستخدَم ×2، متغيّر `surahs` غير مستخدَم) — لم تُحدثها هذه الجلسة؛ تُؤجَّل لتنظيف منفصل.

## ٦. Git
- الفرع: `fix/include-tajweed` (من `d9a8d5e`).
- commit الإصلاح: `aa8dfad` — `fix: use include=["tajweed"] for fetch_ayah tajweed …` (4 ملفّات، +31/-3).
- `git add` موجَّه بالاسم (لا `-A`/`.`).

## ٧. الحالة المعلّقة (بوّابات منفصلة لاحقة)
- ⏸️ **الطور 8 (review/merge):** PR → CI → `merge --ff-only` إلى `main` — ينتظر ACK.
- ⏸️ **الطور 11 (deploy):** `flyctl deploy` → image v5 → تحقّق handshake (`include_tajweed` غائب من الإنتاج) → **24س مراقبة** — ينتظر ACK مستقلًّا.
- بعد الإنتاج: تحديث `STATE.md` (image v5، charter 4383).

## ٨. الأثر على المستخدم
بعد النشر: العملاء الذين يتبعون قالبَي الدراسة/التجويد أو بند 7 سيستدعون `fetch_ayah(include=["tajweed"])`
الصحيح بدل معامل يفشل ⇒ مسار التجويد يعمل. لا تغيير في سلوك العرض ولا في أي أداة أخرى.

## ٩. أوامر مرجعية
```bash
TAFSIR_DB_PATH=data/quran.db uv run pytest tests/ -q     # 38/38
grep -rn include_tajweed src/                            # فارغ
uv run python -c "from tafsir.server import SERVER_INSTRUCTIONS as s; print('كيف تفضّل عرضه' in s, len(s))"  # True 4383
```

## ١٠. مراجع
- commit: `aa8dfad` على `fix/include-tajweed`
- audit الأرض: تقرير Deploy 1 (A1–A5) في chat history
- وثائق ذات صلة: `docs/ADR/0003-display-protocol-v1.2.md` (ملاحظة التصحيح) · `STATE.md` §Current Work In Progress
- الجلسة السابقة: `sessions/2026-06-03_phase8-and-token-incident.md`

## ١١. تحقّق لاحق — نسخة البروتوكول
2026-06-03: تحقّق read-only من نسخة البروتوكول. initialize حيّ بـ protocolVersion=2025-11-25
→ الخادم أعاده كما هو ⇒ سقف الإنتاج 2025-11-25 (SDK mcp 1.27.1؛ supported
[2024-11-05·2025-03-26·2025-06-18·2025-11-25]). الكود لا يفرض نسخة.
«2024-11-05» السابق في STATE كان صدى عميلٍ قديم — صُحِّح.

## ١٢. تقوية حوكمة — .gitignore
2026-06-03: أُضيف .env إلى .gitignore (تقوية وقائية ضدّ التزام الأسرار) — repo-only، لا إنتاج، لا deploy.

## ١٣. توثيق — PRD
2026-06-04: أُضيف docs/PRD.md — وثيقة متطلبات مفصّلة مبنيّة من أدلّة المستودع (doc-only).
رُصد خلاله تعارض DB_SIZE_MB=214 مع الحجم الفعليّ ~223.5MiB → backlog (إصلاح كود منفصل،
مرشَّح للضمّ إلى Step 2).
