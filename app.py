from flask import Flask, request
import requests
import json

app = Flask(__name__)

# ⚠️ 填你的 LINE token
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
        print(json.dumps(data, ensure_ascii=False, indent=2))

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
# 訊息處理（重點）
# =========================
def handle_message(text):

    print("📩 RAW:", repr(text))

    # 🔥 統一全形 → 半形
    text = str(text).replace("！", "!").strip()

    print("🧹 CLEAN:", repr(text))

    # =========================
    # 相簿模式
    # =========================
    if text.startswith("!"):

        raw = text[1:].strip()

        print("📦 RAW AFTER !:", repr(raw))

        result = parse_album(raw)

        print("📊 RESULT:", result)

        if result:
            return (
                "📌解析成功\n"
                f"日期: {result['date']}\n"
                f"工地: {result['site']}\n"
                f"進度: {result['progress']}\n"
                f"人員: {result['person']}"
            )

        return (
            "❌格式錯誤\n\n"
            "正確格式：\n"
            "!115.04.15大莊園：室內隔間完成（銘）"
        )

    # =========================
    # 一般訊息
    # =========================
    return "你說的是：" + text


# =========================
# 解析器（穩定版）
# =========================
def parse_album(text):

    try:
        if "：" not in text:
            return None

        left, right = text.split("：", 1)

        left = left.strip()
        right = right.strip()

        if len(left) < 10:
            return None

        date = left[:10]
        site = left[10:].strip()

        if "（" not in right or "）" not in right:
            return None

        progress = right.split("（")[0].strip()
        person = right.split("（")[1].replace("）", "").strip()

        if not date or not site or not progress or not person:
            return None

        return {
            "date": date,
            "site": site,
            "progress": progress,
            "person": person
        }

    except Exception as e:
        print("❌ parse error:", str(e))
        return None


# =========================
# reply
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

        print("📤 status:", res.status_code)
        print("📤 response:", res.text)

    except Exception as e:
        print("❌ reply error:", str(e))


# =========================
# run
# =========================
if __name__ == "__main__":
    app.run()
