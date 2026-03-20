# Mini Cloud Deployment Platform

A small cloud engineering portfolio project built with **Terraform, Docker, GitHub Actions, and AWS**.

This project demonstrates a simplified deployment platform for a containerized application using a production-style workflow:

- infrastructure provisioned with Terraform
- application packaged with Docker
- image stored in Amazon ECR
- application deployed on Amazon ECS Fargate
- traffic exposed through an Application Load Balancer
- deployments triggered automatically from GitHub Actions

The project is designed to be **reproducible from a fresh machine** and **cost-aware to destroy and rebuild**.

---

## What This Project Demonstrates

- Infrastructure as Code with Terraform
- Remote Terraform state in S3 with DynamoDB locking
- Docker-based application packaging
- CI/CD with GitHub Actions
- Container deployments with ECS Fargate
- Load balancing with ALB
- CloudWatch log visibility
- Least-privilege IAM for CI/CD
- ECR image lifecycle cleanup

---

## Architecture Overview

High-level deployment flow:

1. Developer pushes code to `main`
2. GitHub Actions builds the Docker image
3. GitHub Actions pushes the image to Amazon ECR
4. GitHub Actions forces a new ECS deployment
5. ECS Fargate pulls the latest image
6. The application is served through an Application Load Balancer

Terraform is used to provision and manage the AWS infrastructure for this workflow.

---

## Project Structure

~~~text
mini-cloud-deployment-platform
│
├── app
│   └── FastAPI demo application
│
├── terraform
│   ├── bootstrap
│   │   └── S3 backend + DynamoDB locking
│   └── platform
│       └── AWS application platform infrastructure
│
├── .github
│   └── workflows
│       └── deploy.yml
│
├── docs
│   ├── build-log.md
│   ├── iam
│   └── screenshots
│
├── README.md
└── LICENSE
~~~

---

## Prerequisites

Before using this project from a fresh machine, install and configure:

- Git
- Terraform
- AWS CLI
- Docker Desktop
- Python 3.x

You also need:

- an AWS account
- AWS credentials configured locally for Terraform and AWS CLI
- GitHub repository secrets configured for GitHub Actions

Recommended local verification commands:

~~~powershell
terraform version
aws --version
docker --version
python --version
~~~

---

## Before Running Terraform

Make sure AWS credentials are configured locally before using the Terraform commands.

Example verification:

~~~powershell
aws sts get-caller-identity
~~~

Also note:

- `terraform/bootstrap` creates the remote Terraform backend
- `terraform/platform` uses that backend for the actual platform resources
- GitHub Actions deployment requires repository secrets such as AWS credentials to already exist in the GitHub repo settings

---

## Terraform Layout

This project uses two Terraform layers:

### `terraform/bootstrap`
Creates the Terraform backend infrastructure:
- S3 bucket for remote state
- DynamoDB table for state locking

### `terraform/platform`
Creates the actual application platform:
- ECR repository
- ECS cluster
- ECS task definition
- ECS service
- ALB
- target group
- listener
- networking
- CloudWatch log group
- supporting resources

This split exists because the remote backend must be created before the main platform can use it.

---

## Rebuild from a Fresh Machine

Create the backend first:

~~~powershell
cd terraform\bootstrap
terraform init
terraform apply
~~~

Then create the platform:

~~~powershell
cd ..\platform
terraform init
terraform apply
~~~

Useful Terraform outputs after deployment include:
- `alb_dns_name`
- `ecr_repository_url`
- `ecs_cluster_name`
- `ecs_service_name`

---

## Clean Destroy Order

Destroy the platform first:

~~~powershell
cd terraform\platform
terraform destroy
~~~

Then destroy the backend last:

~~~powershell
cd ..\bootstrap
terraform init
terraform destroy
~~~

This order matters. If the backend is destroyed first, the platform layer loses access to its Terraform state and locking configuration.

---

## CI/CD

The GitHub Actions workflow in `.github/workflows/deploy.yml` performs the following on every push to `main`:

1. checkout repository
2. configure AWS credentials
3. authenticate to Amazon ECR
4. build Docker image from `app/`
5. push image to ECR
6. force new ECS deployment

This creates a working push-to-deploy flow for the application.

---

## Observability and Operations

The ECS service writes container logs to CloudWatch Logs.

Log group:

~~~text
/ecs/mini-cloud-deployment-platform
~~~

The project also includes:
- a custom least-privilege IAM policy for the GitHub Actions CI/CD user
- an ECR lifecycle policy to clean up older untagged images automatically

---

## Supporting Documentation

- Build log: `docs/build-log.md`
- CI/CD IAM policy: `docs/iam/github-actions-mini-cloud-deploy-policy.json`

---

## Why This Project

This project was built as part of my cloud engineering portfolio to demonstrate hands-on experience with:

- AWS infrastructure
- Terraform workflows
- container deployments
- CI/CD automation
- remote Terraform state management
- least-privilege IAM design
- CloudWatch log verification
- cost-aware rebuild and destroy workflows

It represents a simplified internal deployment workflow similar to what engineering teams use for containerized services.

---

## Author

Selim Çelem

AWS Certified Cloud Practitioner  
GitHub: https://github.com/selimcelem