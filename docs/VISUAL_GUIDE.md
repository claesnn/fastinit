# 🎯 fastinit - Visual Quick Reference

## Installation Flow

```
┌─────────────────────────────────────────────────────────┐
│                    Install fastinit                     │
└─────────────────────────────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    ┌─────────┐      ┌─────────┐      ┌─────────┐
    │ Windows │      │  Unix   │      │   Pip   │
    │         │      │   Mac   │      │         │
    └─────────┘      └─────────┘      └─────────┘
          │                │                │
          ▼                ▼                ▼
    install.ps1      install.sh       pip install -e .
          │                │                │
          └────────────────┴────────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Verify with:    │
                  │ fastinit       │
                  │ version         │
                  └─────────────────┘
```

## Project Creation Flow

```
┌─────────────────────────────────────────────────────────┐
│         fastinit init my-api [OPTIONS]                  │
└─────────────────────────────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    ┌─────────┐      ┌─────────┐      ┌─────────┐
    │  --db   │      │  --jwt  │      │ --docker│
    │         │      │         │      │         │
    └─────────┘      └─────────┘      └─────────┘
          │                │                │
          ▼                ▼                ▼
    SQLAlchemy       PyJWT/         Dockerfile
    + Database       PyJWKClient      docker-
    Session          + Security       compose.yml
                     Utils
                           │
          ┌────────────────┴────────────────┐
          │                                  │
          ▼                                  ▼
    ┌──────────────┐              ┌──────────────┐
    │   my-api/    │              │  Generated   │
    │   ├── app/   │              │  Files:      │
    │   ├── tests/ │              │  - main.py   │
    │   ├── .env   │              │  - config.py │
    │   └── ...    │              │  - deps.py   │
    └──────────────┘              └──────────────┘
```

## Component Generation Flow

```
┌─────────────────────────────────────────────────────────┐
│            fastinit new crud Product                    │
│            --fields "name:str,price:float"               │
└─────────────────────────────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    ┌──────────┐     ┌──────────┐    ┌──────────┐
    │  Model   │     │ Service  │    │  Route   │
    │          │     │          │    │          │
    └──────────┘     └──────────┘    └──────────┘
          │                │                │
          ▼                ▼                ▼
    product.py     product_service.py  products.py
    (SQLAlchemy)   (CRUD methods)      (REST API)
          │                │                │
          └────────────────┴────────────────┘
                           │
                           ▼
              ┌───────────────────────┐
              │  Complete CRUD API:   │
              │  GET /products        │
              │  GET /products/{id}   │
              │  POST /products       │
              │  PUT /products/{id}   │
              │  DELETE /products/{id}│
              └───────────────────────┘
```

## Project Structure Visualization

```
my-api/
├── 📁 app/
│   ├── 🐍 main.py                    ← FastAPI app entry point
│   │
│   ├── 📁 api/                       ← API layer
│   │   ├── 🐍 deps.py               ← Dependencies (DB, Auth)
│   │   └── 📁 routes/               ← API routes
│   │       ├── 🐍 health.py         ← Health checks
│   │       └── 🐍 products.py       ← Generated routes
│   │
│   ├── 📁 core/                      ← Core utilities
│   │   ├── 🐍 config.py             ← Settings (Pydantic)
│   │   └── 🐍 security.py           ← JWT utilities
│   │
│   ├── 📁 db/                        ← Database layer
│   │   ├── 🐍 base.py               ← SQLAlchemy Base
│   │   └── 🐍 session.py            ← Session factory
│   │
│   ├── 📁 models/                    ← Database models
│   │   └── 🐍 product.py            ← Generated model
│   │
│   ├── 📁 services/                  ← Business logic
│   │   └── 🐍 product_service.py    ← Generated service
│   │
│   └── 📁 schemas/                   ← Pydantic schemas
│
├── 📁 tests/                         ← Test suite
│   └── 🐍 test_api.py
│
├── 📄 .env.example                   ← Environment template
├── 📄 .gitignore                     ← Git ignore rules
├── 📄 requirements.txt               ← Python dependencies
├── 🐳 Dockerfile                     ← Container config
├── 🐳 docker-compose.yml            ← Services orchestration
└── 📖 README.md                      ← Project docs
```

