# INDUSTRIAL INTERNSHIP REPORT

## Cover Page

**INDUSTRIAL INTERNSHIP REPORT**  
**EduAgent AI - Student Support and Admin Automation Platform**  

Submitted by: **Nilang Vipulkumar Jotaniya**  
CVMU Enrollment No.: **12202040701108**  
Branch: **Computer Engineering**  
College: **MBIT**  
University: **The Charutar Vidya Mandal (CVM) University, Vallabh Vidyanagar - 388120**  
Month, Year: **April 2026**

---

## First Page (Title Page)

**EduAgent AI - Student Support and Admin Automation Platform**  

Submitted by  
**Nilang Vipulkumar Jotaniya**  
**12202040701108**  

In partial fulfillment for the award of the degree of  
**BACHELOR OF ENGINEERING / TECHNOLOGY**  
in  
**Computer Engineering**  

**MBIT**  
**The Charutar Vidya Mandal (CVM) University, Vallabh Vidyanagar - 388120**  

**April 2026**

---

## College Certificate

This is to certify that **Nilang Vipulkumar Jotaniya (12202040701108)** has submitted the Industrial Internship report based on internship/project work on **"EduAgent AI - Student Support and Admin Automation Platform"** in partial fulfillment for the degree of Bachelor of Engineering in Computer Engineering, **MBIT**, The Charutar Vidya Mandal (CVM) University, Vallabh Vidyanagar, during the academic year **2025-26**.


Internal Guide Signature: ____________________  
Name: **Assistant Professor Mr. Dhruv Dalwadi**

Head of Department Signature: ____________________  
Name: **Dr. Gopi Bhatt**

---

## Company Certificate

**Company Logo: [Insert official Edunet Foundation (SAP) logo here]**

Date: **10/04/2026**

TO WHOM IT MAY CONCERN

This is to certify that **Nilang Vipulkumar Jotaniya**, a student of **MBIT**, has successfully completed internship/project work in the field of **AI-enabled Student Support System Development** from **22/12/2025** to **10/04/2026** (Total duration: **16 weeks**) under the guidance of **Edunet Foundation (SAP) mentor team**.

During this period, the candidate worked on system analysis, backend API design, AI response pipeline integration, admin dashboard development, student portal implementation, and data management workflows.

We wish him/her every success in future.

For **Edunet Foundation (SAP)**  
Authorized Signature with Stamp

---

## Candidate's Declaration

I, **Nilang Vipulkumar Jotaniya (12202040701108)**, hereby declare that this Industrial Internship report submitted in partial fulfillment for the degree of Bachelor of Engineering in Computer Engineering, **MBIT**, The Charutar Vidya Mandal (CVM) University, Vallabh Vidyanagar, is a bonafide record of work carried out by me and no part of this report has been copied from any other report/source without due reference.

Signature: ____________________  
Date: **10/04/2026**

---

## Acknowledgement

I express my sincere gratitude to **Assistant Professor Mr. Dhruv Dalwadi**, **Dr. Gopi Bhatt**, and the faculty of **MBIT** for their valuable guidance and support throughout this internship/project.

I also thank **Edunet Foundation (SAP) mentor team** for technical direction and continuous review.

Finally, I thank my peers and family for their encouragement during planning, development, testing, and report preparation.

---

## Abstract

EduAgent AI is a student-support platform designed to provide instant academic assistance and institutional workflow automation through separate student and admin portals. The system combines a FastAPI backend, MongoDB data storage, and a local LLM pipeline to answer student queries related to fees, attendance, examinations, documents, and policies.

The project implements role-separated interfaces: (1) student portal for profile, fee overview, document access, reminders, and AI chat; (2) admin panel for FAQ management, escalation handling, document upload, exam/fee updates, and student master data maintenance. Additional features include enrollment-based authentication, helpfulness feedback tracking, document download tracking, reminder workflows, and CSV/XLSX/PDF student import support.

