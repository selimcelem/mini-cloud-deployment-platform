# Mini Cloud Deployment Platform - Build Log

This document records the chronological steps taken while building the platform.

The goal is to make the entire setup reproducible on a new machine and understandable for recruiters and engineers reviewing the project.

---

# Step 1 - Repository Setup

Created a new repository:

~~~text
mini-cloud-deployment-platform
~~~

Initial repository structure:

~~~text
mini-cloud-deployment-platform
│
├── app
├── terraform
├── .github/workflows
├── docs
├── README.md
└── LICENSE
~~~

Purpose of this step:

- establish clean project structure
- separate concerns (application, infrastructure, CI/CD, docs)
- prepare for scalable architecture

Commit:

~~~text
feat: initialize repository structure and project documentation
~~~

---

# Step 2 - FastAPI Demo Application

A minimal FastAPI application was created to act as the containerized workload.

File structure:

~~~text
app/
├── main.py
├── requirements.txt
└── .gitignore
~~~

Endpoints implemented:

~~~text
/
health
version
env
~~~

Purpose of endpoints:

| Endpoint | Purpose |
|---|---|
| `/` | Verify service is running |
| `/health` | Health check for ALB and ECS |
| `/version` | Show deployment version |
| `/env` | Debug runtime environment |

The application can be run locally with:

~~~powershell
uvicorn main:app --reload
~~~

---

# Step 3 - Python Environment Setup

A Python virtual environment was created.

Commands used:

~~~powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r app\requirements.txt
~~~

Local API testing:

~~~powershell
cd app
uvicorn main:app --reload
~~~

Service tested via:

~~~text
http://127.0.0.1:8000
http://127.0.0.1:8000/health
http://127.0.0.1:8000/version
http://127.0.0.1:8000/env
~~~

---

# Step 4 - Docker Installation

Docker Desktop was installed.

Verification commands:

~~~powershell
docker --version
docker run hello-world
~~~

This confirmed:

- Docker Engine is installed
- container runtime works
- WSL integration is functioning

---

# Step 5 - Containerizing the Application

Docker files created:

~~~text
app/Dockerfile
app/.dockerignore
~~~

Docker image built with:

~~~powershell
docker build -t mini-cloud-deployment-platform:local .\app
~~~

Container run locally:

~~~powershell
docker run --rm -p 8000:8000 mini-cloud-deployment-platform:local
~~~

Environment variable test:

~~~powershell
docker run --rm -p 8000:8000 ^
-e APP_VERSION=local-docker ^
-e ENVIRONMENT=docker ^
mini-cloud-deployment-platform:local
~~~

This confirmed:

- container networking works
- environment variables are injected correctly
- application runs identically inside container

Commit:

~~~text
feat: containerize FastAPI demo application
~~~

---

# Step 6 - Terraform Project Structure

## What was created

Terraform directory structure:

~~~text
terraform/
├── bootstrap
└── platform
~~~

Commands used:

~~~powershell
mkdir .\terraform\bootstrap
mkdir .\terraform\platform
~~~

## Why this is needed

Terraform cannot use an S3 backend until the S3 bucket already exists.

To ensure full reproducibility from scratch, infrastructure is split into:

- bootstrap layer → creates backend resources (S3 + DynamoDB)
- platform layer → defines actual infrastructure (ECS, ALB, etc.)

## Design considerations

Separate Terraform into two stages:

1. Bootstrap (local state → creates backend)
2. Platform (remote state → uses backend)

This prevents circular dependencies and matches production setups.

Commit:

~~~text
chore: create terraform project structure (bootstrap + platform)
~~~

---

# Step 7 - Terraform Backend Bootstrap (Remote State Infrastructure)

## What was created

Terraform configuration for backend infrastructure.

Location:

~~~text
terraform/bootstrap
~~~

Files:

~~~text
providers.tf
backend_resources.tf
~~~

Resources provisioned:

