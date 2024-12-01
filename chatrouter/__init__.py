# -*-coding:utf8;-*-
from typing import Any, Callable, Dict, Optional, List, Union, Type, Pattern
from typing_extensions import Self, Never
import re
import inspect
from abc import ABC, abstractmethod
import os
import importlib.util
import aiofiles


###############################################################################
# Simple but useful router for chatbot. ##########################################################
###############################################################################

__author__ = "guangrei"

__version__ = "v1.0.5"

###############################################################################
# Storage ##########################################################
###############################################################################

_data: Dict[str, Any] = {}  # chatrouter storage

data_user: Dict[str, Any] = {}  # data user storage

###############################################################################
# Interface ##########################################################
###############################################################################


class MultiLanguage(ABC):
    data: Dict[str, Dict[str, Callable[..., str]]]

    def __init_subclass__(cls: Type[Self], **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "data"):
            raise NotImplementedError

    @abstractmethod
    def __init__(self, domain: str) -> None:
        pass

    @abstractmethod
    def translate(self, text: str, target: str) -> Union[str, Callable[..., str]]:
        """
        menerjemahkan text secara otomatis
        """
        pass

    @classmethod
    @abstractmethod
    def gettext(
        cls: Type[Self], id: str, default: str = "null", instance: Optional[Self] = None
    ) -> Union[str, Callable[..., str]]:
        """
        mendapatkan text secara dinamis berdasarkan id.
        """
        pass


class AsyncMultiLanguage(ABC):
    data: Dict[str, Dict[str, Callable[..., str]]]

    def __init_subclass__(cls: Type[Self], **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "data"):
            raise NotImplementedError

    @abstractmethod
    def __init__(self, domain: str) -> None:
        pass

    @abstractmethod
    async def translate(self, text: str, target: str) -> Union[str, Callable[..., str]]:
        """
        menerjemahkan text secara otomatis
        """
        pass

    @classmethod
    @abstractmethod
    async def gettext(
        cls: Type[Self], id: str, default: str = "null", instance: Optional[Self] = None
    ) -> str:
        """
        mendapatkan text secara dinamis berdasarkan id.
        """
        pass


###############################################################################
# Template ##########################################################
###############################################################################


class template:
    tpl_start = """
    Welcome to `{name}`!
			    
    {description}
			    
    hints: type /help to show help messages.
    """

    tpl_help = """
    List public commands for route-group {group}:
    """

    tpl_warn_default = """
    warning: no default handler for route-group `{id}:{msg}`!
    """


###############################################################################
# Core Class ##########################################################
###############################################################################


