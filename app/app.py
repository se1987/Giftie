
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv
from datetime import datetime

from services.chatgpt_service import process_message, get_conversation_history, extract_keywords
from services.rakuten_service import search_products

# 環境変数をロード
load_dotenv()

app = Flask(__name__)

# LINEチャネルアクセストークンとシークレットを環境変数から取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    raise ValueError("Error: LINE_CHANNEL_ACCESS_TOKEN and LINE_CHANNEL_SECRET must be set")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ユーザーの状態を管理する辞書
user_states = {}

@app.route("/callback", methods=['POST'])
def callback():
    # X-Line-Signatureヘッダーの値を取得
    signature = request.headers['X-Line-Signature']

    # リクエストボディをテキストとして取得
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # Webhookボディを処理
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    user_id = event.source.user_id

    # ユーザーの状態を管理
    current_date = datetime.now()
    last_interaction_date = user_states.get(user_id, {}).get("last_interaction_date", current_date)
    days_since_last_interaction = (current_date - last_interaction_date).days

    if user_id not in user_states:
        user_states[user_id] = {"step": 0, "last_interaction_date": current_date}

    step = user_states[user_id]["step"]

    if days_since_last_interaction > 0:
        if step == 0:
            reply_message = "久しぶり！お元気でしたか？私はギフティーです。まず、贈る相手について少し教えてください。贈る相手の性別を教えてください。（例: 男性、女性、どちらでも）"
            user_states[user_id]["step"] = 1
        else:
            reply_message = "お久しぶりです！再びお手伝いできて嬉しいです。どのようなプレゼントをお探しですか？"
    else:
        if step == 0:
            reply_message = "こんにちは！私はギフティーです。あなたにぴったりのプレゼントを提案します。まず、贈る相手について少し教えてください。贈る相手の性別を教えてください。（例: 男性、女性、どちらでも）"
            user_states[user_id]["step"] = 1
        elif step == 1:
            user_states[user_id]["gender"] = user_message
            reply_message = "相手の年齢を教えてください。（例: 30歳）"
            user_states[user_id]["step"] = 2
        elif step == 2:
            user_states[user_id]["age"] = user_message
            reply_message = "相手との関係を教えてください。（例: 友人、恋人、家族）"
            user_states[user_id]["step"] = 3
        elif step == 3:
            user_states[user_id]["relationship"] = user_message
            reply_message = "どのカテゴリーのプレゼントが良いですか？（例: アクセサリー、ファッション、ガジェット、グルメ）"
            user_states[user_id]["step"] = 4
        elif step == 4:
            user_states[user_id]["category"] = user_message
            reply_message = "相手の趣味や嗜好について教えてください。（例: 音楽、スポーツ、料理、読書など）"
            user_states[user_id]["step"] = 5
        elif step == 5:
            user_states[user_id]["hobby"] = user_message
            reply_message = "予算を教えてください。（例: 5000円、10000円）"
            user_states[user_id]["step"] = 6
        elif step == 6:
            user_states[user_id]["budget"] = int(user_message.replace("円", "").strip())  # 予算を整数に変換
            conversation_history = get_conversation_history(user_id)
            gpt_response = process_message(user_id, user_message, conversation_history)
            print(f"ChatGPT Response: {gpt_response}")
            gender = user_states[user_id].get("gender")
            keywords = extract_keywords(gpt_response, gender)
            print(f"Extracted keywords: {keywords}")
            products = search_products(keywords, user_states[user_id]["budget"])  # 予算を渡す
            user_states[user_id]["suggestions"] = products
            if products:
                reply_message = "あなたの情報に基づいて、以下のプレゼントを提案します！\n" + "\n".join(products) + "\nもっと詳しく知りたい商品番号を教えてください。または、再提案を希望する場合は「再提案」と入力してください。"
            else:
                reply_message = "該当する商品が見つかりませんでした。もう一度やり直してください。"
            user_states[user_id]["step"] = 7
        elif step == 7:
            if user_message.lower() == "再提案":
                reply_message = "新しい提案を準備します。少々お待ちください..."
                user_states[user_id]["step"] = 6  # 再提案のため予算の確認ステップに戻る
            else:
                try:
                    suggestion_index = int(user_message.split("提案")[1]) - 1
                    reply_message = f"{user_states[user_id]['suggestions'][suggestion_index]}の詳細はこちらです：..."
                    user_states[user_id]["step"] = 8
                except (IndexError, ValueError):
                    reply_message = "正しい商品番号を入力してください。"
                    user_states[user_id]["step"] = 7
        elif step == 8:
            if user_message.lower() == "購入":
                reply_message = "購入手続きに進みます。以下のリンクから購入ページにアクセスしてください：..."
                user_states[user_id]["step"] = 0  # 購入後、ステップを初期化
            elif user_message.lower() == "質問":
                reply_message = "ご質問をどうぞ。"
                user_states[user_id]["step"] = 8  # 質問中は同じステップを維持
            else:
                reply_message = '本日はご利用ありがとうございました！またのご利用をお待ちしております。ご意見やご感想がありましたら教えてくださいね。'
                user_states[user_id]["step"] = 0  # 初期ステップに戻す

    user_states[user_id]["last_interaction_date"] = current_date

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

