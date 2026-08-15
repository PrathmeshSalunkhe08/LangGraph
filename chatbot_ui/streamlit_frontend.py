import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

# Step 1: Thread configuration for LangGraph state memory
CONFIG = {'configurable': {'thread_id': 'thread-1'}}

# Step 2: Initialize message history list in Streamlit session_state
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# Step 3: Display previous conversation history from session_state
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

# Example of stored message dictionary structure:
# {'role': 'user', 'content': 'Hi'}
# {'role': 'assistant', 'content': 'Hello'}

# Step 4: Create chat input widget at bottom of the page
user_input = st.chat_input('Type here')

# Step 5: Process user message & stream response
if user_input:

    # A. Append user query to session state & display immediately on screen
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # B. Stream assistant response tokens in real-time from LangGraph using chatbot.stream
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config={'configurable': {'thread_id': 'thread-1'}},
                stream_mode='messages'
            )
        )

    # C. Save final streamed assistant message to session_state message_history
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
