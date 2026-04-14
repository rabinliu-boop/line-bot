from flask import Flask, request
import requests
import json

app = Flask(__name__)

# ⚠️ 請填你的 LINE token
CHANNEL_ACCESS_TOKEN = "Mn03tLk/2u8uW4mUHoS+9Z7xfkvqDpeAhfgPCP4wN/BcaEiNEvkU5WYvBaeZrSYMFiVetB6aOHp0zLpQ46RJ0GSnJ+15+XUrqrZsD15/iHm/MilMrvlbcrpeEm2pMC9/DlWvU3D1FD02E7ea9qYMwQdB04t89/1O/w1cDnyilFU="

# =========================
# 首頁測試
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
# 訊息處理
# =========================
def handle_message(text):

    # 👉 相簿模式
    if text.startswith("!"):
        raw = text[1:].strip()  # 去掉 !

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
                "請用以下格式：\n"
                "!115.04.15大莊園：室內隔間完成（銘）"
            )

    # 👉 一般訊息
    return "你說的是：" + text


# =========================
# 超穩定解析（重點）
# =========================
def parse_album(text):

    try:
        # 必須有 ：
        if "：" not in text:
            return None

        left, right = text.split("：", 1)

        left = left.strip()
        right = right.strip()

        # 日期固定 10 碼（115.04.15）
        date = left[:10]
        site = left[10:].strip()

        # 人員（最後括號）
        if "（" in right and "）" in right:
            progress = right.split("（")[0].strip()
            person = right.split("（")[1].replace("）", "").strip()
        else:
            return None

        # 基本檢查
        if not date or not site or not progress or not person:
            return None

        return {
            "date": date,
            "site": site,
            "progress": progress,
            "person": person
        }

    except:
        return None


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
