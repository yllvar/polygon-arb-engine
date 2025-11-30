"""
Polygon Arbitrage Engine - Streamlit Frontend
Real-time web interface for arbitrage monitoring and execution
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import json

# Configuration
API_BASE_URL = "http://localhost:5050"
PAGE_REFRESH_INTERVAL = 5  # seconds

class ArbitrageAPI:
    """Client for Polygon Arbitrage Engine API"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
    
    def get_status(self) -> dict:
        """Get bot status and statistics"""
        try:
            response = self.session.get(f"{self.base_url}/status")
            return response.json()
        except Exception as e:
            st.error(f"Failed to connect to API: {e}")
            return {}
    
    def scan_opportunities(self, min_profit: float = 1.0, use_test_data: bool = True) -> dict:
        """Scan for arbitrage opportunities"""
        try:
            if use_test_data:
                # Use test endpoint for immediate response
                response = self.session.post(
                    f"{self.base_url}/scan/test",
                    timeout=5
                )
            else:
                # Use real scan endpoint (can take minutes)
                response = self.session.post(
                    f"{self.base_url}/scan",
                    json={"min_profit_usd": min_profit, "quick_mode": True},
                    timeout=120
                )
            return response.json()
        except Exception as e:
            st.error(f"Scan failed: {e}")
            return {}
    
    def simulate_trade(self, strategy: dict) -> dict:
        """Simulate a trade strategy"""
        try:
            response = self.session.post(
                f"{self.base_url}/simulate",
                json={"strategy": strategy},
                timeout=10
            )
            return response.json()
        except Exception as e:
            st.error(f"Simulation failed: {e}")
            return {}
    
    def execute_trade(self, proposal: dict, auto_execute: bool = False) -> dict:
        """Execute a trade proposal"""
        try:
            response = self.session.post(
                f"{self.base_url}/propose",
                json={
                    "proposal": proposal,
                    "auto_execute": auto_execute
                },
                timeout=30
            )
            return response.json()
        except Exception as e:
            st.error(f"Execution failed: {e}")
            return {}

