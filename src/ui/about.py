import streamlit as st

def show_about_page():
    st.title("About This Project")
    
    st.subheader("FinSage: An AI-Powered Financial Analyst Tool")
    st.markdown("""
    This project is an interactive web application designed to analyze a large dataset of user financial profiles. It combines a Business Intelligence (BI) dashboard, a machine learning forecasting model, and a generative AI chatbot into one unified platform.
    """)
    
    st.markdown("---")
    
    st.subheader("Technology Stack")
    st.markdown("""
    * **Framework:** Streamlit
    * **Data Analysis:** Pandas, Plotly
    * **Machine Learning:** Statsmodels (for ARIMA model)
    * **Generative AI:** Google Gemini Pro (using a simple RAG)
    """)
    
    st.markdown("---")

    st.subheader("Page Explanations")
    st.markdown("""
    * **Dashboard:** A high-level visual overview with interactive charts showing key metrics and distributions from the data.
    * **User Data:** A tool for filtering and drilling down into the raw dataset. You can also download your filtered results.
    * **Expense Forecast:** This page displays a time-series forecast (using an ARIMA model) to predict future average expenses. It also includes a "decomposition" plot to show the underlying trend and seasonality.
    * **AI Chat:** A chatbot (powered by Google Gemini) that uses a RAG system to answer questions about the dataset's global averages.
    """)

    st.markdown("---")
    st.subheader("Data Source")
    st.markdown("The app uses the 'Personal Finance ML Dataset', which contains 32,154 anonymized user profiles.")