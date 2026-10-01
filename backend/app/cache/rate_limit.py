from fastapi import HTTPException,status
from app.cache.redis import redis_client

RATE_LIMIT=10
WINDOW_SECONDS=60

async def check_rate_limit(user_id:int):
    key=f"rate_limit:user:{user_id}"

    current_count=await redis_client.incr(key)
    if current_count==1:
        await redis_client.expire(
            key,WINDOW_SECONDS
        )

    if current_count > RATE_LIMIT:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,detail="Rate limit exceeded ,Try again later")