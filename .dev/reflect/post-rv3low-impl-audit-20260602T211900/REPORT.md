```yaml
contract_version: 1.1.0
status: partial
mode: post
tier_reached: 2
confidence_calibrated: 0.88
citations_total: 12
citations_revalidated: 12
citations_dropped: 0
citations_inferred: 0
citation_budget_policy: full_reread
evidence_validator_ran: true
regression_present: true
unauthorized_deviation_present: true
needs_human_decision: true
deviation_count_by_class: {authorized: 0, necessary: 0, drift: 0, regression: 2}
promotion_action: skipped
promotion_skip_reason: gate-failed
```

# Reflect UC-2 Post-Execution Audit — TASK-RF-20260602-135209 (Reflect-V3-Serena low-complexity)

**Mode:** post · **Tier:** 2 (heterogeneous ensemble: sonnet + haiku reviewers, executor=Opus excluded per §7.1) · **Verdict:** DIVERGENCES FOUND — 2 task-introduced Regressions.

## Why Tier 2 + why this matters

The reflect executor (Opus) IS the agent that produced the work under review, so single-agent self-review is structurally biased (§11.0). Two independent reviewers on classes disjoint from the executor (sonnet=correctness, haiku=qa) audited the on-disk artifacts against the driving spec's literal FR acceptance criteria. **They found 2 genuine spec-adherence regressions that all 8 internal rf-qa phase gates passed over** — because the inline gates verified field/section *presence* and invariant *names*, but did not (a) diff exact enum *tokens* against the spec's acceptance-criterion values, nor (b) execute the C1 predicate against the spec's worked numeric example. This is precisely the value the independent ensemble adds over inline self-QA.

## Findings (evidence-validated — every citation independently re-Read; 0 dropped)

### F-1 · REGRESSION (HIGH) · FR-8 C1 unbounded-retention predicate is inverted

- **Spec (gold standard):** FR-8.6 / C1 (`04-spec-low-complexity.md:271,280`) — emit `memory_retention_unbounded: true` when read-only entries make the **≤20-total target unreachable** (the read-only-dominated case, e.g. 25 total / 24 readonly / 1 deletable).
- **Implementation:** `SKILL.md:432` encodes the predicate as `(slug_count − readonly_count) > 20`, i.e. `deletable_count > 20`. For 25-total/24-readonly this is `1 > 20 = false` → the loud flag would **NOT** fire in exactly the case the spec mandates.
- **Internal contradiction:** my own eval fixture `cases/serena-memory-retention/expected.yaml:21` asserts `memory_retention_unbounded: true` for "25 total, 24 readonly, deletable=1" — the protocol text and its eval fixture disagree.
- **Correct predicate (intent):** fire when total slug-prefixed count `> 20` AND deletables alone are within budget (`(slug_count − readonly_count) ≤ 20`) — i.e. read-only entries are the cause. Equivalently `readonly_count` pushes total over 20.
- **Severity:** C1 was the spec review's single *provably-wrong* (CRITICAL) item; this re-introduces a provably-wrong predicate. **Classification: Regression** (contradicts FR-8.6 acceptance criterion).
- **Fix:** rewrite SKILL.md:432 predicate to key on total-unreachable-due-to-readonly (e.g. `slug_count > 20 AND (slug_count − readonly_count) ≤ 20 → memory_retention_unbounded: true`).

### F-2 · REGRESSION (LOW / cosmetic) · FR-6 `onboarding_status_source` enum mismatch

