# Round 2 — Rebuttal advocate for variant-C (BLIND, truth-seeking)

## 0. Posture

Round 1 settled the framing in C's favor: X-007 (refactor not built; A's 8/8 and
B's 7/7 replays fabricated), X-005 (#158 phantom; A correct, C safely silent), and
X-006 (deliverable is a gate-approval container embedding an efficacy audit). I do
not relitigate those. Round 2's job is the opposite of a victory lap: graft A/B's
genuine assets into C's container honestly, freeze the canonical numbers, and carry
the one still-live source divergence (M6) forward correctly. Where C was thin, A and B
were right, and I say so explicitly below.

---

## 1. Concession repair — grafting S-004 / S-005 into C's container

C legitimately lacked a per-stage theatre scorecard (S-004) and a would-have-caught
matrix (S-005). These are the analytical heart of an efficacy audit and the merged
report needs them. They graft into C's container as a **new "Predicted coverage"
subsection of the embedded efficacy audit**, under two hard constraints:

1. **Reframed as prediction, not fact.** A's/B's matrices were written as
   *retrospective replay results* ("round 2, 100%"). Since X-007 establishes the
   refactor is unbuilt, every would-have-caught cell must be relabeled
   **"predicted/pre-build coverage — to be backtested post-G1"** and carry a
   `NOT YET PROVEN` status token (C's existing blocker semantic, SKILL output
   contract). No cell may assert a run that did not happen.

2. **Grounded denominator.** The per-stage scorecard must use the **frozen E1–E5
   denominator** and the stage rows from `theatre-vs-value-scorecard.md` (the only
   source-traceable figures), NOT A's invented 2/4/3/4/3 or B's 6/6/7/7/7.

**Concrete graft.** Adopt the scorecard table verbatim from
`theatre-vs-value-scorecard.md` lines 13–16 (per-stage value/theatre split:
`sc:troubleshoot` 52/48, `task-builder` 35/65, `sc:reflect` 40/60, QA gates 35/65),
and add a 5-row would-have-caught matrix keyed E1–E5, each cell mapping to the
H0–H5 wave/control predicted to close it (E1→H1 runtime-entrypoint;
E2/E3→H3 unmask-and-sweep + whole-artifact classifier; E4→H2 contract ledger;
E5→H4 effective-input proof). The matrix is a **design-time prediction grid**, not a
replay log. This gives the merge A/B's structure and C's honesty simultaneously.

---

## 2. X-001 — lone-catch attribution (single best evidence-grounded answer)

R1 had three answers: A's human-PR-tail, B's inside-#154 adversarial surface, C's
sc:reflect=E5. **The most evidence-grounded single attribution is sc:reflect catching
E5/REFLECT-E01 (the wrong-diff/base trap).**

Evidence, three independent sources:
- `theatre-vs-value-scorecard.md:15`: "`sc:reflect` … **Caught E5/REFLECT-E01
  wrong-diff trap**."
- `theatre-vs-value-scorecard.md:24`: "Reflect had a distinct high-value niche.
  `sc:reflect` caught the wrong-diff/base-selection trap in E5."
- `defect-escape-table.md:11` REFLECT-E01: "**Hit live while auditing #151**" → fixed
  PR #153 `10723863`.

A's external-human-tail and B's adversarial-during-#154 are both about F-A (the
completion-substring fix, escape-table PRD-E05, landed *inside* #154 `e97aa4fd`) —
a different escape, and the evidence names no external reviewer ID. The cleanly
attributable catch with a named surface and a named escape is **reflect→E5**. The
merge should credit reflect with E5, mark F-A/E2 as "fixed inside #154, catcher
surface unproven," and not assert A's unsourced external-reviewer record.

---

## 3. X-002 / X-003 — canonical set, denominator, theatre figure

**X-003 (cardinality).** Confirmed: the canonical operative set is **E1–E5 (5
families)**, frozen by `GATE-0.md:20` and backed by exactly five on-disk
`escape-E1..E5/` directories. A's 8 and B's 7 are **finer-grained instances**, not a
competing top-level count. The reconciliation: the broader forensic
`defect-escape-table.md` actually enumerates **9 rows** (PRD-E01..E06 + REFLECT-E01..E03);
GATE-0 deliberately collapsed those 9 into the 5 operative canonical families. So A's
"8" and B's "7" are each partial re-slicings of the 9-row forensic table — neither
matches the canonical freeze. **Merged scorecard denominator = 5 (E1–E5).** A's/B's
M-items appear as *instances mapped under the E-family*, with the 9-row table cited as
the forensic appendix.

