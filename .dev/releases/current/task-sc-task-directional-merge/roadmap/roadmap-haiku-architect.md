---
spec_source: "TDD_TASK_DIRECTIONAL_MERGE.compressed.md"
complexity_score: 0.92
complexity_class: HIGH
primary_persona: architect
adversarial: true
base_variant: "none"
variant_scores: "convergence_score=0.86"
convergence_score: 0.86
prd_source: "PRD_TASK_DIRECTIONAL_MERGE.compressed.md"
extraction_source: "extraction.md"
---

# Task Directional Merge (/sc:task → /task) Roadmap

## Executive Summary

This roadmap plans the directional merge of the donor `/sc:task` command-and-skill surface into the recipient `/task` skill while preserving five load-bearing invariants, nine manifest exceptions, the rf-qa floor, and resumability across the live in-flight MDTM population. The work is organized by technical layer rather than by source-document order: foundation contracts, verification and pre-flight semantics, TFEP transfer, CLI/deprecation integration, and production readiness.

The implementation spine is the TDD's ten-step commit sequence, with extraction IDs preserved as separate deliverables so acceptance and traceability remain audit-ready. The highest-risk areas are INV-04 resumability, Step-5/Step-6 atomicity, CR-7 ordering, donor literal preservation, and residual `/sc:task` references outside authorized buckets.

Key targets are: 8/8 transfer verdicts preserved, 9/9 manifest exceptions traceable, 18/18 AC-ATK tests covered, 12/12 AC-SM tests covered, 136+ in-flight task files resumable, 144 residual references reduced to zero outside authorized buckets, F2 catalog expanded from 10 to 13 entries additively, and four post-merge rf-qa invocation surfaces retained or added without displacement.

## Milestone Summary

|Milestone|Technical Layer|Duration|Primary Deliverables|Exit Gate|
|---|---|---:|---|---|
|M1|Foundation contracts|5 days|Tier schema, CR-7 ordering, Gate 1 dispatch, compatibility shim, marker consumer boundary|Step-1 gate exits 0; ordering grep passes; in-flight parse resume passes|
|M2|Verification and pre-flight semantics|4 days|STRICT roster widening, git pre-flight matrix, rf-qa floor anchors, F1/F2 invariant guards|AC-ATK-02/10/11/13 and AC-SM-02/07 pass|
|M3|TFEP core transfer|6 days|Baseline YAML, prohibitions, escalation gradient, incident report schema, donor diff audit|AC-ATK-03/06/12 and AC-SM-08 pass|
|M4|CLI integration and donor deprecation|6 days|Runtime prompt reroutes, command soft-deprecation facade, donor hard-delete, CR-DEP-06 manifest, sync flock|Step-5/6 atomic gates pass; residual violations equal 0|
|M5|Production readiness and audit closure|4 days|Documentation rollup, runbooks, operational alerts, full AC-SM/KPI audit, deferred regeneration banners|mkdocs build clean; all success criteria green|

Total planned duration: 25 implementation days, with Step-5 and Step-6 treated as atomic release windows and no parallel writes to `task/SKILL.md` during the Step-5 boundary.

## Dependency Graph

```text
M1 Foundation contracts
  ├─> M2 Verification and pre-flight semantics
  │     └─> M3 TFEP core transfer
  │            └─> M4 CLI integration and donor deprecation
  │                   └─> M5 Production readiness and audit closure
  ├─> M4 Step-5 is blocked by S-1 in-flight discharge/snapshot-freeze
  └─> M4 Step-6 is blocked by Step-5 atomicity, donor diff audit, rf-qa chain verifier, and sync-dev flock readiness
```

Cross-cutting dependency rules:
- CR-7 ordering is load-bearing from M1 onward: `path_override_check()` → `tier_field_validate()` → `gate_1_dispatch()`.
- `rf-qa` remains a floor in M2, M3, M4, and M5; `quality-engineer` may supplement but never replace it.
- `Tier:` and Gate 1 ship together in M1; the CR-FM-03 compatibility shim is not deferred.
- Runtime references to `/sc:task` must be eliminated from `src/` and `.claude/` by M4, while authorized archived buckets remain dispositioned.

## M1: Foundation Contracts

**Duration:** 5 days  
**Purpose:** Establish the atomic task-entry contract that all later transfer work depends on: canonical tier vocabulary, row-1 CR-7 ordering, compatibility parsing, Gate 1 dispatch, and marker read boundaries.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---:|---|---|---|---|---|---|---:|---|
|1|FR-CS-1|Atomic foundation landing|Land CR-FM-01..03, CR-TASK-01..04, CR-7 sentinel, row-1 call site, and AC-ATK-05 register in one source-tree merge.|COMP-001, COMP-002|None|CR-FM-04 grep plus sentinel grep pass|L|Must|
|2|FR-CS-2|Tier classification and Gate 1|Implement `Tier:` contract, Gate 1 dispatch, canonical enum validation, and malformed-tier HALT before F1 starts.|COMP-001|FR-CS-1|Closed enum and parse-error tests pass|M|Must|
|3|FR-TU-1|Tier field and marker transfer|Add optional `Tier:` ∈ `{STRICT, STANDARD, LIGHT, EXEMPT}`, task-entry classification header, once-per-entry dispatch, and read-only per-item marker.|COMP-001|FR-CS-1|AC-ATK-05; `gate-1:` emitted exactly once|M|Must|
|4|FR-TU-2|Path override ordering|Fire `path_override_check()` first, then `tier_field_validate()`, then `gate_1_dispatch()`; critical ANY-match forces STRICT, trivial ALL-match forces LIGHT.|COMP-002|FR-CS-1, FR-TU-1|AC-ATK-01/13; AC-SM-07/08|M|Must|
|5|NFR-INV-1|F1 progress monotonicity|Preserve READ→IDENTIFY→EXECUTE→UPDATE→REPEAT and forbid new environment-driven HALT mid-checklist.|COMP-001, COMP-002|FR-TU-1, FR-TU-2|AC-ATK-02/10/13|M|Must|
|6|NFR-INV-4a|Parse-layer resumability|All existing MDTM TASK files parse and resume with YAML frontmatter, checklist syntax, append-only log, and absent `Tier:` defaulting to STANDARD.|COMP-001|FR-CS-1|136+ in-flight parse fixture passes|M|Must|
|7|NFR-INV-5|Refusal-of-definition|Treat `Tier:` and `(Tier: ...)` as metadata for audit conditioning, not runtime work definition or per-item dispatch.|COMP-001|FR-TU-1|Marker consumer audit passes|M|Must|
|8|NFR-ME-1|Pre-loop dispatch only|Constrain dispatch to task entry; per-item marker is read-only and cannot re-run Gate 1 during F1 EXECUTE.|COMP-001|NFR-INV-5|CR-TASK-02/03 acceptance|S|Must|
|9|NFR-ME-6|Tier and Gate 1 atomicity|Ship `Tier:` field, compatibility shim, CR-7 call order, and Gate 1 together to avoid partial semantics.|COMP-001, COMP-002|FR-CS-1|AC-ATK-06/17|S|Must|
|10|DM-001|Tier frontmatter schema|Define inline `Tier:` with fields: storage=frontmatter row 1; cardinality=0..1; type=string; enum=STRICT/STANDARD/LIGHT/EXEMPT; required=no; default=STANDARD; mutability=author-set only; validation=closed enum/order/HALT/fallback; retention=task lifetime.|COMP-001|FR-TU-1|Every field verified in schema fixture|M|Must|
|11|DM-002|Per-item marker schema|Define marker with fields: storage=checklist body; cardinality=0..N; token=`(Tier: <VALUE>)`; regex accepts checkbox plus `(Tier: <enum>)` with enum STRICT/STANDARD/LIGHT/EXEMPT; placement=after checkbox; default chain=per-item→task→STANDARD; malformed=warn; consumers={CR-TASK-07 baseline-skip}.|COMP-001|DM-001|Closed consumer test passes|M|Must|
|12|API-001|Path override API|Implement `path_override_check(task_target_paths: list[str]) -> forced_stance ∈ {STRICT, LIGHT, none}` with critical ANY-match, trivial ALL-match, one Task Log line, and INV-01/04/05 binding.|COMP-002|FR-TU-2|Ordering and emission tests pass|M|Must|
|13|API-002|Tier validation API|Implement `tier_field_validate(frontmatter: dict) -> tier_field ∈ {STRICT, STANDARD, LIGHT, EXEMPT}` with absent-to-STANDARD shim, non-enum `ValueError`, and rejected literal guard.|COMP-001|DM-001|Malformed tier HALT fixture passes|M|Must|
|14|API-003|Gate 1 dispatch API|Implement `gate_1_dispatch(forced_stance: str, tier_field: str) -> execution_profile` with precedence STRICT override, LIGHT override, then task tier mapping; fire once per task entry.|COMP-001|API-001, API-002|Single-dispatch test passes|M|Must|
|15|COMP-001|Tier parser and Gate 1 component|Add row-0 CR-7 sentinel, task-level tier parser section, F1 dispatch bullet, and helper wiring while preserving INV-04 and INV-05.|COMP-001|FR-TU-1|CR-FM-01..03 and CR-TASK-01..03 accepted|M|Must|
|16|COMP-002|Critical/trivial path override component|Add adjacent pre-loop override section using critical globs `auth/ security/ crypto/ models/ migrations/` and trivial globs `*.md docs/ *test*.py`.|COMP-002|FR-TU-2|CR-TASK-01 accepted; sentinel present|S|Must|
|17|TEST-001|Row-1 call-order test|Add `tests/skills/task/test_row1_call_order.py::test_path_override_first` asserting AST/grep order for the three Gate 1 calls.|COMP-001, COMP-002|API-001..003|AC-ATK-01 pass|S|Must|
|18|TEST-005|Marker consumer closed-set test|Add `tests/audit/test_marker_consumers.py::test_closed_consumer_set` proving only `{CR-TASK-07 baseline-skip}` consumes item markers.|COMP-001|DM-002|AC-ATK-05 pass|S|Must|
|19|TEST-010|Pre-loop HALT policy test|Add input-invalid vs environment-non-ideal fixture: malformed Tier HALTs; git dirty warns and continues.|COMP-001|API-002|AC-ATK-10 pass|S|Must|
|20|TEST-013|Executable ordering grep|Add grep-level order check for `path_override_check`, `tier_field_validate`, and `gate_1_dispatch` at row-1.|COMP-001, COMP-002|API-001..003|AC-ATK-13 pass|S|Must|
|21|TEST-025|CR-FM-04 ordering audit|Add row-1 and row-10 ordering tests requiring 2 greps × 3 function names = 6 monotonic hits.|COMP-001, COMP-002|TEST-013|AC-SM-07 pass|S|Must|
|22|MIG-001|Step 1 foundation rollout|Execute M1 atomic foundation rollout with CR-FM-03 shim, canonicalization, helpers, sentinel, and 136+ in-flight resume check.|COMP-001, COMP-002|Rows 1-21|Step-1 gate exits 0; rollback is single revert|L|Must|

