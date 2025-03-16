#!/bin/bash
# エラー発生時にエラーメッセージと行番号を出力して終了するハンドラ
set -euo pipefail
error_handler() {
  echo "エラーが発生しました。行番号: $1" >&2
  exit 1
}
trap 'error_handler $LINENO' ERR

# rm -f /app/data/database/database.db

# TOKEN=$(curl -s -H "Metadata-Flavor: Google" \
#   "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token" | jq -r '.access_token')

# PROJECT_ID=$(curl -s -H "Metadata-Flavor: Google" \
#   "http://metadata.google.internal/computeMetadata/v1/project/project-id")

# NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
# ONE_MINUTE_AGO=$(date -u -d '-1 minute' +"%Y-%m-%dT%H:%M:%SZ")


# export PODS=$(curl -s -H "Authorization: Bearer ${TOKEN}" \
#   "https://monitoring.googleapis.com/v3/projects/${PROJECT_ID}/timeSeries?filter=metric.type%3D%22run.googleapis.com/container/instance_count%22&interval.startTime=${ONE_MINUTE_AGO}&interval.endTime=${NOW}" \
#   | jq -r '[.timeSeries[]? | (.points[0]?.value.int64Value // 0)] | map(tonumber) // 0 | add')

# echo "Pods: $PODS"

# litestream restore -if-replica-exists -config /etc/litestream.yml /app/data/database/database.db && \
echo $(sqlite3 /app/data/database/database.db .tables) && \
echo $(sqlite3 /app/data/database.db .tables) && \
litefs mount &
LITEFS_PID=$!

# 必要な他のプロセスもバックグラウンドで起動する例：
litestream replicate -exec 'streamlit run /app/app.py --server.port 8080' &
STREAMLIT_PID=$!

# すべてのバックグラウンドプロセスの終了を待つ
wait $LITEFS_PID $STREAMLIT_PID
