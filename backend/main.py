from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

origins = [
    "*",  # Consider restricting this to your frontend domain for security
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InsightRequest(BaseModel):
    my_profile: str
    their_profile: str
    meeting_purpose: str

@app.post("/generate-insight")
async def generate_insight(data: InsightRequest):
    prompt = f"""
You are a B2B outreach assistant that crafts DISC-personality-based messages.

Inputs:
- My profile: {data.my_profile}
- Their profile: {data.their_profile}
- Meeting purpose: {data.meeting_purpose}

Output instructions:
1. Identify DISC type of the *prospect* and tailor all outreach accordingly.
2. Output multiple outreach messages in this exact format:
   How Vijay R would outreach :
   Subject : ...
   Message : ...
   How Kiran D would outreach :
   Subject : ...
   Message : ...
   How Parsu would outreach :
   Subject : ...
   Message : ...
   How Lenin G would outreach :
   Subject : ...
   Message : ...
3. Limit each message to 300–500 characters.
4. Do NOT use markdown (no ###, **, or -).
5. Include copy buttons after each block.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return {"output": response["choices"][0]["message"]["content"]}
