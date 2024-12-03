# -*-coding:utf8;-*-
from asyncmodels.main import chatbot
import chatrouter
from db import user


@chatbot.add_command("/next", description="go next group!")
async def next() -> str:
    n = await chatrouter.util.async_invoke("next", "/start")
    if n:
        user.session = "next"
        return str(n)
    else:
        return "access denied!"
