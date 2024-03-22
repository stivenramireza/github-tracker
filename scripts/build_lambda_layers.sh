python -m venv venv
source venv/bin/activate
pip install --upgrade -r requirements.txt

apt update -y && apt install zip -y
mkdir dist

BUCKET_NAME=github-tracker-lambda-stivenramireza

DEPENDENCIES_LAMBDA_LAYER_PACKAGE=github-tracker-dependencies.zip
zip -r ./dist/$DEPENDENCIES_LAMBDA_LAYER_PACKAGE venv
aws s3 cp ./dist/$DEPENDENCIES_LAMBDA_LAYER_PACKAGE s3://$BUCKET_NAME/$DEPENDENCIES_LAMBDA_LAYER_PACKAGE
