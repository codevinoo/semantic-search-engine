"""FastAPI server for semantic search."""

from fastapi import FastAPI
from pydantic import BaseModel

from search.index import SearchIndex

app = FastAPI(title="Semantic Search Engine", version="1.0.0")
index = SearchIndex()


class IndexRequest(BaseModel):
    documents: list[str]


class SearchRequest(BaseModel):
    query: str
    k: int = 5


@app.get("/health")
def health():
    return {"status": "ok", "documents": len(index.docs)}


@app.post("/index")
def add_documents(req: IndexRequest):
    index.add(req.documents)
    return {"indexed": len(req.documents), "total": len(index.docs)}


@app.post("/search")
def search(req: SearchRequest):
    results = index.search(req.query, k=req.k)
    return {
        "query": req.query,
        "results": [{"text": text, "score": score} for text, score in results],
    }
