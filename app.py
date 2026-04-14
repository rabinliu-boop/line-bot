from flask import Flask, request
import requests
import json
import re

app = Flask(__name__)

# ⚠️ 請換成你的 LINE token
CHANNEL_ACCESS_TOKEN = "Mn03tLk/2u8uW4mUHoS+9Z7xfkvqDpeAhfgPCP4wN/BcaEiNEvkU5WYvBaeZrSYMFiVetB6aOHp0zLpQ46RJ0GSnJ+15+XUrqrZsD15/iHm/MilMrvlbcrpeEm2pMC9/DlWvU3D1FD02E7ea9qYMwQdB04t89/1O/w1cDnyilFU="

# =========================
# 首頁
# =========================
@app.route("/")
def home():
    return "Bot is running"

# =========================
# webhook
# =========================
@app.route("/callback", methods=["POST"])
def callback():
    try:
        data = request.json
        print("🔥 收到LINE請求")
        print(data)

        for event in data.get("events", []):
            if event["type"] == "message":

                text = event["message"]["text"]
                reply_token = event["replyToken"]

                reply = handle_message(text)

                reply_message(reply_token, reply)

        return "OK"

    except Exception as e:
        print("❌ callback error:", str(e))
        return "OK"

# =========================
# 訊息處理中心
# =========================
def handle_message(text):

    # 👉 相簿模式
    if text.startswith("!"):

        raw = text.replace("!", "").strip()

        # 空值防呆
        if not raw:
            return "❌請輸入內容\n範例：\n!115.04.15大莊園：室內隔間完成（銘）"

        result = parse_album(raw)

        if result:
            return (
                "📌解析成功\n"
                f"日期: {result['date']}\n"
                f"工地: {result['site']}\n"
                f"進度: {result['progress']}\n"
                f"人員: {result['person']}"
            )
        else:
            return (
                "❌格式錯誤\n\n"
                "正確格式：\n"
                "!115.04.15大莊園：室內隔間完成（銘）"
            )

    # 👉 一般訊息
    return "你說的是：" + text


# =========================
# 解析相簿格式
# =========================
def parse_album(text):

    pattern = r"(\d{3}\.\d{2}\.\d{2})([^：]+)：(.+?)（(.+?)）"
    match = re.match(pattern, text)

    if not match:
        return None

    return {
        "date": match.group(1),
        "site": match.group(2),
        "progress": match.group(3),
        "person": match.group(4)
    }


# =========================
# LINE reply
# =========================
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

    try:
        res = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            timeout=5
        )

        print("reply status:", res.status_code)
        print("reply response:", res.text)

    except Exception as e:
        print("❌ reply error:", str(e))


# =========================
# 啟動
# =========================
if __name__ == "__main__":
    app.run()
