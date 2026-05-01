"""Demonstrate Meilisearch's core search features against the movies index.

Run with:  python scripts/02_search_demo.py
"""
import os
from pathlib import Path

import meilisearch
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

HOST = os.getenv("MEILI_HOST", "http://localhost:7700")
KEY = os.getenv("MEILI_MASTER_KEY", "aSampleMasterKeyForDevelopmentOnly")
INDEX_NAME = "movies"


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(f"  {title}")
    print("=" * 72)


def show_hits(result: dict, fields=("title", "year", "rating")) -> None:
    hits = result.get("hits", [])
    took = result.get("processingTimeMs", "?")
    estimated = result.get("estimatedTotalHits", len(hits))
    print(f"  -> {len(hits)} hits shown / {estimated} total  [{took} ms]")
    for h in hits:
        line = "  - " + " | ".join(f"{f}={h.get(f)!r}" for f in fields)
        print(line)


def main() -> None:
    client = meilisearch.Client(HOST, KEY)
    index = client.index(INDEX_NAME)

    section("1) Basic full-text search: 'godfather'")
    res = index.search("godfather", {"limit": 3})
    show_hits(res)

    section("2) Typo tolerance: 'godfther' (intentional typo)")
    res = index.search("godfther", {"limit": 3})
    show_hits(res)

    section("3) Typo tolerance: 'interstelar' (missing letter)")
    res = index.search("interstelar", {"limit": 3})
    show_hits(res)

    section("4) Prefix search: 'inter' (Meilisearch matches as you type)")
    res = index.search("inter", {"limit": 3})
    show_hits(res)

    section("5) Filter: action movies after 2010, sorted by rating desc")
    res = index.search("", {
        "filter": ["genres = 'Action'", "year > 2010"],
        "sort": ["rating:desc"],
        "limit": 5,
    })
    show_hits(res)

    section("6) Filter + search: 'space' inside Sci-Fi genre")
    res = index.search("space", {
        "filter": "genres = 'Sci-Fi'",
        "limit": 5,
    })
    show_hits(res)

    section("7) Highlighting: where did the term match?")
    res = index.search("dream", {
        "limit": 2,
        "attributesToHighlight": ["title", "overview"],
        "highlightPreTag": "<<",
        "highlightPostTag": ">>",
    })
    for h in res["hits"]:
        formatted = h.get("_formatted", {})
        print(f"  - title : {formatted.get('title')}")
        print(f"    where : {formatted.get('overview')}")

    section("8) Phrase search with quotes: '\"dark knight\"'")
    res = index.search('"dark knight"', {"limit": 3})
    show_hits(res)


if __name__ == "__main__":
    main()
    print("\nAll search demos finished.\n")
