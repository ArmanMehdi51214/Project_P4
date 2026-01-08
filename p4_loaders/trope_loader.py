from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import List, Any, Optional

from p4_core.trope import TropeChild

logger = logging.getLogger(__name__)


class TropeLoader:
    def load(self, path: str | Path) -> List[TropeChild]:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Child tropes file not found: {path}")

        logger.info("Loading child tropes from %s", path)

        text = path.read_text(encoding="utf-8")

        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            logger.warning(
                "Strict JSON parsing failed for %s (%s). Attempting cleanup.",
                path.name,
                e,
            )
            data = self._load_with_cleanup(text, path)

        if not isinstance(data, list):
            raise ValueError(f"Expected list in {path}, got {type(data)}")

        out: List[TropeChild] = []
        for i, row in enumerate(data):
            if not isinstance(row, dict):
                logger.warning("Skipping non-dict trope row %s: %r", i, row)
                continue

            out.append(
                TropeChild(
                    id=str(row.get("id") or ""),
                    name=str(row.get("name") or ""),
                    parent_archetype_raw=_opt_str(row.get("parent_archetype")),
                    description=_opt_str(row.get("description")),
                    genre_tag=_opt_str(row.get("genre_tag")),
                )
            )

        out2 = [t for t in out if t.id and t.name]
        if len(out2) != len(out):
            logger.warning(
                "Dropped %d tropes missing id/name",
                len(out) - len(out2),
            )

        logger.info("Loaded %d child tropes", len(out2))
        return out2

    def _load_with_cleanup(self, text: str, path: Path):
        """
        Attempts to repair common JSON issues:
        - trailing commas in objects/arrays
        """
        # Remove trailing commas before } or ]
        cleaned = re.sub(r",\s*(\]|\})", r"\1", text)

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(
                "Cleanup parsing also failed for %s at line %s col %s",
                path.name,
                e.lineno,
                e.colno,
            )
            raise
def _opt_str(v: Any) -> Optional[str]:
    if v is None:
        return None
    s = str(v).strip()
    return s if s else None
