from fastapi import FastAPI
from app.core.config import settings
from app.cache.redis import redis_client
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router

app=FastAPI(title=settings.app_name,version="1.0.0")

app.include_router(auth_router)
app.include_router(users_router)

@app.get("/health")
async def health():

    return {
        "status":"ok",
        "service":settings.app_name
    }


@app.get("/redis/health")
async def redis_health_check():
    await redis_client.set("health_check","working",ex=60)

    value=await redis_client.get("health_check")
    return {
        "status":"ok",
        "redis":value
    }

