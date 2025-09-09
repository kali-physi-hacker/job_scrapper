import re
from typing import Iterable, Set


TECH_SKILLS = {
    # languages
    "python", "java", "javascript", "typescript", "go", "rust", "ruby", "php", "c#", "c++",
    # web
    "react", "vue", "angular", "node", "nextjs", "django", "flask", "fastapi", "spring",
    # data
    "sql", "postgres", "mysql", "mongodb", "redis", "spark", "hadoop",
    # cloud
    "aws", "gcp", "azure", "docker", "kubernetes", "terraform",
    # tools
    "git", "linux", "graphql", "rest", "grpc", "ci/cd",
}


def tokenize(text: str) -> Iterable[str]:
    for tok in re.findall(r"[a-zA-Z+#.\-/]{2,}", text.lower()):
        yield tok.strip(".-/")


def extract_basic_skills(text: str) -> Set[str]:
    toks = set(tokenize(text))
    found = set()
    for skill in TECH_SKILLS:
        if skill in toks:
            found.add(skill)
    return found