- **Spec:** FR-6.1 (`04-spec-low-complexity.md:239`) mandates `onboarding_status_source: activation_msg | list_memories_proxy | unknown`.
- **Implementation:** `SKILL.md:230` uses `activation_message | list_memories_proxy | none`. Two token mismatches: `activation_message`≠`activation_msg`, and `none`≠`unknown`. The `none` vs `unknown` mismatch is the more material one — `unknown` is the token FR-6.4 and the §9.2 `onboarding_status` field use, so the SOURCE enum is internally inconsistent with the STATUS enum.
- **Leak:** the wrong tokens also appear in `cases/serena-wave0-config/expected.yaml:20` and the evals.json id-21 assertion *description* (`evals.json:527`). NOTE: the actual id-21 assertion is `regex_present` on field *presence* (`evals.json:526`), so it does not catch the enum mismatch — which is why the gates missed it.
- **Classification: Regression** (contradicts FR-6.1's literal enum value contract), but trivial-fix severity.
- **Fix:** rename `activation_message`→`activation_msg` and `none`→`unknown` in SKILL.md:230 + expected.yaml:20 + evals.json:527.

## Pre-existing / out-of-scope (NOT task-introduced — surfaced for completeness)

### G-1 · report-template.md:14 still renders `contract_version: 1.0.0`

- `git diff HEAD` confirms `refs/report-template.md` was **unmodified** by this task; the `1.0.0` literal predates the session and was explicitly excluded from research-07's authoritative 5-site bump scope (it was cited there as the pre-existing 3-segment precedent). It is the same class as the task's own logged "MINOR advisory" co-located doc-refresh.
- **However**, it is a genuine consistency gap: after the §9.1 bump to 1.1.0, a generated REPORT.md header (rendered from this template, consumed by downstream parsers per report-template.md:11) would declare `contract_version: 1.0.0`, contradicting the contract it implements. **Recommend** bumping report-template.md:14 → `1.1.0` as a follow-up (it realizes the contract-bump intent; not a task regression).

### G-2 · evals.json ids 22 & 24 — `yaml_list_contains` indexed-scalar field_path won't grade

- Independently re-confirmed by the haiku reviewer against `grader.py:177-183`: `field_path: missing_implementations.0.abstract_name_path` (id 22) and `third_party_api_grounding.0.api_name` (id 24) resolve to scalars; `yaml_list_contains` requires a list → always-False at grade time. **Already logged** as a PG-4 Follow-Up Item; harmless for un-graded scaffolds; reconcile before scaffold promotion.

## What is ADHERENT (independently confirmed)

FR-1 (find_implementations + C3 Class-guard), FR-2 (find_declaration step 2a + 1B.3), FR-3 (include_info corrected path, no standalone tool), FR-4 (search_deps `<ext:…>` predicate), FR-5 (summarize_changes UC-2 step 7'), FR-7 (get_current_config + three-valued serena_version C2) — all adherent with file:line evidence. Corrected-form guards clean (`check_onboarding_performed`=0, `find_referencing_code_snippets`=0 in SKILL.md). No project-mutating Serena symbolic-editing tools in allowed-tools. 4 of 5 contract-bump sites + §9.1/§9.2 fence discipline correct. C2/C3/C4/C5 invariants correctly encoded.

## Promotion verdict (Wave 7)

**BLOCKED** — §14.5.2 gate condition 4 (`no_drift_no_regression`) FAILS with 2 regressions; condition 2 (`status == success`) also fails (status: partial). `promotion_action: skipped`, `promotion_skip_reason: gate-failed`. The task folder stays in `.dev/tasks/to-do/`. This is correct: a work-unit with open regressions must not auto-archive.

## Recommended remediation (audit-first — not auto-applied; `--remediate` not set)

1. **F-1 (HIGH):** fix the C1 predicate at SKILL.md:432 → fire on read-only-dominated total-unreachable, then `make sync-dev` + re-verify against expected.yaml:21.
2. **F-2 (LOW):** rename the FR-6 source enum tokens to spec (`activation_msg`/`unknown`) in SKILL.md:230 + expected.yaml:20 + evals.json:527.
3. **G-1 (follow-up):** bump report-template.md:14 → 1.1.0.
4. **G-2 (follow-up):** reconcile the ids 22/24 yaml_list_contains field_path before scaffold promotion.

F-1 and F-2 are small, well-scoped corrections to work from this same session.
