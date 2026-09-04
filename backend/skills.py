import re
from collections import Counter

KNOWN_SKILLS = [
    "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust",
    "Ruby", "PHP", "Swift", "Kotlin", "SQL", "R",
    "React", "Vue", "Angular", "Node.js", "Django", "Flask", "FastAPI",
    "Spring", "Rails", "Next.js", "Express",
    "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "Jenkins",
    "CI/CD", "Linux",
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
    "Machine Learning", "TensorFlow", "PyTorch", "pandas", "NumPy",
    "Git", "REST", "GraphQL", "Kafka", "Spark", "Hadoop", "Airflow",
]


def _skill_pattern(skill: str) -> re.Pattern:
    # \b fails at the edges of skills like "C++" or "C#" (their own edge
    # char isn't a word char, so \b never fires there); only require a
    # non-alnum boundary on edges that are actually alnum.
    escaped = re.escape(skill)
    prefix = r"(?<![A-Za-z0-9])" if skill[0].isalnum() else ""
    suffix = r"(?![A-Za-z0-9])" if skill[-1].isalnum() else ""
    return re.compile(prefix + escaped + suffix, re.IGNORECASE)


SKILL_PATTERNS = {skill: _skill_pattern(skill) for skill in KNOWN_SKILLS}


def count_skills(jobs: list[dict]) -> Counter:
    counts = Counter()
    for job in jobs:
        text = f"{job.get('title', '')} {job.get('description', '')}"
        for skill, pattern in SKILL_PATTERNS.items():
            if pattern.search(text):
                counts[skill] += 1
    return counts
