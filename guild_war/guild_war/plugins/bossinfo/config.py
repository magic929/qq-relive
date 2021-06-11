from nonebot import get_driver
from pydantic import BaseSettings


class Config(BaseSettings):

    # plugin custom config
    plugin_setting: str = "default"
    base_url: str = ""
    boss_info_path: str = "v1/bossinfo/"
    search_api: str = "search/boss"
    set_api: str = "set"
    pojie_url: str = "karth.top"
    set_team_api: str = "set/team"
    set_notice_api: str = "set/notice"

    class Config:
        extra = "ignore"

global_config = get_driver().config
plugin_config = Config(**global_config.dict())