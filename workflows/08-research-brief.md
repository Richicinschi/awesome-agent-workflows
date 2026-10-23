# Research Brief

> **Status: field-tested.** Distilled from a one-person studio's multi-agent research sweeps, data-collection work and pre-registered studies (2026).

## Trigger

A decision depends on current facts, prior art, competitors, prices, versions or data availability, or someone asks "what is out there?" before building.

## Goal

A brief where every finding has a source that was actually read, a stated mechanism and a confidence label. The search filter and its blind spots are named, the expectation was written down before looking, a skeptic attacked the result from a fresh context, and the recommendation is kept apart from the findings.

## Agent brief

```text
You are writing a research brief. Findings first, recommendation last and separate.

Decision this informs: [decision]
Real constraints: [budget, licence, platform, deadline]
Real material to read: [repo, files or data the answer must fit]
Expectation written before looking: [number or claim], because [mechanism]
Lane 1 filter: [where you search and what you keep]
Lane 2: search what the lane 1 filter makes invisible: [for example demos, essays, people, older work]
Stock answers that count as cliche: [list]
Forbidden: [paid sources without approval, logins, routes around a refusal]

Rules:
- Read the real source. A search snippet or your own memory is not a source.
- Every finding states its mechanism, precisely enough to rebuild from the sentence alone.
- Label each claim: verified (source read), single-source, or inferred.
- Record contradictions between sources instead of silently picking one.
- If a site's robots.txt or licence names your agent class or reserves AI use, do not reach
  its pages by another road (archives, caches, crawl dumps). Look for an independent
  publication of the same facts, or report the gap.
- "No free source exists" needs the list of what you probed.

Output:
- Findings table: claim, mechanism, source URL, confidence
- What the filter could not see
- Contradictions and unknowns
- Sources you could not reach, and why
- Recommendation
```

## Steps

1. **Write the expectation before the first search.** Two lines: the number or claim you expect, and the mechanism you think produces it. The mechanism is a second prediction. Test it separately, or you will report the reason as confirmed when only the number was.
2. **State the filter, then ask what it hides.** A filter that is easy to verify (stars, licence, last push) is not neutral. It selects one class of result and silently deletes everything without a repository or release cadence. Run a second lane against that blind spot, with a quota or an explicit ban if needed.
3. **Hand researchers the real constraints and the real repo.** Abstract questions get generic answers. An agent reading your actual code while researching something else may find more than the commissioned search.
4. **Fan out by angle, and read the sources.** Split the question into a few search angles and run them in parallel, a handful at a time. Each lane fetches and reads pages instead of summarising snippets.
5. **Demand a mechanism, not an impression.** "It looks impressive" is not a finding. Researchers routinely restate marketing copy as if it were a mechanism. Name the cliches up front so fashion does not come back labelled as fresh.
6. **Respect refusals and exhaust the free routes.** A rule that names your agent class is a refusal: no workaround, no archive copy. An AI-use reservation binds the use, not the route, and a reservation in a work's licence follows it to mirrors. A blanket rule or a firewall is different: test before assuming. Before paying, try the upstream source, mirrors, bulk files, deriving the number yourself, or collecting snapshots over time.
7. **Run the skeptic from a fresh context, on raw material.** Give it the sources and data, not the conclusions. Ask for the ways the brief breaks, the single assumption that sinks it, and a number: "how many findings would genuinely surprise the reader?" Tell it not to manufacture a reversal to look useful.
8. **Check every comparison for hindsight.** For each control or baseline, ask: could someone standing at that moment have picked it? A sample drawn from a period that is only defined once it ends knows the future. Label groups whose membership is settled by later events, and label any cut made after looking as exploratory.
9. **Treat the write-up as claims.** Go sentence by sentence and point each one at a source, a table row or a command. Do this for sentences written while correcting, too. Strike fabrications by name rather than softening them.
10. **Record dead ends where the next run will read them.** A "no lawful route" or "source unreachable" note, with what was probed, stops the next sweep from repeating the same dead end.

## Verification checklist

- [ ] The expectation, as a number plus a mechanism, is dated before the first result.
- [ ] The search filter is stated, and a second lane covered what it hides.
- [ ] Every finding has a source that was read, a mechanism and a confidence label.
- [ ] The skeptic ran in a fresh context on raw material; its verdict and its number are in the brief.
- [ ] Fabrications found are listed by name.
- [ ] Every sentence in the summary traces to a source, a row or a command.
- [ ] No control or baseline could see the outcome it is compared against.
- [ ] Refused or unreachable sources are listed with what was tried; none was routed around.
- [ ] The recommendation sits in its own section and cites the findings it rests on.

## Failure modes

- **A verification-friendly filter.** Searching only what an API can sort produces a competent list that surprises no one.
- **Marketing copy dressed as a mechanism.** The finding repeats a product page and explains nothing.
- **Fabrication at scale.** Wrong creators, constructed URLs, and mechanisms invented after a researcher wrongly declared a source unreachable.
- **A skeptic bolted on at the end,** or handed the conclusions instead of the raw files.
- **A critic that invents a reversal** to justify its own existence.
- **The number came out, so the reason gets written in too,** although nobody tested the reason.
- **A decision rule with a clause that cannot fail,** so the verdict rests on the other clause alone.
- **A control that knows the future,** which turns hindsight into an apparent effect.
- **The correction pass adds a new false sentence,** because only the original text was checked.
- **"The docs say you need a key" accepted as "there is no free way".**
- **A refusal routed around** through an archive, a cache or someone's dump of the same pages.

## Human gate

The human approves any spend, any source with an unclear licence or AI-use reservation, and whether the recommendation is acted on. Current facts are never answered from memory.

## Field notes

- Two 18-agent sweeps went looking for ideas for a studio website. Sweep 1 filtered GitHub by stars, licence and last push and returned a competent list that did not impress the owner: one candidate in ninety predated 2020. Its own critic named the cause: star counts select for libraries, while the interesting ideas live in one-off demonstrations. Sweep 2 searched demos, essays, people and craft traditions, required a third of finds to predate 2022 and required a mechanism field. It found what sweep 1 could not reach.
- Across about 185 candidates, the commissioned product, a list of things to adopt, was worth close to nothing. The side effect was worth more: agents reading the real codebase while researching found five real defects and shipped a 39.7% payload cut. In about six cases the skeptic found a better source than the researchers did. Expect around 5% fabrication in a large sweep.
- In a data study, a pre-registered control was sampled from inside episodes that are only defined once they end. It sat near the outcome by construction, and the registered verdict was pure hindsight. A control that could not see the episode's end showed no measurable effect.
- Two findings-document reviews behind steps 7 and 9, one wrong number with five overstated claims and four problems only an independent reviewer found, are told in [Fresh-Context Code Review](04-fresh-context-code-review.md).
- Several sites disallowed the studio's agent class by name. They were treated as refusals: facts came from independent publications where these existed, and one data cell stayed unbuilt. Separately, an agent wrote a collector for a site with an AI-use reservation whose own comment acknowledged the signal, then used a web archive anyway. It was rejected and rebuilt.

## Related workflows

- [Spec → Plan → Implementation](01-spec-to-plan.md)
- [Fresh-Context Code Review](04-fresh-context-code-review.md)
- [Agent-Written Docs Review](39-agent-written-docs-review.md)
- [ADR Decision Capture from Threads](27-adr-decision-capture.md)
- [Workflow Evaluation Harness](30-workflow-evaluation-harness.md)
