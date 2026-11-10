---
topic: "Theme ponytail for IronClaude issue 346: severity-and-necessity audit of applied fixes with ponytail:ponytail-review, added to the /sc:spec-panel Review Loop as additive variant spec-panel-ponytail (full topic text in return-contract.yaml command field)"
domain: code
strategy: agile
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-11-08T14:40:00Z
---

# Seed Brief: 346-ponytail

## Socratic dialogue (unattended: answered from the brief and the on-disk evidence)

Clarify batch
1. Entry point? The `## Review Loop` section of `/sc:spec-panel` (PR 427, `src/superclaude/commands/spec-panel.md:256-264`), delivered as a new variant command `spec-panel-ponytail`.
2. Scope? One new command file (copy of spec-panel plus one section), one helper script, tests, one design note. No change to the original command.
3. Failure prevented? A review loop that never reaches PASS because each fix adds text that the next whole-or-changed-line review attacks.
4. Hard constraints? 427 text stays byte-identical inside the copy; canonical cap text and S1-S5 pins (`tests/skills/test_review_severity_rule.py`); `/sc:spec-panel` never modifies a spec without consent (C6); `~/.claude/commands/sc/spec-panel.md` is not edited by experiments.
5. Done? A spec that a later `/sc:workflow` can plan from, plus a pre-registered S1 measurement.

Validate batch
6. Existing patterns? `/sc:implement` QA (delta diff, resolved/open/regressed, inherited text capped at a note), rf-qa Fix Cycle, `ponytail:ponytail-review` (lists findings, changes no code, ends `Verdict:` and `Lean: -N lines possible.`).
7. Consumers? Orca coordinators and people running review, fix, re-review by hand.
8. Test surface? Text-presence tests for the command, unit tests for the script, one live S1 run (2 replicates).
9. Forcing function? Issue 346 stays open; 427 did not converge (AB-REPORT, ARMB-REPORT).
10. Rollback? Delete the variant file; nothing else changes.

## Problem Statement
After PR 427, the spec-panel loop still ends review 3 with 5-6 open critical+major findings (control 6.0) and no clean PASS; 89-100% of new findings sit on lines the last fix changed. Revisers also apply minor findings (one run applied 15 of 15 rows, 9 minor) and grow the spec by about 30%. The owner wants one non-repeating audit that checks, per applied fix, whether the finding was truly blocking and whether the added text is needed, and then shrinks or reverts the rest.

## Known Context
- Evidence: `exp346-p1-logs/.dev/experiments/346-validation/phase4/AB-REPORT.md`, `ARMB-REPORT.md`, `DECISIONS.md` (D9: workers load the user-level command; additive names are needed).
- Real loop artifacts: `exp346-ab-flg-r2/.dev/orca-command-refactor/review/` (disposition tables carry finding id, blocking yes/no, disposition, where).
- `ponytail:ponytail-review` is a plugin skill at `~/.claude/plugins/cache/ironclaude/ponytail/5.3.3/skills/ponytail-review/SKILL.md`; it is written for code changes and returns grouped prose, not a table.
- Review 3 in flg-r2: 6 prior blocking resolved, 1 new blocking (N12) introduced by the N5 fix.

## Constraints
- Additive variant `spec-panel-ponytail`; original command untouched.
- Mechanical over prose where possible (a file the loop writes and a script checks).
- The audit runs once and is never re-reviewed.
- Keep the 3-review cap; no fourth review.
- No commits, pushes, or edits outside this worktree.

## Success Criteria
- S1 review-3 open critical+major mean at most 3 (control 6.0), and growth after two fix cycles at most 44.4% (control 63.5%), both replicates on the better side of both controls.
- A falsification result is stated before any run.
- Exact file list and the one-line brief substitution are given.

## Open Questions
- Placement: end of fix cycle 2 (owner), after every fix cycle, or triage before the first fix?
- Who applies reverts: the auditor, a reviser, or a script from a patch?
- Does a revert reopen the finding, and how does the verdict use the audit table?
- Can the ponytail skill be called from inside a command run, and is a wrapper brief needed to get a table out of it?
- Does an audit after review 3's input change what review 3 sees (ordering of audit vs review 3)?

## Enrichment Context
Full artifact: `enrichment/codebase-context.md` (codebase, quality_tier primary; research skipped by `--no-research`).
- `ponytail:ponytail-review` lists findings in prose groups (Must fix / Should fix / Nice to have), ends `Verdict:` and `Lean: -N lines possible.`, and changes no code; it has no table and no severity column, so the audit brief must ask for a table on top of it, and a script, not the skill, must apply reverts.
- Ponytail is a pinned third-party plugin installed by the IronClaude installer; a host without it has no such skill, so the variant needs a stated fallback.
- `/sc:implement` QA (`refs/qa.md:91`) forbids a ponytail judgment from changing severity or verdict and never invokes the plugin; adoption there would reverse a written rule.
- spec-panel never modifies a spec without consent: apply must sit outside the reviewer (coordinator or script).
- Installed commands reach scripts only through a skill folder (`~/.claude/skills/<name>/scripts/`), run with `uv run --no-project python`.
- Prior art for a safe apply: `.dev/review-severity-rule/implement-tools/apply_rows.py` (old/new rows, exact-occurrence check, `STOP, nothing written`).
- Real disposition tables already carry finding id, blocking yes/no, disposition and the inline finding id at every edit, so a per-fix audit can key on the finding id.
