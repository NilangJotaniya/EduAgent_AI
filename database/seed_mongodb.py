import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.mongo_db import get_database


def seed_faqs(db):
    if db.faqs.count_documents({}) > 0:
        print(f"FAQs already seeded ({db.faqs.count_documents({})} found). Skipping.")
        return

    faqs = [
        {
            "category": "Attendance",
            "question": "What is the minimum attendance requirement?",
            "answer": (
                "The minimum attendance requirement at MBIT, CVM University is 75%. "
                "Students with attendance below 75% will not be permitted to appear in "
                "the final examinations. Students between 65-74% may apply for condonation "
                "with valid medical documents. Below 65% results in automatic detention."
            ),
            "keywords": "attendance, minimum, requirement, percentage, 75, detained, condonation"
        },
        {
            "category": "Attendance",
            "question": "How can I apply for attendance condonation?",
            "answer": (
                "Students at MBIT with attendance between 65-74% can apply for condonation. "
                "Submit Form ATT-02 to the academic office with your medical certificate or "
                "valid reason. Applications must be submitted at least 7 days before exams. "
                "The condonation committee reviews each case individually."
            ),
            "keywords": "condonation, leave, medical, attendance shortage, form, apply"
        },
        {
            "category": "Fees",
            "question": "What is the fee payment deadline?",
            "answer": (
                "At MBIT, CVM University, semester fees must be paid within the first 30 days "
                "of the semester start date. Late payments attract a fine of Rs. 100 per day "
                "after the deadline. Students with unpaid fees will not receive hall tickets "
                "for semester exams. Payment can be done online via the student portal or at "
                "the accounts office."
            ),
            "keywords": "fee, payment, deadline, semester, fine, late fee, hall ticket"
        },
        {
            "category": "Fees",
            "question": "Can I pay fees in installments?",
            "answer": (
                "Yes, at MBIT fees can be paid in two installments upon approval. Submit an "
                "installment request form to the Accounts Department with a valid reason. "
                "First installment (60% of total) by the 30th day of semester start, "
                "remaining 40% within 60 days."
            ),
            "keywords": "installment, partial payment, fee payment, emi, split fee"
        },
        {
            "category": "Exam",
            "question": "How do I apply for re-evaluation of exam papers?",
            "answer": (
                "At MBIT, CVM University you can apply for re-evaluation within 7 days of "
                "the result declaration date. Collect Form RE-01 from the examination "
                "department. Submit with a fee of Rs. 500 per subject. Results are typically "
                "updated within 3-4 weeks. If marks improve, the fee is refunded."
            ),
            "keywords": "re-evaluation, recheck, result, exam, marks, form, paper viewing"
        },
        {
            "category": "Exam",
            "question": "How do I get my hall ticket for the semester exam?",
            "answer": (
                "Hall tickets at MBIT are issued 7-10 days before the exam start date. "
                "Requirements: fees fully paid, attendance above 75%, no pending library dues. "
                "Download from the student portal or collect from the exam section. "
                "Hall ticket is mandatory for exam hall entry."
            ),
            "keywords": "hall ticket, admit card, exam entry, exam section, download"
        },
        {
            "category": "Scholarship",
            "question": "What scholarships are available for students?",
            "answer": (
                "Available scholarships at MBIT, CVM University:\n"
                "1. Merit Scholarship: Top 10% of class — Rs. 10,000/year\n"
                "2. Need-based Scholarship: EWS students — up to full fee waiver\n"
                "3. Sports Scholarship: National/state athletes — Rs. 5,000/semester\n"
                "4. Government Scholarships: SC/ST/OBC via Gujarat state portal\n"
                "Contact the scholarship desk in Block C for application forms."
            ),
            "keywords": "scholarship, merit, need-based, sports, sc, st, obc, financial aid"
        },
        {
            "category": "Admission",
            "question": "What documents are required for admission at MBIT?",
            "answer": (
                "Required documents for admission at MBIT, CVM University:\n"
                "1. 10th standard marksheet and passing certificate\n"
                "2. 12th standard marksheet and passing certificate\n"
                "3. Transfer Certificate (TC) from previous institution\n"
                "4. Migration Certificate (if from another university)\n"
                "5. 4 recent passport-size photographs\n"
                "6. Aadhar Card photocopy\n"
                "7. Caste certificate if applicable\n"
                "8. Medical fitness certificate\n"
                "All originals must be presented at verification."
            ),
            "keywords": "admission, documents, required, certificate, marksheet, tc, aadhar"
        },
        {
            "category": "Library",
            "question": "How many books can I borrow from the MBIT library?",
            "answer": (
                "MBIT library allows students to borrow up to 4 books for 14 days. "
                "Books can be renewed once for 7 more days if not reserved by others. "
                "Late return fine: Rs. 2 per day per book. "
                "Reference books are for in-library use only. "
                "Library hours: Monday to Saturday, 8:00 AM to 7:00 PM."
            ),
            "keywords": "library, books, borrow, issue, return, fine, renew"
        },
        {
            "category": "General",
            "question": "How do I get a bonafide certificate from MBIT?",
            "answer": (
                "To get a bonafide certificate at MBIT:\n"
                "1. Visit the administrative office (9 AM - 4 PM, Mon-Fri)\n"
                "2. Bring your MBIT college ID card\n"
                "3. Fill the request form and state the purpose\n"
                "Certificate issued within 2 working days. "
                "Same-day express service available with prior approval."
            ),
            "keywords": "bonafide, certificate, document, official, attestation"
        },
        {
            "category": "General",
            "question": "What are MBIT college working hours?",
            "answer": (
                "MBIT, CVM University working hours:\n"
                "- Classes: Monday to Saturday, 8:00 AM to 5:00 PM\n"
                "- Administrative Office: Monday to Friday, 9:00 AM to 4:30 PM\n"
                "- Library: Monday to Saturday, 8:00 AM to 7:00 PM\n"
                "- Principal's Office: By appointment only\n"
                "Closed on national holidays and semester breaks."
            ),
            "keywords": "timing, hours, office hours, college time, working hours, schedule"
        },
    ]

    db.faqs.insert_many(faqs)
    print(f"✅ Inserted {len(faqs)} FAQs into MongoDB")


