# Pre-execution compatibility-plan reflection

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 1
confidence_calibrated: 0.71
coverage_degraded: parsed-sparse
citation_budget_policy: full_reread
```

## Summary

Do not execute this plan as written. The independent Tier1 reviewer found a broad-copy scope risk in Task2; the separate Tier1b calibrator returned0.71, not a passed gate. Canonical source is already compatible, while the installed skill is stale; a normal one-skill refresh should not require an unconditional copy of unrelated project mirrors. All helper invocations were explicit sonnet/Tier1b. The owner permits only this one model class, so required heterogeneous escalation cannot run; this is an openly degraded Tier1 advisory result, not a heterogeneous or complete-plan pass.

## Inferred requirements (Pass 2)

Eleven quote-pinned inferred rows are preserved in coverage-card.json and coverage-matrix.json with exact source-line spans. No parsed requirement IDs were found. Parent deterministic item-only containment matching (fixed stopwords recorded in matrix) yields4/11, union coverage0.363636; parsed coverage is null and parsed-sparse remains explicit. Seven automatic misses include policies that the human review sees in global Constraints; those global provisions are not falsely counted as deterministic item matches. This low textual score is not a claim that seven requirements were actually omitted; it prevents a vacuous full-coverage claim.

| ID | Verbatim source quote | Citation | Deterministic match |
|---|---|---|---|
| INF-001 | No permission/tool broadening, installed/mirror workaround, gate waiver, unrelated refactor, merge or issue closure. | source.md:5 | none |
| INF-002 | Every subsequent helper must use explicit verified Tier1b; no Opus fallback. | source.md:5 | none |
| INF-003 | no new canonical source edit is justified unless focused tests prove an actual canonical gap. | source.md:9 | T2 |
| INF-004 | Inspect installer implementation and target before running; preserve entire previous skill package in a private backup outside installed primitive directories. | source.md:11 | none |
| INF-005 | Do not use full superclaude install/update (would overwrite unrelated customization), do not hand-edit installed definitions, agent profiles, settings or permission lists. | source.md:11 | none |
| INF-006 | The normal scoped refresh must copy existing canonical content unchanged, not add tools or weaken rejection rules. | source.md:11 | none |
| INF-007 | preserve authorization/active-source hashes/backup and run focused canonical contract/install tests | source.md:15 | T1 |
| INF-008 | explicit Tier1b restricted diagnostic-worker smoke check and independent evidence check before resuming existing diagnosis. | source.md:15 | T2 |
| INF-009 | No destructive tests, huge files, benchmarks, gates waived or invented passes. | source.md:15 | none |
| INF-010 | Plan ends at verified compatibility readiness, not source bounded-reader fix, PR repair push or merge. | source.md:17 | T2 |
| INF-011 | Stage .dev/tasks always. Do not stage .claude mirrors. | source.md:17 | none |

## Grounded findings

- Scope risk: plan:43 mandates make sync-dev, which copies every skill/agent/command/hook at Makefile:112-142. Source:5,11 requests narrowly scoped normal installation and no mirror workaround. This is an unconditional broad-copy instruction, not proof of actual byte changes or customization loss. The reviewer explicitly clarified that byte-identical copying is not capability broadening and did not run a copy. Parent separately confirmed current make verify-sync passes; no write occurred, and that does not make the unnecessary instruction selective.
- Destructive sequencing: install_skill.py:47-52 removes the existing skill before copytree. Source:11 requires preserving and checking the previous target. Private backup permissions, runtime-selected source/target identity and before/after invariance baselines should be explicit before any force replacement. Parent separately verified the actual runtime source points to this checkout and intended target; no installation has run.

## Grounding Gaps

Only one model class is owner-permitted: model/calibrator/executor diversity is degraded; no Opus or alternate fallback is used. Coverage is inference-assisted and item containment is not semantic proof. The independent calibrator's0.71 score is preserved and not increased by later parent evidence. Initial canonical51-test baseline and runtime source binding are parent-collected, not future install or smoke success. No installed/profile/permission/PR mutation or execution has occurred. Input snapshot remains pinned. This is a pre-execution scope check, not an observed runtime regression.

## Recommendations

Preserve this plan and check unchanged; do not edit it from this advisory review or execute its broad-copy instruction. A new bounded plan should use only the existing selective installer plus read-only synchronization verification, explicitly bind runtime source/target and private complete backup, and pin profiles/settings/unrelated-skill baselines before deletion. Clarify requirement IDs and task-specific coverage without changing the owner's scope or claiming prior checks passed. No code fix, permission broadening, confidence waiver or new PR review allowance follows from this report. The separate original0.80 diagnostic failure remains immutable.
