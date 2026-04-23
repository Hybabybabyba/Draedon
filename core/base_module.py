from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any
from datetime import datetime

@dataclass
class module_result:
    module: str
    target: str
    success: bool
    data: dict[str, Any]
    error: str=""
    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

class base_module(ABC):
    name: str="base"
    description: str=""
    accepts: list[str]=[]

    @abstractmethod
    def run(self, target: str) -> module_result:
        pass

    def can_handle(self, target_type: str) -> bool:
        return target_type in self.accepts
    
    def ok(self, target: str, data: dict) ->module_result:
        return module_result(
            module=self.name,
            target=target,
            success=True,
            data=data
        )
    
    def fail(self, target: str, error: str) -> module_result:
        return module_result(
            module=self.name,
            target=target,
            success=False,
            data={},
            error=error
        )
