from src.Models.ServiceModels import AddInput, AmountListResponse, TopListResponse
from abc import ABC, abstractmethod
from fastapi import BackgroundTasks
from typing import Optional, Any
from datetime import datetime


class UseCase(ABC):
    @abstractmethod
    async def add_instance(self, instance: AddInput, back_tasks: BackgroundTasks) -> (int, bool):
        """
        adding search instance with unique search path and region to database and
        runs background task for updating state of the instance

        returns (instance_id: int, success: bool)

        if input was incorrect returns success with `False` value

        if everything fine, runs async background tasks to update instances
        """
        pass

    @abstractmethod
    async def update_instance(self, add_amt: Any, item_id: int, **kwargs):
        """
        updates search path amount

        setting new amount if input is Tuple with 3 fields - add amount: int, top adds: Optional[List], success: bool
        returns None
        """

    @abstractmethod
    async def stat_amount(self, item_id: int, time_from: datetime, time_to: datetime) -> AmountListResponse:
        """
        returns the statistics of search path and region bundle id

        if time duration not `None` returns list of `amount` history
        """
        pass

    @abstractmethod
    async def get_top_adds(self, item_id: int, time_from: datetime, time_to: datetime) -> Optional[TopListResponse]:
        """
        returns the statistics of top adds by search_path and region bundle id

        if time duration not None returns list of top adds history
        """
        pass
