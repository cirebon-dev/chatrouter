# -*-coding:utf8;-*-
import chatrouter
from typing import Any
from models.main import chatbot
from db import user


@chatbot.add_default_command()
def default_handler(msg: str) -> Any:
    if len(user.steps):
        user.steps.append(msg)
        return chatrouter.util.get_func(chatbot.id, user.steps[0])()

    c = chatrouter.util.parse_command(msg)
    if c:
        return f"command {c} not found!"
    else:
        return "sorry, i can't get what you says!"
