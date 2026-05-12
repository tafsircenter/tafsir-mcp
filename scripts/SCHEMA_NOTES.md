# SCHEMA_NOTES — خريطة قاعدة البيانات النهائية
> مُنشأ بواسطة scripts/inspect_schema.py — مرجع إلزامي قبل بناء أي أداة

---

## 1. جدول Mapping النهائي: المفهوم → الجدول → العمود

| المفهوم | الجدول | المفاتيح | العمود/الملاحظة |
|---|---|---|---|
| نص الآية (الرسم) | `word_content_rasm` | `surahNo`, `ayahNo`, `wordNo` | `word` — يُجمَّع بترتيب `wordNo` |
| ملاحظات الرسم العثماني | `word_content_rasm` | نفسه | `rasm` — نثر وصفي، قد يكون `-` |
| تجويد الآية | `ayah_content_tajweed` | `surahNo`, `ayahNo` | `tajweed` |
| إعراب الآية (كاملاً) | `ayah_content_irab` | `surahNo`, `ayahNo` | **`irabAyah1`** ⚠️ (ليس `irab`) |
| تفسير الطبري | `tafsir_tabary` | **`sura`**, **`aya`** | `tafsir` — يحوي `id` إضافي |
| تفسير ابن كثير | `tafsir_katheer` | **`sura`**, **`aya`** | `tafsir` |
| تفسير البغوي | `tafsir_baghawy` | **`sura`**, **`aya`** | `tafsir` |
| تفسير السعدي | `tafsir_saadi` | **`sura`**, **`aya`** | `tafsir` — لا NULL (6236 صف كامل) |
| التفسير الميسر | `tafsir_moyassar` | **`sura`**, **`aya`** | `tafsir` |
| مختصر التفسير (عربي) | `QuranTafseer` | `surahNo`, `ayahNo` | `Mukhtasarar` |
| مختصر التفسير (إنجليزي) | `QuranTafseer` | `surahNo`, `ayahNo` | `Mukhtasaren` — لا NULL (6236 كامل) |
| مختصر التفسير (بنغالي) | `QuranTafseer` | `surahNo`, `ayahNo` | `Mukhtasarbn` — لا NULL (6236 كامل) |
| سبب النزول | `ayah_content_nozool` | `surahNo`, `ayahNo` | `nozoolInfo` — نص واحد يحوي السند والمتن معاً |
| معنى الكلمة | `word_content_meaning` | `surahNo`, `ayahNo`, `wordNo` | `meaning` |
| إعراب الكلمة | `word_content_irab` | `surahNo`, `ayahNo`, `wordNo` | **`irabMushakkal`** ⚠️ (ليس `irab`) |
| صرف الكلمة | `word_content_sarf` | `surahNo`, `ayahNo`, `wordNo` | `sarf` |
| جذر الكلمة | `word_statistics` | `surahNo`, `ayahNo`, `wordNo` | `root` |
| تكرار الكلمة في القرآن | `word_statistics` | نفسه | `repeatitionCount` ⚠️ (مهجأة خطأ في DB) |
| تكرار الجذر | `word_statistics` | نفسه | `rootRepeatitionCount` |
| قراءات الكلمة | `qeraat_info` | `surahNo`, `ayahNo`, `wordNo` | `content` + `note` (انظر تنسيق خاص ↓) |
| فوائد المختصر | `mokhtasar_fawaed` | `page` | `content` — **صفوف متعددة لكل صفحة** ⚠️ |
| اسم السورة | `surah_stats` | `surahNo` | `surahName` (مثال: "الفاتحة") |
| تفاصيل أسماء السورة | `surah_content` | `surahNo` | `surahNameInfo` — نص طويل متعدد الأسماء |
| نوع النزول (مكي/مدني) | `surah_stats` | `surahNo` | `makkiMadani` |
| ترتيب النزول | `surah_stats` | `surahNo` | `revelationSeq` |
| عدد آيات السورة | `surah_stats` | `surahNo` | `ayahCount` |
| فضائل السورة | `surah_content` | `surahNo` | `surahFadael` |
| أهداف السورة | `surah_content` | `surahNo` | `surahGoals` |
| معلومات نزول السورة | `surah_content` | `surahNo` | `surahNujoolInfo` |

