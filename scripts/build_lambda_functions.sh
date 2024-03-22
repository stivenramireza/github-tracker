BUCKET_NAME=github-tracker-lambda-stivenramireza

AUTHORIZER_LAMBDA_PACKAGE=authorizer.zip
zip -r ./dist/$AUTHORIZER_LAMBDA_PACKAGE src
aws s3 cp ./dist/$AUTHORIZER_LAMBDA_PACKAGE s3://$BUCKET_NAME/$AUTHORIZER_LAMBDA_PACKAGE

GET_METRICS_LAMBDA_PACKAGE=get-metrics.zip
zip -r ./dist/$GET_METRICS_LAMBDA_PACKAGE src
aws s3 cp ./dist/$GET_METRICS_LAMBDA_PACKAGE s3://$BUCKET_NAME/$GET_METRICS_LAMBDA_PACKAGE

POST_GITHUB_WEBHOOK_LAMBDA_PACKAGE=post-github-webhook.zip
zip -r ./dist/$POST_GITHUB_WEBHOOK_LAMBDA_PACKAGE src
aws s3 cp ./dist/$POST_GITHUB_WEBHOOK_LAMBDA_PACKAGE s3://$BUCKET_NAME/$POST_GITHUB_WEBHOOK_LAMBDA_PACKAGE