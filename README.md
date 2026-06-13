# 🚀 AI Resume Intelligence Platform

An intelligent resume analysis platform built using Python, Streamlit, SQLAlchemy, and NLP techniques.

The application helps job seekers evaluate how well their resumes match a specific job description by extracting skills from both documents, calculating a match score, identifying skill gaps, and recommending learning resources to improve their profile.

---

## 📌 Project Overview

Recruiters often receive hundreds of resumes for a single job opening, while applicants struggle to understand whether their skills align with job requirements.

This project aims to bridge that gap by providing an automated system that:

* Extracts skills from resumes and job descriptions
* Compares candidate skills with job requirements
* Calculates an ATS-style match score
* Identifies missing skills
* Suggests learning resources for improvement
* Stores previous analyses for future reference

---

## ✨ Features

### 🔐 User Management

* User Registration
* Secure Login System
* Password Hashing & Authentication

### 📄 Resume Processing

* Upload Resume (PDF/DOCX)
* Upload Job Description (PDF/DOCX)
* Resume Text Extraction
* Job Description Parsing

### 🤖 Skill Analysis

* Automatic Skill Extraction
* Resume vs JD Comparison
* Match Score Calculation
* Skill Gap Identification
* ATS Compatibility Assessment

### 📚 Learning Recommendations

* Recommended Skills Based on Missing Areas
* Tutorial Links for Learning
* Skill Completion Tracking

### 📂 Resume Library

* Store Previously Analyzed Resumes
* View Historical Match Scores
* Search and Filter Resumes
* Re-analyze Existing Resumes

### 📊 Dashboard

* Resume Statistics
* Analysis Overview
* User Activity Summary

---

## 🛠️ Tech Stack

| Category        | Technologies            |
| --------------- | ----------------------- |
| Frontend        | Streamlit               |
| Backend         | Python                  |
| Database        | SQLite, SQLAlchemy      |
| NLP             | Custom Skill Extraction |
| File Processing | PDFPlumber, python-docx |
| Authentication  | Passlib, Bcrypt         |

---

## 📸 Application Screenshots

### Dashboard

*(<img width="1886" height="886" alt="image" src="https://github.com/user-attachments/assets/5eb53e72-34dc-4758-982d-0298621d7ef5" />
)*

### Resume Analysis

*(<img width="1848" height="710" alt="image" src="https://github.com/user-attachments/assets/10ce54ff-6e99-43d1-b0be-52ad3fad32f5" />
)*

### Resume Library

*(<img width="1807" height="900" alt="image" src="https://github.com/user-attachments/assets/b4d0b832-31d7-4b48-bd65-683ccaa464af" />
)**(<img width="1837" height="873" alt="image" src="https://github.com/user-attachments/assets/89b78af4-0a35-43ee-b819-ae6c1010a0ab" />
)

### Learning Recommendations

*(<img width="1830" height="822" alt="image" src="https://github.com/user-attachments/assets/3e7a9e83-ef11-4816-a290-2a2723c19685" />
)*

---

## 📂 Project Structure

```text
AI-Resume-Intelligence-Platform/
│
├── auth/
├── backend/
│   ├── ai/
│   ├── matching/
│   ├── parsers/
│   ├── preprocessing/
│   └── skills/
│
├── database/
├── ui/
├── uploads/
│
├── app.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Clone the Repository

```bash
git clone https://github.com/Madhurima776/AI-Resume-Intelligence-Platform.git
cd AI-Resume-Intelligence-Platform
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app.py
```

---

## 🎯 Future Enhancements

The current version focuses on resume analysis from a job seeker's perspective.

Planned improvements include:

* Semantic Skill Matching using LLMs
* Recruiter Dashboard
* Bulk Resume Screening
* Candidate Ranking System
* Resume Improvement Suggestions
* Interview Question Generation
* Analytics & Visualization Dashboard
* Cloud Deployment

---

## 👩‍💻 Author

**Nissy Madhurima**

B.Tech Student | AI & Data Science Enthusiast | Python Developer

This project was developed as part of my learning journey in Artificial Intelligence, NLP, and Full-Stack Application Development.


---

## 📜 License

This project is licensed under the MIT License.
