FROM python:3.12.7-slim-bookworm AS build
WORKDIR /app

# Poetry の設定ファイルをコピーして依存関係リストを生成・インストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

ADD https://github.com/benbjohnson/litestream/releases/download/v0.3.13/litestream-v0.3.13-linux-amd64.deb /tmp/litestream.deb

RUN dpkg -i /tmp/litestream.deb && \
    rm /tmp/litestream.deb

FROM python:3.12.7-slim-bookworm AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# pip でインストールされたライブラリと実行ファイル（例：streamlit）をコピー
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=build /usr/local/bin /usr/local/bin
COPY --from=build /usr/bin/litestream /usr/local/bin/litestream
ENV PATH=$PATH:/usr/local/bin

COPY litestream.yml /etc/litestream.yml

# for debian/ubuntu-based images
RUN apt-get update -y && apt-get install -y ca-certificates libgomp1 fuse3 sqlite3 jq curl && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY litefs.yml /etc/litefs.yml
# LiteFS のバイナリをコピー
COPY --from=flyio/litefs:0.5 /usr/local/bin/litefs /usr/local/bin/litefs
# アプリケーションソースコードもコピー
COPY app.py .
COPY data data
COPY src src
COPY run.sh .
RUN chmod +x ./run.sh

EXPOSE 8080 20202
CMD ["./run.sh"]
