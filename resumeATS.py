import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd
from adv import resume_analyser
from analyze_github_with_ai import analyze_github_with_ai
from create_activity_tab import create_activity_chart
from create_word_count import create_word_cloud
from detect_industry import detect_industry
from fetch_github_profile import fetch_github_profile
from functions import (
    calculate_match_score,
    format_checker,
    generate_resume_heatmap,
    get_industry_advice,
)
from get_gemini_output import get_gemini_output
import re
from githubfn import githubfn
import plotly.express as px 
import uuid
import matplotlib.pyplot as plt
from read_pdf import read_pdf 
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize session state for resume versions
if "resume_versions" not in st.session_state:
    st.session_state.resume_versions = {}

# Initialize session state for GitHub profile cache
if "github_profiles" not in st.session_state:
    st.session_state.github_profiles = {}

# Streamlit UI
st.set_page_config(page_title="Advanced ATS Resume Checker", layout="wide")

st.markdown(
    """
    <style>
    .main {
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        color: white;
        background-color: #4CAF50;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        transition: 0.3s;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
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
    .highlight {
        background-color: #FFFF99;
        padding: 2px;
        border-radius: 3px;
    }
    .keyword-match {
        background-color: #c8e6c9;
        padding: 2px 5px;
        border-radius: 3px;
        margin: 2px;
        display: inline-block;
    }
    .keyword-missing {
        background-color: #ffcdd2;
        padding: 2px 5px;
        border-radius: 3px;
        margin: 2px;
        display: inline-block;
    }
    .stat-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .tab-content {
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 0 0 10px 10px;
    }
    h3 {
        color: #2C3E50;
    }
    .repo-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        # background-color: #f9f9f9;
    }
    .github-stats {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
    }
    .github-stat-item {
        text-align: center;
        margin: 10px;
        padding: 15px;
        border-radius: 10px;
        # background-color: #f0f0f0;
        min-width: 120px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🚀 Advanced ATS Resume Checker")
st.subheader("Optimize Your Resume and Land Your Dream Job")

tab1, tab2, tab3,tab4 = st.tabs(
    [
        "Resume Analysis",
        "GitHub Analyzer",
        "Industry Insights",
        "Analyse"
    ]
)
with tab1:
    resume_analyser()
with tab2:
  githubfn()

with tab3:
    st.header("Industry Insights")

    industries = [
        "Technology",
        "Healthcare",
        "Finance",
        "Marketing",
        "Education",
        "Engineering",
        "General",
    ]
    selected_industry = st.selectbox("Select your industry", industries)

    st.markdown(f"### Top Skills for {selected_industry}")

    industry_skills = {
        "Technology": [
            "Programming Languages",
            "Cloud Computing",
            "DevOps",
            "Machine Learning",
            "Database Management",
            "API Development",
            "Software Architecture",
            "Agile Methodologies",
            "Version Control",
            "Cybersecurity",
        ],
        "Healthcare": [
            "Patient Care",
            "Medical Terminology",
            "Electronic Health Records",
            "Clinical Procedures",
            "HIPAA Compliance",
            "Care Coordination",
            "Medical Coding",
            "Healthcare IT Systems",
            "Case Management",
            "Treatment Planning",
        ],
        "Finance": [
            "Financial Analysis",
            "Accounting",
            "Risk Management",
            "Financial Modeling",
            "Regulatory Compliance",
            "Budgeting",
            "Forecasting",
            "Investment Management",
            "Banking Systems",
            "Financial Reporting",
        ],
        "Marketing": [
            "Digital Marketing",
            "SEO/SEM",
            "Content Strategy",
            "Social Media Management",
            "Analytics",
            "Brand Development",
            "Campaign Management",
            "Market Research",
            "CRM Software",
            "Copywriting",
        ],
        "Education": [
            "Curriculum Development",
            "Instructional Design",
            "Student Assessment",
            "Classroom Management",
            "Educational Technology",
            "Differentiated Instruction",
            "Learning Management Systems",
            "Student Engagement",
            "Education Policy",
            "Lesson Planning",
        ],
        "Engineering": [
            "CAD Software",
            "Project Management",
            "Technical Documentation",
            "Quality Control",
            "Systems Analysis",
            "Design Verification",
            "Prototyping",
            "Manufacturing Processes",
            "Structural Analysis",
            "Compliance Standards",
        ],
        "General": [
            "Project Management",
            "Communication",
            "Leadership",
            "Microsoft Office",
            "Data Analysis",
            "Problem-Solving",
            "Team Collaboration",
            "Customer Service",
            "Strategic Planning",
            "Process Improvement",
        ],
    }

    skills = industry_skills.get(selected_industry, industry_skills["General"])

    # Display skills in two columns
    col1, col2 = st.columns(2)

    for i, skill in enumerate(skills):
        if i < len(skills) // 2:
            col1.markdown(f"✅ **{skill}**")
        else:
            col2.markdown(f"✅ **{skill}**")

    st.markdown(f"### Resume Tips for {selected_industry}")
    st.markdown(get_industry_advice(selected_industry))

    st.markdown("### ATS Optimization Tips")
    st.markdown(
        """
    1. **Use standard section headings** - "Experience", "Education", "Skills" rather than creative alternatives
    2. **Match keywords exactly** as they appear in the job description
    3. **Use a clean, single-column layout** with standard fonts
    4. **Avoid headers/footers, tables, and text boxes** - they often confuse ATS systems
    5. **Include your full contact information** at the top of the first page
    6. **Save your file as a standard PDF** format
    7. **Use bullet points** rather than paragraphs for experience descriptions
    8. **Quantify achievements** with numbers and percentages when possible
    """
    )


with tab4:
    col1, col2 = st.columns([3, 2])

    with col1:
        upload_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

        job_description = st.text_area("Enter the job description", height=200)

        analysis_option = st.radio(
            "Choose analysis type:",
            ["Quick Scan", "Detailed Analysis", "ATS Optimization", "Formatting Check"],
        )

        version_name = st.text_input(
            "Save this analysis as (optional)",
            placeholder="e.g., Software Developer - Google",
        )

        analyze_button = st.button("Analyze Resume", key="analyze")

    with col2:
        st.markdown("### How It Works")
        st.write(
            """
        1. Upload your resume in PDF format
        2. Paste the job description you're applying for
        3. Choose your preferred analysis type
        4. Get detailed feedback to improve your chances!
        """
        )

        st.markdown("### Why Use Our ATS Checker?")
        st.write(
            """
        - **AI-Powered Analysis**: Get insights beyond basic keyword matching
        - **Visual Feedback**: See which parts of your resume need improvement
        - **Industry-Specific Advice**: Tailored recommendations for your field
        - **Track Improvements**: Save multiple versions to measure progress
        """
        )

    # Process and display results
    if analyze_button and upload_file is not None:
        with st.spinner("Analyzing your resume..."):
            pdf_text = read_pdf(upload_file)

            # Store the version if name provided
            if version_name:
                version_id = str(uuid.uuid4())[:8]
                st.session_state.resume_versions[version_id] = {
                    "name": version_name,
                    "text": pdf_text,
                    "job_description": job_description,
                    "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
                }
                st.success(f"Saved as '{version_name}'")

            # Basic info extraction
            industry = detect_industry(pdf_text)
            formatting_issues = format_checker(pdf_text)

            # Calculate match score if job description provided
            match_score = None
            if job_description:
                match_score, matched_keywords, missing_keywords = calculate_match_score(
                    pdf_text, job_description
                )
                heatmap_data = generate_resume_heatmap(pdf_text, matched_keywords)

            # Get AI analysis
            if analysis_option == "Quick Scan":
                prompt = f"""
                You are ResumeChecker, an expert in resume analysis. Provide a quick scan of the following resume:
                
                1. Identify the most suitable profession for this resume.
                2. List 3 key strengths of the resume.
                3. Suggest 2 quick improvements.
                4. Give an overall ATS score out of 100.
                
                Resume text: {pdf_text}
                Job description (if provided): {job_description}
                Industry detected: {industry}
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
                Industry detected: {industry}
                """
            elif analysis_option == "ATS Optimization":
                prompt = f"""
                You are ResumeChecker, an expert in ATS optimization. Analyze the following resume and provide optimization suggestions:
                
                1. Identify keywords from the job description that should be included in the resume.
                2. Suggest reformatting or restructuring to improve ATS readability.
                3. Recommend changes to improve keyword density without keyword stuffing.
                4. Provide 3-5 bullet points on how to tailor this resume for the specific job description.
                5. Give an ATS compatibility score out of 100 and explain how to improve it.
                
                Resume text: {pdf_text}
                Job description: {job_description}
                Industry detected: {industry}
                """
            else:  # Formatting Check
                prompt = f"""
                You are ResumeChecker, an expert in resume formatting. Provide an analysis of the following resume's formatting:
                
                1. Identify any formatting issues that might cause problems with ATS systems.
                2. Suggest improvements to the resume structure and layout.
                3. Comment on the use of sections, bullet points, and whitespace.
                4. Provide specific reformatting suggestions.
                5. Rate the overall formatting quality out of 10.
                
                Resume text: {pdf_text}
                Formatting issues detected: {formatting_issues}
                """

            response = get_gemini_output(pdf_text, prompt)

            # Display results
            st.subheader("Analysis Results")

            # Show match score if available
            if match_score is not None:
                st.markdown(f"### 📊 Resume-Job Description Match: {match_score:.1f}%")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("#### ✅ Matched Keywords")
                    keyword_html = ""
                    for keyword in matched_keywords:
                        keyword_html += f'<span  class="keyword-match">{keyword}</span>'
                    st.markdown(keyword_html, unsafe_allow_html=True)

                with col2:
                    st.markdown("#### ❌ Missing Keywords")
                    keyword_html = ""
                    for keyword in missing_keywords:
                        keyword_html += (
                            f'<span  class="keyword-missing">{keyword}</span>'
                        )
                    st.markdown(keyword_html, unsafe_allow_html=True)

                # Display heatmap if we have data
                if "heatmap_data" in locals():
                    st.markdown("### 🔥 Resume Heatmap")
                    st.write(
                        "This visualization shows which sections of your resume match keywords from the job description."
                    )

                    fig = px.bar(
                        heatmap_data,
                        x="score",
                        y="section",
                        labels={"score": "Match Score", "section": "Resume Section"},
                        color="score",
                        color_continuous_scale=["red", "yellow", "green"],
                        title="Keyword Match by Resume Section",
                        orientation="h",
                    )

                    st.plotly_chart(fig, use_container_width=True)

            # Display main analysis
            st.markdown("### 📝 Expert Analysis")
            st.markdown(response)

            # Display industry-specific advice
            st.markdown(f"### 🏢 {industry} Industry Tips")
            st.markdown(get_industry_advice(industry))

            # Display formatting issues
            if formatting_issues:
                st.markdown("### ⚠️ Formatting Issues")
                for issue in formatting_issues:
                    st.warning(issue)

            # Create visual word cloud
            st.markdown("### 📊 Resume Keywords")
            word_cloud_fig = create_word_cloud(pdf_text)
            st.pyplot(word_cloud_fig)
   