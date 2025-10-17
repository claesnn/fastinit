#!/bin/bash
# Installation and Setup Script for fastinit

echo -e "\033[1;36mfastinit - Installation Script\033[0m"
echo "================================"
echo ""

# Check Python version
echo -e "\033[1;33mChecking Python version...\033[0m"
if ! command -v python3 &> /dev/null; then
    echo -e "\033[1;31mError: Python 3 is not installed or not in PATH\033[0m"
    exit 1
fi
python_version=$(python3 --version)
echo -e "\033[1;32mFound: $python_version\033[0m"

# Check if pip is available
echo -e "\n\033[1;33mChecking pip...\033[0m"
if ! command -v pip3 &> /dev/null; then
    echo -e "\033[1;31mError: pip is not installed\033[0m"
    exit 1
fi
pip_version=$(pip3 --version)
echo -e "\033[1;32mFound: $pip_version\033[0m"

# Install in development mode
echo -e "\n\033[1;33mInstalling fastinit in development mode...\033[0m"
pip3 install -e .

if [ $? -ne 0 ]; then
    echo -e "\033[1;31mError: Installation failed\033[0m"
    exit 1
fi

echo -e "\n\033[1;33mInstalling development dependencies...\033[0m"
pip3 install pytest black flake8 mypy

# Verify installation
echo -e "\n\033[1;33mVerifying installation...\033[0m"
fastinit version

if [ $? -ne 0 ]; then
    echo -e "\033[1;31mError: fastinit installation verification failed\033[0m"
    exit 1
fi

echo ""
echo -e "\033[1;32m================================\033[0m"
echo -e "\033[1;32mInstallation Complete!\033[0m"
echo -e "\033[1;32m================================\033[0m"
echo ""
echo -e "\033[1;36mYou can now use fastinit:\033[0m"
echo "  fastinit init my-project"
echo "  fastinit init my-project --db --jwt --logging"
echo "  fastinit new crud Product"
echo ""
echo -e "\033[1;36mFor more information, see:\033[0m"
echo "  README.md"
echo "  QUICKSTART.md"
echo ""
