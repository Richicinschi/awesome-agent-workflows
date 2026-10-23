# Spec → Plan → Implementation

> **Status: field-tested.** Distilled from how a one-person studio turns vague requests into specs, plans and code while running up to ten coding-agent sessions at once (2026).

## Trigger

A request is vague, multi-step, or likely to cause rework if built directly. Also use it to harden a rough draft or a page of notes into a real spec. Skip it for trivial, unambiguous asks: just do those.

## Goal

Three artifacts, in order, each approved before the next starts: a decision-resolved spec with explicit non-goals and open questions, a plan of small tasks that each carry their own verification command, and an implementation that matches the plan. Nothing gets built on a guess.

## Agent brief

```text
You are running "Spec -> Plan -> Implementation". Do not write code until I approve the spec.

Target: [feature, system or refactor]
Starting point: [a one-line goal, or the path to a draft to harden]
Code and docs to read first: [paths]
Spec location: [path for the spec file]

Phase 1, drill:
- Read the code and docs above before asking anything. Note which files you read.
- Open with your one-sentence reading of the goal and a 0-100% confidence, with the reason.
- Ask exactly one question per turn. Every question carries your recommended answer:
  "My read: [X]. Agree, or override?"
- Track coverage: goal, users, scope and non-goals, architecture, interfaces, data,
  dependencies, errors, edge cases, testing, risks, rollout, open questions.
- Stop when you can predict my next three answers and every branch is resolved or deferred,
  or when I say "draft" or "stop".

Phase 2, confirm and write:
- Restate outcome, user, why now, success criteria, constraints, out of scope and key
  decisions. Wait for an explicit yes. "Sounds good" is not a yes.
- Write the spec. Unresolved items go under Open questions. Never fill them with guesses.

Phase 3, plan:
- Split the spec into tasks. Each task names its files, its verification command and the
  expected pass signal. Mark each task risky or mechanical.

Phase 4, implement (only after I approve the plan):
- Report per task: files changed, command run, actual output, deviations from the spec.
```

## Steps

1. **Decide whether the workflow is worth it.** A one-line fix needs no spec. A small feature may need a short brainstorm. A non-trivial feature, a system, a refactor or a rough draft gets the full drill.
2. **Ground the drill in the code.** The agent reads the relevant files and docs before the first question. Questions must be about what the code actually does, not what the agent imagines it does.
3. **Open with a hypothesis and a confidence number.** "My read: you want X. Confidence 55%, unsure whether it reuses Y." A wrong guess is fine. It gives the human something concrete to correct.
4. **Ask one question per turn, each with a recommended answer.** Reacting to a proposal is fast; composing an answer from scratch is slow. Two crisp answers in a row: go deeper, into edge cases and trade-offs. Two vague answers: offer a concrete default and narrow to yes or no.
5. **Probe answers that sound like what you are supposed to want.** Buzzwords like "scalable", "clean" or "modern", or "I think we should...", often hide the real requirement. Ask: "If you did not have to justify it to anyone, what would you actually want?"
6. **Track coverage and resolve every branch.** Keep the dimension checklist visible and mark each one covered, partial or open. When an answer opens sub-decisions, follow them before moving on. Scale the list to the task: a small feature will not need all thirteen.
7. **Stop on a testable threshold, then get a real yes.** Stop when the next three answers are predictable and nothing is unresolved, or when the human calls it. Restate the design line by line. Vague approval does not count; keep drilling the parts the human hesitates on.
8. **Write the spec and review it yourself.** Fill each section to its real complexity. Keep a decision log, one line per fork: "chose X over Y because Z". The non-goals section is the one that stops scope creep. Then scan for placeholders, contradictions, scope creep and any requirement that reads two ways, and fix them.
9. **Plan in small, verifiable tasks.** Each task lists the files it touches, the command that proves it, and the expected signal, for example "12/12 green". Mark tasks that touch infrastructure, data, secrets or money as risky.
10. **Implement with review proportional to risk.** Risky tasks get a review cycle each. Mechanical tasks are implemented directly, then verified once at the end. Finish with one independent review that gets the spec and the raw diff, not the implementer's summary.

## Verification checklist

- [ ] The spec exists at a known path and its non-goals section names at least one excluded item.
- [ ] Every applicable coverage dimension is either covered or listed under open questions.
- [ ] The decision log records each key fork with the rejected option and the reason.
- [ ] The human gave an explicit yes on the restated design, and the message is quoted or linked.
- [ ] The spec self-review found no placeholders, contradictions or two-way requirements.
- [ ] Every plan task names a verification command and an expected pass signal.
- [ ] Each completed task reports the command it ran and the actual output.
- [ ] Deviations from the spec were brought back to the human, not absorbed silently.
- [ ] The final review ran in a fresh context on the spec plus the diff.

## Failure modes

- **Drilling in the abstract.** Questions are not grounded in the code, so the spec designs against a system that does not exist.
- **Batched questions.** Five questions in one turn get one vague answer, and the branches stay open.
- **Questions with no recommended answer.** The human has to compose every reply, gets tired, and starts saying "whatever you think".
- **A should-want answer recorded as a requirement.** "Make it scalable" ends up in the spec with nothing behind it.
- **"Sounds good" taken as approval.** The agent starts building on a design the human never read closely.
- **Padding or guessing.** The spec is long because of filler, or open questions were quietly filled in.
- **Tasks with no verification command.** "Done" then means only that the agent stopped.
- **Review ceremony on routine work.** Repeating implementer plus two reviewers for every mechanical task produces noise, not safety.
- **Quoting an old plan as current.** Prices, store policies and tool versions in a plan go stale.
- **Agents re-learning the same environment facts.** Sequential agents share no memory unless someone writes the lessons down.

## Human gate

No implementation until the human gives an explicit yes on the restated spec, and again on the plan. Any change to the approved spec during implementation goes back to the human. Only the human decides what is deferred.

## Field notes

- The studio's drilling procedure combines two public, MIT-licensed agent skills: `interview-me` (from addyosmani/agent-skills: hypothesis plus confidence, restate and require a yes, the predict-the-next-three stop rule) and `grill-me` (from mattpocock/skills: resolve every branch, explore the code instead of speculating). It adds an adaptive one-question-at-a-time loop with commands such as `skip`, `coverage` and `draft`.
- Two lessons that shaped this workflow are told in full elsewhere: the per-task review loop the owner stopped as "too repetitive", behind step 10, in [Fresh-Context Code Review](04-fresh-context-code-review.md); and the implementer that ended its turn while a background test run continued, which led to a lessons file every later brief reads first, in [Agent Task Contract and Scope Box](12-agent-task-contract.md).
- A 24-section pre-development plan, from store submission to timeline, is referenced by section number rather than re-derived each time. Its pricing and policy claims are re-checked before being quoted, because a plan written months ago ages.

## Related workflows

- [Agent Task Contract and Scope Box](12-agent-task-contract.md)
- [Parallel Agent Development](02-parallel-agent-development.md)
- [Fresh-Context Code Review](04-fresh-context-code-review.md)
- [ADR Decision Capture from Threads](27-adr-decision-capture.md)
- [Context Compaction and Handoff](36-context-compaction-handoff.md)
- [Research Brief](08-research-brief.md)
