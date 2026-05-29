from flask import Flask, request, jsonify
from groq import Groq
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

conversation_history = []

def reset_history():
    global conversation_history
    conversation_history = [{
        "role": "system",
        "content": """You are an expert AI assistant for Charan, a 3rd year Computer Science student and aspiring AI Engineer.

You specialize in three areas:
1. DSA — explain problems step by step, give hints before full solutions, use Java for code examples
2. AI Engineering — explain LLMs, APIs, RAG, agents, prompt engineering with practical examples
3. General Coding — Python, JavaScript, React, Node.js, Flask

Your communication style:
- Be direct and concise, no fluff
- Use examples and analogies to explain concepts
- When explaining DSA, always show step by step thinking
- When explaining AI concepts, relate them to real world applications
- Give code examples in the language relevant to the topic
- If asked about a problem, give hints first, full solution only if asked

Always address the user as Charan."""
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