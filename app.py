from flask import Flask, request, jsonify
from brain import chrome_reply

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>CHROME</title>
<style>
body{background:#0b0b0b;color:white;font-family:sans-serif;padding:15px}
#box{height:70vh;overflow:auto;border:1px solid #333;padding:10px;border-radius:12px}
.msg{margin:8px 0;padding:10px;border-radius:10px}
.me{background:#1a73e8;text-align:right}
.bot{background:#222}
input{width:75%;padding:12px;border-radius:20px;border:none}
button{padding:12px 16px;border-radius:20px;border:none;background:#1a73e8;color:white}
</style></head>
<body>
<h2>CHROME</h2>
<div id="box"></div><br>
<input id="inp" placeholder="Parle a CHROME...">
<button onclick="send()">Envoyer</button>
<script>
async function send(){
  let v=document.getElementById('inp').value;
  if(!v) return;
  let box=document.getElementById('box');
  box.innerHTML+='<div class="msg me">'+v+'</div>';
  document.getElementById('inp').value='';
  let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:v})});
  let d=await r.json();
  box.innerHTML+='<div class="msg bot">'+d.reply+'</div>';
  box.scrollTop=box.scrollHeight;
}
</script></body></html>
"""

@app.route("/")
def home():
    return HTML

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("message", "")
    reply = chrome_reply(msg)
    if reply is None:
        reply = "Je t'ecoute. Essaie !remember pour que je retienne, et !recall pour que je me souvienne."
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
