# # # # import streamlit as st
# # # # import pandas as pd

# # # # def show_user_data_page(df):
# # # #     st.title("User Data Viewer")
# # # #     st.markdown("Filter and review the user data.")
    
# # # #     if df.empty:
# # # #         st.warning("No data to display.")
# # # #         return
        
# # # #     # --- Filters moved from sidebar to main page ---
# # # #     st.subheader("Interactive Filters")
    
# # # #     # Create three columns for the filters
# # # #     col1, col2, col3 = st.columns(3)
    
# # # #     with col1:
# # # #         # Filter by Region
# # # #         regions = st.multiselect(
# # # #             "Region",
# # # #             options=df['region'].unique(),
# # # #             default=[]  # <-- FIX: Set default to empty list
# # # #         )
    
# # # #     with col2:
# # # #         # Filter by Education
# # # #         education = st.multiselect(
# # # #             "Education Level",
# # # #             options=df['education_level'].unique(),
# # # #             default=[]  # <-- FIX: Set default to empty list
# # # #         )
    
# # # #     with col3:
# # # #         # Filter by Credit Score
# # # #         min_score, max_score = int(df['credit_score'].min()), int(df['credit_score'].max())
# # # #         score_range = st.slider(
# # # #             "Credit Score Range",
# # # #             min_value=min_score,
# # # #             max_value=max_score,
# # # #             value=(min_score, max_score)
# # # #         )
    
# # # #     # --- End of filters ---
# # # #     st.markdown("---") # Add a visual separator

# # # #     # --- NEW FILTER LOGIC ---
    
# # # #     # Start with the full dataframe
# # # #     df_filtered = df.copy()

# # # #     # Apply filters only if a selection is made
# # # #     if regions:  # This list is only non-empty if the user selected something
# # # #         df_filtered = df_filtered[df_filtered['region'].isin(regions)]

# # # #     if education: # This list is only non-empty if the user selected something
# # # #         df_filtered = df_filtered[df_filtered['education_level'].isin(education)]

# # # #     # The slider filter is always active, which is correct
# # # #     df_filtered = df_filtered[
# # # #         (df_filtered['credit_score'] >= score_range[0]) &
# # # #         (df_filtered['credit_score'] <= score_range[1])
# # # #     ]

# # # #     # --- Display Dataframe ---
# # # #     st.markdown(f"Displaying **{len(df_filtered)}** of **{len(df)}** records.")
# # # #     st.dataframe(df_filtered.sort_values(by='record_date', ascending=False), use_container_width=True)


# # # import streamlit as st
# # # import pandas as pd
# # # from src.llm_interface import get_gemini_response, configure_gemini

# # # def show_user_data_page(df):
# # #     st.title("User Data & AI Analyst")
# # #     st.markdown("Filter the user data below and ask **FinSage** for specific insights.")
    
# # #     if df.empty:
# # #         st.warning("No data to display.")
# # #         return
        
# # #     # --- Interactive Filters (Main Page) ---
# # #     st.subheader("Interactive Filters")
# # #     col1, col2, col3 = st.columns(3)
    
# # #     with col1:
# # #         regions = st.multiselect(
# # #             "Region",
# # #             options=df['region'].unique(),
# # #             default=[]
# # #         )
    
# # #     with col2:
# # #         education = st.multiselect(
# # #             "Education Level",
# # #             options=df['education_level'].unique(),
# # #             default=[]
# # #         )
    
# # #     with col3:
# # #         min_score, max_score = int(df['credit_score'].min()), int(df['credit_score'].max())
# # #         score_range = st.slider(
# # #             "Credit Score Range",
# # #             min_value=min_score,
# # #             max_value=max_score,
# # #             value=(min_score, max_score)
# # #         )
    
# # #     # --- Filter Logic ---
# # #     df_filtered = df.copy()

# # #     if regions:
# # #         df_filtered = df_filtered[df_filtered['region'].isin(regions)]

# # #     if education:
# # #         df_filtered = df_filtered[df_filtered['education_level'].isin(education)]

# # #     df_filtered = df_filtered[
# # #         (df_filtered['credit_score'] >= score_range[0]) &
# # #         (df_filtered['credit_score'] <= score_range[1])
# # #     ]

# # #     # --- Data Display ---
# # #     st.markdown(f"Displaying **{len(df_filtered)}** of **{len(df)}** records.")
# # #     # --- REAL-TIME STATS (Add this section) ---
# # #     st.markdown("---")
# # #     kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    
# # #     with kpi_col1:
# # #         st.metric("Users Displayed", len(df_filtered))
        
