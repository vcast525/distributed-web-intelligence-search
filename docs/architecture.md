# Architecture Document

## Architecture Overview

The Distributed Web Intelligence Search Engine uses a containerized, distributed application architecture to collect, process, store, index, manage, and search web-based intelligence from approved external sources.

The system simulates how enterprise analysts could centralize external intelligence from regulatory, technology, risk, compliance, financial, cybersecurity, government, and industry sources within a single searchable application.

The architecture separates the user-facing dashboard, API communication, asynchronous job processing, web content retrieval, source repository management, document storage, search indexing, and infrastructure orchestration into distinct system layers.

This separation of responsibilities improves scalability, maintainability, reliability, and future extensibility.

---

## User-Facing Concept

The end user interacts with a centralized React dashboard that allows analysts to search indexed web intelligence collected from approved external sources.

The frontend provides the visual experience that is powered by the distributed backend architecture.

```text
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│              APEX FINANCIAL INTELLIGENCE                    │
│                                                             │
│  Intelligence Workspace              Source Library         │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🔎 FIND INDEXED CONTENT                                   │
│                                                             │
│  ┌─────────────────────────────────────────────┐            │
│  │ risk                                        │   SEARCH   │
│  └─────────────────────────────────────────────┘            │
│                                                             │
│  Search Scope                                               │
│  ┌─────────────────────────────────────────────┐            │
│  │ Entire Source Library                       │            │
│  └─────────────────────────────────────────────┘            │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  RESULTS                                                    │
│                                                             │
│  10 visible results shown from 10 total results for risk    │
│                                                             │
│  Federal Deposit Insurance Corporation                      │
│  fdic.gov                                                   │
│                                                             │
│  "...risk management..."                                    │
│                                                             │
│  Relevance Score: 12.58                                     │
│                                                             │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  Federal Reserve Bank of St. Louis                          │
│  stlouisfed.org                                             │
│                                                             │
│  "...economic data and financial risk..."                   │
│                                                             │
│  Relevance Score: 10.42                                     │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SOURCE LIBRARY                                             │
│                                                             │
│  100 indexed sources                                        │
│                                                             │
│  Source cards display source name, URL, HTTP status,        │
│  processing status, indexing status, and delete controls.   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
The Intelligence Workspace allows users to search indexed content using a keyword query and a defined Search Scope.

The Source Library allows users to review and manage the intelligence sources currently available to the platform.

The frontend makes the distributed backend system understandable and usable by presenting ingestion, search, source management, and system status through a clean user interface.

---

## User-Facing Pipeline Concept

The user-facing pipeline concept shows how the frontend can visually represent the backend ingestion, processing, storage, and indexing workflow.

This concept exists to make the distributed backend system easier to understand by connecting each backend component to something the user can see on screen.

```text

┌────────────────────────────────────────────────────────────────┐
│                                                                │
│              DISTRIBUTED WEB INTELLIGENCE                      │
│                                                                │
│  Submit approved sources for distributed retrieval,            │
│  processing, storage, indexing, and search.                    │
│                                                                │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  APPROVED SOURCE                                               │
│                                                                │
│  Name        Federal Reserve                                   │
│  URL         https://www.federalreserve.gov/                   │
│  Category    Regulatory & Government Intelligence              │
│                                                                │
│                      [ INGEST SOURCE ]                         │
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
│  SOURCE INFORMATION                                            │
│                                                                │
│  Name            Federal Reserve                               │
│                                                                │
│  URL             https://www.federalreserve.gov/               │
│                                                                │
│  Category        Regulatory & Government Intelligence          │
│                                                                │
│  HTTP Status     200 OK                                        │
│                                                                │
│  Crawled At      July 9, 2026                                  │
│                                                                │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  EXTRACTED CONTENT                                             │
│                                                                │
│  Federal Reserve Board - Home                                  │
│                                                                │
│  The Federal Reserve Board supervises and regulates            │
│  financial institutions and supports financial stability...    │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

This frontend concept helps connect backend engineering work to visible user value.

