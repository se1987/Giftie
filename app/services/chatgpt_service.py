# import os
# from dotenv import load_dotenv
# from openai import OpenAI
# from langchain.prompts import PromptTemplate

# # 環境変数をロード
# load_dotenv()

# # OpenAI APIキーの設定
# openai_api_key = os.getenv("OPENAI_API_KEY")

# if not openai_api_key:
#     raise ValueError("Error: OpenAI API key is not set")

# # OpenAIの設定
# client = OpenAI(api_key=openai_api_key)

# # プロンプトテンプレートの設定
# prompt_template = PromptTemplate(
#     input_variables=["user_message", "conversation_history"],
#     template="""
#     あなたは親切なアシスタントです。以下はユーザーからの会話履歴と最新のメッセージです。
#     会話履歴: {conversation_history}
#     ユーザー: {user_message}
#     アシスタント:
#     """
# )

# def get_conversation_history(user_id):
#     # ダミーデータを返す
#     return "ユーザー: 友人への良いギフトのアイデアは何ですか？\nAI: いくつかのギフトの提案があります:"

# def process_message(user_id, user_message, conversation_history):
#     prompt = prompt_template.format(user_message=user_message, conversation_history=conversation_history)
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "あなたは親切なアシスタントです。"},
#             {"role": "user", "content": conversation_history},
#             {"role": "user", "content": user_message}
#         ],
#         max_tokens=150
#     )
#     return response.choices[0].message.content.strip()

# def extract_keywords(gpt_response):
#     # 簡易的なキーワード抽出: 各提案の最初の名詞を抽出する
#     keywords = []
#     for line in gpt_response.split('\n'):
#         if line.strip():
#             keyword = line.split()[0]
#             if keyword:
#                 keywords.append(keyword + " プレゼント")
#     return keywords

# import os
# from dotenv import load_dotenv
# from openai import OpenAI
# from langchain.prompts import PromptTemplate
# import re

# # 環境変数をロード
# load_dotenv()

# # OpenAI APIキーの設定
# openai_api_key = os.getenv("OPENAI_API_KEY")

# if not openai_api_key:
#     raise ValueError("Error: OpenAI API key is not set")

# # OpenAIの設定
# client = OpenAI(api_key=openai_api_key)

# # プロンプトテンプレートの設定
# prompt_template = PromptTemplate(
#     input_variables=["user_message", "conversation_history"],
#     template="""
#     あなたは親切なアシスタントです。以下はユーザーからの会話履歴と最新のメッセージです。
#     会話履歴: {conversation_history}
#     ユーザー: {user_message}
#     アシスタント:
#     """
# )

# def get_conversation_history(user_id):
#     # ダミーデータを返す
#     return "ユーザー: 友人への良いギフトのアイデアは何ですか？\nAI: いくつかのギフトの提案があります:"

# def process_message(user_id, user_message, conversation_history):
#     prompt = prompt_template.format(user_message=user_message, conversation_history=conversation_history)
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "あなたは親切なアシスタントです。"},
#             {"role": "user", "content": conversation_history},
#             {"role": "user", "content": user_message}
#         ],
#         max_tokens=150
#     )
#     return response.choices[0].message.content.strip()

# def extract_keywords(gpt_response, gender=None):
#     # 名詞を抽出する正規表現
#     noun_pattern = re.compile(r'\b\w+\b')
#     keywords = []
    
#     for line in gpt_response.split('\n'):
#         words = noun_pattern.findall(line)
#         for word in words:
#             if word:  # 単語が存在する場合
#                 formatted_keyword = word + " プレゼント" + (" " + gender if gender else "")
#                 keywords.append(formatted_keyword)
                
#     # 重複を削除しつつ、適切なキーワードを抽出
#     unique_keywords = list(set(keywords))
#     print(f"Extracted keywords: {unique_keywords}")  # デバッグ用ログ
#     return unique_keywords

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
    あなたは親切なアシスタントです。以下はユーザーからの会話履歴と最新のメッセージです。
    会話履歴: {conversation_history}
    ユーザー: {user_message}
    アシスタント:
    """
)

# プロンプトテンプレート for keyword extraction
keyword_extraction_template = PromptTemplate(
    input_variables=["response"],
    template="""
    以下の文章から、関連するキーワードを抽出してください。各提案について3つの重要な名詞を抽出し、それぞれのキーワードを空白で区切って出力してください。
    例1: (美味しいスイーツやお菓子の詰め合わせ) -> スイーツ お菓子 詰め合わせ
    例2: (おしゃれな文房具セット) -> おしゃれ 文房具 セット
    
    文章:
    {response}
    """
)

def get_conversation_history(user_id):
    # ダミーデータを返す
    return "ユーザー: 友人への良いギフトのアイデアは何ですか？\nAI: いくつかのギフトの提案があります:"

def process_message(user_id, user_message, conversation_history):
    prompt = prompt_template.format(user_message=user_message, conversation_history=conversation_history)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたは親切なアシスタントです。"},
            {"role": "user", "content": conversation_history},
            {"role": "user", "content": user_message}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

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
        keyword = keyword.lstrip('1234567890. ')  # 見出し番号とスペースを削除
        formatted_keyword = keyword + " プレゼント" + (" " + gender if gender else "")
        formatted_keywords.append(formatted_keyword)
    
    return formatted_keywords