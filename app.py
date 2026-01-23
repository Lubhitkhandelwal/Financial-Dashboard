import streamlit as st
from src.data_loader import load_data
# We do NOT load categorizer components
from src.forecaster import load_forecaster_model
from src.llm_interface import configure_gemini

# Import NEW/UPDATED UI pages
from src.ui.dashboard import show_dashboard_page
from src.ui.user_data import show_user_data_page # Renamed
# We do NOT import categorize_tool
from src.ui.forecasts import show_forecasts_page
from src.ui.ai_chat import show_ai_chat_page

from src.ui.about import show_about_page

# --- Page Configuration ---
st.set_page_config(
    page_title="FinSage - AI Finance Analyst", # Updated title
    page_icon="📊",
    layout="wide"
)

# --- Load Data and Models (Cached) ---
with st.spinner("Loading financial data and AI models..."):
    df = load_data()
    # We only load the forecaster model
    forecaster_model = load_forecaster_model()
    
# Configure Gemini API
configure_gemini()
    
# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
page_options = [
    "Dashboard", 
    "User Data", # Renamed
    "Expense Forecast", 
    "AI Chat",
    "About"
    # "Categorizer Tool (Demo)" is REMOVED
]
page = st.sidebar.radio("Go to:", page_options)

# st.sidebar.markdown("---")
# st.sidebar.info(
#     "This app is a demo combining data analysis, time-series forecasting (ARIMA), "
#     "and LLMs (Gemini) with Streamlit." # Updated info
# )

# --- Page Routing ---
if page == "Dashboard":
    show_dashboard_page(df)

elif page == "User Data":
    show_user_data_page(df) # Updated page call

elif page == "Expense Forecast":
    show_forecasts_page(df, forecaster_model)
    
elif page == "AI Chat":
    show_ai_chat_page(df)

elif page == "About":  
    show_about_page()

# "Categorizer Tool" route is REMOVED