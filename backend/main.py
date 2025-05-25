
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InsightRequest(BaseModel):
    my_profile: str
    their_profile: str
    meeting_purpose: str

@app.post("/generate-insight")
async def generate_insight(req: InsightRequest):
    my_profile = req.my_profile.strip()
    their_profile = req.their_profile.strip()
    meeting_purpose = req.meeting_purpose.strip()

    prompt = f"""
    You are Atomicwork's DISC-personalized outreach generator.

    STEP 1: Based on the two LinkedIn profiles (mine and the prospect's), analyze the PROSPECT and extract DISC personality traits.

    STEP 2: Generate a Strategic Meeting Prep block including:
    - Connection Angle
    - Common Ground
    - Talking Points
    - Ice Breakers
    - Key Questions

    STEP 3: Generate 10 outreach variations — grouped under founder personas:
    How Vijay R would outreach:
    Subject:
    Message:

    How Kiran D would outreach:
    Subject:
    Message:

    How Parsu M would outreach:
    Subject:
    Message:

    How Lenin Gali would outreach:
    Subject:
    Message:

    Each founder should have at least 2 variations.
    Use a blend of DISC tone, Common Ground, Ice Breakers, ROI Storytelling, and Key Questions.
    All messages must:
    - Mention the prospect’s first name
    - Be 500 characters only
    - Use plain text (no markdown, no bullets)
    - Make sure you ### or ** in outreach variations
    - Make sure you use DISC tone using the strategic meeting prep block data points all 5 combos

    My Profile:
    {my_profile}

    Prospect Profile:
    {their_profile}

    Meeting Purpose:
    {meeting_purpose}
    """

    try:
 client = openai.OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7
)
output = completion.choices[0].message.content
    