| User-Facing Element | Backend Component | What It Proves |
| --- | --- | --- |
| Approved Source | FastAPI ingestion endpoint and Pydantic models | The system can accept structured source metadata |
| Pipeline Status | Redis, Celery, crawler, processor, MongoDB, Elasticsearch | The distributed processing workflow can be observed across each stage |
| Crawled Status | Crawler service | The system contacted the approved external website |
| Processed Status | Processor service | The system extracted useful text from raw HTML |
| Stored Status | MongoDB | The system persisted the source document |
| Indexed Status | Elasticsearch | The system prepared the document for search |
| Source Information | MongoDB document fields | The system stores and exposes structured source metadata |
| Extracted Content | Processor output | The system produces cleaned text from raw HTML |

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

The user interacts only with the React frontend.

The frontend communicates with FastAPI through REST API requests.

FastAPI routes search requests to Elasticsearch, source management requests to MongoDB, and ingestion requests to Redis and Celery.

Redis coordinates queued ingestion jobs.

Celery workers process ingestion jobs asynchronously.

MongoDB stores source records and processed content.

Elasticsearch indexes searchable content and returns relevance-ranked search results.

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

The architecture contains three primary application workflows:

1. Source ingestion and distributed processing
2. Search and result retrieval
3. Source repository management

These workflows operate through shared backend services while remaining logically separated.

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
                          REACT FRONTEND
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
              ┌─────────────────┼─────────────────┬─────────────────┐
              │                 │                 │                 │
              ▼                 ▼                 ▼                 ▼
            POST               GET               GET              DELETE
      /api/v1/ingest     /api/v1/search    /api/v1/sources   /api/v1/sources/{id}
              │                 │                 │                 │
              ▼                 ▼                 ▼                 ▼
       Submit Sources     Search Content    Retrieve Sources   Delete Source
              │                 │                 │                 │
              ▼                 │                 ▼                 ▼
         API SCHEMAS            │         Source Manager       Source Manager
              │                 │                 │                 │
              ▼                 │                 ▼                 ▼
      PYDANTIC VALIDATION       │              MONGODB          MONGODB
              │                 │                 │                 │
              ▼                 │                 │                 ▼
      BACKEND APPLICATION       │                 │          ELASTICSEARCH
             LOGIC              │                 │
              │                 │                 │
              ▼                 │                 │
            REDIS               │                 │
              │                 │                 │
              ▼                 │                 │
        CELERY WORKERS          │                 │
              │                 │                 │
              ▼                 │                 │
          WEB CRAWLER           │                 │
              │                 │                 │
              ▼                 │                 │
           MONGODB              │                 │
              │                 │                 │
              ▼                 │                 │
     CONTENT PROCESSING         │                 │
          PIPELINE              │                 │
              │                 │                 │
              ▼                 ▼                 │
       ELASTICSEARCH ◄──── SEARCH SERVICE         │
              │                 │                 │
              ▼                 ▼                 ▼
        SEARCHABLE CONTENT   SEARCH RESULTS   SOURCE LIBRARY
              │                 │                 │
              └─────────────────┴─────────────────┘
                                │
                                ▼
                          FASTAPI API
                                │
                                ▼
                          REACT FRONTEND
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
5. The React frontend sends requests to the backend through API endpoints.
6. FastAPI provides the backend application framework and exposes the system’s API endpoints.
7. API schemas define the structure and validation rules for request and response data.
8. Pydantic validates incoming application data before it enters the backend processing workflow.
9. The ingestion endpoint accepts approved sources submitted for distributed web processing.
10. Redis coordinates asynchronous processing through message brokering.
11. Celery workers execute processing jobs outside the FastAPI request lifecycle.
12. The web crawler retrieves external web content.
13. MongoDB stores collected source metadata, raw content, and processed web documents.
14. The content processing pipeline extracts, transforms, and prepares web content for search indexing.
15. Elasticsearch indexes processed content and provides full-text search and relevance scoring.
16. The search endpoint receives user queries and retrieves matching content from Elasticsearch.
17. The sources endpoint retrieves Source Library information from MongoDB.
18. The delete source endpoint removes selected source records from MongoDB and Elasticsearch when available.
19. FastAPI returns structured responses to the frontend.
20. The frontend presents search results and Source Library information through the user-facing application.

