# Research Completeness Verification

**Topic:** Harden /sc:troubleshoot + sc:troubleshoot-protocol — add "Pipeline Hardening Closure" protocol mode (waves/gates H0-H5)
**Date:** 2026-06-10
**Analysis type:** completeness-verification
**Lens:** completeness (BREADTH — verify every area needed to BUILD the task file has research coverage)
**Files analyzed:** 6 (01-skill-structure-inventory.md, 02-command-and-contract-integration.md, 03-refs-conventions-and-report-template.md, 04-mdtm-template-and-examples.md, 05-doc-crossvalidation-spec-vs-code.md, 06-sync-verify-and-tests.md)
**Driving spec:** /config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/troubleshoot-pipeline-hardening-spec.md

---

## Verdict: PASS

All 9 lens criteria PASS. The research set provides complete BREADTH coverage to build the MDTM task file: every one of the 9 file changes has a pinned insertion point, the output-contract extension surface is fully mapped, the refs house style is documented with exemplar citations, the H5-placement decision is explicitly resolved with evidence, the MDTM template rules + QA gate floors are quoted verbatim with the correct rule references, the spec-vs-code validation is complete (zero contradicted/unverified), and the sync/verify/test validation surface is fully characterized. Three MINOR observations are recorded below; none block the build.

---

## Scope Required by the Spec (what the build needs)

The spec mandates 9 file changes:

**4 EDITS** (spec §9 lines 320-325):
1. `commands/troubleshoot.md` — advertise hardening (thin)
2. `skills/sc-troubleshoot-protocol/SKILL.md` — waves/gates H0-H5 + output contract + blocking gate
3. `refs/report-template.md` — `## Pipeline Hardening Closure` section + NOT PROVEN rule
4. `refs/remediation-handoff.md` — remediation gating

**5 NEW REFS** (spec §9 lines 329-333):
5. `refs/pipeline-hardening-closure.md`
6. `refs/runtime-entrypoint-verification.md`
7. `refs/contract-enumeration.md`
8. `refs/unmask-and-sweep.md`
9. `refs/effective-input-proof.md`

Plus the cross-cutting surfaces the lens enumerates: (a) insertion points for all 9, (b) output-contract extension, (c) refs house style, (d) H5 placement decision, (e) MDTM template rules + QA floors, (f) spec-vs-code validation, (g) sync/verify/test surface.

---

## Coverage Audit (scope item → covering research file)

| Scope item | Covered by | Status |
|---|---|---|
| SKILL.md section map + H-wave insertion seam | 01 §0, §1/§2 | COVERED |
| Output Contract location + 8 new fields + house style | 01 §3; 02 §2; 05 §4 | COVERED |
| Blocking-gate precedent ("cannot mark remediated") | 01 §4 (L327-337 template); 02 §3.2; 03 §3 | COVERED |
| commands/troubleshoot.md thin-edit surface | 02 §1 (all sub-sections) | COVERED |
| Refs house style (frontmatter, fences, tables, length, close) | 03 §1 | COVERED |
| report-template.md insertion point | 03 §2 (between L132-134 + post-EOF rule) | COVERED |
| remediation-handoff.md wiring | 03 §3; 02 §3.3 | COVERED |
| Per-new-ref build recipe (×5) | 03 §4 | COVERED |
| H5 placement decision | 03 §4.6 (explicit, evidence-based) | COVERED |
| MDTM template rules (frontmatter, B2, A3/A4, D3, E1/E2) | 04 §1 | COVERED |
| QA gate floors (M3/M4/I19/I20/I21/I22/I15/I16) | 04 §2 | COVERED |
| Anti-orphaning + POST-reflect form | 04 §3, §4 | COVERED |
| Item-form convention + worked examples | 04 §5 | COVERED |
| Validation item encoding (markdown, not code) | 04 §6; 06 §1-4 | COVERED |
| Spec-vs-code validation (all 9 paths, E1-E5, H→R, fields↔cards) | 05 (all sections) | COVERED |
| sync-dev / verify-sync mechanics | 06 §1 | COVERED |
| markdownlint config + hooks | 06 §2 | COVERED |
| Tests applicability | 06 §3 (TESTING_REQUIREMENTS=NONE, verified) | COVERED |

