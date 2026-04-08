from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone
from fastapi.responses import JSONResponse
from database import summary_trading_collection
from utils.serialization import fix_id
import uuid
from models.trades import TradeCreate, TradeDelete, TradeUpdate,AccountRequest




router = APIRouter(prefix="/analytics", tags=["analytics"])



@router.post("/create_trading_data")
async def create_trading_data(payload: TradeCreate):
    try:
        data = payload.dict()

        if not data.get("account_id"):
            return JSONResponse({"error": "account_id is required"}, status_code=400)

        capital = float(data.get("capital", 0))
        raw_trades = data.get("trades", [])

        trades = [
            t for t in raw_trades
            if t.get("symbol") and t.get("symbol") != "string"
        ]

        # =========================
        # 🟢 EMPTY CASE
        # =========================
        if not trades:
            final_data = {
                "account_id": data["account_id"],
                "trades": [],
                "chart": [],
                "created_at": datetime.now(timezone.utc)
               
            }

            await summary_trading_collection.update_one(
                {"account_id": data["account_id"]},
                {"$set": final_data},
                upsert=True
            )

            saved_data = await summary_trading_collection.find_one({
                "account_id": data["account_id"]
            })

            return JSONResponse({
                "Success": "Trading data stored successfully"
            }, status_code=200)

        # =========================
        # 🔽 SORT
        # =========================
        trades = sorted(trades, key=lambda x: x.get("date", ""))

        # =========================
        # 🆔 TRADE ID
        # =========================
        for t in trades:
            if not t.get("trade_id"):
                t["trade_id"] = "TRD-" + uuid.uuid4().hex[:8].upper()

        # =========================
        # 📈 CHART
        # =========================
        running_pnl = 0
        chart = []

        for t in trades:
            running_pnl += float(t.get("pnl", 0))
            return_percent = (running_pnl / capital) * 100 if capital else 0

            chart.append({
                "date": t.get("date"),
                "return": round(return_percent, 2)
            })

        # =========================
        # 💾 SAVE
        # =========================
        final_data = {
            "account_id": data["account_id"],
            "trades": trades,
            "chart": chart,
            "created_at": datetime.now(timezone.utc)
            
        }

        await summary_trading_collection.update_one(
            {"account_id": data["account_id"]},
            {"$set": final_data},
            upsert=True
        )

      
        return JSONResponse({
            "Success": "Trading data stored successfully"
        }, status_code=200)

    except Exception as e:
        return JSONResponse({"Error": str(e)}, status_code=500)




