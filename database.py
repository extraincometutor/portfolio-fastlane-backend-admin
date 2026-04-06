from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://doadmin:0ZeKg6Q321x79G4t@db-mongodb-fra1-25085-01-421631d0.mongo.ondigitalocean.com/")

client = AsyncIOMotorClient(MONGO_URL)
db = client["portfolio_db"]

accounts_collection = db["accounts"]
users_collection = db["users"]
summary_data_collection = db["summary_data"]
summary_trading_collection = db["summary_trading"]
