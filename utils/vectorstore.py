import chromadb

client = chromadb.Client()

collection = client.get_or_create_collection("eduagent_docs")

def add_documents():

    docs = [
        "Exam schedule will be released in May.",
        "Fee payment deadline is March 10.",
        "Minimum attendance required is 75%.",
        "Scholarship forms open in June."
    ]

    for i, doc in enumerate(docs):
        collection.add(documents=[doc], ids=[str(i)])

def search_docs(query):
    results = collection.query(query_texts=[query], n_results=2)
    return results["documents"][0]
