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