The outcome demonstrates that a practical college assistant can be built with modular architecture, secure role separation, and extensible data pipelines. The developed system reduces repetitive query handling and improves information access for students while giving administrators structured control over institutional data.

---

## List of Figures

- Fig 1.1 Overall System Architecture  
- Fig 1.2 Student Portal Navigation Flow  
- Fig 2.1 Admin Dashboard Module Layout  
- Fig 2.2 Data Flow for Student Query Handling  
- Fig 3.1 Reminder Notification Workflow  
- Fig 4.1 Document Upload and Download Tracking Flow

---

## List of Tables

- Table 1.1 Technology Stack and Purpose  
- Table 1.2 Functional Module Mapping  
- Table 2.1 API Endpoint Summary  
- Table 3.1 Test Cases and Results  
- Table 4.1 Performance and Response Observations

---

## List of Symbols, Abbreviations and Nomenclature

- AI: Artificial Intelligence  
- API: Application Programming Interface  
- FAQ: Frequently Asked Question  
- LLM: Large Language Model  
- DB: Database  
- UI: User Interface  
- UX: User Experience  
- CRUD: Create, Read, Update, Delete  
- JWT: JSON Web Token

---

## Table of Contents

1. Chapter 1 - Introduction and Project Overview  
2. Chapter 2 - Existing System Study and Problem Definition  
3. Chapter 3 - Proposed System and Design  
4. Chapter 4 - Implementation Details  
5. Chapter 5 - Testing and Validation  
6. Chapter 6 - Conclusion, Limitations and Future Scope  
7. References  
8. Appendix

---

# Chapter 1 - Introduction and Project Overview

## 1.1 Introduction
Educational institutions handle repetitive student queries about examinations, fees, attendance, and document access. Manual handling creates delays and inconsistency. EduAgent AI addresses this by combining AI-powered query response with structured admin workflows.

## 1.2 Purpose
- Provide instant academic query resolution for students.
- Reduce manual repetitive support workload.
- Enable admin control for FAQs, escalations, fees, exams, documents, and student records.

## 1.3 Objectives
- Build separate portals for students and admins.
- Support enrollment-number based student login.
- Integrate AI response generation with FAQ/document context.
- Maintain data consistency using MongoDB.
- Provide trackable actions (helpful votes, reminders, downloads).

## 1.4 Scope
### In Scope
- Student chat and profile dashboard
- Admin management modules
- PDF upload and access tracking
- Escalation queue and status updates

### Out of Scope (Current Version)
- Multi-factor authentication
- Full production CI/CD pipeline
- Enterprise SSO integration

## 1.5 Technology Stack
- Frontend: React + TypeScript + Vite
- Backend: FastAPI (Python)
- Database: MongoDB
- AI Runtime: Ollama local model

---

# Chapter 2 - Existing System Study and Problem Definition

## 2.1 Existing System
Traditional college support is mostly form-based/manual. Information is fragmented across notice boards, staff communication, PDFs, and separate portals.

## 2.2 Problems in Existing System
- Slow response time for common queries
- Duplicate effort for staff
- Lack of traceability for repeated questions
- Poor discoverability of documents

## 2.3 Requirements of New System
- Quick student query resolution
- Controlled admin content updates
- Role-based access separation
- Reliable student identity mapping via enrollment numbers

## 2.4 Feasibility
- Technical feasibility: High, using FastAPI + React + MongoDB
- Operational feasibility: High, workflow aligns with college support processes
- Economic feasibility: Moderate and scalable due open-source stack

---

# Chapter 3 - Proposed System and Design

## 3.1 Proposed Architecture
The platform follows a modular client-server architecture:
- Student frontend communicates with backend APIs for profile, fees, documents, reminders, chat
- Admin frontend manages institutional data through authenticated admin APIs
- Backend orchestrates data operations and AI response generation

## 3.2 Module Design
- Student Authentication and Profile
- Student Chat and Feedback
- Admin FAQ Management
- Escalation Management
- Document Library and Tracking
- Exam/Fee Data Management
- Student Master and Import

