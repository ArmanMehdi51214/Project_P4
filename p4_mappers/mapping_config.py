from p4_config.constants import DEFAULT_MAPPING_THRESHOLD

MAPPING_THRESHOLD = DEFAULT_MAPPING_THRESHOLD

# Weighting of child text fields
CHILD_TEXT_WEIGHTS = {
    "parent_archetype_raw": 0.5,
    "name": 0.3,
    "description": 0.2,
}
