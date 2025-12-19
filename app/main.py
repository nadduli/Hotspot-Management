#!/usr/bin/python3
"""
Main Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.db.init_db import init_db
from app.db.session import get_db


settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    description="API for managing hotspots",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
origins = [
    "http://localhost",
    "http://localhost:3000",  # React/Next.js default
    "http://localhost:5173",  # Vite default
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    async for db in get_db():
        await init_db(db)
        break

from app.api.v1.auth import router as auth_router
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])

from app.api.v1.users import router as users_router
app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])


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
