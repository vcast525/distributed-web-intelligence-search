# Technical Design Document

## Solution Summary

The Distributed Web Intelligence Search Engine is a containerized, distributed full-stack application that collects, processes, stores, indexes, manages, and searches web-based intelligence from approved external sources.

The application provides enterprise analysts with a centralized intelligence workspace for retrieving relevant regulatory, technology, risk, compliance, financial, cybersecurity, government, and industry information.

The completed system combines a React frontend with a FastAPI backend and distributed processing infrastructure.

* React provides the user-facing Intelligence Workspace and Source Library.
* FastAPI provides the application REST API.
* Redis supports Celery message brokering and distributed job coordination.
* Celery workers execute background web retrieval and processing tasks outside the FastAPI request lifecycle.
* HTTPX retrieves web content asynchronously.
* BeautifulSoup parses HTML documents and extracts structured content.
* MongoDB stores source records, retrieved content, processing information, and indexing metadata.
* Elasticsearch indexes processed content and provides full-text search and relevance scoring.
* A bulk ingestion workflow populates the application with 100 approved intelligence sources.
* Docker Compose orchestrates the complete multi-service application environment.
* The completed application demonstrates frontend development, backend API design, asynchronous processing, distributed workers, database persistence, search indexing, source management, containerized infrastructure, technical documentation, and full-stack system integration.

---

## Technology Stack

### Frontend

* React
* JavaScript
* HTML
* CSS
* Vite

### Backend

* Python
* FastAPI
* Pydantic
* Pydantic Settings
* Uvicorn

### Distributed Processing

* Celery
* Redis

### Web Ingestion

* HTTPX
* BeautifulSoup

### Data Storage

* MongoDB
* PyMongo

### Search and Indexing

* Elasticsearch
* Elasticsearch Python Client

### Infrastructure

* Docker
* Docker Compose

### Development and Validation

* PyCharm
* Git
* GitHub
* Swagger/OpenAPI Documentation
* Browser-based functional testing
* Docker service validation
* FastAPI health checks

---

## Dependency Reference

| Package | Category | Purpose in This Project |
| --- | --- | --- |
| `fastapi` | Backend API | Builds REST API endpoints used for ingestion, search, source management, and system health |
| `uvicorn[standard]` | Application Server | Runs the FastAPI application |
| `celery` | Distributed Processing | Executes web retrieval and processing jobs outside the API request lifecycle |
| `redis` | Distributed Coordination | Supports Celery message brokering and background job coordination |
| `pymongo` | Database Client | Connects the Python application to MongoDB |
| `elasticsearch` | Search Client | Connects the application to the Elasticsearch search engine |
| `httpx` | HTTP Client | Retrieves external web pages asynchronously |
| `beautifulsoup4` | HTML Processing | Parses HTML and extracts useful web content |
| `pydantic-settings` | Configuration | Loads application settings from environment variables |

---

## Infrastructure Reference

| Service | Category | Purpose in This Project |
| --- | --- | --- |
| `api` | Application Service | Receives ingestion, search, source management, and health requests |
| `redis` | Coordination Service | Handles Celery message brokering and queued background work |
| `mongodb` | Document Database | Stores source records, retrieved web content, and processing metadata |
| `elasticsearch` | Search Engine | Indexes processed content and executes full-text searches |
| `worker` | Distributed Processing Service | Executes web retrieval, processing, storage, and indexing jobs outside the API lifecycle |
| `mongodb_data` | Persistent Volume | Preserves MongoDB data when containers restart |
| `elasticsearch_data` | Persistent Volume | Preserves Elasticsearch indexes when containers restart |

---

## Application Reference

| Component | Category | Purpose in This Project |
| --- | --- | --- |
| `app/main.py` | Application Entry Point | Creates and configures the FastAPI application |
| `app = FastAPI()` | FastAPI Application Object | Defines the running backend API application |
| `/health` | Health Check Endpoint | Confirms the API is running and responding |
| `/docs` | Swagger UI | Provides an interactive browser-based interface for API documentation and testing |
| OpenAPI | API Specification | Automatically describes available API endpoints and schemas |
| Uvicorn | Application Server | Runs the FastAPI application inside the API container |
| `app/models/ingestion.py` | Data Model Module | Stores request and response models for source ingestion |
| `BaseModel` | Pydantic Model Foundation | Defines and validates structured API data |
| `HttpUrl` | Validation Type | Ensures submitted values are valid HTTP or HTTPS URLs |
| `IngestionRequest` | Request Model | Defines structured source data submitted to the ingestion API |
| `IngestionResponse` | Response Model | Defines structured ingestion API responses |

---

## Frontend Reference

