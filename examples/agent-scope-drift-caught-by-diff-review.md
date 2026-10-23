# Worked Example: Diff Review Catches Agent Scope Drift

## Situation

A coding agent is asked to make a small UI change to a web application. The requested change is completed, but the agent also modifies unrelated components and styling files.

The agent reports that the task is complete. Before merging, the maintainer reviews the changed files and discovers edits outside the requested scope.

## Workflow selected

* Fresh-Context Code Review

## Agent brief

```text
Make the requested UI change.

Goal: update the specified UI component without changing unrelated behavior.

Scope: only the files and components required for this change.

Non-goals:
- Do not refactor unrelated components.
- Do not modify unrelated styling.
- Do not update dependencies.
- Do not change other UI components unless required by the task.

Verification required:
- Run the relevant tests or checks.
- Review git status and git diff before reporting completion.
- Confirm every changed file is required for the requested task.

Stop if: completing the task requires changes outside the defined scope.
```

## What the reviewer checks

1. Reads the issue and intended behavior.
2. Reviews the list of changed files.
3. Inspects the diff for unrelated edits.
4. Checks that each changed file is required by the task.
5. Runs the relevant tests or checks.
6. Confirms that no unrelated refactoring was introduced.
7. Reports exact evidence instead of relying on the agent's completion summary.

## Example finding

```text
Blocking issue: the requested UI change is correct, but the branch also modifies two unrelated components.

Evidence:
- src/components/Header.tsx was changed even though the task only required changes to Button.tsx.
- src/styles/theme.css contains unrelated spacing changes.

Required fix:
Revert the unrelated changes and keep only the files required for the requested UI change.
```

## Example final review

```text
Recommendation: approve after unrelated changes are removed.

Verification run:
- git diff --stat -> 3 files changed
- Reviewed git diff -> 2 unrelated changes identified
- Relevant test suite -> 18 passed
- After cleanup -> 1 file changed

Residual risk: future UI changes may still introduce accidental scope expansion; keep the changed-file review as a required completion step.
```

## Lesson

A successful implementation does not mean the agent stayed within scope. A final changed-file and diff review can catch unrelated edits before they reach the merge.