No scope item is uncovered.

---

## Per-Criterion Findings (the 9 lens criteria)

### Criterion 1 — Source files identified with paths and insertion line ranges? — PASS

Every one of the 9 file changes has a concrete path AND a pinned insertion line/anchor:

- **SKILL.md (edit):** File 01 §0 gives the full section index with line ranges and a numbered "Recommended insertion points" list (items 1-13) — e.g. Output Contract rows append after L61; H-wave inserts at the `---` seam L383; Wave-Structure ASCII map line after L87; Refs table after L546; blocking gate modeled on L327-337; Will Not Do after L497. Lines verified against a 549-line read (01 notes the brief's 548 was off-by-one).
- **commands/troubleshoot.md (edit):** File 02 §1.1-1.6 pins description L3, Behavioral Summary step 4 (L67), `--output-dir` artifact list (L56), handoff L80, "keep thin" enforcement L62/L82.
- **report-template.md (edit):** File 03 §2.2 pins the exact anchor — insert `## Pipeline Hardening Closure` between L132 (after "If there are no follow-ups, write 'None.'") and L134 (`## Grounding Gaps`), INSIDE the four-backtick fence; the `## Pipeline Hardening Closure rule` prose appends after EOF L259.
- **remediation-handoff.md (edit):** File 03 §3 pins a `## Pipeline-hardening precondition` between L2 and L4, plus a Failure-modes table row after L122.
- **5 new refs (create):** File 03 §4.1-4.5 gives per-file content recipes with exact spec line ranges for verbatim cards/tables; File 05 §1 confirms all 5 are genuinely absent and parent `refs/` exists.

Evidence quality is strong: line numbers are paired with quoted anchor text, reducing the risk of stale-line drift at build time.

### Criterion 2 — Output paths/format clear (the 9 target files + what each gets)? — PASS

File 03 §6 ("Summary for the builder") enumerates all 9 with precise create/edit instructions and the spec-section each derives from. File 05 §1 cross-validates every path's existence state ([CODE-VERIFIED] exists for the 4 edits; [CODE-VERIFIED] absent for the 5 creates). The output FORMAT of each surface is characterized: SKILL.md output contract is a markdown table (NOT JSON/YAML) — explicitly confirmed in 01 §3 and 02 §2.1; the audit footer is YAML-in-HTML-comment (02 §2.1B); REPORT.md is a bold-key list (02 §2.1C). Refs are no-frontmatter + single-H1 markdown (03 §1.1). No ambiguity about what each file receives.

### Criterion 3 — Logical breakdown enabling per-file checklist items? — PASS

File 03 §4 decomposes each new ref into its constituent `##` sections with derive-from spec lines, enabling one checklist item per ref with a fully-specified content contract. File 01's 13-item insertion list decomposes the SKILL.md edit into independently-addressable sub-edits (contract rows, derivation rule, H-wave, ASCII map, blocking gate, Will/Will-Not, Error table, Refs table, Token-cost row). File 02 decomposes the command edit into ≤4 advertising-only touches. This granularity directly supports A3's "individual checklist item for EVERY file" (04 §1d) — the 9-file-operation floor is satisfiable.

### Criterion 4 — Patterns/conventions documented (ref house style, markdownlint)? — PASS

File 03 §1 is a dedicated, exemplar-cited house-style section: no frontmatter (the single most important convention, with MD025 rationale), single `# Title` line 1, `## `/`### ` hierarchy, fence language tags (`text` for fill-in cards, `markdown` for report fragments), four-backtick nesting rule for report-template.md, raw GFM pipe tables, ~60-260 line length band, and the "rationale/blocking-rule closing section" pattern — each tied to a specific exemplar file:line. File 06 §2 independently confirms the markdownlint config (`.markdownlint.json` quoted in full: MD013/MD029/MD036/MD033 OFF, MD025/MD040/MD041/MD047 ON, MD024 siblings_only) and the pre-commit hook behavior (runs on `src/` and `.claude/` mirrors with `--fix`; excludes `.dev/`). The two files corroborate each other on MD025. House-style coverage is thorough.

### Criterion 5 — MDTM template notes present with rule references (A3/B2/M3/M4/I19/I20/I21)? — PASS

File 04 is comprehensive and cites the requested rules by ID with line numbers:

- **A3** Complete Granular Breakdown (04 §1d, template L108-112) — drives the 9-item floor.
- **B2** Self-Contained Item 5+1 pattern (04 §1c, template L159-166), with the B3/B5 single-paragraph-vs-structured-bullet tension explicitly resolved in favor of the skill's structured-bullet form (SKILL.md:2186-2198).
- **M3** lens-based 8-step QA sequence (04 §2a, template L1059-1096) — each step an explicit `- [ ]` item.
- **M4** source-fidelity 6-step gate (04 §2b, L1098-1121), runs AFTER M3 per I21:788.
- **I19** agent floors quoted verbatim (04 §2c) — final <500=6 / 500-1500=8 / 1500-3000=10 / >3000=12; intermediate=5.
- **I20** serialized fix authorization (04 §2d, L745-757).
- **I21** source-fidelity applicability (04 §2e, L759-788) — MANDATORY for this source→protocol transform.

Also covered beyond the requested set: I22 intensity (Deep→full), I15/I16 phase-gate + binary PASS/FAIL, D3 section ordering, E1/E2 flat checkboxes. Rule references are accurate and load-bearing.

### Criterion 6 — Granularity sufficient for per-file/per-card checklist items? — PASS

The decomposition supports per-file AND per-card items. Each of the 5 refs has a section-by-section content recipe (03 §4) including which spec card goes verbatim where (e.g. H1 card spec L136-151 → `## Card` in runtime-entrypoint-verification.md; H2 ledger spec L171-180 → `## Ledger` in contract-enumeration.md). The QA gate is decomposed into per-M3/M4-step items (04 §2a/§2b, §5 worked examples 6.1-6.7). The validation phase is decomposed into discrete make/lint/git items (04 §6, 06 VALIDATION sequence). Granularity is sufficient.

### Criterion 7 — Doc cross-validation tags present ([CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED])? — PASS

File 05 is the dedicated cross-validator and uses the tags rigorously: all 4 edit-targets [CODE-VERIFIED] exist; all 5 new refs [CODE-VERIFIED] absent; E1-E5 mechanisms [CODE-VERIFIED] consistent with their root-cause.md evidence; H→R mappings [CODE-VERIFIED] consistent with generalized-remediation-set.md; §6.2 fields ↔ §7 cards [CODE-VERIFIED] no orphans; `make sync-dev`/`make verify-sync` [CODE-VERIFIED] real (Makefile:109/166). Explicit result: **ZERO [CODE-CONTRADICTED] and ZERO [UNVERIFIED]** spec claims (05 §6). File 06 independently [CODE-VERIFIED]-confirms the Makefile mechanics, markdownlint config, and tests-not-affected with grep evidence (zero matches for the skill in `tests/`). Cross-validation discipline is met across both 05 and 06.

### Criterion 8 — QA gate floor + source-fidelity (M4/I21) applicability resolved? — PASS

Resolved unambiguously. File 04 §2 establishes that BOTH gates apply: M3 (lens gate, size trigger >500 lines) AND M4 (source-fidelity, I21 source-transformation trigger). I21 is MANDATORY because the build READS a source spec to produce protocol content (04 §2e). I19 floor for the primary output (>500 lines → 500-1500 band → 8 agents minimum, 4 structural + 4 content) is stated, with adversarial N=10 (04 §2c, §5). Fidelity ordering (M4 after M3, I21:788) and fix-cycle caps (M4=3 cycles→HALT; synthesis/task-integrity=2; I16) are pinned. Example A (04 §5) provides a worked source→protocol fidelity-lens precedent. M4/I21 applicability is fully resolved.

### Criterion 9 — Unresolved ambiguities documented (G1 halt condition; H5 placement; tests scope)? — PASS

All three named ambiguities are documented and resolved:

- **H5 placement:** File 03 §4.6 gives an explicit, 4-point evidence-based decision: H5 is a Rule (not a Gate/card), folds into `pipeline-hardening-closure.md` as a `## Rule H5 — off-path-reviewer` section, does NOT get a 6th ref (spec §9 names exactly 5), and is NOT folded into effective-input-proof.md (scope mismatch). This keeps the build at exactly 5 new refs, matching the spec inventory and the track goal.
- **Tests scope:** File 06 §3 resolves TESTING_REQUIREMENTS = NONE with grep evidence (zero tests parse the troubleshoot skill/command or count refs; spec §9's conditional antecedent is FALSE). I18 is N/A (markdown, not code) per 04 §6. Resolved.
- **G1 halt condition:** The spec's §12 G1 halt is a pre-build approval stop (do not edit src/ until G1 approval). This is correctly understood as a precondition on the build itself rather than a task-item ambiguity; the research treats the spec as the approved driving input. File 05 §1 implicitly relies on G1-approval having been granted (it green-lights CREATE/EDIT items). See MINOR-3 below — the research does not explicitly restate the G1 gate as a build precondition, but it is not a coverage gap for BREADTH because it is a process precondition, not a file-change surface.

Additional spec self-consistency ambiguities (F1, F2) are documented in 05 §4 as non-blocking spec-text reconciliations, not code contradictions — appropriately characterized so the builder does not mistake them for stale-path fixes.

---

## Cross-File Consistency Check (within assigned subset)

No contradictions between research files. Corroborations strengthen confidence:

- Output-contract surface: 01 §3, 02 §2, and 05 §4 agree it is a markdown table at SKILL.md L37-61, 8 new fields append after L61, mirroring `diagnosability_*` precedents.
- Blocking-gate precedent: 01 §4 (L327-337 calibration gate) and 02 §3.2 (status:partial coupling) agree on the mechanism for "cannot mark remediated."
- markdownlint MD025: 03 §1.1/§5 and 06 §2 agree (no frontmatter, single H1).
- sync mechanics: 04 §6, 05 §5, and 06 §1 agree sync-dev auto-mirrors new refs (no per-file registration) and verify-sync is the drift gate.
- POST-reflect form: 04 §4/§5 flags the two example task files use the now-MALFORMED HALT form and mandates the SELF-RUN subagent form (SKILL.md:2193-2198) — internally consistent and matches project memory `feedback_sc_reflect_vs_inline_rfqa`.

---

## MINOR Observations (non-blocking; do not change the PASS verdict)

**MINOR-1 — Command filename imprecision in File 06.** File 06 §1 and its VALIDATION sequence refer to the command source as `sc-troubleshoot.md` (e.g. "`✅ sc-troubleshoot.md` if edited"; `git add ... src/superclaude/commands/sc-troubleshoot.md`). The actual source file is `src/superclaude/commands/troubleshoot.md` (verified on disk; the `.claude/` mirror lands at `.claude/commands/sc/troubleshoot.md`). The spec §9 and Files 02/05 use the correct path. The builder must use `commands/troubleshoot.md`, NOT `commands/sc-troubleshoot.md` (which does not exist). This is a naming slip in 06's prose, not a coverage gap — the correct path is well-established by 02/05/spec.

**MINOR-2 — F1 verdict-enum reconciliation is the builder's judgment call.** File 05 §4 F1 notes §6.2's `pipeline_hardening_verdict` enum (`pass|blocked|advisory|not_applicable`) vs §8's Closure-verdict line (`pass|blocked|advisory`, omitting `not_applicable`). Both 05 and 03 §2.3 surface it; 03 recommends rendering the §8 block with the §6.2 superset. The research correctly flags it as spec-text reconciliation (not code-driven), but does not fully pre-decide whether the built report-template should carry `not_applicable` in the verdict line or rely on the separate Applicability line. The builder should make this a single explicit reconciliation item. Low-risk; both files give enough to decide.

**MINOR-3 — G1 approval precondition not restated as an explicit build-gate note.** The spec §12 mandates "Proceed only after human approval of the G1 package" before any `src/` edit. The research (esp. 05) green-lights CREATE/EDIT items assuming G1 approval is granted, which is reasonable for a task-builder research phase, but no file restates G1 as a build precondition the task file should encode (e.g., a frontmatter note or a Phase-0 confirmation). For a BREADTH gate this is not a coverage gap — G1 is a process/approval precondition, not one of the 9 file-change surfaces — but the builder/orchestrator should confirm G1 approval status before the task executes edits to shared protocol files.

---

## Depth Assessment

**Expected depth (this lens):** BREADTH — confirm every build-required area has coverage.
**Actual depth achieved:** Exceeds the breadth bar. The research is consistently line-pinned (insertion anchors with quoted context), verbatim-spec-mapped (each new ref's sections tied to exact spec line ranges), and cross-validated (05/06 confirm every path and mechanism against the real repo with grep/Read evidence). The H5-placement and tests-scope decisions are resolved with explicit rationale rather than left open. The QA-floor stack is quoted, not paraphrased.
**Missing breadth elements:** None. All 7 lens sub-areas (a-g) are covered.

---

## Recommendations for the Builder

1. Use `src/superclaude/commands/troubleshoot.md` as the command edit-target path (NOT `sc-troubleshoot.md`); the mirror is `.claude/commands/sc/troubleshoot.md`. (Addresses MINOR-1.)
2. Build exactly 5 new refs; fold Rule H5 into `pipeline-hardening-closure.md` per 03 §4.6. Do NOT create a 6th ref.
3. Encode 9 distinct file-operation content items (4 edits + 5 creates) per A3, plus the SKILL.md sub-edits (contract rows, H-wave, ASCII map, blocking gate, Refs table, Will/Will-Not) as their own items.
4. Set `spec_path` to the driving spec so the M4 fidelity gate and POST-reflect `--spec` activate (04 §1a, §4).
5. Apply BOTH M3 (lens, >500-line trigger) AND M4 (source-fidelity, I21) gates; floor at 8 agents (4 structural + 4 content) if final output lands 500-1500 lines, adversarial N=10. (Criterion 8.)
6. Use the SELF-RUN POST-reflect subagent form (SKILL.md:2193-2198), penultimate; Done-flip last. Do NOT copy the examples' deprecated HALT/`reflect_post: PENDING` form or `start_commit..HEAD` diff base. (04 §4/§5.)
7. Add one explicit spec-text reconciliation item for F1 (verdict-enum). (Addresses MINOR-2.)
8. Encode validation as discrete `make sync-dev` → `make verify-sync` → markdownlint → git-scope items; add NO pytest tests (TESTING_REQUIREMENTS=NONE). Never stage `.claude/` mirrors. (06 §3, VALIDATION sequence.)
9. Confirm G1 approval status before the task executes shared-protocol edits. (Addresses MINOR-3.)

---

## VERDICT: PASS

All 9 lens criteria PASS. Research provides complete BREADTH coverage for building the MDTM task file. Three MINOR observations (command-filename imprecision in File 06; F1 verdict-enum reconciliation as a builder judgment call; G1 approval precondition not restated) are documented for the builder but none constitute a coverage gap or block the build.
