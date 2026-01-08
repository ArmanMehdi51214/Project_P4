from __future__ import annotations
from typing import Dict, Tuple


def clamp(v: float) -> float:
    return max(0.0, min(1.0, v))


def apply_biome_modifiers(
    base_ocean: Dict[str, float],
    biome_mods: Dict[str, float],
) -> Tuple[Dict[str, float], str]:
    """
    Applies biome OCEAN deltas to archetype baseline.
    Returns final OCEAN + explanation string.
    """
    final = {}
    explanations = []

    for trait in ["openness", "conscientiousness", "extroversion", "agreeableness", "neuroticism"]:
        base = base_ocean.get(trait, 0.5)
        delta = biome_mods.get(trait, 0.0)
        final_val = clamp(base + delta)

        final[trait] = round(final_val, 3)

        if abs(delta) > 0:
            sign = "+" if delta > 0 else ""
            explanations.append(f"{trait} {sign}{delta}")

    explanation = "Biome influence: " + ", ".join(explanations) if explanations else "Minimal environmental influence."

    return final, explanation
