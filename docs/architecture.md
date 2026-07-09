# Architecture Document

## Architecture Overview

The Distributed Web Intelligence Search Engine uses a containerized, distributed application architecture to collect, store, process, index, and search web-based intelligence from approved external sources.

The system is designed to simulate how enterprise analysts could search across regulatory, technology, risk, compliance, and industry sources from one centralized application.

The architecture separates the user-facing search experience, API communication, asynchronous job processing, web crawling, raw content storage, content processing, search indexing, and infrastructure orchestration into distinct system layers.

This separation of responsibilities improves scalability, maintainability, reliability, and future extensibility.

---

## User-Facing Concept

The end user interacts with a centralized search interface that allows analysts to search indexed web intelligence collected from approved external sources.

The frontend provides the visual experience that is powered by the distributed backend architecture.

```text
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│              APEX FINANCIAL INTELLIGENCE                    │
│                                                             │
│  Dashboard     Search Intelligence     Sources     Admin    │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🔎 SEARCH COMPANY INTELLIGENCE                             │
│                                                             │
│  ┌─────────────────────────────────────────────┐            │
│  │ Artificial Intelligence Banking Regulation │   SEARCH   │
│  └─────────────────────────────────────────────┘            │
│                                                             │
│  Search across indexed regulatory and industry sources      │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  127 RESULTS FOUND                         SORT: RELEVANCE   │
│                                                             │
│  Federal Reserve Releases AI Banking Guidance               │
│  federalreserve.gov                                         │
│                                                             │
│  "...new artificial intelligence requirements for           │
│  financial institutions and risk management..."             │
│                                                             │
│  Relevance Score: 97%                                       │
│                                                             │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  OCC Announces Technology Risk Framework                    │
│  occ.gov                                                    │
│                                                             │
│  "...artificial intelligence risk management..."            │
│                                                             │
│  Relevance Score: 91%                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
## User-Facing Pipeline Concept

The user-facing pipeline concept shows how the frontend can visually represent the backend ingestion, processing, storage, and indexing workflow.

This concept exists to make the distributed backend system easier to understand by connecting each backend component to something the user can see on screen.

```text
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│              DISTRIBUTED WEB INTELLIGENCE                      │
│                                                                │
│  Submit URLs for distributed crawling, processing,             │
│  storage, indexing, and search.                                │
│                                                                │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ENTER WEBSITE URL                                             │
│                                                                │
│  ┌───────────────────────────────────────────────────────┐     │
│  │ https://example.com                                   │     │
│  └───────────────────────────────────────────────────────┘     │
│                                                                │
│                      [ INGEST URL ]                            │
│                                                                │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  PIPELINE STATUS                                               │
│                                                                │
│  🌐 Crawled     ✅ Completed                                   │
│                                                                │
│  🧹 Processed   ✅ Completed                                   │
│                                                                │
│  🗄️ Stored      ✅ MongoDB                                     │
│                                                                │
│  🔎 Indexed     ✅ Elasticsearch                               │
│                                                                │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  PAGE INFORMATION                                              │
│                                                                │
│  URL             https://example.com                           │
│                                                                │
│  Title           Example Domain                                │
│                                                                │
│  HTTP Status     200 OK                                        │
│                                                                │
│  Crawled At      July 9, 2026                                  │
│                                                                │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  EXTRACTED CONTENT                                             │
│                                                                │
│  Example Domain                                                │
│                                                                │
│  This domain is for use in illustrative examples...            │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

This frontend concept helps connect backend engineering work to visible user value.

| User-Facing Element | Backend Component | What It Proves |
| --- | --- | --- |
| Enter Website URL | FastAPI ingestion endpoint | The user can submit a URL into the system |
| Pipeline Status | Redis, Celery, crawler, processor, MongoDB, Elasticsearch | The user can see each processing stage |
| Crawled Status | Crawler service | The system contacted the external website |
| Processed Status | Processor service | The system extracted useful text from raw HTML |
| Stored Status | MongoDB | The system persisted the webpage document |
| Indexed Status | Elasticsearch | The system prepared the document for search |
| Page Information | MongoDB document fields | The user can see structured webpage metadata |
| Extracted Content | Processor output | The user can see cleaned text produced from raw HTML |

