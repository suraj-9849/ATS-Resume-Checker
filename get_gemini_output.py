from dotenv import load_dotenv
import google.generativeai as genai
import os
def get_gemini_output(pdf_text, prompt):
    load_dotenv()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content([pdf_text, prompt])
    return response.text
