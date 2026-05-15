# Tafsir MCP — دليل النشر والتحديث

> دليل تشغيلي لنشر تحديثات إلى الإنتاج على Fly.io.

---

## 🏗️ نظرة معماريّة
المستخدم (Claude.ai / ChatGPT)
↓
https://mcp.tafsir.net/mcp  (GoDaddy DNS → Fly.io)
↓
Fly.io Anycast Network
↓
Machine في bom (Mumbai) — shared-cpu-1x، 1GB RAM
↓
Docker container
↓
Uvicorn :7860 → FastMCP → SQLite (quran.db 214MB)
### المكوّنات الخارجيّة

| المكوّن | الدور |
|---|---|
| **GitHub** (`tafsircenter/tafsir-mcp`) | مصدر الكود |
| **HF Datasets** (`tafsircenter/tafsir-mcp-data`) | قاعدة البيانات `quran.db` |
| **Fly.io** (`tafsir-mcp`، personal org) | استضافة الـ runtime |
| **GoDaddy** | إدارة DNS لـ `tafsir.net` |
| **Let's Encrypt** | شهادات SSL (تتجدّد تلقائياً كل 60-90 يوم) |

### النسخة الاحتياطيّة

- **HF Space** (`tafsircenter-tafsir-mcp.hf.space`) — Private، يمكن إحياؤه لو احتجنا
- **PyPI** (`tafsir-mcp`) — نسخة STDIO للاستخدام المحلّي

---

## 🚀 كيف تنشر تحديثاً

### المتطلّبات

- `flyctl` مثبّت: `brew install flyctl`
- مسجَّل دخول Fly: `fly auth login`
- صلاحيات write على repo GitHub

### الخطوات

#### 1. إنشاء فرع جديد

```bash
cd ~/projects/quranic-scholar-mcp
git switch main
git pull --ff-only origin main
git switch -c feat/your-feature-name
```

#### 2. تعديل الكود

الملفّات الشائعة:
- `src/tafsir/server.py` — منطق الخادم، الأدوات، الموارد
- `src/tafsir/data_loader.py` — تحميل DB
- `deploy/server_http.py` — HTTP entry + `/health` endpoint
- `deploy/Dockerfile` — إعداد الصورة
- `fly.toml` — إعداد Fly

#### 3. اختبار محلّي

```bash
# تشغيل في الخلفية
uv run python deploy/server_http.py &

# اختبار /health
curl -i http://localhost:7860/health
# يجب 200 OK + {"status":"ok"}

# اختبار /mcp
curl -i http://localhost:7860/mcp
# يجب 406 (سلوك MCP الصحيح)

# إيقاف
kill %1
```

#### 4. Commit + Merge + Push

```bash
git add <ملفات تعديلك>
git commit -m "feat: وصف واضح"

git switch main
git merge feat/your-feature-name --ff-only
git push origin main
git branch -d feat/your-feature-name
```

#### 5. النشر إلى Fly.io

```bash
fly deploy
```

⏰ يستغرق 3-5 دقائق. **لا تقاطع** الأمر.

#### 6. التحقّق

```bash
fly status
fly checks list
curl -i https://mcp.tafsir.net/health
curl -i https://mcp.tafsir.net/mcp
```

---

## 🔄 Rollback

### عرض الإصدارات السابقة

```bash
fly releases
```

### الرجوع لإصدار سابق

```bash
fly releases rollback <version-number>
```

> ⚠️ لا rollback إذا الـ DB كانت migrated. في هذه الحالة، أصلح الكود + deploy جديد.

---

## 🌐 إدارة DNS و SSL

### إضافة domain فرعيّ جديد

```bash
fly certs add subdomain.tafsir.net
```

Fly يطبع DNS records المطلوبة. أضفها في **GoDaddy → DNS Management → tafsir.net → Records**:

| Type | Name | Value |
|---|---|---|
| A | `subdomain` | `66.241.124.207` |
| AAAA | `subdomain` | `2a09:8280:1::115:e7f0:0` |

### التحقّق

```bash
fly certs check subdomain.tafsir.net
fly certs list
```

Let's Encrypt يجدّد تلقائياً. لا تدخل يدوياً.

---

## 🆘 Troubleshooting

### `fly deploy` يعطي تحذير "not listening"

سلوك معتاد بسبب race timing بين Fly's proxy و Uvicorn startup. تحقّق بعد deploy:

```bash
fly checks list  # يجب passing
curl https://mcp.tafsir.net/health  # يجب 200
```

لو الاثنان أخضران، التحذير لا يهمّ.

### `503 Service Unavailable`

```bash
fly logs
```

ابحث عن exception أو OOM kill.

### Machines stopped

طبيعيّ. `auto_stop_machines = 'stop'` يوقف Machines بعد ~6 دقائق idle. تستيقظ في 3-10 ثوان عند أوّل طلب.

### Certificate expired

لا يحدث (Let's Encrypt يجدّد). لو حدث:

```bash
fly certs check mcp.tafsir.net
```

---

## 📋 ملفّات مفاتيح

| الملف | الدور |
|---|---|
| `fly.toml` | إعداد Fly (app, region, port, health check) |
| `deploy/Dockerfile` | بناء صورة Docker |
| `deploy/server_http.py` | HTTP entry point + `/health` endpoint |
| `deploy/README.md` | وثائق المستخدم |
| `deploy/DEPLOY.md` | هذا الملف |
| `src/tafsir/data_loader.py` | تحميل DB من HF Datasets |
| `pyproject.toml` | dependencies Python |

---

## 🔗 روابط مرجعيّة

- **إنتاج:** https://mcp.tafsir.net/mcp
- **Fly Dashboard:** https://fly.io/apps/tafsir-mcp
- **GitHub:** https://github.com/tafsircenter/tafsir-mcp
- **HF Datasets:** https://huggingface.co/datasets/tafsircenter/tafsir-mcp-data
- **PyPI:** https://pypi.org/project/tafsir-mcp/

---

## 📞 طوارئ

لو الإنتاج معطّل ولا تستطيع تشخيصه:

1. أرسل screenshot من `fly status` و `fly logs` للمبرمج
2. الـ rollback أسرع من التشخيص في الطوارئ — استعمله
3. HF Space (Private) يمكن إحياؤه كبديل مؤقت