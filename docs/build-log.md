# Mini Cloud Deployment Platform - Build Log

This document records the chronological steps taken while building the platform.

The goal is to make the entire setup reproducible on a new machine.

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

Committed initial project structure and documentation.

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

Service was tested via:

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

This confirmed Docker Engine and WSL integration were functioning correctly.

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
docker run --rm -p 8000:8000 -e APP_VERSION=local-docker -e ENVIRONMENT=docker mini-cloud-deployment-platform:local
~~~

This confirmed:

- container networking works
- environment variables work
- the service runs correctly inside a container

Commit:

~~~text
feat: containerize FastAPI demo application
~~~

---

# Current Status

Completed so far:

- repository initialized
- README created
- FastAPI demo service implemented
- local Python environment tested
- Docker installed and verified
- application containerized and tested locally

---

# Next Steps

Planned next phases:

1. Terraform remote state setup (S3 + DynamoDB)
2. Amazon ECR container registry
3. ECS Fargate service deployment
4. Application Load Balancer
5. CI/CD pipeline with GitHub Actions