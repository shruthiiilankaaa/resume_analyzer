import re
from collections import Counter
import textstat

def get_word_count(text):
    """Return total word count in resume text."""
    words = re.findall(r'\w+', text)
    return len(words)

def get_readability_score(text):
    """Calculate Flesch Reading Ease Score. Higher is easier to read."""
    return textstat.flesch_reading_ease(text)

def keyword_density(text, top_n=10):
    """Return top N keywords in resume with count and % density."""
    words = re.findall(r'\w+', text.lower())
    counter = Counter(words)
    total_words = len(words)
    most_common = counter.most_common(top_n)

    return [(word, count, round((count / total_words) * 100, 2)) for word, count in most_common]

def compare_keyword_density(resume_text, jd_text, top_n=10):
    """Compare keyword frequency between resume and job description."""
    resume_counter = Counter(re.findall(r'\w+', resume_text.lower()))
    jd_counter = Counter(re.findall(r'\w+', jd_text.lower()))

    jd_common = jd_counter.most_common(top_n)
    comparison = []
    for word, jd_count in jd_common:
        resume_count = resume_counter.get(word, 0)
        comparison.append({
            'keyword': word,
            'jd_count': jd_count,
            'resume_count': resume_count,
            'gap': jd_count - resume_count
        })
    return comparison

def extract_experience_periods(text):
    """
    Extracts total years and months of experience from phrases like 'from 2020 to 2023'.
    """
    import dateutil.parser as dp
    import datetime

    matches = re.findall(r'(from\s+(\d{4})\s+(to|-)\s+(\d{4}))', text.lower())
    total_months = 0
    for match in matches:
        start_year = int(match[1])
        end_year = int(match[3])
        months = (end_year - start_year) * 12
        if months > 0:
            total_months += months

    years = total_months // 12
    months = total_months % 12
    return years, months


# CLI block for testing this module independently
if __name__ == "__main__":
    from analyze_resume import extract_text_from_file

    resume_path = input("Enter path to resume file (.pdf/.docx): ").strip().replace('"', '')
    jd_path = input("Enter path to job description file (.txt): ").strip().replace('"', '')

    try:
        resume_text = extract_text_from_file(resume_path)
        with open(jd_path, 'r', encoding='utf-8') as f:
            jd_text = f.read()

        # Word count & readability
        word_count = get_word_count(resume_text)
        readability = get_readability_score(resume_text)

        print(f"\n=== Resume Length & Readability ===")
        print(f"Word Count: {word_count}")
        print(f"Flesch Reading Ease Score: {readability:.2f} (Higher is easier)")

        if word_count < 200:
            print("Recommendation: Resume is short. Add more details.")
        elif word_count > 1000:
            print("Recommendation: Resume is long. Be more concise.")

        if readability < 30:
            print("Recommendation: Improve readability with simpler language.")
        elif readability > 70:
            print("Great readability!")

        # Keyword Density
        print(f"\n=== Top {10} Keywords in Resume ===")
        kd = keyword_density(resume_text, top_n=10)
        for word, count, density in kd:
            print(f"{word}: {count} times ({density}%)")

        # Compare with JD
        print(f"\n=== Keyword Comparison with JD ===")
        comparison = compare_keyword_density(resume_text, jd_text, top_n=10)
        for c in comparison:
            gap = c['gap']
            status = "👍" if gap <= 0 else f"⚠️ Gap: {gap}"
            print(f"{c['keyword']} - JD: {c['jd_count']} | Resume: {c['resume_count']} {status}")

    except Exception as e:
        print(f"Error: {e}")
