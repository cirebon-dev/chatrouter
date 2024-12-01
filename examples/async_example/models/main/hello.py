# -*-coding:utf8;-*-
from models.main import chatbot


@chatbot.add_command("hello")
async def hello() -> str:
    return "hello world!"


@chatbot.add_command("hello {name}")
async def hello_name(name: str) -> str:
    return f"hello {name}!"
