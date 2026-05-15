# Refactoring Plan — Merge Draft B Strengths into Draft A Base

## Overview

- **Base variant:** Draft A (variant-1) — selected for Correctness 5/5 (vs B 3/5) and combined score 0.902
- **Incorporated variant:** Draft B (variant-2) — overlay decision instruments
- **Change count:** 11 incorporations + 1 X-001 reconciliation + 1 new §10 (shared assumptions) + 1 appendix (out-of-scope risks)
- **Estimated overall risk:** Low — additive overlays + provenance annotations; no removal of A content except RK-13/14/18 moved to appendix
- **Review status:** Auto-approved (non-interactive mode)

---

## Planned Changes

### Change #1 — Add ADOPT / DEFER / REJECT verdict pills to §6 candidate tables

- **Source:** Draft B §6 verdict column (B1-B20 ADOPT/DEFER/REJECT)
- **Target location:** A's §6.1 task-side candidates (TU-001..TU-006) and §6.2 sprint-side candidates (SE-001..SE-006)
- **Integration approach:** Add a new "Verdict" field to each candidate's bullet block. Map B-ID verdicts onto A's TU-/SE- IDs:
  - TU-001 ← B1 (CRITICAL FAIL) → **ADOPT**
  - TU-002 ← B2 (output-type axis) → **ADOPT**
  - TU-003 ← B3 (six principles) + B4 (anti-sycophancy slice) → **ADOPT**
  - TU-004 ← B5 (BLOCKED <0.70) → **ADOPT**
  - TU-005 ← B10 (config extraction) → **DEFER**
  - TU-006 ← (no B-ID) → **DEFER** (per debate concession)
  - SE-001 ← B15 (fail-closed empty output) → **ADOPT**
  - SE-002 ← B12 (per-task UID) → **ADOPT**
  - SE-003 ← B13 (sub-phase resume) → **ADOPT**
  - SE-004 ← B14 (ExecutionMode enum) → **ADOPT**
  - SE-005 ← B18 (GateFailureSeverity enum) → **ADOPT**
  - SE-006 ← B17 (auto-diagnostic threshold) → **DEFER**
  - Also add **Mandatory completion checklist** (B6) as TU-007 → **ADOPT** (A had this as part of TU-003 inline; B surfaces it as a separate candidate)
- **Rationale:** debate point C-002 (winner: B, confidence 92%). Reviewer-facing decision device.
- **Risk level:** Low. Pure overlay. Mark each verdict `[inference]` because verdicts are synthesized.

### Change #2 — Add S / M / L effort labels to §6 candidate tables

- **Source:** Draft B header definition + §6 effort column
- **Target location:** A's §6.1 and §6.2
- **Integration:** Add "Effort: S | M | L" field to each candidate. Mapped values per B:
  - TU-001=M, TU-002=M, TU-003=S, TU-004=S, TU-005=M, TU-006=S/M (debate concession: keep DEFER), TU-007=S
  - SE-001=S, SE-002=M, SE-003=M, SE-004=S, SE-005=S, SE-006=M
- **Rationale:** debate point C-009 (winner: B, confidence 90%). Sprint sizing.
- **Risk level:** Low. Mark `[inference]`.

### Change #3 — Convert §7 risk register to B's 6-column schema

- **Source:** Draft B §7 (ID, Risk, Sev, Like, Blast radius, Owner, Mitigation)
- **Target location:** A's §7
- **Integration:** Restructure A's table:
  - Keep ID column (RK-01..RK-20)
  - Drop Source column (move source-extract reference into the Mitigation cell as parenthetical)
  - Add Sev column (High/Med/Low). Derived from A's Blast radius and Likelihood per `[inference]` rule.
  - Keep Like column (rename Likelihood → Like for parity)
  - Keep Blast radius column
  - Add Owner column (Lead / Tier owner / Skill owner / Sprint owner / DevOps / Ops / Quality agent owner). `[inference]` per row.
  - Keep Mitigation hook column (renamed Mitigation)
