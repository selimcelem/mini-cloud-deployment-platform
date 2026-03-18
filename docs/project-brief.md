# Mini Cloud Deployment Platform - Project Brief

## Project Information

| Field | Value |
|------|------|
| Project Name | Mini Cloud Deployment Platform |
| Date | 2026 |
| Project Client | Self-initiated portfolio project |

---

## Project Overview

This project demonstrates a reproducible cloud deployment platform using Terraform, Docker, GitHub Actions CI/CD, AWS ECS Fargate, an Application Load Balancer, and CloudWatch logging.

The objective is to showcase:

- infrastructure-as-code practices  
- automated deployments  
- container orchestration  
- cost-aware cloud architecture  

---

## Goals & Objectives

- Demonstrate Infrastructure as Code with Terraform  
- Deploy containerized workloads on AWS ECS Fargate  
- Implement CI/CD pipeline using GitHub Actions  
- Provide reproducible infrastructure using remote Terraform state in S3  
- Maintain a cost-efficient architecture that can be destroyed and rebuilt on demand  

---

## Constraints & Assumptions

- Project remains beginner-friendly and reproducible  
- Expensive services such as RDS and NAT Gateway are avoided  
- Infrastructure must be destroyable to keep costs near $0  
- Single ECS task is sufficient for MVP  

---

## Project Scope

- Python FastAPI demo application  
- Docker containerization  
- Terraform infrastructure provisioning  
- Amazon ECS Fargate service  
- Application Load Balancer with health checks  
- GitHub Actions CI/CD pipeline  
- CloudWatch logging and observability  
- Architecture diagram and documentation  

---

## Target Audience

- Recruiters evaluating cloud/platform engineering skills  
- Junior Cloud Engineer roles  
- DevOps and Platform Engineering teams  

---

## Success Criteria

- Infrastructure deploys successfully with `terraform apply`  
- Application is reachable through the ALB endpoint  
- CI/CD pipeline builds and deploys automatically  
- Infrastructure can be destroyed and rebuilt reliably  
- Documentation clearly explains architecture and deployment workflow  

---

## Cost Strategy

Infrastructure runs only when needed.

After testing or demonstrations, the environment is removed using:

```powershell
terraform destroy
```