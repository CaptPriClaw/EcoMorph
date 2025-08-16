# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- CHANGED: Use relative imports ---
from .database import engine
from . import models
from .routes import auth, users, waste, product, marketplace, points
# -------------------------------------

# This line creates all the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EcoMorph API",
    description="The backend for the EcoMorph upcycling marketplace.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include Routers ---
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(waste.router)
app.include_router(product.router)
app.include_router(marketplace.router)
app.include_router(points.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the EcoMorph API! ♻️"}