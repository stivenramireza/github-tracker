BUCKET_NAME=github-tracker-lambda-stivenramireza

aws s3 cp ./dist/authorizer.zip s3://${BUCKET_NAME}/authorizer.zip 
aws s3 cp ./dist/get-metrics.zip s3://${BUCKET_NAME}/get-metrics.zip 
aws s3 cp ./dist/post-github-webhook.zip s3://${BUCKET_NAME}/post-github-webhook.zip