---

## 2. تحذيرات وملاحظات إلزامية لبناء الأدوات

### ⚠️ اختلاف أسماء المفاتيح بين الجداول

| الجداول | عمود السورة | عمود الآية |
|---|---|---|
| `tafsir_tabary/katheer/baghawy/saadi/moyassar` | `sura` | `aya` |
| `ayah_content_*`, `word_content_*`, `word_statistics`, `qeraat_info`, `surah_*`, `QuranTafseer` | `surahNo` | `ayahNo` |

**خطر الخلط بين `sura`/`surahNo` و`aya`/`ayahNo` — تحقق في كل استعلام.**

### ⚠️ أعمدة تختلف عن الاسم المتوقع

| الجدول | الاسم المتوقع | الاسم الفعلي |
|---|---|---|
| `ayah_content_irab` | `irab` | **`irabAyah1`** |
| `word_content_irab` | `irab` | **`irabMushakkal`** |
| `word_statistics` | `repetitionCount` | **`repeatitionCount`** (typo في DB) |
| `word_statistics` | `frequency` | **`repeatitionCount`** (المعنى نفسه) |

### ⚠️ mokhtasar_fawaed — صفوف متعددة لكل صفحة

- الجدول يحوي **2212 صفاً** موزعة على **604 صفحة** = متوسط 3.7 فائدة/صفحة
- للحصول على فوائد صفحة كاملة، استخدم `GROUP_CONCAT` أو أرجع list:
  ```sql
  SELECT content FROM mokhtasar_fawaed WHERE page = ? ORDER BY rowid
  ```
  لا تستخدم `SELECT *` مع افتراض صف واحد.

### ⚠️ qeraat_info — تنسيق خاص في عمود content

- **تنسيق `@قارئ/نص@`** يُمثّل كل رواية:
  ```
  @يعقوب وعاصم والكسائي وخلف العاشر/قرأ (مَالِكِ) بإثبات الألف...@باقي الرواة/قرؤوا (مَلِكِ)...@
  ```
- عمود `note` يحوي الشرح المقارن للقراءتين (قد يكون NULL)
- هناك **صفوف متعددة لكل آية** (بعدد الكلمات التي بها خلاف)
- كلمة بلا خلاف تحوي: `"لا خلاف بين القراء في هذا الموضع"`

### ⚠️ ayah_content_nozool — نص موحّد لا عمودان

- عمود **واحد فقط** `nozoolInfo` يحوي السند والمتن معاً في نص طويل
- **لا تُفرّق بين السند والمتن برمجياً** — أرجع النص كاملاً كما هو
- يبدأ النص عادة بـ `"قوله تعالى: {...}"` ثم الروايات بالإسناد
- **201 آية فقط** لها سبب نزول — الفاتحة كاملها `COUNT=0`

### ✅ بيانات كاملة بلا ثغرات

| الجدول | الحالة |
|---|---|
| `tafsir_saadi.tafsir` | 0 NULL — 6236 صف كامل |
| `QuranTafseer.Mukhtasaren` | 0 NULL — 6236 صف كامل |
| `QuranTafseer.Mukhtasarbn` | 0 NULL — 6236 صف كامل |
| `word_content_rasm` | كاملة لكل الآيات بما فيها الحروف المقطعة (3:1→"الم"، 36:1→"يس") |

### ℹ️ surahNameInfo — نص طويل لا قائمة منظمة

- لا توجد أعمدة منفصلة `name1`, `name2` — كل الأسماء في `surahNameInfo`
- النص يبدأ بـ `"سورة X\n\nأسماؤها التوقيفية:\nX، وY، وZ"`
- استخدم `surah_stats.surahName` كاسم موجز رئيسي
- أرجع `surahNameInfo` كاملاً لمن يحتاج قائمة الأسماء

---

## 3. مفاجآت وشذوذ

1. **`tafsir_tabary` له عمود `id` إضافي** — الجداول الأخرى ليس لها. لا يؤثر على الاستعلام بـ `sura/aya`.