### Integration Points

|Surface|Integration Contract|Owner|Validation|
|---|---|---|---|
|`src/superclaude/skills/task/SKILL.md` F1 entry|Insert CR-7 sentinel and call order before any F1 item dispatch|Engineering Lead|AC-ATK-01, AC-SM-07|
|Task frontmatter parser|Read `Tier:` without mutating task files; default absent field to STANDARD|Engineering Lead|NFR-INV-4a fixture|
|Task Log / Notes|Append `gate-1:` and `path-override:` emissions without disrupting resume|Framework Maintainer|Resume parse test|
|Marker consumer register|Permit only CR-TASK-07 baseline-skip consumer until a new ME row exists|rf-qa Owner|TEST-005|

### Milestone Dependencies

- No earlier roadmap milestone blocks M1.
- M1 blocks all later milestones because every downstream transfer assumes the canonical tier enum and CR-7 ordering.
- M1 must land as an atomic source-tree change; splitting `Tier:` from Gate 1 violates ME-6.

### Open Questions

|ID|Decision Needed|Owner|Target|Roadmap Handling|
|---|---|---|---|---|
|OQ-TIER-VOCABULARY|Confirm canonical vocabulary `{STRICT, STANDARD, LIGHT, EXEMPT}` and retire `TRIVIAL`.|Engineering Lead|Before Step 1|Block enum fixtures until accepted.|
|OQ-FM-03-SUNSET|Confirm CR-FM-03 shim sunset rule, recommended `N=50 generations AND ≥90 days post Step 6 AND CR-MIGR-FM-03 authored`.|Engineering Lead|Before Step 1|Document as exit condition, not M1 blocker for initial ship.|
|Q-GATE-1-5-TOKEN-COLLISION|Pin grammar namespace for future `gate-1.5` subtypes.|Engineering Lead|Before M4|Track here because namespace choices interact with M1 emission grammar.|

### Risk Assessment

|Risk|Impact|Mitigation|Residual|
|---|---|---|---|
|CR-7 ordering drifts during edits|Gate 1 semantics invert, forcing wrong tier|Sentinel plus AST/grep checks|Low after TEST-001/013/025|
|Compatibility shim mutates old files|INV-04 regression|Read-only parser default; no file rewrite|Low|
|Marker becomes runtime dispatcher|INV-05 violation|Closed consumer register and ME review gate|Medium until TEST-005 is wired|

## M2: Verification and Pre-Flight Semantics

