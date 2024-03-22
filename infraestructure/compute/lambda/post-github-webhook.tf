data "aws_s3_object" "post_github_webhook" {
  bucket = var.lambda_bucket
  key    = "post-github-webhook.zip"
}

resource "aws_lambda_function" "post_github_webhook" {
  function_name    = "post-github-webhook"
  handler          = "src.functions.post_github_webhook.handler"
  runtime          = "python3.12"
  s3_bucket        = var.lambda_bucket
  timeout          = 300
  s3_key           = "post-github-webhook.zip"
  role             = var.repo_collector_role_arn
  source_code_hash = data.aws_s3_object.get_metrics.version_id
  layers           = [aws_lambda_layer_version.github_tracker_dependencies.arn]

  vpc_config {
    security_group_ids = var.security_groups_ids
    subnet_ids         = var.subnet_ids
  }

  environment {
    variables = {
      DB_HOST     = "github-tracker.cjygis626apo.us-east-2.rds.amazonaws.com"
      DB_PORT     = "5432"
      DB_USER     = "stivenramireza"
      DB_PASSWORD = "rds!db-4a17b183-e653-4743-a595-288d88b7e0d3"
      DB_NAME     = "postgres"
    }
  }
}

output "post_github_webhook_invoke_arn" {
  value = aws_lambda_function.post_github_webhook.invoke_arn
}

output "post_github_webhook_lambda_name" {
  value = aws_lambda_function.post_github_webhook.function_name
}
