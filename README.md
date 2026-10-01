# Enterprise RAG AI Assistant

A production-oriented **Enterprise RAG AI Assistant** built with **FastAPI, LangChain, LangGraph, Google Gemini, PostgreSQL, pgvector, Redis, and React**.

The system enables authenticated users to upload enterprise documents and ask questions against their authorized documents. It combines document ingestion, semantic search, reranking, context-aware generation, citations, caching, rate limiting, and streaming responses.

---

## Features

* JWT authentication
* Secure password hashing
* User-isolated document access
* PDF document ingestion
* Intelligent document chunking
* Gemini embeddings
* PostgreSQL + pgvector vector search
* LangChain RAG pipeline
* LangGraph workflow orchestration
* Cross-encoder reranking
* Gemini LLM generation
* Citation-aware answers
* Redis response caching
* Redis-based rate limiting
* Conditional workflow routing
* Retrieval fallback handling
* Streaming LLM responses
* Async FastAPI architecture
* PostgreSQL persistence
* Alembic migrations
* Docker and Docker Compose support
* Pytest-ready architecture

---

# Architecture

```text
                              ┌─────────────────┐
                              │    React UI     │
                              │ TypeScript       │
                              └────────┬────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │    FastAPI      │
                              │      API        │
                              └────────┬────────┘
                                       │
                 ┌─────────────────────┼─────────────────────┐
                 │                     │                     │
                 ▼                     ▼                     ▼
            JWT Auth             Redis Cache          Rate Limiter
                 │                     │                     │
                 └─────────────────────┼─────────────────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │    LangGraph    │
                              │    Workflow     │
                              └────────┬────────┘
                                       │
                                       ▼
                                Cache Check
                                  /     \
                               HIT       MISS
                                │          │
                                │          ▼
                                │    Query Analyzer
                                │          │
                                │          ▼
                                │       Retriever
                                │          │
                                │          ▼
                                │       pgvector
                                │          │
                                │          ▼
                                │       Reranker
                                │          │
                                │          ▼
                                │   Document Check
                                │       /     \
                                │      NO      YES
                                │      │         │
                                │      ▼         ▼
                                │  Fallback   Context
                                │                │
                                │                ▼
                                │          Gemini LLM
                                │                │
                                │                ▼
                                │          Token Stream
                                │                │
                                └────────────────┤
                                                 ▼
                                             React UI
```

---

# Tech Stack

## Backend

* Python 3.11+
* FastAPI
* SQLAlchemy
* PostgreSQL
* pgvector
* Alembic
* Redis
* Pydantic

## AI / GenAI

* Google Gemini
* LangChain
* LangGraph
* Gemini Embeddings
* Sentence Transformers
* Cross-Encoder Reranker

## Frontend

* React
* TypeScript
* Tailwind CSS

## Infrastructure

* Docker
* Docker Compose
* PostgreSQL
* Redis

---

# Project Structure

```text
enterprise-rag-ai/
│
├── backend/
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   │
│   │   ├── api/
│   │   │   ├── deps.py
│   │   │   │
│   │   │   ├── schemas/
│   │   │   │
│   │   │   └── routes/
│   │   │       ├── auth.py
│   │   │       ├── users.py
│   │   │       ├── documents.py
│   │   │       └── chat.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   │
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   ├── database.py
│   │   │   └── models/
│   │   │
│   │   ├── cache/
│   │   │   ├── redis.py
│   │   │   ├── cache.py
│   │   │   └── rate_limit.py
│   │   │
│   │   ├── rag/
│   │   │   ├── loaders.py
│   │   │   ├── chunking.py
│   │   │   ├── embeddings.py
│   │   │   ├── ingestion.py
│   │   │   ├── repository.py
│   │   │   ├── retriever.py
│   │   │   ├── langchain_retriever.py
│   │   │   ├── document_mapper.py
│   │   │   ├── reranker.py
│   │   │   ├── context.py
│   │   │   ├── prompts.py
│   │   │   └── chain.py
│   │   │
│   │   ├── graph/
│   │   │   ├── state.py
│   │   │   ├── nodes.py
│   │   │   ├── workflow.py
│   │   │   └── streaming.py
│   │   │
│   │   └── llm/
│   │       └── provider.py
│   │
│   ├── alembic/
│   ├── tests/
│   ├── requirements.txt
│   ├── alembic.ini
│   └── .env
│
├── frontend/
│
├── docker-compose.yml
│
├── .gitignore
│
└── README.md
```

