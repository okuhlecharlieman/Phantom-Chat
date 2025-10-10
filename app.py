
from flask import Flask, render_template, request, jsonify
import random
import requests

app = Flask(__name__)


messages = [
    "Did you feel that cold breeze? 👻",
    "Someone’s watching you...",
    "You shouldn’t have typed that...",
    "It’s too late to log off now...",
]

def get_ai_reply(user_message):
    # Hugging Face Inference API for DialoGPT (no auth required for small requests)
    url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
    payload = {"inputs": {"text": user_message}}
    try:
        response = requests.post(url, json=payload, timeout=8)
        if response.status_code == 200:
            data = response.json()
            # Extract generated text
            ai_reply = data.get('generated_text')
            if ai_reply:
                return ai_reply
    except Exception:
        pass
    # Fallback to spooky message
    return random.choice(messages)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    reply = get_ai_reply(user_message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
