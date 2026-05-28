---
spec_source: "TDD_TASK_DIRECTIONAL_MERGE.compressed.md"
complexity_score: 0.92
complexity_class: HIGH
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: none
---

# Task Directional Merge (/sc:task → /task) — Project Roadmap

## Executive Summary

This roadmap executes the directional merge of the donor `/sc:task` command-and-skill pair into the recipient `/task` skill across a 10-step canonical commit sequence governed by ME-6 atomicity, three sequencing constraints (S-1, S-2, S-3), and a server-side push-policy enforcer (AC-ATK-17) that closes the H-2 rebase-split bypass. The merge transplants 8 Transfer Units (TU-1..TU-8) covering tier classification, path overrides, verification roster widening, git pre-flight, TFEP baseline, TFEP prohibitions, mid-phase rf-qa escalation, and incident reporting — while preserving 5 load-bearing invariants (INV-01..INV-05) under 9 manifest exceptions (ME-1..ME-9).

**Business Impact:** Internal framework feature; collapses two parallel task-execution surfaces (2 → 1 paired entry per K-07/K-08), eliminates 144 residual donor-surface occurrences across 40+ files (K-03), and establishes rf-qa as the structural verification floor at 4 invocation points post-merge. No customer-facing revenue/conversion metrics apply.

**Complexity:** HIGH (0.92) — 19 functional + 18 non-functional requirements; 5 load-bearing invariants with INV-04 split into parse/semantic layers (HIGHEST EXPOSURE); 3 coarse atomic commits (Steps 1, 5, 6); 136-file in-flight floor (monotonic upward); 144 residuals; server-side CI enforcement; load-bearing resumability across the live in-flight population.

**Critical path:** OQ resolution (M1 entry) → M1 atomic foundation (CR-FM-01..03 + CR-TASK-01..04 + CR-7 sentinel) → M2 routing + pre-flight → M3 TFEP cluster (R-DRIFT-03 patch precondition) → M4 verbatim diff audit (R-DRIFT-02 patch precondition) → M5 atomic soft-deprecation (S-2 binding) → M6 atomic hard-delete (S-3 binding; INV-04 highest exposure) → M7-M10 audit closure.

**Key architectural decisions:**

- **CR-7 ORDERING enforced by sentinel + AST-grade ordering grep** at row-1 of recipient skill (not by markdown discipline alone) — closes R-ATK-01; structural barrier against wrong-stance dispatch.
- **Server-side CI push-policy enforcement** at `.github/workflows/push-policy.yml` is the canonical venue for the 7-foundation-row atomicity check; local `.git/hooks/pre-push` rejected as bypassable via `--no-verify`.
- **TFEP baseline persists on disk** at `${TASK_DIR}/research/test-baseline.yaml` (ADAPT delta from donor in-memory form) because INV-04 binds resumability across session boundaries.
- **`flock` on `.claude/skills/.sync-lock`** wraps `make sync-dev` + `make verify-sync` to close both the forward-looking prune race and the live copy-overwrite race in `Makefile:121`.
- **AC-ATK-18 content-level audit at resume time** emits `gate-1.5: legacy-surface-reference` warn-and-continue per occurrence; never HALTs (preserves INV-01 / ME-3).

**Open risks requiring resolution before M1:**

- OQ-TIER-VOCABULARY: confirm canonical post-merge tier vocabulary is `{STRICT, STANDARD, LIGHT, EXEMPT}` (4-tier code) and retire vestigial `TRIVIAL` from spec §4.
- OQ-FM-03-SUNSET: bind CR-FM-03 default-to-STANDARD shim sunset condition (recommended: `N=50 generations AND ≥90 days post Step 6 AND CR-MIGR-FM-03 authored`).
- Q-GATE-1-5-TOKEN-COLLISION: pin grammar `gate-1.5: <subtype> ...` with closed subtype set to prevent parser ambiguity.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|----|-------|------|----------|--------|--------------|--------------|------|
|M1|Foundation: CR-7 Ordering + Tier Field + Gate 1 Dispatch (atomic)|Feature|P0|L|—|18|HIGH|
|M2|Routing Widening + Git Pre-Flight Side-Channel|Feature|P0|M|M1|10|MEDIUM|
|M3|TFEP Cluster: Baseline + Prohibitions + Escalation + Incident (byte-for-byte transplant)|Feature|P0|XL|M2|24|HIGH|
|M4|Donor Verbatim Diff Audit Window (CR-TASK-12 seven-diff)|Feature|P0|M|M3|10|MEDIUM|
|M5|Soft-Deprecation: Donor Command Stubification + CLI Re-Route (atomic, S-2)|Feature|P0|L|M4|18|HIGH|
|M6|Hard-Delete: Donor Skill Removal + Mirror Sync + Residual Manifest (atomic, S-3, INV-04 HIGHEST)|Feature|P0|L|M5|14|HIGH|
|M7|Invariant Survival Walkthrough + Anchor Content Audit|Feature|P0|M|M6|10|MEDIUM|
|M8|Documentation Rollup + mkdocs Build Gate|Feature|P1|M|M7|10|MEDIUM|
|M9|CR-DEP-06 Residual-Reference Manifest (post-Step-6 one-shot)|Feature|P0|S|M6|6|MEDIUM|
|M10|Audit Closure + KPI Baseline + Phase 7.5 Convergence|Feature|P0|M|M8,M9|10|LOW|

## Dependency Graph

M1 → M2 → M3 → M4 → M5 → M6 → M7 → M8 → M10; M6 → M9 → M10; M3 (TU-7) depends on OQ-F-05-MANIFESTIZATION resolution; M3 (TU-6) depends on OQ-PROHIBITION-DISPOSITION-MATRIX resolution; M3 entry depends on R-DRIFT-03 anchor patch landing in 3 artifacts + CR-TASK-12 audit anchors; M4 entry depends on R-DRIFT-02 anchor patch landing in 3 artifacts + CR-TASK-12 audit anchors; M5 entry depends on S-1 in-flight discharge (live named targets TASK-PRD-20260514-121039 + TASK-TDD-20260514-121250 + broader 136-file population) AND Q-GAP-01 (cleanup_audit/test_prompts.py) authored; M6 entry depends on AC-ATK-07 rf-qa F-07 chain verifier PASS AND Q-GAP-04 flock portability fallback documented; M7 entry depends on Q-2 content audit of 7 anchor artifacts complete.

## M1: Foundation — CR-7 Ordering + Tier Field + Gate 1 Dispatch (Atomic)