**X-002 (theatre figure).** The only evidence-grounded figure is **41% value / 59%
theatre**, source-confirmed verbatim at `theatre-vs-value-scorecard.md:5`
("Estimated net defect-catching value: **41% value / 59% theatre or mis-targeted
ceremony**") and restated at `:56`. A's 6.25%/0.94 and B's 3.0%/0.97 are
self-constructed over invented obligation counts and must be demoted to "illustrative
re-derivation, denominator unverified." **Merged headline = 41/59 from line 5.**

---

## 4. A-002 — should-have-caught as a fair denominator: QUALIFY (softened from REJECT)

R1 I REJECTed A-002 outright. I **soften to QUALIFY**. The *frame* "should-have-caught"
is legitimate and useful — it is how you reason about a preventive gate's miss rate.
What I reject is binding the ratio to A's or B's **invented per-stage counts**. So:
accept the frame, reject the fabricated denominators, bind every ratio to the
`theatre-vs-value-scorecard.md` per-stage value/theatre splits and the frozen E1–E5
set. QUALIFY, not REJECT: keep the concept, ground the arithmetic.

---

## 5. M6 — RE-VERIFIED with fresh reads (carry forward as LIVE)

R1 cited "executor.py:259 emits `research-qa` vs config.py:30 `qa-research-gate`." I
re-read source on 2026-06-10. **The divergence is real and live, but R1's file
attribution was ambiguous/stale and is corrected here:**

- The tokens are **not** in the sprint module (`cli/sprint/executor.py:259` is a
  `to_yaml` docstring; grep of `cli/sprint/` for these tokens = empty).
- They live in the **PRD** module:
  - `src/superclaude/cli/prd/executor.py:259` → `"research-qa": "qa/qa-research-gate-report.md",`
  - `src/superclaude/cli/prd/config.py:30` → `r"|analyst-completeness|qa-research-gate"`
  - (also `prd/gates.py:476` keys `"research-qa"`; `prd/executor.py:878,916,922,1157`.)
- **State correction:** the divergence is **committed**, last touched PR #149
  `f131592f` (`git diff HEAD` on both files = empty). R1's "UNCOMMITTED — not in git
  at all" (A) is **wrong**; B's "no committed fix found in supplied evidence" is the
  closer phrasing. The producer emits step-id `research-qa`; the resume `_STEP_ID_PATTERN`
  validates `qa-research-gate` — a genuine producer/validator identifier mismatch,
  live and committed.

**Carry-forward:** M6 enters the merged report as a **live (not closed)** instance
under the E4-family contract-identity mechanism, citing
`prd/executor.py:259` / `prd/config.py:30`, committed via #149. It is an additional
exemplar of "human-readable taxonomy substituted for executable API identity," not a
resolved item.

---

## 6. Merge reconciliation — what variant-C contributes as the spine

C is the structural base; A and B supply contents that hang on C's frame. C's spine:

1. **Honest G1 status.** "G1-ready, implementation pending approval" — the only
   framing consistent with git (troubleshoot files unchanged since #116 `022bccee`;
   `refs/` hardening files absent). This is the report's outer container.
2. **Frozen E1–E5 canonical set** as the single denominator (GATE-0 + 5 on-disk
   dirs), with A's/B's M-items and the 9-row escape table as mapped instances/appendix.
3. **Halt-pending-approval posture.** Explicit G1 halt note, no `.claude/` mirror
   edits, `make sync-dev`/`verify-sync` routing, paste-ready approval prompt — the
   process-discipline backbone A/B both violated by claiming edits already shipped.
4. **Remediation/hardening spec linkage.** The 7 reusable closure controls + H0–H5
   wave/gate spec with machine-checkable output statuses and `NOT PROVEN` blocker
   semantics — the implementable target the embedded efficacy audit justifies.

A's patch-relative-vs-baseline-relative distinction (U-001) and negative-witness
discipline (U-002) graft in as **design rationale for the H1/H3 waves and the post-G1
backtest plan** — preserved as predicted, never asserted. B's Executable Contract
Identity Ledger (4.4) graft in as the concrete mechanism for H2 and for the M6/E4
contract-identity instance. C's container + A's analytical depth + B's contract
mechanism = the complete merged report.

---

## 7. Per-contradiction final stance (Round 2)

- **X-001:** sc:reflect→E5/REFLECT-E01 (scorecard:15,24; table:11). C-correct.
- **X-002:** 41/59 (scorecard:5). C-correct; A/B figures illustrative only.
- **X-003:** canonical 5 (E1–E5; GATE-0:20 + 5 dirs); A/B M-items are instances;
  9-row table = forensic appendix. C-correct.
- **X-004:** keep F-B out of the denominator (B's discipline); F-A is an E2/E3-family
  instance fixed inside #154. QUALIFY.
- **X-005:** #158 phantom; real fix `b97c9960` (unmerged author commit). A-correct;
  use A's exact framing.
- **X-006:** gate-approval container embedding the efficacy audit. C-correct.
- **X-007:** refactor unbuilt; A's 8/8 + B's 7/7 fabricated. C-correct, decisive.
- **X-008:** no coverage claim pre-G1; A's irreducibility analysis becomes the
  predicted post-G1 backtest plan. C-correct.

- **A-002:** QUALIFY (softened from REJECT) — keep the frame, ground the arithmetic.