The goal is not only to build a backend system, but to make the backend system observable, understandable, and demonstrable through a visible user experience.
---

## High-Level Architecture

The high-level architecture demonstrates the primary interaction between the user-facing frontend, FastAPI backend, and Elasticsearch search engine.

```text
User
 ↓
Frontend Search Interface
 ↓
FastAPI REST API
 ↓
Elasticsearch Search Index
 ↓
Search Results Returned to User
```

The user interacts only with the frontend application.

The frontend communicates with FastAPI through REST API requests.

FastAPI processes the search request and communicates with Elasticsearch.

Elasticsearch searches indexed documents, calculates relevance scores, identifies matching content, and returns results to FastAPI.

FastAPI returns the structured search results to the frontend for presentation to the user.

---

## Ingestion Architecture

The ingestion architecture is responsible for collecting external web content and preparing it for search.

```text
Administrator
 ↓
FastAPI Ingestion Endpoint
 ↓
Redis Queue
 ↓
Celery Worker Pool
 ↓
Web Crawler
 ↓
MongoDB Raw Content Storage
 ↓
Text Processing Pipeline
 ↓
Elasticsearch Search Index
```

An administrator submits approved URLs or domains through the FastAPI ingestion endpoint.

FastAPI validates the request and submits ingestion jobs for asynchronous processing.

Redis coordinates queued jobs between the FastAPI application and Celery workers.

Celery workers retrieve queued jobs and execute the web crawling process outside the FastAPI request lifecycle.

The crawler retrieves HTML content and metadata from approved external websites.

Raw content is stored in MongoDB.

The processing pipeline transforms raw HTML into structured, searchable text.

Processed content is indexed into Elasticsearch.

---

## Full System Architecture

The complete system architecture connects the business requirements, user-facing application, API layer, data contracts, backend processing services, storage systems, and search infrastructure into a single distributed application.

The architecture demonstrates how a business requirement becomes a user-facing capability and how that capability is implemented through frontend components, API endpoints, backend services, and distributed infrastructure.

```text
                         BUSINESS PROBLEM
                                │
                                ▼
                    APPLICATION REQUIREMENTS
                                │
                                ▼
                     SOFTWARE CAPABILITIES
                                │
                                ▼
                    USER-FACING APPLICATION
                                │
                                ▼
                          FRONTEND UI
                                │
                                ▼
                     API REQUEST / RESPONSE
                                │
                                ▼
                           FASTAPI API
                                │
                                ▼
                         API ENDPOINTS
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼

            POST               GET               GET

      /api/v1/ingest     /api/v1/search        /health

              │                 │                 │
              ▼                 ▼                 ▼

        Submit URLs       Search Content     Check System
                                                 Health

              │                 │
              ▼                 │
         API SCHEMAS             │
              │                 │
              ▼                 │
      PYDANTIC VALIDATION        │
              │                 │
              ▼                 │
      BACKEND APPLICATION        │
             LOGIC               │
              │                 │
              ▼                 │
            REDIS               │
              │                 │
              ▼                 │
        CELERY WORKERS           │
              │                 │
              ▼                 │
          WEB CRAWLER            │
              │                 │
              ▼                 │
           MONGODB               │
              │                 │
              ▼                 │
     CONTENT PROCESSING          │
          PIPELINE               │
              │                 │
              ▼                 │
       ELASTICSEARCH ◄───────────┘
              │
              ▼
        SEARCH RESULTS
              │
              ▼
          FASTAPI API
              │
              ▼
          FRONTEND UI
              │
              ▼
    SEARCH RESULTS DISPLAYED
              │
              ▼
             USER


                  DEVELOPER DOCUMENTATION FLOW

                           PYTHON CODE
                                │
                                ▼
                         PYDANTIC MODELS
                                │
                                ▼
                           FASTAPI
                                │
                                ▼
                    OPENAPI SPECIFICATION
                                │
                                ▼
                          SWAGGER UI
                                │
                                ▼
                 DEVELOPERS EXPLORE AND TEST
                         API ENDPOINTS
```

