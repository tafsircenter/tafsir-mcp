# جلسة 2026-06-02 — Repo Context Refactor

> تحويل بنية وثائق المشروع من «context-pack ضخم يتقادم» إلى معمارية متعدّدة الملفات
> بتردّدات تحديث مختلفة (STATE.md حيّ · sessions/ append-only · docs/ أرشيف+ADR · .claude سياق Claude Code).
> توثيق بحت — لا مساس بـ `src/`/`tests/`/`deploy/`/`pyproject.toml`، لا نشر.

---

## ١. السياق
`tafsir-mcp-context-pack-v3.md` (لقطة 15 مايو) صار بعمر ~18 يومًا ويتقادم. القرار: تقسيم السياق إلى ملفات
بتردّدات تحديث مختلفة. تُنفَّذ **قبل Deploy 1** (include_tajweed)، وخطة Deploy 1 محفوظة كـWIP داخل `STATE.md`
كي لا تُنسى. دورة هذه المهمة: 5 (plan) → 6 (implement) → 7 (test: pytest فقط) → 8 (review/PR/merge) → 9 → 10 (هذا السجلّ).
**لا 11 (deploy) ولا 12 (monitor)** لأنها لا تمسّ الإنتاج.

## ٢. القرارات المتخذة
| السؤال | القرار |
|---|---|
| بنية السياق | جدول النقل: STATE.md (حيّ) · sessions/ (append-only) · docs/ (أرشيف+ADR) · .claude/ (rules+skills) |
| السجلّات القديمة | **تُجمَّد كما هي** (append-only، تعكس حالة تاريخها) — لا تُعدَّل متونها إطلاقًا |
| روابط 05-16/05-17 القديمة | تُحلّ عبر «جدول النقل» في هذا السجلّ فقط، لا بتعديل المتون |
| `SCHEMA_NOTES.md` / `DATA_SOURCES.md` | **مؤجَّلان** لميزة المحتوى لاحقًا — خارج نطاق هذا الـRefactor |
| HF في STATE.md | pointer واحد لـ ADR-0001 فقط، دون تأطيرها كـ«حالة/منصّة» |
| `git add` | موجَّه بالاسم فقط (لا `-A`) — `.env` ليس بعد في `.gitignore` |

## ٣. التغييرات في الكود
لا شيء. `src/`، `tests/`، `deploy/`، `pyproject.toml` لم تُلمَس. التغييرات كلها `.md` + ملفات `.claude/`،
ما عدا سطر pointer واحد في `CLAUDE.md` وفقرة Deployment في `README.md`.

## ٤. الأطوار 6 + 7 — الـ5 commits
| # | hash | المحتوى |
|---|---|---|
| 1 | `8b7723f` | `docs: add STATE.md live-state file + CLAUDE.md pointer` — STATE.md (لقطة الإنتاج · إصدارات المنصّات · WIP لـDeploy 1 · المؤجَّلات · الدريفتان المصحَّحان) + سطر pointer في CLAUDE.md |
| 2 | `6e3a98f` | `docs: move context into sessions/ and docs/ archives` — النقل (انظر جدول النقل §6) + رأسا ARCHIVED (v3 يحمل تحذير §7.2/§7.4) |
| 3 | `4295dc4` | `docs: add ADR 0001-0003 + MAP stub` — قرارات Fly>HF · read-only DB · display v1.2 + docs/MAP.md (stub للطور 4) |
| 4 | `d6d72de` | `chore(claude): add path-scoped rules and skills` — rules/{tools,deploy,instructions}.md + skills/{stabilize,deploy-fly,verify-production}.md |
| 5 | `1884324` | `docs: note Fly.io production + HF legacy in README` — قسم الاستضافة (mcp.tafsir.net + HF legacy→ADR-0001) |

## ٥. الاختبارات (الطور 7)
- `pytest tests/ -q` بعد النقل: **35/35** (لا مساس بالكود).
- إعادة تشغيل بعد إنشاء هذا السجلّ (الطور 10): انظر §9.

