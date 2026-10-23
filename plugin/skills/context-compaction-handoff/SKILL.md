---
name: context-compaction-handoff
description: "Use when a long agent session is about to compact, hand off, or restart. Close a long session so the next one can continue from files alone: work pushed, branches tidy, lessons in memory, current state written as verified reality."
---

# Context Compaction and Handoff

Status: field-tested. Generated from the workflow card at https://github.com/Richicinschi/awesome-agent-workflows/blob/main/workflows/36-context-compaction-handoff.md; edit the card, not this file.

## Goal

The next session, or this one after compaction, can continue from files alone: work is on a remote, branches are tidy, durable lessons are in memory, each project's current state is written as verified reality, and open items are named. Nothing important lives only in the context window.

## Agent brief

```text
You are closing out a session so the next one can continue safely.

Context:
- Repos touched this session: [list]
- Project state files: [path to each project's current-state section]
- Memory folder and index: [paths]
- Campaign lessons file, if this is a multi-agent run: [path or none]
- Session archive: [location or none]

Work these in order. If a step does not apply, say which and why.
1. Run the workspace health or hygiene check. Fix failures before going on.
2. Commit in coherent groups; each message says why. Push, or open a PR where main is protected.
3. Confirm zero unpushed commits per repo, against every remote.
4. Delete merged branches this session created. Leave any branch checked out in another
   worktree or pushed by another live session. Keep branches with open PRs or ones the
   human asked to keep.
5. Sweep durable lessons into memory. Correct any memory this session proved wrong.
6. Archive the transcript verbatim if the setup keeps one.
7. Update each project's current-state line to what you verified, not what you attempted.
8. Re-run the hygiene check.

Never: merge a PR, force-push, rewrite history, tag, or finalize another live session's work.

Report:
- What shipped (commit hashes, PR numbers)
- What was verified, and how
- What is deliberately left open, and why
- What the next session should pick up first
```

## Steps

1. **Establish the real state first.** Run the workspace's health or hygiene check before closing anything. Never close out against the state you assume. Fix hard failures, and report warnings.
2. **Get every change onto a remote.** Group changes into coherent commits, never one "wip" blob, with messages that explain why. Then count unpushed commits per repo against all remotes, not only the default one, since a fork remote can legitimately hold the work. Unpushed commits are the one state that cannot be recovered.
3. **Tidy only your own branches.** Delete merged branches this session created, local and remote. Leave any branch checked out in another worktree or pushed by another live session, even if it looks abandoned (see [Git Worktree Agent Lanes](https://github.com/Richicinschi/awesome-agent-workflows/blob/main/workflows/35-git-worktree-agent-lanes.md)). Keep branches with an open PR or that the human asked to keep, and say which survived and why.
4. **Treat the context window as volatile.** Anything the next agent needs goes into a file: a progress ledger, a lessons file, the project's state file. A compaction summary is a hint, not evidence. The next agent should re-check anything it would otherwise trust from that summary.
5. **Run the memory sweep.** It is the step most often skipped. Write only what is non-obvious, durable, decision-changing and carries its why. Correcting a memory this session proved wrong is worth more than any addition. Writing nothing is a valid outcome, so say so instead of padding.
6. **Put orchestration friction in a lessons file.** In a multi-agent campaign, sequential agents have no memory of each other, so the orchestrator is the only carrier of what went wrong. Keep a lessons file beside the progress ledger, make "read the lessons file" the first instruction of every dispatch, and append after each task. If you had to send an agent a correction, that correction belongs in the file.
7. **Archive the transcript verbatim, and only your own.** Copy the raw transcript first and write the summary page from it, one page per session. Never finalize a transcript another session may still be writing. Leave that to the human.
8. **Write current state as verified reality.** Update each touched project's state line from what you ran and saw, not from intent. Keep the summary line short and point to the archive for history. If the state file is over its budget, archive old dated entries instead of trimming them (see the memory hygiene card).
9. **Confirm the gate, then report.** Re-run the hygiene check. It is clean, or you name each item left open and why. A broken state you cannot fix goes in the report in plain words. A quiet handoff over a broken state is the failure this workflow exists to prevent.

## Verification checklist

- [ ] The unpushed-commit count is 0 for every touched repo, checked against all remotes, and the command output is recorded.
- [ ] Only merged branches this session created were deleted, and every surviving non-default branch has a stated reason (open PR, the human asked to keep it, or it belongs to another worktree or live session).
- [ ] Each current-state line matches something run this session (a test, a command, a commit hash), not a plan.
- [ ] The memory sweep result is recorded: entries written or corrected, or an explicit "nothing durable this session".
- [ ] Every correction sent to a subagent by message is now a line in the lessons file.
- [ ] The final hygiene check is clean, or each open item is named with its reason.
- [ ] A cold session could start from the files alone. The report names the first thing to pick up.

## Failure modes

- The compaction summary becomes the only carrier of state, and the next agent treats it as evidence.
- The transcript is archived but memory is not updated, so the next session starts from stale ground truth.
- The state line records intent ("fixed the importer") when the fix was attempted, not verified.
- Untidiness is left "for later". It is cheap to fix in the session that created it and expensive weeks later.
- The memory sweep is padded with invented entries to look productive.
- The agent finalizes or cleans up a session that is still live in another window.
- Each subagent is re-taught by message, so the lesson is lost at the next dispatch.
- The handoff merges a PR or force-pushes "to finish cleanly".

## Human gate

The human merges PRs and approves any force-push, history rewrite or tag. The human decides whether to finish or clean up another session's work. Any claim that unfinished work is safe to resume without re-verification needs explicit human approval.
