from flask import Flask, request, jsonify
import json, os, requests

app = Flask(__name__)

# --- Load the knowledge base ---
with open("knowledge_base.json", "r") as f:
    KNOWLEDGE_BASE = json.load(f)

# --- Telegram setup ---
TELEGRAM_TOKEN = os.getenv("7441762426:AAG6CTvPAFFV-dRbtjXSNT6OLAKcbjwPzGU")
TELEGRAM_URL = f"https://api.telegram.org/bot{7441762426:AAG6CTvPAFFV-dRbtjXSNT6OLAKcbjwPzGU}"

# --- Function to handle queries ---
def handle_query(query):
    query = query.lower()
    for key, value in KNOWLEDGE_BASE.items():
        if key in query:
            return value
    return "Sorry, I don't have info on that yet. Try asking about irrigation, soil, pests, or fertilizer."

# --- Telegram webhook route ---
@app.route("/telegram_webhook", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if not data or "message" not in data:
        return "ok"
    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")
    reply = handle_query(text)
    requests.post(f"{TELEGRAM_URL}/sendMessage", json={"chat_id": chat_id, "text": reply})
    return "ok"

# --- Local test route (for testing without Telegram) ---
@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message", "")
    return jsonify({"reply": handle_query(msg)})

if __name__== "__main__":
    app.run( host="0.0.0.0.",port=5000)