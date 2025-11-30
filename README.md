# Polygon Arbitrage Engine

Polygon-based arbitrage engine that scans 300+ token pairs across multiple DEXes to find and execute profitable arbitrage opportunities using flashloans.

## Features

### Core Functionality
- **Multi-DEX Arbitrage**: Scans QuickSwap, SushiSwap, Uniswap V3, and Curve
- **Flashloan Integration**: Supports both Aave V3 and Balancer V2 flashloans
- **Accurate Pricing**: Direct DEX contract queries (no approximations)
- **Smart Execution**: Automatic trade execution with profit verification
- **Trade Persistence**: SQLite database for trade history and analytics
- **CLI Interface**: Natural language interface for bot control
- **Web Dashboard**: Real-time Streamlit interface for monitoring and execution

### Safety & Reliability
- **RPC Redundancy**: 15+ Polygon RPC endpoints with automatic failover
- **Gas Optimization**: EIP-1559 with dynamic fee calculation
- **Private Transactions**: Alchemy private RPC for MEV protection
- **Error Handling**: Comprehensive logging and error tracking
- **Caching**: Persistent cache for pool data (24h expiration)
- **Slippage Modeling**: Accurate price impact calculations using constant product formula
- **Unit Testing**: 16 comprehensive tests covering all math calculations

## Recent Improvements

### Critical Fixes Applied ✅

All critical trading logic and pricing issues have been resolved:

- **Fixed Data Structure Access**: Now uses actual DEX quotes instead of non-existent reserve data
- **Rewritten Arbitrage Calculations**: Complete overhaul with proper slippage modeling
- **Dynamic Gas Estimation**: Real-time gas prices and POL/USD conversion
- **FlashbotsTxBuilder Fix**: Added compatibility alias for Polygon (no Flashbots on Polygon)
- **Comprehensive Unit Tests**: 16/16 tests passing, covering edge cases and math validation

See `FIXES_SUMMARY.md` for detailed technical information about all fixes applied.


## Installation

### Prerequisites
- Python 3.8+
- Polygon RPC access (Alchemy, Infura, or public)
- OpenAI API key (optional, for AI features)
- Wallet with MATIC for gas

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-aggregator.git
cd ai-aggregator
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
nano .env  # Edit with your keys
```

Required `.env` variables:
```bash
# API Keys
ALCHEMY_API_KEY=your_alchemy_key
OPENAI_API_KEY=your_openai_key  # Optional

# Wallet (for execution)
WALLET_PRIVATE_KEY=your_private_key

# Bot Settings
ARBIGIRL_MIN_PROFIT_USD=1.0
ARBIGIRL_AUTO_EXECUTE=false  # Set to true for auto-execution
```

4. **Deploy flashloan contract** (optional, for execution)
   - See `remix bot/flashloan_contract.py` for deployment instructions
   - Or use Remix IDE with `remix bot/flashloanbot.sol`
   - Update `.env` with `FLASHLOAN_CONTRACT_ADDRESS=0x...`

## Usage

### Quick Start

1. **Configure environment**
```bash
cp .env.example .env
nano .env  # Edit with your keys
```

2. **Start the CLI**
```bash
python bridge.py
```

## Web Dashboard (Optional)

For a visual web interface, use the Streamlit dashboard:

### **Install Frontend Dependencies**
```bash
cd frontend
pip install -r requirements.txt
```

### **Launch Web Dashboard**
```bash
# Start backend API first (in separate terminal)
python api_server.py

