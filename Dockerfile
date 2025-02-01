FROM python:3.12-slim-bookworm as build
WORKDIR /app

# Poetry のインストール（キャッシュ無効化）
RUN pip install --no-cache-dir poetry

# Poetry の設定ファイルをコピーして依存関係リストを生成・インストール
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt -o requirements.txt --without-hashes && \
    pip install --no-cache-dir -r requirements.txt && \
    pip uninstall -y poetry && \
    rm -rf /root/.cache/pip

FROM python:3.12-slim-bookworm as runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# pip でインストールされたライブラリと実行ファイル（例：streamlit）をコピー
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=build /usr/local/bin /usr/local/bin
# アプリケーションソースコードもコピー
COPY --from=build /app /app

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]