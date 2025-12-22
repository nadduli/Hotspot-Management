from fastapi import APIRouter
from .auth import router as auth_router


app = APIRouter()


# --- Authentication and User Management ---
app.include_router(auth_router)