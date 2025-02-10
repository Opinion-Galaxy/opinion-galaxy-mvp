#!/bin/bash
# エラー発生時にエラーメッセージと行番号を出力して終了するハンドラ
set -euo pipefail
error_handler() {
  echo "エラーが発生しました。行番号: $1" >&2
  exit 1
}
trap 'error_handler $LINENO' ERR

rm -f /app/data/database/database.db

litestream restore -if-replica-exists -config /etc/litestream.yml /app/data/database/database.db
echo $(sqlite3 /app/data/database/database.db .tables)
python /app/export.py