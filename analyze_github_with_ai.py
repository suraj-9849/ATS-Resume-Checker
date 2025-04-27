import os
from dotenv import load_dotenv
import google.generativeai as genai
import os
from dotenv import load_dotenv
import google.generativeai as genai
def analyze_github_with_ai(github_info, resume_text=None, job_description=None):

    load_dotenv()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    """Use AI to analyze GitHub profile and optionally compare with resume and job description"""
    if "error" in github_info:
        return f"Error analyzing GitHub profile: {github_info['error']}"

    # Prepare GitHub summary text
    repos_text = "\n".join(
        [
            f"- {repo['name']}: {repo['description'] or 'No description'} (Language: {repo['language'] or 'Unknown'}, Stars: {repo['stars']}, Forks: {repo['forks']})"
            for repo in github_info["repos"][:10]  # Top 10 repos
        ]
    )

    languages_text = "\n".join(
        [
            f"- {lang}: {count} repos"
            for lang, count in sorted(
                github_info["language_counts"].items(), key=lambda x: x[1], reverse=True
            )
        ]
    )

    github_summary = f"""
    GitHub Profile Summary for {github_info['username']}:
    
    Bio: {github_info['bio'] or 'No bio provided'}
    Public Repositories: {github_info['public_repos']}
    Followers: {github_info['followers']}
    Following: {github_info['following']}
    Total Stars Received: {github_info['stargazers_total']}
    Total Forks Received: {github_info['fork_total']}
    
    Top Repositories:
    {repos_text}
    
    Programming Languages:
    {languages_text}
    """

    # Create AI prompt based on available information
    if resume_text and job_description:
        prompt = f"""
        You are GitHubAnalyzer, an expert in developer profiles and technical hiring. Please analyze the following GitHub profile and compare it with the resume and job description:
        
        1. Identify the developer's key strengths based on their GitHub activity.
        2. Compare the skills shown in GitHub with those mentioned in the resume.
        3. Identify any skills evident in GitHub projects that are missing from the resume.
        4. Evaluate how well the GitHub profile supports the job application for the given description.
        5. Provide 3-5 specific recommendations for improving how the GitHub profile and resume work together.
        6. Give a score out of 100 for how well the GitHub profile enhances their job application.
        
        {github_summary}
        
        Resume text: {resume_text}
        
        Job description: {job_description}
        """
    elif resume_text:
        prompt = f"""
        You are GitHubAnalyzer, an expert in developer profiles and technical hiring. Please analyze the following GitHub profile and compare it with the resume:
        
        1. Identify the developer's key strengths based on their GitHub activity.
        2. Compare the skills shown in GitHub with those mentioned in the resume.
        3. Identify any skills evident in GitHub projects that are missing from the resume.
        4. Provide 3-5 specific recommendations for improving how the GitHub profile and resume work together.
        5. Give a score out of 100 for how complete and impressive the GitHub profile is.
        
        {github_summary}
        
        Resume text: {resume_text}
        """
    else:
        prompt = f"""
        You are GitHubAnalyzer, an expert in developer profiles and technical hiring. Please analyze the following GitHub profile:
        
        1. Identify the developer's key strengths based on their GitHub activity.
        2. Evaluate the quality and completeness of their GitHub profile.
        3. Identify the most impressive aspects of their GitHub portfolio.
        4. Provide 3-5 specific recommendations for improving their GitHub profile.
        5. Give a score out of 100 for how complete and impressive the GitHub profile is.
        
        {github_summary}
        """

    # Get AI analysis
    response = model.generate_content(prompt)
    return response.text
