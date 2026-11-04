import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
r = client.models.generate_content(model=sys.argv[1], contents="Say hello in one sentence.")
print(r.text)