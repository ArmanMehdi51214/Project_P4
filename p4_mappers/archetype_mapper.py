from __future__ import annotations

import logging
import numpy as np
from typing import List, Dict

from p4_core.archetype import ArchetypeParent
from p4_core.trope import TropeChild
from p4_embeddings.embedder import MiniLMEmbedder
from p4_mappers.mapping_config import MAPPING_THRESHOLD

logger = logging.getLogger(__name__)


class ArchetypeMapper:
    def __init__(self, embedder: MiniLMEmbedder):
        self.embedder = embedder

    def map_children_to_parents(
        self,
        parents: List[ArchetypeParent],
        children: List[TropeChild],
    ) -> List[Dict]:

        logger.info("Embedding parent archetypes...")
        parent_texts = [
            f"{p.name}. {p.primary_goal or ''} {p.primary_fear or ''}"
            for p in parents
        ]
        parent_embeddings = self.embedder.embed(parent_texts)

        results = []

        logger.info("Mapping %d child tropes → parents", len(children))

        for child in children:
            child_text = " ".join(
                t for t in [
                    child.parent_archetype_raw,
                    child.name,
                    child.description,
                ]
                if t
            )

            child_emb = self.embedder.embed(child_text)[0]
            scores = np.dot(parent_embeddings, child_emb)

            best_idx = int(np.argmax(scores))
            best_score = float(scores[best_idx])
            best_parent = parents[best_idx]

            results.append({
                "child_id": child.id,
                "child_name": child.name,
                "resolved_parent_id": best_parent.id,
                "resolved_parent_name": best_parent.name,
                "confidence_score": round(best_score, 4),
                "review_needed": best_score < MAPPING_THRESHOLD,
            })

        low_conf = sum(1 for r in results if r["review_needed"])
        logger.info(
            "Mapping complete. Low-confidence mappings: %d / %d",
            low_conf, len(results)
        )

        return results
