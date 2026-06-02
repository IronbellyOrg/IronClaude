# Partition A10 — Release Split + Workflow + PRD/TDD Refactor

**Partition focus:** Release-split RCA + PRD/TDD refactor — input-quality and downstream-coupling failures, plus the two top-level rescrutiny design/workflow files.

**Directories mined:**
1. `.dev/releases/complete/release-split/`
2. `.dev/releases/complete/release-split-workspace-rca/`
3. `.dev/releases/complete/task-builder-merge/`
4. `.dev/releases/complete/cross-framework-deep-analysis/`
5. `.dev/releases/complete/v3.65-prd-refactor/`
6. `.dev/releases/complete/v3.66-tdd-skill-refactor-v2/`
7. Top-level `sc-reflect-rescrutiny-design.md` + `sc-reflect-rescrutiny-workflow.md`

---

## Findings

### F-A10-001: sc:release-split Mode-A invocation was structurally non-adversarial
- **Type:** FAILURE
- **Pipeline step:** debate
- **Symptom:** Part 2 of sc:release-split called `sc:adversarial` in Mode A (`--compare`), passing the proposal and original spec as two existing files. The "adversarial" debate was just two-document comparison; the three roles (Advocate/Skeptic/Pragmatist) existed conceptually but were not mapped to actual agent specs. No multi-model diversity — the same context produced one perspective.
- **Root cause (claimed):** Original release-split design hardcoded Mode A and never wired `--generate` Mode B; debate framing was prose-only, not agent-backed.
- **Remediation applied:** Refactor plan to switch Part 2 to Mode B with `--source --generate --agents` and defaults `opus:architect,haiku:analyzer`; Part 1 brainstorm becomes injected context rather than one of the compared files. Includes Mode-A fallback on failure.
- **Outcome:** Plan dated 2026-03-17, status "Proposed — not yet implemented"; reflection pass added 6 findings (return-contract field count, prerequisites phase, generate-type compatibility, convergence threshold alignment, parsing-algorithm reference, error-handling table).
- **Still possible today (Auggie check):** UNKNOWN — refactor was proposed but the artifact does not certify it shipped; verification against current src/superclaude/skills/sc-release-split-protocol/SKILL.md was not performed in this partition.
- **Source artifacts:** `.dev/releases/complete/release-split/release-split-agents-refactor-plan.md` §1-§4; Appendix A reflection table.

### F-A10-002: `--generate split-proposal` was an unrecognized adversarial artifact type
- **Type:** FAILURE
- **Pipeline step:** generate-opus-architect
- **Symptom:** Original refactor plan specified `--generate split-proposal` for sc:adversarial Mode B invocation. sc:adversarial's `--generate` flag expects recognized artifact types (`roadmap`, `spec`, `design`, etc.). An unknown value risks runtime failure if the consumer validates against a fixed list.
- **Root cause (claimed):** Cross-skill contract mismatch — release-split invented a new generate-type without checking the adversarial allowlist.
- **Remediation applied:** Plan amended to use `--generate spec` and rely on agent-instruction context to shape output as a split proposal (Design Decision D6).
- **Outcome:** Caught by reflection before implementation. Plan now Section 4.2E step 4.
- **Still possible today (Auggie check):** UNKNOWN — adversarial generate-type allowlist not enumerated in this partition's artifacts.
- **Source artifacts:** `.dev/releases/complete/release-split/release-split-agents-refactor-plan.md` Finding 3, Design Decision D6.

### F-A10-003: Convergence thresholds drifted across sibling skills
- **Type:** FAILURE
- **Pipeline step:** score
- **Symptom:** Original release-split plan used 0.7/0.5 PASS/PARTIAL thresholds; sc:roadmap uses 0.6/0.5. Differing thresholds across skills creates confusion with no documented justification.
- **Root cause (claimed):** No cross-skill threshold-policy authority; each skill picked its own.
- **Remediation applied:** Adopt sc:roadmap thresholds (≥0.6 PASS, 0.5-0.59 PARTIAL with interactive gate, <0.5 FAIL/abort).
- **Outcome:** Plan amended (Design Decision D7).
- **Still possible today (Auggie check):** YES (INFERENTIAL) — no centralized threshold table exists; new skills may pick arbitrary thresholds. Inference based on absence of cross-skill policy reference in current artifacts.
- **Source artifacts:** `.dev/releases/complete/release-split/release-split-agents-refactor-plan.md` Finding 4, D7.

### F-A10-004: Adversarial return-contract had 9 fields; release-split consumed only 4
- **Type:** FAILURE
- **Pipeline step:** merge
- **Symptom:** Release-split Mode B consumer planned to read only 4 of 9 fields returned by sc:adversarial (`status`, `merged_output_path`, `convergence_score`, `artifacts_dir`). Missing: `base_variant`, `unresolved_conflicts`, `fallback_mode`, `failure_stage`, `invocation_method` — silently dropping observability signals.
- **Root cause (claimed):** Consumer authored without enumerating producer contract; partial consumption was not flagged by any schema.
- **Remediation applied:** Plan expanded to consume all 9 fields with documented consumer defaults (Section 4.3 Return Contract Consumption table).
- **Outcome:** Caught by reflection Finding 1.
- **Still possible today (Auggie check):** YES (INFERENTIAL) — no schema validation enforces full contract consumption; pattern will recur for any new skill consuming sc:adversarial without explicit field enumeration.
- **Source artifacts:** `.dev/releases/complete/release-split/release-split-agents-refactor-plan.md` Finding 1, Section 4.3.

