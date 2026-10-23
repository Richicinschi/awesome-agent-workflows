#!/usr/bin/env python3
"""Small repository hygiene check for Awesome Agent Workflows."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDERS = ("TBD", "TODO", "Lorem ipsum", "<todo>")
REQUIRED = [
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "docs/WORKFLOW-CATALOG.md",
    "docs/curation-policy.md",
    "docs/launch/GROWTH-PLAN.md",
    "templates/agent-brief.md",
    "templates/workflow-card.md",
]

LOCAL_LINK = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)")
STATUSES = ("field-tested", "candidate", "draft")
STATUS_LINE = re.compile(r"^> \*\*Status: ([a-z-]+)\.\*\*", re.MULTILINE)
# Sentences from the generic template the early cards were generated from.
TEMPLATE_MARKERS = (
    "Gather only the context needed for this workflow.",
    "**Collect targeted context.** Read only the files, logs, docs, issues, or commands needed for this workflow.",
)


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_required_files() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).exists()]
    if missing:
        fail(f"missing required files: {missing}")


def check_catalog() -> None:
    data = json.loads((ROOT / "agent-workflows.json").read_text(encoding="utf-8"))
    if len(data) < 10:
        fail("expected at least 10 workflows in agent-workflows.json")
    ids = [item["id"] for item in data]
    if len(ids) != len(set(ids)):
        fail("workflow ids must be unique")
    for item in data:
        path = ROOT / item["path"]
        if not path.exists():
            fail(f"workflow path missing: {item['path']}")
    checks = [item["verification"] for item in data]
    if len(checks) != len(set(checks)):
        fail("verification sentences must be specific to each workflow")


def check_status() -> None:
    data = json.loads((ROOT / "agent-workflows.json").read_text(encoding="utf-8"))
    for item in data:
        status = item.get("status")
        if status not in STATUSES:
            fail(f"{item['id']}: status must be one of {STATUSES}, got {status!r}")
        text = (ROOT / item["path"]).read_text(encoding="utf-8", errors="replace")
        match = STATUS_LINE.search(text)
        if not match or match.group(1) != status:
            fail(f"{item['path']}: status line must say {status!r} to match agent-workflows.json")
        if status != "draft":
            for marker in TEMPLATE_MARKERS:
                if marker in text:
                    fail(f"{item['path']}: {status} card still contains generic template text")
        if status == "field-tested" and "## Field notes" not in text:
            fail(f"{item['path']}: field-tested card needs a '## Field notes' section")


def check_placeholders() -> None:
    allow_angle_templates = {"templates/agent-brief.md", "templates/workflow-card.md"}
    for path in ROOT.rglob("*.md"):
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        for marker in PLACEHOLDERS:
            if marker in text:
                fail(f"placeholder marker {marker!r} found in {rel}")
        if rel not in allow_angle_templates and re.search(r"<[^>\n]{3,}>", text):
            fail(f"angle-bracket placeholder found in {rel}")


def check_local_links() -> None:
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        for raw in LOCAL_LINK.findall(text):
            target = raw.split("#", 1)[0].strip()
            if not target:
                continue
            candidate = (path.parent / target).resolve()
            if not str(candidate).startswith(str(ROOT)):
                fail(f"local link escapes repo in {path.relative_to(ROOT)}: {raw}")
            if not candidate.exists():
                fail(f"broken local link in {path.relative_to(ROOT)}: {raw}")


def check_skills() -> None:
    from build_skills import SKILLS, render_all

    expected = render_all()
    actual = {p.parent.name: p.read_text(encoding="utf-8") for p in SKILLS.glob("*/SKILL.md")}
    stale = sorted(k for k in expected.keys() | actual.keys() if expected.get(k) != actual.get(k))
    if stale:
        fail(f"plugin skills out of date ({', '.join(stale)}): run python3 scripts/build_skills.py")


def main() -> None:
    check_required_files()
    check_catalog()
    check_status()
    check_skills()
    check_placeholders()
    check_local_links()
    print("repo hygiene check passed")


if __name__ == "__main__":
    main()
