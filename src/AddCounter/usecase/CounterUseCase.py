from src.Models.ServiceModels import AddInput, AmountListResponse, TopListResponse
from src.AddRefresher.TaskRunner import PeriodicTaskRunner
from src.AddCounter.Repository import Repository
from src.utils.Network import NetworkWorker
from src.AddCounter.UseCase import UseCase
from fastapi import BackgroundTasks
from typing import Optional, Any
from datetime import datetime


class CounterUseCase(UseCase):
    def __init__(self, repository: Repository):
        self._repository = repository
        self._task_runner = PeriodicTaskRunner(NetworkWorker.get_search_ref, self.update_instance, time_delay=10)

    async def add_instance(self, instance: AddInput, back_tasks: BackgroundTasks) -> (int, bool):
        if not instance.search_path or not instance.region:
            return 0, False
        region_id, ok = await NetworkWorker.get_region_id(instance.region)
        if not ok:
            return 0, False
        resp, ok = await self._repository.create_instance(instance.search_path, region_id)
        if not ok:
            return 0, False
        back_tasks.add_task(self._task_runner.run, search_path=instance.search_path, region=region_id,
                            item_id=resp)
        return resp, ok

    async def update_instance(self, add_amt: Any, item_id: int, **kwargs):
        if isinstance(add_amt, tuple) and len(add_amt) > 2:
            if isinstance(add_amt[0], int) and isinstance(add_amt[2], bool) and add_amt[2]:
                await self._repository.set_amount(item_id, add_amt[0], add_amt[1])

    async def stat_amount(self, item_id: int, time_from: datetime, time_to: datetime) -> Optional[AmountListResponse]:
        if not time_to or not time_from:
            return None
        return await self._repository.stat_amount(item_id, time_from, time_to)

    async def get_top_adds(self, item_id: int, time_from: datetime, time_to: datetime) -> Optional[TopListResponse]:
        if not time_from or not time_to:
            return None
        return await self._repository.get_top_by_id(item_id, time_from, time_to)
