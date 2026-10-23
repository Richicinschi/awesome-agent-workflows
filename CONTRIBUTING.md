# Contributing

Thanks for improving Awesome Agent Workflows.

## What to add

Good PRs usually add one of these:

- a workflow card in `workflows/`;
- a reusable agent brief in `templates/`;
- a high-quality resource link with an explanation;
- a failure mode and guardrail from real agent work;
- a correction to unclear wording or broken links.

## Card status

Every workflow card carries a status line under its title, matching the `status` field in `agent-workflows.json`:

- **draft**: still the generic template the early cards were generated from. Its `verification` sentence in `agent-workflows.json` is the target a rewrite must meet. The most useful contribution is turning one into a real card.
- **candidate**: specific steps, failure modes and verification, reviewed, but not yet used on real work.
- **field-tested**: used on a real project, with a `## Field notes` section saying what happened. Only claim this for practice you have actually run.

To promote a card, rewrite its steps, checklist and failure modes for that workflow specifically, update its status line and `agent-workflows.json`, and give it its own `verification` sentence. The lint check enforces the status line, the field notes and unique verification sentences.

## Workflow contribution checklist

- [ ] The workflow has a clear trigger.
- [ ] The agent brief is copy-pasteable.
- [ ] The steps are ordered and bounded.
- [ ] Verification evidence is explicit.
- [ ] Human approval gates are stated.
- [ ] The workflow avoids vendor lock-in unless vendor-specific behavior is essential.

## Local checks

Run:

```bash
python3 scripts/lint_repo.py
```

## Style

- Be concrete.
- Prefer commands, checklists, and examples over theory.
- Do not include secrets, private customer data, or proprietary prompts.
- Avoid hype. Explain the operational value.

## Roadmap

See [`docs/ROADMAP.md`](docs/ROADMAP.md) for the next high-value contribution clusters.
