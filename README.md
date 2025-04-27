# 🚀 Advanced ATS Resume Checker

An AI-powered tool to analyze and optimize your resume for Applicant Tracking Systems (ATS) and improve your job application success rate.

![ATS Resume Checker](https://placehold.co/800x400/e9f5eb/31572c?text=ATS+Resume+Checker&font=montserrat)

## ✨ Features

### Resume Analysis

- **AI-Powered Analysis**: Get intelligent insights beyond basic keyword matching
- **Multiple Analysis Options**: Choose from Quick Scan, Detailed Analysis, ATS Optimization, or Formatting Check
- **Keyword Matching**: See which keywords from job descriptions match your resume
- **Visual Feedback**: Resume heatmaps and word clouds visualize your resume's strengths
- **Industry-Specific Advice**: Get tailored recommendations for your field
- **Version Tracking**: Save multiple versions to measure improvements over time

### GitHub Profile Analysis

- **Repository Assessment**: Analyze your GitHub profile to complement your resume
- **Skills Gap Identification**: See if your GitHub projects showcase skills missing from your resume
- **Technical Validation**: Demonstrate coding abilities with actual GitHub projects
- **Language Visualization**: See your programming language distribution and activity patterns
- **AI-Powered Insights**: Get recommendations on how to improve your GitHub profile

### Industry Insights

- **Industry-Specific Skills**: View top skills required for various industries
- **Resume Optimization Tips**: Get tailored advice for your specific industry
- **ATS Best Practices**: Learn how to format your resume for optimal ATS performance

## 🛠️ Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/ATS-Resume-Checker.git
   cd ATS-Resume-Checker

   ```

2. Create and activate a virtual environment (optional but recommended):

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your Google API key:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## 🚀 Usage

1. Start the Streamlit application:

   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. Use the three main tabs to:
   - Analyze your resume against job descriptions
   - Evaluate your GitHub profile to complement your resume
   - Get industry-specific insights and best practices

## 📋 How to Use

### Resume Analysis

1. Upload your resume in PDF format
2. Paste the job description you're applying for
3. Choose your preferred analysis type:
   - **Quick Scan**: Fast overview of your resume's strengths and weaknesses
   - **Detailed Analysis**: Comprehensive breakdown of your resume's components
   - **ATS Optimization**: Focused feedback on improving ATS compatibility
   - **Formatting Check**: Analysis of your resume's structure and layout
4. Review the results and make improvements to your resume

### GitHub Profile Analyzer

1. Enter your GitHub username
2. Optionally, use an existing resume from the Resume Analysis tab
3. Review insights about your repositories, languages, and activity
4. Use the AI analysis to understand how your GitHub profile complements your resume

### Industry Insights

1. Select your industry from the dropdown menu
2. Review the top skills for your chosen industry
3. Read industry-specific resume tips and ATS optimization advice

## 📊 Features in Detail

### Resume Analysis

- **Keyword Matching**: Identifies which keywords from the job description appear in your resume
- **Resume Heatmap**: Visualizes which sections of your resume match job description keywords
- **Word Cloud**: Shows the most prominent keywords in your resume
- **Formatting Check**: Detects issues that might cause problems with ATS systems
- **Industry Detection**: Automatically identifies your target industry and provides relevant advice

### GitHub Analysis

- **Repository Overview**: Displays your top repositories with stars, forks, and languages
- **Language Distribution**: Visualizes the programming languages you use most frequently
- **Activity Chart**: Shows your GitHub activity patterns
- **AI Recommendations**: Provides personalized advice on improving your GitHub profile

## 🔧 Requirements

- Python 3.7+
- Streamlit
- Google Generative AI API key
- NLTK
- Pandas
- Plotly
- Matplotlib
- WordCount
- PyMuPDF (for PDF reading)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Google Generative AI](https://ai.google/discover/generativeai/) for providing the AI capabilities
- [Streamlit](https://streamlit.io/) for the web application framework
- [NLTK](https://www.nltk.org/) for natural language processing capabilities
- All the open-source libraries that made this project possible
