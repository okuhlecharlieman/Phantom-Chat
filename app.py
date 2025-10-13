
from flask import Flask, render_template, request, jsonify
import random
import requests
import logging
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Set up logging to both file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
    handlers=[
        logging.FileHandler('chat.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)


messages = [
    "Did you feel that cold breeze? 👻",
    "Someone's watching you...",
    "You shouldn't have typed that...",
    "It's too late to log off now...",
    "The spirits are restless tonight... 👻",
    "I sense a dark presence... 🕯️",
    "Your soul feels... interesting... 💀",
    "Do you believe in ghosts? You will... 👻",
    "The shadows are moving... 🌘",
]

def make_spooky_response(text):
    """Make any response more spooky"""
    spooky_prefixes = [
        "*whispers* ",
        "*ethereal voice* ",
        "*ghostly* ",
        "👻 ",
        "*cold breath* ",
        "*shadows dancing* ",
    ]
    spooky_suffixes = [
        " 👻",
        " 🌘",
        " 🕯️",
        " 💀",
        "...",
        "... 👻",
    ]
    return random.choice(spooky_prefixes) + text + random.choice(spooky_suffixes)

def get_ai_reply(user_message):
    # Using a smaller, more reliable model
    url = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('HUGGING_FACE_API_TOKEN')}"
    }
    payload = {
        "inputs": user_message,
        "wait_for_model": true
    }
    
    try:
        logging.info(f"Sending request to Hugging Face API with message: {user_message}")
        logging.info(f"Headers: {headers}")
        logging.info(f"Payload: {payload}")
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        logging.info(f"Response status code: {response.status_code}")
        logging.info(f"Response headers: {response.headers}")
        
        # Log the raw response text
        logging.info(f"Raw response text: {response.text}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                logging.info(f"Parsed API Response: {data}")
                
                # Try different response formats
                if isinstance(data, dict):
                    if 'generated_text' in data:
                        ai_reply = data['generated_text']
                    elif 'response' in data:
                        ai_reply = data['response']
                    elif 'outputs' in data:
                        ai_reply = data['outputs']
                    else:
                        logging.error(f"Could not find response in data structure: {data}")
                        return make_spooky_response(random.choice(messages))
                elif isinstance(data, list) and len(data) > 0:
                    ai_reply = str(data[0])
                else:
                    logging.error(f"Unexpected API response format: {data}")
                    return make_spooky_response(random.choice(messages))
                
                if ai_reply and isinstance(ai_reply, str):
                    return make_spooky_response(ai_reply)
                else:
                    logging.error(f"Invalid AI reply format: {ai_reply}")
                    return make_spooky_response(random.choice(messages))
            except json.JSONDecodeError as e:
                logging.error(f"Failed to parse JSON response: {e}")
                return make_spooky_response(random.choice(messages))
        else:
            logging.error(f"Hugging Face API error: {response.status_code} {response.text}")
            if response.status_code == 403:
                logging.error("Authentication error - check your API token")
            elif response.status_code == 503:
                logging.error("Model is loading - this can take a few minutes on first request")
    except requests.exceptions.Timeout:
        logging.error("API request timed out")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {str(e)}")
    except Exception as e:
        logging.exception(f"Exception in get_ai_reply: {e}")
    
    # Fallback to spooky message
    return make_spooky_response(random.choice(messages))

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
