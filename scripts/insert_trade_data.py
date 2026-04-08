import asyncio
import os
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone


# Mongo URL
MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://doadmin:0ZeKg6Q321x79G4t@db-mongodb-fra1-25085-01-421631d0.mongo.ondigitalocean.com/"
)


client = AsyncIOMotorClient(MONGO_URL)
db = client["portfolio_db"]
collection = db["summary_trading"]

async def insert_exact_sheet_data():

    trades = [

                {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-02-12","type": "Sell","symbol": "XAUUSD","lot_size": 0.50,
        "open": 5064.09,"close": 4945.58,"swap": 0.00,"pnl": 5925.50,
        "max_drawdown": 0.00,"cumulative_balance": 255925.50,"cum_profit": 5925.50,
        "return": 2.4,"profitandloss": "Profit","position_size": 50,
        "per_pip_value": 100,"pip": 118.51,"swap_per_days": 0,
        "value": 0,"adj": 0,"adjisted_swap": 0,"month": "Feb","month_profit": "FebProfit"
        },

        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-02-12","type": "Sell","symbol": "EURUSD","lot_size": 1.00,
        "open": 1.18772,"close": 1.18653,"swap": 0.00,"pnl": 119.00,
        "max_drawdown": 0.00,"cumulative_balance": 256044.50,"cum_profit": 6044.50,
        "return": 2.4,"profitandloss": "Profit","position_size": 10,
        "per_pip_value": 10,"pip": 11.90,"swap_per_days": 0,
        "value": 0,"adj": 0,"adjisted_swap": 0,"month": "Mar","month_profit": "MarProfit"
        },

        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-02-12","type": "Sell","symbol": "XAUUSD","lot_size": 0.50,
        "open": 5075.46,"close": 4915.41,"swap": 0.00,"pnl": 8002.50,
        "max_drawdown": 0.00,"cumulative_balance": 264047.00,"cum_profit": 14047.00,
        "return": 5.6,"profitandloss": "Profit","position_size": 50,
        "per_pip_value": 100,"pip": 160.05,"swap_per_days": 0,
        "value": 0,"adj": 0,"adjisted_swap": 0,"month": "Feb","month_profit": "FebProfit"
        },

        # ===== 2026-02-13 =====
        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-02-13","type": "Sell","symbol": "XAUUSD","lot_size": 0.60,
        "open": 4980.91,"close": 5032.53,"swap": 0.00,"pnl": -3097.20,
        "max_drawdown": -1.19,"cumulative_balance": 260949.80,"cum_profit": 10949.80,
        "return": 4.4,"profitandloss": "Loss","position_size": 60,
        "per_pip_value": 100,"pip": -51.62,"swap_per_days": 0,
        "value": 0,"adj": 0,"adjisted_swap": 0,"month": "Feb","month_profit": "FebLoss"
        },

        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-02-13","type": "Sell","symbol": "EURUSD","lot_size": 1.00,
        "open": 1.18588,"close": 1.18679,"swap": 0.00,"pnl": -91.00,
        "max_drawdown": -0.03,"cumulative_balance": 260858.80,"cum_profit": 10858.80,
        "return": 4.3,"profitandloss": "Loss","position_size": 10,
        "per_pip_value": 10,"pip": -9.10,"swap_per_days": 0,
        "value": 0,"adj": 0,"adjisted_swap": 0,"month": "Mar","month_profit": "MarLoss"
        },

        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-02-13","type": "Sell","symbol": "XAUUSD","lot_size": 0.60,
        "open": 4950.25,"close": 5015.63,"swap": 25.30,"pnl": -3897.50,
        "max_drawdown": -1.52,"cumulative_balance": 256961.30,"cum_profit": 6961.30,
        "return": 2.8,"profitandloss": "Loss","position_size": 60,
        "per_pip_value": 100,"pip": -65.38,"swap_per_days": 1,
        "value": 25.20,"adj": 0.1,"adjisted_swap": 25.30,"month": "Feb","month_profit": "FebLoss"
        },

        # ===== 2026-02-16 =====
        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-02-16","type": "Sell","symbol": "XAUUSD","lot_size": 0.60,
        "open": 4994.78,"close": 4910.45,"swap": 24.90,"pnl": 5084.70,
        "max_drawdown": 0.00,"cumulative_balance": 262046.00,"cum_profit": 12046.00,
        "return": 4.8,"profitandloss": "Profit","position_size": 60,
        "per_pip_value": 100,"pip": 84.33,"swap_per_days": 1,
        "value": 25.20,"adj": -0.3,"adjisted_swap": 24.90,"month": "Feb","month_profit": "FebProfit"
        },

        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-02-16","type": "Sell","symbol": "EURUSD","lot_size": 1.00,
        "open": 1.18650,"close": 1.18542,"swap": 0.00,"pnl": 108.00,
        "max_drawdown": 0.00,"cumulative_balance": 262154.00,"cum_profit": 12154.00,
        "return": 4.9,"profitandloss": "Profit","position_size": 10,
        "per_pip_value": 10,"pip": 10.80,"swap_per_days": 0,
        "value": 0,"adj": 0,"adjisted_swap": 0,"month": "Mar","month_profit": "MarProfit"
        },

        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-02-16","type": "Sell","symbol": "XAUUSD","lot_size": 0.70,
        "open": 5006.13,"close": 4917.18,"swap": 29.20,"pnl": 6255.70,
        "max_drawdown": 0.00,"cumulative_balance": 268409.70,"cum_profit": 18409.70,
        "return": 7.4,"profitandloss": "Profit","position_size": 70,
        "per_pip_value": 100,"pip": 88.95,"swap_per_days": 1,
        "value": 29.40,"adj": -0.2,"adjisted_swap": 29.20,"month": "Feb","month_profit": "FebProfit"
        },

        # ===== 2026-02-17 =====
        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-02-17","type": "Buy","symbol": "EURUSD","lot_size": 1.00,
        "open": 1.18414,"close": 1.18108,"swap": 0.00,"pnl": -306.00,
        "max_drawdown": -0.11,"cumulative_balance": 268103.70,"cum_profit": 18103.70,
        "return": 7.2,"profitandloss": "Loss","position_size": 10,
        "per_pip_value": 10,"pip": -30.60,"swap_per_days": 0,
        "value": 0,"adj": 0,"adjisted_swap": 0,"month": "Mar","month_profit": "MarLoss"
        },

        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-02-17","type": "Sell","symbol": "XAUUSD","lot_size": 0.70,
        "open": 4870.71,"close": 4991.73,"swap": 29.25,"pnl": -8442.15,
        "max_drawdown": -3.25,"cumulative_balance": 259661.55,"cum_profit": 9661.55,
        "return": 3.9,"profitandloss": "Loss","position_size": 70,
        "per_pip_value": 100,"pip": -121.02,"swap_per_days": 1,
        "value": 29.40,"adj": -0.15,"adjisted_swap": 29.25,"month": "Feb","month_profit": "FebLoss"
        },

        # ===== 2026-02-18 =====
        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-02-18","type": "Buy","symbol": "XAUUSD","lot_size": 0.70,
        "open": 4991.73,"close": 4995.80,"swap": -44.51,"pnl": 240.39,
        "max_drawdown": 0.00,"cumulative_balance": 259901.94,"cum_profit": 9901.94,
        "return": 4.0,"profitandloss": "Profit","position_size": 70,
        "per_pip_value": 100,"pip": 4.07,"swap_per_days": 1,
        "value": -44.71,"adj": 0.2,"adjisted_swap": -44.51,"month": "Feb","month_profit": "FebProfit"
        },

        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-02-18","type": "Buy","symbol": "XAUUSD","lot_size": 0.70,
        "open": 4975.51,"close": 4995.80,"swap": -44.56,"pnl": 1375.74,
        "max_drawdown": 0.00,"cumulative_balance": 261277.68,"cum_profit": 11277.68,
        "return": 4.5,"profitandloss": "Profit","position_size": 70,
        "per_pip_value": 100,"pip": 20.29,"swap_per_days": 1,
        "value": -44.71,"adj": 0.15,"adjisted_swap": -44.56,"month": "Feb","month_profit": "FebProfit"
        },

        # ===== 2026-02-19 =====
        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-02-19","type": "Sell","symbol": "EURUSD","lot_size": 1.00,
        "open": 1.18006,"close": 1.17672,"swap": 0.00,"pnl": 334.00,
        "max_drawdown": 0.00,"cumulative_balance": 261611.68,"cum_profit": 11611.68,
        "return": 4.6,"profitandloss": "Profit","position_size": 10,
        "per_pip_value": 10,"pip": 33.40,"swap_per_days": 0,
        "value": 0,"adj": 0,"adjisted_swap": 0,"month": "Mar","month_profit": "MarProfit"
        },


