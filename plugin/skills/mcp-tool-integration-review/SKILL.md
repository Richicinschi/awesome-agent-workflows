---
name: mcp-tool-integration-review
description: "Use when adding or changing an MCP server, tool, plugin, or external integration. Let nothing reach an agent until it passes a security scan, a human has read what it can execute and reach, and it fills a real gap; adopt only the smallest safe part."
---

# MCP and Tool Integration Review

Status: field-tested. Generated from the workflow card at https://github.com/Richicinschi/awesome-agent-workflows/blob/main/workflows/37-mcp-tool-integration-review.md; edit the card, not this file.

## Goal

Nothing reaches an agent's context or tool list until it has passed a security scan, a human has read what it can execute and reach, and someone has checked that it fills a real gap. What gets adopted is the smallest safe part, rewritten in house style, with its upstream and licence recorded.

## Agent brief

```text
You are executing the "MCP and Tool Integration Review" workflow.

Candidate: [repo URL, package name, MCP server, or skill path]
Job it would do: [what the human wants it for]
What we already have for that job: [existing skills, tools, scripts, docs]
Scanner: [scanner command; static pass only unless spend is approved]
Forbidden: installing, enabling or running the candidate before the gate clears;
           copying files into the live skills or tools folder; paid scan passes.

Do, in order:
1. Scan the candidate before cloning or installing it. Save the report to a file.
2. Triage every finding by reading the flagged file and line.
3. List what it can execute, read, write and reach over the network.
4. Fetch the licence and the default branch's last commit date from the source.
5. Propose one disposition: SKIP, FOLD (into which existing item), NEW SKILL,
   or NEW AGENT, with a one-line reason.

Required output:
- Scan score and verdict; each finding marked real or false positive, with file:line
- Capability table: commands, file paths, env vars, network hosts, secrets it touches
- Licence (fetched, not inferred) and the attribution line to keep
- Disposition and reason; for SKIP, why it died, so nobody re-evaluates it
- The exact parts to adapt, if any, and what to strip
```

## Steps

1. **Scan first, as a hard gate.** Run a skill or package security scanner before you clone, install or enable anything. Some scanners accept a remote git URL, so the code never lands in your tree. Default to the static pass. An LLM semantic pass may be billable; run it only when a human approves the spend. Save the report.
2. **Triage by reading the flagged line, not the score.** A critical finding means stop and read. Prompt injection, data exfiltration or privilege escalation in code the tool actually runs is a hard block until a human clears each finding. Static heuristics cannot tell security or devops docs from malware, so check each finding at file:line before you believe it or dismiss it. The deciding question: is this executable payload, or documentation and templates?
3. **Map what it can execute and reach.** For an MCP server or tool: every command it spawns, every path it reads or writes, every env var and secret it asks for, every host it calls, and whether it runs code it downloads. For a skill: scripts it tells the agent to run, install commands, and any instruction that widens permissions. Write it down as a table.
4. **Check the source, not the shop window.** Fetch the licence file; no licence means no right to adapt, whatever the star count. Read the default branch's last commit date, not a "last pushed" field that fires on any branch. Compare the package publish date with repo activity. Note a single maintainer, no security contact, past CVEs, and risky features such as deserialization or running third-party code.
5. **Decide the disposition against what you have.** SKIP if an existing skill, script or doc already does the job; this is the most common outcome. FOLD the one good idea into an existing item. NEW SKILL only for a real gap. NEW AGENT when the thing is an autonomous scan, report and act role. For an MCP server, ask whether a `curl` call or two lines of code would do the same job.
6. **Check it works outside its home framework.** Skills generated for one framework often hardcode its runtime: its CLIs, daemons and state folders. Copied alone they are inert. If a candidate needs a runtime you will not install, treat it as reference reading.
7. **Adapt only the safe parts.** Rewrite what you keep in your own conventions. Strip everything the scan flagged that you do not need. Bump pinned dependency versions that have known vulnerabilities. Retune defaults to your policy instead of inheriting upstream's.
8. **Record attribution.** Put the upstream repo, path and licence in the adapted file's metadata. Keep the licence file where the licence requires it (ShareAlike, notices). Log the disposition with its reason, skips included.
9. **Bound it at the tool layer.** Install at the narrowest scope, project rather than user-wide, with the fewest permissions. Where a rule must never break, enforce it with a hook that blocks the command, then test the hook by feeding it a forbidden command and checking that it refuses.
10. **Land it through review.** Commit the adaptation on its own branch and let a human merge. Do not install from the agent's session straight into a shared skill or tool folder.

## Verification checklist

- [ ] A saved scan report exists for the exact version adopted, dated before the install.
- [ ] Every finding above low has a file:line and a real or false-positive verdict.
- [ ] A capability table lists commands, paths, env vars, network hosts and secrets.
- [ ] The licence was fetched from the repo and permits the planned use.
- [ ] The disposition names the existing item the candidate was compared against.
- [ ] Adapted files carry upstream repo, path and licence in their metadata.
- [ ] Any enforcing hook was fed a forbidden input and blocked it.
- [ ] Every skipped candidate has a one-line reason on record.

## Failure modes

- Installing first and scanning later, so the scan reviews code that has already run.
- Trusting a red score blindly. To static rules, devops and security skills can look exactly like malicious ones.
- Trusting a green score blindly. A scanner is a gate, not an oracle; still read what the tool executes.
- Reading popularity as fitness: stars without a licence, recent pushes on a side branch, a README written before an OS update broke the trick it relies on.
- A licence the tooling cannot see. An API can report "no assertion" for a noncommercial licence, and lists and LLMs then pass it on as if it were permissive.
- Copy-and-install: adopting a whole folder when one idea was worth folding in, which breeds duplicate skills.
- Mistaking "related to my stack" for "is a skill". Framework dependencies belong in a package manager and starter templates in a clone, not in the agent's skill folder.
- Treating zero adoptions as failure, so a weak candidate gets through to justify the review.

## Human gate

A human clears every high or critical finding before adoption, approves any paid scan pass, approves tools that can read secrets, write outside the repo, call the network or run downloaded code, and merges the adaptation.
