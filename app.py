from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Ghost replies
GHOST_REPLIES = [
    "I see you...",
    "Why are you here?",
    "Don't look behind you...",
    "You can't escape me...",
    "The darkness is watching...",
    "You shouldn't be here...",
    "I am always near..."
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    # Choose random ghost reply
    ghost_message = random.choice(GHOST_REPLIES)
    return jsonify({"reply": ghost_message})

if __name__ == "__main__":
    app.run(debug=True)
