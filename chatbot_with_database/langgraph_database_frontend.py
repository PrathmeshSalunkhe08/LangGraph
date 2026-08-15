import streamlit as st
from langgraph_database_backend import chatbot,retrive_all_threads
from langchain_core.messages import HumanMessage, AIMessage
import uuid

# **************************************** Utility Functions *************************

# Generates a new random unique thread ID (UUID v4) for isolated conversation sessions
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

# Resets current chat session: creates a new thread_id, adds it to threads list, and clears message history
def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

# Adds a new thread_id to session state chat_threads list if not already present
def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

# Loads state snapshot from LangGraph checkpointer for a specific thread_id
def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    # Check if messages key exists in state values, return empty list if not
    return state.values.get('messages', [])


# **************************************** Session Setup ******************************

# Initialize message_history list in session_state if not present
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# Initialize thread_id in session_state if not present
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

# Initialize list of all chat_threads in session_state if not present
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrive_all_threads()
# Ensure the active thread_id is recorded in chat_threads
add_thread(st.session_state['thread_id'])


# **************************************** Sidebar UI *********************************

st.sidebar.title('LangGraph Chatbot')

# 'New Chat' button: triggers reset_chat() to start a fresh thread session
if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

# Display previous conversation threads in reverse order (newest on top)
for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []

        # Convert LangGraph Message objects to simple dictionary format for Streamlit
        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            temp_messages.append({'role': role, 'content': msg.content})

        st.session_state['message_history'] = temp_messages


# **************************************** Main UI ************************************

# Loading and displaying the current thread's conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

# Chat input bar at bottom of the page
user_input = st.chat_input('Type here')

if user_input:

    # 1. Add user message to history & render on screen
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # 2. Config object linking LangGraph memory to the current thread_id
    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

    # 3. Stream AI response tokens from LangGraph backend in real-time
    with st.chat_message("assistant"):
        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages"
            ):
                if isinstance(message_chunk, AIMessage):
                    # Yield only assistant response tokens
                    yield message_chunk.content

        ai_message = st.write_stream(ai_only_stream())

    # 4. Save AI assistant response to session_state message_history
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
