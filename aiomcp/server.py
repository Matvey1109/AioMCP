import asyncio

from .protocol import Message, MessageType
from .tool_manager import ToolManager


class AioMCPServer:
    def __init__(self, name: str = "aiomcp"):
        self.name = name
        self.tool_manager = ToolManager()

    async def handle_message(self, message: Message) -> Message:
        if message.type == MessageType.INIT:
            return Message(
                type=MessageType.RESULT,
                data={"status": "ready", "server": self.name},
                id=message.id,
            )

        elif message.type == MessageType.TOOLS_LIST:
            return Message(
                type=MessageType.RESULT,
                data={
                    "tools": [tool.to_dict() for tool in self.tool_manager.list_tools()]
                },
                id=message.id,
            )

        elif message.type == MessageType.TOOL_CALL:
            tool_name = message.data.get("name")
            arguments = message.data.get("arguments", {})
            print(f"Server: Executing {tool_name}")

            try:
                result = await self.tool_manager.execute_tool(tool_name, arguments)
                return Message(
                    type=MessageType.RESULT, data={"result": result}, id=message.id
                )
            except Exception as e:
                return Message(
                    type=MessageType.ERROR, data={"error": str(e)}, id=message.id
                )

        else:
            return Message(
                type=MessageType.ERROR,
                data={"error": f"Unknown message type: {message.type}"},
                id=message.id,
            )

    async def handle_connection(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        try:
            while True:
                data = await reader.readline()
                if not data:
                    break

                message = Message.from_json(data.decode().strip())
                response = await self.handle_message(message)

                writer.write(response.to_json().encode() + b"\n")
                await writer.drain()

        except Exception as e:
            print(f"Connection error: {e}")
        finally:
            writer.close()
            await writer.wait_closed()

    async def start_server(self, host: str, port: int):
        server = await asyncio.start_server(self.handle_connection, host, port)
        print(f"AioMCP Server running on {host}:{port}")

        async with server:
            await server.serve_forever()
