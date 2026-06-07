# Workflow Catalog

This catalog summarizes the initial workflow set. Each workflow is intentionally short, operational, and tool-agnostic.

## Categories

### Planning and execution

- [`01-spec-to-plan.md`](../workflows/01-spec-to-plan.md) — convert fuzzy ideas into specs, then implementation plans.
- [`02-parallel-agent-development.md`](../workflows/02-parallel-agent-development.md) — split independent work across bounded agents.

### Debugging and verification

- [`03-bug-root-cause.md`](../workflows/03-bug-root-cause.md) — reproduce first, fix second.
- [`04-fresh-context-code-review.md`](../workflows/04-fresh-context-code-review.md) — review without author-context contamination.

### Safety and launch

- [`05-security-review.md`](../workflows/05-security-review.md) — threat-model and evidence-backed findings.
- [`07-release-runbook.md`](../workflows/07-release-runbook.md) — staged rollout, rollback, and first-hour checks.
- [`10-repo-growth-launch.md`](../workflows/10-repo-growth-launch.md) — make a public repo discoverable without spam.

### Research and runtime checks

- [`06-browser-qa.md`](../workflows/06-browser-qa.md) — verify real browser behavior.
- [`08-research-brief.md`](../workflows/08-research-brief.md) — collect and cite current sources.
- [`09-local-ai-stack.md`](../workflows/09-local-ai-stack.md) — setup and verify local/self-hosted AI agent stacks.

## Selection rule

Choose the workflow whose **trigger** matches the risk you face. If two workflows apply, run the higher-risk one first:

1. Security/data/production risk.
2. Ambiguous requirements.
3. Hard-to-reproduce bugs.
4. Parallelization opportunity.
5. Launch/visibility work.
