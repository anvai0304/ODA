import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging

# Setup logging
logger = logging.getLogger("gemini_logger")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] - %(message)s")

# Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")  # ✅ Make sure variable is exactly this
genai.configure(api_key=api_key)

# Create model instance
model = genai.GenerativeModel("gemini-pro")  # ✅ Correct name, no 'models/'

def generate_country_summary(country, year_df, top_athletes_df):
    try:
        medals_by_year = year_df.set_index('Year')['Medal'].to_dict()
        top_athletes_list = top_athletes_df['Name'].tolist()

        prompt = f"""
        Provide a summary of {country}'s Olympic performance.

        Medal counts by year: {medals_by_year}

        Top athletes: {', '.join(top_athletes_list)}

        Keep it short and insightful, under 4 sentences. Highlight any noticeable trends or top sports.
        """

        logger.info(f"Generating summary for {country}")
        response = model.generate_content(prompt)
        summary = response.text.strip()
        logger.info(f"Generated summary for {country}: {summary}")

        return summary

    except Exception as e:
        error_msg = f"Error generating summary: {e}"
        logger.error(error_msg)
        return error_msg
