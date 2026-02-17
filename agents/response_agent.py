from utils.ollama_llm import ask_llm
from utils.memory import get_memory

def generate_answer(user_input, context):

    memory = get_memory()

    prompt = f"""
    You are EduAgent AI, a fast academic assistant.

    Conversation History:
    {memory}

    Academic Knowledge:
    {context}

    Answer clearly and briefly.

    Question: {user_input}
    """

    return ask_llm(prompt)