class group:
    """
    class ini digunakan untuk membuat command group
    """

    def __init__(
        self,
        name: str,
        description: Optional[Union[str, MultiLanguage, AsyncMultiLanguage]] = None,
        asynchronous: bool = False,
    ) -> None:
        """
        fungsi ini adalah kelas konstruktor
        """

        self._async = asynchronous
        self.description = description

        if description is None:
            start_name = "start command!"
            help_name = "help command!"
        elif isinstance(description, str):
            start_name = "start command!"
            help_name = "help command!"
        else:
            start_name = description  # type: ignore[assignment]
            help_name = description  # type: ignore[assignment]

        if name not in _data:
            _data[name] = {}
            hashid = str(hash("/start"))
            _data[name][hashid] = {}

            if not asynchronous:
                _data[name][hashid]["callback"] = self._start
            else:
                _data[name][hashid]["callback"] = self._async_start

            _data[name][hashid]["description"] = start_name
            _data[name][hashid]["att"] = "/start"
            _data[name][hashid]["strict"] = True
            _data[name][hashid]["pattern"] = util.compile("/start", strict=True)
            hashid = str(hash("/help"))
            _data[name][hashid] = {}

            if not asynchronous:
                _data[name][hashid]["callback"] = self._help
            else:
                _data[name][hashid]["callback"] = self._async_help

            _data[name][hashid]["description"] = help_name
            _data[name][hashid]["att"] = "/help"
            _data[name][hashid]["strict"] = True
            _data[name][hashid]["pattern"] = util.compile("/help", strict=True)

        self.id = name

    def add_command(
        self,
        route: Union[str, List[str]],
        description: Optional[Union[str, MultiLanguage]] = None,
        strict: bool = False,
        regex: bool = False,
    ) -> Callable[..., Any]:
        """
        fungsi untuk menambahkan command
        """

        def dec(func: Callable[..., Any]) -> Callable[..., Any]:
            if self._async and not inspect.iscoroutinefunction(func):
                raise ValueError("function must be awaitable!")

            elif not self._async and inspect.iscoroutinefunction(func):
                raise ValueError(
                    "coroutine function is not supported in synchronous mode!"
                )
            if isinstance(route, str):
                keyroute = str(hash(route))
                pattern = util.compile(route, regex=regex, strict=strict)
                _data[self.id][keyroute] = {}
                _data[self.id][keyroute]["callback"] = func
                _data[self.id][keyroute]["description"] = description
                _data[self.id][keyroute]["att"] = route
                _data[self.id][keyroute]["strict"] = strict
                _data[self.id][keyroute]["pattern"] = pattern
            else:
                for i in route:
                    keyroute = str(hash(i))
                    pattern = util.compile(i, regex=regex, strict=strict)
                    _data[self.id][keyroute] = {}
                    _data[self.id][keyroute]["callback"] = func
                    _data[self.id][keyroute]["description"] = description
                    _data[self.id][keyroute]["att"] = i
                    _data[self.id][keyroute]["strict"] = strict
                    _data[self.id][keyroute]["pattern"] = pattern
            return func

        return dec

    def add_default_command(self) -> Callable[..., Any]:
        """
        fungsi untuk menambahkan default command
        """

        def dec(func: Callable[..., Any]) -> Callable[..., Any]:
            if self._async and not inspect.iscoroutinefunction(func):
                raise ValueError("function must be awaitable!")

            elif not self._async and inspect.iscoroutinefunction(func):
                raise ValueError(
                    "coroutine function is not supported in synchronous mode!"
                )

            _data[self.id]["__default__"] = {}
            _data[self.id]["__default__"]["callback"] = func
            return func

        return dec

    def midleware(self) -> Callable[..., Any]:
        """
        fungsi untuk menambahkan midleware
        """

        def dec(func: Callable[..., Any]) -> Callable[..., Any]:
            if self._async and not inspect.iscoroutinefunction(func):
                raise ValueError("function must be awaitable!")

            elif not self._async and inspect.iscoroutinefunction(func):
                raise ValueError(
                    "coroutine function is not supported in synchronous mode!"
                )

            _data[self.id]["__midleware__"] = {}
            _data[self.id]["__midleware__"]["callback"] = func
            return func

        return dec

    def _start(self) -> str:
        """
        fungsi ini sebagai default callback /start commands
        """
        d = self.description
        if d is None:
            render = template.tpl_start.format(
                name=self.id.title(), description="no description!"
            )
        elif isinstance(d, str):
            render = template.tpl_start.format(name=self.id, description=d)
        else:
            render = d.gettext(self.id)  # type: ignore[assignment]
            render = render.format(name=self.id, description="no description!")
        return util.strip_text(render)

    async def _async_start(self) -> str:
        """
        fungsi ini sebagai default callback /start commands
        """

        d = self.description
        if d is None:
            render = template.tpl_start.format(
                name=self.id.title(), description="no description!"
            )
        elif isinstance(d, str):
            render = template.tpl_start.format(name=self.id, description=d)
        else:
            render = await d.gettext(self.id)  # type: ignore[misc]
            render = render.format(name=self.id, description="no description!")
        ret = await util.async_strip_text(render)
        return ret

    def _help(self) -> str:
        """
        fungsi ini sebagai default callback /help commands.
        hanya menampilkan publik commands (command yang diawali dengan "/" dan memiliki deskripsi)
        """

        render = template.tpl_help.format(group=self.id.title())
        hasil = util.strip_text(render)
        i = 1
        helps = util.list_public_commands(self.id)
        for k, v in helps.items():
            hasil = hasil + f"\n{i}. {k} - {v}"
            i = i + 1
        hasil = hasil + "\n\npowered by `chatrouter`."
        return hasil.strip()

    async def _async_help(self) -> str:
        """
        fungsi ini sebagai default callback /help commands.
        hanya menampilkan publik commands (command yang diawali dengan "/" dan memiliki deskripsi)
        """

        render = template.tpl_help.format(group=self.id.title())
        hasil = await util.async_strip_text(render)
        i = 1
        helps = await util.async_list_public_commands(self.id)
        for k, v in helps.items():
            hasil = hasil + f"\n{i}. {k} - {v}"
            i = i + 1
        hasil = hasil + "\n\npowered by `chatrouter`."
        return hasil.strip()


