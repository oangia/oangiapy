gcloud functions deploy agent52 \
   --region=asia-southeast1 \
   --runtime=python313 \
   --source=. \
   --entry-point=hello_http \
   --trigger-http \
   --allow-unauthenticated