In addition to the primary application workflow, the architecture contains a developer documentation and testing workflow.

Python code and Pydantic models define the API operations and data contracts used by the application. FastAPI uses these definitions to automatically generate an OpenAPI specification. Swagger UI reads the OpenAPI specification and provides developers and testers with a visual interface for exploring, understanding, and testing the application’s API endpoints.

The architecture therefore contains three primary application workflows:

* Web content ingestion and distributed processing
* Web intelligence search and result retrieval
* Source repository management

The ingestion workflow operates asynchronously to collect, validate, queue, crawl, store, process, and index external web content.

The search workflow operates synchronously to receive user queries, search previously indexed content, and return relevance-ranked results to the frontend application.

The source repository management workflow allows the frontend to retrieve, display, refresh, and delete indexed source records.

Together, these workflows demonstrate how business requirements, user-facing interfaces, APIs, data schemas, distributed processing systems, databases, search infrastructure, source management services, and developer tooling work together within a complete end-to-end software application.

---

## Frontend Layer

The frontend layer is implemented with React.

Frontend responsibilities include:

* Provide the main dashboard experience
* Display the APEX Financial Intelligence interface
* Accept keyword search queries
* Provide Search Scope selection
* Support Entire Source Library searches
* Support individual source selection
* Display search status messages
* Display relevance-ranked search results
* Display no-results states
* Display the Source Library
* Display indexed source count
* Display indexed source cards
* Refresh source repository data
* Delete individual sources
* Communicate with FastAPI through REST API calls

The frontend is organized around a clear information architecture:

* APEX Financial Intelligence
* Intelligence Workspace
* Query Workspace
* Search Scope
* Results
* Source Library
* Source Repository

The frontend shields users from backend complexity while demonstrating the value of the distributed architecture.

---

## Search Scope Behavior

The dashboard includes a Search Scope control that determines where the system searches.

The Search Scope supports:

* Entire Source Library
* Individual indexed source

### Entire Source Library

When a user enters a keyword and selects Entire Source Library, the system searches across all indexed sources.

### Individual Source Selection Without Keyword

When a user selects an individual source without a keyword query, the dashboard displays information about that selected indexed source.

### Keyword Search Within Individual Source

When a user enters a keyword and selects an individual source, the application evaluates search results against the selected source.

If matching results exist within the selected source, the matching results are displayed.

If no matching results exist within the selected source, the application displays a clear no-results message.

This behavior ensures the interface clearly distinguishes between searching the full repository, viewing a single indexed source, and searching within a specific source scope.

---

## API Layer

The API layer is built with FastAPI.

API responsibilities include:

* Accept ingestion requests
* Validate incoming request payloads
* Submit ingestion work to Celery
* Expose search endpoints
* Expose source management endpoints
* Expose health check endpoints
* Return structured JSON responses
* Provide Swagger/OpenAPI documentation
* Coordinate communication between frontend and backend services

FastAPI acts as the main gateway into the application.

The frontend never communicates directly with Redis, Celery, MongoDB, or Elasticsearch.

All user-facing requests flow through FastAPI.

---

## API Endpoint Architecture

The FastAPI application exposes endpoints supporting ingestion, search, source management, and system validation.

### Ingestion Endpoint

`POST /api/v1/ingest`

Accepts structured source ingestion requests and queues new sources for asynchronous processing.

### Search Endpoint

`GET /api/v1/search`

Searches indexed intelligence content through Elasticsearch.

### Sources Endpoint

`GET /api/v1/sources`

Retrieves indexed source repository records from MongoDB.

### Delete Source Endpoint

`DELETE /api/v1/sources/{document_id}`

Deletes an indexed source record from MongoDB and Elasticsearch.

### Health Endpoint

`GET /health`

Validates application availability.

---

## Bulk Ingestion Architecture

The project includes a bulk ingestion script that submits curated source records to the ingestion API.

The bulk ingestion process supports the 100-source intelligence repository.

The bulk ingestion workflow is:

1. Source records are stored in `data/source_taxonomy.json`.
2. `scripts/bulk_ingest_sources.py` loads the source file.
3. The script submits the source records to `POST /api/v1/ingest`.
4. FastAPI validates the structured source payload.
5. Existing duplicate sources are skipped.
6. New sources are queued through Redis.
7. Celery workers process queued ingestion jobs asynchronously.
8. MongoDB stores source records and processed content.
9. Elasticsearch indexes searchable content.
10. React displays the resulting Source Library.

The script submits all approved source records in one workflow instead of requiring manual entry through Swagger.

This demonstrates how bulk data ingestion can be automated in a distributed application.

---

## Ingestion Architecture

The ingestion architecture is responsible for collecting external web content and preparing it for search.

The ingestion workflow is:

1. An approved source enters the system through the ingestion endpoint.
2. FastAPI validates the request.
3. The application checks whether the URL already exists.
4. If the source already exists, it is skipped.
5. If the source is new, the ingestion job is submitted to Redis.
6. Celery workers retrieve queued ingestion jobs.
7. Workers retrieve web content from approved external URLs.
8. Retrieved content is processed.
9. MongoDB stores the source record and processed document.
10. Elasticsearch indexes the searchable document.
11. The indexed content becomes available to the search interface.

The ingestion workflow operates asynchronously.

FastAPI accepts the ingestion request and queues the processing work.

Celery workers execute the ingestion operation independently from the API request lifecycle.

---

## Queue and Coordination Layer

Redis provides message brokering and coordination between FastAPI and Celery.

Redis responsibilities include:

* Act as the Celery message broker
* Coordinate queued ingestion jobs
* Support asynchronous background processing
* Allow FastAPI and Celery workers to operate independently
* Prevent ingestion workloads from blocking API requests

Redis allows the API layer to remain responsive while background workers process ingestion jobs.

---

## Worker Layer

Celery workers execute long-running ingestion jobs.

Worker responsibilities include:

* Retrieve queued jobs from Redis
* Process structured source payloads
* Fetch external webpage content
* Process HTML content
* Create MongoDB documents
* Call Elasticsearch indexing services
* Log pipeline progress
* Return processing summaries

The worker pipeline follows five visible stages:

1. Source Received
2. Website Crawled
3. MongoDB Stored
4. Elasticsearch Indexed
5. Pipeline Completed

This clean logging structure makes the distributed ingestion process easier to observe and validate.

---

## Web Content Retrieval Layer

The web content retrieval layer requests content from approved external URLs.

Crawler responsibilities include:

* Send HTTP requests to approved source URLs
* Capture HTTP status codes
* Retrieve HTML content when available
* Return crawl success or failure information
* Support asynchronous execution within worker tasks

The current implementation retrieves content from the submitted source URL.

The system does not yet perform deep recursive crawling across every internal page, document, or linked resource within the external domain.

Recursive crawling is intentionally identified as a future enhancement.

---

## Processing Layer

The processing layer transforms retrieved HTML content into structured searchable information.

Processing responsibilities include:

* Parse HTML content
* Extract page title
* Extract headings
* Extract paragraphs
* Extract clean text
* Normalize HTML content
* Remove unnecessary formatting
* Prepare structured document fields

The processing layer creates the bridge between raw web content and searchable intelligence.

---

## Storage Layer

MongoDB stores source records, metadata, retrieved content, and processing information.

MongoDB responsibilities include:

* Store source name
* Store source category
* Store source URL
* Store HTTP status code
* Store page title
* Store clean text
* Store headings
* Store paragraphs
* Store raw HTML
* Store normalized HTML
* Store processing status
* Store indexing status
* Store crawl timestamps
* Store Elasticsearch document identifiers

MongoDB provides flexible document-based storage suitable for semi-structured web content.

The document-oriented MongoDB data model supports varying source structures without requiring a rigid relational schema.

---

## Indexing Layer

The indexing service prepares processed content for storage within Elasticsearch.

Indexing responsibilities include:

* Receive processed documents
* Structure indexed document fields
* Submit documents to Elasticsearch
* Maintain searchable source information
* Support downstream keyword retrieval
* Preserve source name and category metadata

