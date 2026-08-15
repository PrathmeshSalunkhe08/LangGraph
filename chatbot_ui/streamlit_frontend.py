import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

# Step 1: Define thread configuration for LangGraph state persistence memory
# MemorySaver checkpointer uses thread_id to track conversation history per session
CONFIG = {'configurable': {'thread_id': 'thread-1'}}

# Step 2: Initialize message history list in Streamlit session_state
# session_state persists across Streamlit script reruns
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# Step 3: Display previous conversation history from session_state
# Loops through stored messages and renders user and assistant chat bubbles
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

# Example of message dict structure saved in history:
# {'role': 'user', 'content': 'Hi'}
# {'role': 'assistant', 'content': 'Hello! How can I help you?'}

# Step 4: Create chat input widget at bottom of the page
user_input = st.chat_input('Type here')

# Step 5: Handle user message submission
if user_input:

    # A. Append user query to session state & display immediately on screen
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # B. Invoke LangGraph compiled graph (chatbot) with current query & thread_id config
    response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)
    
    # C. Extract final response message content from LLM
    ai_message = response['messages'][-1].content
    
    # D. Append assistant response to session state & display on screen
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)
