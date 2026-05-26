# D-0041 — T04.01 Spec: FR-CONV.4 Axis Overlay Wrapper

**Task:** T04.01 (Phase 4 — M4 Five Adversarial Axes Overlay)
**Roadmap items:** R-070
**Date:** 2026-05-17
**Status:** PASS (wrapper landed at PR-07 commit `0abf897`; verified for M4 entry)
**Tier:** STANDARD
**Confidence:** [█████████-] 90%

---

## 1. Scope

T04.01 lands the FR-CONV.4 Five Adversarial Axes overlay wrapper across
`rf-qa-qualitative.md` (task-qualitative phase header subsection +
output-template axis column) and the `task-builder` SKILL.md
(task-qualitative spawn-prompt INSTRUCTIONS block). The wrapper
operationalises the PR-07 5-axis adversarial taxonomy (drift,
contradictions, omissions, weakened-criteria, invented-content) as a
sharpening overlay across the existing 15-item task-qualitative
checklist — overlay-only, no new code path, no new stage.

The wrapper IS the framework that subsequent Phase-4 tasks fill in:
- **T04.02 / D-0042** populates the AX-1 (Drift) + AX-2 (Contradictions)
  canonical-axes block entries.
- **T04.03 / D-0043** populates AX-3 (Omissions) + AX-4
  (Weakened-criteria) entries.
- **T04.04 / D-0044** populates AX-5 (Invented-content) entry.
- **T04.05 / D-0045** wires the `none` sentinel value (≠ N/A) +
  `drift-axis-inactive` annotation emitter for GOAL-baseline-absent
  fixtures.
- **T04.07 / D-0046** adds the `axis` column to the Items Reviewed table
  between `Check` and `Result` (rf-qa-qualitative.md:675-714).
- **T04.08 / D-0047** inserts the `### Five Adversarial Axes` header
  subsection BEFORE the 15-item Checklist header.
- **T04.09 / D-0048** verifies the 15-item checklist body byte-stable.
- **T04.10 / D-0049** verifies the severity-floor block (786-795)
  byte-stable.
- **T04.11 / D-0050** finalises the COMP-004-M4 axis-column edit at
  675-714.
- **T04.13 / D-0051** wires the COMP-001-M4 SKILL.md
  task-qualitative-prompt axis directive at SKILL.md:~961.
- **T04.14 / D-0052** commits TEST-011..014 axis-overlay fixtures.
- **T04.15 / D-0053** lands MIG-004 strictly-additive single commit.

T04.01 itself is the "wrapper is present, overlay-only, INV-013
composition-safe with inherited structural PASS" gate that unblocks all
of the above.

## 2. Wrapper anatomy

### 2.1 Consumer side — `src/superclaude/agents/rf-qa-qualitative.md`

