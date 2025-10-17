# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
