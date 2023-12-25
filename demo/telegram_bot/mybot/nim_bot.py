# -*-coding:utf8;-*-
from .pustaka import db
import requests
import chatrouter


chatbot = chatrouter.group(
    "nim_playground", description="now you can send me nim code :)")
success_template = """
Result ✅
---------
{output}
"""
error_template = """
Result ❎
---------
{output}
"""


def run_nim(code):
    """
    run nim  code playground.
    inspired by https://github.com/nim-lang/nimbot/blob/8dbee85051c0ed16544425150841a424761d55d7/src/playground.nim
    """
    api = "https://play.nim-lang.org/compile"
    payload = {"code": code.strip(), "compilationTarget": "c"}
    r = requests.post(api, json=payload).json()
    if "error" in r:
        return False, r["error"]
    log = r["log"]
    compilelog = r["compileLog"]
    success = "success" in compilelog.lower()
    if not success:
        for line in compilelog.split("\n"):
            if "error:" in line.lower():
                return False, line
    return True, log


@chatbot.add_command("/quit", description="exit from nim playground!", strict=True)
def quit_handler():
    message = chatrouter.data_user
    db.update_user_session(message.from_user.id, "main")
    return chatrouter.util.get_func("main", "/start")()


@chatbot.add_default_command()
def default_handler(code):
    res = run_nim(code)
    return res[1].strip()
