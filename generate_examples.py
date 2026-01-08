import json
import logging
from pathlib import Path

from p4_config.paths import get_data_paths
from p4_loaders.archetype_loader import ArchetypeLoader
from p4_loaders.trope_loader import TropeLoader
from p4_loaders.terrain_loader import TerrainLoader

from p4_embeddings.embedder import MiniLMEmbedder
from p4_mappers.archetype_mapper import ArchetypeMapper

from p4_generator.npc_generator import generate_npc
from p4_utils.terrain_utils import find_cell_with_biome


# -------------------------------------------------
# Logging
# -------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


# -------------------------------------------------
# Helper: load or build archetype mapping
# -------------------------------------------------
def load_mappings(parents, tropes):
    mapping_path = Path("config_archetypes_mapped.json")

    if mapping_path.exists():
        with mapping_path.open("r", encoding="utf-8") as f:
            logging.info("Loading existing archetype mapping")
            return json.load(f)

    logging.info("Generating archetype mapping (first run)")
    embedder = MiniLMEmbedder()
    mapper = ArchetypeMapper(embedder)
    mappings = mapper.map_children_to_parents(parents, tropes)

    with mapping_path.open("w", encoding="utf-8") as f:
        json.dump(mappings, f, indent=2)

    return mappings


# -------------------------------------------------
# Main example generation
# -------------------------------------------------
def main():
    paths = get_data_paths()
    examples_dir = Path("examples")
    examples_dir.mkdir(exist_ok=True)

    # -----------------------------
    # Load core data
    # -----------------------------
    parents = ArchetypeLoader().load(paths.parent_archetypes_path)
    tropes = TropeLoader().load(paths.tropes_child_path)
    parents_by_id = {p.id: p for p in parents}

    mappings = load_mappings(parents, tropes)

    terrain_loader = TerrainLoader()

    # -----------------------------
    # Example maps & target biomes
    # -----------------------------
    showcase = [
        {
            "map_file": "Tokyo_MegaCity.json",
            "biome_code": 50,
            "output": "tokyo_urban_npc.json",
        },
        {
            "map_file": "Yakutsk_FrozenTundra.json",
            "biome_code": 100,
            "output": "yakutsk_tundra_npc.json",
        },
        {
            "map_file": "Manaus_DeepJungle.json",   # optional wildlands
            "biome_code": 10,
            "output": "amazon_wildlands_npc.json",
        },
        {
            "map_file": "McMurdo_DryValleys.json",  # optional wasteland
            "biome_code": 60,
            "output": "wasteland_scavenger_npc.json",
        },
    ]

    # -----------------------------
    # Generate NPCs
    # -----------------------------
    for entry in showcase:
        map_path = paths.terrain_dir / entry["map_file"]
        if not map_path.exists():
            logging.warning(f"Map not found, skipping: {entry['map_file']}")
            continue

        terrain_map = terrain_loader.load_map(map_path)
        coords = find_cell_with_biome(terrain_map, entry["biome_code"])

        if coords is None:
            logging.warning(
                f"No biome {entry['biome_code']} found in {entry['map_file']}"
            )
            continue

        npc = generate_npc(
            x=coords[0],
            y=coords[1],
            terrain_map=terrain_map,
            parents_by_id=parents_by_id,
            tropes=tropes,
            mapping_rows=mappings,
            seed=42,
        )

        out_path = examples_dir / entry["output"]
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(npc, f, indent=2)

        logging.info(f"Saved example NPC → {out_path}")

    logging.info("✅ Example NPC generation complete.")


if __name__ == "__main__":
    main()
