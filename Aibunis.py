from flask import Flask, request, render_template, jsonify
import requests
from dotenv import load_dotenv
import os

load_dotenv()
GROQ = os.getenv("GROQ_KEY")
CHARACTER = os.getenv("PROMPT")

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get('prompt', '')
    api_url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {GROQ}'
    }
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": CHARACTER},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            ai_message = result['choices'][0]['message']['content']
        else:
            ai_message = f"API error (status {response.status_code}): {response.text}"
    except Exception as e:
        ai_message = f"Error fetching data: {e}"

    return jsonify({"ai_message": ai_message})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    # app.run(debug=True)