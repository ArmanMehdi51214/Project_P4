from typing import Dict


# OCEAN deltas applied on top of archetype bias
BIOME_OCEAN_MODIFIERS: Dict[int, Dict[str, float]] = {
    # Urban
    50: {
        "conscientiousness": +0.15,
        "neuroticism": +0.10,
        "agreeableness": -0.10,
    },

    # Forest
    10: {
        "openness": +0.10,
        "extroversion": -0.10,
    },

    # Water
    80: {
        "neuroticism": +0.15,
        "conscientiousness": +0.10,
    },

    # Wasteland
    60: {
        "conscientiousness": +0.25,
        "agreeableness": -0.20,
        "neuroticism": +0.20,
    },
    20: {
        "conscientiousness": +0.10,
        "agreeableness": -0.10,
    },
    30: {
        "openness": +0.05,
        "conscientiousness": +0.05,
    },

    # Extreme
    70: {
        "conscientiousness": +0.30,
        "extroversion": -0.25,
        "neuroticism": +0.25,
    },
    90: {
        "neuroticism": +0.15,
        "openness": +0.05,
    },
    95: {
        "neuroticism": +0.15,
        "openness": +0.05,
    },
    100: {
        "conscientiousness": +0.20,
        "extroversion": -0.20,
        "neuroticism": +0.20,
    },
    40: {
    "conscientiousness": +0.10,
    "agreeableness": +0.05,
    "extroversion": -0.05,
    }

}
