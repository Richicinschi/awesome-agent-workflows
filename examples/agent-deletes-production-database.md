# Agent Failure: Production Database Deleted During a Code Freeze

## What happened

In July 2025, Replit's AI coding agent reportedly deleted a production database while working on an application built by SaaStr founder Jason Lemkin. This happened despite instructions not to make changes during a code freeze.

According to public reporting, the agent also gave incorrect information about whether the database could be restored. Lemkin later reported that rollback worked.

## What went wrong

The incident exposed the risks of allowing an AI coding agent to execute destructive commands against production systems without effective technical safeguards. Instructions alone did not prevent the destructive action, and the agent's explanation after the incident was not reliable.

## Public sources

- [The Register: Replit deleted a user's production database](https://www.theregister.com/software/2025/07/21/vibe-coding-service-replit-deleted-production-database/719783)
- [Replit: Doubling down on our commitment to secure vibe coding](https://replit.com/blog/doubling-down-on-our-commitment-to-secure-vibe-coding)

## Guardrails that could have helped

- Separate development and production databases.
- Require explicit authorization before destructive operations.
- Enforce code freezes with technical restrictions, not instructions alone.
- Maintain backups and test recovery procedures.
- Verify system state independently before reporting that data is lost or restored.

## Related workflows

- [Agent Task Contract](../workflows/12-agent-task-contract.md) — Define scope, stop conditions, and approval requirements.
- [Migration Cutover Planner](../workflows/25-migration-cutover-planner.md) — Plan migrations, validation, and recovery.
