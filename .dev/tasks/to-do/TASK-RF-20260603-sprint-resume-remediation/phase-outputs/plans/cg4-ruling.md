RULING: YES

Operator ruling recorded by Ryan W (2026-06-02) in
`.dev/brainstorms/20260602-sprint-auto-resume-default/cg4-decision-record.md`:
**"YES + F-2-as-prerequisite"** — design §7 governs the non-interactive path; F-1 is as-designed
(no gate tightening), with the F-2 partial-path surfacing as the hard prerequisite.

Source: operator-recorded (genuine human ruling, NOT an auto-applied default).

Rationale & spec-edit consequences (YES branch):
- F-1 = closed as-designed (Necessary deviation, REPORT.md:35). No `_verdict`/gate change; no
  `--accept-partial` flag. `integrity.py:_verdict` stays `accept_suspect or validated_last`.
- F-2 = MANDATORY and is the informedness prerequisite — already LANDED in Phase 3 (the
  `BoundaryReport.partial_paths` field + printer surface), so `--yes` is now informed pre-consent.
- Spec amendments applied (Step 1.5, YES branch):
  - `design.md` §4(c) — partial conjunct re-worded to
    `(partial reported AND (quarantined OR --yes/assented))`, reconciling §4(c) with §7:293.
  - `merged-requirements.md` FR-2.4 — clarified that on the non-interactive path,
    "`--yes` + a printed partial-paths report" constitutes "explicitly assessed-and-accepted".
  - `design.md` §7 and `integrity.py:_verdict` — UNCHANGED (already encode §7).

Consequence for promotion: strict-gate condition 8 (needs_human_decision==false) is now CLEARED.
Condition 4 (drift==0, regression==0) is addressable (F-3/F-2 fixed). Promotion may be re-run.
