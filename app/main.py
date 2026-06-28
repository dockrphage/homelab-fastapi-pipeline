import os
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
import redis
import psycopg2
import time
from typing import Dict, Any

app = FastAPI(
    title="Unified Pipeline Demo API",
    description="Demonstrating Build Once, Deploy Many Times",
    version="1.0.0"
)

# Environment-specific configurations
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "appdb")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
API_KEY = os.getenv("API_KEY", "dev-key")
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint showing environment information"""
    return {
        "environment": ENVIRONMENT,
        "service": "fastapi-unified-pipeline",
        "status": "healthy",
        "timestamp": time.time(),
        "configs": {
            "db_host": DB_HOST,
            "redis_host": REDIS_HOST,
            "log_level": LOG_LEVEL,
            "api_key_masked": f"{API_KEY[:4]}...{API_KEY[-4:]}"
        }
    }

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Simple health check endpoint"""
    return {"status": "healthy", "env": ENVIRONMENT}

@app.get("/readiness")
async def readiness_check() -> Dict[str, str]:
    """Readiness probe endpoint"""
    # Simulate checking database connectivity
    try:
        # If DB_HOST is set, we could test connection here
        return {"status": "ready", "checks": "all passed"}
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not ready", "error": str(e)}
        )

@app.get("/env")
async def show_env() -> Dict[str, str]:
    """Show all environment variables (for debugging)"""
    return {
        "ENVIRONMENT": ENVIRONMENT,
        "DB_HOST": DB_HOST,
        "DB_USER": DB_USER,
        "DB_NAME": DB_NAME,
        "REDIS_HOST": REDIS_HOST,
        "LOG_LEVEL": LOG_LEVEL,
        "API_KEY_MASKED": f"{API_KEY[:4]}...{API_KEY[-4:]}" if API_KEY else "not set"
    }
