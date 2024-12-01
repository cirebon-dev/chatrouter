# -*-coding:utf8;-*-
from typing import List, Union
from typing_extensions import Never


class user:
    session: str = "main"
    steps: List[Union[Never, str]] = []
    is_login: bool = False