The architecture can be understood as a complete end-to-end software engineering workflow:

1. A business problem establishes the need for the application.

2. Application requirements define what the software must accomplish.

3. Software capabilities translate those requirements into specific system functionality.

4. The user-facing application provides a visual interface through which users interact with those capabilities.

5. The frontend sends requests to the backend through API endpoints.

6. FastAPI provides the backend application framework and exposes the system's API endpoints.

7. API schemas define the structure and validation rules for request and response data.

8. Pydantic validates incoming application data before it enters the backend processing workflow.

9. The ingestion endpoint accepts URLs submitted for distributed web processing.

10. Redis coordinates asynchronous processing by supporting message brokering, rate limiting, and URL deduplication.

11. Celery workers execute processing jobs outside the FastAPI request lifecycle.

12. The web crawler retrieves external web content.

13. MongoDB stores the collected raw and processed web documents.

14. The content processing pipeline extracts, transforms, and prepares web content for search indexing.

15. Elasticsearch indexes the processed content and provides full-text search, relevance scoring, and result highlighting.

16. The search endpoint receives user queries and retrieves matching content from Elasticsearch.

17. FastAPI returns the search results to the frontend.

18. The frontend presents the results through the user-facing application.

In addition to the primary application workflow, the architecture contains a developer documentation and testing workflow.

Python code and Pydantic models define the API operations and data contracts used by the application. FastAPI uses these definitions to automatically generate an OpenAPI specification. Swagger UI reads the OpenAPI specification and provides developers and testers with a visual interface for exploring, understanding, and testing the application's API endpoints.

The architecture therefore contains two primary application workflows:

- Web content ingestion and distributed processing
- Web intelligence search and result retrieval

The ingestion workflow operates asynchronously to collect, validate, queue, crawl, store, process, and index external web content.

The search workflow operates synchronously to receive user queries, search previously indexed content, and return relevance-ranked results to the frontend application.

The architecture also supports a developer-facing documentation workflow through FastAPI, OpenAPI, and Swagger UI. This workflow allows developers to visually inspect and test backend capabilities without requiring the complete frontend application to be available.

Together, these workflows demonstrate how business requirements, user-facing interfaces, APIs, data schemas, distributed processing systems, databases, search infrastructure, and developer tooling work together within a complete end-to-end software application.

---

## Frontend Layer

The frontend layer represents the user-facing search experience.

Frontend responsibilities include:

* Provide a centralized search interface for analysts
* Accept keyword-based search queries
* Display relevance-ranked search results
* Display source URLs
* Display document titles
* Display highlighted matching content
* Display relevance scores
* Display indexed document counts
* Provide an administrative source ingestion interface
* Communicate with FastAPI through REST API endpoints

The frontend shields end users from the complexity of the distributed backend architecture.

Users interact with a simple search experience while the backend application manages ingestion, distributed processing, persistence, indexing, and retrieval.

---

## API Layer

The API layer is built using FastAPI and serves as the primary application gateway.

API responsibilities include:

* Accept ingestion requests
* Validate incoming request payloads
* Expose search endpoints
* Expose system health endpoints
* Return structured JSON responses
* Provide Swagger/OpenAPI documentation
* Route requests to backend services
* Coordinate communication between application components

The API layer separates frontend communication from internal application processing.

FastAPI does not perform long-running crawling operations directly.

Instead, ingestion jobs are submitted for asynchronous background processing.

---

## Queue and Coordination Layer

Redis provides fast, in-memory coordination between application components.

Redis responsibilities include:

* Act as the message broker for Celery
* Coordinate queued ingestion jobs
* Support API rate limiting
* Support URL deduplication
* Prevent unnecessary duplicate crawling
* Coordinate distributed worker activity
* Provide low-latency temporary state management

Redis allows the FastAPI application and Celery workers to operate independently.

This separation prevents long-running crawling operations from blocking API requests.

---

## Worker Layer

