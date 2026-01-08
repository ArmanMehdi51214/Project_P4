from __future__ import annotations

from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer


class MiniLMEmbedder:
    """
    Central embedding engine for Project P4.
    Uses sentence-transformers/all-MiniLM-L6-v2
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        normalize: bool = True,
        batch_size: int = 32,
    ):
        self.model_name = model_name
        self.normalize = normalize
        self.batch_size = batch_size
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: Union[str, List[str]]) -> np.ndarray:
        if isinstance(texts, str):
            texts = [texts]

        embeddings = self.model.encode(
            texts,
            batch_size=self.batch_size,
            normalize_embeddings=self.normalize,
            show_progress_bar=False,
        )
        return np.asarray(embeddings)

    def embedding_dim(self) -> int:
        return self.model.get_sentence_embedding_dimension()
