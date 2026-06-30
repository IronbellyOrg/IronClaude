# Research: Doc Cross-Validation (spec vs code)

**Topic type:** Doc Cross-Validator
**Scope:** spec §3/§9/§11 vs repo
**Status:** Complete
**Date:** 2026-06-10

---

## 1. spec §9 — file targets cross-validation

### Primary expected edits (spec §9, lines 320–325) — must EXIST

| Spec path | Status |
|---|---|
| `src/superclaude/commands/troubleshoot.md` | **[CODE-VERIFIED]** exists |
| `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` | **[CODE-VERIFIED]** exists |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md` | **[CODE-VERIFIED]** exists (16909 bytes) |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/remediation-handoff.md` | **[CODE-VERIFIED]** exists (5434 bytes) |

All 4 edit-targets exist. None are stale. The builder may safely create EDIT items against them.

### Likely new ref/template files (spec §9, lines 329–333) — must NOT yet EXIST

Parent dir `src/superclaude/skills/sc-troubleshoot-protocol/refs/` **[CODE-VERIFIED]** exists (contains 8 ref files: calibrator-eval-cases, diagnosability-audit, doc-discovery, escalation-rubric, hypothesis-card-template, remediation-handoff, report-template, triage-checklist).

| Spec proposed-new path | Status |
|---|---|
| `refs/pipeline-hardening-closure.md` | **[CODE-VERIFIED]** absent — genuine CREATE |
| `refs/runtime-entrypoint-verification.md` | **[CODE-VERIFIED]** absent — genuine CREATE |
| `refs/contract-enumeration.md` | **[CODE-VERIFIED]** absent — genuine CREATE |
| `refs/unmask-and-sweep.md` | **[CODE-VERIFIED]** absent — genuine CREATE |
| `refs/effective-input-proof.md` | **[CODE-VERIFIED]** absent — genuine CREATE |

All 5 new files are genuinely absent; parent dir exists. No filename collision. CREATE items are safe.

### §9 tests/docs (lines 337–338)

- `tests/` **[CODE-VERIFIED]** exists.
- `docs/` **[CODE-VERIFIED]** exists.

Both are conditional ("if approval scope includes validation" / "only if user-facing docs expected"). No specific file named, so no stale-path risk.

## 2. spec §3 escape table (E1–E5) + §11 justification vs evidence

Each escape dir was confirmed to contain `root-cause.md` AND `remediation.md` (plus hyp-1/2, rem-1/2). The spec's §3 "Failure shape" and §11 "Justification" were cross-read against each `root-cause.md`'s "Final root cause" / "Verdict".

| Escape | Evidence files present | Spec §3 + §11 mechanism vs root-cause.md | Status |
|---|---|---|---|
| E1 — cloud `--file` misuse | root-cause.md + remediation.md | Spec §3: "helper/argv proof accepted while real headless subprocess rejected local paths via cloud/session-token `--file`; sibling pipelines avoided pattern." root-cause.md "Final root cause" says exactly this: false `--file` contract untested at headless Claude subprocess boundary; sibling sweep (roadmap/tasklist/validate) would expose PRD outlier. §11 "runtime-boundary + sibling-contract failure" matches. | **[CODE-VERIFIED]** consistent |
| E2 — completion-phase false positive | root-cause.md + remediation.md | Spec §3: "parser enforced parallel invariant on final sequential completion bookend via syntactic/positional matching not semantic topology." root-cause.md "Verdict": generated-artifact contract miss; parser used phase-number/heading match not role; Phase 7 intentionally sequential. §11 "generated-artifact topology failure" matches. | **[CODE-VERIFIED]** consistent |
| E3 — Task Log findings-heading sibling | root-cause.md + remediation.md | Spec §3: "E2 fix removed one symptom but did not sweep same-token sibling headings; hard heuristic gate halted on non-executable Task Log placeholder headings." root-cause.md: PR #154 fixed final-phase symptom but left whole-artifact parser scanning `Phase N` headings incl. `### Phase 2 - ... Findings`; hard-fatal heuristic halted valid run. §11 "unmasked sibling classifier failure" matches. | **[CODE-VERIFIED]** consistent |
| E4 — generic/trailing evaluator divergence | root-cause.md + remediation.md | Spec §3: "shared `SemanticCheck.advisory` contract validated on generic gate path while real PRD runtime used bespoke evaluator treating advisory failures as fatal." root-cause.md "Verdict": PR #155 verified generic `gate_passed` but normal PRD path calls `PrdExecutor._evaluate_gate` which ignores `advisory`. §11 "shared-contract consumer divergence" matches. | **[CODE-VERIFIED]** consistent |
| E5 — POST-reflect wrong diff base | root-cause.md + remediation.md | Spec §3: "review selector audited a commit range that omitted dirty `/task` work and could include foreign commits." root-cause.md "Final root-cause": `/sc:reflect --mode post --diff <start_commit>..HEAD` two-dot range audits commits not dirty working tree; `/task` mutates files without committing. §11 "independent-review effective-input failure" matches. | **[CODE-VERIFIED]** consistent |

