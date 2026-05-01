"""Demonstrate faceted search with Meilisearch.

Faceting lets you build the typical 'filters sidebar' of an e-commerce site:
how many results fall into each genre, year bucket, etc.

Run with:  python scripts/03_facet_demo.py
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


def print_facets(result: dict) -> None:
    distribution = result.get("facetDistribution", {})
    for facet, counts in distribution.items():
        print(f"\n  facet: {facet}")
        sorted_counts = sorted(counts.items(), key=lambda kv: -kv[1])
        for value, count in sorted_counts[:10]:
            bar = "#" * count
            print(f"    {value:<30} {count:>3}  {bar}")


def main() -> None:
    client = meilisearch.Client(HOST, KEY)
    index = client.index(INDEX_NAME)

    section("Facet distribution across the entire index")
    res = index.search("", {
        "facets": ["genres", "director"],
        "limit": 0,
    })
    print(f"  total documents in scope: {res.get('estimatedTotalHits')}")
    print_facets(res)

    section("Facets restricted to: rating > 8.5")
    res = index.search("", {
        "filter": "rating > 8.5",
        "facets": ["genres"],
        "limit": 0,
    })
    print(f"  total documents in scope: {res.get('estimatedTotalHits')}")
    print_facets(res)

    section("Combined: search 'crime' + facet by genre and year")
    res = index.search("crime", {
        "facets": ["genres", "year"],
        "limit": 3,
    })
    print(f"  total documents in scope: {res.get('estimatedTotalHits')}")
    for hit in res.get("hits", []):
        print(f"    > {hit['title']} ({hit['year']})")
    print_facets(res)


if __name__ == "__main__":
    main()
    print("\nFacet demo finished.\n")
