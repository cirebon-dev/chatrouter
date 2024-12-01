#!/usr/bin/env python
from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

setup(
    name="chatrouter",
    version="v1.0.8",
    description="Typed router for chatbot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="guangrei",
    author_email="myawn@pm.me",
    url="https://github.com/cirebon-dev/chatrouter",
    packages=["chatrouter"],
    package_data={"chatrouter": ["py.typed"]},
    license="MIT",
    platforms="any",
    install_requires=["aiofiles", "typing-extensions", "types-aiofiles"],
)
