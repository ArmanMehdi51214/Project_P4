from __future__ import annotations
import random
from typing import List, Dict

from p4_core.trope import TropeChild


def select_trope(
    tropes: List[TropeChild],
    mapping_rows: List[Dict],
    parent_id: str,
    biome_theme: str,
    rng: random.Random,
) -> TropeChild:
    """
    Selects a child trope matching parent archetype and biome theme if possible.
    """

    # Step 1: all tropes mapped to this parent
    valid_trope_ids = {
        m["child_id"]
        for m in mapping_rows
        if m["resolved_parent_id"] == parent_id
    }

    candidates = [t for t in tropes if t.id in valid_trope_ids]

    if not candidates:
        raise ValueError(f"No child tropes mapped to parent {parent_id}")

    # Step 2: prefer genre/theme match
    themed = [
        t for t in candidates
        if t.genre_tag and biome_theme.lower() in t.genre_tag.lower()
    ]

    pool = themed if themed else candidates
    return rng.choice(pool)
