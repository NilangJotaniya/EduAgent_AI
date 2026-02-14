from utils.vectorstore import search_docs

def retrieve_info(user_input):
    docs = search_docs(user_input)
    return docs
