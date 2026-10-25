import os
import hmac
import hashlib
from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "shiksha_hub_verify_2026")

@app.route("/", methods=["GET"])
def home():
    return "SHIKSHA HUB WhatsApp Webhook is running!", 200

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200

    return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json(silent=True) or {}
    print("WhatsApp webhook event received:", data)

    try:
        entries = data.get("entry", [])
        for entry in entries:
            for change in entry.get("changes", []):
                value = change.get("value", {})
                for message in value.get("messages", []):
                    sender = message.get("from", "")
                    text = message.get("text", {}).get("body", "").strip()
                    if text:
                        print(f"Incoming message from {sender}: {text}")
    except Exception as error:
        print("Webhook processing error:", error)

    return "EVENT_RECEIVED", 200
