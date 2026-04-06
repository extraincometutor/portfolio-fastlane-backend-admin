import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
import random

MONGO_URL = "mongodb://localhost:27017" # Update if needed
client = AsyncIOMotorClient(MONGO_URL)
db = client["portfolio_db"]

async def seed():
    # 1. Create Account
    account_id = "ID-984251"
    account = {
        "account_id": account_id,
        "name": "Institutional Portfolio",
        "starting_capital": 50000.0,
        "currency": "USD",
        "created_at": datetime(2024, 12, 1)
    }
    await db["accounts"].update_one({"account_id": account_id}, {"$set": account}, upsert=True)

    # 2. Create Strategy
    strategy_id = "ALPHA-QUANT-V4"
    strategy = {
        "strategy_id": strategy_id,
        "name": "Alpha Quant Crypto (V4)",
        "version": "V4",
        "description": "Net of Fees & Slippage",
        "created_at": datetime(2024, 12, 1)
    }
    await db["strategies"].update_one({"strategy_id": strategy_id}, {"$set": strategy}, upsert=True)

    # 3. Create Sample Trades for 2025
    await db["trades"].delete_many({"account_id": account_id})
    
    trades = [
        {"date": datetime(2025, 12, 28), "asset": "BTC/USD", "type": "LONG", "entry": 98420.50, "exit": 102150.00, "size": 1.5, "fees": 150.40},
        {"date": datetime(2025, 12, 15), "asset": "ETH/USD", "type": "SHORT", "entry": 4820.00, "exit": 4950.50, "size": 25.0, "fees": 120.50},
        {"date": datetime(2025, 11, 22), "asset": "SOL/USD", "type": "LONG", "entry": 245.10, "exit": 268.40, "size": 500.0, "fees": 134.20},
        {"date": datetime(2025, 11, 5), "asset": "BTC/USD", "type": "LONG", "entry": 92100.00, "exit": 95450.00, "size": 0.8, "fees": 76.36},
        {"date": datetime(2025, 10, 18), "asset": "ETH/USD", "type": "LONG", "entry": 3950.00, "exit": 4210.00, "size": 15.0, "fees": 63.15},
        {"date": datetime(2025, 9, 30), "asset": "SOL/USD", "type": "SHORT", "entry": 210.50, "exit": 222.10, "size": 800.0, "fees": 177.68},
        {"date": datetime(2025, 8, 12), "asset": "BTC/USD", "type": "LONG", "entry": 78400.00, "exit": 82900.00, "size": 1.2, "fees": 99.48},
        {"date": datetime(2025, 7, 25), "asset": "ETH/USD", "type": "LONG", "entry": 3200.00, "exit": 3450.00, "size": 40.0, "fees": 138.00},
        {"date": datetime(2025, 6, 14), "asset": "BTC/USD", "type": "SHORT", "entry": 69800.00, "exit": 71200.00, "size": 0.5, "fees": 35.60},
        {"date": datetime(2025, 5, 2), "asset": "SOL/USD", "type": "LONG", "entry": 165.00, "exit": 182.50, "size": 1000.0, "fees": 182.50},
    ]

    for t in trades:
        net_pnl_val = 0
        if t["type"] == "LONG":
            net_pnl_val = (t["exit"] - t["entry"]) * t["size"] - t["fees"]
        else:
            net_pnl_val = (t["entry"] - t["exit"]) * t["size"] - t["fees"]
        
        net_percent = (net_pnl_val / (t["entry"] * t["size"])) * 100
        
        await db["trades"].insert_one({
            "account_id": account_id,
            "strategy_id": strategy_id,
            "asset": t["asset"],
            "type": t["type"],
            "entry_price": t["entry"],
            "exit_price": t["exit"],
            "size": t["size"],
            "fees": t["fees"],
            "opened_at": t["date"] - timedelta(days=2),
            "closed_at": t["date"],
            "net_pnl_value": round(net_pnl_val, 2),
            "net_pnl_percent": round(net_percent, 2)
        })

    print("Seed data inserted. Remember to run the analytics trigger to populate metrics!")

if __name__ == "__main__":
    asyncio.run(seed())
