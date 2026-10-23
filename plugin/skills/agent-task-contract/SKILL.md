---
name: agent-task-contract
description: "Use when before delegating a task to an AI agent. Give the agent a contract that prevents drive-by edits and unsupported success claims."
---

# Agent Task Contract and Scope Box

Status: field-tested. Generated from the workflow card at https://github.com/Richicinschi/awesome-agent-workflows/blob/main/workflows/12-agent-task-contract.md; edit the card, not this file.

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
- **An inferred edit list.** In one sub-project the list was too narrow four separate times, each discovered only after the agents finished.
- **A silent scope box.** Nothing forbids git operations or builds in a shared checkout, so a well-meaning agent commits, stashes or rebuilds under other live sessions.
- **Trusting the summary.** An agent reported success while silently skipping an entire assigned spec file. Only checking the files on disk caught it.
- **Re-teaching by message.** A correction sent in chat helps one agent; the next agent repeats the mistake.
- **Briefs from a stale plan.** A rename landed in code but not in the plan, so the next wave was briefed against a field that no longer existed.
- **Ceremony on routine work.** Identical implement-then-review cycles on mechanical tasks added noise, not safety, and the human stopped them as too repetitive.

## Human gate

The human approves the scope box (edit list, forbidden actions, done condition) before dispatch whenever the task touches a shared surface, public state, money or deletion. Widening the box mid-task is a human decision: the agent stops and reports instead of expanding scope on its own.
