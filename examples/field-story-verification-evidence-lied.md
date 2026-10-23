# Field Story: When the Verification Evidence Itself Was Wrong

> **Field-tested.** Observed in July 2026 while coding agents ran health checks across about two dozen repositories in one workspace. Every defect below reported success or silence, never an obvious failure.

## What the agents were asked to do

Run each project's checks, report pass or fail with the exact output, and compare against a recorded baseline before claiming anything was healthy.

## What went wrong

The agents did report evidence. The evidence was wrong, in eight different ways:

1. **A pipe ate the exit code.** `node probe.mjs | tail -6` looked successful while the probe returned 1. The pipeline's exit status belongs to `tail`.
2. **The logged exit code came from the wrong command.** `node probe.mjs > log 2>&1; echo "EXIT=$?" >> log` made the shell's own exit status come from `echo`, so the task runner reported success for a run that had exited 1.
3. **A gate that was partly green read as a gate that ran.** A two-step gate printed `All checks passed!` from the linter, a native binary, then died before the tests started because the virtualenv's script launchers were broken. The tests had not run for two days.
4. **A doubled quiet flag deleted the summary.** The project's config already set `-q` for pytest. The checker added another `-q`, which became `-qq` and removed the summary line, so only a progress bar was left to read.
5. **The summary went to stderr.** One project printed its test summary to stderr, and the checker captured only stdout, so the result was invisible.
6. **Tests turned into skips after a folder move.** A project hardcoded its old absolute path in 19 files. After the move its data-dependent tests hit their `skipif` guards, so 17 tests went from running to skipped and the suite still read `857 passed`.
7. **A fix was verified on the wrong tree.** A fix was tested and confirmed in a git worktree while the main checkout, the one that actually runs, kept executing the old version.
8. **A red check lied about its cause.** Node 22 refuses to spawn `.cmd` files. The error handler mapped any non-numeric exit status to "timeout", so a spawn failure that took milliseconds was reported as a 900-second timeout.

## What evidence revealed the issue

Comparing counts, not colours. Each one surfaced when someone compared the pass, skip and fail split against a known-good baseline, read the raw exit code, or re-ran the single failing project by itself, instead of trusting the green or red the check printed.

## Guardrail that would have prevented it

- Never judge a check through a pipe. Capture the exit code of the command itself.
- Capture both stdout and stderr, and let each project's own config decide verbosity.
- Record a baseline of pass, skip and fail counts. A drop in passes or a rise in skips is a failure until explained.
- Prove each gate can fail: break a fixture, re-run, see red. A check that cannot go red is decoration.
- Verify against the tree that actually runs the code, not the branch where you made the fix.
- Give "could not start" its own exit code, separate from timeout and failure.
- When writing a cause into a commit, pin or handoff, mark whether you measured it or inferred it.

## Related workflow cards

- [CI Red-to-Green Reproducer](../workflows/19-ci-red-to-green.md)
- [Agent Patch Intake Triage](../workflows/16-patch-intake-triage.md)
- [Workflow Evaluation Harness](../workflows/30-workflow-evaluation-harness.md)

## Lesson

Asking an agent for evidence is necessary but not sufficient. The evidence pipeline has its own bugs, and they fail upward: a skipped test, a swallowed summary and a lost exit code all look exactly like health. Trust counts against a baseline, not the colour of the check.
