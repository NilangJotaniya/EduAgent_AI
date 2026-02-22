import streamlit as st
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="Admin Panel — EduAgent AI",
    page_icon="🔧",
    layout="wide"
)

# ============================================================
# ADMIN PASSWORD PROTECTION
# ============================================================
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")


def check_authentication() -> bool:
    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False

    if not st.session_state.admin_authenticated:
        st.title("🔐 Admin Login")
        st.markdown("---")
        st.info("This panel is restricted to administrative staff only.")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### Enter Admin Password")
            entered = st.text_input("Password:", type="password")
            if st.button("🔓 Login", type="primary", use_container_width=True):
                if entered == ADMIN_PASSWORD:
                    st.session_state.admin_authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Incorrect password.")
        return False
    return True


if not check_authentication():
    st.stop()

# ============================================================
# IMPORT MONGODB FUNCTIONS
# ============================================================
try:
    from database.mongo_db import (
        get_statistics, get_escalated_queries, update_escalated_query,
        get_all_faqs, add_faq, update_faq, delete_faq,
        get_all_exams, add_exam, delete_exam,
        get_all_fees, add_fee, delete_fee,
        get_all_uploaded_pdfs, record_uploaded_pdf, delete_uploaded_pdf_record
    )
    db_connected = True
except Exception as e:
    st.error(f"❌ MongoDB connection failed: {e}\n\nCheck your MONGO_URI in .env")
    db_connected = False
    st.stop()

# ============================================================
# HEADER
# ============================================================
col_title, col_logout = st.columns([8, 1])
with col_title:
    st.title("🔧 EduAgent AI — Admin Panel")
    st.caption(
        f"Connected to MongoDB Atlas  |  "
        f"{datetime.now().strftime('%A, %B %d %Y, %I:%M %p')}"
    )
with col_logout:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Logout"):
        st.session_state.admin_authenticated = False
        st.rerun()

st.markdown("---")

# ============================================================
# STATISTICS DASHBOARD
# ============================================================
st.markdown("### 📊 System Overview")
stats = get_statistics()

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("📝 FAQs",             stats["total_faqs"])
c2.metric("🚨 Total Escalated",  stats["total_escalated"])
c3.metric("⏳ Pending Review",   stats["pending_escalated"],
          delta=f"{stats['pending_escalated']} need action"
          if stats["pending_escalated"] > 0 else None,
          delta_color="inverse")
c4.metric("📄 PDFs Uploaded",    stats["uploaded_pdfs"])
c5.metric("📅 Exam Entries",     stats["exam_entries"])
c6.metric("💰 Fee Entries",      stats["fee_entries"])

st.markdown("---")

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🚨 Escalated Queries",
    "📝 Manage FAQs",
    "📄 PDF Documents",
    "📅 Exam Schedule",
    "💰 Fee Structure"
])

# ==============================
# TAB 1 — ESCALATED QUERIES
# ==============================
with tab1:
    st.markdown("### 🚨 Escalated Queries")
    st.markdown("Student queries flagged by the AI as sensitive. Please respond within 24 hours.")

    status_filter = st.selectbox(
        "Filter by status:",
        ["all", "pending", "in-progress", "resolved"]
    )

    queries = get_escalated_queries(status_filter)

    if not queries:
        st.success("✅ No queries found for this filter.")
    else:
        st.caption(f"Showing {len(queries)} record(s)")

        for q in queries:
            icon = {"pending": "🔴", "in-progress": "🟡",
                    "resolved": "🟢"}.get(q.get("status", "pending"), "⚪")

            with st.expander(
                f"{icon} [{q.get('timestamp', '')[:16]}]  —  "
                f"{q.get('student_query', '')[:85]}..."
            ):
                col_left, col_right = st.columns([3, 2])

                with col_left:
                    st.markdown("**Full Query:**")
                    st.info(q.get("student_query", ""))
                    st.markdown(f"**Flagged Because:** `{q.get('reason', '')}`")
                    st.markdown(f"**Status:** `{q.get('status', 'pending')}`")
                    if q.get("admin_notes"):
                        st.markdown(f"**Previous Notes:** {q['admin_notes']}")

                with col_right:
                    current_status = q.get("status", "pending")
                    status_options = ["pending", "in-progress", "resolved"]
                    new_status = st.selectbox(
                        "Update Status:",
                        status_options,
                        index=status_options.index(current_status)
                        if current_status in status_options else 0,
                        key=f"esc_status_{q['_id']}"
                    )
                    notes = st.text_area(
                        "Admin Notes:",
                        value=q.get("admin_notes", ""),
                        key=f"esc_notes_{q['_id']}"
                    )
                    if st.button("💾 Save", key=f"esc_save_{q['_id']}"):
                        if update_escalated_query(q["_id"], new_status, notes):
                            st.success("✅ Updated!")
                            st.rerun()
                        else:
                            st.error("❌ Update failed.")

