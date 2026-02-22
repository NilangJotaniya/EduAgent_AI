import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ============================================================
# PAGE CONFIG — must be first Streamlit command
# ============================================================
st.set_page_config(
    page_title="EduAgent AI - Student Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# AUTO-START LOCAL LLM
# ============================================================
@st.cache_resource
def startup_llm():
    from start_llm import initialize_llm
    return initialize_llm()

with st.spinner("🚀 Starting EduAgent AI... Checking local LLM (phi3:mini)..."):
    llm_status = startup_llm()

# ============================================================
# STYLING
# ============================================================
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px; border-radius: 12px;
        color: white; text-align: center; margin-bottom: 25px;
    }
    .main-header h1 { font-size: 2.5rem; margin: 0; font-weight: 700; }
    .main-header p  { margin: 8px 0 0 0; opacity: 0.9; }

    .status-ok {
        background: #d4edda; color: #155724;
        padding: 8px 14px; border-radius: 6px;
        border: 1px solid #c3e6cb; font-size: 13px; margin: 4px 0;
    }
    .status-fail {
        background: #f8d7da; color: #721c24;
        padding: 8px 14px; border-radius: 6px;
        border: 1px solid #f5c6cb; font-size: 13px; margin: 4px 0;
    }
    .agent-log-item {
        font-size: 11px; color: #444;
        padding: 4px 8px;
        border-left: 3px solid #667eea;
        margin: 3px 0; background: #f8f9ff;
        border-radius: 0 4px 4px 0;
    }

    /* PDF download card shown in chat */
    .pdf-download-card {
        background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
        border: 1px solid #a5d6a7;
        border-radius: 10px;
        padding: 15px 18px;
        margin: 10px 0;
    }
    .pdf-download-card h4 {
        color: #2e7d32;
        margin: 0 0 6px 0;
        font-size: 14px;
    }
    .pdf-download-card p {
        color: #555;
        margin: 0 0 10px 0;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# INITIALIZE AGENTS
# ============================================================
@st.cache_resource
def initialize_agents():
    try:
        from agents.query_agent      import QueryUnderstandingAgent
        from agents.retrieval_agent  import InformationRetrievalAgent
        from agents.response_agent   import ResponseGenerationAgent
        from agents.escalation_agent import EscalationAgent

        return (
            QueryUnderstandingAgent(),
            InformationRetrievalAgent(),
            ResponseGenerationAgent(),
            EscalationAgent(),
            True
        )
    except Exception as e:
        return None, None, None, None, str(e)

query_agent, retrieval_agent, response_agent, \
    escalation_agent, agents_ready = initialize_agents()

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## 🎓 EduAgent AI")
    st.markdown("*Multi-Agent Academic Assistant*")
    st.markdown("---")

    # LLM Status
    st.markdown("### 🖥️ Local AI Status")
    if llm_status.get("ready"):
        st.markdown(
            '<div class="status-ok">🟢 phi3:mini — Online (Local AI)</div>',
            unsafe_allow_html=True
        )
        st.caption("Running on your machine — no internet needed!")
    else:
        st.markdown(
            '<div class="status-fail">🔴 LLM Offline</div>',
            unsafe_allow_html=True
        )
        st.caption(llm_status.get("message", ""))
        st.info("Fix: Open a terminal and run `ollama serve`, then refresh.")

    st.markdown("---")

    # Agent Status
    st.markdown("### 🤖 Agent Status")
    for name in ["🔍 Query Understanding", "📚 Information Retrieval",
                 "🧠 Response Generation", "⚠️ Escalation"]:
        if agents_ready is True:
            st.success(name)
        else:
            st.error(name)

    st.markdown("---")

    # Topics
    st.markdown("### 💬 I Can Help With:")
    for t in ["📅 Exam schedules & timetables",
              "💰 Fee structure & payments",
              "📊 Attendance requirements",
              "🎓 Scholarships & financial aid",
              "📄 Admission & documents",
              "📚 Library information",
              "📥 Download college documents"]:
        st.caption(t)

    st.markdown("---")

    # Agent Activity Log
    st.markdown("### 📋 Agent Activity Log")
    if "agent_log" in st.session_state and st.session_state.agent_log:
        for log in st.session_state.agent_log[-6:]:
            st.markdown(
                f'<div class="agent-log-item">{log}</div>',
                unsafe_allow_html=True
            )
    else:
        st.caption("Activity will appear here as you chat...")

# ============================================================
# MAIN AREA
# ============================================================
st.markdown("""
<div class="main-header">
    <h1>🎓 EduAgent AI</h1>
    <p>Multi-Agent Academic Assistant &nbsp;|&nbsp;
       Powered by phi3:mini (100% Local AI) &nbsp;|&nbsp;
       MongoDB Atlas Database</p>
</div>
""", unsafe_allow_html=True)

if not llm_status.get("ready"):
    st.error("""
    ⚠️ **Local AI (phi3:mini) is not running.**
    1. Open a new terminal
    2. Run: `ollama serve`
    3. Refresh this page (F5)
    """)

if agents_ready is not True:
    st.warning(f"⚠️ Agent initialization issue: {agents_ready}")

# ============================================================
# CHAT HISTORY
# ============================================================
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": (
            "👋 **Hello! I'm EduAgent AI**, your intelligent academic assistant.\n\n"
            "I'm powered by **phi3:mini** running locally on your machine, "
            "with data stored in **MongoDB Atlas**.\n\n"
            "I can help you with:\n"
            "- 📅 Exam schedules and timetables\n"
            "- 💰 Fee structure and payment info\n"
            "- 📊 Attendance policies\n"
            "- 🎓 Scholarships and admissions\n"
            "- 📥 **Download college documents** (timetables, handbooks, etc.)\n\n"
            "**What would you like to know today?**"
        ),
        "pdf_matches": []   # No PDFs with welcome message
    })