# # #     with kpi_col2:
# # #         if not df_filtered.empty:
# # #             avg_inc = df_filtered['monthly_income_usd'].mean()
# # #             st.metric("Avg. Monthly Income", f"${avg_inc:,.2f}")
            
# # #     with kpi_col3:
# # #         if not df_filtered.empty:
# # #             avg_cred = df_filtered['credit_score'].mean()
# # #             st.metric("Avg. Credit Score", f"{avg_cred:.0f}")
# # #     st.dataframe(df_filtered.sort_values(by='record_date', ascending=False), use_container_width=True)

# # #     st.markdown("---") # Visual Separator before Chat

# # #     # --- INTEGRATED AI CHAT ---
# # #     st.subheader("💬 Ask FinSage about this Filtered View")
    
# # #     # Initialize Gemini
# # #     configure_gemini()

# # #     # Use a specific session state key for this page to avoid conflicts
# # #     if "data_page_chat_history" not in st.session_state:
# # #         st.session_state.data_page_chat_history = []

# # #     # Display Chat History
# # #     for message in st.session_state.data_page_chat_history:
# # #         with st.chat_message(message["role"]):
# # #             st.markdown(message["content"])

# # #     # Chat Input Box
# # #     user_query = st.chat_input("Ex: What is the average income for this specific filtered group?")

# # #     if user_query:
# # #         # 1. Add user message to history
# # #         st.session_state.data_page_chat_history.append({"role": "user", "content": user_query})
# # #         with st.chat_message("user"):
# # #             st.markdown(user_query)
            
# # #         # 2. Generate and display AI response
# # #         with st.spinner("FinSage is analyzing the data on your screen..."):
# # #             # IMPORTANT: We pass df_filtered so the AI only sees what the user has filtered!
# # #             response = get_gemini_response(user_query, df_filtered)
            
# # #         st.session_state.data_page_chat_history.append({"role": "assistant", "content": response})
# # #         with st.chat_message("assistant"):
# # #             st.markdown(response)

# # #     # Optional: Add a 'Clear Chat' button in the sidebar or below
# # #     if st.button("Clear Chat History"):
# # #         st.session_state.data_page_chat_history = []
# # #         st.rerun()


# # #     # # --- 6. EXPORT REPORT BUTTON ---
# # #     # st.markdown("---")
# # #     # st.subheader("📄 Generate Analyst Report")

# # #     # if st.session_state.data_page_chat_history:
# # #     #     # 1. Prepare the report text
# # #     #     report_text = f"FINSAGE ANALYST REPORT\n"
# # #     #     report_text += f"{'='*30}\n"
# # #     #     report_text += f"Records Analyzed: {len(df_filtered)}\n"
# # #     #     report_text += f"Selected Regions: {', '.join(regions) if regions else 'All'}\n"
# # #     #     report_text += f"Education Levels: {', '.join(education) if education else 'All'}\n"
        
# # #     #     if not df_filtered.empty:
# # #     #         report_text += f"Avg. Monthly Income: ${df_filtered['monthly_income_usd'].mean():,.2f}\n"
# # #     #         report_text += f"Avg. Credit Score: {df_filtered['credit_score'].mean():.0f}\n"
        
# # #     #     report_text += f"\n{'='*30}\n"
# # #     #     report_text += "AI ANALYSIS HISTORY:\n"
        
# # #     #     for msg in st.session_state.data_page_chat_history:
# # #     #         role = "USER" if msg["role"] == "user" else "FINSAGE"
# # #     #         report_text += f"\n[{role}]: {msg['content']}\n"

# # #     #     # 2. Add the download button
# # #     #     st.download_button(
# # #     #         label="Download Analysis as TXT",
# # #     #         data=report_text,
# # #     #         file_name="FinSage_Analyst_Report.txt",
# # #     #         mime="text/plain"
# # #     #     )
# # #     # else:
# # #     #     st.info("Chat with FinSage first to generate a report history.")

# # #     # --- 6. EXPORT REPORT BUTTON ---
# # #     st.markdown("---")
# # #     st.subheader("📄 Generate Analyst Report")

# # #     # Check if the chat history exists in session state
# # #     if "data_page_chat_history" in st.session_state and len(st.session_state.data_page_chat_history) > 0:
        
# # #         # 1. Create the report content
# # #         report_text = f"FINSAGE ANALYST REPORT\n"
# # #         report_text += f"{'='*30}\n"
# # #         report_text += f"Records Analyzed: {len(df_filtered)}\n"
# # #         report_text += f"Avg. Monthly Income: ${df_filtered['monthly_income_usd'].mean():,.2f}\n"
# # #         report_text += f"Avg. Credit Score: {df_filtered['credit_score'].mean():.0f}\n"
# # #         report_text += f"\nAI ANALYSIS HISTORY:\n"
        
