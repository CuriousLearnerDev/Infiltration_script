from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import Message

word=on_keyword({"信息收集"})

@word.handle()
async def _():
    help="""信息收集：
whois查询：
子域名探测："""
    await word.finish(Message(help))