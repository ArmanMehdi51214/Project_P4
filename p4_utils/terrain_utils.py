from typing import Tuple, Optional
from p4_loaders.terrain_loader import TerrainMap


def find_cell_with_biome(
    terrain_map: TerrainMap,
    target_biome: int,
) -> Optional[Tuple[int, int]]:
    for (x, y), cell in terrain_map.cells.items():
        if cell.biome_code == target_biome:
            return x, y
    return None
