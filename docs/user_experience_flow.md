# User Experience Flow Document

This document explains the user-facing application concept for the Distributed Web Intelligence Search Engine.

The purpose of this document is to connect the visible frontend experience to the backend architecture, infrastructure services, and business value of the application.

---

## User-Facing Application Concept

The end user interacts with a centralized search interface that allows analysts, business users, and recruiters to understand the value of the system visually.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│              APEX FINANCIAL INTELLIGENCE SEARCH                            │
│                                                                            │
│   Search publicly available business intelligence across the web           │
│                                                                            │
│   ┌──────────────────────────────────────────────────────────────┐  ┌────┐ │
│   │ Search company intelligence...                               │  │ 🔍 │ │
│   └──────────────────────────────────────────────────────────────┘  └────┘ │
│                                                                            │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  📊 SYSTEM OVERVIEW                                                        │
│                                                                            │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐ ┌─────────────┐ │
│  │  1,247         │ │  4,892         │ │  1,198         │ │  99.8%      │ │
│  │  Pages Crawled │ │  Documents     │ │  URLs Indexed  │ │  System     │ │
│  │                │ │  Processed     │ │                │ │  Health     │ │
│  └────────────────┘ └────────────────┘ └────────────────┘ └─────────────┘ │
│                                                                            │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  🔎 SEARCH RESULTS                                      127 RESULTS FOUND  │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ JPMorgan Chase Announces New Technology Investment                   │  │
│  │                                                                      │  │
│  │ www.example.com/business/technology                                  │  │
│  │                                                                      │  │
│  │ The company announced significant investments in cloud computing     │  │
│  │ and artificial intelligence infrastructure...                        │  │
│  │                                                                      │  │
│  │ RELEVANCE SCORE: 94%                                                 │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Financial Services Technology Trends                                 │  │
│  │                                                                      │  │
│  │ www.example.com/research/financial-services                          │  │
│  │                                                                      │  │
│  │ Financial institutions continue investing in distributed systems...   │  │
│  │                                                                      │  │
│  │ RELEVANCE SCORE: 87%                                                 │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ⚙️ SYSTEM HEALTH                                                         │
│                                                                            │
│  FastAPI       🟢 Operational        Redis          🟢 Operational         │
│  MongoDB       🟢 Operational        Elasticsearch  🟢 Operational         │
│  Celery        🟢 Operational                                              │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Full User-to-System Flow

```text
                            👤 BUSINESS USER
                                   │
                                   ▼
                    ┌────────────────────────────┐
                    │                            │
                    │       WEB INTERFACE        │
                    │                            │
                    │  🔎 Search Intelligence    │
                    │  📊 View System Metrics    │
                    │  ⚙️ View System Health     │
                    │                            │
                    └─────────────┬──────────────┘
                                  │
                                  │ API REQUEST
                                  ▼
                    ┌────────────────────────────┐
                    │                            │
                    │          FASTAPI           │
                    │                            │
                    │  POST /api/v1/ingest       │
                    │  GET  /api/v1/search       │
                    │  GET  /health              │
                    │                            │
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │                            │
                    │           REDIS            │
                    │                            │
                    │  📬 Message Broker         │
                    │  🚦 Rate Limiting          │
                    │  🔁 URL Deduplication      │
                    │                            │
                    └─────────────┬──────────────┘
                                  │
                                  │ JOB QUEUE
                                  ▼
                    ┌────────────────────────────┐
                    │                            │
                    │       CELERY WORKERS       │
                    │                            │
                    │  👷 Crawl Websites         │
                    │  👷 Fetch HTML             │
                    │  👷 Parse Content          │
                    │  👷 Process Jobs           │
                    │                            │
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │                            │
                    │          MONGODB           │
                    │                            │
                    │   🗄️ Store Raw Content     │
                    │   🗄️ Store Metadata        │
                    │   🗄️ Store Crawl Results   │
                    │                            │
                    └─────────────┬──────────────┘
                                  │
                                  │ CONTENT PROCESSING
                                  ▼
                    ┌────────────────────────────┐
                    │                            │
                    │       ELASTICSEARCH        │
                    │                            │
                    │   🔎 Index Content         │
                    │   🔎 Full-Text Search      │
                    │   🔎 Relevance Scoring     │
                    │   🔎 Result Highlighting   │
                    │                            │
                    └─────────────┬──────────────┘
                                  │
                                  │ SEARCH RESULTS
                                  ▼
                    ┌────────────────────────────┐
                    │                            │
                    │          FASTAPI           │
                    │                            │
                    │      RETURNS RESULTS       │
                    │                            │
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                              👤 USER
```

---

## Workflow 1: Build the Intelligence

This workflow explains how web content becomes searchable intelligence.

```text
Business submits approved URLs
        ↓
FastAPI receives ingestion request
        ↓
Redis queues ingestion jobs
        ↓
Celery workers retrieve jobs
        ↓
Crawler visits approved websites
        ↓
Raw HTML is stored in MongoDB
        ↓
Processing pipeline extracts clean text
        ↓
Elasticsearch indexes processed content
        ↓
Content becomes searchable
```

---

## Workflow 2: Use the Intelligence

This workflow explains how users search the indexed intelligence.

```text
User enters search keyword
        ↓
Frontend sends request to FastAPI
        ↓
FastAPI sends query to Elasticsearch
        ↓
Elasticsearch searches indexed documents
        ↓
Elasticsearch ranks results by relevance
        ↓
FastAPI returns structured results
        ↓
Frontend displays results to user
```

---

## User Experience and Backend Connection

| User Sees | Backend Component | Purpose |
| --- | --- | --- |
| Search bar | Frontend | Allows the user to enter a keyword query |
| Search request | FastAPI | Receives and validates the search query |
| Search results | Elasticsearch | Retrieves relevant indexed documents |
| Relevance score | Elasticsearch | Ranks results based on match quality |
| Highlighted text | Elasticsearch | Shows where the search term matched |
| System metrics | MongoDB and Elasticsearch | Shows crawled, processed, and indexed content counts |
| System health | FastAPI, Redis, MongoDB, Elasticsearch, Celery | Shows whether application services are operational |
| Admin ingestion | FastAPI and Redis | Allows approved URLs to be submitted for crawling |
| Background processing | Celery workers | Processes crawling jobs outside the API lifecycle |
| Raw content storage | MongoDB | Preserves original crawled web data |

---

## Why This User Experience Matters

The backend architecture exists to support a simple business-facing outcome:

Users need to search across collected web intelligence without manually visiting every source.

The frontend provides a simple search experience.

The backend provides the distributed processing, storage, indexing, and retrieval required to make that experience possible.

This document connects the visible product experience to the backend systems that power it.

---

## Click-Click-Click Summary

```text
User searches a topic
        ↓
Frontend sends request
        ↓
FastAPI receives request
        ↓
Elasticsearch searches indexed content
        ↓
Results are ranked and highlighted
        ↓
Frontend displays useful intelligence
        ↓
Business user finds information faster
```

```text
Administrator submits URLs
        ↓
FastAPI accepts ingestion request
        ↓
Redis queues the work
        ↓
Celery workers process the work
        ↓
MongoDB stores raw content
        ↓
Elasticsearch indexes clean content
        ↓
Search experience becomes possible
```

## Documentation Purpose

This document should be used as the visual anchor for Project #9.

Whenever a backend service, API endpoint, database collection, worker task, or search feature is added, it should connect back to this user experience flow.