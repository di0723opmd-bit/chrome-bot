from flask import Flask, request, jsonify
from brain import chrome_reply, prove_memory, recall

app = Flask(__name__)

@app.route("/")
def home():
    return "CHROME est en ligne. Mémoire active."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("message", "")
    reply = chrome_reply(msg)
    if reply is None:
        reply = "Je t'écoute. Dis-moi quoi retenir avec !remember, ou demande-moi !recall."
    return jsonify({"reply": reply})

@app.route("/prove")
def prove():
    return jsonify({"preuve": prove_memory()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