# Then launch frontend
./scripts/start-frontend.sh
# Or manually:
cd frontend && streamlit run streamlit_app.py
```

### **Access Web Interface**
- **Frontend:** http://localhost:8501
- **Backend API:** http://localhost:5050

The web dashboard provides:
- 📊 Real-time opportunity monitoring
- 📈 Visual profit charts and analytics  
- ⚡ One-click trade execution
- 📋 Historical performance tracking
- 🧪 Test data mode for instant demonstration

### **Web Interface Features**

#### **📊 Real-time Dashboard**
- Live bot statistics (profit, trades, uptime)
- Auto-refreshing opportunity monitoring
- Interactive profit charts using Plotly
- Status indicators and alerts

#### **🎯 Opportunity Scanner**
- Manual and automated scanning
- Adjustable profit thresholds
- Token filtering and sorting
- One-click trade execution from opportunities

#### **⚡ Trade Execution Interface**
- Manual trade proposal creation
- Auto-execute option for confirmed trades
- Real-time execution feedback
- Trade history tracking

#### **🎨 User Experience**
- **Test Mode:** Toggle for instant mock data vs real scans
- **Responsive Design:** Works on desktop, tablet, and mobile
- **Real-time Updates:** Auto-refreshing data and live charts
- **Professional Interface:** Modern, intuitive design

### **API Endpoints**
The web interface connects to the backend via REST API:
- `GET /status` - Bot statistics and uptime
- `POST /scan` - Scan for arbitrage opportunities
- `POST /scan/test` - Test scan with mock data (instant)
- `POST /simulate` - Simulate trade strategies
- `POST /propose` - Execute trade proposals
- `GET /cache/status` - Cache status information

### **Performance**
- **Test Scans:** Instant response with mock data
- **Real Scans:** ~2-3 minutes (full arbitrage calculation)
- **Auto-refresh:** Configurable intervals (1-30 seconds)
- **Timeout Handling:** Graceful error management

3. **Run a scan**
```
You> scan
```

4. **Enable continuous scanning**
```
You> scan continuous
```

5. **Check status**
```
You> status
```

### Graph Automation Mode

For automated background arbitrage with graph-based pathfinding:

```bash
# Start automation
./start-automation.sh

# Check status
./status-automation.sh

# View logs
tail -f logs/automation-*.log

# Stop automation
./stop-automation.sh
```

See `AUTOMATION_README.md` for detailed automation setup.

## Configuration

### Supported DEXes
- **QuickSwap** (V2)
- **SushiSwap** (V2)
- **Uniswap V3**
- **Curve** (partial support)

### Supported Tokens
- WMATIC
- WETH
- USDC
- USDT
- WBTC
- And more in `registries.py`

### RPC Endpoints
The bot uses 15+ public and private RPC endpoints with automatic failover:
- Alchemy (preferred)
- Infura
- Ankr
- Nodies
- Public endpoints

See `rpc_mgr.py` for full list.

## Database & Analytics

### Trade Database

All trades are logged to SQLite database (`trades.db`):

```python
from trade_database import get_database

db = get_database()

# Get analytics
stats = db.get_analytics(days=30)
print(f"Total profit: ${stats['total_profit_usd']}")
print(f"Win rate: {stats['win_rate_percent']}%")

# Get recent trades
recent = db.get_recent_trades(limit=10)

# Export to CSV
db.export_to_csv("trades_export.csv", days=30)
```

### Database Schema

- **trades**: Trade execution history
- **opportunities**: All detected opportunities
- **errors**: Error log with context
- **performance_metrics**: Scan times, success rates, etc.

## Development

### Project Structure

```
ai-aggregator/
├── ai_bridge.py               # Unified CLI client
├── run_graph_automation.py   # Graph-based automation runner
├── automation-manager.sh     # Service management script
├── arb_scanner.py             # Arbitrage detection logic
├── pool_scanner.py            # Pool discovery and scanning
├── price_math.py              # Price calculations (V2/V3)
├── tx_builder.py              # Transaction builder + Gas optimization
├── flashloan_contract.py      # Contract ABI and helpers
├── advanced_mev_module.py     # Advanced MEV and graph arbitrage
├── trade_database.py          # SQLite persistence layer
├── rpc_mgr.py                 # RPC manager with failover
├── polygon_arb_bot.py         # Main bot orchestrator
├── registries.py              # Token and DEX registries
├── abis.py                    # Contract ABIs
├── cache.py                   # Persistent caching system
├── auto_executor.py           # Flash loan execution
├── price_data_fetcher.py      # Pool data fetching
├── test_math_calculations.py  # Unit tests
├── requirements.txt           # Python dependencies
└── remix bot/                 # Remix IDE files
    └── flashloanbot.sol       # Solidity flashloan contract
