import boto3

# 設定
collection_id = "my-face-collection"
bucket = "rekognitionstack-rekognitionimagebucketc049fbb2-f2scpvz3ieys"
image_key = "face1.jpg"
external_image_id = "player1"

rekognition = boto3.client("rekognition", region_name="ap-northeast-1")

# コレクションの存在チェック & なければ作成
def ensure_collection_exists():
    try:
        rekognition.describe_collection(CollectionId=collection_id)
        print(f"✅ コレクション '{collection_id}' は既に存在します")
    except rekognition.exceptions.ResourceNotFoundException:
        rekognition.create_collection(CollectionId=collection_id)
        print(f"📦 コレクション '{collection_id}' を作成しました")

# 顔登録処理
def index_face():
    response = rekognition.index_faces(
        CollectionId=collection_id,
        Image={"S3Object": {"Bucket": bucket, "Name": image_key}},
        ExternalImageId=external_image_id,
        DetectionAttributes=["DEFAULT"]
    )

    if response['FaceRecords']:
        print(f"✅ 顔を登録しました: FaceId = {response['FaceRecords'][0]['Face']['FaceId']}")
    else:
        print("⚠️ 顔が検出されませんでした")

if __name__ == "__main__":
    ensure_collection_exists()
    index_face()
