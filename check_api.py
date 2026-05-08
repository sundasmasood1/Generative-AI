from google.genai import Client
import os
from dotenv import load_dotenv

load_dotenv()  # 👈 IMPORTANT

client = Client(api_key=os.getenv("GENAI_API_KEY"))

models = client.models.list()

for m in models:
    print(m.name)