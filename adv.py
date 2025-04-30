import os
import streamlit as st
import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import PyPDF2
import google.generativeai as genai
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv

load_dotenv()
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)


def resume_analyser():
    st.session_state.page_config_set = True
    st.markdown(
        """
    <style>
        .main-header {
            font-size: 2.5rem;
            color: #1E3A8A;
            text-align: center;
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid #E5E7EB;
        }
        .sub-header {
            font-size: 1.5rem;
            color: #1E3A8A;
            margin-top: 1rem;
            margin-bottom: 0.5rem;
        }
        .card {
            background-color: #F9FAFB;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .success-text {
            color: #059669;
            font-weight: bold;
        }
        .warning-text {
            color: #D97706;
            font-weight: bold;
        }
        .error-text {
            color: #DC2626;
            font-weight: bold;
        }
        .info-card {
            background-color: #EFF6FF;
            border-left: 5px solid #3B82F6;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .result-container {
            padding: 20px;
            border-radius: 10px;
            background-color: #F3F4F6;
            margin-top: 20px;
        }
        .footer {
            text-align: center;
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid #E5E7EB;
            color: #6B7280;
            font-size: 0.8rem;
        }
        .stButton>button {
            background-color: #2563EB;
            color: white;
            font-weight: bold;
            padding: 0.5rem 2rem;
            border-radius: 5px;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )
    def extract_text_from_pdf(pdf_file):
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
        
    def preprocess_text(text):
        text = text.lower()

        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\d+", " ", text)

        tokens = word_tokenize(text)
        stop_words = set(stopwords.words("english"))
        filtered_tokens = [word for word in tokens if word not in stop_words]

        return " ".join(filtered_tokens)
        
    def calculate_keyword_match(resume_text, job_description):
        job_desc_processed = preprocess_text(job_description)
        job_keywords = set(job_desc_processed.split())
        resume_processed = preprocess_text(resume_text)
        resume_words = set(resume_processed.split())

        matching_keywords = job_keywords.intersection(resume_words)

        if len(job_keywords) > 0:
            match_percentage = (len(matching_keywords) / len(job_keywords)) * 100
        else:
            match_percentage = 0

        return match_percentage, list(matching_keywords)

    def get_ai_analysis(resume_text, job_description):
        prompt = f"""
        Analyze the resume against the job description below and provide:
        1. A score from 0-100 indicating how well the resume matches the job requirements
        2. Top 3 strengths of the candidate for this role
        3. Top 3 gaps or missing skills
        4. Brief recommendation (2-3 sentences)
        
        Format the response as a JSON with the following keys: score, strengths, gaps, recommendation
        
        Job Description:
        {job_description}
        
        Resume:
        {resume_text}
        """

        try:
            load_dotenv()
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error during analysis: {str(e)}"


    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            "<h3 class='sub-header'>📝 Job Description</h3>", unsafe_allow_html=True
        )
        job_description = st.text_area(
            "Paste the job description here",
            height=300,
            placeholder="Copy and paste the job description to analyze candidates against...",
        )

    with col2:
        st.markdown("<h3 class='sub-header'>📄 Resume Upload</h3>", unsafe_allow_html=True)
        uploaded_files = st.file_uploader(
            "Select multiple resumes", type="pdf", accept_multiple_files=True
        )
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} resume(s) uploaded")

            with st.expander("View uploaded files"):
                for file in uploaded_files:
                    st.write(f"📄 {file.name}")
        else:
            st.info("Please upload PDF resumes (Multiple files allowed)")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button("🔍 Analyze Resumes", use_container_width=True)

    # Initialize df as an empty DataFrame outside the conditional block
    df = pd.DataFrame()
    
    if uploaded_files and job_description and analyze_button:
        st.markdown(
            "<h3 class='sub-header'>🔄 Processing Resumes</h3>", unsafe_allow_html=True
        )
        progress_bar = st.progress(0)
        status_text = st.empty()
        results = []

        for i, file in enumerate(uploaded_files):
            status_text.markdown(
                f"<p style='text-align:center'>Analyzing {file.name}...</p>",
                unsafe_allow_html=True,
            )

            # Reset file position to beginning before reading
            file.seek(0)
            resume_text = extract_text_from_pdf(BytesIO(file.read()))

            match_percentage, matching_keywords = calculate_keyword_match(
                resume_text, job_description
            )

            ai_analysis = get_ai_analysis(resume_text, job_description)

            results.append(
                {
                    "Filename": file.name,
                    "Keyword Match %": match_percentage,
                    "Matching Keywords": matching_keywords,
                    "AI Analysis": ai_analysis,
                    "Resume Text Length": len(resume_text),
                }
            )
            progress_bar.progress((i + 1) / len(uploaded_files))

        df = pd.DataFrame(results)
        df = df.sort_values(by="Keyword Match %", ascending=False)

        status_text.markdown(
            "<h3 class='sub-header' style='text-align:center'>✅ Analysis Complete!</h3>",
            unsafe_allow_html=True,
        )
        
    # Only create tabs if we have data to show
    if not df.empty:
        tab1, tab2 = st.tabs(["📊 Leaderboard", "📝 Detailed Analysis"])
        
        with tab1:
            top_performer = df.iloc[0]
            st.markdown(
                f"""
                <div style="border-radius:10px; padding:15px; margin-bottom:20px; border-left:5px solid #3B82F6;">
                    <h4 style="margin-top:0;">🏆 Top Match: {top_performer['Filename']}</h4>
                    <p>This resume scored <span style="font-weight:bold; color:#2563EB;">{top_performer['Keyword Match %']:.1f}%</span> match with {len(top_performer['Matching Keywords'])} keywords matched.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(
                    "<p style='text-align:center;font-size:0.9rem;color:#6B7280'>Top Performer</p>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<h3 style='text-align:center;margin-top:0'>{top_performer['Filename']}</h3>",
                    unsafe_allow_html=True,
                )

            with col2:
                st.markdown(
                    "<p style='text-align:center;font-size:0.9rem;color:#6B7280'>Highest Match</p>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<h3 style='text-align:center;margin-top:0'>{top_performer['Keyword Match %']:.1f}%</h3>",
                    unsafe_allow_html=True,
                )

            with col3:
                st.markdown(
                    "<p style='text-align:center;font-size:0.9rem;color:#6B7280'>Keywords Matched</p>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<h3 style='text-align:center;margin-top:0'>{len(top_performer['Matching Keywords'])}</h3>",
                    unsafe_allow_html=True,
                )

            # Summary statistics
            st.markdown(
                "<h4 class='sub-header'>Match Statistics</h4>", unsafe_allow_html=True
            )
            stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
            with stat_col1:
                st.metric("Average Match", f"{df['Keyword Match %'].mean():.1f}%")
            with stat_col2:
                st.metric("Median Match", f"{df['Keyword Match %'].median():.1f}%")
            with stat_col3:
                st.metric("Min Match", f"{df['Keyword Match %'].min():.1f}%")
            with stat_col4:
                st.metric("Max Match", f"{df['Keyword Match %'].max():.1f}%")

            # Create visualization section with tabs for different charts
            st.markdown(
                "<h4 class='sub-header'>Visual Analysis</h4>", unsafe_allow_html=True
            )
            chart_tabs = st.tabs(["Bar Chart", "Distribution", "Keyword Analysis"])

            with chart_tabs[0]:  # Bar Chart Tab
                # Create horizontal bar chart
                fig, ax = plt.subplots(figsize=(10, 6))

                # Add color gradient based on match percentage
                colors = plt.cm.viridis(df["Keyword Match %"] / 100)

                bars = sns.barplot(
                    x="Keyword Match %",
                    y="Filename",
                    data=df,
                    palette=colors,
                    orient="h",
                    ax=ax,
                )

                # Add percentage values on bars
                for i, bar in enumerate(bars.patches):
                    bars.text(
                        bar.get_width() + 1,
                        bar.get_y() + bar.get_height() / 2,
                        f"{bar.get_width():.1f}%",
                        ha="left",
                        va="center",
                        fontsize=10,
                    )

                ax.set_title("Resume Match Percentage", fontsize=14)
                ax.set_xlabel("Match Percentage (%)", fontsize=12)
                ax.set_ylabel("Resume", fontsize=12)
                ax.spines["top"].set_visible(False)
                ax.spines["right"].set_visible(False)

                # Display chart
                st.pyplot(fig)

            with chart_tabs[1]:  # Distribution Tab
                if len(df) >= 3:  # Only show distribution if we have enough data
                    # Create distribution plot
                    fig, ax = plt.subplots(figsize=(10, 6))

                    # Distribution plot
                    sns.histplot(
                        df["Keyword Match %"],
                        kde=True,
                        color="#3B82F6",
                        ax=ax,
                        bins=min(10, len(df)),
                    )

                    # Add vertical lines for mean and median
                    plt.axvline(
                        df["Keyword Match %"].mean(),
                        color="red",
                        linestyle="--",
                        label=f'Mean: {df["Keyword Match %"].mean():.1f}%',
                    )
                    plt.axvline(
                        df["Keyword Match %"].median(),
                        color="green",
                        linestyle="-.",
                        label=f'Median: {df["Keyword Match %"].median():.1f}%',
                    )

                    ax.set_title("Distribution of Match Percentages", fontsize=14)
                    ax.set_xlabel("Match Percentage (%)", fontsize=12)
                    ax.set_ylabel("Frequency", fontsize=12)
                    plt.legend()

                    # Display chart
                    st.pyplot(fig)
                else:
                    st.info("Need at least 3 resumes to show distribution analysis")

            with chart_tabs[2]:  # Keyword Analysis Tab
                # Collect all matching keywords across resumes
                all_keywords = []
                for keywords in df["Matching Keywords"]:
                    all_keywords.extend(keywords)

                # Count frequency of each keyword
                keyword_freq = {}
                for keyword in all_keywords:
                    if keyword in keyword_freq:
                        keyword_freq[keyword] += 1
                    else:
                        keyword_freq[keyword] = 1

                # Convert to DataFrame for plotting
                keyword_df = pd.DataFrame(
                    list(keyword_freq.items()), columns=["Keyword", "Frequency"]
                )
                keyword_df = keyword_df.sort_values(by="Frequency", ascending=False).head(
                    15
                )

                # Create horizontal bar chart for keywords
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.barplot(
                    x="Frequency",
                    y="Keyword",
                    data=keyword_df,
                    palette="Blues_d",
                    orient="h",
                    ax=ax,
                )

                ax.set_title("Most Common Matching Keywords", fontsize=14)
                ax.set_xlabel("Frequency", fontsize=12)
                ax.set_ylabel("Keyword", fontsize=12)
                ax.spines["top"].set_visible(False)
                ax.spines["right"].set_visible(False)

                # Display keyword chart
                st.pyplot(fig)

            # Resume comparison table
            st.markdown(
                "<h4 class='sub-header'>Resume Comparison Table</h4>",
                unsafe_allow_html=True,
            )

            # Enhanced table with color coding
            table_df = df[["Filename", "Keyword Match %"]].copy()

            # Add color indicators based on match percentage
            def color_match(val):
                try:
                    value = float(val.replace("%", ""))
                    if value >= 75:
                        return "background-color: #DCFCE7; color: #166534"  # Green for high matches
                    elif value >= 50:
                        return "background-color: #FEF9C3; color: #854D0E"  # Yellow for medium matches
                    else:
                        return "background-color: #FEE2E2; color: #991B1B"  # Red for low matches
                except:
                    return ""

            # Format percentages
            table_df["Keyword Match %"] = table_df["Keyword Match %"].map(
                lambda x: f"{x:.1f}%"
            )

            # Display stylized table
            st.dataframe(
                table_df.style.applymap(color_match, subset=["Keyword Match %"]),
                use_container_width=True,
            )

            # Keyword match heatmap
            st.markdown(
                "<h4 class='sub-header'>Keyword Presence Across Resumes</h4>",
                unsafe_allow_html=True,
            )

            # Get top keywords (limit to 15 for visual clarity)
            top_keywords = sorted(
                [(k, v) for k, v in keyword_freq.items()], key=lambda x: x[1], reverse=True
            )[:15]
            top_keywords = [k[0] for k in top_keywords]

            # Create a matrix of keyword presence (1 if present, 0 if not)
            heatmap_data = []
            for _, row in df.iterrows():
                filename = row["Filename"]
                keywords = set(row["Matching Keywords"])
                row_data = [1 if kw in keywords else 0 for kw in top_keywords]
                heatmap_data.append(row_data)

            # Create DataFrame for heatmap
            heatmap_df = pd.DataFrame(
                heatmap_data, index=df["Filename"], columns=top_keywords
            )

            # Create heatmap
            fig, ax = plt.subplots(figsize=(12, len(df) * 0.5 + 2))
            sns.heatmap(
                heatmap_df,
                cmap="YlGnBu",
                cbar=False,
                ax=ax,
                linewidths=1,
                linecolor="white",
                annot=True,
                fmt="d",
            )

            plt.title("Keyword Presence Across Resumes", fontsize=14)
            plt.tight_layout()

            st.pyplot(fig)

        # Tab 2: Detailed Analysis
        with tab2:
            st.markdown(
                "<h3 class='sub-header'>Detailed Resume Analysis</h3>",
                unsafe_allow_html=True,
            )

            for i, row in df.iterrows():
                with st.expander(
                    f"📄 {row['Filename']} - Match: {row['Keyword Match %']:.1f}%"
                ):
                    analysis_col1, analysis_col2 = st.columns([1, 2])

                    # Document info
                    with analysis_col1:
                        st.markdown("<h4>Document Info</h4>", unsafe_allow_html=True)
                        st.write(f"**File Name:** {row['Filename']}")
                        st.write(f"**Match Score:** {row['Keyword Match %']:.1f}%")
                        st.write(
                            f"**Content Length:** {row['Resume Text Length']} characters"
                        )

                        st.markdown("<h4>Matching Keywords</h4>", unsafe_allow_html=True)

                        if not row["Matching Keywords"]:
                            st.info("No keywords matched")
                        else:
                            # Create a more visual representation of keywords
                            keyword_cols = st.columns(2)
                            for idx, keyword in enumerate(sorted(row["Matching Keywords"])):
                                col_idx = idx % 2
                                keyword_cols[col_idx].markdown(f"✅ {keyword}")

                    # AI Analysis
                    with analysis_col2:
                        st.markdown("<h4>AI Analysis</h4>", unsafe_allow_html=True)

                        try:
                            # Clean the AI response
                            cleaned_response = (
                                row["AI Analysis"]
                                .replace("```json", "")
                                .replace("```", "")
                                .strip()
                            )

                            try:
                                # Try to parse as JSON for better display
                                parsed_json = pd.read_json(cleaned_response, typ="series")

                                # Score display
                                score = parsed_json.get("score", "N/A")
                                st.markdown(
                                    f"<h2 style='text-align:center'>Score: {score}/100</h2>",
                                    unsafe_allow_html=True,
                                )

                                # Create columns for strengths and gaps
                                strength_col, gaps_col = st.columns(2)

                                with strength_col:
                                    st.markdown(
                                        "<h5>📈 Strengths</h5>", unsafe_allow_html=True
                                    )
                                    strengths = parsed_json.get("strengths", [])
                                    if isinstance(strengths, list):
                                        for strength in strengths:
                                            st.markdown(f"✅ {strength}")
                                    else:
                                        st.write(strengths)

                                with gaps_col:
                                    st.markdown("<h5>📉 Gaps</h5>", unsafe_allow_html=True)
                                    gaps = parsed_json.get("gaps", [])
                                    if isinstance(gaps, list):
                                        for gap in gaps:
                                            st.markdown(f"❌ {gap}")
                                    else:
                                        st.write(gaps)

                                st.markdown(
                                    "<h5>💡 Recommendation</h5>", unsafe_allow_html=True
                                )
                                recommendation = parsed_json.get(
                                    "recommendation", "No recommendation provided."
                                )
                                st.info(recommendation)

                            except:
                                # If JSON parsing fails, just display the text
                                st.text_area("Raw Analysis", cleaned_response, height=300)
                        except:
                            st.error("Error parsing AI analysis")

        # Only show export options if we have results
        if not df.empty:
            # Export options
            st.markdown("---")
            export_col1, export_col2 = st.columns(2)

            with export_col1:
                # Export as CSV
                csv = (
                    df[["Filename", "Keyword Match %", "Matching Keywords", "AI Analysis"]]
                    .to_csv(index=False)
                    .encode("utf-8")
                )
                st.download_button(
                    "📥 Download Results as CSV",
                    csv,
                    "resume_analysis_results.csv",
                    "text/csv",
                    key="download-csv",
                    use_container_width=True,
                )

            with export_col2:
                excel_buffer = BytesIO()
                df[
                    ["Filename", "Keyword Match %", "Matching Keywords", "AI Analysis"]
                ].to_excel(excel_buffer, index=False, engine="openpyxl")
                excel_buffer.seek(0)

                st.download_button(
                    "📊 Download Results as Excel",
                    excel_buffer,
                    "resume_analysis_results.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download-excel",
                    use_container_width=True,
                )