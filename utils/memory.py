chat_history = []

def add_to_memory(user, ai):
    chat_history.append({
        "user": user,
        "ai": ai
    })

def get_memory():
    history_text = ""
    for chat in chat_history[-5:]:
        history_text += f"User: {chat['user']}\nAI: {chat['ai']}\n"
    return history_text
