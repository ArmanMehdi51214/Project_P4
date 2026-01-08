from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class WorldCell:
    x: int
    y: int
    geo_data: Dict[str, Any]
    game_heuristics: Optional[Dict[str, Any]] = None

    @property
    def biome_code(self) -> Optional[int]:
        v = self.geo_data.get("biome_code")
        return int(v) if v is not None else None

    @property
    def human_density(self) -> Optional[float]:
        v = self.geo_data.get("human_density")
        return float(v) if v is not None else None

    @property
    def elevation(self) -> Optional[float]:
        v = self.geo_data.get("elevation")
        return float(v) if v is not None else None

    @property
    def roughness(self) -> Optional[float]:
        v = self.geo_data.get("roughness")
        return float(v) if v is not None else None

    @property
    def is_water(self) -> Optional[bool]:
        v = self.geo_data.get("is_water")
        return bool(v) if v is not None else None
