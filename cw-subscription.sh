gcloud pubsub subscriptions create sw-cw-bq-pp-subscription \
  --topic=sw-cf-bq-pp-dt-rs \
  --push-endpoint="https://workflowexecutions.googleapis.com/v1/projects/acep-ext-eielson-2021/locations/us-west1/workflows/sw-cw-bq-pp/executions" \
  --push-auth-service-account=untar-ingest@acep-ext-eielson-2021.iam.gserviceaccount.com
