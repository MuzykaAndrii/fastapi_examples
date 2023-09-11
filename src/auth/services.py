from typing import Optional

from jwt import (
    decode,
    ExpiredSignatureError,
    InvalidTokenError,
)
from config import TOKEN_AUDIENCE, AUTH_SECRET
from auth.dal import UserDAL
from auth.models import (
    User,
)

from fastapi import HTTPException
from typing import Optional
import jwt


async def get_user_by_jwt(token: str) -> Optional[User]:
    user_id = get_user_id_by_jwt(token)

    if not user_id:
        return None
    
    user = await UserDAL.get_by_id(user_id)

    if not user:
        return None
    
    return user




def get_user_id_by_jwt(token: str) -> Optional[int]:
    try:
        jwt_data = jwt.decode(
            token,
            key=AUTH_SECRET,
            algorithms=['HS256'],
            audience=TOKEN_AUDIENCE,
        )
        user_id = int(jwt_data.get('sub')[0])
        return user_id
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="JWT token has expired")
    
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="JWT token is invalid")
    
    except (ValueError, TypeError, IndexError):
        raise HTTPException(status_code=401, detail="Invalid user ID in JWT token")
    
    except Exception:
        raise HTTPException(status_code=500)



def user_is_admin(user: User) -> bool:
    if user.role_id == 2 or user.is_superuser:
        return True
    return False