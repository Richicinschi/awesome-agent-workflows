# v0.4.0 — Field-tested cards, honest status, installable skills

The early workflow cards were generated from two templates: 30 of them shared one body word for word and the other 10 shared another. This release starts fixing that, in the open.

Highlights:

- Rewrites 14 cards from real practice in a one-person studio running up to ten coding-agent sessions at once, each with specific steps, failure modes, a human gate and field notes: [Spec → Plan → Implementation](../../workflows/01-spec-to-plan.md), [Parallel Agent Development](../../workflows/02-parallel-agent-development.md), [Fresh-Context Code Review](../../workflows/04-fresh-context-code-review.md), [Research Brief](../../workflows/08-research-brief.md), [Repo Growth Launch](../../workflows/10-repo-growth-launch.md), [Agent Task Contract](../../workflows/12-agent-task-contract.md), [Regression-Test-First Bug Fix](../../workflows/13-regression-test-first-bugfix.md), [CI Red-to-Green](../../workflows/19-ci-red-to-green.md), [Agent Memory Hygiene](../../workflows/32-agent-memory-hygiene-review.md), [Git Worktree Agent Lanes](../../workflows/35-git-worktree-agent-lanes.md), [Context Compaction and Handoff](../../workflows/36-context-compaction-handoff.md), [MCP and Tool Integration Review](../../workflows/37-mcp-tool-integration-review.md), [Secrets and Config Audit](../../workflows/38-secrets-config-audit.md) and [Long-Running Task Checkpoint](../../workflows/40-long-running-task-checkpoint.md).
- Every card now carries a status: 14 field-tested, 1 candidate, 26 draft. Drafts are labelled as drafts, and each has a target verification sentence for whoever rewrites it.
- Ships the field-tested and candidate cards as skills: a Claude Code plugin (`/plugin install agent-workflows --marketplace Richicinschi/awesome-agent-workflows`) whose `SKILL.md` files also work with Codex CLI. The skills are generated from the cards, so there is one source.
- Adds a searchable catalog site with status, risk and category filters.
- The lint now enforces status lines, field notes on field-tested cards, unique verification sentences and skills that match their cards.

Want to help? Pick a draft card and make it real: see [CONTRIBUTING](../../CONTRIBUTING.md).
