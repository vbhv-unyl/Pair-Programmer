# app/main.py
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db
from app.routers.health import router as health_router
from app.routers.rooms import router as rooms_router
from app.routers.ws import router as ws_router
from app.routers.autocomplete import router as autocomplete_router

app = FastAPI(title="Sharecode API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(health_router, prefix="/api")
app.include_router(rooms_router, prefix="/api")
app.include_router(ws_router, prefix="/api")
app.include_router(autocomplete_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "ShareCode Backend. Try GET /api/health"}
