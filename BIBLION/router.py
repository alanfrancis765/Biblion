import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = "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"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful book assistant. "
                "When a user gives a book name, provide: "
                "1. Title\n2. Author\n3. Publication Year\n4. Genre\n5. Short Summary. "
                "If the book is not found, politely say so."
            )
        },
        {"role": "user", "content": user_message}
    ]

    response = requests.post(
        OPENROUTER_URL,
        headers=HEADERS,
        json={
            "model": "google/gemini-2.5-flash-preview-09-2025",
            "messages": messages,
            "max_tokens": 500,
            "temperature": 0.7
        }
    )

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    else:
        return jsonify({"error": response.text}), response.status_code

if __name__ == "__main__":
    app.run(debug=True, port=5000)
