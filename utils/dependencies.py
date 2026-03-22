from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from bson import ObjectId
from config.db import db
from utils.jwt_handler import SECRET_KEY, ALGORITHM

security = HTTPBearer()

usersCollection = db["users"]


async def get_current_user(token=Depends(security)):

    try:

        payload = jwt.decode(
            token.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = await usersCollection.find_one(
            {"_id": ObjectId(user_id)}
        )

        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    