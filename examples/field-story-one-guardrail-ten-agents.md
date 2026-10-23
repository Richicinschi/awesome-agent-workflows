# Field Story: A Guardrail Built for One Agent Became a 90% False Alarm at Ten

> **Field-tested.** Observed in July 2026 in a one-person studio that runs up to ten coding-agent sessions at once from one workspace holding about 26 git repositories.

## What the agents were asked to do

Each session worked on its own project. A shared "session hygiene" check ran whenever a session tried to finish: if any repository in the workspace had uncommitted or untracked work, it blocked the session from ending and told it to clean up first.

With one agent, that rule was sound. Untidy state could only be that agent's own mess.

## What went wrong

The check looked at the whole workspace, but its message blamed the current session. With several agents live, those stopped being the same thing. A session was blocked by files that only another, still-running session could resolve.

If ten sessions are live and each is mid-edit in its own repo, any one of them sees nine repos it does not own. The false-block rate is roughly (N-1)/N: 90% at ten sessions, and it grows with every project added. In one afternoon the check blocked four consecutive attempts to finish because of another agent's files.

The worse failure was one step further. A session-archiving procedure finalized every "pending" session except the current one. Of five pending sessions that day, three were still live. Obeying the hygiene check would have sealed two in-flight sessions belonging to other agents.

## What evidence revealed the issue

Measuring every repository in the workspace that day:

- only two of 26 repos tripped it;
- both had a last commit less than half an hour old, so they were being actively worked in;
- the other 24, idle from 15 hours to over 40 days, were spotless.

Nothing had rotted. The check was reporting activity and calling it untidiness.

## Guardrail that fixed it

Separate activity from rot by recency, and block only on states that cannot be recovered:

- a repo touched in the last 6 hours gets a note, never a block;
- a branch checked out in a worktree, or carrying an open pull request, is never "stray";
- work older than 48 hours gets a recommendation;
- **only unpushed commits block**, because work that exists on no remote is the one state that cannot be recovered.

Eight tests pin those rules so a later edit cannot quietly widen what the check may stop a session for.

The archiving tool now refuses to finalize any transcript written in the last 15 minutes unless explicitly forced. Finishing or cleaning up another session's work is a human decision, never an agent's.

## Why the rule lives in code, not in the prompt

The same rule had been written in plain language in the agents' instructions. It lost twice in one day, both times to the agent that had just written it. Rules that must never break belong in a check. Only rules that need judgement belong in a paragraph.

## Related workflow cards

- [Parallel Agent Development](../workflows/02-parallel-agent-development.md)
- [Git Worktree Agent Lanes](../workflows/35-git-worktree-agent-lanes.md)
- [Prompt and Policy Change Control](../workflows/31-prompt-policy-change-control.md)

## Lesson

Any check written while one agent ran becomes wrong in the same way once several run: it evaluates shared state but blames the current session. Before adding agents, ask of every guardrail: "whose work is this check really looking at?" Then block only what cannot be undone, and never let one agent finalize what another still owns.