###############################################################################
# Core Functions ##########################################################
###############################################################################


def add_command(
    route: str,
    description: Optional[Union[str, MultiLanguage, AsyncMultiLanguage]] = None,
    strict: bool = False,
    group_route: str = "main",
    asynchronous: bool = False,
    regex: bool = False,
) -> Callable[..., Any]:
    """
    fungsi untuk menambahkan command secara cepat
    """

    group(group_route, asynchronous=asynchronous)

    def dec(func: Callable[..., Any]) -> Callable[..., Any]:
        if asynchronous and not inspect.iscoroutinefunction(func):
            raise ValueError("function must be awaitable!")
        elif not asynchronous and inspect.iscoroutinefunction(func):
            raise ValueError("coroutine function is not supported in synchronous mode!")

        if isinstance(route, str):
            keyroute = str(hash(route))
            pattern = util.compile(route, regex=regex, strict=strict)
            _data[group_route][keyroute] = {}
            _data[group_route][keyroute]["callback"] = func
            _data[group_route][keyroute]["description"] = description
            _data[group_route][keyroute]["att"] = route
            _data[group_route][keyroute]["strict"] = strict
            _data[group_route][keyroute]["pattern"] = pattern
        else:
            for i in route:
                keyroute = str(hash(i))
                pattern = util.compile(i, regex=regex, strict=strict)
                _data[group_route][keyroute] = {}
                _data[group_route][keyroute]["callback"] = func
                _data[group_route][keyroute]["description"] = description
                _data[group_route][keyroute]["att"] = i
                _data[group_route][keyroute]["strict"] = strict
                _data[group_route][keyroute]["pattern"] = pattern
        return func

    return dec


def add_default_command(
    group_route: str = "main", asynchronous: bool = False
) -> Callable[..., Any]:
    """
    fungsi untuk menambahkan default command secara cepat
    """

    group(group_route, asynchronous=asynchronous)

    def dec(func: Callable[..., Any]) -> Callable[..., Any]:
        if asynchronous and not inspect.iscoroutinefunction(func):
            raise ValueError("function must be awaitable!")
        elif not asynchronous and inspect.iscoroutinefunction(func):
            raise ValueError("coroutine function is not supported in synchronous mode!")
        _data[group_route]["__default__"] = {}
        _data[group_route]["__default__"]["callback"] = func
        return func

    return dec


def midleware(
    group_route: str = "main", asynchronous: bool = False
) -> Callable[..., Any]:
    """
    fungsi untuk menambahkan midleware secara cepat
    """

    group(group_route, asynchronous=asynchronous)

    def dec(func: Callable[..., Any]) -> Callable[..., Any]:
        if asynchronous and not inspect.iscoroutinefunction(func):
            raise ValueError("function must be awaitable!")

        elif not asynchronous and inspect.iscoroutinefunction(func):
            raise ValueError("coroutine function is not supported in synchronous mode!")

        _data[group_route]["__midleware__"] = {}
        _data[group_route]["__midleware__"]["callback"] = func
        return func

    return dec


