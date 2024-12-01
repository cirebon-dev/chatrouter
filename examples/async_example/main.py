# -*-coding:utf8;-*-
import chatrouter
from db import user
import asyncio

chatrouter.autoloader("models")


async def main() -> None:
    w = await chatrouter.async_run(chatrouter.group("main"), "/start")
    print(w)
    while True:
        try:
            i = input("you: ")
            r = await chatrouter.async_run(chatrouter.group(user.session), i)
            print(f"bot: {r}")
        except BaseException as e:
            print(f"\nbot: {type(e).__name__}: {str(e)}")
            exit(0)


if __name__ == "__main__":
    asyncio.run(main())
