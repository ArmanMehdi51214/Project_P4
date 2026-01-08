from __future__ import annotations

import random
from typing import Dict, List

from p4_core.world_cell import WorldCell
from p4_rules.biome_registry import get_biome
from p4_rules.archetype_pools import ARCHETYPE_POOLS
from p4_rules.biome_rules import BIOME_OCEAN_MODIFIERS

from p4_generator.ocean_calculator import apply_biome_modifiers
from p4_generator.archetype_selector import select_archetype
from p4_generator.trope_selector import select_trope


def generate_npc(
    x: int,
    y: int,
    terrain_map,
    parents_by_id: Dict,
    tropes: List,
    mapping_rows: List[Dict],
    seed: int = 1337,
) -> Dict:
    rng = random.Random(seed)

    # -------------------------------------------------
    # Terrain lookup
    # -------------------------------------------------
    cell: WorldCell | None = terrain_map.get_cell(x, y)
    if cell is None:
        raise ValueError(f"No terrain cell at ({x}, {y})")

    biome = get_biome(cell.biome_code)
    if biome is None:
        # Fallback: treat unknown land biomes as frontier hinterland
        biome = get_biome(40)

    # -------------------------------------------------
    # Archetype selection (biome constrained)
    # -------------------------------------------------
    allowed_archetypes = ARCHETYPE_POOLS.get(biome.code, [])
    if not allowed_archetypes:
        raise ValueError(f"No archetype pool for biome {biome.code}")

    parent = select_archetype(parents_by_id, allowed_archetypes, rng)

    # -------------------------------------------------
    # Psychology shaping
    # -------------------------------------------------
    biome_mods = BIOME_OCEAN_MODIFIERS.get(biome.code, {})
    ocean_stats, explanation = apply_biome_modifiers(
        parent.ocean_bias,
        biome_mods,
    )

    trait = max(ocean_stats, key=ocean_stats.get)

    # -------------------------------------------------
    # Trope selection (genre-aware)
    # -------------------------------------------------
    trope = select_trope(
        tropes=tropes,
        mapping_rows=mapping_rows,
        parent_id=parent.id,
        biome_theme=biome.theme,
        rng=rng,
    )

    # -------------------------------------------------
    # Final NPC payload
    # -------------------------------------------------
    npc = {
        "npc_id": f"NPC_GEN_x{x}y{y}",
        "name": trope.name,
        "archetype_parent": parent.id,
        "archetype_name": parent.name,
        "trope_child": trope.id,
        "trope_name": trope.name,
        "origin": {
            "coordinates": {"x": x, "y": y},
            "biome_id": biome.code,
            "mapped_theme": biome.theme,
        },
        "psychometrics": {
            "ocean_stats": ocean_stats,
            "dominant_trait": f"High {trait.capitalize()}",
            "environmental_influence": explanation,
        },
        "narrative": {
            "goal": parent.primary_goal,
            "fear": parent.primary_fear,
            "visual_description": trope.description,
            "dialogue_voice": biome.theme,
        },
    }

    return npc
