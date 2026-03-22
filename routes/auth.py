from fastapi import APIRouter, HTTPException
from models.User import User
from models.Login import LoginUser
from config.db import db
from utils.jwt_handler import create_access_token
from passlib.context import CryptContext

router = APIRouter(prefix="/api/auth", tags=["Auth"])

usersCollection = db["users"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------------- PASSWORD UTILS ----------------
def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


# ---------------- REGISTER ----------------
@router.post("/register")
async def register(user: User):

    existing_user = await usersCollection.find_one({"email": user.email})

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    user_dict = user.dict()

    user_dict["password"] = hash_password(user_dict["password"])

    result = await usersCollection.insert_one(user_dict)

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id)
    }


# ---------------- LOGIN ----------------
@router.post("/login")
async def login(user: LoginUser):

    db_user = await usersCollection.find_one({"email": user.email})

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({
        "id": str(db_user["_id"])
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }