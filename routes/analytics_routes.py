from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone
from fastapi.responses import JSONResponse
from database import summary_trading_collection
from utils.serialization import fix_id
import uuid

router = APIRouter(prefix="/analytics", tags=["analytics"])


# =========================
# 🔹 MODELS
# =========================
class TradeCreate(BaseModel):
    account_id: str
    trade_id: Optional[str] = None   # pass to EDIT an existing trade; omit to INSERT new
    date: Optional[str] = None       # if omitted, defaults to today
    type: str
    symbol: str
    lot_size: float
    open_price: float
    close_price: float
    swap: Optional[float] = 0.0
    profit_loss: float


class Trade(BaseModel):
    date: str
    type: str
    symbol: str
    lot_size: float
    open: float
    close: float
    swap: Optional[float] = 0
    pnl: float


class TradingData(BaseModel):
    account_id: str
    capital: float
    trades: List[Trade]
    #summary: Optional[dict] = None


class TradeDelete(BaseModel):
    account_id: str
    date: str
    symbol: str


# =========================
# 🔥 CREATE FULL TRADING DATA
# =========================
@router.post("/create_trading_data")
async def create_trading_data(payload: TradingData):
    try:
        data = payload.dict()

        # ✅ Validate account_id
        if not data.get("account_id"):
            return JSONResponse({
                "Error": "account_id is required"
            }, status_code=400)

        # ✅ Filter trades safely
        trades = [
            t for t in data.get("trades", [])
            if t.get("symbol") and t.get("symbol") != "string"
        ]

        # ✅ Sort safely
        trades = sorted(trades, key=lambda x: x.get("date", ""))

        # ✅ Assign trade_id
        for t in trades:
            if not t.get("trade_id"):
                t["trade_id"] = "TRD-" + uuid.uuid4().hex[:8].upper()

        capital = data.get("capital", 0)

        # ✅ Summary calculation
        total_pnl = 0
        total_swap = 0
        winning_trades = 0
        losing_trades = 0

        for t in trades:
            pnl = float(t.get("pnl", 0))
            swap = float(t.get("swap", 0))

            total_pnl += pnl
            total_swap += swap

            if pnl > 0:
                winning_trades += 1
            elif pnl < 0:
                losing_trades += 1

        total_trades = len(trades)

        # ✅ Chart calculation
        running_pnl = 0
        chart = []

        for t in trades:
            running_pnl += float(t.get("pnl", 0))
            return_percent = (running_pnl / capital) * 100 if capital else 0

            chart.append({
                "date": t.get("date"),
                "return": round(return_percent, 2)
            })

        final_data = {
            "account_id": data["account_id"],
            "capital": capital,
            "trades": trades,
            "chart": chart,
            "summary": {
                "total_pnl": round(total_pnl, 2),
                "total_swap": round(total_swap, 2),
                "total_trades": total_trades,
                "winning_trades": winning_trades,
                "losing_trades": losing_trades
            },
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }

        # ✅ Insert / Replace
        result = await summary_trading_collection.replace_one(
            {"account_id": data["account_id"]},
            final_data,
            upsert=True
        )

        print("Mongo result:", result.raw_result)

        saved_data = await summary_trading_collection.find_one(
            {"account_id": data["account_id"]}
        )

        return JSONResponse({
            "Success": "Trading data created/replaced successfully",
            "data": fix_id(saved_data)
        }, status_code=200)

    except Exception as e:
        print("ERROR:", str(e))  
        return JSONResponse({
            "Error": str(e)
        }, status_code=500)




