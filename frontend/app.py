import streamlit as st
import requests
from datetime import datetime
from typing import Dict, Any

# Page configuration
st.set_page_config(
    page_title="📈 Financial Ticker Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE_URL = st.secrets["api"]["backend_url"]

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1f77b4;
    }
    
    .success-message {
        padding: 1rem;
        border-radius: 10px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    
    .error-message {
        padding: 1rem;
        border-radius: 10px;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    
    .info-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "analysis_history" not in st.session_state:
        st.session_state.analysis_history = []

def display_header():
    """Display the main header"""
    st.markdown('<h1 class="main-header">📈 Financial Ticker Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("---")

def display_sidebar():
    """Display sidebar with controls and information"""
    with st.sidebar:
        st.header("🔧 Controls")
        
        # API Configuration
        st.subheader("API Configuration")
        api_base = st.text_input("API Base URL", value="https://stock-recommendation-api-arf3dtcygbgeggdp.canadacentral-01.azurewebsites.net/analyze", help="Base URL for the analysis API")
        
        # Analysis History
        st.subheader("📊 Analysis History")
        if st.session_state.analysis_history:
            for i, analysis in enumerate(reversed(st.session_state.analysis_history[-5:])):
                if st.button(f"🔍 {analysis['ticker']}", key=f"history_{i}"):
                    st.session_state.selected_analysis = analysis
        else:
            st.info("No analysis history yet")
        
        # Clear history button
        if st.button("🗑️ Clear History"):
            st.session_state.messages = []
            st.session_state.analysis_history = []
            st.rerun()
        
        # Information
        st.subheader("ℹ️ About")
        st.info("""
        This application analyzes financial tickers by sending requests to your backend API and presents the results in an easy-to-understand format.

        Simply enter a ticker symbol with exchange (e.g., INFY.NS, HAL.NS) to get started.
        """)

def format_financial_data(data: Dict[Any, Any]) -> Dict[str, Any]:
    """Simply return the data as is for display"""
    return data

def display_analysis_results(response_data: Dict[Any, Any], ticker: str):
    """Display analysis results in a formatted way"""
    try:
        # Create single tab for details
        tab1, = st.tabs(["🔍 Details"])
        
        with tab1:
            st.subheader("API Response")
            
            # Show raw JSON in an expandable section
            with st.expander("📄 Raw API Response", expanded=False):
                st.json(response_data)
            
            # Show formatted data
            if response_data:
                st.subheader("Analysis Results")
                for key, value in response_data.items():
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
    
    except Exception as e:
        st.error(f"Error formatting response data: {str(e)}")
        st.json(response_data)

def display_chat_interface():
    """Display the main chat interface"""
    # Chat messages container
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                if message["role"] == "user":
                    st.markdown(f"**Analyzing ticker:** `{message['content']}`")
                else:
                    if "error" in message:
                        st.error(f"❌ Error: {message['error']}")
                    else:
                        display_analysis_results(message["content"], message.get("ticker", "Unknown"))

def handle_user_input():
    """Handle user input and API requests"""
    # Input section
    st.subheader("🎯 Enter Ticker Symbol")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        ticker_input = st.text_input(
            "Ticker Symbol",
            placeholder="e.g., HAL.NS, INFY.NS",
            label_visibility="collapsed"
        )
    
    with col2:
        analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)
    
    # Handle input from chat input or button
    if analyze_button and ticker_input:
        process_ticker_analysis(ticker_input.strip().upper())
    
    # Chat input as alternative
    # if prompt := st.chat_input("Or type ticker here and press Enter..."):
    #     process_ticker_analysis(prompt.strip().upper())

def process_ticker_analysis(ticker: str):
    """Process ticker analysis request"""
    if not ticker:
        st.warning("⚠️ Please enter a ticker symbol")
        return
    
    # Add user message to chat
    st.chat_message("user").markdown(f"**Analyzing ticker:** `{ticker}`")
    st.session_state.messages.append({"role": "user", "content": ticker})
    
    # Show loading spinner
    with st.spinner(f"🔄 Analyzing {ticker}..."):
        try:
            # Make API request
            api_url = f"{API_BASE_URL}/{ticker}"
            response = requests.post(api_url)
            
            if response.status_code == 200:
                response_data = response.json()
                
                # Display results
                with st.chat_message("assistant"):
                    display_analysis_results(response_data, ticker)
                
                # Add to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response_data,
                    "ticker": ticker,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Add to analysis history
                st.session_state.analysis_history.append({
                    "ticker": ticker,
                    "data": response_data,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Success message
                st.success(f"✅ Successfully analyzed {ticker}")
                
            else:
                error_msg = f"API request failed with status code {response.status_code}"
                st.error(f"❌ {error_msg}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "error": error_msg,
                    "ticker": ticker
                })
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Connection error: {str(e)}"
            st.error(f"❌ {error_msg}")
            st.session_state.messages.append({
                "role": "assistant",
                "error": error_msg,
                "ticker": ticker
            })
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            st.error(f"❌ {error_msg}")
            st.session_state.messages.append({
                "role": "assistant",
                "error": error_msg,
                "ticker": ticker
            })
    
    # Rerun to update the interface
    st.rerun()

def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Display header
    display_header()
    
    # Display sidebar
    display_sidebar()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Handle user input
        handle_user_input()
        
        # Display chat interface
        display_chat_interface()
    
    with col2:
        # Summary statistics
        if st.session_state.analysis_history:
            st.subheader("📊 Quick Stats")
            st.metric("Total Analyses", len(st.session_state.analysis_history))
            
            # Most recent analysis
            if st.session_state.analysis_history:
                recent = st.session_state.analysis_history[-1]
                st.metric("Last Analyzed", recent['ticker'])
                st.caption(f"At {datetime.fromisoformat(recent['timestamp']).strftime('%H:%M:%S')}")
        
        # Tips section
        st.subheader("💡 Tips")
        st.info("""
        **Popular Tickers to Try:**
        - INFOSYS (INFY.NS)
        - HAL (HAL.NS)
        - Microsoft (MSFT.NE)
        - Amazon (AMZN.NE)
        - NVIDIA (NVDA.DE)
        """)

if __name__ == "__main__":
    main()