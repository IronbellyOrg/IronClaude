# Issue 429: release testing and sign-off review

Structure: coordinator brief fields, following the task-local findings template in .dev/issuecleanup/g1/362/report-template.md.

## Verdict and evidence
**Verdict: still-relevant.** Keep issue [#429](https://github.com/IronbellyOrg/IronClaude/issues/429) open. Existing post-release install proof and manual guides partly support its goal, but the inspected source does not implement its reusable, agent-first real-world and abuse-testing gate with standardized scoring before final sign-off. No issue-specific implementation PR was found; supporting pieces that predate the issue are not proof that #429 is in progress.

Evidence at checkout `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`:
- `src/superclaude/commands/post-release.md:15-36`: existing-tag input and only an output-directory option; no scored pre-release mode.
- `src/superclaude/skills/sc-post-release-protocol/SKILL.md:187-199`: real installation runs, but functional guides are documents for humans, not automated functional tests.
- `src/superclaude/skills/sc-post-release-protocol/SKILL.md:287-306`: reporting contract records coverage and install results, not a standardized release score or minimum sign-off threshold; a RED install is an honest reportable outcome.
- `docs/developer-guide/release-procedure.md:64-78`: a real manual go/no-go gate already exists, including full tests, upgrade checks and owner-defined release-specific checks. It is not the scored, reusable agent-run gate requested here.
- Foundational PR #218 merged 2026-07-06 (`0d3b99c84fbfc3efa4757343ebd9d4cf37228ab1`), before #429 was created on 2026-11-07. Newer PR #649 (`bc3d796aa89c33d1f9e4766ea9fd18417ab0a61e`) adds release evidence, not the missing gate; PR #667 is another merged evidence/documentation pass, not the requested implementation.

## Real current state
- **Exists:** tag-anchored post-release scanning, agent scanner/consolidator/writer roles, clean install validation, human test-guide templates, coverage matrices, transcripts and incremental manifests (`SKILL.md:91-105,161-199,218-223`). The manual release procedure also requires tests, builds, upgrade checks and release-specific checks before tagging.
- **Recorded real execution:** 6.0.0 install/upgrade results are retained and end `RESULT: GREEN` (`docs/testing/v6.0.0/c-e2e-transcript.txt:2199-2202`). Its report explicitly skipped new user/operator guides and says those areas were not re-scanned (`docs/testing/v6.0.0/post-release-report.md:129-135`). This audit did not rerun those installations.
- **Not found in the inspected implementation:** a general agent-first functional test executor, an explicit misuse/abuse campaign, rules choosing agent versus human per test, an issue-producing human-task runbook handoff, or a standardized scored release approval gate. Existing guide coverage and install GREEN are not substitutes for these requirements.
- **Issue discussion update:** #429's only comment (2026-11-17) recommended waiting for #354's final workflow ledger and choosing extension versus separate pipeline. #354 now has a final workflow ledger dated 2026-11-18, but it still records failed/unverified checks and a later repeat; it is input, not a proven release-wide PASS. #201 was explicitly folded into #429 and closed on 2026-11-17.
- **Newer remote evidence:** PR #667 merged on 2026-11-19, commit `141e97fec7bc0cc5cfe9995bd2e328f428fccf4d`, describes 6.1.0 docs/install work and explicitly excludes new human guides. That directory is absent in this checkout, so its source/transcript contents are **UNVERIFIED locally**; the merge metadata, file list and PR body were read through allowed `gh pr view`. Do not confuse this with evidence that #429 is implemented.

## Concrete next steps
1. Use #354's existing final ledger and the current manual release checks as inputs now; do not wait for the entire still-open historical testing issue to close. Identify capabilities with conclusive agent evidence, capabilities needing a person, and gaps that neither covers.
2. Resolve the architectural choice still open in #429: a pre-sign-off mode in the existing protocol versus a separate gate using its discovery, evidence and manifest conventions. Recommendation: preserve post-release follow-through semantics and reuse its evidence structures rather than treating documentation completion as functional success. This report does not authorize that decision or a build.
3. Specify normal-use and misuse/abuse test cases, isolated targets, allowed actions, agent/human routing, evidence freshness, and how unresolved or unverified results block sign-off. Produce a human runbook suitable for a coordinator-created issue; workers must not post it themselves.
4. Define a versioned scorecard with consistent criteria, coverage denominators, failure handling, a minimum passing score, and non-waivable blocking checks so a high average cannot hide a security or data-loss failure.
5. Implement the selected route and demonstrate one end-to-end release-candidate run plus negative checks: failed, missing or unverified required evidence must prevent sign-off. Reuse the manual gate and installer proof instead of replacing them speculatively.

## Complexity and size
**Complexity: complex. Size: L.** Discovery and install proof are reusable, but consistent scoring, real functional and abuse execution, isolated environments, human handoff and a before-sign-off decision cross several boundaries and require negative-path validation; this is not a small post-release wording change.

## Priority
**P1, recommended triage priority, not a GitHub field change.** It closes a high-impact release-confidence gap across user-facing behavior and misuse scenarios; present installs and manual checks do not establish full intended behavior before sign-off. It blocks the requested scored release approval process, but no observed outage, exploit or universal release stop was verified, so not P0. The existing release procedure remains usable while this feature is designed.

## Dependencies
- GitHub's `blockedBy` and `blocking` fields for #429 both returned empty lists, count 0. **No formal issue dependency or blocked downstream issue is verified.**
- #354 (v5.0.0 impact validation) is an evidence/input relationship, not a mandatory completion dependency: the final workflow ledger is already posted even though later work remains open.
- #201 (TDD-driven release gating) was absorbed into this issue and is closed, not a prerequisite to reopen.
- #571 (6.0.0 release cleanup plan) and #647 (6.1.0 removals) change what the gate must test; they are release-surface context rather than prerequisites. No dependency on the separate #487 experiment framework is established.

## Related issues
- [#201](https://github.com/IronbellyOrg/IronClaude/issues/201), TDD-driven release gates: CLOSED, explicitly folded into #429 by the 2026-11-17 comment.
- [#354](https://github.com/IronbellyOrg/IronClaude/issues/354), v5.0.0 impact runbook: OPEN, real test/measurement evidence and the 2026-11-18 final workflow ledger; unresolved/unverified checks and a future repeat remain in its discussion.
- [#571](https://github.com/IronbellyOrg/IronClaude/issues/571), 6.0.0 release cleanup plan: OPEN; describes the manual release gate and a restricted docs/install post-release scope. Its historical planning statements are not used as proof that current code is absent.
- [#647](https://github.com/IronbellyOrg/IronClaude/issues/647), 6.1.0 task/documentation bundle removal: CLOSED according to `gh issue list`; release-surface context, also referenced by PR #667. Detailed issue history was not inspected.
- [#487](https://github.com/IronbellyOrg/IronClaude/issues/487), reusable spec/task experiment framework: OPEN; proposes scoring and reproducible model experiments. Potential reuse discussion only, not proof of a release gate implementation or a prerequisite for #429.

## Related PRs
No PR is returned in #429's `closedByPullRequestsReferences`; an exact `#429` body-reference search returned no matching PR. A general numeric search also matched unrelated HTTP-429 work, which was excluded. Search results are not proof that no unlinked work exists.

| PR | Verified state and commit | Relationship |
|---|---|---|
| [#218](https://github.com/IronbellyOrg/IronClaude/pull/218) | MERGED 2026-07-06; `0d3b99c84fbfc3efa4757343ebd9d4cf37228ab1` | Command/protocol split and install/activation tests, predates #429. |
| [#353](https://github.com/IronbellyOrg/IronClaude/pull/353) | MERGED 2026-11-03; `5e513796b8f2087ef79323dbf928aaa9924508a0` | v5.0.0 docs, install proof and human guides used by #354; partial outcomes recorded, not the new gate. |
| [#649](https://github.com/IronbellyOrg/IronClaude/pull/649) | MERGED 2026-11-18; `bc3d796aa89c33d1f9e4766ea9fd18417ab0a61e` | v6.0.0 docs/install follow-through; no new user/operator test guides by decision. Files and transcript are in this checkout. |
| [#667](https://github.com/IronbellyOrg/IronClaude/pull/667) | MERGED 2026-11-19; `141e97fec7bc0cc5cfe9995bd2e328f428fccf4d` | v6.1.0 docs/install follow-through, guides excluded; metadata/body/files verified remotely, actual files absent locally and not fetched. |

The post-release source history's newest relevant change is `119622e3a` (#356, 2026-11-04); no later source-package change appeared in the path-limited local log. This does not claim remote master contains no later change.

## Verification limits and negative evidence
- Review date: 2026-11-23. This is a source and issue-history assessment, not a newly run release test. No source files, issues, PRs, labels, comments, links, branches or commits were changed; only this task's report directory was written. No staging was authorized.
- **UNVERIFIED: full GitHub event timeline.** The permitted `gh issue view/list` surface supplies body/comments, state, timestamps, dependencies and closing PR references but no event timeline field. The whole sole comment on #429 was read; earlier/later label, assignment or cross-reference events cannot be certified from that surface. No forbidden API or browser route was used. Do not interpret the report as a complete timeline audit.
- **UNVERIFIED: unlinked work or implementation on other branches.** Exact body-reference PR search returned no #429 result; the post-release PR title search found the supporting work listed above. Broader source grep found unrelated gate/scoring code; no claim of repository-wide proof of absence is made.
- **Checkout/remote mismatch:** `docs/testing/v6.1.0/post-release-report.md` was missing on two Read attempts, and the local directory listing contains 5.0.0 and 6.0.0 records only. PR #667's merged state/body/file list are remotely verified, but its artifact contents are **UNVERIFIED** here. No fetch, checkout or remote mutation was performed.
- Other negative evidence: package grep did not identify scoring, abuse or pre-release behavior; `.github/workflows` name/content grep found no post-release/pre-release/release-gate match; tests name/content search found install/routing/worker-contract references. These are search limits, not proofs about every possible mechanism. The broad `.dev` search was noisy and capped, then narrowed; the only exact issue-number/phrase hit was unrelated HTTP-429 research.
- Failed tool attempt: this installed `gh` rejects `issue view --comments --json`; the successful retry used `--json ...comments...`. Codegraph could not outline the Markdown protocol; direct source Reads supplied evidence. No fresh test run or runtime exploit/abuse attempt was made, as required by the quick static analysis boundary.
- Required command output: `.dev/issuecleanup/g1/429/analyze/analyze-report.md`; command contract and handoff are adjacent under the requested analysis directory. The analysis records graph readiness, recommendations and verification limits. Independent evidence review is recorded in `.dev/issuecleanup/g1/429/review.md`.
