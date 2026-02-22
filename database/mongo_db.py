import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

_client = None
_db = None


def get_database():
    """
    Get the MongoDB database connection.
    Uses a single shared connection (singleton pattern) for efficiency.

    Returns:
        pymongo Database object

    Raises:
        Exception if MONGO_URI is not set in .env
    """
    global _client, _db

    if _db is not None:
        return _db

    try:
        from pymongo import MongoClient
        from pymongo.server_api import ServerApi

        # Read the connection string from .env file
        mongo_uri = os.getenv("MONGO_URI")

        if not mongo_uri:
            raise ValueError(
                "MONGO_URI not found in .env file!\n"
                "Add this line to your .env:\n"
                "mongodb+srv://username:password@eduagent.0xt78mo.mongodb.net/"
            )

        _client = MongoClient(mongo_uri, server_api=ServerApi('1'))

        _client.admin.command('ping')
        print("✅ Connected to MongoDB Atlas successfully!")

        db_name = os.getenv("MONGO_DB_NAME", "eduagent_db")
        _db = _client[db_name]

        return _db

    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        raise


def close_connection():
    """Close the MongoDB connection cleanly."""
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None
        print("MongoDB connection closed.")


# ============================================================
# FAQ OPERATIONS
# ============================================================

def get_all_faqs(category: str = None) -> list:
    """
    Fetch all FAQs, optionally filtered by category.

    In MongoDB, documents are Python dictionaries.
    The _id field is a MongoDB ObjectId — we convert it to string.

    Parameters:
        category (str): Optional filter e.g. "Exam", "Fees"

    Returns:
        list of FAQ dicts
    """
    db = get_database()
    query = {}
    if category and category != "All":
        # Case-insensitive search using regex
        import re
        query["category"] = {"$regex": f"^{category}$", "$options": "i"}

    faqs = list(db.faqs.find(query))

    # Convert ObjectId to string so it can be used in forms
    for faq in faqs:
        faq["_id"] = str(faq["_id"])

    return faqs


def search_faqs(query_text: str, category: str) -> list:
    """
    Search FAQs by text matching in question, answer, keywords.

    Uses MongoDB's $or operator to search across multiple fields.
    $regex does case-insensitive partial text matching.

    Parameters:
        query_text (str): Text to search for
        category   (str): Category to prioritize in search

    Returns:
        list of up to 3 matching FAQ dicts
    """
    db = get_database()
    import re

    # Build a case-insensitive regex pattern
    pattern = re.compile(query_text, re.IGNORECASE)

    # Search in multiple fields using $or
    results = list(db.faqs.find(
        {
            "$or": [
                {"question": {"$regex": pattern}},
                {"answer":   {"$regex": pattern}},
                {"keywords": {"$regex": pattern}},
                {"category": {"$regex": re.compile(category, re.IGNORECASE)}}
            ]
        }
    ).limit(3))

    for r in results:
        r["_id"] = str(r["_id"])

    return results


def add_faq(category: str, question: str, answer: str, keywords: str) -> bool:
    """
    Insert a new FAQ document into the faqs collection.

    Parameters:
        category (str): e.g. "Exam", "Fees"
        question (str): The question text
        answer   (str): The answer text
        keywords (str): Comma-separated keywords

    Returns:
        True if inserted, False if error
    """
    db = get_database()
    try:
        db.faqs.insert_one({
            "category":   category,
            "question":   question,
            "answer":     answer,
            "keywords":   keywords,
            "created_at": datetime.now().isoformat()
        })
        return True
    except Exception as e:
        print(f"❌ Error adding FAQ: {e}")
        return False


def update_faq(faq_id: str, answer: str, keywords: str) -> bool:
    """
    Update an existing FAQ's answer and keywords.

    Uses $set to update only specific fields (not replace entire document).
    """
    from bson import ObjectId
    db = get_database()
    try:
        db.faqs.update_one(
            {"_id": ObjectId(faq_id)},
            {"$set": {"answer": answer, "keywords": keywords}}
        )
        return True
    except Exception as e:
        print(f"❌ Error updating FAQ: {e}")
        return False


def delete_faq(faq_id: str) -> bool:
    """Delete a FAQ document by its MongoDB _id."""
    from bson import ObjectId
    db = get_database()
    try:
        db.faqs.delete_one({"_id": ObjectId(faq_id)})
        return True
    except Exception as e:
        print(f"❌ Error deleting FAQ: {e}")
        return False


# ============================================================
# EXAM SCHEDULE OPERATIONS
# ============================================================

def get_all_exams() -> list:
    """Fetch all exam schedule entries sorted by date."""
    db = get_database()
    exams = list(db.exam_schedules.find().sort("exam_date", 1))
    for e in exams:
        e["_id"] = str(e["_id"])
    return exams


def add_exam(subject: str, exam_date: str, exam_time: str,
             venue: str, semester: int) -> bool:
    """Insert a new exam schedule entry."""
    db = get_database()
    try:
        db.exam_schedules.insert_one({
            "subject":   subject,
            "exam_date": exam_date,
            "exam_time": exam_time,
            "venue":     venue,
            "semester":  semester
        })
        return True
    except Exception as e:
        print(f"❌ Error adding exam: {e}")
        return False


