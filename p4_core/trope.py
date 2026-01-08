from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class TropeChild:
    id: str
    name: str
    parent_archetype_raw: Optional[str]  # synonym string (unreliable key)
    description: Optional[str]
    genre_tag: Optional[str]
