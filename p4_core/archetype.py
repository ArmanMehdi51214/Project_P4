from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict


@dataclass(frozen=True)
class ArchetypeParent:
    id: str
    name: str
    function_category: Optional[str]
    ocean_bias: Dict[str, float]
    primary_goal: Optional[str]
    primary_fear: Optional[str]
