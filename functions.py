import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import matplotlib.pyplot as plt

# Download NLTK resources
try:
    nltk.data.find("tokenizers/punkt")
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("punkt")
    nltk.download("stopwords")

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize session state for resume versions
if "resume_versions" not in st.session_state:
    st.session_state.resume_versions = {}

# Initialize session state for GitHub profile cache
if "github_profiles" not in st.session_state:
    st.session_state.github_profiles = {}


def extract_keywords(text):
    """Extract important keywords from text after removing stopwords"""
    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(text.lower())
    filtered_words = [
        word for word in word_tokens if word.isalpha() and word not in stop_words
    ]

    # Count frequency
    word_freq = {}
    for word in filtered_words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1

    # Sort by frequency
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return sorted_words[:25]  # Return top 25 keywords


def calculate_match_score(resume_text, job_description):
    """Calculate percentage match between resume and job description"""
    if not job_description:
        return None, []

    # Extract keywords from job description
    job_keywords = extract_keywords(job_description)
    job_words = [word[0] for word in job_keywords]

    # Check which keywords are in resume
    resume_lower = resume_text.lower()
    matched_keywords = []
    missing_keywords = []

    for word in job_words:
        if re.search(r"\b" + re.escape(word) + r"\b", resume_lower):
            matched_keywords.append(word)
        else:
            missing_keywords.append(word)

    # Calculate match percentage
    if len(job_words) > 0:
        match_percentage = (len(matched_keywords) / len(job_words)) * 100
    else:
        match_percentage = 0

    return match_percentage, matched_keywords, missing_keywords


def generate_resume_heatmap(resume_text, matched_keywords):
    """Generate data for a heatmap visualization of the resume"""
    paragraphs = resume_text.split("\n\n")
    scores = []

    for i, para in enumerate(paragraphs):
        if not para.strip():
            continue

        matches = 0
        for keyword in matched_keywords:
            if re.search(r"\b" + re.escape(keyword) + r"\b", para.lower()):
                matches += 1

        score = matches / len(matched_keywords) if matched_keywords else 0
        scores.append(
            {
                "section": f"Section {i+1}",
                "text": para[:50] + "..." if len(para) > 50 else para,
                "score": score,
            }
        )

    return pd.DataFrame(scores)


def format_checker(pdf_text):
    """Check for common formatting issues in resumes"""
    issues = []

    # Check for common formatting issues
    if len(pdf_text.split("\n\n")) < 3:
        issues.append(
            "Possible formatting issue: Text extraction found few paragraph breaks. This could indicate problems with PDF formatting."
        )

    # Check for potential table structures
    if pdf_text.count("|") > 5 or pdf_text.count("\t") > 10:
        issues.append(
            "Possible tables detected. ATS systems often struggle with tables."
        )

    # Check for bullet point consistency
    bullet_types = [chr(8226), "-", "*", "•", "○", "►", "✓", "➢"]
    used_bullets = [b for b in bullet_types if b in pdf_text]
    if len(used_bullets) > 1:
        issues.append(
            f"Multiple bullet point styles detected ({', '.join(used_bullets)}). Consider standardizing."
        )

    # Check for typical section headers
    if not re.search(r"\b(experience|work|employment)\b", pdf_text.lower()):
        issues.append("No clear 'Experience' section detected.")

    if not re.search(r"\b(education|degree|university|college)\b", pdf_text.lower()):
        issues.append("No clear 'Education' section detected.")

    if not re.search(r"\b(skills|abilities|competencies)\b", pdf_text.lower()):
        issues.append("No clear 'Skills' section detected.")

    return issues


def get_industry_advice(industry):
    """Get industry-specific advice"""
    advice = {
        "Technology": """
        - Emphasize technical skills and list programming languages
        - Include GitHub/portfolio links
        - Highlight specific technical achievements with metrics
        - List certifications and notable projects
        """,
        "Healthcare": """
        - Include all relevant licenses and certifications prominently
        - Emphasize patient care metrics and outcomes
        - Highlight experience with specific medical systems/software
        - Include continuing education and specialized training
        """,
        "Finance": """
        - Quantify achievements with specific numbers and percentages
        - Highlight regulatory compliance knowledge
        - Emphasize analytical and technical financial skills
        - Include relevant certifications (CPA, CFA, etc.)
        """,
        "Marketing": """
        - Include specific campaign results and metrics
        - Highlight experience with marketing tools and platforms
        - Showcase creativity and strategic thinking examples
        - Include portfolio or examples of successful campaigns
        """,
        "Education": """
        - Highlight teaching philosophy and methodologies
        - Include student achievement metrics
        - List curriculum development experience
        - Emphasize classroom management skills
        """,
        "Engineering": """
        - Detail specific projects with technical specifications
        - List all relevant software proficiencies
        - Include certifications and technical standards knowledge
        - Quantify project outcomes and efficiency improvements
        """,
    }

    if industry in advice:
        return advice[industry]
    else:
        return """
        - Quantify achievements with specific metrics
        - Use action verbs to begin bullet points
        - Target skills specifically mentioned in job descriptions
        - Keep formatting clean and consistent
        """


def create_language_chart(github_info):
    """Create chart of programming languages used"""
    if "error" in github_info or not github_info.get("language_counts"):
        return None

    # Prepare data
    languages = list(github_info["language_counts"].keys())
    counts = list(github_info["language_counts"].values())

    # Create pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(counts, labels=languages, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    plt.title("Programming Languages Distribution")

    return fig
