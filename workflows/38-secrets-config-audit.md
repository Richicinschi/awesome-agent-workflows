# Secrets and Config Audit

> **Status: field-tested.** Distilled from preparing private repos for public or shared hosting in a one-person studio that runs up to ten coding-agent sessions at once (2026).

## Trigger

Before a repo's first public push, before a private repo is flipped to public, before it is handed to a cloud agent session or a third party, and before any CI or deploy setup that copies config off the machine.

## Goal

The repo, including every commit reachable from its history, carries only what the product needs. No secrets, keys or env files. No IP addresses or home-network details. No personal data. No traces of how the work was done. Anything that cannot be removed cleanly is escalated before the push, because a public push cannot be taken back.

## Agent brief

```text
You are executing the "Secrets and Config Audit" workflow.
Read-only: do not commit, rewrite history or push.

Repo: [path]
Destination: [public GitHub, shared cloud session, client handoff]
What the product needs to ship: [source, assets, build config, licence]
Known secret locations: [env files, key stores, CI variables]
Identifiers to search for: [names, emails, usernames, hostnames, home paths]

Do, in order:
1. List every tracked file and classify it: product, config, process trace, personal.
2. Scan the working tree AND the full history (all refs) for secrets, key patterns,
   env files, IPv4 and IPv6 addresses, hostnames, home paths, emails and names.
3. Scan commit messages and trailers, not only file contents.
4. Check archived web pages, PDFs and fixtures for embedded client addresses
   or download stamps.
5. Check each env or key file's encoding before trusting a clean search.

Required output:
- Findings table: commit, file, match, category, still in the tree (yes or no)
- Files that must leave the repo, and how to keep them out
- Whether history needs rewriting, or a fresh single-commit repo is simpler
- Every scan command run, with its match count, including the zero-match scans
```

## Steps

1. **Write down what the product needs.** List what belongs in the repo: source, assets, build and deploy config, licence, user docs. Everything else has to justify itself. Agent instruction files, specs and plans, audit reports, session notes and memory files are process traces; they stay on your machine.
2. **Find the secrets in the tree.** Look for env files, key files, tokens in config, and secrets pasted into docs or examples. Keys stay server-side: never in frontend code, fixtures or committed files. Ship an example env file with variable names and no values.
3. **Check encodings before trusting a clean search.** An env file saved as UTF-16 puts a null byte after every ASCII character, so a plain text search for a key pattern can miss it, and a naive env loader mangles it. Detect the encoding and decode before you scan.
4. **Scan the full history, not the working tree.** Deleting a file in a later commit leaves it in every earlier one. Search all refs, for example `git grep -E '([0-9]{1,3}\.){3}[0-9]{1,3}' $(git rev-list --all)` for IPv4, and the same form for IPv6, key patterns, hostnames, home paths and emails. A dedicated secret scanner over the history makes a good second pass.
5. **Hunt network details, comments included.** IP addresses, VPN exit addresses, LAN ranges, router layout and machine hostnames do not belong in any commit: not in config comments, debug notes, logs or commit messages. Describe the finding in words instead ("the direct connection reaches the host; the VPN exit is refused"). Fixtures that need an address use the documentation ranges 192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24 and 2001:db8::/32. Tools that record which machine ran something write a label, not a hostname.
6. **Check captured documents.** Saved web pages can print the fetching client's address inside their scripts, and PDFs can carry "downloaded by" stamps. Scan archived pages for dotted quads and remote-address keys, and extract PDF text before committing the file.
7. **Strip personal data and process traces.** Search for names, emails other than the git author's, usernames and home-directory paths. Read commit messages and trailers too: co-author and session trailers are process traces. Keep local-only files out with `.git/info/exclude` when even the ignore list should not reveal what they are.
8. **Choose rewrite or restart.** If history carries a leak, either rewrite the history or start a fresh repo with one clean commit, keeping the old history private and backed up (for example as a git bundle). Either way, rotate any secret that was ever committed; removing it from history does not un-leak it.
9. **Re-scan exactly what will be pushed.** Run the same scans on the rewritten or fresh repo and record zero matches per pattern. Then a human pushes.

## Verification checklist

- [ ] Every tracked file is classified, and none is a process trace or a personal file.
- [ ] Secret, IP, hostname, path, email and name scans ran over all refs, with commands and match counts recorded.
- [ ] Commit messages and trailers were scanned.
- [ ] Env and key files were checked for encoding before they were scanned.
- [ ] Archived pages and PDFs were scanned for client addresses and download stamps.
- [ ] Test fixtures use documentation address ranges only.
- [ ] Any secret that was ever committed has been rotated, not only deleted.
- [ ] The final scan ran on the exact repo being pushed and found zero matches.

## Failure modes

- Scanning only the working tree. The leak was removed in a later commit, but it is still in every earlier one, and the first push publishes them all.
- Treating a comment as harmless. An address in a config comment is as public as one in code.
- A scan that cannot see the file: a UTF-16 env file, a binary format, a PDF searched as raw bytes.
- Forgetting commit metadata. Messages and trailers carry names and process traces that no file scan reads.
- Hiding private files with a `.gitignore` that names them, which publishes the list of what you meant to hide.
- Real private LAN addresses in test fixtures.
- Deleting a committed secret and calling it fixed without rotating it.
- An agent rewriting history or force-pushing on its own initiative.

## Human gate

A human approves any history rewrite or force-push, makes the first public push or the private-to-public flip, and rotates or revokes any secret that was ever committed. The agent audits and proposes; it does not publish.

## Field notes

- A research repo's history carried a home IP and a VPN exit IP in a config-file comment. The comment had already been removed from the tree but was still in 51 commits, so publishing the repo meant rewriting the whole history. Since then: no IPs or home-network details in any commit, and a full-history scan before every first push.
- Saved copies of a public statistics portal's pages turned out to print the fetching client's address in their script. Those copies stay out of git, and archived pages and PDFs are scanned before they are committed.
- Before a learning app's repo went to cloud agent sessions, with a possible public flip later, it was rebuilt as a new repo with one clean commit of product files only. The old full-history repo stays private, local-only files are excluded through `.git/info/exclude`, and cloud sessions get their instructions in the prompt, not in committed files.
- The studio's root env file turned out to be UTF-16 encoded, which a naive env loader mangles. The key in it is server-side only, never in frontend code or a commit.
- History rewrites are never the agent's call. The agent's permission layer blocks them, and any filter-repo pass waits for the owner's explicit go-ahead.

## Related workflows

- [MCP and Tool Integration Review](37-mcp-tool-integration-review.md)
- [Release Runbook](07-release-runbook.md)
- [Security Review Sprint](05-security-review.md)
- [Agent Memory Hygiene Review](32-agent-memory-hygiene-review.md)
