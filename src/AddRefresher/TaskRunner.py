import asyncio
from typing import Callable


class PeriodicTaskRunner:
    def __init__(self, func: Callable, callback: Callable, time_delay: int = 3600):
        self._func = func
        self._delay = time_delay
        self._finish_callback = callback

    async def run(self, **kwargs):
        """background task with sleep timer for running async functions with finish callbacks"""
        while True:
            result = await self._func(**kwargs)
            await self._finish_callback(result, **kwargs)
            await asyncio.sleep(self._delay)
