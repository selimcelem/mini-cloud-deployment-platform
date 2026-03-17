terraform {
  backend "s3" {
    bucket         = "selimcelem-mini-cloud-platform-tfstate"
    key            = "platform/dev/terraform.tfstate"
    region         = "eu-central-1"
    dynamodb_table = "mini-cloud-platform-tf-locks"
    encrypt        = true
  }
}