def autoloader(path: str) -> List[Union[str, Never]]:
    """
    ini adalah fungsi untuk meload file python secara otomatis.
    """
    loaded: List[Union[str, Never]] = []
    rc = re.compile("@.*add_command")
    rd = re.compile("@.*add_default_command")
    rm = re.compile("@.*midleware")
    patterns = (rc, rd, rm)

    def is_loadable(codes: List[str]) -> bool:
        for code in codes:
            for pattern in patterns:
                if pattern.match(code):
                    return True
        return False

    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name.endswith(".py") and file_name != "__init__.py":
                pyfile = os.path.join(root, file_name)
                with open(pyfile, "r") as f:
                    codes = f.readlines()
                if is_loadable(codes):
                    spec = importlib.util.spec_from_file_location(
                        "chatrouterapp", pyfile
                    )
                    if spec is not None:
                        mod = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(mod)  # type: ignore[union-attr]
                    loaded.append(pyfile)
    return loaded


async def async_autoloader(path: str) -> List[Union[str, Never]]:
    """
    Asynchronous version chatrouter.autoloader.
    """
    loaded: List[Union[str, Never]] = []
    rc = re.compile("@.*add_command")
    rd = re.compile("@.*add_default_command")
    rm = re.compile("@.*midleware")
    patterns = (rc, rd, rm)

    async def is_loadable(codes: List[str]) -> bool:
        for code in codes:
            for pattern in patterns:
                if pattern.match(code):
                    return True
        return False

    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name.endswith(".py") and file_name != "__init__.py":
                pyfile = os.path.join(root, file_name)
                async with aiofiles.open(pyfile, mode="r") as f:
                    codes = await f.readlines()
                do_load = await is_loadable(codes)
                if do_load:
                    spec = importlib.util.spec_from_file_location(
                        "chatrouterapp", pyfile
                    )
                    if spec is not None:
                        mod = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(mod)  # type: ignore[union-attr]
                    loaded.append(pyfile)
    return loaded


def run(route: group, msg: str) -> Any:
    """
    ini adalah fungsi utama untuk interpretasi chatrouter
    """

    if "__midleware__" in _data[route.id]:
        coba = _data[route.id]["__midleware__"]["callback"]()

        if coba is not True:
            return coba

    if len(msg):
        for k, v in _data[route.id].items():
            if k not in ("__default__", "__midleware__"):
                args = util._route(v["pattern"], msg)

                if args is not False:
                    return v["callback"](*args)

    if "__default__" in _data[route.id]:
        return _data[route.id]["__default__"]["callback"](msg)
    else:
        render = template.tpl_warn_default.format(id=route.id, msg=msg)
        return render.strip()


async def async_run(route: group, msg: str) -> Any:
    """
    Asynchronous version chatrouter.run.
    """

    if "__midleware__" in _data[route.id]:
        coba = await _data[route.id]["__midleware__"]["callback"]()

        if coba is not True:
            return coba

    if len(msg):
        for k, v in _data[route.id].items():
            if k not in ("__default__", "__midleware__"):
                args = await util._async_route(v["pattern"], msg)
                if args is not False:
                    ret = await v["callback"](*args)
                    return ret

    if "__default__" in _data[route.id]:
        ret = await _data[route.id]["__default__"]["callback"](msg)
        return ret
    else:
        render = template.tpl_warn_default.format(id=route.id, msg=msg)
        return render.strip()


###############################################################################
# Utilities ##########################################################
###############################################################################