# ==============================
# TAB 2 — MANAGE FAQs
# ==============================
with tab2:
    st.markdown("### 📝 FAQ Management")

    # Add new FAQ
    with st.expander("➕ Add New FAQ", expanded=False):
        with st.form("form_add_faq"):
            col_q, col_c = st.columns([3, 1])
            with col_q:
                new_q = st.text_input("Question:")
            with col_c:
                new_cat = st.selectbox(
                    "Category:",
                    ["Exam", "Fees", "Attendance", "Scholarship",
                     "Admission", "Library", "General"]
                )
            new_ans  = st.text_area("Answer:", height=120)
            new_kw   = st.text_input("Keywords (comma-separated):")

            if st.form_submit_button("✅ Add FAQ", type="primary"):
                if new_q.strip() and new_ans.strip():
                    if add_faq(new_cat, new_q.strip(), new_ans.strip(), new_kw.strip()):
                        st.success("✅ FAQ added to MongoDB!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to add FAQ.")
                else:
                    st.error("Question and Answer are required.")

    st.markdown("---")
    st.markdown("#### Existing FAQs")

    all_faqs = get_all_faqs()
    categories = ["All"] + sorted(set(f.get("category", "") for f in all_faqs))
    selected_cat = st.selectbox("Filter by Category:", categories)

    display_faqs = (
        all_faqs if selected_cat == "All"
        else [f for f in all_faqs if f.get("category") == selected_cat]
    )

    if not display_faqs:
        st.info("No FAQs found.")
    else:
        st.caption(f"Showing {len(display_faqs)} FAQ(s)")
        for faq in display_faqs:
            with st.expander(
                f"📌 [{faq.get('category','?')}]  "
                f"{faq.get('question','')[:70]}..."
            ):
                col_edit, col_act = st.columns([4, 1])
                with col_edit:
                    edited_ans = st.text_area(
                        "Answer:", value=faq.get("answer", ""),
                        key=f"faq_ans_{faq['_id']}"
                    )
                    edited_kw = st.text_input(
                        "Keywords:", value=faq.get("keywords", ""),
                        key=f"faq_kw_{faq['_id']}"
                    )
                with col_act:
                    st.markdown("<br><br>", unsafe_allow_html=True)
                    if st.button("💾 Update", key=f"faq_upd_{faq['_id']}",
                                 use_container_width=True):
                        if update_faq(faq["_id"], edited_ans, edited_kw):
                            st.success("Updated!")
                            st.rerun()
                    if st.button("🗑️ Delete", key=f"faq_del_{faq['_id']}",
                                 use_container_width=True):
                        if delete_faq(faq["_id"]):
                            st.success("Deleted!")
                            st.rerun()

