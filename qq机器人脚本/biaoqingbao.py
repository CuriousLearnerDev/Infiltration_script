from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.plugin import on_command
from pathlib import Path
matcher = on_command("表情包")

@matcher.handle()
async def handle_picture():
    # 本地图片位置
    path = Path("/home/kali/qq/qq/qq/plugins/biaoqingbao.jpeg")
    # 构造图片消息段
    image = MessageSegment.image(path)
    # 发送图片
    await matcher.finish(image)