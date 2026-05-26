# D-0028 — T03.03 Spec: API-002-M3 Spawn-Prompt Injection at SKILL.md §A.10.5

**Task:** T03.03 (Phase 3)
**Roadmap items:** R-054
**Date:** 2026-05-17
**Status:** PASS (pending sub-agent quality-engineer verification at `D-0028/quality-engineer-report.md`)

---

## 1. Scope

T03.03 implements API-002-M3 at `src/superclaude/skills/task-builder/SKILL.md` §A.10.5:

1. **Orchestrator extraction step** (directive prose at line 1100) — instructs the orchestrator to: (a) read `${TASK_DIR}qa/qa-task-validation-report.md` (rf-qa's A.10 output), (b) extract the "Items Reviewed" PASS/FAIL table **contiguously** as a single span between the `## Items Reviewed` heading and the next top-level `## ` heading, (c) splice the extracted span byte-for-byte into the rf-qa-qualitative spawn prompt as a `## Inherited Structural Verdict` section, (d) at the API-002 wire-contract position: after TARGET FILES + PROJECT CONVENTIONS, before ADVERSARIAL STANCE / INSTRUCTIONS.

2. **Verbatim splice template** — the QA prompt's `## Inherited Structural Verdict` block (lines 1127-1148) carries the heading + verbatim-embed placeholder + paraphrase guidance + ANTI-INFLATION RULE (INV-019). It sits at the API-002 wire-contract position: after PROJECT CONVENTIONS (ends line 1125) and before ADVERSARIAL STANCE (line 1150) / INSTRUCTIONS (line 1152).

API-002 is the contract; T03.02's DM-002 (3-field schema with verbatim prompt_directive and reinjection_rule lines) is the wire payload. **Note on inter-task gap:** the present branch of SKILL.md does NOT yet carry the T03.02 DM-002 verbatim lines (no `DM-002.prompt_directive:` or `DM-002.reinjection_rule:` lines in the block). T03.02's D-0027 spec states PASS, but the corresponding source-file lines are absent from this branch's `src/superclaude/skills/task-builder/SKILL.md`. T03.03 lays the splice-position contract on top of the wrapper that PR-04 (commit `3a57a0d`) established; when T03.02's DM-002 verbatim lines do land, they will populate the block in-place — the spec.md and splice-position contract in T03.03 are forward-compatible with that addition (block remains at lines 1127ff regardless of whether DM-002 verbatim lines are present inside it).

## 2. Implementation anatomy (post-T03.03 layout)

### 2.1 Orchestrator extraction directive (SKILL.md:1100)

Single paragraph immediately above `**QA prompt:**` (line 1102). Augmented in T03.03 to make extraction contiguity and splice position explicit:

| Contract element | Phrase from directive |
|---|---|
| Producer artifact | `read ${TASK_DIR}qa/qa-task-validation-report.md (rf-qa's A.10 output)` |
| **Contiguous extraction** | `Extract the "Items Reviewed" PASS/FAIL table contiguously — a single span between the ## Items Reviewed heading and the next top-level (## ) heading` |
| Byte-exact fidelity | `verbatim, with no editing/summarising/renaming/re-ordering` |
| Splice mechanism | `Splice the extracted span byte-for-byte into the rf-qa-qualitative spawn prompt as a ## Inherited Structural Verdict section` |
| **Splice position** | `at the API-002 wire-contract position: after the TARGET FILES + PROJECT CONVENTIONS context blocks and before the ADVERSARIAL STANCE / INSTRUCTIONS directive blocks` |
| Dynamic enumeration (INV-010) | `dynamically enumerate every TB-Add-* item from rf-qa.md's current checklist` |
| Freshness (INV-002) | `On EVERY fix cycle re-spawn, the orchestrator MUST re-read the freshly-written qa-task-validation-report.md and re-inject the new verdict — never reuse a stale verdict from a prior cycle` |
| Fallback | `If qa-task-validation-report.md is missing or malformed, omit the section and let rf-qa-qualitative fall back to its standalone behavior` |

### 2.2 Spawn-prompt template (SKILL.md:1102-1196, code-fenced QA prompt block)

Post-T03.03 ordering inside the code-fenced QA prompt:

| Line(s) | Section | Role |
|---|---|---|
| 1103 | ``` | Fence open |
| 1104-1109 | QA_PHASE / TASK FILE / RESEARCH DIR / TRACK GOAL | Header |
| 1111-1112 | `TARGET FILES (verify ALL …)` + placeholder | Context: file list |
| 1114-1125 | `PROJECT CONVENTIONS:` block | Context: project patterns |
| **1127-1148** | **`## Inherited Structural Verdict (rf-qa A.10 output — DO NOT re-verify)` + body + ANTI-INFLATION RULE** | **API-002 splice site (wire-contract position)** |
| 1150 | `**ADVERSARIAL STANCE:**` | Directive: stance |
| 1152-… | `INSTRUCTIONS:` | Directive: act |

Position ordering: `TARGET FILES (1111) < PROJECT CONVENTIONS (1114) < ## Inherited Structural Verdict (1127) < ADVERSARIAL STANCE (1150) < INSTRUCTIONS (1152)`. Satisfies R-054 / roadmap row 213 ("placement:after-TARGET-FILES-before-INSTRUCTIONS").

### 2.3 Spliced block contents (SKILL.md:1127-1148)

The block emits:
- Heading: `## Inherited Structural Verdict (rf-qa A.10 output — DO NOT re-verify)` (line 1127)
- Verbatim-embed placeholder for rf-qa's Items Reviewed table (lines 1128-1130)
- Paraphrase guidance for PASS / FAIL handling (lines 1132-1144)
- ANTI-INFLATION RULE (INV-019 enforcement, lines 1146-1148) — cross-references Self-Audit obligation on the consumer side
- **Forward-compat note:** when T03.02 / D-0027 implementation lands, the block will additionally carry the verbatim `DM-002.prompt_directive` and `DM-002.reinjection_rule` lines inside this range (still within the same splice position).

## 3. Invariants enforced

| Invariant | Enforcement site | Guarantee |
|---|---|---|
| **API-002 splice position** | SKILL.md:1100 directive + lines 1111 (TARGET FILES) / 1114 (PROJECT CONVENTIONS) / 1127 (heading) / 1150 (ADVERSARIAL STANCE) / 1152 (INSTRUCTIONS) | Block sits after TARGET FILES + PROJECT CONVENTIONS, before ADVERSARIAL STANCE / INSTRUCTIONS. Verified by line-number ordering grep. |
| INV-002 (freshness) | SKILL.md:1100 directive | Orchestrator re-reads rf-qa report and re-injects NEW verdict at every fix-cycle spawn boundary. T03.05 + TEST-008 (D-0036) enforce mechanically. |
| INV-010 (dynamic enumeration) | SKILL.md:1100 directive | Orchestrator pulls TB-Add catalogue live from rf-qa.md. T03.07 + TEST-010 (D-0038) enforce. |
| INV-019 (Self-Audit obligation) | SKILL.md:1146-1148 ANTI-INFLATION RULE | Consumer output MUST list (a) relied-on PASS items + (b) ≥1 semantic check. T03.04 + TEST-009 (D-0037) enforce on the consumer side. |
| Byte-exact extraction | SKILL.md:1100 directive ("verbatim, with no editing/summarising/renaming/re-ordering" + "byte-for-byte") | Static contract documented; runtime diff vs `${TASK_DIR}qa/qa-task-validation-report.md` Items Reviewed table = zero bytes. T03.11 / TEST-007 (D-0035) exercises runtime fixture. |
| Anti-inflation block byte-stability | rf-qa-qualitative.md:766-775 (untouched by T03.03) | Block byte-identical by construction (T03.03 does not touch rf-qa-qualitative.md). T03.08 / D-0032 captures formal byte-diff. |

## 4. Diff summary

Two hunks landed in `src/superclaude/skills/task-builder/SKILL.md` (mirror parity preserved via `make sync-dev`; `make verify-sync` PASS):

1. **Directive at line 1100** — augmented in place: added explicit contiguity clause (`a single span between the ## Items Reviewed heading and the next top-level (## ) heading`) and explicit wire-contract splice-position clause (`at the API-002 wire-contract position: after the TARGET FILES + PROJECT CONVENTIONS context blocks and before the ADVERSARIAL STANCE / INSTRUCTIONS directive blocks`). The "verbatim" / "byte-for-byte" / "no editing/summarising/renaming/re-ordering" phrasing was strengthened. The freshness rule (INV-002), dynamic enumeration rule (INV-010), and missing-artifact fallback clause are byte-identical pre/post.

2. **Spawn-prompt template (the code-fenced QA prompt at lines 1102-1196)** — the `## Inherited Structural Verdict` block was **relocated** from before TARGET FILES (pre-T03.03 line 1111) to after PROJECT CONVENTIONS (post-T03.03 line 1127). Block CONTENT is byte-identical pre/post — only the position changed. Pre-T03.03 placement violated R-054 (`placement:after-TARGET-FILES-before-INSTRUCTIONS`); T03.03 corrects this.

Other sections of SKILL.md (A.10.6 DM-005 published row, A.10.7 DM-002 published schema, all sections outside A.10.5) are unmodified by T03.03.

## 5. Verification

| Check | Method | Result |
|---|---|---|
| Splice position: after TARGET FILES + PROJECT CONVENTIONS, before ADVERSARIAL STANCE / INSTRUCTIONS | `grep -n "TARGET FILES\|PROJECT CONVENTIONS:\|## Inherited Structural Verdict\|\*\*ADVERSARIAL STANCE\|^INSTRUCTIONS:" SKILL.md` (output captured in §6 below) | Ordering: 1111 (TARGET FILES) < 1114 (PROJECT CONVENTIONS) < 1127 (## Inherited Structural Verdict) < 1150 (ADVERSARIAL STANCE) < 1152 (INSTRUCTIONS) — API-002 contract satisfied. |
| Heading verbatim | `grep -c "## Inherited Structural Verdict (rf-qa A.10 output — DO NOT re-verify)" SKILL.md` | 1 match at line 1127. |
| Directive present and augmented | `grep -c "API-002 wire-contract position" SKILL.md` and `grep -c "contiguously" SKILL.md` | Both 1 match at line 1100. |
| Byte-exact fidelity contract documented | `grep -c "byte-for-byte" SKILL.md` and `grep -c "no editing/summarising/renaming/re-ordering" SKILL.md` | Both 1 match at line 1100. |
| Mirror sync clean | `make verify-sync` | PASS. |

Sub-agent quality-engineer verification at `D-0028/quality-engineer-report.md` per Verification Method = Sub-agent (quality-engineer) in T03.03 task spec.

## 6. Grep evidence (live)

```
$ grep -n "TARGET FILES\|PROJECT CONVENTIONS:\|## Inherited Structural Verdict\|\*\*ADVERSARIAL STANCE\|^INSTRUCTIONS:\|API-002 wire-contract\|contiguously" src/superclaude/skills/task-builder/SKILL.md | head -15
1100: **Inherited Structural Verdict (PR-04 ...) ... Extract the "Items Reviewed" ... contiguously ... at the API-002 wire-contract position ...
1111: TARGET FILES (verify ALL — no spot-checking):
1114: PROJECT CONVENTIONS:
1127: ## Inherited Structural Verdict (rf-qa A.10 output — DO NOT re-verify)
1150: **ADVERSARIAL STANCE:** ...
1152: INSTRUCTIONS:
```

(See `D-0028/evidence.md` for the full grep transcript.)

## 7. Rollback path

Per roadmap row R-054: disable passthrough flag (`FF_INHERITED_STRUCTURAL_VERDICT`), fall back to independent structural re-checking. Mechanically:

1. In SKILL.md §A.10.5, comment out the directive paragraph at line 1100 so the orchestrator no longer runs the extraction step.
2. Comment out the spawn-prompt embed at lines 1127-1148 (the `## Inherited Structural Verdict` block). Result: rf-qa-qualitative receives no inherited verdict and falls back to its standalone Critical Rule #11 behavior (per the rf-qa-qualitative wrapper landed at T03.01 / D-0026, commit `3a57a0d`).
3. Subsequent fix-cycle re-spawns continue using the standalone path until the flag is re-enabled.

DM-005 phase contract (A.10.6) and DM-002 published schema (A.10.7) remain documentary; marking them `(inert under FF_INHERITED_STRUCTURAL_VERDICT=off)` is sufficient. Cleanup of the FF is consolidated in M7 (release spec §8.3 row 4).

## 8. Known gap: T03.02 DM-002 verbatim lines absent from this branch

D-0027/spec.md (T03.02) declares status PASS and describes lines 1132 + 1134 of SKILL.md as carrying the verbatim `DM-002.prompt_directive` and `DM-002.reinjection_rule` lines. Reality on the present branch: those two lines are NOT in the source file. The block at lines 1127-1148 carries the placeholder + paraphrase + ANTI-INFLATION RULE only.

This gap does NOT block T03.03's deliverable:
- T03.03's core contract is the **splice position** (the API-002 wire-contract location) + the **extraction rule** (contiguous span, byte-for-byte, verbatim).
- DM-002's wire payload (the verbatim prompt_directive + reinjection_rule lines) is a separate scoping concern; when its source-file lines do land in a follow-up commit, they will populate this block in-place without disturbing the T03.03 splice position.
- The T03.03 directive at line 1100 already documents the byte-exact extraction contract; DM-002's wire-payload verbatim strings are referenced from D-0027 schema (which itself sits at A.10.7 documentation, line 1265+).

Recommend: re-run T03.02's implementation (insert `DM-002.prompt_directive: "…"` and `DM-002.reinjection_rule: "…"` lines into the block at A.10.5) as a follow-up commit before T03.16 / MIG-003 landing. T03.02's gap is flagged here but is not a T03.03 blocker.

## 9. Cross-references

- Phase 3 task spec: `.dev/releases/current/task-builder-merge/phase-3-tasklist.md` T03.03 (L105-153)
- Roadmap rows: R-054 (line 213) — M3 implementation; R-022 (line 113) — `placement:after-TARGET-FILES-before-INSTRUCTIONS` contract-freeze clause
- DM-002 entity spec: T03.02 / D-0027 (3-field schema); ⚠️ verbatim-line implementation absent from current SKILL.md — see §8
- DM-005 phase contract: T02.04 / D-0019 (published at SKILL.md A.10.6, line 1226+)
- FR-CONV.3 wrapper: T03.01 / D-0026 (commit `3a57a0d`)
- Sibling edit task: T03.09 (COMP-001-M3 SKILL.md A.10.5 spawn injection edit) — verifies grep + range coverage of this T03.03 work
- Anti-inflation preservation: T03.08 / D-0032 (formal byte-diff of rf-qa-qualitative.md:766-775; out of scope for T03.03 — that file untouched here)
- Quality-engineer verdict: `D-0028/quality-engineer-report.md`
- Sub-agent evidence: `D-0028/evidence.md`
