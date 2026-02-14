from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["eduagent"]
chat_collection = db["chat_memory"]

def save_chat(user, ai):

    chat_collection.insert_one({
        "user": user,
        "ai": ai
    })
