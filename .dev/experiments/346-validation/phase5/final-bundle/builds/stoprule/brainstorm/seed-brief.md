---
topic: "Issue #346 theme 'stoprule': severity discipline and a mechanical stop rule for the /sc:spec-panel review, fix, re-review loop"
domain: code
strategy: enterprise
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-11-08T14:15:46Z
---

# Seed Brief: 346-stoprule

## Problem Statement
A `/sc:spec-panel` review, fix, re-review loop over a planning spec never reaches a clean PASS within its 3-review cap. PR 427 (the `## Review Loop` section) halves spec growth but leaves 5-6 open critical+major findings at review 3. Severity labels drift upward between rounds, the PASS/FAIL verdict is the reviewer's own judgement, and the cap is prose, so nothing mechanical bounds what counts as blocking or forces the loop to end on a defined outcome. This brainstorm designs a frozen rubric, an evidence rule for blocking findings, an independent second grader, a ratchet that demotes late-found findings, a script-computed verdict and a defined cap-hit escalation.

## Known Context
Dialogue run unattended (Clarify + Validate batches, `code` domain), answered from the experiment record:
- Entry point: `src/superclaude/commands/spec-panel.md` `## Review Loop` (7 single-line bullets, line 256); design `docs/designs/spec-panel-review-loop.md`.
- Measured (S1, n=2 per arm; `exp346-p1-logs/.dev/experiments/346-validation/phase4/AB-REPORT.md`, `ARMB-REPORT.md`): R3 critical+major proxy control 8/4 (mean 6.0), 427 6/5, 427+flags 6/1 (mean 3.5); growth after 2 cycles 63.5% / 29.7% / 30.0%; no run reached PASS.
- 89% (R2) and 100% (R3) of new findings in 427 runs carry `origin=changed`.
- Observed in reports: control R3 graded every Boundary-Table GAP MAJOR (FR-8) and resolved two expert disagreements to MAJOR; R3-8 was "present in the round-2 input, not flagged then" and still blocking; Arm B revisers applied all 15 findings including 9 minor ("the brief says to apply confirmed findings"); flg-r2 R3 had one blocking finding (N12) on a line the N5 fix wrote.
- 427 bullet 2 already says a MAJOR is blocking only if it names a concrete wrong outcome; Arm B shows the reviewer applies it (flg-r1 relabelled R3-7/R3-8 minor) but inconsistently.
- Workers load commands from `~/.claude/commands/sc/` (personal beats project), so a test variant needs its own command name.
- Prior art to reuse: `confidence-calibrator` agent (re-grades with formation context stripped), `evidence-validator` agent (re-reads citations), rf-qa Fix Cycle, `sc-implement-protocol/refs/qa.md` severity model.

## Constraints
- Additive variant command `spec-panel-stoprule`; never edit `~/.claude/commands/sc/spec-panel.md`; builds on the 427 text.
- Prefer mechanical enforcement (script, file the loop writes and reads, computed check); name residual prose risk.
- 3-review cap text must stay canonical (`at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings`); no `src/superclaude/` paths in installed primitives; UV for Python.
- Must be measurable on S1 with the same briefs plus a one-line name substitution.
- Cost must be stated: extra agent calls, sessions, wall time.

## Success Criteria
- On S1, review-3 open critical+major (after confirmation) <= 3 in both replicates (control mean 6.0), or a clean PASS before review 3.
- Growth after two fix cycles <= 44.4% (control 63.5%).
- The verdict line is reproducible by a script from the finding file alone.
- A sampled audit shows the second grader demotes no more than a stated share of real defects.

## Open Questions
- Where does confirmation live: a second agent call inside the command, a separate step the coordinator runs, or a script plus agent?
- Is the second grader independent enough with the same model family, or must it use a different model class?
- Does demoting late-found findings hide real defects the first review missed, and how is that bounded?
- Does a computed PASS simply move the problem (the reviewer stops writing blocking findings, or writes them without quotes)?
- What exactly is escalated at the cap, and in what format?
- Should the reviser read only confirmed blocking findings (to cut growth further)?

## Enrichment Context
Codebase scan (fallback_1: codegraph + Grep/Read; auggie unavailable). Full notes: `enrichment/codebase-context.md`. Research: skipped (`--no-research`).
- `/sc:implement` already derives severity from four yes/no checklist answers with a parent file Read-back, never reads the reviewer's label, and has the parent compute the verdict (`src/superclaude/skills/sc-implement-protocol/refs/qa.md:37-97`). It deliberately has no second model pass, and its `late` blockers still block (`qa.md:167`). Stoprule borrows the derivation and computed verdict, and departs on both points (second grader; late demotion).
- Independent re-graders exist: `confidence-calibrator` (context stripped, rubric applied mechanically) and `evidence-validator` (citation re-read), both `model: sonnet`.
- FR-8/FR-9 (`spec-panel.md:328-329`) force GAP and blank-behaviour rows to MAJOR minimum: a mechanical upward severity floor the stoprule rubric must override inside the variant.
- Skill scripts run as `uv run --no-project python "<skill base>/scripts/x.py"`; a command needs a companion skill folder to carry a script.
- Revisers applied minor findings when the brief said "apply confirmed findings" (Arm B disposition round 2: 15 of 15, 9 minor).
