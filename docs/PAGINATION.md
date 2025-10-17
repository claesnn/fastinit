# Pagination Options

FastInit now supports three different pagination strategies for generated routes and services:

## 1. Limit/Offset Pagination (Default)

This is the traditional pagination approach that uses `skip` and `limit` parameters.

**Usage:**
```bash
fastinit new route users
# or explicitly
fastinit new route users --pagination limit-offset
fastinit new service UserService --pagination limit-offset
fastinit new crud Product --pagination limit-offset
```

**Generated Route:**
```python
@router.get("/users", response_model=List[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all users."""
    return UserService.get_all(db, skip=skip, limit=limit)
```

**Generated Service:**
```python
@staticmethod
def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Get all User records."""
    return db.query(User).offset(skip).limit(limit).all()
```

**API Call Example:**
```bash
GET /users?skip=20&limit=10
```

**Pros:**
- Simple to implement
- Can jump to any page
- Familiar to most developers

**Cons:**
- Performance degrades with large offsets
- Inconsistent results if data changes between requests

## 2. Cursor Pagination

Cursor-based pagination uses the ID of the last item as a cursor to fetch the next set of results.

**Usage:**
```bash
fastinit new route users --pagination cursor
fastinit new service UserService --pagination cursor
fastinit new crud Product --pagination cursor
```

**Generated Route:**
```python
@router.get("/users", response_model=List[UserResponse])
def get_users(
    cursor: Optional[int] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all users."""
    return UserService.get_all(db, cursor=cursor, limit=limit)
```

**Generated Service:**
```python
@staticmethod
def get_all(db: Session, cursor: Optional[int] = None, limit: int = 100) -> List[User]:
    """Get all User records with cursor pagination."""
    query = db.query(User)
    if cursor:
        query = query.filter(User.id > cursor)
    return query.order_by(User.id).limit(limit).all()
```

**API Call Example:**
```bash
# First page
GET /users?limit=10

# Next page (assuming last ID was 10)
GET /users?cursor=10&limit=10
```

**Pros:**
- Consistent performance regardless of dataset size
- No duplicate or missing items when data changes
- Efficient for "infinite scroll" UIs

**Cons:**
- Cannot jump to arbitrary pages
- Requires ordered data (typically by ID)

## 3. No Pagination

Returns all records without any pagination. Use with caution on large datasets.

**Usage:**
```bash
fastinit new route users --pagination none
fastinit new service UserService --pagination none
fastinit new crud Product --pagination none
```

**Generated Route:**
```python
@router.get("/users", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(get_db)
):
    """Get all users."""
    return UserService.get_all(db)
```

**Generated Service:**
```python
@staticmethod
def get_all(db: Session) -> List[User]:
    """Get all User records."""
    return db.query(User).all()
```

**API Call Example:**
```bash
GET /users
```

**Pros:**
- Simplest implementation
- No pagination complexity

**Cons:**
- Can cause performance issues with large datasets
- May timeout or run out of memory
- Not suitable for production with growing data

## Choosing the Right Pagination Strategy

- **Use Limit/Offset** when:
  - You need page numbers (e.g., "Page 1 of 10")
  - Dataset is relatively small
  - Users need to jump to specific pages

- **Use Cursor** when:
  - Dataset is large
  - Implementing infinite scroll or "load more"
  - Data frequently changes
  - Performance is critical

- **Use None** when:
  - Dataset is guaranteed to be small
  - You need all data at once
  - Building internal tools or admin interfaces
  - Dataset size is controlled (e.g., lookup tables)

## Full Example

Generate a complete CRUD with cursor pagination:

```bash
fastinit new crud Product --fields "name:str,price:float,description:str" --pagination cursor
```

This will generate:
- `app/models/product.py` - SQLAlchemy model
- `app/schemas/product.py` - Pydantic schemas
- `app/services/product_service.py` - Service with cursor pagination
- `app/api/routes/products.py` - Route with cursor pagination
