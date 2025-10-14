# AioMCP

A lightweight, asynchronous Model Context Protocol (MCP) implementation in Python built with asyncio.

## What is MCP?

The **Model Context Protocol (MCP)** is an open protocol that enables AI assistants to connect with external data sources and tools. Think of it as a standardized way for AI models to interact with your applications, databases, APIs, and services.

📚 **Learn more about MCP**:
+ https://modelcontextprotocol.io/docs/getting-started/intro
+ https://en.wikipedia.org/wiki/Model_Context_Protocol

## Features

- 🚀 **Asynchronous by design** - Built on asyncio for high performance
- 🔧 **Extensible tool system** - Easily add custom tools and services
- 📡 **Simple protocol** - Clean JSON-based communication
- 🔌 **Client & Server** - Complete implementation of both sides

## Quick Start

### Running the Example

**Start the server:**
```bash
python main.py server
```

**In another terminal, run the client:**
```bash
python main.py client
```

## Project Structure

```
aiomcp/
├── protocol.py         # Message types and serialization
├── tool_services.py    # Abstract tool service classes
├── tool_manager.py     # Tool registration and management
├── server.py           # MCP server implementation
├── client.py           # MCP client implementation
main.py                 # Entry point for examples
```

## Available Tools

AioMCP comes with three example tools:

1. **`echo`** - Echo back input text
2. **`add`** - Add two numbers
3. **`say_hello`** - Generate greeting messages

## Creating Custom Tools

### 1. Create a Tool Service

```python
from aiomcp.tool_services import ToolService

class CustomToolService(ToolService):
    async def execute(self, arguments: dict[str, Any]) -> Any:
        # Your tool logic here
        return "Result"
```

### 2. Register Your Tool

```python
from aiomcp.tool_manager import ToolManager
from aiomcp.protocol import Tool

tool_manager = ToolManager()
tool_manager.register_tool(
    Tool(
        name="custom_tool",
        description="My custom tool",
        parameters={
            "type": "object",
            "properties": {
                "param1": {"type": "string", "description": "First parameter"}
            },
            "required": ["param1"]
        }
    ),
    CustomToolService()
)
```

## Use Cases

- 🤖 **AI Assistant Integration** - Connect LLMs to your tools
- 🔌 **Plugin Systems** - Dynamic tool discovery and execution
- 🏗 **Microservices** - Lightweight RPC between services
- 🧪 **Testing** - Mock external services in tests
