import json
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Optional


class MessageType(StrEnum):
    INIT = "init"
    TOOLS_LIST = "tools_list"
    TOOL_CALL = "tool_call"
    RESULT = "result"
    ERROR = "error"


@dataclass
class Message:
    type: MessageType
    data: dict[str, Any]
    id: Optional[str] = None

    def to_json(self) -> str:
        return json.dumps({"type": self.type.value, "data": self.data, "id": self.id})

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls(type=MessageType(data["type"]), data=data["data"], id=data.get("id"))


class Tool:
    def __init__(self, name: str, description: str, parameters: dict[str, Any]):
        self.name = name
        self.description = description
        self.parameters = parameters

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }
