import streamlit as st
import plotly.express as px
import pandas as pd

def show_dashboard_page(df):
    st.title("Financial Dashboard")
    st.markdown("A high-level overview of the financial dataset.")
    
    if df.empty:
        st.warning("No data to display.")
        return

    # --- On-page filter ---
    st.header("Filters")
    region_list = ["All"] + df['region'].unique().tolist()
    selected_region = st.selectbox("Select a Region to analyze:", region_list)

    # Filter the dataframe based on selection
    if selected_region == "All":
        filtered_df = df
    else:
        filtered_df = df[df['region'] == selected_region]

    st.markdown("---")

    # --- KPI Metrics (now using the filtered_df) ---
    st.header(f"Metrics for: {selected_region}")
    avg_income = filtered_df['monthly_income_usd'].mean()
    avg_expense = filtered_df['monthly_expenses_usd'].mean()
    avg_savings = filtered_df['savings_usd'].mean()
    avg_credit = filtered_df['credit_score'].mean()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg. Income", f"${avg_income:,.0f}")
    col2.metric("Avg. Expense", f"${avg_expense:,.0f}")
    col3.metric("Avg. Savings", f"${avg_savings:,.0f}")
    col4.metric("Avg. Credit Score", f"{avg_credit:,.0f}")

    st.markdown("---")

    # --- Charts - Row 1 ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribution of Credit Scores")
        fig_hist = px.histogram(filtered_df, 
                                x='credit_score', 
                                nbins=30,
                                template="plotly_dark"
                               )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        st.subheader("Savings vs. Monthly Income")
        fig_scatter = px.scatter(
            filtered_df.sample(min(1000, len(filtered_df))), 
            x='monthly_income_usd', 
            y='savings_usd', 
            color='employment_status',
            title="Savings vs. Income",
            hover_data=['age', 'job_title'],
            template="plotly_dark"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("---")
    
    # --- Charts - Row 2 ---
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Education Level Distribution")
        education_counts = filtered_df['education_level'].value_counts().reset_index()
        fig_pie = px.pie(education_counts, 
                         names='education_level', 
                         values='count',
                         title="Education Levels",
                         template="plotly_dark"
                        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col4:
        st.subheader("Employment Status")
        employment_counts = filtered_df['employment_status'].value_counts().reset_index()
        fig_bar = px.bar(employment_counts, 
                         x='employment_status', 
                         y='count',
                         title="Employment Status",
                         template="plotly_dark"
                        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # --- NEW SECTION: Charts - Row 3 (Demographics) ---
    col5, col6 = st.columns(2)

    with col5:
        st.subheader("Age Distribution")
        fig_age_hist = px.histogram(filtered_df, 
                                    x='age', 
                                    nbins=30,
                                    template="plotly_dark"
                                   )
        st.plotly_chart(fig_age_hist, use_container_width=True)

    with col6:
        st.subheader("Loan Status")
        loan_counts = filtered_df['has_loan'].value_counts().reset_index()
        fig_loan_pie = px.pie(loan_counts, 
                              names='has_loan', 
                              values='count',
                              title="Proportion of Users with a Loan",
                              template="plotly_dark"
                             )
        st.plotly_chart(fig_loan_pie, use_container_width=True)
    
    st.markdown("---")

    # --- NEW SECTION: Charts - Row 4 (Advanced) ---
    col7, col8 = st.columns(2)

    with col7:
        st.subheader("Average Savings Over Time")
        # We must resample the data just like in the forecast notebook
        df_time = filtered_df.set_index('record_date')
        monthly_avg_savings = df_time['savings_usd'].resample('MS').mean().reset_index()
        
        fig_time_series = px.line(monthly_avg_savings, 
                                  x='record_date', 
                                  y='savings_usd',
                                  title="Average User Savings (Monthly)",
                                  template="plotly_dark"
                                 )
        st.plotly_chart(fig_time_series, use_container_width=True)

    with col8:
        st.subheader("Financial Correlation Heatmap")
        # Select only the key numerical columns
        numeric_cols = ['age', 'monthly_income_usd', 'monthly_expenses_usd', 
                        'savings_usd', 'loan_amount_usd', 'debt_to_income_ratio', 
                        'credit_score']
        
        corr_matrix = filtered_df[numeric_cols].corr()
        
        fig_heatmap = px.imshow(corr_matrix, 
                                text_auto=True,  # Show the correlation numbers
                                aspect="auto",
                                title="Correlation Between Financial Metrics",
                                template="plotly_dark"
                               )
        st.plotly_chart(fig_heatmap, use_container_width=True)