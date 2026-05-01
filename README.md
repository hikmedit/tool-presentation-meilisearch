# Meilisearch — YZV 322E Tool Presentation Demo

A reproducible demo of [Meilisearch](https://www.meilisearch.com/), the
developer-friendly open-source search engine, prepared for the
**YZV 322E Applied Data Engineering** Individual Tool Presentation
(Spring 2026, ITU).

- **Tool category:** Elasticsearch / Kibana (alternative search engine)
- **Author:** Hikmet Gultekin — 150220321
- **Course:** YZV 322E — Applied Data Engineering — Dr. Mehmet Tunçel

---

## 1. What is this tool?

Meilisearch is an open-source, RESTful search engine written in Rust. It is
designed for instant ("search-as-you-type") experiences with built-in typo
tolerance, prefix search, filtering, faceting, and sorting. It positions
itself as a lightweight, developer-friendly alternative to Elasticsearch /
OpenSearch when the use case is application search rather than log
analytics.

## 2. Prerequisites

| Requirement      | Tested with        |
| ---------------- | ------------------ |
| OS               | macOS 14+, Linux, Windows (WSL2) |
| Docker           | 24+ (tested on 28.4) |
| Docker Compose   | v2 (`docker compose`) |
| Python           | 3.10 – 3.14        |
| Free disk        | ~150 MB for the image |
| Free port        | `7700` (Meilisearch HTTP API) |

You only need Docker + Python. Nothing else has to be installed globally.

## 3. Installation (copy-pasteable)

```bash
# 1. Clone the repo
git clone https://github.com/hikmedit/tool-presentation-meilisearch.git
cd tool-presentation-meilisearch

# 2. Create the env file (the default master key is fine for the demo)
cp .env.example .env

# 3. Start Meilisearch in the background
docker compose up -d

# 4. Confirm it is healthy (should print {"status":"available"})
curl http://localhost:7700/health

# 5. Create a Python virtual environment and install the client
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 4. Running the example

Run the three scripts in order. Each one is independent of the others
(except that script 1 must run first to populate the index).

```bash
# A. Index the 40 sample movies into Meilisearch
python scripts/01_index_data.py

# B. Run the search feature tour: typo tolerance, filtering, highlighting
python scripts/02_search_demo.py

# C. Run the faceted-search demo (what you would build a sidebar from)
python scripts/03_facet_demo.py
```

You can also explore the index visually in the bundled web mini-dashboard:
open <http://localhost:7700> in a browser, paste the master key from `.env`,
and search the `movies` index live.

To shut everything down:

```bash
docker compose down            # stop the container, keep the data volume
docker compose down -v         # stop and remove the data as well
```

## 5. Expected output

### Script 1 — `01_index_data.py`

```
Connecting to Meilisearch at http://localhost:7700 ...
  health: {'status': 'available'}
Loaded 40 movies from movies.json
Configuring searchable + filterable + sortable attributes ...
Adding documents to index 'movies' ...
  task uid: 1  status: enqueued
Waiting for indexing to finish ...
  final status: succeeded  duration: PT0.0...S
Index ready. Documents: 40
Done in 0.3s
```

### Script 2 — `02_search_demo.py` (excerpt)

```
========================================================================
  2) Typo tolerance: 'godfther' (intentional typo)
========================================================================
  -> 1 hits shown / 1 total  [1 ms]
  - title='The Godfather' | year=1972 | rating=9.2

========================================================================
  3) Typo tolerance: 'inteseller' (heavy typo)
========================================================================
  -> 1 hits shown / 1 total  [1 ms]
  - title='Interstellar' | year=2014 | rating=8.7
```

The full demo prints eight numbered sections covering basic search, two
typo cases, prefix search, filter + sort, filtered search, highlighting, and
phrase queries.

### Script 3 — `03_facet_demo.py` (excerpt)

```
  facet: genres
    Drama                          24  ########################
    Action                         11  ###########
    Adventure                      11  ###########
    Crime                           9  #########
    Sci-Fi                          8  ########
    ...
```

A screenshot of these runs is included in `docs/expected_output.png`
(captured locally; see commit history).

## 6. Repository layout

```
.
├── docker-compose.yml      # single-service Meilisearch v1.11
├── requirements.txt        # meilisearch + python-dotenv
├── .env.example            # master key + host
├── data/movies.json        # 40 sample documents
├── scripts/
│   ├── 01_index_data.py    # configures settings + uploads documents
│   ├── 02_search_demo.py   # typo, filter, highlight, phrase
│   └── 03_facet_demo.py    # facet distribution
├── slides/
│   └── meilisearch_presentation.pptx
├── AI_USAGE.md             # AI usage disclosure
├── README.md               # this file
├── repo.txt                # public GitHub URL (submission deliverable)
└── video_link.txt          # unlisted YouTube link (submission deliverable)
```

## 7. Course connection

This tool maps to the **Elasticsearch / Kibana** week of the course. Like
Elasticsearch, Meilisearch builds an inverted index over JSON documents and
exposes a REST API; unlike Elasticsearch, it focuses exclusively on the
end-user search use case (instant search, typo tolerance) and ships with a
much smaller operational footprint — a single statically-linked Rust
binary, sub-second cold start, and an optional master-key authentication
model out of the box. In a course pipeline (NiFi / Kafka → search) you can
swap Elasticsearch for Meilisearch when the goal is product / catalog /
documentation search rather than log analytics.

## 8. AI usage disclosure

I used ChatGPT and Claude for research about Meilisearch and for coding
help while writing the demo scripts. See [`AI_USAGE.md`](./AI_USAGE.md).
