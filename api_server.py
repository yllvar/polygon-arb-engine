#!/usr/bin/env python3
"""
API Server Starter for Polygon Arbitrage Engine
Starts the FastAPI server for the Streamlit frontend
"""

import sys
import os
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Set config paths
os.environ["PROJECT_ROOT"] = str(project_root)
os.environ["CONFIG_PATH"] = str(project_root / "config")

# Import and start the API server
from bridge import start_api_server

if __name__ == "__main__":
    print("🚀 Starting Polygon Arbitrage Engine API Server...")
    print("   API: http://localhost:5050")
    print("   Docs: http://localhost:5050/docs")
    print("   Press Ctrl+C to stop")
    print()
    
    try:
        start_api_server()
    except KeyboardInterrupt:
        print("\n👋 API Server stopped")
