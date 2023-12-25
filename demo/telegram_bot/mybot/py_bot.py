# -*-coding:utf8;-*-
from .pustaka import db
import requests
import chatrouter


chatbot = chatrouter.group(
    "python_playground", description="now you can send me python code :)")


def run_py(code):
    """
    this playground use https://github.com/healeycodes/untrusted-python
    """
    api = "https://untrusted-python.fly.dev/api/exec"
    payload = {"code": code.strip()}
    r = requests.post(api, json=payload)
    return r.text.strip()


@chatbot.add_command("/quit", description="exit from python playground!", strict=True)
def quit_handler():
    message = chatrouter.data_user
    db.update_user_session(message.from_user.id, "main")
    return chatrouter.util.get_func("main", "/start")()


@chatbot.add_default_command()
def default_handler(code):
    return run_py(code)
