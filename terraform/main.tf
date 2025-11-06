# minimal_lambda.tf
terraform {
  required_providers {
    aws = { source = "hashicorp/aws" }
  }
}

provider "aws" {
  region = var.aws_region
}

# Create a ZIP package of the Lambda function
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = "${path.module}/lambda_function.zip"
}

resource "aws_lambda_function" "lambda_function" {
  function_name = var.function_name
  filename      = data.archive_file.lambda_zip.output_path
  
  # Format: "filename.function_name"
  # - "lambda_function" = your Python file (lambda_function.py)
  # - "lambda_handler" = the function in that file to call
  handler       = var.lambda_handler
  
  role          = "arn:aws:iam::039590066154:role/LabRole"
  runtime       = "python3.13"

  # Optional but recommended
  description = "Processes incoming data files"
  timeout     = 60
  memory_size = 128
}

