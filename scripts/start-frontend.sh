#!/bin/bash

# Polygon Arbitrage Engine - Frontend Launcher
# Starts Streamlit web interface

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

echo -e "${BLUE}🔧 Polygon Arbitrage Engine - Frontend Launcher${NC}"
echo "=================================================="

# Check if frontend directory exists
if [ ! -d "$FRONTEND_DIR" ]; then
    echo -e "${RED}❌ Frontend directory not found: $FRONTEND_DIR${NC}"
    echo "Please ensure the frontend directory exists."
    exit 1
fi

# Check if requirements.txt exists
if [ ! -f "$FRONTEND_DIR/requirements.txt" ]; then
    echo -e "${RED}❌ requirements.txt not found in frontend directory${NC}"
    exit 1
fi

# Check Python environment
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 not found. Please install Python 3.8+${NC}"
    exit 1
fi

# Check if Streamlit is installed
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Streamlit not found. Installing dependencies...${NC}"
    cd "$FRONTEND_DIR"
    pip3 install -r requirements.txt
    echo -e "${GREEN}✅ Dependencies installed${NC}"
fi

# Check if backend API is running
echo -e "${BLUE}🔍 Checking backend API...${NC}"
if curl -s http://localhost:5050/status > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend API is running (http://localhost:5050)${NC}"
else
    echo -e "${YELLOW}⚠️  Backend API not running. Please start it first:${NC}"
    echo "   cd $PROJECT_ROOT && python main.py"
    echo "   or: ./scripts/start-automation.sh"
    echo ""
    echo -e "${YELLOW}Continue anyway? (y/N): ${NC}"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

# Change to frontend directory
cd "$FRONTEND_DIR"

# Set Streamlit configuration
export STREAMLIT_SERVER_PORT=${STREAMLIT_SERVER_PORT:-8501}
export STREAMLIT_SERVER_ADDRESS=${STREAMLIT_SERVER_ADDRESS:-localhost}
export STREAMLIT_SERVER_HEADLESS=${STREAMLIT_SERVER_HEADLESS:-false}

# Launch Streamlit
echo -e "${GREEN}🚀 Starting Streamlit frontend...${NC}"
echo "   URL: http://localhost:$STREAMLIT_SERVER_PORT"
echo "   Press Ctrl+C to stop"
echo ""

# Start Streamlit with configuration
python3 -m streamlit run streamlit_app.py \
    --server.port "$STREAMLIT_SERVER_PORT" \
    --server.address "$STREAMLIT_SERVER_ADDRESS" \
    --server.headless "$STREAMLIT_SERVER_HEADLESS" \
    --browser.gatherUsageStats false \
    --theme.primaryColor "#FF6B6B" \
    --theme.backgroundColor "#FFFFFF" \
    --theme.secondaryBackgroundColor "#F0F2F6" \
    --theme.textColor "#262730"
