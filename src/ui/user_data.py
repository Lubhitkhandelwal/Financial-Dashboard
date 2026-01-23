import streamlit as st
import pandas as pd

def show_user_data_page(df):
    st.title("User Data Viewer")
    st.markdown("Filter and review the user data.")
    
    if df.empty:
        st.warning("No data to display.")
        return
        
    # --- Filters moved from sidebar to main page ---
    st.subheader("Interactive Filters")
    
    # Create three columns for the filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Filter by Region
        regions = st.multiselect(
            "Region",
            options=df['region'].unique(),
            default=[]  # <-- FIX: Set default to empty list
        )
    
    with col2:
        # Filter by Education
        education = st.multiselect(
            "Education Level",
            options=df['education_level'].unique(),
            default=[]  # <-- FIX: Set default to empty list
        )
    
    with col3:
        # Filter by Credit Score
        min_score, max_score = int(df['credit_score'].min()), int(df['credit_score'].max())
        score_range = st.slider(
            "Credit Score Range",
            min_value=min_score,
            max_value=max_score,
            value=(min_score, max_score)
        )
    
    # --- End of filters ---
    st.markdown("---") # Add a visual separator

    # --- NEW FILTER LOGIC ---
    
    # Start with the full dataframe
    df_filtered = df.copy()

    # Apply filters only if a selection is made
    if regions:  # This list is only non-empty if the user selected something
        df_filtered = df_filtered[df_filtered['region'].isin(regions)]

    if education: # This list is only non-empty if the user selected something
        df_filtered = df_filtered[df_filtered['education_level'].isin(education)]

    # The slider filter is always active, which is correct
    df_filtered = df_filtered[
        (df_filtered['credit_score'] >= score_range[0]) &
        (df_filtered['credit_score'] <= score_range[1])
    ]

    # --- Display Dataframe ---
    st.markdown(f"Displaying **{len(df_filtered)}** of **{len(df)}** records.")
    st.dataframe(df_filtered.sort_values(by='record_date', ascending=False), use_container_width=True)