# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth  
from app.routers import aggregated_news
from app.routers import original_content
from app.routers import superadmin
from app.models import User, Profile

app = FastAPI(
    title="Ensight API",
    description="Backend for Ensight — Module 1",
    version="1.0.0",
)

# CORS settings
origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(aggregated_news.router)
app.include_router(original_content.router)
app.include_router(superadmin.router) 

@app.get("/")
def root():
    return {"message": "Ensight backend is up and running 🚀"}
