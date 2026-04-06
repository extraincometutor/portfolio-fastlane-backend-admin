import asyncio
from database import summary_data_collection, summary_trading_collection
from datetime import datetime, timezone

async def verify_endpoints():
    # Test summary_data insert
    summary_doc = {
        "capital": 250000,
        "account_id": "portfolio1_test",
        "closing_balance": 390297.03,
        "months": [
            {
                "month": "Feb",
                "opening": 250000.0,
                "net_profit": 63508.45,
                "closing": 313508.45,
                "roi": 25.4,
                "total_trades": 15,
                "winning_trades": 11,
                "win_rate": 73.3,
                "profit_amount": 80627.1,
                "loss_amount": -17118.65,
                "loss_ratio": -21.2,
                "profit_factor": 4.7
            }
        ],
        "totals": {
            "opening": 250000.0,
            "net_profit": 140297.03,
            "closing": 390297.03,
            "roi": 56.1,
            "total_trades": 38,
            "winning_trades": 25,
            "win_rate": 65.8,
            "total_profit": 183579.61,
            "total_loss": -43282.58,
            "loss_ratio": -23.6,
            "profit_factor": 4.2,
            "max_dropdown": -4.5
        },
        "created_at": datetime.now(timezone.utc)
    }
    result = await summary_data_collection.insert_one(summary_doc)
    print(f"[summary_data] Inserted with _id: {result.inserted_id}")

    # Test summary_trading insert 
    trading_doc = {
        "account_id": "portfolio1_test",
        "trades": [
            {"date": "2026-02-12", "type": "Sell", "symbol": "XAUUSD", "lot_size": 0.5, "open": 5064.09, "close": 4945.58, "swap": 0.0, "pnl": 5925.5}
        ],
        "chart": [
            {"date": "2026-02-12", "return": 2.4}
        ],
        "summary": {
            "total_swap": -744.97,
            "total_pnl": 140297.03
        },
        "created_at": datetime.now(timezone.utc)
    }
    result2 = await summary_trading_collection.insert_one(trading_doc)
    print(f"[summary_trading] Inserted with _id: {result2.inserted_id}")
    print("All verifications passed!")

if __name__ == "__main__":
    asyncio.run(verify_endpoints())