## 3.3 Database Design (Collections)
- `students`
- `faqs`
- `escalations`
- `exams`
- `fees` / `fee_ledger`
- `pdf_documents`
- `reminders`
- `download_events`

## 3.4 Security and Access Control
- Separate student token and admin password-protected flows
- Student-only data returned via token-bound APIs
- Admin-only mutation endpoints restricted by admin auth

---

# Chapter 4 - Implementation Details

## 4.1 Backend (FastAPI)
Major endpoint groups implemented:
- Student login/profile/fees/reminders/documents
- Chat API with FAQ/document-aware response generation
- Admin APIs for FAQs, escalations, exams, fees, PDF, students

## 4.2 Student Portal
Features delivered:
- Enrollment/password login
- Student details dashboard
- Fee and notice visibility
- Document center
- AI assistant chat with quick prompts

## 4.3 Admin Portal
Features delivered:
- Admin login and dashboard
- FAQ CRUD and feedback metrics
- Escalation status updates
- PDF upload and download event visibility
- Exam/Fee updates
- Student create/edit/import

## 4.4 Special Improvements Completed
- Removed student-side admin authority exposure
- Added "Back to Admin" navigation only as link
- Opening student site from admin launches fresh login session
- UI typography and layout alignment improved

---

# Chapter 5 - Testing and Validation

## 5.1 Testing Strategy
- Module-level API checks
- Frontend build-time validation (TypeScript + Vite)
- Role-based access path checks
- Functional workflow checks across student/admin routes

## 5.2 Sample Test Cases
- Student login with valid enrollment and password -> Pass
- Student cannot access admin CRUD endpoints -> Pass
- Admin can create/update student records -> Pass
- PDF upload and tracked student download events -> Pass
- Reminder sent by admin appears in student notifications -> Pass

## 5.3 Build/Compile Validation
- Student UI build: Pass
- Admin UI build: Pass
- Backend Python compile checks: Pass

## 5.4 Observed Issues and Fixes
- Sidebar authority confusion resolved by removing admin controls from student area
- Session carryover resolved using fresh-launch token reset (`?fresh=1` flow)
- Multiple UI regressions corrected with iterative route/nav restoration

---

# Chapter 6 - Conclusion, Limitations and Future Scope

## 6.1 Conclusion
EduAgent AI provides a practical, role-separated digital support platform for college operations. It successfully combines AI response capability with structured administrative management and improves student information accessibility.

## 6.2 Limitations
- Local model response quality depends on model size/hardware
- Production-grade identity federation not yet implemented
- Limited analytics/reporting dashboards

## 6.3 Future Scope
- SSO and stronger auth policies
- Rich analytics for question trends and performance
- Streamed AI responses and multilingual support
- Automated semester-wise report generation

---

## References / Bibliography

- FastAPI Official Documentation. https://fastapi.tiangolo.com  
- React Official Documentation. https://react.dev  
- MongoDB Documentation. https://www.mongodb.com/docs  
- Vite Documentation. https://vitejs.dev  
- Ollama Documentation. https://ollama.com

---

## Appendix (Optional)

### Appendix A - Major API Endpoints
(Include endpoint table from implementation)

### Appendix B - Screenshots
- Student Login Screen
- Student Details Dashboard
- Student Chat Page
- Admin Dashboard (FAQ/Escalations/PDF/Fees/Students)

### Appendix C - Internship Experience Notes
- Environment and support provided
- Team interaction and mentor guidance
- Challenges and resolutions
- Offer/continuation status (if applicable)

---

## Mandatory Formatting Checklist (As per provided format)

- Paper size: A4  
- Margins: Left 1.25", Right 1", Top 1", Bottom 1"  
- Font: Times New Roman  
- Regular text: 12 pt  
- Chapter heading: 16 pt bold all caps  
- Section heading: 14 pt bold all caps  
- Subsection heading: 12 pt bold leading caps  
- Black text for content  
- Page numbering: Roman for prelims, Arabic from Chapter 1  
- Hard bound black cover with golden letters (for hard copy)

