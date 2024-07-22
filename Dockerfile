
# ベースイメージとしてPythonを使用
FROM python:3.9

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係のインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコピー
COPY . .

# 環境変数の設定（必要に応じて）
ENV FLASK_ENV=development

# Flaskアプリケーションの起動
CMD ["python", "app/app.py"]

