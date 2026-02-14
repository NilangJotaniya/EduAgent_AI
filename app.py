import streamlit as st

from agents.query_agent import understand_query
from agents.retrieval_agent import retrieve_info
from agents.response_agent import generate_answer
from agents.escalation_agent import check_escalation
from utils.vectorstore import add_documents

st.title("🎓 EduAgent AI – Multi-Agent Assistant")

# Load knowledge base once
add_documents()

user_input = st.text_input("Ask your academic question:")

if st.button("Send"):

    if user_input:

        category = understand_query(user_input)

        context = retrieve_info(user_input)

        answer = generate_answer(user_input, context)

        escalate = check_escalation(answer)

        st.write("📌 Category:", category)
        st.write("🤖 EduAgent AI:", answer)

        if escalate:
            st.warning("⚠️ Escalation Needed: Contact Admin")