- S3 bucket for Terraform state
- S3 versioning enabled
- S3 encryption enabled
- S3 public access blocked
- DynamoDB table for state locking

## Why this is needed

Terraform state is the source of truth for infrastructure.

Remote state:

- enables collaboration
- prevents concurrent writes (locking)
- allows CI/CD pipelines to run safely
- follows production best practices

## Commands used

~~~powershell
cd terraform\bootstrap
terraform init
terraform plan
terraform apply
~~~

## Result

Successfully created:

- Terraform state S3 bucket
- DynamoDB lock table

Verified via:

~~~powershell
aws s3 ls
aws dynamodb list-tables
~~~

---

# Step 8 - Configure Platform Terraform Remote Backend

## What was created

Terraform backend and provider configuration for the platform layer.

Location:

~~~text
terraform/platform
~~~

Files created:

~~~text
backend.tf
providers.tf
.terraform.lock.hcl
~~~

## Why this is needed

The platform layer must use remote Terraform state instead of local state.

This allows:

- centralized state storage in S3
- state locking with DynamoDB
- reproducible infrastructure changes from any machine
- safe future CI/CD execution

## Commands used

~~~powershell
notepad .\terraform\platform\backend.tf
notepad .\terraform\platform\providers.tf

cd .\terraform\platform
terraform init
terraform init -reconfigure
terraform init -upgrade
terraform providers
~~~

## Result

The platform Terraform layer is now configured to use:

- S3 remote state
- DynamoDB state locking
- pinned AWS provider version via `.terraform.lock.hcl`

---

# Step 9 - Amazon ECR and CI/CD Pipeline Setup

## What was created

Platform infrastructure and CI/CD components for container image delivery.

Location:

~~~text
terraform/platform
.github/workflows
docs
~~~

Files created or updated:

~~~text
terraform/platform/ecr.tf
.github/workflows/deploy.yml
docs/project-brief.md
~~~

AWS resources created:

- Amazon ECR repository: `mini-cloud-deployment-platform`
- IAM user: `github-actions-mini-cloud-platform`
  - used for GitHub Actions authentication
  - attached policies:
    - AmazonEC2ContainerRegistryFullAccess
    - AmazonECSFullAccess

CI/CD workflow created:

- GitHub Actions workflow to:
  - build Docker image
  - authenticate to AWS using repository secrets
  - push image to Amazon ECR on every push to `main`

## Why this is needed

The application must be packaged as a container image before it can be deployed to ECS.

Amazon ECR provides a private container registry for storing application images.

GitHub Actions automates the build and push process so deployments are repeatable and no manual Docker push is required.

A dedicated IAM user was created for CI/CD to allow GitHub Actions to securely interact with AWS services.

This follows the principle of least privilege by restricting access to only the required services (ECR and ECS).

## Commands used

~~~powershell
cd .\terraform\platform
terraform plan
terraform apply

aws ecr describe-repositories --repository-names mini-cloud-deployment-platform --region eu-central-1

git add .
git commit -m "feat: add ECR repository and CI/CD pipeline for Docker image deployment"
git push

aws ecr list-images --repository-name mini-cloud-deployment-platform --region eu-central-1
~~~

## Result

Successfully created the Amazon ECR repository and verified it in AWS.

Successfully ran the GitHub Actions workflow to:

- build the Docker image
- authenticate to AWS
- push the image to ECR

Verified that the repository now contains the `latest` image tag.

This confirms a complete CI/CD loop from code commit to container registry delivery.

---

# Step 10 - ECS Fargate Deployment with Application Load Balancer

## What was created

Runtime infrastructure to deploy and expose the application publicly on AWS.

Location:

~~~text
terraform/platform
~~~

Files created or updated:

~~~text
terraform/platform/networking.tf
terraform/platform/ecs.tf
terraform/platform/service.tf
~~~

AWS resources created:

