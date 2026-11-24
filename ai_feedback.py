import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_ai_resume_feedback(resume_text, jd_text, api_key=None):
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OpenAI API key is required for AI feedback.")

    client = OpenAI(api_key=key)

    prompt = f"""
    You are a hiring expert. Given the following RESUME and JOB DESCRIPTION:

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {jd_text}

    Analyze the resume's fitness for the job. Then:
    - List strengths
    - Point out weak areas or missing skills
    - Suggest 3 ways to improve the resume
    - Provide a fit summary in one paragraph
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content


# Test it
if __name__ == "__main__":
    with open("extracted_resume.txt", "r", encoding="utf-8") as r, open("jd_sample.txt", "r", encoding="utf-8") as j:
        resume_text = r.read()
        jd_text = j.read()

    feedback = get_ai_resume_feedback(resume_text, jd_text)
    print("\n🧠 AI Resume Feedback:\n")
    print(feedback)