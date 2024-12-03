# -*-coding:utf8;-*-
import chatrouter
from typing import Any
from asyncmodels.main import chatbot
from db import user


@chatbot.add_default_command()
async def default_handler(msg: str) -> Any:
    if len(user.steps):
        user.steps.append(msg)
        call = await chatrouter.util.async_get_func(chatbot.id, user.steps[0])
        ret = await call()
        return ret

    c = await chatrouter.util.async_parse_command(msg)
    if c:
        return f"command {c} not found!"
    else:
        return "sorry, i can't get what you says!"
