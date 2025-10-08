from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

messages = [
    "Did you feel that cold breeze? 👻",
    "Someone’s watching you...",
    "You shouldn’t have typed that...",
    "It’s too late to log off now...",
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    return jsonify({"reply": random.choice(messages)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
