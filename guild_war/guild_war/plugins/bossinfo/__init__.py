from nonebot import CommandGroup
from nonebot.rule import to_me
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp.event import GroupMessageEvent, MessageEvent
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.typing import T_State
import httpx

from .config import plugin_config
from .data_source import set_boss

boss = CommandGroup('boss', block=True)
boss_search = boss.command('search', aliases={"信息"}, rule=to_me())
boss_set = boss.command('set', aliases={"更新"}, rule=to_me())

serach_api = f'{plugin_config.base_url}{plugin_config.boss_info_path}{plugin_config.search_api}'
set_api = f'{plugin_config.base_url}{plugin_config.boss_info_path}{plugin_config.set_api}'


async def serach_boss(key1, key2):
    params = {'name': key1, 'level': key2}
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(serach_api, params=params)
            if res.status_code != 200:
                return None
            res = res.json()
            hp = ""
            teams = ""
            notice = ""
            name = res['name']
            level = res['level']
            if "details" in res:
                notice = res["details"]["notice"]
                if "teams" in res["details"]:
                    for team in res["details"]["teams"]:
                        teams += f'{team["team"]}, {team["turn"]}T'
            if "status" in res:
                hp = res["details"]["hp"]

            return f'{name}\n难度：{level}\n注意事项：{notice}\n推荐队伍：{teams}\n当前血量：{hp}'

    except (httpx.HTTPError, KeyError):
        return None
    

@boss_search.handle()
async def get_first_handle_boss_info(bot: Bot, event: MessageEvent, state: T_State):
    args = str(event.get_message()).strip().split(" ")
    if len(args) == 1:
        if args[0].isdigit():
            state["level"] = args
        else:
            state["name"] = args

    if len(args) == 2:
        state["name"] = args[0]
        state['level'] = args[1]
    
    return False


@boss_search.got("level", prompt="请输入boss难度")
@boss_search.got("name", prompt="请输入boss名字")
async def get_handle_boss_info(bot:Bot, event: MessageEvent, state:T_State):
    result = await serach_boss(state["name"], state["level"])
    if result:
        await boss_search.finish(result)
    await boss_search.reject("查找失败，请输入正确参数")


@boss_set.handle()
async def boss_set_handle(bot: Bot, event: MessageEvent, state: T_State):
    args = str(event.get_message()).strip().split(" ")
    if len(args) == 1:
        if plugin_config.pojie_url in args[0]:
            state["url"] = args[0]
    
    if len(args) >= 2:
        state["url"] = args[0]
        state["other_name"] = args[1:]


@boss_set.got("url", prompt="请输入破解网站对应角色地址")
async def boss_set_do(bot: Bot, event: MessageEvent, state: T_State):
    result = await set_boss(state["url"], state["other_name"])
    if result:
        await boss_set.finish("boss情报已记录")
    await boss_set.reject("boss情报记录失败")