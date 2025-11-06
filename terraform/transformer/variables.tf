variable "aws_region" {
  default = "us-east-1"
}

variable "bypass_state_bucket_name" {
  description = "Bucket de State do Terraform"
  type        = string
  default     = "bypass-state-bucket"
}
