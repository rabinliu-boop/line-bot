from flask import Flask, request

app = Flask(__name__)

# 測試首頁（避免404）
@app.route("/")
def home():
    return "Bot is running"

# LINE webhook
@app.route("/callback", methods=["POST"])
def callback():
    print("🔥 收到LINE請求")
    print(request.json)
    return "OK"

if __name__ == "__main__":
    app.run()
