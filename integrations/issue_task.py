"""Strict, offline parser for GitHub issue tasks. Never performs network calls.

Expected title: [AI-TASK] <short description>
Expected body:
    provider: gemini
    instructions:
    Write a synthetic answer.

Only authorized issue authors may be accepted by the *calling workflow*;
this module cannot authenticate GitHub actors.
"""
import re
from dataclasses import dataclass

PROVIDERS = frozenset({"gemini", "deepseek", "manus", "claude", "perplexity"})
TITLE_PREFIX = "[AI-TASK] "
MAX_INSTRUCTIONS = 8000

@dataclass(frozen=True)
class Task:
    provider: str
    instructions: str
    title: str

def parse_issue(title: str, body: str) -> Task:
    if not isinstance(title, str) or not title.startswith(TITLE_PREFIX):
        raise ValueError("issue title must start with '[AI-TASK] '")
    description = title[len(TITLE_PREFIX):].strip()
    if not description or len(description) > 120:
        raise ValueError("invalid task description")
    if not isinstance(body, str) or len(body) > 12000:
        raise ValueError("invalid issue body")
    lines = body.replace("\r\n", "\n").split("\n")
    provider_lines = [line for line in lines if re.match(r"^provider\s*:", line, re.I)]
    if len(provider_lines) != 1:
        raise ValueError("expected exactly one provider field")
    match = re.fullmatch(r"provider:\s*([a-z]+)\s*", provider_lines[0])
    if not match or match.group(1) not in PROVIDERS:
        raise ValueError("unsupported or malformed provider")
    instruction_indices = [i for i, line in enumerate(lines) if line.strip() == "instructions:"]
    if len(instruction_indices) != 1:
        raise ValueError("expected exactly one instructions field")
    idx = instruction_indices[0]
    if any(line.strip() for line in lines[:idx] if line != provider_lines[0]):
        raise ValueError("unexpected header fields")
    instructions = "\n".join(lines[idx + 1:]).strip()
    if not instructions or len(instructions) > MAX_INSTRUCTIONS:
        raise ValueError("empty or oversized instructions")
    return Task(match.group(1), instructions, description)

def task_key(repository: str, issue_number: int, provider: str) -> str:
    if not re.fullmatch(r"CarlosVergaraChile/[A-Za-z0-9_.-]+", repository):
        raise ValueError("repository not authorized")
    if not isinstance(issue_number, int) or isinstance(issue_number, bool) or issue_number <= 0:
        raise ValueError("invalid issue number")
    if provider not in PROVIDERS:
        raise ValueError("unsupported provider")
    return f"{repository}#{issue_number}:{provider}"
