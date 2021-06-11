from nonebot import CommandGroup
from nonebot.rule import to_me
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp.event import GroupMessageEvent, MessageEvent
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.typing import T_State
import httpx

from .config import plugin_config
from .data_source import *

boss = CommandGroup('boss', block=True)
boss_search = boss.command('search', aliases={"信息"}, rule=to_me())
boss_set = boss.command('set', aliases={"更新"}, rule=to_me())
boss_team = boss.command('set_team', aliases={"添加队伍"}, rule=to_me())
boss_notice = boss.command('set_notice', aliases={"添加注意"}, rule=to_me())

serach_api = f'{plugin_config.base_url}{plugin_config.boss_info_path}{plugin_config.search_api}'
set_api = f'{plugin_config.base_url}{plugin_config.boss_info_path}{plugin_config.set_api}'


async def serach_boss(key1, key2):
    params = {'name': key1, 'level': key2}
    try:
        async with httpx.AsyncClient(timeout=10) as client:
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
                        teams += f'{team["team"]}{team["turn"]}T\n                 '
            if "status" in res:
                hp = res["status"]["hp"]

            return f'{name}\n难度：{level}\n注意事项：{notice}\n推荐队伍：{teams.strip()}\n当前血量：{hp}'

    except Exception as e:
        print("error: ", e)
        return False
    

@boss_search.handle()
async def get_first_handle_boss_info(bot: Bot, event: MessageEvent, state: T_State):
    args = str(event.get_message()).strip().split(" ")
    if len(args) == 1:
        await boss_search.reject("请重新输入boss名字和难度")

    if len(args) == 2:
        state["name"] = args[0]
        state['level'] = args[1]
    
    result = await serach_boss(state["name"], state["level"])
    if result:
        await boss_search.finish(result)
    await boss_search.reject("查找失败")



# @boss_search.got()
# async def get_handle_boss_info(bot:Bot, event: MessageEvent, state:T_State):
    


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


@boss_team.args_parser
async def boss_team_parser(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip().split(" ")
    if len(args) < 2:
        await boss_team.reject("请输入队伍和回数")
    state["team"] = args[0]
    state["turn"] = args[1]


@boss_team.handle()
async def boss_set_team_handle(bot: Bot, event: MessageEvent, state: T_State):
    args = str(event.get_message()).strip().split(" ")
    if len(args) < 2:
        await boss_team.reject("请输入boss名字和难度")
    (state['name'], state['level']) = (args[0], args[1])


@boss_team.got('team_turn', prompt="请输入队伍和回数")
async def boss_set_team(bot: Bot, event: Event, state:T_State):
    result = await set_team(state["name"], state["level"], state["team"], state["turn"])
    if result:
        await boss_team.finish(result)
    await boss_team.finish("添加失败")


@boss_notice.handle()
async def boss_set_notice_handle(bot: Bot, event: MessageEvent, state: T_State):
    args = str(event.get_message()).strip().split(" ")
    if len(args) < 2:
        await boss_notice.reject("请输入boss名字和难度")
    (state['name'], state['level']) = (args[0], args[1])


@boss_notice.got('notice', prompt="请输入注意事项")
async def boss_set_notice(bot: Bot, event: MessageEvent, state: T_State):
    result = await set_notice(state["name"], state["level"], state["notice"])
    if result:
        await boss_notice.finish(result)
    await boss_notice.finish("添加失败")