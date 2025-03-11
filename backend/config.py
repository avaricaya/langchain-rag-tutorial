from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
import os


sys.path.append('/home/avari/ChatBot_Repo/RAG/Chatbot')
from ollama_query_data import get_response

for p in sys.path:
    print(p)

app = Flask(__name__)
CORS(app) ##check if this is necessary


@app.post("/")
def chat():
    query = request.json.get("message")
    response = get_response(query)
    return jsonify({'response': response})

@app.route("/")
def welcome():
    return render_template('test.html')

if __name__ == "__main__":
    app.run(debug=True)