## Feature Options Matrix

```
╔═══════════════════╦═════════╦═════════╦═════════╦═════════╗
║    Feature        ║   DB    ║   JWT   ║ Logging ║ Docker  ║
╠═══════════════════╬═════════╬═════════╬═════════╬═════════╣
║ Basic Project     ║    -    ║    -    ║    -    ║    -    ║
║ With Database     ║    ✓    ║    -    ║    -    ║    -    ║
║ With Auth         ║    -    ║    ✓    ║    -    ║    -    ║
║ With Logging      ║    -    ║    -    ║    ✓    ║    -    ║
║ With Docker       ║    -    ║    -    ║    -    ║    ✓    ║
║ Full Stack        ║    ✓    ║    ✓    ║    ✓    ║    ✓    ║
╚═══════════════════╩═════════╩═════════╩═════════╩═════════╝
```

## Database Options

```
┌─────────────────────────────────────────────────────────┐
│                   --db --db-type                         │
└─────────────────────────────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    ┌──────────┐     ┌──────────┐    ┌──────────┐
    │PostgreSQL│     │  MySQL   │    │  SQLite  │
    │          │     │          │    │          │
    │ Port:    │     │ Port:    │    │ File:    │
    │ 5432     │     │ 3306     │    │ app.db   │
    └──────────┘     └──────────┘    └──────────┘
          │                │                │
          ▼                ▼                ▼
    psycopg2-binary   pymysql         (built-in)
```

## JWT Authentication Flow

```
┌─────────────────────────────────────────────────────────┐
│                  Client Request                          │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
              ┌───────────────────────┐
              │  POST /auth/login     │
              │  {username, password} │
              └───────────────────────┘
                           │
                           ▼
          ┌────────────────────────────────┐
          │  Create JWT Token:             │
          │  - PyJWT.encode()              │
          │  - Set expiration              │
          │  - Sign with SECRET_KEY        │
          └────────────────────────────────┘
                           │
                           ▼
              ┌───────────────────────┐
              │  Return Token:        │
              │  {"access_token": "…"}│
              └───────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│         GET /api/protected                               │
│         Authorization: Bearer <token>                    │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
          ┌────────────────────────────────┐
          │  Verify Token:                 │
          │  - PyJWT.decode()              │
          │  - Check expiration            │
          │  - Validate signature          │
          │  OR                            │
          │  - PyJWKClient.verify()        │
          │    (for remote JWKs)           │
          └────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
        ┌─────────┐              ┌─────────┐
        │ Valid   │              │ Invalid │
        │ ✓       │              │ ✗       │
        └─────────┘              └─────────┘
              │                         │
              ▼                         ▼
        Protected                 401 Unauthorized
        Resource
```

## Docker Deployment Flow

```
┌─────────────────────────────────────────────────────────┐
│              docker-compose up                           │
└─────────────────────────────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    ┌──────────┐     ┌──────────┐    ┌──────────┐
    │   Web    │     │Database  │    │  Network │
    │ Service  │     │ Service  │    │          │
    └──────────┘     └──────────┘    └──────────┘
          │                │                │
          │                │                │
          │    ┌───────────┘                │
          │    │                            │
          ▼    ▼                            ▼
    ┌──────────────┐              ┌─────────────┐
    │  FastAPI App │◄────────────►│   Network   │
    │  Port: 8000  │              │   Bridge    │
    └──────────────┘              └─────────────┘
          │
          │
          ▼
    ┌──────────────┐
    │  Database    │
    │  Port: 5432  │
    │  (internal)  │
    └──────────────┘
          │
          ▼
    ┌──────────────────────┐
    │   Access Points:     │
    │   App: :8000         │
    │   Docs: :8000/docs   │
    │   DB: :5432 (local)  │
    └──────────────────────┘
```

