
from flask import Flask, render_template, request, jsonify
import random
import requests
import logging
logging.basicConfig(
    filename='chat.log',
    level=logging.INFO,  # Changed to INFO to see all requests
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
    filemode='a'  # Append mode
)

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
    payload = {"inputs": user_message}  # Fixed payload format
    
    try:
        logging.info(f"Sending request to Hugging Face API with message: {user_message}")
        response = requests.post(url, json=payload, timeout=8)
        
        if response.status_code == 200:
            data = response.json()
            logging.info(f"API Response: {data}")
            
            # Handle different response formats
            if isinstance(data, list) and len(data) > 0:
                # List response format
                ai_reply = data[0].get('generated_text', '')
            elif isinstance(data, dict):
                # Dictionary response format
                ai_reply = data.get('generated_text', '')
            else:
                logging.error(f"Unexpected API response format: {data}")
                return random.choice(messages)
                
            if ai_reply:
                # Make the reply more ghostly
                spooky_prefixes = ["*whispers* ", "*ethereal voice* ", "*ghostly* ", "👻 "]
                return random.choice(spooky_prefixes) + ai_reply
        else:
            logging.error(f"Hugging Face API error: {response.status_code} {response.text}")
    except requests.exceptions.Timeout:
        logging.error("API request timed out")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {str(e)}")
    except Exception as e:
        logging.exception(f"Exception in get_ai_reply: {e}")
    
    # Fallback to spooky message
    return random.choice(messages)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "")
        reply = get_ai_reply(user_message)
        return jsonify({"reply": reply})
    except Exception as e:
        logging.exception(f"Exception in /chat endpoint: {e}")
        return jsonify({"reply": random.choice(messages)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
