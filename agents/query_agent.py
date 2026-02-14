from utils.ollama_llm import ask_llm

def understand_query(user_input):

    prompt = f"""
    Classify this student query into ONE category:
    exams, fees, attendance, scholarship, general

    Query: {user_input}

    Return only category name.
    """

    category = ask_llm(prompt)
    return category.strip()
