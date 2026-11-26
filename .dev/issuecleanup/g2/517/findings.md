# Issue 517 review

Template: coordinator brief required fields; section skeleton adopted from `.dev/issuecleanup/g2/468/report-template.md`.

## Verdict and evidence
**Verdict: still-relevant.** Review date: 2026-11-24. Issue [#517](https://github.com/IronbellyOrg/IronClaude/issues/517) is OPEN with no assignee; the November 17 comment still accurately describes the repository defect. Checked worktree HEAD and its existing local origin/master: `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`.

- The exact reported thinking/medium-effort 400 matches none of `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:396-433`. Requests keep their effort when forwarded (`:839-847`), and that error reaches the unchanged-error return (`:933-962`), not the next model.
- PR [#516](https://github.com/IronbellyOrg/IronClaude/pull/516), merged as `b0977b4f2b7ad2ca19d0048b0774da6fbbac8580`, only sets one worker's low effort. PR [#518](https://github.com/IronbellyOrg/IronClaude/pull/518), merged as `167184c6ba449ab49b7f2af1dc9f4c9080006bd3`, moves that worker to Tier 2b. Neither repairs the proxy.
- Latest proxy change PR [#738](https://github.com/IronbellyOrg/IronClaude/pull/738), commit `720cbaf96653c1c983497ba480f76ca6e60e5369`, handles only the image-specific 400 (`:419-422`, `:956-961`), not effort rejection.
- Live issue timeline has nine events: bug label/type, project/field/status metadata, two comments and references from #523 and #488. It has no closing event, commit reference or linked-PR event. Current open ccsession PR search returned none; effort/proxy PR search returned only #516. Unpushed work is UNVERIFIED, so the issue is not classified in-progress.
## Real current state
The shared tier/named-model routing exists and is implemented: both routes converge in `_forward_tier` (`src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:698-706`). Usage and server-error failover exist, as do oversized-backup and text-only-image exceptions. Effort-specific recovery is NOT BUILT in this source.

Tier 3 still has two configured environment slots (`src/superclaude/skills/ccsession-tag/ccsession-models.json:113-118`); the documented order is GLM-5.3 then Qwen3.8 Max (`src/superclaude/skills/ccsession-tag/MODEL-TIERS.md:45`). Actual live slot values and whether the provider still rejects medium are UNVERIFIED. The workaround remains in `src/superclaude/agents/issue-worker-t3.md:6-12`: Tier 2b, low effort.

A plain SWITCH_RULES addition would be wrong: all matching reasons call `cool_down` (`local-gateway-alias-proxy.py:914-927`), which stores a model-keyed cooldown (`:471-475`) and defaults to 3,600 seconds (`:123`). This contradicts the issue's explicit requirement that a later high-effort request still use that same model. The November 12 traffic percentages and park replay are historical issue-comment claims, not newly measured results.

The real-proxy scripted test fixture already exists (`tests/unit/test_ccsession_tiers.py:847-907`). Tests cover unrelated 400 pass-through (`:1039-1060`), backup size (`:1075-1087`), and image rejection without parking (`:1104-1149`), but the effort-recovery case was not found by the bounded ccsession test search.
## Concrete next steps
1. Keep #517 open. Recommended smallest complete fix: a narrowly matched effort-incompatibility 400 advances this request to the next eligible model without cooldown/failure counting; reuse the current routing loop and no-parking pattern from #738. Handle all-incompatible/no-backup outcomes without misreporting quota exhaustion. This is a recommendation, not an approved implementation decision; retry-with-low is the issue's alternative if the owner prefers preserving the model at a changed effort.
2. Add regressions using the existing scripted fixture: adaptive thinking plus medium effort reaches a successful backup; the original model serves a following high-effort request; unrelated first-model 400s pass through; oversized-backup behavior and usage/server cooldown are preserved. Include streamed/non-streamed, allowed named-model routing, exhausted/incompatible backups and no compatible fallback.
3. Run the focused tier/proxy tests before considering closure, then verify with an isolated proxy against a live gateway if authorized. This review ran no runtime tests and authorizes no live calls.
4. Do not alter tier membership, the one-worker workaround, provider config or caller default effort for this repository fix. No capability cache or general provider-rewrite framework is required.
## Complexity and size
**Complexity: medium. Size: S.** The change is concentrated in one existing shared route plus its existing test module, but must preserve cooldown semantics and distinguish request incompatibility from model failure across streaming, named requests and exhausted fallbacks.
## Priority
**Priority: P2.** This breaks default-medium requests when an incompatible model is reached despite an available fallback, affecting shared routing rather than one worker; explicit low/high effort and an existing worker workaround reduce urgency, there is no demonstrated data loss, and present-day live frequency is UNVERIFIED.
## Dependencies
- **Needs:** no open issue dependency established. Server-error foundation #392 is already delivered by #481; tier-layout issue #488 is closed. #737 is closed and #738 supplies a reusable no-parking precedent, not an unresolved prerequisite.
- **Blocks:** no formal downstream issue blocker verified. #523 references this as shared failover behavior, but adding its model is not shown to require effort recovery first. A provider-side compatibility repair is an alternative outside this repository, not a verified dependency.
## Related issues
- [#488](https://github.com/IronbellyOrg/IronClaude/issues/488), closed: tier restructuring; mentioned in the issue's review comment and a timeline source.
- [#523](https://github.com/IronbellyOrg/IronClaude/issues/523), open: adding Muse Ember to Tier 4; timeline source mentions #517 as related failover behavior, not a formal block.
- [#737](https://github.com/IronbellyOrg/IronClaude/issues/737), closed: text-only image rejection fails to advance to the next model; adjacent request-incompatibility case fixed by #738.
- [#392](https://github.com/IronbellyOrg/IronClaude/issues/392): server-error/named-model failover foundation, identified by merged #481's closing reference. Its issue body was not independently read in this run; issue details beyond that PR reference are UNVERIFIED.
## Related PRs
| PR | Verified state | Relevance |
|---|---|---|
| [#516](https://github.com/IronbellyOrg/IronClaude/pull/516) | MERGED 2026-11-12, `b0977b4f2b7ad2ca19d0048b0774da6fbbac8580` | One-worker low-effort workaround; explicitly leaves the shared proxy defect open. |
| [#518](https://github.com/IronbellyOrg/IronClaude/pull/518) | MERGED 2026-11-12, `167184c6ba449ab49b7f2af1dc9f4c9080006bd3` | Pins that worker to Tier 2b while retaining low effort; does not edit the proxy. |
| [#481](https://github.com/IronbellyOrg/IronClaude/pull/481) | MERGED 2026-11-10, `12d6bb497f8733caa0083f2892529c6575e970a6` | Shared server-error and named-model failover/cooldown foundation. |
| [#738](https://github.com/IronbellyOrg/IronClaude/pull/738) | MERGED 2026-11-23, `720cbaf96653c1c983497ba480f76ca6e60e5369` | Adjacent image-specific request rejection, no-parking fallback and focused tests; does not match effort errors. |
## Verification limits and negative evidence
- Sources: current issue body and both comments; all nine timeline events summarized with source issue numbers; bodies, changed-file lists and merge identities of #516/#518/#481/#738; current source and associated test excerpts; proxy git history. No source files changed.
- Analysis output: `.dev/issuecleanup/g2/517/analyze/analyze-report.md`; command contract: `.dev/issuecleanup/g2/517/analyze/return-contract.yaml`; handoff: `.dev/issuecleanup/g2/517/analyze/handoff/1-analyze.md`.
- Negative checks: proxy search for `effort` found only a best-effort comment; ccsession test search for `effort` or `always engages in thinking` found only launcher settings-preservation checks. Effort/proxy PR search returned only #516; open ccsession PR search returned none. The initial loose PR search for `517` returned unrelated #378/#622 and was not treated as evidence of a fix.
- UNVERIFIED: live gateway behavior today, current workspace environment slot values, deployed proxy version, present-day occurrence rate, actual Retry-After headers on the historical 400s, model-quality comparisons, unpushed branches, and whether remote master advanced after the existing local origin/master reference. No fetch, tests, builds or live model calls were run.
- Process deviations: the timeline was read using one read-only `gh api` GET despite the brief's issue/pr view/list-only restriction; no mutation was performed and no further API calls followed. Early worker-contract/analyze reads exceeded the later-applied 80-line chunk limit. Initial report edits were freshness-blocked, then retried only after Reading the stubs. The graph's incomplete/ambiguous callee rows were excluded or marked degraded in the analysis. These limits are disclosed rather than hidden.
- No staging, commits, pushes, issue/PR edits, comments, labels, closes, links, installations or worktree operations were performed. The coordinator owns all follow-up actions.
