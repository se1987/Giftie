
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import os
from dotenv import load_dotenv
from database import create_connection, close_connection

load_dotenv()

app = Flask(__name__)

# LINE API設定
line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))

# OpenAI API設定
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_message = event.message.text

    connection = create_connection()

    # ユーザー情報の保存
    cursor = connection.cursor()
    cursor.execute("INSERT IGNORE INTO users (user_id) VALUES (%s)", (user_id,))
    connection.commit()

    # 過去のメッセージ履歴を取得
    cursor.execute("SELECT message, response FROM messages WHERE user_id = %s", (user_id,))
    messages = cursor.fetchall()

    conversation_history = "\n".join([f"{row[0]}: {row[1]}" for row in messages])

    # ChatGPTにメッセージを送信
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": conversation_history},
            {"role": "user", "content": user_message}
        ]
    )

    reply_text = response.choices[0].message.content

    # メッセージと応答を保存
    cursor.execute(
        "INSERT INTO messages (user_id, message, response) VALUES (%s, %s, %s)",
        (user_id, user_message, reply_text)
    )
    connection.commit()
    cursor.close()
    close_connection(connection)

    # LINEに返信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