Celery workers execute long-running ingestion and crawling jobs outside the FastAPI request lifecycle.

Worker responsibilities include:

* Retrieve queued jobs through Redis
* Execute web crawling operations
* Fetch external web page content
* Parse HTML documents
* Handle failed HTTP requests
* Store raw page data
* Initiate downstream processing
* Support horizontal scaling through multiple worker instances

The worker architecture allows the application to distribute workloads across multiple independent processes.

Additional workers can be added as ingestion workloads increase.

---

## Crawling Layer

The crawling layer retrieves web content from approved external URLs and domains.

Crawler responsibilities include:

* Request web pages using an asynchronous HTTP client
* Respect application rate limits
* Capture HTTP response status codes
* Retrieve raw HTML content
* Extract basic page metadata
* Identify discovered URLs when applicable
* Prevent duplicate crawling
* Send collected content to MongoDB for persistence

The crawler operates through Celery workers rather than directly within the FastAPI application.

This design separates resource-intensive crawling operations from user-facing API requests.

---

## Storage Layer

MongoDB stores raw crawled web content and associated metadata.

MongoDB responsibilities include:

* Store source URLs
* Store page titles
* Store raw HTML
* Store HTTP status codes
* Store crawl timestamps
* Store content metadata
* Store ingestion information
* Support downstream content processing

MongoDB provides flexible document-based storage suitable for semi-structured and unstructured web content.

Raw web documents may contain varying metadata and content structures.

The document-oriented MongoDB data model supports this variability without requiring a rigid relational table structure.

---

## Processing Layer

The processing layer transforms raw web content into clean, structured, searchable information.

Processing responsibilities include:

* Retrieve raw content from MongoDB
* Remove irrelevant HTML elements
* Remove scripts and unnecessary page components
* Extract document titles
* Extract headings
* Extract paragraphs
* Extract metadata
* Normalize whitespace
* Clean text content
* Prepare documents for indexing
* Create structured searchable records
* Submit processed documents to Elasticsearch

The processing layer creates the bridge between raw web content storage and full-text search indexing.

---

## Search Layer

Elasticsearch stores indexed content and powers the full-text search functionality.

Elasticsearch responsibilities include:

* Store searchable document content
* Create full-text search indexes
* Support keyword-based queries
* Calculate document relevance
* Rank matching search results
* Provide highlighted matching text
* Support efficient search retrieval
* Return structured search results
* Power the `/api/v1/search` endpoint

Elasticsearch transforms processed web content into searchable business intelligence.

The search engine allows users to locate relevant information without manually reviewing every collected document.

---

## Infrastructure Layer

Docker Compose orchestrates the complete distributed application environment.

Infrastructure responsibilities include:

* Start the FastAPI service
* Start Redis
* Start MongoDB
* Start Elasticsearch
* Start Celery worker services
* Configure service communication
* Provide isolated application containers
* Support repeatable local development environments
* Simplify application startup
* Support future infrastructure expansion

Each major application component operates as an independent service.

Docker Compose coordinates these services and allows the complete distributed system to run as a unified application environment.

---

## Ingestion Data Flow

The ingestion workflow collects external web content and prepares it for search.

```text
1. Administrator submits approved URLs or domains.

2. FastAPI receives and validates the ingestion request.

3. Rate limiting rules are evaluated.

4. Redis receives and coordinates ingestion jobs.

5. URL deduplication rules determine whether content has already been processed.

6. Celery workers retrieve queued jobs.

7. Workers initiate web crawling operations.

8. The crawler retrieves raw HTML and page metadata.

9. Raw content is stored in MongoDB.

10. The processing pipeline retrieves raw content.

11. HTML content is cleaned and transformed into structured text.

12. Processed content is submitted to Elasticsearch.

13. Elasticsearch indexes the document.

14. Indexed content becomes available through the search API.
```

---

## Search Data Flow

The search workflow allows users to retrieve indexed web intelligence.

