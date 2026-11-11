---
topic: "Issue #346 theme LEDGER: replace repeated whole-document re-reviews with a finding ledger and separate find and verify phases (spec-panel first, then reflect, rf-qa, implement final review)"
domain: architecture
strategy: agile
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-11-08T14:30:00Z
---

# Seed Brief: 346-ledger

Unattended run: no person answered the Socratic questions. Answers below come from the coordinator brief, the experiment reports and the review files named in Known Context. Domain `architecture` (four review tools across components); strategy `agile` by the heuristic (the topic names an experiment).

## Socratic dialogue (standard: clarify + validate, answered from context)

1. What hurts? A review, fix, re-review loop over a document never reaches a clean PASS within 3 reviews; each round finds a fresh batch of defects that the last fix introduced or exposed.
2. Scope? First adopter `/sc:spec-panel` (as an additive variant command `spec-panel-ledger`); later adopters `/sc:reflect`, rf-qa agents, `/sc:implement` final review.
3. Constraint hierarchy? Mechanical enforcement over prose; build on the PR 427 `## Review Loop` text; testable on this machine without editing `~/.claude/commands/sc/spec-panel.md`; cost must be stated.
4. Who maintains it? This repo (IronClaude fork); source of truth `src/superclaude/`, synced to `.claude/` and installed to `~/.claude/`.
5. Migration tolerance? Additive: a new command file next to the old one; the original command stays unchanged until an experiment proves the variant.
6. Existing patterns? 427's `--re-review --baseline` (prior-findings table resolved/open/regressed plus changed-line findings with `origin=`); `/sc:implement` re-review (delta diff + per-prior-finding check, unchanged-text findings capped at note); rf-qa Fix Cycle steps 1-5; reviewers already write a Part 1 resolution table and revisers already write a disposition table (one row per finding, with "Where (revised spec)").
7. Data model impact? A new ledger file per loop, read and written by a script, carried across sessions.
8. Contract impact? The report's last line `verdict: PASS|FAIL` becomes computed from the ledger instead of written by the reviewer.
9. Operational impact? One extra script call per step; one extra final sweep session.
10. Rollback? Delete the variant command; the original stays.

## Problem Statement

PR 427 halves spec growth but does not make the loop converge: in the controlled S1 experiment no run of any arm reached PASS, and 89% (review 2) and 100% (review 3) of new findings sat on lines the previous fix changed. A fresh look at the document after each fix keeps finding fix-induced defects, severity labels drift upward between rounds, revisers add mechanisms and apply minor findings, and the verdict and the 3-review cap are reviewer judgement and prose, not computed. The ledger theme changes the loop so that only review 1 finds; later rounds only verify the ledger rows and stop by a computed count.

## Known Context

- Evidence: `exp346-p1-logs/.dev/experiments/346-validation/phase4/AB-REPORT.md`, `ARMB-REPORT.md`, `DECISIONS.md` (D5 metrics M1-M5, D10/D11 bars, D9 machine fact).
- Results (S1, n=2 per arm): R3 critical+major proxy control 8/4 (mean 6.0), 427 6/5 (5.5), 427+flags 6/1 (3.5); growth after 2 fix cycles control 63.5%, 427 29.7%, 427+flags 30.0%. Bar: R3 proxy <= 3, growth <= 44.4%, effect > within-arm spread, every replicate on the better side.
- Real reports (flg-r2): R3 resolved all 6 prior blocking findings, then found N12 (MAJOR, blocking, origin=changed) created by the N5 fix, which added a new "record the agent command" step. Reviser disposition-round2 applied all 15 rows including 9 minor ones and fixed "related defects found while applying" (E5, AC-1.2), widening scope. Coordinator briefs still say "any finding of any severity is FAIL".
- 427 contract: `src/superclaude/commands/spec-panel.md` `## Review Loop` (7 bullets, line 256); design `docs/designs/spec-panel-review-loop.md` states "every rule here is prose read by a model".
- Machine fact (D9): workers load `~/.claude/commands/sc/spec-panel.md`; personal beats project; a parallel arm needs a different command NAME.
- Reach: 427 touches 1 of 5 incident types; S2 `/sc:reflect`, S3 plain agent, S4 rf-qa/rf-analyst, S5 `/sc:implement` final review are outside it.

## Constraints

- Design only; no implementation, no commits.
- Mechanical enforcement preferred; every prose-only rule names its residual risk.
- Builds on the 427 text; delivered as additive variant `spec-panel-ledger`.
- Keep the canonical cap text `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings` (pinned by `tests/skills/test_review_severity_rule.py`).
- Installed primitives use installed paths, never `src/superclaude/` paths.
- Measurement on S1 with the same briefs and metrics; one-line name substitution in the briefs.

## Success Criteria

- A ledger file format a script can parse, with its location and the status transitions each actor may make.
- A computed termination rule over ledger rows that yields PASS, FAIL-continue or ESCALATE.
- A clear statement of what differs from 427 `--re-review`.
- An adoption path for reflect, rf-qa and implement final review.
- A recommendation between a stateful reviewer session and a file ledger.
- Predicted S1 numbers for R3 critical+major and growth, and a falsification result.

## Open Questions

- Who may set `verified` and `reopened`: only the verifier, or a script from the verifier's per-row answer?
- Is the "new defect on changed lines" check allowed to add blocking rows, and how many before it stops the loop?
- Does the final whole-document sweep count as review 3 of 3, or as a fourth pass outside the cap?
- How is severity frozen at review 1 so labels cannot drift upward?
- How does the script tell which lines a row's fix changed (anchor quote vs diff hunk)?
- How does the metric "R3 critical+major" map onto a ledger loop whose round 3 is a verify pass plus a sweep?

## Enrichment Context

Full artifact: `enrichment/codebase-context.md` (quality_tier `fallback_1`: native Grep/Read; auggie not in this session; research skipped by `--no-research`).

- Prior art for a computed verdict: `/sc:implement` reviewers return per-AC marks "and no verdict; the orchestrator computes it" (`sc-implement-protocol/refs/qa.md:97,334`); finding lines carry `anchor=`, `at=`, and parent-written `sev=`, `origin=` (`:135-144`); inherited text is capped at note "mechanically from the `git diff` hunk headers" (`:166`). Implement still lets each re-review raise new blockers anywhere in changed text (`:186`).
- rf-qa Fix Cycle re-checks only prior blocking issues and has a prose monotonicity halt `|F_{n+1}| < |F_n|` (`agents/rf-qa.md:379-416`).
- Scripts ship inside skill folders and run as `uv run --no-project python "<skill base>/scripts/<name>.py"` (`sc-implement-protocol/refs/managed-workspace.md:54`); install copies the whole skill folder (`cli/install_skill.py:52`). A command file alone cannot carry a script, so the ledger script needs a skill folder (for example `review-ledger`).
- Observed (flg-r2): the round-3 reviewer already writes a per-finding resolution table and computes changed lines with `git diff --no-index -w -U0`; the reviser already writes one disposition row per finding and tags edits with finding ids, but applies minor findings and fixes "related defects found while applying". The new blocking N12 came from a fix that added a new step. Briefs still say "any finding of any severity is FAIL".