**Duration:** 4 days  
**Purpose:** Widen verification without displacing rf-qa, add environment-side pre-flight warnings, and pin the invariant rules that protect F1 progress and F2 additivity before TFEP transfer begins.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---:|---|---|---|---|---|---|---:|---|
|1|FR-CS-3|Path overrides and roster widening|Land TU-2 path overrides and TU-3 STRICT verification roster widening after M1 dispatch semantics are stable.|COMP-002, COMP-003|FR-CS-1, FR-CS-2|CR-FM-04 ordering plus ME-2 anchor check|M|Must|
|2|FR-TU-3|Gate-2 roster widening|Widen STRICT `verifier_roster` to `[rf-qa, quality-engineer]` while keeping `rf-qa` present at every existing invocation surface.|COMP-003|FR-TU-1|AC-ATK-11; AC-SM-02|M|Must|
|3|FR-TU-4|Git pre-flight matrix|Add Layer-2 git status pre-flight with states `{clean, dirty, tool-absent, not-a-repo, error-other}` and actions `{WARN-CONTINUE, GRACEFUL-SKIP}`; no HALT.|COMP-004|NFR-INV-1|AC-ATK-02; AC-ATK-10|M|Must|
|4|NFR-INV-2|F2 additivity guard|Protect the existing 10-entry F2 catalog from deletion, weakening, or narrowing before M3 adds three TFEP prohibitions.|COMP-006|M1|Prohibition additive test passes|S|Must|
|5|NFR-INV-3|rf-qa floor preservation|Guarantee `rf-qa` remains named at phase-gate, post-completion structural, post-completion qualitative, and future TFEP escalation surfaces.|COMP-003, COMP-007|FR-TU-3|AC-ATK-07/11|M|Must|
|6|NFR-ME-2|rf-qa supplemented only|Permit `quality-engineer` as an additive role but reject replacements or displacements of `rf-qa` in any widened roster.|COMP-003|NFR-INV-3|CR-TASK-05; AC-ATK-11|S|Must|
|7|NFR-ME-3|Side-channel no-HALT rule|Ensure TU-4 and later TFEP side effects do not introduce new environment-driven F1 HALT semantics.|COMP-004|NFR-INV-1|AC-ATK-02/10/18|S|Must|
|8|NFR-ME-5|No per-item execute substitution|Record D15b git pre-flight as accepted and D15c per-item execute synthesis as terminally rejected.|COMP-004|FR-TU-4|CR-TASK-06 acceptance|S|Must|
|9|API-010|rf-qa phase-gate surface|Preserve phase-gate `subagent_type: "rf-qa"`, output `${TASK_DIR}/reviews/qa-phase-[N]-report.md`, partitioning, and adversarial prompt envelope.|COMP-003|NFR-INV-3|Invocation grep ≥1|S|Must|
|10|API-011|rf-qa structural validation surface|Preserve post-completion structural rf-qa with `qa_phase="report-validation"`, output `${TASK_DIR}/reviews/qa-final-validation-report.md`, all-output consistency fields.|COMP-003|NFR-INV-3|Invocation grep ≥1|S|Must|
|11|API-012|rf-qa-qualitative operational surface|Preserve post-completion qualitative review with `qa_phase="task-qualitative"`, output `${TASK_DIR}/reviews/qa-qualitative-review.md`, target-file and 15-item checklist fields.|COMP-003|NFR-INV-3|Invocation grep ≥1|S|Must|
|12|COMP-003|Verification roster widening component|Add STRICT tier `quality-engineer` routing at phase gate and post-completion while keeping rf-qa floor and agent-list documentation.|COMP-003|FR-TU-3|CR-TASK-05 accepted|M|Must|
|13|COMP-004|Git pre-flight component|Add F1 pre-execution Task Log side-channel and helper for five git/environment states, all warning or graceful skip.|COMP-004|FR-TU-4|CR-TASK-06 accepted|M|Must|
|14|TEST-002|Git dirty dispatch matrix|Add `tests/skills/task/test_git_dirty_dispatch.py::test_5_row_matrix` parametrizing all five states with exact log line, action token, proceed sentinel, and no HALT.|COMP-004|FR-TU-4|AC-ATK-02 pass|S|Must|
|15|TEST-007|rf-qa chain verifier|Add `tests/audit/test_rf_qa_step6_gate.py::test_chain_links` verifying five chain anchors and rf-qa PASS before hard-delete.|COMP-003|NFR-INV-3|AC-ATK-07 pass|S|Must|
|16|TEST-011|ME-10 carve-out check|Add `tests/audit/test_me10_carve_out.py::test_me10_authored_or_annotated` to force ME-10 row or explicit one-time non-generalization annotation.|COMP-003, COMP-007|FR-TU-3|AC-ATK-11 pass|S|Must|
|17|TEST-020|Manifest exception traceability|Add `tests/audit/test_me_traceability.py::test_each_me_has_cr_row` requiring ME-1..ME-9 each map to at least one CR row.|COMP-001..008|NFR-ME-1..9|AC-SM-02 pass|S|Must|
|18|MIG-002|Step 2 rollout|Land STRICT roster widening, D15b git pre-flight, and `tier_preflight_git_status()` helper with fine-grained rollback.|COMP-003, COMP-004|MIG-001|AC-ATK-02/10 pass|M|Must|

### Integration Points

|Surface|Integration Contract|Owner|Validation|
|---|---|---|---|
|Phase-Gate QA block|Append `quality-engineer` only when STRICT while retaining rf-qa|rf-qa Owner|TEST-007, TEST-020|
|Post-completion validation|Keep structural and qualitative QA surfaces distinct and rf-qa-visible|rf-qa Owner|API-011/012 greps|
|F1 pre-execution|Write git status disposition as Task Log side-channel, never mid-loop HALT|Engineering Lead|TEST-002|
|F2 catalog guard|Freeze baseline 10-entry catalog before M3 additions|Engineering Lead|NFR-INV-2 audit|

### Milestone Dependencies

- M2 starts only after M1 establishes canonical tier dispatch.
- M2 must finish before M3 so TFEP escalation can rely on rf-qa floor rules and no-HALT side-channel discipline.
- M2 test additions are prerequisites for Step-3 and Step-6 safety gates.

### Open Questions

|ID|Decision Needed|Owner|Target|Roadmap Handling|
|---|---|---|---|---|
|OQ-F-05-MANIFESTIZATION|Decide whether F-05 fourth rf-qa invocation needs retroactive ME-10 or a one-time non-generalizing carve-out.|Engineering Lead|Before Step 4|TEST-011 blocks M3 TFEP escalation closure.|
|OQ-PROHIBITION-DISPOSITION-MATRIX|Decide verifier-spawned F1 disposition for AC-ATK-11 generalization.|Engineering Lead|Before Step 3|Feeds M3 TFEP prohibition rows.|

### Risk Assessment

|Risk|Impact|Mitigation|Residual|
|---|---|---|---|
|Roster widening accidentally replaces rf-qa|INV-03 violation|Content-keyed anchor and chain verifier|Low|
|Git dirty state becomes hard stop|INV-01 violation|Five-row matrix with proceed sentinel|Low|
|F2 baseline unclear before additions|Additivity audit becomes ambiguous|Freeze pre-merge count and test before M3|Medium until M3 donor diff fixtures land|

## M3: TFEP Core Transfer