# # #         for msg in st.session_state.data_page_chat_history:
# # #             role = msg["role"].upper()
# # #             report_text += f"\n[{role}]: {msg['content']}\n"

# # #         # 2. Place the Download and Clear buttons side-by-side
# # #         btn_col1, btn_col2 = st.columns(2)
# # #         with btn_col1:
# # #             st.download_button(
# # #                 label="📥 Download Analysis as TXT",
# # #                 data=report_text,
# # #                 file_name="FinSage_Report.txt",
# # #                 mime="text/plain",
# # #                 use_container_width=True
# # #             )
# # #         with btn_col2:
# # #             if st.button("🗑️ Clear Chat History", use_container_width=True):
# # #                 st.session_state.data_page_chat_history = []
# # #                 st.rerun()
# # #     else:
# # #         # This tells the user EXACTLY what to do if the button is missing
# # #         st.info("💡 The Export button will appear here once you ask FinSage a question and receive an insight.")


# import streamlit as st
# import pandas as pd
# from src.llm_interface import get_gemini_response, configure_gemini

# def show_user_data_page(df):
#     st.title("User Data & AI Analyst")
#     st.markdown("Filter the user data below and ask **FinSage** for specific insights.")
    
#     if df.empty:
#         st.warning("No data to display.")
#         return
        
#     # --- 1. Interactive Filters (Main Page) ---
#     st.subheader("Interactive Filters")
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         regions = st.multiselect("Region", options=df['region'].unique(), default=[])
    
#     with col2:
#         education = st.multiselect("Education Level", options=df['education_level'].unique(), default=[])
    
#     with col3:
#         min_score, max_score = int(df['credit_score'].min()), int(df['credit_score'].max())
#         score_range = st.slider("Credit Score Range", min_value=min_score, max_value=max_score, value=(min_score, max_score))
    
#     # --- 2. Filter Logic ---
#     df_filtered = df.copy()
#     if regions:
#         df_filtered = df_filtered[df_filtered['region'].isin(regions)]
#     if education:
#         df_filtered = df_filtered[df_filtered['education_level'].isin(education)]

#     df_filtered = df_filtered[
#         (df_filtered['credit_score'] >= score_range[0]) &
#         (df_filtered['credit_score'] <= score_range[1])
#     ]

#     # --- 3. Real-Time KPI Stats ---
#     st.markdown("---")
#     kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    
#     with kpi_col1:
#         st.metric("Users Displayed", len(df_filtered))
        
#     with kpi_col2:
#         if not df_filtered.empty:
#             avg_inc = df_filtered['monthly_income_usd'].mean()
#             st.metric("Avg. Monthly Income", f"${avg_inc:,.2f}")
            
#     with kpi_col3:
#         if not df_filtered.empty:
#             avg_cred = df_filtered['credit_score'].mean()
#             st.metric("Avg. Credit Score", f"{avg_cred:.0f}")

#     # --- 4. Data Display ---
#     st.dataframe(df_filtered.sort_values(by='record_date', ascending=False), use_container_width=True)

#     st.markdown("---") # Visual Separator before Chat

#     # --- 5. Integrated AI Chat ---
#     st.subheader("💬 Ask FinSage about this Filtered View")
#     configure_gemini()

#     if "data_page_chat_history" not in st.session_state:
#         st.session_state.data_page_chat_history = []

#     # Display Chat History
#     for message in st.session_state.data_page_chat_history:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     # Chat Input Box
#     user_query = st.chat_input("Ex: What is the average income for this specific filtered group?")

#     if user_query:
#         st.session_state.data_page_chat_history.append({"role": "user", "content": user_query})
#         with st.chat_message("user"):
#             st.markdown(user_query)
            
#         with st.spinner("FinSage is analyzing..."):
#             response = get_gemini_response(user_query, df_filtered)
            
#         st.session_state.data_page_chat_history.append({"role": "assistant", "content": response})
#         st.rerun()

#     # --- 6. EXPORT REPORT BUTTON ---
#     # This stays outside the 'if user_query' block so it appears whenever history exists
#     if st.session_state.data_page_chat_history:
#         st.markdown("---")
#         st.subheader("📄 Generate Analyst Report")
        