# =========================
# 🔹 ADD / UPDATE SINGLE TRADE
# =========================
@router.post("/update_trading_summary")
async def update_trading_summary(data: TradeUpdate):
    try:
        trade = data.dict()
        trade_date = trade.get("date") or datetime.now().strftime("%Y-%m-%d")
        incoming_trade_id = trade.get("trade_id")

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
        

        previous_cum_profit = 0

        if existing and existing.get("trades"):

            last_trade = existing["trades"][-1]
            previous_cum_profit = last_trade.get("cum_profit", 0)

        # Current pnl
        current_pnl = trade["profit_loss"]

        # Calculate cumulative profit
        cum_profit = previous_cum_profit + current_pnl
        trade["cum_profit"] = cum_profit    

        month_profits = trade.get("month_profit", "")
        profit_loss_type = trade.get("profitandloss", "")

        month_profit = f"{month_profits}{profit_loss_type}"
        
        # =========================
        # ✅ COMMON TRADE OBJECT
        # =========================
        trade_data = {
            "trade_id": incoming_trade_id if incoming_trade_id else "TRD-" + uuid.uuid4().hex[:8].upper(),
            "date": trade_date,
            "type": trade["type"],
            "symbol": trade["symbol"],
            "lot_size": trade["lot_size"],
            "open": trade["open_price"],
            "close": trade["close_price"],
            "swap": trade.get("swap", 0),
            "pnl": trade["profit_loss"],
            "max_drawdown": trade.get("max_drawdown", 0),
            "cumulative_balance": trade.get("cumulative_balance", 0),
            "cum_profit": cum_profit,
            "return": trade.get("return_data", 0),
            "profitandloss": trade.get("profitandloss", ""),
            "position_size": trade.get("position_size", 0),
            "per_pip_value": trade.get("per_pip_value", 0),
            "pip": trade.get("pip", 0),
            "swap_per_days": trade.get("swap_per_days", 0),
            "value": trade.get("value", 0),
            "adj": trade.get("adj", 0),
            "adjisted_swap": trade.get("adjisted_swap", 0),
            "month": trade.get("month", ""),
            "month_profit": month_profit
        }

        # =========================
        # ✅ EDIT OR INSERT
        # =========================
        if incoming_trade_id:
            # EDIT
            match_index = next(
                (i for i, t in enumerate(trades)
                 if t.get("trade_id") == incoming_trade_id),
                None
            )

            if match_index is None:
                return JSONResponse(
                    {"Error": f"Trade with id '{incoming_trade_id}' not found"},
                    status_code=400
                )

            trades[match_index] = trade_data

        else:
            # INSERT
            trades.insert(0, trade_data)

        # =========================
        # ✅ CHART CALCULATION ONLY
        # =========================
        sorted_trades = sorted(trades, key=lambda x: x["date"])

        running_pnl = 0
        chart = []

        for t in sorted_trades:
            running_pnl += t.get("pnl", 0)
            return_pct = (running_pnl / capital) * 100 if capital else 0

            chart.append({
                "date": t["date"],
                "return": trade.get("return_data", 0)
            })

        # =========================
        # ✅ UPDATE PAYLOAD (NO SUMMARY)
        # =========================
        update_payload = {
            "trades": trades,
            "chart": chart,
            "updated_at": datetime.now(timezone.utc)
        }

        await summary_trading_collection.update_one(
            {"account_id": trade["account_id"]},
            {
                "$set": update_payload,
                "$unset": {"summary": ""},  # ❌ REMOVE summary
                "$setOnInsert": {
                    "account_id": trade["account_id"],
                    "capital": capital,
                    "created_at": datetime.now(timezone.utc)
                }
            },
            upsert=True
        )

       

        return JSONResponse({
            "Success": "Trade updated successfully"
        }, status_code=200)

    except Exception as e:
        return JSONResponse({
            "Error": str(e)
        }, status_code=500)


# =========================
# 🔹 VIEW TRADING SUMMARY
# =========================


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
        existing = await summary_trading_collection.find_one({
            "account_id": payload.account_id
        })

        if not existing:
            return JSONResponse({
                "Error": "Account not found"
            }, status_code=400)

        trades = existing.get("trades", [])
        capital = existing.get("capital", 0)

        # ✅ DELETE USING trade_id
        updated_trades = [
            t for t in trades
            if t.get("trade_id") != payload.trade_id
        ]

        if len(updated_trades) == len(trades):
            return JSONResponse({
                "Error": "Trade not found"
            }, status_code=400)

        # =========================
        # 📊 REBUILD CHART (optional)
        # =========================
        running_pnl = 0
        chart = []

        updated_trades.sort(key=lambda x: x.get("date", ""))

        for t in updated_trades:
            running_pnl += t.get("pnl", 0)

            return_percent = (
                (running_pnl / capital) * 100
                if capital else 0
            )

            chart.append({
                "date": t.get("date"),
                "return": round(return_percent, 2)
            })

        # =========================
        # 💾 UPDATE DB (NO SUMMARY)
        # =========================
        await summary_trading_collection.update_one(
            {"account_id": payload.account_id},
            {
                "$set": {
                    "trades": updated_trades,
                    "chart": chart,
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )

        updated_doc = await summary_trading_collection.find_one({
            "account_id": payload.account_id
        })

        return JSONResponse({
            "Success": "Trade deleted successfully"
        }, status_code=200)

    except Exception as e:
        return JSONResponse({
            "Error": str(e)
        }, status_code=500)