**Duration:** 6 days  
**Purpose:** Transfer the donor TFEP semantics into `/task` as disk-resident, tier-gated, side-channel behavior: baseline capture, additive prohibitions, escalation routing, incident reporting, and donor literal audits.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---:|---|---|---|---|---|---|---:|---|
|1|FR-CS-4|Donor diff audit window|Run CR-TASK-12 seven-diff audit over six donor strings plus CR-7 sentinel block before donor removal work begins.|COMP-006..008|M2|Zero diff against `tests/fixtures/donor-blocks/`|M|Must|
|2|FR-TU-5|TFEP baseline YAML|Write `${TASK_DIR}/research/test-baseline.yaml` before F1 for STRICT/STANDARD tiers using `uv run pytest --collect-only -q` and persist across resume cycles.|COMP-005|M2|AC-ATK-03 four-state observer|M|Must|
|3|FR-TU-6|TFEP prohibitions and carve-outs|Add three VIOLATION-level prohibitions and three permitted exceptions to F2 without deleting any existing F2 entry; post-merge target count is 13.|COMP-006|NFR-INV-2|AC-ATK-11; CR-TASK-12|M|Must|
|4|FR-TU-7|TFEP escalation gradient|Route TFEP escalation to rf-qa as the fourth invocation point with six-step halt/freeze, context YAML, tier ladder, consume, tasklist insertion, and strict resume flow.|COMP-007|NFR-INV-3, NFR-ME-2|AC-ATK-11; AC-SM-02|L|Must|
|5|FR-TU-8|TFEP incident report file|Write `${TASK_DIR}/research/tfep-incident-report.md` as a side-effect file with seven donor fields and outcome enum `{success, escalated, failed}`; never add an in-task heading.|COMP-008|FR-TU-7|AC-ATK-12(b); AC-SM-04|M|Must|
|6|NFR-ME-4|Tier-gated baseline|Run baseline capture only for STRICT/STANDARD; skip LIGHT/EXEMPT without per-row deltas.|COMP-005|FR-TU-5|CR-TASK-07 accepted|S|Must|
|7|NFR-ME-9|Donor ceremony drop audit|Keep ten donor ceremony drops dropped while preserving surviving citations only through authorized CR-DEP-06 dispositions.|COMP-006..008|FR-CS-4|CR-DEP-01/05; R-RULE-11|M|Must|
|8|DM-003|TFEP baseline schema|Define baseline fields: storage=`${TASK_DIR}/research/test-baseline.yaml`; cardinality=0..1; tiers=STRICT/STANDARD; emission=pre-F1; procedure=`uv run pytest --collect-only -q` and `uv run pytest --tb=no -q`; persistence=disk; schema_version=1; captured_at=ISO-8601 UTC; tier enum={STRICT,STANDARD}; tests=list `{test_id,status}`; status enum={passing,failing}; observation order=exists→getsize→safe_load→schema; retention=task lifetime.|COMP-005|FR-TU-5|All fields asserted|M|Must|
|9|DM-004|TFEP incident schema|Define incident fields: storage=`${TASK_DIR}/research/tfep-incident-report.md`; cardinality=0..1; tier=STRICT post-fire; emission=post-completion; trigger=STRICT plus TFEP fired plus resolved; fields=`Trigger`, `Escalation count`, `Failing tests`, `Root cause`, `Solution`, `Outcome`, `Forensic artifacts`; outcome enum={success,escalated,failed}; constraints=no LIGHT/EXEMPT/STANDARD-no-fire, no mid-loop write, no enum drift.|COMP-008|FR-TU-8|Seven-field fixture passes|M|Must|
|10|API-013|Mid-phase TFEP rf-qa API|Add rf-qa invocation #4 with `qa_phase="tfep-incident-[N]"`, output `${TASK_DIR}/reviews/qa-tfep-incident-[N]-report.md`, trigger classification, baseline diff, failing tests, and escalation stage.|COMP-007|FR-TU-7|Authoritative count=4|M|Must|
|11|COMP-005|Baseline snapshot component|Add pre-F1 disk emitter and session-resumption read path for `test-baseline.yaml`, preserving INV-04.|COMP-005|FR-TU-5|CR-TASK-07 accepted|M|Must|
|12|COMP-006|Prohibition and carve-out component|Append three donor prohibitions and a carve-out subsection after F2, preserving INV-02 and INV-01.|COMP-006|FR-TU-6|CR-TASK-08/12 accepted|M|Must|
|13|COMP-007|Escalation trigger component|Add TFEP escalation router as F1 side-channel with fourth rf-qa surface and one-time non-generalization annotation if ME-10 is not authored.|COMP-007|FR-TU-7|CR-TASK-09 accepted|L|Must|
|14|COMP-008|Incident report component|Add markdown side-effect writer for seven-field incident report and literal outcome enum preservation.|COMP-008|FR-TU-8|CR-TASK-10/12 accepted|M|Must|
|15|TEST-003|Baseline observer test|Add `tests/skills/task/test_baseline_trinary.py::test_4_state_observer` covering absent, empty, parse-fail, schema-fail in canonical observation order.|COMP-005|DM-003|AC-ATK-03 pass|S|Must|
|16|TEST-006|Seven donor zero-diffs|Add `tests/skills/task/test_cr_task_12_donor_diffs.py::test_seven_zero_diffs` with seven fixture comparisons under `tests/fixtures/donor-blocks/`.|COMP-006..008|FR-CS-4|AC-ATK-06 pass|M|Must|
|17|TEST-009|sha256 digest audit|Add `tests/skills/task/test_cr_task_11_digest.py::test_sha256_matches_baseline` proving digest baselines use sha256, not md5.|COMP-006..008|FR-CS-4|AC-ATK-09 pass|S|Must|
|18|TEST-012|Incident schema and enum test|Add incident report fixture plus canonical enum test proving seven fields and tier enum `{STRICT, STANDARD, LIGHT, EXEMPT}`.|COMP-008|DM-004|AC-ATK-12 pass|S|Must|
|19|TEST-019|V/C/K byte-match audit|Add `tests/audit/test_vck_verdicts.py::test_transfer_manifest_byte_match` asserting 8/8 transfer verdicts match the manifest.|COMP-001..008|FR-TU-1..8|AC-SM-01 pass|S|Must|
|20|TEST-022|F-finding anchor audit|Add `tests/audit/test_f_findings_cite_anchors.py::test_each_f_row_has_artifact_anchor` requiring valid line-range cite for F-01..F-08.|COMP-001..008|FR-TU-1..8|AC-SM-04 pass|S|Must|
|21|TEST-026|CR-TASK-12 full audit|Add `tests/skills/task/test_cr_task_12_donor_diffs.py::test_6_donor_plus_1_sentinel` asserting six donor diffs plus sentinel diff return zero.|COMP-006..008|TEST-006|AC-SM-08 pass|S|Must|
|22|MIG-003|Step 3 TFEP rollout|Land TFEP baseline, prohibitions, carve-outs, escalation, incident report, and CR-TASK-07..10 after R-DRIFT-03 patch precondition.|COMP-005..008|MIG-002|AC-ATK-03/12 pass|L|Must|
|23|MIG-004|Step 4 donor audit rollout|Land donor fixture snapshot and seven-diff audit window after R-DRIFT-02 patch precondition.|COMP-006..008|MIG-003|AC-SM-08 pass|M|Must|

### Integration Points

|Surface|Integration Contract|Owner|Validation|
|---|---|---|---|
|First Item Protocol|Capture baseline YAML before F1 for STRICT/STANDARD only|Engineering Lead|TEST-003|
|F2 catalog|Append prohibitions and carve-outs; never weaken existing entries|Engineering Lead|NFR-INV-2, TEST-006|
|TFEP escalation router|Invoke rf-qa mid-phase as fourth surface using forensic context|rf-qa Owner|API-013, TEST-011|
|Post-completion validation|Write incident report file only after resolved STRICT TFEP escalation|rf-qa Owner|TEST-012|
|Donor fixture corpus|Freeze literal donor strings for byte-preservation audit|Documentation/Release Owner|TEST-006/026|

### Milestone Dependencies

- M3 depends on M2's rf-qa floor and side-channel no-HALT rules.
- M3 donor diff fixtures must land before M4 donor deletion.
- R-DRIFT-03 must be patched before Step 3; R-DRIFT-02 must be patched before Step 4.

### Open Questions

|ID|Decision Needed|Owner|Target|Roadmap Handling|
|---|---|---|---|---|
|OQ-TFEP-FIELD-COUNT|Resolve 6-vs-7 field incident-report cardinality; roadmap uses seven fields from Schema 4.|Engineering Lead|Before Step 4|Blocks TEST-012 final assertion if not accepted.|
|Q-R-DRIFT-02|Patch donor anchor `:127-135` → `:133-135` in three artifacts plus CR-TASK-12 anchors.|Documentation/Release Owner|Before Step 4|Precondition for MIG-004.|
|Q-R-DRIFT-03|Patch donor anchor `:200-210` → `:157-161` in three artifacts plus CR-TASK-12 anchors.|Documentation/Release Owner|Before Step 3|Precondition for MIG-003.|
|Q-GAP-05|Decide helper-module boundaries for TFEP baseline and incident writer.|Engineering Lead|Before implementation|Use smallest direct helpers that tests can import.|
|Q-GAP-09|Align incident-report template form with donor field names and outcome enum.|rf-qa Owner|Before Step 4|Fold into DM-004 fixture.|

### Risk Assessment

|Risk|Impact|Mitigation|Residual|
|---|---|---|---|
|Baseline stays in memory|INV-04 resume loss|Disk-resident YAML and resume read path|Low|
|Donor strings drift during transfer|AC-SM-08 failure|Seven frozen fixture diffs|Low after TEST-006/026|
|TFEP escalation floods rf-qa|Queue saturation|Reactive refusal threshold after telemetry; exact incident context|Medium|
|Incident report field mismatch|Forensic artifact invalid|Seven-field schema test and enum test|Low|

## M4: CLI Integration and Donor Deprecation

