from flask import Flask, request
import requests
import json

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = "Mn03tLk/2u8uW4mUHoS+9Z7xfkvqDpeAhfgPCP4wN/BcaEiNEvkU5WYvBaeZrSYMFiVetB6aOHp0zLpQ46RJ0GSnJ+15+XUrqrZsD15/iHm/MilMrvlbcrpeEm2pMC9/DlWvU3D1FD02E7ea9qYMwQdB04t89/1O/w1cDnyilFU="

@app.route("/")
def home():
    return "Bot is running"


@app.route("/callback", methods=["POST"])
def callback():

    try:
        data = request.get_json(silent=True)

        print("🔥 RAW:", data)

        if not data:
            return "OK"

        for event in data.get("events", []):

            if event.get("type") != "message":
                continue

            text = event["message"].get("text", "")
            reply_token = event.get("replyToken")

            reply = handle_message(text)

            reply_message(reply_token, reply)

        return "OK"

    except Exception as e:
        print("❌ callback error:", str(e))
        return "OK"


# =========================
# 核心處理
# =========================
def handle_message(text):

    print("📩 RAW:", repr(text))

    text = str(text).replace("！", "!").strip()

    print("🧹 CLEAN:", repr(text))

    if text.startswith("!"):

        raw = text[1:].strip()

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

        return "❌格式錯誤\n請加：\n： 和 （）"

    return "你說的是：" + text


# =========================
# 🔥 修正 parser（支援你現在格式）
# =========================
def parse_album(text):

    try:
        # ❗ 修正：你現在沒有「：」版本
        if "：" not in text:
            return None

        left, right = text.split("：", 1)

        date = left[:10]
        site = left[10:].strip()

        if "（" not in right or "）" not in right:
            return None

        progress = right.split("（")[0].strip()
        person = right.split("（")[1].replace("）", "").strip()

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
# 🔥 修正 reply（關鍵）
# =========================
def reply_message(reply_token, text):

    try:
        url = "https://api.line.me/v2/bot/message/reply"

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + CHANNEL_ACCESS_TOKEN.strip()
        }

        payload = {
            "replyToken": reply_token,
            "messages": [
                {"type": "text", "text": text}
            ]
        }

        # ❗ 重要：不要 encode，不要 json.dumps
        res = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=5
        )

        print("📤 status:", res.status_code)
        print("📤 response:", res.text)

    except Exception as e:
        print("❌ reply error:", str(e))


if __name__ == "__main__":
    app.run()
