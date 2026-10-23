---
name: fresh-context-code-review
description: "Use before merging or trusting agent-authored code. Get one independent review from a reviewer that never saw the author's reasoning, re-runs the evidence itself and ends with file:line findings and a verdict."
---

# Fresh-Context Code Review

Status: field-tested. Generated from the workflow card at https://github.com/Richicinschi/awesome-agent-workflows/blob/main/workflows/04-fresh-context-code-review.md; edit the card, not this file.

## Goal

One independent pass by a reviewer that never saw the author's reasoning. It works from the raw diff, the raw evidence files and commands it runs itself. It ends with file:line findings and an explicit verdict: APPROVE or CHANGES REQUESTED.

## Agent brief

```text
You are reviewing a change with no prior context. Do not trust any summary.

Inputs (raw only):
- Diff or branch: [branch, PR number or commit range]
- The goal, in the requester's own words: [goal]
- Raw evidence: [test logs, data files, generated tables]
- Commands you may run: [test, lint, build, dry-run commands]
- Forbidden: [editing files, pushing, merging, production, secrets]

You were deliberately NOT given the author's explanation, their summary
of results, or their list of what they already checked.

Do:
1. Read the diff and the code it touches. Assume there is a bug until
   you have shown there is not.
2. Run the checks yourself. Record the exact command, its exit code and
   the pass, skip and fail counts.
3. For each new or changed test, name the production change that would
   turn it red. If you cannot name one, flag the test.
4. For each claim in the PR text, docs or findings, point to the line,
   table row or command output that supports it. Flag any sentence that
   is stronger than its evidence.
5. Reproduce or trace a suspected bug before you report it.

Output:
- Findings: file:line, severity, why, suggested fix
- Commands run, with exit codes and counts
- Claims you could not verify
- Verdict: APPROVE or CHANGES REQUESTED
```

## Steps

1. **Decide where the review goes.** Put one independent review at the end of a piece of work. Do not run an implementer, a spec reviewer and a quality reviewer after every mechanical task. Keep multi-round review for work that is risky, complex or ambiguous.
2. **Start a genuinely fresh context.** Use a new session or a sub-agent that did not see the conversation. A reviewer that shares the author's context grades the author's story instead of the code. If your tool supports it, make the reviewer read-only.
3. **Hand over raw material, not conclusions.** Give the diff, raw logs, data files and the goal as first written. Leave out the author's summary and their "what I verified" list. A reviewer handed a conclusion tends to confirm it.
4. **Fix the review order.** Correctness first, then project conventions, then security, then simplification. Style comments never outrank a correctness question.
5. **Re-run the evidence instead of reading it.** The reviewer runs the tests itself, on the exact commit under review. If the change is already in use, also check the checkout that actually runs it: a fix confirmed in a worktree can leave the main checkout running old code. Take the exit code of the command itself, not of a pipe. Capture stdout and stderr. Compare pass, skip and fail counts with a recorded baseline.
6. **Ask of every test: what would make it go red?** Break the line a test claims to protect and confirm that test fails. Be most suspicious of casts in test helpers, inputs built by hand in the shape the consumer expects, and assertions on one field of a larger result. For a deep pass, use [Agent-Generated Test Review](https://github.com/Richicinschi/awesome-agent-workflows/blob/main/workflows/41-agent-generated-test-review.md).
7. **Treat prose as claims.** Point every sentence in the PR description, docs or findings at a line, a table row or an output. A reason written next to a number is a second claim and needs its own evidence.
8. **Prove before asserting.** Reproduce or trace each suspected bug before it goes in the findings. An unproven finding costs the author as much time as an unproven claim costs the reviewer.
9. **Return a fixed format with a verdict.** Each finding gets file:line, severity, why and a fix. The review ends with APPROVE or CHANGES REQUESTED. "Looks good" is not a verdict.
10. **Check the fixes too.** Corrections made after review are new, unreviewed text and code. Put them through the same checks before you merge.

## Verification checklist

- [ ] The reviewer's context held none of the author's conversation, summary or conclusions.
- [ ] The reviewer ran the checks itself, on the exact commit under review.
- [ ] Each check is recorded as command, exit code, and pass, skip and fail counts.
- [ ] Counts match the baseline, or each drop in passes or rise in skips is explained.
- [ ] Each new or changed test has a named break that turns it red, or is flagged.
- [ ] Each claim in the PR text or docs points to evidence; overstated sentences are listed.
- [ ] Each finding has file:line and severity, and was reproduced or traced.
- [ ] The review ends with an explicit verdict.
- [ ] Changes made in response to the review were checked again.

## Failure modes

- **Same-context review.** The reviewer inherits the author's assumptions and checks that the story hangs together.
- **Review of the summary.** The reviewer reads "all tests pass" and never runs the command.
- **Self-review mistaken for review.** Checking that each sentence matches a table catches typos. It cannot catch a table that answers the wrong question.
- **Ceremony on routine work.** A review after every mechanical task repeats itself and reads as noise, which buries the one review that matters.
- **The wrong tree.** A pass in a worktree says nothing about the checkout that runs. The case where that happened is told in [Git Worktree Agent Lanes](https://github.com/Richicinschi/awesome-agent-workflows/blob/main/workflows/35-git-worktree-agent-lanes.md).
- **Unproven findings.** The reviewer reports a bug it never reproduced, and the author wastes a cycle disproving it.
- **Unchecked corrections.** The fix for a finding introduces a new error that nobody reviews.

## Human gate

The human reads the verdict and the findings, not the author's summary, and decides whether to merge. CHANGES REQUESTED blocks the merge until the fixes are made and checked again. Only the human can override it, and the override is written down.
