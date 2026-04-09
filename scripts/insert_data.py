import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import uuid

# =========================
# DB CONFIG
# =========================
MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://doadmin:0ZeKg6Q321x79G4t@db-mongodb-fra1-25085-01-421631d0.mongo.ondigitalocean.com/"
)

client = AsyncIOMotorClient(MONGO_URL)
db = client["portfolio_db"]
collection = db["summary_data"]

# =========================
# MONTH ORDER
# =========================
MONTH_ORDER = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def sort_months(months: list) -> list:
    return sorted(
        months,
        key=lambda x: (
            x.get("year", 0),
            MONTH_ORDER.index(x["month"]) if x.get("month") in MONTH_ORDER else 99
        )
    )


def recalculate_opening_closing(capital: float, months: list) -> list:
    current_balance = capital

    for m in months:
        m["opening"] = round(current_balance, 2)
        current_balance += m.get("net_profit", 0)
        m["closing"] = round(current_balance, 2)

    return months


# =========================
# 🔥 MAIN TOTAL CALCULATION
# =========================
def recalculate_totals(capital: float, months: list) -> dict:

    if capital <= 0:
        return {
            "closing_balance": 0,
            "totals": {
                "opening": 0,
                "net_profit": 0,
                "closing": 0,
                "roi": 0,
                "total_trades": 0,
                "profit_trades": 0,
                "win_rate": 0,
                "profit": 0,
                "loss": 0,
                "profit_factor": 0,
                "loss_ratio": 0,
                "max_drawdown": 0
            }
        }

    total_net_profit = 0
    total_trades = 0
    profit_trades = 0
    total_profit = 0
    total_loss = 0

    # =========================
    # AGGREGATION
    # =========================
    for m in months:
        total_net_profit += m.get("net_profit", 0)
        total_trades += m.get("total_trades", 0)
        profit_trades += m.get("profit_trades", 0)

        total_profit += abs(m.get("profit", 0))
        total_loss += abs(m.get("loss", 0))

    total_closing = capital + total_net_profit

    # =========================
    # METRICS
    # =========================
    roi = (total_net_profit / capital * 100) if capital else 0
    win_rate = (profit_trades / total_trades * 100) if total_trades else 0
    profit_factor = (total_profit / total_loss) if total_loss else 0
    loss_ratio = (total_loss / total_profit * 100) if total_profit else 0

    # =========================
    # MAX DRAWDOWN
    # =========================
    peak = capital
    balance = capital
    max_drawdown = 0

    for m in months:
        balance += m.get("net_profit", 0)

        if balance > peak:
            peak = balance

        drawdown = ((peak - balance) / peak) * 100 if peak else 0

        if drawdown > max_drawdown:
            max_drawdown = drawdown

    return {
        "closing_balance": round(total_closing, 2),
        "totals": {
            "opening": round(capital, 2),
            "net_profit": round(total_net_profit, 2),
            "closing": round(total_closing, 2),
            "roi": round(roi, 2),

            "total_trades": total_trades,
            "profit_trades": profit_trades,
            "win_rate": round(win_rate, 2),

            "profit": round(total_profit, 2),
            "loss": round(total_loss, 2),

            "profit_factor": round(profit_factor, 2),
            "loss_ratio": round(loss_ratio, 2),

            "max_drawdown": round(max_drawdown, 2)
        }
    }


# =========================
# INSERT DATA
# =========================
async def insert_summary_data():

    capital = 100000

    months = [
        {
            "month": "Nov",
            "year": 2025,
            "net_profit": 29237.39,
            "total_trades": 24,
            "profit_trades": 17,
            "profit": 37061.42,
            "win_rate": 70.8,
            "roi": 29.24,
            "loss": -7824.02,
            "summary_id": "SUM-" + uuid.uuid4().hex[:8].upper()
        },
        {
            "month": "Dec",
            "year": 2025,
            "net_profit": 30740.84,
            "total_trades": 19,
            "profit_trades": 12,
            "profit": 38601.53,
            "win_rate": 63.16,
            "roi": 23.80,
            "loss": -7860.69,
            "summary_id": "SUM-" + uuid.uuid4().hex[:8].upper()
        },
        {
            "month": "Jan",
            "year": 2026,
            "net_profit": 50254.81,
            "total_trades": 24,
            "profit_trades": 16,
            "profit": 76255.44,
            "win_rate": 66.67,
            "roi": 31.40,
            "loss": -26000.63,
            "summary_id": "SUM-" + uuid.uuid4().hex[:8].upper()
        },
        {
            "month": "Feb",
            "year": 2026,
            "net_profit": 64543.82,
            "total_trades": 30,
            "profit_trades": 20,
            "profit": 104511.28,
            "win_rate": 66.67,
            "roi": 30.70,
            "loss": -39967.47,
            "summary_id": "SUM-" + uuid.uuid4().hex[:8].upper()
        },
        {
            "month": "Mar",
            "year": 2026,
            "net_profit": 82812.29,
            "total_trades": 21,
            "profit_trades": 15,
            "profit": 95972.72,
            "win_rate": 71.43,
            "roi": 30.10,
            "loss": -13160.43,
            "summary_id": "SUM-" + uuid.uuid4().hex[:8].upper()
        }
    ]

    # ========================= # PROCESS FLOW
    # =========================
    months = sort_months(months)
    months = recalculate_opening_closing(capital, months)
    totals_data = recalculate_totals(capital, months)

    data = {
        "account_id": "portfolio1",
        "capital": capital,
        "months": months,
        "opening_balance": totals_data["totals"]["opening"],
        "totals": totals_data["totals"],
        "closing_balance": totals_data["closing_balance"],
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }

    result = await collection.insert_one(data)
    print("✅ Inserted ID:", result.inserted_id)


# =========================
# RUN
# =========================
if __name__ == "__main__":
    asyncio.run(insert_summary_data())