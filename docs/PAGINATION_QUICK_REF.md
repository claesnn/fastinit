# FastInit Pagination Quick Reference

## Command Syntax

```bash
fastinit new [route|service|crud] NAME [OPTIONS] --pagination [STRATEGY]
```

## Strategies

| Strategy      | Flag                  | Default | Use Case                    |
|---------------|----------------------|---------|----------------------------|
| Limit/Offset  | `--pagination limit-offset` | ✓ Yes   | Admin panels, page numbers |
| Cursor        | `--pagination cursor`       | No      | Large datasets, feeds      |
| None          | `--pagination none`         | No      | Small static data          |

## Quick Commands

```bash
# Generate with default (limit-offset)
fastinit new crud User

# Generate with cursor pagination
fastinit new crud Post --pagination cursor

# Generate without pagination
fastinit new crud Category --pagination none

# Individual components
fastinit new route users --pagination cursor
fastinit new service UserService --pagination cursor
```

## Generated Code Comparison

### Route Signatures

```python
# Limit-Offset (default)
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

# Cursor
def get_posts(cursor: Optional[int] = None, limit: int = 100, db: Session = Depends(get_db)):

# None
def get_categories(db: Session = Depends(get_db)):
```

### Service Methods

```python
# Limit-Offset (default)
def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

# Cursor
def get_all(db: Session, cursor: Optional[int] = None, limit: int = 100) -> List[Post]:
    query = db.query(Post)
    if cursor:
        query = query.filter(Post.id > cursor)
    return query.order_by(Post.id).limit(limit).all()

# None
def get_all(db: Session) -> List[Category]:
    return db.query(Category).all()
```

## API Usage

```bash
# Limit-Offset
curl "http://localhost:8000/users?skip=20&limit=10"

# Cursor (first page)
curl "http://localhost:8000/posts?limit=10"
# Cursor (next page, assuming last ID was 10)
curl "http://localhost:8000/posts?cursor=10&limit=10"

# None
curl "http://localhost:8000/categories"
```

## Decision Matrix

| Question                          | Answer      | Strategy      |
|-----------------------------------|-------------|---------------|
| Dataset < 100 records?            | Yes         | → **none**    |
| Need page numbers?                | Yes         | → **limit-offset** |
| Dataset > 10,000 records?         | Yes         | → **cursor**  |
| Need infinite scroll?             | Yes         | → **cursor**  |
| Data changes frequently?          | Yes         | → **cursor**  |
| Traditional admin interface?      | Yes         | → **limit-offset** |
| Mobile app / real-time feed?      | Yes         | → **cursor**  |

## Pro Tips

✓ **Default is sensible**: Limit-offset works well for most use cases
✓ **Cursor scales better**: Choose cursor for large or growing datasets  
✓ **None for lookups**: Perfect for dropdown options and reference data
✓ **Consistent within project**: Use the same strategy for similar endpoints
✓ **Can mix strategies**: Different endpoints can use different pagination

## Common Patterns

```bash
# E-commerce
fastinit new crud Product --pagination cursor

# Blog
fastinit new crud Post --pagination cursor
fastinit new crud Comment --pagination cursor

# Admin
fastinit new crud User --pagination limit-offset
fastinit new crud Order --pagination limit-offset

# Lookups
fastinit new crud Country --pagination none
fastinit new crud Status --pagination none
```

## More Info

- Full guide: `docs/PAGINATION.md`
- Visual guide: `docs/PAGINATION_VISUAL.md`
- Examples: `examples/pagination_examples.py`
- Tests: `tests/test_pagination.py`
