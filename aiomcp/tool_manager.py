from typing import Any

from .protocol import Tool
from .tool_services import AddService, EchoService, SayHelloService, ToolService


class ToolManager:
    def __init__(self):
        self._tools: dict[str, Tool] = {}
        self._services: dict[str, ToolService] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        # Echo tool
        self.register_tool(
            Tool(
                name="echo",
                description="Echo back the input text",
                parameters={
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Text to echo back"}
                    },
                    "required": ["text"],
                },
            ),
            EchoService(),
        )

        # Add tool
        self.register_tool(
            Tool(
                name="add",
                description="Add two numbers",
                parameters={
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "First number"},
                        "b": {"type": "number", "description": "Second number"},
                    },
                    "required": ["a", "b"],
                },
            ),
            AddService(),
        )

        # Say Hello tool
        self.register_tool(
            Tool(
                name="say_hello",
                description="Generate a greeting message",
                parameters={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Name to greet"}
                    },
                    "required": ["name"],
                },
            ),
            SayHelloService(),
        )

    def register_tool(self, tool: Tool, service: ToolService):
        self._tools[tool.name] = tool
        self._services[tool.name] = service

    def get_tool(self, name: str) -> Tool:
        return self._tools[name]

    def list_tools(self) -> list[Tool]:
        return list(self._tools.values())

    async def execute_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        if tool_name not in self._services:
            raise ValueError(f"Unknown tool: {tool_name}")

        service = self._services[tool_name]
        return await service.execute(arguments)
