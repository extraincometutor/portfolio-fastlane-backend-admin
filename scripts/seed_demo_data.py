import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta, timezone

# Use the MONGO_URL provided in the request
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://doadmin:0ZeKg6Q321x79G4t@db-mongodb-fra1-25085-01-421631d0.mongo.ondigitalocean.com/")

client = AsyncIOMotorClient(MONGO_URL)
db = client["portfolio_db"]

async def insert_demo_data():
    account_id = "ID-984251"
    strategy_id = "ALPHA-QUANT-V4"

    print(f"Connecting to MongoDB at {MONGO_URL.split('@')[-1]}...")

    # 1. Account Info
    account = {
        "account_id": account_id,
        "name": "Institutional Portfolio",
        "starting_capital": 50000.00,
        "ending_capital": 69300.00,
        "net_return_percent": 38.60,
        "monthly_avg_return": 2.80,
        "benchmark_return": 1.20,
        "currency": "USD",
        "created_at": datetime(2024, 1, 1)
    }
    await db["accounts"].update_one({"account_id": account_id}, {"$set": account}, upsert=True)
    print("✓ Account updated")

    # 2. Strategy Info
    strategy = {
        "strategy_id": strategy_id,
        "name": "Alpha Quant Crypto (V4)",
        "version": "V4",
        "description": "Net of Fees & Slippage",
        "created_at": datetime(2024, 1, 1)
    }
    await db["strategies"].update_one({"strategy_id": strategy_id}, {"$set": strategy}, upsert=True)
    print("✓ Strategy updated")

    # 3. Monthly Performance Breakdown Matrix (2025)
    performance = {
        "account_id": account_id,
        "year": 2025,
        "monthly_returns": {
            "JAN": 3.2, "FEB": 2.1, "MAR": -1.4, "APR": 4.8,
            "MAY": 3.1, "JUN": -0.5, "JUL": 2.9, "AUG": 5.2,
            "SEP": -2.1, "OCT": 6.4, "NOV": 4.5, "DEC": 3.8
        },
        "quarterly_returns": {
            "Q1": 3.9, "Q2": 7.4, "Q3": 6.0, "Q4": 14.7
        },
        "ytd_return": 38.6
    }
    await db["monthly_performance"].update_one(
        {"account_id": account_id, "year": 2025},
        {"$set": performance},
        upsert=True
    )
    print("✓ Performance Matrix updated")

    # 4. Risk Analysis Metrics
    risk = {
        "account_id": account_id,
        "max_drawdown": 8.4,
        "sharpe_ratio": 2.1,
        "win_rate": 64.0,
        "profit_factor": 1.85,
        "recovery_time_days": 14,
        "alpha_vs_benchmark": 12.4,
        "volatility_ann": 15.2,
        "calculated_at": datetime.now(timezone.utc)
    }
    await db["risk_metrics"].update_one({"account_id": account_id}, {"$set": risk}, upsert=True)
    print("✓ Risk Analysis updated")

    # 5. Equity Curve (Simplified path for 2025)
    # Clear old data for a clean curve
    await db["equity_curve"].delete_many({"account_id": account_id})
    equity_points = []
    base_equity = 50000.0
    monthly_performance = [3.2, 2.1, -1.4, 4.8, 3.1, -0.5, 2.9, 5.2, -2.1, 6.4, 4.5, 3.8]
    
    current_equity = base_equity
    for i, perf in enumerate(monthly_performance):
        current_equity *= (1 + perf/100)
        equity_points.append({
            "account_id": account_id,
            "timestamp": datetime(2025, i+1, 1),
            "equity": round(current_equity, 2),
            "drawdown": 0.0 # Simplified
        })
    
    await db["equity_curve"].insert_many(equity_points)
    print(f"✓ Equity Curve updated ({len(equity_points)} points)")

    # 6. Recent Trade History (Latest 10)
    await db["trades"].delete_many({"account_id": account_id})
    trades = [
        {"date": datetime(2025, 12, 28), "asset": "BTC/USD", "type": "LONG", "entry": 98420.50, "exit": 102150.00, "size": 1.5, "fees": 150.40, "pnl_pct": 3.79},
        {"date": datetime(2025, 12, 15), "asset": "ETH/USD", "type": "SHORT", "entry": 4820.00, "exit": 4950.50, "size": 25.0, "fees": 120.50, "pnl_pct": -2.71},
        {"date": datetime(2025, 11, 22), "asset": "SOL/USD", "type": "LONG", "entry": 245.10, "exit": 268.40, "size": 500.0, "fees": 134.20, "pnl_pct": 9.51},
        {"date": datetime(2025, 11, 5), "asset": "BTC/USD", "type": "LONG", "entry": 92100.00, "exit": 95450.00, "size": 0.8, "fees": 76.36, "pnl_pct": 3.64},
        {"date": datetime(2025, 10, 18), "asset": "ETH/USD", "type": "LONG", "entry": 3950.00, "exit": 4210.00, "size": 15.0, "fees": 63.15, "pnl_pct": 6.58},
        {"date": datetime(2025, 9, 30), "asset": "SOL/USD", "type": "SHORT", "entry": 210.50, "exit": 222.10, "size": 800.0, "fees": 177.68, "pnl_pct": -5.51},
        {"date": datetime(2025, 8, 12), "asset": "BTC/USD", "type": "LONG", "entry": 78400.00, "exit": 82900.00, "size": 1.2, "fees": 99.48, "pnl_pct": 5.74},
        {"date": datetime(2025, 7, 25), "asset": "ETH/USD", "type": "LONG", "entry": 3200.00, "exit": 3450.00, "size": 40.0, "fees": 138.00, "pnl_pct": 7.81},
        {"date": datetime(2025, 6, 14), "asset": "BTC/USD", "type": "SHORT", "entry": 69800.00, "exit": 71200.00, "size": 0.5, "fees": 35.60, "pnl_pct": -2.01},
        {"date": datetime(2025, 5, 2), "asset": "SOL/USD", "type": "LONG", "entry": 165.00, "exit": 182.50, "size": 1000.0, "fees": 182.50, "pnl_pct": 10.61},
    ]

    trade_docs = []
    for t in trades:
        net_pnl_val = 0
        if t["type"] == "LONG":
            net_pnl_val = (t["exit"] - t["entry"]) * t["size"] - t["fees"]
        else:
            net_pnl_val = (t["entry"] - t["exit"]) * t["size"] - t["fees"]
        
        trade_docs.append({
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
            "net_pnl_percent": t["pnl_pct"]
        })
    
    await db["trades"].insert_many(trade_docs)
    print(f"✓ Trade History updated ({len(trade_docs)} trades)")

    print("\nDemo data insertion complete!")

if __name__ == "__main__":
    asyncio.run(insert_demo_data())
