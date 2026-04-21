def match_skills(resume_skills, jd_skills):
    resume_skills = set(resume_skills)  # ← convert to set
    jd_skills = set(jd_skills)          # ← convert to set
    
    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills
    score = (len(matched) / len(jd_skills)) * 100 if jd_skills else 0

    return {
        "matched": list(matched),
        "missing": list(missing),
        "score": round(score, 2)
    }