# =========================
# 🔹 ADD / UPDATE SINGLE TRADE
# =========================
@router.post("/update_trading_summary")
async def update_trading_summary(data: TradeCreate):
    try:
        trade = data.dict()
        trade_date = trade.get("date") or datetime.now().strftime("%Y-%m-%d")
        incoming_trade_id = trade.get("trade_id")  # present = edit, absent = new

        # Fetch existing document
        existing = await summary_trading_collection.find_one(
            {"account_id": trade["account_id"]}
        )

        if existing:
            trades = existing.get("trades", [])
            capital = existing.get("capital", 0)
        else:
            trades = []
            capital = 0

        if incoming_trade_id:
            # ── EDIT mode: find by trade_id and update in-place ──
            match_index = next(
                (i for i, t in enumerate(trades)
                 if t.get("trade_id") == incoming_trade_id),
                None
            )
            if match_index is None:
                return JSONResponse(
                    {"Error": f"Trade with id '{incoming_trade_id}' not found"},
                    status_code=404
                )
            updated_trade = {
                "trade_id": incoming_trade_id,  # keep same id
                "date": trade_date,
                "type": trade["type"],
                "symbol": trade["symbol"],
                "lot_size": trade["lot_size"],
                "open": trade["open_price"],
                "close": trade["close_price"],
                "swap": trade.get("swap", 0),
                "pnl": trade["profit_loss"]
            }
            trades[match_index] = updated_trade
        else:
            # ── INSERT mode: generate new trade_id and prepend ──
            new_trade = {
                "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
                "date": trade_date,
                "type": trade["type"],
                "symbol": trade["symbol"],
                "lot_size": trade["lot_size"],
                "open": trade["open_price"],
                "close": trade["close_price"],
                "swap": trade.get("swap", 0),
                "pnl": trade["profit_loss"]
            }
            trades.insert(0, new_trade)

        # Recalculate summary from all trades
        total_pnl = sum(t.get("pnl", 0) for t in trades)
        total_swap = sum(t.get("swap", 0) for t in trades)
        total_trades = len(trades)
        winning_trades = sum(1 for t in trades if t.get("pnl", 0) > 0)
        losing_trades = sum(1 for t in trades if t.get("pnl", 0) < 0)

        # Rebuild chart in date order
        sorted_trades = sorted(trades, key=lambda x: x["date"])
        running_pnl = 0
        chart = []
        for t in sorted_trades:
            running_pnl += t.get("pnl", 0)
            return_pct = (running_pnl / capital) * 100 if capital else 0
            chart.append({
                "date": t["date"],
                "return": round(return_pct, 2)
            })

        update_payload = {
            "trades": trades,
            "chart": chart,
            "summary": {
                "total_pnl": round(total_pnl, 2),
                "total_swap": round(total_swap, 2),
                "total_trades": total_trades,
                "winning_trades": winning_trades,
                "losing_trades": losing_trades
            },
            "updated_at": datetime.now(timezone.utc)
        }

        await summary_trading_collection.update_one(
            {"account_id": trade["account_id"]},
            {
                "$set": update_payload,
                "$setOnInsert": {
                    # Only fires when creating a NEW document
                    "account_id": trade["account_id"],
                    "capital": capital,
                    "created_at": datetime.now(timezone.utc)
                }
            },
            upsert=True
        )

        updated_doc = await summary_trading_collection.find_one(
            {"account_id": trade["account_id"]}
        )

        return JSONResponse({
            "Success": "Trade updated & summary recalculated",
            "data": fix_id(updated_doc)
        }, status_code=200)

    except Exception as e:
        return JSONResponse({
            "Error": str(e)
        }, status_code=500)


# =========================
# 🔹 VIEW TRADING SUMMARY
# =========================
class AccountRequest(BaseModel):
    account_id: str


@router.post("/view_trading_summary")
async def view_trading_summary(mod: AccountRequest):
    try:
        data = await summary_trading_collection.find_one({"account_id": mod.account_id},{
            "_id":0
        })

        if not data:
            return JSONResponse({
                "Error": "Account not found"
            }, status_code=400)

        return JSONResponse({
            "Success": fix_id(data)
        }, status_code=200)

    except Exception as e:
        return JSONResponse({
            "Error": str(e)
        }, status_code=500)


# =========================
# 🔹 DELETE TRADE
# =========================
@router.post("/delete_trade")
async def delete_trade(payload: TradeDelete):
    try:
        existing = await summary_trading_collection.find_one({"account_id": payload.account_id})

        if not existing:
            return JSONResponse({
                "Error": "Account not found"
            }, status_code=400)

        trades = existing.get("trades", [])
        capital = existing.get("capital", 0)

        updated_trades = [
            t for t in trades
            if not (t["date"] == payload.date and t["symbol"] == payload.symbol)
        ]

        if len(updated_trades) == len(trades):
            return JSONResponse({
                "Error": "Trade not found"
            }, status_code=400)

        # Recalculate summary
        total_pnl = sum(t.get("pnl", 0) for t in updated_trades)
        total_swap = sum(t.get("swap", 0) for t in updated_trades)
        total_trades = len(updated_trades)
        winning_trades = len([t for t in updated_trades if t["pnl"] > 0])
        losing_trades = len([t for t in updated_trades if t["pnl"] < 0])

        # Rebuild chart using account capital
        running_pnl = 0
        chart = []

        for t in updated_trades:
            running_pnl += t.get("pnl", 0)
            return_percent = (running_pnl / capital) * 100 if capital else 0
            chart.append({
                "date": t["date"],
                "return": round(return_percent, 2)
            })

        await summary_trading_collection.update_one(
            {"account_id": payload.account_id},
            {
                "$set": {
                    "trades": updated_trades,
                    "chart": chart,
                    "summary": {
                        "total_pnl": round(total_pnl, 2),
                        "total_swap": round(total_swap, 2),
                        "total_trades": total_trades,
                        "winning_trades": winning_trades,
                        "losing_trades": losing_trades
                    },
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )

        updated_doc = await summary_trading_collection.find_one(
            {"account_id": payload.account_id}
        )

        return JSONResponse({
            "Success": "Trade deleted & summary updated",
            "data": fix_id(updated_doc)
        }, status_code=200)

    except Exception as e:
        return JSONResponse({
            "Error": str(e)
        }, status_code=500)
''''''