**Objective:** Land the 7 mutually-presupposing foundation rows in a single source-tree merge commit under ME-6 atomicity, establishing the tier classification contract, the row-1 call ordering (`path_override_check → tier_field_validate → gate_1_dispatch`), the CR-7 ORDERING sentinel, the CR-FM-03 default-to-STANDARD compat shim covering 136 live in-flight files, and the AC-ATK-05 closed-enumeration consumer register. | **Duration:** T+0 to T+5d (Week 1) | **Entry:** OQ-TIER-VOCABULARY + OQ-FM-03-SUNSET + Q-GAP-02/05/06 + Q-GATE-1-5-TOKEN-COLLISION resolved | **Exit:** Step-1 pre-commit gate exits 0; AC-SM-07 CR-FM-04 ordering grep returns 3 names monotonic; AC-SM-12 100% in-flight resume PASS against 136-file live population

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-TU-1|Tier field + Gate-1 dispatch + per-item marker|Recipient frontmatter gains optional `Tier:` field; classification header emitted TEXT-ONLY; Gate-1 dispatch fires once per task entry (ME-1)|task/SKILL.md|—|frontmatter `Tier:` ∈ {STRICT, STANDARD, LIGHT, EXEMPT}; gate-1 emits exactly once per entry; per-item marker is read-only (no re-dispatch)|M|P0|
|2|FR-TU-2|Critical/Trivial Path Override at row 1 (CR-7 ORDERING)|Row-1 site fires path_override_check → tier_field_validate → gate_1_dispatch in fixed order; CR-7 sentinel lands at Step 1|task/SKILL.md|FR-TU-1|3 call-sites in fixed order; CR-7 sentinel present byte-identical; critical paths (auth/, security/, crypto/, models/, migrations/) force STRICT (ANY-match); trivial paths (*.md, docs/, *test*.py) take override (ALL-match)|M|P0|
|3|FR-CS-1|Step 1 M1 atomic foundation commit|Land 7 mutually-presupposing foundation rows in single source-tree merge under ME-6 atomicity|task/SKILL.md|FR-TU-1, FR-TU-2|atomic single commit; CR-FM-04 ordering grep PASS; CR-TASK-01 sentinel grep PASS; pre-commit gate exits 0|L|P0|
|4|DM-001|Tier frontmatter field (Schema 1, CR-FM-01)|Optional inline MDTM frontmatter field at row-1 canonical position|task/SKILL.md|FR-TU-1|field-name:Tier-singular-cap; type:string-closed-enum; valid-values:STRICT\|STANDARD\|LIGHT\|EXEMPT; required:optional; default-when-absent:STANDARD-via-CR-FM-03-shim-no-file-mutation; canonical-position:row-1; mutability:author-set-never-runtime-mutated; constraint:closed-enum-INV-05|S|P0|
|5|DM-002|Per-item inline marker (Schema 2, CR-FM-02 / AC-ATK-05)|Optional per-row tier marker following checkbox|task/SKILL.md|FR-TU-1|marker-form:(Tier:VALUE)-parenthesized; regex:`^- \[[ x]\] \(Tier: (STRICT\|STANDARD\|LIGHT\|EXEMPT)\) `; cardinality:0..N-per-task; placement:after-checkbox-before-text; default-when-absent:falls-back-Schema-1-then-CR-FM-03; closed-consumer-register:{CR-TASK-07-baseline-skip}; constraint:NEVER-re-dispatches-Gate-1-per-ME-1|S|P0|
|6|COMP-001|Tier field parser + Gate 1 dispatch|Pre-loop classifier (read-only); LOC ~20 post-merge|task/SKILL.md|DM-001|kind:pre-loop-classifier-read-only; insertion-target:row-0-sentinel-plus-new-subsection-after-L73; pattern-source:donor-:9-enum-plus-commands-task-md-:55,61,104; INV-protected:INV-04-parse-INV-05; ME-bound:ME-1-ME-6; CR-row-author:CR-FM-01..03-CR-TASK-01..03; LOC-post-merge:~20|M|P0|
|7|COMP-002|Path override critical/trivial|Pre-loop classifier (read-only); LOC ~10|task/SKILL.md|DM-001|kind:pre-loop-classifier-read-only; insertion-target:row-0-shared-sentinel-plus-new-subsection-adjacent-to-COMP-001; pattern-source:donor-sc-task-protocol-:121-5-critical-globs-plus-:123-3-trivial-globs; INV-protected:INV-05; ME-bound:ME-6; CR-row-author:CR-TASK-01-plus-CR-7-ordering-sentinel; LOC-post-merge:~10|S|P0|
|8|API-001|path_override_check function|FIRST in CR-7 ORDERING; signature `path_override_check(task_target_paths: list[str]) -> forced_stance ∈ {STRICT, LIGHT, none}`|task/SKILL.md|COMP-002|position:FIRST-in-CR-7-ORDERING; signature:path_override_check(list[str])->str-in-{STRICT,LIGHT,none}; body:critical-hard-elevate-ANY-match-trivial-skip-ALL-match-else-none; side-effect:append-1-line-Task-Log; emission:path-override:forced_stance=STRICT(matched:glob)\|forced_stance=LIGHT\|no-match; invariants:INV-01,INV-04,INV-05|S|P0|
|9|API-002|tier_field_validate function|SECOND in CR-7 ORDERING; signature `tier_field_validate(frontmatter: dict) -> tier_field ∈ {STRICT, STANDARD, LIGHT, EXEMPT}`|task/SKILL.md|DM-001|position:SECOND-in-CR-7-ORDERING; signature:tier_field_validate(dict)->str-in-{STRICT,STANDARD,LIGHT,EXEMPT}; body:closed-enum-validation-absent-Tier-returns-STANDARD-CR-FM-03-shim; negative-set-guard:{ITERATIVE,SIMPLE,IMPLEMENT,COMPLEX}-rejected; side-effect:none-read-only; invariants:INV-01,INV-04,INV-05|S|P0|
|10|API-003|gate_1_dispatch function|THIRD in CR-7 ORDERING; signature `gate_1_dispatch(forced_stance, tier_field) -> execution_profile`|task/SKILL.md|API-001, API-002|position:THIRD-in-CR-7-ORDERING; signature:gate_1_dispatch(str,str)->execution_profile; resolution-precedence:forced_stance==STRICT-then-STRICT;forced_stance==LIGHT-then-LIGHT;none-then-map-tier_field; ME-1-binding:fires-once-per-task-entry-NOT-per-F1-iteration; ME-6-binding:D09a-plus-Gate-1-ship-together-CS-1-M1-atomic|S|P0|
|11|NFR-INV-1|F1 progress monotonicity invariant|F1 loop READ→IDENTIFY→EXECUTE→UPDATE→REPEAT preserved; no new HALT semantic mid-checklist; environment-non-ideal warn-and-continue only|task/SKILL.md|FR-CS-1|F1 5-step pattern preserved at task/SKILL.md:79-98 byte-identical; no new HALT verb in F1 vocabulary; per-item dispatch forbidden (ME-1); AC-ATK-02 5-row matrix returns warn-and-continue for all 5 rows|M|P0|
|12|NFR-INV-5|Refusal-of-definition invariant|Tier field + per-item marker = metadata conditioning audits, NOT work-definition driving runtime dispatch; no embedded runtime classifier (D09b rejected)|task/SKILL.md|DM-001, DM-002|closed-enum consumer register present at AC-ATK-05; new consumer requires new ME-NN row; ME-1 design-review checklist enforced; D09b LR-REJECT-3 stays terminal|M|P0|
|13|NFR-ME-1|PRE-LOOP DISPATCH ONLY binding|Per-item dispatch forbidden; Tier marker is tier-conditioned READ only|task/SKILL.md|NFR-INV-5|AC-ATK-05 closed-enum committed; tests/audit/test_marker_consumers.py PASS; load-bearing per validation-spec|S|P0|
|14|NFR-ME-6|M1 atomicity binding|7 foundation rows ship together in one source-tree merge under ME-6|task/SKILL.md|FR-CS-1|single-commit atomic landing; M1 atomicity rule audit at merge-master.md:60; AC-ATK-06 frozen-fixture snapshot present; AC-ATK-17 server-side pre-push hook active|M|P0|
|15|TEST-001|AC-ATK-01 row-1 call order test|tests/skills/task/test_row1_call_order.py::test_path_override_first asserts AST/grep order|tests/skills/task/|API-001..003|AST or line-range-pinned grep returns 3 function names in monotonically-increasing line order; reorder blocks commit|S|P0|
|16|TEST-005|AC-ATK-05 marker consumers closed-set test|tests/audit/test_marker_consumers.py::test_closed_consumer_set asserts only {CR-TASK-07 baseline-skip}|tests/audit/|DM-002|only authorized consumer = {CR-TASK-07 baseline-skip}; new consumer requires new ME-NN; test PASS on M1 commit|S|P0|
|17|TEST-013|AC-ATK-13 row-1 ordering grep test|tests/skills/task/test_row1_ordering_grep.py::test_executable_grep asserts both CR-FM-04 greps return 3 names monotonic|tests/skills/task/|API-001..003|both CR-FM-04 greps (row 1 + row 10) return 3 function names in monotonic order; 0 reorders detected|S|P0|
|18|TEST-025|AC-SM-07 CR-FM-04 ordering test|tests/skills/task/test_cr_fm_04_ordering.py asserts 2 greps × 3 function names = 6 hits monotonic|tests/skills/task/|TEST-013|2 greps × 3 names = 6 hits monotonic; 0 reorders; Step-4 pre-commit gate|S|P0|
|19|MIG-001|Step 1 M1 atomic foundation commit|Atomic-7 deliverable bundle landing under ME-6 / CR-7 / CR-9|task/SKILL.md|FR-CS-1, NFR-ME-6|Step-1 pre-commit gate exits 0; AC-SM-07 cleared; AC-SM-12 100% in-flight resume PASS against 136-file live population; rollback granularity: coarse (atomic-by-design); single revert reverses 7 rows|L|P0|
|20|OPS-003|Runbook R3: Tier mis-classification recovery|Symptoms: item executes under wrong tier|task/SKILL.md|API-001..003|symptoms:item-dispatched-under-wrong-tier; diagnosis-steps:read-frontmatter-Tier,read-per-item-marker,compute-3-level-fallback,compare-actual-dispatch-Task-Log; resolution:log-incident,fix-canonicalization,page-Eng-Lead-if-parser-bug; escalation:Eng-Lead-1h-rf-qa-for-errata; prevention:CR-FM-01-canonicalization-table-closed-enum-validation|S|P1|
|21|Q-GAP-02|HTML-vs-shell sentinel form decision|PRD S24.2 commits to HTML-comment form `<!-- CR-7 ORDERING ... -->`; specify binding mechanism|task/SKILL.md|FR-TU-2|sentinel form chosen (HTML-comment); binding mechanism specified (sentinel-presence grep AC-ATK-13 vs AST-level AC-ATK-01); test fixture authored|S|P0|
|22|Q-GAP-05|preflight.py helper module authoring|`superclaude/skills/task/preflight.py` authored per AC-ATK-10 fixture binding|src/superclaude/skills/task/|FR-TU-1|module exists at expected path; passes type checks; AC-ATK-10 fixture binding satisfied|S|P0|
|23|Q-GAP-06|frontmatter_validator.py helper module authoring|`superclaude/skills/task/frontmatter_validator.py` authored per CR-FM-01 binding + AC-ATK-12(c)|src/superclaude/skills/task/|DM-001|module exists at expected path; CR-FM-01 binding satisfied; AC-ATK-12(c) canonical table fixture PASS|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|CR-7 ORDERING sentinel comment block|HTML-comment marker|Row-0 of task/SKILL.md|M1|CR-FM-04 ordering grep; AC-ATK-13 sentinel audit|
|`path_override_check → tier_field_validate → gate_1_dispatch` call chain|Sequential dispatch wiring|Row-1 site of task/SKILL.md|M1|F1 loop entry; AC-ATK-01 AST check|
|AC-ATK-05 closed-enum consumer register|Authorization registry|`tests/audit/test_marker_consumers.py` + `task/SKILL.md` doc block|M1|Per-item marker dispatch path; new-consumer review gate|
|CR-FM-03 default-to-STANDARD compat shim|Conditional parser default|`tier_field_validate()` body|M1|All 136 live in-flight files at resume; gate-1.4 shim-status emission|

### Milestone Dependencies — M1

