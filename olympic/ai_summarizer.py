import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('AIzaSyBUvhn9WTCWptVbzDqPKnsb07ODtE2liQk')

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-pro")

def generate_country_summary(country, year_df, top_athletes_df):
    medals_by_year = year_df.set_index('Year')['Medal'].to_dict()
    top_athletes_list = top_athletes_df['Name'].tolist()

    prompt = f"""
    Provide a summary of {country}'s Olympic performance.

    Medal counts by year: {medals_by_year}

    Top athletes: {', '.join(top_athletes_list)}

    Keep it short and insightful, under 4 sentences. Highlight any noticeable trends or top sports.
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating summary: {e}"
