# QA Report: Task-Research Alignment (Cross-Validation Lens)

**QA_MODE:** task-integrity
**LENS:** task-research-alignment
**Date:** 2026-06-10
**Auditor:** rf-analyst (no team context)
**Adversarial stance:** Assume builder/refactor dropped or misrepresented findings.

## Scope
- TASK FILE: TASK-RF-troubleshoot-hardening-20260610-144537.md
- RESEARCH DIR: research/ (7 files)
- DRIVING SPEC (refactored): troubleshoot-pipeline-hardening-spec.md
- CHANGE LEDGER: qa/tasklist-refactor-ledger.md
- TRACK GOAL: Add "Pipeline Hardening Closure" mode (H0-H5) to sc:troubleshoot-protocol — 4 markdown edits + 5 new refs.

---

## Method

Read in full: the entire task file (476 lines, 4 reads), the refactored driving spec (444 lines), the change ledger, and research files 01, 02, 03, 06, 07. Spot-verified spec field counts via `awk`/`grep` against the live spec. Adversarial stance: assumed the builder/refactor dropped or misrepresented findings; hunted for missing items, fabricated items, and stale-enum leakage.

Note on research currency: the driving spec was REFACTORED after the research files were written. Research 01 §3, 02 §2.1, and 03 §2.3/§4 therefore describe the OLD enum (`pass | blocked | advisory`, `N/A`, "8 fields", "NOT PROVEN" with a space). The ledger's GLOBAL CORRECTION G-ENUM (CS-3) and CS-7/CS-4 upgrade those to the current state. This is expected staleness, NOT a fabrication — the task file must (and does) follow the spec + ledger, not the pre-refactor research prose. Per the spawn prompt, 07-gap-fill GF-5 is likewise known-stale.

---

## Checklist 1 — Codebase findings (9 target files) → task items

| # | Codebase finding (research) | Task item | Status |
|---|---|---|---|
| 1 | NEW hub `pipeline-hardening-closure.md` (03 §4.1, GF-6) | Step 2.1 | COVERED |
| 2 | NEW H1 `runtime-entrypoint-verification.md` (03 §4.2) | Step 2.2 | COVERED |
| 3 | NEW H2 `contract-enumeration.md` (03 §4.3) | Step 2.3 | COVERED |
| 4 | NEW H3 `unmask-and-sweep.md` (03 §4.4) | Step 2.4 | COVERED |
| 5 | NEW H4 `effective-input-proof.md` (03 §4.5) | Step 2.5 | COVERED |
| 6 | EDIT `commands/troubleshoot.md` desc L3 + Behavioral Summary L60-67 + `--output-dir` L56 (02 §1, GF-2) | Steps 2.6, 2.7 | COVERED |
| 7 | EDIT `SKILL.md` Output Contract L37-61 + Wave 4.5 seam L383 + Refs registry L536-546 + calibration gate L327-337 + Wave 6 L439 + Will Not Do L484-497 (01) | Steps 2.8a/2.8b, 2.9, 2.10, 2.11a/b/c | COVERED |
| 8 | EDIT `report-template.md` insert §8 block inside 4-backtick fence (03 §2.2) + append NOT_PROVEN rule after EOF (03 §2.4) | Steps 2.12, 2.13 | COVERED |
| 9 | EDIT `remediation-handoff.md` precondition subsection + failure-mode row (03 §3.3) | Step 2.14 | COVERED |

All 9 file changes (4 edits + 5 new refs) have corresponding task items. The SKILL.md edit is correctly decomposed into 6 atomic items targeting each of the distinct insertion seams research 01 identified. No codebase-grounded change is orphaned.

---

## Checklist 2 — Refactored-spec changes (ledger CS-1..CS-m1) → task items

