# -*-coding:utf8;-*-
import chatrouter
from .pustaka import db
import telebot


chatbot = chatrouter.group("main", "this is main bot")


@chatbot.add_command("/nim_playground", "run nim playground!", strict=True)
def start_nim():
    message = chatrouter.data_user
    db.update_user_session(message.from_user.id, "nim_playground")
    return chatrouter.util.get_func("nim_playground", "/start")()


@chatbot.add_command("/python_playground", "run python playground!", strict=True)
def start_python():
    message = chatrouter.data_user
    db.update_user_session(message.from_user.id, "python_playground")
    return chatrouter.util.get_func("python_playground", "/start")()


@chatbot.add_command("/go_playground", "run go playground!", strict=True)
def start_go():
    message = chatrouter.data_user
    db.update_user_session(message.from_user.id, "go_playground")
    return chatrouter.util.get_func("go_playground", "/start")()


@chatbot.add_default_command()
def default_handle(command):
    command = telebot.util.extract_command(command)
    if command is not None:
        return f"command {command} not found!"
    else:
        return "command not found!"
