# Agent Tool Comparison Matrix

This is a workflow-fit matrix, not a vendor ranking.

| Tool style | Best fit | Watch out for | Start with |
| --- | --- | --- | --- |
| Claude Code | multi-step repo work, planning, review, refactors | confident summaries without fresh verification | `01`, `04`, `15` |
| Codex CLI | terminal-native implementation and debugging | scope drift after broad repo inspection | `12`, `13`, `19` |
| Cursor agents | IDE-aware edits and fast review loops | unsaved buffers and broad file edits | `11`, `16`, `39` |
| Aider | focused patching with selected files | too many files weaken boundaries | `12`, `13`, `21` |
| OpenCode | terminal workflows and agentic coding loops | tool permissions and destructive commands | `35`, `36`, `40` |
| Local/self-hosted agents | privacy-sensitive tasks and offline stacks | weaker reasoning on high-risk review | `09`, `32`, `37` |
| Framework agents | repeatable workflows and automation | hidden state, retries, and side effects | `30`, `31`, `37` |

## Selection rule

Pick the workflow based on risk first, then tool fit. A high-risk task should use the security, release, migration, memory, or tool-integration workflow even if the agent tool has a convenient shortcut.
