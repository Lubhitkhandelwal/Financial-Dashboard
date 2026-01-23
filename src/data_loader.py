import pandas as pd
import streamlit as st
import os

PROCESSED_DATA_PATH = 'data/processed/cleaned_finance_data.csv'

@st.cache_data
def load_data():
    if not os.path.exists(PROCESSED_DATA_PATH):
        st.error("Cleaned data file not found. Please run Notebook 01 first.")
        return pd.DataFrame()
        
    df = pd.read_csv(PROCESSED_DATA_PATH)
    df['record_date'] = pd.to_datetime(df['record_date'])
    return df