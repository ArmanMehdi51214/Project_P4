from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class BiomeDefinition:
    code: int
    name: str
    theme: str
    harshness: float        # 0..1
    population_density: float  # 0..1
    isolation: float        # 0..1


# Master biome registry
BIOME_REGISTRY: Dict[int, BiomeDefinition] = {
    # Transitional / Rural Fringe
    40: BiomeDefinition(
        code=40,
        name="Mixed Rural / Peri-Urban",
        theme="Frontier Hinterland",
        harshness=0.45,
        population_density=0.35,
        isolation=0.4,
    ),

    # Urban & Standard
    50: BiomeDefinition(50, "Built-up Urban", "Cyberpunk Sprawl", 0.6, 0.9, 0.2),
    10: BiomeDefinition(10, "Tree Cover", "Wildlands", 0.4, 0.3, 0.5),
    80: BiomeDefinition(80, "Permanent Water", "The Wasteland", 0.7, 0.1, 0.7),

    # Wasteland Set
    60: BiomeDefinition(60, "Bare / Sparse", "The Wasteland", 0.9, 0.05, 0.8),
    20: BiomeDefinition(20, "Shrubland", "The Wasteland", 0.6, 0.2, 0.6),
    30: BiomeDefinition(30, "Grassland", "Frontier Plains", 0.5, 0.4, 0.4),

    # Extreme Set
    70: BiomeDefinition(70, "Snow & Ice", "Frozen Expanse", 0.95, 0.02, 0.9),
    90: BiomeDefinition(90, "Wetlands", "Swamplands", 0.7, 0.15, 0.6),
    95: BiomeDefinition(95, "Mangroves", "Swamplands", 0.75, 0.12, 0.65),
    100: BiomeDefinition(100, "Moss / Lichen (Tundra)", "Frozen Expanse", 0.85, 0.05, 0.85),
}


def get_biome(code: int) -> Optional[BiomeDefinition]:
    return BIOME_REGISTRY.get(code)
