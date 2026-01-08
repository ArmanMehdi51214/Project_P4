from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import List, Any, Dict, Optional

from p4_core.archetype import ArchetypeParent

logger = logging.getLogger(__name__)


class ArchetypeLoader:
    def load(self, path: str | Path) -> List[ArchetypeParent]:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Parent archetypes file not found: {path}")

        logger.info("Loading parent archetypes from %s", path)

        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError(f"Expected list in {path}, got {type(data)}")

        out: List[ArchetypeParent] = []
        for i, row in enumerate(data):
            if not isinstance(row, dict):
                logger.warning("Skipping non-dict archetype row %s: %r", i, row)
                continue

            out.append(
                ArchetypeParent(
                    id=str(row.get("id") or ""),
                    name=str(row.get("name") or ""),
                    function_category=_opt_str(row.get("function_category")),
                    ocean_bias=_as_ocean(row.get("ocean_bias")),
                    primary_goal=_opt_str(row.get("primary_goal")),
                    primary_fear=_opt_str(row.get("primary_fear")),
                )
            )

        # minimal validation: must have ids/names
        out2 = [a for a in out if a.id and a.name]
        if len(out2) != len(out):
            logger.warning("Dropped %d archetypes missing id/name", len(out) - len(out2))

        logger.info("Loaded %d parent archetypes", len(out2))
        return out2


def _opt_str(v: Any) -> Optional[str]:
    if v is None:
        return None
    s = str(v).strip()
    return s if s else None


def _as_ocean(v: Any) -> Dict[str, float]:
    """
    Robust OCEAN dict parsing. Missing keys are allowed (logged later in Phase 4).
    """
    if not isinstance(v, dict):
        return {}
    out: Dict[str, float] = {}
    for k, val in v.items():
        try:
            out[str(k)] = float(val)
        except Exception:
            continue
    return out
