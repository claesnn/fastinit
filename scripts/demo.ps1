# Demo Script for fastinit
# This script demonstrates all the key features of fastinit

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "   fastinit CLI - Feature Demo" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check if fastinit is installed
Write-Host "[1/8] Checking fastinit installation..." -ForegroundColor Yellow
$version = fastinit version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: fastinit is not installed. Please run install.ps1 first." -ForegroundColor Red
    exit 1
}
Write-Host "✓ fastinit is installed" -ForegroundColor Green
Write-Host ""

# Demo 1: Basic Project
Write-Host "[2/8] Creating a basic FastAPI project..." -ForegroundColor Yellow
fastinit init demo-basic --force
Write-Host "✓ Basic project created: demo-basic/" -ForegroundColor Green
Write-Host ""

# Demo 2: Project with Database
Write-Host "[3/8] Creating a project with PostgreSQL database..." -ForegroundColor Yellow
fastinit init demo-db --db --db-type postgresql --force
Write-Host "✓ Database project created: demo-db/" -ForegroundColor Green
Write-Host ""

# Demo 3: Project with JWT Auth
Write-Host "[4/8] Creating a project with JWT authentication..." -ForegroundColor Yellow
fastinit init demo-jwt --jwt --logging --force
Write-Host "✓ JWT project created: demo-jwt/" -ForegroundColor Green
Write-Host ""

# Demo 4: Full-featured Project
Write-Host "[5/8] Creating a full-featured project..." -ForegroundColor Yellow
fastinit init demo-full --db --db-type postgresql --jwt --logging --docker --force
Write-Host "✓ Full-featured project created: demo-full/" -ForegroundColor Green
Write-Host ""

# Demo 5: Generate a Model
Write-Host "[6/8] Generating a User model in demo-full..." -ForegroundColor Yellow
fastinit new model User --project-dir demo-full --fields "username:str,email:str,age:int,is_active:bool"
Write-Host "✓ User model generated" -ForegroundColor Green
Write-Host ""

# Demo 6: Generate a Service
Write-Host "[7/8] Generating UserService in demo-full..." -ForegroundColor Yellow
fastinit new service UserService --project-dir demo-full --model User
Write-Host "✓ UserService generated" -ForegroundColor Green
Write-Host ""

# Demo 7: Generate CRUD
Write-Host "[8/8] Generating complete CRUD for Product in demo-full..." -ForegroundColor Yellow
fastinit new crud Product --project-dir demo-full --fields "name:str,price:float,description:text,in_stock:bool"
Write-Host "✓ Product CRUD generated (model + service + routes)" -ForegroundColor Green
Write-Host ""

# Summary
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "   Demo Complete!" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Created demo projects:" -ForegroundColor Green
Write-Host "  • demo-basic/     - Basic FastAPI project" -ForegroundColor White
Write-Host "  • demo-db/        - Project with PostgreSQL" -ForegroundColor White
Write-Host "  • demo-jwt/       - Project with JWT auth" -ForegroundColor White
Write-Host "  • demo-full/      - Full-featured project" -ForegroundColor White
Write-Host ""
Write-Host "Generated components in demo-full/:" -ForegroundColor Green
Write-Host "  • User model + UserService" -ForegroundColor White
Write-Host "  • Product CRUD (model + service + routes)" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. cd demo-full" -ForegroundColor White
Write-Host "  2. python -m venv venv" -ForegroundColor White
Write-Host "  3. venv\Scripts\activate" -ForegroundColor White
Write-Host "  4. pip install -r requirements.txt" -ForegroundColor White
Write-Host "  5. Copy .env.example to .env and configure" -ForegroundColor White
Write-Host "  6. uvicorn app.main:app --reload" -ForegroundColor White
Write-Host "  7. Visit http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Or run with Docker:" -ForegroundColor Cyan
Write-Host "  docker-compose up" -ForegroundColor White
Write-Host ""
