# -*-coding:utf8;-*-
from .pustaka import db
import requests
import chatrouter


chatbot = chatrouter.group(
    "go_playground", description="now you can send me go code :)")


def run_go(code):
    api = "https://play.golang.org/compile"
    payload = {"body": code.strip()}
    r = requests.post(api, json=payload).json()
    if r['Errors'] == "":
        res = ""
        for v in r['Events']:
            res = res + v["Message"]
        return res.strip()
    else:
        return r['Errors'].strip()


@chatbot.add_command("/quit", description="exit from python playground!", strict=True)
def quit_handler():
    message = chatrouter.data_user
    db.update_user_session(message.from_user.id, "main")
    return chatrouter.util.get_func("main", "/start")()


@chatbot.add_default_command()
def default_handler(code):
    return run_go(code)
