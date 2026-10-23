---
name: repo-growth-launch
description: "Use when a public repository needs useful packaging and launch readiness. Launch a public repo honestly: content that survives a click-through, one rule-following submission per venue, fast replies to contributors, and every public action by the maintainer."
---

# Repo Growth Launch

Status: field-tested. Generated from the workflow card at https://github.com/Richicinschi/awesome-agent-workflows/blob/main/workflows/10-repo-growth-launch.md; edit the card, not this file.

## Goal

Content that holds up when a visitor clicks through, one tailored submission per venue that follows that venue's rules, a contribution path that gets fast replies, and every public action taken by the human maintainer. No fake engagement of any kind. The plan and copy for this repo live in the [Ethical Growth Plan](https://github.com/Richicinschi/awesome-agent-workflows/blob/main/docs/launch/GROWTH-PLAN.md) and the [Posting Checklist](https://github.com/Richicinschi/awesome-agent-workflows/blob/main/docs/launch/POSTING-CHECKLIST.md).

## Agent brief

```text
You are preparing a public repository for launch. You prepare; the maintainer posts.

Repo: [URL]
One-line pitch: [what it does, for whom]
Strongest single page: [path]
Venues under consideration: [curated lists, forums, communities]
Traffic baseline: [stars, views and clones over the last 14 days]

Do:
- Audit content depth first: compare file bodies for repeated or templated text and
  report how many files share identical sections.
- For each venue, read its CONTRIBUTING file or posting rules and record: entry format,
  disclosure wording, minimum repo age, stars or account karma, required flair, and who
  may submit (some accept only a human using a web form). Say whether the repo qualifies today.
- Draft one submission per qualifying venue, written for that venue.
- Draft release notes that thank each contributor by handle.
- List open "good first issue" items and every issue or PR waiting more than [N] days.

Do not:
- Post, comment, open PRs on other repositories, or submit any form.
- Write as the maintainer or use the maintainer's accounts.
- Propose bought stars, star exchanges, paid engagement or the same copy in many places.

Output:
- Content audit with counts
- Venue table: rule link, qualifies yes/no, draft
- Contributor queue with the age of the oldest unanswered item
- The maintainer's manual steps, in order
```

## Steps

1. **Measure before deciding what to fix.** Record stars, views and clones for the last 14 days. Zero views means nobody arrives, which is a distribution problem. More polish will not change it.
2. **Audit content depth before any promotion.** People who find you on a curated list click through to a page. Compare bodies across files and count the templated ones. Fix or remove them before anything is posted.
3. **Lead with the strongest single page.** Pick one page a visitor can use in five minutes. That page, not the index, is what you link from venues that want one concrete thing.
4. **Read every venue's rules and write them down.** Rules differ a lot. Some lists take a PR with a one-line entry and a disclosure such as "I maintain it". Some take recommendations only from a human through their web issue form, never from a CLI or an agent, and restrict accounts that ignore this. Some require a minimum repo age or star count. Show HN on Hacker News is for things people can try and excludes reading material and lists, so a docs repo goes in as a normal link to its strongest page. Some subreddits require minimum account karma and a specific flair.
5. **Write one tailored submission per venue.** Use the venue's format and disclosure. Include the repo link once and ask a specific question. Never mass-post the same text.
6. **Make the contribution path real and answer fast.** Label small, concrete issues "good first issue"; that is where outside contributors start. Reply within days, not months. Slow review is a cost paid by the people who showed up.
7. **Hold inbound links to your own curation policy.** A link to a storefront with no operational content gets declined, politely, with a constructive alternative such as contributing a worked example. Cite the [curation policy](https://github.com/Richicinschi/awesome-agent-workflows/blob/main/docs/curation-policy.md) and do not name or shame anyone.
8. **Thank contributors by handle in the release notes.** A mention by handle notifies each contributor.
9. **Hand every public action to the human, one venue at a time.** The agent prepares drafts and checklists. The maintainer posts, submits forms, opens list PRs and replies. Posting in one place at a time keeps replies answerable.
10. **Log what happens and watch the stop conditions.** For each post, record venue, link, whether it stayed up, replies and issues opened. Slow down if posts are removed, replies show the pitch is unclear, or replies cannot be handled promptly.

## Verification checklist

- [ ] A 14-day traffic baseline is recorded before the first post.
- [ ] The content audit ran and the count of templated files is zero, or those files are kept out of what is promoted.
- [ ] A venue table exists, with a link to each venue's rules and a qualifies yes/no.
- [ ] Each submission is unique to its venue and carries the disclosure that venue asks for.
- [ ] No post, comment, list PR or form submission was made by an agent.
- [ ] Open "good first issue" items exist, and no contributor issue or PR has waited more than a few days.
- [ ] The release notes name every contributor by handle.
- [ ] The launch log has a row for every post, including removals.

## Failure modes

- **Polishing a repo nobody visits.** The launch plan and post copy get written and never posted.
- **Promoting templated content.** A visitor from a curated list opens a page, sees the same body as the last one, and leaves.
- **Mass-posting one link.** The same resource sent to many lists reads as spam and gets declined.
- **An agent submitting where only humans may.** It breaks the venue's rules and can get the maintainer restricted.
- **Submitting before qualifying.** A post that fails a minimum-age, star or karma rule gets removed, and the first impression is spent.
- **Show HN for reading material.** Wrong section, so the post is out of place from the start.
- **Contributors left waiting.** People arrive through good first issues and then wait months for review.
- **Stars as the goal.** Bought stars and star-for-star rings are out, and so is any result claimed before it was measured.

## Human gate

Every public action belongs to the maintainer: posts, comments, PRs to curated lists, web form submissions and replies. Agents draft and never write as the maintainer. No bought stars, star exchanges, paid engagement, spam or deceptive automation.
