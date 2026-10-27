# D-0051 — T04.13 Evidence: COMP-001-M4 SKILL.md task-qualitative prompt axis directive

**Task:** T04.13 (Phase 4 — M4 Five Adversarial Axes Overlay)
**Roadmap items:** R-083
**Date:** 2026-05-17
**Status:** PASS
**Tier:** STANDARD
**Confidence:** [████████--] 85%

---

## 0. TL;DR

The Task-Qualitative QA prompt's axis-annotation directive at `src/superclaude/skills/task-builder/SKILL.md:1158-1170` (mirror parity at `.claude/skills/task-builder/SKILL.md:1158-1170`, sha256 `8e4a367a…ffa9a916`) now binds explicitly to the canonical `{AX-1, AX-2, AX-3, AX-4, AX-5, none}` vocabulary defined at `src/superclaude/agents/rf-qa-qualitative.md:540`. Per-row annotation rule, `none` sentinel semantics, `N/A` ban, and `drift-axis-inactive` Summary-block emission are all stated verbatim against the canonical source. Edit is overlay-only inside a single fenced-block INSTRUCTIONS clause; no code-path changes.

| AC | Status | Section |
|---|---|---|
| #1 `grep -n "Axis" SKILL.md` ≥1 match | ✅ PASS (3 matches) | §1 |
| #1.alt Line-tolerance [958, 964] | ⚠️ DRIFT (documented) | §1 + spec.md §4 |
| #2 Directive references `{AX-1..AX-5, none}` vocabulary | ✅ PASS | §2 |
| #3 Evidence at `D-0051/evidence.md` | ✅ PASS | this file |
| #4 Edit confined to the named line range | ✅ PASS (≤ block boundary) | §3 |

---

## 1. AC#1 — Grep `Axis` returns ≥1 match in SKILL.md

**Command:**
```
grep -n "Axis" src/superclaude/skills/task-builder/SKILL.md
```

**Output:**
```
1160:invented-content. Every task-qualitative row's Axis column carries
1165:fired, NOT an N/A escape). `N/A`/`n/a`/`—`/blank in the Axis column
1169:the Summary block (not as an Axis-column cell value) and proceed with
```

**Interpretation:** 3 matches, all within the axis-annotation directive at lines 1158–1170. AC#1 (≥1 match) satisfied.

**Line-tolerance drift (planned-vs-actual):** the roadmap tolerance `[958, 964]` is the pre-M3 estimate; M3 (FR-CONV.3 Inherited Structural Verdict — PR-04 passthrough) and the R-038/R-039 Execution Context header rules collectively inserted ~200 lines upstream of A.10.5, shifting the directive to 1158–1170. See `spec.md` §4 for the planned-vs-actual table. This is the expected outcome of the M3→M4 sequencing documented in the roadmap; the substantive intent (axis-annotation directive inside the Task-Qualitative QA prompt) is satisfied.

## 2. AC#2 — Directive references `{AX-1..AX-5, none}` canonical vocabulary

**Command (multiline grep):**
```
rg -nU "AX-1, AX-2, AX-3,\s+AX-4, AX-5, none" src/superclaude/skills/task-builder/SKILL.md
```

**Output:**
```
1161:exactly one value from the canonical vocabulary `{AX-1, AX-2, AX-3,
1162:AX-4, AX-5, none}` — FAIL rows MUST carry the most-specific firing
```

**Cross-reference:** identical vocabulary set is declared canonical at `src/superclaude/agents/rf-qa-qualitative.md:540`:

```
The canonical Axis-column vocabulary for the task-qualitative phase is
the closed set `{AX-1, AX-2, AX-3, AX-4, AX-5, none}` …
```

Both files reference the same closed set, so the SKILL.md directive transmits a vocabulary that the consumer (`rf-qa-qualitative`) honours verbatim. AC#2 satisfied.

**Additional rules transmitted by the directive (anti-drift binding):**

| Rule | rf-qa-qualitative.md source line | SKILL.md directive line |
|---|---|---|
| `none` is a positive PASS-row statement, not an N/A escape | 542 | 1163–1165 |
| `N/A`/`n/a`/`—`/blank forbidden in Axis column for task-qualitative | 543 | 1165–1166 |
| `drift-axis-inactive` annotation goes in **Summary** block, not as Axis-column cell value | 544 | 1167–1170 |
| FAIL row MUST carry one of AX-1..AX-5 | 542 | 1162–1163 |

All four downstream rules are mirrored in the SKILL.md directive — orchestrator and consumer cannot disagree about per-row annotation semantics.

## 3. AC#4 — Edit confined to the directive block

**Approach:** `git diff` on `src/superclaude/skills/task-builder/SKILL.md` for this task.

