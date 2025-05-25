from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

class InsightRequest(BaseModel):
    my_profile: str
    their_profile: str
    meeting_purpose: str

@app.post("/generate-insight")
async def generate_insight(req: InsightRequest):
    prompt = f"""
You are a DISC-aware AI that creates LinkedIn outreach strategies.

Given:
- My LinkedIn profile: {req.my_profile}
- Prospect's LinkedIn profile: {req.their_profile}
- Purpose: {req.meeting_purpose}

Steps:
1. Analyze the prospect's DISC personality type (D, I, S, C).
2. Create outreach variations that match the DISC tone.
3. Generate outreach messages in the style of 4 founders: Vijay R, Kiran D, Parsu, Lenin G.
4. Each message must have:
   - How [Founder Name] would outreach :
   - Subject :
   - Message : (max 500 characters)
   - Include [Copy] tag after each message block.

Return only the 4 formatted message blocks, nothing else.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0.7,
        messages=[
            {"role": "system", "content": "You generate LinkedIn outreach using DISC and founder personas."},
            {"role": "user", "content": prompt}
        ]
    )

    final_output = response.choices[0].message.content
    return {"output": final_output}
