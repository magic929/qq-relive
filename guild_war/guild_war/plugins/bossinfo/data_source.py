import httpx

from .config import plugin_config

set_api = f'{plugin_config.base_url}{plugin_config.boss_info_path}{plugin_config.set_api}'
set_team_api = f'{plugin_config.base_url}{plugin_config.boss_info_path}{plugin_config.set_team_api}'
set_notice_api = f'{plugin_config.base_url}{plugin_config.boss_info_path}{plugin_config.set_notice_api}'

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


async def set_team(key1, key2, key3, key4):
    paydata = {
        "name": key1,
        "level": key2,
        "team": key3,
        "turn": key4
    }
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(set_team_api, json=paydata)
            res = res.json()
            return res["msg"]
    except Exception as e:
        print("error: ", e)
        return False

async def set_notice(key1, key2, key3):
    paydata = {
        "name": key1,
        "level": key2,
        "notice": key3
    }
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(set_notice_api, json=paydata)
            res = res.json()
            return res["msg"]
    except Exception as e:
        print("error", e)
        return False
