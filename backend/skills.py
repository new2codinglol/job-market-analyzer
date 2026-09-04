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


def count_skills(jobs: list[dict]) -> Counter:
    counts = Counter()
    for job in jobs:
        text = f"{job.get('title', '')} {job.get('description', '')}".lower()
        for skill in KNOWN_SKILLS:
            if skill.lower() in text:
                counts[skill] += 1
    return counts