def delete_exam(exam_id: str) -> bool:
    """Delete an exam entry by MongoDB _id."""
    from bson import ObjectId
    db = get_database()
    try:
        db.exam_schedules.delete_one({"_id": ObjectId(exam_id)})
        return True
    except Exception as e:
        print(f"❌ Error deleting exam: {e}")
        return False


# ============================================================
# FEE STRUCTURE OPERATIONS
# ============================================================

def get_all_fees() -> list:
    """Fetch all fee structure entries."""
    db = get_database()
    fees = list(db.fee_structure.find())
    for f in fees:
        f["_id"] = str(f["_id"])
    return fees


def add_fee(fee_type: str, amount: float,
            due_date: str, description: str) -> bool:
    """Insert a new fee entry."""
    db = get_database()
    try:
        db.fee_structure.insert_one({
            "fee_type":    fee_type,
            "amount":      amount,
            "due_date":    due_date,
            "description": description
        })
        return True
    except Exception as e:
        print(f"❌ Error adding fee: {e}")
        return False


def delete_fee(fee_id: str) -> bool:
    """Delete a fee entry by MongoDB _id."""
    from bson import ObjectId
    db = get_database()
    try:
        db.fee_structure.delete_one({"_id": ObjectId(fee_id)})
        return True
    except Exception as e:
        print(f"❌ Error deleting fee: {e}")
        return False


# ============================================================
# ESCALATED QUERIES OPERATIONS
# ============================================================

def save_escalated_query(student_query: str, reason: str) -> bool:
    """
    Save a flagged query to MongoDB for admin review.

    Called by the EscalationAgent when a sensitive query is detected.
    """
    db = get_database()
    try:
        db.escalated_queries.insert_one({
            "student_query": student_query,
            "reason":        reason,
            "timestamp":     datetime.now().isoformat(),
            "status":        "pending",
            "admin_notes":   ""
        })
        print("⚠️  Escalated query saved to MongoDB")
        return True
    except Exception as e:
        print(f"❌ Error saving escalated query: {e}")
        return False


def get_escalated_queries(status_filter: str = "all") -> list:
    """
    Fetch escalated queries, optionally filtered by status.

    Parameters:
        status_filter: "all", "pending", "in-progress", or "resolved"
    """
    db = get_database()
    query = {} if status_filter == "all" else {"status": status_filter}
    results = list(db.escalated_queries.find(query).sort("timestamp", -1))
    for r in results:
        r["_id"] = str(r["_id"])
    return results


def update_escalated_query(query_id: str, status: str,
                           admin_notes: str) -> bool:
    """Update the status and admin notes of an escalated query."""
    from bson import ObjectId
    db = get_database()
    try:
        db.escalated_queries.update_one(
            {"_id": ObjectId(query_id)},
            {"$set": {"status": status, "admin_notes": admin_notes}}
        )
        return True
    except Exception as e:
        print(f"❌ Error updating escalated query: {e}")
        return False


# ============================================================
# UPLOADED PDFs TRACKING
# ============================================================

def record_uploaded_pdf(filename: str, pages: int, chunks: int) -> bool:
    """Record a successfully processed PDF in MongoDB."""
    db = get_database()
    try:
        db.uploaded_pdfs.insert_one({
            "filename":      filename,
            "original_name": filename,
            "pages":         pages,
            "chunks":        chunks,
            "uploaded_at":   datetime.now().isoformat(),
            "uploaded_by":   "admin"
        })
        return True
    except Exception as e:
        print(f"❌ Error recording PDF: {e}")
        return False


def get_all_uploaded_pdfs() -> list:
    """Fetch all uploaded PDF records."""
    db = get_database()
    pdfs = list(db.uploaded_pdfs.find().sort("uploaded_at", -1))
    for p in pdfs:
        p["_id"] = str(p["_id"])
    return pdfs


def delete_uploaded_pdf_record(pdf_id: str) -> bool:
    """Delete a PDF record from MongoDB."""
    from bson import ObjectId
    db = get_database()
    try:
        db.uploaded_pdfs.delete_one({"_id": ObjectId(pdf_id)})
        return True
    except Exception as e:
        print(f"❌ Error deleting PDF record: {e}")
        return False


# ============================================================
# STATISTICS
# ============================================================

def get_statistics() -> dict:
    """
    Get count statistics for the admin dashboard.
    Uses MongoDB's count_documents() method.
    """
    db = get_database()
    try:
        return {
            "total_faqs":       db.faqs.count_documents({}),
            "total_escalated":  db.escalated_queries.count_documents({}),
            "pending_escalated":db.escalated_queries.count_documents(
                                    {"status": "pending"}),
            "uploaded_pdfs":    db.uploaded_pdfs.count_documents({}),
            "exam_entries":     db.exam_schedules.count_documents({}),
            "fee_entries":      db.fee_structure.count_documents({})
        }
    except Exception as e:
        print(f"❌ Error fetching stats: {e}")
        return {k: 0 for k in ["total_faqs", "total_escalated",
                                "pending_escalated", "uploaded_pdfs",

                                "exam_entries", "fee_entries"]}