Note: E4's root-cause.md additionally cites concrete code symbols `PrdExecutor._evaluate_gate` and `pipeline.gates.gate_passed`. These are the only spec-adjacent claims that name live code; they live in the EVIDENCE files (root-cause.md), not in the spec's §9 edit list, so they do not become edit-target task items. They are corroborated by the frozen contract-implementations.md and not contradicted. **[CODE-VERIFIED at evidence-file level]** — spec does not ask the builder to edit those files.

## 3. generalized-remediation-set.md — R1–R7 + H→R mappings

R1–R7 all present in `generalized-remediation-set.md` **[CODE-VERIFIED]**:

- R1 Runtime-Boundary Contract Closure
- R2 Shared-Contract Consumer Enumeration and Parity Proof
- R3 Whole-Artifact Classifier Boundary Tests
- R4 Unmask-and-Sweep After Any Escape Fix
- R5 Effective-Input Proof for Independent Review and Audit Gates
- R6 Severity Cost and Blast-Radius Review
- R7 Generalized Escape Closure Definition

### Spec H→R mappings vs generalized-remediation-set.md

The spec maps each hardening wave/gate to generalized R-controls (§7 lines 132, 167, 198, 234, 268). Cross-check against the remediation set's intent and its "Deduplicated Coverage Matrix":

| Spec gate | Spec claims maps to | Consistency with generalized-remediation-set.md | Status |
|---|---|---|---|
| H1 Runtime-entrypoint gate | R1, R3, R5, R6 | R1 (runtime boundary) ✓, R5 (effective-input for E5 which H1 names) ✓, R6 (severity, H1 asserts continue/warn/halt) ✓, R3 (whole-artifact, H1 names E2/E3 full-artifact replay) ✓. All four are coherent: H1 is the runtime-proof gate and legitimately draws on R1/R3/R5/R6. | **[CODE-VERIFIED]** consistent |
| H2 Contract-enumeration wave | R1, R2, R5, R6 | R2 (consumer enumeration) is the spine ✓; R1 (boundary ledger overlaps R2 producer/transformer/consumer) ✓; R6 (severity per consumer — R6 step 3 "verify severity on every runtime consumer") ✓; R5 (effective-input — weakest link, but R5 secondary-catches E4 which H2 inventories) acceptable. | **[CODE-VERIFIED]** consistent |
| H3 Unmask-and-sweep wave | R3, R4, R6, R7 | R4 (unmask-and-sweep) is the spine ✓; R3 (whole-artifact classifier — H3 requires full-artifact + sibling fixtures) ✓; R6 (severity cost review — H3 "severity cost review for hard gates") ✓; R7 (closure definition) ✓. | **[CODE-VERIFIED]** consistent |
| H4 Effective-input gate | R5 | R5 is exactly "Effective-Input Proof for Independent Review and Audit Gates" — 1:1 match ✓. | **[CODE-VERIFIED]** consistent |
| H5 Off-path-reviewer rule | R1, R3, R4, R5, R6 | Off-path review is a cross-cutting requirement; R1 step 5, R5 step 4 both mention off-path review blocking. R3/R4/R6 are the surfaces an off-path reviewer would inspect. Coherent as a composite rule. | **[CODE-VERIFIED]** consistent |

