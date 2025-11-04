from flask import Flask, request, jsonify
import json, os, requests

app = Flask(__name__)

# --- Load the knowledge base ---
with open("knowledge_base.json", "r") as f:
    KNOWLEDGE_BASE = json.load(f)

# --- Telegram setup ---
TELEGRAM_TOKEN = "7441762426:AAG6CTvPAFFV-dRbtjXSNT6OLAKcbjwPzGU"
TELEGRAM_URL = "https://api.telegram.org/bot{7441762426:AAG6CTvPAFFV-dRbtjXSNT6OLAKcbjwPzGU}"

# --- Function to handle queries ---
def handle_query(query):
    ...
    return "some reply"
# --- Telegram webhook route ---
@app.route("/telegram_webhook", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"status":"ignored"}),200
    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")
    reply = handle_query(text)

   response= requests.post(f"{TELEGRAM_URL}/sendMessage", json={"chat_id": chat_id, "text": reply})
    print("Telegram sendMessage response:",response.text)
return jsonify({"status":"ok"},200)

# --- Local test route (for testing without Telegram) ---
@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message", "")
    return jsonify({"reply": handle_query(msg)})
if __name__== "_main_":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)