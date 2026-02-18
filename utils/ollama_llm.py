import streamlit as st
from langchain_community.llms import Ollama

@st.cache_resource
def load_llm():
    return Ollama(model="phi3:mini")

llm = load_llm()

def ask_llm(prompt):
    response = ""
    for chunk in llm.stream(prompt):
        response += chunk
        yield response
