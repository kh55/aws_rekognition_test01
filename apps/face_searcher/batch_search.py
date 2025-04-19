# AWS Rekognitionを使用して顔検索を行うバッチ処理スクリプト
import boto3
import csv

# AWSリソースの設定
collection_id = "my-face-collection"  # 顔コレクションのID
bucket = "rekognitionstack-rekognitionimagebucketc049fbb2-f2scpvz3ieys"  # S3バケット名
region = "ap-northeast-1"  # AWSリージョン

# AWSサービスのクライアントを初期化
rekognition = boto3.client("rekognition", region_name=region)
s3 = boto3.client("s3", region_name=region)

def list_images():
    """
    S3バケットから画像ファイルの一覧を取得する
    戻り値: 画像ファイルのキー（パス）のリスト
    """
    response = s3.list_objects_v2(Bucket=bucket)
    return [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].lower().endswith(('.jpg', '.jpeg', '.png'))]

def search_face(image_key):
    """
    指定された画像から顔を検索し、コレクション内で最も類似度の高い顔を探す
    引数:
        image_key: S3バケット内の画像ファイルのキー
    戻り値:
        tuple: (マッチした顔の外部ID, 類似度) または (None, None)
    """
    try:
        response = rekognition.search_faces_by_image(
            CollectionId=collection_id,
            Image={"S3Object": {"Bucket": bucket, "Name": image_key}},
            MaxFaces=1,
            FaceMatchThreshold=80
        )
        if response['FaceMatches']:
            return response['FaceMatches'][0]['Face']['ExternalImageId'], response['FaceMatches'][0]['Similarity']
        else:
            return None, None
    except Exception as e:
        print(f"❌ エラー: {image_key} → {e}")
        return None, None

def run_batch():
    """
    バッチ処理を実行する
    1. S3バケットから画像一覧を取得
    2. 各画像に対して顔検索を実行
    3. 結果をCSVファイルに出力
    """
    images = list_images()
    print(f"🔍 検索対象画像数: {len(images)}")
    
    with open("face_search_results.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Image", "MatchedExternalId", "Similarity"])

        for image_key in images:
            print(f"🔎 {image_key} を検索中...")
            match_id, similarity = search_face(image_key)
            if match_id:
                print(f"✅ {image_key} → {match_id} ({similarity:.2f}%)")
            else:
                print(f"❌ {image_key} → 一致なし")
            writer.writerow([image_key, match_id or "NotFound", f"{similarity:.2f}%" if similarity else "-"])

if __name__ == "__main__":
    run_batch()
