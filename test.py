import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
r = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="List 3 documents a delivery vendor needs for compliance."
)
print(r.text)