**Command:**
```
git diff --stat -- src/superclaude/skills/task-builder/SKILL.md
git diff -- src/superclaude/skills/task-builder/SKILL.md | head -40
```

**Result:** Single hunk; the existing 6-line directive (pre-edit lines 1158–1163) was replaced with a 13-line directive (post-edit lines 1158–1170). No other lines in SKILL.md were touched. Surrounding clauses — ADVERSARIAL STANCE (line 1151), the shell-command-precondition rule (line 1165 pre-edit / 1172 post-edit), assigned_phases (line 1168 pre-edit / 1175 post-edit), QA_GATE_REQUIREMENTS reflection (line 1172 pre-edit / 1179 post-edit) — all unchanged.

Edit confined to a single fenced-block INSTRUCTIONS clause inside `### A.10.5: Task File Qualitative Validation`. No code paths added; no logic branches introduced. AC#4 satisfied (within the block; line-range drift documented in §1).

## 4. Byte-equality across `src/` ↔ `.claude/` mirror

```
sed -n '1158,1170p' src/superclaude/skills/task-builder/SKILL.md | sha256sum
8e4a367ac66a038e1b08d6b579cc7f4bdd5508ffbae57dc4291eff91ffa9a916  -

sed -n '1158,1170p' .claude/skills/task-builder/SKILL.md | sha256sum
8e4a367ac66a038e1b08d6b579cc7f4bdd5508ffbae57dc4291eff91ffa9a916  -
```

Both hashes match. `make verify-sync` reports `✅ All components in sync.` (Skills: 20, Agents: 35, Commands: 40, Hooks: 11).

## 5. Pre/post directive diff

**Pre-edit (6 lines, lines 1158–1163):**
```
Apply the 5 Adversarial Axes (PR-07) as a sharpening overlay across all
15 checks: drift, contradictions, omissions, weakened-criteria,
invented-content. Annotate every FAIL finding with the most-specific
axis in the Items Reviewed table's Axis column. The drift axis requires
a BUILD_REQUEST.GOAL baseline; if no GOAL verbatim is reachable, mark
drift-axis-inactive and proceed with the other four axes.
```

**Post-edit (13 lines, lines 1158–1170):** see `spec.md` §3 or SKILL.md:1158-1170 directly.

**Substantive deltas:**
- Adds explicit `{AX-1, AX-2, AX-3, AX-4, AX-5, none}` canonical-vocabulary reference (was absent pre-edit, even though the rf-qa-qualitative consumer enforces it).
- Promotes per-FAIL annotation to per-row annotation (every task-qualitative row, PASS or FAIL, carries an Axis value).
- Adds `none`-as-positive-statement clarification (matches rf-qa-qualitative.md:542 semantics).
- Adds explicit `N/A`/`n/a`/`—`/blank ban for the Axis column (matches rf-qa-qualitative.md:543).
- Clarifies `drift-axis-inactive` belongs in the **Summary** block, NOT as an Axis-column cell value (matches rf-qa-qualitative.md:544 — was ambiguous pre-edit).

## 6. Roadmap-item traceability

| R-id | Roadmap intent | Evidence |
|---|---|---|
| R-083 | "Axis-annotation directive at SKILL.md:~961 in Task-Qualitative prompt; instructs annotation per row." | Directive at SKILL.md:1158-1170 (post-M3 shift documented in §1 + spec.md §4); per-row annotation explicit at lines 1160–1166; canonical vocabulary at lines 1161–1162. |

## 7. Dependencies

- T04.12 (Checkpoint CP-P04-T07-T11) — **PASS** confirmed at `.dev/releases/current/task-builder-merge/checkpoints/CP-P04-T07-T11.md` (axis column, header subsection, 15-item body + severity floor all verified).
- Canonical vocabulary at `rf-qa-qualitative.md:540-544` — landed via PR-07 (T04.01 D-0041 evidence) and verified intact at T04.09 + T04.12.

## 8. Validation (manual reviewer note)

The directive binds the orchestrator-side spawn prompt to the consumer-side canonical rules byte-for-byte at the vocabulary level. A reviewer can verify in two commands:

```
grep -n "AX-1\.\.AX-5\|AX-1, AX-2, AX-3" src/superclaude/skills/task-builder/SKILL.md
grep -n "AX-1, AX-2, AX-3" src/superclaude/agents/rf-qa-qualitative.md
```

Both should return the closed set `{AX-1, AX-2, AX-3, AX-4, AX-5, none}` in matching contexts (orchestrator instruction + consumer canonical-rules subsection).

---

**Status: PASS** — all 4 acceptance criteria satisfied (AC#1 with documented line-tolerance drift; AC#2/#3/#4 literal). Ready for T04.14 (TEST-011..014 axis-overlay fixtures).
