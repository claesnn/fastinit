# FastInit Documentation

Comprehensive documentation for the FastInit CLI tool.

## 📖 Documentation

### Getting Started
- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Detailed getting started guide

### Usage & Reference
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Complete usage reference
- **[VISUAL_GUIDE.md](VISUAL_GUIDE.md)** - Visual quick reference with diagrams
- **[FEATURES.md](FEATURES.md)** - Complete feature list

### Development
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute to FastInit
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes

## Quick Links

- [Main README](../README.md) - Project overview
- [Examples](../examples/) - Code examples
- [Scripts](../scripts/) - Development scripts

## Installation

```bash
pip install fastinit
```

## Basic Usage

```bash
# Create a new FastAPI project
fastinit init my-api

# Create with database and auth
fastinit init my-api --db --jwt

# Generate CRUD components
fastinit new crud Product --fields "name:str,price:float"
```
