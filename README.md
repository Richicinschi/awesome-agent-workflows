# Awesome Agent Workflows

> Copy-pasteable workflows for shipping real work with AI coding agents, CLI agents, and autonomous development tools.

[![Awesome](https://awesome.re/badge-flat2.svg)](https://awesome.re)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

![Awesome Agent Workflows banner](assets/banner.svg)

AI agents are powerful, but most examples stop at toy prompts. This repo collects **field-tested workflows**: how to hand off a task, constrain an agent, verify its work, recover when it drifts, and ship without trusting vibes.

Use it with Claude Code, Codex CLI, Cursor agents, Aider, OpenCode, Gemini CLI, LangGraph, CrewAI, custom tool-using agents, or any assistant that can read instructions and run tools.

## Why this exists

The bottleneck is no longer "can an agent write code?" The bottleneck is **operating agents safely**:

- turning fuzzy requests into executable specs;
- splitting work across parallel agents without merge chaos;
- forcing evidence before "done" claims;
- reviewing code from a fresh context;
- keeping secrets, production, and public repos safe;
- launching useful projects without spam or fake engagement.

This repository is a practical playbook for that work.

## Quick start

1. Pick the workflow that matches your situation.
2. Copy the **Agent brief** into your agent tool.
3. Fill in the variables.
4. Run the verification steps before merging or shipping.

```text
Goal: Add a workflow card for fresh-context code review.
Scope: README.md, workflows/, templates/, docs/ only.
Non-goals: Do not change CI, repo settings, secrets, or unrelated files.
Verification: Run python3 scripts/lint_repo.py and report the exact output.
Stop conditions: Ask before publishing, deleting files, or changing repository settings.
```

Start here: [`templates/agent-brief.md`](templates/agent-brief.md)

## Workflow library

| Workflow | Use when | Output |
| --- | --- | --- |
| [Spec → Plan → Implementation](workflows/01-spec-to-plan.md) | the request is vague or multi-step | design, plan, implementation checklist |
| [Parallel Agent Development](workflows/02-parallel-agent-development.md) | 2+ independent tasks can run at once | bounded subagent tasks + integration pass |
| [Root-Cause Debugging](workflows/03-bug-root-cause.md) | a bug is unclear or recurring | reproduction, hypothesis tree, verified fix |
| [Fresh-Context Code Review](workflows/04-fresh-context-code-review.md) | before merge or public release | spec compliance + quality/security review |
| [Security Review Sprint](workflows/05-security-review.md) | auth, secrets, network, permissions, parsers | threat model + findings with evidence |
| [Browser Runtime QA](workflows/06-browser-qa.md) | web UI or browser automation changes | screenshots, console/network checks, bug report |
| [Release Runbook](workflows/07-release-runbook.md) | publishing, deploying, or announcing | staged launch + rollback triggers |
| [Research Brief](workflows/08-research-brief.md) | market/API/library decisions | source-backed brief + recommendation |
| [Local AI Stack Setup](workflows/09-local-ai-stack.md) | self-hosted/local LLM agents | reproducible install and health checks |
| [Repo Growth Launch](workflows/10-repo-growth-launch.md) | making a public repo useful and discoverable | README, topics, demos, launch checklist |

For a compact index, see [`docs/WORKFLOW-CATALOG.md`](docs/WORKFLOW-CATALOG.md).

## Workflow card format

Each workflow uses the same structure:

- **Trigger** — when to use it.
- **Goal** — what should be true at the end.
- **Agent brief** — copy-paste prompt skeleton.
- **Steps** — ordered, bounded execution loop.
- **Verification** — evidence required before claiming success.
- **Failure modes** — common ways agents drift.
- **Human gate** — decisions that should not be automated silently.

Template: [`templates/workflow-card.md`](templates/workflow-card.md)

## Recommended tools and references

### Agent workflow inspiration

- [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) — Claude Code ecosystem list.
- [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) — agent skills and reusable capabilities.
- [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) — specialized subagent patterns.
- [milisp/codexia](https://github.com/milisp/codexia) — agent workstation patterns for Codex/Claude-style tools.
- [rohitg00/awesome-ai-apps](https://github.com/rohitg00/awesome-ai-apps) — real-world AI app examples.

### Agent frameworks and CLIs

- [OpenAI Codex](https://github.com/openai/codex)
- [OpenAI Agents Python](https://github.com/openai/openai-agents-python)
- [Anthropic Claude Code docs](https://docs.anthropic.com/en/docs/claude-code)
- [Aider](https://github.com/Aider-AI/aider)
- [OpenCode](https://github.com/sst/opencode)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [CrewAI](https://github.com/crewAIInc/crewAI)

### Quality gates

- [templates/pr-review.md](templates/pr-review.md)
- [templates/release-checklist.md](templates/release-checklist.md)
- [`scripts/lint_repo.py`](scripts/lint_repo.py) for local repository hygiene checks.

## What makes a workflow good?

A good workflow is:

- **portable** — works across tools, not just one vendor;
- **bounded** — says what the agent may and may not touch;
- **observable** — defines evidence before success claims;
- **recoverable** — has stop conditions and rollback steps;
- **short enough to use** — copyable in a real session.

## Contributing

Contributions are welcome. Please add workflows that are practical, tested, and vendor-neutral when possible.

Good contributions include:

- a workflow you have used on a real repo;
- a failure mode and the guardrail that prevented it;
- a reusable agent brief template;
- a launch, QA, review, or debugging checklist;
- a link to a high-quality public resource with a short explanation.

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a PR.

## Public launch plan

The ethical growth plan lives in [`docs/launch/GROWTH-PLAN.md`](docs/launch/GROWTH-PLAN.md). It explicitly avoids paid, fake, or bot engagement. If this repo helps, share it with people building with agents and star it so others can find it.

## License

MIT — see [`LICENSE`](LICENSE).

## Disclaimer

This repository is community-maintained and not affiliated with Anthropic, OpenAI, Cursor, Aider, SST/OpenCode, LangChain, CrewAI, or any other vendor mentioned here.
