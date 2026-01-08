from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataPaths:
    """
    Centralized locations for project data.

    We keep client attachments and terrain folders *as-is* and reference them here.
    """
    project_root: Path

    @property
    def attachments_dir(self) -> Path:
        return self.project_root / "santoshr61-attachments"

    @property
    def terrain_dir(self) -> Path:
        return self.project_root / "Terrain_Test_Suite_JSON_Revised"

    @property
    def parent_archetypes_path(self) -> Path:
        # Prefer attachments copy (client-provided bundle)
        p = self.attachments_dir / "parent archetypes.json"
        if p.exists():
            return p
        # fallback root copy
        return self.project_root / "parent archetypes.json"

    @property
    def tropes_child_path(self) -> Path:
        p = self.attachments_dir / "tropes_child.json"
        if p.exists():
            return p
        return self.project_root / "tropes_child.json"


def get_data_paths(project_root: str | Path | None = None) -> DataPaths:
    """
    Auto-detect root if not provided: assumes this file is in p4_config/.
    """
    if project_root is None:
        project_root = Path(__file__).resolve().parents[1]
    return DataPaths(project_root=Path(project_root).resolve())
