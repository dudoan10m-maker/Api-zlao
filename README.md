# Ghost Message API — Render starter

This is a deployable Flask API starter. **It does not send messages yet**: sending to Messenger/Zalo groups requires a supported official API, authorized account/app, and correct permissions. The endpoint deliberately returns HTTP 501 instead of falsely claiming delivery.

## Deploy from Android
1. Download and extract this ZIP.
2. Open https://github.com/ and create a new repository (for example `ghost-message-api`).
3. Upload `app.py`, `requirements.txt`, `render.yaml`, and `README.md` to the repository root.
4. Open https://dashboard.render.com/ → **New** → **Blueprint** (or create a **Web Service** connected to the repo).
5. If using Web Service manually: Runtime **Python**; Build Command `pip install -r requirements.txt`; Start Command `gunicorn app:app`; Health Check Path `/health`.
6. In Render → service → **Environment**, set `API_SECRET` to a long random secret. Set `ALLOWED_ORIGINS` to your frontend website origin; use `*` only for initial testing.
7. Deploy. Render gives a URL such as `https://your-service.onrender.com`.
8. Test by opening `https://your-service.onrender.com/health`. It should show `{"ok":true,"status":"healthy"}`.

## Endpoint
`POST https://your-service.onrender.com/api/send`

Headers:
- `Content-Type: application/json`
- `X-API-Key: YOUR_API_SECRET`

JSON body:
```json
{
  "platform": "zalo",
  "target": "AUTHORIZED_GROUP_ID",
  "message": "Hello"
}
```

Expected for now: HTTP 501 explaining that provider integration is not configured. This is intentional; deployment alone does not grant permission to send into arbitrary Messenger/Zalo groups. Never put the API secret in a public frontend HTML file for a public website; use a protected server-side flow instead.