# ==============================
# TAB 3 — PDF DOCUMENTS
# ==============================
with tab3:
    st.markdown("### 📄 PDF Document Management")
    st.info(
        "Upload college handbooks, rulebooks, or any academic PDF. "
        "The AI will learn from them and use the content to answer student queries."
    )

    uploaded_file = st.file_uploader("Select a PDF:", type=["pdf"])

    if uploaded_file:
        col_info, col_btn = st.columns([3, 1])
        with col_info:
            st.markdown(f"**File:** {uploaded_file.name}")
            st.markdown(f"**Size:** {uploaded_file.size / 1024:.1f} KB")
        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 Upload & Process", type="primary"):
                with st.spinner("Reading PDF and building knowledge base..."):
                    try:
                        save_path = os.path.join("uploaded_pdfs", uploaded_file.name)
                        os.makedirs("uploaded_pdfs", exist_ok=True)
                        with open(save_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                        from utils.pdf_processor import PDFProcessor
                        result = PDFProcessor().process_pdf(save_path, uploaded_file.name)

                        if result["success"]:
                            record_uploaded_pdf(
                                uploaded_file.name,
                                result["pages"],
                                result["chunks"]
                            )
                            st.success(
                                f"✅ Processed! Pages: {result['pages']} | "
                                f"Chunks: {result['chunks']}"
                            )
                        else:
                            st.error(f"❌ {result.get('error')}")
                    except Exception as e:
                        st.error(f"❌ Upload failed: {e}")

    st.markdown("---")
    st.markdown("#### Uploaded Documents")
    pdfs = get_all_uploaded_pdfs()

    if not pdfs:
        st.info("No PDFs uploaded yet.")
    else:
        for pdf in pdfs:
            col_n, col_s, col_d = st.columns([4, 3, 1])
            with col_n:
                st.markdown(f"📄 **{pdf.get('original_name', '')}**")
                st.caption(f"Uploaded: {pdf.get('uploaded_at', '')[:16]}")
            with col_s:
                st.caption(
                    f"Pages: {pdf.get('pages', 0)}  |  "
                    f"Chunks: {pdf.get('chunks', 0)}"
                )
            with col_d:
                if st.button("🗑️", key=f"pdf_del_{pdf['_id']}"):
                    delete_uploaded_pdf_record(pdf["_id"])
                    fp = os.path.join("uploaded_pdfs", pdf.get("filename", ""))
                    if os.path.exists(fp):
                        os.remove(fp)
                    st.rerun()
            st.markdown("---")

# ==============================
# TAB 4 — EXAM SCHEDULE
# ==============================
with tab4:
    st.markdown("### 📅 Exam Schedule Management")

    with st.expander("➕ Add New Exam"):
        with st.form("form_add_exam"):
            col_s, col_sem = st.columns([3, 1])
            with col_s:
                subject = st.text_input("Subject:")
            with col_sem:
                semester = st.number_input("Semester:", 1, 8, 1)
            col_d, col_t, col_v = st.columns(3)
            with col_d:
                exam_date = st.date_input("Date:")
            with col_t:
                exam_time = st.time_input("Time:")
            with col_v:
                venue = st.text_input("Venue:")

            if st.form_submit_button("➕ Add", type="primary"):
                if subject.strip():
                    if add_exam(subject.strip(), str(exam_date),
                                str(exam_time), venue.strip(), semester):
                        st.success(f"✅ {subject} added!")
                        st.rerun()
                else:
                    st.error("Subject is required.")

    exams = get_all_exams()
    if exams:
        st.markdown("#### Current Schedule")
        for e in exams:
            col_info, col_del = st.columns([5, 1])
            with col_info:
                st.markdown(
                    f"**{e.get('subject','')}** — "
                    f"{e.get('exam_date','')} at {e.get('exam_time','')} | "
                    f"Venue: {e.get('venue','')} | Sem: {e.get('semester','')}"
                )
            with col_del:
                if st.button("🗑️", key=f"exam_del_{e['_id']}"):
                    if delete_exam(e["_id"]):
                        st.rerun()
            st.markdown("---")
    else:
        st.info("No exam entries yet.")

# ==============================
# TAB 5 — FEE STRUCTURE
# ==============================
with tab5:
    st.markdown("### 💰 Fee Structure Management")

    with st.expander("➕ Add New Fee"):
        with st.form("form_add_fee"):
            col_ft, col_amt = st.columns(2)
            with col_ft:
                fee_type = st.text_input("Fee Type:")
            with col_amt:
                amount = st.number_input("Amount (Rs.):", min_value=0.0, step=100.0)
            col_dd, col_desc = st.columns(2)
            with col_dd:
                due_date = st.text_input("Due Date:")
            with col_desc:
                description = st.text_input("Description:")

            if st.form_submit_button("➕ Add", type="primary"):
                if fee_type.strip():
                    if add_fee(fee_type.strip(), amount,
                               due_date.strip(), description.strip()):
                        st.success(f"✅ {fee_type} added!")
                        st.rerun()
                else:
                    st.error("Fee type is required.")

    fees = get_all_fees()
    if fees:
        st.markdown("#### Current Fee Structure")
        total = 0
        for f in fees:
            col_info, col_del = st.columns([5, 1])
            with col_info:
                st.markdown(
                    f"**{f.get('fee_type','')}** — "
                    f"Rs. {f.get('amount',0):,.0f} | "
                    f"Due: {f.get('due_date','')} | "
                    f"{f.get('description','')}"
                )
                total += f.get("amount", 0)
            with col_del:
                if st.button("🗑️", key=f"fee_del_{f['_id']}"):
                    if delete_fee(f["_id"]):
                        st.rerun()
            st.markdown("---")
        st.markdown(f"**Total Annual Fee: Rs. {total:,.0f}**")
    else:
        st.info("No fee entries yet.")