# app.py
import streamlit as st
import docx2txt
import PyPDF2
import re

# --- Function to extract text from PDF ---
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# --- Function to extract text from DOCX ---
def extract_text_from_docx(docx_file):
    return docx2txt.process(docx_file)

# --- Function to calculate match score ---
def calculate_score(resume_text, job_desc):
    resume_text = resume_text.lower()
    job_desc = job_desc.lower()
    job_keywords = re.findall(r'\w+', job_desc)

    matched_keywords = [word for word in job_keywords if word in resume_text]
    score = (len(matched_keywords) / len(set(job_keywords))) * 100 if job_keywords else 0
    return round(score, 2), set(matched_keywords)

# --- Streamlit UI ---
st.title("📄 Resume Screening App")

job_description = st.text_area("Paste Job Description Here:")

uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])

if uploaded_file and job_description:
    if uploaded_file.type == "application/pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    else:
        resume_text = extract_text_from_docx(uploaded_file)

    st.subheader("Resume Text Preview")
    st.write(resume_text[:500] + "..." if len(resume_text) > 500 else resume_text)

    score, matched_keywords = calculate_score(resume_text, job_description)
    st.subheader("📊 Match Score")
    st.write(f"✅ Resume matches {score}% of Job Description")

    st.subheader("🔑 Matched Keywords")
    st.write(", ".join(matched_keywords))