- VPC
- 2 public subnets
- Internet Gateway
- public route table and associations
- security group for ALB
- security group for ECS tasks
- ECS cluster
- ECS task execution IAM role
- ECS task definition
- CloudWatch log group
- Application Load Balancer
- ALB target group
- ALB listener
- ECS service running on Fargate

## Why this is needed

The ECR image must be run as a managed container service in AWS.

ECS Fargate provides serverless container runtime without managing EC2 instances.

The Application Load Balancer provides a public entry point and routes traffic to healthy ECS tasks.

The networking layer allows the service to run in a dedicated VPC and receive internet traffic in a controlled way.

The ALB and ECS task security groups were separated so that:

- the ALB accepts public HTTP traffic on port 80
- ECS tasks accept application traffic on port 8000 only from the ALB

This follows a more realistic production-style network design.

## Commands used

~~~powershell
notepad .\terraform\platform\networking.tf
notepad .\terraform\platform\ecs.tf
notepad .\terraform\platform\service.tf

cd .\terraform\platform
terraform plan
terraform apply

aws elbv2 describe-load-balancers --names mini-cloud-platform-alb --region eu-central-1
aws elbv2 describe-target-health --target-group-arn arn:aws:elasticloadbalancing:eu-central-1:837649971999:targetgroup/mini-cloud-platform-tg/47e734ac7156e176 --region eu-central-1
~~~

## Result

Successfully deployed the FastAPI container to ECS Fargate.

Successfully exposed the application through an internet-facing Application Load Balancer.

Verified that:

- the ALB is active
- the ECS target became healthy after correcting the ALB security group
- the `/` endpoint works
- the `/health` endpoint works

This confirms a complete deployment path from container image in ECR to a publicly reachable service in AWS.

---

# Step 11 - Improve ECR Destroy Behavior

## What was changed

Updated the ECR repository configuration to support clean teardown.

File updated:

~~~text
terraform/platform/ecr.tf
~~~

Change made:

- added `force_delete = true` to the ECR repository resource

## Why this is needed

Terraform destroy initially failed because the ECR repository still contained images.

By default, AWS does not allow deletion of a non-empty ECR repository.

Setting `force_delete = true` ensures future destroy operations can remove the repository even when images are still present.

## Commands used

~~~powershell
notepad .\terraform\platform\ecr.tf
cd .\terraform\platform
terraform plan
~~~

## Result

The Terraform configuration now supports cleaner rebuild and destroy cycles for the platform infrastructure.

---

# Step 12 - Add Terraform Outputs for Key Platform Resources

## What was created

Terraform outputs for the most important platform values.

File created:

~~~text
terraform/platform/outputs.tf
~~~

Outputs added:

- `alb_dns_name`
- `ecr_repository_url`
- `ecs_cluster_name`
- `ecs_service_name`

## Why this is needed

Terraform outputs make the deployed environment easier to use and verify.

Instead of manually querying AWS, the most important values can now be retrieved directly from Terraform after deployment.

This improves reproducibility and makes the project easier to understand from a fresh machine.

## Commands used

~~~powershell
notepad .\terraform\platform\outputs.tf
cd .\terraform\platform
terraform apply
terraform output
~~~

## Result

The platform now exposes key deployment values directly through Terraform outputs, including the public ALB DNS name and core ECS/ECR resource identifiers.

---

## Step 13: GitHub Actions ECS deployment trigger

### What was created
The GitHub Actions workflow in `.github/workflows/deploy.yml` was extended to trigger an ECS service redeployment after pushing the Docker image to Amazon ECR.

### Why this is needed
The previous workflow stopped after pushing the image to ECR. That meant the new image existed in the registry, but ECS would keep running the old task until a manual redeploy was triggered. Adding `aws ecs update-service --force-new-deployment` closes that gap and enables true push-to-deploy behavior.

### Commands used
The workflow now runs this ECS deployment command after the image push:

    aws ecs update-service \
      --cluster mini-cloud-deployment-platform-cluster \
      --service mini-cloud-platform-service \
      --force-new-deployment

