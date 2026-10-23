---
name: parallel-agent-development
description: "Use when multiple independent tasks can run at once. Split work safely and integrate results."
---

# Parallel Agent Development

Status: field-tested. Generated from the workflow card at https://github.com/Richicinschi/awesome-agent-workflows/blob/main/workflows/02-parallel-agent-development.md; edit the card, not this file.

## Goal

Finish the phase faster without agents colliding. Every task owns a measured, disjoint set of files. Shared files, builds, browsers and commits have exactly one owner: the lead. The lead accepts work only from what is on disk, then integrates and verifies once on the combined result.

## Agent brief

```text
You are one of [N] agents working in parallel on [phase goal]. Other agents are live at the same time.

Before anything else, read [path to the dispatch-lessons file].

Your task: [one-sentence outcome]
Workspace: [absolute path to your worktree or repo]
Edit only these files: [measured list]
Shared files you must NOT write: [ledgers, metadata, indexes]. Put that data in your report instead.

Do not:
- commit, stash, switch branches or stage files,
- run the production build, clear build caches or stop dev servers,
- drive the shared browser session [unless this is the browser lane],
- change shared rules, interfaces or config, even if they look wrong. Report it instead.

Use absolute paths in every command. The working directory can reset between commands.

Done when: [acceptance criteria]
Verify with: [exact command]. Read its exit code directly, never through a pipe.

Report:
- Files changed (must be a subset of your edit list)
- Files in your list you did not change, and why
- Verification command, exit code, raw summary line
- Data for the shared files, if any
- New friction or environment surprises a later agent should know
```

## Steps

1. **Decide what stays with the lead.** Keep architecture and judgement calls, the split itself, anything spanning more than one repo, anything that needs git operations, and any task whose brief would be longer than the work. Delegate bulk, uniform, file-independent work.
2. **Measure each task's file list.** Produce it with a search or a file listing, never from memory, and check that no two lists intersect. If two do, merge those tasks or run them in sequence.
3. **Take shared files out of the tasks.** Ledgers, metadata files, indexes and shared config are written by nobody in the wave. Workers return that data in their reports and the lead merges it once.
4. **Give every shared resource one owner.** Disjoint files are not enough. Name the resources that collide anyway: the git index (only the lead commits), build output and dependency caches (no parallel builds, no cache clearing), a shared browser automation session (one agent per wave drives it), and running dev servers.
5. **Freeze the rules before dispatch.** If briefs are generated from a plan, patch the plan first, so the next wave is not briefed against a name that no longer exists. A rule change that comes up mid-wave waits for a sequential pass afterwards.
6. **Isolate workers that share a repo.** One worktree and branch per implementer (see [Git Worktree Agent Lanes](https://github.com/Richicinschi/awesome-agent-workflows/blob/main/workflows/35-git-worktree-agent-lanes.md)), or one repo per agent. Start the longest-running tracks first, even before the plan document is finished.
7. **Dispatch the wave at once, sized to your limits.** Send every independent brief together. If your harness caps concurrent agents, read the cap from its error instead of guessing, and batch above it. Very large fan-outs can trip server-side rate limits, so prefer several waves of moderate size.
8. **Judge progress from disk only.** A dispatch acknowledgement looks the same for every agent, a quiet transcript does not mean an idle agent, and a final report can be wrong. Compare each worker's changed files against its edit list and rerun its verification yourself.
9. **Integrate centrally, verify once, record lessons.** Merge lanes one at a time, check `git diff --cached` before each commit, run the full check on the integrated tree, then commit from the lead. For mechanical work one review of the integrated result is enough; keep per-task review for risky or ambiguous tasks. Append every friction a worker reported, and every correction you had to send, to the dispatch-lessons file.

## Verification checklist

- [ ] Each task's file list came from a command, and no two lists intersect.
- [ ] `git diff --name-only` for each worker shows only files from its edit list.
- [ ] No worker committed, built, cleared a cache or drove the browser outside its assignment.
- [ ] Shared files were written once, by the lead, after the wave.
- [ ] Every assigned file is either changed on disk or explained in the worker's report.
- [ ] The full verification ran on the integrated tree, with the exit code read directly.
- [ ] `git diff --cached` before the final commit contains only intended changes.
- [ ] New friction is in the dispatch-lessons file before the next wave is briefed.

## Failure modes

- **Inferred file lists.** In one sub-project the guessed list was too narrow four separate times, each found only after the agents had finished.
- **A rule changed mid-flight.** A color mapping gained rules while eight agents were working. Their output disagreed with itself and needed a whole reconciliation task.
- **A shared browser.** Page selection in a shared browser automation server was global. One agent's navigation hard-reloaded another agent's page onto the wrong dev server and wiped its in-memory state. A named isolated context did not prevent it.
- **Commits from inside the wave.** Parallel commits race for the git index lock, and `git checkout [rev] -- [path]` silently stages a file that a later, unrelated commit sweeps in.
- **Trusting the report.** An agent claimed success while silently skipping an entire assigned spec file.
- **Reading meaning into silence.** A slow agent was taken as proof that dispatches above the limit queue. They did not; that wave was simply under the limit. A null result was over-read as a finding and later retracted.
- **Fan-out too wide.** In one fan-out of about 60 agents, about 36 of 62 calls were rate-limited by the server, the final synthesis step included.
- **Over-orchestration.** Repeating identical implement-then-review cycles on routine tasks until the human stopped it as too repetitive.

## Human gate

The human approves the split before dispatch: the task list, each edit list, and who owns each shared resource. Any change to a shared rule during a wave is the human's call and waits for a sequential pass. Merging the integrated result stays with the human.
