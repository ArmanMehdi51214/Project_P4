from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple, Optional, Any, List, Iterable

from p4_core.world_cell import WorldCell

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TerrainMap:
    """
    In-memory terrain grid indexed by (x, y).
    """
    name: str
    meta: Dict[str, Any]
    cells: Dict[Tuple[int, int], WorldCell]

    def get_cell(self, x: int, y: int) -> Optional[WorldCell]:
        return self.cells.get((x, y))


class TerrainLoader:
    def load_map(self, path: str | Path) -> TerrainMap:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Terrain map not found: {path}")

        logger.info("Loading terrain map from %s", path)

        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            raise ValueError(f"Expected dict in terrain file {path}, got {type(data)}")

        meta = data.get("meta") or {}
        grid = data.get("grid") or []

        if not isinstance(meta, dict):
            logger.warning("meta is not a dict in %s; forcing empty meta", path)
            meta = {}

        if not isinstance(grid, list):
            raise ValueError(f"Expected grid list in {path}, got {type(grid)}")

        north_lat = _read_north_lat(meta)

        cells: Dict[Tuple[int, int], WorldCell] = {}
        patched = 0

        for row in grid:
            if not isinstance(row, dict):
                continue

            x = row.get("x")
            y = row.get("y")
            geo = row.get("geo_data") or {}
            heur = row.get("game_heuristics")

            if not isinstance(x, int) or not isinstance(y, int):
                continue
            if not isinstance(geo, dict):
                geo = {}

            # --- LATITUDE OVERRIDE PATCH (ingestion-time) ---
            biome_code = geo.get("biome_code")
            biome_code_int = None
            try:
                biome_code_int = int(biome_code) if biome_code is not None else None
            except Exception:
                biome_code_int = None

            if north_lat is not None and (north_lat > 65 or north_lat < -60):
                if biome_code_int == 10:
                    geo["biome_code"] = 100
                    patched += 1

            cell = WorldCell(x=x, y=y, geo_data=geo, game_heuristics=heur if isinstance(heur, dict) else None)
            cells[(x, y)] = cell

        name = str(meta.get("project_name") or path.stem)
        if patched > 0:
            logger.warning("Applied latitude override patch to %d cells in %s", patched, name)

        logger.info("Loaded terrain map '%s' with %d cells", name, len(cells))
        return TerrainMap(name=name, meta=meta, cells=cells)

    def load_folder(self, folder: str | Path) -> List[TerrainMap]:
        """
        Loads all .json maps in a folder.
        """
        folder = Path(folder)
        if not folder.exists():
            raise FileNotFoundError(f"Terrain folder not found: {folder}")

        maps: List[TerrainMap] = []
        for p in sorted(folder.glob("*.json")):
            try:
                maps.append(self.load_map(p))
            except Exception as e:
                logger.exception("Failed to load map %s: %s", p, e)

        logger.info("Loaded %d terrain maps from %s", len(maps), folder)
        return maps


def _read_north_lat(meta: Dict[str, Any]) -> Optional[float]:
    """
    Robustly read northern latitude from meta. Handles both:
      meta['bounding_box']['north']
      meta['bbox']['north']
    In sf_context_grid.json, it's meta['bbox']['north']. (Seen in your file.)
    """
    # try bounding_box
    bb = meta.get("bounding_box")
    if isinstance(bb, dict) and "north" in bb:
        try:
            return float(bb["north"])
        except Exception:
            pass

    # try bbox
    bb = meta.get("bbox")
    if isinstance(bb, dict) and "north" in bb:
        try:
            return float(bb["north"])
        except Exception:
            pass

    return None
