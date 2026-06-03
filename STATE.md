# STATE.md — Tafsir MCP Live State

> آخر تحديث: 2026-06-03 (Deploy 1 منشور v5 — تحت مراقبة 24س)
> يُحدَّث في الطور 10 من كل نشر/إصدار. التفاصيل التاريخية في `sessions/` و `docs/ADR/`.
> اقرأ هذا الملف أولًا للحالة الحيّة، ثم `CLAUDE.md` للقواعد.

## Production الحيّ (Fly.io)
| البند | القيمة |
|---|---|
| Endpoint | https://mcp.tafsir.net/mcp |
| Health | https://mcp.tafsir.net/health (200) |
| Region | bom (Mumbai) |
| Image | `tafsir-mcp:deployment-01KT6SD1MAJHAQ4NZ13V4FRMY3` |
| Fly version | v5 (كان v4) |
| نُشر في | 2026-06-03 ~13:07 UTC (Deploy 1) |
| Last good image (rollback) | v4 — `tafsir-mcp:deployment-01KRVQKWPN1FTVJH79EZMC8W7H` |
| Charter | v1.2 (4383 codepoint، توقيع «كيف تفضّل عرضه»؛ include=["tajweed"] مُصحَّح) |
| Tools / Resources / Prompts | 13 / 3 / 5 |
| Protocol | متفاوَض عليه (السقف 2025-11-25، مرصود حيًّا 2026-06-03 عبر initialize)؛ الكود لا يفرض نسخة — SDK mcp 1.27.1 |

## الإصدارات عبر المنصّات
| المنصة | الإصدار | الحالة |
|---|---|---|
| GitHub HEAD (main) | 1a6fb74 | Deploy 1 (include_tajweed) هبط ونُشر v5 |
| PyPI | 1.0.0 | 🔴 متخلّف عن v1.1 و v1.2 |
| pyproject.toml | 1.0.0 | 🟡 لم يُرفع رقمه بعد |
| Charter (live) | v1.2 | ✅ |
| DB schema / quran.db | SHA256 `10e61f61…cc27` | مستقرّ · المحلي ≡ HF ≡ صورة الإنتاج |

## الطور 8 + حادث توكن HF (مُغلق 2026-06-03)
- **هبوط الـRefactor:** `main` = `4923f3a` (كان `6e85de0`) — 6 commits وثائقية هبطت عبر `--ff-only` (2026-06-03)، بلا merge commit.
- **حادث أمني مُغلق (2026-06-03):** GitHub Push Protection حجب توكن HF (صلاحية WRITE) كان مضمَّنًا في `docs/context-pack-v3.md` §11.6 (حكاية تسريب تاريخية). عولِج بإعادة كتابة الفرع (استبدال بالنمط، **بلا قيمة سرّ في أي أمر/ملف**): التوكن الكامل = 0 عبر كل commit (تحقّق C4/C5)، §11.6 ورأس ARCHIVED سليمان، pytest 35/35 → دُفع، CI أخضر، دُمج `--ff-only`، purge للبلوب القديم محلّيًّا، وحُذف الفرع.
- **التوكن مُدوَّر (منجَز):** القديم (WRITE) أُلغي، وأُنشئ بديل fine-grained مقصور على الـdataset ⇒ السرّ المسرَّب ميت.
- **قرار مُسجَّل:** قُصاصة ميتة (4 أحرف، غير مستغَلّة) في §11.6 تُركت عمدًا — توسيع نمط التنقية كان سيُصيب اسم دالّة تنزيل HF في `data_loader` خطأً.
- **الإنتاج لم يُمَسّ:** Fly v4 كما هو؛ دمج `main` لا يُطلق نشرًا (`test.yml` اختبار فقط · `publish.yml` عند release يدوي · نشر Fly يدوي بيد المالك).
- **ثانوي:** ترقية actions (`checkout`/`setup-uv` → Node-24) قبل 2026-06-16.

## Current Work In Progress
- 🚀 **Deploy 1 — include_tajweed fix: منشور (v5)، تحت مراقبة 24س** (commitان: `aa8dfad` إصلاح · `1a6fb74` توثيق)
  - **التغيير:** `include_tajweed=True/true` → `include=["tajweed"]` في `study.py` (×2) و`server.py` (بند 7).
  - **التحقّق الإنتاجي (2026-06-03 ~13:07 UTC):** `include_tajweed` غائب · `include=["tajweed"]` حاضر · الميثاق 4383 codepoint · توقيع v1.2 سليم · 13 أداة · `/health` 200 · checks passing.
  - **نافذة المراقبة:** بدأت ~2026-06-03 13:07 UTC، تنتهي ~2026-06-04 13:07 UTC. خطّ الأساس: لا أخطاء/429/Traceback.
  - **لا يُختم «منجَز» إلا بعد 24س نظيفة** (الطور 12)؛ بعدها يُنقل للأرشيف ويُحدَّث هذا القسم.
  - **rollback خلال المراقبة:** `flyctl deploy --image tafsir-mcp:deployment-01KRVQKWPN1FTVJH79EZMC8W7H` (v4).

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
`sessions/2026-06-03_deploy1-include-tajweed.md` (Deploy 1 — منشور v5، تحت مراقبة)
— السابقة: `sessions/2026-06-03_phase8-and-token-incident.md`

## ملاحظات تشغيلية
- الميزانية المتوقّعة ~$0.07/شهر · حماية: 2 machines max + auto-stop · Spending Limit يُضبط يدويًّا (UI أزاله Fly — تأكيد المالك مطلوب).
- HF Space (legacy): انظر `docs/ADR/0001-fly-over-hf-space.md`.
