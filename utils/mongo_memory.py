from pymongo import MongoClient

client = MongoClient("mongodb+srv://<admin>:<password>@eduagent.0xt78mo.mongodb.net/?appName=eduagent")
db = client["eduagent"]
chat_collection = db["chat_memory"]

def save_chat(user, ai):

    chat_collection.insert_one({
        "user": user,
        "ai": ai
    })

