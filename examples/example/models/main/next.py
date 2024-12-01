# -*-coding:utf8;-*-
from models.main import chatbot
import chatrouter
from db import user


@chatbot.add_command("/next", description="go next group!")
def next() -> str:
    n = chatrouter.util.invoke("next", "/start")
    if n:
        user.session = "next"
        return str(n)
    else:
        return "access denied!"