---

# Prerequisites

Install:

* Python 3.11+
* Node.js 20+
* Docker
* Docker Compose
* Git

You also need a Google Gemini API key.

---

# Clone the Repository

```bash
git clone <your-repository-url>

cd enterprise-rag-ai
```

---

# Start Infrastructure

Start PostgreSQL and Redis:

```bash
docker compose up -d
```

Check running containers:

```bash
docker ps
```

Expected services:

```text
enterprise_rag_postgres
enterprise_rag_redis
```

---

# PostgreSQL + pgvector

The application uses PostgreSQL with the `pgvector` extension.

Connect to PostgreSQL:

```bash
docker exec -it enterprise_rag_postgres psql \
  -U rag_user \
  -d enterprise_rag
```

Enable pgvector:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Verify:

```sql
SELECT extname
FROM pg_extension
WHERE extname = 'vector';
```

---

# Redis

Check Redis:

```bash
docker exec -it enterprise_rag_redis redis-cli ping
```

Expected:

```text
PONG
```

---

# Backend Setup

Move into the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

## Windows

```bash
venv\Scripts\activate
```

## Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create:

```text
backend/.env
```

Example:

```env
APP_NAME=Enterprise RAG AI

DATABASE_URL=postgresql+asyncpg://rag_user:rag_password@localhost:5432/enterprise_rag

REDIS_URL=redis://localhost:6379/0

JWT_SECRET=change-this-to-a-long-random-secret

JWT_ALGORITHM=HS256

DEBUG=true

GOOGLE_API_KEY=your_gemini_api_key
```

Never commit `.env` to Git.

Add:

```gitignore
.env
venv/
__pycache__/
.pytest_cache/
*.pyc
```

---

# Database Migrations

Run existing migrations:

```bash
alembic upgrade head
```

Create a migration after changing database models:

```bash
alembic revision --autogenerate -m "description"
```

Apply it:

```bash
alembic upgrade head
```

---

# Run FastAPI

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# Health Check

```http
GET /health
```

Example:

```bash
curl http://127.0.0.1:8000/health
```

Response:

```json
{
  "status": "ok"
}
```

---

# Authentication

The API uses JWT Bearer authentication.

## Register

```http
POST /auth/register
```

Example:

```json
{
  "email": "user@example.com",
  "password": "strongpassword"
}
```

---

## Login

```http
POST /auth/login
```

Example:

```json
{
  "email": "user@example.com",
  "password": "strongpassword"
}
```

Response:

```json
{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
}
```

Use the token:

```http
Authorization: Bearer <JWT_TOKEN>
```

---

# Authentication Flow

```text
Client
  │
  ▼
POST /auth/login
  │
  ▼
Verify Email + Password
  │
  ▼
Create JWT
  │
  ▼
Return Access Token
  │
  ▼
Client stores token
  │
  ▼
Authorization: Bearer <token>
  │
  ▼
get_current_user()
  │
  ▼
Decode JWT
  │
  ▼
user_id
```

---

# Current User

Protected endpoint:

```http
GET /users/me
```

FastAPI dependency:

```python
user_id: int = Depends(get_current_user)
```

Authentication dependency:

```text
Authorization Header
        ↓
HTTPBearer
        ↓
JWT Token
        ↓
decode_access_token()
        ↓
user_id
        ↓
Protected Endpoint
```

---

# Document Ingestion

The document ingestion pipeline:

```text
PDF
 │
 ▼
PyPDFLoader
 │
 ▼
Pages
 │
 ▼
RecursiveCharacterTextSplitter
 │
 ▼
Chunks
 │
 ▼
Gemini Embeddings
 │
 ▼
Vector Embeddings
 │
 ▼
PostgreSQL + pgvector
```

Current chunking configuration:

```text
chunk_size = 1000
chunk_overlap = 150
```

---

# RAG Pipeline

User question flow:

```text
User Question
      │
      ▼
Query Normalization
      │
      ▼
Gemini Embedding
      │
      ▼
pgvector Similarity Search
      │
      ▼
Top-K Candidates
      │
      ▼
Cross-Encoder Reranker
      │
      ▼
Top Relevant Documents
      │
      ▼
Context Builder
      │
      ▼
Gemini
      │
      ▼
Answer + Citations
```

---

# LangGraph Workflow

The RAG workflow is orchestrated using LangGraph.

```text
START
  │
  ▼
check_cache
  │
  ├──────── cached ────────► END
  │
  ▼
analyze_query
  │
  ▼
retrieve
  │
  ▼
rerank
  │
  ├──── no documents ────► fallback ───► END
  │
  ▼
build_context
  │
  ▼
generate
  │
  ▼
citations
  │
  ▼
cache
  │
  ▼
END
```

---

# LangGraph State

The workflow maintains state similar to:

```python
class RAGState(TypedDict):

    query: str

    user_id: int

    document_id: int | None

    retrieved_documents: list[Document]

    reranked_documents: list[Document]

    context: str

    answer: str

    citations: list[dict]

    cached: bool

    error: str | None
```

---

# Vector Search

The system uses PostgreSQL and pgvector for semantic retrieval.

Conceptually:

```text
User Query
    │
    ▼
Embedding Vector
    │
    ▼
pgvector
    │
    ▼
Cosine Similarity
    │
    ▼
Relevant Chunks
```

Retrieval is scoped to the authenticated user.

---

# Reranking

Initial vector search retrieves a larger candidate set.

Example:

```text
pgvector
   ↓
Top 20 candidates
   ↓
Cross Encoder
   ↓
Top 5 relevant documents
```

The reranker uses:

```text
BAAI/bge-reranker-base
```

This improves the relevance of the final context supplied to the LLM.

---

# Citations

Retrieved documents contain metadata such as:

```text
chunk_id
document_id
page_number
distance
rerank_score
```

The generated response can use this information to provide document/page references.

Example:

```text
According to the employee handbook, employees receive
20 annual leave days.

Source:
Employee Handbook — Page 12
```

---

# Redis Cache

Repeated questions can be cached.

## Cache Miss

```text
Request
   │
   ▼
Redis
   │
   └── MISS
         │
         ▼
       RAG
         │
         ▼
      Gemini
         │
         ▼
       Redis
```

## Cache Hit

```text
Request
   │
   ▼
Redis
   │
   └── HIT
         │
         ▼
    Cached Answer
```

Cache keys are scoped using:

```text
user_id
+
document_id
+
query hash
```

This prevents different users from accidentally sharing cached responses.

---

# Rate Limiting

Redis is used for distributed rate limiting.

Example configuration:

```python
RATE_LIMIT = 10
WINDOW_SECONDS = 60
```

Meaning:

```text
10 requests per minute per user
```

When the limit is exceeded:

```http
429 Too Many Requests
```

This protects:

* Gemini API usage
* Backend resources
* Database resources
* Application availability

---

# Streaming

The application supports streaming LLM responses.

Instead of waiting for the complete response:

```text
Gemini generates complete answer
        ↓
FastAPI sends answer
```

the system streams:

```text
Gemini
  │
  ├── token
  ├── token
  ├── token
  ├── token
  └── token
       │
       ▼
FastAPI StreamingResponse
       │
       ▼
React UI
```

This improves perceived response latency.

---

# Multi-Tenant Security

Every document belongs to a user.

