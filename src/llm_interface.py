import google.generativeai as genai
import streamlit as st
import pandas as pd
import re

# --- NEW IMPORT: Bring in the forecasting model ---
from src.forecaster import load_forecaster_model, get_forecast

def configure_gemini():
    """
    Configures the Gemini API using Streamlit's secrets.
    """
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    except Exception as e:
        st.error(f"Failed to configure Gemini: {e}. Please check your .streamlit/secrets.toml file.")

def get_forecast_summary():
    """
    Runs the ARIMA model to get a short text summary of future predictions.
    """
    try:
        # 1. Load the model (cached)
        model_fit = load_forecaster_model()
        
        if model_fit is None:
            return "Forecast data is currently unavailable."

        # 2. Generate a 6-month forecast
        # We only need the mean forecast for the text summary
        mean_forecast, _, _ = get_forecast(model_fit, steps=6)
        
        # 3. Format it into a readable string
        forecast_text = "\n**Projected Future Expenses (Next 6 Months):**\n"
        if not mean_forecast.empty:
            for date, value in mean_forecast.items():
                date_str = date.strftime('%b %Y')
                forecast_text += f"- {date_str}: ${value:,.2f}\n"
                
            # Add trend analysis
            first_val = mean_forecast.iloc[0]
            last_val = mean_forecast.iloc[-1]
            if last_val > first_val:
                forecast_text += "(Overall Trend: Expenses are projected to INCREASE)"
            elif last_val < first_val:
                forecast_text += "(Overall Trend: Expenses are projected to DECREASE)"
            else:
                forecast_text += "(Overall Trend: Expenses are projected to remain STABLE)"
        
        return forecast_text

    except Exception as e:
        return f"Error generating forecast: {e}"

def get_data_summary(df, region_name="all users"):
    """
    Creates a simple text summary of the *provided* DataFrame.
    """
    if df.empty:
        return f"No financial data available for {region_name}."
        
    avg_income = df['monthly_income_usd'].mean()
    avg_expense = df['monthly_expenses_usd'].mean()
    avg_savings = df['savings_usd'].mean()
    avg_credit_score = df['credit_score'].mean()
    loan_count = df['has_loan'].value_counts().get("Yes", 0)
    
    summary = f"""
    Here is a summary for {region_name}:
    - Average Monthly Income: {avg_income:,.2f} USD
    - Average Monthly Expenses: {avg_expense:,.2f} USD
    - Average Total Savings: {avg_savings:,.2f} USD
    - Average Credit Score: {avg_credit_score:,.0f}
    - Total Number of Users with a Loan: {loan_count}
    """
    return summary

def get_gemini_response(question, df):
    """
    Answers a user's question by combining:
    1. Filtered Historical Data (Region-aware)
    2. Future Forecast Data (ARIMA)
    """
    
    # Use the model that works for you (gemini-1.5-flash is recommended if available)
    model = genai.GenerativeModel("gemini-flash-latest") 
    
    # --- 1. Get Forecast Context ---
    forecast_context = get_forecast_summary()
    
    # --- 2. Dynamic Region Filtering ---
    data_to_summarize = df 
    region_context = "all users"
    question_lower = question.lower()
    
    if 'asia' in question_lower:
        data_to_summarize = df[df['region'].str.title() == 'Asia']
        region_context = "users in Asia"
    elif 'europe' in question_lower:
        data_to_summarize = df[df['region'].str.title() == 'Europe']
        region_context = "users in Europe"
    elif 'africa' in question_lower:
        data_to_summarize = df[df['region'].str.title() == 'Africa']
        region_context = "users in Africa"
    elif 'north america' in question_lower:
        data_to_summarize = df[df['region'].str.title() == 'North America']
        region_context = "users in North America"
    elif 'other' in question_lower:
        data_to_summarize = df[df['region'].str.title() == 'Other']
        region_context = "users in the 'Other' region"

    # --- 3. Get Historical Data Context ---
    historical_context = get_data_summary(data_to_summarize, region_context)
    
    # --- 4. Build the Master Prompt ---
    prompt = f"""
    You are 'FinSage', an expert AI financial analyst.
    Your personality is helpful, insightful, and clear.
    
    A user has asked the following question:
    "{question}"
    
    -----------------------------------------
    SECTION 1: HISTORICAL DATA ({region_context})
    {historical_context}
    -----------------------------------------
    SECTION 2: FUTURE FORECAST (Global Average Expenses)
    {forecast_context}
    -----------------------------------------
    
    Instructions:
    1. Answer the user's question based *only* on the provided data.
    2. If they ask about "Asia", "Europe", etc., use the Historical Data section.
    3. If they ask about "Future", "Next Month", or "Predictions", use the Future Forecast section.
    4. You can combine both! (e.g., "Current average expense is X, and it is projected to increase to Y").
    5. Do not make up numbers.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error communicating with Gemini: {e}")
        return "Sorry, I'm having trouble connecting to the AI model right now."