#!/usr/bin/env python
import sys
from setuptools import setup
from os import path
import chatrouter


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()
setup(
    name='chatrouter',
    version=chatrouter.__version__,
    description='Router for chatbot',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=chatrouter.__author__,
    author_email='myawn@pm.me',
    url='https://github.com/cirebon-dev/chatrouter',
    py_modules=['chatrouter'],
    # scripts=['chatrouter.py'],
    license='MIT',
    platforms='any',
    # install_requires=["requests"]
)
