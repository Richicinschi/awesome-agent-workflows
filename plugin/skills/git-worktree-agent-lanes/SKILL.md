---
name: git-worktree-agent-lanes
description: "Use when multiple agents or humans need to work in the same repo concurrently. Use worktrees and branch naming to isolate lanes and avoid stomping shared state."
---

# Git Worktree Agent Lanes

Status: field-tested. Generated from the workflow card at https://github.com/Richicinschi/awesome-agent-workflows/blob/main/workflows/35-git-worktree-agent-lanes.md; edit the card, not this file.

## Goal

Each lane works in its own worktree, on its own branch, cut from a freshly fetched remote main. No agent moves HEAD, the index or the working files under another. Lanes reach main only through branches a human merges, and nothing another session owns is stashed, cleaned or committed.

## Agent brief

```text
Other agents may be live in [shared checkout path]. Treat that checkout as read-only:
no checkout, switch, stash, clean, reset, commit, or "git add -A" there.

Set up your lane:
1. git -C [shared checkout path] fetch origin
2. git -C [shared checkout path] worktree add [absolute lane path] -b [lane branch] origin/main
3. Copy in the untracked inputs the work needs: [env file, local config]. Never commit them.

Work only inside [absolute lane path]. Use absolute paths or "git -C [absolute lane path]"
in every command. The shell's working directory can reset between commands.

Before every commit:
- "git -C [absolute lane path] branch --show-current" must print [lane branch]
- "git -C [absolute lane path] diff --cached --name-only" must list only your files

Verify in the lane with: [command]. The shared checkout keeps running the old code
until your branch is merged; say so in your report.

Push the lane branch. Do not merge, force-push, or delete any branch or worktree
you did not create.

Report: lane path, branch, commit hashes, files changed, verification command and
exit code, pushed yes or no.
```

## Steps

1. **Assume someone else is live.** Before any git write in a shared checkout, ask whether another agent could be working there. If yes or unsure, treat it as read-only. Signals: modified files you did not touch, very recent commits, and entries in `git worktree list`.
2. **Cut from the fetched remote, not the local tree.** A shared checkout drifts behind its remote and fills up with other sessions' edits. Run `git fetch`, compare, then `git worktree add [lane path] -b [lane branch] origin/main`.
3. **One lane, one branch, one owner.** Name branches by lane and never take over a branch another worktree has checked out. Put the lane where your toolchain expects it; in the studio a mobile build failed when the worktree sat on a different drive from the package cache.
4. **Bring ignored inputs on purpose.** A new worktree has no untracked or ignored files. Copy the env file and local config in; link large ignored data instead of duplicating it. If a file kept live in the shared checkout is the current truth for every session, copy that live version into the lane at commit time instead of committing the lane's stale copy.
5. **Address the lane by absolute path.** Prefix every command with `git -C [lane path]` or `cd [lane path] &&`, on every line, and check the branch before committing.
6. **Stage only your files.** No `git add -A` or `git add .`. Read `git diff --cached --name-only` before each commit.
7. **Verify where the code will run.** A pass in the lane proves the lane. After merge, run the check again on the checkout that actually executes the code.
8. **Hand off, do not finalize.** Push the branch and hand it to the human for merge. Unpushed commits are the one state that cannot be recovered, so push before the session ends.
9. **Remove only your own lane.** After merge, `git worktree remove [lane path]`, `git worktree prune`, and delete your branch. Leave every other worktree, stash and branch alone, even if it looks abandoned.
10. **Recover a misplaced commit by cherry-pick.** If a commit lands on the wrong branch, cherry-pick its hash into a clean lane. Moving the polluted branch back (`git branch -f [branch] [good hash]` while it is not checked out) changes another lane's state, so get the human's agreement first.

## Verification checklist

- [ ] `git worktree list` shows the lane at the expected path on the expected branch.
- [ ] The lane branch started from `origin/main` right after a fetch.
- [ ] HEAD and `git status` of the shared checkout are the same before and after the work.
- [ ] Every lane commit contains only lane files; no env file or secret is tracked.
- [ ] The branch is pushed, so no commit exists only locally.
- [ ] After merge, the change was re-verified on the checkout that actually runs it.
- [ ] Only worktrees and branches this lane created were removed.

## Failure modes

- **Committing in the shared tree.** While one session worked in a shared checkout, another switched HEAD to its own branch. The first session's hotfix commit landed on the other session's branch, and its push went to a wrong, empty branch.
- **A stale or dirty base.** Branching from the local checkout carries other sessions' edits, or misses commits that are already on the remote.
- **Verified in the lane, not live.** A fix passed in a worktree while the real checkout kept running the old version, twice in one day.
- **Working directory reset.** Bare git and package commands ran against the parent repo: a feature branch was created there twice by accident, a push went to the wrong remote, and an install ran in a folder with no package file.
- **`git add -A` in a shared checkout.** It sweeps in other sessions' in-flight edits. One status check in the studio showed five files modified by other live sessions, mixed with the current session's own.
- **Cleaning up someone else's lane.** Stashing, resetting or removing a worktree that another live session still uses destroys its work.
- **Missing ignored inputs.** Tests fail or skip in the lane because the env file or local data was never copied in, and the result gets read as a real failure or a clean pass.

## Human gate

Merging, force-pushing, deleting branches or worktrees the agent did not create, and touching any other session's uncommitted changes need an explicit human decision. Ask before deleting worktrees, stashing unknown changes, or force-pushing.
