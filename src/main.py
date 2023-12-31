from google.cloud import bigquery, pubsub_v1
from google.api_core.exceptions import Forbidden, BadRequest, GoogleAPICallError
import logging
import base64
import json
import os

def bq_pp(event, context):
    print(f'Received event: {event}')  
    logging.info(f'Received event: {event}')

    try:
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        message_dict = json.loads(pubsub_message)

        project_id = message_dict.get('project_id')
        dataset_id = message_dict.get('dataset_id')
        table_id = message_dict.get('table_id')

        # Get environment variables
        pp_table = os.getenv('PP_TABLE')
        pubsub_topic = os.getenv('PUBSUB_TOPIC')

        if not all([project_id, dataset_id, table_id, pp_table, pubsub_topic]):
            print('Error: Missing necessary parameters in the message or environment variables.')
            return

        bigquery_uri = f'{project_id}.{dataset_id}.{table_id}'

        print(f'BigQuery URI: {bigquery_uri}')
        logging.info(f'BigQuery URI: {bigquery_uri}')

        client = bigquery.Client(project=project_id)

        # Define the query
        query = f"""
        CREATE OR REPLACE TABLE `{project_id}.{dataset_id}.{pp_table}`
        AS 
        SELECT 
            TIMESTAMP_ADD(
                TIMESTAMP(
                    PARSE_DATETIME(
                        '%Y/%m/%d %I:%M:%S %p', 
                        CASE
                            WHEN t.datetime NOT LIKE '20%/%' THEN t.measurement_name
                            WHEN t.measurement_name LIKE '20%/%' THEN t.measurement_name
                            ELSE t.datetime
                        END
                    )
                ),
                INTERVAL CAST(t.millis AS INT64) MILLISECOND
            ) AS datetime,
            CASE
                WHEN t.datetime NOT LIKE '20%/%' THEN t.datetime
                WHEN t.measurement_name LIKE '20%/%' THEN t.datetime
                ELSE t.measurement_name
            END AS measurement_name,
            CAST(t.measurement_value AS FLOAT64) AS measurement_value,
            t.measurement_status
        FROM `{bigquery_uri}` t
        ORDER BY datetime;
        """
        # Run the query
        query_job = client.query(query)
        query_job.result()  # Wait for the job to finish

        # Code to publish to PubSub Topic
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, pubsub_topic)  # Use the variable here

        message = {
            'project_id': project_id,
            'dataset_id': dataset_id,
            'table_id' : pp_table,  # Use the same variable here
        }
        
        publish_message = publisher.publish(topic_path, json.dumps(message).encode('utf-8'))
        publish_message.result()
        
    except Forbidden as e:
        print(f'Forbidden error occurred: {str(e)}. Please check the Cloud Function has necessary permissions.')
        raise e
    except BadRequest as e:
        print(f'Bad request error occurred: {str(e)}. Please check the query and the table.')
        raise e
    except GoogleAPICallError as e:
        print(f'Google API Call error occurred: {str(e)}. Please check the API request.')
        raise e
    except Exception as e:
        print(f'An unexpected error occurred: {str(e)}')
        raise e
