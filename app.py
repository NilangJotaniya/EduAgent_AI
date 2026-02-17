# ✅ Auto start Ollama first
from utils.ollama_manager import start_ollama
start_ollama()

import streamlit as st

from agents.retrieval_agent import retrieve_info
from agents.response_agent import generate_answer
from utils.memory import add_to_memory
from utils.mongo_memory import save_chat
from utils.vectorstore import add_documents


# --------------------------------
# 🎨 Streamlit Page Setup
# --------------------------------
st.set_page_config(page_title="EduAgent AI", layout="wide")

st.title("🎓 EduAgent AI – Academic Assistant")


# --------------------------------
# 🧠 Load Knowledge Base Once
# --------------------------------
add_documents()


# --------------------------------
# 💬 Chat History State
# --------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------
# 💬 Show Old Messages (ChatGPT Style)
# --------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# --------------------------------
# 💬 Chat Input Box (NEW UI)
# --------------------------------
if prompt := st.chat_input("Ask your academic question..."):

    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # --------------------------------
    # 🤖 AI PROCESSING
    # --------------------------------
    context = retrieve_info(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        # Generate Answer
        answer = generate_answer(prompt, context)

        # Typing effect
        full_response = ""
        for word in answer.split():
            full_response += word + " "
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Save memory
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    add_to_memory(prompt, full_response)
    save_chat(prompt, full_response)
