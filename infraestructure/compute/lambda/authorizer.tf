data "aws_s3_object" "authorizer" {
  bucket = var.lambda_bucket
  key    = "authorizer.zip"
}

resource "aws_lambda_function" "authorizer" {
  function_name    = "authorizer"
  handler          = "src.functions.authorizer.handler"
  runtime          = "python3.12"
  s3_bucket        = var.lambda_bucket
  timeout          = 300
  s3_key           = "authorizer.zip"
  role             = var.repo_collector_role_arn
  source_code_hash = data.aws_s3_object.get_metrics.version_id
  layers           = [aws_lambda_layer_version.github_tracker_dependencies.arn]

  vpc_config {
    security_group_ids = var.security_groups_ids
    subnet_ids         = var.subnet_ids
  }

  environment {
    variables = {
      DEMO = "DEMO"
    }
  }
}

output "authorizer_invoke_arn" {
  value = aws_lambda_function.authorizer.invoke_arn
}

output "authorizer_lambda_name" {
  value = aws_lambda_function.authorizer.function_name
}
