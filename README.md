# SW-CW-BQ-PP Cloud Function

<br>

Welcome to `sw-cf-bq-pp`, a repository that plays a pivotal role in the ACEP SW Data Pipeline. It is tasked with reshaping the data post-initial validation, ensuring that it is in an optimal format for querying within BigQuery.

To see how this repository contributes to the grand scheme of things, please navigate to the [ACEP SW Data Pipeline Overview](https://github.com/acep-uaf/sw-stack) repository.

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

Deploy the Cloud Function with the provided shell script:

```bash
./eiedeploy.sh
```

This script wraps the following `gcloud` command:

```bash
 #!/bin/bash

 # Source the .env file
 source eiedeploy.env

 # Deploy the function
 gcloud functions deploy sw-cf-bq-pp \
   --$GEN2 \
   --runtime=$RUNTIME \
   --region=$REGION \
   --service-account=$SERVICE_ACCOUNT \
   --source=$SOURCE \
   --entry-point=$ENTRY_POINT \
   --memory=$MEMORY \
   --timeout=$TIMEOUT \
   --trigger-topic=$TRIGGER_TOPIC \
   --set-env-vars PP_TABLE=$PP_TABLE,PUBSUB_TOPIC=$PUBSUB_TOPIC
```
### .env File Configuration
 
 Before deploying the Cloud Function, ensure that the `eiedeploy.env` file contains the necessary environment variables, as the deployment script sources this file. This file should define values for:
 
 ```bash
   GEN2=<value>
   RUNTIME=<value>
   REGION=<value>
   SERVICE_ACCOUNT=<value>
   SOURCE=<value>
   ENTRY_POINT=<value>
   MEMORY=<value>
   TIMEOUT=<value>
   TRIGGER_TOPIC=<value>
   PP_TABLE=<value>
   PUBSUB_TOPIC=<value>
  ```
 Replace `<value>` with the appropriate values for your deployment.

### Environment Variable Descriptions
 
  Below are descriptions for each environment variable used in the deployment script:
 
  - **GEN2**=`<value>`:
    - Description: Specifies the generation of the Cloud Function to deploy.  For example: `gen2` when you intend to deploy a second generation Google Cloud Function.
 
  - **RUNTIME**=`<value>`:
    - Description: Specifies the runtime environment in which the Cloud Function executes. For example: `python311` for Python 3.11.
 
  - **REGION**=`<value>`:
    - Description: The Google Cloud region where the Cloud Function will be deployed and run. Example values are `us-west1`, `europe-west1`, etc.
 
  - **SERVICE_ACCOUNT**=`<value>`:
    - Description: The service account under which the Cloud Function will run. This defines the permissions that the Cloud Function has at deployment.
 
  - **SOURCE**=`<value>`:
    - Description: Path to the source code of the Cloud Function. Typically, this points to a directory containing all the necessary files for the function.
 
  - **ENTRY_POINT**=`<value>`:
    - Description: Specifies the name of the function or method within the source code to be executed when the Cloud Function is triggered.
 
  - **MEMORY**=`<value>`:
    - Description: The amount of memory to allocate for the Cloud Function. This is denoted in megabytes, e.g., `16384MB`.
 
  - **TIMEOUT**=`<value>`:
    - Description: The maximum duration the Cloud Function is allowed to run before it is terminated. Expressed in seconds, e.g., `540s`.
 
  - **TRIGGER_TOPIC**=`<value>`:
    - Description: The Google Cloud topic under which the Cloud Function is subscribed.

  - **PP_TABLE**=`<value>`:
    - Description: The Post Processed Google BigQuery table that is created.
 
  - **PUBSUB_TOPIC**=`<value>`:
    - Description: The name of the Pub/Sub topic to which the Cloud Function publishes messages.
 
  Set each `<value>` in the `eiedeploy.env` file appropriately before deploying the Cloud Function. **Note:** For security reasons, do not cheeck the `eiedeploy.env` with values set  into a public repository such as github.

## Dependencies
The function relies on the following packages, as outlined in the `requirements.txt` file:
- google-cloud-bigquery
- google-cloud-storage
- google-cloud-pubsub

### Conclusion

---

The `sw-cf-bq-pp` repository is an integral component of the [ACEP SW Data Pipeline](https://github.com/acep-uaf/sw-stack). As a Cloud Function written in Python, it's primarily focused on reshaping and optimizing data for querying within Google's BigQuery service. This optimization is executed post-initial validation, ensuring the data is aptly structured for the subsequent stages.

Leveraging the synergy between Google BigQuery and Pub/Sub, this repository serves as a robust intermediary, dynamically transforming data upon the receipt of Pub/Sub messages. The fine-tuning this Cloud Function offers goes a long way in guaranteeing the precision and structure of data queries, which in turn elevates the overall efficiency and efficacy of the entire data pipeline.

We cordially invite the open-source community to delve into the depths of this repository, grasp its functionalities, and perhaps contribute to its enhancement. For a comprehensive understanding of licensing, we direct you to the [LICENSE](https://github.com/acep-uaf/sw-cf-bq-pp/blob/main/LICENSE) file in the repository's root.

Your exploration and engagement with this solution are highly valued. We're optimistic that integrating this functionality will vastly enrich your data transformation processes within the Google Cloud Platform.

---

