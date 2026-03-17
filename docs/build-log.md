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

## Key design decision

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

# Next Steps

1. Configure Terraform remote backend (platform layer)
2. Create Amazon ECR repository
3. Deploy ECS Fargate service
4. Configure Application Load Balancer
5. Implement CI/CD pipeline (GitHub Actions)