Separating processing and indexing responsibilities improves modularity and future maintainability.

---

## Search Layer

Elasticsearch stores indexed content and powers the full-text search functionality.

Elasticsearch responsibilities include:

* Store searchable document content
* Maintain full-text search indexes
* Support keyword-based queries
* Calculate document relevance
* Rank matching search results
* Support efficient search retrieval
* Return structured search results
* Power backend search functionality

Elasticsearch transforms processed web content into searchable intelligence.

The search engine allows users to locate relevant information without manually reviewing every collected source.

---

## Source Management Layer

The Source Management layer retrieves and manages indexed source records.

Source management responsibilities include:

* Retrieve all indexed sources
* Return Source Library information to React
* Include source metadata in API responses
* Support Source Library refresh
* Support individual source deletion
* Remove deleted source records from MongoDB
* Remove corresponding indexed records from Elasticsearch when available

The Source Management layer supports the administrative side of the React dashboard.

---

## Infrastructure Layer

Docker Compose orchestrates the complete distributed application environment.

Infrastructure responsibilities include:

* Start the FastAPI API service
* Start the Celery worker service
* Start Redis
* Start MongoDB
* Start Elasticsearch
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

1. Administrator or bulk ingestion script submits approved sources.
2. FastAPI receives and validates the ingestion request.
3. Duplicate source checks determine whether the source has already been processed.
4. New ingestion jobs are submitted to Redis.
5. Celery workers retrieve queued jobs.
6. Workers initiate web content retrieval.
7. The crawler retrieves HTML and response metadata.
8. Content is processed into structured text fields.
9. MongoDB stores the source record, metadata, raw content, and processed content.
10. Elasticsearch indexes the processed document.
11. Indexed content becomes available through the search API.
12. React displays updated source repository information.

---

## Search Data Flow

The search workflow allows users to retrieve indexed web intelligence.

1. User enters a keyword search through the React frontend.
2. User selects a Search Scope.
3. React sends the search query to FastAPI.
4. FastAPI validates the search request.
5. FastAPI submits the query to Elasticsearch.
6. Elasticsearch performs a full-text search.
7. Matching documents are identified.
8. Search results are ranked by relevance.
9. Elasticsearch returns structured results to FastAPI.
10. FastAPI returns the results to React.
11. React applies Search Scope display logic when needed.
12. React displays results or a no-results message.

---

## Source Library Data Flow

The Source Library workflow allows users to review and manage indexed sources.

1. React requests indexed source records from FastAPI.
2. FastAPI routes the request to the source management service.
3. The source management service retrieves records from MongoDB.
4. FastAPI returns source data to React.
5. React displays the Source Library.
6. User may refresh the Source Library.
7. User may delete an individual source.
8. FastAPI processes the delete request.
9. MongoDB removes the selected source record.
10. Elasticsearch removes the corresponding indexed record when available.
11. React updates the Source Library display.

---

## Service Communication Architecture

Application services communicate through clearly defined interfaces.

```text
React Frontend
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
   ├──────────────► MongoDB
   │                    │
   │                    ▼
   │               Source Library
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

Frontend-to-backend communication occurs through HTTP and REST API requests.

FastAPI-to-Redis communication occurs when ingestion jobs are submitted to the background queue.

Redis-to-Celery communication occurs as workers retrieve queued ingestion tasks.

Celery workers communicate with external websites during web content retrieval.

Celery workers communicate with MongoDB to store source records and processed documents.

Celery workers communicate with Elasticsearch through the indexing service.

FastAPI communicates with MongoDB for source management operations.

FastAPI communicates with Elasticsearch for search operations.

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
        Source A       Source B       Source C
```

Additional Celery workers can be added without redesigning the primary application architecture.

This approach supports horizontal scaling.

As the number of ingestion jobs increases, additional worker instances can process queued work concurrently.

The current system demonstrates this concept using a worker-based architecture coordinated through Redis.

---

## Reliability Architecture

The architecture separates user-facing API requests from long-running background operations.

This separation provides several reliability benefits:

