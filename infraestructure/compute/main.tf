module "lambda" {
  source                  = "./lambda"
  lambda_bucket           = var.lambda_bucket
  repo_collector_role_arn = var.repo_collector_role_arn

  security_groups_ids = ["sg-0922a37827487a6ce"]
  subnet_ids          = var.subnet_ids
}
