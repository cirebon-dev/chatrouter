# -*-coding:utf8;-*-
from asyncmodels.next import chatbot
import chatrouter
from db import user
from typing import Any


@chatbot.add_command("/quit", "exit from next!")
async def quit() -> Any:
    user.session = "main"
    ret = await chatrouter.util.async_invoke("main", "/start")
    return ret
