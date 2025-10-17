# Pagination Strategies Visual Comparison

## 1. Limit/Offset Pagination (Default)

```
┌─────────────────────────────────────────────────────────────┐
│                    Database (1000 records)                  │
│  ID: 1    2    3    4  ...  97   98   99   100  ... 1000   │
└─────────────────────────────────────────────────────────────┘
           │                        │
           │ skip=0, limit=10       │ skip=90, limit=10
           ▼                        ▼
    ┌──────────────┐         ┌──────────────┐
    │ Records 1-10 │         │ Records 91-100│
    └──────────────┘         └──────────────┘
         Page 1                   Page 10

Request Examples:
  GET /users?skip=0&limit=10    # First page
  GET /users?skip=10&limit=10   # Second page
  GET /users?skip=90&limit=10   # Tenth page

Generated Route:
  def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
      return UserService.get_all(db, skip=skip, limit=limit)

Generated Service:
  def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
      return db.query(User).offset(skip).limit(limit).all()

Pros:
  ✓ Can jump to any page directly
  ✓ Simple to understand
  ✓ Familiar to most developers
  ✓ Good for small-medium datasets

Cons:
  ✗ Performance degrades with large offsets
  ✗ Inconsistent if data changes between requests
  ✗ Database scans all skipped records
```

## 2. Cursor-Based Pagination

```
┌─────────────────────────────────────────────────────────────┐
│                    Database (1000 records)                  │
│  ID: 1    2    3  ...  10   11   12  ...  20   21  ... 1000│
└─────────────────────────────────────────────────────────────┘
           │                        │
           │ cursor=None, limit=10  │ cursor=10, limit=10
           ▼                        ▼
    ┌──────────────┐         ┌──────────────┐
    │ Records 1-10 │         │ Records 11-20 │
    │  last_id=10  │─────────▶ cursor=10     │
    └──────────────┘         └──────────────┘
      First Batch              Next Batch

Request Examples:
  GET /posts?limit=10              # First page, returns IDs 1-10
  GET /posts?cursor=10&limit=10    # Next page, returns IDs 11-20
  GET /posts?cursor=20&limit=10    # Next page, returns IDs 21-30

Generated Route:
  def get_posts(cursor: Optional[int] = None, limit: int = 100, 
                db: Session = Depends(get_db)):
      return PostService.get_all(db, cursor=cursor, limit=limit)

Generated Service:
  def get_all(db: Session, cursor: Optional[int] = None, 
              limit: int = 100) -> List[Post]:
      query = db.query(Post)
      if cursor:
          query = query.filter(Post.id > cursor)
      return query.order_by(Post.id).limit(limit).all()

Pros:
  ✓ Consistent performance regardless of position
  ✓ No duplicate or missing items if data changes
  ✓ Efficient for infinite scroll
  ✓ Scales well with large datasets

Cons:
  ✗ Cannot jump to arbitrary pages
  ✗ No total page count
  ✗ Requires ordered data
```

## 3. No Pagination

```
┌─────────────────────────────────────────────────────────────┐
│              Database (Small Dataset - 50 records)          │
│  ID: 1    2    3    4    5  ...  48   49   50              │
└─────────────────────────────────────────────────────────────┘
                            │
                  No filtering/pagination
                            ▼
                   ┌──────────────┐
                   │ All 50 records│
                   └──────────────┘

Request Example:
  GET /categories              # Returns all records

Generated Route:
  def get_categories(db: Session = Depends(get_db)):
      return CategoryService.get_all(db)

Generated Service:
  def get_all(db: Session) -> List[Category]:
      return db.query(Category).all()

Pros:
  ✓ Simplest implementation
  ✓ No pagination complexity
  ✓ Perfect for small, static datasets

Cons:
  ✗ Can cause performance issues
  ✗ May timeout with large datasets
  ✗ Not suitable for growing data
```

## Use Case Decision Tree

```
                    Start: Need to list records?
                                │
                                ▼
                    How many records typically?
                                │
                    ┌───────────┴───────────┐
                    │                       │
                < 100 records           > 100 records
              (relatively fixed)       (can grow)
                    │                       │
                    ▼                       ▼
              ┌──────────┐         Will users need to...
              │   NONE   │                 │
              └──────────┘     ┌───────────┴────────────┐
                               │                        │
              Examples:    Jump to pages          Scroll infinitely
              - Categories  (page numbers)        (load more)
              - Statuses        │                        │
              - Countries       ▼                        ▼
              - Tags      ┌──────────────┐      ┌──────────────┐
                          │ LIMIT-OFFSET │      │    CURSOR    │
                          └──────────────┘      └──────────────┘
                          
                          Examples:              Examples:
                          - Admin panels         - Social feeds
                          - Search results       - Comments
                          - User management      - Notifications
                          - Reports              - Messages
                                                 - Activity logs
```

## Performance Comparison (1 Million Records)

```
Fetching records 900,000 - 900,010:

┌──────────────────┬─────────────┬──────────────┬─────────────┐
│  Strategy        │ Query Time  │ DB Scans     │ Consistency │
├──────────────────┼─────────────┼──────────────┼─────────────┤
│ Limit/Offset     │ ~2000ms     │ 900,010 rows │ ✗ Unstable  │
│ Cursor           │ ~50ms       │ 11 rows      │ ✓ Stable    │
│ None             │ ~30000ms    │ All rows     │ ✓ Stable    │
└──────────────────┴─────────────┴──────────────┴─────────────┘

Note: Actual performance varies by database, indexes, and hardware
```

## API Response Patterns

### Limit/Offset Response
```json
{
  "data": [...],
  "pagination": {
    "skip": 20,
    "limit": 10,
    "total": 1000,
    "page": 3,
    "total_pages": 100
  }
}
```

### Cursor Response
```json
{
  "data": [...],
  "pagination": {
    "next_cursor": 30,
    "has_more": true,
    "limit": 10
  }
}
```

### No Pagination Response
```json
{
  "data": [...],
  "total": 50
}
```

## Migration Path

If you start with one pagination type and need to change later:

```
NONE → LIMIT-OFFSET → CURSOR
  ↓         ↓            ↓
Easy     Moderate      Hard

Going forward: Easy (just add parameters)
Going backward: Hard (breaking change for clients)
```

**Recommendation**: Start with the most restrictive option you'll need:
- If unsure, use `cursor` - it scales better
- Use `limit-offset` only if page numbers are required
- Use `none` only for guaranteed small datasets
