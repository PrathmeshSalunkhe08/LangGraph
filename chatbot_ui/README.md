# LangGraph Streamlit Chatbot

A simple, interactive chatbot UI built using **Streamlit** and powered by **LangGraph** with Groq LLM (`llama-3.1-8b-instant`).

## Features
- 💬 **Interactive Chat Interface**: Native Streamlit `st.chat_message` and `st.chat_input`.
- 🧠 **LangGraph Memory Persistence**: State checkpointing using `InMemorySaver` with configurable Thread IDs.
- ⚙️ **Sidebar Controls**: Easy thread switching, session info, and clear chat history button.
- 🔑 **Graceful Error Handling**: Helpful UI banners for missing API keys or backend load issues.

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install streamlit langgraph langchain-groq python-dotenv
   ```

2. **Configure API Key**:
   Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. **Run the Streamlit App**:
   ```bash
   streamlit run streamlit_frontend.py
   ```
