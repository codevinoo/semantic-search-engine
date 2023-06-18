import json
import numpy as np

try:
    import faiss
except ImportError:
    faiss = None

from search.embedder import embed_texts


class SearchIndex:
    def __init__(self, dim: int = 384):
        self.dim = dim
        self.docs: list[str] = []
        self.index = faiss.IndexFlatIP(dim) if faiss else None
        self.vectors: np.ndarray | None = None

    def add(self, documents: list[str]) -> None:
        vecs = embed_texts(documents).astype(np.float32)
        self.docs.extend(documents)
        if self.index is not None:
            self.index.add(vecs)
        else:
            self.vectors = vecs if self.vectors is None else np.vstack([self.vectors, vecs])

    def search(self, query: str, k: int = 5) -> list[tuple[str, float]]:
        q = embed_texts([query]).astype(np.float32)
        if self.index is not None:
            scores, idxs = self.index.search(q, min(k, len(self.docs)))
            return [(self.docs[i], float(scores[0][j])) for j, i in enumerate(idxs[0]) if i >= 0]
        sims = (self.vectors @ q.T).flatten()
        top = np.argsort(-sims)[:k]
        return [(self.docs[i], float(sims[i])) for i in top]

    def save(self, path: str) -> None:
        with open(path, "w") as f:
            json.dump({"docs": self.docs}, f)

    @classmethod
    def load(cls, path: str) -> "SearchIndex":
        idx = cls()
        with open(path) as f:
            data = json.load(f)
        idx.add(data["docs"])
        return idx