- None (foundation milestone)

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-TIER-VOCABULARY|Confirm canonical post-merge tier vocabulary is {STRICT, STANDARD, LIGHT, EXEMPT} (4-tier code); retire vestigial TRIVIAL from spec §4|INV-05 protection scope and ME-1 enumeration depend on this; tier classifier author at Step 1 codifies wrong enum set if unresolved|Engineering Lead|Before M1 entry|
|2|OQ-FM-03-SUNSET|Confirm CR-FM-03 default-to-STANDARD shim sunset binding N (recommended: N=50 generations AND ≥90 days post Step 6 AND CR-MIGR-FM-03 authored)|All 136 live files would transition from resumable to input-invalid HALT if sunset dropped without migration row|Engineering Lead|Before M1 entry|
|3|Q-GATE-1-5-TOKEN-COLLISION|Pin grammar `gate-1.5: <subtype> ...` with closed subtype set to disambiguate pre-flight vs legacy-surface-reference vs deleted-related-doc|Parser ambiguity; gate-1.5 emissions could collide between pre-flight and resume-time content audit|Engineering Lead / §14 author|Before M1 entry|
|4|Q-GAP-11|Acknowledgment-gate persistence shape (single Task Log line vs separate ack file) for Schema 5 one-shot ack mechanism|AC-ATK-18(c) closure depends on this; affects resume-time UX|§7 / §8 author|Before M1 entry|
|5|Q-AC-ATK-05-CLOSED-ENUM|AC-ATK-05 closed-enumeration register `[UNVERIFIED]` until M1 atomic-landing commit; authorized set: {CR-TASK-07 baseline-skip}|Architecture elevates to M1 commitment; new consumer requires new ME-10+|Engineering Lead / §6 author|M1 atomic commit landing|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-ATK-01 CR-7 markdown discipline weakness — sentinel could be stripped silently by future auto-gen tool|MEDIUM|M|H|Closed by sentinel + AST-grade grep (AC-ATK-13); CR-FM-04 ordering grep enforces function-name order independently of comment presence|Engineering Lead|
|2|R-RES-01 Tier-conditioned read boundary thin — wrapper-routed dispatch could describe forbidden per-item dispatch as "read"|MEDIUM|M|H|AC-ATK-05 closed-enum register + ME-1 design-time review checklist + CI lint step rejecting undeclared marker consumers|rf-qa|
|3|ME-6 atomicity violation — rebase-split lands intermediate broken state|HIGH|M|H|Server-side `.github/workflows/push-policy.yml` enforcement (AC-ATK-17, lands at M5/M6 boundary); local pre-commit gate Step-1|Engineering Lead|
|4|Tier vocabulary drift (TRIVIAL vs LIGHT/EXEMPT) confuses downstream skill authors|MEDIUM|M|M|OQ-TIER-VOCABULARY resolved pre-M1; canonical 4-tier set pinned in CR-FM-01 + propagated to all spec citations|Engineering Lead|
|5|CR-FM-03 sunset unbound — future audit row dropping default bricks 136 shim-era TASK files|MEDIUM|L|H|OQ-FM-03-SUNSET binding authored at M1 (CR-AUDIT-FM-03-SUNSET row); gate-1.4 shim-status emission counts down|Engineering Lead|

## M2: Routing Widening + Git Pre-Flight Side-Channel

**Objective:** Widen Gate-2 verification roster to `[rf-qa, quality-engineer]` on STRICT tier (TU-3, ME-2 preserved — rf-qa never replaced), and add Layer-2 git pre-flight with 5-row warn-and-continue disposition matrix (TU-4, ME-3 — no new HALT in F1). | **Duration:** T+5d to T+7d (Week 1-2) | **Entry:** M1 atomic commit landed; CR-FM-04 row-1 grep PASS | **Exit:** AC-ATK-02 5-row matrix test PASS (no HALT for any row); AC-ATK-10 input-invalid vs environment-non-ideal asymmetry table present; quality-engineer companion spawns at 2 of 4 rf-qa surfaces

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-TU-3|Gate-2 verification roster widening|Phase-Gate QA block widens verifier_roster to [rf-qa, quality-engineer] on STRICT; quality-engineer additive only (rf-qa never replaced per ME-2)|task/SKILL.md:181-211|FR-CS-1|verifier_roster=[rf-qa, quality-engineer] on STRICT; rf-qa always present (ME-2 binding); STANDARD/LIGHT/EXEMPT unchanged|M|P0|
|2|FR-TU-4|D15b git pre-flight (warn-and-continue)|F1 entry block gains Layer-2 pre-flight git status check with 5-row disposition matrix; NO HALT (ME-3 binding; INV-01 progress guarantee)|task/SKILL.md|FR-CS-1|5-row matrix {clean, dirty, tool-absent, not-a-repo, error-other} × {WARN-CONTINUE, GRACEFUL-SKIP}; no HALT for any row; tier-gated to STRICT|M|P0|
|3|FR-CS-2|Step 2 commit roster|Tier frontmatter contract + Gate-1 dispatch closed-enum canonicalization + parse-error HALT for malformed Tier|task/SKILL.md|FR-CS-1|CR-FM-01 canonicalization rules table committed; CR-TASK-02 parse-error HALT for non-enum Tier value; pre-commit gate exits 0|S|P0|
|4|FR-CS-3|Step 3 path overrides + Gate-2 roster widening commit|Lands TU-2 path overrides and TU-3 verification roster widening on STRICT|task/SKILL.md|FR-TU-3, FR-TU-4|CR-FM-04 row-1 ordering re-run PASS; ME-2 anchor check PASS; pre-commit gate exits 0|M|P0|
|5|COMP-003|Verification roster widening|Phase-gate + post-completion expansion (additive spawn); LOC ~14|task/SKILL.md|FR-TU-3|kind:phase-gate-post-completion-expansion-additive-spawn; insertion-target:Step-3b-inside-L191-198,Step-1b-inside-L219-226,Step-4-verdict-processing-edit,bullet-agent-type-list-L290-299; pattern-source:donor-sc-task-protocol-:89-quality-engineer-plus-:116-STRICT-routing-row; INV-protected:INV-03-rf-qa-floor-preserved; ME-bound:ME-2-supplemented-not-replaced; CR-row-author:CR-TASK-05; LOC-post-merge:~14|M|P0|
|6|COMP-004|Git pre-flight Task Log emission|F1 pre-execution side-channel (5-row warn-and-continue); LOC ~12|task/SKILL.md|FR-TU-4|kind:F1-pre-execution-side-channel-5-row-warn-and-continue; insertion-target:new-subsection-between-L102-and-L104; pattern-source:donor-sc-task-protocol-:81-Verify-git-working-directory-clean; INV-protected:INV-01-additive-surface-no-new-HALT; ME-bound:ME-3; CR-row-author:CR-TASK-06; LOC-post-merge:~12|S|P0|
|7|NFR-INV-3|Phase-gate rf-qa floor|rf-qa remains named role at all 4 invocation points post-merge (widenings permitted; replacements/displacements prohibited)|task/SKILL.md|FR-TU-3|grep returns ≥3 matches for subagent_type:"rf-qa" pre-merge; AC-ATK-07 F-07 chain verifier PASS; AC-ATK-11 retroactive ME-10 or non-generalization annotation present; CR-FM-04 content-keyed anchor enforced|M|P0|
|8|NFR-ME-2|rf-qa SUPPLEMENTED NOT REPLACED|4 invocation points: Gate-2, post-completion structural, post-completion qualitative, mid-phase TU-7 (load-bearing)|task/SKILL.md|NFR-INV-3|widenings permitted; replacements prohibited; content-keyed anchor (CR-FM-04); CR-TASK-05 acceptance criterion authored|S|P0|
|9|NFR-ME-3|SIDE-CHANNEL ONLY, NO F1 HALT|No new HALT semantics in F1 from TU-4/6/7/8 + TU-5; AC-ATK-02 5-row matrix all rows warn-and-continue|task/SKILL.md|FR-TU-4|AC-ATK-02 5-row matrix returns warn-and-continue for all 5 rows; AC-ATK-10 input-invalid (HALT) vs environment-non-ideal (warn-continue) asymmetry per row; F2 grep confirms no new env-state HALT row|S|P0|
|10|TEST-002|AC-ATK-02 git dirty dispatch 5-row matrix test|tests/skills/task/test_git_dirty_dispatch.py::test_5_row_matrix parametrize R1..R5|tests/skills/task/|COMP-004|parametrize {clean, dirty, tool-absent, not-a-repo, error-other}; for each: exact Task Log line; action token; proceed sentinel TRUE; no HALT; Step-2 pre-commit gate|M|P0|
|11|TEST-010|AC-ATK-10 pre-loop HALT policy test|tests/skills/task/test_preloop_halt_policy.py::test_2_category_table|tests/skills/task/|NFR-ME-3|input-invalid Tier → HALT exit-code 2; environment-non-ideal git-dirty → WARN-CONTINUE exit-code 0; Step-2 pre-commit|S|P0|
|12|MIG-002|Step 2 commit landing — TU-3 + TU-4|Deliverables: Gate 2 widened roster + D15b Layer 2 git pre-flight + helper modules|task/SKILL.md|FR-CS-2, FR-CS-3|AC-ATK-02 5-row dispatch PASS; AC-ATK-10 two-category fixture PASS; rollback granularity: fine (per-CR); tier_preflight_git_status() helper authored|M|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`quality-engineer` companion spawn (Phase-Gate Step 3b)|Parallel subagent spawn|`task/SKILL.md:198`|M2|Phase-Gate QA Step 4 verdict-processing (consumes 2 reports on STRICT)|
|`quality-engineer` companion spawn (Post-Completion Step 1b)|Parallel subagent spawn|`task/SKILL.md:226`|M2|Post-Completion verdict processing|
|`git status` 5-row disposition matrix|Conditional dispatch table|`COMP-004` body|M2|F1 entry block; Task Log emission line|
|AC-ATK-10 unified pre-loop HALT policy table|Decision matrix|`task/SKILL.md` error-handling region|M2|All pre-loop validators; routing input-invalid vs environment-non-ideal|

### Milestone Dependencies — M2

- M1 atomic commit landed; CR-FM-04 row-1 grep PASS; CR-7 ORDERING sentinel present byte-identical

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-RES-03 F-04 over-escalation unbounded by design — rf-qa queue flood risk on baseline-absent classification|MEDIUM|M|M|Reactive refusal threshold post queue-depth telemetry (OPS metric); AC-CR-TASK-09-F04 classification documented|rf-qa Lead|
|2|TU-3 widening invalidates ME-2 if quality-engineer accidentally displaces rf-qa|HIGH|L|H|Test fixture asserts subagent_type:"rf-qa" present at all 4 invocation points; CR-FM-04 content-keyed anchor audit|Engineering Lead|
|3|AC-ATK-02 5-row matrix incomplete — implementer adds HALT for `error-other` row|HIGH|L|H|AC-ATK-10 input-invalid (HALT) vs environment-non-ideal (warn-continue) asymmetry table authored; AC-ATK-02 parametrized test catches HALT introduction|Engineering Lead|

