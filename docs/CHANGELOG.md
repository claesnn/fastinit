# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Alembic Auto-Import Feature**: Alembic now automatically imports database settings from pydantic_settings
  - `alembic/env.py` automatically reads `DATABASE_URL` from `app.core.config.settings`
  - Single source of truth for database configuration - no need to edit `alembic.ini`
  - Generated for all projects with `--db` flag
  - Includes comprehensive documentation in `docs/ALEMBIC_INTEGRATION.md`
  - Added example usage in `examples/alembic_example.py`
  - Test coverage for Alembic generation and configuration
- **Flexible Pagination Strategies**: Support for three pagination types in code generation
  - `--pagination limit-offset` (default): Traditional skip/limit pagination
  - `--pagination cursor`: Cursor-based pagination for better performance on large datasets
  - `--pagination none`: No pagination (returns all records)
- Pagination support for `fastinit new route` command
- Pagination support for `fastinit new service` command
- Pagination support for `fastinit new crud` command
- Comprehensive pagination documentation in `docs/PAGINATION.md`
- Pagination examples in `examples/pagination_examples.py`
- Full test suite for pagination feature in `tests/test_pagination.py`

## [0.1.0] - 2025-10-17

### Added
- Initial release of fastinit
- `fastinit init` command to bootstrap FastAPI projects
- Support for database integration (PostgreSQL, MySQL, SQLite)
- JWT authentication with PyJWT and PyJWKClient
- Configurable logging
- Docker and docker-compose support
- Health check endpoints
- `fastinit new model` command to generate SQLAlchemy models
- `fastinit new service` command to generate service classes
- `fastinit new route` command to generate API routes
- `fastinit new crud` command to generate complete CRUD setup
- Environment-based configuration with Pydantic
- Interactive mode for project initialization
- Comprehensive project templates
- Auto-generated documentation
