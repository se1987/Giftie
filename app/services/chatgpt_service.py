import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain.prompts import PromptTemplate

# 環境変数をロード
load_dotenv()

# OpenAI APIキーの設定
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("Error: OpenAI API key is not set")

# OpenAIの設定
client = OpenAI(api_key=openai_api_key)

# プロンプトテンプレートの設定
prompt_template = PromptTemplate(
    input_variables=["user_message", "conversation_history"],
    template="""
    あなたは親切なアシスタントです。以下はユーザーからの会話履歴と最新のメッセージです。良いギフトのアイデアを5つ提案してください。
    例: 1.インテリア雑貨やキャンドル 2.リラックスできる入浴剤セット 3.人気のアイシャドウやリップ
    会話履歴: {conversation_history}
    ユーザー: {user_message}
    相手の年齢: {age}
    相手との関係: {relationship}
    カテゴリー: {category}
    趣味: {hobby}
    アシスタント:
    """
)

# プロンプトテンプレート for keyword extraction
keyword_extraction_template = PromptTemplate(
    input_variables=["response"],
    template="""
    以下の文章から、関連するキーワードを抽出してください。各提案について3つの重要な名詞を抽出し、それぞれのキーワードを空白で区切って出力してください。
    例1: (1.美味しいスイーツやお菓子の詰め合わせ) -> スイーツ お菓子 詰め合わせ
    例2: (2.おしゃれな文房具セット) -> おしゃれ 文房具 セット
    
    文章:
    {response}
    """
)

def get_conversation_history(user_id):
    # ダミーデータを返す
    return "ユーザー: 良いギフトのアイデアは何ですか？\nAI: いくつかのギフトの提案があります:"

def process_message(user_id, user_message, conversation_history, age, relationship, category, hobby):
    prompt = prompt_template.format(
        user_message=user_message, 
        conversation_history=conversation_history,
        age=age,
        relationship=relationship,
        category=category,
        hobby=hobby
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたは親切なアシスタントです。"},
            {"role": "user", "content": conversation_history},
            {"role": "user", "content": user_message},
            {"role": "user", "content": f"相手の年齢: {age}"},
            {"role": "user", "content": f"相手との関係: {relationship}"},
            {"role": "user", "content": f"カテゴリー: {category}"},
            {"role": "user", "content": f"趣味: {hobby}"}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

# この関数がapp.pyに呼び出されて、キーワード＋プレゼント＋性別情報を渡す
def extract_keywords(gpt_response, gender=None):
    prompt = keyword_extraction_template.format(response=gpt_response)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたはキーワード抽出のエキスパートです。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    raw_keywords = response.choices[0].message.content.strip().split("\n")
    
    # キーワードに "プレゼント" と性別を追加し、見出し番号を削除
    formatted_keywords = []
    for keyword in raw_keywords:

        formatted_keyword = keyword
        formatted_keywords.append(formatted_keyword)
    
    return formatted_keywords