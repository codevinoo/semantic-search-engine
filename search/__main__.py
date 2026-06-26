import argparse
import glob
from pathlib import Path

from search.index import SearchIndex


def main():
    parser = argparse.ArgumentParser(description="Semantic search CLI")
    sub = parser.add_subparsers(dest="cmd")

    idx_p = sub.add_parser("index", help="Index documents from a directory")
    idx_p.add_argument("--docs", required=True)
    idx_p.add_argument("--output", default="index.json")

    q_p = sub.add_parser("query", help="Search the index")
    q_p.add_argument("text")
    q_p.add_argument("--index", default="index.json")
    q_p.add_argument("-k", type=int, default=5)

    srv_p = sub.add_parser("serve", help="Start REST API server")
    srv_p.add_argument("--port", type=int, default=8000)
    srv_p.add_argument("--index", default="index.json")

    args = parser.parse_args()

    if args.cmd == "index":
        docs = []
        for fp in glob.glob(str(Path(args.docs) / "*.txt")):
            docs.append(Path(fp).read_text().strip())
        index = SearchIndex()
        index.add(docs)
        index.save(args.output)
        print(f"indexed {len(docs)} documents → {args.output}")

    elif args.cmd == "query":
        index = SearchIndex.load(args.index)
        for doc, score in index.search(args.text, k=args.k):
            preview = doc[:100] + ("..." if len(doc) > 100 else "")
            print(f"[{score:.3f}] {preview}")

    elif args.cmd == "serve":
        import uvicorn
        from search.api import app, index as api_index

        if Path(args.index).exists():
            loaded = SearchIndex.load(args.index)
            api_index.docs = loaded.docs
            if loaded.index is not None:
                api_index.index = loaded.index
        uvicorn.run(app, host="0.0.0.0", port=args.port)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