### Result
A push to `main` now:
1. builds the Docker image
2. pushes the image to Amazon ECR
3. forces ECS to deploy the new image automatically

---

## Step 14: Verify CloudWatch logging and operational visibility

### What was verified
The ECS service log group in CloudWatch was opened and the application log streams were inspected.

Log group used:

    /ecs/mini-cloud-deployment-platform

Recent log streams were present and contained live request logs from the running ECS tasks, including health check traffic and real application requests such as `GET / HTTP/1.1`.

### Why this is needed
Deployment success alone is not enough for a production-style platform. Basic observability is also required.

Verifying CloudWatch logs confirms that:
- ECS tasks can write application logs
- the logging configuration is working
- operational troubleshooting is possible after deployment

### Commands used
No local CLI commands were required for this verification step.

AWS Console path used:
- CloudWatch
- Logs
- Log groups
- `/ecs/mini-cloud-deployment-platform`

### Result
CloudWatch logging is working for the ECS service.

Recent log streams showed both ALB health check requests and real application requests, confirming that:
1. the application is running
2. the ALB is reaching the container
3. live requests are reaching the app
4. logs are being shipped successfully to CloudWatch

---

## Step 15: Reduce CI/CD IAM permissions and add ECR lifecycle policy

### What was changed
The GitHub Actions IAM user was moved away from broad AWS-managed permissions to a custom least-privilege policy.

Old policies removed:
- `AmazonEC2ContainerRegistryFullAccess`
- `AmazonECS_FullAccess`

New custom policy added:
- [`GitHubActionsMiniCloudDeployPolicy`](iam/github-actions-mini-cloud-deploy-policy.json)

This custom policy allows only the actions required for this project’s CI/CD workflow:
- authenticate to Amazon ECR
- push images to the `mini-cloud-deployment-platform` repository
- trigger redeployment of the `mini-cloud-platform-service` ECS service
- describe the ECS service during deployment operations

In addition, an Amazon ECR lifecycle policy was added to clean up old untagged images automatically.

Lifecycle rule added:
- keep only the 5 most recent untagged images
- expire older untagged images asynchronously

### Why this is needed
The original GitHub Actions IAM user permissions were broader than necessary for this project.

Reducing CI/CD IAM permissions to a custom least-privilege policy improves security and demonstrates better production-style IAM practice. It limits the CI user to only the AWS actions actually required for container delivery and ECS redeployment.

The ECR lifecycle policy is needed to prevent old untagged images from accumulating over time, which keeps the repository cleaner and supports better cost and hygiene control.

### Commands used
Local validation and AWS CLI commands used:

    Get-Content .\docs\iam\github-actions-mini-cloud-deploy-policy.json | ConvertFrom-Json

    aws iam create-policy `
      --policy-name GitHubActionsMiniCloudDeployPolicy `
      --policy-document file://docs/iam/github-actions-mini-cloud-deploy-policy.json

    aws iam attach-user-policy `
      --user-name github-actions-mini-cloud-platform `
      --policy-arn arn:aws:iam::837649971999:policy/GitHubActionsMiniCloudDeployPolicy

    aws iam list-attached-user-policies `
      --user-name github-actions-mini-cloud-platform

    aws ecr get-lifecycle-policy `
      --repository-name mini-cloud-deployment-platform `
      --region eu-central-1

### Result
The GitHub Actions deployment pipeline was successfully re-tested after removing the broad ECR and ECS managed policies, confirming that the custom least-privilege policy is sufficient for the workflow.

The ECR lifecycle policy is attached successfully. Cleanup of old untagged images will occur asynchronously after ECR evaluates the repository against the rule.

---

# Next Steps

1. Add cleanup and destroy instructions to the README
2. Reassess README accuracy now that ECS CI/CD is fully working
3. Add selected screenshots to `docs/screenshots/` for recruiter-facing proof