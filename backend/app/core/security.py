
import jwt
from .config import settings

from datetime import datetime,timedelta,timezone
from fastapi  import Depends,HTTPException,status
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer

ACCESS_TOKEN_EXPIRE_MINUTES=60

from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

bearer_scheme=HTTPBearer()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(user_id:int)->str:
    expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload={
        "sub":str(user_id),"exp":expire
    }
    return jwt.encode(
        payload,settings.jwt_secret,algorithm=settings.jwt_algorithm
    )


def decode_access_token(credentials:HTTPAuthorizationCredentials=Depends(bearer_scheme))->int:
    try:
        payload=jwt.decode(credentials.credentials,settings.jwt_secret,algorithm=[settings.jwt_algorithm])
        user_id=payload.get("sub")
        if not user_id:
            raise ValueError
        return int(user_id)
    
    except Exception as e:
        raise HTTPException(status_code=401,detail="Invalid or expired token")



def get_current_user(credentials:HTTPAuthorizationCredentials=Depends(bearer_scheme))->int:
    token=credentials.credentials
    user_id=decode_access_token(token)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired token",headers={
            'www-Authenticate':'Bearer'
        })
    return user_id

