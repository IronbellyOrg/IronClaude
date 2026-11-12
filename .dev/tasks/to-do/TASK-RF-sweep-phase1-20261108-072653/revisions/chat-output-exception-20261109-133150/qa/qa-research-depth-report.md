# QA Report: Research Depth

**Date:** 2026-11-09
**Phase:** research-depth
**Fix authorization:** false
**Producer:** rf-qa-qualitative ae25f9f3e5028c2ba
**Transport:** Parent persisted the returned independent assessment. Producer explicitly could not write reports; no parent verification or finding downgrade is implied.
**Overall verdict:** FAIL
**Blocking findings:** 1
**Minor notes:** 1

## Reviewed documents

Citation root R is `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/revisions/chat-output-exception-20261109-133150/` under `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode`.

- R01: R/research/01-style-and-tests.md.
- R02: R/research/02-executor-preservation.md.
- R03: R/research/03-template-and-plan-integration.md.

Scope note read in full; all source Read calls <=150 lines.

## Items Reviewed

| # | Depth check | Result | Independent evidence and assessment |
|---|---|---|---|
| 1 | Research explains HOW components work | PASS | Inspected both style copies, installer copying, development sync, injection hook, executor helpers/resume. R01 explains installation chain; R02 explains numeric-map vs label completion and original-start reuse. |
| 2 | Flows traced end-to-end | FAIL | Style/install/error/tests/review flow traced, but no positive source of coordinator authority. R01:38 requires role, :42 unknown fallback, :87 identity unverified. Positive exception still needs an invented predicate. RD-01. |
| 3 | Edge cases/errors/failure modes | PASS | R01:56-63 covers malformed JSON, unreadable/missing reports, lookup exhaustion, unknown identity/injection. R02:26-36,43-56 covers stale map, immutable starts, HEAD changes, history preservation and design loss during retry. Positive-role gap counted under2/5, not a separate finding. |
| 4 | Replicable patterns | PASS | R01 gives exception text, seven mandatory sites, wrapper conflicts, section-scoped text checks; graph/severity patterns independently read. R03 gives per-file ownership, gate inputs/fixer allowlists/final diff. Static versus live behavior distinguished. |
| 5 | Builder can act without invention | FAIL | Allocation concrete, preservation detailed; positive coordinator-only trigger and person-requested sweep in coordinator session remain unspecified. RD-01. |

Checks passed 3/5; failed2/5; unique blocking findings1; fixed0.

## Issues Found

### RD-01: IMPORTANT, blocking - Coordinator eligibility remains undefined

Locations: R01:38-44,56-63,87; propagated into R03:46-47,71-76.

Proposed exception requires a coordinator executing the loaded skill, excludes person-run invocations, prohibits files/tool/report/quoted text from establishing role and defaults to ordinary formatting for unknown role. It never identifies trusted positive evidence that makes the role known. This is not a demand for a runtime detector or proof of model reliability: it is a missing instruction contract and classification of overlapping cases.

Independent source: `docs/designs/orchestrator-mode.md:655-663` specifies explicit invocation, tools, fallback/parse/read/output, not coordinator identity. Its lines677-679 assign duties without a role-establishing input. Source search for role establishment in distributable Markdown found no matching rule; this is supporting negative evidence, not proof that no mechanism exists anywhere. R01:87 honestly marks identity unverified but does not meet scope's unambiguous-trigger requirement.

Concrete case: an already established coordinator receives a direct person request to sweep. It is both coordinator-executed and person-requested. Does person-run exclude it, or mean only a non-coordinator session? Research does not say.

A builder must invent authority, broaden exception using invocation/report text, or always use unknown fallback (leaving required positive exception unsatisfied). Exact-string tests can preserve this ambiguity.

Required gap-fill before builder:
- Identify existing trusted session-level evidence for coordinator status, or explicitly say none sufficient was established.
- Define person-run relative to role, including person-requested sweep in existing coordinator session.
- Specify same eligibility in style wording, future skill and test matrix.
- Keep report/file/tool role claims non-authoritative and unknown fallback ordinary.
- If distinction cannot fit authorized scope, state precise blocker instead of delegating unspecified detection.

No new flag, hook, parser or permission expansion is implied.

### MN-01: MINOR - Future behavioral-verification route not selected

R01:63 separates behavioral verification from static assertions but leaves manual/eval route to later selection. Retain this limit in completion report; wording-test passes are not live format/injection-resistance passes. Does not independently fail research.

## Other Scope Findings

- Seven mandatory restatements and WHAT/recommended-action conflict correctly covered against canonical style.
- Failure visibility/file injection boundary sound as instructions, not proven model resistance.
- Installed activation distinction substantiated: sync omits styles, nonforced install may retain existing file, hook reads HOME style.
- R02 preservation checks are substantive; five-file manifest not misrepresented as recursive evidence proof.
- R03 maps separate source/skill/test bodies and later consumers, with early edit explicitly conditional on revised phase approval.
- Historical failed predicates/scoped waivers preserved; counts alone not semantic coverage.

## Confidence and Tool Engagement

Reviewer reported Verified5/5, Unverifiable0, Unchecked0, confidence100%. This means checks investigated including failed ones, not a research pass. Read54/Grep5/Glob1/Bash0; no external research, network, tests, Orca, Git mutations, helpers, subagents or team tools. Live model behavior, installed reload timing, Git-object existence and complete historical-byte parity were not independently demonstrated; explicit limits, not successful runtime checks.

## Self-Audit

No inherited structural PASS relied on. Independent semantic checks compared actual style to designed skill flow (exposing missing role contract), installer/sync/hook to distinguish activation, helper/resume/retry semantics for preservation, and command/static-test patterns for limits. About40 discrete source-backed assertions checked, not all historical statements or future behaviors executed/proven.

## Recommended Action

Obtain targeted gap-fill for RD-01 and re-review amended trigger contract before builder. Remaining research is concrete enough to retain; no wholesale re-research warranted. No change/fix made by reviewer; original conclusion FAIL preserved.

VERDICT: FAIL