- **Rationale:** debate points C-004, C-010 (winner: B, confidence 88-90%). Accountability device.
- **Risk level:** Low. Mark Sev and Owner assignments `[inference]`.

### Change #4 — Move RK-13, RK-14, RK-18 to appendix; retain RK-19, RK-20 in main register

- **Source:** Debate Round 2 concession by Variant B advocate
- **Target location:** New §7.1 "Out-of-scope risks retained for traceability" appendix immediately after main §7 risk table
- **Integration:** Move 3 rows; keep their content verbatim; add header note "These risks are out of scope for this release but retained because they document the regression surface for future releases."
- **Rationale:** Debate C-005 partial concession. Reduces main register noise while preserving A's completeness discipline.
- **Risk level:** Low.

### Change #5 — Add Blocking? Y/N flag to §8 open questions

- **Source:** Draft B §8 Blocking? column
- **Target location:** A's §8.1-§8.10 question subsections
- **Integration:** For each of A's Q1-Q14, append a "Blocking?" line. Mapping per B's commitments + debate:
  - Q1 (sentinel rename) → **Blocking? Y** (scope-boundary)
  - Q2 (caller rename) → **Blocking? Y** (paired with Q1)
  - Q3 (output-type precedence) → **Blocking? Y** (TU-002 prereq)
  - Q4 (opinion output-type detection) → **Blocking? N**
  - Q5 (BLOCKED message format) → **Blocking? N**
  - Q6 (`--skip-compliance` × BLOCKED) → **Blocking? N** (resolved: yes with `--reason`)
  - Q7 (config file materialization) → **Blocking? Y** (TU-005/TU-006 scope-boundary)
  - Q8 (skill ref path correction) → **Blocking? N**
  - Q9 (severity enum scope) → **Blocking? N**
  - Q10 (sprint result file back-compat) → **Blocking? N**
  - Q11 (telemetry metering) → **Blocking? N**
  - Q12 (tasklist keyword reconciliation) → **Blocking? N**
  - Q13 (v3.7 unfinished follow-ups) → **Blocking? N**
  - Q14 (six-principles enforcement mechanism) → **Blocking? N**
- **Rationale:** debate C-006 (winner: B, confidence 87%). Triage device.
- **Risk level:** Low.

### Change #6 — Add Options + Recommendation columns to §8 open questions

- **Source:** Draft B §8 Options + Recommendation pattern
- **Target location:** A's §8
- **Integration:** Each of A's questions gets:
  - "Options:" line enumerating (a), (b), (c) alternatives
  - "Recommendation:" line stating the synthesizer's recommended option
- **Rationale:** debate C-006. Converts exploratory questions into decision-ready ones.
- **Risk level:** Low. Mark Recommendation `[inference]` where synthesized.

### Change #7 — Apply B's Q6 resolution to A's Q6 contradiction (X-001 reconciliation)

- **Source:** Draft B §8 Q6: "(c) yes with `--reason` — preserves escape hatch; audits abuse"
- **Target location:** A's §8.3 (BLOCKED-state UX) Q6
- **Integration:** Keep A's Q6 framing as an open question (preserves the audit trail B does not). Add explicit recommendation block beneath it: "Recommendation: yes, `--skip-compliance` can override BLOCKED provided `--reason "..."` is supplied. Audit log entry on use. Citation: B's draft Q6 + R-12 mitigation."
- **Rationale:** debate X-001 (winner: B, confidence 78%). Reconciliation, not removal of A's question framing.
- **Risk level:** Low.

### Change #8 — Add status-pill column to §5 overlap matrix

- **Source:** Draft B status legend (✅ adopted / ⚠ partial / ❌ missing / 🛑 blocked)
- **Target location:** A's §5 overlap matrix (47 rows)
- **Integration:** Add a "Status pill" column to the 47-row matrix using B's vocabulary. Map A's labels:
  - MERGED → ✅
  - PARTIAL → ⚠
  - NOT-YET → ❌
  - For sprint-blocked items (e.g., O42 TurnLedger persistence out of scope) → 🛑
