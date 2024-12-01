# -*-coding:utf8;-*-
from db import user
from models.main import chatbot


username = "admin"
password = "123"


@chatbot.add_command(
    "/login", description="login to access protected group!", strict=True
)
async def login() -> str:
    if user.is_login:
        return "you are already logged in, type /logout to logged out!"

    if len(user.steps) < 2 or user.steps[0] != "/login":
        user.steps = ["/login"]
        return "please enter username.."
    if len(user.steps) == 2:
        if user.steps[1] != username:
            user.steps = []
            return "invalid user name, please type /login to retry!"
        else:
            return "please enter password.."

    if len(user.steps) == 3:
        if user.steps[2] != password:
            user.steps = []
            return "invalid password, please type /login to retry!"
        else:
            user.is_login = True
            user.steps = []
            return "login success!"
    return "ok"


@chatbot.add_command("/logout", strict=True)
async def logout() -> str:
    if not user.is_login:
        return "you aren't logged in, please type /login !"
    else:
        user.is_login = False
        return "success logged out!"