| Component | Category | Purpose in This Project |
| --- | --- | --- |
| `frontend/` | Frontend Application | Contains the React user interface |
| `frontend/src/App.jsx` | Primary React Component | Manages the primary dashboard structure, state, API communication, search behavior, and Source Library |
| `frontend/src/App.css` | Application Styling | Defines dashboard layout, visual hierarchy, responsive behavior, search components, result cards, and Source Library presentation |
| `frontend/src/main.jsx` | React Entry Point | Initializes and renders the React application |
| React State | Frontend State Management | Tracks search queries, selected Search Scope, search results, source records, loading states, and application messages |
| Fetch Requests | API Communication | Connects the React frontend to FastAPI endpoints |
| Search Scope | Search Control | Allows users to search the Entire Source Library or work with an individual indexed source |
| Search Intelligence | Status Interface | Communicates search execution information and result counts |
| Search Results | Results Interface | Displays relevance-ranked indexed content |
| Source Library | Source Management Interface | Displays and manages the 100-source intelligence repository |

---

## Distributed Processing Reference

| Component | Category | Purpose in This Project |
| --- | --- | --- |
| `app/workers/celery_app.py` | Distributed Processing Configuration | Creates and configures the Celery application |
| `Celery` | Distributed Task Queue | Executes background jobs outside the FastAPI request lifecycle |
| `app/workers/tasks.py` | Worker Task Module | Stores background jobs executed by Celery workers |
| `@celery_app.task` | Task Registration | Registers a Python function as a Celery background task |
| `process_ingestion_job` | Background Task | Receives and processes an individual source ingestion job |
| Task Result | Worker Output | Returns structured information after processing completes |
| `broker` | Message Transport | Uses Redis to deliver queued tasks to Celery workers |
| `backend` | Result Storage | Uses Redis to store task status and results |
| `task_serializer` | Data Serialization | Converts task data into JSON for transport |
| `result_serializer` | Result Serialization | Converts task results into JSON |
| `accept_content` | Security and Configuration | Restricts accepted task message formats |
| `timezone` / `enable_utc` | Time Configuration | Standardizes distributed task timestamps |
| `asyncio` | Async Execution Support | Allows synchronous Celery tasks to execute asynchronous crawler functions |
| `asyncio.run()` | Async Runtime Bridge | Runs asynchronous web retrieval from inside a Celery worker task |
| `crawl_result` | Crawler Result Object | Stores the structured response returned by the crawler service |

---

## Web Retrieval Reference

| Component | Category | Purpose in This Project |
| --- | --- | --- |
| `app/services/crawler.py` | Crawler Service Module | Stores web page retrieval logic |
| `fetch_url` | Crawler Function | Requests a webpage and returns structured response data |
| `httpx.AsyncClient` | Async HTTP Client | Retrieves webpage content asynchronously from submitted URLs |
| Request Timeout | Request Safety Setting | Prevents the crawler from waiting indefinitely for an external website response |
| `status_code` | HTTP Response Metadata | Captures the HTTP status code returned by the target website |
| `content` | Raw Web Content | Stores the HTML content returned by the webpage |
| `RequestError` | Error Handling | Captures network, timeout, and connection failures |

---

## Content Processing Reference

| Component | Category | Purpose in This Project |
| --- | --- | --- |
| `app/services/processor.py` | Content Processing Service | Centralizes webpage parsing and text extraction logic |
| `BeautifulSoup` | HTML Parser | Parses raw HTML retrieved by the crawler |
| `process_html()` | Processing Function | Converts raw HTML into structured, searchable webpage content |
| `soup` | Parsed HTML Object | Provides programmatic access to webpage elements |
| `title` | Metadata Extraction | Extracts the webpage title |
| `headings` | Content Extraction | Extracts heading text |
| `paragraphs` | Content Extraction | Extracts paragraph text from the webpage |
| `clean_text` | Searchable Content | Combines extracted content into normalized searchable text |
| `processed_content` | Processing Result Object | Stores structured content returned by the processing service |
| `processing_status` | Processing Metadata | Identifies the current stage of the webpage ingestion lifecycle |

---

## Database Persistence Reference

| Component | Category | Purpose in This Project |
| --- | --- | --- |
| MongoDB Client | Database Client | Creates the application's connection to MongoDB |
| `MONGODB_URL` | Connection String | Identifies the MongoDB service used by the application |
| Database Connection | Database Infrastructure | Maintains communication between the Python application and MongoDB |
| Application Database | Document Database | Stores persistent data collected and processed by the application |
| Webpage Collection | MongoDB Collection | Stores individual source and webpage documents retrieved by the crawler |
| Source Records | Persistent Documents | Store source metadata, retrieved content, processing information, and indexing status |

---

## Search Indexing Reference

