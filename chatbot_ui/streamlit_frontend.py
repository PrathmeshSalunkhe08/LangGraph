import streamlit as st
from langchain_core.messages import HumanMessage
from langgraph_backend import workflow
import time

# 1. Page Title
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot")

# 2. Initialize Session State for Messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]

# 3. Display Chat Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 4. Chat Input & Streaming Response
user_input = st.chat_input("Type your message...")

if user_input:
    # Display and record user message
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Stream response from LangGraph backend
    def stream_ai_response():
        config = {"configurable": {"thread_id": "default_thread"}}
        for chunk, metadata in workflow.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
            stream_mode="messages"
        ):
            if chunk.content:
                yield chunk.content
                time.sleep(0.02)

    with st.chat_message("assistant"):
        ai_reply = st.write_stream(stream_ai_response)

    # Record assistant message
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})





