# app/__init__.py

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# データベースインスタンスの作成
db = SQLAlchemy()

def create_app():
    # Flaskアプリケーションのインスタンスを作成
    app = Flask(__name__)
    
    # CORSの設定
    CORS(app)

    # 設定の読み込み
    app.config.from_object('config.Config')  # 'config.Config' を適切な設定ファイルに変更

    # データベースの初期化
    db.init_app(app)

    # ルートやブループリントの登録
    from .routes import main_bp  # .routes はあなたのモジュールに合わせて変更
    app.register_blueprint(main_bp)

    return app


