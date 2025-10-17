#!/bin/bash
# Demo Script for fastinit
# This script demonstrates all the key features of fastinit

echo ""
echo -e "\033[1;36m=====================================\033[0m"
echo -e "\033[1;36m   fastinit CLI - Feature Demo\033[0m"
echo -e "\033[1;36m=====================================\033[0m"
echo ""

# Check if fastinit is installed
echo -e "\033[1;33m[1/8] Checking fastinit installation...\033[0m"
if ! command -v fastinit &> /dev/null; then
    echo -e "\033[1;31mError: fastinit is not installed. Please run install.sh first.\033[0m"
    exit 1
fi
echo -e "\033[1;32m✓ fastinit is installed\033[0m"
echo ""

# Demo 1: Basic Project
echo -e "\033[1;33m[2/8] Creating a basic FastAPI project...\033[0m"
fastinit init demo-basic --force
echo -e "\033[1;32m✓ Basic project created: demo-basic/\033[0m"
echo ""

# Demo 2: Project with Database
echo -e "\033[1;33m[3/8] Creating a project with PostgreSQL database...\033[0m"
fastinit init demo-db --db --db-type postgresql --force
echo -e "\033[1;32m✓ Database project created: demo-db/\033[0m"
echo ""

# Demo 3: Project with JWT Auth
echo -e "\033[1;33m[4/8] Creating a project with JWT authentication...\033[0m"
fastinit init demo-jwt --jwt --logging --force
echo -e "\033[1;32m✓ JWT project created: demo-jwt/\033[0m"
echo ""

# Demo 4: Full-featured Project
echo -e "\033[1;33m[5/8] Creating a full-featured project...\033[0m"
fastinit init demo-full --db --db-type postgresql --jwt --logging --docker --force
echo -e "\033[1;32m✓ Full-featured project created: demo-full/\033[0m"
echo ""

# Demo 5: Generate a Model
echo -e "\033[1;33m[6/8] Generating a User model in demo-full...\033[0m"
fastinit new model User --project-dir demo-full --fields "username:str,email:str,age:int,is_active:bool"
echo -e "\033[1;32m✓ User model generated\033[0m"
echo ""

# Demo 6: Generate a Service
echo -e "\033[1;33m[7/8] Generating UserService in demo-full...\033[0m"
fastinit new service UserService --project-dir demo-full --model User
echo -e "\033[1;32m✓ UserService generated\033[0m"
echo ""

# Demo 7: Generate CRUD
echo -e "\033[1;33m[8/8] Generating complete CRUD for Product in demo-full...\033[0m"
fastinit new crud Product --project-dir demo-full --fields "name:str,price:float,description:text,in_stock:bool"
echo -e "\033[1;32m✓ Product CRUD generated (model + service + routes)\033[0m"
echo ""

# Summary
echo -e "\033[1;36m=====================================\033[0m"
echo -e "\033[1;36m   Demo Complete!\033[0m"
echo -e "\033[1;36m=====================================\033[0m"
echo ""
echo -e "\033[1;32mCreated demo projects:\033[0m"
echo "  • demo-basic/     - Basic FastAPI project"
echo "  • demo-db/        - Project with PostgreSQL"
echo "  • demo-jwt/       - Project with JWT auth"
echo "  • demo-full/      - Full-featured project"
echo ""
echo -e "\033[1;32mGenerated components in demo-full/:\033[0m"
echo "  • User model + UserService"
echo "  • Product CRUD (model + service + routes)"
echo ""
echo -e "\033[1;36mNext steps:\033[0m"
echo "  1. cd demo-full"
echo "  2. python -m venv venv"
echo "  3. source venv/bin/activate"
echo "  4. pip install -r requirements.txt"
echo "  5. Copy .env.example to .env and configure"
echo "  6. uvicorn app.main:app --reload"
echo "  7. Visit http://localhost:8000/docs"
echo ""
echo -e "\033[1;36mOr run with Docker:\033[0m"
echo "  docker-compose up"
echo ""