| Ledger correction | Spec basis | Task item(s) | Status |
|---|---|---|---|
| CS-3 G-ENUM (advisory removed; 3-token enum everywhere) | §6.2 C3, §10.11 | Header OQ2, 2.1, 2.8a, 2.9, 2.11b, 2.12, 2.14, all QA/M4 lens prompts | COVERED |
| CS-1 trigger→gate map (T1–T9 table; flat list gone) + trigger-overrides-skip (M6) | §6.1 | 2.1 (`## Trigger`), 2.9 (Wave 4.5 computes set from map) | COVERED |
| CS-2 C2 verdict invariant (vacuous-pass closed, M8) | §6.2 | 2.1 (`## Verdict invariant`), 2.11b, 2.13 | COVERED |
| CS-2b/M2 H5-mandatory + off-path→blocked | §7 H5 | 2.1 (`## Rule H5`), 2.11b, 2.12 (off-path line) | COVERED |
| CS-7/CS-4 full ~13-field contract + Default column + status/path rule M7 (was "8 fields") | §6.2 | 2.8a (5 non-gate), 2.8b (4 status + 4 path + M7) | COVERED |
| CS-11 H2 consumer-discovery manifest (absent ⇒ NOT_PROVEN) | §7 H2 M11 | 2.3 (`## Consumer-discovery manifest`) | COVERED |
| CS-9 H3 E3-style sibling-heading negative fixture completion criterion | §7 H3 | 2.4 (`## Completion criteria`) | COVERED |
| CS-10 H3 fixpoint-after-discovery (M9) | §7 H3 | 2.4 (`## Fixpoint after discovery`) | COVERED |
| CS-5 H4 no-op vs empty-with-changes (M5) | §7 H4 | 2.5 (`## No-op vs empty`) | COVERED |
| Defaults column (CS-4) | §6.2 | 2.8a (default tokens stated per field) | COVERED |
| Escape/skip pattern `^E\d+$`/`E\d+\+` (m1) | §6.2 | 2.1, 2.8a (`known_escapes_caught` pattern) | COVERED |
| advisory-removed (OQ2 rewrite; A10-M2 obsolete) | ledger Header | Open Question 2 rewritten; OQ acknowledges no divergence note | COVERED |
| NOT_PROVEN first-class status forcing blocked | §8 | 2.13 (report rule), 2.1 (`## Closure verdict + NOT_PROVEN rule`) | COVERED |
| A10-I2 SPLIT failure-wiring (calibration gate / Wave 6 / Will Not Do) | §5.2, §8 | 2.11a, 2.11b, 2.11c | COVERED |
| A10-I1 SPLIT M4 (spawn / fix / loop) | A.10 | 5.5a, 5.5b, 5.5c | COVERED |
| A10-C1 POST-reflect penultimate ordering | A.10 | Post-Completion order: summary → POST-reflect → Done | COVERED |
| Phase-4 QA polarity fix (enum + field-count + new invariants) | A.10 | Steps 4.3, 4.6, 4.7, 4.9 prompts | COVERED |

Every ledger correction maps to a concrete task item. The two SPLITs (A10-I2 → 2.11a/b/c; A10-I1 → 5.5a/b/c) and the POST-reflect reorder are all present in the final task file.

---

## Findings (adversarial)

### Finding A1 (MINOR) — H2 ledger "How found" provenance not threaded into the manifest requirement

- **Severity:** MINOR
- **Type:** Spec-content under-specification (not a drop)
- **Evidence:** Spec §7 H2 ledger row `How found` (spec L205: "Semantic retrieval, exact search terms, symbol/reference search, template inventory, generated fixture inventory") and the separate M11 **consumer-discovery manifest** requirement (spec L211-214) are two distinct spec elements. Task Step 2.3 reproduces the 9-row ledger VERBATIM (covers `How found`) AND adds a `## Consumer-discovery manifest` section (covers M11). Both are present.
- **Why flagged anyway:** The task item does not explicitly state that the `How found` ledger column and the M11 manifest are the SAME provenance evidence at two granularities (ledger = per-contract, manifest = run-level reproducible query set). A builder could render them as two unrelated lists. The spec intends the manifest to be the machine-checkable backing for the ledger's `How found` claims.
- **Recommendation:** Non-blocking. Optionally add one clause to Step 2.3: "the manifest is the reproducible backing for the ledger's `How found` column." Both elements ARE covered, so this is a cohesion nuance, not a missing item.

### Finding A2 (MINOR) — Wave 5 report-compose step-list insertion (research 01 §6 / 02 §1) has no dedicated task item