def seed_exams(db):
    if db.exam_schedules.count_documents({}) > 0:
        print(f"Exams already seeded ({db.exam_schedules.count_documents({})} found). Skipping.")
        return

    exams = [
        {"subject": "Mathematics",           "exam_date": "2025-03-10", "exam_time": "10:00 AM", "venue": "Hall A",        "semester": 2},
        {"subject": "Physics",               "exam_date": "2025-03-12", "exam_time": "10:00 AM", "venue": "Hall B",        "semester": 2},
        {"subject": "Computer Science",      "exam_date": "2025-03-14", "exam_time": "02:00 PM", "venue": "Lab 1",         "semester": 2},
        {"subject": "English Communication", "exam_date": "2025-03-16", "exam_time": "10:00 AM", "venue": "Hall A",        "semester": 2},
        {"subject": "Chemistry",             "exam_date": "2025-03-18", "exam_time": "10:00 AM", "venue": "Hall C",        "semester": 2},
        {"subject": "Engineering Drawing",   "exam_date": "2025-03-20", "exam_time": "10:00 AM", "venue": "Drawing Hall",  "semester": 2},
        {"subject": "Environmental Science", "exam_date": "2025-03-22", "exam_time": "10:00 AM", "venue": "Hall B",        "semester": 2},
    ]

    db.exam_schedules.insert_many(exams)
    print(f"✅ Inserted {len(exams)} exam schedule entries into MongoDB")


def seed_fees(db):
    if db.fee_structure.count_documents({}) > 0:
        print(f"Fees already seeded ({db.fee_structure.count_documents({})} found). Skipping.")
        return

    fees = [
        {"fee_type": "Tuition Fee",          "amount": 45000.0, "due_date": "Within 30 days of semester start", "description": "Core academic fee for instruction"},
        {"fee_type": "Library Fee",          "amount": 500.0,   "due_date": "At the time of admission",         "description": "Annual library access and maintenance"},
        {"fee_type": "Sports Fee",           "amount": 300.0,   "due_date": "At the time of admission",         "description": "Access to sports facilities"},
        {"fee_type": "Exam Fee",             "amount": 800.0,   "due_date": "Before each semester examination", "description": "Per-semester exam processing fee"},
        {"fee_type": "Development Fee",      "amount": 2000.0,  "due_date": "At the time of admission",         "description": "Infrastructure and development"},
        {"fee_type": "Laboratory Fee",       "amount": 1500.0,  "due_date": "Per semester with exam fee",       "description": "Lab consumables and equipment"},
        {"fee_type": "Student Activity Fee", "amount": 200.0,   "due_date": "At the time of admission",         "description": "Cultural events and student clubs"},
    ]

    db.fee_structure.insert_many(fees)
    print(f"✅ Inserted {len(fees)} fee structure entries into MongoDB")


def seed_all():
    print("\n" + "="*55)
    print("  🌱 EduAgent AI — MongoDB Seeder (MBIT, CVM University)")
    print("="*55)

    try:
        db = get_database()
        seed_faqs(db)
        seed_exams(db)
        seed_fees(db)

        print(f"\n✅ All data seeded into MongoDB!")
        print(f"   Database : {db.name}")
        print(f"   FAQs     : {db.faqs.count_documents({})}")
        print(f"   Exams    : {db.exam_schedules.count_documents({})}")
        print(f"   Fees     : {db.fee_structure.count_documents({})}")
        print(f"\n   Run: streamlit run app.py")

    except Exception as e:
        print(f"\n❌ Seeding failed: {e}")
        print("   Check that MONGO_URI is correctly set in .env")

    print("="*55 + "\n")


if __name__ == "__main__":
    seed_all()