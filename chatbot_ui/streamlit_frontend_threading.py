import streamlit as st
import uuid
import time
from langchain_core.messages import HumanMessage
from langgraph_backend import workflow

# 1. Page Title
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot")

# 2. Initialize Session State for Multi-Thread Chats
if "chats" not in st.session_state:
    initial_thread = "thread_1"
    st.session_state.chats = {
        initial_thread: {
            "name": "Chat 1",
            "messages": [{"role": "assistant", "content": "Hello! How can I help you today?"}]
        }
    }
    st.session_state.current_thread_id = initial_thread

# 3. Sidebar: New Chat & Chat Thread Selection
with st.sidebar:
    st.title("💬 Chat Threads")
    
    # 'New Chat' Button
    if st.button("➕ New Chat", use_container_width=True):
        new_thread_id = f"thread_{uuid.uuid4().hex[:6]}"
        chat_count = len(st.session_state.chats) + 1
        st.session_state.chats[new_thread_id] = {
            "name": f"Chat {chat_count}",
            "messages": [{"role": "assistant", "content": "Hello! How can I help you today?"}]
        }
        st.session_state.current_thread_id = new_thread_id
        st.rerun()
    
    st.divider()
    st.subheader("Previous Chats")
    
    # Render all chat threads as selectable buttons
    for thread_id, chat_data in list(st.session_state.chats.items()):
        is_active = (thread_id == st.session_state.current_thread_id)
        button_label = f"💬 {chat_data['name']}" + (" (Active)" if is_active else "")
        if st.button(button_label, key=thread_id, use_container_width=True):
            st.session_state.current_thread_id = thread_id
            st.rerun()

current_thread_id = st.session_state.current_thread_id
active_chat = st.session_state.chats[current_thread_id]

# 4. Display Chat Messages for Active Thread
for msg in active_chat["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. Chat Input & Streaming Response
user_input = st.chat_input("Type your message...")

if user_input:
    # Display user message on screen & save to active thread history
    with st.chat_message("user"):
        st.write(user_input)
    active_chat["messages"].append({"role": "user", "content": user_input})

    # Update thread name based on first message
    user_msgs = [m for m in active_chat["messages"] if m["role"] == "user"]
    if len(user_msgs) == 1:
        short_title = user_input[:20] + "..." if len(user_input) > 20 else user_input
        active_chat["name"] = short_title

    # Stream AI response using the active thread_id for LangGraph memory
    def stream_ai_response():
        config = {"configurable": {"thread_id": current_thread_id}}
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

    # Save assistant message to active thread history
    active_chat["messages"].append({"role": "assistant", "content": ai_reply})






