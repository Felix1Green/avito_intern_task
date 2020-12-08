from typing import Optional, List
import aiohttp


class NetworkWorker:
    @staticmethod
    async def get_region_id(region: str) -> (int, bool):
        """
        returns the region id from the external service by passing region:str param

        if the response from api was not json serializable or it does not have correct keys,
        returns success with `False` value

        otherwise, returns `True` with region id param
        """
        url = f'https://www.avito.ru/api/1/slocations?limit=10&query={region}&key' \
              f'=ZaeC8aidairahqu2Eeb1quee9einaeFieboocohX'
        async with aiohttp.ClientSession() as requests:
            async with requests.get(url) as response:
                try:
                    serialized_resp = await response.json()
                except ValueError:
                    return 0, False
                if 'result' in serialized_resp and 'locations' in serialized_resp['result'] \
                        and len(serialized_resp['result']['locations']) > 0:
                    return serialized_resp['result']['locations'][0].get('id'), True
                return 0, False

    @staticmethod
    async def get_search_ref(search_path: str, region: int, top: int = 5, *args, **kwargs) -> (int, Optional[List], bool):
        """
        returns the search_path reference(add amount:int, top adds:List, success:bool)
        by search_path, region id and top amount params

        if the response from api was not json serializable or it does not have correct keys,
        returns success with `False` value

        otherwise, returns `True` with add amount and top adds
        """
        url = f'https://www.avito.ru/api/10/items?locationId={region}&query={search_path}&key' \
              f'=ZaeC8aidairahqu2Eeb1quee9einaeFieboocohX'
        async with aiohttp.ClientSession() as request:
            async with request.get(url) as response:
                try:
                    serialized_resp = await response.json()
                except ValueError:
                    return 0, None, False
        top_result = []
        try:
            result = serialized_resp['result']['mainCount']
            for i, val in enumerate(serialized_resp['result']['items']):
                if len(top_result) >= top:
                    break
                if 'value' not in val or 'title' not in val['value'] or 'uri' not in val['value']:
                    continue
                top_result.append({'title': val['value']['title'], 'uri': val['value']['uri']})
        except KeyError:
            return 0, None, False
        return result, top_result, True
