#!/usr/bin/env python3
"""
Polygon Arbitrage Engine - Main Entry Point
"""

import sys
import os
from pathlib import Path

# Add src to path and set up config paths
project_root = Path(__file__).parent
src_path = project_root / "src"
config_path = project_root / "config"
sys.path.insert(0, str(src_path))

# Set config paths for the modules
os.environ["PROJECT_ROOT"] = str(project_root)
os.environ["CONFIG_PATH"] = str(config_path)

# Import and run the main CLI
if __name__ == "__main__":
    from bridge import main
    main()