**Duration:** 6 days  
**Purpose:** Move runtime emissions to `/task`, enforce atomic Step-5/Step-6 boundaries, remove the donor skill as a live surface, protect in-flight resumability, and prove residual references are authorized or eliminated.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---:|---|---|---|---|---|---|---:|---|
|1|FR-CS-5|Step-5 soft-deprecation boundary|Atomically reroute donor command facade, sha256 baseline, CLI residual grep, docs redirect, sprint CLI reroutes, and sprint TUI reroute after S-1 discharge.|API-004..009, API-014|MIG-004, S-1|AC-ATK-15/17; AC-SM-09|L|Must|
|2|FR-CS-6|Step-6 hard-delete boundary|Atomically remove donor SKILL.md, enforce directory absence, run sync rule, and require rf-qa F-07 chain verifier before deletion lands.|API-014|FR-CS-5|AC-ATK-07; `make verify-sync` 0|L|Must|
|3|FR-CS-7|Sprint and pipeline fix-up|Ensure no runtime caller emits `/sc:task` after Step 5 across sprint and cleanup-audit prompt builders.|API-004..009|FR-CS-5|pytest pass; AC-ATK-17 active|M|Must|
|4|FR-CR-DEP-06|Residual manifest|Write `${RELEASE_DIR}/cr-dep-06-residual-manifest.{md,yaml}` after Step 6, enumerate all surviving deprecation-surface strings, and require zero residuals outside authorized buckets.|API-004..014|FR-CS-6|AC-ATK-18(d); CR-DEP-05 grep|M|Must|
|5|NFR-INV-4b|Semantic resumability|Detect deprecated surface references inside in-flight checklist bodies, emit Gate-1.5 token, require one-shot ack, and continue execution without HALT.|DM-005|M1, FR-CR-DEP-06|AC-ATK-18(a-d)|L|Must|
|6|NFR-S-1|In-flight discharge|Complete or snapshot-freeze any in-flight PRD/TDD task body referencing donor surfaces before Step 5; default max wait 14 days.|DM-005|M3|AC-ATK-08|M|Must|
|7|NFR-S-2|CLI runtime atomicity|Ensure Step-5 command facade and CLI fix-forward land atomically; server-side push policy rejects rebase-split intermediate states.|API-004..009, API-014|FR-CS-5|AC-ATK-17|M|Must|
|8|NFR-S-3|Sync rule atomicity|Protect `make sync-dev` and `make verify-sync` with exclusive `flock` on `.claude/skills/.sync-lock` to avoid prune/copy races.|API-014|FR-CS-6|AC-ATK-16; 0 flakes ×30|M|Must|
|9|DM-005|Gate-1.5 emission schema|Define emission fields: storage=Task Log lines; cardinality=0..N per resume; variants=`legacy-surface-reference` and `deleted-related-doc`; legacy byte form=`gate-1.5: legacy-surface-reference detected file=<path> action=warn-and-continue surface=<symbol>`; surface enum={/sc:task,sc-task-protocol,task-unified}; related-doc byte form=`gate-1.5: deleted-related-doc file=<path> action=warn-and-continue referenced_from=<path>`; layers=parse/content/reference; ack=`gate-1.5: ack received user=<id> ts=<ISO-8601>`; constraints=no HALT/no migration/no Tier bundle/no silent sunset.|DM-005|NFR-INV-4b|All fields asserted|M|Must|
|10|API-004|Sprint process emission reroute|Change sprint phase prompt from `/sc:task Execute all tasks in @...` to `/task Execute all tasks in @...` and assert no `/sc:task` remains in rendered prompt.|API-004|FR-CS-5|AC-ATK-17 boundary assertion|S|Must|
|11|API-005|Cleanup surface scan reroute|Change `build_surface_scan_prompt` emission to `/task Perform a surface-level scan ...` for G-001.|API-005|FR-CS-5|CLI grep clean|S|Must|
|12|API-006|Cleanup structural analysis reroute|Change `build_structural_analysis_prompt` emission to `/task Perform deep structural analysis ...` for G-002/G-003.|API-006|FR-CS-5|CLI grep clean|S|Must|
|13|API-007|Cleanup cross-cutting reroute|Change `build_cross_cutting_prompt` emission to `/task Detect duplication, sprawl, and consolidation ...` for G-004.|API-007|FR-CS-5|CLI grep clean|S|Must|
|14|API-008|Cleanup consolidation reroute|Change `build_consolidation_prompt` emission to `/task Consolidate audit findings ...` for G-005.|API-008|FR-CS-5|CLI grep clean|S|Must|
|15|API-009|Cleanup validation reroute|Change `build_validation_prompt` emission to `/task Validate audit findings ...` for G-006.|API-009|FR-CS-5|CLI grep clean|S|Must|
|16|API-014|Donor command facade deprecation|Change command skill target from `Skill sc:task-protocol` to `Skill task`, rewrite eight adjacent brand occurrences, and preserve `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` tokens as semantic fixtures.|API-014|FR-CS-5|CR-DEP-01; sha256 baseline|M|Must|
|17|TEST-008|Git SHA embedding test|Add `tests/scripts/test_embed_git_sha.py::test_idempotent` plus CR-DEP-05 stale verification requiring `[CODE-VERIFIED]` tags to carry 40-char SHA suffix.|API-004..014|NFR-S-1|AC-ATK-08 pass|S|Must|
|18|TEST-014|CR-DEP-05 grep test|Add `tests/audit/test_cr_dep_05_grep.py::test_4_sub_resolutions` for grep scope, cluster root, Step-6 gate, and CR-DOC-13 widening.|API-004..014|FR-CR-DEP-06|AC-ATK-14 pass|S|Must|
|19|TEST-015|Step-5 docs atomicity test|Add `tests/audit/test_cr_doc_01_step.py::test_landed_with_dep_01` requiring command facade and user docs rewrite in same Step-5 roster.|API-014|FR-CS-5|AC-ATK-15 pass|S|Must|
|20|TEST-016|sync-dev flock test|Add `tests/audit/test_make_sync_dev_flock.py::test_concurrent_worktree` running two parallel sync operations and verifying post-prune tree parity.|API-014|NFR-S-3|AC-ATK-16 pass|M|Must|
|21|TEST-017|Server-side hook test|Add `tests/ci/test_pre_receive_hook.py::test_rebase_split_rejected` fabricating a split commit pair and requiring hook rejection.|API-004..014|NFR-S-2|AC-ATK-17 pass|M|Must|
|22|TEST-018|Resume and manifest test|Add Gate-1.5 token, sprint-emit block, and CR-DEP-06 manifest tests proving resume content audit and ≥144 residual enumeration.|DM-005|NFR-INV-4b, FR-CR-DEP-06|AC-ATK-18 pass|M|Must|
|23|TEST-023|S-constraint hazard audit|Add tests proving S-1 cites HZ-03, S-2 cites HZ-06/HZ-07, and S-3 cites HZ-14.|NFR-S-1..3|NFR-S-1..3|AC-SM-05 pass|S|Must|
|24|TEST-027|Step-5 roster equality|Add `tests/audit/test_step_5_commit_roster.py::test_exact_file_list` checking Step-5 commit files equal final merge roster.|API-004..014|FR-CS-5|AC-SM-09 pass|S|Must|
|25|TEST-028|Step-6 roster equality|Add `tests/audit/test_step_6_commit_roster.py::test_exact_file_list` checking Step-6 commit files equal hard-delete roster.|API-014|FR-CS-6|AC-SM-10 pass|S|Must|
|26|TEST-029|Rejected ledger reintroduction test|Add `tests/audit/test_no_rejected_re_proposal.py::test_zero_ledger_re_introductions` proving LR-REJECT-* patterns are not re-proposed.|API-014|NFR-ME-9|AC-SM-11 pass|S|Must|
|27|TEST-030|Step gates and live resume test|Add gate tests for Steps 1/5/6 plus live in-flight MDTM resume fixture using current file count, not a fixed historical count.|DM-005|NFR-INV-4b|AC-SM-12 pass|M|Must|
|28|MIG-005|Step 5 soft-deprecation rollout|Land command facade change, CLI reroutes, residual grep, docs redirect, condensation table, and in-flight freeze as one atomic Step-5 change.|API-004..009, API-014|MIG-004, NFR-S-1|AC-ATK-15/17; AC-SM-09|L|Must|
|29|MIG-006|Step 6 hard-delete rollout|Remove donor skill from source and dev copies, prune with sync-dev, write CR-DEP-06 manifest, and prefer roll-forward after this destructive boundary.|API-014|MIG-005|AC-SM-10; verify-sync 0|L|Must|
|30|MIG-007|Step 7 invariant walkthrough|Run invariant re-read, F-row anchor audit, and R-DOC-01 content-audit downgrade after donor removal.|COMP-001..008|MIG-006|AC-SM-03/04 pass|M|Must|

