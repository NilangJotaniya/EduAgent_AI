import os
import re

PDF_STORAGE_DIR = "uploaded_pdfs"

KEYWORD_SYNONYMS = {
    "timetable":   ["timetable", "time_table", "schedule", "exam_schedule", "exam_time"],
    "schedule":    ["schedule", "timetable", "time_table", "exam_schedule"],
    "exam":        ["exam", "examination", "test", "timetable", "schedule"],
    "fee":         ["fee", "fees", "fee_structure", "charges", "payment"],
    "syllabus":    ["syllabus", "curriculum", "course"],
    "handbook":    ["handbook", "manual", "guide", "rulebook", "rules"],
    "admission":   ["admission", "prospectus", "enrollment"],
    "scholarship": ["scholarship", "financial_aid", "stipend"],
    "attendance":  ["attendance", "attendance_policy"],
    "library":     ["library", "library_rules"],
    "hostel":      ["hostel", "dormitory", "hostel_rules"],
    "calendar":    ["calendar", "academic_calendar", "planner"],
    "result":      ["result", "results", "marksheet", "grades"],
    "holiday":     ["holiday", "holidays", "vacation"],
    "form":        ["form", "application", "template"],
}


def _normalize(text: str) -> str:
    """
    Normalize text for comparison:
    - lowercase
    - replace spaces, hyphens, underscores with space
    - remove special characters
    """
    text = text.lower()
    text = re.sub(r"[_\-]", " ", text)
    text = re.sub(r"[^a-z0-9 ]", "", text)
    return text


def _score_match(query_words: list, filename: str) -> int:
    """
    Score how well a query matches a PDF filename.

    Higher score = better match.
    Returns 0 if no match at all.

    Parameters:
        query_words (list): Individual words from the student query
        filename    (str):  PDF filename like "Exam_Timetable_Sem2.pdf"

    Returns:
        int: match score (0 = no match)
    """
    filename_norm = _normalize(filename.replace(".pdf", ""))
    filename_words = filename_norm.split()

    score = 0

    for q_word in query_words:
        # Direct word match in filename
        if q_word in filename_words:
            score += 3  # Strong match
        elif q_word in filename_norm:
            score += 2  # Partial match

        # Synonym/keyword expansion match
        synonyms = KEYWORD_SYNONYMS.get(q_word, [])
        for syn in synonyms:
            syn_norm = _normalize(syn)
            if syn_norm in filename_norm:
                score += 1  # Weak but valid match

    return score


def find_matching_pdfs(student_query: str) -> list:
    """
    Find uploaded PDF files that match the student's query.

    Parameters:
        student_query (str): The student's question

    Returns:
        list of dicts, each with:
          "filename"     : the PDF filename
          "filepath"     : full path to the file on disk
          "display_name" : clean name for showing to student
          "score"        : match relevance score
    """
    if not os.path.exists(PDF_STORAGE_DIR):
        return []

    # Get all PDF files in the upload directory
    all_pdfs = [
        f for f in os.listdir(PDF_STORAGE_DIR)
        if f.lower().endswith(".pdf") and
        os.path.isfile(os.path.join(PDF_STORAGE_DIR, f))
    ]

    if not all_pdfs:
        return []

    # Normalize the student query
    query_norm  = _normalize(student_query)
    query_words = query_norm.split()

    # Filter out very short/common words that don't help matching
    stopwords   = {"the", "a", "an", "is", "are", "can", "i", "me",
                   "my", "what", "when", "where", "how", "get",
                   "give", "please", "want", "need", "do", "for",
                   "of", "to", "in", "on", "at", "and", "or"}
    query_words = [w for w in query_words if w not in stopwords and len(w) > 2]

    # Score every PDF against the query
    matches = []
    for filename in all_pdfs:
        score = _score_match(query_words, filename)
        if score > 0:
            # Create a clean display name from the filename
            display_name = filename.replace(".pdf", "")
            display_name = re.sub(r"[_\-]", " ", display_name)
            display_name = display_name.title()

            matches.append({
                "filename":     filename,
                "filepath":     os.path.join(PDF_STORAGE_DIR, filename),
                "display_name": display_name,
                "score":        score
            })

    # Sort by score — best match first
    matches.sort(key=lambda x: x["score"], reverse=True)

    # Return top 3 matches maximum
    return matches[:3]


def should_offer_download(student_query: str) -> bool:
    """
    Quick check: does this query seem to be asking for a document?

    Used to decide whether to run the full PDF matching.
    Checks for download-intent keywords in the query.

    Parameters:
        student_query (str): Student's question

    Returns:
        bool: True if query seems to want a document
    """
    download_intent_words = [
        "timetable", "time table", "schedule", "syllabus",
        "form", "document", "pdf", "download", "get me",
        "send me", "provide", "share", "fee structure",
        "handbook", "calendar", "circular", "notice",
        "prospectus", "rulebook", "policy", "guidelines"
    ]

    query_lower = student_query.lower()
    return any(word in query_lower for word in download_intent_words)


def get_pdf_bytes(filepath: str) -> bytes:
    """
    Read a PDF file from disk and return its raw bytes.
    Used by Streamlit's st.download_button.

    Parameters:
        filepath (str): Full path to the PDF file

    Returns:
        bytes: The raw PDF file content
    """
    with open(filepath, "rb") as f:
        return f.read()