class util:
    """
    class ini berisi utilitas
    """

    @staticmethod
    def strip_text(text: str) -> str:
        """
        Multi line text strip.
        """
        t = text.split("\n")
        result = []
        for i in t:
            result.append(i.strip())
        return "\n".join(result)

    @staticmethod
    async def async_strip_text(text: str) -> str:
        """
        Asynchronous version chatrouter.util.strip_text.
        """
        t = text.split("\n")
        result = []
        for i in t:
            result.append(i.strip())
        return "\n".join(result)

    @staticmethod
    def parse_command(text: str) -> Union[str, None]:
        """
        fungsi untuk memisahkan command dari text
        """

        if text.startswith("/"):
            command = text.split(" ")[0]
            command = command.split("@")[0]
            return command.strip()
        else:
            return None

    @staticmethod
    async def async_parse_command(text: str) -> Union[str, None]:
        """
        Asynchronous version chatrouter.util.parse_command.
        """

        if text.startswith("/"):
            command = text.split(" ")[0]
            command = command.split("@")[0]
            return command.strip()
        else:
            return None

    @staticmethod
    def parse_text(text: str) -> Union[str, None]:
        """
        fungsi memisahkan text dari command
        """
        if text.startswith("/"):
            res: List[str] = text.split(" ")
            if len(res) > 1:
                del res[0]
                text = " ".join(res)
                return text.strip()
            else:
                return None
        else:
            return None

    @staticmethod
    async def async_parse_text(text: str) -> Union[str, None]:
        """
        Asynchronous version chatrouter.util.parse_text.
        """
        if text.startswith("/"):
            res: List[str] = text.split(" ")
            if len(res) > 1:
                del res[0]
                text = " ".join(res)
                return text.strip()
            else:
                return None
        else:
            return None

    @staticmethod
    def parse_mention(text: str) -> List[Union[str, Never]]:
        """
        fungsi memisahkan mention dari text
        """
        result: List[Union[str, Never]] = []
        words = text.split()
        for word in words:
            if word.startswith("@"):
                result.append(word[1:])
        return result

    @staticmethod
    async def async_parse_mention(text: str) -> List[Union[str, Never]]:
        """
        Asynchronous version chatrouter.util.parse_mention.
        """
        result: List[Union[str, Never]] = []
        words = text.split()
        for word in words:
            if word.startswith("@"):
                result.append(word[1:])
        return result

    @staticmethod
    def parse_hastag(text: str) -> List[Union[str, Never]]:
        """
        fungsi memisahkan hastag dari text
        """
        result: List[Union[str, Never]] = []
        words = text.split()
        for word in words:
            if word.startswith("#"):
                result.append(word[1:])
        return result

    @staticmethod
    async def async_parse_hastag(text: str) -> List[Union[str, Never]]:
        """
        Asynchronous version chatrouter.util.parse_hastag.
        """
        result: List[Union[str, Never]] = []
        words = text.split()
        for word in words:
            if word.startswith("#"):
                result.append(word[1:])
        return result

    @staticmethod
    def list_public_commands(id: str) -> Dict[str, str]:
        """
        get public commands by id.
        """
        result: Dict[str, str] = {}
        for k, v in _data[id].items():
            if k in ("__default__", "__midleware__"):
                continue

            if v["att"].startswith("/") and v["description"]:
                d = v["description"]
                if isinstance(v["description"], str):
                    des = d
                else:
                    des = d.gettext(k)
                result[v["att"]] = des
        return result

    @staticmethod
    async def async_list_public_commands(id: str) -> Dict[str, str]:
        """
        Asynchronous version chatrouter.util.list_public_commands.
        """
        result: Dict[str, str] = {}
        for k, v in _data[id].items():
            if k in ("__default__", "__midleware__"):
                continue

            if v["att"].startswith("/") and v["description"]:
                d = v["description"]
                if isinstance(v["description"], str):
                    des = d
                else:
                    des = await d.gettext(k)
                result[k] = des
        return result

    @staticmethod
    def get_func(group: str, route: str) -> Callable[..., Any]:
        """
        fungsi utilitas ini dapat digunakan untuk mengambil callback pada group dan route tertentu
        """

        route = str(hash(route))
        return _data[group][route]["callback"]  # type: ignore[no-any-return]

    @staticmethod
    async def async_get_func(group: str, route: str) -> Callable[..., Any]:
        """
        Asynchronous version chatrouter.util.get_func.
        """

        route = str(hash(route))
        return _data[group][route]["callback"]  # type: ignore[no-any-return]

    @staticmethod
    def invoke(group: str, route: str, *args: Any, **kwargs: Any) -> Any:
        """
        fungsi utilitas ini dapat digunakan untuk invoke callback pada group dan route tertentu
        """
        if not util.group_exists(group):
            raise ValueError

        if "__midleware__" in _data[group]:
            call_midleware = _data[group]["__midleware__"]["callback"]()

            if call_midleware is not True:
                return call_midleware

        route = str(hash(route))
        callback = _data[group][route]["callback"]
        return callback(*args, **kwargs)

    @staticmethod
    async def async_invoke(group: str, route: str, *args: Any, **kwargs: Any) -> Any:
        """
        Asynchronous version chatrouter.util.invoke.
        """
        exists = await util.async_group_exists(group)

        if not exists:
            raise ValueError

        if "__midleware__" in _data[group]:
            call_midleware = await _data[group]["__midleware__"]["callback"]()

            if call_midleware is not True:
                return call_midleware

        route = str(hash(route))
        callback = _data[group][route]["callback"]
        ret = await callback(*args, **kwargs)
        return ret

    @staticmethod
    def compile(string: str, regex: bool = False, strict: bool = False) -> Pattern[str]:
        """
        fungsi ini untuk mengcompile regex pattern
        """
        if not regex:
            ret = re.sub(r"\{([^}]+)\}", r"(.*)", string)
            ret = re.escape(ret)
            ret = ret.replace(r"\(\.\*\)", "(.*)")
            if not strict:
                return re.compile("^" + ret.strip() + "$", flags=re.IGNORECASE)
            else:
                return re.compile("^" + ret.strip() + "$")
        else:
            if not strict:
                return re.compile(string.strip(), flags=re.IGNORECASE)
            else:
                return re.compile(string.strip())

    @staticmethod
    async def async_compile(
        string: str, regex: bool = False, strict: bool = False
    ) -> Pattern[str]:
        """
        Asynchronous version chatrouter.util.compile.
        """
        if not regex:
            ret = re.sub(r"\{([^}]+)\}", r"(.*)", string)
            ret = re.escape(ret)
            ret = ret.replace(r"\(\.\*\)", "(.*)")
            if not strict:
                return re.compile("^" + ret.strip() + "$", flags=re.IGNORECASE)
            else:
                return re.compile("^" + ret.strip() + "$")
        else:
            if not strict:
                return re.compile(string.strip(), flags=re.IGNORECASE)
            else:
                return re.compile(string.strip())

    @staticmethod
    def group_exists(name: str) -> bool:
        """
        fungsi ini untuk mengecek group
        """

        return name in _data

    @staticmethod
    async def async_group_exists(name: str) -> bool:
        """
        Asynchronous version chatrouter.util.group_exists.
        """

        return name in _data

    @staticmethod
    def command_exists(group: str, command: str) -> bool:
        """
        fungsi ini untuk mengecek command
        """

        command = str(hash(command))
        return command in _data[group]

    @staticmethod
    async def async_command_exists(group: str, command: str) -> bool:
        """
        Asynchronous version chatrouter.util.command_exists.
        """

        command = str(hash(command))
        return command in _data[group]

    @staticmethod
    def remove_command(group: str, command: str) -> None:
        """
        fungsi ini untuk menghapus command
        """

        command = str(hash(command))
        del _data[group][command]

    @staticmethod
    async def async_remove_command(group: str, command: str) -> None:
        """
        Asynchronous version chatrouter.util.remove_command.
        """

        command = str(hash(command))
        del _data[group][command]

    @staticmethod
    def _route(pattern: Pattern[str], string: str) -> Union[List[str], bool]:
        """
        fungsi ini private dan berfungsi sebagai route
        """

        match = pattern.match(string.strip())
        if match:
            return list(match.groups())
        else:
            return False

    @staticmethod
    async def _async_route(
        pattern: Pattern[str], string: str
    ) -> Union[List[str], bool]:
        """
        Asynchronous version chatrouter.util._route.
        """

        match = pattern.match(string.strip())
        if match:
            return list(match.groups())
        else:
            return False