```

### Adding a New DEX

1. Add DEX factory address to `registries.py`
2. Add pool discovery logic in `helpers/discover_pools.py`
3. Add price calculation in `price_math.py`
4. Add router address to pool registry

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
python test_math_calculations.py

# Individual test files
python test_fixes.py
```

## Security Considerations

### Before Running in Production

1. **Test on Testnet First**
   - Deploy to Mumbai testnet
   - Test with small amounts
   - Verify all functions work

2. **Secure Your Keys**
   - Never commit `.env` file
   - Use hardware wallet for large amounts
   - Rotate keys regularly

3. **Set Profit Thresholds**
   - Start with conservative thresholds
   - Account for gas costs
   - Monitor slippage

4. **Monitor Execution**
   - Set up alerts (Telegram/Email)
   - Review trade logs daily
   - Track profitability

### Risk Mitigation

- **Maximum Loss Limits**: Set in configuration
- **Circuit Breakers**: Auto-pause after N failures
- **Slippage Protection**: Configured in trade execution
- **Gas Price Ceiling**: Max acceptable gas price

## Troubleshooting

### Common Issues

**"RPC endpoint timeout"**
- Check your RPC API keys
- Try different endpoints in `rpc_mgr.py`
- Increase timeout values

**"No opportunities found"**
- Lower `MIN_PROFIT_USD` threshold
- Check if pools are loaded (`status` command)
- Verify RPC connectivity

**"Execution failed"**
- Ensure wallet has MATIC for gas
- Check contract is deployed
- Verify contract address in `.env`

**"CLI not responding"**
- Check if `ai_bridge.py` is running
- Verify RPC endpoints are working
- Check `.env` configuration

### Logs

- CLI logs: `arbigirl.log`
- Automation logs: `logs/automation-*.log`
- Database: `trades.db` (use SQLite browser)

## Roadmap

### Completed ✅
- Multi-DEX pool scanning
- Accurate price calculations with slippage modeling
- Arbitrage detection with graph-based pathfinding
- Trade database with analytics
- AI-powered CLI interface
- Graph automation system
- Comprehensive unit tests (16/16 passing)
- Dynamic gas cost estimation
- Flash loan execution automation

### In Progress 🚧
- Advanced MEV protection strategies
- Performance optimization for high-frequency scanning
- Enhanced error handling and recovery

### Planned 📋
- Multi-chain support (Ethereum, Arbitrum, Optimism)
- Machine learning optimization
- Web dashboard
- Backtesting framework
- Mobile app for monitoring

## Performance

### Benchmarks (Polygon Mainnet)

- **Pool Scan**: 30-60 seconds for 300+ pairs
- **Opportunity Detection**: < 5 seconds
- **RPC Calls**: 15-30 per scan (batched)
- **Cache Hit Rate**: ~85% after first scan

### Optimization Tips

- Use Alchemy or Infura for faster RPC
- Enable caching (default 24h)
- Run on server with good connectivity
- Use direct mode for fastest scanning

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## License

See [LICENSE](LICENSE) file for details.

## Disclaimer

**This software is for educational purposes only.**

- Use at your own risk
- No guarantee of profits
- Test thoroughly before production use
- Comply with all applicable laws
- MEV can be competitive and unprofitable

No liability is assumed for any losses incurred.

## Support

- GitHub Issues: [Report bugs](https://github.com/yllvar/polygon-arb-engine/issues)
- Documentation: See `docs/QUICK_START.md` for setup guide
- Logs: Check logs directory for debugging
- Automation: See `docs/AUTOMATION_README.md` for graph automation

## Acknowledgments

- OpenZeppelin for secure contract patterns
- Aave and Balancer for flashloan protocols
- Web3.py for Ethereum interaction
- FastAPI for REST API framework

---

**Happy arbitraging! 🚀💰**
