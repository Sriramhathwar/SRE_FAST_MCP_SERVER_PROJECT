from flask import Flask, request, jsonify
from agent.agent import handle_query
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/ask", methods=["POST"])
def ask():
    print("Inside ask block")
    query = request.json["query"]
    answer = handle_query(query)
    print("Answer : ", answer)
    return jsonify({"answer": answer})

app.run(host="0.0.0.0", port=5001)