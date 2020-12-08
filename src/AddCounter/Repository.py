from src.Models.ServiceModels import AmountListResponse, TopListResponse
from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime


class Repository(ABC):
    @abstractmethod
    async def create_instance(self, search_path: str, region: int) -> (int, bool):
        """
        creates instance of search path region id bundle and returns new instance id

        returns existing instance id if search path and region bundle already exists
        """
        pass

    @abstractmethod
    async def stat_amount(self, item_id: int, time_from: datetime, time_to: datetime) -> AmountListResponse:
        """returns the history of search path and region bundle amount"""
        pass

    @abstractmethod
    async def set_amount(self, item_id: int, amount: int, add_top: Optional[List]):
        """setting new amount of search path and region bundle as a new row"""
        pass

    @abstractmethod
    async def get_top_by_id(self, item_id: int, time_from: datetime, time_to: datetime) -> TopListResponse:
        """returns history of top adds by id of search path and region bandle"""
        pass
