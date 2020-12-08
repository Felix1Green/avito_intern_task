from src.AddCounter.Repository import Repository
from src.Models.ServiceModels import TopListResponse, AmountListResponse, SingleAmount, SingleTop
from typing import Optional, List
from datetime import datetime
import asyncpg
import asyncio
import json


class CounterPostgresRepository(Repository):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self._connection_pool: Optional[asyncio.pool.Pool] = None
        self._create_query = """INSERT INTO advertisement (search_string, region) 
                                VALUES ($1,$2) RETURNING ADD_ID;"""
        self._get_stat_query = """SELECT add_num, time_stamp FROM advertisementcounter 
                            where ADD_ID = $1 and time_stamp between $2 and $3"""
        self._get_top_query = """SELECT add_top, time_stamp FROM advertisementcounter 
                                    where ADD_ID = $1 and time_stamp between $2 and $3"""
        self._set_add_query = """INSERT INTO advertisementcounter (ADD_ID, ADD_NUM, ADD_TOP)
                                    VALUES ($1,$2,$3)"""
        self._get_add_id_query = """SELECT ADD_ID FROM advertisement WHERE search_string = $1 AND region = $2"""

    async def create_connections(self, host='localhost', port=5432, user='postgres', password='postgres',
                                 database='postgres'):
        if self._connection_pool:
            return
        self._connection_pool = await asyncpg.create_pool(user=user, password=password, host=host,
                                                          port=port, database=database)

    async def close_connections(self):
        if self._connection_pool:
            await self._connection_pool.close()

    async def create_instance(self, search_path: str, region: int) -> (int, bool):
        if not self._connection_pool:
            raise ConnectionError
        async with self._connection_pool.acquire() as conn:
            try:
                add_raw_id = await conn.fetchval(self._create_query, search_path, region)
            except asyncpg.exceptions.UniqueViolationError:
                add_raw_id = await conn.fetchval(self._get_add_id_query, search_path, region)
        if not isinstance(add_raw_id, int):
            return 0, False
        return add_raw_id, True

    async def stat_amount(self, item_id: int, time_from: datetime, time_to: datetime) -> AmountListResponse:
        if not self._connection_pool:
            raise ConnectionError
        async with self._connection_pool.acquire() as conn:
            db_rows = await conn.fetch(self._get_stat_query, item_id, time_from, time_to)
        result = AmountListResponse(counter_rows=[])
        for i in db_rows:
            result.counter_rows.append(SingleAmount(**i))
        return result

    async def set_amount(self, item_id: int, amount: int, add_top: Optional[List]):
        if not self._connection_pool:
            raise ConnectionError
        if not isinstance(add_top, list):
            add_top = []
        async with self._connection_pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(self._set_add_query, item_id, amount, json.dumps(add_top))

    async def get_top_by_id(self, item_id: int, time_from: datetime, time_to: datetime) -> TopListResponse:
        if not self._connection_pool:
            raise ConnectionError
        async with self._connection_pool.acquire() as conn:
            rows = await conn.fetch(self._get_top_query, item_id, time_from, time_to)
        result = TopListResponse(rows=[])
        for i in rows:
            try:
                result.rows.append(SingleTop(top=json.loads(i['add_top']), time_stamp=i['time_stamp']))
            except (TypeError, ValueError):
                continue
        return result
