#!/bin/bash

# DocuVerify-Sec Automated Setup Script
# Installs all dependencies and initializes the application

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  DocuVerify-Sec: Automated Setup & Initialization             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${YELLOW}[1/6]${NC} Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $PYTHON_VERSION"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 8 ]); then
    echo -e "${RED}✗ Python 3.8 or higher required. You have $PYTHON_VERSION${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python $PYTHON_VERSION OK${NC}"
echo ""

# Create virtual environment
echo -e "${YELLOW}[2/6]${NC} Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi
echo ""

# Activate virtual environment
echo -e "${YELLOW}[3/6]${NC} Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Upgrade pip
echo -e "${YELLOW}[4/6]${NC} Upgrading pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo -e "${GREEN}✓ pip upgraded${NC}"
echo ""

# Install dependencies
echo -e "${YELLOW}[5/6]${NC} Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo -e "${GREEN}✓ All dependencies installed${NC}"
else
    echo -e "${RED}✗ requirements.txt not found!${NC}"
    exit 1
fi
echo ""

# Create uploads directory
echo -e "${YELLOW}[6/6]${NC} Setting up directories..."
mkdir -p uploads
chmod 755 uploads
echo -e "${GREEN}✓ Uploads directory created${NC}"
echo ""

# Check for Tesseract (optional)
echo -e "${YELLOW}[Optional]${NC} Checking for Tesseract OCR..."
if command -v tesseract &> /dev/null; then
    TESS_VERSION=$(tesseract --version 2>&1 | head -n1)
    echo -e "${GREEN}✓ Tesseract found: $TESS_VERSION${NC}"
else
    echo -e "${YELLOW}⚠ Tesseract not found - EasyOCR will be used as fallback${NC}"
    echo "  To install: "
    echo "    Ubuntu/Debian: sudo apt-get install tesseract-ocr"
    echo "    macOS: brew install tesseract"
fi
echo ""

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << EOF
venv/
__pycache__/
*.pyc
.DS_Store
.env
uploads/*
!uploads/.gitkeep
*.log
.pytest_cache/
dist/
build/
*.egg-info/
EOF
    echo -e "${GREEN}✓ .gitignore created${NC}"
fi
echo ""

# Setup complete
echo "╔════════════════════════════════════════════════════════════════╗"
echo -e "${GREEN}✓ SETUP COMPLETE!${NC}"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo ""
echo "1. Start the server:"
echo "   ${GREEN}python app.py${NC}"
echo ""
echo "2. Open your browser:"
echo "   ${GREEN}http://localhost:5000${NC}"
echo ""
echo "3. Upload a document for analysis"
echo ""
echo "To stop the server, press Ctrl+C"
echo ""
echo "For more information, see README.md and QUICKSTART.md"
echo ""
