# -*-coding:utf8;-*-
from typing import Any, Callable, Union
import re
"""
Simple but useful router for chatbot.
"""

__author__ = "guangrei"
__version__ = "v0.0.5"

_data: dict = {}  # chatrouter storage
data_user: Any = None  # data user storage
_start_template_ = """
Welcome to {name}!
			
{description}
			
hints: type /help to show help messages.
"""
_help_template_ = """
Router group: {group}
List public commands:
"""


class group:
    """
    class ini digunakan untuk membuat command group
    """

    def __init__(self, name: str, description: str = "no description!") -> None:
        """
        fungsi ini adalah kelas konstruktor
        """
        self.start_msg = _start_template_.format(
            name=name, description=description).strip()
        if name not in _data:
            _data[name] = {}
            _data[name]["/start"] = {}
            _data[name]["/start"]["callback"] = self._start
            _data[name]["/start"]["description"] = "start command!"
            _data[name]["/start"]["strict"] = True
            _data[name]["/help"] = {}
            _data[name]["/help"]["callback"] = self._help
            _data[name]["/help"]["description"] = "help command!"
            _data[name]["/help"]["strict"] = True
        self.id = name

    def add_command(self,  route: str, description: str = "", strict: bool = False) -> Callable:
        """
        fungsi untuk menambahkan command
        """
        method = util.compile(route)

        def dec(func: Callable) -> Callable:
            _data[self.id][method] = {}
            _data[self.id][method]["callback"] = func
            _data[self.id][method]["description"] = description
            _data[self.id][method]["strict"] = strict
            return func
        return dec

    def add_default_command(self) -> Callable:
        """
        fungsi untuk menambahkan default command
        """
        def dec(func: Callable) -> Callable:
            _data[self.id]["__default__"] = {}
            _data[self.id]["__default__"]["callback"] = func
            return func
        return dec

    def _help(self) -> str:
        """
        fungsi ini sebagai default callback /help commands.
        hanya menampilkan publik commands (command yang diawali dengan "/" dan memiliki deskripsi)
        """
        hasil = _help_template_.format(group=self.id).strip()
        i = 1
        for k, v in _data[self.id].items():
            if k.startswith("/") and len(v["description"]):
                hasil = hasil + f'\n{i}. {k} - {v["description"]}'
                i = i+1
        return hasil.strip()

    def _start(self) -> str:
        """
        fungsi ini sebagai default callback /start commands
        """
        return self.start_msg


class util:
    """
    class ini berisi utilitas
    """
    def get_func(group: str, route: str) -> Callable:
        """
        fungsi utilitas ini dapat digunakan untuk mengambil callback pada group dan route tertentu
        """
        route = util.compile(route)
        return _data[group][route]["callback"]
        
    def compile(string: str) -> str:
        """
        fungsi ini untuk mengcompile regex pattern
        """
        pattern = re.sub(r'\{([^}]+)\}', r'(.*)', string)
        return pattern.strip()
        
    def group_exists(name: str) -> bool:
        """
        fungsi ini untuk mengecek group
        """
        return name in _data
        
    def command_exists(group: str, command: str) -> bool:
        """
        fungsi ini untuk mengecek command
        """
        command = util.compile(command)
        return command in _data[group]
    
    def remove_command(group: str, command: str) -> None:
        """
        fungsi ini untuk menghapus command
        """
        command = util.compile(command)
        del _data[group][command]

    def _route(pattern: str, string: str, strict: bool) -> Union[list, bool]:
        """
        fungsi ini private dan berfungsi sebagai route
        """
        if strict:
            match = re.match(pattern, string.strip())
        else:
            match = re.match(pattern, string.strip(), re.IGNORECASE)
        if match:
            return list(match.groups())
        else:
            return False


def run(route: group, msg: str) -> Union[str, None]:
    """
    ini adalah fungsi utama untuk interpretasi chatrouter
    """
    if len(msg):
        for k, v in _data[route.id].items():
            if k != "__default__":
                args = util._route(k, msg, v["strict"])
                if args is not False:
                    return v["callback"](*args)
    if "__default__" in _data[route.id]:
        return _data[route.id]["__default__"]["callback"](msg)
    else:
        return f"info: no default handler for route {route.id}:{msg}"


if __name__ == '__main__':
    pass