- **Rationale:** debate C-011 (winner: B, confidence 82%). Pill vocabulary is a navigation aid.
- **Risk level:** Low. Pure addition.

### Change #9 — Add "Rejected candidates (for transparency)" subsection under §6

- **Source:** Draft B B8, B9, B19, B20 (REJECT verdicts)
- **Target location:** New §6.4 (after §6.3 ranking)
- **Integration:** New table with columns ID, Candidate, Why rejected. Rows:
  - **Reintroduce `/sc:task-unified` as live command** (B8) — Regresses v3.7 canonicalization (§9.1 BLOCKING). Linked to NG-1.
  - **Replace keyword classifier with NLP** (B9) — Out of scope; longstanding limitation (R6 L99); not a merge concern. Linked to NG-3 partial.
  - **Adopt LW bash orchestrator / multi-backup strategy** (B19) — Explicit anti-pattern (R1 L64, L88). Linked to NG-4.
  - **Adopt LW Python-from-bash subprocess pattern** (B20) — Explicit anti-pattern (R1 L88). Linked to NG-4.
- **Rationale:** debate C-003 (winner: B, confidence 80%). Forces reviewer to acknowledge rejected ideas.
- **Risk level:** Low. Pure addition.

### Change #10 — Add Q8 release-split commitment to §9.3

- **Source:** Draft B §8 Q8 explicit recommendation "(b) split — natural seam"
- **Target location:** A's §9.3 (R1/R2 split semantics)
- **Integration:** A currently has the release-split as `[inference]`. Update to: "`[inference]` Recommendation per B's Q8 (Blocking? Y): apply release-split protocol to this v3.75 release. Task-side TU-001..TU-007 ships in one release; sprint-side SE-001..SE-006 ships as sibling release. Natural seam: `/sc:task` surface vs `cli/sprint/`. Different reviewers, different blast radius. Reference: `sc-release-split-protocol`."
- **Rationale:** debate U-012 (winner: B, confidence 85%). A flags inference; B commits.
- **Risk level:** Low.

### Change #11 — Add TL;DR opener to §1

- **Source:** Draft B §1 TL;DR sentence
- **Target location:** Top of A's §1 (before §1.1)
- **Integration:** New paragraph: "**TL;DR.** Merge the historically-distinctive strengths of `/sc:task-unified` into canonical `/sc:task` without regressing the v3.7 canonicalization (which already removed `/sc:task-unified` as a live command). Merge surface: tier classification rigor + sprint-executor adoptables (consumer of `/sc:task`). 7 task-side ADOPTs (TU-001..TU-004, TU-007) + 5 sprint-side ADOPTs (SE-001..SE-005); 3 DEFERs (TU-005, TU-006, SE-006). Release-split recommended: tier-rigor and sprint-side ship as sibling releases per `sc-release-split-protocol`."
- **Rationale:** debate C-001 (Tie/Merge). Scan-time entry point.
- **Risk level:** Low.

### Change #12 — Add new §10 "Shared assumptions surfaced during adversarial review"

- **Source:** diff-analysis.md A-001..A-005 promoted synthetic diff points
- **Target location:** New §10 after §9
- **Integration:** New section enumerating the 5 promoted assumptions with classification and impact. Both source drafts implicit; the adversarial pass surfaced them.
- **Rationale:** AD-2 requirement (UNSTATED preconditions surfaced from agreement points). Documentation of synthesis-grade findings.
- **Risk level:** Low. New content.

### Change #13 — Add "Synthesis preamble" tag at top of merged document

- **Source:** Provenance system requirement
- **Target location:** Top of merged document, before §1
- **Integration:** HTML comment block: `<!-- Provenance: Synthesized by /sc:adversarial from Draft A (variant-1) + Draft B (variant-2). Base = A (completeness/traceability, qual_score 26/30, quant_score 0.935, Correctness 5/5). Overlay = B (decision instruments). Convergence: 86.8% over 38 diff points. Merge date: 2026-05-14. -->`
- **Rationale:** Provenance discipline per T05.04.
- **Risk level:** Low.

