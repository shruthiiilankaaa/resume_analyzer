# summary_generator.py

def generate_resume_summary(text, model="gpt-4o-mini", api_key=None):
    from openai import OpenAI

    client = OpenAI(api_key=api_key)

    prompt = (
        "Analyze the following resume text and generate a concise 3-4 line professional summary "
        "that highlights the candidate's key strengths, experience, and skills:\n\n"
        f"{text[:3000]}"  # limit size
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error generating summary: {e}"
