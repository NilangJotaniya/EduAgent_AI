from utils.ollama_llm import ask_llm

def generate_answer(user_input, context):

    prompt = f"""
    You are EduAgent AI.

    Use this academic information:
    {context}

    Answer the student question clearly.

    Question: {user_input}
    """

    response = ask_llm(prompt)
    return response
