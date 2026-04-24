from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any
from datetime import datetime

@dataclass
class module_result:
    module_name: str
    target: str
    success: bool
    result_data: dict[str, Any]
    error: str = ""
    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

class base_module(ABC):
    name: str = "base"
    description: str = ""
    supported_types: list[str] = []

    @abstractmethod
    def run(self, target: str) -> module_result:
        pass

    def can_handle(self, target_type: str) -> bool:
        return target_type in self.supported_types

    def ok(self, target: str, data: dict) -> module_result:
        return module_result(
            module_name=self.name,
            target=target,
            success=True,
            result_data=data,
        )

    def fail(self, target: str, error: str) -> module_result:
        return module_result(
            module_name=self.name,
            target=target,
            success=False,
            result_data={},
            error=error,
        )
