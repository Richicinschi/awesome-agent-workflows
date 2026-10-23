# Agent Task Contract and Scope Box

> **Status: field-tested.** Distilled from briefing subagents and parallel coding-agent sessions in a one-person studio that runs up to ten sessions at once (2026).

## Trigger

You are about to hand a task to an agent that does not share your context: a subagent, a second session, another tool or model. It matters most when other agents are live in the same workspace, or when several briefs come out of one plan.

## Goal

A brief the agent can execute without your conversation: one outcome, a measured list of files it may edit, the forbidden actions that matter in this workspace, the lessons earlier agents paid for, a done condition that is a command, and a report you can check against disk.

## Agent brief

```text
Goal: [one sentence describing the outcome, not the activity]

First, read [path to the dispatch-lessons file]. It lists environment facts and
mistakes earlier agents made. Follow it.

Workspace: [absolute repo or worktree path]. Use absolute paths in every command.

Scope box:
- Edit only: [measured file list]
- Read as needed: [paths]
- Preserve: [what must survive unchanged: history entries, public names, approved wording]
- Never: [commit / switch branches / stash / clean / stage everything],
  write [shared files], run [builds, deploys, paid or public actions],
  change [shared rules or interfaces]

Rules for the change: [exact rules, plus one worked before-and-after example]

Done when: [acceptance criteria]
Verify with: [exact command]. Report the exit code and the raw summary line,
not a paraphrase.

Stop and report instead of guessing if the work needs a file outside the box,
a rule is ambiguous, or verification fails.

Report:
- Files changed (must be a subset of the edit list)
- Files in the edit list you did not change, and why
- Verification command, exit code, summary line
- New friction: anything the next agent should be told up front
```

## Steps

1. **Check the task deserves a brief.** If the brief would be longer than doing the work, or the task needs judgement, crosses repositories, or needs git operations, keep it. For routine, well-specified work, one brief and one final review beat a reviewer agent per task.
2. **Write the goal as an outcome.** "Every page uses the new product name and historical entries are untouched", not "update the naming".
3. **Measure the edit list.** Produce it with a search or a listing and paste it into the brief. Say what to preserve and what to rewrite.
4. **Name this workspace's forbidden actions.** "Be careful" does nothing. List the concrete shared surfaces: git operations in a shared checkout, builds and caches, a shared browser session, shared ledgers, rules other agents rely on, plus anything public, paid or destructive.
5. **Make it self-contained.** Assume the agent sees only the brief: goal, exact files, exact rules, what to preserve, acceptance criteria, absolute paths, and environment facts such as which interpreter works.
6. **Point at the lessons file first.** The first instruction after the goal is "read the lessons file". Agents have no memory of each other, so the file is the only carrier of what earlier agents learned, and unlike a chat message it survives context compaction.
7. **Define done as a command.** Give the exact verification command and ask for the exit code read directly, not through a pipe, plus the raw summary line.
8. **Check the report against disk.** Compare `git diff --name-only` with the edit list, look at every listed file that did not change, and rerun the verification yourself.
9. **Feed the lessons file.** Append any new friction the agent reported. If you had to send a mid-task correction, that correction goes into the file before the next brief goes out.

## Verification checklist

- [ ] Someone who has not seen your conversation could execute the brief as written.
- [ ] The edit list came from a command, and the preserve list is explicit.
- [ ] Forbidden actions name concrete shared resources in this workspace.
- [ ] Done is a command with an expected result.
- [ ] The returned diff is a subset of the edit list.
- [ ] Every edit-list file that was not changed is explained in the report.
- [ ] The lead reran the verification and read the exit code directly.
- [ ] New friction, and any correction sent mid-task, is in the lessons file.

## Failure modes

- **Context the agent never had.** The brief leans on your conversation, so the agent fills the gaps with guesses.
- **An inferred edit list.** A list written from memory can come out too narrow, and the gap shows only after the agents finish. A case where that happened four times is in [Parallel Agent Development](02-parallel-agent-development.md).
- **A silent scope box.** Nothing forbids git operations or builds in a shared checkout, so a well-meaning agent commits, stashes or rebuilds under other live sessions.
- **Trusting the summary.** A success report can hide a skipped file; only the files on disk show it. The skipped spec file is told in [Parallel Agent Development](02-parallel-agent-development.md).
- **Re-teaching by message.** A correction sent in chat helps one agent; the next agent repeats the mistake.
- **Briefs from a stale plan.** A rename landed in code but not in the plan, so the next wave was briefed against a field that no longer existed.
- **Ceremony on routine work.** Identical implement-then-review cycles on mechanical tasks add noise, not safety. The loop the human stopped as too repetitive is told in [Fresh-Context Code Review](04-fresh-context-code-review.md).

## Human gate

The human approves the scope box (edit list, forbidden actions, done condition) before dispatch whenever the task touches a shared surface, public state, money or deletion. Widening the box mid-task is a human decision: the agent stops and reports instead of expanding scope on its own.

## Field notes

- The dispatch-lessons file came out of a multi-agent audit-fix campaign on a Python repository in July 2026, run as a sequence of implementer agents. One ended its turn while a full test suite was still running in the background, leaving its work uncommitted. The human's directive: learn from agent limitations as they happen, so no later agent repeats them. The fix was a file next to the campaign's progress ledger, not a better message to that one agent: unlike the orchestrator's context, the file survives compaction, and it can be audited.
- What went into it was mostly environment facts no agent could guess: the system interpreter was broken and a specific one had to be used, the shell's working directory reset between commands, git staging needed discipline, and commit signing could hang.
- The 24-file find-and-replace that a brief of about 30 lines could have sent off in parallel is told in [Parallel Agent Development](02-parallel-agent-development.md).
- A check judged through a pipe reported success while the command was returning 1, which is why the brief asks for the exit code read directly. More cases in [when the verification evidence itself was wrong](../examples/field-story-verification-evidence-lied.md).

## Related workflows

- [Parallel Agent Development](02-parallel-agent-development.md)
- [Git Worktree Agent Lanes](35-git-worktree-agent-lanes.md)
- [Fresh-Context Code Review](04-fresh-context-code-review.md)
- [Context Compaction and Handoff](36-context-compaction-handoff.md)
- [Worked example: diff review catches agent scope drift](../examples/agent-scope-drift-caught-by-diff-review.md)
