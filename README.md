# Giftie (ギフティー)
A LINE chatbot that recommends gifts using ChatGPT and external APIs.

# Task Manager for pre-engineer
**TEAM A: sayoko, mikiko, nanako,ami @section8_teamA**

## 概要
Giftie（ギフティー）は、LINEを通じてユーザーに最適なプレゼントを提案するチャットボットアプリです。ユーザーがLINE上でプレゼントに関する質問を送信すると、ChatGPTがユーザーのリクエストを理解し、楽天市場APIを使用して関連する商品を検索し、最適なプレゼントを提案します。

## 技術スタック
#### フロントエンド
> LINE Messaging API
#### バックエンド
> Python (Flask)
#### データベース
> MySQL
#### LLM
> ChatGPT API
#### 外部知識参照(RAG)
> 楽天商品検索API
#### 使用したプラットフォーム、サービス
> Docker, GitHub

## 役割分担
- LINE Messaging API：sayoko
- MySQL：mikiko
- ChatGPT API：nanako
- 楽天商品検索API：ami
- Docker, GitHub：sayoko + nanako

## ドキュメント
- API設計書：swagger
- ナッレジ共有：notion

## こだわったポイント
・基本的な要件を満たし、かつ、チーム開発における流れを体験すること
・今まで行ってきたことを他言語で再現すること
・こまめな情報共有や知見の共有をすること

## 課題の要件の達成/未達成
|評価|要件|備考|
|---|----|---|
| o |OpenAI API は、APIサーバを経由して利用|  |
| o |外部知識参照(RAG)|楽天商品検索API|
| o |メインのユーザはスマホ|  |
| o |クライアントの指定| LINE |
| △ | ユーザの過去の対話内容をふまえた回答|未:提案済URLの保存|
| x |特定の話題以外は回答できないという制限|  |