| Component | Category | Purpose in This Project |
| --- | --- | --- |
| `app/services/indexer.py` | Search Indexing Service | Centralizes Elasticsearch indexing logic |
| `Elasticsearch` | Search Client | Connects the Python application to Elasticsearch |
| `ELASTICSEARCH_URL` | Connection String | Identifies the Elasticsearch service used by the application |
| Search Index | Elasticsearch Index | Stores processed searchable documents |
| Indexing Function | Index Operation | Sends processed webpage content into Elasticsearch |
| `search_document` | Searchable Document | Contains cleaned content fields used for search |
| `client.index()` | Elasticsearch Index Operation | Inserts a searchable document into the Elasticsearch index |
| `elasticsearch_id` | Search Document Identifier | Stores the unique document identifier created by Elasticsearch |
| `index_result` | Indexing Result Object | Stores structured metadata returned after successful Elasticsearch indexing |

---

## Search Service Reference

| Component | Category | Purpose in This Project |
| --- | --- | --- |
| `app/services/search.py` | Search Service | Centralizes Elasticsearch search logic |
| Keyword Query | Search Input | Contains the intelligence term submitted by the user |
| Elasticsearch Query | Search Operation | Searches indexed document content |
| Relevance Score | Search Ranking | Represents Elasticsearch relevance scoring for matching documents |
| Search Results | Search Output | Returns structured matching documents |
| Total Results | Search Metadata | Identifies the number of results returned by the search operation |
| Search Scope | Frontend Search Control | Determines whether results are evaluated across the Entire Source Library or an individual indexed source |

---

## Source Management Reference

| Component | Category | Purpose in This Project |
| --- | --- | --- |
| `app/services/source_manager.py` | Source Management Service | Centralizes Source Library retrieval and deletion operations |
| Source Retrieval | Repository Operation | Retrieves indexed source records from MongoDB |
| Source Metadata | Repository Data | Provides source name, category, URL, HTTP status, and processing information |
| Source Deletion | Repository Operation | Removes selected source records |
| Elasticsearch Cleanup | Search Maintenance | Removes corresponding indexed records when available |
| Source Refresh | Frontend Operation | Retrieves current Source Library information from the backend |

---

## Bulk Ingestion Reference

| Component | Category | Purpose in This Project |
| --- | --- | --- |
| `scripts/bulk_ingest_sources.py` | Bulk Ingestion Utility | Automates submission of multiple approved intelligence sources |
| Source Taxonomy | Source Collection | Defines the approved source records used to populate the intelligence repository |
| FastAPI Ingestion Endpoint | Submission Interface | Accepts structured source records from the bulk ingestion script |
| Duplicate Detection | Ingestion Control | Prevents unnecessary repeated processing of existing sources |
| Redis | Queue Infrastructure | Coordinates accepted ingestion jobs |
| Celery Workers | Processing Infrastructure | Process accepted source ingestion jobs asynchronously |
| 100-Source Repository | Application Dataset | Provides a substantial collection of approved external intelligence sources |

---

## Technology Selection Rationale

### React

React provides the frontend application layer.

React was selected because it supports:

* Component-based user interface development
* Application state management
* Dynamic content rendering
* Event-driven user interaction
* REST API communication
* Conditional interface behavior
* Maintainable frontend development

React provides the user-facing Intelligence Workspace and Source Library.

The React frontend transforms the distributed backend architecture into a usable business application.

---

### Python

Python is used as the primary backend application programming language.

Python provides strong support for API development, asynchronous HTTP communication, web content processing, distributed task execution, database connectivity, search engine integration, and automation.

The Python ecosystem provides mature libraries for every major backend component required by the application.

---

### FastAPI

FastAPI provides the REST API layer.

FastAPI was selected because it supports:

* High-performance API development
* Asynchronous request handling
* Pydantic data validation
* Automatic Swagger/OpenAPI documentation
* Modular route organization
* Integration with Python backend services

FastAPI serves as the primary application gateway for ingestion requests, search requests, source management operations, and system health checks.

---

### Redis

Redis provides fast in-memory coordination between distributed application components.

Redis primarily supports:

* Celery message brokering
* Background job coordination

Redis was selected because its low-latency in-memory architecture is well suited for distributed coordination.

---

### Celery

Celery provides asynchronous distributed task processing.

Celery workers execute long-running web retrieval and content processing operations outside the FastAPI request lifecycle.

Celery was selected because it supports:

* Background job execution
* Distributed worker processing
* Task queue management
* Worker scalability
* Integration with Redis

The Celery architecture allows additional worker instances to be added as ingestion workloads increase.

---

### HTTPX

HTTPX provides asynchronous HTTP communication for retrieving external web pages.

HTTPX was selected because it supports:

