from google.cloud import bigquery, pubsub_v1
import logging
from google.api_core.exceptions import NotFound, Forbidden
import base64
import json

def bq_pp(event, context):
    print(f'Received event: {event}')  
    logging.info(f'Received event: {event}')

    try:
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        message_dict = json.loads(pubsub_message)

        project_id = message_dict.get('project_id')
        dataset_id = message_dict.get('dataset_id')
        table_id = message_dict.get('table_id')

        bigquery_uri = f'{project_id}:{dataset_id}.{table_id}'
        print(f'BigQuery URI: {bigquery_uri}')
        logging.info(f'BigQuery URI: {bigquery_uri}')

        #client = bigquery.Client(project=project_id)

    except Forbidden as e:
        print(f'Error occurred: {str(e)}. Please check the Cloud Function has necessary permissions.')
        raise