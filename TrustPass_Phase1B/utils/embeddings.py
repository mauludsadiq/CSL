# trustpass/utils/embeddings.py

import numpy as np

def get_embedding(text: str) -> np.ndarray:
    """Mock 384-dim embedding vector."""
    return np.random.rand(384)

def evaluate_embedding_similarity(text: str, references: list[str]) -> float:
    text_vec = get_embedding(text)
    ref_vecs = [get_embedding(ref) for ref in references]
    return np.mean([
        np.dot(text_vec, r) / (np.linalg.norm(text_vec) * np.linalg.norm(r))
        for r in ref_vecs
    ])
