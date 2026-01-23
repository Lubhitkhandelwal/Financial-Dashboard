import streamlit as st
import plotly.graph_objects as go
from src.forecaster import get_forecast, get_historical_data, get_decomposition
import pandas as pd
import plotly.express as px

def show_forecasts_page(df, model_fit):
    st.title("Expense Forecast")
    st.markdown("Forecasting the *average* monthly expense across all users (from Notebook 03).")
    
    if model_fit is None:
        st.error("Model not loaded. Please run Notebook 03.")
        return
        
    # --- Get Data ---
    historical_data = get_historical_data(df)
    
    forecast_steps = st.slider("Months to forecast:", min_value=6, max_value=36, value=12)
    
    with st.spinner("Generating forecast..."):
        # Now get all three components from our updated function
        mean_forecast, lower_bounds, upper_bounds = get_forecast(model_fit, steps=forecast_steps)
    
    # --- NEW: Key Metrics ---
    st.header("Key Forecast Metrics")
    col1, col2, col3 = st.columns(3)
    
    # Get the last historical value
    last_hist_val = historical_data.iloc[-1]
    
    # Get the final forecasted value
    final_forecast_val = mean_forecast.iloc[-1]
    
    # Get the 12-month (or selected) forecast value
    forecast_12m = mean_forecast.iloc[forecast_steps - 1]
    
    col1.metric("Last Actual Expense", f"${last_hist_val:,.2f}")
    col2.metric(f"{forecast_steps}-Month Forecast", f"${forecast_12m:,.2f}")
    col3.metric("Change", f"{final_forecast_val - last_hist_val:,.2f}", 
               delta_color="inverse")
    
    st.markdown("---")

    # --- Plot ---
    st.header("Forecast Plot")
    fig = go.Figure()

    # Plot Future Confidence Interval (the "min" and "max" band)
    fig.add_trace(go.Scatter(
        x=upper_bounds.index, y=upper_bounds, mode='lines',
        line=dict(color='rgba(170, 170, 170, 0)'), showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=lower_bounds.index, y=lower_bounds, mode='lines',
        line=dict(color='rgba(170, 170, 170, 0)'), fill='tonexty',
        fillcolor='rgba(100, 0, 100, 0.25)', name='95% Confidence Interval'
    ))
    
    # Historical Data (Blue)
    fig.add_trace(go.Scatter(
        x=historical_data.index,
        y=historical_data.values,
        mode='lines',
        name='Historical Avg. Expenses',
        line=dict(color='#0068C9')
    ))
    
    # Forecasted Mean Data (Dotted Purple)
    fig.add_trace(go.Scatter(
        x=mean_forecast.index,
        y=mean_forecast.values,
        mode='lines',
        name='Future Forecast (Mean)',
        line=dict(dash='dot', color='#5800D4', width=2)
    ))
    
    fig.update_layout(
        title="Average Monthly Expense Forecast (with 95% Confidence Interval)",
        xaxis_title="Date",
        yaxis_title="Amount (USD)",
        legend_title="Data Type",
        template="plotly_dark"  # <-- Added dark theme!
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Forecasted Data")
    # Show all three values in the table
    forecast_df = pd.DataFrame({
        'Forecast (Mean)': mean_forecast,
        'Lower Bound (95%)': lower_bounds,
        'Upper Bound (95%)': upper_bounds
    })
    st.dataframe(forecast_df, use_container_width=True)
    
    st.markdown("---")

    # --- NEW: Time-Series Decomposition ---
    st.header("Historical Data Analysis")
    
    # Put it in an expander so it's clean
    with st.expander("Show Time-Series Decomposition"):
        trend, seasonal, resid = get_decomposition(historical_data)
        
        if trend is not None:
            st.markdown("""
            This chart breaks down your historical data into its core components:
            * **Trend:** The long-term direction.
            * **Seasonal:** The repeating 12-month pattern.
            * **Residual:** The random, unpredictable "noise".
            """)
            
            # Create a dataframe for easy plotting
            decomp_df = pd.DataFrame({
                'Original': historical_data,
                'Trend': trend,
                'Seasonal': seasonal,
                'Residual': resid
            })
            
            # Plot all components
            fig_decomp = px.line(decomp_df, 
                                 facet_row='variable', 
                                 title="Time-Series Decomposition",
                                 template="plotly_dark")
            
            # Make the plots independent and cleaner
            fig_decomp.update_yaxes(matches=None)
            st.plotly_chart(fig_decomp, use_container_width=True)
            
        else:
            st.info("Not enough historical data (24+ months) to perform a seasonal decomposition.")