import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from PyPDF2 import PdfReader

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_output(pdf_text, prompt):
    response = model.generate_content([pdf_text, prompt])
    return response.text

def read_pdf(uploaded_file):
    if uploaded_file is not None:
        pdf_reader = PdfReader(uploaded_file)
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
        return pdf_text
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="ATS Resume Checker", layout="wide")

st.markdown("""
    <style>
    .main {
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        transition: 0.3s;
        border: none;
    }
    .stButton>button:hover {
        background-color: #333;
        color: #f1f1f1;
    }
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea {
        border-radius: 8px;
        border: 1px solid #ccc;
        padding: 8px;
        font-size: 14px;
    }
    .stRadio>div {
        padding: 10px;
        border-radius: 10px;
    }
    .stFileUploader>div>div {
        border: 2px dashed #555 !important;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)


st.title("ATS Resume Checker")
st.subheader("Optimize Your Resume for ATS and Land Your Dream Job")

upload_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

job_description = st.text_area("Enter the job description (optional)")

analysis_option = st.radio("Choose analysis type:", 
                           ["Quick Scan", "Detailed Analysis", "ATS Optimization"])

if st.button("Analyze Resume"):
    if upload_file is not None:
        pdf_text = read_pdf(upload_file)
        
        if analysis_option == "Quick Scan":
            prompt = f"""
            You are ResumeChecker, an expert in resume analysis. Provide a quick scan of the following resume:
            
            1. Identify the most suitable profession for this resume.
            2. List 3 key strengths of the resume.
            3. Suggest 2 quick improvements.
            4. Give an overall ATS score out of 100.
            
            Resume text: {pdf_text}
            Job description (if provided): {job_description}
            """
        elif analysis_option == "Detailed Analysis":
            prompt = f"""
            You are ResumeChecker, an expert in resume analysis. Provide a detailed analysis of the following resume:
            
            1. Identify the most suitable profession for this resume.
            2. List 5 strengths of the resume.
            3. Suggest 3-5 areas for improvement with specific recommendations.
            4. Rate the following aspects out of 10: Impact, Brevity, Style, Structure, Skills.
            5. Provide a brief review of each major section (e.g., Summary, Experience, Education).
            6. Give an overall ATS score out of 100 with a breakdown of the scoring.
            
            Resume text: {pdf_text}
            Job description (if provided): {job_description}
            """
        else: 
            prompt = f"""
            You are ResumeChecker, an expert in ATS optimization. Analyze the following resume and provide optimization suggestions:
            
            1. Identify keywords from the job description that should be included in the resume.
            2. Suggest reformatting or restructuring to improve ATS readability.
            3. Recommend changes to improve keyword density without keyword stuffing.
            4. Provide 3-5 bullet points on how to tailor this resume for the specific job description.
            5. Give an ATS compatibility score out of 100 and explain how to improve it.
            
            Resume text: {pdf_text}
            Job description: {job_description}
            """
        
        response = get_gemini_output(pdf_text, prompt)
        
        st.subheader("Analysis Results")
        st.write(response)
    else:
        st.error("Please upload a resume to analyze.")

st.sidebar.title("Resources")
st.sidebar.markdown("""
- [Resume Writing Tips](https://cdn-careerservices.fas.harvard.edu/wp-content/uploads/sites/161/2023/08/College-resume-and-cover-letter-4.pdf)
- [ATS Optimization Guide](https://career.io/career-advice/create-an-optimized-ats-resume)
- [Interview Preparation](https://hbr.org/2021/11/10-common-job-interview-questions-and-how-to-answer-them)
""")

st.sidebar.title("Feedback")
st.sidebar.text_area("Help us improve! Leave your feedback:")
st.sidebar.button("Submit Feedback")
