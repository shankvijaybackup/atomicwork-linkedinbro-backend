from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from openai import OpenAI
import os
from dotenv import load_dotenv
import re

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class InsightRequest(BaseModel):
    my_profile: str = Field(..., example="Paste your full LinkedIn summary here.")
    their_profile: str = Field(..., example="Paste their full LinkedIn summary here.")
    meeting_purpose: str = Field(..., example="LinkedIn Outreach")

def sanitize_text(text: str) -> str:
    text = text.replace("\r", " ").replace("\n", " ").replace("\t", " ")
    text = re.sub(r'[\x00-\x1f\x7f]', ' ', text)
    text = re.sub(r'"', '\\"', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def detect_disc_type(profile: str) -> str:
    profile = profile.lower()
    if any(word in profile for word in ["executive", "results", "leader", "driven"]):
        return "D"
    elif any(word in profile for word in ["community", "network", "inspire", "talk"]):
        return "I"
    elif any(word in profile for word in ["team", "support", "dependable", "collaborate"]):
        return "S"
    elif any(word in profile for word in ["process", "detail", "compliance", "efficient"]):
        return "C"
    return "C"

@app.post("/generate-insight")
async def generate_insight(data: InsightRequest):
    try:
        their_profile_clean = sanitize_text(data.their_profile)
        my_profile_clean = sanitize_text(data.my_profile)
        disc_type = detect_disc_type(their_profile_clean)

        founder_context = """
Atomicwork's leadership is defined by:
- **Vijay Rayapati (CEO)**: Agentic AI evangelist, believes in future-proofing IT, focuses on cost-efficiency and CIO trust.
- **Kiran Darisi (CTO)**: Technical authority, emphasizes scalability, reliability, and AI-first architecture.
- **Parsuram (CPO)**: Passionate about consumer-grade UX for enterprise, simplifying workflows.
- **Lenin Gali (Chief Business Officer)**: GTM strategist, enterprise buyer psychology, emphasizes business value.
Their communication style is confident, visionary, technically articulate, and sharply value-oriented.
"""

        atomicwork_context = """
Atomicwork is a GPT-style ITSM platform built into Teams and Slack, native to Azure and OKTA. Built with compliance guardrails for secure enterprise automation.

Key differentiators:
- **Conversational ITSM**: Meet users where they work — inside Slack and Teams.
- **Agentic AI**: Autonomous resolution, routing, and remediation.
- **Speed-to-Deploy**: Enterprise-ready in weeks.
- **Azure & OKTA-native**: Identity-aware, compliant by design.
- **Guardrails & Audit**: Built for enterprise trust and governance.
- **Modern UX**: Consumer-grade support experience.
- **50% Lower TCO**: Reduces overhead with zero-touch automation.

Use Case Examples:
- Reduced incident volume by 40% in 3 weeks through autonomous resolution.
- 80% of routine tickets auto-resolved with zero-touch workflows.
- Improved CSAT by 25% after moving to conversational ITSM inside Slack/Teams.
"""

        disc_hooks = {
            "D": "Highlight ROI, metrics, cost-saving and impact acceleration.",
            "I": "Infuse excitement, share visionary benefits and social proof.",
            "S": "Emphasize consistency, trust, and team-wide enablement.",
            "C": "Focus on process rigor, compliance, security and audit trails."
        }

        prompt = f"""
You are an AI sales assistant helping a GTM team at Atomicwork.

Based on the LinkedIn profiles below and the DISC profile type \"{disc_type}\", prepare:

### 1. Strategic Meeting Prep
- **Connection Angle** (1 paragraph)
- **Common Ground** (4–6 bullets)
- **Talking Points** (4–5 bullets)
- **Ice Breakers** (2–3 openers)
- **Key Questions** (4–5 strategic questions)

### 2. Outreach Pack by Founder Persona
Generate **1 personalized outreach message** (subject line + 500-character message) from each of the following:
- **Vijay Rayapati** (CEO): Visionary, ROI-led, agentic AI champion.
- **Kiran Darisi** (CTO): Technical, scalable systems thinker, AI-first.
- **Parsuram** (CPO): UX obsessed, workflow simplifier, product storyteller.
- **Lenin Gali** (CBO): Business-value driver, buyer psychology expert.

Use DISC type tone modifiers:
- D = Direct, result-driven, ROI-focused
- I = Energetic, enthusiastic, story-driven
- S = Reliable, steady, people-first
- C = Analytical, efficient, precise

Add this value hook based on DISC type: {disc_hooks[disc_type]}

Incorporate Atomicwork's positioning:
{atomicwork_context}

And founder tone/personality:
{founder_context}

**My Profile:** {my_profile_clean}
**Their Profile:** {their_profile_clean}
**Meeting Purpose:** {data.meeting_purpose}

Format your output in Markdown, with clear blocks per founder. Add "Copy" button hint markers like `[Copy]` at the end of each subject/message.
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return {"output": response.choices[0].message.content}
    except Exception as e:
        return {"error": f"Error generating insights: {e}"}
