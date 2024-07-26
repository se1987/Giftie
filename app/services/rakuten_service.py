import os
import requests
import logging

# ログの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 環境変数から楽天APIのアプリIDを取得
rakuten_app_id = os.getenv('RAKUTEN_APP_ID')

if not rakuten_app_id:
    raise ValueError("Error: Rakuten App ID is not set")

def search_products(keywords, budget):
    # 楽天APIのエンドポイント
    endpoint = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"

    # 各キーワードについて検索を行い、結果を収集
    results = []
    for keyword in keywords:
        print(f"Searching with keyword: {keyword}")  # キーワードのログ出力
        min_price = max(int(budget * 0.8), 1)  # 最小値が1円未満にならないように調整
        max_price = int(budget * 1.2)  # 最大値をbudgetの120%に設定
        params = {
            'applicationId': rakuten_app_id,
            'keyword': keyword,
            'sort': 'standard',  # 標準ソート
            'hits': 5,  # 検索結果の最大取得件数
            'minPrice': min_price,  # 最小価格
            'maxPrice': max_price,  # 最大価格
            'format': 'json',
            'formatVersion': 2
        }
        logger.info(f"Sending request to Rakuten API with params: {params}")  # リクエストの詳細をログに記録
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Received response: {data}")  # レスポンスの詳細をログに記録
        if 'Items' in data:
            for item in data['Items']:
                item_price = item['itemPrice']
                item_name = item['itemName']
                item_url = item['itemUrl']
                results.append(f"{item_name} - {item_price}円 - {item_url}")
                break  # 各キーワードで最初の1商品だけ追加

    return results