#         # Prepare the report text
#         report_text = f"FINSAGE ANALYST REPORT\n{'='*30}\n"
#         report_text += f"Records Analyzed: {len(df_filtered)}\n"
#         if not df_filtered.empty:
#             report_text += f"Avg. Monthly Income: ${df_filtered['monthly_income_usd'].mean():,.2f}\n"
#         report_text += f"\nAI ANALYSIS HISTORY:\n"
        
#         for msg in st.session_state.data_page_chat_history:
#             role = msg["role"].upper()
#             report_text += f"\n[{role}]: {msg['content']}\n"

#         btn_col1, btn_col2 = st.columns(2)
#         with btn_col1:
#             st.download_button(
#                 label="📥 Download Analysis as TXT",
#                 data=report_text,
#                 file_name="FinSage_Report.txt",
#                 mime="text/plain",
#                 use_container_width=True
#             )
#         with btn_col2:
#             if st.button("🗑️ Clear Chat History", use_container_width=True):
#                 st.session_state.data_page_chat_history = []
#                 st.rerun()
#     else:
#         st.info("💡 The Export button will appear here once you ask FinSage a question.")


# # import streamlit as st
# # import pandas as pd
# # from src.llm_interface import get_gemini_response, configure_gemini

# # def show_user_data_page(df):
# #     st.title("User Data & AI Analyst")
    
# #     if df.empty:
# #         st.warning("No data to display.")
# #         return
        
# #     # --- 1. Filters ---
# #     st.subheader("Interactive Filters")
# #     col1, col2, col3 = st.columns(3)
# #     with col1:
# #         regions = st.multiselect("Region", options=df['region'].unique(), default=[])
# #     with col2:
# #         education = st.multiselect("Education Level", options=df['education_level'].unique(), default=[])
# #     with col3:
# #         min_score, max_score = int(df['credit_score'].min()), int(df['credit_score'].max())
# #         score_range = st.slider("Credit Score Range", min_value=min_score, max_value=max_score, value=(min_score, max_score))
    
# #     # --- 2. Filter Logic ---
# #     df_filtered = df.copy()
# #     if regions:
# #         df_filtered = df_filtered[df_filtered['region'].isin(regions)]
# #     if education:
# #         df_filtered = df_filtered[df_filtered['education_level'].isin(education)]
# #     df_filtered = df_filtered[(df_filtered['credit_score'] >= score_range[0]) & (df_filtered['credit_score'] <= score_range[1])]

# #     # --- 3. KPI Metrics ---
# #     st.markdown("---")
# #     k1, k2, k3 = st.columns(3)
# #     k1.metric("Selected Records", len(df_filtered))
# #     if not df_filtered.empty:
# #         k2.metric("Avg. Income", f"${df_filtered['monthly_income_usd'].mean():,.2f}")
# #         k3.metric("Avg. Credit Score", f"{df_filtered['credit_score'].mean():.0f}")

# #     # --- 4. Data Table ---
# #     st.dataframe(df_filtered.sort_values(by='record_date', ascending=False), use_container_width=True)

# #     st.markdown("---")
# #     st.subheader("💬 FinSage AI Chat")
# #     configure_gemini()

# #     # Initialize history
# #     if "data_page_chat_history" not in st.session_state:
# #         st.session_state.data_page_chat_history = []

# #     # --- 5. EXPORT BUTTON (Moved UP for visibility) ---
# #     if len(st.session_state.data_page_chat_history) > 0:
# #         # Create Report String
# #         report_text = f"FINSAGE REPORT\nRecords: {len(df_filtered)}\n"
# #         for msg in st.session_state.data_page_chat_history:
# #             report_text += f"\n[{msg['role'].upper()}]: {msg['content']}\n"
        
# #         # Display buttons in a row
# #         c1, c2 = st.columns(2)
# #         with c1:
# #             st.download_button("📥 Download Report", data=report_text, file_name="FinSage_Report.txt", use_container_width=True)
# #         with c2:
# #             if st.button("🗑️ Clear Chat", use_container_width=True):
# #                 st.session_state.data_page_chat_history = []
# #                 st.rerun()
# #     else:
# #         st.caption("The Download button will appear here once you start chatting.")

# #     # --- 6. Chat Interface ---
# #     for message in st.session_state.data_page_chat_history:
# #         with st.chat_message(message["role"]):
# #             st.markdown(message["content"])

# #     user_query = st.chat_input("Ask FinSage about the data above...")

# #     if user_query:
# #         st.session_state.data_page_chat_history.append({"role": "user", "content": user_query})
# #         # Generate response
# #         response = get_gemini_response(user_query, df_filtered)
# #         st.session_state.data_page_chat_history.append({"role": "assistant", "content": response})
# #         st.rerun() # Forces the Export button to appear immediately


