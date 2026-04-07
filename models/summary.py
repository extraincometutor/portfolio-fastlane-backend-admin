from os.path import abspath, join, dirname
from sys import path, exc_info
base_dir = abspath(join(dirname(__file__), "../"))
path.append(base_dir)


from pydantic import BaseModel, Field
from typing import Optional




class CreateSummary(BaseModel):
    account_id: str




class AddSummary(BaseModel):
    capital: float
    month: str
    year: int
    opening: float
    net_profit: float
    closing: float
    roi: float
    total_trades: int
    profit_trades: int
    win_rate: float
    max_drawdown: float
    profit_factor: float
    profit: float
    loss: float
    loss_ratio: float
    summary_id: Optional[str] = None 
    account_id: str
   
     


class AccountRequest(BaseModel):
    account_id: str


class DeleteMonthRequest(BaseModel):
    account_id: str
    summary_id: str