```text
User A
 ├── Document A1
 ├── Document A2
 └── Document A3

User B
 ├── Document B1
 └── Document B2
```

User A must never retrieve User B's documents.

Retrieval therefore applies a user scope:

```text
document.user_id == current_user_id
```

This isolation must also be respected by:

* Vector search
* Document APIs
* Cache keys
* Conversation APIs
* Citation generation

---

# Error Handling

The application handles retrieval failures explicitly.

If no relevant documents are found:

```text
Retriever
    ↓
No relevant documents
    ↓
Fallback Node
    ↓
"I could not find relevant information
in the documents available to you."
```

The system should not blindly ask the LLM to answer when there is insufficient retrieved context.

---

# Testing

Run:

```bash
pytest
```

Verbose mode:

```bash
pytest -v
```

Recommended test structure:

```text
tests/
├── test_auth.py
├── test_users.py
├── test_documents.py
├── test_retrieval.py
├── test_rag.py
├── test_cache.py
├── test_rate_limit.py
└── test_chat.py
```

---

# Development Roadmap

## Phase 1 — Infrastructure

* [x] FastAPI setup
* [x] PostgreSQL
* [x] pgvector
* [x] Redis
* [x] Docker Compose

## Phase 2 — Authentication

* [x] User model
* [x] Registration
* [x] Login
* [x] Password hashing
* [x] JWT authentication
* [x] Protected routes
* [x] `get_current_user`

## Phase 3 — Gemini

* [x] Gemini LLM
* [x] Gemini embeddings
* [x] LangChain Gemini integration

## Phase 4 — RAG

* [x] PDF loader
* [x] Document chunking
* [x] Embeddings
* [x] pgvector retrieval
* [x] Context building
* [x] Citations

## Phase 5 — LangGraph

* [x] State
* [x] Nodes
* [x] Edges
* [x] Conditional routing
* [x] Retrieval node
* [x] Reranking node
* [x] Generation node
* [x] Citation node

## Phase 6 — Production Features

* [x] Redis cache
* [x] Rate limiting
* [x] Cache hit/miss routing
* [x] Retrieval fallback
* [x] Streaming architecture

## Phase 7 — Advanced RAG

* [ ] Hybrid search
* [ ] BM25
* [ ] Reciprocal Rank Fusion
* [ ] Query expansion
* [ ] Multi-query retrieval
* [ ] Context compression
* [ ] Advanced reranking
* [ ] Retrieval evaluation

## Phase 8 — Observability

* [ ] Structured logging
* [ ] Request IDs
* [ ] Metrics
* [ ] Distributed tracing
* [ ] Token usage tracking
* [ ] Latency tracking
* [ ] LLM observability
* [ ] LangSmith integration

## Phase 9 — Production Deployment

* [ ] Backend Docker image
* [ ] Frontend Docker image
* [ ] Nginx
* [ ] CI/CD
* [ ] Production secrets management
* [ ] Cloud deployment
* [ ] Monitoring
* [ ] Health checks
* [ ] Horizontal scaling

---

# Production Improvements

The following improvements are planned for a production deployment:

### Reliability

* Retry policies
* Timeouts
* Circuit breakers
* Graceful error handling
* Background document processing

### Security

* JWT expiration
* Refresh tokens
* Role-based access control
* Input validation
* File validation
* Upload size limits
* Secure secrets management

### RAG Quality

* Hybrid retrieval
* BM25
* Vector search
* Reciprocal Rank Fusion
* Query rewriting
* Reranking
* Context compression
* Evaluation datasets

### Performance

* Redis caching
* Async database access
* Streaming
* Connection pooling
* Batch embeddings
* Background ingestion

### Observability

* Structured logs
* Request IDs
* Metrics
* Traces
* Token usage
* LLM latency
* Retrieval latency
* Reranking latency

---

# Example End-to-End Flow

