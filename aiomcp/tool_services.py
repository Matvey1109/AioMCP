from abc import ABC, abstractmethod
from typing import Any


class ToolService(ABC):
    @abstractmethod
    async def execute(self, arguments: dict[str, Any]) -> Any:
        pass


class EchoService(ToolService):
    async def execute(self, arguments: dict[str, Any]) -> str:
        return f"Echo: {arguments['text']}"


class AddService(ToolService):
    async def execute(self, arguments: dict[str, Any]) -> Any:
        return arguments["a"] + arguments["b"]


class SayHelloService(ToolService):
    async def execute(self, arguments: dict[str, Any]) -> Any:
        name = arguments["name"]
        return f"Hello, {name}!"
