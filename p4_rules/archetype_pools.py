from typing import Dict, List


ARCHETYPE_POOLS: Dict[int, List[str]] = {
    # Urban
    50: [
        "ARCH_LEADER_03",  # Charismatic Populist
        "ARCH_LEADER_06",  # Corporate Bureaucrat
        "ARCH_LEADER_04",  # Authoritarian General
        "ARCH_MENTOR_02",  # Cynical Veteran
    ],

    # Forest
    10: [
        "ARCH_MENTOR_01",  # Wise Hermit
        "ARCH_MENTOR_03",  # Nurturing Teacher
    ],

    # Water
    80: [
        "ARCH_LEADER_07",  # Warlord Barbarian
        "ARCH_MENTOR_02",
    ],

    # Wasteland
    60: [
        "ARCH_LEADER_07",
        "ARCH_MENTOR_02",
    ],
    20: [
        "ARCH_MENTOR_02",
        "ARCH_MENTOR_01",
    ],
    30: [
        "ARCH_LEADER_05",  # Reluctant Leader
        "ARCH_MENTOR_03",
    ],
    40: [
    "ARCH_LEADER_05",  # Reluctant Leader
    "ARCH_MENTOR_03",  # Community Elder / Teacher
    "ARCH_MENTOR_02",  # Cynical Veteran 
    ],


    # Extreme
    70: [
        "ARCH_MENTOR_02",
        "ARCH_MENTOR_01",
    ],
    90: [
        "ARCH_LEADER_07",
        "ARCH_MENTOR_01",
    ],
    95: [
        "ARCH_LEADER_07",
        "ARCH_MENTOR_01",
    ],
    100: [
        "ARCH_MENTOR_02",
        "ARCH_MENTOR_01",
    ],
}
