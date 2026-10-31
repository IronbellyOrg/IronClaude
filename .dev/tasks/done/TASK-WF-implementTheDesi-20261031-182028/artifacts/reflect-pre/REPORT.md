# Reflect report: pre-execution review of the pr-submit Codex plan

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.83
citations_total: 57
citations_revalidated: 57
citations_dropped: 0
citations_inferred: 3
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

Status is `partial` because the adversarial merge ended `BLOCKED_BY_INVARIANTS` (two HIGH invariant findings, INV-001 and INV-002, were open at the end of Round 2.5 and depth `standard` has no Round 3). The evidence-validator dropped zero of 57 citations; per §11.2 the run records `zero-drop-flag: true` in audit.log.

- Spec: `.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/source.md` (linked design `.dev/pr-submit-codex/design/pr-submit-codex-design.md`)
- Tasklist: `.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/TASK-WF-implementTheDesi-20261031-182028.md`
- Coverage: 0 parsed IDs, 141 inferred rows; containment match 76/141 (`coverage_pct_union` 0.539, `S_dev_density` 0.461); the reviewers agree most unmatched rows are covered in substance, and the real gaps are the merged findings below.
- Tier decision: rule 4 (`S_domains` 3) plus the parsed-sparse pre-filter → Tier 2 with 3 reviewers (sonnet, glm via haiku slot, opus), calibrator fable (disjoint), executor class unresolved (WARN).
- Merged verdict: `adversarial/merged-verdict.yaml` (28 findings: 2 high, 13 medium, 13 low; base reviewer-3, convergence 0.94).

## Inferred requirements (Pass 2)

All 141 rows are in `artifacts/coverage-matrix.yaml` with quote, citation and match result (2 from source.md:1, 139 from design sections 4-16). No inferred row was dropped by the evidence gate.

## Deviations (UC-1: plan vs spec)

### Deviation D-001: Task 2 silently disables Codex for contract-setup overrides
- **Location:** .dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/TASK-WF-implementTheDesi-20261031-182028.md:44
- **Mapped tasklist item:** Task 2
- **Spec section:** design §14 ("defaults baked, YAML-overridable", design:303), §4 (design:96-97, 108)
- **Evidence:** src/superclaude/pr_submit/contract_setup/writer.py:151-163 writes no Codex keys; detection.py:183-184 prefers that override; detection.py:147-157 already falls back for missing decline keys.
- **Classification:** drift
- **Classification rationale:** the task acceptance contradicts the design's baked-default rule; all three advocates conceded.
- **Default remediation:** from_yaml falls back to the shipped Codex values when a key is absent (key-presence check); explicit "" disables; direct construction stays empty.

All other findings are gaps or refinements (missing or under-specified obligations), listed with remedies in `adversarial/merged-verdict.yaml`.

## Inferred-claim audit

- `citations_inferred: 3`
- Inferred-fraction: 3 / 57 = 0.05

## Recommendations

### Recommendation R-001: Make the Codex completion time robust (M-01, M-03)
- **File:** src/superclaude/pr_submit/classifier.py, src/superclaude/pr_submit/reviewers.py
- **Change:** add a keyword `completed_at` to `_thread_findings`; Codex completion = max(marker `updated_at`, Codex formal review `submitted_at` for the head).
- **Verifier:** a test fixture whose Codex root `createdAt` is later than the marker `updated_at` still classifies `findings`.
- **Linked deviation(s):** none (gap)
- **Priority:** P0

### Recommendation R-002: Feed sticky absence into the wait outcomes (M-02, M-09)
- **File:** src/superclaude/pr_submit/reviewers.py, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
- **Change:** `augment_wait_outcome`/`codex_wait_outcome`/`merge_wait` take the absent set; an Augment silence outcome with Codex present continues with Codex.
- **Verifier:** a merge row test where Augment is absent and Codex done returns Codex's outcome immediately.
- **Linked deviation(s):** none
- **Priority:** P0

### Recommendation R-003: Follow the design, not Task 2's line 44 (M-05)
- **File:** src/superclaude/pr_submit/detection.py
- **Change:** key-presence fallback to shipped Codex values.
- **Verifier:** override without Codex keys loads Codex identities; override with `codex_bot_login: ""` disables Codex.
- **Linked deviation(s):** D-001
- **Priority:** P1

### Recommendation R-004: Absorb the remaining medium findings in their tasks (M-04, M-06..M-15)
- **File:** n/a (Tasks 3, 7-14)
- **Change:** apply each remedy in merged-verdict.yaml during the named task.
- **Verifier:** each task's QA checks the corresponding remedy.
- **Linked deviation(s):** none
- **Priority:** P1

### Recommendation R-005: Apply the low findings (M-16..M-28)
- **File:** n/a
- **Change:** as listed in merged-verdict.yaml.
- **Verifier:** per-task QA.
- **Linked deviation(s):** none
- **Priority:** P2