### Change #14 — Add TU-007 (Mandatory completion checklist) as a first-class candidate

- **Source:** Draft B B6 (Mandatory completion checklist — 6 conditions)
- **Target location:** A's §6.1 (after TU-006)
- **Integration:** New candidate block: TU-007 — Mandatory task completion checklist. Source: R2 L85; B's B6. Current state: O20 in A's matrix flags this PARTIAL ("TFEP exists; explicit 6-condition completion checklist not stated as such"). Proposed: explicit 6-condition checklist programmatically enforced. Risk per B: Low. Effort: S. Verdict: ADOPT. Coverage-notes Known gap "TFEP completion-checklist six conditions not enumerated verbatim" carries forward.
- **Rationale:** A absorbed this into TU-003; B explicitly elevates it. Debate convergence keeps both representations (A's coverage-notes flag + new TU-007 candidate row).
- **Risk level:** Low.

---

## Changes NOT Being Made

| Diff Point | B Approach Considered | Rationale for keeping A approach |
|------------|------------------------|-------------------------------------|
| Overlap matrix scale | B's 21-row C1-C21 instead of A's 47-row O1-O47 | Debate S-003: A wins (85% confidence). B's matrix is a proper subset; A's broader matrix is required for traceability. B's advocate explicitly conceded. |
| Compression to ~207 lines | Remove A's §4 subsections, collapse §9.x, drop coverage-notes | Debate C-008: A wins (95% confidence). Compression IS the source of B's hallucination risk (K1, K5 NOT MET). |
| Q1+Q2 collapse to single Q3 | Merge sentinel + caller-string questions | Debate C-007: A wins (70% confidence). B's advocate conceded splitting back. The `/sc:forensic` consumer-enumeration uncertainty must remain visible. |
| H1-H10 historical strengths table | Flatten A's §3.1-§3.4 into a single table | Debate covered S-006-adjacent. A's deeper citations are required for traceability. |
| Drop §9.5 v3.7 baselines | Remove baseline numbers (921 passed, 57 failed, etc.) | Debate U-004: A wins (90% confidence). Test baselines define what "regression" means; B's advocate conceded retention. |
| Drop §9.7 Wave-4 parser regression | Remove parser-regression note | Debate U-005: A wins (88% confidence). SE-003 prompt-template work could regress this. B's advocate conceded retention. |

---

## Risk Summary

| Change # | Risk | Impact | Rollback |
|----------|------|--------|----------|
| 1, 2, 5, 6 | Verdict/effort overlays may project unearned certainty if `[inference]` markers stripped during downstream consumption | Medium | Re-add `[inference]` markers; reference base-selection.md tiebreaker (Correctness 5/5 for A's discipline) |
| 3 | Owner-column assignments may misallocate responsibility if consumers treat them as authoritative | Medium | Owners are `[inference]`; document in §7 preamble that assignments are recommendations not assignments |
| 4 | Moving RK-13/14/18 to appendix could hide regression risk if appendix is overlooked | Low | Appendix is appended directly after main register; same document |
| 7 | Q6 recommendation block may be misread as a final decision | Low | Marked clearly as recommendation; A's question framing preserved |
| 8 | Status pills duplicate MERGED/PARTIAL/NOT-YET label | None — both columns present, pills are secondary navigation |
| 9 | "Rejected candidates" subsection could be confused with deferred work | Low | Section explicitly titled "Rejected candidates (for transparency)" |
| 10 | §9.3 update commits to release-split which is itself a recommendation | Low | Marked `[inference]` and tagged as recommendation per B's Q8 |
| 11 | TL;DR could become stale if downstream decisions diverge | Low | Single-paragraph; easy to update |
| 12 | New §10 introduces content not in either source draft | Low | This is the adversarial pipeline's intended output; both drafts' UNSTATED assumptions are surfaced |
| 13, 14 | Pure additions; no rollback needed | None |

---

## Review Status

- **Default mode (non-interactive):** Auto-approved
- **Approval timestamp:** 2026-05-14
- **Reviewer:** debate-orchestrator (sc-adversarial-protocol pipeline)