* Asynchronous HTTP requests
* Connection pooling
* Request timeout configuration
* HTTP status handling
* Modern Python async programming

HTTPX allows crawler workers to retrieve web content efficiently.

---

### BeautifulSoup

BeautifulSoup provides HTML parsing and content extraction.

BeautifulSoup was selected because it supports:

* HTML document parsing
* DOM traversal
* Element extraction
* Metadata extraction
* Text extraction
* Web content processing

BeautifulSoup transforms raw HTML documents into content that can be cleaned, processed, stored, and indexed.

---

### MongoDB

MongoDB provides persistent storage for source records and retrieved web content.

MongoDB was selected because web content is semi-structured and may contain varying metadata and document structures.

MongoDB supports:

* Flexible document storage
* JSON-like data models
* Raw HTML persistence
* Processed content storage
* Source metadata storage
* Processing metadata
* Scalable document-based architecture

MongoDB acts as the primary system of record for ingested source information.

---

### Elasticsearch

Elasticsearch provides full-text search and content indexing.

Elasticsearch was selected because it supports:

* Full-text search
* Relevance scoring
* Search result ranking
* Scalable indexing
* Structured search responses

Elasticsearch transforms processed web content into searchable business intelligence.

---

### Docker

Docker provides isolated application environments for each major system component.

Docker was selected because it supports:

* Service isolation
* Repeatable environments
* Dependency management
* Application portability
* Simplified local development

---

### Docker Compose

Docker Compose orchestrates the complete multi-service application.

Docker Compose manages:

* FastAPI
* Redis
* MongoDB
* Elasticsearch
* Celery workers

Docker Compose allows the complete distributed system to be started and managed through a centralized infrastructure configuration.

---

## Project Structure

    distributed-web-intelligence-search/
    │
    ├── app/
    │   ├── api/
    │   ├── core/
    │   ├── models/
    │   ├── services/
    │   ├── workers/
    │   ├── __init__.py
    │   └── main.py
    │
    ├── data/
    │   └── source_taxonomy.json
    │
    ├── docs/
    │   ├── images/
    │   │   ├── 01_dashboard-overview.png
    │   │   ├── 02_search-results.png
    │   │   ├── 03_search-scope.png
    │   │   ├── 04_source-repository.png
    │   │   ├── 05_swagger-api.png
    │   │   └── 06_distributed-infrastructure.png
    │   ├── architecture.md
    │   ├── requirements.md
    │   ├── roadmap.md
    │   ├── technical_design.md
    │   └── user_experience_flow.md
    │
    ├── frontend/
    │   ├── src/
    │   │   ├── App.jsx
    │   │   ├── App.css
    │   │   ├── main.jsx
    │   │   └── index.css
    │   ├── package.json
    │   └── vite.config.js
    │
    ├── scripts/
    │   └── bulk_ingest_sources.py
    │
    ├── .env
    ├── .env.example
    ├── .gitignore
    ├── docker-compose.yml
    ├── Dockerfile
    ├── README.md
    └── requirements.txt

---

## Application Module Design

### API Module

The `app/api` module contains FastAPI route definitions.

The module separates API endpoints according to their application responsibilities.

#### Health API

Responsibilities include:

* Expose the health check endpoint
* Return API availability status
* Support infrastructure validation

#### Ingestion API

Responsibilities include:

* Accept structured source submissions
* Validate ingestion requests
* Check for existing sources
* Submit background tasks
* Return ingestion status information

#### Search API

Responsibilities include:

* Accept keyword search queries
* Validate search parameters
* Query Elasticsearch
* Return relevance-ranked results

#### Source Management API

Responsibilities include:

* Retrieve indexed source records
* Return Source Library information
* Process individual source deletion requests

---

### Core Module

The `app/core` module contains shared application infrastructure and configuration.

Responsibilities include:

* Load environment variables
* Define application settings
* Configure service connection information
* Centralize application configuration
* Configure database connectivity
* Configure Redis connectivity
* Configure Elasticsearch connectivity
* Configure application logging

---

### Models Module

The `app/models` module contains Pydantic models and application data structures.

#### Ingestion Models

Responsibilities include:

* Define source ingestion request structures
* Define ingestion response structures
* Validate source names
* Validate source categories
* Validate source URLs

#### Search Models

Responsibilities include:

* Define search result structures
* Define search response structures
* Provide consistent API response contracts

---

### Services Module

The `app/services` module contains application business logic.

Service responsibilities include:

* Web content retrieval
* HTML processing
* MongoDB persistence
* Elasticsearch indexing
* Search execution
* Source repository management
* Duplicate source detection

The modular service architecture prevents business logic from being concentrated directly within API route functions.

---

### Workers Module

The `app/workers` module contains Celery configuration and distributed background tasks.

