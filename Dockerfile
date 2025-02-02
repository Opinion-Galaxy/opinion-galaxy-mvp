FROM python:3.12-slim-bookworm as build
WORKDIR /app

# Poetry の設定ファイルをコピーして依存関係リストを生成・インストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

ADD https://github.com/benbjohnson/litestream/releases/download/v0.3.13/litestream-v0.3.13-linux-amd64.deb /tmp/litestream.deb

RUN dpkg -i /tmp/litestream.deb && \
    rm /tmp/litestream.deb

FROM python:3.12-slim-bookworm as runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

ENV LITEFS_FILE=/data/database.db
ENV LITEFS_HTTP_ADDR=0.0.0.0:2020

# pip でインストールされたライブラリと実行ファイル（例：streamlit）をコピー
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

COPY litestream.yml /etc/litestream.yml

# for debian/ubuntu-based images
RUN apt-get update -y && apt-get install -y ca-certificates fuse3 sqlite3 jq curl iproute2 hostname && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY litefs.yml /etc/litefs.yml
# LiteFS のバイナリをコピー
COPY --from=flyio/litefs:0.5 /usr/local/bin/litefs /usr/local/bin/litefs
# アプリケーションソースコードもコピー
COPY app.py .
COPY data data
COPY src src
COPY run.sh .

EXPOSE 8080 2020
RUN chmod +x ./run.sh
CMD ["./run.sh"]