resource "aws_ecr_repository" "app" {
  name                 = "mini-cloud-deployment-platform"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}