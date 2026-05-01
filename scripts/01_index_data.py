"""Index the sample movies dataset into Meilisearch.

Run with:  python scripts/01_index_data.py
"""
import json
import os
import sys
import time
from pathlib import Path

import meilisearch
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

HOST = os.getenv("MEILI_HOST", "http://localhost:7700")
KEY = os.getenv("MEILI_MASTER_KEY", "aSampleMasterKeyForDevelopmentOnly")
INDEX_NAME = "movies"


def main() -> None:
    client = meilisearch.Client(HOST, KEY)

    print(f"Connecting to Meilisearch at {HOST} ...")
    health = client.health()
    print(f"  health: {health}")

    data_path = ROOT / "data" / "movies.json"
    with data_path.open(encoding="utf-8") as f:
        movies = json.load(f)
    print(f"Loaded {len(movies)} movies from {data_path.name}")

    index = client.index(INDEX_NAME)

    print("Configuring searchable + filterable + sortable attributes ...")
    index.update_settings({
        "searchableAttributes": ["title", "overview", "director", "genres"],
        "filterableAttributes": ["genres", "year", "director", "rating"],
        "sortableAttributes": ["year", "rating"],
        "rankingRules": [
            "words",
            "typo",
            "proximity",
            "attribute",
            "sort",
            "exactness",
            "rating:desc",
        ],
    })

    print(f"Adding documents to index '{INDEX_NAME}' ...")
    task = index.add_documents(movies, primary_key="id")
    print(f"  task uid: {task.task_uid}  status: {task.status}")

    print("Waiting for indexing to finish ...")
    final = client.wait_for_task(task.task_uid, timeout_in_ms=10_000)
    print(f"  final status: {final.status}  duration: {final.duration}")

    if final.status != "succeeded":
        print(f"Indexing failed: {final}")
        sys.exit(1)

    stats = index.get_stats()
    print(f"\nIndex ready. Documents: {stats.number_of_documents}")


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"\nDone in {time.time() - start:.2f}s")
