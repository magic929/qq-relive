import httpx

from .config import plugin_config

set_api = f'{plugin_config.base_url}{plugin_config.boss_info_path}{plugin_config.set_api}'

async def set_boss(key1, key2):
    print(key1, key2, set_api)
    paydata = {"url": key1}
    params = {"other_name": key2}
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(set_api, json=paydata, params=params)
            print(res.status_code)
            if res.status_code != 200:
                return False
        return True
    
    except (httpx.HTTPError, KeyError):
        return False