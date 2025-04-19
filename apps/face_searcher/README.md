## apps/face\_searcher/README.md

# 🔍 顔検索スクリプト - face\_searcher

このスクリプトは、試合中などの画像から Amazon Rekognition により誰が写っているかを判定します。

---

## 📦 セットアップ

```bash
cd apps/face_searcher
python3 -m venv .venv  # または face_indexer の venv を使う
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 🔍 実行手順

1. 検索対象画像を S3 にアップロード

```bash
aws s3 cp game1.jpg s3://<作成したS3バケット名>/
```

2. スクリプト実行

```bash
python main.py
```

---

## 🔧 設定内容（main.py内）

- `collection_id`："my-face-collection"
- `bucket`：S3バケット名
- `image_key`：検索対象画像のファイル名
- `FaceMatchThreshold`：類似度しきい値（例：85）

---

## ✅ 出力例

```
🔍 画像 `game1.jpg` から顔を検索中...
✅ 一致した顔：
- ExternalImageId: player1, 類似度: 98.42%
```

---

## 🧠 補足

- 顔が検出されない場合は角度・明るさを変えて画像を追加登録しましょう
- 類似度が低い場合は `FaceMatchThreshold` を70程度に緩めてもOK

