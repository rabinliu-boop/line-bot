from flask import Flask, request
import requests

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = "你的token請貼這裡"

@app.route("/")
def home():
    return "Bot is running"

@app.route("/callback", methods=["POST"])
def callback():
    data = request.json
    print("🔥 收到LINE請求")
    print(data)

    for event in data.get("events", []):
        if event["type"] == "message":
            text = event["message"]["text"]
            reply_token = event["replyToken"]

            reply_message(reply_token, "你說的是：" + text)

    return "OK"

def reply_message(reply_token, text):
    url = "https://api.line.me/v2/bot/message/reply"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }

    payload = {
        "replyToken": reply_token,
        "messages": [
            {"type": "text", "text": text}
        ]
    }

    res = requests.post(url, headers=headers, json=payload)
    print("reply status:", res.status_code)
    print("reply response:", res.text)

if __name__ == "__main__":
    app.run()
