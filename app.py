from flask import Flask, request

app = Flask(__name__)

@app.route("/callback", methods=["POST"])
def callback():
    data = request.json
    print("收到訊息：", data)
    return "OK"

if __name__ == "__main__":
    app.run()