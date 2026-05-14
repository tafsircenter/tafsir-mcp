---
title: Tafsir MCP Server
emoji: 📖
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
pinned: true
short_description: خادم MCP للوصول العلمي الموثّق إلى القرآن الكريم
tags:
  - mcp
  - quran
  - tafsir
  - claude
  - chatgpt
  - arabic
---

# Tafsir MCP Server

خادم **Model Context Protocol** للوصول العلمي الموثّق إلى القرآن الكريم — برعاية [مركز تفسير للدراسات القرآنية](https://tafsir.net).

يوفّر **13 أداة + 3 موارد + 5 قوالب دراسة** عبر Streamable HTTP — جاهز للربط المباشر بـClaude.ai و ChatGPT.

---

## 🔗 رابط الخادم

```
https://tafsircenter-tafsir-mcp.hf.space/mcp
```

---

## للاستخدام في Claude.ai

1. **Settings → Connectors → Add custom connector**
2. الاسم: `Tafsir`
3. URL: انسخ الرابط أعلاه
4. اضغط **Connect** (بدون OAuth — المحتوى علمي عام)

## للاستخدام في ChatGPT

يتطلب اشتراك Plus / Pro / Business / Enterprise / Edu:

1. **Settings → Apps → Advanced**
2. فعّل **Developer Mode**
3. **Create app** + ضع الرابط

---

## الأدوات المتوفّرة (13)

| الأداة | الوظيفة |
|---|---|
| `fetch_ayah` | نص آية بالرسم العثماني (تجويد/إعراب اختياري) |
| `fetch_tafsir` | تفاسير الطبري، ابن كثير، البغوي، السعدي، الميسر، المختصر |
| `fetch_nuzool_reason` | سبب نزول الآية إن ثبت |
| `fetch_surah_info` | معلومات السورة الكاملة |
| `analyze_word` | تحليل كلمة: معنى/إعراب/صرف/إحصاء/قراءات |
| `find_root_occurrences` | مواضع جذر في القرآن |
| `get_root_stats` | إحصاءات جذر |
| `get_qeraat_variants` | القراءات المختلفة |
| `search_quran_text` | بحث FTS5 في نصوص الآيات |
| `search_in_tafsir` | بحث في متن تفسير محدد |
| `get_quran_overview` | إحصاءات عامة |
| `get_page_fawaed` | فوائد صفحة المصحف |
| `get_surah_statistics` | إحصاءات مفصّلة لسورة |

## الموارد (3)

- `quran://surahs` — فهرس 114 سورة
- `quran://tafsirs` — فهرس 8 مصادر تفسيرية مع كامل بيانات الإسناد
- `quran://schema` — توثيق مخطط قاعدة البيانات (للمطوّرين)

## القوالب (5)

`study_ayah` · `compare_tafsirs` · `root_study` · `surah_overview` · `tajweed_lesson`

---

## للمطوّرين

نسخة STDIO محلية للاستخدام في Claude Code أو Cursor أو Gemini CLI:

```
pip install tafsir-mcp
```

| المصدر | الرابط |
|---|---|
| الكود | https://github.com/tafsircenter/tafsir-mcp |
| قاعدة البيانات | https://huggingface.co/datasets/tafsircenter/tafsir-mcp-data |
| PyPI | https://pypi.org/project/tafsir-mcp/ |

## الترخيص

MIT — الكود مفتوح. نصوص القرآن والتفاسير تُعاد حرفياً من قاعدة بيانات موثّقة، **كل تفسير منسوب لقائله** بإسناده الكامل.