### Integration Points

|Surface|Integration Contract|Owner|Validation|
|---|---|---|---|
|`src/superclaude/cli/sprint/process.py`|Emit `/task` at sprint runtime boundary and block legacy content matches|Engineering Lead|TEST-018|
|`src/superclaude/cli/cleanup_audit/prompts.py`|Reroute five prompt builders from `/sc:task` to `/task`|Engineering Lead|API-005..009 greps|
|`src/superclaude/commands/task.md`|Point command facade at `Skill task` and preserve classification HTML markers|Framework Maintainer|API-014, TEST-015|
|`make sync-dev` / `make verify-sync`|Use exclusive lock around source-to-dev skill sync and prune|DevOps|TEST-016|
|Server-side push policy|Reject split commits that expose broken Step-5 or Step-6 intermediate state|DevOps|TEST-017|
|CR-DEP-06 manifest|Archive residual dispositions and require zero violations outside authorized buckets|Documentation/Release Owner|TEST-018|

### Milestone Dependencies

- M4 cannot begin Step-5 until S-1 in-flight discharge or snapshot-freeze is complete.
- M4 Step-6 cannot begin until Step-5 landed atomically and M3 donor fixtures pass.
- M4 must finish before M5 can claim command-surface and maintenance-surface KPIs.

### Open Questions

|ID|Decision Needed|Owner|Target|Roadmap Handling|
|---|---|---|---|---|
|OQ-F-NN-BIJECTION|Confirm canonical F-NN ↔ TU-NN bijection once final content audit completes.|Engineering Lead|Before Step 7|Blocks MIG-007 closure.|
|Q-R-DOC-01|Downgrade artifact gap flags to content-verification owed and propagate to AC-SM status fields.|Documentation/Release Owner|Before Step 7|Handled in MIG-007.|
|Q-GAP-04|Document `flock` portability for macOS/BSD or supported fallback.|DevOps|Before Step 6|Blocks TEST-016 portability acceptance.|
|Q-GAP-08|Finalize condensation table location and contents for Step-5 docs atomicity.|Documentation/Release Owner|Before Step 5|Feeds MIG-005.|
|Q-GAP-10|Choose ack persistence shape for Gate-1.5 one-shot acknowledgment.|Engineering Lead|Before Step 5|Feeds DM-005 and TEST-018.|
|Q-GAP-12|Standardize schema version fields across residual manifest and TFEP artifacts.|Engineering Lead|Before Step 6|Feeds CR-DEP-06 manifest.|

### Risk Assessment

|Risk|Impact|Mitigation|Residual|
|---|---|---|---|
|Step-5 split by rebase|Broken runtime emits legacy command|Server-side hook and roster equality|Low after TEST-017/027|
|In-flight task blocked by legacy body text|INV-04 semantic failure|Gate-1.5 warn-and-continue plus ack|Medium due live population|
|sync-dev race overwrites skill copy|Source/dev divergence|flock and concurrent fixture|Medium until platform fallback accepted|
|Residual references misunderstood as violations|Unnecessary churn or missed real violation|Bucketed manifest with per-string disposition|Low|

## M5: Production Readiness and Audit Closure

**Duration:** 4 days  
**Purpose:** Close documentation, deferred regeneration, operational runbooks, KPI validation, and final audit evidence after the live donor surface has been removed.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---:|---|---|---|---|---|---|---:|---|
|1|FR-CS-8|Documentation rollup|Run docs rollup, CR-DOC-13 R-RULE-11 audit, and mkdocs build with zero broken-link warnings; use hot-fix fallback only with explicit authorization flag.|Docs|MIG-006|mkdocs build clean|M|Must|
|2|FR-CS-9|Leave-as-is enforcement|Enforce authorized buckets A/C/D/E/F/G/H, scope CR-REF-12 to `src` and `.claude`, and check cluster roots for deprecation notes.|Docs, Audit|FR-CR-DEP-06|Bucket audit clean|M|Must|
|3|FR-CS-10|Deferred regeneration banners|Add frozen-pre-merge banner to `docs/generated/*` files that retain `/sc:task` or `sc-task-protocol` until regeneration is scheduled.|Docs|FR-CS-9|Banner grep clean|S|Must|
|4|NFR-ME-7|D08 deferred invariant|Keep D08 terminally deferred until parser ships; do not reopen during the merge.|Governance|M4|Ledger audit clean|S|Must|
|5|NFR-ME-8|D01 deferred invariant|Keep D01 terminally deferred until loader semantics and Rule 6 split are ready; do not bundle into this merge.|Governance|M4|Ledger audit clean|S|Must|
|6|TEST-004|Condensation table audit|Add `tests/audit/test_condensation_table.py::test_79_to_67_to_65` proving bucket math: 79 row-instances → 65 distinct CR-IDs → 67 PASS-line-items.|Docs, Audit|MIG-005|AC-ATK-04 pass|S|Must|
|7|TEST-021|Invariant walkthrough audit|Add `tests/audit/test_invariant_walkthrough.py::test_inv_1_through_5_re_readable` proving all five invariants have worked-example anchors.|Docs, Audit|MIG-007|AC-SM-03 pass|S|Must|
|8|TEST-024|Row and step count audit|Add `tests/audit/test_row_and_step_counts.py::test_67_rows_in_master` and `test_10_steps_in_sequence`.|Docs, Audit|MIG-010|AC-SM-06 pass|S|Must|
|9|MIG-008|Step 8 docs rollout|Land CR-DOC-02..09, CR-DOC-11 partial, mkdocs build gate, and CR-DOC-13 R-RULE-11 audit; pin mkdocs version before gate.|Docs|MIG-007|Zero broken-link warnings|M|Must|
|10|MIG-009|Step 9 residual manifest finalization|Finalize the one-shot residual-reference manifest and close AC-ATK-18(d) evidence.|Docs, Audit|MIG-006|Manifest archived and clean|S|Must|
|11|MIG-010|Step 10 audit closure|Run final docs, deferred ack, AC-SM-01..12 audits from clean checkout, and K-01..K-08 baseline measurement.|Docs, Audit|MIG-008, MIG-009|All audits green|M|Must|
|12|OPS-001|Critical path override runbook|Document symptoms, diagnosis, resolution, escalation, and prevention for STRICT override when critical paths conflict with LIGHT/EXEMPT author intent.|COMP-002|MIG-001|Runbook review pass|S|Must|
|13|OPS-002|Gate-1.5 triage runbook|Document canonical Gate-1.5 token triage, ack flow, residual disposition lookup, and no-HALT rule for resume matches.|DM-005|MIG-006|Runbook review pass|S|Must|
|14|OPS-003|Tier misclassification runbook|Document fallback inspection order, expected vs actual dispatch comparison, incident file use, and parser bug escalation.|COMP-001|MIG-001|Runbook review pass|S|Must|
|15|OPS-004|TFEP escalation runbook|Document baseline read, incident report inspection, carve-out classification, rf-qa escalation, and schema-drift prevention.|COMP-005..008|MIG-003|Runbook review pass|S|Must|
|16|OPS-005|In-flight resume triage runbook|Document CR-FM-03 default, Gate-1.5 body grep, related_docs ENOENT traversal, warn-and-continue resolution, and Engineering Lead escalation.|DM-005|MIG-006|Runbook review pass|S|Must|