* API requests do not wait for web content retrieval operations to complete
* Failed crawling tasks do not directly crash the frontend experience
* Worker processes handle tasks independently
* Failed HTTP requests can be logged and managed
* Duplicate URLs can be detected before unnecessary processing
* MongoDB persists source and processing information
* Elasticsearch provides a dedicated search layer
* Search operations remain separate from ingestion operations
* Source management operations remain separate from ingestion processing
* Individual application services can be monitored independently

---

## Maintainability Architecture

The application uses a modular project structure that separates major system responsibilities.

The backend is organized into:

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

The frontend is organized under:

```text
frontend/
├── src/
│   ├── App.jsx
│   ├── App.css
│   ├── main.jsx
│   └── index.css
├── package.json
└── vite.config.js
```

Supporting assets and automation are organized under:

```text
docs/
├── images/
├── architecture.md
├── requirements.md
├── roadmap.md
├── technical_design.md
└── user_experience_flow.md

data/
└── source_taxonomy.json

scripts/
└── bulk_ingest_sources.py
```

Application modules are organized according to their responsibilities.

The api module contains REST API routes and request handling.

The core module contains shared configuration and logging setup.

The models module contains application data models and schemas.

The services module contains business logic, crawling functionality, content processing, database communication, source management, indexing, and search operations.

The workers module contains Celery configuration and distributed background tasks.

The frontend module contains the React user interface.

The data folder contains the curated source taxonomy used for bulk ingestion.

The scripts folder contains utility automation such as bulk source ingestion.

This modular design improves code organization, testing, maintainability, and future expansion.

---

## Architecture Benefits

* Clear separation between frontend and backend responsibilities
* Clear separation between ingestion, search, and source management workflows
* Asynchronous background processing
* Distributed worker-based execution
* Horizontally scalable ingestion architecture
* Centralized source repository
* Flexible document-based persistence
* Full-text search capability
* Relevance-ranked search results
* Search Scope behavior
* Source Library management
* API-driven application design
* Containerized infrastructure
* Modular backend project structure
* Integrated React frontend
* Improved system maintainability
* Improved fault isolation
* Support for future recursive crawling
* Support for future AI/RAG capabilities
* Enterprise-style architecture documentation

---

## Current Architecture Limitations

The completed Project #9 architecture intentionally focuses on the core distributed ingestion and search platform.

Current limitations include:

* The crawler processes submitted source pages only.
* The crawler does not yet perform recursive multi-page crawling.
* The system does not yet extract and process PDFs or external document files.
* Some websites may block automated requests or return rate-limit responses.
* The current search flow uses keyword-based Elasticsearch retrieval.
* The system does not yet generate AI summaries.
* The system does not yet provide source citations through an AI assistant.
* The current project is designed for local Docker-based development rather than production cloud deployment.
* The current testing approach is primarily manual validation.

These limitations are documented so that future enhancements can be scoped clearly.

---

## Future Architecture Enhancements

Potential future architecture enhancements include:

* Deep recursive web crawling
* Configurable crawl depth
* Internal link discovery
* Domain restrictions
* PDF and document ingestion
* Scheduled source monitoring
* Automated content refresh
* Enhanced retry strategies
* Dead-letter queue processing
* Search filtering and faceted searchokay h
* Advanced Elasticsearch aggregations
* Semantic search
* Vector embeddings
* Retrieval-Augmented Generation
* AI-generated intelligence summaries
* Natural-language question answering
* Source citations
* User authentication and authorization
* Role-based access control
* Source approval workflows
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

---

## Final Architecture Summary

The Distributed Web Intelligence Search Engine demonstrates a distributed, full-stack application architecture that connects a React dashboard, FastAPI backend, Redis message broker, Celery worker processing, MongoDB storage, Elasticsearch search indexing, Docker-based infrastructure, and source management capabilities.

The architecture supports approved source ingestion, asynchronous background processing, source metadata persistence, full-text search indexing, relevance-ranked retrieval, Source Library management, and Search Scope behavior.

The completed system provides a strong foundation for future enhancements such as recursive crawling, document ingestion, semantic search, and AI-powered Retrieval-Augmented Generation.