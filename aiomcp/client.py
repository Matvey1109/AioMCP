import asyncio
from typing import Any

from .protocol import Message, MessageType


class AioMCPClient:
    def __init__(self):
        self.reader = None
        self.writer = None
        self.message_id = 0

    async def connect(self, host: str, port: int):
        self.reader, self.writer = await asyncio.open_connection(host, port)

        init_msg = Message(
            type=MessageType.INIT, data={"client": "aiomcp-client"}, id=self._next_id()
        )

        response = await self.send_message(init_msg)
        print(f"Connected: {response.data}")

    def _next_id(self) -> str:
        self.message_id += 1
        return str(self.message_id)

    async def send_message(self, message: Message) -> Message:
        self.writer.write(message.to_json().encode() + b"\n")
        await self.writer.drain()

        response_data = await self.reader.readline()
        return Message.from_json(response_data.decode().strip())

    async def list_tools(self) -> list:
        msg = Message(type=MessageType.TOOLS_LIST, data={}, id=self._next_id())

        response = await self.send_message(msg)
        return response.data["tools"]

    async def call_tool(self, tool_name: str, arguments: dict) -> Any:
        msg = Message(
            type=MessageType.TOOL_CALL,
            data={"name": tool_name, "arguments": arguments},
            id=self._next_id(),
        )

        response = await self.send_message(msg)
        if response.type == MessageType.ERROR:
            raise Exception(response.data["error"])

        return response.data["result"]

    async def close(self):
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
