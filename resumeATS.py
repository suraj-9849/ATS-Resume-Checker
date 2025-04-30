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
    create_language_chart,
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

tab1, tab2, tab3 = st.tabs(
    [
        "Resume Analysis",
        "GitHub Analyzer",
        "Industry Insights",
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
