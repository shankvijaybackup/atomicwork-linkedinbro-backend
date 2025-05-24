from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

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
    my_profile: str
    their_profile: str
    meeting_purpose: str

@app.post("/generate-insight")
async def generate_insight(data: InsightRequest):
    atomicworkContext = """
AI-First, Human-Centric - ServiceNow built workflows; Atomicwork automates them intelligently. Our Agentic AI at the core of your service management frees employees from repetitive tasks.

Radical Simplicity, Lightning Deployment - Enterprise-grade ITSM in weeks. Complexity belongs in the past. Atomicwork makes speed your advantage.

Employee Support That Feels Like Consumer Experience - Imagine ServiceNow with the UX of your favorite apps. That’s Atomicwork.

Purpose-Built AI Agents - Atomicwork deploys AI Agents for IT, HR, Finance to instantly resolve employee requests and deliver proactive service.

Automate 90%, Humanize the 10% - We automate intelligently so your teams can focus on the work that truly needs empathy and insight.

Future-Proof & Vendor-Free - No lock-in. Atomicwork’s open architecture avoids costly customizations and supports agility.

Built for Global Scale - Enterprise-ready from day one with global security, compliance, and performance.

50% Lower TCO - Slash platform overhead and integration cost. Free up budgets for innovation.

Loved by Employees, Trusted by CIOs - Atomicwork drives adoption, satisfaction, and strategic trust.

Endorsed by 50+ Top CIOs - Personally backed by industry leaders as the definitive challenger to ServiceNow, Atlassian, and BMC.

Reusable Models:
Talking Points:
• Applying Agentic AI to reduce incident volume
• Workflow simplification in hybrid IT environments
• Pitfalls in scaling AI in enterprise ops
• Low-friction integrations vs. legacy ITSM challenges
• ROI storytelling: cost + employee experience

Ice Breakers:
• “What’s the biggest AI opportunity you see in IT right now?”
• “What inspired your move into tech-led ops?”
• “If budget weren’t a constraint, what would you automate today?”

Key Questions:
• What metrics define success in your current ITSM stack?
• How is your team currently approaching AI pilots or proofs of value?
• What’s your north star when evaluating cost-saving tech?
• What’s been most difficult to modernize—people, process, or tools?
• What do you hope to change in IT ops over the next 12 months?
"""

    prompt = f"""
You are an AI assistant preparing a strategic meeting summary and outreach message set
based on two LinkedIn profile summaries and a meeting purpose.

Here are the inputs:
- My Profile Summary: {data.my_profile}
- Their Profile Summary: {data.their_profile}
- Meeting Purpose: {data.meeting_purpose}

Use the Atomicwork company positioning and product context below:

{atomicworkContext}

Your output should include:

### 1. Strategic Meeting Prep
- **Connection Angle** – 1 paragraph
- **Common Ground** – 4–6 bullets
- **Talking Points** – 4–5 bullets
- **Ice Breakers** – 2–3 friendly openers
- **Key Questions** – 4–5 strategic questions

### 2. Outreach Pack Variations
Generate **10 outreach variations**. Each variation must include:
- **Subject Line**: under 8 words
- **LinkedIn DM Message**: under 300 characters, actionable and conversational

Each outreach message should be distinct — with a unique hook such as:
• Agentic AI  
• Reducing TCO  
• Modern UI/UX  
• Deployment Speed  
• ROI & Business Value  
• Compliance-readiness  
• Future-proof AI Stack  
• Employee Delight  
• Executive Recognition  
• Low-friction Integrations

Make sure Atomicwork is naturally woven in. Format everything in **Markdown** using clear headers.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return {"output": response.choices[0].message.content}
