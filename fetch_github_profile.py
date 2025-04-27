import requests
import streamlit as st
import os

def fetch_github_profile(username):
    """Fetch GitHub profile information for the given username"""
    # Check if profile is cached
    if username in st.session_state.github_profiles:
        return st.session_state.github_profiles[username]

    try:
        # Make API requests
        profile_url = f"https://api.github.com/users/{username}"
        repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"

        profile_response = requests.get(profile_url)
        repos_response = requests.get(repos_url)

        if profile_response.status_code != 200:
            return {
                "error": f"Profile not found. Status code: {profile_response.status_code}"
            }

        profile_data = profile_response.json()
        repos_data = repos_response.json() if repos_response.status_code == 200 else []

        # Extract relevant information
        github_info = {
            "username": profile_data.get("login"),
            "name": profile_data.get("name"),
            "bio": profile_data.get("bio"),
            "avatar_url": profile_data.get("avatar_url"),
            "followers": profile_data.get("followers"),
            "following": profile_data.get("following"),
            "public_repos": profile_data.get("public_repos"),
            "location": profile_data.get("location"),
            "joined_at": profile_data.get("created_at"),
            "updated_at": profile_data.get("updated_at"),
            "html_url": profile_data.get("html_url"),
            "repos": [],
        }

        # Process repos
        language_counts = {}
        stargazers_total = 0
        fork_total = 0

        for repo in repos_data:
            github_info["repos"].append(
                {
                    "name": repo.get("name"),
                    "description": repo.get("description"),
                    "language": repo.get("language"),
                    "stars": repo.get("stargazers_count"),
                    "forks": repo.get("forks_count"),
                    "updated_at": repo.get("updated_at"),
                    "html_url": repo.get("html_url"),
                    "is_fork": repo.get("fork", False),
                }
            )

            # Count languages
            lang = repo.get("language")
            if lang:
                language_counts[lang] = language_counts.get(lang, 0) + 1

            # Count stars and forks
            stargazers_total += repo.get("stargazers_count", 0)
            fork_total += repo.get("forks_count", 0)

        # Add summary statistics
        github_info["language_counts"] = language_counts
        github_info["stargazers_total"] = stargazers_total
        github_info["fork_total"] = fork_total

        # Sort repos by stars
        github_info["repos"] = sorted(
            github_info["repos"], key=lambda x: x.get("stars", 0), reverse=True
        )

        # Cache the result
        st.session_state.github_profiles[username] = github_info

        return github_info

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
