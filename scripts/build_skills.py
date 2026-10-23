#!/usr/bin/env python3
"""Build agent skills (plugin/skills/*/SKILL.md) from the non-draft workflow cards.

The cards are the source of truth. Run this after editing a field-tested or
candidate card; scripts/lint_repo.py fails when the skills are out of date.
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugin" / "skills"
BLOB = "https://github.com/Richicinschi/awesome-agent-workflows/blob/main"
SHIPPED = ("field-tested", "candidate")
# Card sections an agent needs at run time, in card order.
KEEP = ("Goal", "Agent brief", "Steps", "Verification checklist", "Failure modes", "Human gate")
LOCAL_LINK = re.compile(r"\]\((?!https?://|mailto:|#)([^)]+)\)")


def sections(text: str) -> dict[str, str]:
    found: dict[str, list[str]] = {}
    current = None
    fenced = False
    for line in text.split("\n"):
        if line.startswith("```"):
            fenced = not fenced
        if not fenced and line.startswith("## "):
            current = line[3:].strip()
            found[current] = []
        elif current is not None:
            found[current].append(line)
    return {name: "\n".join(lines).strip() for name, lines in found.items()}


def absolute_links(text: str, card: str) -> str:
    base = (Path(card).parent).as_posix()

    def repl(match: re.Match[str]) -> str:
        target = (Path(base) / match.group(1)).as_posix()
        parts: list[str] = []
        for piece in target.split("/"):
            if piece == "..":
                if not parts:
                    raise SystemExit(f"{card}: link climbs above the repo root: {match.group(1)}")
                parts.pop()
            elif piece != ".":
                parts.append(piece)
        return f"]({BLOB}/{'/'.join(parts)})"

    return LOCAL_LINK.sub(repl, text)


def render(item: dict) -> str:
    text = (ROOT / item["path"]).read_text(encoding="utf-8").replace("\r\n", "\n")
    found = sections(text)
    trigger = item["trigger"].rstrip(".")
    first = trigger.split()[0]
    if not (len(first) > 1 and first.isupper()):  # keep acronyms such as "CI" intact
        trigger = trigger[0].lower() + trigger[1:]
    lead = "Use" if trigger.split()[0] in ("before", "after", "during", "while", "when") else "Use when"
    description = f"{lead} {trigger}. {item['goal']}"
    body = [
        "---",
        f"name: {item['id']}",
        f"description: {json.dumps(description, ensure_ascii=False)}",
        "---",
        "",
        f"# {item['title']}",
        "",
        f"Status: {item['status']}. Generated from the workflow card at {BLOB}/{item['path']}; edit the card, not this file.",
    ]
    for name in KEEP:
        if name in found:
            body += ["", f"## {name}", "", absolute_links(found[name], item["path"])]
    return "\n".join(body) + "\n"


def render_all() -> dict[str, str]:
    data = json.loads((ROOT / "agent-workflows.json").read_text(encoding="utf-8"))
    return {item["id"]: render(item) for item in data if item.get("status") in SHIPPED}


def main() -> None:
    skills = render_all()
    if SKILLS.exists():
        shutil.rmtree(SKILLS)
    for skill_id, content in skills.items():
        target = SKILLS / skill_id / "SKILL.md"
        target.parent.mkdir(parents=True)
        target.write_text(content, encoding="utf-8", newline="\n")
    print(f"built {len(skills)} skills in {SKILLS.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
