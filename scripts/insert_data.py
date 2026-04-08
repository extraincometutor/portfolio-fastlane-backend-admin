import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import uuid

# Mongo URL
MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://doadmin:0ZeKg6Q321x79G4t@db-mongodb-fra1-25085-01-421631d0.mongo.ondigitalocean.com/"
)

client = AsyncIOMotorClient(MONGO_URL)
db = client["portfolio_db"]
collection = db["summary_data"]

async def insert_summary_data():

    capital = 100000.00

    months = [
        {
            "month": "Nov",
            "year": 2025,
            "opening": 100000.00,
            "net_profit": 29237.39,
            "closing": 129237.39,
            "roi": 29.2,
            "total_trades": 24,
            "profit_trades": 17,
            "win_rate": 70.8,
            "max_drawdown": 0,
            "profit_factor": 4.7,
            "profit": 37061.42,
            "loss": -7824.02,
            "loss_ratio": -21.1,
            "summary_id": "SUM-" + uuid.uuid4().hex[:8].upper()
        },
        {
            "month": "Dec",
            "year": 2025,
            "opening": 129237.39,
            "net_profit": 30740.84,
            "closing": 159978.23,
            "roi": 23.8,
            "total_trades": 19,
            "profit_trades": 12,
            "win_rate": 63.2,
            "max_drawdown": 0,
            "profit_factor": 4.9,
            "profit": 38601.53,
            "loss": -7860.69,
            "loss_ratio": -20.4,
            "summary_id": "SUM-" + uuid.uuid4().hex[:8].upper()
        },
        {
            "month": "Jan",
            "year": 2026,
            "opening": 159978.23,
            "net_profit": 50254.81,
            "closing": 210233.04,
            "roi": 31.4,
            "total_trades": 24,
            "profit_trades": 16,
            "win_rate": 66.7,
            "max_drawdown": 0,
            "profit_factor": 2.9,
            "profit": 76255.44,
            "loss": -26000.63,
            "loss_ratio": -34.1,
            "summary_id": "SUM-" + uuid.uuid4().hex[:8].upper()
        },
        {
            "month": "Feb",
            "year": 2026,
            "opening": 210233.04,
            "net_profit": 64543.82,
            "closing": 274776.85,
            "roi": 30.7,
            "total_trades": 30,
            "profit_trades": 20,
            "win_rate": 66.7,
            "max_drawdown": 0,
            "profit_factor": 2.6,
            "profit": 104511.28,
            "loss": -39967.47,
            "loss_ratio": -38.2,
            "summary_id": "SUM-" + uuid.uuid4().hex[:8].upper()
        },
        {
            "month": "Mar",
            "year": 2026,
            "opening": 274776.85,
            "net_profit": 82812.29,
            "closing": 357589.15,
            "roi": 30.1,
            "total_trades": 21,
            "profit_trades": 15,
            "win_rate": 71.4,
            "max_drawdown": 0,
            "profit_factor": 7.3,
            "profit": 95972.72,
            "loss": -13160.43,
            "loss_ratio": -13.7,
            "summary_id": "SUM-" + uuid.uuid4().hex[:8].upper()
        }
    ]

    # =========================
    # TOTALS CALCULATION
    # =========================
    total_profit = sum(m["net_profit"] for m in months)
    total_trades = sum(m["total_trades"] for m in months)
    profit_trades = sum(m["profit_trades"] for m in months)

    win_rate = (profit_trades / total_trades * 100) if total_trades else 0

    totals = {
        "total_profit": total_profit,
        "total_trades": total_trades,
        "profit_trades": profit_trades,
        "win_rate": round(win_rate, 2)
    }

    closing_balance = months[-1]["closing"]

    # =========================
    # FINAL DOCUMENT
    # =========================
    data = {
        "account_id": "portfolio1",
        "capital": capital,
        "months": months,
        "totals": totals,
        "closing_balance": closing_balance,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }

    result = await collection.insert_one(data)
    print("Inserted ID:", result.inserted_id)


# RUN
if __name__ == "__main__":
    asyncio.run(insert_summary_data())