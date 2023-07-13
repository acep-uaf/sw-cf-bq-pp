# SW-CW-BQ-PP Cloud Function

The `sw-cw-bq-pp` is a Cloud Function written in Python designed to process data in a BigQuery table. The function is triggered by a Pub/Sub topic and is responsible for processing data from a specified BigQuery table.

## Cloud Function

### Description

The gen 2 Cloud Function `bq_pp` is a Python function utilizing the `google.cloud.bigquery` library to interact with Google's BigQuery service. This function is initiated by an event from a Pub/Sub topic.

Upon receiving the event, the function decodes the base64-encoded data from the event payload, and loads the resulting JSON string into a Python dictionary. It extracts the `project_id`, `dataset_id`, and `table_id` from the message. If any of these values are missing, the function will log an error message and halt its execution.

Provided that all the necessary parameters are present, the function composes the BigQuery URI using the provided identifiers. After setting up a BigQuery client with the specified `project_id`, it prepares a SQL query. This query creates or replaces a table (`vtndpp`) in the specified dataset.

The query specifically reshapes the table's data by parsing dates, adding milliseconds to timestamps, recasting measurement values as floating-point numbers, and rearranging the order of the columns. It derives this new table from the table specified in the Pub/Sub message, and the query sorts the results by the `datetime` column.

The function attempts to execute the query using the BigQuery client and waits for the query to finish. If the query execution encounters issues such as Forbidden, BadRequest, or any Google API Call errors, the function will catch these exceptions and log the error messages accordingly.

Thus, the `bq_pp` function essentially acts as an intermediary that processes and transforms BigQuery data upon receiving a message from Pub/Sub. This functionality enables dynamic transformations and reshaping of data in BigQuery based on incoming Pub/Sub messages.

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