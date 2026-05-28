from flask import Flask, request, jsonify
from groq import Groq
import json
from datetime import datetime

app = Flask(__name__)
client = Groq(api_key="GROQ_API_KEY")

conversation_history = []

def reset_history():
    global conversation_history
    conversation_history = [{
        "role": "system",
        "content": "You are a helpful AI assistant for Charan, an aspiring AI Engineer."
    }]

reset_history()

@app.route("/")
def home():
    return open("index.html", encoding="utf-8").read()

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    conversation_history.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        messages=conversation_history,
        model="llama-3.3-70b-versatile",
    )

    ai_reply = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": ai_reply})

    return jsonify({"reply": ai_reply})

@app.route("/clear", methods=["POST"])
def clear():
    reset_history()
    return jsonify({"status": "cleared"})

@app.route("/save", methods=["POST"])
def save():
    filename = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(conversation_history, f, indent=4)
    return jsonify({"filename": filename})

if __name__ == "__main__":
    app.run(debug=True)