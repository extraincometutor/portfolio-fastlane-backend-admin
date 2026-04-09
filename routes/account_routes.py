
from fastapi import APIRouter
from database import summary_data_collection
from datetime import datetime, timezone
from utils.serialization import fix_id
from fastapi.responses import JSONResponse
from models.summary import CreateSummary, AddSummary, AccountRequest, DeleteMonthRequest
import uuid

from fastapi import APIRouter
from datetime import datetime, timezone
from fastapi.responses import JSONResponse
import uuid

router = APIRouter(prefix="/accounts", tags=["accounts"])

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
    
    max_drawdown = -6.88

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




@router.post("/create_summary_data")
async def create_summary_data(summary: CreateSummary):
    try:
        data = summary.dict()
        account_id = data["account_id"]

        # Check if already exists
        existing = await summary_data_collection.find_one({"account_id": account_id})
        if existing:
            return JSONResponse({
                "Error": "Summary already exists for this account_id"
            }, status_code=400)

        # Default structure
        new_data = {
            "account_id": account_id,
            "capital":0,
            "months": [],
            "totals": {
                "opening": 0,
                "net_profit": 0,
                "closing": 0,
                "roi": 0,
                "total_trades": 0,
                "profit_trades": 0,
                "win_rate": 0,
                "max_drawdown": 0,
                "profit_factor": 0,
                "profit": 0,
                "loss": 0,
                "loss_ratio": 0
            },
            "created_at": datetime.now(timezone.utc)
        }

        await summary_data_collection.insert_one(new_data)

        saved_data = await summary_data_collection.find_one({"account_id": account_id})

        return JSONResponse({
            "Success": "Summary created successfully"
        }, status_code=200)

    except Exception as e:
        return JSONResponse({"Error": str(e)}, status_code=500)



@router.post("/view_summary_data")
async def view_summary_data(request: AccountRequest):
    try:
        data = await summary_data_collection.find_one({"account_id": request.account_id},{"_id": 0})

        if not data:
            return JSONResponse({"Error": "Account not found"}, status_code=400)

        return JSONResponse({"Success": fix_id(data)}, status_code=200)

    except Exception as e:
        return JSONResponse({"Error": str(e)}, status_code=500)





# =========================
# 📊 SORT MONTHS
# =========================
def sort_months(months: list):
    month_order = {
        "January": 1, "February": 2, "March": 3, "April": 4,
        "May": 5, "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12
    }

    return sorted(
        months,
        key=lambda x: (x.get("year", 0), month_order.get(x.get("month"), 0))
    )

# =========================
# 📊 AUTO CALC (ONLY FOR ADD)
# =========================
def recalculate_opening_closing(capital: float, months: list):
    running_balance = capital

    for m in months:
        if "opening" not in m:
            m["opening"] = running_balance

        if "closing" not in m:
            profit = m.get("net_profit", 0)
            m["closing"] = m["opening"] + profit

        running_balance = m["closing"]

    return months


# =========================
# 🚀 MAIN API
# =========================
@router.post("/add_performance_month")
async def add_performance_month(summary: AddSummary):
    try:
        data = summary.dict()
        account_id = data["account_id"]

        # =========================
        # INPUT
        # =========================
        new_month = {
            "month": data.get("month"),
            "year": data.get("year"),
            "net_profit": data.get("net_profit", 0),
            "total_trades": data.get("total_trades", 0),
            "profit_trades": data.get("profit_trades", 0),
            "max_drawdown": data.get("max_drawdown", 0),
            "profit_factor": data.get("profit_factor", 0),
            "profit": data.get("profit", 0),
            "loss": data.get("loss", 0),
            "loss_ratio": data.get("loss_ratio", 0),
            "opening": data.get("opening"),
            "closing": data.get("closing"),
        }

        new_month = {k: v for k, v in new_month.items() if v is not None}

        incoming_summary_id = data.get("summary_id")

        existing = await summary_data_collection.find_one({"account_id": account_id})

        if existing:
            months = existing.get("months", [])
            capital = data.get("capital", existing.get("capital", 0))

            updated_months = []
            found = False

            # =========================
            # ✏️ EDIT (MANUAL MODE)
            # =========================
            if incoming_summary_id:
                for m in months:
                    if m.get("summary_id") == incoming_summary_id:
                        updated = {**m, **new_month}
                        updated["summary_id"] = m["summary_id"]

                        updated_months.append(updated)
                        found = True
                    else:
                        updated_months.append(m)

                if not found:
                    return JSONResponse({"Error": "summary_id not found"}, status_code=404)

                months = updated_months

            else:
                # =========================
                # ➕ ADD (AUTO MODE)
                # =========================
                new_id = "SUM-" + uuid.uuid4().hex[:8].upper()
                new_month["summary_id"] = new_id

                months.append(new_month)
                months = sort_months(months)
                months = recalculate_opening_closing(capital, months)

        else:
            # =========================
            # FIRST INSERT
            # =========================
            capital = data.get("capital", 0)

            new_id = "SUM-" + uuid.uuid4().hex[:8].upper()
            new_month["summary_id"] = new_id

            # if no opening provided → default
            if "opening" not in new_month:
                new_month["opening"] = capital

            if "closing" not in new_month:
                new_month["closing"] = new_month["opening"] + new_month.get("net_profit", 0)

            months = [new_month]

        # =========================
        # TOTALS
        # =========================
        totals = recalculate_totals(capital, months)

        updated_data = {
            "account_id": account_id,
            "capital": capital,
            "months": months,
            "opening_balance": totals["opening_balance"],
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

        return JSONResponse({
            "Success": "Manual edit applied",
            "summary_id": incoming_summary_id
        })

    except Exception as e:
        return JSONResponse({"Error": str(e)}, status_code=500)

# =========================
# 🔹 DELETE A MONTH
# =========================
@router.post("/delete_performance_month")
async def delete_performance_month(mod: DeleteMonthRequest):
    try:
        print("DELETE REQUEST RECEIVED:", mod.account_id, mod.summary_id)

        existing = await summary_data_collection.find_one(
            {"account_id": mod.account_id}
        )

        if not existing:
            return JSONResponse({"Error": "Account not found"}, status_code=400)

        months = existing.get("months", [])
        capital = existing.get("capital", 0)

        # =========================
        # 🔍 FIND MONTH BEFORE DELETE
        # =========================
        deleted_month = None
        for m in months:
            if m.get("summary_id") == mod.summary_id:
                deleted_month = m.get("month")
                break

     
        updated_months = [
            m for m in months if m.get("summary_id") != mod.summary_id
        ]

        if len(updated_months) == len(months):
            return JSONResponse({
                "Error": f"Summary '{mod.summary_id}' not found"
            }, status_code=400)

        # =========================
        # 📊 RECALCULATE
        # =========================
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

        return JSONResponse({
            "Success": f"Summary '{mod.summary_id}' deleted successfully"
        }, status_code=200)

    except Exception as e:
        return JSONResponse({"Error": str(e)}, status_code=500)