if "agent_log" not in st.session_state:
    st.session_state.agent_log = []


# ============================================================
# HELPER: Render a single chat message (with optional PDF downloads)
# ============================================================
def render_message(message: dict):
    """
    Renders a chat message. If the message has PDF matches attached,
    shows download buttons below the text.
    """
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Show PDF download cards if any were found
        pdf_matches = message.get("pdf_matches", [])
        if pdf_matches:
            st.markdown("---")
            st.markdown("#### 📥 Related Documents Available for Download:")

            for pdf in pdf_matches:
                filepath = pdf.get("filepath", "")
                filename = pdf.get("filename", "")
                display  = pdf.get("display_name", filename)

                if os.path.exists(filepath):
                    # Read the PDF bytes
                    with open(filepath, "rb") as f:
                        pdf_bytes = f.read()

                    # Render a styled card with download button
                    st.markdown(
                        f"""
                        <div class="pdf-download-card">
                            <h4>📄 {display}</h4>
                            <p>Click the button below to download this document.</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Streamlit's built-in download button
                    # This creates a proper file download in the browser
                    st.download_button(
                        label=f"⬇️ Download {display}",
                        data=pdf_bytes,
                        file_name=filename,
                        mime="application/pdf",
                        key=f"dl_{filename}_{id(message)}",
                        use_container_width=False
                    )


# Render all previous messages
for message in st.session_state.messages:
    render_message(message)


# ============================================================
# HANDLE NEW USER INPUT
# ============================================================
if prompt := st.chat_input("Ask me anything about academic matters..."):

    # Add user message to history and display it
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "pdf_matches": []
    })
    with st.chat_message("user"):
        st.markdown(prompt)

    # ---- Generate AI Response ----
    with st.chat_message("assistant"):
        response_text = ""
        pdf_matches   = []

        if not llm_status.get("ready"):
            response_text = (
                "⚠️ The local AI (phi3:mini) is not running. "
                "Open a terminal, run `ollama serve`, then refresh this page."
            )
            st.markdown(response_text)

        elif agents_ready is not True:
            response_text = f"⚠️ System error: {agents_ready}"
            st.markdown(response_text)

        else:
            status_text = st.empty()

            try:
                # ---- AGENT 1: ESCALATION CHECK ----
                status_text.caption("⚠️ Escalation Agent: Checking query sensitivity...")
                escalation_result = escalation_agent.process(prompt)
                st.session_state.agent_log.append("⚠️ Escalation Agent: Checked")

                if escalation_result["escalated"]:
                    status_text.empty()
                    response_text = escalation_result["message"]
                    st.session_state.agent_log.append("🚨 Query escalated to admin staff")
                    st.markdown(response_text)

                else:
                    # ---- PDF MATCH CHECK ----
                    # Run this early so we can mention the download in the response
                    status_text.caption("📥 Checking for downloadable documents...")
                    from utils.pdf_matcher import should_offer_download, find_matching_pdfs

                    if should_offer_download(prompt):
                        pdf_matches = find_matching_pdfs(prompt)
                        if pdf_matches:
                            st.session_state.agent_log.append(
                                f"📥 PDF Matcher: {len(pdf_matches)} document(s) found"
                            )
                        else:
                            st.session_state.agent_log.append(
                                "📥 PDF Matcher: No matching documents found"
                            )

                    # ---- AGENT 2: QUERY UNDERSTANDING ----
                    status_text.caption("🔍 Query Agent: Analyzing your question...")
                    query_analysis = query_agent.analyze(prompt)
                    st.session_state.agent_log.append(
                        f"🔍 Query Agent: Category = '{query_analysis['category']}'"
                    )

                    # ---- AGENT 3: INFORMATION RETRIEVAL ----
                    status_text.caption("📚 Retrieval Agent: Searching database...")
                    retrieved_data = retrieval_agent.retrieve(query_analysis)
                    faq_count = len(retrieved_data.get("faqs", []))
                    st.session_state.agent_log.append(
                        f"📚 Retrieval Agent: {faq_count} FAQ(s) found"
                    )

                    # ---- AGENT 4: RESPONSE GENERATION ----
                    # Let the AI know a PDF is available so it mentions it
                    if pdf_matches:
                        retrieved_data["pdf_download_available"] = [
                            p["display_name"] for p in pdf_matches
                        ]

                    status_text.caption(
                        "🧠 Response Agent: phi3:mini is generating your answer..."
                    )
                    response_text = response_agent.generate(prompt, retrieved_data)
                    st.session_state.agent_log.append(
                        "🧠 Response Agent: Answer generated ✅"
                    )

                    status_text.empty()
                    st.markdown(response_text)

                    # ---- SHOW PDF DOWNLOAD BUTTONS ----
                    if pdf_matches:
                        st.markdown("---")
                        st.markdown("#### 📥 Related Documents Available for Download:")

                        for pdf in pdf_matches:
                            filepath = pdf.get("filepath", "")
                            filename = pdf.get("filename", "")
                            display  = pdf.get("display_name", filename)

                            if os.path.exists(filepath):
                                with open(filepath, "rb") as f:
                                    pdf_bytes = f.read()

                                st.markdown(
                                    f"""
                                    <div class="pdf-download-card">
                                        <h4>📄 {display}</h4>
                                        <p>Click below to download this document directly.</p>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                                st.download_button(
                                    label=f"⬇️ Download {display}",
                                    data=pdf_bytes,
                                    file_name=filename,
                                    mime="application/pdf",
                                    key=f"dl_{filename}_{len(st.session_state.messages)}",
                                    use_container_width=False
                                )

            except Exception as e:
                status_text.empty()
                response_text = (
                    f"❌ Something went wrong: {str(e)}\n\n"
                    "Please try again."
                )
                st.markdown(response_text)
                st.session_state.agent_log.append(f"❌ Error: {str(e)[:50]}")

    # Save assistant message (with pdf_matches so download buttons
    # re-appear if user scrolls up through history)
    st.session_state.messages.append({
        "role":        "assistant",
        "content":     response_text,
        "pdf_matches": pdf_matches
    })


# ============================================================
# QUICK QUESTION BUTTONS
# ============================================================
st.markdown("---")
st.markdown("#### 💡 Quick Questions — Click to Ask:")

col1, col2, col3, col4 = st.columns(4)
quick_questions = [
    (col1, "📅 Exam Timetable",    "Can you give me the exam timetable?"),
    (col2, "💰 Fee Structure",     "What is the complete fee structure?"),
    (col3, "📊 Attendance Policy", "What is the minimum attendance requirement?"),
    (col4, "🎓 Scholarships",      "What scholarships are available?"),
]

for col, label, question in quick_questions:
    with col:
        if st.button(label, use_container_width=True):
            st.session_state.messages.append({
                "role": "user", "content": question, "pdf_matches": []
            })
            st.rerun()

st.markdown("")
if st.button("🗑️ Clear Chat History", type="secondary"):
    st.session_state.messages = []
    st.session_state.agent_log = []
    st.rerun()
