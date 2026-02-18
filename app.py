import streamlit as st

from utils.ollama_manager import start_ollama
from agents.query_agent import understand_query
from agents.retrieval_agent import retrieve_info
from agents.response_agent import generate_answer
from utils.memory import add_to_memory
from utils.mongo_memory import save_chat
from utils.vectorstore import add_documents

# Auto start Ollama
start_ollama()

st.set_page_config(page_title="EduAgent AI")

# ----------- PRO UI STYLING -----------
st.markdown("""
<style>
.big-title {
    font-size:48px;
    font-weight:700;
    background: linear-gradient(90deg,#6366f1,#ec4899);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.chat-bubble-user {
    background:#1e293b;
    padding:12px;
    border-radius:10px;
    margin:5px;
}

.chat-bubble-ai {
    background:#312e81;
    padding:12px;
    border-radius:10px;
    margin:5px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">🎓 EduAgent AI</div>', unsafe_allow_html=True)
st.write("Your Intelligent Academic Assistant powered by Local AI.")

# Load knowledge base
add_documents()

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- CHAT HISTORY ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# ---------- CHAT INPUT ----------
user_input = st.chat_input("Ask about exams, fees, attendance...")

if user_input:

    # Show user message immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Retrieval
    category = understand_query(user_input)
    context = retrieve_info(user_input)

    # Create assistant container
    assistant_container = st.chat_message("assistant")
    message_placeholder = assistant_container.empty()

    full_answer = ""

    # STREAM RESPONSE
    response_stream = generate_answer(user_input, context)

    for partial in response_stream:
        full_answer = partial
        message_placeholder.write(full_answer)

    # Save memory
    add_to_memory(user_input, full_answer)
    save_chat(user_input, full_answer)

    # Append assistant message AFTER streaming
    st.session_state.messages.append(
        {"role": "assistant", "content": full_answer}
    )