2. **آية الكرسي (2:255) تحوي 50 كلمة** — أطول آية فردية في الفاتحة (7 كلمات فقط). المنطق يتعامل معهما بنفس الطريقة.

3. **الحروف المقطعة كلمة واحدة** — `الم` (3:1) و`يس` (36:1) مُخزَّنة كـ `wordNo=1` وحيد. `reconstruct_ayah` يُرجعها صحيحة.

4. **`word_statistics.root`** يحوي الجذر بصيغة مُطابقة للكلمة (مثال: `سمي`، `أله`، `رحم`) — ليس دائماً بالشكل الاشتقاقي القاموسي.

5. **`word_content_rasm.rasm`** قد يكون `-` (شرطة) عندما لا توجد ملاحظة رسم — تحقق قبل الإرجاع.

6. **قيمة `sujud` في `surah_stats`** هي نص (`"لا"` / اسم موضع السجدة) وليست boolean.

7. **جدول `mokhtasar_fawaed` مفهرس بـ `page` وليس بـ `surahNo/ayahNo`** — ليس له مفتاح آية مباشر. لاستخدامه بالآية يجب جدول وسيط (غير موجود) أو البحث النصي.

---

## 4. SQL آمن جاهز للنسخ

```sql
-- نص آية كاملة
SELECT word, wordNo FROM word_content_rasm
WHERE surahNo = ? AND ayahNo = ? ORDER BY wordNo;

-- تجويد
SELECT tajweed FROM ayah_content_tajweed WHERE surahNo = ? AND ayahNo = ?;

-- إعراب الآية
SELECT irabAyah1 FROM ayah_content_irab WHERE surahNo = ? AND ayahNo = ?;

-- تفاسير الخمسة (استبدل اسم الجدول فقط)
SELECT tafsir FROM tafsir_saadi WHERE sura = ? AND aya = ?;

-- مختصر (عربي/إنجليزي/بنغالي)
SELECT Mukhtasarar, Mukhtasaren, Mukhtasarbn FROM QuranTafseer
WHERE surahNo = ? AND ayahNo = ?;

-- سبب النزول
SELECT nozoolInfo FROM ayah_content_nozool WHERE surahNo = ? AND ayahNo = ?;

-- تحليل كلمة (ترتيب: رسم، معنى، إعراب، صرف، إحصاء)
SELECT r.word, r.rasm, m.meaning, i.irabMushakkal, s.sarf,
       ws.root, ws.repeatitionCount, ws.rootRepeatitionCount
FROM word_content_rasm r
LEFT JOIN word_content_meaning  m  ON m.surahNo=r.surahNo AND m.ayahNo=r.ayahNo AND m.wordNo=r.wordNo
LEFT JOIN word_content_irab     i  ON i.surahNo=r.surahNo AND i.ayahNo=r.ayahNo AND i.wordNo=r.wordNo
LEFT JOIN word_content_sarf     s  ON s.surahNo=r.surahNo AND s.ayahNo=r.ayahNo AND s.wordNo=r.wordNo
LEFT JOIN word_statistics       ws ON ws.surahNo=r.surahNo AND ws.ayahNo=r.ayahNo AND ws.wordNo=r.wordNo
WHERE r.surahNo = ? AND r.ayahNo = ? ORDER BY r.wordNo;

-- قراءات كلمة
SELECT wordNo, content, note FROM qeraat_info
WHERE surahNo = ? AND ayahNo = ? ORDER BY wordNo;

-- فوائد صفحة (صفوف متعددة!)
SELECT content FROM mokhtasar_fawaed WHERE page = ? ORDER BY rowid;

-- معلومات السورة
SELECT s.surahName, s.makkiMadani, s.revelationSeq, s.ayahCount,
       s.wordCount, s.charCount, s.beginType, s.longestWord,
       s.mostFreqWord, s.mostFreqChar, s.sujud,
       c.surahNameInfo, c.surahFadael, c.surahGoals, c.surahNujoolInfo
FROM surah_stats s
JOIN surah_content c ON c.surahNo = s.surahNo
WHERE s.surahNo = ?;
```
