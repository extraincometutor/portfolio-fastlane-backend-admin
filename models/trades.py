
from os.path import abspath, join, dirname
from sys import path, exc_info
base_dir = abspath(join(dirname(__file__), "../"))
path.append(base_dir)


from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from typing import List


class TradeCreate(BaseModel):
    account_id: str
  

class TradeUpdate(BaseModel):
    account_id: str
    trade_id: Optional[str] = None  
    date: Optional[str] = None      
    type: str
    symbol: str
    lot_size: float
    open_price: float
    close_price: float
    swap: Optional[float] = 0.0
    profit_loss: float
    max_drawdown: float
    cumulative_balance: float
    cum_profit: float
    return_data: float
    profitandloss: str
    position_size: float
    per_pip_value: float
    pip: float
    swap_per_days: float
    value: float
    adj:float
    adjisted_swap:float
    month: str
    month_profit:str


class TradeDelete(BaseModel):
    account_id: str
    trade_id: str



class AccountRequest(BaseModel):
    account_id: str
