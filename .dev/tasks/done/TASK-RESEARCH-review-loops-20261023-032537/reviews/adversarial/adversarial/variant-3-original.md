# Research: Review Contracts Change During the Loop

**Investigation type:** Evidence-backed causal hypothesis
**Scope:** Six selected historical sessions; candidate three, not a final rank
**Status:** Complete, hypothesis for debate; not ranked or independently approved
**Date:** 2026-10-23
**Governing template:** tech-research/SKILL.md, Codebase Research Agent Prompt

## Hypothesis
Review does not always preserve one operative contract across stages or attempts. Literal criteria are softened, useful hardening is treated as required compliance, conflicting source instructions are unresolved, or installed policy changes mid-run. This can create reversals and additional reviews even when delivery files do not change.

## Exact Mechanism
1. The written requirement, the early review's interpretation and the later review's rule are not equivalent.
2. A local pass or claimed fix is judged under one interpretation, then a fresh reviewer applies another or a newly loaded policy.
3. The next verdict may reflect a real original violation, added checking scope, policy migration or a mixture, rather than new implementation damage.
4. Without recording the exact original criterion and loaded rules, evidence correction and changed acceptance are indistinguishable in the outcome.

## Supporting Incidents and Primary Evidence
**Counting:** Contract mechanisms in one run are not additional independent sessions or reviews.

Each row identifies a distinct contract mechanism; none establishes that all later findings were invented.

| Mechanism | Observed consequence | Research and primary anchors |
|---|---|---|
| Task QA relaxes a literal lint criterion | Task6 accepts unchanged preexisting lint findings as no-new-findings despite a no-finding-on-changed-line clause. FINAL applies the original clause; owner acceptance is obtained only later. | [Credential finals](../research/06-session-0690ee9f.md), section4; `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866.jsonl:1215,1230,1935,1938`; nested Task6 reviewer `agent-a6d8fbaf69a56dd14.jsonl:61` under that session. |
| FINAL rubric changes between reviewers | Old rule treats stale evidence as issues; later rule says moved line alone is not issues and changes acceptance handling. Final pass follows both evidence fixes and policy change. Their separate effects cannot be isolated. | [Credential finals](../research/06-session-0690ee9f.md), section5; exact captured texts in [historical-review-rules.json](../research/historical-review-rules.json). Original nested `agent-acf0a51e6992c50ee.jsonl:18` at20:26:30.085Z and `agent-a4bfff371c63a6c39.jsonl:18` at20:32:19.277Z, both beneath the credential session above. |
| Implementation migration adds a fresh review | Original reviewer returns compliant, but updated resume rules require a new operator review before completion. That review finds real earlier omissions. | [Monitor case](../research/05-session-e002bed2.md), section5.4; `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-orca-upstream-tracking/e002bed2-7877-42c1-8665-8cb8595587b6.jsonl:42,58,849,874,893,902`. No adviser/revert ladder executed for this task. |
| Broader risk checking enters compliance review | Some monitor findings concern uncapped fields explicitly absent from the plan or case-insensitive matching not clearly required. Later user-authorized fixes do not make these retroactively original criteria. | [Monitor case](../research/05-session-e002bed2.md), sections4-5; same monitor log `:906`, `:1143`; per-review prompts require any defect of any severity to be noncompliant. |
| Source and review scope disagree | Orca prose and diagram conflict on up-to-date state and repository-check timing. CI boundary-file comparison is initially called an incomplete original repair, then conceded optional because the original finding names different files. | [Orca planning](../research/01-session-ac2cd1fd.md), section6, source `:142,285,382,402`; [CI planning](../research/04-session-43582de1.md), section6.3 and eight-entry addendum, regenerated debate `adversarial/round2-v1.md` under the exact review directory in that case. |

## Counterevidence
- Oracle review retains exactly the original default-path requirement; no moving criterion explains its second failure. The limitation is frozen repair authority ([oracle case](../research/02-session-a9b88895.md), sections4/6).
- The manual-page reviewer twice requests the same real rendering proof. Static checks do not satisfy that unchanged criterion; acceptance is not repaired rendering ([documentation case](../research/03-session-6f744b87.md), sections2-4).
- The fresh monitor review finds genuine defects present before the policy change. Migration adds a review, but does not make those findings invalid or cause their original code.

## Scope, Overlap and Competing Explanations
This is a family of contract-consistency failures, not a claim that all reviewers invent requirements. Keep original source contradictions, unauthorized interpretation changes, justified operator decisions and live policy migrations individually attributed.
Weak checks and repair-induced defects remain competing explanations for the artifact's actual state. Contract instability primarily explains reversals, disagreement, extra review entry, and difficulty attributing final convergence. It is a proven amplifier in two runs, not a universal source of defects.

## Discriminating Test
Preserve original requirement text, accepted exceptions, exact loaded rubric bytes and artifact state for every reviewed attempt.
- Have independent reviewers adjudicate each disputed finding twice: once under the original fixed contract, once under the actually changed contract.
- Classify differences as original violation, authorized acceptance, explicitly added hardening, unresolved contradiction, or rule-version effect.
- If identical policy/criteria and artifact state still yield the same substantive failures, contract change does not explain those failures. If a verdict or required fresh review changes solely with the contract, the mechanism gains support.
No historical replay was run for this card. The experiment must not waive valid findings or treat an operator's accepted gap as compliant work.

## Provisional Evidence Strength and Limits
Direct captured tool results prove two rubric versions in the credential run; monitor records prove migration reopened a compliant check. Literal lint relaxation and later reapplication are also explicit.
Which actor changed the installed rubric, and whether policy change alone would pass the unrepaired package, remain unknown. Broader hardening findings vary in validity; do not combine them into a count of fabricated defects.

## Key Takeaways
- Record both the original acceptance contract and the exact review policy actually loaded; current installed rules cannot establish historical execution.
- A changed verdict can follow valid evidence repairs and changed rules together. That is not a controlled demonstration of repair effectiveness.

## Gaps and Questions
The effects of policy changes and evidence corrections are confounded in the credential final pass. Stable-criterion oracle/render failures remain counterexamples. No evidence establishes that all broad review demands were invalid, or that minimum reviewer counts caused the instability.

## Stale Documentation Found
The same installed rubric path returned materially different contents to consecutive reviewers. [Captured historical rule evidence](../research/historical-review-rules.json) preserves both versions; [current-rule map](../research/scope-rules.md) is explicitly not substituted for them. Source contradictions are disclosed rather than silently resolved.

## Summary
The sample contains genuine contract inconsistency and mid-run policy changes that explain extra reviews or reversals. These mechanisms amplify other defects but do not make every later finding invalid. Their relative importance must be debated alongside the stable-contract cases and independently traced implementation defects.
