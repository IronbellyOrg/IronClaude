# D-0053 — T04.15 Spec: MIG-004 PR-07 Landing Migration

**Task:** T04.15 (Phase 4)
**Roadmap items:** R-088, R-089 (`roadmap.md:282` MIG-004 governance row + `roadmap.md:283` / `:455` FF_FIVE_ADVERSARIAL_AXES governance row)
**Date:** 2026-05-17
**Status:** PASS (landed at commit `<MIG-004-SHA>` — captured in `evidence.md` § 2)

---

## 1. Scope

MIG-004 is the single-commit landing migration for FR-CONV.4 — the
Five Adversarial Axes overlay (PR-07) inserted as a sharpening lens
ABOVE the rf-qa-qualitative 15-item Task-File Qualitative Review
checklist, plus the canonical `{AX-1, AX-2, AX-3, AX-4, AX-5, none}`
vocabulary, the `axis` column on the Items Reviewed table, and the
`drift-axis-inactive` Summary-block annotation when no
BUILD_REQUEST.GOAL verbatim baseline is reachable. The migration is
strictly additive in the sense required by `roadmap.md:282` ("revertable
by removing axis column + drift-axis-inactive annotation; 15-item
checklist untouched"):

- The 15-item checklist body at the post-M4 lines corresponding to the
  original `rf-qa-qualitative.md:527-583` span is byte-identical
  pre/post (verified by TEST-014 baseline hash and the
  quality-engineer sub-agent — see `evidence.md` § 4).
- The severity-floor / Critical Rules block (originally at
  `:786-795`, post-M4 at `:831-840` due to strictly-additive
  insertions above; baseline SHA-256
  `770f439517cab45a605f0e098561946f04485d406393567fa8bbeaba9de91fc7`)
  is byte-identical pre/post. Rule #6 — "Contradictions are always
  IMPORTANT or CRITICAL" — appears verbatim with no softening tokens.
- MIG-002 Execution Context Header emission unchanged.
- MIG-003 Inherited Structural Verdict + Self-Audit (INV-013
  composition, INV-019 obligation, INV-002 freshness, INV-010 dynamic
  enumeration) unchanged.
- BUILD_REQUEST schema, MALFORMED retry max-2 failure-mode, TB-Add-7
  degraded-form tolerance, TB-Add-8 evidence-binding all preserved.

## 2. FF_FIVE_ADVERSARIAL_AXES feature flag

| Field | Value |
|---|---|
| Flag name | `FF_FIVE_ADVERSARIAL_AXES` |
| Designation | **Logical flag** (no runtime gate; the overlay is a behavior-only edit to rf-qa-qualitative.md + SKILL.md, so the flag is a documentation/governance handle, not an executable switch). |
| Scope | (a) `### Five Adversarial Axes` header subsection inserted at `src/superclaude/agents/rf-qa-qualitative.md:528` (pre-existing line `527`/`546` shift); (b) AX-1..AX-5 canonical entries + `none` sentinel + `drift-axis-inactive` Summary-block annotation at the same subsection; (c) `axis` column inserted between `Check` and `Result` on the Items Reviewed table (post-M4 line `709`; pre-M4 `675-714` span); (d) Canonical annotation rules block immediately following the axis enumeration; (e) Trailing Summary-block annotation guidance for `drift-axis-inactive`; (f) SKILL.md A.10.5 spawn-prompt directive at `src/superclaude/skills/task-builder/SKILL.md:1158-1170` (axis-annotation directive citing `{AX-1..AX-5, none}` vocabulary and forbidding `N/A`/`n/a`/`—`/blank). |
| Default value at M4 | `ON` (DEFAULT-ON at landing — overlay materialises in every task-qualitative run). |
| Activation commit | `<MIG-004-SHA>` on `feat/mig-002-execution-context-header` (Phase 4 piggybacks the M2 landing branch; final merge to `master` follows release-spec §19.x sequencing). |
| Governance file | This spec (`D-0053/spec.md`). |
| Revert path | **Removes overlay; checklist intact.** See § 3 below for the per-line procedure. The 15-item checklist body and severity-floor block remain byte-identical under rollback. |
| Cleanup gate | **K-004 axis-distribution audit** (release-spec §7 K-004 row 426 + `roadmap.md:559` R-009 row): post-GA, measure the empirical distribution of axis annotations across rf-qa-qualitative runs. If any one axis dominates ≥80% of annotations or the `none` sentinel falls below the noise floor of expected passing checks, the overlay vocabulary is re-tuned before consolidation. |
| Cleanup window | **M7 consolidation** (post-M3..M6 stabilization; per `roadmap.md:283` row 20 "Enabled at merge; cleanup at GA + 30 days post-axis-distribution audit (K-004); owner rf-qa-qualitative maintainer; consolidated cleanup tracking in M7") — when K-004 reports a healthy distribution AND no axis-annotation regressions are observed across M4..M6, the overlay is folded into the rf-qa-qualitative agent contract proper and the flag is retired. Operationalised by the OPS-001 runbook (M7). |
| Cross-references | Phase 4 task T04.15 (this artifact); M7 consolidation window (OPS-001 runbook + K-004 gate); roadmap items R-088 (single-commit landing) and R-089 (governance); roadmap.md:282 MIG-004 governance row; roadmap.md:283 / :455 FF_FIVE_ADVERSARIAL_AXES governance table rows; roadmap.md:559 R-009 K-004 risk-registry row; release-spec.md:426 K-004 row; D-0025 (MIG-002 governance, cross-flag M7 coordination); D-0039 (MIG-003 governance, INV-013 composition reference). |

## 3. Per-line rollback path (commit body authoritative)

Documented in the MIG-004 commit body (`git log <MIG-004-SHA>`):

1. **`rf-qa-qualitative.md`** — remove the `axis` column from the
   Items Reviewed table header at post-M4 line ~709 (revert the
   header line `| # | Check | axis | Result | Evidence |` to the
   M3 baseline `| # | Check | Result | Evidence |`). Drop the
   AX-1..AX-5 / `none` / `drift-axis-inactive` annotation rows from
   the example body row at post-M4 line ~711.
2. **`rf-qa-qualitative.md`** — remove the `### Five Adversarial
   Axes (PR-07 — applied as a sharpening overlay across all 15
   checks below)` heading at post-M4 line 528 and its body
   (AX-1..AX-5 definitions, `none` sentinel rule, `drift-axis-inactive`
   Summary-block annotation rule). The `#### Checklist (15 items)`
   header at post-M4 line 546 (which originally was at line 527
   pre-M4) re-anchors to its pre-M4 position; the 15-item checklist
   body is untouched at every step.
3. **`rf-qa-qualitative.md`** — remove the trailing axis-annotation
   guidance block at post-M4 line ~714+ (the "subsection under 'Five
   Adversarial Axes' for the binding spec" paragraph and the
   `drift-axis-inactive` Summary-block guidance). The Summary block
   itself reverts to its M3 shape (no axis-related annotation).
4. **`SKILL.md`** — remove the axis-annotation directive paragraph
   at `:1158-1170` from the A.10.5 spawn prompt (the "Apply the 5
   Adversarial Axes (PR-07) as a sharpening overlay …" paragraph
   ending at "… emit the literal `drift-axis-inactive` annotation
   in the Summary block (not as an Axis-column cell value) and
   proceed with the other four axes (AX-2..AX-5)."). The preceding
   adversarial-stance language and the following make-target /
   shell-precondition guidance both remain intact.
5. **`tests/audit/`** — the four TEST-011..014 fixtures
   (`test_five_axes_overlay.py`, `test_axis_column_populated.py`,
   `test_drift_axis_inactive_when_no_goal_baseline.py`,
   `test_severity_floor_unweakened.py`) may remain in the tree
   under rollback — they fail-closed on the absence of the
   overlay, providing automatic verification that the rollback
   completed. Alternatively they can be removed for a clean revert;
   the severity-floor fixture's baseline hashes remain valid
   without the overlay (the slice is anchored on the Critical Rules
   header, which is unchanged).

**Invariant during rollback:** the 15-item checklist body
(`rf-qa-qualitative.md:527-583` pre-M4; post-M4 the same content at
shifted line numbers) and the severity-floor / Critical Rules block
(`rf-qa-qualitative.md:786-795` pre-M4; post-M4 `:831-840` per
TEST-014 baseline) are both untouched at every step. MIG-003
Inherited Structural Verdict / Self-Audit, MIG-002 Execution Context
Header, BUILD_REQUEST 15-field schema, MALFORMED retry max-2,
TB-Add-7 / TB-Add-8 / Critical Rule #11 all function unchanged
under rollback.

**Fallback behavior post-rollback:** rf-qa-qualitative reverts to
the M3 baseline — the 15-item Task-File Qualitative Review runs
without the axis overlay; the Items Reviewed table reverts to a
4-column shape (`| # | Check | Result | Evidence |`); rf-qa-qualitative
reports emit no axis-column cells and no `drift-axis-inactive`
Summary-block annotation. INV-013 inherited-PASS composition,
INV-019 Self-Audit obligation, INV-002 freshness, INV-010 dynamic
enumeration all continue to function unchanged. The PR-07 axis lens
is dormant; the structural rigor of the consumer reverts to its
M3 envelope.

## 4. Acceptance Criteria mapping

| AC (phase-4-tasklist.md T04.15) | Evidence location |
|---|---|
| `make verify-sync` exits 0 immediately after MIG-004 commit | `evidence.md` § 3 (logged exit code) |
| Commit body documents axis-overlay removal as rollback path | `git show <MIG-004-SHA>` commit body, "Rollback path (per-line revert via overlay-removal)" section; cross-referenced from this spec § 3 |
| Sub-agent report confirms 15-item checklist + severity floor byte-identical | `evidence.md` § 4 (quality-engineer sub-agent verdict PASS; baseline SHA-256 `770f439517cab45a605f0e098561946f04485d406393567fa8bbeaba9de91fc7` matches across both src/ and .claude/ mirrors at post-M4 `:831-840`; Critical Rules block SHA-256 `fd7f2e457bf63ce0045ec5d7014e9af67c1b46892f49b090334be17bbd2fff0f` matches across both mirrors) |
| FF_FIVE_ADVERSARIAL_AXES `TASKLIST_ROOT/artifacts/D-0053/spec.md` records (a) logical-flag designation, (b) revert path = remove overlay, (c) cleanup gate = K-004 axis-distribution audit, (d) M7 consolidation reference | This spec § 2 (designation row "Logical flag"; revert-path row "Removes overlay; checklist intact" → § 3 procedure; cleanup-gate row "K-004 axis-distribution audit" → release-spec §7 K-004 row 426; cleanup-window row "M7 consolidation" → roadmap.md:283 row 20) |

## 5. Dependencies

- T04.14 PASS (`D-0052/evidence.md` — TEST-011..014 axis-overlay
  pytest fixtures green: 37 / 37 PASS in 0.06 s wall-clock,
  asserting axes-header-before-checklist ordering, axis-column
  populated with canonical vocabulary, `drift-axis-inactive`
  annotation literal in Summary block, and severity-floor block
  byte-identical to baseline).
- T04.13 PASS (`D-0051/evidence.md` — SKILL.md A.10.5
  axis-annotation directive inserted at `:1158-1170`).
- T04.12 mid-checkpoint PASS (`CP-P04-T07-T11.md`) — axis column +
  header subsection + 15-item body + severity floor all verified
  in mid-phase gate.
- T04.11 PASS (`D-0050/evidence.md` — COMP-004-M4 axis-column
  insertion at Items Reviewed table).
- T04.10 PASS (`D-0049/evidence.md` — severity-floor byte-stability
  audit; baseline hashes captured).
- T04.09 PASS (`D-0048/evidence.md` — 15-item checklist body
  byte-stability audit).
- T04.08 PASS (`D-0047/evidence.md` — Five Adversarial Axes header
  subsection inserted before 15-item Checklist header).
- T04.07 PASS (`D-0046/evidence.md` — Axis column added to Items
  Reviewed table).
- T04.06 mid-checkpoint PASS (`CP-P04-T01-T05.md`) — FR-CONV.4
  wrapper + AX-1..AX-5 + `none` sentinel + `drift-axis-inactive`
  annotation all verified.
- T04.05 PASS (`D-0045/evidence.md` — `none` sentinel +
  `drift-axis-inactive` annotation wired).
- T04.04 PASS (`D-0044/evidence.md` — AX-5 axis entry).
- T04.03 PASS (`D-0043/evidence.md` — AX-3 + AX-4 axis entries).
- T04.02 PASS (`D-0042/evidence.md` — AX-1 + AX-2 axis entries).
- T04.01 PASS (`D-0041/evidence.md` — FR-CONV.4 axis-overlay
  wrapper landed).
- M3 PASS (`D-0039/evidence.md`) — INV-013 inherited-PASS
  composition base, INV-019 Self-Audit obligation, INV-002
  freshness, INV-010 dynamic enumeration all in place; MIG-004
  composes on top.

## 6. Risk + mitigation

| Risk | Mitigation |
|---|---|
| 5-axis annotation ambiguity over-flags items (K-004, R-M4-1, R-009) | Overlay is annotation-only — no new code path or runtime gate. The 15-item checklist still runs unchanged; the axes are a sharpening lens, not new checks. K-004 axis-distribution audit (post-GA, before M7 consolidation) measures empirical distribution and retunes the vocabulary if any axis dominates. `roadmap.md:301` row R-M4-1 + `roadmap.md:559` R-009 + `release-spec.md:426` K-004 row jointly bind this mitigation. |
| GOAL-baseline absent silently disables drift detection without operator awareness | `drift-axis-inactive` Summary-block annotation is the canonical signal that AX-1 was lens-disabled; emitted on its own line inside the Summary block (not as an Axis-column cell value), not encoded as `Axis = N/A`, and not silently omitted. TEST-013 fixture asserts the literal annotation appears in the Summary block; the canonical-annotation-rules sub-block in rf-qa-qualitative.md (post-M4 `:538-544`) forbids cell-level placement. |
| Severity floor weakened during PR-07 wiring (Critical Rule #6 paraphrased) | T04.10 byte-stability gate captured the slice SHA-256 `770f439…` and block SHA-256 `fd7f2e4…` pre-edit; this commit's post-commit hashes match (see `evidence.md` § 4). TEST-014 fixture's `TestRule6Verbatim` class asserts the exact text `**Contradictions are always IMPORTANT or CRITICAL** — If two sections say different things about the same topic, that's never minor. Always surface contradictions.` appears verbatim, and `TestRule6Verbatim.test_no_softening_tokens_in_critical_rules_block` rejects softening tokens (`may be MINOR`, `could be MINOR`, `typically`, `should be IMPORTANT`, `consider IMPORTANT`). Mirror parity (`.claude/agents/rf-qa-qualitative.md`) also enforced. |
| Axis column drift to `N/A`/`n/a`/`—`/blank cells (escaping the lens) | SKILL.md A.10.5 directive at `:1163-1166` explicitly forbids `N/A`/`n/a`/`—`/blank for the task-qualitative phase; canonical-annotation-rules sub-block in rf-qa-qualitative.md mandates `{AX-1..AX-5, none}` only. `none` is a positive statement (axes applied, nothing fired), not an escape. TEST-012 fixture asserts no forbidden values land in the example row enumeration. |
| 15-item checklist body modified during overlay insertion | T04.09 byte-stability gate; TEST-011 fixture asserts the 15-item body content is unchanged across the overlay landing. Quality-engineer sub-agent independently re-verifies (`evidence.md` § 4). |
| Consumer relies on overlay annotation without reading the underlying check | Overlay is a sharpening lens applied to the *existing* 15 checks — every Items Reviewed row still carries the original Check column, Result column, and Evidence column. The axis column is supplementary metadata. Critical Rule #11 (reliance-vs-verification) continues to govern downstream consumers per MIG-003. |
| K-004 axis-distribution audit fails on first post-GA window | Operational rollback path: § 3 above (overlay removal; checklist intact). Consumer falls back to M3 baseline (4-column Items Reviewed table); 15-item checklist + severity floor + INV-013 / INV-019 / INV-002 / INV-010 / Critical Rule #11 all unaffected. Release-spec.md K-004 row codifies this fallback as the canonical mitigation; OPS-001 runbook (M7) operationalises the audit + retune flow. |
