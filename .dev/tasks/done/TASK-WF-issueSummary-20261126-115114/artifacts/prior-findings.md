```yaml
contract_version: 1.9.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.7967
citations_total: 24
citations_revalidated: 24
citations_dropped: 0
citations_inferred: 0
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

# Pre-execution reflection: performance phrases

## Coverage matrix

Source snapshot: .dev/tasks/to-do/TASK-WF-issueSummary-20261126-031841/source.md. Candidate: the sibling TASK-WF-issueSummary-20261126-031841.md. Short source.md citations below resolve to that snapshot.

The deterministic matrix in coverage-matrix.yaml has 0 parsed and 16 quote-pinned inferred requirements. Five match by content-word containment (threshold 0.6): INF-001,003,005,008,011. Parsed-only coverage is null; union coverage is 0.3125; S_dev_density is 0.6875. The sparse-label pre-filter requires Tier2. Semantic reviewer coverage is broader than lexical matching and is not substituted for these numbers. The QA reviewer noted an additional representative-leak observation span at source.md:13 omitted from extraction but already covered by Task2.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | Extend the troubleshooting protocol's performance keyword row with “too long to load”, “takes forever” and “hangs”, so everyday wording such as “ccsession is taking too long to load” selects the performance type without an explicit flag. | source.md:11 | Task1, containment |
| INF-002 | Decide and document why “leak” remains listed under both performance and security, or how it should be handled, without silently sending security-sensitive leak reports only to performance. | source.md:11 | none |
| INF-003 | Record an observed manual run for the exact sample | source.md:11 | Task2, containment |
| INF-004 | follow the source-to-development-copy synchronization process | source.md:11 | none |
| INF-005 | extend a test only if existing tests already cover this table; otherwise record the manual verification | source.md:11 | Task1, containment |
| INF-006 | does not include a Jev call, comparison, preflight component or gateway change | source.md:11 | none |
| INF-007 | It assumes retaining the existing ambiguity rule or making only a narrowly bounded clarification, not redesigning security classification or implementing the parent feature. | source.md:13 | none |
| INF-008 | Source-text inspection is not the required observed manual result. | source.md:20 | Task2, containment |
| INF-009 | synchronization must populate it before verifying | source.md:23 | none |
| INF-010 | Do not stage generated `.claude/` copies. | source.md:23 | none |
| INF-011 | Implementation must run both and record the observed result; neither ran in this check. | source.md:24 | Task2, containment |
| INF-012 | preserve the issue's conditional test requirement rather than inventing a new test system. | source.md:25 | none |
| INF-013 | No manual troubleshooting run, test execution or synchronization verification was performed. Those remain implementation acceptance work, not claimed passes. | source.md:34 | none |
| INF-014 | Nothing to decide: build what the issue asks for, within its own scope. | source.md:38 | none |
| INF-015 | Existing command entry point and `--type` interface; inspect for consistency, but no command-file change is currently required by the issue. | source.md:22 | none |
| INF-016 | Performance type influences specialist lenses only if escalation reaches Tier 2; the phrase fix does not force agents to run. | source.md:21 | none |

## Deviations

### Deviation MF-1: Missing changed-skill selection mechanism

- **Location:** .dev/tasks/to-do/TASK-WF-issueSummary-20261126-031841/TASK-WF-issueSummary-20261126-031841.md:44-47
- **Mapped tasklist item:** Task 2
- **Spec section:** source.md:11,20,23
- **Evidence:** plan:23 requires the changed checkout skill and forbids changing the user-wide installation just to pass; Task2:44,47 names the ordinary invocation and the consumed copy, but no loading mechanism. CLAUDE.md:96 documents personal-before-project skills. Actual runtime precedence is unobserved.
- **Classification:** drift (pre-execution missing mechanism)
- **Grade/label:** Blocking (Missing), HIGH. Affected action: Task2's exact-sample observation and acceptance; ordinary invocation may use unchanged installed instructions.
- **Default remediation:** Specify a real execution route that consumes the changed checkout instructions, preserves the global installation, creates the Wave0 output/audit and records actual results without type override. Merely reading the keyword row and emitting expected text is not sufficient.

### Minor findings and follow-up candidates

- MF-2 Medium: unrelated repository-wide synchronization failure has no explicit reporting branch. No unrelated drift was observed. Location: plan:36,50.
- MF-3 Medium: ambiguous leak wording has no fixed sample. Existing ambiguity preservation remains required. Location: plan:44,48.
- MF-4 Note: run depth/output/escalation not pinned; plan already requires honest scope reporting.
- MF-5 Note: exclusion list omits the word comparison, but source binding excludes it.
- MF-6 Note: extraction omitted representative-leak observation, which the plan covers.

The adversarial review merged one blocker, two Medium findings and three Notes. Its diff-point agreement is 41/41 (1.0), but the independent invariant probe left two HIGH conditions open: the suggested direct-Read repair has not been shown to execute the skill rather than perform a static comparison, and its sufficiency is unproven. These conditions belong to the same missing-execution-route blocker, not proof that a repair works. The merge status is partial, not a clean pass. No implementation or runtime acceptance has occurred.

## Inferred-claim audit

- citations_inferred: 0

## Recommendations

### Recommendation R-001: Make the acceptance run consume the changed skill

- **File:** Task 2 in the candidate plan.
- **Change:** Add an explicit execution/loading method for the changed checkout skill, including writable audit output, preserving the exact sample and no --type override. Do not claim that static table inspection or reading instructions alone is an observed invocation. Preserve the global install and label any bounded Wave0-only run honestly.
- **Verifier:** A fresh reviewer confirms the repaired plan provides an executable method that produces the original acceptance evidence. Implementation must retain the actual invocation/consumed source and audit output.
- **Linked deviation:** MF-1; also discharges its two open sufficiency conditions.
- **Priority:** P1.

Review verdict: FAIL (one blocking finding). Minor findings are recorded only, never part of the repair brief. Requested reviewer classes differ but gateway identities and executor class are unverified; calibration diversity is degraded. This is review pressure, not a claim of verified model independence.
