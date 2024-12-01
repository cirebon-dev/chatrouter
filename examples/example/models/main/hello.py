# -*-coding:utf8;-*-
from models.main import chatbot


@chatbot.add_command("hello")
def hello() -> str:
    return "hello world!"


@chatbot.add_command("hello {name}")
def hello_name(name: str) -> str:
    return f"hello {name}!"
