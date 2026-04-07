
from fastapi import APIRouter
from database import summary_data_collection
from datetime import datetime, timezone
from utils.serialization import fix_id
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/accounts", tags=["accounts"])


# =========================
# 🔹 MODELS
# =========================
class MonthData(BaseModel):
    month: str
    opening: float
    net_profit: float
    closing: float
    roi: float
    total_trades: int
    winning_trades: int
    win_rate: float
    profit_amount: float
    loss_amount: float
    loss_ratio: float
    profit_factor: float


class SummaryDataCreate(BaseModel):
    account_id: str
    capital: float
    closing_balance: float
    months: List[MonthData]
    summary_id: Optional[str] = None  


class AccountRequest(BaseModel):
    account_id: str


class DeleteMonthRequest(BaseModel):
    account_id: str
    month: str


# =========================
# 🔹 HELPERS
# =========================
def recalculate_totals(capital: float, months: list) -> dict:
    """Recalculate all totals and metrics from a sorted months list."""
    total_net_profit = 0
    total_trades = 0
    total_winning_trades = 0
    total_profit = 0
    total_loss = 0

    for m in months:
        total_net_profit += m.get("net_profit", 0)
        total_trades += m.get("total_trades", 0)
        total_winning_trades += m.get("winning_trades", 0)
        total_profit += abs(m.get("profit_amount", 0))
        total_loss += abs(m.get("loss_amount", 0))

    total_closing = capital + total_net_profit

    total_roi = (total_net_profit / capital * 100) if capital else 0
    win_rate = (total_winning_trades / total_trades * 100) if total_trades else 0
    profit_factor = (total_profit / total_loss) if total_loss else 0
    loss_ratio = (
        (total_loss / (total_profit + total_loss) * 100)
        if (total_profit + total_loss) else 0
    )

    # Max drawdown
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
            "roi": round(total_roi, 2),
            "total_trades": total_trades,
            "winning_trades": total_winning_trades,
            "win_rate": round(win_rate, 2),
            "total_profit": round(total_profit, 2),
            "total_loss": round(total_loss, 2),
            "loss_ratio": round(loss_ratio, 2),
            "profit_factor": round(profit_factor, 2),
            "max_drawdown": round(max_drawdown, 2),
            "profit_loss_ratio": round((total_profit / total_loss), 2) if total_loss else 0
        }
    }


MONTH_ORDER = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def sort_months(months: list) -> list:
    return sorted(months, key=lambda x: MONTH_ORDER.index(x["month"]) if x["month"] in MONTH_ORDER else 99)


def recalculate_opening_closing(capital: float, months: list) -> list:
    """Recalculate opening/closing balance for each month in sequence."""
    current_balance = capital
    for m in months:
        m["opening"] = round(current_balance, 2)
        current_balance += m.get("net_profit", 0)
        m["closing"] = round(current_balance, 2)
    return months


# =========================
# 🔥 CREATE / UPDATE SUMMARY
# =========================
import uuid

@router.post("/create_summary_data")
async def create_summary_data(summary: SummaryDataCreate):
    try:
        data = summary.dict()
        account_id = data["account_id"]
        new_months = data.get("months", [])

        existing = await summary_data_collection.find_one({"account_id": account_id})

        # =========================
        # 🔥 ADD summary_id TO NEW MONTHS
        # =========================
        for m in new_months:
            if "summary_id" not in m:
                m["summary_id"] = "SUM-" + uuid.uuid4().hex[:8].upper()

        if existing:
            existing_months = existing.get("months", [])
            capital = existing.get("capital", data.get("capital", 0))

            # Keep old summary_id if month exists
            months_map = {m["month"]: m for m in existing_months}

            for m in new_months:
                if m["month"] in months_map:
                    # preserve old summary_id
                    m["summary_id"] = months_map[m["month"]].get("summary_id", str(uuid.uuid4()))
                months_map[m["month"]] = m

            months = list(months_map.values())

        else:
            months = new_months
            capital = data.get("capital", 0)

        # =========================
        # 🔹 SORT + RECALCULATE
        # =========================
        months = sort_months(months)
        months = recalculate_opening_closing(capital, months)

        totals = recalculate_totals(capital, months)

        updated_data = {
            "account_id": account_id,
            "capital": capital,
            "months": months,
            "closing_balance": totals["closing_balance"],
            "totals": totals["totals"],
            "updated_at": datetime.now(timezone.utc)
        }

        await summary_data_collection.update_one(
            {"account_id": account_id},
            {
                "$set": updated_data,
                "$setOnInsert": {"created_at": datetime.now(timezone.utc)}
            },
            upsert=True
        )

        saved_data = await summary_data_collection.find_one({"account_id": account_id})

        return JSONResponse({
            "Success": "Summary updated with month summary_id",
            "data": fix_id(saved_data)
        }, status_code=200)

    except Exception as e:
        return JSONResponse({"Error": str(e)}, status_code=500)