## M3: TFEP Cluster — Baseline + Prohibitions + Escalation + Incident (Byte-for-Byte Transplant)

**Objective:** Transplant the contiguous TFEP block from donor `sc-task-protocol/SKILL.md:125-244` into recipient under ME-6 byte-for-byte preservation: TU-5 disk-resident baseline at `${TASK_DIR}/research/test-baseline.yaml`; TU-6 three additive VIOLATION-level prohibitions + three permitted-exception carve-outs (F2 catalog 10 → 13); TU-7 mid-phase rf-qa escalation as the FOURTH rf-qa invocation point (F-05 authorized; AC-ATK-11 one-time carve-out); TU-8 seven-field incident-report side-effect file with byte-identical Outcome enum `{success / escalated / failed}` from donor `:232`. | **Duration:** T+7d to T+10d (Week 2) | **Entry:** M2 landed; **R-DRIFT-03 PATCH PRECONDITION applied** to 3 artifacts + CR-TASK-12 audit anchors; OQ-F-05-MANIFESTIZATION + OQ-PROHIBITION-DISPOSITION-MATRIX + OQ-TFEP-FIELD-COUNT resolved | **Exit:** AC-ATK-03 4-state observer PASS; AC-ATK-12(b) 7-field schema fixture PASS; AC-CR-TASK-09-F04 over-escalate PASS; F2 catalog grows 10 → 13 entries verbatim

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-TU-5|TFEP baseline snapshot on disk|Pre-F1 STRICT/STANDARD writes `${TASK_DIR}/research/test-baseline.yaml` containing pytest collect output; disk persistence load-bearing for INV-04 (ME-4 tier-gated)|task/SKILL.md|FR-CS-3|file emitted pre-F1 on STRICT/STANDARD; absent on LIGHT/EXEMPT; AC-ATK-03 four-state observation order pinned os.path.exists → os.path.getsize → yaml.safe_load → schema|M|P0|
|2|FR-TU-6|TFEP Prohibitions + Carve-outs (additive to F2)|F2 catalog 10-entry pre-merge absorbs 3 additive VIOLATION-level prohibitions + 3 permitted-exception carve-outs via byte-for-byte verbatim transplant from donor `:127-142`; post-merge count: 13 entries|task/SKILL.md:104-117|FR-CS-3|F2 count 10 → 13 verbatim; no existing prohibition deleted/weakened/narrowed; AC-ATK-11 disposition matrix; CR-TASK-12 verbatim diff audit PASS|M|P0|
|3|FR-TU-7|TFEP escalation gradient + mid-phase rf-qa (FOURTH invocation point)|TFEP escalation routes to rf-qa mid-phase as fourth rf-qa invocation point; six-step flow: halt-and-freeze → 9-field failure context YAML → forensic invocation tier ladder → consume → tasklist insertion → resume --compliance strict|task/SKILL.md|FR-TU-5, NFR-ME-2|fourth rf-qa invocation point present alongside L191/L221/L230; rf-qa identity preserved (ME-2); AC-ATK-11 F-05 paragraph-level surface-widening precedent; AC-SM-02 ME-2 traceability|L|P0|
|4|FR-TU-8|TFEP incident reporting side-effect file|Per TFEP resolution, writes `${TASK_DIR}/research/tfep-incident-report.md` with seven-field schema byte-identical to donor `:225-233`; Outcome enum `{success, escalated, failed}` byte-identical to donor `:232`|task/SKILL.md|FR-TU-7|seven fields: Trigger; Escalation count; Failing tests; Root cause; Solution; Outcome; Forensic artifacts; Outcome ∈ {success, escalated, failed} byte-identical donor :232; NO in-task heading; AC-ATK-12(b) schema enumeration PASS|M|P0|
|5|DM-003|TFEP Baseline YAML (Schema 3)|File-resident pre-loop test baseline classifying failures pre-existing vs new|task/SKILL.md|FR-TU-5|path:${TASK_DIR}/research/test-baseline.yaml; cardinality:0..1-per-task-STRICT/STANDARD-only; emission-point:First-Item-Protocol-pre-F1; persistence:YAML-on-disk-reused-across-resume; schema_version:int=1; captured_at:ISO-8601-UTC; tier:string-in-{STRICT,STANDARD}; tests:list-of-{test_id,status}; status-enum:{passing,failing}; 4-state-observation-order-pinned-absent-empty-parse-fail-schema-fail; retention:lifetime-of-task-git-tracked|S|P0|
|6|DM-004|tfep-incident-report.md (Schema 4)|Post-completion side-effect file with 7-field schema|task/SKILL.md|FR-TU-8|path:${TASK_DIR}/research/tfep-incident-report.md; cardinality:0..1-per-task-STRICT-post-fire; emission-point:Post-Completion-Validation; donor-schema-source:sc-task-protocol-:220-236-verbatim-ME-6; Trigger:string-enum-like; Escalation count:int-{1,2,3}; Failing tests:list-of-{test_id,classification-in-{pre-existing,new}}; Root cause:free-form-markdown; Solution:free-form-markdown; Outcome:closed-enum-{success,escalated,failed}-byte-identical-donor-:232; Forensic artifacts:path-or-list-under-${TASK_DIR}/reviews/|S|P0|
|7|DM-005|Gate-1.5 Emission Token (Schema 5, polymorphic)|Emission-only Task Log lines surfacing forward-looking compat-shim observations|task/SKILL.md|FR-TU-5|storage:emission-only-Task-Log-lines-in-Task-Log/Notes-section; cardinality:0..N-per-resume; folding-decision:single-polymorphic-schema-two-variants; variant-A-legacy-surface-reference:triggered-by-content-grep-at-resume-action=warn-and-continue-surface-enum-{/sc:task,sc-task-protocol,task-unified}; variant-B-deleted-related-doc:triggered-by-related_docs-traversal-ENOENT-action=warn-and-continue; one-shot-ack-gate:single-user-ack-per-resume-entry-gate-1.5:ack-received-user=ID-ts=ISO-8601; constraint:NEVER-HALT-NEVER-migration-NEVER-bundled-with-Tier-migration|S|P0|
|8|COMP-005|TFEP baseline snapshot|Pre-F1 side-effect file emitter (YAML); LOC ~10 + on-disk file|task/SKILL.md|FR-TU-5|kind:pre-F1-side-effect-file-emitter-YAML; insertion-target:new-subsection-between-L179-and-L181-plus-bullet-Session-Resumption-Step-4; pattern-source:donor-:144-153-in-memory-adapted-to-file-resident-per-INV-04; INV-protected:INV-04; ME-bound:ME-3-ME-4; CR-row-author:CR-TASK-07; LOC-post-merge:~10|S|P0|
|9|COMP-006|TFEP prohibitions + carve-outs|F2 catalog additive insertion + carve-out subsection; +3 bullets +~6 lines carve-out|task/SKILL.md|FR-TU-6|kind:F2-catalog-additive-insertion-plus-carve-out-subsection; insertion-target:append-after-L117-plus-carve-out-subsection-inside-TFEP-block; pattern-source:donor-:133-135-3-VIOLATION-rules-byte-for-byte-plus-:137-140-3-permitted-exceptions; INV-protected:INV-02-INV-01; ME-bound:ME-3; CR-row-author:CR-TASK-08,CR-TASK-12; LOC-post-merge:F2-10-to-13-plus-6-lines|S|P0|
|10|COMP-007|TFEP escalation trigger (mid-phase rf-qa)|F1-side-channel escalation router; 4th rf-qa invocation surface; LOC ~15|task/SKILL.md|FR-TU-7|kind:F1-side-channel-escalation-router-4th-rf-qa-invocation-surface; insertion-target:new-subsection-inside-TFEP-block; pattern-source:donor-:157-161-3-MUST-escalate-triggers; INV-protected:INV-03-additive-rf-qa-surface-ME-2-preserved; ME-bound:ME-2-ME-3; CR-row-author:CR-TASK-09; AC-ATK-11-carve-out:one-time-non-generalizing; LOC-post-merge:~15|M|P0|
|11|COMP-008|TFEP incident report|Post-resolution side-effect file emitter (Markdown); LOC ~12 + on-disk file|task/SKILL.md|FR-TU-8|kind:post-resolution-side-effect-file-emitter-Markdown; insertion-target:new-subsection-inside-TFEP-block; pattern-source:donor-:222-234-7-field-schema-byte-for-byte-plus-Outcome-enum-literal-:232; INV-protected:INV-04; ME-bound:ME-3-ME-6; CR-row-author:CR-TASK-10,CR-TASK-12; LOC-post-merge:~12|S|P0|
|12|API-013|rf-qa Invocation #4 (Mid-phase TFEP)|NEW inside TFEP block between L179 and L181; qa_phase: "tfep-incident-[N]"|task/SKILL.md|COMP-007|anchor:NEW-inside-TFEP-block-L179-L181; qa_phase:tfep-incident-N; output-path:${TASK_DIR}/reviews/qa-tfep-incident-N-report.md; additional-prompt-fields:TFEP-trigger-classification+baseline-diff+failing-tests-list+escalation-gradient-stage; authoritative-count:4-rf-qa-invocations-post-merge|S|P0|
|13|NFR-INV-2|F2 catalog additivity invariant|F2 catalog at `:104-117` extended only additively; pre-merge 10 entries; TU-6 adds 3 → post-merge 13|task/SKILL.md|FR-TU-6|pytest tests/skills/task/test_prohibitions_additive.py PASS; AC-ATK-11 disposition matrix; no existing prohibition deleted/weakened/narrowed; post-merge count ≥ 12 (target 13)|M|P0|
|14|NFR-INV-4a|Resumability parse layer|Every MDTM TASK file parses cleanly post-merge; CR-FM-03 default-to-STANDARD shim handles absent Tier|task/SKILL.md|FR-TU-5|tests/skills/task/test_compat_shim_parse.py parametrized over live in-flight population (136 floor); AC-ATK-12(c) sunset binding|M|P0|
|15|NFR-INV-4b|Resumability semantic layer (HIGHEST EXPOSURE)|Meaningful resume path through in-flight checklist body MUST survive merge; warn-and-continue per ME-3 (NOT HALT)|task/SKILL.md|FR-TU-5, DM-005|AC-ATK-18 four sub-bindings: (a) content-layer grep at resume; (b) sprint-emit boundary content-grep; (c) one-shot ack gate via legacy-surface-ack:1; (d) CR-DEP-06 manifest; manual walkthrough on H-4 target|M|P0|
|16|NFR-ME-4|BASELINE TIER-GATED (Ancillary)|TU-5 baseline collection runs only on STRICT/STANDARD; LIGHT/EXEMPT skip|task/SKILL.md|FR-TU-5|CR-TASK-07 acceptance criterion: baseline YAML present pre-F1 on STRICT/STANDARD; absent on LIGHT/EXEMPT|S|P1|
|17|TEST-003|AC-ATK-03 baseline trinary 4-state test|tests/skills/task/test_baseline_trinary.py::test_4_state_observer parametrize|tests/skills/task/|DM-003|parametrize {absent, empty, parse-fail, schema-fail}; observer order pinned (exists → getsize → safe_load → schema); all four → classification=new-all; Step-3 pre-commit|M|P0|
|18|TEST-012|AC-ATK-12 incident schema 7 fields + canonical enum test|tests/skills/task/test_tfep_incident_schema.py + tests/audit/test_cr_fm_01_canonical.py|tests/skills/task/, tests/audit/|DM-004, DM-001|Schema enumerates exactly 7 fields {Trigger, Escalation count, Failing tests, Root cause, Solution, Outcome, Forensic artifacts}; Tier enum closed {STRICT, STANDARD, LIGHT, EXEMPT}; Outcome enum byte-identical donor :232|M|P0|
|19|MIG-003|Step 3 M3 TFEP cluster commit|R-DRIFT-03 patch precondition + TU-5 + TU-6 + TU-7 + TU-8|task/SKILL.md|FR-TU-5..8|R-DRIFT-03 anchor patch applied to 3 artifacts + CR-TASK-12 anchors BEFORE this commit; AC-ATK-03 4-state PASS; AC-ATK-12(b) 7-field PASS; AC-CR-TASK-09-F04 over-escalate PASS; rollback granularity: fine (per-CR within DM-7/DM-9 order)|L|P0|
|20|OPS-001|Runbook R1: Critical Path Override invocation|Symptoms: F1 dispatched to STRICT for auth/security/crypto/models/migrations item despite Tier LIGHT/EXEMPT|task/SKILL.md|FR-TU-7|symptoms:F1-STRICT-dispatch-despite-LIGHT-or-EXEMPT-frontmatter; diagnosis:read-Task-Log-path-override-fired,confirm-CR-7-sentinel,verify-path_override_check-FIRST; resolution:honor-override-STRICT-wins,require-rf-qa-sign-off-on-suppression; escalation:rf-qa-1h-Eng-Lead-4h; prevention:operator-training-CR-7-sentinel-AST-grep-audit|S|P1|
|21|OPS-004|Runbook R4: TFEP escalation handling|Symptoms: F-05 authorized TFEP-escalation invocation logged; baseline classifies ≥1 new-test fail|task/SKILL.md|FR-TU-7, FR-TU-8|symptoms:F-05-TFEP-escalation-fired-baseline-classifies-new-test-fail; diagnosis:confirm-baseline-AC-ATK-03-4-state,read-incident-report,classify-carve-outs,confirm-prohibition-disposition-matrix; resolution:parse-fail-or-schema-fail-treat-as-new,carve-out-record-exception,else-HALT-route-rf-qa-adjudication; escalation:rf-qa-30min; prevention:AC-ATK-03-4-state-tier-gated-baseline-ME-4|S|P1|
|22|Q-GAP-10|tfep-incident-report.md template field alignment|Seven-field schema fields enumeration must match donor `:222-234` verbatim|task/SKILL.md|FR-TU-8|TDD-layer naming convention {tier, item_id, trigger, classification, action, timestamp, sha} is research inference; §7 Schema 4 confirms 7 fields; donor verbatim alignment owed|S|P0|
|23|Q-GAP-12|Schema-version field uniformity|Schema 3 includes schema_version:1; decide whether all 5 schemas adopt uniform version field|task/SKILL.md|DM-003, DM-004, DM-005|design decision: uniform schema_version across all 5 schemas vs Schema-3-only; document in §7 Data Models|S|P2|
|24|Q-GATE-1-5-SCHEMA|6th Gate-1.5 schema decision (folded into Schema 5)|Decide whether `gate-1.5: deleted-related-doc` is 6th canonical schema OR Schema 5 variant — adopted: fold-into-Schema-5|task/SKILL.md|DM-005|Schema 5 polymorphic with two variants (legacy-surface-reference + deleted-related-doc); preserves single-grammar parser; documented in §7|S|P1|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`${TASK_DIR}/research/test-baseline.yaml`|Disk-resident YAML emission|TU-5 baseline subsection|M3|TFEP trigger classification (pre-existing vs new); resume continuity|
|F2 prohibition catalog row 11-13 (additive)|Catalog append|`task/SKILL.md:117` boundary|M3|F2 prohibition enforcement; AC-ATK-11 disposition matrix routing|
|rf-qa mid-phase invocation (TFEP)|Subagent spawn (4th invocation)|TU-7 new subsection inside TFEP block|M3|TFEP escalation gradient → rf-qa adjudication → tasklist insertion|
|`${TASK_DIR}/research/tfep-incident-report.md`|Disk-resident Markdown emission|TU-8 new subsection inside TFEP block|M3|Post-Completion Validation read; Schema 4 7-field validation|
|Gate-1.5 emission token (legacy-surface-reference + deleted-related-doc)|Emission-only Task Log token|`gate-1.5:` prefix grammar in Task Log/Notes|M3 (foundation) → M6 (resume-time activation)|AC-ATK-18 resume content audit; one-shot ack gate|

