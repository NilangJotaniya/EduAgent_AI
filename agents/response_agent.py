import requests
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_NAME      = "phi3:mini"

INSTITUTION_NAME     = os.getenv("INSTITUTION_NAME",     "MBIT, CVM University")
INSTITUTION_LOCATION = os.getenv("INSTITUTION_LOCATION", "Anand, Gujarat, India")
INSTITUTION_TYPE     = os.getenv("INSTITUTION_TYPE",     "Engineering College")
ACADEMIC_YEAR        = os.getenv("ACADEMIC_YEAR",        "2025-2026")
AGENT_PURPOSE        = os.getenv(
    "AGENT_PURPOSE",
    "Answer only academic administration queries for MBIT students. "
    "Do not discuss internships, personal details, or anything unrelated to college academics."
)


class ResponseGenerationAgent:

    def __init__(self):
        self.api_url = f"{OLLAMA_BASE_URL}/api/generate"
        self.model   = MODEL_NAME
        print(f"✅ Response Agent initialized — Model: {MODEL_NAME}")
        print(f"   Serving: {INSTITUTION_NAME}, {INSTITUTION_LOCATION}")

    def format_context(self, retrieved_data: dict) -> str:
        """Convert retrieved MongoDB data into clean text for the AI prompt."""
        parts = []

        if retrieved_data.get("faqs"):
            parts.append("RELEVANT FAQs FROM DATABASE:")
            for i, faq in enumerate(retrieved_data["faqs"], 1):
                parts.append(f"  Q{i}: {faq.get('question', '')}")
                parts.append(f"  A{i}: {faq.get('answer', '')}")
                parts.append("")

        if retrieved_data.get("exam_schedule"):
            parts.append("EXAM SCHEDULE FROM DATABASE:")
            for exam in retrieved_data["exam_schedule"]:
                parts.append(
                    f"  - {exam.get('subject', '')}: "
                    f"{exam.get('date', '')} at {exam.get('time', '')} "
                    f"| Venue: {exam.get('venue', '')}"
                )
            parts.append("")

        if retrieved_data.get("fees"):
            parts.append("FEE STRUCTURE FROM DATABASE:")
            for fee in retrieved_data["fees"]:
                desc = f" | {fee.get('description', '')}" if fee.get("description") else ""
                parts.append(
                    f"  - {fee.get('type', '')}: "
                    f"Rs. {fee.get('amount', 0):,.0f} "
                    f"| Due: {fee.get('due_date', '')}"
                    f"{desc}"
                )
            parts.append("")

        if retrieved_data.get("pdf_context"):
            parts.append("FROM UPLOADED COLLEGE DOCUMENTS:")
            parts.append(retrieved_data["pdf_context"])
            parts.append("")

        if retrieved_data.get("pdf_download_available"):
            doc_names = ", ".join(retrieved_data["pdf_download_available"])
            parts.append(f"DOWNLOADABLE DOCUMENTS AVAILABLE: {doc_names}")
            parts.append(
                "Tell the student a download button appears below your response."
            )
            parts.append("")

        if not parts:
            return "NO DATA FOUND IN DATABASE FOR THIS QUERY."

        return "\n".join(parts)

    def generate(self, student_query: str, retrieved_data: dict) -> str:
        """
        Generate AI response using local phi3:mini.

        Parameters:
            student_query  (str):  Student's original question
            retrieved_data (dict): Data from InformationRetrievalAgent

        Returns:
            str: AI-generated response
        """
        context      = self.format_context(retrieved_data)
        has_download = bool(retrieved_data.get("pdf_download_available"))

        # ==============================================================
        # SYSTEM PROMPT
        # Defines who the AI is, which institution it serves,
        # and strict rules to prevent hallucination and data leakage.
        # ==============================================================
        system_prompt = f"""You are EduAgent AI, the official academic assistant for:

INSTITUTION  : {INSTITUTION_NAME}
LOCATION     : {INSTITUTION_LOCATION}
TYPE         : {INSTITUTION_TYPE}
ACADEMIC YEAR: {ACADEMIC_YEAR}
PURPOSE      : {AGENT_PURPOSE}

IDENTITY RULES — ABSOLUTE, NO EXCEPTIONS:
1. You ONLY represent {INSTITUTION_NAME}. You serve ONLY its students.
2. NEVER mention any other college, university, foundation, or organization.
   Do NOT say "Code Unnati", "Edunet Foundation", "SAP", "Venom Technologies",
   or any other company, program, or organization name under any circumstances.
3. If asked "who are you" or "what are you", respond with ONLY:
   "I am EduAgent AI, the official academic assistant for {INSTITUTION_NAME},
   {INSTITUTION_LOCATION}. I help students with academic queries about exams,
   fees, attendance, scholarships, and more."
   Do NOT add anything else to this answer.

DATA RULES — ABSOLUTE, NO EXCEPTIONS:
4. Answer ONLY using the DATABASE CONTEXT provided below.
5. If the context says "NO DATA FOUND" or does not contain the answer, say:
   "I don't have that specific information in the system yet. Please contact
   the {INSTITUTION_NAME} administrative office directly for accurate details."
6. NEVER invent, guess, or assume ANY data — not fees, not dates, not names,
   not addresses, not amounts, not semester details.
   If it is NOT in the context below, do NOT say it.
7. NEVER use information from your AI training data about any institution.
8. NEVER reveal any personal information, student names, resume details,
   uploaded document contents beyond academic info, or internship details.
9. NEVER discuss internship programs, personal student records, or any
   data unrelated to MBIT academic administration.

FORMATTING RULES:
10. Be clear, warm, and well-structured in your responses.
11. Use bullet points when listing multiple items.
12. Keep responses concise and directly relevant to the question.
13. Always end with: "Is there anything else I can help you with?"
{f"14. A downloadable document is available — tell the student to click the download button that appears below your response." if has_download else ""}"""

        # ==============================================================
        # USER PROMPT — The question + database context
        # ==============================================================
        user_prompt = (
            f"--- DATABASE CONTEXT (from {INSTITUTION_NAME} official records) ---\n"
            f"{context}\n"
            f"--- END OF DATABASE CONTEXT ---\n\n"
            f"Student Question: {student_query}"
        )

        # ==============================================================
        # FULL PROMPT in phi3:mini format
        # phi3 uses <|system|>, <|user|>, <|assistant|> special tags
        # ==============================================================
        full_prompt = (
            f"<|system|>\n{system_prompt}\n<|end|>\n"
            f"<|user|>\n{user_prompt}\n<|end|>\n"
            f"<|assistant|>\n"
        )

        try:
            print(f"🧠 Response Agent: Sending query to {MODEL_NAME}...")
            print(f"   Context: {len(context)} chars")

            response = requests.post(
                self.api_url,
                json={
                    "model":  self.model,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {
                        "temperature":    0.1,   # Very low = very factual, minimal creativity
                        "num_predict":    600,   # Max tokens in response
                        "top_p":          0.85,
                        "repeat_penalty": 1.2   # Prevents repetitive output
                    }
                },
                timeout=180  # 3 minutes max for phi3:mini
            )

            if response.status_code == 200:
                result = response.json()
                text   = result.get("response", "").strip()

                if text:
                    print(f"✅ Response generated ({len(text)} chars)")
                    return text

                return (
                    "I received an empty response from the AI. "
                    "Please try asking your question again."
                )

            return (
                f"⚠️ The AI returned an error (HTTP {response.status_code}). "
                "Please try again in a moment."
            )

        except requests.exceptions.Timeout:
            return (
                "⏳ **The AI is taking longer than expected.**\n\n"
                "phi3:mini sometimes takes up to 2 minutes on the first query "
                "while loading into memory. Please try again."
            )

        except requests.exceptions.ConnectionError:
            return (
                "❌ **Cannot connect to the local AI.**\n\n"
                "Open a terminal and run: `ollama serve`\n"
                "Then refresh this page (F5)."
            )

        except Exception as e:
            print(f"❌ Response Agent error: {e}")
            return (
                f"❌ Unexpected error: {str(e)}\n\n"
                "Please try again or restart the application."
            )
