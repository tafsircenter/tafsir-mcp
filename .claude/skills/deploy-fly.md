# Skill — Deploy to Fly.io (مكثَّف من deploy/DEPLOY.md)

النشر بيد المالك (Model A). الإنتاج على Fly فقط، عبر `mcp.tafsir.net`.

```bash
# 1. فرع نظيف
git switch main && git pull --ff-only origin main
git switch -c fix/<slug>
# 2. عدّل (VS Code عند فشل لصق العربية في Terminal)
# 3. اختبر محليًّا
uv run pytest tests/ -q                  # 35/35 (+ حُرّاس)
uv run python deploy/server_http.py &
curl -i http://localhost:7860/health     # 200
curl -i http://localhost:7860/mcp        # 406 (سلوك MCP صحيح)
kill %1
# 4. commit + merge (fast-forward only)
git add <مسار محدّد>                      # لا -A (تفادي تسريب .env)
git commit -m "fix: …"
git switch main && git merge fix/<slug> --ff-only && git push origin main
# 5. حدّث STATE.md بآخر image ناجح، ثم انشر
flyctl deploy --remote-only
# 6. تحقّق
flyctl status && flyctl checks list
curl -i https://mcp.tafsir.net/health
git branch -d fix/<slug>
```
Rollback: `flyctl deploy --image tafsir-mcp:<previous-deployment-id> --app tafsir-mcp`.
آخر image ناجح معروف محفوظ في `STATE.md`.