### Milestone Dependencies — M3

- M2 landed
- **R-DRIFT-03 anchor patch landed** in `transfer-manifest.md` TU-7 L277 + `integration-sketches.md` IS-ADOPT-9 L142 + `invariant-survival-walkthrough.md` §2.6 step 4 L277 (replace `:200-210` → `:157-161`) AND CR-TASK-12 audit anchors updated

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-F-05-MANIFESTIZATION|Decide retroactive ME-10 vs one-time carve-out for F-05 per AC-ATK-11|TU-7 mid-phase invocation widens INV-03 surface; future TU-style merges could cite F-05 as precedent without this gate|Engineering Lead|Before M3 entry|
|2|OQ-PROHIBITION-DISPOSITION-MATRIX|Decide verifier-spawned F1 disposition per AC-ATK-11 generalization|TFEP prohibition firing inside verifier-spawned mid-phase rf-qa context needs explicit disposition (root F1 vs verifier-spawned F1 vs mid-phase rf-qa)|Engineering Lead|Before M3 entry|
|3|OQ-TFEP-FIELD-COUNT|Resolve TU-8 incident-report 6-vs-7 field cardinality; §7 Schema 4 commits to 7|TU-8 schema enumeration depends; Outcome enum reconciles to donor literal :232 byte-identical|Engineering Lead|Before M3 entry|
|4|Q-R-DRIFT-03|Patch donor anchor :200-210 → :157-161 in 3 artifacts + CR-TASK-12 anchors|MEDIUM, M3-blocking — CR-TASK-12 verbatim-diff audit would fire against D23 forensic-results content (REJECTed by ledger LR-DEFER-6) and erroneously block M3 commit|Documentation/Release Owner|Before M3 entry|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-DRIFT-03 donor anchor off-by-43 — CR-TASK-12 audit mis-fires against D23 forensic-results|MEDIUM (M3-blocking)|M|H|Patch single-source: replace `:200-210` → `:157-161` in 3 artifacts + CR-TASK-12 audit anchors pre-Step-3|Documentation/Release Owner|
|2|R-RES-02 F-05 fourth rf-qa invocation widens INV-03 surface — anchor extension-point-contracts.md:11-17 NOT amended|MEDIUM|M|H|AC-ATK-11 retroactive ME-10 OR one-time non-generalizing carve-out; document chosen disposition in commit msg|Engineering Lead|
|3|R-RES-03 F-04 over-escalation unbounded — rf-qa queue flood risk|MEDIUM|M|M|Reactive refusal threshold post queue-depth telemetry; documented as accepted residual per §15 Concession 3|rf-qa Lead|
|4|TU-8 incident-report schema drift at resume — older 6-field file fails 7-field validation|MEDIUM|L|M|Emit `gate-1.5: tfep-incident-schema-drift detected file=<path> expected_fields=7 found_fields=<n> action=warn-and-continue`; route to rf-qa per OPS-004|rf-qa Lead|

## M4: Donor Verbatim Diff Audit Window (CR-TASK-12 Seven-Diff)

