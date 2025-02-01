FROM python:3.12-slim-bookworm as build
WORKDIR /app

# Poetry の設定ファイルをコピーして依存関係リストを生成・インストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

FROM python:3.12-slim-bookworm as runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# pip でインストールされたライブラリと実行ファイル（例：streamlit）をコピー
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=build /usr/local/bin /usr/local/bin
# アプリケーションソースコードもコピー
COPY app.py .
COPY data data
COPY src src
COPY run.sh .

EXPOSE 8501

USER root
CMD ["./run.sh"]