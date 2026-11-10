---
topic: "THEME diffgate (issue #346): mechanical delta scope for /sc:spec-panel re-reviews, building on PR 427's ## Review Loop section. Re-review surface is COMPUTED (unified diff of saved baseline vs current document plus prior blocking findings with ids); reviewer gets only that surface plus read-only context; every new finding must cite a changed hunk or a prior finding id, else it is recorded 'deferred: pre-existing' and can never be blocking after review 1. Ships as additive variant command spec-panel-diffgate."
domain: code
strategy: agile
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-11-08T14:16:30Z
---

# Seed Brief: 346-diffgate

## Socratic dialogue (unattended: answered from on-disk evidence, no person available)

Clarify batch (domain `code`):

1. Entry point? `src/superclaude/commands/spec-panel.md`, section `## Review Loop` (line 256, 7 single-line bullets from PR 427) and its Usage line (line 22, `--re-review <prior-findings-file> --baseline <saved-copy>`). The new behaviour ships as a copy: `src/superclaude/commands/spec-panel-diffgate.md`.
2. Scope? One new command file (variant), one new helper script, one new test file, docs. The original `/sc:spec-panel` is not edited.
3. Failure mode to prevent? A review, fix, re-review loop over a document that never reaches PASS within 3 reviews because each fresh review finds defects the last fix introduced or exposed (measured: 89% of review-2 and 100% of review-3 new findings sit on lines the previous fix changed, `origin=changed`).
4. Non-negotiable constraints? Keep 427's literals and pinned cap text (`at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings`); installed primitives never name `src/superclaude/` paths; the command never edits the spec without consent; the user-level `~/.claude/commands/sc/spec-panel.md` is never edited by an experiment.
5. Done? A written spec (SPEC.md) for spec-panel-diffgate with a script outline, a checker, a measurement plan on scenario S1 with predicted numbers, and a falsification condition.

Validate batch:

6. Existing implementations to align with? 427's `--re-review/--baseline` (prose; the Arm B reviewer computed its own `git diff --no-index -w` and self-tagged `origin`); `/sc:implement` QA re-reviews get a delta diff and a per-finding resolved/open/regressed check (`~/.claude/skills/sc-implement-protocol/refs/qa.md`); rf-qa Fix Cycle steps 1-5.
7. Consumers? Orca coordinators and humans running a document loop; later `/sc:reflect`, rf-qa agents and the `/sc:implement` final review.
8. Test surface? Unit tests of the script (diff, hunk ids, anchor checker, ledger) under `uv run pytest`; text-presence tests for the command; a live A/B on S1 (2 replicates) for behaviour.
9. Forcing function? Issue #346 is open; 427 and 427+flags failed the pre-registered bar (R3 critical+major mean must be <= 3; growth <= 44.4%).
10. Rollback? The variant is additive: delete the file, or simply stop calling it.

## Problem Statement
A document review loop with `/sc:spec-panel` does not converge within its 3-review cap. PR 427 halved growth (63.5% to ~30%) but left the last-round blocking count at 5-6 (Arm B 6 and 1), and no run of any arm reached PASS. The re-review surface, the anchoring of findings, the verdict and the cap are all prose a model is asked to obey; the measured root cause (new findings on lines the previous fix changed) survives every prose variant tried.

## Known Context
- Experiment numbers (S1, 2 replicates/arm): control growth +57.7/+69.3%, R3 proxy 8/4; 427 growth +23.1/+36.3%, R3 6/5; Arm B (427+flags) growth +27.8/+32.1%, R3 6/1 (flg-r2 R3 had 4 findings, 1 blocking: N12, `origin=changed`).
- Arm B reports honoured the flags (status table, `origin=` tags, `review: N of 3`), but the reviewer derived the diff itself and judged scope itself.
- Arm B round-2 reviser applied all 15 rows including 5 minor findings and 4 citation notes ("Minor findings were applied too"), so fix cycles still touched lines no blocking finding named.
- Severity labels drift up between rounds; 427 grading relabels some MAJOR as minor, but the label is still reviewer judgement.
- Workers load `/sc:spec-panel` from `~/.claude/commands/sc/`; an experiment needs a different command name.
- Enrichment artifacts: `enrichment/codebase-context.md` (Wave 2A).

## Constraints
- Additive variant `spec-panel-diffgate`; `/sc:spec-panel` untouched.
- Mechanical over prose; every remaining prose rule named with its residual risk.
- Builds on 427 text (keep the 7 bullets' literals where still true).
- No new dependency; Python stdlib (`difflib`) via `uv run`; script must work outside this checkout (installed path, not `src/superclaude/...`).
- 3-review cap unchanged (pinned by `tests/skills/test_review_severity_rule.py`).
- Honest cost accounting (extra tool calls, sessions, wall time).

## Success Criteria
- On S1 (same briefs with one name substitution and the diffgate step lines), R3 critical+major <= 3 in both replicates, or a clean PASS by review 3; growth after two fix cycles <= 44.4%.
- A report whose finding cites neither a current hunk id nor a prior finding id is rejected by a script, not by a reviewer's self-assessment.
- A line changed by fix cycle k is reviewable in review k+1 only; never re-opened after that unless a later fix changes it again.
- Pre-existing defects review 1 missed end in a deferred list shown once at the end, never driving a fix cycle.

## Open Questions
- Who runs the script: the reviewer command itself (Bash inside the command), the coordinator, or a reviser-side step? Which placement can a model not skip?
- Granularity of the surface: hunks, changed lines, or changed sections (a hunk without its section context invites false findings)?
- How to bound fix-induced defects on changed lines without blinding the reviewer to real regressions (e.g., a fix-hunk budget per blocking finding, a "touched once" ledger, severity ceiling for review-3 findings)?
- Should the reviser side also be gated (every fix hunk must map to one blocking finding id; unmapped hunks reverted or rejected)?
- What does the checker do on reject: re-run the reviewer once, drop the unanchored finding to deferred, or fail the run?
- How does this generalise to `/sc:reflect`, rf-qa and the `/sc:implement` final review?

## Enrichment Context
Codebase scan: fallback_1 tier (auggie unavailable; Grep/Glob/Read). Research: skipped (`--no-research`). Full notes: `enrichment/codebase-context.md`.
- 427 bullet 5 asks the reviewer to find changed lines and self-tag `origin`; nothing computes or checks it (design doc section 12 says so).
- Nearest mechanical prior art: `/sc:implement` QA (`sc-implement-protocol/refs/qa.md`): structured finding lines with `at=`/`anchor=`/`origin=`, the parent Reads anchors back and derives the verdict; inherited text capped at note from `git diff` hunk headers; later reviews cannot re-open accepted text.
- Scripts ship inside a skill folder that has a `SKILL.md` (`install_skills.py:167-170`) and are run as `uv run --no-project python "<skill base>/scripts/<x>.py"`; stdlib `difflib` suffices (already used in `cli/eval/expect.py`).
- Pinned tests: `tests/skills/test_spec_panel_review_loop.py` (427 text), `tests/skills/test_review_severity_rule.py` (cap text, scans every command file), `tests/skills/test_worker_contract.py` (spec-panel Unattended section).
- A new command name is additive under `install_commands.py`; installed primitives name `~/.claude/...` paths plus the project `.claude/` copy, never `src/superclaude/`.
