import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd
from analyze_github_with_ai import analyze_github_with_ai
from create_activity_tab import create_activity_chart
from fetch_github_profile import fetch_github_profile
from functions import (
    create_language_chart,
)
import uuid
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


def githubfn():
    st.header("🔎 GitHub Profile Analyzer")

    st.markdown(
        """
    ### Enhance Your Resume with GitHub Analysis
    
    Your GitHub profile is a powerful portfolio that showcases your coding skills and projects.
    Let's analyze your GitHub profile to identify strengths that complement your resume!
    """
    )

    # Setup UI columns
    col1, col2 = st.columns([2, 3])

    with col1:
        # Input GitHub username
        github_username = st.text_input("Enter GitHub Username")

        # Option to use resume from tab 1
        use_resume = st.checkbox("Use resume from Resume Analysis tab", value=True)

        # Select resume version if available
        resume_version_id = None
        resume_text = None
        job_desc = None

        if use_resume and st.session_state.resume_versions:
            resume_version_id = st.selectbox(
                "Select resume version",
                options=list(st.session_state.resume_versions.keys()),
                format_func=lambda x: st.session_state.resume_versions[x]["name"],
            )

            if resume_version_id:
                resume_text = st.session_state.resume_versions[resume_version_id][
                    "text"
                ]
                job_desc = st.session_state.resume_versions[resume_version_id][
                    "job_description"
                ]

        # Option to upload a resume directly in this tab
        if not use_resume:
            upload_resume_file = st.file_uploader(
                "Upload your resume (PDF)", type=["pdf"], key="github_resume_upload"
            )
            job_desc = st.text_area(
                "Job Description (optional)", height=100, key="github_job_desc"
            )

            if upload_resume_file:
                resume_text = read_pdf(upload_resume_file)

        # Analysis button
        analyze_github_button = st.button(
            "Analyze GitHub Profile", key="analyze_github"
        )

    with col2:
        st.markdown("### Benefits of GitHub Profile Analysis")
        st.write(
            """
        - **Identify Skill Gaps**: See if your GitHub projects showcase skills that are missing from your resume
        - **Showcase Your Best Work**: Highlight projects that are most relevant to job applications
        - **Technical Credibility**: Demonstrate coding ability beyond what's stated in your resume
        - **Bridge the Resume-Code Gap**: Ensure your GitHub profile reinforces your resume claims
        """
        )

        st.info(
            """
        **Pro Tip**: Technical recruiters and hiring managers often check candidates' GitHub profiles
        to validate their technical skills and see real code examples. Make sure your profile is optimized!
        """
        )

    # Process and display results after button click
    if analyze_github_button and github_username:
        with st.spinner("Analyzing GitHub profile..."):
            # Fetch GitHub profile
            github_info = fetch_github_profile(github_username)

            # Check for errors
            if "error" in github_info:
                st.error(f"Error: {github_info['error']}")
            else:
                # Display profile summary
                st.subheader("GitHub Profile Summary")

                # Profile header with image and basic info
                col1, col2 = st.columns([1, 3])

                with col1:
                    st.image(github_info["avatar_url"], width=150)

                with col2:
                    st.markdown(
                        f"### [{github_info['name'] or github_info['username']}]({github_info['html_url']})"
                    )
                    if github_info["bio"]:
                        st.markdown(f"*{github_info['bio']}*")
                    st.markdown(
                        f"📍 Location: {github_info['location'] or 'Not specified'}"
                    )
                    st.markdown(f"🗓️ Joined: {github_info['joined_at'][:10]}")

                # GitHub stats
                st.markdown("### 📊 GitHub Statistics")

                stat_cols = st.columns(4)
                with stat_cols[0]:
                    st.markdown(
                        f"""
                    <div  class="github-stat-item">
                        <h3>{github_info['public_repos']}</h3>
                        <p>Repositories</p>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                with stat_cols[1]:
                    st.markdown(
                        f"""
                    <div  class="github-stat-item">
                        <h3>{github_info['followers']}</h3>
                        <p>Followers</p>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                with stat_cols[2]:
                    st.markdown(
                        f"""
                    <div  class="github-stat-item">
                        <h3>{github_info['stargazers_total']}</h3>
                        <p>Total Stars</p>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                with stat_cols[3]:
                    st.markdown(
                        f"""
                    <div  class="github-stat-item">
                        <h3>{github_info['fork_total']}</h3>
                        <p>Total Forks</p>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                # Top repositories
                st.markdown("### 🏆 Top Repositories")
                top_repos = github_info["repos"][:5]  # Show top 5 repos

                for repo in top_repos:
                    st.markdown(
                        f"""
                    <div  class="repo-card">
                        <h4><a href="{repo['html_url']}" target="_blank">{repo['name']}</a></h4>
                        <p>{repo['description'] or 'No description available'}</p>
                        <p>
                            <strong>Language:</strong> {repo['language'] or 'Not specified'} | 
                            <strong>Stars:</strong> {repo['stars']} | 
                            <strong>Forks:</strong> {repo['forks']} | 
                            <strong>Last updated:</strong> {repo['updated_at'][:10]}
                        </p>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                # Language visualization
                st.markdown("### 💻 Programming Languages")

                lang_cols = st.columns(2)

                with lang_cols[0]:
                    # Language chart
                    lang_chart = create_language_chart(github_info)
                    if lang_chart:
                        st.pyplot(lang_chart)
                    else:
                        st.info("No language data available")

                with lang_cols[1]:
                    activity_chart = create_activity_chart(github_info)
                    if activity_chart:
                        st.pyplot(activity_chart)
                    else:
                        st.info("Not enough repository data available")

                # AI analysis
                st.markdown("### 🤖 AI Analysis")

                with st.spinner("Generating AI insights..."):
                    ai_analysis = analyze_github_with_ai(
                        github_info, resume_text, job_desc
                    )
                    st.markdown(ai_analysis)

                # Recommendations section
                st.markdown("### 🚀 GitHub Profile Optimization")

                st.markdown(
                    """
                #### General Recommendations:
                
                1. **Pin Your Best Repositories**: Make sure your most impressive and relevant projects are pinned to the top
                2. **Complete README Files**: Each repository should have a detailed README with project description, screenshots, and setup instructions
                3. **Consistent Contributions**: Regular activity shows dedication and ongoing skill development
                4. **Clean Code**: Ensure your repositories showcase good coding practices and documentation
                5. **Link to Live Demos**: Where applicable, provide links to live versions of your projects
                """
                )

                # Save analysis option
                save_analysis = st.checkbox("Save this GitHub analysis")
                if save_analysis:
                    analysis_name = st.text_input(
                        "Analysis name", value=f"GitHub Analysis - {github_username}"
                    )
                    if st.button("Save Analysis"):
                        # Create a unique ID for this analysis
                        analysis_id = str(uuid.uuid4())[:8]

                        # Store in session state - we could create a new session state variable for GitHub analyses
                        if "github_analyses" not in st.session_state:
                            st.session_state.github_analyses = {}

                        st.session_state.github_analyses[analysis_id] = {
                            "name": analysis_name,
                            "github_username": github_username,
                            "github_info": github_info,
                            "ai_analysis": ai_analysis,
                            "resume_id": resume_version_id,
                            "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
                        }

                        st.success(f"Analysis saved as '{analysis_name}'")
