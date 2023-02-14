# Semantic Search Engine

Vector-based semantic search using sentence embeddings and approximate nearest neighbor indexing.

## Features

- Document ingestion and chunking
- Embedding generation with sentence-transformers
- FAISS index for fast similarity search
- REST API for query and indexing

## Usage

```bash
pip install -r requirements.txt
python -m search index --docs ./sample_docs
python -m search query "distributed consensus algorithms"
```

## License

MIT
