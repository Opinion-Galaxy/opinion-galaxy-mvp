# Opinion-Galaxy

## 概要

国民が中立な意見を反映し、意見のトレンドをトラッキングするための、政治意見の可視化および選挙予測アプリケーション

### 説明

https://zenn.dev/edegp/articles/f9be4f4f19814f

## デモ

https://opinion-galaxy-591561871703.asia-northeast1.run.app


## Develop

### フロントエンド
```
poetry install
poetry run streamlit run app.py
```

### 本番環境と同様の環境構築
```
docker build . -t opinion-galaxy  --platform linux/amd64 -f Dockerfile.dev

docker run --privileged -it --platform linux/amd64 -e FIREBASE_API_KEY="your-api-key" -v /path/to/database:/var/lib/litefs -p 8080:8080 -p 20202:20202 -t opinion-galaxy
```

### ダミーデータの作成
`dataset/create_dummy_data.ipynb`を実行