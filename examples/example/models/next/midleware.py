# -*-coding:utf8;-*-
from models.next import chatbot
from db import user


@chatbot.midleware()
def check() -> bool:
    if not user.is_login:
        return False
    else:
        return True