Cross-check vs the Coverage Matrix in generalized-remediation-set.md (which maps R→E, the inverse direction): the matrix's R→E primary mappings (R1→E1,E4,E5 / R2→E4 / R3→E2,E3 / R4→E3,E4 / R5→E5 / R6→E2,E3,E4 / R7→all) are consistent with the spec's per-escape §11 justification (E1→runtime+sibling=R1; E2→topology=R3+R6; E3→unmask=R4+R3; E4→consumer=R2+R1; E5→effective-input=R5). No contradiction found between spec H→R and remediation R→E.

## 4. spec §6.2 output-contract fields ↔ §7 card templates internal consistency

This is an internal-consistency check of the spec itself (not a code cross-check), to ensure the builder does not create a "produce field X" item with no card to fill it, or a "produce card Y" item that feeds nothing.

### §6.2 fields → producing card in §7

| §6.2 field | Producing card/wave in §7 | Status |
|---|---|---|
| `pipeline_hardening_applicable` (bool) | H0 ("Required outputs: `pipeline_hardening_applicable` decision", line 121) | OK — produced by H0 |
| `pipeline_hardening_verdict` (string) | §8 report "Closure verdict: pass \| blocked \| advisory" (line 311); §6.2 enum adds `not_applicable` | MINOR — see flag F1 below |
| `runtime_entrypoint_card_path` (str\|null) | H1 "Runtime-entrypoint verification" card (lines 137–151) | OK — produced by Gate H1 |
| `contract_ledger_path` (str\|null) | H2 "Required ledger" table (lines 171–181) | OK — produced by Wave H2 |
| `unmask_sweep_path` (str\|null) | H3 "Required outputs" (lines 200–211) | OK — produced by Wave H3 |
| `effective_input_card_path` (str\|null) | H4 "Effective Input Proof" card (lines 242–253) | OK — produced by Gate H4 |
| `off_path_review_decision` (string) | H5 Off-path-reviewer rule (lines 266–293) produces the decision | OK — produced by Rule H5 |
| `known_escapes_caught` (list[str]) | H0 "Candidate known escapes caught" (line 123); each gate has "Escapes caught in one shot" | OK — produced by H0 + per-gate |

Every §6.2 path field has a corresponding producing card. **No orphan field.**

### §7 cards → consuming §6.2 field (reverse)

| §7 wave/gate | Produces artifact consumed by §6.2 field | Status |
|---|---|---|
| H0 Applicability | `pipeline_hardening_applicable`, `known_escapes_caught` | OK |
| H1 Runtime-entrypoint | `runtime_entrypoint_card_path` | OK |
| H2 Contract-enumeration | `contract_ledger_path` | OK |
| H3 Unmask-and-sweep | `unmask_sweep_path` | OK |
| H4 Effective-input | `effective_input_card_path` | OK |
| H5 Off-path-reviewer | `off_path_review_decision` | OK |

No §7 card lacks a contract field. **No orphan card.**

### Internal-consistency flags (not code contradictions, spec self-consistency)

- **F1 (cosmetic, non-blocking):** §6.2 `pipeline_hardening_verdict` enum is `pass | blocked | advisory | not_applicable` (line 105) but §8 report's "Closure verdict" line lists only `pass | blocked | advisory` (line 311), omitting `not_applicable`. The §6.2 "Applicability: applicable | not applicable" line in §8 (line 303) covers the not-applicable case separately, so this is a presentation inconsistency, not a logic gap. Builder should reconcile the §8 report template's verdict enum with §6.2 (add `not_applicable`) — but this is a spec-text reconciliation, NOT a stale-code issue.
- **F2 (naming, non-blocking):** §6.2 field names use `_card_path`/`_ledger_path`/`_path` suffixes; the proposed new ref files in §9 use different stems (`runtime-entrypoint-verification.md`, `contract-enumeration.md`, `unmask-and-sweep.md`, `effective-input-proof.md`). The ref files are TEMPLATES (the card SHAPES), while the `_path` fields point to per-RUN produced artifacts. These are different artifact classes — no conflict, just worth the builder noting the template-vs-instance distinction so it doesn't conflate "create ref template" with "emit runtime path".

## 5. spec §10 acceptance criteria — real-mechanism check

§10 criterion 10 (line 357) names `make sync-dev`, `make verify-sync`, and `.claude/` mirrors.

