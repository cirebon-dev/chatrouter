[![status workflow test](https://github.com/cirebon-dev/chatrouter/actions/workflows/python-app.yml/badge.svg)](https://github.com/cirebon-dev/chatrouter/actions) 
[![status workflow build](https://github.com/cirebon-dev/chatrouter/actions/workflows/release_to_pypi.yml/badge.svg)](https://github.com/cirebon-dev/chatrouter/actions)
[![Downloads](https://static.pepy.tech/badge/chatrouter)](https://pepy.tech/project/chatrouter)

Chatrouter is an enhanced router for chatbots and easily integrates with any bot library.

## key features

1. turned complexity into simplicity.

from:
```python
if user_session == "A":
    ...
elif user_session == "B":
    ...
elif user_session == "C":
    ...
else:
    ...
```
to:
```python
chatbot = chatrouter.group(user_session)
r = chatrouter.run(chatbot, msg)
```
2. Readable route.

```python
@chatbot.add_command("call me {my_name}")
# or 
chatbot.add_command("call me {my_name} and {my_friend}")
# etc
```

3. case sensitive and insensitive.

default case is `insensitive` but you can add `strict=True` to a route/command to make it case  sensitive.

4. public and private command.

command start with "/" and have description is public command, for example:
```python
@chatbot.add_command("/test", description="test command", strict=True)
```
5. invoke callback anywhere.

```python
func = chatrouter.util.get_func("group_name", "command_name")
```

6. auto generated `/start` and `/help` command.

7. object storage `chatrouter.data_user`.

8. support asynchronous.

## installation

```
pip install chatrouter
```

## quick example

```python
# -*-coding:utf8;-*-
import chatrouter


chatbot = chatrouter.group("test", "this is test bot!")


@chatbot.add_command("call me {name}")
def say_handler(name):
    return f"hello {name}, nice to meet you!"


@chatbot.add_command("repeat me {one} and {two}")
def repeat_handler(one, two):
    return f"ok {one}.. {two}"


@chatbot.add_default_command()
def default_handler(command):
    return f"command {command} not found!"


if __name__ == '__main__':
    print(chatrouter.run(chatbot, "/start"))
    while True:
        try:
            i = input("you: ")
            r = chatrouter.run(chatbot, i)
            print(f"bot: {r}")
        except BaseException as e:
            print("bot: byebye!")
            exit(0)

```
asynchronous example
```python
#-*-coding:utf8;-*-
import asyncio
import chatrouter


chatbot = chatrouter.group("test", asynchronous=True)

@chatbot.add_command("call me {name}")
async def test(name):
    return f"hello {name}!"

async def main():
    user_input = "call me human"
    response = await chatrouter.async_run(chatbot, user_input)
    print(response)

if __name__ == '__main__':
    asyncio.run(main())
```
for more complex example, please open [demo/telegram_bot](https://github.com/cirebon-dev/chatrouter/tree/main/demo/telegram_bot).