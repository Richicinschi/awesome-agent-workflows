# Agent Memory Hygiene Review

> **Status: field-tested.** Distilled from keeping a file-based agent memory (a one-line index loaded every session, one fact per file, and a tagged archive vault) usable across up to ten concurrent coding-agent sessions in a one-person studio (2026).

## Trigger

- The always-loaded memory index or instructions file is near its load budget (a size hook warns, or the agent notices).
- A session just proved a memory wrong, or two memories disagree.
- Memory feels stale, duplicated, padded with task status, or holds something that should not be there.
- End of a session, as part of the close-out sweep.

## Goal

Memory stays small enough to load every session, true as of today, and lossless. Space is freed by moving full text to a tagged archive with a pointer left behind, never by shortening or deleting. Every correction is visible.

## Agent brief

```text
You are running an "Agent Memory Hygiene Review".

Memory layout:
- Always-loaded index: [path; one line per memory file]
- Memory files: [folder; one fact per file, each with a type and a one-line description]
- Archive vault: [path; verbatim entries grouped and #tagged]
- Load budget: [characters or lines for the index and the instructions file]

Why this review now: [over budget / memory proved wrong / conflict / sensitive content / end of session]

Rules:
- Never free space by shortening, summarising or deleting. Move the full text to the vault, tag it, leave one pointer line.
- Before acting on a memory that names a file, flag, branch, service or running process, check it still exists.
- Corrections stay visible: date them and say what was wrong.
- Never copy secrets, credentials or other people's personal data into the vault. List them for the human.

Report:
- Index and instructions-file size before and after, against the budget
- Entries moved: tag used, pointer left, archive search that found them
- Memories corrected: old claim, new claim, evidence
- Duplicates merged and conflicts found
- Items that need a human decision
```

## Steps

1. **Measure against the budget.** Record the size of the index and of the always-loaded instructions file before touching anything. A small script that prints total size and lists dated entries oldest to newest makes the next steps mechanical.
2. **Check each memory against the world.** A memory is a claim as of the day it was written. For every entry that names a file, flag, branch, container or service, check it exists now. Mark stale entries and do not act on them until checked.
3. **Write corrections into the memory, visibly.** When a memory is wrong, add a dated note that says what was wrong and what is true now. A silent overwrite erases the reason the old claim was believed, which is the trap the next session needs to avoid.
4. **Merge near-duplicates.** Two files about one fact drift apart and end up disagreeing. Sharpen the better file, move the other one's unique detail into it, and vault the leftover. Then make sure every memory file has exactly one index line and every index line points at a file that exists.
5. **Apply the admission test.** A memory earns its place only if it is non-obvious (not derivable from the code, git history or instructions file), durable (still true next month), decision-changing, and carries its why. Task status and run output belong in session notes or the project's state file. Convert relative dates like "yesterday" to absolute ones.
6. **Vault, do not cut.** When over budget, move whole entries verbatim into the archive, grouped and tagged by project and by status (for example closed, parked, historical, gated). Leave one pointer line in the index. Moving with a pointer is allowed. Cutting words is not.
7. **Verify each move before removing the original.** Write the entry to the archive, search the archive for a unique phrase from it, and only then remove it from the index. If the write or the search fails, stop. Check by date and title so the same entry is not archived twice.
8. **Keep the instructions file meaningful.** Keep the newest one or two dated handoff entries, the rules, the stack and the pointers, and archive older history. Do not strip it to hit a number. A cold session must still be able to orient from it.
9. **Separate sensitive content.** Secrets, credentials, other people's personal data or confidential material are the one case where vaulting is wrong, because a verbatim copy spreads it. List these for the human instead.
10. **Re-measure and report.** Confirm both files are under budget, and restore any vaulted entry whose project has become active again.

## Verification checklist

- [ ] Sizes before and after are recorded, and both files are under budget.
- [ ] For every moved entry, an archive search for a unique phrase from it returned a hit, and a pointer line remains in the index.
- [ ] Every index line points to an existing file, and every memory file has exactly one index line.
- [ ] Every correction carries a date and names the old claim. Nothing was replaced silently.
- [ ] Every memory the review acted on was checked against the current state of the file, flag or service it names.
- [ ] Lossless test passed: for anything removed from the index, the full original can be opened by tag or link.
- [ ] Sensitive items are listed for the human and were not copied into the archive.

## Failure modes

- The agent "summarises to save space". The detail it cuts is exactly the context a future session needed.
- The agent deletes from the index first and archives second. The archive write fails and the entry is gone.
- A stale memory steers a plan. It says a machine is always busy, or a service is always up, after that stopped being true.
- A wrong memory is overwritten without a note, so the reasoning that produced it gets repeated later.
- The sweep becomes a diary: session status, run output and "currently doing X" fill the index until it no longer fits the budget.
- A rule is stored without its why and gets rationalised away the first time it is inconvenient.
- An index line points at a file that was renamed, so the memory silently stops loading.
- A secret or a client's personal data is vaulted verbatim along with the rest.

## Human gate

The human approves any deletion or redaction of a memory, any change to user-profile facts or to a standing rule they gave, and every retention decision about sensitive content. Moving an entry to the vault with a pointer needs no approval, because nothing is lost.

## Field notes

- The owner stated the rule explicitly and repeated it: memory is never freed by loss. Everything must be saved somewhere and tagged so it can be found. The test the studio adopted: after freeing space, can you still open and read the full original by tag or link? If not, undo it and vault instead.
- The first curation of the always-loaded instructions file, in June 2026, found it at 61.8k characters against a roughly 40k warning limit. One pass moved 11 dated handoff entries verbatim into an archive page and brought the file to 31.6k. The procedure checks each entry is in the archive before removing it. A hook now measures after edits and at session start. It only reminds; it never edits or blocks.
- A memory said the main workstation was permanently saturated by an always-on container fleet. In October 2026 the container runtime turned out to have been down for days after a reboot, and the high RAM reading was two kernel memory leaks. The memory was not replaced. It gained a dated "sharpened" paragraph: the rule stands while the fleet runs, but measure first.
- The index works because each line is short and points elsewhere. Many lines end with a pointer to the vault for the full text, so the index stays loadable while the detail stays findable.

## Related workflows

- [Context Compaction and Handoff](36-context-compaction-handoff.md)
- [Prompt and Policy Change Control](31-prompt-policy-change-control.md)
- [Documentation Drift Audit](26-documentation-drift-audit.md)
- [Secrets and Config Audit](38-secrets-config-audit.md)
