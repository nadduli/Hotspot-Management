#!/usr/bin/python3
"""
Main Application Entry Point
"""

from fastapi import FastAPI
from app.core.config import get_settings


settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    description="API for managing hotspots",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/", tags=["Home"])
async def read_root():
    return {
        "message": "Welcome to the Hotspot Management API!",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health", tags=["Home"])
async def health_check():
    return {"status": "healthy"}
