gcloud functions deploy sw-cw-bq-pp \
  --gen2 \
  --runtime=python311 \
  --region=us-west1 \
  --source=src \
  --entry-point=bq_pp \
  --memory 16384MB \
  --timeout 540s  \
  --trigger-topic sw-cf-bq-pp-dt-rs \
  --set-env-vars PP_TABLE=vtndpp,PUBSUB_TOPIC=sw-cf-bq-pp-gr