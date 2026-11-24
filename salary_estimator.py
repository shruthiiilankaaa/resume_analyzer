# salary_estimator.py

def estimate_salary(years_exp, skills):
    # Simple base salaries (in USD)
    base_salary = 40000
    increment_per_year = 3000

    skill_bonus = 0
    # Example: premium skills add bonuses
    premium_skills = {"machine learning", "data science", "aws", "devops", "cybersecurity", "blockchain"}
    for skill in skills:
        if skill.lower() in premium_skills:
            skill_bonus += 5000

    salary = base_salary + (years_exp * increment_per_year) + skill_bonus

    # Simple tiers
    if years_exp < 2:
        level = "Junior"
    elif years_exp < 5:
        level = "Mid-level"
    else:
        level = "Senior"

    return level, round(salary, 2)

if __name__ == "__main__":
    years_exp = float(input("Enter total years of experience: "))
    skills_input = input("Enter comma-separated skills: ")
    skills = [s.strip() for s in skills_input.split(",")]
    level, salary = estimate_salary(years_exp, skills)
    print(f"\nEstimated Candidate Level: {level}")
    print(f"Estimated Salary Range: ${salary} per year (approximate)")
