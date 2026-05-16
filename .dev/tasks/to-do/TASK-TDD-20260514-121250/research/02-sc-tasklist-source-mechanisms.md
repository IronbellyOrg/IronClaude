# Research: sc-tasklist-protocol Source Mechanisms (Intent-Port Reference)

**Status:** Complete
**Date:** 2026-05-14
**Agent type:** Doc Analyst
**Source:** src/superclaude/skills/sc-tasklist-protocol/SKILL.md (1,390 lines)

**Important:** This skill is NOT modified by the Task-Builder Convergence v3.9 release. It is read here as the source of the 5 mechanisms being intent-ported into task-builder. The five mechanisms (TB-Add catalogue, Execution Context header concept, Inherited Structural Verdict origin, Five Adversarial Axes naming, Monotonicity + regression stop-conditions) are extracted as INTENT, not implementation, per FINAL-REPORT §6.3.

---

## 1. Source-of-Truth Structure for Each Imported Mechanism

### (a) TB-Add Catalogue — Source: Stage 6 Structural + Semantic + Sprint-Compat Quality Gates (lines 979-1034)

The sc-tasklist Stage 6 gate is actually **three sub-gates totaling 20 numbered checks** (not 17, despite the Stage 6 completion message at line 1357 stating "all 17 checks passed" — see §5 Stale Documentation).

**Sub-gate 1 — Sprint Compatibility Self-Check (checks 1-8), lines 983-992:**
1. `tasklist-index.md` exists + has Phase Files table
2. Every phase file referenced in index exists in bundle
3. Phase numbers contiguous (no gaps)
4. All task IDs match `T<PP>.<TT>` zero-padded format
5. Every phase file starts with `# Phase N -- <Name>` level-1 heading + em-dash
6. Every phase file ends with end-of-phase checkpoint task
7. No phase file contains Deliverable Registry / Traceability / templates
8. Index contains literal phase filenames in at least one table cell

