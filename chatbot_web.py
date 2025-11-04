import os
from flask import Flask, request, jsonify, make_response

# Import your existing chatbot logic
try:
    from name import get_response
except ImportError:
    # Fallback implementation if name module is not found
    def get_response(message):
        return f"Echo: {message}"


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    html = """
<!doctype html>
<html>
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>Chatbot</title>
    <style>
      :root { color-scheme: dark; }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        background: #0b0b0b;
        color: #eaeaea;
        font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        min-height: 100vh;
        display: grid;
        place-items: center;
      }
      .card {
        width: min(820px, 92vw);
        background: #0f0f10;
        border: 1px solid #1e1e22;
        border-radius: 14px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6), 0 0 0 1px #111 inset;
        display: flex;
        flex-direction: column;
        overflow: hidden;
      }
      .header {
        padding: 14px 18px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(180deg, #121214, #0f0f10);
        border-bottom: 1px solid #1e1e22;
      }
      .title { font-weight: 600; font-size: 16px; color: #ffffff; }
      .status { font-size: 12px; color: #8a8f98; }

      .chat {
        height: min(60vh, 560px);
        overflow: auto;
        padding: 16px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        scroll-behavior: smooth;
        background: repeating-linear-gradient(
          0deg,
          rgba(255,255,255,0.02),
          rgba(255,255,255,0.02) 1px,
          transparent 1px,
          transparent 20px
        );
      }
      .msg { max-width: 88%; padding: 10px 12px; border-radius: 12px; line-height: 1.4; }
      .user { align-self: flex-end; background: #1e2a4a; color: #e5eeff; border: 1px solid #29365a; }
      .bot { align-self: flex-start; background: #131416; color: #eaeaea; border: 1px solid #232428; }
      .time { display: block; margin-top: 6px; font-size: 11px; color: #9aa3ad; }

      .input-row {
        display: flex;
        gap: 10px;
        padding: 12px;
        border-top: 1px solid #1e1e22;
        background: #0e0e10;
      }
      .inp {
        flex: 1;
        background: #0a0a0b;
        color: #eaeaea;
        border: 1px solid #22252a;
        border-radius: 10px;
        padding: 12px 14px;
        outline: none;
      }
      .inp::placeholder { color: #808691; }
      .inp:focus { border-color: #3d7fff; box-shadow: 0 0 0 2px rgba(61,127,255,0.2); }

      .btn {
        background: #1463ff;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0 16px;
        min-width: 92px;
        font-weight: 600;
        cursor: pointer;
      }
      .btn:disabled { opacity: .7; cursor: not-allowed; }

      @media (max-width: 520px) {
        .chat { height: 56vh; }
        .btn { min-width: 84px; }
      }
    </style>
  </head>
  <body>
    <div class=\"card\">
      <div class=\"header\">
        <div class=\"title\">Chatbot</div>
      </div>
      <div id=\"chat\" class=\"chat\" aria-live=\"polite\" aria-label=\"Chat messages\"></div>
      <div class=\"input-row\">
        <input id=\"text\" class=\"inp\" autocomplete=\"off\" placeholder=\"Type a message and press Enter\" />
        <button id=\"send\" class=\"btn\">Send</button>
      </div>
    </div>

    <script>
      const chat = document.getElementById('chat');
      const input = document.getElementById('text');
      const sendBtn = document.getElementById('send');

      function now() {
        const d = new Date();
        return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      }

      function appendMessage(text, who) {
        const div = document.createElement('div');
        div.className = 'msg ' + (who === 'user' ? 'user' : 'bot');
        div.innerText = text;
        const time = document.createElement('span');
        time.className = 'time';
        time.textContent = now();
        div.appendChild(time);
        chat.appendChild(div);
        chat.scrollTop = chat.scrollHeight;
      }

      async function sendMessage() {
        const text = input.value.trim();
        if (!text) return;
        appendMessage(text, 'user');
        input.value = '';
        input.focus();
        sendBtn.disabled = true;
        try {
          const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
          });
          const data = await res.json();
          appendMessage(data.reply || '...', 'bot');
        } catch (e) {
          appendMessage('Error: ' + String(e), 'bot');
        } finally {
          sendBtn.disabled = false;
        }
      }

      sendBtn.addEventListener('click', sendMessage);
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          sendMessage();
        }
      });

      // Initial bot greeting
      appendMessage("Hi! I'm your Python chatbot. How can I help?", 'bot');
      input.focus();
    </script>
  </body>
</html>
    """
    return make_response(html)


@app.route("/chat", methods=["POST"])
def chat_api():
    payload = request.get_json(silent=True) or {}
    msg = str(payload.get("message") or "")
    reply = get_response(msg)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8001"))
    app.run(host="0.0.0.0", port=port, debug=True)
