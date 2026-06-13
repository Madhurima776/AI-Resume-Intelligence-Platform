import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)


def semantic_skill_match(
        resume_skills,
        jd_skills
):

    prompt = f"""
You are an expert recruiter.

Resume Skills:
{resume_skills}

Job Description Skills:
{jd_skills}

Compare them semantically.

Rules:

1. Consider synonyms.
2. Consider related technologies.
3. Consider equivalent skills.

Return ONLY JSON.

Format:

{{
    "matched": [],
    "missing": [],
    "equivalent": {{}}
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content

    return json.loads(result)