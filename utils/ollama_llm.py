from langchain_community.llms import Ollama

# This connects to your LOCAL AI
llm = Ollama(model="llama3.1")

def ask_llm(prompt):
    response = llm.invoke(prompt)
    return response
