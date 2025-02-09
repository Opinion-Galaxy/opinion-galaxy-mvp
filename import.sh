#!/bin/bash
set -euo pipefail
error_handler() {
  echo "エラーが発生しました。行番号: $1" >&2
  exit 1
}
trap 'error_handler $LINENO' ERR

HOST="localhost"
PORT=20202

# タイムアウト（秒数）
TIMEOUT=30
START_TIME=$(date +%s)

# ポートが開くまでループしてチェック
while true; do
    if nc -z "$HOST" "$PORT"; then
        echo "ポート $PORT は開いています。litefs import を実行します。"
        break
    fi

    # タイムアウトの確認
    CURRENT_TIME=$(date +%s)
    ELAPSED_TIME=$((CURRENT_TIME - START_TIME))

    if [ "$ELAPSED_TIME" -ge "$TIMEOUT" ]; then
        echo "タイムアウト: ポート $PORT が $TIMEOUT 秒以内に開きませんでした。"
        exit 1
    fi

    echo "ポート $PORT を確認中..."
    sleep 2
done

litefs import -name litefs /app/data/database/database.db
litefs import -name litefs /app/data/database.db