from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import requests
import os
from dotenv import load_dotenv  

app = Flask(__name__)

# Allow all domains to access your API (this is fine in development, but in production, specific domains should be restricted)
CORS(app)

# Configure OpenAI API URL and default instructions
OPENAI_API_URL = "https://api.openai.com/v1/realtime"
DEFAULT_INSTRUCTIONS = "You are helpful and have some tools installed.\n\nIn the tools you have the ability to control a robot hand."

# FLASK_ENVが指定されていなければ 'development' とみなす
if os.environ.get('FLASK_ENV', 'development') != 'production':
    # ローカル環境の場合は .env ファイルから環境変数を読み込む
    load_dotenv()

# 環境変数からAPIキーを取得
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# Homepage route (optional)
@app.route('/')
def home():
    return "Flask API is running!"

@app.route('/api/rtc-connect', methods=['POST'])
def connect_rtc():
    # Get the request body from the client
    body = request.get_data(as_text=True)

    # Build the OpenAI API request URL
    url = f"{OPENAI_API_URL}?model=gpt-4o-realtime-preview-2024-12-17&instructions={DEFAULT_INSTRUCTIONS}&voice=ash"

    # Set the request headers
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/sdp"
    }

    # Send POST request to the OpenAI API
    response = requests.post(url, headers=headers, data=body)

    # Return the OpenAI response, maintaining the same content type
    return response.content, 200, {'Content-Type': 'application/sdp'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8813))
    debug_mode = os.environ.get('FLASK_ENV', 'development') != 'production'
    app.run(port=port, debug=debug_mode)
