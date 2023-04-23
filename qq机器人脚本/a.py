import whois



def Whois_check(DNS):
    DNS = DNS.strip()
    # 检查dns前面是不是有http或者有https://，有替换空
    DNS = DNS.replace("http://", '')
    DNS = DNS.replace("https://", '')
    DNS = DNS.replace("/", '')

    try:
        req_whois = whois.whois(DNS)
        # print(req_whois)
        data = f"""
查询的域名是："f{DNS}"
注册商：
    "{str(req_whois["registrar"])}"
域名服务器：
    "{str(req_whois["whois_server"])}"
推荐网址：
    "{str(req_whois["referral_url"])}"
更新时间：
    "{str(req_whois["updated_date"])}"
创建时间：
    "{str(req_whois["creation_date"])}"
过期时间：
    "{str(req_whois["expiration_date"])}"
名称服务器：
    "{str(req_whois["name_servers"])}"
电子邮件：
    "{str(req_whois["emails"])}"
status：
    "{str(req_whois["status"])}"
dnssec：
    "{str(req_whois["dnssec"])}"
名称：
    "{str(req_whois["name"])}"
组织：
    "{str(req_whois["org"])}"
城市：
    "{str(req_whois["city"])}"
国家：
    "{str(req_whois["country"])}"\n"""
        return data

    except Exception as bc:
        return "有错误！错误提示" + str(bc)


from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment, Bot, Event

from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText

ND = on_command("whois", aliases={"whois"}, priority=2, block=True)


@ND.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if plain_text:
        matcher.set_arg("Name", args)  # 如果用户发送了参数则直接赋值


@ND.got("Name", prompt="用法：whois 域名")
async def handle_city(Name: Message = Arg(), sname: str = ArgPlainText("Name")):
    try:

        await ND.send(Whois_check(sname))
    except Exception as e:
        await ND.send("搜图插件出现故障，请联系Mangata")