# ===== 2026-02-20 =====
        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-02-20","type": "Buy","symbol": "XAUUSD","lot_size": 0.70,
        "open": 5006.47,"close": 5182.69,"swap": -178.69,"pnl": 12156.71,
        "max_drawdown": 0.00,"cumulative_balance": 285134.16,"cum_profit": 35134.16,
        "return": 14.1,"profitandloss": "Profit","position_size": 70,
        "per_pip_value": 100,"pip": 176.22,"swap_per_days": 4,
        "value": -178.84,"adj": 0.15,"adjisted_swap": -178.69,
        "month": "Feb","month_profit": "FebProfit"
        },

        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-02-20","type": "Buy","symbol": "XAUUSD","lot_size": 0.70,
        "open": 5017.43,"close": 5193.23,"swap": -223.85,"pnl": 12082.16,
        "max_drawdown": 0.00,"cumulative_balance": 297216.32,"cum_profit": 47216.32,
        "return": 18.9,"profitandloss": "Profit","position_size": 70,
        "per_pip_value": 100,"pip": 175.80,"swap_per_days": 5,
        "value": -223.55,"adj": -0.3,"adjisted_swap": -223.85,
        "month": "Feb","month_profit": "FebProfit"
        },

        # ===== 2026-02-24 =====
        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-02-24","type": "Sell","symbol": "EURUSD","lot_size": 1.00,
        "open": 1.17792,"close": 1.18053,"swap": 0.00,"pnl": -261.00,
        "max_drawdown": -0.09,"cumulative_balance": 296955.32,"cum_profit": 46955.32,
        "return": 18.8,"profitandloss": "Loss","position_size": 10,
        "per_pip_value": 10,"pip": -26.10,"swap_per_days": 0,
        "value": 0,"adj": 0,"adjisted_swap": 0,
        "month": "Mar","month_profit": "MarLoss"
        },

        # ===== 2026-02-25 =====
        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-02-25","type": "Buy","symbol": "XAUUSD","lot_size": 0.80,
        "open": 5185.20,"close": 5164.82,"swap": -51.40,"pnl": -1681.80,
        "max_drawdown": -0.57,"cumulative_balance": 295273.52,"cum_profit": 45273.52,
        "return": 18.1,"profitandloss": "Loss","position_size": 80,
        "per_pip_value": 100,"pip": -20.38,"swap_per_days": 1,
        "value": -51.10,"adj": -0.3,"adjisted_swap": -51.40,
        "month": "Feb","month_profit": "FebLoss"
        },

        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-02-25","type": "Buy","symbol": "XAUUSD","lot_size": 0.80,
        "open": 5152.06,"close": 5347.50,"swap": -357.52,"pnl": 15277.68,
        "max_drawdown": 0.00,"cumulative_balance": 310551.20,"cum_profit": 60551.20,
        "return": 24.2,"profitandloss": "Profit","position_size": 80,
        "per_pip_value": 100,"pip": 195.44,"swap_per_days": 7,
        "value": -357.67,"adj": 0.15,"adjisted_swap": -357.52,
        "month": "Feb","month_profit": "FebProfit"
        },

        # ===== 2026-02-26 =====
        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-02-26","type": "Buy","symbol": "EURUSD","lot_size": 1.00,
        "open": 1.17990,"close": 1.18193,"swap": 0.00,"pnl": 203.00,
        "max_drawdown": 0.00,"cumulative_balance": 310754.20,"cum_profit": 60754.20,
        "return": 24.3,"profitandloss": "Profit","position_size": 10,
        "per_pip_value": 10,"pip": 20.30,"swap_per_days": 0,
        "value": 0,"adj": 0,"adjisted_swap": 0,
        "month": "Mar","month_profit": "MarProfit"
        },

        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-02-26","type": "Buy","symbol": "XAUUSD","lot_size": 0.80,
        "open": 5198.32,"close": 5234.71,"swap": -50.95,"pnl": 2860.25,
        "max_drawdown": 0.00,"cumulative_balance": 313614.45,"cum_profit": 63614.45,
        "return": 25.4,"profitandloss": "Profit","position_size": 80,
        "per_pip_value": 100,"pip": 36.39,"swap_per_days": 1,
        "value": -51.10,"adj": 0.15,"adjisted_swap": -50.95,
        "month": "Feb","month_profit": "FebProfit"
        },

        # ===== 2026-03-02 =====
        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-03-02","type": "Buy","symbol": "XAUUSD","lot_size": 0.80,
        "open": 5324.99,"close": 5324.72,"swap": 0.00,"pnl": -21.60,
        "max_drawdown": -0.01,"cumulative_balance": 313592.85,"cum_profit": 63592.85,
        "return": 25.4,"profitandloss": "Loss","position_size": 80,
        "per_pip_value": 100,"pip": -0.27,"swap_per_days": 0,
        "value": 0,"adj": 0,"adjisted_swap": 0,
        "month": "Mar","month_profit": "MarLoss"
        },

        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-03-02","type": "Sell","symbol": "EURUSD","lot_size": 1.00,
        "open": 1.17111,"close": 1.16811,"swap": 0.00,"pnl": 300.00,
        "max_drawdown": 0.00,"cumulative_balance": 313892.85,"cum_profit": 63892.85,
        "return": 25.6,"profitandloss": "Profit","position_size": 10,
        "per_pip_value": 10,"pip": 30.00,"swap_per_days": 0,
        "value": 0,"adj": 0,"adjisted_swap": 0,
        "month": "Mar","month_profit": "MarProfit"
        },

        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-03-02","type": "Buy","symbol": "XAUUSD","lot_size": 0.80,
        "open": 5315.66,"close": 5327.74,"swap": -51.40,"pnl": 915.00,
        "max_drawdown": 0.00,"cumulative_balance": 314807.86,"cum_profit": 64807.86,
        "return": 25.9,"profitandloss": "Profit","position_size": 80,
        "per_pip_value": 100,"pip": 12.08,"swap_per_days": 1,
        "value": -51.10,"adj": -0.3,"adjisted_swap": -51.40,
        "month": "Mar","month_profit": "MarProfit"
        },


        

        # ===== 2026-03-03 =====
        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-03-03","type": "Buy","symbol": "XAUUSD","lot_size": 0.80,
        "open": 5156.67,"close": 5161.13,"swap": -102.49,"pnl": 254.31,
        "max_drawdown": 0.00,"cumulative_balance": 315062.16,"cum_profit": 65062.16,
        "return": 26.0,"profitandloss": "Profit","position_size": 80,
        "per_pip_value": 100,"pip": 4.46,"swap_per_days": 2,
        "value": -102.19,"adj": -0.3,"adjisted_swap": -102.49,"month": "Mar","month_profit": "MarProfit"
        },

        # ===== 2026-03-05 =====
        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-03-05","type": "Sell","symbol": "XAUUSD","lot_size": 0.80,
        "open": 5076.74,"close": 5184.29,"swap": 168.15,"pnl": -8435.85,
        "max_drawdown": -2.75,"cumulative_balance": 306626.31,"cum_profit": 56626.31,
        "return": 22.7,"profitandloss": "Loss","position_size": 80,
        "per_pip_value": 100,"pip": -107.55,"swap_per_days": 5,
        "value": 168.00,"adj": 0.15,"adjisted_swap": 168.15,"month": "Mar","month_profit": "MarLoss"
        },

        # ===== 2026-03-10 =====
        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-03-10","type": "Sell","symbol": "XAUUSD","lot_size": 0.80,
        "open": 5175.18,"close": 5179.09,"swap": 33.75,"pnl": -279.05,
        "max_drawdown": -0.09,"cumulative_balance": 306347.26,"cum_profit": 56347.26,
        "return": 22.5,"profitandloss": "Loss","position_size": 80,
        "per_pip_value": 100,"pip": -3.91,"swap_per_days": 1,
        "value": 33.60,"adj": 0.15,"adjisted_swap": 33.75,"month": "Mar","month_profit": "MarLoss"
        },

        # ===== 2026-03-12 =====
        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-03-12","type": "Sell","symbol": "XAUUSD","lot_size": 0.80,
        "open": 5142.95,"close": 5012.69,"swap": 134.55,"pnl": 10555.35,
        "max_drawdown": 0.00,"cumulative_balance": 316902.61,"cum_profit": 66902.61,
        "return": 26.8,"profitandloss": "Profit","position_size": 80,
        "per_pip_value": 100,"pip": 130.26,"swap_per_days": 4,
        "value": 134.40,"adj": 0.15,"adjisted_swap": 134.55,"month": "Mar","month_profit": "MarProfit"
        },

        # ===== 2026-03-17 =====
        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-03-17","type": "Sell","symbol": "XAUUSD","lot_size": 0.90,
        "open": 5005.84,"close": 4827.57,"swap": 75.30,"pnl": 16119.60,
        "max_drawdown": 0.00,"cumulative_balance": 333022.21,"cum_profit": 83022.21,
        "return": 33.2,"profitandloss": "Profit","position_size": 90,
        "per_pip_value": 100,"pip": 178.27,"swap_per_days": 2,
        "value": 75.60,"adj": -0.3,"adjisted_swap": 75.30,"month": "Mar","month_profit": "MarProfit"
        },

        # ===== 2026-03-18 =====
        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-03-18","type": "Sell","symbol": "XAUUSD","lot_size": 0.90,
        "open": 4998.65,"close": 4763.83,"swap": 37.95,"pnl": 21171.75,
        "max_drawdown": 0.00,"cumulative_balance": 354193.96,"cum_profit": 104193.96,
        "return": 41.7,"profitandloss": "Profit","position_size": 90,
        "per_pip_value": 100,"pip": 234.82,"swap_per_days": 1,
        "value": 37.80,"adj": 0.15,"adjisted_swap": 37.95,"month": "Mar","month_profit": "MarProfit"
        },

        # ===== 2026-03-20 =====
        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-03-20","type": "Sell","symbol": "XAUUSD","lot_size": 0.90,
        "open": 4706.37,"close": 4563.93,"swap": 0.00,"pnl": 12819.60,
        "max_drawdown": 0.00,"cumulative_balance": 367013.56,"cum_profit": 117013.56,
        "return": 46.8,"profitandloss": "Profit","position_size": 90,
        "per_pip_value": 100,"pip": 142.44,"swap_per_days": 0,
        "value": 0,"adj": 0,"adjisted_swap": 0,"month": "Mar","month_profit": "MarProfit"
        },

        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-03-20","type": "Sell","symbol": "XAUUSD","lot_size": 0.90,
        "open": 4583.22,"close": 4251.30,"swap": 38.00,"pnl": 29910.80,
        "max_drawdown": 0.00,"cumulative_balance": 396924.36,"cum_profit": 146924.36,
        "return": 58.8,"profitandloss": "Profit","position_size": 90,
        "per_pip_value": 100,"pip": 331.92,"swap_per_days": 1,
        "value": 37.80,"adj": 0.2,"adjisted_swap": 38.00,"month": "Mar","month_profit": "MarProfit"
        },

        # ===== 2026-03-23 =====
        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-03-23","type": "Buy","symbol": "XAUUSD","lot_size": 0.90,
        "open": 4461.87,"close": 4441.23,"swap": -57.33,"pnl": -1914.93,
        "max_drawdown": -0.48,"cumulative_balance": 395009.43,"cum_profit": 145009.43,
        "return": 58.0,"profitandloss": "Loss","position_size": 90,
        "per_pip_value": 100,"pip": -20.64,"swap_per_days": 1,
        "value": -57.48,"adj": 0.15,"adjisted_swap": -57.33,"month": "Mar","month_profit": "MarLoss"
        },

        # ===== 2026-03-24 =====
        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-03-24","type": "Buy","symbol": "XAUUSD","lot_size": 0.90,
        "open": 4347.25,"close": 4411.65,"swap": 0.00,"pnl": 5796.00,
        "max_drawdown": 0.00,"cumulative_balance": 400805.43,"cum_profit": 150805.43,
        "return": 60.3,"profitandloss": "Profit","position_size": 90,
        "per_pip_value": 100,"pip": 64.40,"swap_per_days": 0,
        "value": 0,"adj": 0,"adjisted_swap": 0,"month": "Mar","month_profit": "MarProfit"
        },

        # ===== 2026-03-25 =====
        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-03-25","type": "Buy","symbol": "XAUUSD","lot_size": 0.90,
        "open": 4563.20,"close": 4510.78,"swap": 0.00,"pnl": -4717.80,
        "max_drawdown": -1.19,"cumulative_balance": 396087.63,"cum_profit": 146087.63,
        "return": 58.4,"profitandloss": "Loss","position_size": 90,
        "per_pip_value": 100,"pip": -52.42,"swap_per_days": 0,
        "value": 0,"adj": 0,"adjisted_swap": 0,"month": "Mar","month_profit": "MarLoss"
        },

        # ===== 2026-03-26 =====
        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-03-26","type": "Buy","symbol": "XAUUSD","lot_size": 0.90,
        "open": 4535.72,"close": 4423.09,"swap": 0.00,"pnl": -10136.70,
        "max_drawdown": -2.63,"cumulative_balance": 385950.93,"cum_profit": 135950.93,
        "return": 54.4,"profitandloss": "Loss","position_size": 90,
        "per_pip_value": 100,"pip": -112.63,"swap_per_days": 0,
        "value": 0,"adj": 0,"adjisted_swap": 0,"month": "Mar","month_profit": "MarLoss"
        },

        {
        "trade_id": "TRD-" + uuid.uuid4().hex[:8].upper(),
        "date": "2026-03-26","type": "Sell","symbol": "XAUUSD","lot_size": 0.90,
        "open": 4438.31,"close": 4390.02,"swap": 0.00,"pnl": 4346.10,
        "max_drawdown": 0.00,"cumulative_balance": 390297.03,"cum_profit": 140297.03,
        "return": 56.1,"profitandloss": "Profit","position_size": 90,
        "per_pip_value": 100,"pip": 48.29,"swap_per_days": 0,
        "value": 0,"adj": 0,"adjisted_swap": 0,"month": "Mar","month_profit": "MarProfit"
        }


    ]

    # =========================
    # CHART
    # =========================
    chart = [{"date": t["date"], "return": t["return"]} for t in trades]

    # =========================
    # SUMMARY
    # =========================
    total_pnl = sum(t["pnl"] for t in trades)
    total_swap = sum(t["swap"] for t in trades)

    doc = {
        "account_id": "portfolio1",
        "trades": trades,
        "chart": chart,
        "summary": {
            "total_swap": total_swap,
            "total_pnl": total_pnl
        },
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }

    result = await collection.insert_one(doc)
    print("Inserted ID:", result.inserted_id)


if __name__ == "__main__":
    asyncio.run(insert_exact_sheet_data())