Three insertion regions, all landed at commit `0abf897` ("PR-07
adversarial category naming (5-axis overlay)"):

| Region | Lines (post-MIG-003) | Purpose |
|---|---|---|
| Five Adversarial Axes header subsection | 528 | `#### Five Adversarial Axes (PR-07 — applied as a sharpening overlay across all 15 checks below)` — sits BEFORE `#### Checklist (15 items)` (line 538). |
| Five-axes prose body | 530–536 | One paragraph + 5 bullets (Drift, Contradictions, Omissions, Weakened criteria, Invented content). Drift bullet carries the BUILD_REQUEST.GOAL-baseline requirement and the `drift-axis-inactive` fallback rule. Contradictions bullet pins the severity floor to IMPORTANT (cf. Critical Rule #6). |
| Items Reviewed table `axis` column | 700+ (M4 axis-column-edit pending in T04.07 / T04.11) | Column header annotation directive present in the surrounding prose at 530; the column structure itself is finalised by T04.07 / T04.11 (D-0046 / D-0050). |

The pre-existing **15-item checklist body** at lines 538–573 (15
numbered items between `#### Checklist (15 items)` and `### Adaptation
Guidance`) is **not touched** by the wrapper hunks; the wrapper sits
above the checklist as an overlay rather than rewriting any check.

The pre-existing **severity-floor / Critical Rules block** at
`rf-qa-qualitative.md:786-795` is **not touched** by the wrapper hunks
either; T04.10 (D-0049) will hash-verify this preservation post-M4.

### 2.2 Producer side — `src/superclaude/skills/task-builder/SKILL.md`

One insertion region, landed at commit `0abf897`:

| Region | Lines (post-MIG-003) | Purpose |
|---|---|---|
| Task-qualitative INSTRUCTIONS axis directive | 1158–1163 | "Apply the 5 Adversarial Axes (PR-07) as a sharpening overlay across all 15 checks: drift, contradictions, omissions, weakened-criteria, invented-content. Annotate every FAIL finding with the most-specific axis in the Items Reviewed table's Axis column. The drift axis requires a BUILD_REQUEST.GOAL baseline; if no GOAL verbatim is reachable, mark drift-axis-inactive and proceed with the other four axes." |

The COMP-001-M4 finer-grained axis-annotation directive at the
`SKILL.md:~961` site (table-row "Axis: AX-1..AX-5 / none" directive)
remains scheduled for T04.13 / D-0051 — that is **NOT** in T04.01's
scope; T04.01 only verifies the PR-07-landed wrapper INSTRUCTIONS block
above is present and overlay-only.

## 3. Invariants enforced by the wrapper

| Invariant | Enforcement site | Wrapper guarantee |
|---|---|---|
| INV-013 (composition with inherited structural PASS) | rf-qa-qualitative.md 530–536 + SKILL.md 1158–1163 | Axes are explicitly framed as **NOT new checks** — they are adversarial lenses applied to items the consumer still runs (i.e., items NOT covered by the Inherited Structural Verdict PASS list per FR-CONV.3). The PR-07 prose at line 530 reads "These axes are NOT new checks — they are adversarial lenses that sharpen the existing 15-item checklist." This forecloses (a) axis-from-overlay substitution for a structural check and (b) PASS-from-inheritance substitution for a semantic check. T04.05 + T04.14 TEST-013 enforce the composition further. |
| Overlay-only constraint (CB-3) | Whole wrapper (rf-qa-qualitative.md 528–536, SKILL.md 1158–1163) | No new code path is introduced. The wrapper is prose-only inside markdown agent definitions; no conditional branch, no new pipeline stage, no new agent file, no new tool. T04.08 + T04.09 byte-diff-verify the 15-item checklist body is unchanged. |
| 15-item checklist body byte-stability | rf-qa-qualitative.md 538–573 (untouched by wrapper) | Wrapper sits above the checklist; the 15 numbered items between line 542 (item 1 "Gate/command dry-run") and line 573 (item 15 "Cross-reference accuracy for templates") are preserved verbatim. T04.09 (D-0048) hash-verifies post-M4. |
| Contradictions severity floor (IMPORTANT/CRITICAL) | rf-qa-qualitative.md 533 (axis bullet) + rf-qa-qualitative.md 786–795 (Critical Rule #6 block, untouched) | The Contradictions axis bullet at line 533 explicitly pins the severity floor: "Severity floor: IMPORTANT (cf. Critical Rule #6)." The canonical floor itself at :786–795 is untouched by the wrapper. T04.10 (D-0049) hash-verifies post-M4. |
| drift-axis-inactive fallback (when GOAL baseline absent) | rf-qa-qualitative.md 532 (Drift bullet) + SKILL.md 1162–1163 | When no BUILD_REQUEST.GOAL verbatim is reachable in the spawn prompt or task file, the Drift axis is INACTIVE for the review and the consumer annotates `drift-axis-inactive`; the other four axes proceed. T04.05 (D-0045) finalises the annotation emitter; T04.14 TEST-013 enforces. |

## 4. Why the wrapper was already landed at `0abf897`

Commit `0abf897` ("PR-07 adversarial category naming (5-axis overlay)")
landed the wrapper during the PR-07 intent-port cycle that fed this
release. The release spec calls this out: M4 builds on the wrapper that
PR-07 established. T04.01 is the formal verification gate that the
wrapper is present, unchanged in src↔.claude parity, INV-013
composition-safe, and overlay-only as required by Phase 4's entry
conditions.

Any future modification to the wrapper structure must go through one of
the subsequent Phase-4 tasks (T04.02–T04.15), each of which has its own
acceptance criteria and (for T04.15 / MIG-004) sub-agent verification.

## 5. Rollback path

As stated in roadmap row R-070: **revertable by removing axis column +
annotation; 15-item checklist untouched.** Mechanically:

1. In `rf-qa-qualitative.md`, delete the `#### Five Adversarial Axes`
   subsection at lines 528–536. The 15-item Checklist header at line 538
   and its body at lines 542–573 remain untouched.
2. In `rf-qa-qualitative.md`, drop the `Axis` column from the Items
   Reviewed table (the column edit lands in T04.07 / T04.11; revert is
   the inverse).
3. In `rf-qa-qualitative.md`, remove the `drift-axis-inactive`
   annotation rule (lands in T04.05; revert removes the bullet).
4. In `task-builder/SKILL.md`, delete the axis-overlay INSTRUCTIONS
   block at lines 1158–1163 and the COMP-001-M4 directive at ~961 (when
   landed in T04.13).
5. The consumer behavior reverts to the pre-PR-07 15-item-only
   structural-and-qualitative check.

`FF_FIVE_ADVERSARIAL_AXES` is the logical feature-flag governing this
overlay; cleanup is consolidated in M7 (release-spec §8.3, M7 row).

## 6. Cross-references

- Phase 4 task spec: `.dev/releases/current/task-builder-merge/phase-4-tasklist.md` T04.01
- Roadmap row: R-070 (M4 first row)
- Release spec: release-spec.md §4.6 (sequencing), §8.3 (governance,
  M7 FF_FIVE_ADVERSARIAL_AXES row)
- INV-013 source: `.dev/tasks/done/TASK-TDD-20260514-121250/research/14-invariant-preservation.md:36`
  ("ADDRESSED LOW (probe line 23; routed because the composition matters)")
- PR-07 landing commit: `0abf897`
- T04.08/T04.09/T04.10 are the byte-stability gates that hash-verify the
  wrapper remained overlay-only after the M4 finishing edits.

## 7. Acceptance criteria mapping

| AC | Met by | Evidence |
|---|---|---|
| `grep -n "Five Adversarial Axes" rf-qa-qualitative.md` returns line N preceding `Checklist (15 items)` | Wrapper landed at 528 < 538 | `D-0041/evidence.md` §1 |
| Wrapper does not introduce a new conditional code path (overlay-only) | Prose-only markdown insertions; no .py / .sh / new agent / new pipeline stage touched | `D-0041/evidence.md` §2 |
| 15-item checklist body unchanged | Wrapper sits BEFORE the checklist; items 1–15 at lines 542–573 verbatim | `D-0041/evidence.md` §3 |
| Evidence at `D-0041/evidence.md` | This file's sibling | `D-0041/evidence.md` exists |