import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from src.llm_interface import get_gemini_response, configure_gemini

def show_user_data_page(df):
    st.title("User Data & AI Analyst")
    st.markdown("Filter the user data below and consult with **FinSage** for specific insights.")
    
    if df.empty:
        st.warning("No data to display.")
        return
        
    # --- 1. Interactive Filters ---
    st.subheader("Interactive Filters")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        regions = st.multiselect("Region", options=df['region'].unique(), default=[])
    with col2:
        education = st.multiselect("Education Level", options=df['education_level'].unique(), default=[])
    with col3:
        min_score, max_score = int(df['credit_score'].min()), int(df['credit_score'].max())
        score_range = st.slider("Credit Score Range", min_value=min_score, max_value=max_score, value=(min_score, max_score))
    
    # --- 2. Filter Logic ---
    df_filtered = df.copy()
    if regions:
        df_filtered = df_filtered[df_filtered['region'].isin(regions)]
    if education:
        df_filtered = df_filtered[df_filtered['education_level'].isin(education)]
    df_filtered = df_filtered[(df_filtered['credit_score'] >= score_range[0]) & (df_filtered['credit_score'] <= score_range[1])]

    # --- 3. Real-Time KPI Stats ---
    st.markdown("---")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Selected Records", len(df_filtered))
    if not df_filtered.empty:
        kpi2.metric("Avg. Monthly Income", f"${df_filtered['monthly_income_usd'].mean():,.2f}")
        kpi3.metric("Avg. Credit Score", f"{df_filtered['credit_score'].mean():.0f}")

    # --- 4. Data Table ---
    st.dataframe(df_filtered.sort_values(by='record_date', ascending=False), use_container_width=True)

    st.markdown("---")

    # --- 5. Integrated AI Chat ---
    st.subheader("💬 Ask FinSage about this Filtered View")
    configure_gemini()

    if "data_page_chat_history" not in st.session_state:
        st.session_state.data_page_chat_history = []

    # Display Chat History
    for message in st.session_state.data_page_chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input Box
    user_query = st.chat_input("Ask FinSage about the data above...")

    if user_query:
        st.session_state.data_page_chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)
            
        with st.spinner("FinSage is analyzing..."):
            response = get_gemini_response(user_query, df_filtered)
            
        st.session_state.data_page_chat_history.append({"role": "assistant", "content": response})
        st.rerun()

    # --- 6. EXPORT REPORT SECTION (PDF) ---
    if st.session_state.data_page_chat_history:
        st.markdown("---")
        st.subheader("📄 Generate Analyst Report")

        def create_pdf(history, stats):
            pdf = FPDF()
            pdf.add_page()
            
            # Header
            pdf.set_font("Arial", "B", 20)
            pdf.cell(0, 10, "FinSage Analyst Report", ln=True, align="C")
            pdf.set_font("Arial", "I", 10)
            pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align="C")
            pdf.ln(10)

            # Stats Section
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Dataset Summary (Filtered Context):", ln=True)
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 10, f"- Total Records: {stats['count']}", ln=True)
            pdf.cell(0, 10, f"- Avg Income: ${stats['income']:,.2f}", ln=True)
            pdf.cell(0, 10, f"- Avg Credit Score: {stats['credit']:.0f}", ln=True)
            pdf.ln(10)

            # Chat Logs
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Financial Analysis Logs:", ln=True)
            pdf.set_font("Arial", "", 11)
            for msg in history:
                role = "USER" if msg["role"] == "user" else "FINSAGE AI"
                pdf.set_font("Arial", "B", 11)
                pdf.multi_cell(0, 10, f"{role}:")
                pdf.set_font("Arial", "", 11)
                pdf.multi_cell(0, 7, msg["content"].encode('latin-1', 'replace').decode('latin-1'))
                pdf.ln(5)
            
            return pdf.output(dest="S").encode("latin-1")

        # Prepare context data
        current_stats = {
            "count": len(df_filtered),
            "income": df_filtered['monthly_income_usd'].mean() if not df_filtered.empty else 0,
            "credit": df_filtered['credit_score'].mean() if not df_filtered.empty else 0
        }

        # PDF and Clear Buttons
        pdf_bytes = create_pdf(st.session_state.data_page_chat_history, current_stats)
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            st.download_button(
                label="📥 Download Analyst Report (PDF)",
                data=pdf_bytes,
                file_name=f"FinSage_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        with btn_col2:
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state.data_page_chat_history = []
                st.rerun()
    else:
        st.info("💡 The Export button will appear here once you've started a chat session.")