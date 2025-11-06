terraform {
  required_providers {
    aws = { source = "hashicorp/aws" }
  }
  backend "s3" {}
}

provider "aws" {
  region = var.aws_region
}

data "terraform_remote_state" "bypass_transformer" {
  backend = "s3"
  config = {
    bucket = var.bypass_state_bucket_name
    key    = "terraform/bypass-transformer/state.tfstate"
    region = var.aws_region
  }
}

output "transformer_ec2_public_ip" {
  value = data.terraform_remote_state.bypass_transformer.outputs.ec2_public_ip
}

