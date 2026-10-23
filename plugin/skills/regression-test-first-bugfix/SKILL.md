---
name: regression-test-first-bugfix
description: "Use when a bug has a concrete symptom or user report. Capture the bug as a test that goes red on the exact symptom, green after the fix and red again when the fix is removed, with the cause marked measured or inferred."
---

# Regression-Test-First Bug Fix

Status: field-tested. Generated from the workflow card at https://github.com/Richicinschi/awesome-agent-workflows/blob/main/workflows/13-regression-test-first-bugfix.md; edit the card, not this file.

## Goal

A test at the seam where the bug lives. It goes red on this exact symptom before the fix, green after it, and has been shown to go red again when the fix is removed. The cause goes into the commit, marked as measured or inferred.

## Agent brief

```text
You are fixing a bug test-first. Do not change production code until a
test reproduces the bug.

Context:
- Repo and test command: [repo, exact test command]
- Symptom as reported: [exact error text, wrong value, or steps]
- Where it shows up: [user path, data set, version, environment]
- Allowed scope: [files and commands]
- Forbidden: [editing existing expected values, skipping or deleting
  tests, production data, secrets]

Do:
1. Build one command that reproduces the reported symptom. Run it and
   keep the command and its output.
2. Turn it into a test at the seam where the bug happens. Use the same
   data types, units and producers that production uses.
3. Run the test on the unfixed code. It must fail with the reported
   symptom, not with a different error.
4. Make the smallest fix. Run the test: green. Re-run the command from
   step 1: fixed.
5. Prove the test can fail: undo the fix or break the line it protects,
   run the test unchanged, see red for the right reason, then restore.
6. Run the full suite. Compare pass, skip and fail counts with the
   counts from before your change.

Output:
- Reproduction command and its red output
- Test name, red output before the fix, green output after
- The break used to prove the test can fail
- Suite counts before and after
- Cause, marked MEASURED or INFERRED
```

## Steps

1. **Pin down the exact symptom.** Write down the error text, the wrong value or the input that triggers it. The test will assert this symptom, not "does not crash".
2. **Build a loop that can go red before you theorise.** One command, already run once, that drives the real code path and fails on this bug. It should be fast and give the same verdict every run. If you cannot build one, stop and say what you tried.
3. **Choose the seam where the bug lives.** A unit test that cannot reproduce the chain of calls that triggered the bug gives false confidence. If the bug sits between two modules, call the real producer and feed its real output to the consumer. If no correct seam exists, record that as a finding instead of writing a shallow test.
4. **Feed the test what production feeds the code.** Same data types, same units, real ids. A fixture that matches production's shape but not its type, or names ids that do not exist, never reaches the bug.
5. **Watch it fail for the right reason.** The red output must show the reported symptom. Order assertions so a crash cannot hide behind a count: assert there was no exception before you assert how many things were produced.
6. **Make the smallest fix, then re-run both loops.** The new test goes green. The original reproduction command from step 2 also goes green. Do not refactor while anything is red.
7. **Prove the test can fail.** Undo the fix, or delete the line the test protects, and confirm this specific test goes red. Run it unbroken first. Check that the break really changed behaviour, and that a red came from an assertion, not from a crash. Restore the code and leave no patched state behind for the next check.
8. **Do not re-aim existing tests.** If an old test now fails because behaviour changed on purpose, re-derive its expected value from the requirement. Never copy the new output into the expected value. The test name survives such an edit while the assertion stops testing anything.
9. **Compare counts, not colour.** Record pass, skip and fail counts before and after. A drop in passes or a rise in skips is a failure until it is explained.
10. **Write the cause down honestly.** State in the commit which hypothesis turned out correct, and mark it MEASURED or INFERRED. Remove temporary debug logging (tag it with a unique prefix so one search finds it all).

## Verification checklist

- [ ] The reproduction command and its red output were recorded before any production edit.
- [ ] The test's red output shows the reported symptom, not a nearby error.
- [ ] The test uses production's data types and units, and the real producer at the seam.
- [ ] The test is green after the fix, and the original reproduction no longer reproduces.
- [ ] A recorded break (fix undone or line deleted) turned this test red, and the code was restored.
- [ ] No existing expected values were edited and no tests were skipped or deleted, or each case was approved.
- [ ] Pass, skip and fail counts before and after are recorded, with no unexplained change.
- [ ] The commit states the cause and marks it measured or inferred; debug logging is gone.

## Failure modes

- **The test was written after the fix.** It has only ever been seen green, so it is a hypothesis, not a test.
- **Red for the wrong reason.** An import error or a broken fixture fails the test, and that gets counted as reproducing the bug.
- **A fixture that never reaches the code path.** Ids that do not exist are skipped, and the assertion compares nothing.
- **A fixture in a different unit or type than production.** The code works on test data and nowhere else.
- **A hand-built input at a seam.** The test builds the consumer's expected shape by hand, so it never sees what the producer really returns.
- **A count asserted before the exception check.** A crash and an empty result look the same.
- **A mutation check that lies.** It counts a crash as a catch, uses a break that changes nothing, or leaks a patch into later checks.
- **A plausible cause written as fact.** A matching line in a changelog becomes the "cause", and the real one is never looked for.

## Human gate

If the symptom cannot be reproduced, stop and ask for access, a captured artifact or permission to add instrumentation before making speculative changes. A human approves any edit to an existing test's expected values, any skipped or deleted test, and any fix that ships without a regression test because no correct seam exists.