- **Severity:** MINOR
- **Type:** Possible codebase-finding gap (insertion seam)
- **Evidence:** Research 01 recommended-insertion #6 (line 141): "Wave 5 report compose — insert into the section list at L408 area — add a 'Pipeline Hardening Closure' REPORT.md section per spec §8." This is a SEPARATE seam from the Wave 4.5 wave (01 #5) and the Output Contract (01 #3). The task file's Step 2.9 creates `### Wave 4.5` and the ASCII map line, and Step 2.12 inserts the section into `report-template.md` — but NO task item edits SKILL.md's Wave 5 *report-compose section list* (the L392-408 enumeration) to add "render the Pipeline Hardening Closure section."
- **Adversarial reading:** The report template gains the section (2.12), but the SKILL.md Wave-5 compose loop that walks the template section list is not explicitly told to render it. In practice the compose step renders "the report template," so an inserted template section is rendered transitively — which is why this is MINOR not IMPORTANT. But research 01 explicitly called this out as insertion point #6 and it has no 1:1 item.
- **Recommendation:** Non-blocking (the template-driven compose covers it transitively). If the builder wants belt-and-suspenders fidelity to research 01 #6, add a half-sentence to Step 2.9 noting the Wave 5 compose renders the new template section when `pipeline_hardening_applicable=true`. Research 01 #10 (`## Will Do` bullets after L482), #11 (Error Handling rows after L522), and #13 (Token Cost Profile row) are likewise NOT given dedicated items — these were research SUGGESTIONS ("optionally"), and the ledger's DO-NOT-CHANGE/scope did not promote them to required items, so their omission is a deliberate scope decision, not a drop.

### Finding A3 (MINOR) — `commands/troubleshoot.md` skill-side `description` and the Will/Will-Not + Activation-enumeration touches are scoped out without an explicit OQ note

- **Severity:** MINOR
- **Type:** Scope-boundary traceability
- **Evidence:** Research 02 §1.4 (L69) suggested appending "pipeline hardening closure" to the Activation L82 enumeration; §1.5 (L73) suggested an optional one-line Will: bullet in the command. GF-2 explicitly decided the COMMAND `description` (L3) + Behavioral Summary + `--output-dir` are the advertising surface and the SKILL.md frontmatter `description` need NOT be kept in lock-step. Task Steps 2.6/2.7 implement exactly the GF-2 decision (command description + Behavioral Summary + output-dir). The Activation-enumeration and command Will: touches are silently omitted.
- **Adversarial reading:** These omissions are CORRECT per acceptance #1 (keep command thin) and GF-2, but the task file does not record WHY the research-suggested Activation/Will touches were dropped. A reviewer cross-checking research 02 §1.4/§1.5 against the task could read the omission as a drop rather than a scope decision.
- **Recommendation:** Non-blocking. The omissions align with GF-2 + acceptance #1. Optionally note in Step 2.6's context that the Activation enumeration and command Will-bullet were intentionally NOT touched to keep the command minimal-thin. No item is actually missing.

### Finding A4 (INFORMATIONAL) — no fabricated task items detected

- **Severity:** INFORMATIONAL (clean)
- **Evidence:** Every Phase-2 item names a file that is either one of the 5 spec §9 new refs or one of the 4 spec §9 primary-edit files. Every embedded content element traces to a spec section (§4, §6.1, §6.2, §7 H0-H5, §8, §10) or a research finding (GF-1 anchors, 03 house-style, 01 seams). Spot-checks: H1 card = 13 fields (verified `awk` against spec = 13); H4 card = 10 fields (verified = 10); verdict enum 3-token with `advisory` surviving ONLY as E4-mechanism prose (verified `grep`: spec lines 45, 184, 190, 272 are E4 examples; lines 112, 127, 368, 414 explicitly state advisory is REMOVED). The SCOPE GUARDRAIL (no PRD/pipeline/reflect source edits; `PrdExecutor._evaluate_gate` / `pipeline.gates.gate_passed` frozen-evidence-only) is stated in Key Constraints and honored — no Phase-2 item touches Python source. No item invents a file/section grounded in NEITHER research NOR the refactored spec.

---

## Remaining checklist answers

### CL3 — Fabricated actions (grounded in NEITHER research NOR refactored spec)?
**NONE FOUND.** See Finding A4. All 14 Phase-2 build items + all validation/QA/M4/post-completion items trace to the spec or research. The frozen-evidence Python symbols are correctly fenced off as non-edit-targets.

### CL4 — Research edge cases reflected in verification criteria?
**YES — all four covered.**
- markdownlint MD025 (no frontmatter + single H1): Phase-2 preamble (L178) + Step 3.3 + QA Step 4.2/4.4. Grounded in 06 §2 (.markdownlint.json MD025 ENABLED) + 03 §1.1.
- four-backtick fence integrity: Step 2.12 (insert INSIDE the 4-backtick fence, no nested 3-backtick), Step 2.13 (append OUTSIDE the fence), QA Step 4.2 ("four-backtick fence still closes correctly"). Grounded in 03 §1.4/§2.2/§5.
- sync-dev auto-mirror of new refs: Step 3.1 (explicitly notes "new refs auto-mirror per the Makefile"). Grounded in 06 §1 FINDING (find -type f mirrors all refs; no per-file registration).
- no `.claude/` staging: Step 3.4 (grep `^[AM].*\.claude/`, `git restore --staged`, never `git add -f`). Grounded in 06 §4 + CLAUDE.md ABSOLUTE RULE.