# Initialize API client
api = ArbitrageAPI()

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format currency amounts"""
    if amount >= 1000000:
        return f"${amount/1000000:.2f}M"
    elif amount >= 1000:
        return f"${amount/1000:.2f}K"
    else:
        return f"${amount:.2f}"

def format_percentage(pct: float) -> str:
    """Format percentage with color coding"""
    return f"{pct:.2f}%"

def create_opportunity_chart(opportunities: list) -> go.Figure:
    """Create opportunity profit chart"""
    if not opportunities:
        return go.Figure()
    
    df = pd.DataFrame(opportunities)
    
    fig = px.bar(
        df, 
        x='pair', 
        y='profit_usd',
        color='dex_buy',
        title="Arbitrage Opportunities by Profit",
        labels={
            'profit_usd': 'Profit (USD)',
            'pair': 'Token Pair',
            'dex_buy': 'Buy DEX'
        },
        hover_data=['roi_percent', 'dex_sell']
    )
    
    fig.update_layout(
        xaxis_title="Token Pair",
        yaxis_title="Profit (USD)",
        showlegend=True,
        height=400
    )
    
    return fig

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Polygon Arbitrage Engine",
        page_icon="🔧",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .profit-positive {
        color: #00cc66;
        font-weight: bold;
    }
    .profit-negative {
        color: #ff4444;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.title("🔧 Polygon Arbitrage Engine")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Controls")
        
        # Auto-refresh
        auto_refresh = st.checkbox("🔄 Auto-refresh", value=True)
        refresh_interval = st.slider("Refresh interval (seconds)", 1, 30, 5)
        
        # Scan settings
        st.subheader("🔍 Scan Settings")
        use_test_data = st.checkbox("🧪 Use Test Data (Fast)", value=True, help="Use mock data for instant response vs real scan (takes minutes)")
        min_profit = st.number_input(
            "Minimum Profit ($)", 
            min_value=0.1, 
            max_value=1000.0, 
            value=1.0, 
            step=0.1
        )
        
        # Manual scan button
        if st.button("🚀 Scan Now", type="primary"):
            scan_type = "Test" if use_test_data else "Real"
            with st.spinner(f"{scan_type} scan for opportunities..."):
                scan_result = api.scan_opportunities(min_profit, use_test_data=use_test_data)
                st.session_state.last_scan = scan_result
                st.session_state.scan_time = datetime.now()
                st.session_state.use_test_data = use_test_data
                st.success(f"{scan_type} scan completed!")
    
    # Main content area
    col1, col2, col3, col4 = st.columns(4)
    
    # Get bot status
    status = api.get_status()
    
    if status:
        # Display metrics
        with col1:
            st.metric(
                "💰 Total Profit", 
                format_currency(status.get("statistics", {}).get("total_profit_usd", 0))
            )
        
        with col2:
            st.metric(
                "🎯 Opportunities Found", 
                status.get("statistics", {}).get("total_opportunities_found", 0)
            )
        
        with col3:
            st.metric(
                "⚡ Trades Executed", 
                status.get("statistics", {}).get("total_trades_executed", 0)
            )
        
        with col4:
            uptime = status.get("uptime_seconds", 0)
            st.metric(
                "⏱️ Uptime", 
                f"{int(uptime//3600)}h {int((uptime%3600)//60)}m"
            )
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🎯 Opportunities", "⚡ Execute", "📈 Analytics"])
    
    with tab1:
        st.subheader("📊 Real-time Dashboard")
        
        # Last scan results
        if 'last_scan' in st.session_state:
            scan_data = st.session_state.last_scan
            scan_time = st.session_state.scan_time
            is_test = st.session_state.get('use_test_data', False)
            
            # Warning for test data
            if is_test and scan_data.get('is_test_data'):
                st.warning("🧪 **Using Test Data** - This is mock data for demonstration only")
            
            st.info(f"Last scan: {scan_time.strftime('%Y-%m-%d %H:%M:%S')} ({'Test Mode' if is_test else 'Real Mode'})")
            
            if scan_data.get('found_opportunities'):
                opportunities = scan_data['found_opportunities']
                
                # Summary stats
                total_profit = sum(opp.get('profit_usd', 0) for opp in opportunities)
                avg_profit = total_profit / len(opportunities) if opportunities else 0
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Current Opportunities", len(opportunities))
                with col2:
                    st.metric("Total Potential Profit", format_currency(total_profit))
                with col3:
                    st.metric("Average Profit", format_currency(avg_profit))
                
                # Opportunity chart
                fig = create_opportunity_chart(opportunities)
                st.plotly_chart(fig, use_container_width=True)
                
                # Opportunities table
                st.subheader("🎯 Current Opportunities")
                df = pd.DataFrame(opportunities)
                
                # Format for display
                df['profit_usd'] = df['profit_usd'].apply(lambda x: f"${x:.2f}")
                df['roi_percent'] = df['roi_percent'].apply(lambda x: f"{x:.2f}%")
                
                st.dataframe(
                    df[['pair', 'dex_buy', 'dex_sell', 'profit_usd', 'roi_percent']],
                    use_container_width=True
                )
            else:
                st.warning("No opportunities found in last scan")
        else:
            st.info("Click 'Scan Now' to find opportunities")
    
    with tab2:
        st.subheader("🎯 Opportunity Scanner")
        
        # Advanced scan settings
        col1, col2 = st.columns(2)
        with col1:
            token_filter = st.text_input("Token Filter (e.g., WETH)", "")
        with col2:
            max_opportunities = st.number_input("Max Opportunities", 1, 100, 20)
        
        if st.button("🔍 Advanced Scan"):
            with st.spinner("Running advanced scan..."):
                scan_result = api.scan_opportunities(min_profit)
                
                if scan_result.get('opportunities'):
                    opps = scan_result['opportunities']
                    
                    # Filter by token if specified
                    if token_filter:
                        opps = [opp for opp in opps if token_filter.upper() in opp.get('pair', '')]
                    
                    # Limit results
                    opps = opps[:max_opportunities]
                    
                    st.success(f"Found {len(opps)} opportunities")
                    
                    for i, opp in enumerate(opps, 1):
                        with st.expander(f"{i}. {opp.get('pair')} - ${opp.get('profit_usd', 0):.2f}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Buy DEX:** {opp.get('dex_buy')}")
                                st.write(f"**Sell DEX:** {opp.get('dex_sell')}")
                                st.write(f"**Profit:** ${opp.get('profit_usd', 0):.2f}")
                            with col2:
                                st.write(f"**ROI:** {opp.get('roi_percent', 0):.2f}%")
                                st.write(f"**Amount:** ${opp.get('amount_usd', 0):,.0f}")
                                
                                # Execute button
                                if st.button(f"⚡ Execute {i}", key=f"execute_{i}"):
                                    # Create proposal
                                    proposal = {
                                        "strategy_id": f"manual_{i}",
                                        "summary": f"Arbitrage {opp.get('pair')}",
                                        "profit_usd": opp.get('profit_usd', 0),
                                        "payload": opp.get('payload', {})
                                    }
                                    
                                    result = api.execute_trade(proposal, auto_execute=False)
                                    
                                    if result.get('status') == 'proposed':
                                        st.success("Trade proposal created!")
                                    else:
                                        st.error(f"Failed to create proposal: {result}")
                else:
                    st.warning("No opportunities found")
    
    with tab3:
        st.subheader("⚡ Trade Execution")
        st.info("Manual trade execution interface")
        
        # Manual trade form
        with st.form("manual_trade"):
            st.subheader("Create Trade Proposal")
            
            col1, col2 = st.columns(2)
            with col1:
                pair = st.text_input("Token Pair", "WETH/USDC")
                dex_buy = st.selectbox("Buy DEX", ["QuickSwap", "SushiSwap", "Uniswap V3"])
                profit_target = st.number_input("Profit Target ($)", 1.0, 1000.0, 5.0)
            
            with col2:
                dex_sell = st.selectbox("Sell DEX", ["QuickSwap", "SushiSwap", "Uniswap V3"])
                trade_amount = st.number_input("Trade Amount ($)", 100, 100000, 5000)
                auto_execute = st.checkbox("Auto-execute", value=False)
            
            submitted = st.form_submit_button("🚀 Create Proposal", type="primary")
            
            if submitted:
                proposal = {
                    "strategy_id": f"manual_{int(time.time())}",
                    "summary": f"Manual arbitrage {pair}",
                    "profit_usd": profit_target,
                    "payload": {
                        "pair": pair,
                        "dex_buy": dex_buy,
                        "dex_sell": dex_sell,
                        "amount_usd": trade_amount
                    }
                }
                
                result = api.execute_trade(proposal, auto_execute=auto_execute)
                
                if result.get('status') in ['proposed', 'ok']:
                    st.success(f"Trade {'executed' if auto_execute else 'proposed'} successfully!")
                    if result.get('proposal_id'):
                        st.write(f"Proposal ID: {result.get('proposal_id')}")
                else:
                    st.error(f"Failed: {result}")
    
    with tab4:
        st.subheader("📈 Analytics & History")
        
        # Performance charts (placeholder for now)
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("📊 Profit Over Time")
            st.text("Historical profit chart (coming soon)")
        
        with col2:
            st.info("🎯 Success Rate")
            st.text("Trade success rate chart (coming soon)")
        
        # Recent activity log
        st.subheader("📋 Recent Activity")
        activity_data = [
            {"time": "12:34:56", "action": "Scan", "result": "5 opportunities found"},
            {"time": "12:33:21", "action": "Execute", "result": "Success: $2.34 profit"},
            {"time": "12:30:15", "action": "Scan", "result": "No opportunities"},
        ]
        
        df_activity = pd.DataFrame(activity_data)
        st.dataframe(df_activity, use_container_width=True)
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()

if __name__ == "__main__":
    main()
