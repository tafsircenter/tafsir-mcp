# Skill — Verify Production (smoke بعد النشر)

read-only على الإنتاج: `initialize` + `*/list` فقط. **ممنوع `tools/call`** على الإنتاج.

```bash
# 1. الصحة
curl -s -o /dev/null -w "%{http_code}\n" https://mcp.tafsir.net/health   # 200

# 2. حالة Fly (ميّز auto-stop/start عن النشر — أكّد عبر releases)
flyctl status --app tafsir-mcp
flyctl releases --app tafsir-mcp        # آخر release الفعلي + تاريخه

# 3. handshake: protocolVersion + طول الميثاق + توقيع v1.2
curl -s -D /tmp/h.txt -X POST https://mcp.tafsir.net/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"verify","version":"1.0"}}}' \
  -o /tmp/b.txt
python3 - <<'PY'
import json
raw=open('/tmp/b.txt',encoding='utf-8').read()
d=''.join(l[5:].lstrip() for l in raw.splitlines() if l.startswith('data:')) or raw
r=json.loads(d)['result']; i=r['instructions']
print('proto', r['protocolVersion'], '| chars', len(i),
      '| v1.2', 'كيف تفضّل عرضه' in i)
PY

# 4. tools/list بنفس الجلسة (Mcp-Session-Id من ترويسة الخطوة 3) → 13 أداة

# 5. logs (لا 429/ERROR/Traceback)
flyctl logs --app tafsir-mcp --no-tail | grep -E "429|ERROR|Traceback" | tail
```
معيار النجاح: health 200 · release هو المتوقّع · proto 2024-11-05 · charter v1.2 (4384) · 13 أداة · لا أخطاء.
