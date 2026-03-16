# Mini Cloud Deployment Platform

A small cloud deployment platform built with **Terraform, Docker, and AWS** that demonstrates how a containerized application can be deployed automatically using Infrastructure as Code and CI/CD.

This project simulates a simplified version of a modern cloud deployment workflow used in real engineering teams.

The goal of this project is to showcase practical cloud engineering skills including:

- Infrastructure as Code (Terraform)
- Containerization (Docker)
- Continuous Integration / Continuous Deployment (GitHub Actions)
- Container registry management (Amazon ECR)
- Container orchestration (Amazon ECS Fargate)
- Secure infrastructure design in AWS

---

# Architecture Overview

The platform deploys a containerized application to AWS using an automated pipeline.

High level flow:

1. Developer pushes code to GitHub
2. GitHub Actions builds the Docker image
3. The image is pushed to Amazon ECR
4. Terraform provisions AWS infrastructure
5. ECS Fargate runs the containerized application
6. Application is exposed through an Application Load Balancer

---

# Project Structure

mini-cloud-deployment-platform
│
├── app
│   └── Containerized demo application
│
├── terraform
│   └── Infrastructure as Code for AWS resources
│
├── .github
│   └── workflows
│       └── CI/CD pipeline definitions
│
├── docs
│   └── Project documentation and architecture overview
│
├── README.md
└── LICENSE

---

# Technology Stack

- **Terraform** — Infrastructure as Code
- **Docker** — Containerized application
- **GitHub Actions** — CI/CD pipeline
- **Amazon ECR** — Container registry
- **Amazon ECS (Fargate)** — Serverless container runtime
- **Application Load Balancer** — Public access to service

---

# Key Concepts Demonstrated

This project demonstrates several important cloud engineering concepts.

### Infrastructure as Code

All AWS resources are provisioned using Terraform rather than manually through the AWS console.

### Containerized Application Deployment

The application is packaged into a Docker container and deployed through ECS.

### CI/CD Pipeline

GitHub Actions automatically builds and deploys the application whenever code is pushed to the repository.

### Cloud Architecture

The platform demonstrates how multiple AWS services integrate to run a production-style workload.

---

# Why This Project

This project was built as part of my cloud engineering portfolio to demonstrate hands-on experience with:

- AWS infrastructure
- Terraform workflows
- Container deployments
- CI/CD automation

It represents a simplified deployment platform similar to what many engineering teams use internally to deploy services.

---

# Author

Selim Çelem

AWS Certified Cloud Practitioner  
GitHub: https://github.com/selimcelem