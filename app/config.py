import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

# 環境変数を読み込む
load_dotenv()

# 環境変数からデータベースURLを取得
DATABASE_URL = os.getenv('DATABASE_URL')

# SQLAlchemyのインスタンスを作成
db = SQLAlchemy()

class Config:
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
