---
name: ci-red-to-green
description: "Use when cI fails after an agent change. Reproduce or explain CI failure before pushing fixes."
---

# CI Red-to-Green Reproducer

Status: field-tested. Generated from the workflow card at https://github.com/Richicinschi/awesome-agent-workflows/blob/main/workflows/19-ci-red-to-green.md; edit the card, not this file.

## Goal

Reproduce the failing item alone, with its full output and its real exit code. Name the component that failed, with evidence, and mark the cause as measured or inferred. Fix that cause, then show the check green with pass, skip and fail counts that match the baseline.

## Agent brief

```text
A check is red. Find out what actually failed before changing anything.

Context:
- Failing check: [job name, script, or probe line]
- Raw log: [full log file or link, not a summary]
- Last known green: [commit and its pass, skip and fail counts]
- Exact command the check runs: [command, working directory, env]
- Allowed scope: [files and commands]
- Forbidden: [skipping or deleting tests, marking tests flaky,
  loosening thresholds or timeouts, pinning a version as the fix,
  editing the baseline, pushing just to let CI try again]

Do:
1. Read the raw log from the first error. Decide whether the job ran
   at all. Quota, billing, runner and spawn errors are not code
   failures.
2. Re-run only the failing item, alone, with the check's exact command.
   Capture stdout, stderr and the exit code of that command itself.
   No pipes.
3. Name the component that failed. Print the real exception and the
   real names involved. A plausible story or a matching changelog
   entry is a hypothesis, not a cause.
4. Fix the cause. Re-run the item alone, then the whole check, on the
   checkout that actually runs the code.
5. Compare pass, skip and fail counts with the last green run.

Output:
- Did the job run: yes or no, with the log line that shows it
- Reproduction command, exit code and the key output lines
- Cause, marked MEASURED (with evidence) or INFERRED
- Fix and files changed
- Counts before and after, against the baseline
```

## Steps

1. **First ask whether the check ran at all.** Some reds have nothing to do with the code: a job that never started because an account hit its spending limit, a runner that refused to spawn the process, a probe run from a copy of the repo where the projects are missing. Read from the first error, not the last line.
2. **Get the whole raw log.** Capture both stdout and stderr, because some tools print their summary to stderr. Do not add verbosity flags on top of the project's own config. A second quiet flag can delete the summary line.
3. **Re-run the single failing item alone.** Use the check's exact command, working directory, environment and flags. A timeout during a busy full run may be machine load. Run the item by itself before calling it a regression.
4. **Take the exit code of the command itself.** Not the exit code of a pipe, and not the status of an `echo` that ran after it. Know which tools return non-zero on success, so a false red does not train you to ignore exit codes.
5. **Name the component that failed before naming a cause.** Print the real exception and list the real names involved. If a test counts results before checking for an exception, a crash and an empty result look the same. A changelog entry that matches the symptom is only a hypothesis. Mark every cause MEASURED or INFERRED.
6. **Fix the cause, not the check.** Do not skip the test, mark it flaky, raise the timeout, loosen a threshold or pin a dependency version on an inferred cause. Those need a human decision.
7. **Verify on the tree that runs.** Confirm the fix in the checkout that actually executes, not only in the worktree or branch where you made it.
8. **Read every step of a multi-step gate.** A gate whose first step prints "passed" and whose second step dies looks like a gate that ran. Static analysis passing does not mean the tests ran.
9. **Compare counts against the baseline.** A drop in passes or a rise in skips is a failure until explained. Never record a baseline you have not seen printed yourself. Never change the baseline in a commit that does not also change the code that moved it.
10. **If you changed the check itself, prove it can still go red.** Break a fixture on purpose, re-run, see red, restore. A check that cannot go red is decoration.

## Verification checklist

- [ ] A log line shows whether the job actually ran.
- [ ] The failing item was reproduced alone with the check's exact command.
- [ ] Stdout, stderr and the exit code of the command itself were captured, with no pipe in between.
- [ ] The failing component is named with evidence, and the cause is marked measured or inferred.
- [ ] No test was skipped, deleted or marked flaky, and no threshold, timeout or version pin changed, without human approval.
- [ ] The fix was confirmed on the checkout that runs the code.
- [ ] Every step of a multi-step gate left its own output.
- [ ] Pass, skip and fail counts match the baseline, or each difference is explained.
- [ ] Any change to the check itself was shown to go red on a deliberate break.

## Failure modes

- **A job that never ran gets diagnosed as broken code.** A billing or runner error sends the agent hunting for a bug that is not there.
- **The red lies about its cause.** An error handler that maps every non-numeric exit status to "timeout" reports a millisecond spawn failure as a 900-second timeout.
- **A matching changelog entry becomes the cause.** The guess gets written into a version pin, notes and handoffs, and outlives the bug.
- **A pipe or an echo swallows the exit code.** The run looks green and exited 1.
- **A partial green.** The linter passes, the test runner never starts, and the gate reads as passed.
- **Load mistaken for a regression.** Tests that spawn workers and bind ports time out on a busy machine.
- **Skips replace passes.** The suite still prints a large "passed" number while tests quietly stopped running.
- **The checker's own parsing breaks.** Windows line endings defeat a regex that strips timings, so every run "regresses" against its own baseline.

## Human gate

Ask before disabling, skipping or deleting a test, marking it flaky, raising a timeout, loosening a threshold, pinning a version or editing a baseline. Before any of these, show the human the reproduction output and whether the cause was measured or inferred.
