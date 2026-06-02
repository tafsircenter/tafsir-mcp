# STATE.md — Tafsir MCP Live State

> آخر تحديث: 2026-06-02 (بعد Repo Context Refactor، قبل Deploy 1)
> يُحدَّث في الطور 10 من كل نشر/إصدار. التفاصيل التاريخية في `sessions/` و `docs/ADR/`.
> اقرأ هذا الملف أولًا للحالة الحيّة، ثم `CLAUDE.md` للقواعد.

## Production الحيّ (Fly.io)
| البند | القيمة |
|---|---|
| Endpoint | https://mcp.tafsir.net/mcp |
| Health | https://mcp.tafsir.net/health (200) |
| Region | bom (Mumbai) |
| Image | `tafsir-mcp:deployment-01KRVQKWPN1FTVJH79EZMC8W7H` |
| Fly version | v4 |
| نُشر في | 2026-05-17 19:47 UTC (آخر release؛ لا v5) |
| Last good image (rollback) | v4 (نفس الجاري — لا نشر بعده) |
| Charter | v1.2 (4384 codepoint، توقيع «كيف تفضّل عرضه») |
| Tools / Resources / Prompts | 13 / 3 / 5 |
| Protocol | MCP 2024-11-05 |

## الإصدارات عبر المنصّات
| المنصة | الإصدار | الحالة |
|---|---|---|
| GitHub HEAD (main) | 6e85de0 | يطابق Fly v4 |
| PyPI | 1.0.0 | 🔴 متخلّف عن v1.1 و v1.2 |
| pyproject.toml | 1.0.0 | 🟡 لم يُرفع رقمه بعد |
| Charter (live) | v1.2 | ✅ |
| DB schema / quran.db | SHA256 `10e61f61…cc27` | مستقرّ · المحلي ≡ HF ≡ صورة الإنتاج |

## Current Work In Progress
- ⏸️ **Deploy 1 — include_tajweed fix** (الطور 5 plan معتمد، بانتظار ACK لـ Phase 6 implement بعد هذا الـRefactor)
  - **الملفات:**
    - `src/tafsir/prompts/study.py` — السطران 41 و 179 (`study_ayah` + `tajweed_lesson`)
    - `src/tafsir/server.py` — السطر 111 (`SERVER_INSTRUCTIONS` بند 7)
  - **التغيير:** استبدال `include_tajweed=True` بـ `include=["tajweed"]` (الصيغة الصحيحة لتوقيع الأداة `include: list[str]`)
  - **الاختبارات:** 38/38 = 35 أساس + 3 حُرّاس:
    - حارس بقاء v1.2: وجود «كيف تفضّل عرضه» في `SERVER_INSTRUCTIONS`
    - حارس غياب: `include_tajweed` غير موجود في `study_ayah`/`tajweed_lesson`/`SERVER_INSTRUCTIONS`
    - regression: `grep -rc include_tajweed src/` = 0
  - **النشر:** فرع نظيف → `--ff-only` → push → `flyctl deploy` → 24س مراقبة
  - **rollback:** `flyctl deploy --image tafsir-mcp:deployment-01KRVQKWPN1FTVJH79EZMC8W7H` (v4)
  - الخطة الكاملة محفوظة في chat history للجلسة الحالية؛ تُستأنف من بوابة Phase 6.

## البنود المؤجَّلة (بعد Deploy 1)
1. **Step 2 — Repo hygiene batch:** `.env` في `.gitignore` + bump `pyproject` 1.0.0→1.2.0.
2. **Step 3 — Deploy 2:** `surah.py:28` → `Annotated[int, Field(ge=1, le=114)]`.
3. **Step 4 — Release v1.2.0:** GitHub release + PyPI publish.
4. **Step 5 — Rate limiting:** طور 5 plan منفصل (middleware، 20/h مقابل 60/min، graceful degradation).
5. **مستقبلًا:** `display.py` للتجزئة القهرية · `structuredContent`/`outputSchema` للأدوات الإحصائية · ميزة محتوى (تفاسير/ترجمات جديدة).

## Drift مُصحَّح هذه الجلسة (data-layer audit)
- **القرطبي غائب من الإنتاج:** لا جدول `tafsir_qurtubi` في `quran.db` (5 تفاسير كلاسيكية فقط).
- **ترجمات المختصر = AR/EN/BN** (أعمدة `Mukhtasarar/en/bn` في `QuranTafseer`) — لا EN/FR/ID.

## آخر جلسة موثَّقة
`sessions/2026-06-02_repo-context-refactor.md` (هذه المهمة)

## ملاحظات تشغيلية
- الميزانية المتوقّعة ~$0.07/شهر · حماية: 2 machines max + auto-stop · Spending Limit يُضبط يدويًّا (UI أزاله Fly — تأكيد المالك مطلوب).
- HF Space (legacy): انظر `docs/ADR/0001-fly-over-hf-space.md`.
