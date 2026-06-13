def compare_skills(resume_skills, jd_skills):

    resume_set = {
        skill.lower()
        for skill in resume_skills
    }

    jd_set = {
        skill.lower()
        for skill in jd_skills
    }

    matched = list(
        resume_set.intersection(jd_set)
    )

    missing = list(
        jd_set - resume_set
    )

    score = 0

    if len(jd_set) > 0:

        score = round(
            (
                len(matched)
                /
                len(jd_set)
            ) * 100,
            2
        )

    return {
        "score": score,
        "matched": matched,
        "missing": missing
    }