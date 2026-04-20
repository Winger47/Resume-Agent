SKILLS = {
    "python", "fastapi", "django", "flask",
    "docker", "kubernetes", "aws", "gcp", "azure",
    "redis", "rabbitmq", "postgresql", "mysql", "mongodb",
    "react", "nodejs", "javascript", "typescript",
    "git", "ci/cd", "grpc", "kafka",
    "langchain", "chromadb", "numpy", "pandas",
    "celery", "linux", "rest", "graphql"
}


def extract_skills(text):
    extracted_skills = set()
    for skill in SKILLS:
        if skill in text.lower():
            extracted_skills.add(skill)
    return extracted_skills
