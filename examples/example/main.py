# -*-coding:utf8;-*-
import chatrouter
from db import user

chatrouter.autoloader("models")

if __name__ == "__main__":
    print(chatrouter.run(chatrouter.group("main"), "/start"))
    while True:
        try:
            i = input("you: ")
            r = chatrouter.run(chatrouter.group(user.session), i)
            print(f"bot: {r}")
        except BaseException as e:
            print(f"\nbot: {type(e).__name__}: {str(e)}")
            exit(0)