**Objective:** Establish the byte-for-byte preservation audit gate against the still-present donor SKILL.md before Step-5 stubification. CR-TASK-12 seven-diff audit (6 donor strings + 1 sentinel-comment block) returns zero-diff against frozen fixture `tests/fixtures/donor-blocks/`. Replace md5sum with sha256 per AC-ATK-09 mechanical substitution; capture sha256 baselines for CR-DEP-02. | **Duration:** T+10d to T+12d (Week 2) | **Entry:** M3 landed; **R-DRIFT-02 PATCH PRECONDITION applied** to 3 artifacts + CR-TASK-12 audit anchors; Q-GAP-07 donor-block fixtures authored | **Exit:** CR-TASK-12 returns 7 zero-diffs (AC-SM-08 gate); AC-ATK-06 frozen-fixture snapshot script live

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-CS-4|Step 4 TU/donor verbatim diff audits + sentinel landing|CR-TASK-12 seven-diff audit pass (6 donor strings + 1 sentinel-comment block) against donor blocks|task/SKILL.md, tests/fixtures/donor-blocks/|FR-CS-3|zero-diff against tests/fixtures/donor-blocks/; pre-commit gate; 6 donor strings + 1 sentinel block|M|P0|
|2|TEST-006|AC-ATK-06 donor diffs seven zero-diffs test|tests/skills/task/test_cr_task_12_donor_diffs.py::test_seven_zero_diffs|tests/skills/task/|FR-CS-4|7 diff invocations return zero against tests/fixtures/donor-blocks/*.txt; Step-4 pre-commit|S|P0|
|3|TEST-026|AC-SM-08 CR-TASK-12 seven-diff test|tests/skills/task/test_cr_task_12_donor_diffs.py::test_6_donor_plus_1_sentinel|tests/skills/task/|TEST-006|7 diffs return zero (6 donor + 1 sentinel block); AC-SM-08 closure|S|P0|
|4|TEST-009|AC-ATK-09 sha256 digests test|tests/skills/task/test_cr_task_11_digest.py::test_sha256_matches_baseline|tests/skills/task/|FR-CS-4|all 3 audit digests use sha256 (NOT md5); baselines pinned; Step-5 pre-commit|S|P0|
|5|TEST-008|AC-ATK-08 git SHA embedding test|tests/scripts/test_embed_git_sha.py::test_idempotent + tests/audit/test_cr_dep_05_grep.py::test_post_step5_stale_verification|tests/scripts/, tests/audit/|FR-CS-4|every [CODE-VERIFIED] tag carries (git-sha:<SHA>) suffix; idempotent; PRD final-commit + Step-5/6 pre-commit|S|P0|
|6|MIG-004|Step 4 M-sync + audits commit|CR-TASK-11 (sha256 replaces md5sum) + CR-FM-04 ordering + CR-TASK-12 seven-diff|task/SKILL.md|FR-CS-4|all three audit rows pass; commit blocked otherwise; rollback granularity: fine|M|P0|
|7|Q-GAP-07|tests/fixtures/donor-blocks/*.txt authoring|8 files: 6 donor strings + 2 sentinel blocks (CR-7 + CR-8) must be authored pre-Step-6|tests/fixtures/donor-blocks/|FR-CS-4|fixtures: TU2_path.txt, TU2_redirect.txt, TU6_prohibitions.txt, TU6_carve_outs.txt, TU7_triggers.txt, TU8_schema.txt, CR7_sentinel.txt, CR8_sentinel.txt; CR-TASK-12 audit moves to fixture-backed after Step 6 hard-delete|S|P0|
|8|FR-CS-7|Step 7 Sprint/pipeline integrator fix-up (preview)|No runtime caller emits /sc:task post-stubification; sets up server-side hook|task/SKILL.md, src/superclaude/cli/|FR-CS-4|pytest pass + AC-ATK-17 server-side pre-push hook active; covered by M5/M6 atomicity|S|P0|
|9|TEST-004|AC-ATK-04 condensation table test|tests/audit/test_condensation_table.py::test_79_to_67_to_65|tests/audit/|FR-CS-4|6 bucket rows sum to 79 row-instances → 65 distinct CR-IDs → 67 PASS-line-items; names 2 duplicate CR-IDs|S|P1|
|10|TEST-011|AC-ATK-11 ME-10 carve-out test|tests/audit/test_me10_carve_out.py::test_me10_authored_or_annotated|tests/audit/|FR-TU-7|ME-10 row authored OR explicit non-generalization annotation present at final-merge-plan.md:148|S|P0|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`tests/fixtures/donor-blocks/*.txt` (8 files)|Frozen-fixture snapshot|`tests/fixtures/`|M4 (live donor present) → M6 (fixture-backed post-deletion)|CR-TASK-12 seven-diff audit at every commit through M10|
|sha256 digest baselines|Hash baseline files|`tests/fixtures/digest-baselines/`|M4|CR-DEP-02 baseline check at M5; CR-TASK-11 audit; CR-DIST-02 mirror digest|
|`scripts/embed_git_sha.py`|Tag-embedding script|`scripts/`|M4|All `[CODE-VERIFIED]` tags receive `(git-sha:<40-char>)` suffix at PRD final commit per AC-ATK-08|

### Milestone Dependencies — M4

- M3 landed
- **R-DRIFT-02 anchor patch landed** in `transfer-manifest.md` TU-6 L238 + `integration-sketches.md` IS-ADOPT-2 L52 + `invariant-survival-walkthrough.md` §2.6 step 3 L263 (replace `:127-135` → `:133-135`) AND CR-TASK-12 audit anchors updated

### Open Questions — M4

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|Q-R-DRIFT-02|Patch donor anchor :127-135 → :133-135 in 3 artifacts + CR-TASK-12 anchors|LOW (mechanical, content verbatim preserved); but blocks CR-TASK-12 audit if not patched|Documentation/Release Owner|Before M4 entry|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-DRIFT-02 donor anchor off-by-2 — CR-TASK-12 audit cite drift|LOW|M|L|Patch `:127-135` → `:133-135` in 3 artifacts + CR-TASK-12 audit anchors pre-Step-4|Documentation/Release Owner|
|2|Donor-block fixtures absent at M5/M6 boundary — CR-TASK-12 audit cannot continue post-hard-delete|HIGH|L|H|Q-GAP-07 fixtures authored at M4; AC-ATK-06 frozen-fixture snapshot script captures donor body byte-identical|Engineering Lead|
|3|sha256 substitution incomplete — some audit row still uses md5sum|MEDIUM|L|M|AC-ATK-09 mechanical substitution + TEST-009 PASS confirms all 3 audit digests sha256|Engineering Lead|

## M5: Soft-Deprecation — Donor Command Stubification + CLI Re-Route (Atomic, S-2)

**Objective:** Atomically stubify the donor `/sc:task` command (CR-DEP-01), capture sha256 baseline (CR-DEP-02), re-route 6 CLI emission sites (`sprint/process.py:170` + 5 `cleanup_audit/prompts.py` sites), and emit doc redirect (CR-DOC-01). S-2 binding: all 6 sites re-routed atomically with command stubification or sprint runs pinned to this SHA die. Server-side pre-push hook (AC-ATK-17) closes H-2 rebase-split bypass. | **Duration:** T+12d to T+15d (Week 3) | **Entry:** M4 landed; **S-1 in-flight discharge** (live named targets TASK-PRD-20260514-121039 + TASK-TDD-20260514-121250 + broader 136-file population complete OR snapshot-frozen with decision record); Q-GAP-01 cleanup_audit/test_prompts.py authored; Q-GAP-08 condensation table authored; Q-GAP-09 server-side hook hosting decided | **Exit:** AC-ATK-15 Step-5 atomicity test PASS; AC-ATK-17 server-side pre-receive hook PASS (no rebase-split bypass); AC-SM-09 commit roster equality test PASS; `superclaude sprint run` returns 0 emission boundary failures

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-CS-5|Step 5 donor command stubification (atomic, S-2 binding)|Atomic landing: CR-DEP-01 stubify /sc:task command + CR-DEP-02 sha256 baseline + CR-DEP-05 CLI residual grep + CR-DOC-01 doc redirect + CR-REF-01..02 sprint CLI re-route + CR-REF-09 sprint TUI re-route|src/superclaude/commands/task.md, src/superclaude/cli/|FR-CS-4|atomic single commit; AC-ATK-15 Step-5 atomicity test PASS; AC-ATK-17 server-side pre-receive hook PASS; pytest pass + CR-DEP-02 sha256 baseline + CR-DEP-05 grep|L|P0|
|2|API-004|Sprint CLI Emission Site (sprint/process.py:170)|Pre-merge: `f"/sc:task Execute all tasks in @{phase_file} "` → Post-merge: `f"/task Execute all tasks in @{phase_file} "`|src/superclaude/cli/sprint/process.py:170|FR-CS-5|literal swap; AC-ATK-17 boundary contract: `assert prompt.startswith("/task Exec"); assert "/sc:task" not in prompt`; tests/sprint/test_process.py:80-89 updated lockstep|S|P0|
|3|API-005|Cleanup-Audit Surface Scan (prompts.py:26)|Builder: build_surface_scan_prompt; pre-merge `/sc:task Perform a surface-level scan ...` → post-merge `/task ...`|src/superclaude/cli/cleanup_audit/prompts.py:26|FR-CS-5|1-line edit; new tests/cleanup_audit/test_prompts.py::test_surface_scan_prompt_emits_task; caller: cli/cleanup_audit/executor.py:197 (G-001)|S|P0|
|4|API-006|Cleanup-Audit Structural Analysis (prompts.py:47)|Builder: build_structural_analysis_prompt; pre-merge `/sc:task Perform deep structural analysis ...` → post-merge `/task ...`|src/superclaude/cli/cleanup_audit/prompts.py:47|FR-CS-5|1-line edit; new tests/cleanup_audit/test_prompts.py::test_structural_analysis_prompt_emits_task; callers: executor.py:211 (G-002), :228 (G-003)|S|P0|
|5|API-007|Cleanup-Audit Cross-Cutting (prompts.py:69)|Builder: build_cross_cutting_prompt; pre-merge `/sc:task Detect duplication, sprawl ...` → post-merge `/task ...`|src/superclaude/cli/cleanup_audit/prompts.py:69|FR-CS-5|1-line edit; new tests/cleanup_audit/test_prompts.py::test_cross_cutting_prompt_emits_task; caller: executor.py:245 (G-004)|S|P0|
|6|API-008|Cleanup-Audit Consolidation (prompts.py:92)|Builder: build_consolidation_prompt; pre-merge `/sc:task Consolidate audit findings ...` → post-merge `/task ...`|src/superclaude/cli/cleanup_audit/prompts.py:92|FR-CS-5|1-line edit; new tests/cleanup_audit/test_prompts.py::test_consolidation_prompt_emits_task; caller: executor.py:263 (G-005)|S|P0|
|7|API-009|Cleanup-Audit Validation (prompts.py:116)|Builder: build_validation_prompt; pre-merge `/sc:task Validate audit findings ...` → post-merge `/task ...`|src/superclaude/cli/cleanup_audit/prompts.py:116|FR-CS-5|1-line edit; new tests/cleanup_audit/test_prompts.py::test_validation_prompt_emits_task; caller: executor.py:278 (G-006)|S|P0|
|8|API-014|Donor Command Stubification (CR-DEP-01)|`src/superclaude/commands/task.md:100`: `> Skill sc:task-protocol` → `> Skill task` (Form 1, synth-05 binding)|src/superclaude/commands/task.md:100|FR-CS-5|line 100 rewrite + 8 brand-name occurrences at lines 12, 19, 41, 106, 117, 128, 139, 169 swept; HTML marker `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` preserved verbatim (test-fixture anchor; load-bearing semantic token)|S|P0|
|9|NFR-S-1|In-flight discharge (population-generalized)|Any in-flight PRD/TDD task in `.dev/tasks/` referencing donor surfaces MUST complete before Step 5 OR be snapshot-frozen with decision record|.dev/tasks/, scripts/|FR-CS-5|--max-wait 14d default; scripts/embed_git_sha.py walks every [CODE-VERIFIED] tag; CR-DEP-05 grep extension flags post-Step-5 stale-tag drift; live spec-named targets (TASK-PRD-20260514-121039 LIVE 258 refs; TASK-TDD-20260514-121250 LIVE) AND broader 136-file population bound|M|P0|
|10|NFR-S-2|CLI runtime atomicity|Step-5 commit MUST be atomic with CLI fix-forward; server-side push-policy enforcer on landing commit at master|.github/workflows/, scripts/|FR-CS-5, API-004..009|AC-ATK-17 server-side pre-receive hook re-greps /sc:task\b against src/superclaude/cli/**/*.py; fallback scripts/atomic_step_5.sh flock -xn /tmp/step5.lock; anti-persona enforcement; V3 origin|M|P0|
|11|TEST-015|AC-ATK-15 CR-DOC-01 atomic Step-5 test|tests/audit/test_cr_doc_01_step.py::test_landed_with_dep_01|tests/audit/|FR-CS-5|Step-5 commit roster includes both commands/task.md and docs/user-guide/commands.md; Step-8 fallback only with AUTHORIZE_HOT_FIX=1|S|P0|
|12|TEST-017|AC-ATK-17 server-side pre-receive hook test|tests/ci/test_pre_receive_hook.py::test_rebase_split_rejected|tests/ci/|NFR-S-2|fabricate rebase-split commit pair; hook exits non-zero on intermediate broken state|M|P0|
|13|TEST-019|AC-SM-01 V/C/K byte-match test|tests/audit/test_vck_verdicts.py::test_transfer_manifest_byte_match|tests/audit/|FR-CS-5|8/8 V/C/K verdicts identical byte-for-byte against transfer-manifest.md §4|S|P0|
|14|TEST-027|AC-SM-09 Step-5 commit roster test|tests/audit/test_step_5_commit_roster.py::test_exact_file_list|tests/audit/|FR-CS-5|git log --name-only <step5-commit> set-equal to final-merge-plan.md:375 roster|S|P0|
|15|MIG-005|Step 5 atomic soft-deprecation commit (S-2 binding)|CR-DEP-01 + CR-DEP-02 sha256 + CR-DEP-05 grep + CR-DOC-01 atomic + CR-REF-01..05 + In-flight target population frozen|src/superclaude/commands/task.md, src/superclaude/cli/, docs/|FR-CS-5, NFR-S-1, NFR-S-2|AC-ATK-15 Step-5 atomicity PASS; AC-ATK-17 server-side hook PASS; AC-SM-09 commit roster equality PASS; rollback granularity: coarse (atomic, S-2 binding); if M6 already shipped cannot cleanly roll back without also reverting M6|L|P0|
|16|Q-GAP-01|cleanup_audit/test_prompts.py absence|Spec under-counts CLI emission sites by 5/6; cleanup_audit/prompts.py L26, L47, L69, L92, L116 not named|tests/cleanup_audit/test_prompts.py|API-005..009|test module authored with 5 fixtures (one per builder); each asserts prefix grep + regression guard; R-DIV-01 closure|M|P0|
|17|Q-GAP-08|docs/condensation-table.md artifact authoring|Per AC-ATK-04 condensation-bucket table|docs/condensation-table.md|TEST-004|6 bucket rows sum to 79 → 65 distinct CR-IDs → 67 PASS line-items; names 2 duplicate CR-IDs; pre-commit gate|S|P1|
|18|Q-GAP-09|Server-side pre-receive hook hosting|GitHub Actions or self-hosted-git pre-receive availability decided|.github/workflows/push-policy.yml|NFR-S-2|hook venue chosen (GitHub Actions OR self-hosted); fallback scripts/atomic_step_5.sh with flock; documented in CI|M|P0|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`/sc:task` → `/task` literal swap (6 emission sites)|String replacement registry|`API-004..009`|M5|sprint runner; cleanup-audit executor; all subprocess prompts|
|`> Skill sc:task-protocol` → `> Skill task`|Skill invocation flip|`commands/task.md:100`|M5|`/task` command dispatch via Claude Code|
|Server-side push-policy enforcer|CI workflow|`.github/workflows/push-policy.yml`|M5|Every push to master/integration; AC-ATK-17 closure for H-2|
|`scripts/embed_git_sha.py`|Tag-embedding|`scripts/`|M5|Pre-commit hook on every PRD/TDD final commit; AC-ATK-08|
|`scripts/atomic_step_5.sh`|Fallback atomicity wrapper|`scripts/`|M5|`flock -xn /tmp/step5.lock` if server-side hook unavailable|

