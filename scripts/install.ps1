# Installation and Setup Script for fastinit

Write-Host "fastinit - Installation Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}
Write-Host "Found: $pythonVersion" -ForegroundColor Green

# Check if pip is available
Write-Host "`nChecking pip..." -ForegroundColor Yellow
$pipVersion = pip --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: pip is not installed" -ForegroundColor Red
    exit 1
}
Write-Host "Found: $pipVersion" -ForegroundColor Green

# Install in development mode
Write-Host "`nInstalling fastinit in development mode..." -ForegroundColor Yellow
pip install -e .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Installation failed" -ForegroundColor Red
    exit 1
}

Write-Host "`nInstalling development dependencies..." -ForegroundColor Yellow
pip install pytest black flake8 mypy

# Verify installation
Write-Host "`nVerifying installation..." -ForegroundColor Yellow
$fastinitVersion = fastinit version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: fastinit installation verification failed" -ForegroundColor Red
    exit 1
}

Write-Host "`n================================" -ForegroundColor Green
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "You can now use fastinit:" -ForegroundColor Cyan
Write-Host "  fastinit init my-project" -ForegroundColor White
Write-Host "  fastinit init my-project --db --jwt --logging" -ForegroundColor White
Write-Host "  fastinit new crud Product" -ForegroundColor White
Write-Host ""
Write-Host "For more information, see:" -ForegroundColor Cyan
Write-Host "  README.md" -ForegroundColor White
Write-Host "  QUICKSTART.md" -ForegroundColor White
Write-Host ""