### F-A10-005: skill-creator plugin wrote eval workspace into `.claude/skills/` (governance violation)
- **Type:** FAILURE
- **Pipeline step:** OTHER (skill-creator harness output placement)
- **Symptom:** ~100 eval artifacts (`iteration-1/`, `with_skill/`, `without_skill/`, `eval_metadata.json`, `grading.json`, `benchmark.json`, plus bespoke `fidelity_checker.py`) landed under `.claude/skills/sc-release-split-protocol-workspace/` instead of `.dev/eval-workspaces/`. Workspace was committed alongside the skill (commit `6c84826`, 2026-03-18).
- **Root cause (claimed):** Anthropic's vendored `skill-creator` plugin hardcodes "Put results in `<skill-name>-workspace/` as a sibling to the skill directory" (SKILL.md L167). No override flag, no env var, no argparse default — convention is enforced by prompting only. IronClaude had no PreToolUse hook, no `.gitignore` entry, no CLAUDE.md override.
- **Remediation applied:** Five-layer fix: (R1) `.dev/README.md` documents `.dev/eval-workspaces/`; (R2) Makefile `verify-sync` extended with context-aware "no SKILL.md — move to .dev/eval-workspaces/" message; (R3) CI wiring of verify-sync + lint-architecture in `quick-check.yml`; (R4) `*-workspace` suffix blocklist; (R5) PreToolUse hook in `.claude/settings.json` rejecting writes to `.claude/skills/*-workspace/**`; (R6) `make eval-skill SKILL=<name>` convenience target; (R7) CLAUDE.md addendum explicitly overriding skill-creator sibling convention. Tracked in 5-phase tasklist `release-split-workspace-rca/` with 21 tasks.
- **Outcome:** Workspace physically relocated (commit `86d2749`); preventive 5-phase remediation tasklist generated and validated (validation report: 14 findings, 14 RESOLVED, 0 blocking). Sprint-ready.
- **Still possible today (Auggie check):** NO (INFERENTIAL) — remediation R5 (PreToolUse hook) provides mechanical enforcement; verification against `.claude/settings.json` not performed in this partition.
- **Source artifacts:** `.dev/releases/complete/release-split-workspace-rca/rca-2-eval-harness.md` F1-F5; `rca-3-naming-convention.md` F1-F11; `tasklist-index.md`; `validation/ValidationReport.md`.

### F-A10-006: `make verify-sync` error message misled authors to wrong fix
- **Type:** FAILURE
- **Pipeline step:** wiring-verification
- **Symptom:** When `.claude/skills/<name>-workspace/` existed without a matching `src/superclaude/skills/<name>-workspace/`, verify-sync emitted "MISSING in src/superclaude/skills/: <name> (not distributable!)". This implies the author forgot to add a skill to src/. The actual failure is the opposite: the directory is not a skill and shouldn't be in `.claude/skills/` at all. A diligent author would respond by copying the workspace into src/ — making the bug worse.
- **Root cause (claimed):** Error message assumed only one failure shape (sync drift), never anticipated misplaced non-skill artifacts.
- **Remediation applied:** D2.1 — replace message with context-aware "no SKILL.md — not a skill, must not live here. Move to .dev/eval-workspaces/."
- **Outcome:** Roadmap M2 row 21 specifies verbatim message (em-dash U+2014); Validation Report M1/M2/M3 enforce byte-exact match across roadmap → tasklist → AC chain.
- **Still possible today (Auggie check):** NO (INFERENTIAL) — tracked-to-completion in release-split-workspace-rca tasklist with verbatim-message ACs.
- **Source artifacts:** `release-split-workspace-rca/rca-3-naming-convention.md` F6; `validation/ValidationReport.md` M1-M3.

### F-A10-007: verify-sync existed but was opt-in; no CI invoked it
- **Type:** FAILURE
- **Pipeline step:** wiring-verification
- **Symptom:** The mechanical safety net to catch misplaced non-skill directories existed in the Makefile but was never invoked by any CI workflow (`quick-check.yml`, `test.yml`, `publish-pypi.yml`, `pull-sync-framework.yml`). Mechanical detection without invocation is decorative.
- **Root cause (claimed):** Governance gap — Makefile target authored without corresponding CI wiring.
- **Remediation applied:** D2.3 — wire `make verify-sync` and `make lint-architecture` into `.github/workflows/quick-check.yml` as PR-blocking gates.
- **Outcome:** Roadmap M2 row 23; tasklist T02.03.
- **Still possible today (Auggie check):** UNKNOWN — CI workflow state not verified in this partition.
- **Source artifacts:** `release-split-workspace-rca/rca-3-naming-convention.md` F6; `tasklist-index.md` R-006.

### F-A10-008: task-builder-merge declared zero obligations via manual override
- **Type:** REMEDIATION
- **Pipeline step:** anti-instinct
- **Symptom:** Anti-instinct audit auto-detection returned 0 contracts because the audit's regex did not match this release's M1 contract-freeze row pattern. Manual override declared 7 integration contracts (IC-001 through IC-007) to align audit with documented release scope.
- **Root cause (claimed):** Anti-instinct scanner's contract-detection regex is brittle to roadmap formatting variants; assumes a single canonical row shape.
- **Remediation applied:** `manual_declaration: true` flag in frontmatter with `manual_declaration_reason` explaining the auto-detection miss; 7 IC contracts declared by hand citing roadmap rows.
- **Outcome:** Audit reports 7/7 contracts covered; fingerprint coverage 0.81 (above 0.7 threshold). Audit passes — but only because the human did the work the scanner was supposed to do.
- **Still possible today (Auggie check):** YES (INFERENTIAL) — the scanner's regex is unchanged unless a separate task addressed it; future releases will recur unless the scanner is generalized.
- **Source artifacts:** `.dev/releases/complete/task-builder-merge/anti-instinct-audit.md` lines 1-13 (frontmatter), lines 31-42 (contract table).

