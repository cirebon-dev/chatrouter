[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) 
[![status workflow test](https://github.com/cirebon-dev/chatrouter/actions/workflows/python-app.yml/badge.svg)](https://github.com/cirebon-dev/chatrouter/actions) 
[![status workflow build](https://github.com/cirebon-dev/chatrouter/actions/workflows/release_to_pypi.yml/badge.svg)](https://github.com/cirebon-dev/chatrouter/actions)

[![Downloads](https://static.pepy.tech/badge/chatrouter)](https://pepy.tech/project/chatrouter)
[![Downloads](https://static.pepy.tech/badge/chatrouter/month)](https://pepy.tech/project/chatrouter)
[![Downloads](https://static.pepy.tech/badge/chatrouter/week)](https://pepy.tech/project/chatrouter)

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

or

```python
chatrouter.invoke("group", "route", *args, **kwargs)
```

6. auto generated `/start` and `/help` command.

7. object storage `chatrouter.data_user`.

8. support route with regex.

9. support autoloader `chatrouter.autoloader("path")`.

10. support Asynchronous.

11. typed python.

## installation

```
pip install chatrouter
```

## Usage

for usage, please see [examples](https://github.com/cirebon-dev/chatrouter/tree/main/examples) directory.