Worker responsibilities include:

* Initialize Celery
* Configure Redis message brokering
* Register worker tasks
* Execute source ingestion jobs
* Coordinate crawler services
* Process retrieved content
* Store source records
* Trigger Elasticsearch indexing
* Log distributed pipeline progress
* Handle processing failures

---

## API Design

### Health Check Endpoint

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/health` | Validate API availability |

Example response:

    {
      "status": "healthy",
      "service": "distributed-web-intelligence-search"
    }

---

### Ingestion Endpoint

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | `/api/v1/ingest` | Submit an approved intelligence source for ingestion |

The completed ingestion workflow accepts structured source metadata.

Example conceptual request:

    {
      "name": "Federal Reserve",
      "category": "Regulatory & Government Intelligence",
      "url": "https://www.federalreserve.gov/"
    }

The ingestion endpoint:

1. Receives the source submission.
2. Validates the request through Pydantic.
3. Checks whether the source already exists.
4. Skips existing duplicate sources when appropriate.
5. Queues new source ingestion work.
6. Returns structured status information.

---

### Search Endpoint

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/api/v1/search` | Search indexed web intelligence |

The search endpoint accepts a keyword query and retrieves relevance-ranked content from Elasticsearch.

Example conceptual request:

    GET /api/v1/search?q=risk

Example conceptual response:

    {
      "query": "risk",
      "total_results": 10,
      "results": [
        {
          "title": "Example Search Result",
          "url": "https://example.com",
          "score": 9.8,
          "content": "Example indexed content containing the requested keyword."
        }
      ]
    }

---

