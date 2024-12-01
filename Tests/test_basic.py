# -*- coding: utf-8 -*-
import unittest
import chatrouter


chatbot = chatrouter.group("test", "this is test bot!")


@chatbot.add_command("hello")
def hello() -> str:  # noqa
    return "hello world!"


@chatbot.add_command("hello {name}")
def hello_name(name: str) -> str:  # noqa
    return f"hello {name}!"


@chatbot.add_default_command()
def default_handler(command: str) -> str:  # noqa
    return f"command {command} not found!"


class Chatrouterest(unittest.TestCase):
    def test_response_one(self) -> None:
        response = chatrouter.run(chatbot, "hello")
        self.assertEqual(response, "hello world!")

    def test_response_two(self) -> None:
        response = chatrouter.run(chatbot, "hello user")
        self.assertEqual(response, "hello user!")

    def test_response_default(self) -> None:
        response = chatrouter.run(chatbot, "test")
        self.assertEqual(response, "command test not found!")
