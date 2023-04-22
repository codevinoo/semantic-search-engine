import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    _MODEL = SentenceTransformer("all-MiniLM-L6-v2")
except Exception:
    _MODEL = None


def embed_texts(texts: list[str]) -> np.ndarray:
    if _MODEL is not None:
        return _MODEL.encode(texts, normalize_embeddings=True)
    # Fallback hash embedding for environments without model download
    vecs = []
    for t in texts:
        h = abs(hash(t)) % (2**31)
        v = np.zeros(384)
        v[h % 384] = 1.0
        vecs.append(v)
    return np.array(vecs, dtype=np.float32)
