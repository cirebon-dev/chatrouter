# -*-coding:utf8;-*-
from models.next import chatbot
from db import user


@chatbot.midleware()
async def check() -> bool:
    if not user.is_login:
        return False
    else:
        return True
