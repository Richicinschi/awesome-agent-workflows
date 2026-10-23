# Field Story: Eight Ways a Green Test Suite Proved Nothing

> **Field-tested.** Observed in July 2026 in a studio where coding agents write most of the code: one feature branch (XP, streaks and progress for a TypeScript learning app), plus one case from a separate Python repository.

## What the work was

Implement a gamification feature with tests, and report when the suite was green.

## What went wrong

The suite was green. Eight separate assertions in that one branch could not have failed, each in a different way:

1. **A fixture that named ids that do not exist.** The migration test used exercise ids from a day of the curriculum that has no exercises. The code skips unknown ids, so the test never reached the migration it was named after.
2. **An assertion comparing two identical inputs.** "Pays the same with hints as without", but the input type had no hints field. Both calls were literally the same call.
3. **A guard its input could never reach.** A `Math.max(1, ...)` floor on a value whose smallest possible non-zero input was 1.83. Delete the guard and the suite stays green.
4. **A missing clamp nobody would notice.** Deleting `Math.max(0, totalXp)` left all 14 tests green while the progress bar would render -20%. The test checked only one field of the result.
5. **A type cast in a test helper.** `as UserProgress` let a field rename (`xp` to `totalXp`) typecheck cleanly with every test passing. Without the cast it is a compile error.
6. **and 7. Two terms you could delete from a total.** Removing `+ reviewXp` or `+ streakXp` from the total each left the suite green. No test ever set those values non-zero and read the total.
8. **A test re-aimed by editing its numbers.** After a behaviour change, updating the expected values would have left the test asserting a state that was already true before the action ran.

The same shape showed up in an unrelated Python repository: **1,029 green tests over a broken engine.** Production data loaded timestamps in milliseconds, while every test fixture built its time grid in nanoseconds. A raw integer comparison was off by a factor of a million, which silently disabled three parts of the engine for three weeks. The tests passed because the fixtures never once used the unit production uses.

## What evidence revealed the issue

None of the eight was caught by the suite passing. Each was caught by review or by mutation testing: break one line of production code on purpose, then check that a specific test goes red.

The Python case was caught by asking an old, recorded result to reproduce exactly. It did not, and the gap led to the unit mismatch. That one cheap reproduction check outperformed the thousand-test suite.

## Guardrail that would have prevented it

- **Mutate before you trust.** For each new test, delete or change the line it claims to protect and confirm that test fails. An assertion you have only ever seen pass is a hypothesis, not a test.
- **Never edit expected values to match new behaviour.** Re-derive what the test should assert. Editing the numbers is how a suite quietly stops testing anything.
- **Be most suspicious of** casts in test helpers, assertions that check one field of a larger shape, totals built from several inputs, and fixtures whose data type differs from production's.
- **Keep one recorded result that must still reproduce.** It catches whole classes of bugs that unit tests share a blind spot with.
- **Make the human gate explicit.** An agent's "tests added, all green" is a claim about the suite, not about the behaviour.

## Related workflow cards

- [Agent-Generated Test Review](../workflows/41-agent-generated-test-review.md)
- [Regression-Test-First Bug Fix](../workflows/13-regression-test-first-bugfix.md)
- [Fresh-Context Code Review](../workflows/04-fresh-context-code-review.md)

## Lesson

A test suite can be green because it cannot fail. Agents produce these tests fluently and in volume, so passing tests are not evidence that the agent built the right thing. Proof that a test can go red is.
