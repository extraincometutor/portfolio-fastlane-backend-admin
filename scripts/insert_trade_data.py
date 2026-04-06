import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone

MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://doadmin:0ZeKg6Q321x79G4t@db-mongodb-fra1-25085-01-421631d0.mongo.ondigitalocean.com/"
)

client = AsyncIOMotorClient(MONGO_URL)
db = client["portfolio_db"]
trading_summary_collection = db["summary_trading"]

async def insert_trades():
    trades = [
    # ===== EXISTING =====
    {"date": "2026-02-12", "type": "Sell", "symbol": "XAUUSD", "lot_size": 0.5, "open": 5064.09, "close": 4945.58, "swap": 0, "pnl": 5925.50},
    {"date": "2026-02-12", "type": "Sell", "symbol": "XAUUSD", "lot_size": 0.5, "open": 5075.46, "close": 4915.41, "swap": 0, "pnl": 8002.50},
    {"date": "2026-02-13", "type": "Sell", "symbol": "XAUUSD", "lot_size": 0.6, "open": 4980.91, "close": 4982.66, "swap": 0, "pnl": -105},
    {"date": "2026-02-13", "type": "Sell", "symbol": "XAUUSD", "lot_size": 0.6, "open": 4950.25, "close": 5015.63, "swap": 25.3, "pnl": -3897.50},
    {"date": "2026-02-16", "type": "Sell", "symbol": "XAUUSD", "lot_size": 0.7, "open": 4994.78, "close": 4910.45, "swap": 29.1, "pnl": 5932.20},
    {"date": "2026-02-16", "type": "Sell", "symbol": "XAUUSD", "lot_size": 0.7, "open": 5006.13, "close": 4917.18, "swap": 29.2, "pnl": 6255.70},
    {"date": "2026-02-17", "type": "Sell", "symbol": "XAUUSD", "lot_size": 1, "open": 4870.71, "close": 4890.02, "swap": 41.85, "pnl": -1889.15},

    # ===== ADDED (EURUSD) =====
    {"date": "2026-02-12", "type": "Sell", "symbol": "EURUSD", "lot_size": 1.0, "open": 1.18772, "close": 1.18653, "swap": 0, "pnl": 119.00},
    {"date": "2026-02-13", "type": "Sell", "symbol": "EURUSD", "lot_size": 1.0, "open": 1.18588, "close": 1.18679, "swap": 0, "pnl": -91.00},
    {"date": "2026-02-16", "type": "Sell", "symbol": "EURUSD", "lot_size": 1.0, "open": 1.18650, "close": 1.18542, "swap": 0, "pnl": 108.00},
    {"date": "2026-02-17", "type": "Buy", "symbol": "EURUSD", "lot_size": 1.0, "open": 1.18414, "close": 1.18108, "swap": 0, "pnl": -306.00},
    {"date": "2026-02-19", "type": "Sell", "symbol": "EURUSD", "lot_size": 1.0, "open": 1.18006, "close": 1.17672, "swap": 0, "pnl": 334.00},
    {"date": "2026-02-24", "type": "Sell", "symbol": "EURUSD", "lot_size": 1.0, "open": 1.17792, "close": 1.18053, "swap": 0, "pnl": -261.00},
    {"date": "2026-02-26", "type": "Buy", "symbol": "EURUSD", "lot_size": 1.0, "open": 1.17990, "close": 1.18193, "swap": 0, "pnl": 203.00},
    {"date": "2026-03-02", "type": "Sell", "symbol": "EURUSD", "lot_size": 1.0, "open": 1.17111, "close": 1.16811, "swap": 0, "pnl": 300.00},

    # ===== FIXED / EXTRA XAUUSD (missing ones) =====
    {"date": "2026-02-13", "type": "Sell", "symbol": "XAUUSD", "lot_size": 0.6, "open": 4980.91, "close": 5032.53, "swap": 0, "pnl": -3097.20},
    {"date": "2026-02-17", "type": "Sell", "symbol": "XAUUSD", "lot_size": 0.7, "open": 4870.71, "close": 4991.73, "swap": 29.25, "pnl": -8442.15},

    # ===== CONTINUE EXISTING =====
    {"date": "2026-02-18", "type": "Buy", "symbol": "XAUUSD", "lot_size": 1, "open": 4991.73, "close": 4995.8, "swap": -63.67, "pnl": 343.33},
    {"date": "2026-02-18", "type": "Buy", "symbol": "XAUUSD", "lot_size": 1, "open": 4975.51, "close": 4995.8, "swap": -63.72, "pnl": 1965.28},

    # ===== NEW LATE TRADES =====
    {"date": "2026-03-24", "type": "Buy", "symbol": "XAUUSD", "lot_size": 0.9, "open": 4347.25, "close": 4411.65, "swap": 0, "pnl": 5796.00},
    {"date": "2026-03-25", "type": "Buy", "symbol": "XAUUSD", "lot_size": 0.9, "open": 4563.20, "close": 4510.78, "swap": 0, "pnl": -4717.80},
    {"date": "2026-03-26", "type": "Buy", "symbol": "XAUUSD", "lot_size": 0.9, "open": 4535.72, "close": 4423.09, "swap": 0, "pnl": -10136.70},
    {"date": "2026-03-26", "type": "Sell", "symbol": "XAUUSD", "lot_size": 0.9, "open": 4438.31, "close": 4390.02, "swap": 0, "pnl": 4346.10}
]
    chart = [
    {"date": "2026-02-12", "return": 2.4},
    {"date": "2026-02-12", "return": 2.4},
    {"date": "2026-02-12", "return": 5.6},
    {"date": "2026-02-13", "return": 4.4},
    {"date": "2026-02-13", "return": 4.3},
    {"date": "2026-02-13", "return": 2.8},
    {"date": "2026-02-16", "return": 4.8},
    {"date": "2026-02-16", "return": 4.9},
    {"date": "2026-02-16", "return": 7.0},
    {"date": "2026-02-17", "return": 6.9},
    {"date": "2026-02-17", "return": 3.5},
    {"date": "2026-02-18", "return": 3.6},
    {"date": "2026-02-18", "return": 4.2},
    {"date": "2026-02-19", "return": 4.3},
    {"date": "2026-02-19", "return": 8.8},
    {"date": "2026-02-20", "return": 13.7},
    {"date": "2026-02-20", "return": 18.5},
    {"date": "2026-02-24", "return": 18.4},
    {"date": "2026-02-25", "return": 17.8},
    {"date": "2026-02-25", "return": 23.9},
    {"date": "2026-02-26", "return": 23.9},
    {"date": "2026-02-26", "return": 25.1},
    {"date": "2026-03-02", "return": 25.1},
    {"date": "2026-03-02", "return": 25.2},
    {"date": "2026-03-02", "return": 25.6},
    {"date": "2026-03-03", "return": 25.7},
    {"date": "2026-03-05", "return": 22.3},
    {"date": "2026-03-10", "return": 22.2},
    {"date": "2026-03-12", "return": 26.4},
    {"date": "2026-03-17", "return": 32.9},
    {"date": "2026-03-18", "return": 41.3},
    {"date": "2026-03-20", "return": 46.4},
    {"date": "2026-03-20", "return": 58.4},
    {"date": "2026-03-23", "return": 57.6},
    {"date": "2026-03-24", "return": 60.0},
    {"date": "2026-03-25", "return": 58.1},
    {"date": "2026-03-26", "return": 54.0},
    {"date": "2026-03-26", "return": 55.8}
]
    doc = {
        "trades": trades,
        "chart": chart,
        "summary": {
            "total_swap": -744.97,
            "total_pnl": 140297.03
        },
        "account_id":"portfolio1",
        "created_at": datetime.now(timezone.utc)
    }
    result = await trading_summary_collection.insert_one(doc)
    print("Inserted ID:", result.inserted_id)

if __name__ == "__main__":
    asyncio.run(insert_trades())