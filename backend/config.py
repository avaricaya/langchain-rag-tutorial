from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
import os



from  ollama_query_data import get_reponse

app = Flask(__name__)
CORS(app) ##check if this is necessary


@app.post("/")
def chat():
    query = request.json.get("message")
    response = get_response(query)
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)