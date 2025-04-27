
import re
import os
def detect_industry(resume_text):
    """Detect the likely industry of the resume"""
    industry_keywords = {
        "Technology": [
            "software",
            "developer",
            "programming",
            "IT",
            "web",
            "computer",
            "engineer",
            "code",
            "agile",
            "scrum",
            "devops",
            "cloud",
            "aws",
            "azure",
            "api",
        ],
        "Healthcare": [
            "patient",
            "medical",
            "clinical",
            "nurse",
            "doctor",
            "health",
            "care",
            "hospital",
            "physician",
            "therapy",
        ],
        "Finance": [
            "finance",
            "accounting",
            "audit",
            "budget",
            "financial",
            "investment",
            "banking",
            "tax",
            "revenue",
        ],
        "Marketing": [
            "marketing",
            "brand",
            "digital",
            "content",
            "social media",
            "campaign",
            "SEO",
            "market",
            "advertising",
        ],
        "Education": [
            "teach",
            "education",
            "course",
            "student",
            "curriculum",
            "school",
            "professor",
            "instructor",
            "academic",
        ],
        "Engineering": [
            "engineering",
            "mechanical",
            "electrical",
            "civil",
            "design",
            "CAD",
            "technical",
        ],
    }

    resume_lower = resume_text.lower()
    industry_scores = {}

    for industry, keywords in industry_keywords.items():
        score = 0
        for keyword in keywords:
            if re.search(r"\b" + re.escape(keyword) + r"\b", resume_lower):
                score += 1
        industry_scores[industry] = score

    # Get top industry
    top_industry = max(industry_scores.items(), key=lambda x: x[1])

    # Only return if score is significant
    if top_industry[1] > 2:
        return top_industry[0]
    else:
        return "General"

