from fastapi import APIRouter,Depends

from app.core.security import decode_access_token

router = APIRouter(prefix="/users",tags=["Users"])

@router.get("/me")
async def get_me(user_id:int=Depends(decode_access_token)):
    return {
        "user_id":user_id
    }