```text
1. User registers
        ↓
2. User logs in
        ↓
3. API returns JWT
        ↓
4. User uploads PDF
        ↓
5. PDF is parsed
        ↓
6. Document is chunked
        ↓
7. Gemini creates embeddings
        ↓
8. Embeddings stored in pgvector
        ↓
9. User asks a question
        ↓
10. JWT identifies user
        ↓
11. Rate limiter checks request
        ↓
12. Redis cache is checked
        ↓
13. Cache MISS
        ↓
14. LangGraph starts
        ↓
15. Query analyzed
        ↓
16. pgvector retrieves candidates
        ↓
17. Cross-encoder reranks candidates
        ↓
18. Relevant context is built
        ↓
19. Gemini generates response
        ↓
20. Response streams to React
        ↓
21. Citations are returned
        ↓
22. Result is cached
```

---

# Key Engineering Concepts

## 1. RAG

Retrieval-Augmented Generation combines document retrieval with LLM generation.

```text
Documents
   ↓
Retriever
   ↓
Relevant Context
   ↓
LLM
   ↓
Grounded Answer
```

---

## 2. LangChain

LangChain provides reusable components for:

* LLM integration
* Embeddings
* Document loaders
* Text splitters
* Retrievers
* Prompt templates
* RAG pipelines

---

## 3. LangGraph

LangGraph is used for explicit workflow orchestration.

It allows the application to model:

* State
* Nodes
* Edges
* Conditional routing
* Fallbacks
* Streaming
* Future retries
* Future human-in-the-loop workflows

---

## 4. pgvector

pgvector allows PostgreSQL to store and search embedding vectors.

This allows traditional relational data and vector search to coexist in the same database.

---

## 5. Redis

Redis is used for:

* Response caching
* Rate limiting
* Future session/state management
* Distributed coordination

---

## 6. Reranking

Vector similarity is useful for candidate retrieval, but a cross-encoder can perform a more detailed query-document relevance comparison.

```text
Query
  ↓
Vector Search
  ↓
20 candidates
  ↓
Cross Encoder
  ↓
5 best candidates
```

---

# Resume Project Description

## Enterprise RAG AI Assistant

> Built a production-oriented multi-tenant Enterprise RAG AI Assistant using FastAPI, LangChain, LangGraph, Google Gemini, PostgreSQL/pgvector, and Redis. Implemented JWT authentication, secure user-isolated document retrieval, PDF ingestion, semantic vector search, cross-encoder reranking, citation-aware generation, Redis caching, distributed rate limiting, conditional LangGraph workflows, retrieval fallback handling, and streaming LLM responses.

---

# Skills Demonstrated

```text
Python
FastAPI
Async Programming
REST APIs
JWT Authentication
PostgreSQL
SQLAlchemy
Alembic
pgvector
Redis
Docker
LangChain
LangGraph
RAG
Embeddings
Vector Search
Reranking
Prompt Engineering
Google Gemini
LLM Streaming
Caching
Rate Limiting
Multi-Tenant Architecture
AI System Design
Production GenAI Engineering
```

---

# Future Architecture

The final production architecture is planned to evolve toward:

```text
                         React
                           │
                           ▼
                        Nginx
                           │
                           ▼
                    FastAPI Instances
                     /      |       \
                    /       |        \
                 Auth     Redis     Metrics
                           │
                           ▼
                       LangGraph
                           │
            ┌──────────────┼──────────────┐
            │              │              │
         Query          Retrieval      Memory
         Router         Pipeline
                           │
                 ┌─────────┴─────────┐
                 │                   │
              Vector               BM25
              Search              Search
                 │                   │
                 └─────────┬─────────┘
                           │
                         RRF
                           │
                       Reranker
                           │
                    Context Builder
                           │
                         Gemini
                           │
                      Streaming
                           │
                         React

                    PostgreSQL
                         +
                      pgvector

                    Redis

                  Observability
```

---

# License

This project is intended for educational, portfolio, and learning purposes.

Add an appropriate open-source license before publicly distributing the project.
