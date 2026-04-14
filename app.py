from flask import Flask, request
import requests
import json

app = Flask(__name__)

# ⚠️ 換成你的 LINE Channel Access Token
CHANNEL_ACCESS_TOKEN = "請貼你的token"

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
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": "Bearer " + CHANNEL_ACCESS_TOKEN.strip()
    }

    payload = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }

    res = requests.post(
        url,
        headers=headers,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8")
    )

    print("reply status:", res.status_code)
    print("reply response:", res.text)

if __name__ == "__main__":
    app.run()
