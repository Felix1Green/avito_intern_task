from pydantic import BaseModel
from datetime import datetime
from typing import List


class AddInput(BaseModel):
    """models that represents the api input for creating new search path and region bundle"""
    search_path: str
    region: str


class SingleAmount(BaseModel):
    """model that represents the single amount for search_path and region bundle"""
    add_num: int
    time_stamp: datetime


class SingleTop(BaseModel):
    """model that represents the single top of adds for search path and region bundle"""
    top: List[dict]
    time_stamp: datetime


class AddCorrectResponse(BaseModel):
    """model that represents the server response with instance id after creation"""
    item_id: int


class IncorrectInputResponse(BaseModel):
    """model that represents error message from server"""
    message: str


class TopListResponse(BaseModel):
    """model that represents server response with top adds history"""
    rows: List[SingleTop]


class AmountListResponse(BaseModel):
    """models that represents server response with amount history"""
    counter_rows: List[SingleAmount]
