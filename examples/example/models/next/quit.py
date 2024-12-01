# -*-coding:utf8;-*-
from models.next import chatbot
import chatrouter
from db import user
from typing import Any


@chatbot.add_command("/quit", "exit from next!")
def quit() -> Any:
    user.session = "main"
    return chatrouter.util.invoke("main", "/start")
