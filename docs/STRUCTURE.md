# 📁 Project Structure

This document describes the organized file structure of the Polygon Arbitrage Engine project.

## 📂 Directory Structure

```
polygon-arb-engine/
├── 📄 README.md              # Main project documentation
├── 📄 LICENSE                # MIT License
├── 📄 requirements.txt       # Python dependencies
├── 📄 .env                   # Environment configuration (create from .env.example)
├── 📄 .gitignore            # Git ignore rules
├── 🐍 main.py               # Main entry point (CLI interface)
│
├── 📁 src/                  # Core Python modules
│   ├── 🐍 __init__.py       # Package initialization
│   ├── 🐍 bridge.py         # Main CLI and API server
│   ├── 🐍 polygon_arb_bot.py # Core arbitrage bot
│   ├── 🐍 run_graph_automation.py # Automation runner
│   ├── 🐍 advanced_mev_module.py # MEV and graph arbitrage
│   ├── 🐍 price_data_fetcher.py # Pool data fetching
│   ├── 🐍 arb_finder.py     # Arbitrage opportunity detection
│   ├── 🐍 price_math.py     # Price calculations
│   ├── 🐍 cache.py          # Caching system
│   ├── 🐍 rpc_mgr.py        # RPC endpoint management
│   ├── 🐍 trade_database.py # SQLite database
│   ├── 🐍 tx_builder.py     # Transaction building
│   ├── 🐍 auto_executor.py  # Trade execution
│   ├── 🐍 registries.py     # DEX and token registries
│   ├── 🐍 abis.py           # Smart contract ABIs
│   ├── 🐍 test_math_calculations.py # Math tests
│   └── 🐍 test_fixes.py     # Fix validation tests
│
├── 📁 config/               # Configuration files
│   ├── 📄 .env.example      # Environment template
│   ├── 📄 rpc_endpoints.json # RPC endpoint configuration
│   ├── 📄 pool_registry.json # Pool addresses and metadata
│   └── 📄 failed_pairs.json # Failed pool discovery records
│
├── 📁 frontend/            # Streamlit web interface
│   ├── 📄 streamlit_app.py # Main Streamlit application
│   ├── 📄 requirements.txt # Frontend dependencies
│   ├── 📄 README.md       # Frontend documentation
│   └── 📁 assets/         # CSS, images, etc.

├── 📁 scripts/              # Shell scripts and batch files
│   ├── 🐚 start-automation.sh    # Start automation (Linux/Mac)
│   ├── 🐚 stop-automation.sh     # Stop automation
│   ├── 🐚 status-automation.sh   # Check automation status
│   ├── 🐚 automation-manager.sh # Advanced management
│   ├── 🦶 start-automation.bat   # Start automation (Windows)
│   ├── 🦶 stop-automation.bat    # Stop automation (Windows)
│   ├── 🦶 status-automation.bat  # Check status (Windows)
│   ├── 🦶 start-automation-background.bat # Background start (Windows)
│   └── 📄 arbigirl-automation.service # systemd service file
│
├── 📁 deployment/           # Smart contract deployment
│   └── 📁 remix bot/        # Remix IDE files
│       ├── 📄 flashloan_contract.py # Contract helper
│       └── 📄 flashloanbot.sol     # Solidity contract
│
├── 📁 docs/                 # Documentation
│   ├── 📄 README.md          # This file
│   ├── 📄 QUICK_START.md    # Quick start guide
│   ├── 📄 AUTOMATION_README.md # Automation documentation
│   ├── 📄 FIXES_SUMMARY.md  # Bug fixes summary
│   ├── 📄 README_ARBSYSTEM.md # Simple arbitrage system
│   ├── 📄 WINDOWS_QUICK_START.md # Windows setup guide
│   └── 📄 READ ME.txt       # Cache rules and guidelines
│
├── 📁 data/                 # Data and cache files
│   └── 📁 cache/            # Cached data
│       ├── 📄 arb_cache.json
│       ├── 📄 dex_health_cache.json
│       ├── 📄 general_cache.json
│       ├── 📄 liquidity_cache.json
│       ├── 📄 oracle_cache.json
│       ├── 📄 pair_prices_cache.json
│       ├── 📄 pool_registry_cache.json
│       └── 📄 router_gas_cache.json
│
├── 📁 helpers/              # Helper utilities
│   ├── 🐍 discover_pools.py  # Pool discovery utility
│   ├── 🐍 pool_verifier.py  # Pool verification tool
│   └── 📄 hop_map.json      # Token hop mapping
│
├── 📁 plugins/              # External plugins
│   └── 📄 index.js          # Node.js plugin interface
│
├── 📁 tests/                # Test files (empty - ready for expansion)
├── 📁 logs/                 # Log files (created during runtime)
├── 📁 .git/                 # Git repository
└── 📁 __pycache__/          # Python cache (generated)
```

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Copy environment template
cp config/.env.example .env

# Edit .env with your configuration
nano .env
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Bot

#### Option A: CLI Interface
```bash
python main.py
```

#### Option B: Background Automation
```bash
./scripts/start-automation.sh
```

#### Option C: Check Status
```bash
./scripts/status-automation.sh
```

## 📝 Key Changes

### Before (Messy):
- 30+ files in root directory
- Mixed file types
- No clear separation of concerns

### After (Organized):
- ✅ Clean root directory with only essential files
- ✅ Logical grouping by functionality
- ✅ Clear separation of code, config, docs, and scripts
- ✅ Easy navigation and maintenance

## 🔧 Configuration Files

- **`.env`** - Your private configuration (API keys, settings)
- **`config/rpc_endpoints.json`** - RPC endpoint configuration
- **`config/pool_registry.json`** - DEX pool addresses
- **`config/.env.example`** - Configuration template

## 📚 Documentation

All documentation is now organized in the `docs/` folder:
- `QUICK_START.md` - Getting started guide
- `AUTOMATION_README.md` - Automation features
- `FIXES_SUMMARY.md` - Recent bug fixes
- And more...

## 🧪 Testing

Test files are located in `src/`:
- `test_math_calculations.py` - Mathematical calculations
- `test_fixes.py` - Bug fix validation

Run tests with:
```bash
python src/test_math_calculations.py
python src/test_fixes.py
```

## 🎯 Next Steps

This organization makes the project:
- 🧹 **Cleaner** - Easy to navigate
- 🔧 **Maintainable** - Clear file locations
- 📦 **Deployable** - Structured for production
- 👥 **Team-friendly** - Easy collaboration