```text
1. User enters a keyword search through the frontend.

2. Frontend sends the search query to FastAPI.

3. FastAPI validates the search request.

4. FastAPI submits the query to Elasticsearch.

5. Elasticsearch performs a full-text search.

6. Matching documents are identified.

7. Search results are ranked by relevance.

8. Matching text is highlighted.

9. Elasticsearch returns structured results to FastAPI.

10. FastAPI returns the results to the frontend.

11. Frontend displays results to the user.
```

---

## Service Communication Architecture

Application services communicate through clearly defined interfaces.

```text
Frontend
   │
   │ HTTP / REST
   ▼
FastAPI
   │
   ├──────────────► Elasticsearch
   │                    │
   │                    ▼
   │               Search Results
   │
   ▼
Redis
   │
   ▼
Celery Workers
   │
   ├──────────────► External Websites
   │
   ▼
MongoDB
   │
   ▼
Processing Pipeline
   │
   ▼
Elasticsearch
```

FastAPI communicates with the frontend through REST API requests.

FastAPI communicates with Redis to submit asynchronous background jobs.

Celery workers communicate with Redis to retrieve queued work.

Workers communicate with approved external websites to retrieve content.

Workers and processing services communicate with MongoDB to persist and retrieve raw content.

The processing pipeline communicates with Elasticsearch to index searchable documents.

FastAPI communicates with Elasticsearch to execute user search queries.

---

## Scalability Architecture

The distributed worker architecture allows the system to scale as ingestion demand increases.

```text
                       Redis Queue
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
       Celery Worker  Celery Worker  Celery Worker
             │             │             │
             ▼             ▼             ▼
        Website A      Website B      Website C
```

Additional Celery workers can be added without redesigning the primary application architecture.

This approach supports horizontal scaling.

As the number of ingestion jobs increases, additional worker instances can process queued work concurrently.

---

## Reliability Architecture

The architecture separates user-facing API requests from long-running background operations.

This separation provides several reliability benefits:

* API requests do not wait for web crawling operations to complete
* Failed crawling tasks do not directly crash the frontend experience
* Worker processes can handle tasks independently
* Failed HTTP requests can be logged and managed
* Duplicate URLs can be detected before unnecessary processing
* Raw content remains persisted in MongoDB
* Search operations remain separate from ingestion operations
* Individual application services can be monitored independently

---

## Maintainability Architecture

The application uses a modular project structure that separates major system responsibilities.

```text
app/
├── api/
├── core/
├── models/
├── services/
├── workers/
├── __init__.py
└── main.py
```

Application modules are organized according to their responsibilities.

The `api` module contains REST API routes and request handling.

The `core` module contains application configuration and shared infrastructure settings.

The `models` module contains application data models and schemas.

The `services` module contains application business logic, crawling functionality, content processing, database communication, and search operations.

The `workers` module contains Celery configuration and distributed background tasks.

The `main.py` file serves as the FastAPI application entry point.

This modular design improves code organization, testing, maintainability, and future expansion.

---

## Architecture Benefits

* Clear separation between frontend and backend responsibilities
* Clear separation between ingestion and search workflows
* Asynchronous background processing
* Distributed worker-based execution
* Horizontally scalable crawling architecture
* Centralized raw content storage
* Flexible document-based persistence
* Full-text search capability
* Relevance-ranked search results
* Search result highlighting
* API-driven application design
* Containerized infrastructure
* Modular project structure
* Improved system maintainability
* Improved fault isolation
* Support for future enhancements
* Enterprise-style architecture documentation

---

## Future Architecture Enhancements

Potential future enhancements include:

* User authentication and authorization
* Role-based access control
* Source approval workflows
* Scheduled web crawling
* Automated content refresh
* Advanced crawl scheduling
* Additional Celery worker queues
* Dead-letter queue processing
* Enhanced retry strategies
* Distributed Bloom filter implementation
* Search filtering and faceted search
* Advanced Elasticsearch aggregations
* Search analytics
* User search history
* Saved searches
* Administrative monitoring dashboard
* Application metrics
* Distributed tracing
* Centralized logging
* Kubernetes orchestration
* Cloud deployment
* Managed MongoDB services
* Managed Elasticsearch services
* Automated CI/CD pipelines