### Milestone Dependencies — M5

- M4 landed (CR-TASK-12 seven-diff PASS; sha256 baselines pinned)
- **S-1 in-flight discharge**: spec-named targets `TASK-PRD-20260514-121039` (LIVE, 258 refs) and `TASK-TDD-20260514-121250` (LIVE) complete OR snapshot-frozen; broader 136-file in-flight population recounted at pre-commit time and disposed
- AC-ATK-07 rf-qa F-07 chain verifier ready (preparation for M6)
- Q-GAP-01 + Q-GAP-08 + Q-GAP-09 closed

### Open Questions — M5

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|Q-3|S-1 named-target population update — confirm supplement-not-replace framing (live targets + 136-file population)|NFR-S-1 binding scope; if framing wrong, S-1 either over-blocks (waiting on absent target) or under-blocks (misses live target)|Engineering Lead|Before M5 entry|
|2|Q-4|CR-DEP-06 elevation confirmation (144 binding count for residual manifest)|CR-DEP-06 manifest scope (61 backlog + 83 docs/generated = 144); live recount drift to 153 across 45 files documented|Engineering Lead|Before M5 entry|

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-S-2 CLI runtime atomicity break — Step-5 commit lands without 6-site re-routing|HIGH|M|H|AC-ATK-17 server-side pre-receive hook re-greps landing commit (NOT working tree) for `/sc:task\b` across `src/superclaude/cli/{sprint,cleanup_audit}/**`; rejects push if grep matches AND donor body not also deleted|Engineering Lead|
|2|R-H-02 rebase-split bypass — H-2 scenario lands intermediate broken master SHA|HIGH|M|H|AC-ATK-17 server-side hook + S-5 rebase-ban policy; local pre-push hook rejected as bypassable via --no-verify|Engineering Lead|
|3|R-S-1 in-flight tasks not discharged at Step-5 entry — live spec-named targets persist|HIGH|M|H|S-1 generalization: complete OR snapshot-freeze OR auto-invoke option (b) at --max-wait 14d expiry; pinned git-SHA on [CODE-VERIFIED] tags|Engineering Lead|
|4|R-FM-02 Step-5 atomic flaky pytest no-progress state|MEDIUM|M|M|Pin env vars (PYTHONHASHSEED, locale, timezone) per FM-04; CI gate sign-off; retry-then-revert protocol|Engineering Lead|
|5|R-FM-03 Parallel subagent SKILL.md conflict at row 1 vs row 10 during Step 5|MEDIUM|L|H|Ban parallel subagent dispatch on task/SKILL.md during Step 5; single-executor discipline|Engineering Lead|

## M6: Hard-Delete — Donor Skill Removal + Mirror Sync + Residual Manifest (Atomic, S-3, INV-04 HIGHEST)

