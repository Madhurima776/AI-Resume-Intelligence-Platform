import re

COMMON_SKILLS = [

    "python",
    "java",
    "c++",
    "sql",
    "mysql",
    "postgresql",

    "html",
    "css",
    "javascript",

    "react",
    "nodejs",
    "fastapi",

    "machine learning",
    "deep learning",

    "tensorflow",
    "pytorch",

    "pandas",
    "numpy",

    "excel",
    "power bi",
    "tableau",

    "aws",
    "azure",

    "git",
    "github",
    "docker"
]


def extract_skills_llm(text):

    text = text.lower()

    found = []

    for skill in COMMON_SKILLS:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):

            found.append(skill)

    return list(set(found))