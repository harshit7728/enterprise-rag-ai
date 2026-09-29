from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.api.schemas.auth import (
    RegisterRequest,TokenResponse,LoginRequest
)

from app.core.security import verify_password


from app.core.security import (
    create_access_token,hash_password
)

from app.db.models import User



router=APIRouter(prefix="/auth",tags=["Authentication"])


@router.post("/register",response_model=TokenResponse)
async def register(request:RegisterRequest,db:AsyncSession=Depends(get_db)):
    result=await db.execute(
        select(User).where(User.email==request.email)
    )
    existing_user=result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=409,detail="Email already registered"
        )
    
    user=User(email=request.email,password_hash=hash_password(request.password))

    db.add(user)
    await db.commit()
    await db.refresh(user)

    token=create_access_token(user.id)
    return TokenResponse(access_token=token)




@router.post("/login")
async def login(request:LoginRequest,db:AsyncSession=Depends(get_db)):
    result=await db.execute(select(User).where(User.email==request.email))
    user=result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401,detail="Invalid Credentials"
        )
    
    
    valid_password=verify_password(request.password,user.password_hash)

    if not valid_password:
        raise HTTPException(
            status_code=401,detail="Invalid Credentials"
        )

    token=create_access_token(user.id)

    return TokenResponse(access_token=token)


