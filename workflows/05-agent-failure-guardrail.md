# Agent Failure: Acting Before Verifying

## What the agent was asked to do
An AI coding agent was asked to update a configuration file and report the changes.

## What went wrong
The agent made changes based on an assumption about the existing configuration instead of checking the full file first. This could have overwritten an important setting.

## What evidence revealed the issue
A review of the proposed changes showed that an existing setting had been changed unexpectedly.

## Guardrail that would have prevented it
Before editing, the agent should read the relevant file and identify settings that must remain unchanged. After editing, it should review the diff and run relevant checks before reporting completion.

## Follow-up workflow to add
Add a workflow checklist that requires agents to inspect files before editing, review the final diff, and verify the result before claiming the task is complete.
