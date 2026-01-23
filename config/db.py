import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGOURI")
MONGO_DB = os.getenv("MONGO_DB")

print("MONGO_URI:", MONGO_URI)
print("MONGO_DB:", MONGO_DB)

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]