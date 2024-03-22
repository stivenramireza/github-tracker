terraform {
  backend "s3" {
    bucket = "github-tracker-stivenramireza"
    key    = "terraform.tfstate"
    region = "us-east-2"
  }
}

provider "aws" {
  region = "us-east-2"
}

module "iam" {
  source = "./iam"
}

module "s3" {
  source = "./s3"
}

module "compute" {
  source                  = "./compute"
  lambda_bucket           = module.s3.lambda_bucket
  repo_collector_role_arn = module.iam.repo_collector_role_arn
  subnet_ids              = ["subnet-092c95fe466201281", "subnet-0e34b6fb7a9fcab8e", "subnet-0902b3b3cee677559"]
}
