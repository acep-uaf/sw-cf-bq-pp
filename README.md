# SW-CW-BQ-PP Cloud Function

The `sw-cw-bq-pp` is a Cloud Function written in Python designed to process data in a BigQuery table. The function is triggered by a Pub/Sub topic and is responsible for processing data from a specified BigQuery table.

## Cloud Function

### Description

The gen 2 Cloud Function `sw-cw-bq-pp` is written in Python and uses the Google Cloud `bigquery` library to interact with BigQuery. The function is triggered by a Pub/Sub topic and is responsible for processing data from a specified BigQuery table. The function receives a message with the BigQuery table's project_id, dataset_id, and table_id, runs a processing query on the specified table, and saves the result in a new table.

### Deployment

Deploy this Cloud Function by running the `eiedeploy.sh` shell script:

```bash
./eiedeploy.sh
```


This script wraps the following `gcloud` command:

```bash
gcloud functions deploy sw-cw-bq-pp \
  --gen2 \
  --runtime=python311 \
  --region=us-west1 \
  --source=src \
  --entry-point=bq_pp \
  --memory 16384MB \
  --timeout 540s  \
  --trigger-topic sw-cf-bq-pp-dt-rs
```


### Dependencies

The Cloud Function's dependencies are listed in the `requirements.txt` file and include the `google-cloud-bigquery` package.