**Objective:** Atomically remove donor `src/superclaude/skills/sc-task-protocol/` directory under CR-DEP-03 + CR-DEP-04 + CR-DIST-02; close the 136-file in-flight semantic resumability surface with AC-ATK-18 content-level audit, one-shot ack gate, and CR-DEP-06 manifest. `flock` discipline on `make sync-dev` closes both prune race and live copy-overwrite race in `Makefile:121` (AC-ATK-16). rf-qa rebound as F-07 chain-integrity verifier spawns at pre-commit (AC-ATK-07). Destructive-by-default: roll FORWARD preferred over revert. | **Duration:** T+15d to T+17d (Week 3) | **Entry:** M5 landed; AC-ATK-07 rf-qa F-07 chain verifier authored; Q-GAP-04 flock portability fallback documented (`brew install flock` on macOS or `lockfile-create` fallback) | **Exit:** AC-SM-10 commit roster equality PASS; `make verify-sync` returns 0; donor `sc-task-protocol/` directory absent from both `src/` AND `.claude/`; CR-DEP-06 manifest: residual count outside authorized buckets = 0

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-CS-6|Step 6 donor skill hard-delete (atomic, S-3 binding)|Atomic landing: CR-DEP-03 hard-delete donor SKILL.md + CR-DEP-04 directory absence + CR-DIST-02 sync rule|src/superclaude/skills/sc-task-protocol/|FR-CS-5|atomic single commit; AC-ATK-07 rf-qa F-07 chain verifier PASS; `make verify-sync` returns 0; rollback granularity: destructive-by-default; roll FORWARD preferred|L|P0|
|2|FR-CS-9|Step 9 leave-as-is enforcement across buckets|Buckets A, C, D, E, F, G, H; CR-REF-12 scoped to [src] + [.claude]; CR-REF-18 DEPRECATION-NOTE.md cluster root check|src/superclaude/, .claude/|FR-CS-6|CR-REF-12 grep PASS; cluster root check PASS|S|P1|
|3|FR-CR-DEP-06|Post-Step-6 one-shot residual-reference manifest (elevated to Must)|Script `scripts/audit/cr_dep_06_manifest.sh` writes `${RELEASE_DIR}/cr-dep-06-residual-manifest.{md,yaml}` enumerating every surviving deprecation-surface string outside authorized leave-as-is buckets|scripts/audit/, ${RELEASE_DIR}/|FR-CS-6|residual count outside authorized buckets = 0 (pre-commit gate); 144 binding occurrences (61 backlog + 83 docs/generated) enumerated; per-bucket disposition; live recount on 2026-05-16 = 153/45 files|M|P0|
|4|NFR-S-3|Makefile sync-rule atomicity with flock|`make sync-dev` + `make verify-sync` MUST acquire exclusive flock on `.claude/skills/.sync-lock`|Makefile, .claude/skills/|FR-CS-6|covers both forward-looking prune-loop race AND LIVE copy-overwrite race at Makefile:121; AC-ATK-16 pytest concurrency fixture PASS; K-04 target 0 flakes across 30 consecutive CI runs|M|P0|
|5|NFR-ME-9|DONOR-CEREMONY DROP AUDIT (Load-bearing)|10 named drops remain dropped; two axes (rejected-pattern + surviving-citation via CR-DEP-06)|src/, .claude/|FR-CR-DEP-06|CR-DEP-01 soft-deprecate audit; CR-DEP-05 grep returns zero on both [src] and [.claude]; R-RULE-11 audit clean; AC-ATK-17 server-side hook|M|P0|
|6|TEST-007|AC-ATK-07 rf-qa F-07 chain test|tests/audit/test_rf_qa_step6_gate.py::test_chain_links|tests/audit/|FR-CS-6|5 chain anchors verified (sprint goal → T06.03 → §2 rubric → §4 traceability → CR-TASK-01..10 + CR-FM-01..03 landed); rf-qa returns PASS pre-Step-6|M|P0|
|7|TEST-016|AC-ATK-16 make sync-dev flock test|tests/audit/test_make_sync_dev_flock.py::test_concurrent_worktree|tests/audit/|NFR-S-3|two parallel make sync-dev subprocesses; flock held during prune; post-prune dir match expected; local + CI matrix|M|P0|
|8|TEST-018|AC-ATK-18 resume content audit + sprint-emit + manifest test|tests/skills/task/test_cr_fm_03_resume_grep.py + tests/cli/test_sprint_emit_legacy_grep.py + tests/audit/test_cr_dep_06_manifest.py|tests/skills/task/, tests/cli/, tests/audit/|FR-CR-DEP-06|(a) Gate-1.5 emission canonical grammar; (b) sprint-emit blocks on content match; (c) post-Step-6 manifest enumerates ≥144 residuals|M|P0|
|9|TEST-028|AC-SM-10 Step-6 commit roster test|tests/audit/test_step_6_commit_roster.py::test_exact_file_list|tests/audit/|FR-CS-6|set-equal to final-merge-plan.md:381 roster|S|P0|
|10|TEST-030|AC-SM-12 step gates + in-flight resume test|tests/audit/test_step_gates.py + tests/skills/task/test_in_flight_mdtm_resume.py|tests/audit/, tests/skills/task/|FR-CR-DEP-06|gates 1/5/6 exit zero; fixture iterates LIVE in-flight count at gate-execution time (NOT hardcoded 25/96/132); 100% resume cleanly under CR-FM-03 shim|M|P0|
|11|MIG-006|Step 6 atomic hard-delete commit (S-3 binding; INV-04 highest exposure)|CR-DEP-03 donor SKILL.md hard-delete + CR-DEP-04 directory absence + `make sync-dev` prune + AC-ATK-16 flock + CR-DEP-06 manifest|src/superclaude/skills/sc-task-protocol/|FR-CS-6, NFR-S-3|AC-SM-10 commit roster PASS; `make verify-sync` returns 0; donor sc-task-protocol/ directory absent from both src/ and .claude/; CR-DEP-06 manifest residual count = 0 outside authorized buckets; rollback granularity: destructive-by-default; roll FORWARD preferred|L|P0|
|12|OPS-002|Runbook R2: Gate-1.5 emission triage|Symptoms: task resume emits gate-1.5: legacy-surface-reference detected|task/SKILL.md|TEST-018|symptoms:resume-emits-gate-1.5-legacy-surface-reference; diagnosis:confirm-token-grammar-AC-ATK-18(b),check-legacy-surface-ack:1-frontmatter,inspect-matched-symbol-CR-DEP-06-disposition; resolution:acknowledge-one-shot-ack-DO-NOT-HALT-ME-3-patch-matched-surface-only-if-disposition-violation; escalation:bucket=src-page-Eng-Lead-30min; prevention:weekly-CR-DEP-06-manifest-re-emit-sprint-emit-boundary-content-grep|S|P1|
|13|OPS-005|Runbook R5: In-flight resume triage|Symptoms: post-merge resume of in-flight MDTM task in 136-file floor|task/SKILL.md|TEST-018, TEST-030|symptoms:resume-of-in-flight-may-emit-gate-1.5-may-ENOENT-related_docs; diagnosis:CR-FM-03-default-shim,Gate-1.5-content-grep,related_docs-find-traversal-emit-gate-1.5-deleted-related-doc; resolution:warn-and-continue,set-legacy-surface-ack:1-after-review,NEVER-HALT-mid-resume; escalation:Eng-Lead-4h-parser-bug-never-block-related_docs-ENOENT; prevention:AC-ATK-18-4-part-fan-out-CR-DEP-06-manifest-archives-weekly|M|P0|
|14|Q-GAP-04|flock portability on macOS/BSD|`flock` is GNU-coreutils only; macOS/BSD lacks it by default|Makefile, scripts/|NFR-S-3|portability fallback documented: `brew install flock` OR `lockfile-create` fallback from procmail-lockfile; FreeBSD `pkg install flock` OR `lockf(1)` semantics; Windows WSL2 yes-out-of-box|S|P0|

### Integration Points — M6

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`flock` exclusive lock on `.claude/skills/.sync-lock`|File-lock primitive|`Makefile` `sync-dev` + `verify-sync` targets|M6|All parallel-worktree sessions; AC-ATK-16 concurrency fixture|
|CR-DEP-06 residual-reference manifest|Audit deliverable file|`${RELEASE_DIR}/cr-dep-06-residual-manifest.{md,yaml}`|M6|Weekly archive to `docs/generated/`; AC-ATK-18(d) closure|
|`gate-1.5: legacy-surface-reference detected`|Resume-time Task Log emission|Runtime emission per match|M6 (activation; foundation at M3)|AC-ATK-18 audit; one-shot ack gate; CR-DEP-06 manifest cross-reference|
|`gate-1.5: deleted-related-doc detected`|`related_docs:` traversal token|Runtime emission per ENOENT|M6|Resume-time path validation; L3 reference layer protection|
|rf-qa F-07 chain-integrity verifier|Subagent invocation (pre-commit)|Step-6 pre-commit gate|M6|AC-ATK-07 closure; procedural chain audit before destructive commit|

### Milestone Dependencies — M6

- M5 landed (donor command stubified; CLI re-routed; sha256 baselines pinned; S-1 discharge complete)
- AC-ATK-07 rf-qa F-07 chain-integrity verifier authored and tested
- Q-GAP-04 `flock` portability fallback documented for macOS / BSD targets

### Open Questions — M6

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|Q-GAP-11|Acknowledgment-gate persistence shape|Schema 5 one-shot ack mechanism affects resume UX; carry-over from M1 if not resolved|§7 / §8 author|Before M6 entry|

### Risk Assessment and Mitigation — M6

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|INV-04 semantic-layer break — H-4 resumed task hits deleted donor file as PRIMARY ARTIFACT|HIGH (HIGHEST EXPOSURE per validation-spec §9 L285)|H|H|AC-ATK-18 four sub-bindings: content-layer grep at resume + sprint-emit boundary content-grep + one-shot ack gate + CR-DEP-06 manifest; H-4 named target `TASK-RESEARCH-20260403-sprint-task-exec` manual walkthrough|Engineering Lead|
|2|R-ATK-16 make sync-dev worktree race — Session A `cp` at Makefile:121 overwrites Session B in-progress edit|HIGH|M|H|`flock -x .claude/skills/.sync-lock` wraps sync-dev + verify-sync; Q-GAP-04 portability fallback documented; AC-ATK-16 concurrency fixture PASS|Engineering Lead|
|3|R-FM-08 donor file-rename evasion — `*.deprecated` rename bypasses absence check|LOW|L|M|CR-DEP-04 enforces `find -type d` returns empty for donor directory (not just file absence); `git diff --diff-filter=D` assertion on Step-6 commit|Engineering Lead|
|4|R-FM-01 symlink defeat of `make verify-sync`|LOW (LOW/HIGH)|L|H|Pre-Step-6 audit: `find src/superclaude/skills .claude/skills -type l` returns empty|Engineering Lead|
|5|R-OPS-02 H-4 manual operator intervention required for named at-risk task|MEDIUM|H|M|AC-ATK-18 pre-flight + pre-flag at-risk task ID `TASK-RESEARCH-20260403-sprint-task-exec` in operator runbook; explicit decision record on freeze/reroute/migrate|rf-qa Lead|
|6|`flock` unavailable on macOS/BSD — AC-ATK-16 cannot run|MEDIUM|M|M|Q-GAP-04: `brew install flock` (macOS) OR `lockfile-create` fallback from procmail-lockfile; Linux out-of-box (util-linux); Windows WSL2 inherits Linux semantics|DevOps|
