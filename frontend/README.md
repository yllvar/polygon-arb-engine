# 🌐 Streamlit Frontend Setup

## 🚀 Quick Start

### **1. Install Dependencies**
```bash
cd frontend
pip install -r requirements.txt
```

### **2. Start Backend API**
```bash
# Terminal 1: Start the API server
cd ..
python main.py

# Or start in background
./scripts/start-automation.sh
```

### **3. Launch Frontend**
```bash
# Terminal 2: Start Streamlit
cd frontend
streamlit run streamlit_app.py

# Or specify port
streamlit run streamlit_app.py --server.port 8501
```

### **4. Access Web Interface**
- **Frontend:** http://localhost:8501
- **Backend API:** http://localhost:5050

## 🎯 Features

### **📊 Real-time Dashboard**
- Live bot statistics (profit, trades, uptime)
- Auto-refreshing opportunity monitoring
- Visual profit charts and metrics
- Status indicators and alerts

### **🎯 Opportunity Scanner**
- Manual and automated scanning
- Adjustable profit thresholds
- Token filtering and sorting
- One-click trade execution

### **⚡ Trade Execution**
- Manual trade proposal creation
- Auto-execute option for confirmed trades
- Real-time execution feedback
- Trade history tracking

### **📈 Analytics**
- Profit over time charts
- Success rate metrics
- DEX performance comparison
- Activity logs and history

## 🎨 Interface Overview

### **Main Navigation**
- **Dashboard:** Real-time overview and metrics
- **Opportunities:** Scanner and opportunity details
- **Execute:** Manual trade interface
- **Analytics:** Charts and historical data

### **Key Components**
- **Sidebar Controls:** Scan settings, auto-refresh
- **Metrics Cards:** Key performance indicators
- **Interactive Charts:** Opportunity visualization
- **Data Tables:** Detailed opportunity listings
- **Trade Forms:** Manual execution interface

## 🔧 Configuration

### **Environment Variables**
```bash
# API Configuration
API_BASE_URL=http://localhost:5050
PAGE_REFRESH_INTERVAL=5

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
```

### **Customization**
- Edit `streamlit_app.py` for UI changes
- Modify `API_BASE_URL` for different backend
- Adjust refresh intervals and defaults

## 📱 Mobile Support

The Streamlit interface is responsive and works on:
- **Desktop browsers** (Chrome, Firefox, Safari)
- **Tablet devices** (iPad, Android tablets)
- **Mobile browsers** (limited functionality)

## 🛡️ Security Notes

- Frontend runs locally by default
- API keys stored in backend `.env` file
- Trade execution requires manual confirmation
- Auto-execute can be disabled for safety

## 🐛 Troubleshooting

### **Common Issues**

#### **"Failed to connect to API"**
```bash
# Check if backend is running
curl http://localhost:5050/status

# Start backend if needed
python main.py
```

#### **"Streamlit not found"**
```bash
# Install Streamlit
pip install streamlit

# Verify installation
streamlit --version
```

#### **"Port already in use"**
```bash
# Use different port
streamlit run streamlit_app.py --server.port 8502
```

### **Debug Mode**
```bash
# Run with debug logging
streamlit run streamlit_app.py --logger.level debug
```

## 🔄 Development

### **Adding New Features**
1. Update `streamlit_app.py` with new components
2. Add corresponding API endpoints if needed
3. Update `requirements.txt` for new dependencies
4. Test with `streamlit run`

### **Custom Styling**
```python
# Add custom CSS in streamlit_app.py
st.markdown("""
<style>
.custom-class {
    background-color: #f0f2f6;
    padding: 20px;
}
</style>
""", unsafe_allow_html=True)
```

## 📊 API Integration

### **Available Endpoints**
- `GET /status` - Bot statistics
- `POST /scan` - Scan opportunities
- `POST /simulate` - Simulate trades
- `POST /propose` - Execute trades

### **Data Flow**
```
Frontend (Streamlit) → API Client → Backend API → Core Bot Logic
```

## 🚀 Production Deployment

### **Docker Setup**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

### **Cloud Deployment**
- **Streamlit Cloud:** Direct deployment
- **Heroku:** With Docker
- **AWS EC2:** Custom setup
- **DigitalOcean:** Droplet deployment

## 📞 Support

For issues with the Streamlit frontend:
1. Check backend API is running
2. Verify dependencies are installed
3. Check network connectivity
4. Review logs for error messages

**Frontend enhances the CLI experience with visual monitoring and easy trade execution!** 🎯
