import streamlit as st
from src.llm_interface import get_gemini_response, configure_gemini

def show_ai_chat_page(df):
    st.title("FinSage AI Chat 💬")
    st.markdown("Ask questions about your financial summary.")
    
    # Ensure Gemini is configured
    configure_gemini()
    
    # --- NEW: Clear Chat Button in Sidebar ---
    st.sidebar.markdown("---") # Visual separator
    if st.sidebar.button("Clear Chat History"):
        # Reset the messages to the initial welcome message
        st.session_state.messages = [{
            "role": "assistant", 
            "content": "Hello! I'm FinSage. How can I help you understand your financial summary today?"
        }]
        st.rerun() # Rerun to show the cleared chat

    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant", 
            "content": "Hello! I'm FinSage. How can I help you understand your financial summary today?"
        }]

    # --- NEW: Suggested Questions in an Expander ---
    # This guides the user to questions your simple bot can answer
    with st.expander("Click for suggested questions..."):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("What's the average income?"):
                st.session_state.messages.append({"role": "user", "content": "What's the average income?"})
                st.rerun() # Rerun to trigger the AI response

        with col2:
            if st.button("What's the average credit score?"):
                st.session_state.messages.append({"role": "user", "content": "What's the average credit score?"})
                st.rerun()
                
        with col3:
            if st.button("How many users have a loan?"):
                st.session_state.messages.append({"role": "user", "content": "How many users have a loan?"})
                st.rerun()
    st.markdown("---")

    # --- UPDATED: Chat Display with Avatars ---
    # Display all messages in history
    for message in st.session_state.messages:
        with st.chat_message(message["role"], 
                             avatar="🤖" if message["role"] == "assistant" else "🧑‍💻"):
            st.markdown(message["content"])

    # --- UPDATED: Chat Logic (Event-Based) ---
    
    # First, check if a new prompt was entered in the chat box
    if prompt := st.chat_input("Ask about avg. income, expense, savings, etc."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun() # Rerun to display the user's message

    # Now, check if the *last* message was from the user (from button or chat box)
    # If it was, the assistant needs to reply
    if st.session_state.messages[-1]["role"] == "user":
        # Get the last user message
        user_question = st.session_state.messages[-1]["content"]
        
        # Display the assistant's response in real-time
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Analyzing..."):
                response = get_gemini_response(user_question, df)
                st.markdown(response)
                
        # Add the AI's response to the history
        st.session_state.messages.append({"role": "assistant", "content": response})