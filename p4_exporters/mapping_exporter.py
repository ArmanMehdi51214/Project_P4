import json
from pathlib import Path
from typing import List, Dict


class MappingExporter:
    def export(
        self,
        mappings: List[Dict],
        output_path: str | Path,
    ) -> None:
        output_path = Path(output_path)
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(mappings, f, indent=2)

        print(f"✔ Archetype mapping exported → {output_path} ({len(mappings)} rows)")