### Sources Endpoint

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/api/v1/sources` | Retrieve indexed source repository records |

The sources endpoint returns source information used by the React Source Library.

Returned information may include:

* Source name
* Source category
* Source URL
* HTTP status
* Processing status
* Indexing status
* Crawl timestamp

---

### Delete Source Endpoint

| Method | Endpoint | Purpose |
| --- | --- | --- |
| DELETE | `/api/v1/sources/{document_id}` | Delete an individual indexed source |

The deletion workflow:

1. Receives the selected document identifier.
2. Locates the source record.
3. Removes the source record from MongoDB.
4. Removes the corresponding indexed Elasticsearch document when available.
5. Returns structured deletion status.
6. Allows React to refresh the Source Library.

---

## Ingestion Request Model

The ingestion request model validates incoming source submissions.

| Field | Data Type | Description |
| --- | --- | --- |
| name | String | Human-readable intelligence source name |
| category | String | Intelligence classification assigned to the source |
| url | HTTP URL | Approved external source URL |

The ingestion endpoint validates that:

* A source name is provided
* A source category is provided
* A valid HTTP or HTTPS URL is provided
* Request payloads follow the required schema

---

## MongoDB Document Design

MongoDB stores source information and processed web content as document records.

Stored information may include:

| Field | Data Type | Description |
| --- | --- | --- |
| source_name | String | Human-readable source name |
| source_category | String | Intelligence category |
| url | String | Original submitted URL |
| title | String | Retrieved webpage title |
| raw_html | String | Original retrieved HTML |
| normalized_html | String | Normalized HTML content |
| clean_text | String | Extracted searchable content |
| headings | Array | Extracted webpage headings |
| paragraphs | Array | Extracted webpage paragraphs |
| status_code | Integer | HTTP response status |
| crawled_at | DateTime | Web retrieval timestamp |
| processing_status | String | Current processing state |
| indexing_status | String | Current indexing state |
| elasticsearch_id | String | Corresponding Elasticsearch document identifier |

MongoDB acts as the primary system of record for source information and retrieved content.

---

## Elasticsearch Document Design

Processed documents are indexed into Elasticsearch.

Indexed information may include:

| Field | Data Type | Description |
| --- | --- | --- |
| source_name | Text or Keyword | Human-readable source name |
| source_category | Keyword | Intelligence classification |
| url | Keyword | Original source URL |
| title | Text | Searchable webpage title |
| headings | Text | Extracted webpage headings |
| content | Text | Clean searchable content |
| crawled_at | Date | Original retrieval timestamp |
| indexed_at | Date | Search indexing timestamp |

Elasticsearch uses the indexed fields to support:

* Keyword search
* Full-text retrieval
* Relevance scoring
* Search result ranking

---

## Bulk Ingestion Design

The bulk ingestion workflow populates the application with approved intelligence sources.

The workflow is:

1. Curated source information is maintained in the project data collection.
2. `bulk_ingest_sources.py` loads approved source records.
3. The script submits sources to the FastAPI ingestion endpoint.
4. FastAPI validates each request.
5. Duplicate sources are identified.
6. Existing sources are skipped when appropriate.
7. New ingestion jobs are queued.
8. Redis coordinates queued jobs.
9. Celery workers process the sources.
10. MongoDB stores source information.
11. Elasticsearch indexes searchable content.
12. React displays the completed Source Library.

The bulk ingestion utility eliminates the need to submit 100 sources manually.

---

## Redis Design

Redis supports distributed message brokering and background processing coordination.

### Message Brokering

Redis coordinates task communication between FastAPI and Celery workers.

The workflow is:

    FastAPI
       ↓
    Redis Queue
       ↓
    Celery Workers

Redis allows FastAPI to submit background work without waiting for ingestion processing to complete.

---

## Celery Task Design

The primary ingestion task coordinates the distributed web processing workflow.

The task workflow is:

    Receive Structured Source
       ↓
    Validate Source Information
       ↓
    Check Existing Source
       ↓
    Fetch Web Page
       ↓
    Capture HTTP Response
       ↓
    Process HTML
       ↓
    Store MongoDB Document
       ↓
    Index Elasticsearch Document
       ↓
    Complete Task

Celery tasks support:

* Background execution
* Worker logging
* Error handling
* Distributed worker execution
* Separation from the API request lifecycle

The completed worker pipeline logs five major stages:

1. Source Received
2. Website Crawled
3. MongoDB Stored
4. Elasticsearch Indexed
5. Pipeline Completed

---

## Web Retrieval Design

The web retrieval service processes approved source URLs.

The system:

* Accepts an approved external source URL
* Sends an asynchronous HTTP request
* Applies request timeout configuration
* Captures HTTP response status
* Retrieves available HTML content
* Returns structured crawl results
* Handles request failures

The current implementation processes the submitted source page.

The system does not yet recursively crawl every internal page or linked document within an external website.

Deep recursive crawling is reserved as a future enhancement.

---

## Content Processing Design

The content processing service transforms raw HTML into structured searchable information.

The processing workflow is:

    Raw HTML
       ↓
    BeautifulSoup Parsing
       ↓
    Page Title Extraction
       ↓
    Heading Extraction
       ↓
    Paragraph Extraction
       ↓
    Text Cleaning
       ↓
    Structured Content
       ↓
    MongoDB Persistence
       ↓
    Elasticsearch Indexing

The processing layer creates the bridge between retrieved web content and searchable intelligence.

---

## Search Design

The search workflow allows users to retrieve indexed intelligence.

The workflow is:

    User Keyword
       ↓
    React Search Interface
       ↓
    FastAPI Search Endpoint
       ↓
    Search Service
       ↓
    Elasticsearch Query
       ↓
    Relevance-Ranked Results
       ↓
    FastAPI Response
       ↓
    React Results Interface

The search service:

* Accepts keyword queries
* Submits search operations to Elasticsearch
* Retrieves matching documents
* Returns relevance scores
* Returns structured search information
* Supports frontend Search Scope behavior

---

## Search Scope Design

The Search Scope control determines how the frontend evaluates and presents search behavior.

Available Search Scope options include:

* Entire Source Library
* Individual indexed source

### Entire Source Library Search

When a user enters a keyword and selects Entire Source Library:

1. React submits the keyword search.
2. FastAPI queries Elasticsearch.
3. Elasticsearch returns relevance-ranked results.
4. React displays the available matching results.
5. Search Intelligence displays execution and result count information.

### Individual Source Selection

When a user selects an individual source without entering a keyword:

1. React updates the selected Search Scope.
2. The application displays the selected source information.
3. The user can review the individual indexed source.

### Keyword Search Within Individual Source

When a user enters a keyword and selects an individual source:

1. React submits the keyword query.
2. FastAPI queries Elasticsearch.
3. Search results are returned.
4. React evaluates results against the selected source.
5. Matching source results are displayed.
6. If no matching results exist, a clear no-results message is displayed.

---

## Source Library Design

The Source Library provides the source repository management interface.

The Source Library displays:

* Total indexed source count
* Source name
* Source category
* Source URL
* HTTP status
* Processing status
* Indexing status
* Source management controls

Source Library functionality includes:

* Retrieve indexed source records
* Refresh Source Library data
* Select individual sources
* Delete individual source records

The Source Library connects React, FastAPI, the Source Management service, MongoDB, and Elasticsearch.

---

## Frontend Design

The React frontend provides the complete user-facing web intelligence experience.

The completed interface includes:

* Application branding
* Intelligence Workspace navigation
* Source Library navigation
* Keyword search input
* Search button
* Search Scope control
* Entire Source Library selection
* Individual source selection
* Search Intelligence status information
* Search execution messages
* Search result count information
* Relevance-ranked search result cards
* No-results messaging
* Clear search functionality
* Source Library repository
* Indexed source count
* Source metadata cards
* Source refresh functionality
* Individual source deletion

The frontend communicates with FastAPI through REST API requests.

The interface provides a visual layer over the distributed backend architecture.

---

## Frontend State Design

React state manages dynamic application behavior.

Application state includes:

* Search query
* Search results
* Search execution status
* Search messages
* Selected Search Scope
* Source records
* Source count
* Loading states
* Error states

State changes occur when:

* The user enters a keyword
* The user submits a search
* The user changes Search Scope
* Search results are returned
* No matching results are found
* The user clears search results
* Source records are loaded
* The Source Library is refreshed
* A source is deleted

The frontend state design allows the interface to respond dynamically without requiring full-page browser reloads.

---

## User Experience Design

The application interface separates major functionality into understandable sections.

### Intelligence Workspace

Provides the primary search experience.

### Find Indexed Content

Allows users to enter keyword queries.

### Search Scope

Allows users to define where searches are evaluated.

### Search Intelligence

Provides search execution and status information.

### Search Results

Displays relevance-ranked indexed content.

### Source Library

Displays and manages the indexed intelligence repository.

The interface uses visual hierarchy, spacing, dividers, cards, status messaging, and consistent terminology to distinguish application functionality.

---

## Docker Compose Design

Docker Compose orchestrates the complete distributed application environment.

Configured services include:

| Service | Responsibility |
| --- | --- |
| API | Run the FastAPI application |
| Redis | Coordinate Celery background jobs |
| MongoDB | Store source records and retrieved web content |
| Elasticsearch | Store and search indexed content |
| Celery Worker | Execute distributed background processing jobs |

The architecture supports additional Celery worker instances.

A conceptual scaling strategy is:

    docker compose up --scale worker=3

This configuration allows multiple workers to process queued ingestion jobs concurrently.

---

## Environment Configuration

Application configuration is managed through environment variables.

Environment settings may include:

    APP_NAME
    APP_ENV
    REDIS_URL
    MONGODB_URL
    MONGODB_DATABASE
    ELASTICSEARCH_URL
    ELASTICSEARCH_INDEX
    CRAWLER_REQUEST_TIMEOUT
    CELERY_BROKER_URL

The `.env.example` file documents required configuration values without storing application secrets.

---

## Error Handling Strategy

The application handles common system failures through structured backend and frontend behavior.

Error scenarios include:

* Invalid URLs
* HTTP request timeouts
* Connection failures
* Unavailable websites
* Non-success HTTP responses
* Duplicate sources
* Redis connection failures
* MongoDB connection failures
* Elasticsearch connection failures
* Celery task failures
* Invalid search queries
* Search queries returning no matching results
* Source deletion failures
* Frontend API communication failures

Errors are logged with sufficient information to support troubleshooting.

API errors return structured responses without exposing sensitive internal system information.

The frontend provides understandable user-facing status and error messages where appropriate.

---

## Logging Strategy

Application logging provides visibility into distributed system operations.

Logging events include:

* API startup
* Ingestion requests
* Search requests
* Duplicate source detection
* Task submission
* Worker task execution
* Web retrieval activity
* HTTP failures
* MongoDB persistence
* Content processing
* Elasticsearch indexing
* Search execution
* Source retrieval
* Source deletion
* Application errors

Worker logs identify major processing stages to improve pipeline observability.

---

## Validation and Testing Strategy

Project #9 uses multiple forms of application validation.

### Infrastructure Validation

Infrastructure validation confirms:

* FastAPI container operation
* Celery worker operation
* Redis container operation
* MongoDB container operation
* Elasticsearch container operation

The distributed environment is validated through Docker Compose service status.

### Health Validation

The FastAPI health endpoint confirms application availability.

Expected response:

    {
      "status": "healthy",
      "service": "distributed-web-intelligence-search"
    }

### API Validation

Swagger/OpenAPI documentation supports interactive API exploration and endpoint validation.

API validation includes:

* Health endpoint requests
* Ingestion requests
* Search requests
* Source retrieval requests
* Source deletion requests

### Ingestion Validation

Ingestion validation confirms:

* Structured source requests are accepted
* Duplicate sources are handled
* Jobs are queued
* Celery workers process jobs
* Web retrieval executes
* MongoDB records are created
* Elasticsearch documents are indexed

### Bulk Ingestion Validation

Bulk ingestion validation confirms:

* Approved source records are loaded
* Sources are submitted to FastAPI
* Existing sources are skipped when appropriate
* New sources are processed
* The Source Library reaches the expected 100-source repository

### Search Validation

Search validation includes three primary scenarios.

#### Scenario 1: Entire Source Library Search

* Enter a keyword query
* Keep Search Scope set to Entire Source Library
* Submit the search
* Confirm relevance-ranked results appear
* Confirm Search Intelligence displays accurate result information

#### Scenario 2: Individual Source Selection

* Clear the keyword query
* Select an individual source
* Confirm the selected source information appears correctly

#### Scenario 3: Keyword Search Within Individual Source

* Enter a keyword query
* Select an individual source
* Submit the search
* Confirm matching results appear when available
* Confirm a no-results message appears when no source-specific matches exist

### Frontend Validation

Frontend validation confirms:

* Dashboard loads successfully
* Navigation functions correctly
* Search input accepts queries
* Search Scope updates correctly
* Search requests execute successfully
* Search Intelligence messaging is accurate
* Search Results display correctly
* No-results messaging is understandable
* Clear search functionality works
* Source Library loads correctly
* Indexed source count is accurate
* Source refresh works
* Source deletion works

### Documentation Validation

Documentation validation confirms:

* README reflects the completed application
* Requirements reflect implemented functionality
* Architecture reflects the completed system
* Technical design reflects actual application components
* User experience documentation reflects the completed frontend
* Roadmap distinguishes completed functionality from future enhancements
* Application screenshots are stored and referenced correctly

---

## Security Considerations

The application includes foundational security and responsible processing considerations.

Security considerations include:

* Input validation
* URL validation
* Environment-based configuration
* Protection of application secrets
* Controlled external requests
* Structured error handling
* Avoidance of sensitive information in logs
* Separation between frontend and backend infrastructure
* API-based access to backend services

Future enhancements may include:

* User authentication
* Role-based authorization
* Administrative permissions
* API keys
* Audit logging
* Network restrictions

---

## Performance Considerations

Application performance considerations include:

* Asynchronous HTTP requests
* Distributed worker processing
* Redis in-memory coordination
* MongoDB document storage
* Elasticsearch optimized search indexes
* Configurable worker scaling
* Duplicate source detection
* Separation of ingestion and search workloads
* React state-based interface updates

The distributed architecture allows individual components to scale according to workload requirements.

---

## Current Technical Limitations

The completed Project #9 implementation intentionally focuses on the core distributed ingestion and search platform.

Current limitations include:

* Web retrieval processes submitted source pages rather than recursively crawling entire websites.
* The application does not yet extract and index linked PDF documents.
* Some external websites may block automated requests.
* Some external websites may return rate-limit responses.
* Search currently uses keyword-based Elasticsearch retrieval.
* The application does not yet support semantic search.
* The application does not yet generate AI summaries.
* The application does not yet provide Retrieval-Augmented Generation.
* The application does not yet provide AI-generated source citations.
* The current implementation uses local Docker-based infrastructure rather than production cloud deployment.
* Testing primarily focuses on functional and integration validation rather than a comprehensive automated test suite.

---

## Future Enhancements

Potential future enhancements include:

* Deep recursive web crawling
* Internal link discovery
* Configurable crawl depth
* Domain restrictions
* PDF and document ingestion
* Scheduled crawling
* Automated content refresh
* Source change detection
* Advanced retry strategies
* Dead-letter queues
* Search filters
* Faceted search
* Elasticsearch aggregations
* Search analytics
* Saved searches
* Search history
* Semantic search
* Vector embeddings
* Retrieval-Augmented Generation
* AI-generated intelligence summaries
* Natural-language question answering
* Source citations
* User authentication
* Role-based access control
* Administrative monitoring
* Prometheus metrics
* Grafana dashboards
* Distributed tracing
* Centralized logging
* Kubernetes deployment
* Cloud infrastructure
* Managed MongoDB
* Managed Elasticsearch
* Automated CI/CD workflows

---

## Final Technical Design Summary

The Distributed Web Intelligence Search Engine demonstrates the technical design of a distributed, full-stack software application.

The completed system integrates:

* React
* FastAPI
* Pydantic
* Redis
* Celery
* HTTPX
* BeautifulSoup
* MongoDB
* Elasticsearch
* Docker
* Docker Compose
* Swagger/OpenAPI
* Git
* GitHub

The technical design supports structured source ingestion, bulk ingestion of 100 approved intelligence sources, asynchronous background processing, external web retrieval, HTML processing, persistent document storage, Elasticsearch indexing, keyword-based search, relevance-ranked retrieval, Search Scope behavior, Source Library management, source deletion, API documentation, and a professional React dashboard.

The completed application demonstrates how frontend components, REST APIs, distributed workers, message brokers, databases, search engines, automation scripts, containerized infrastructure, and technical documentation work together within a complete software engineering project.

The architecture also provides a defined path toward future advanced capabilities including deep recursive crawling, semantic search, vector retrieval, and AI-powered Retrieval-Augmented Generation.