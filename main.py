import logging

from p4_config.paths import get_data_paths
from p4_loaders.archetype_loader import ArchetypeLoader
from p4_loaders.trope_loader import TropeLoader
from p4_loaders.terrain_loader import TerrainLoader


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def main():
    setup_logging()
    paths = get_data_paths()

    print("\n=== PHASE 1 SMOKE TEST: LOAD INPUTS ===")

    parents = ArchetypeLoader().load(paths.parent_archetypes_path)
    tropes = TropeLoader().load(paths.tropes_child_path)

    print(f"Loaded parent archetypes: {len(parents)}")
    print(f"Loaded child tropes:      {len(tropes)}")

    terrain_loader = TerrainLoader()

    # Load ONE map (pick a well-known one)
    tokyo_path = paths.terrain_dir / "Tokyo_MegaCity.json"
    if tokyo_path.exists():
        tokyo = terrain_loader.load_map(tokyo_path)
        print(f"\nLoaded map: {tokyo.name} | cells={len(tokyo.cells)}")
        sample = tokyo.get_cell(0, 0)
        if sample:
            print(f"Sample cell (0,0): biome_code={sample.biome_code}, elevation={sample.elevation}, density={sample.human_density}")
    else:
        print("\nTokyo_MegaCity.json not found in terrain folder. Loading folder summary instead:")
        maps = terrain_loader.load_folder(paths.terrain_dir)
        print(f"Loaded maps: {len(maps)}")
        if maps:
            first = maps[0]
            print(f"First map: {first.name} | cells={len(first.cells)}")

    print("\n✅ Phase 1 OK: inputs load cleanly.")


if __name__ == "__main__":
    main()
