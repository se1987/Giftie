
# import os
# import requests
# from dotenv import load_dotenv

# # 環境変数をロード
# load_dotenv()

# RAKUTEN_APP_ID = os.getenv("RAKUTEN_APP_ID")
# RAKUTEN_ENDPOINT = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"

# def search_products(keywords):
#     all_products = []
#     for keyword in keywords:
#         params = {
#             "applicationId": RAKUTEN_APP_ID,
#             "keyword": keyword,
#             "hits": 5,
#         }
#         response = requests.get(RAKUTEN_ENDPOINT, params=params)
#         response_data = response.json()
        
#         if "Items" in response_data:
#             products = [f"{item['Item']['itemName']} - {item['Item']['itemPrice']}円 - {item['Item']['itemUrl']}" for item in response_data['Items']]
#             all_products.extend(products)
#     if not all_products:
#         return ["No products found"]
#     return all_products

import os
import requests

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
        params = {
            'applicationId': rakuten_app_id,
            'keyword': keyword,
            'sort': 'standard',  # 標準ソート
            'hits': 5,  # 検索結果の最大取得件数
            'minPrice': 1,  # 最小価格
            'maxPrice': budget,  # 最大価格
            'format': 'json',
            'formatVersion': 2
        }
        response = requests.get(endpoint, params=params)
        data = response.json()
        if 'Items' in data:
            for item in data['Items']:
                item_price = item['itemPrice']
                item_name = item['itemName']
                item_url = item['itemUrl']
                results.append(f"{item_name} - {item_price}円 - {item_url}")
                break  # 各キーワードで最初の1商品だけ追加

    return results