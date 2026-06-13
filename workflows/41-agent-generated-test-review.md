# Agent-Generated Test Review

## Trigger

An agent added or changed tests, and you need to decide whether those tests protect real behavior before trusting the patch.

## Goal

Accept only tests that would catch the intended regression or contract break, while rejecting tests that only mirror implementation details, mocks, or the agent's own assumptions.

## Agent brief

```text
You are executing the "Agent-Generated Test Review" workflow.

Context:
- Repo/system: [name and path]
- User-visible behavior or regression being protected: [behavior]
- Test files or diff to review: [paths or PR]
- Allowed commands: [test and inspection commands]
- Forbidden scope: [production, secrets, unrelated rewrites, broad refactors]

Required output:
- Test intent summary
- Evidence that each test fails for the right reason before or without the fix
- Assertions that protect user behavior or public contracts
- Mocking and fixture risks
- Verification commands and results
- Required changes before merge
```

## Steps

1. **Restate the behavior under test.** Name the user path, API contract, bug, or invariant the tests claim to protect.
2. **Map each test to that behavior.** For every new or changed test, write one sentence explaining what failure it should catch.
3. **Check red/green evidence.** Prefer an actual failing run against the unfixed code. If that is not available, identify the smallest mutation or disabled fix that should make the test fail.
4. **Inspect assertions.** Favor observable behavior, outputs, state transitions, errors, events, or public API results. Flag assertions that only check private helper calls, call counts, or implementation order.
5. **Review mocks and fixtures.** Confirm mocks model meaningful boundaries and do not replace the behavior the test is supposed to verify. Keep fixtures minimal, named, and tied to the regression.
6. **Look for brittleness.** Flag broad snapshots, time/order dependence, random data, overspecified text, hidden network calls, and fixtures that will be painful to update.
7. **Run the narrowest relevant command.** Execute the specific test file or case first, then any local suite the repo expects for this area.
8. **Decide merge readiness.** Require fixes when tests pass without exercising the regression, only verify mocks, or lack evidence that the intended failure is covered.

## Verification checklist

- [ ] The protected behavior or contract is stated in user-facing terms.
- [ ] Each new or changed test has a clear failure it should catch.
- [ ] Red/green evidence exists, or the missing evidence is called out as a merge blocker.
- [ ] Assertions check behavior rather than private implementation details.
- [ ] Mocks do not replace the unit of behavior being claimed as covered.
- [ ] Snapshots and fixtures are narrow, named, and justified.
- [ ] Relevant test commands ran and their exact results are recorded.

## Failure modes

- The agent adds a test that repeats the implementation instead of checking the behavior.
- The test only proves that a mock was called.
- The test passes before the fix because the setup does not reproduce the bug.
- A broad snapshot hides the important assertion.
- Fixture data is large, anonymous, or unrelated to the regression.
- The reviewer accepts "tests added" as evidence without inspecting what they prove.

## Human gate

A maintainer decides whether missing red/green evidence is acceptable. Do not merge agent-generated tests that cannot fail for the intended reason without explicit human approval.

## Related workflows

- [Regression-Test-First Bug Fix](13-regression-test-first-bugfix.md)
- [Fresh-Context Code Review](04-fresh-context-code-review.md)
- [Agent Patch Intake Triage](16-patch-intake-triage.md)
