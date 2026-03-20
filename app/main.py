from fastapi import FastAPI
from datetime import datetime, timezone
import os

app = FastAPI(title="Mini Cloud Deployment Platform")

APP_VERSION = os.getenv("APP_VERSION", "dev")
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")


@app.get("/")
def read_root():
    return {
        "message": "Hello from the Mini Cloud Deployment Platform",
        "service": "mini-cloud-deployment-platform",
        "environment": ENVIRONMENT,
        "version": APP_VERSION
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp_utc": datetime.now(timezone.utc).isoformat()
    }


@app.get("/version")
def version():
    return {
        "version": APP_VERSION,
        "environment": ENVIRONMENT
    }


@app.get("/env")
def environment_info():
    return {
        "environment": ENVIRONMENT,
        "python_env": os.getenv("PYTHON_ENV", "not-set")
    }