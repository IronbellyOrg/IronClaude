---
topic: "THEME minfix (issue #346): fix-minimality mechanism on the reviser side of the /sc:spec-panel review -> fix -> re-review loop, built on PR 427; mechanical per-finding fix budget checker; additive variant command spec-panel-minfix; measurement on scenario S1"
domain: architecture
strategy: agile
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-11-08T14:40:00Z
---

# Seed Brief: 346-minfix

## Problem Statement
A `/sc:spec-panel` review -> fix -> re-review loop on a document does not reach a clean PASS within the 3-review cap. PR 427 halves spec growth (control +63.5%, 427 +29.7% after two fix cycles on scenario S1) but leaves review-3 open critical+major at 5-6 (bar: 3 or fewer). 89-100% of new findings sit on text the previous fix changed (`origin=changed`): each fix adds text (fields, tables, sections, normative rules) that the next review attacks. 427's Reviser contract is prose and only bans additions "no blocking finding calls for", so blocking findings still get answered with new mechanisms, and its own design (`docs/designs/spec-panel-review-loop.md` section 5 notes) rejected a size limit because "nothing could check it from text". This brainstorm designs the missing piece: a per-finding fix budget enforced by a script.

## Known Context
Dialogue (unattended; answered from the experiment reports, the 427 design doc and the S1 spec history):
- Q1 What hurts: fix-induced findings, not unresolved ones. No finding repeats across rounds (issue #346, "Ruled out").
- Q2 Scope: the reviser step of one command's loop (`/sc:spec-panel`), delivered as an additive variant `spec-panel-minfix`; later adopters `/sc:reflect`, rf-qa, `/sc:implement` final review.
- Q3 Constraint order: convergence > mechanical checkability > cost > wording elegance.
- Q4 Maintainers: this fork; the coordinator (Orca worker or human) runs the loop and keeps the review count, prior report and saved copy (427 Review Loop bullet 4).
- Q5 Migration: parallel run (variant command name), no edit to `~/.claude/commands/sc/spec-panel.md` (D9: workers load the user-level file).
- Q6 Existing patterns: 427 `--re-review/--baseline` (saved copy, not a git ref); `/sc:implement` QA "may not widen the AC"; package CLI `superclaude <group>` (click) under `src/superclaude/cli/`.
- Q7 Data: per-finding ledger file the reviser writes; checker report file; the baseline copy already exists.
- Q8 Contract impact: report gains per-finding budget class; reviser brief gains ledger rule; next re-review reads the checker report.
- Q9 Ops: one extra Bash call per fix cycle (checker), at most one bounded cut-down retry.
- Q10 Rollback: the variant is a separate file; delete it.

Measured reviser additions per fix cycle (bytes, line diff of paragraph-lines, new headings, net normative words MUST/SHALL/must/never/always):
| run | cycle 1 | cycle 2 |
|---|---|---|
| ctl-r1 | 57,763->71,528, +58/-36 lines, +0 h, +4 norm | ->91,102, +88/-32, +1 h, +8 norm |
| ctl-r2 | ->76,214, +95/-55, +0 h, +10 norm | ->97,814, +71/-34, +1 h, +21 norm |
| trt-r1 | ->64,488, +43/-30, +4 h, +4 norm | ->71,113, +25/-23, +0 h, +7 norm |
| trt-r2 | ->71,244, +112/-41, +7 h, +11 norm | ->78,715, +49/-45, +3 h, +2 norm |
| flg-r1 | ->67,886, +41/-33, +0 h, +6 norm | ->73,807, +60/-60, +0 h, +3 norm |
| flg-r2 | ->70,255, +68/-37, +1 h, +7 norm | ->76,328, +25/-24, +0 h, +2 norm |
Lines are whole paragraphs, so a line diff hides size; count words per sentence. flg-r2 disposition (review 1): blocking F1 answered with a new `worker_status` field plus mapping, F2 with a new section 2.4 table, F4 with a fallback directory rule; non-blocking findings "that correct an existing wrong statement" were also applied.

## Constraints
- Build on 427's `## Review Loop` (spec-panel.md line 256); keep its 7 bullets, cap text and test pins (`tests/skills/test_spec_panel_review_loop.py`, `tests/skills/test_review_severity_rule.py`).
- Mechanical enforcement first; every prose-only rule is named with its residual risk.
- Additive variant `spec-panel-minfix` installable beside `~/.claude/commands/sc/spec-panel.md`; experiments never edit the user-level original.
- Installed primitives never cite `src/superclaude/` paths; reach package code through the `superclaude` CLI.
- UV only for Python; no new dependency.
- The checker must not silently block a genuinely necessary larger fix: an explicit, logged override with a reason.
- A finding that cannot be fixed within budget is escalated, never expanded.
- 3-review cap unchanged.

## Success Criteria
- On S1 (same briefs with the one-line name substitution, 2 replicates), review-3 open critical+major mean 3 or fewer (control 6.0) and growth after two fix cycles 44.4% or less (control 63.5%), every replicate on the better side of every control.
- The checker report shows every changed sentence attributed to a finding id, and zero unapproved over-budget fixes reach a review.
- Share of `origin=changed` findings stays measurable (the variant keeps 427's tags).
- A stated falsification result: what numbers mean the idea failed.

## Open Questions
- Budget numbers: fixed words per class (e.g. minor 0 edits, blocking 60 added words) vs relative to the cited span; what are the right first values given the measured cycles?
- Where the checker lives: `superclaude review fixcheck` CLI subcommand, a standalone `uv run` script, or a fixed Bash/diff sequence inside the command text?
- Attribution unit: sentence-level diff with a ledger quoting the exact old sentence, or anchored edit blocks the checker applies itself?
- What happens to over-budget fixes: auto-revert to baseline sentence, one cut-down retry by the reviser, or escalation?
- Override: who may grant it (reviewer report marks a finding `budget: large`, the coordinator, or the reviser with a reason) and how to stop it becoming the default path?
- Does the next re-review read the ledger (to aim at changed sentences) or stay blind to it?
- Does minimality alone lower review-3 blocking, or does it only cut growth again (427 already did)? Which measured causes stay (severity drift, whole-document attack on changed text)?

## Enrichment Context
Full artifact: `enrichment/codebase-context.md` (quality_tier fallback_1: Grep/Glob/Read; Auggie unavailable).
- Checker home with precedent: a stdlib script bundled in a skill and run as `uv run --no-project python "<skill base>/scripts/<name>.py"` (pattern in `sc-issue-protocol/SKILL.md:72`). Works in any project and in the S1 experiment worktrees (repo base 2cb683f5 has no new package code); installs additively as a new folder under `~/.claude/skills/`. A `superclaude` CLI subcommand would need a package reinstall, so it cannot be tested additively.
- `difflib` (stdlib) is enough for a sentence-level diff; no new dependency.
- `superclaude install` copies each `commands/*.md`; a new `spec-panel-minfix.md` installs as `/sc:spec-panel-minfix` without touching `spec-panel.md`.
- 427's design rejected a size limit only because "nothing could check it from text" (`docs/designs/spec-panel-review-loop.md:73`); a script removes that objection. FR-8/FR-9 gap-filling (`spec-panel.md:328-329`) is the main legitimate source of larger fixes and needs the override path.
- Later adopters: `/sc:reflect`, rf-qa Fix Cycle (`agents/rf-qa.md:379-416`), `/sc:implement` QA; a (baseline, revised, ledger) checker is document-agnostic.
