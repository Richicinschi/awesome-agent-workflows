# Long-Running Task Checkpoint

> **Status: field-tested.** Distilled from running long test sweeps, builds and data collectors beside an always-on container fleet on one shared workstation in a one-person studio that runs up to ten coding-agent sessions at once (2026).

## Trigger

- A build, test sweep, migration, scrape, backfill, benchmark, audit or batch job is expected to run longer than about three to five minutes.
- A long job is already running and someone asks whether it is healthy, or whether it is safe to stop.

The trigger is duration, not the kind of job. A long test sweep counts as much as a data pull.

## Goal

The job runs somewhere the agent session cannot kill it. Its logs outlive the session, its progress can be read days later, it stops cleanly, and it ends with evidence of what it produced, not just a status that says it ran.

## Agent brief

```text
You are starting, or checking, a long-running job: [what it does].

Context:
- Expected duration: [estimate]
- Inputs and expected outputs: [paths; what files or rows should appear, roughly how many]
- Machine: [what else runs there; CPU and memory available]
- Secrets needed: [names only, never values]

Requirements:
- Over about five minutes: run it as a named container or another supervised service, never a foreground or background shell.
- Code in the image. Data on the host through a bind mount. Secrets mounted read-only.
- Set CPU and memory limits.
- Unbuffered output. Every N units, one plain progress line: done/total, percent, ok and failed counts, ETA. No redrawing bar.
- A heartbeat line at a fixed interval, so a silent log means trouble.

Report:
- Job name, and the command that shows its logs
- Expected output, and the command that counts it
- Last heartbeat time and current counts
- How a stop will be judged clean (exit codes)
```

## Steps

1. **Estimate before launching.** If the job may run longer than about three to five minutes, it goes into a named container or supervised service. Shorter jobs can stay a plain command.
2. **Run it outside the session's process tree.** A background shell dies with the session, and so does its output. Some agent harnesses also kill background shells when the machine runs low on memory. A named container keeps its logs, can restart after a crash or reboot, and its inspect output says why it stopped.
3. **Keep the data out of the container.** The image carries code only. Data lives on the host and is bind-mounted, so tearing down the container and its volumes cannot delete it. Mount secrets read-only. Resolve tool paths inside the image instead of assuming the host's toolchain is there.
4. **Cap resources on a shared machine.** A native process has no ceiling. Set CPU and memory limits so the job cannot starve the services sharing the box, and check the container runtime is actually up before assuming anything about what is running.
5. **Log progress as periodic lines.** Turn off output buffering, or the log shows nothing until a flush. Print one line every N units, for example `[####....] 41% | 407/987 | OK 309 | ETA 1h 22m`. A redrawing progress bar turns a log stream into thousands of fragments.
6. **Emit a heartbeat whose absence is the alarm.** An empty log looks the same whether the job is healthy, stuck in a retry loop or dead. Print a heartbeat with current counts at a fixed interval, and treat a missing one as a failure.
7. **Check progress by counting outputs, not by status.** A container listed as "Up" can be reading an empty directory. Look inside the job's own view of the filesystem and count files, rows and modification times. Better still, give the job a status tool that reads those counts and exits non-zero when they stall.
8. **Stop it cleanly and read the exit codes.** A stop command printing "Stopped" means the process is no longer running, not that it shut down cleanly. Exit code 0 or 143 is clean; 137 is a kill. If a comment says the job flushes on shutdown, search the code for the signal handler before believing it. Publish outputs atomically, so a kill leaves no half-written files.
9. **Verify the result by what it contains.** Compare output counts with the expected numbers or the previous run, and treat any drop as a failure until it is explained. A tool's own "verified" usually checks the integrity of what it stored, not whether it stored the right things. End wrapper scripts with an explicit success exit when they call native tools that use non-zero codes for success.

## Verification checklist

- [ ] The job runs under a stable name, and its logs are readable after the launching session has ended.
- [ ] The log shows periodic progress lines and heartbeats at the expected interval, with no unexplained gaps.
- [ ] Output counts were taken inside the job's own filesystem view and match the expected numbers or the previous run.
- [ ] No data lives only inside the container. Removing the container and its volumes would delete nothing irreplaceable.
- [ ] CPU and memory limits are set.
- [ ] After any stop, the exit codes are recorded: 0 or 143 clean, 137 investigated.
- [ ] The final result is compared against a previous run or baseline, and any drop is explained.

## Failure modes

- A background shell is killed when the machine runs low on memory, and the loss is found later from missing output.
- The logs die with the session, so nobody can check what happened.
- An empty log is read as a healthy one.
- "Up" is read as working while the job reads an empty directory, because a wrong bind path was silently created as an empty folder.
- Buffered output or a redrawing bar makes the log useless.
- A shutdown prints "Stopped" while every process was killed mid-write.
- A wrapper script exits 1 after a successful run, which teaches everyone to ignore exit codes.
- The job's own tool says "verified" while it silently skipped part of the input.
- The container owns the data, and a teardown deletes it.
- The image lacks a tool the host has, and a supervisor crashloops trying to spawn it.

## Human gate

Ask before killing or restarting a job you did not start, retrying expensive work, deleting volumes or outputs, putting heavy compute on a machine that runs always-on services, or changing external state.

## Field notes

- The studio's rule since July 2026 is that anything over three to five minutes runs as a named container with a persistent log, so a run can be checked days later. In late September and early October 2026 two jobs that ran as background shells anyway, a test gate and a document build, were killed by the agent harness's memory-pressure reaper on a busy workstation. Both losses were found later, from their output. That became a second reason for the rule: a container sits outside the harness's process tree.
- A collector fleet ran with exactly zero bytes of logs. It was fine, but a reconnect storm, a rate-limit backoff and a feed going silent at 3 a.m. would all have produced the same empty log. Health could only be established by counting files on disk. The lesson recorded: emit a heartbeat whose absence is the alarm, and give the fleet a status tool that reads file counts and modification times and exits non-zero.
- A stop command printed "Stopped" for every container in a collector fleet. The exit codes said 137, a kill. The compose file's comment promised a flush on shutdown, but a search of the code found no handler: it was never written. Atomic publishing held, though: the kills left zero partial files.
- A backup reported "snapshot verified" and "no errors" after a new exclude pattern had silently dropped a whole project. It was caught only because the snapshot's file count was compared with the previous one: 89,290 down to 80,249.
- After a data folder moved behind a filesystem link, containers stayed "Up" while reading an empty directory. A restart of the container runtime exposed it, not a code change. The fix was to mount that folder directly. What told the two states apart was a file listing inside the container: nothing through the parent mount, 34 entries through the direct one. More evidence that lied: [When the verification evidence itself was wrong](../examples/field-story-verification-evidence-lied.md).

## Related workflows

- [Context Compaction and Handoff](36-context-compaction-handoff.md)
- [Local AI Stack Setup](09-local-ai-stack.md)
- [Incident Command Center](23-incident-command-center.md)
- [CI Red-to-Green Reproducer](19-ci-red-to-green.md)