### F-A10-009: 30/155 fingerprints missing from roadmap (framework identifiers)
- **Type:** REMEDIATION
- **Pipeline step:** anti-instinct
- **Symptom:** Anti-instinct fingerprint coverage at 0.81 (125/155); 30 missing fingerprints including `fix_authorization`, `audit_trail`, `PRD_TASK_BUILDER_CONVERGENCE`, `MTTR`, `MTBF`, `QA_GATE_REQUIREMENTS`, etc.
- **Root cause (claimed):** Fingerprint set pulled from broader documentation namespace that this convergence release doesn't directly reference. Above-threshold; non-blocking.
- **Remediation applied:** NONE — accepted as "framework-level identifiers not load-bearing for this release."
- **Outcome:** Passed (above 0.7 threshold).
- **Still possible today (Auggie check):** YES — fingerprint set is namespace-wide; smaller releases will continue to fall short of 100% without local-scope override.
- **Source artifacts:** `task-builder-merge/anti-instinct-audit.md` lines 44-72.

### F-A10-010: spec-deviation classifier produced 1 AMBIGUOUS from malformed manifest token
- **Type:** FAILURE
- **Pipeline step:** deviation-analysis
- **Symptom:** Deviation analyzer flagged `src/\` (trailing escape, no character) as a missing-in-roadmap file. Token is a spec-extraction artifact, not a real deliverable.
- **Root cause (claimed):** Spec extractor's tokenizer leaks malformed path tokens that resemble real file paths.
- **Remediation applied:** Classified AMBIGUOUS, no-action; recommends re-extracting spec manifest in a future pass. No upstream fix to tokenizer.
- **Outcome:** Routed to no-action; release closed cleanly.
- **Still possible today (Auggie check):** YES — extractor not changed in this partition; tokenization artifacts will continue leaking into deviation analysis.
- **Source artifacts:** `task-builder-merge/spec-deviations.md` lines 26-32.

### F-A10-011: 2 PRE_APPROVED template files appeared as deviations every release
- **Type:** FAILURE
- **Pipeline step:** deviation-analysis
- **Symptom:** `src/superclaude/examples/prd_template.md` and `tdd_template.md` flagged as "in spec manifest not found in roadmap." These are input scaffolding for skill consumers, not implementation deliverables. They get flagged on every release that touches PRD/TDD scope.
- **Root cause (claimed):** Spec extractor treats every `src/` path as a candidate deliverable; deviation analyzer has no notion of "input vs output scaffolding."
- **Remediation applied:** Manual PRE_APPROVED classification with rationale; no architectural fix.
- **Outcome:** No-action this release; will recur next release.
- **Still possible today (Auggie check):** YES — extractor lacks scaffolding-aware filter; pattern will recur on every PRD/TDD release.
- **Source artifacts:** `task-builder-merge/spec-deviations.md` lines 34-46.

### F-A10-012: 4 INTENTIONAL portfolio-NFR carryovers flagged as deviations
- **Type:** FAILURE
- **Pipeline step:** spec-fidelity
- **Symptom:** Spec NFRs `security:encryption`, `security:hash`, `threshold:<1%`, `threshold:<2%` flagged as "not addressed in roadmap." All four are portfolio-wide NFRs that this release does not measure or commit against.
- **Root cause (claimed):** Spec-fidelity layer treats all NFRs uniformly; no concept of portfolio-wide carryover vs release-scoped NFR.
- **Remediation applied:** Manual INTENTIONAL classification each release; no architectural fix.
- **Outcome:** No-action this release; will recur on every release that inherits portfolio NFRs.
- **Still possible today (Auggie check):** YES — same as F-A10-011; spec/roadmap alignment layer lacks scope-boundary semantics.
- **Source artifacts:** `task-builder-merge/spec-deviations.md` lines 48-74.

### F-A10-013: TFEP run-1 found 5 failures, 2 were test expectation defects vs 3 implementation defects
- **Type:** REMEDIATION
- **Pipeline step:** OTHER (test failure escalation protocol)
- **Symptom:** 5 simultaneous test failures in `tests/roadmap/test_obligation_scanner_meta_context.py` triggered TFEP escalation. Forensic RCA found mixed-cause cluster: 2 expectation-side defects (line-level negation classification working as intended), 3 implementation defects (discharge-line obligation creation, brittle component matching, code-block context loss in section slicing).
- **Root cause (claimed):** Interaction effects between FR-MOD1.9 additions (meta-context classifier) and pre-existing scanner mechanics. Line-level vs clause-scoped policy ambiguity.
- **Remediation applied:** TFEP forensic block T1-T5 in `tasklist-insertion.md`; escalation status = "forensic success, remediation pending user approval due test_is_wrong: true."
- **Outcome:** Diagnosis complete (≥0.9 confidence); remediation requires user authorization to alter test expectations.
- **Still possible today (Auggie check):** UNKNOWN — current `obligation_scanner.py` would need symbolic inspection to confirm fixes shipped; verification not performed in this partition.
- **Source artifacts:** `v3.65-prd-refactor/tfep-run-1/tfep-incident-report.md`; `tfep-run-1/rca-verdict.md`.

### F-A10-014: TFEP run-2 — discharge-intent skip dropped MEDIUM obligations before classification
- **Type:** REMEDIATION
- **Pipeline step:** OTHER (test failure debugging)
- **Symptom:** After run-1 remediation, 2 failures remained. RCA: (H1 CONFIRMED) `_is_discharge_intent_line` triggers `continue` in `scan_obligations`, dropping inline-code scaffold matches before MEDIUM demotion can run. (H3 CONFIRMED) test fixture `mock_data` not matched by word-bounded regex `\bmock(?:ed|s)?\b` because `_` is a word character. Mixed-cause: implementation defect + test defect.
- **Root cause (claimed):** Run-1 remediation introduced over-broad discharge-intent skip; that new branch shadowed legitimate inline-code obligations. Test expectation incompatible with strict FR-MOD1.1 vocabulary semantics.
- **Remediation applied:** Recommended path: narrow the skip; preserve FR-MOD1.1 vocabulary boundaries; align the one out-of-policy test fixture/expectation. Workflow-meta-context-fix.md authored as 9-task remediation plan.
- **Outcome:** Diagnostic complete with high confidence; remediation tracked in workflow file.
- **Still possible today (Auggie check):** UNKNOWN — current scanner state not verified in this partition.
- **Source artifacts:** `v3.65-prd-refactor/tfep-run-2/rca-verdict.md`; `workflow-meta-context-fix.md`.

### F-A10-015: Duplicate-headings gate falsely rejected real roadmap (H3 same-name under different H2s)
- **Type:** FAILURE
- **Pipeline step:** generate-opus-architect (merge-gate)
- **Symptom:** `_no_duplicate_headings` in `gates.py` treated all H3s globally; prd-refactor roadmap had legitimate H3s like "Acceptance Criteria" appearing under multiple distinct H2 sections. Gate rejected the real roadmap as malformed.
- **Root cause (claimed):** Original duplicate-check was global, not section-scoped. H2 should be global-unique; H3 should be unique-within-parent-H2.
- **Remediation applied:** workflow-gate-fix.md — 7-task remediation: rewrite `_no_duplicate_headings` with section-scoped H3 tracking, change return type from `bool` to `bool|str` for diagnostic line numbers, update consumer in `pipeline/gates.py` to handle string returns, update 4 existing test assertions from `is False` to `is not True`, add 10-test `TestNoDuplicateHeadingsScoped` class, regression test against the real failing roadmap.
- **Outcome:** Workflow fully specified with dep graph; estimated ~115 LOC across 5 files.
- **Still possible today (Auggie check):** UNKNOWN — current `gates.py` not inspected in this partition.
- **Source artifacts:** `v3.65-prd-refactor/workflow-gate-fix.md` Tasks 1-7.

### F-A10-016: Spec-drift analysis (commit b942d50) caught silent /task contract change
- **Type:** SUCCESS
- **Pipeline step:** spec-fidelity
- **Symptom:** Mid-release, commit b942d50 modified the /task skill (post-completion validation, non-delegable F1 loop, new `rf-qa-qualitative` agent type). Standard freshness-risk scan caught the drift. 10-section × 6-change-group scoring matrix (60 evaluations) + 8 adversarial debates (every score ≥3) produced verdict: SPEC IS VALID, 6 lightweight acknowledgement annotations recommended.
- **Root cause (claimed):** Spec freshness risk is real but in this case the changes were orthogonal to the PRD refactoring (E2E test compares same /task version on both monolithic and refactored inputs).
- **Remediation applied:** 6 annotations to spec (Stage B note, out-of-scope rf-qa-qualitative declaration, dependency-graph comment, freshness-risk row, E2E test note, migration/downstream notes).
- **Outcome:** SUCCESS — spec preserved; freshness risk documented; no structural refactoring needed. Demonstrates that adversarial debate per flagged section pair is the right gate for "is this drift real?"
- **Still possible today (Auggie check):** YES — this methodology can be reused; pattern preserved as living documentation.
- **Source artifacts:** `v3.65-prd-refactor/spec-drift-analysis-b942d50.md` §1-§5.

### F-A10-017: anti-instinct audit on v3.65 ran with 1 contract, 18 fingerprints (under-instrumented)
- **Type:** REMEDIATION
- **Pipeline step:** anti-instinct
- **Symptom:** v3.65 anti-instinct audit: 0 obligations, 1 contract, 18 fingerprints (13/18 = 0.72 coverage). Missing fingerprints: `WHAT`, `ENCODE`, `GRANULARITY`, `ESCALATION`, `MDTM`. Coverage just barely above 0.7 threshold.
- **Root cause (claimed):** Tiny contract surface for a documentation-refactor release; threshold tuned for bigger releases.
- **Remediation applied:** NONE — passed at floor.
- **Outcome:** Passed.
- **Still possible today (Auggie check):** YES — coverage threshold is uniform across release sizes; doc-only releases will skim the floor.
- **Source artifacts:** `v3.65-prd-refactor/anti-instinct-audit.md`.

### F-A10-018: v3.66 spec-deviations: 14 findings UNCLASSIFIED, hex stable_ids vs gate-required DEV-N
- **Type:** FAILURE
- **Pipeline step:** deviation-analysis
- **Symptom:** Spec-deviations report listed 14 findings all classified UNCLASSIFIED (counts: SLIP=0, INTENTIONAL=0, PRE_APPROVED=0, AMBIGUOUS=0). IDs were hex stable_ids (e.g., `cb46b85f46821f30`) instead of gate-required `DEV-\d+` pattern. `routing_fix_roadmap` and `routing_no_action` frontmatter fields blank.
- **Root cause (claimed):** `_run_deviation_analysis` in `executor.py` populates `records` but never runs classification logic, never assigns DEV-N IDs, never builds `id_mapping` sidecar. Pipeline DEVIATION_ANALYSIS_GATE's `_routing_ids_valid` check fails on hex IDs.
- **Remediation applied:** Phase-1 tasklist (3 tasks): T01.01 classification loop (status==ACTIVE+no debate_verdict→SLIP, debate_verdict→INTENTIONAL, else→AMBIGUOUS); T01.02 DEV-N ID assignment after sorting by stable_id for determinism, plus `id_mapping` dict in sidecar; T01.03 regression test.
- **Outcome:** Tracked in `v3.66-tdd-skill-refactor-v2/tasklist-pipeline-fix/phase-1-deviation-analysis.md`.
- **Still possible today (Auggie check):** UNKNOWN — current `executor.py` not symbolically inspected in this partition.
- **Source artifacts:** `v3.66-tdd-skill-refactor-v2/spec-deviations.md`; `tasklist-pipeline-fix/phase-1-deviation-analysis.md` T01.01-T01.03.

### F-A10-019: v3.66 certify step was unwired; pipeline silently ended at remediate
- **Type:** FAILURE
- **Pipeline step:** certify
- **Symptom:** `_build_steps()` in `executor.py` ends at the remediate step (line 1553 comment claims "constructed dynamically" but no code does this). `roadmap_run_step` has no `step.id == "certify"` dispatch. Pipeline completes without emitting `certification-report.md`. CERTIFY_GATE never runs.
- **Root cause (claimed):** Certify step was specified but never wired. Earlier work added `build_certify_step()` helper and `generate_certification_report()` formatter but no orchestration.
- **Remediation applied:** Phase-2 tasklist: T02.01 add Step to `_build_steps` and handler `_run_certify_step` reading remediation sidecar to infer mode (`tasklist-only` if all findings PENDING, `applied` if any FIXED/FAILED); T02.02 update CERTIFY_GATE to be mode-aware (require `certification_scope: analysis-only` alongside `certified: true` in tasklist-only mode to prevent gaming).
- **Outcome:** Tracked in `v3.66-tdd-skill-refactor-v2/tasklist-pipeline-fix/phase-2-certify-wiring.md`.
- **Still possible today (Auggie check):** UNKNOWN — current `executor.py` `_build_steps` not inspected in this partition.
- **Source artifacts:** `v3.66-tdd-skill-refactor-v2/tasklist-pipeline-fix/phase-2-certify-wiring.md` T02.01-T02.03.

### F-A10-020: DeviationRegistry.load_or_create crashed on legacy list-format findings
- **Type:** FAILURE
- **Pipeline step:** spec-fidelity (convergence loop)
- **Symptom:** `convergence.py:111` calls `findings.items()` assuming dict. If `findings` is a list (legacy format or corruption), crashes with `AttributeError: 'list' object has no attribute 'items'`. The fix in `executor.py` handled this for deviation-analysis but the convergence path didn't.
- **Root cause (claimed):** Two parallel call sites (executor + convergence) loading the same registry shape; only one was hardened.
- **Remediation applied:** T03.01 in `phase-3-hardening-verification.md` — normalization at convergence.py:111: `if isinstance(findings, list): findings = {f.get("stable_id", str(i)): f for i, f in enumerate(findings)}`.
- **Outcome:** Tracked; pending verification.
- **Still possible today (Auggie check):** UNKNOWN — `convergence.py` not symbolically inspected in this partition.
- **Source artifacts:** `v3.66-tdd-skill-refactor-v2/tasklist-pipeline-fix/phase-3-hardening-verification.md` T03.01.

### F-A10-021: spec-fidelity crashed with empty findings_by_file dict
- **Type:** FAILURE
- **Pipeline step:** remediate
- **Symptom:** `execute_remediation` in `remediate_executor.py:753` does `ThreadPoolExecutor(max_workers=len(all_target_files))`. When findings have no `files_affected` (orphaned findings), `all_target_files` is empty → `max_workers=0` → ValueError crash. Pipeline halts hard.
- **Root cause (claimed):** No defensive guard for empty target-file set; `findings_by_file` can be empty either because all findings lack file associations or because the grouping loop produced no entries.
- **Remediation applied:** 3-task surgical fix (T01-T03 in `tasklist-spec-fidelity-bugfix.md`): defense-in-depth early-returns at both the caller (`_run_remediation` in `executor.py:946`) and callee (`execute_remediation` in `remediate_executor.py:753`); return `("PARTIAL", [])` matching documented contract. Plus T03 fixed `run_semantic_layer` call signature mismatch (`got unexpected keyword argument 'spec_path'`) by parsing files via `split_into_sections`.
- **Outcome:** Tracked in tasklist; pending verification.
- **Still possible today (Auggie check):** UNKNOWN — `remediate_executor.py` not inspected in this partition.
- **Source artifacts:** `v3.66-tdd-skill-refactor-v2/tasklist-spec-fidelity-bugfix.md` T01-T04.

### F-A10-022: cross-framework-deep-analysis spec-fidelity flagged 15 deviations (3 HIGH)
- **Type:** FAILURE
- **Pipeline step:** spec-fidelity
- **Symptom:** Roadmap diverged from spec in 15 places (3 HIGH, 8 MEDIUM, 4 LOW). HIGH deviations: (DEV-001) Phase 0 added with no spec basis; (DEV-002) OQ-001 through OQ-008 introduced as binding resolutions vs spec's 3 OI items; (DEV-003) `improvement_backlog_schema` 11-field definition not enumerated, replaced with undefined "AC-010 schema" reference. `tasklist_ready: false`.
- **Root cause (claimed):** Roadmap generator extended spec scope without flagging the additions as scope-extensions vs scope-implementations. No mechanism to require spec patches when roadmap adds binding gate criteria.
- **Remediation applied:** Per-DEV recommended corrections (e.g., DEV-001: add Phase 0 to spec OR absorb into Phase 1; DEV-002: align OQ to OI items, scope OQ-004 through OQ-008 as implementation decisions; DEV-003: cite §5.3 directly, remove undefined "AC-010").
- **Outcome:** 15 actionable corrections registered; tasklist gated until HIGH resolutions land.
- **Still possible today (Auggie check):** YES — pattern is structural (roadmap generators have no "this adds binding scope" detection); will recur on every multi-phase release.
- **Source artifacts:** `cross-framework-deep-analysis/spec-fidelity.md` DEV-001 through DEV-015.

### F-A10-023: cross-framework Phase 2 stalled at 5m47s with 870KB output, 0 events
- **Type:** FAILURE
- **Pipeline step:** OTHER (executor stall detection)
- **Symptom:** Phase 2 diagnostic: stall_seconds=347, output_bytes=869959, events_received=0, growth_rate_bps=12606, files_changed=0. Sub-agent was emitting massive evidence.md Write content (~145KB of file:line citations for 14 Auggie MCP queries) inline as a single tool_use — the executor's stall detector interpreted "no event progress" as a stall.
- **Root cause (claimed):** Stall detector counts events, not bytes; large single Write operations look like stalls. Sub-agent design pattern that batches all evidence into one Write is incompatible with event-based liveness.
- **Remediation applied:** NONE in this artifact; failure was observable in `results/phase-2-diagnostic.md` but no remediation linked.
- **Outcome:** Exit code 1 reported; downstream impact unclear from this artifact.
- **Still possible today (Auggie check):** YES (INFERENTIAL) — stall-detection criteria appear unchanged based on artifact absence of remediation linkage.
- **Source artifacts:** `cross-framework-deep-analysis/results/phase-2-diagnostic.md` lines 1-29.

### F-A10-024: sc:reflect emitted destructive command despite session context
- **Type:** FAILURE
- **Pipeline step:** OTHER (reflect recommendation gate)
- **Symptom:** Bug-of-record: `/sc:reflect` emitted `pct start 300` against a CTID the session had twice asserted to be a Proxmox template. Templates reject `start`. The reflection's validation pass treated its own emitted command as commentary, not as artifact-under-review.
- **Root cause (claimed):** Reflect's validation phase introspected the reflection itself, not the recommendations the reflection produced. No re-scrutiny layer existed between Reflect and Document phases.
- **Remediation applied:** Design doc `sc-reflect-rescrutiny-design.md` — new behavioral phase "Recommendation Re-scrutiny" between Reflect and Document. Activation on detected CLI verbs against allowlisted tools (hypervisor, k8s, VCS, package managers, frontend, Unreal, Unity, cloud, IaC, DB, HTTP, filesystem-destructive). Steps: Extract (verb/object/flags), Session-fact pass (in-context conversation review), External-fact pass (context7/WebSearch when allowlisted verb has no session fact), Decision gate (PASS/HEDGE/BLOCK stratified by LOW/MEDIUM/HIGH stakes).
- **Outcome:** Design merged from `/sc:brainstorm` adversarial debate (Proposal A recursive validation + B-lite session-fact + C-conditional external lookup). Workflow file `sc-reflect-rescrutiny-workflow.md` sequences 17 discrete edits across design doc (Waves 1-4) and `reflect.md` (Wave 5) with sync chain.
- **Still possible today (Auggie check):** UNKNOWN — current `reflect.md` not inspected in this partition.
- **Source artifacts:** `sc-reflect-rescrutiny-design.md` §1, §3.1-§3.6; `sc-reflect-rescrutiny-workflow.md` Wave 1-Wave 5.

### F-A10-025: Re-scrutiny design's variable resolution was under-specified (hedge H1)
- **Type:** REMEDIATION
- **Pipeline step:** anti-instinct (self-review)
- **Symptom:** Original re-scrutiny design §3.3 said "Resolve variable references where possible (`$CTID` from a heredoc array → concrete CTID)." Ambiguous about what counts as "resolvable" and what to do when resolution depends on `$(...)`, env interpolation, or cross-file construction.
- **Root cause (claimed):** Specification gap — variable resolution boundary undefined.
- **Remediation applied:** Tiered policy: resolve eagerly only for literal-in-scope values (heredoc array entries, immediate `VAR=value` above use site, let-binding fixed values); mark `<unresolved>` and route to HEDGE for command substitution, env interpolation, multi-step construction; never PASS a tuple with `<unresolved>` object.
- **Outcome:** Patched into design doc per workflow Task 2.
- **Still possible today (Auggie check):** UNKNOWN — implementation status of reflect.md propagation not verified.
- **Source artifacts:** `sc-reflect-rescrutiny-design.md` §3.3; workflow Task 2.

### F-A10-026: Re-scrutiny activation rule risked recursive self-triggering on its own examples
- **Type:** REMEDIATION
- **Pipeline step:** anti-instinct (self-review)
- **Symptom:** Activation rule fired on any CLI verb in fenced code blocks. The design doc's own §3.2 verb allowlist table and §5 worked examples contain CLI verbs that would re-trigger the rule when the design itself was reviewed by reflect.
- **Root cause (claimed):** No false-positive exclusion for documentation about the gate.
- **Remediation applied:** B5 fix — exclude past-tense verbs, hedging/framing words (`would`, `caught`, `rejected`, `blocked`, `example`, `imagine`), quote blocks introduced by `> **Re-scrutiny caught:**`, and sections marked as worked examples / table cells / audit-annotation examples.
- **Outcome:** Patched into design doc per workflow Task 1.
- **Still possible today (Auggie check):** UNKNOWN — implementation status of reflect.md propagation not verified.
- **Source artifacts:** `sc-reflect-rescrutiny-design.md` §3.1; workflow Task 1.

### F-A10-027: v3.66 validation report — agents disagreed on interleave ratio (0.60 vs 1.0)
- **Type:** REMEDIATION
- **Pipeline step:** generate-sonnet-architect (validation)
- **Symptom:** Heterogeneous adversarial validation: Agent A (opus-architect) computed interleave_ratio = 3/5 = 0.60 (counted phases with file-level deliverables); Agent B (haiku-architect) computed 5/5 = 1.0 (counted any phase with concrete tasks). Definitional disagreement, not severity disagreement.
- **Root cause (claimed):** "Deliverable" ambiguous between "phase producing new/modified files" and "phase with any observable output." Validation formula does not pin the definition.
- **Remediation applied:** CONFLICT routing — resolved as non-blocking, adopt Agent A's stricter 0.60 as canonical (provides more meaningful signal).
- **Outcome:** Roadmap marked tasklist-ready; 4 WARNINGs documented but non-blocking.
- **Still possible today (Auggie check):** YES (INFERENTIAL) — validation formula's deliverable-counting semantic remains under-specified; future runs will hit same disagreement.
- **Source artifacts:** `v3.66-tdd-skill-refactor-v2/validate/validation-report.md` F-11 CONFLICT resolution.

### F-A10-028: Phase 5 over-bundling and Phase 3 compound task flagged by independent agents
- **Type:** REMEDIATION
- **Pipeline step:** generate-sonnet-architect (validation)
- **Symptom:** Agent A flagged Phase 3 Task 3 as compound (two distinct removals: Effective Prompt Examples block + tier table rows). Agent B independently flagged Phase 5 as bundling sync + parity + file checks + evidence + atomic commit. Different phases, same decomposition concern.
- **Root cause (claimed):** Roadmap generator lacks task-granularity heuristic; bundles independently verifiable outputs into single tasks.
- **Remediation applied:** WARNINGs only; no immediate fix (Phase 5 bundling persisted into execution).
- **Outcome:** Cosmetic refinement deferred; tasklist still ready.
- **Still possible today (Auggie check):** YES — roadmap generator's task-granularity heuristic unchanged; future roadmaps will recur.
- **Source artifacts:** `v3.66-tdd-skill-refactor-v2/validate/validation-report.md` F-07, F-09.

### F-A10-029: SC-5 keyword list internally inconsistent in extraction
- **Type:** FAILURE
- **Pipeline step:** extract
- **Symptom:** `extraction.md` SC-5 row listed 3 prohibited terms (`Stage A`, `rf-task-builder`, `subagent`) while NFR-TDD-CMD.2 in the same file listed 4 (`Stage A`, `Stage B`, `rf-task-builder`, `subagent`). Roadmap Phase 2 Task 3 and test-strategy BT-01 correctly included all 4.
- **Root cause (claimed):** Extraction step did not cross-validate row content against NFR clauses; SC-5 was hand-authored and drifted from its source NFR.
- **Remediation applied:** F-06 fix — add `Stage B` to SC-5's measurement method column. Caught by Agent A (haiku-architect) in validation.
- **Outcome:** Flagged WARNING; roadmap still ready but with documented inconsistency.
- **Still possible today (Auggie check):** YES — extraction layer lacks cross-row consistency check; pattern will recur whenever SC rows reference NFR-defined sets.
- **Source artifacts:** `v3.66-tdd-skill-refactor-v2/validate/validation-report.md` F-06.

### F-A10-030: Anti-instinct ID-convention drift between roadmap M1 and M2+ rows (IC-007)
- **Type:** REMEDIATION
- **Pipeline step:** anti-instinct
- **Symptom:** Roadmap uses bare-ID format (`API-001`) for M1 contract-freeze anchors but scoped-suffix format (`API-001-M2`) for M2+ implementation rows. Downstream splitters keying on bare ID would conflate the two; splitters must key on full row identity.
- **Root cause (claimed):** Lack of explicit ID-convention documentation; convention was inferred from row structure.
- **Remediation applied:** IC-007 declared as integration contract with explicit "Documented convention; downstream splitters MUST key on full row identity, not bare ID."
- **Outcome:** Contract covered; convention now documented.
- **Still possible today (Auggie check):** YES — convention is documentary, not enforced; new splitters will recur on bare-ID assumption.
- **Source artifacts:** `task-builder-merge/anti-instinct-audit.md` IC-007 row.

---

## Cross-cutting patterns within this partition

- **Generator/consumer contract drift goes uncaught** — release-split consumed 4 of 9 adversarial return fields (F-A10-004); convergence thresholds drifted across sibling skills (F-A10-003); roadmap generators add binding gate criteria without spec patches (F-A10-022, DEV-001/DEV-002/DEV-006). No schema validation on cross-skill artifact contracts.
- **Manual overrides paper over scanner deficiencies** — anti-instinct audit on task-builder-merge required manual declaration of 7 contracts (F-A10-008); v3.66 spec-deviations required full hand-classification of 14 UNCLASSIFIED findings (F-A10-018). The scanner gates pass only because humans do the work the scanners were supposed to do.
- **Plugin/harness conventions override project conventions when no enforcement layer exists** — skill-creator's hardcoded sibling-workspace path placed ~100 artifacts in `.claude/skills/` despite CLAUDE.md's output-paths rule (F-A10-005). The CLAUDE.md rule was instructional, not mechanical; the hook layer was absent. See F-A10-006/F-A10-007 for the misleading error message and CI gap.
- **Test-failure expectations vs implementation defects co-occur and are hard to disentangle** — TFEP run-1 (F-A10-013) mixed 2 expectation defects with 3 implementation defects; run-2 (F-A10-014) mixed 1 implementation defect with 1 test-vocabulary mismatch. Both required forensic decomposition; neither was auto-resolvable.
- **Validation formulas are under-specified, producing definitional disagreements rather than severity disagreements** — interleave ratio (F-A10-027) had Agent A at 0.60 and Agent B at 1.0 because "deliverable" was undefined; SC-5 keyword list (F-A10-029) was internally inconsistent across the same extraction file.
- **Pipeline steps can be specified, helped-functioned, and tested without ever being wired** — v3.66 certify step (F-A10-019) had `build_certify_step()` and `generate_certification_report()` but no orchestration call; pipeline silently ended at remediate. v3.65 duplicate-headings gate (F-A10-015) was wired but the function-level definition was wrong (global vs section-scoped). Both reflect missing end-to-end smoke gates on the pipeline graph.
- **Spec-to-roadmap fidelity gate flags portfolio-NFRs as deviations every release** — 4 INTENTIONAL NFRs (F-A10-012), 2 PRE_APPROVED templates (F-A10-011), 1 AMBIGUOUS malformed token (F-A10-010) recur because the fidelity layer has no notion of scope-boundary semantics; each release rerouts them manually.

## Brittleness drivers identified

- **No cross-skill artifact-contract schema validation.** sc:adversarial returns 9 fields; release-split documents only 4; no mechanism enforces full consumption or warns about unread fields. Same gap for convergence thresholds, ID conventions, and `--generate` type allowlists. Producers and consumers evolve independently.
- **Anti-instinct scanner's contract/fingerprint detection is regex-based and brittle to roadmap formatting variants.** When the scanner fails, the audit is fulfilled by manual declaration rather than scanner improvement. The brittleness is hidden by the workaround.
- **No PreToolUse hook covers `.claude/skills/*-workspace/**` writes (until R5 lands).** Plugin instruction prompting is the only path; project CLAUDE.md rules cannot override plugin SKILL.md instructions without mechanical enforcement.
- **Verify-sync (and lint-architecture) are opt-in Make targets with no CI invocation.** Mechanical detection without invocation is decorative; the targets caught the F-A10-005 workspace misplacement in principle but never fired because nothing ran them. The misleading error message (F-A10-006) compounded the gap.
- **Spec-fidelity layer treats all NFRs and all file paths uniformly.** No notion of "portfolio-wide carryover NFR vs release-scoped NFR" (F-A10-012), no notion of "input scaffolding vs deliverable output" (F-A10-011). Manual classification each release.
- **Spec extractor leaks malformed path tokens.** F-A10-010 — `src/\` (trailing escape no character) reached the deviation analyzer as a "missing file" because tokenization doesn't validate path well-formedness.
- **Pipeline graph has no end-to-end smoke gate that exercises every step in order.** F-A10-019 — certify step was specified, helped-functioned, and tested but never wired into `_build_steps()`. F-A10-015 — gate function was wired but used wrong scoping algorithm. A smoke gate that runs the full pipeline against a fixture would have caught both at PR time.
- **Test-failure escalation produces high-confidence forensic verdicts but requires user approval before applying expectation changes.** TFEP correctly identifies mixed-cause clusters (F-A10-013) but cannot auto-apply test-side fixes due to `test_is_wrong: true` gating. Causes user-approval bottlenecks on legitimate test-expectation defects.
- **Roadmap generator's task-granularity heuristic over-bundles distinct deliverables.** F-A10-028 — independent agents flagged Phase 3 Task 3 (compound) and Phase 5 (multi-deliverable bundle). Heuristic unchanged after each warning.
- **Stall detector counts events, not bytes.** F-A10-023 — 870KB single Write looked like a stall (0 events in 347s). Sub-agents that batch large evidence files trigger false stalls; failure mode is opaque to downstream consumers.
- **Validation formulas without operational definitions produce definitional debates rather than substantive ones.** F-A10-027/F-A10-029 — interleave-ratio "deliverable" and SC-5 "prohibited terms" are under-specified; reviewers spend effort on definitions rather than on correctness.
- **Reflect skill validates the reflection but not the reflection's emitted recommendations.** F-A10-024 — the destructive `pct start 300` ran the validation phase as commentary on the assistant's prose, not as gate on the assistant's CLI emissions. The new Recommendation Re-scrutiny phase (Wave 5 of `sc-reflect-rescrutiny-workflow.md`) closes the gap but the propagation to `src/superclaude/commands/reflect.md` and sync to `.claude/commands/sc/reflect.md` is its own multi-step risk surface.