- `make sync-dev` **[CODE-VERIFIED]** — see Makefile/CLAUDE.md; copies `src/superclaude/{skills,agents,commands}` → `.claude/`.
- `make verify-sync` **[CODE-VERIFIED]** — checks src/ and .claude/ are in sync (CI-friendly), per project CLAUDE.md "Component Sync".
- `.claude/` mirrors + "not staged except `.claude/settings.json`" **[CODE-VERIFIED]** — matches the project's ABSOLUTE RULE (`.claude/{skills,commands,agents,hooks,templates}` gitignored; only `.claude/settings.json` tracked).

(Confirmed against project CLAUDE.md and global CLAUDE.md "Dev Commands" / "Component Sync" sections. Targets are real and correctly named.)

The other §10 criteria (1–9) reference protocol behaviors (thin command handoff, closure verdict, blocking gates, ledger, controls) — these are design assertions about the to-be-built protocol, not references to existing code, so there is no stale-path risk. Criterion 1 ("`/sc:troubleshoot` remains a thin command handoff") is consistent with §5.1 and with the existing command file existing (verified §1).

Additional verification:
- Makefile **[CODE-VERIFIED]**: `sync-dev:` at `Makefile:109`, `verify-sync:` at `Makefile:166` — both real targets.
- `src/superclaude/commands/troubleshoot.md` **[CODE-VERIFIED]** is a thin command file (frontmatter + triggers + usage + handoff to `sc:troubleshoot-protocol`); criterion 1's "thin command handoff" premise holds against current code.

## 6. Stale/contradicted claims (DO NOT build on)

**Result: ZERO [CODE-CONTRADICTED] and ZERO [UNVERIFIED] spec claims.** Every file path and architectural claim in spec §3, §9, §11 (and the §6.2/§7/§10 cross-checks) verified against repo and frozen evidence.

- **No stale edit-targets.** All 4 §9 primary-edit files exist. The builder may create EDIT items for them.
- **No phantom new files.** All 5 §9 proposed-new ref files are genuinely absent; parent `refs/` dir exists. The builder may create CREATE items for them.
- **No missing evidence.** All E1–E5 escape dirs contain both `root-cause.md` and `remediation.md`, and each spec §3/§11 mechanism description matches its `root-cause.md`.
- **No broken H→R mapping.** Spec §7 H1→R1/R3/R5/R6, H2→R1/R2/R5/R6, H3→R3/R4/R6/R7, H4→R5, H5→R1/R3/R4/R5/R6 are all internally coherent with generalized-remediation-set.md (R1–R7 all present) and its R→E coverage matrix.
- **No orphan contract field / no orphan card.** Every §6.2 `_path` field has a producing §7 card; every §7 card feeds a §6.2 field.
- **Real mechanisms in §10.** `make sync-dev` (Makefile:109), `make verify-sync` (Makefile:166), `.claude/`-mirror gitignore rule all real.

### Non-blocking spec self-consistency notes (reconcile in spec text, NOT code-driven task items)

- **F1:** §8 report "Closure verdict" enum (`pass|blocked|advisory`, spec line 311) omits `not_applicable` present in §6.2 `pipeline_hardening_verdict` (line 105). Cosmetic — §8 covers the N/A case via the separate "Applicability" line. The builder may add a single reconciliation note item, but it is spec-text alignment, not a stale-path fix. Do NOT treat as a code-contradiction.
- **F2:** §6.2 `_path` fields (per-run produced artifacts) vs §9 new ref files (per-skill templates) are different artifact classes; naming differs by design. No conflict; flagged only so the builder distinguishes "create ref template" from "emit runtime path" when authoring items.

### Claims that name live code but are NOT spec edit-targets (verified at evidence-file level only)

- E4 `root-cause.md` cites `PrdExecutor._evaluate_gate` and `pipeline.gates.gate_passed`. These appear only in frozen evidence, not in §9's edit list. The protocol is mechanism-based (issue-agnostic), so the builder must NOT create task items that edit PRD/pipeline source — the hardening lands entirely in the `sc-troubleshoot-protocol` skill + refs + command per §9. Treat any builder impulse to "fix the PRD evaluator" as out-of-scope drift.
