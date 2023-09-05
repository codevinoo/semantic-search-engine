import argparse
import glob
from pathlib import Path
from search.index import SearchIndex


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")
    idx_p = sub.add_parser("index")
    idx_p.add_argument("--docs", required=True)
    q_p = sub.add_parser("query")
    q_p.add_argument("text")
    q_p.add_argument("--index", default="index.json")
    args = parser.parse_args()

    if args.cmd == "index":
        docs = []
        for fp in glob.glob(str(Path(args.docs) / "*.txt")):
            docs.append(Path(fp).read_text())
        index = SearchIndex()
        index.add(docs)
        index.save("index.json")
        print(f"indexed {len(docs)} documents")
    elif args.cmd == "query":
        index = SearchIndex.load(args.index)
        for doc, score in index.search(args.text):
            print(f"[{score:.3f}] {doc[:80]}...")


if __name__ == "__main__":
    main()