## Command Cheat Sheet

```
╔══════════════════════════════════════════════════════════╗
║              fastinit COMMAND REFERENCE                 ║
╠══════════════════════════════════════════════════════════╣
║ 📦 Installation                                          ║
║ pip install -e .                                         ║
║ .\install.ps1  (Windows)                                 ║
║ ./install.sh   (Unix/Mac)                                ║
╠══════════════════════════════════════════════════════════╣
║ 🆕 Create Project                                        ║
║ fastinit init <name>                                    ║
║ fastinit init <name> --db --jwt --logging --docker      ║
║ fastinit init <name> --interactive                      ║
╠══════════════════════════════════════════════════════════╣
║ 🎨 Generate Code                                         ║
║ fastinit new model <Name> --fields "..."                ║
║ fastinit new service <Name>Service --model <Name>       ║
║ fastinit new route <names> --service <Name>Service      ║
║ fastinit new crud <Name> --fields "..."                 ║
╠══════════════════════════════════════════════════════════╣
║ ℹ️  Information                                          ║
║ fastinit --help                                         ║
║ fastinit version                                        ║
║ fastinit init --help                                    ║
║ fastinit new --help                                     ║
╠══════════════════════════════════════════════════════════╣
║ 🚀 Run Generated Project                                 ║
║ cd <project-name>                                        ║
║ python -m venv venv                                      ║
║ venv\Scripts\activate  (Windows)                         ║
║ source venv/bin/activate  (Unix/Mac)                     ║
║ pip install -r requirements.txt                          ║
║ uvicorn app.main:app --reload                            ║
╠══════════════════════════════════════════════════════════╣
║ 🐳 Docker                                                ║
║ docker-compose up                                        ║
║ docker-compose down                                      ║
║ docker build -t my-api .                                 ║
║ docker run -p 8000:8000 my-api                           ║
╚══════════════════════════════════════════════════════════╝
```

## Quick Decision Tree

```
                    Start Here
                        │
                        ▼
            Do you need a database?
                   ╱        ╲
                YES          NO
                 │            │
                 ▼            ▼
      Which database?    Use --jwt?
      PostgreSQL              ╱   ╲
      MySQL                 YES    NO
      SQLite                 │     │
                 │           │     │
                 ▼           ▼     ▼
         Need Docker?    Add flags
              ╱  ╲           │
            YES   NO         │
             │     │         │
             ▼     ▼         ▼
      Add --docker      Run Command:
                        fastinit init
                        my-api [flags]
```

## File Size Reference

```
📊 Generated Project Sizes (Approximate)

Basic Project (no options)
├── Files: ~15
├── Size: ~50 KB
└── Dependencies: ~5

With Database (--db)
├── Files: ~18
├── Size: ~60 KB
└── Dependencies: ~8

With JWT (--jwt)
├── Files: ~19
├── Size: ~65 KB
└── Dependencies: ~10

Full Stack (--db --jwt --logging --docker)
├── Files: ~25
├── Size: ~80 KB
└── Dependencies: ~15
```

## Endpoint Reference

```
🔗 Default Endpoints (All Projects)

GET  /                → Root message
GET  /docs           → Swagger UI
GET  /redoc          → ReDoc UI
GET  /openapi.json   → OpenAPI schema
GET  /api/health     → Basic health
GET  /api/health/ready   → Readiness probe
GET  /api/health/live    → Liveness probe

🗄️ With Database (--db)

GET  /api/health/db  → Database health

🎨 Generated CRUD (fastinit new crud Product)

GET    /products      → List all
GET    /products/{id} → Get by ID
POST   /products      → Create
PUT    /products/{id} → Update
DELETE /products/{id} → Delete
```

---

**💡 Tip**: Keep this reference handy for quick lookups!