### Integration Points

|Surface|Integration Contract|Owner|Validation|
|---|---|---|---|
|Documentation build|Run `mkdocs build` after command docs and generated-doc banners settle|Documentation/Release Owner|FR-CS-8, MIG-008|
|Audit corpus|Run AC-SM and AC-ATK closure from a clean checkout|rf-qa Owner|MIG-010|
|Operational runbooks|Publish five runbooks covering override, Gate-1.5, tier mismatch, TFEP, and resume triage|Framework Maintainer|OPS-001..005|
|Deferred ledgers|Preserve D08/D01 terminal deferrals and rejected-pattern boundaries|Engineering Lead|NFR-ME-7/8, TEST-029|

### Milestone Dependencies

- M5 starts after M4 proves the live donor surface is removed and residual manifest exists.
- M5 cannot close KPIs until M1-M4 tests pass from a clean checkout.
- M5 documentation output must match runtime behavior after Step 6, not pre-merge donor semantics.

### Open Questions

|ID|Decision Needed|Owner|Target|Roadmap Handling|
|---|---|---|---|---|
|Q-GAP-01..12|Close or explicitly defer remaining research gaps: cleanup_audit tests, HTML-vs-shell sentinel form, non-generalization audit, flock portability, helper modules, donor fixtures, condensation table, hook hosting, incident template, ack shape, schema versions.|Engineering Lead|Before Step 10|Track as M5 closure checklist; items with implementation impact remain tied to M1-M4 rows.|
|Q-GATE-1-5-SCHEMA|Confirm `deleted-related-doc` is a Schema 5 variant, not a sixth canonical schema.|Engineering Lead|Before docs rollup|Roadmap treats it as DM-005 Variant B.|

### Risk Assessment

|Risk|Impact|Mitigation|Residual|
|---|---|---|---|
|Docs describe removed donor as live|Users re-enter `/sc:task` path|Docs rollup plus residual grep|Low|
|Generated docs retain legacy text without context|False residual alarm|Frozen-pre-merge banner and bucket disposition|Low|
|Runbooks miss INV-04 edge cases|Operators halt in-flight resumes|OPS-002 and OPS-005 cover no-HALT triage|Medium|
|Audit closure depends on local-only state|CI/local divergence|Clean checkout run and pinned environment variables|Medium|

## Resource Requirements and Dependencies

### People and Ownership

|Role|Primary Responsibilities|Milestones|
|---|---|---|
|Engineering Lead|CR-7 ordering, tier parser, helper functions, CLI reroutes, Step-5/6 atomicity, final technical acceptance|M1-M5|
|rf-qa Owner|rf-qa floor preservation, TFEP escalation review, chain verifier, final AC-SM/AC-ATK audit|M2-M5|
|Documentation/Release Owner|Donor diff fixtures, command docs, mkdocs build, generated-doc banners, CR-DEP-06 manifest archive|M3-M5|
|DevOps|Server-side push policy, sync-dev flock portability, CI clean-checkout execution|M4-M5|
|Framework Maintainer|Runbooks, user-facing command surface, deferred ledger discipline, release readiness signoff|M4-M5|

### External Dependencies

|Dependency|Use|Constraint|
|---|---|---|
|`git`|Pre-flight checks, Step-5/6 commit and manifest gates|Warn/skip only for runtime non-ideal states; CI gate requires availability|
|`uv`|All Python execution and pytest commands|Never use bare `python -m`, `pip`, or `python script.py`|
|`pytest`|Unit, integration, AC-ATK, AC-SM, clean-checkout gates|Run through `uv run pytest`|
|`pyyaml`|Frontmatter, baseline YAML, manifest parsing|Observation order pinned for baseline files|
|`click` and `rich`|CLI prompt generation and rendering|Keep command output stable for grep fixtures|
|`mkdocs`|Documentation build gate|Pin version before M5 docs rollout|
|`flock` / POSIX locking|sync-dev and verify-sync race prevention|Document macOS/BSD fallback before Step 6|
|`sha256sum` or `shasum -a 256`|Command facade digest baseline|md5 digests are rejected|

### Internal Dependencies

|Internal Surface|Use|Milestone|
|---|---|---|
|`src/superclaude/skills/task/SKILL.md`|Recipient merge target for F1/F2/rf-qa/TFEP semantics|M1-M3|
|`src/superclaude/skills/sc-task-protocol/SKILL.md`|Donor literal source and deletion target|M3-M4|
|`src/superclaude/commands/task.md`|Command facade deprecation surface|M4|
|`src/superclaude/cli/sprint/process.py`|Sprint runtime `/task` prompt emission|M4|
|`src/superclaude/cli/cleanup_audit/prompts.py`|Five cleanup-audit prompt emissions|M4|
|`Makefile`|sync-dev, verify-sync, flock integration|M4|
|`.github/workflows/pre-receive-cli-atomicity.yml` or equivalent|Server-side atomicity enforcement|M4|
|`docs/generated/*`|Deferred regeneration banner and authorized residual bucket|M5|
|`.dev/tasks/to-do/*` and `.dev/tasks/done/*`|In-flight and archived MDTM resume population|M1, M4|

## Risk Register

|ID|Risk|Severity|Milestone|Mitigation|Owner|
|---|---|---|---|---|---|
|R-RES-01|Tier-conditioned read boundary is mistaken for per-item dispatch|Medium|M1|Closed marker consumer register and ME review gate|Engineering Lead|
|R-RES-02|Fourth rf-qa invocation widens INV-03 surface without manifest treatment|Medium|M2-M3|ME-10 or one-time non-generalization annotation|rf-qa Owner|
|R-RES-03|TFEP escalation over-escalates without queue bound|Medium|M3|Telemetry and reactive refusal threshold|rf-qa Owner|
|R-RES-04|S-1 wait/snapshot carrier surface remains ambiguous|Medium|M4|AC-ATK-08 disposition before Step 5|Engineering Lead|
|R-RES-05|F-07 chain is procedural but not binding|Low|M4|rf-qa F-07 chain verifier before hard-delete|rf-qa Owner|
|R-ATK-01|Markdown-only CR-7 discipline is weak|Medium|M1|Sentinel plus AST-grade grep|Engineering Lead|
|R-ATK-06|Line-number anchors drift|Medium|M1-M5|Content-keyed anchors and CR-FM-04 extension|Documentation/Release Owner|
|R-ATK-16|sync-dev worktree race|High|M4|Exclusive flock and concurrent fixture|DevOps|
|R-ATK-17|Local pre-push bypass via `--no-verify`|High|M4|Server-side push policy|DevOps|
|R-DRIFT-02|Donor anchor off by two lines|Low|M3|Patch anchors before Step 4|Documentation/Release Owner|
|R-DRIFT-03|Donor escalation anchor off by 43 lines|Medium|M3|Patch anchors before Step 3|Documentation/Release Owner|
|R-FM-01|Symlink defeats verify-sync|Low/High|M4|Pre-Step-6 `find -type l` audit|DevOps|
|R-FM-02|Step-5 pytest flakes without progress|Medium|M4|Pin env vars and CI signoff|DevOps|
|R-FM-03|Parallel subagent conflicts on `task/SKILL.md`|Medium|M4|Ban parallel dispatch on that file during Step 5|Engineering Lead|
|R-FM-04|CI/local environment divergence|Medium|M4-M5|Pin PYTHONHASHSEED, locale, timezone|DevOps|
|R-FM-05|mkdocs version drift|Medium|M5|Pin mkdocs before docs gate|Documentation/Release Owner|
|R-FM-06|Generated docs regeneration unscheduled|Medium|M5|Banner and CR-DEP-06 weekly archive|Documentation/Release Owner|
|R-FM-07|UTF-16 grep evasion|Low|M4|Surface as audit gap and extend grep if needed|Engineering Lead|
|R-FM-08|Donor rename evades file absence check|Low|M4|Enforce directory absence, not only file absence|Engineering Lead|
|R-OPS-02|Manual operator intervention needed for H-4 resume|Medium|M4-M5|Runbook plus pre-flagged at-risk task IDs|Framework Maintainer|
|Q-GAP-04|`flock` portability uncertain on macOS/BSD|Medium|M4|Document fallback before Step 6|DevOps|

