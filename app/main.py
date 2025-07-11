# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import auth  
from app.routers import superadmin
from app.models import User, Profile
from app.routers import article
from app.routers import profile
from app.routers import resource
from app.routers import subscription
from app.routers import corporate



app = FastAPI(
    title="Ensight API",
    description="Backend for Ensight — Module 1",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="uploads"), name="static")
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
app.include_router(superadmin.router) 
app.include_router(article.router) 
app.include_router(profile.router)
app.include_router(resource.router)
app.include_router(subscription.router)
app.include_router(corporate.router) 


@app.get("/")
def root():
    return {"message": "Ensight backend is up and running 🚀"}