### معايير النجاح الخمسة
1. ✅ pytest 35/35 بعد النقل.
2. ✅ الشجرة تطابق المخطَّط (17 ملفًا)؛ ملفات الجذر القديمة اختفت.
3. ✅ لا روابط مكسورة في الوثائق النشطة (CLAUDE/README/ADR/MAP/.claude).
4. ✅ رأسا ARCHIVED على v1 و v3.
5. ✅ تاريخ git محفوظ لـ v1 (`R099` + `git log --follow` يرجع إلى `8b2d68d`/`3e5325d`).

## ٦. جدول النقل (المسار القديم → الجديد)
> مستخرَج بالدليل من `git show --name-status 6e3a98f` و`git log --follow`، لا من الذاكرة.

| المسار القديم | المسار الجديد | دليل git |
|---|---|---|
| `tafsir-mcp-context-pack.md` (v1) | `docs/context-pack-v1.md` | **`R099`** (rename متعقّب، التاريخ محفوظ عبر `--follow` → `8b2d68d`, `3e5325d`) |
| `tafsir-mcp-context-pack-v3.md` | `docs/context-pack-v3.md` | `A` (كان غير متعقّب؛ git يسجّل الوجهة فقط) |
| `SESSION_2026-05-16_display-protocol.md` | `sessions/2026-05-16_display-protocol.md` | `A` (كان غير متعقّب؛ git يسجّل الوجهة فقط) |
| `SESSION_2026-05-17_user-friendly-v1_2.md` | `sessions/2026-05-17_user-friendly-v1.2.md` | `A` (غير متعقّب؛ + توحيد الفاصل `v1_2`→`v1.2`) |

ملاحظة: الثلاثة الأخيرة كانت untracked قبل هذا الـRefactor، فيسجّلها git كـ`A` (إضافة) لا `R` (rename)؛
مصدرها مؤكَّد بأن تلك الأسماء **لم تعد موجودة في الجذر** ضمن commit `6e3a98f` نفسه. فقط v1 كان متعقّبًا فظهر كـrename.

> **هذا الجدول يحلّ الرابطين القديمين** الواردين في متن السجلّين المجمَّدين دون تعديلهما:
> - `sessions/2026-05-16_display-protocol.md` يشير في مراجعه إلى `tafsir-mcp-context-pack-v3.md` ⟵ الآن `docs/context-pack-v3.md`.
> - `sessions/2026-05-17_user-friendly-v1.2.md` يشير في مراجعه إلى `SESSION_2026-05-16_display-protocol.md` ⟵ الآن `sessions/2026-05-16_display-protocol.md`.

## ٧. ملاحظة على مرجع Refs المعلّق
الـ5 commits (8b7723f/6e3a98f/4295dc4/d6d72de/1884324) تحمل `Refs: sessions/2026-06-02_repo-context-refactor.md`.
**إنشاء هذا الملف (commit الطور 10) يحلّ ذلك المرجع المعلّق.**

## ٨. الحالة المعلّقة
- ⏸️ **الطور 8 (review):** `push` → PR → `merge --ff-only` إلى `origin/main` — **ينتظر مراجعة بشرية + ACK**.
- لم يُنفَّذ أي `push`/`PR`/`merge`/`flyctl` في هذه الجلسة.
- بعد دمج هذا الـRefactor: تُستأنف **Deploy 1 (include_tajweed)** من بوابة Phase 6 (الخطة في `STATE.md` §WIP).

## ٩. أوامر مرجعية
```bash
# دليل النقل
git show --name-status 6e3a98f
git log --oneline --follow -- docs/context-pack-v1.md
# اختبار
TAFSIR_DB_PATH=data/quran.db uv run pytest tests/ -q   # 35/35
# الفرع (لا دمج بعد)
git log --oneline main..HEAD
```

## ١٠. مراجع
- الفرع: `docs/repo-context-refactor`
- Commits: `8b7723f` · `6e3a98f` · `4295dc4` · `d6d72de` · `1884324` (+ commit الطور 10 لهذا السجلّ)
- وثائق ذات صلة: `STATE.md` (الحالة الحيّة) · `docs/ADR/0001..0003` · `docs/MAP.md` (stub)
- الجلسة السابقة: `sessions/2026-05-17_user-friendly-v1.2.md`
