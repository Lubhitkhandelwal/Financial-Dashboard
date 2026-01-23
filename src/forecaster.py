import streamlit as st
from statsmodels.tsa.arima.model import ARIMAResults
import os
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose # <-- NEW IMPORT

MODEL_PATH = 'models/forecaster/arima_model.pkl'

@st.cache_resource
def load_forecaster_model():
    """
    Loads the fitted ARIMA model.
    """
    if not os.path.exists(MODEL_PATH):
        st.error("Forecaster model not found. Please run Notebook 03.")
        return None
        
    model_fit = ARIMAResults.load(MODEL_PATH)
    return model_fit

def get_forecast(model_fit, steps=12):
    """
    Generates future forecasts with confidence intervals.
    """
    if model_fit is None:
        return pd.Series(), pd.Series(), pd.Series()
        
    # Get the forecast object
    forecast_object = model_fit.get_forecast(steps=steps)
    
    # Get the mean prediction
    mean_forecast = forecast_object.predicted_mean
    
    # Get the 95% confidence interval DataFrame
    conf_int_df = forecast_object.conf_int(alpha=0.05)
    
    # Get the lower and upper bounds
    lower_bounds = conf_int_df.iloc[:, 0]
    upper_bounds = conf_int_df.iloc[:, 1]
    
    return mean_forecast, lower_bounds, upper_bounds

def get_historical_data(df):
    """
    Prepares the historical *average* monthly expense data for plotting.
    """
    df_time = df.set_index('record_date')
    monthly_avg_expenses = df_time['monthly_expenses_usd'].resample('MS').mean()
    monthly_avg_expenses = monthly_avg_expenses.asfreq('MS', fill_value=monthly_avg_expenses.mean())
    return monthly_avg_expenses

# --- NEW FUNCTION ---
@st.cache_data
def get_decomposition(historical_data):
    """
    Decomposes the time series into trend, seasonal, and residual components.
    """
    # We need at least 2 full cycles (24 months) to get a good seasonal decomposition
    if len(historical_data) > 24:
        decomposition = seasonal_decompose(historical_data, model='additive', period=12)
        trend = decomposition.trend
        seasonal = decomposition.seasonal
        resid = decomposition.resid
        return trend, seasonal, resid
    else:
        # Not enough data to decompose
        return None, None, None