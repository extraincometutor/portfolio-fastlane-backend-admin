import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone

# Mongo URL
MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://doadmin:0ZeKg6Q321x79G4t@db-mongodb-fra1-25085-01-421631d0.mongo.ondigitalocean.com/"
)

client = AsyncIOMotorClient(MONGO_URL)
db = client["portfolio_db"]
trading_summary_collection = db["summary_data"]
async def insert_data():
    data = {
        "capital": 300000.00,
        "months": [
            {
                "month": "Feb",
                "opening": 300000.00,
                "net_profit": 93966.77,
                "closing": 393966.77,
                "roi": 31.30,
                "total_trades": 15,
                "winning_trades": 11,
                "win_rate": 73.30,
                "profit_amount": 101960.59,
                "loss_amount": -7993.82,
                "loss_ratio": -7.80
            },
            {
                "month": "Mar",
                "opening": 393966.77,
                "net_profit": 102538.57,
                "closing": 496505.34,
                "roi": 34.20,
                "total_trades": 11,
                "winning_trades": 7,
                "win_rate": 63.60,
                "profit_amount": 115586.99,
                "loss_amount": -13048.42,
                "loss_ratio": -11.30
            }
        ],
        "totals": {
            "opening": 300000.00,
            "net_profit": 196505.34,
            "closing": 496505.34,
            "roi": 65.50,
            "total_trades": 26,
            "winning_trades": 18,
            "win_rate": 69.20,
            "total_profit": 217547.58,
            "total_loss": -21042.24,
            "loss_ratio": -9.70
        },
        "created_at": datetime.now(timezone.utc)
    }

    result = await trading_summary_collection.insert_one(data)
    print("Inserted ID:", result.inserted_id)

if __name__ == "__main__":
    asyncio.run(insert_data())