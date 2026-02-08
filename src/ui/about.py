# import streamlit as st

# def show_about_page():
#     st.title("About This Project")
    
#     st.subheader("FinSage: An AI-Powered Financial Analyst Tool")
#     st.markdown("""
#     This project is an interactive web application designed to analyze a large dataset of user financial profiles. It combines a Business Intelligence (BI) dashboard, a machine learning forecasting model, and a generative AI chatbot into one unified platform.
#     """)
    
#     st.markdown("---")
    
#     st.subheader("Technology Stack")
#     st.markdown("""
#     * **Framework:** Streamlit
#     * **Data Analysis:** Pandas, Plotly
#     * **Machine Learning:** Statsmodels (for ARIMA model)
#     * **Generative AI:** Google Gemini Pro (using a simple RAG)
#     """)
    
#     st.markdown("---")

#     st.subheader("Page Explanations")
#     st.markdown("""
#     * **Dashboard:** A high-level visual overview with interactive charts showing key metrics and distributions from the data.
#     * **User Data:** A tool for filtering and drilling down into the raw dataset. You can also download your filtered results.
#     * **Expense Forecast:** This page displays a time-series forecast (using an ARIMA model) to predict future average expenses. It also includes a "decomposition" plot to show the underlying trend and seasonality.
#     * **AI Chat:** A chatbot (powered by Google Gemini) that uses a RAG system to answer questions about the dataset's global averages.
#     """)

#     st.markdown("---")
#     st.subheader("Data Source")
#     st.markdown("The app uses the 'Personal Finance ML Dataset', which contains 32,154 anonymized user profiles.")


import streamlit as st

def show_about_page():
    st.title("🛡️ About FinSage")
    st.markdown("""
    **FinSage** is an advanced AI-driven financial intelligence platform designed to bridge the gap between complex data analytics and actionable financial insights. 
    
    Starting as a basic tracker, this project has evolved into a sophisticated analytical engine capable of processing tens of thousands of financial profiles in real-time.
    """)

    st.markdown("---")

    # --- Section 1: Core Capabilities ---
    st.header("🚀 Key Features")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🤖 Context-Aware AI")
        st.write("""
        Utilizing **Dynamic RAG (Retrieval-Augmented Generation)**, our AI analyst 'FinSage' adapts its logic based on your UI filters. 
        It switches instantly between broad trend analysis and personalized 1-on-1 financial coaching.
        """)

        st.subheader("📈 Predictive Forecasting")
        st.write("""
        Built-in time-series analysis using the **ARIMA(1, 1, 1)** model. FinSage doesn't just look at the past; it projects future expense trends to help users prepare for upcoming financial shifts.
        """)

    with col2:
        st.subheader("📊 Real-Time Analytics")
        st.write("""
        The platform processes a dataset of **32,424 financial records**, providing instant KPI metrics including average income, credit health, and savings ratios across various global regions.
        """)

        st.subheader("📄 Professional Reporting")
        st.write("""
        With integrated **PDF Generation**, users can export their filtered data insights and AI-driven advice into a standardized document for audit trails and offline review.
        """)

    st.markdown("---")

    # --- Section 2: Technical Stack ---
    st.header("🛠️ The Tech Stack")
    st.info("""
    - **Frontend:** Streamlit (Python-based Web Framework)
    - **AI Engine:** Google Gemini 1.5 Flash (Generative AI)
    - **Forecasting:** Statsmodels (ARIMA Implementation)
    - **Data Processing:** Pandas & NumPy
    - **Reporting:** FPDF (PDF Generation Engine)
    """)

    st.markdown("---")

    # --- Section 3: The Architecture ---
    st.header("🧠 How it Works")
    st.markdown("""
    The application follows a modular architecture:
    1. **Data Ingestion:** Raw financial data is cleaned and standardized.
    2. **Context Filtering:** User-defined filters narrow the scope of the dataset.
    3. **RAG Pipeline:** The filtered data is summarized and injected into the LLM prompt as 'ground truth' context.
    4. **Inference:** Gemini generates insights based *only* on the provided context, preventing 'AI hallucinations'.
    """)
    
    

    st.markdown("---")
    st.caption("Developed as part of the AIML Project Series | 2026")