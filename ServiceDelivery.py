from src.Models.ServiceModels import AddInput, AddCorrectResponse, IncorrectInputResponse, AmountListResponse, \
    TopListResponse
from src.AddCounter.repository.CounterRepository import CounterPostgresRepository
from src.AddCounter.usecase.CounterUseCase import CounterUseCase
from fastapi import FastAPI, Depends, BackgroundTasks
from src.AddCounter.UseCase import UseCase
from typing import List, Optional
from datetime import datetime
import uvicorn
import os

app = FastAPI()


class GetUseCase:
    @classmethod
    async def create_uc(cls) -> UseCase:
        if not hasattr(cls, 'uc'):
            db_config = get_config_from_environ(['POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_DB'],
                                                ['user', 'password', 'db'])
            rep = CounterPostgresRepository()
            await rep.create_connections('postgresql', '5432', db_config['user'],
                                         db_config['password'], db_config['db'])
            cls.rep = rep
            cls.uc = CounterUseCase(rep)
        return cls.uc

    @classmethod
    async def clean_mem(cls):
        if hasattr(cls, 'rep'):
            await cls.rep.close_connections()


def get_config_from_environ(environ_schema: List[str], object_schema: List[str]) -> dict:
    result = {}
    for index, val in enumerate(environ_schema):
        result[object_schema[index]] = os.getenv(val)
    return result


@app.post("/add/")
async def create_add(body: AddInput, background_tasks: BackgroundTasks, use_case=Depends(GetUseCase.create_uc)):
    item_id, ok = await use_case.add_instance(body, background_tasks)
    if ok:
        return AddCorrectResponse(item_id=item_id)
    return IncorrectInputResponse(message="incorrect input!")


@app.get("/stat/", response_model=Optional[AmountListResponse])
async def get_stat(item_id: int, time_from: str, time_to: str, use_case=Depends(GetUseCase.create_uc)):
    try:
        parsed_time_from = datetime.strptime(time_from, '%Y-%m-%d:%H-%M')
        parsed_time_to = datetime.strptime(time_to, '%Y-%m-%d:%H-%M')
    except ValueError:
        return None
    resp_list = await use_case.stat_amount(item_id, parsed_time_from, parsed_time_to)
    if resp_list:
        return resp_list


@app.get("/top/", response_model=Optional[TopListResponse])
async def get_top_adds(item_id: int, time_from: str, time_to: str, use_case=Depends(GetUseCase.create_uc)):
    try:
        parsed_time_from = datetime.strptime(time_from, '%Y-%m-%d:%H-%M')
        parsed_time_to = datetime.strptime(time_to, '%Y-%m-%d:%H-%M')
    except ValueError:
        return None
    add_list = await use_case.get_top_adds(item_id, parsed_time_from, parsed_time_to)
    if add_list:
        return add_list


@app.on_event("shutdown")
async def stop_workers():
    await GetUseCase.clean_mem()


if __name__ == '__main__':
    uvicorn.run(app, host='', port=8080, log_level='info')
