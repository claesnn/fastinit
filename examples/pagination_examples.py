"""
Example: Generating Components with Different Pagination Strategies

This example demonstrates how to use FastInit to generate components
with different pagination strategies.
"""

# Example 1: Generate CRUD with default limit-offset pagination
# Command: fastinit new crud Product --fields "name:str,price:float,description:text"
#
# This creates:
# - app/models/product.py
# - app/schemas/product.py
# - app/services/product_service.py (with limit-offset pagination)
# - app/api/routes/products.py (with skip/limit parameters)
#
# API usage: GET /products?skip=0&limit=10

# Example 2: Generate CRUD with cursor-based pagination
# Command: fastinit new crud Post --fields "title:str,content:text,author:str" --pagination cursor
#
# This creates components with cursor-based pagination
# - Service method: get_all(db, cursor=None, limit=100)
# - Route parameters: cursor (optional int), limit (default 100)
#
# API usage:
#   First page:  GET /posts?limit=10
#   Next page:   GET /posts?cursor=123&limit=10
#
# Benefits:
# - Better performance on large datasets
# - Consistent results when data changes
# - Ideal for infinite scroll UIs

# Example 3: Generate CRUD with no pagination
# Command: fastinit new crud Category --fields "name:str,slug:str" --pagination none
#
# This creates components without pagination
# - Service method: get_all(db)
# - Route: no pagination parameters
#
# API usage: GET /categories
#
# Use cases:
# - Small, fixed datasets (e.g., lookup tables)
# - Admin interfaces
# - When you need all data at once

# Example 4: Mix and match - generate components separately with different pagination

# Step 1: Generate model and schema
# Command: fastinit new model User --fields "username:str,email:str,is_active:bool"
# Command: fastinit new schema User --fields "username:str,email:str,is_active:bool"

# Step 2: Generate service with cursor pagination
# Command: fastinit new service UserService --model User --pagination cursor

# Step 3: Generate route with cursor pagination
# Command: fastinit new route users --service UserService --pagination cursor

# Example 5: Generate just a service with specific pagination
# Command: fastinit new service CommentService --model Comment --pagination limit-offset
# Command: fastinit new service NotificationService --model Notification --pagination none

# Example 6: Generate just a route with specific pagination
# Command: fastinit new route orders --service OrderService --pagination cursor
# Command: fastinit new route tags --service TagService --pagination none


def example_usage_patterns():
    """
    Common usage patterns for pagination in FastInit
    """

    # Pattern 1: E-commerce products (cursor pagination for better performance)
    # fastinit new crud Product --fields "name:str,price:float,stock:int" --pagination cursor

    # Pattern 2: Blog posts (cursor pagination for chronological feeds)
    # fastinit new crud Post --fields "title:str,content:text,published_at:datetime" --pagination cursor

    # Pattern 3: User management (limit-offset for admin panels)
    # fastinit new crud User --fields "username:str,email:str,role:str" --pagination limit-offset

    # Pattern 4: Small lookup tables (no pagination)
    # fastinit new crud Country --fields "name:str,code:str" --pagination none
    # fastinit new crud Status --fields "name:str,value:str" --pagination none

    # Pattern 5: Comments with cursor (for infinite scroll)
    # fastinit new crud Comment --fields "post_id:int,text:text,user_id:int" --pagination cursor

    # Pattern 6: Settings or config (no pagination needed)
    # fastinit new crud Setting --fields "key:str,value:str" --pagination none


def when_to_use_each_pagination():
    """
    Decision guide for choosing pagination strategy
    """

    strategies = {
        "limit-offset": {
            "use_when": [
                "Need page numbers (e.g., 'Page 1 of 10')",
                "Small to medium datasets",
                "Users need to jump to specific pages",
                "Traditional admin interfaces",
            ],
            "avoid_when": [
                "Dataset is very large (millions of records)",
                "Data changes frequently",
                "Performance is critical",
            ],
            "example": "fastinit new crud User --pagination limit-offset",
        },
        "cursor": {
            "use_when": [
                "Large datasets",
                "Implementing infinite scroll",
                "Data changes frequently",
                "Performance is critical",
                "Mobile apps or real-time feeds",
            ],
            "avoid_when": [
                "Need to jump to arbitrary pages",
                "Need total page count",
                "Users expect traditional pagination",
            ],
            "example": "fastinit new crud Post --pagination cursor",
        },
        "none": {
            "use_when": [
                "Dataset is guaranteed to be small (<100 records)",
                "Lookup tables or reference data",
                "Internal tools",
                "Dropdown/select options",
            ],
            "avoid_when": [
                "Dataset can grow unbounded",
                "Public APIs",
                "Production systems with growing data",
            ],
            "example": "fastinit new crud Category --pagination none",
        },
    }

    return strategies


if __name__ == "__main__":
    print("FastInit Pagination Examples")
    print("=" * 50)
    print("\nSee the function definitions above for detailed examples")
    print("of how to use different pagination strategies with FastInit.")
    print("\nQuick reference:")
    print("  --pagination limit-offset  (default)")
    print("  --pagination cursor")
    print("  --pagination none")
