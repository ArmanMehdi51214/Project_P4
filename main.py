import logging
import json

from p4_config.paths import get_data_paths
from p4_loaders.archetype_loader import ArchetypeLoader
from p4_loaders.trope_loader import TropeLoader
from p4_loaders.terrain_loader import TerrainLoader

from p4_embeddings.embedder import MiniLMEmbedder
from p4_mappers.archetype_mapper import ArchetypeMapper
from p4_exporters.mapping_exporter import MappingExporter

from p4_rules.biome_registry import get_biome
from p4_rules.archetype_pools import ARCHETYPE_POOLS
from p4_rules.biome_rules import BIOME_OCEAN_MODIFIERS

from p4_generator.npc_generator import generate_npc


# ---------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


# ---------------------------------------------------------------------
# Phase 2: Semantic Mapping
# ---------------------------------------------------------------------
def run_phase_2(parents, tropes, force_remap: bool = False):
    """
    Runs semantic mapping or loads existing mapping artifact.
    """
    mapping_path = "config_archetypes_mapped.json"

    if not force_remap:
        try:
            with open(mapping_path, "r", encoding="utf-8") as f:
                mappings = json.load(f)
            print(f"\nLoaded existing archetype mapping ({len(mappings)} rows)")
            return mappings
        except FileNotFoundError:
            pass

    print("\n=== PHASE 2: SEMANTIC MAPPING ===")

    embedder = MiniLMEmbedder()
    mapper = ArchetypeMapper(embedder)

    mappings = mapper.map_children_to_parents(
        parents=parents,
        children=tropes,
    )

    MappingExporter().export(
        mappings=mappings,
        output_path=mapping_path,
    )

    low_conf = sum(1 for m in mappings if m["review_needed"])
    print(f"Low-confidence mappings: {low_conf} / {len(mappings)}")

    return mappings


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------
def main():
    setup_logging()
    paths = get_data_paths()

    # -------------------------------------------------
    # Phase 1: Load Inputs
    # -------------------------------------------------
    print("\n=== PHASE 1: LOAD INPUTS ===")

    parents = ArchetypeLoader().load(paths.parent_archetypes_path)
    tropes = TropeLoader().load(paths.tropes_child_path)

    print(f"Loaded parent archetypes: {len(parents)}")
    print(f"Loaded child tropes:      {len(tropes)}")

    parents_by_id = {p.id: p for p in parents}

    terrain_loader = TerrainLoader()

    tokyo = terrain_loader.load_map(paths.terrain_dir / "Tokyo_MegaCity.json")
    yakutsk = terrain_loader.load_map(paths.terrain_dir / "Yakutsk_FrozenTundra.json")

    print(f"Loaded Tokyo map:   {len(tokyo.cells)} cells")
    print(f"Loaded Yakutsk map: {len(yakutsk.cells)} cells")

    print("\n✅ Phase 1 OK")

    # -------------------------------------------------
    # Phase 2: Semantic Mapping
    # -------------------------------------------------
    mappings = run_phase_2(parents, tropes)

    # -------------------------------------------------
    # Phase 3: Biome Sanity
    # -------------------------------------------------
    print("\n=== PHASE 3: BIOME SANITY ===")

    print("Tokyo biome:", get_biome(50))
    print("Tokyo archetypes:", ARCHETYPE_POOLS.get(50))
    print("Tokyo modifiers:", BIOME_OCEAN_MODIFIERS.get(50))

    print("\nYakutsk biome:", get_biome(100))
    print("Yakutsk archetypes:", ARCHETYPE_POOLS.get(100))
    print("Yakutsk modifiers:", BIOME_OCEAN_MODIFIERS.get(100))

    # -------------------------------------------------
    # Phase 4: NPC Generation (THE PAYOFF)
    # -------------------------------------------------
    print("\n=== PHASE 4: NPC GENERATION ===")

    tokyo_npc = generate_npc(
        x=10,
        y=10,
        terrain_map=tokyo,
        parents_by_id=parents_by_id,
        tropes=tropes,
        mapping_rows=mappings,
        seed=42,
    )

    yakutsk_npc = generate_npc(
        x=10,
        y=10,
        terrain_map=yakutsk,
        parents_by_id=parents_by_id,
        tropes=tropes,
        mapping_rows=mappings,
        seed=42,
    )

    print("\nTOKYO NPC SAMPLE:\n")
    print(json.dumps(tokyo_npc, indent=2))

    print("\nYAKUTSK NPC SAMPLE:\n")
    print(json.dumps(yakutsk_npc, indent=2))


if __name__ == "__main__":
    main()
