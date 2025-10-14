import asyncio
import sys

from aiomcp.client import AioMCPClient
from aiomcp.server import AioMCPServer

HOST = "localhost"
PORT = 8080


async def run_server():
    server = AioMCPServer()
    await server.start_server(HOST, PORT)


async def run_client():
    client = AioMCPClient()

    try:
        await client.connect(HOST, PORT)

        tools = await client.list_tools()
        print("Available tools:")
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description']}")

        result = await client.call_tool("echo", {"text": "Echo text"})
        print(f"Echo result: {result}")

        result = await client.call_tool("add", {"a": 5, "b": 3})
        print(f"Add result: {result}")

        result = await client.call_tool("say_hello", {"name": "John"})
        print(f"Say hello result: {result}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.close()


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [server|client]")
        return

    mode = sys.argv[1]

    if mode == "server":
        asyncio.run(run_server())
    elif mode == "client":
        asyncio.run(run_client())
    else:
        print("Invalid mode. Use 'server' or 'client'")


if __name__ == "__main__":
    main()
