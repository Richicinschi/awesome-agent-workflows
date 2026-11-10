# LazyMind Skill → Workflow Adapter

Use this adapter when a reusable Agent Skill needs explicit state, durable
artifacts, a human approval boundary, and recovery from a failed step. Keep the
native Skill for a short, single-session job where those boundaries add more
ceremony than value.

This example converts this repository's field-tested
[`long-running-task-checkpoint`](../../plugin/skills/long-running-task-checkpoint/SKILL.md)
Skill into a reviewable [LazyMind](https://github.com/LazyAGI/LazyMind)
Workflow. It is a candidate mapping: the contract and local checks have been
reviewed, but this exact conversion has not been run end to end.

## Pinned source and native path

- Repository: [`Richicinschi/awesome-agent-workflows`](https://github.com/Richicinschi/awesome-agent-workflows)
- Commit: [`af73039caed88767d81496687290657fe3ede5f6`](https://github.com/Richicinschi/awesome-agent-workflows/commit/af73039caed88767d81496687290657fe3ede5f6)
- Skill: [`plugin/skills/long-running-task-checkpoint/SKILL.md`](https://github.com/Richicinschi/awesome-agent-workflows/blob/af73039caed88767d81496687290657fe3ede5f6/plugin/skills/long-running-task-checkpoint/SKILL.md), Git blob `6c3508a461bd4adfeaa82ab3294f74a1945251ab`
- License: MIT

The native path is to load that Skill in a compatible coding agent and follow
its brief in one session. Its inputs are the job, expected duration, input and
output paths, machine limits, and names of required secrets. Its outputs are a
stable job name, log command, output-count command, latest heartbeat and counts,
and clean-stop evidence.

## When the Workflow path helps

Use a Workflow when launch approval, observation, stop/retry decisions, and
final verification should be separate states. This prevents a disconnected
agent session from becoming the only record of what ran and prevents a retry
from silently discarding the first attempt's logs.

1. Install LazyMind using its [Quick Start](https://github.com/LazyAGI/LazyMind#quick-start).
2. Add the pinned Skill source above, then choose **Skill → Workflow**.
3. Compare the generated inputs, outputs, steps, tool permissions, and failure
   paths with the pinned Skill before publishing it.
4. Keep command execution disabled until a human has reviewed the exact command,
   working directory, mounts, resource limits, and external effects.

Conversion does not install a container runtime, grant shell access, provide
credentials, or authorize a production job.

## Workflow contract

Preserve these stages and handoffs:

1. **Scope** — record the command, expected duration, inputs, outputs, baseline
   counts, resource limits, working directory, and secret names without values.
2. **Preflight** — verify the supervisor or container runtime, paths, mounts,
   capacity, and required executables. A missing dependency blocks launch.
3. **Launch approval** — present the exact execution plan. Keep the Workflow
   pending until a human approves external effects and resource use.
4. **Start** — create one stably named supervised job and save its identity,
   start time, command hash, and log command as artifacts.
5. **Observe** — capture periodic progress, heartbeat timestamps, output counts,
   and resource status. Silence beyond the declared interval is a failed check,
   not proof that the job is healthy.
6. **Recover** — preserve the prior job identity and logs before any retry. Stop,
   restart, or repeat expensive work only after a human decision.
7. **Verify and hand off** — compare outputs with the expected or previous run,
   record the process exit code and shutdown evidence, and list remaining gaps.

The launch plan hands off to the human approval state. The approved plan hands
off to the supervisor. Logs and counts hand back to observation and final
verification; they are not replaced by a generic success message.

## Restricted trial

Start with a disposable three-step job that writes only inside a temporary test
directory and emits one progress line and heartbeat per step. Do not mount a
real dataset, load credentials, or target a shared machine.

Check that the Workflow:

- remains pending before launch approval;
- records the exact job identity and command hash after approval;
- retains all three progress lines and heartbeats as an artifact;
- verifies the expected output count rather than trusting a running status; and
- preserves the first attempt's logs when a second run exits non-zero, then
  exposes an explicit retry decision instead of starting one automatically.

If shell or supervisor tools are unavailable, stop after generation and
preflight. Mark execution and recovery as unverified rather than simulating a
successful run.

## Human gate and limits

Ask before starting work on a shared machine, using credentials, changing an
external system, killing or restarting a job, retrying paid work, or deleting
outputs or volumes. The operator should verify the approval state, missing-tool
boundary, and preserved-log behavior before relying on this mapping.

This adapter does not claim that LazyMind improves job reliability, that the
conversion has been field-tested, or that this repository endorses LazyMind.
