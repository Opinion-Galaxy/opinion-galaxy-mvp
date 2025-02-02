#!bin/sh

TOKEN=$(curl -s -H "Metadata-Flavor: Google" \
  "http://metadata.google.internal//computeMetadata/v1/instance/service-accounts/default/token" | jq -r '.access_token')

echo $TOKEN

PROJECT_ID=$(curl -s -H "Metadata-Flavor: Google" \
  "http://metadata.google.internal/computeMetadata/v1/project/project-id")

echo $PROJECT_ID

NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
ONE_minute_AGO=$(date -u -d '-1 minute' +"%Y-%m-%dT%H:%M:%SZ")

export PODS =$(curl -s -H "Authorization: Bearer ${TOKEN}" \
  "https://monitoring.googleapis.com/v3/projects/${PROJECT_ID}/timeSeries?filter=metric.type%3D%22run.googleapis.com/container/instance_count%22&interval.startTime=${ONE_HOUR_AGO}&interval.endTime=${NOW}")

echo "Pods: $PODS"

litefs run -- streamlit run app.py --server.port 8080