# =========================
# 🔹 VIEW SUMMARY
# =========================
@router.post("/view_summary_data")
async def view_summary_data(request: AccountRequest):
    try:
        data = await summary_data_collection.find_one({"account_id": request.account_id})

        if not data:
            return JSONResponse({"Error": "Account not found"}, status_code=400)

        return JSONResponse({"Success": fix_id(data)}, status_code=200)

    except Exception as e:
        return JSONResponse({"Error": str(e)}, status_code=500)


# =========================
# 🔹 ADD / UPDATE A MONTH
# =========================
import uuid

@router.post("/add_performance_month")
async def add_performance_month(summary: SummaryDataCreate):
    try:
        data = summary.dict()
        account_id = data["account_id"]
        new_month = data.get("months")[0]

        existing = await summary_data_collection.find_one({"account_id": account_id,"summary_id":data.get("summary_id")})

        incoming_summary_id = new_month.get("summary_id")

        # =========================
        # 🔥 GENERATE ID IF NOT PROVIDED
        # =========================
        if not incoming_summary_id:
            incoming_summary_id = "SUM-" + uuid.uuid4().hex[:8].upper()
            new_month["summary_id"] = incoming_summary_id

        if existing:
            months = existing.get("months", [])
            capital = existing.get("capital", data.get("capital", 0))

            found = False
            updated_months = []

            # =========================
            # 🔁 STRICT MATCH BY summary_id
            # =========================
            for m in months:
                if m.get("summary_id") == incoming_summary_id:
                    # ✅ UPDATE ONLY THIS RECORD
                    updated_months.append(new_month)
                    found = True
                else:
                    updated_months.append(m)

            # =========================
            # ➕ ADD ONLY IF NOT FOUND
            # =========================
            if not found:
                updated_months.append(new_month)

            months = updated_months

        else:
            capital = data.get("capital", 0)
            months = [new_month]

        # =========================
        # 🔹 SORT + RECALCULATE
        # =========================
        months = sort_months(months)
        months = recalculate_opening_closing(capital, months)
        totals = recalculate_totals(capital, months)

        updated_data = {
            "account_id": account_id,
            "capital": capital,
            "months": months,
            "closing_balance": totals["closing_balance"],
            "totals": totals["totals"],
            "updated_at": datetime.now(timezone.utc)
        }

        await summary_data_collection.update_one(
            {"account_id": account_id},
            {
                "$set": updated_data,
                "$setOnInsert": {"created_at": datetime.now(timezone.utc)}
            },
            upsert=True
        )

        saved_data = await summary_data_collection.find_one({"account_id": account_id})

        return JSONResponse({
            "Success": "Handled strictly by summary_id",
            "data": fix_id(saved_data)
        }, status_code=200)

    except Exception as e:
        return JSONResponse({"Error": str(e)}, status_code=500)


# =========================
# 🔹 DELETE A MONTH
# =========================
@router.post("/delete_performance_month")
async def delete_performance_month(mod: DeleteMonthRequest):
    try:
        existing = await summary_data_collection.find_one({"account_id": mod.account_id})

        if not existing:
            return JSONResponse({"Error": "Account not found"}, status_code=400)

        months = existing.get("months", [])
        capital = existing.get("capital", 0)

        updated_months = [m for m in months if m["month"] != mod.month]

        if len(updated_months) == len(months):
            return JSONResponse({"Error": f"Month '{mod.month}' not found"}, status_code=400)

        updated_months = sort_months(updated_months)
        updated_months = recalculate_opening_closing(capital, updated_months)

        totals = recalculate_totals(capital, updated_months)

        updated_data = {
            "months": updated_months,
            "closing_balance": totals["closing_balance"],
            "totals": totals["totals"],
            "updated_at": datetime.now(timezone.utc)
        }

        await summary_data_collection.update_one(
            {"account_id": mod.account_id},
            {"$set": updated_data}
        )

        saved_data = await summary_data_collection.find_one({"account_id": mod.account_id})

        return JSONResponse({
            "Success": f"Month '{mod.month}' deleted and totals updated",
            "data": fix_id(saved_data)
        }, status_code=200)

    except Exception as e:
        return JSONResponse({"Error": str(e)}, status_code=500)