import boto3

collection_id = "my-face-collection"
bucket = "rekognitionstack-rekognitionimagebucketc049fbb2-f2scpvz3ieys"
image_key = "game1.jpg"  # 試合中などの検索対象画像

rekognition = boto3.client("rekognition", region_name="ap-northeast-1")

def search_face():
    response = rekognition.search_faces_by_image(
        CollectionId=collection_id,
        Image={"S3Object": {"Bucket": bucket, "Name": image_key}},
        MaxFaces=3,
        FaceMatchThreshold=85
    )

    if not response['FaceMatches']:
        print("❌ 一致する顔が見つかりませんでした")
    else:
        print("✅ 一致した顔：")
        for match in response['FaceMatches']:
            print(f"- ExternalImageId: {match['Face']['ExternalImageId']}, 類似度: {match['Similarity']:.2f}%")

if __name__ == "__main__":
    print(f"🔍 画像 `{image_key}` から顔を検索中...")
    search_face()
