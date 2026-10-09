import os
import secrets
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# For production, set ALLOWED_ORIGINS to your frontend domain(s), comma-separated.
_origins = [x.strip() for x in os.getenv('ALLOWED_ORIGINS', '*').split(',') if x.strip()]
CORS(app, resources={r"/api/*": {"origins": _origins}})

API_SECRET = os.getenv('API_SECRET', '')

@app.get('/')
def index():
    return jsonify({"service": "Ghost Message API", "status": "running", "health": "/health"})

@app.get('/health')
def health():
    return jsonify({"ok": True, "status": "healthy"})

@app.post('/api/send')
def send_message():
    # Require a secret so strangers cannot use the deployed endpoint.
    if not API_SECRET:
        return jsonify({"ok": False, "error": "Server is not configured: set API_SECRET in Render Environment."}), 503
    supplied = request.headers.get('X-API-Key', '')
    if not secrets.compare_digest(supplied, API_SECRET):
        return jsonify({"ok": False, "error": "Unauthorized: invalid API key."}), 401

    data = request.get_json(silent=True) or {}
    platform = str(data.get('platform', '')).strip().lower()
    target = str(data.get('target', '')).strip()
    message = str(data.get('message', '')).strip()

    if platform not in ('zalo', 'messenger'):
        return jsonify({"ok": False, "error": "platform must be 'zalo' or 'messenger'."}), 400
    if not target or not message:
        return jsonify({"ok": False, "error": "target (group ID) and message are required."}), 400
    if len(message) > 4000:
        return jsonify({"ok": False, "error": "Message is too long (maximum 4000 characters)."}), 400

    # Intentionally do not pretend a message was delivered. Real delivery requires
    # an authorized provider integration and a supported destination/group API.
    return jsonify({
        "ok": False,
        "error": "Provider integration is not configured. This starter does not send messages yet.",
        "platform": platform,
        "target": target,
        "next_step": "Connect an officially supported API and authorized account for this destination."
    }), 501

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '10000')))
