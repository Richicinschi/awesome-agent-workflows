# Git Worktree Agent Lanes

> **Status: field-tested.** Distilled from running up to ten coding-agent sessions at once around one shared workspace repository in a one-person studio (2026).

## Trigger

An agent needs to change a repository that another agent or a human may be using at the same moment: a shared workspace or hub repo, shared docs, or one project split between several implementers. Use it whenever you cannot rule out that another session is live in the same checkout.

## Goal

Each lane works in its own worktree, on its own branch, cut from a freshly fetched remote main. No agent moves HEAD, the index or the working files under another. Lanes reach main only through branches a human merges, and nothing another session owns is stashed, cleaned or committed.

## Agent brief

```text
Other agents may be live in [shared checkout path]. Treat that checkout as read-only:
no checkout, switch, stash, clean, reset, commit, or "git add -A" there.

Set up your lane:
1. git -C [shared checkout path] fetch origin
2. git -C [shared checkout path] worktree add --no-track -b [lane branch] [absolute lane path] origin/main
   (--no-track: the lane must not track main, or a bare push or pull would hit main.)
3. Copy in the untracked inputs the work needs: [env file, local config]. Never commit them.

Work only inside [absolute lane path]. Use absolute paths or "git -C [absolute lane path]"
in every command. The shell's working directory can reset between commands.

Before every commit:
- "git -C [absolute lane path] branch --show-current" must print [lane branch]
- "git -C [absolute lane path] diff --cached --name-only" must list only your files

Verify in the lane with: [command]. The shared checkout keeps running the old code
until your branch is merged; say so in your report.

Push only with: git -C [absolute lane path] push -u origin [lane branch]
Do not merge, force-push, or delete any branch or worktree you did not create.

Report: lane path, branch, commit hashes, files changed, verification command and
exit code, pushed yes or no.
```

## Steps

1. **Assume someone else is live.** Before any git write in a shared checkout, ask whether another agent could be working there. If yes or unsure, treat it as read-only. Signals: modified files you did not touch, very recent commits, and entries in `git worktree list`.
2. **Cut from the fetched remote, not the local tree.** A shared checkout drifts behind its remote and fills up with other sessions' edits. Run `git fetch`, compare, then `git worktree add --no-track -b [lane branch] [lane path] origin/main`. Without `--no-track` the lane branch tracks `origin/main`, so a bare `git push` or `git pull` from the lane would hit main.
3. **One lane, one branch, one owner.** Name branches by lane and never take over a branch another worktree has checked out. Put the lane where your toolchain expects it; in the studio a mobile build failed when the worktree sat on a different drive from the package cache.
4. **Bring ignored inputs on purpose.** A new worktree has no untracked or ignored files. Copy the env file and local config in; link large ignored data instead of duplicating it. If a file kept live in the shared checkout is the current truth for every session, copy that live version into the lane at commit time instead of committing the lane's stale copy.
5. **Address the lane by absolute path.** Prefix every command with `git -C [lane path]` or `cd [lane path] &&`, on every line, and check the branch before committing.
6. **Stage only your files.** No `git add -A` or `git add .`. Read `git diff --cached --name-only` before each commit.
7. **Verify where the code will run.** A pass in the lane proves the lane. After merge, run the check again on the checkout that actually executes the code.
8. **Hand off, do not finalize.** Push explicitly with `git -C [lane path] push -u origin [lane branch]`, never a bare `git push`, and hand the branch to the human for merge. Unpushed commits are the one state that cannot be recovered, so push before the session ends.
9. **Remove only your own lane.** After merge, `git worktree remove [lane path]`, `git worktree prune`, and delete your branch. Leave every other worktree, stash and branch alone, even if it looks abandoned.
10. **Recover a misplaced commit by cherry-pick.** If a commit lands on the wrong branch, cherry-pick its hash into a clean lane. Moving the polluted branch back (`git branch -f [branch] [good hash]` while it is not checked out) changes another lane's state, so get the human's agreement first.

## Verification checklist

- [ ] `git worktree list` shows the lane at the expected path on the expected branch.
- [ ] The lane branch started from `origin/main` right after a fetch, and its upstream is its own remote branch, never `origin/main`.
- [ ] HEAD and `git status` of the shared checkout are the same before and after the work.
- [ ] Every lane commit contains only lane files; no env file or secret is tracked.
- [ ] The branch is pushed, so no commit exists only locally.
- [ ] After merge, the change was re-verified on the checkout that actually runs it.
- [ ] Only worktrees and branches this lane created were removed.

## Failure modes

- **Committing in the shared tree.** While one session worked in a shared checkout, another switched HEAD to its own branch. The first session's hotfix commit landed on the other session's branch, and its push went to a wrong, empty branch.
- **A stale or dirty base.** Branching from the local checkout carries other sessions' edits, or misses commits that are already on the remote.
- **Verified in the lane, not live.** A fix passed in a worktree while the real checkout kept running the old version, twice in one day.
- **Working directory reset.** Bare git and npm commands ran in the wrong folder: a feature branch was created in the parent repo twice by accident, a push was attempted against the parent repo's remote and failed, and an npm command ran in a folder with no package file.
- **`git add -A` in a shared checkout.** It sweeps in other sessions' in-flight edits. One status check in the studio showed five files modified by other live sessions, mixed with the current session's own.
- **Cleaning up someone else's lane.** Stashing, resetting or removing a worktree that another live session still uses destroys its work.
- **Missing ignored inputs.** Tests fail or skip in the lane because the env file or local data was never copied in, and the result gets read as a real failure or a clean pass.

## Human gate

Merging, force-pushing, deleting branches or worktrees the agent did not create, and touching any other session's uncommitted changes need an explicit human decision. Ask before deleting worktrees, stashing unknown changes, or force-pushing.

## Field notes

- Sessions in the studio stopped conflicting on main once every project got its own repository, because agents on different projects physically could not entangle. The workspace hub repo stayed the one shared surface, and the rule for it became: every change goes through a worktree off `origin/main`, on its own branch, for the human to merge.
- In October 2026 the shared hub checkout was 166 commits behind its remote, with 42 tracked files modified and 11 agent-memory files untracked, all owned by sessions that had worked there over the previous ten days. Fetch and compare before trusting anything a shared checkout shows.
- For the commit that landed on another session's branch, the recovery recorded afterwards: cherry-pick it into a clean worktree, then move the polluted branch back. The lasting fix was one agent per working directory.
- A guardrail fix was verified working in a worktree while the real checkout kept running the old version, twice, because the fix was not merged yet: item 7 in [when the verification evidence itself was wrong](../examples/field-story-verification-evidence-lied.md), and the guardrail itself in [one guardrail, ten agents](../examples/field-story-one-guardrail-ten-agents.md).

## Related workflows

- [Parallel Agent Development](02-parallel-agent-development.md)
- [Agent Task Contract and Scope Box](12-agent-task-contract.md)
- [Multi-Repo Change Coordinator](34-multi-repo-change-coordinator.md)
