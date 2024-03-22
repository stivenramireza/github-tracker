data "aws_s3_object" "github_tracker_dependencies" {
  bucket = var.lambda_bucket
  key    = "github-tracker-dependencies.zip"
}

resource "aws_lambda_layer_version" "github_tracker_dependencies" {
  layer_name = "github-tracker-dependencies"
  compatible_runtimes = ["python3.12"]
  s3_bucket = var.lambda_bucket
  s3_key = "github-tracker-dependencies.zip"
}
