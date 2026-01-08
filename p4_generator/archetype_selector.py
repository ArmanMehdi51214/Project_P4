from __future__ import annotations
import random
from typing import Dict, List

from p4_core.archetype import ArchetypeParent


def select_archetype(
    parents_by_id: Dict[str, ArchetypeParent],
    allowed_ids: List[str],
    rng: random.Random,
) -> ArchetypeParent:
    """
    Selects a parent archetype from biome-constrained pool.
    """
    candidates = [
        parents_by_id[aid]
        for aid in allowed_ids
        if aid in parents_by_id
    ]

    if not candidates:
        raise ValueError("No valid archetypes available for this biome.")

    return rng.choice(candidates)