**Sub-gate 2 — Semantic Quality Gate (checks 9-12 plus a 5th un-numbered "Acceptance criteria completeness" rule), lines 994-1003:**
9. Every task has non-empty Effort, Risk, Tier, Confidence, Verification Method
10. All Deliverable IDs (D-####) globally unique across bundle
11. No task has placeholder/empty description ("TBD"/"TODO"/title-only)
12. Every task has at least one Roadmap Item ID (R-###) — no orphan tasks
(unnumbered) Acceptance criteria completeness: at least one bullet names specific, objectively-verifiable output

**Sub-gate 3 — Structural Quality Gate (checks 13-20), lines 1021-1032 (markdown table):**
| Check ID | Check |
|---|---|
| 13 | Task count bounds: every phase has >=1 and <=25 tasks |
| 14 | Clarification Task adjacency: tasks appear immediately before their blocked task |
| 15 | Circular dependency detection: no A->B->C->A chains |
| 16 | XL splitting enforcement: EFFORT=XL tasks must have subtasks |
| 17 | Confidence bar format consistency: all use the standard pattern |
| 18 | Checkpoint task emission: every checkpoint emitted as `### T<PP>.<NN> -- Checkpoint:` heading |
| 19 | End-of-phase position: highest `<NN>` in its phase, no regular task following |
| 20 | Checkpoint Report Path presence: every checkpoint task includes the path line |

**Per release-spec mapping (CB-3, §2 below): checks 11, 13, 14, 15, 16, 17 are intent-imported as TB-Add-1..8; checks 1-8 (Sprint Compatibility), 18-20 (checkpoint/sprint-CLI specific), and 4-5 (T<PP>.<TT> format, em-dash phase heading) are bundle-specific and REJECTED for the single-MDTM task-builder output.**

Target task-builder location: per PRD §14.1, TB-Add-1..8 land in `task-builder/SKILL.md` Phase 1 quality-gate section. Confirm via Research-Doc 01.

---

### (b) Execution Context Header Concept — Source: WEAK / IMPLICIT (sc-tasklist has no direct analogue)

There is **no single "Execution Context header" block** in sc-tasklist comparable to a task-wide preamble. The closest structural analogues are:

- **`tasklist-index.md` Metadata & Artifact Paths table** (lines 617-647) — supplies cross-phase metadata (Sprint Name, Generator Version, TASKLIST_ROOT, Total Phases, Complexity Class, Primary/Consulting Personas, artifact paths). This is the **bundle-wide** context block.
- **Phase Heading + Phase Goal paragraph** (lines 775-783): `# Phase N -- <Phase Name>` + 2-3 sentence phase goal. This is the **phase-wide** context block.
- **§3 Artifact Paths block** (lines 60-86) defining `TASKLIST_ROOT` derivation rules — read by the generator as context, not emitted as a runtime header.

**Conclusion for PR/intent-port:** sc-tasklist's bundle-level context is split across the index Metadata table and per-phase headings. The "Execution Context header" being imported into task-builder is a **conceptual port** (intent: one tasklist-wide context block at the top of the MDTM output), not a verbatim copy. Tag the port as `CONCEPT-PORT-FROM-INDEX-METADATA` rather than `LITERAL-PORT`.

Target task-builder location: per PRD §14.1, the Execution Context header is inserted at the top of task-builder's MDTM template.

---

### (c) Inherited Structural Verdict Origin — Source: WEAK / IMPLICIT, supports PRD CASE-B classification

Searching the full file for `inherit*`, `verdict`, `passthrough` yields only two hits:

- **Line 457** (Section 5.1 Checkpoint deliverables): *"each checkpoint deliverable traces to the roadmap item(s) of the last regular task it gates (**inherited**), so checkpoint outputs remain linked into the Traceability Matrix."* — This is **traceability inheritance** (R-### IDs), NOT a structural-verdict passthrough between Stage 6 sub-gates.
- **Line 875** (phase-file task field): `| Roadmap Item IDs | <inherited from last regular task in range> |` — Same traceability-inheritance pattern, applied to checkpoint tasks.

There is **no mechanism** in sc-tasklist where a structural gate's PASS/FAIL verdict is explicitly inherited by a downstream gate. Stage 6 is monolithic: "If any check 1-20 fails, fix it before writing any output file" (line 1034) — there is no inter-gate verdict passthrough. Stage 7 (Roadmap Validation) is gated by Stage 6 completion (line 1318), but that is a stage-dependency, not a verdict-inheritance.

**Conclusion for PR-04:** This is **CASE-B (sc-tasklist has the conceptual mechanism — traceability inheritance — but is silent on structural-verdict passthrough)**, consistent with the PRD framing. The PR is importing the *naming pattern* for a verdict-inheritance mechanism into task-builder, without an exact line-level source. Tag as `CONCEPT-NAMING-IMPORT` not `LITERAL-PORT`.

Target task-builder location: per PRD §14.1, "Inherited Structural Verdict" notation in task-builder Phase-2 gate section.

---

### (d) Five Adversarial Axes Naming — Source: Stage 7 Validation Instructions (lines 1108-1127) — VERBATIM SOURCE

This is the **strongest, literal source** of the five mechanisms. The 5 axes are defined inside the per-agent validation prompt at lines 1112-1117:

```
> For each task in your assigned range, check:
> 1. **Drift**: Does the task accurately reflect the roadmap requirement it traces to (via `R-###`)? Are acceptance criteria, validation commands, and deliverables faithful to the roadmap?
> 2. **Contradictions**: Does the task contradict any roadmap statement? Does it claim capabilities, fallbacks, or behaviors the roadmap does not support?
> 3. **Omissions**: Does the roadmap require something for this task's scope that the task does not include? Are exit criteria, test commands, or rollback requirements missing?
> 4. **Weakened criteria**: Are checkpoints, acceptance criteria, or validation steps weaker than what the roadmap specifies?
> 5. **Invented content**: Does the task introduce requirements, tests, behaviors, or constraints not present in the roadmap?
```

**Verbatim axis names (the 5):**
1. Drift
2. Contradictions
3. Omissions
4. Weakened criteria
5. Invented content

**Supporting context (the §7 purpose statement at line 1089):** *"Detect drift, contradictions, omissions, weakened criteria, and invented content by comparing every generated task against the source roadmap."*

**Finding-structure schema (the per-axis finding template) at lines 1119-1126:**
- Severity: High | Medium | Low
- Task ID: T<PP>.<TT>
- Problem: 1-2 sentence description
- Roadmap evidence: line numbers / quoted text
- Tasklist evidence: line numbers / quoted text
- Exact fix: concrete, actionable correction

**Conclusion for PR/intent-port:** Direct LITERAL source. Names and finding-structure schema port verbatim into task-builder's adversarial-validation prompt. The 2N-agent split mechanism (lines 1091-1106) is rejected as bundle-specific (task-builder produces a single MDTM file, not N phase files — no split-point).

Target task-builder location: per PRD §14.1, the 5-axis adversarial prompt is embedded in task-builder's Phase-3 adversarial-review section.

---

### (e) Monotonicity + Regression Stop-Conditions — Source: WEAK in sc-tasklist (Stages 9-10, lines 1244-1288, partial concept)

The release-spec's reference to "Stages 9-10 of Post-Generation Roadmap Validation — source of PR-02 monotonicity + regression mechanism" overstates what sc-tasklist actually defines. The literal content:

**Stage 9 (lines 1244-1260):** Delegates to `sc:task` via Skill tool with `--compliance strict`. The orchestrator does NOT apply patches itself. Stage gate is "sc:task reports completion. All checklist items addressed." There is **no F-set / gate_failures set, no strict-shrink rule, no monotonicity invariant** in this stage.

**Stage 10 (lines 1262-1288):** Spot-Check Verification — for each finding in ValidationReport.md, read flagged section, verify exact fix applied, verify "no regression in surrounding context (e.g., the fix didn't break an adjacent checkpoint or acceptance criterion)" (line 1271), record `RESOLVED | UNRESOLVED`. **Stage gate at line 1288**: *"All findings verified. If any remain UNRESOLVED, they are logged but the skill does NOT loop."*

**Search results for monotonicity language** (grep -iE "monoton|regress|strict.*shrink|F-set|gate_fail|stop.cond"): only one hit at line 1271 ("Verify no regression in surrounding context"). No F-set definition, no strict-shrink rule, no monotonicity proof obligation.

**Conclusion for PR-02:** sc-tasklist provides the **conceptual seed** (Stage 10 regression-check + single-pass non-looping discipline) but not the formal `F = gate_failures` set or strict-shrink invariant. The PR-02 mechanism is **CONCEPT-EXTENSION**, not LITERAL-PORT. The names "monotonicity" and "regression stop-condition" appear to originate in the PRD itself, with sc-tasklist as the antecedent inspiration only.

Target task-builder location: per PRD §14.1, monotonicity invariant + regression stop-condition lives in task-builder's Phase-2-to-Phase-3 gate-transition logic.

---

## 2. CB-3 Per-Check Classification Basis

For each of the 20 sc-tasklist Stage-6 numbered checks, classify against TB-Add target IDs (per PRD-derived release-spec mapping). The release-spec's "17-point gate" appears to refer to checks 1-17 in numbering, although the actual count is 20. Per the brief, checks 11, 13, 14, 15, 16, 17 are explicitly called out as imported.

| Check # | sc-tasklist Line | Check Content (short) | Classification | TB-Add target / Rationale |
|---|---|---|---|---|
| 1 | 985 | tasklist-index.md exists with Phase Files table | REJECTED-bundle-specific | task-builder produces single MDTM file, no index |
| 2 | 986 | Every phase file referenced in index exists | REJECTED-bundle-specific | No phase files in single-MDTM output |
| 3 | 987 | Phase numbers contiguous, no gaps | REJECTED-bundle-specific | No multi-phase structure in MDTM |
| 4 | 988 | Task IDs match `T<PP>.<TT>` zero-padded | REJECTED-bundle-specific | task-builder uses MDTM checklist-item IDs, not T-IDs |
| 5 | 989 | Phase file starts with `# Phase N -- <Name>` em-dash heading | REJECTED-bundle-specific | Per-phase heading convention, N/A to single MDTM |
| 6 | 990 | Every phase file ends with end-of-phase checkpoint | REJECTED-bundle-specific | Phase-bundle-specific; no end-of-phase in MDTM |
| 7 | 991 | No phase file contains Registry / Traceability / templates | REJECTED-bundle-specific | Phase-file content-boundary rule, N/A |
| 8 | 992 | Index contains literal phase filenames | REJECTED-bundle-specific | No index in single-MDTM output |
| 9 | 998 | Every task has non-empty Effort, Risk, Tier, Confidence, Verification | NOT-RELEVANT | task-builder does not use Effort/Risk/Tier classification |
| 10 | 999 | Deliverable IDs (D-####) globally unique | NOT-RELEVANT | task-builder does not emit D-#### deliverable registry |
| 11 | 1000 | No task has placeholder/empty description ("TBD"/"TODO"/title-only) | **IMPORTED-as-TB-Add-N** (likely TB-Add-1 or TB-Add-2 per release-spec, exact ID per Research-Doc 01) | Directly applicable to MDTM checklist items — no empty/TBD items |
| 12 | 1001 | Every task has at least one R-### Roadmap Item ID | NOT-RELEVANT | task-builder has different traceability scheme (BUILD_REQUEST evidence) |
| (acceptance) | 1003 | Acceptance Criteria bullets name specific verifiable output | CANDIDATE-FOR-IMPORT (not in canonical 17-check list; consider widening) | Applicable to MDTM checklist Acceptance fields if present |
| 13 | 1025 | Task count bounds: >=1 and <=25 per phase | **IMPORTED-as-TB-Add-N** | Per release-spec call-out. For MDTM: bounds apply per MDTM file's checklist-item count |
| 14 | 1026 | Clarification Task adjacency | **IMPORTED-as-TB-Add-N** | Per release-spec. Applicable to MDTM if task-builder emits clarification items |
| 15 | 1027 | Circular dependency detection (A->B->C->A) | **IMPORTED-as-TB-Add-N** | Per release-spec. Applicable to MDTM dependency graphs |
| 16 | 1028 | XL splitting enforcement (XL must have subtasks) | **IMPORTED-as-TB-Add-N** | Per release-spec. Adaptable to MDTM "items deemed complex must decompose" pattern |
| 17 | 1029 | Confidence bar format consistency | **IMPORTED-as-TB-Add-N** | Per release-spec. Format-consistency check generalizable to MDTM if confidence bars used |
| 18 | 1030 | Checkpoint task emission as `### T<PP>.<NN> -- Checkpoint:` heading | REJECTED-bundle-specific | T-ID + checkpoint conventions are Sprint CLI specific |
| 19 | 1031 | End-of-phase position is highest <NN> in phase | REJECTED-bundle-specific | Phase-position rule, N/A to MDTM |
| 20 | 1032 | Checkpoint Report Path presence per checkpoint | REJECTED-bundle-specific | Wave 2/3 tooling-specific |

**Tally:**
- IMPORTED-as-TB-Add: 6 checks (11, 13, 14, 15, 16, 17) → maps onto TB-Add-1..8 (gap of 2 implies 2 additional TB-Adds beyond direct check-import; per PRD §14.1, these are likely synthesized: "no fluff/subjective adjectives" from Style Rule line 952 + "Minimum Task Specificity" three-criterion rule from lines 957-975).
- REJECTED-bundle-specific: 11 checks (1-8, 18-20) — Sprint CLI / phase-bundle / index-driven conventions
- NOT-RELEVANT: 3 checks (9, 10, 12) — tier/deliverable/R-ID traceability schemes unique to sc-tasklist

**Note on TB-Add-1..8 count:** The release-spec calls out 6 direct check imports (11/13/14/15/16/17). The +2 to reach 8 likely come from the **Minimum Task Specificity Rule** (lines 957-975, 3 sub-criteria: named-artifact, action-verb+explicit-object, no-cross-task-prose-dependency) and the **Task Specificity Check generation-time bullets** (lines 1005-1015). Confirm exact TB-Add IDs via Research-Doc 01 (task-builder skill architecture).

---

## 3. X-001 Rejected Blanket Rule — "No File Paths" Scope-Confinement

**Quote — Style Rules line 954:** *"Do not invent repository file paths; only use the deterministic artifact paths defined in Section 3 and Section 5.1."*

**Quote — Minimum Task Specificity Rule line 961-963:** *"**Named artifact or target**: The description names the specific file, function, endpoint, or component being operated on."*

**Surface contradiction:** Line 954 forbids "repository file paths" while line 961 requires "the specific file" to be named. The resolution in sc-tasklist is **scope-confinement**: line 954 applies to *invented/speculative* repository paths (paths the roadmap does not provide), whereas line 961 requires *concrete* artifact naming **only when the artifact is known** (e.g., from the roadmap or from supplementary TDD/PRD context).

**Why this would have broken task-builder's evidence-bound-item invariant if blanket-applied:** task-builder's per-item Context fields embed `file:line` citations as primary evidence (per BUILD_REQUEST → MDTM contract, see Research-Doc 01). A blanket-applied "no specific file paths" rule would gut this invariant — every MDTM checklist item would lose its concrete file:line evidence, reducing task-builder output to vague placeholder prose.

**The accepted scope-confinement (X-001 rejection rationale):**
- **Tasklist-wide header rule:** "no speculative file paths in the bundle-wide header / Execution Context block" — applies only to the top-of-bundle metadata, where invented paths would mislead readers
- **Per-item Context rule:** "per-item Context fields retain file:line citations" — preserves the evidence-bound-item invariant; concrete artifact citations remain mandatory at the item level

This is the X-001 outcome documented in the release-spec: header-scope rule accepted, item-scope blanket rule rejected.

Target task-builder location: per PRD §14.1, the rule is scoped to the Execution Context header section only; per-item Context fields keep their file:line citations.

---

## 4. Gaps and Questions

1. **Exact TB-Add-1..8 numbering:** The release-spec calls out 6 checks (11/13/14/15/16/17) as imported; TB-Add total is 8. The remaining 2 likely come from the Minimum Task Specificity Rule (lines 957-975) and Task Specificity Check (lines 1005-1015), but their exact TB-Add IDs are not documented in sc-tasklist — confirm via Research-Doc 01 (task-builder skill).
2. **PR-04 Inherited Structural Verdict naming source:** Where in the codebase (if anywhere) does the term "Inherited Structural Verdict" first appear? sc-tasklist uses only "(inherited)" parenthetical and "inherited from last regular task in range" — neither is a verdict-passthrough mechanism. If the term is PRD-original, document as CASE-B per PRD framing.
3. **PR-02 monotonicity formalism:** sc-tasklist Stage 10 has only "no regression in surrounding context" prose (line 1271) and a non-looping rule (line 1288). The formal F-set + strict-shrink rule must originate in the PRD/TDD itself, not in sc-tasklist. Confirm by reading the PRD (Research-Doc 00).
4. **17 vs 20 check count discrepancy:** Stage 6 completion message at line 1357 says "Self-Check: all 17 checks passed" but the actual numbered checks are 1-20. Is "17" a stale counter (legacy from before checks 18-20 were added in v3.7 Wave 4 — see line 1030's "Cause-2 fix (v3.7 Wave 4)" annotation)?
5. **Acceptance Criteria completeness rule:** Lines 1003 is un-numbered. Should it be check 12.5 (between 12 and 13) or check 12-alpha? Affects classification: if numbered, it would be a candidate for import; as currently un-numbered it appears outside the canonical "17-check" list.

---

## 5. Stale Documentation Found

| Tag | Location | Claim | Evidence |
|---|---|---|---|
| CODE-CONTRADICTED | Line 1357 ("Stage 6: 'Self-Check: all 17 checks passed'") | Claims 17 checks | Actual numbered checks in §Self-Check + Semantic + Structural Quality Gates = 20 (checks 1-20, plus 1 un-numbered Acceptance Criteria rule at line 1003). Likely stale: v3.7 Wave 4 added checks 18-20 (per line 1030 annotation) without updating the completion message. |
| CODE-CONTRADICTED | Section heading "Sprint Compatibility Self-Check (Pre-Write, Mandatory)" at line 979 | Header implies the section is bounded | The section actually contains three sub-gates (Sprint Compat 1-8, Semantic 9-12+acceptance, Structural 13-20); the wrapper heading is misleading. The Stage 6 task description should reference all 20 checks, not "17". |
| CODE-VERIFIED | Lines 1112-1117 (five adversarial axes) | Five axes named: Drift / Contradictions / Omissions / Weakened criteria / Invented content | Verified verbatim in source; matches release-spec naming exactly. |
| CODE-VERIFIED | Lines 1025-1032 (Structural Quality Gate table) | Eight structural checks numbered 13-20 | Verified; table is well-formed. |
| UNVERIFIED | Release-spec claim "PR-02 source: Stages 9-10 monotonicity + regression mechanism" | Asserts sc-tasklist defines F-set / strict-shrink | sc-tasklist Stages 9-10 contain only delegation-to-sc:task, "no regression in surrounding context" prose, and a non-looping rule. The formal F-set / monotonicity invariant is NOT in sc-tasklist; it must be PRD-original. Mark mechanism (e) as CONCEPT-EXTENSION rather than LITERAL-PORT. |
| UNVERIFIED | Release-spec claim "PR-04 Inherited Structural Verdict from sc-tasklist" | Implies a verdict-passthrough source exists | Only matches in sc-tasklist are traceability-inheritance (line 457, line 875) — not verdict passthrough. PR-04 is CASE-B per PRD framing. |
| CODE-VERIFIED | Line 954 ("Do not invent repository file paths") | Blanket-style rule | Verified; line 961 requires named artifacts. Tension is real, X-001 scope-confinement resolution is justified. |

---

## 6. Summary (Executive)

The sc-tasklist-protocol SKILL.md provides one **strong literal source** (mechanism (d): the 5 adversarial axes — Drift, Contradictions, Omissions, Weakened criteria, Invented content — at lines 1112-1117), one **medium-strength check-list source** (mechanism (a): Stage 6 structural-gate checks 11/13/14/15/16/17 are direct TB-Add candidates with the remaining 2 of TB-Add-1..8 coming from the Minimum Task Specificity Rule at lines 957-975), and **three weak/concept-only sources** (mechanisms (b) Execution Context header, (c) Inherited Structural Verdict, (e) Monotonicity + regression — sc-tasklist has thematic seeds but no formal/literal definition). PR-04 should be classified CASE-B per PRD framing (sc-tasklist has implicit traceability-inheritance but no structural-verdict passthrough); PR-02 should be classified CONCEPT-EXTENSION (sc-tasklist Stage 10 prose only, no F-set/strict-shrink formalism). The X-001 "no file paths" rule resolves cleanly via scope-confinement: header-only blanket rule accepted, per-item file:line citations preserved (protecting task-builder's evidence-bound-item invariant). One documentation defect found in sc-tasklist itself: Stage 6 completion message claims "17 checks" but the gate actually contains 20 numbered checks plus 1 un-numbered Acceptance Criteria rule (stale legacy from pre-v3.7-Wave-4).

---

**Status:** Complete