### CL5 — Research dependencies reflected in phase ordering?
**YES.**
- insertion-anchor discovery BEFORE edits: Phase 1 Step 1.4 builds `insertion-anchors.md`; every Phase-2 edit item reads it before anchoring. Grounded in GF-1 ("anchor on TEXT not line numbers") — the task explicitly demotes the stale absolute line numbers (G-LINES) and pins TEXT anchors.
- sync BEFORE verify-sync: Step 3.1 (sync-dev) precedes Step 3.2 (verify-sync). Grounded in 06 §1 FINDING ("Creating 5 NEW refs is fine as long as sync-dev ran first").
- M4 (Phase 5) AFTER M3 (Phase 4): stated in Phase 5 preamble ("output must be structurally sound before checking external fidelity"). QA lens gate before source-fidelity gate.
- POST-reflect penultimate, after Task Summary: Post-Completion order is summary → POST-reflect → Done (A10-C1 reorder applied).

### CL6 — Do QA-lens prompts verify the NEW spec content (not the obsolete advisory enum)?
**YES — polarity fix correctly applied.** This was the single highest-risk regression (the pre-refactor lens prompts REJECTED correct output). Verified:
- Step 4.3 (internal-consistency): "the `pipeline_hardening_verdict` enum is consistently the THREE-token `pass | blocked | not_applicable` everywhere — `advisory` MUST be ABSENT (its presence is a defect, per spec C3)". Polarity is correct (advisory absent = pass).
- Step 4.6 (spec-fidelity): "verify the verdict enum is exactly the three tokens ... with `advisory` ABSENT ... flag any surviving `advisory` token or '8-field' framing as a defect." Correct.
- Step 4.7 (completeness-vs-§7): verifies T1–T9 trigger→gate map, C2 invariant (vacuous-pass closed), M7 status/path, NOT_PROVEN→blocked, H2 manifest, H3 sibling-fixture + fixpoint, H4 no-op-vs-empty, H5-mandatory/off-path→blocked, acceptance 11–15. The NEW invariants are all named.
- Step 4.9 (blocking-rule-accuracy): "flag any rule that ... reintroduces `advisory`." Correct.
- Step 5.1/5.2 (M4 fidelity): "a surviving `advisory` token or '8-field' framing is a fidelity DEFECT per spec C3"; verifies the full ~13-field set + all new invariants. Correct.
No lens prompt instructs verifiers that `advisory` MUST be present, and no lens still references the "8-field table" as correct. The CRITICAL POLARITY FIX from the ledger (Phase 4 + Phase 5) is fully landed.

---

## VERDICT: PASS

The built task file faithfully encodes BOTH grounding sources:
- **Codebase grounding:** all 9 target file changes (4 edits + 5 new refs) have task items; the SKILL.md edit is atomically decomposed against the exact insertion seams research 01 identified; all research-identified edge cases (MD025, four-backtick fence, sync-dev auto-mirror, no-.claude-staging) and ordering dependencies (anchor-discovery→edit, sync→verify-sync, M3→M4, POST-reflect penultimate) are reflected.
- **Content grounding:** every refactored-spec change in the ledger (CS-1 trigger map, CS-2 verdict invariant, CS-2b/M2 H5-mandatory, CS-7/CS-4 ~13-field contract + Default + M7, CS-11 H2 manifest, CS-9/CS-10 H3 fixture+fixpoint, CS-5 H4 no-op, CS-3 3-token enum, A10-I1/I2 SPLITs, A10-C1 reorder) maps to a task item.
- **Anti-fabrication:** no task item invents an action grounded in neither source; the frozen Python symbols are correctly fenced as non-edit-targets; spec field counts (H1=13, H4=10) and the 3-token enum verified directly against the live spec.
- **Highest-risk regression averted:** the QA/M4 lens-prompt polarity was correctly flipped (advisory-ABSENT = pass), so the gates now verify the NEW spec content rather than rejecting it.

The four findings above are all MINOR/INFORMATIONAL cohesion-and-traceability nuances (manifest↔ledger provenance link; Wave-5 compose transitive coverage; command-thinness scope-decision traceability). None blocks execution: in each case the required item IS present or the omission is a deliberate, correctly-grounded scope decision. No CRITICAL or IMPORTANT alignment gap was found.

**Severity summary:** 0 CRITICAL · 0 IMPORTANT · 3 MINOR · 1 INFORMATIONAL.
