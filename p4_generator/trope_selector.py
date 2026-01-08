from __future__ import annotations

import random
from typing import List, Dict

from p4_core.trope import TropeChild


# ---------------------------------------------------------------------
# Theme → genre intent (what we WANT)
# ---------------------------------------------------------------------
THEME_GENRE_HINTS = {
    "Cyberpunk Sprawl": ["cyber", "corp", "neon", "hacker"],
    "Frozen Expanse": ["ice", "tundra", "survival", "hermit"],
    "Wildlands": ["tribal", "nature", "druid", "hunter"],
    "Frontier Hinterland": ["farmer", "veteran", "settler"],
    "Swamplands": ["smuggler", "biologist", "hermit"],
    "The Wasteland": ["scavenger", "raider", "nomad"],
}


# ---------------------------------------------------------------------
# Theme → genre exclusions (what we NEVER want)
# ---------------------------------------------------------------------
EXCLUDED_KEYWORDS = {
    "Wildlands": ["cyber", "hacker", "neon", "corp"],
    "Frozen Expanse": ["cyber", "neon", "corp"],
}


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

    # -------------------------------------------------
    # Step 1: tropes mapped to this parent archetype
    # -------------------------------------------------
    valid_trope_ids = {
        m["child_id"]
        for m in mapping_rows
        if m["resolved_parent_id"] == parent_id
    }

    candidates = [t for t in tropes if t.id in valid_trope_ids]

    if not candidates:
        raise ValueError(f"No child tropes mapped to parent {parent_id}")

    # -------------------------------------------------
    # Step 2: prefer genre/theme matches
    # -------------------------------------------------
    hints = THEME_GENRE_HINTS.get(biome_theme, [])
    themed = [
        t for t in candidates
        if t.genre_tag and any(h in t.genre_tag.lower() for h in hints)
    ]

    # -------------------------------------------------
    # Step 3: apply exclusions (world sanity)
    # -------------------------------------------------
    excluded = EXCLUDED_KEYWORDS.get(biome_theme, [])

    if themed and excluded:
        themed = [
            t for t in themed
            if not any(e in (t.genre_tag or "").lower() for e in excluded)
        ]

    pool = themed if themed else candidates
    return rng.choice(pool)