## Success Criteria and Validation Approach

|Criterion|Target|Validation Method|Milestone|
|---|---|---|---|
|KPI-01 / AC-SM-01|8/8 TU verdicts byte-identical|`tests/audit/test_vck_verdicts.py::test_transfer_manifest_byte_match`|M3|
|KPI-02 / AC-SM-02|9/9 ME rows trace to at least one CR row|`tests/audit/test_me_traceability.py`|M2|
|KPI-03 / AC-SM-03|5/5 invariants re-readable with worked example|`tests/audit/test_invariant_walkthrough.py`|M5|
|KPI-04 / AC-SM-04|8/8 F-rows cite valid anchors|`tests/audit/test_f_findings_cite_anchors.py`|M3/M4|
|KPI-05 / AC-SM-05|3/3 S-rows cite named hazards|`tests/audit/test_s_constraints_cite_hz.py`|M4|
|KPI-06 / AC-SM-06|67 row-line-items and 10 commit steps|`tests/audit/test_row_and_step_counts.py`|M5|
|KPI-07 / AC-SM-07|2 greps × 3 names = 6 monotonic hits|`tests/skills/task/test_cr_fm_04_ordering.py`|M1|
|KPI-08 / AC-SM-08|7/7 donor/sentinel diffs return zero|`tests/skills/task/test_cr_task_12_donor_diffs.py`|M3|
|KPI-09 / AC-SM-09|Step-5 commit roster exact-match|`tests/audit/test_step_5_commit_roster.py`|M4|
|KPI-10 / AC-SM-10|Step-6 commit roster exact-match|`tests/audit/test_step_6_commit_roster.py`|M4|
|KPI-11 / AC-SM-11|Zero rejected-ledger re-proposals|`tests/audit/test_no_rejected_re_proposal.py`|M4|
|KPI-12 / AC-SM-12|100% live in-flight resume plus Steps 1/5/6 gates exit 0|`tests/audit/test_step_gates.py` and live resume fixture|M4|
|KPI-13 / K-01|0 AC-ATK-01..18 open or partial|Full AC-ATK audit suite|M5|
|KPI-14 / K-02|100% sprint-runner pytest pass rate|`uv run pytest tests/cli/`|M4|
|KPI-15 / K-03|144 → 0 residuals outside authorized buckets|CR-DEP-06 manifest and grep audit|M4|
|KPI-16 / K-04|0 verify-sync flakes across 30 CI runs|Flock concurrency CI fixture|M4/M5|
|KPI-17 / K-05|100% PASS across 33 spec-named CR rows|Post-Step-6 audit pass|M5|
|KPI-18 / K-06|Donor SKILL.md absent from source and dev copies|Directory absence audit|M4|
|KPI-19 / K-07|Visible command + skill surface count 2 → 1|Command/skill inventory check|M5|
|KPI-20 / K-08|Maintenance surface-pair count 2 → 1|Maintenance inventory check|M5|

Validation rules:
- All Python validation uses UV, for example `uv run pytest`, never bare Python or pip.
- Clean-checkout validation is required for final M5 signoff.
- `rf-qa` is part of validation evidence, not an optional reviewer.
- No revenue, conversion, PII, PHI, GDPR, CCPA, HIPAA, SOC2, or PCI-DSS success metric applies to this internal framework feature.

## Decision Summary

|Decision|Chosen Direction|Rationale|Impacted Milestones|
|---|---|---|---|
|Roadmap phasing|Technical-layer milestones with TDD step mapping|Keeps architectural dependencies visible while preserving ten-step rollout gates|All|
|Canonical tier enum|`STRICT`, `STANDARD`, `LIGHT`, `EXEMPT`|Matches extraction/TDD canonical table and rejects `TRIVIAL`|M1|
|Gate 1 order|`path_override_check` → `tier_field_validate` → `gate_1_dispatch`|CR-7 load-bearing order protects critical path override and compatibility shim|M1|
|Per-item markers|Read-only metadata with closed consumer register|Preserves INV-05 refusal-of-definition|M1|
|rf-qa posture|Supplement, never replace|Preserves INV-03 and ME-2 across four invocation surfaces|M2-M5|
|TFEP baseline|Disk-resident YAML for STRICT/STANDARD only|Preserves INV-04 resumability and ME-4 tier gate|M3|
|Incident report|Seven-field side-effect file with donor outcome enum|Preserves donor literal semantics without adding in-task heading|M3|
|Step-5 boundary|Atomic command facade plus CLI/doc fix-forward|Prevents split runtime state and stale `/sc:task` emission|M4|
|Step-6 boundary|Hard-delete donor skill after verifier and sync gates|Eliminates parallel live skill surface|M4|
|Residuals|Manifest and bucket disposition, zero violations outside allowed buckets|Avoids silent leftover runtime surfaces while allowing archives|M4-M5|
|Deferred items|D08 and D01 remain terminally deferred|Prevents scope expansion beyond directional merge|M5|

Hard non-goals:
- Do not reintroduce `/sc:task` as a non-deprecated live command surface.
- Do not preserve `sc-task-protocol/SKILL.md` as a parallel live skill.
- Do not introduce `TRIVIAL` as a tier value.
- Do not make per-item markers runtime dispatchers.
- Do not replace rf-qa with another verifier.
- Do not add F1 HALT semantics for environment-non-ideal states.

## Timeline Estimates

|Milestone|Duration|TDD Step Mapping|Start Dependency|Exit Evidence|
|---|---:|---|---|---|
|M1 Foundation Contracts|5 days|Step 1 plus Step 2 foundation pieces|Project start|MIG-001 exit criteria; TEST-001/005/010/013/025 pass|
|M2 Verification and Pre-Flight Semantics|4 days|Step 3 plus Step 2 pre-flight coverage|M1 complete|MIG-002 exit criteria; TEST-002/007/011/020 pass|
|M3 TFEP Core Transfer|6 days|Step 3 TFEP cluster plus Step 4 donor diff window|M2 complete|MIG-003/004 exit criteria; TEST-003/006/009/012/019/022/026 pass|
|M4 CLI Integration and Donor Deprecation|6 days|Steps 5, 6, and 7|M3 complete and S-1 discharged/frozen|MIG-005/006/007 exit criteria; TEST-008/014/015/016/017/018/023/027/028/029/030 pass|
|M5 Production Readiness and Audit Closure|4 days|Steps 8, 9, and 10|M4 complete|MIG-008/009/010 exit criteria; TEST-004/021/024 pass; all KPIs green|

Total: 25 implementation days. The estimate assumes one Engineering Lead, one rf-qa Owner, shared Documentation/Release support, and DevOps availability during M4. If Step-5 or Step-6 atomic gates fail, the schedule pauses at the boundary rather than allowing partial merge states.
