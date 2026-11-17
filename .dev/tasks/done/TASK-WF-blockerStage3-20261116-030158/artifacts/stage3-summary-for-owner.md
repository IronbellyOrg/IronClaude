# Stage 3 note for the owner (issue #552), written 2026-11-17

## What changed

The review rule in `src/superclaude/output-styles/pragmatic.md` now grades a finding by what changes if the flawed text is corrected (Decision, Missing, Safety are the only things that block). The same text is copied into ten carrier files (`rf-qa.md`, `rf-qa-qualitative.md`, two document templates, two workflow templates, four rule prompts). `rf-qa.md`, `rf-qa-qualitative.md` and `rf-analyst.md` were rewritten so they no longer fail a review by label. A new command `superclaude review fixcheck` runs mechanical checks over the lines a fix pass edited. The Medium offer now happens once per run and again at any escalation halt.

## Tests re-run for this note (observed 2026-11-17)

- Task 1: `uv run pytest tests/review/test_review_fixcheck.py tests/review/test_review_cli.py` gave `25 passed in 0.43s`.
- Task 7: `uv run pytest tests/skills/test_review_severity_rule.py tests/skills/test_review_severity_mapping.py tests/skills/test_implement_severity_static.py tests/skills/test_review_loop_extension.py tests/skills/test_review_prompt_overrides.py tests/skills/test_spec_panel_review_loop.py tests/skills/test_task_builder_merge.py tests/review/test_review_rules_text.py` gave `274 passed in 4.34s`. Re-pinned: the Medium pin in `test_review_severity_mapping.py` and the S2 pin in `test_implement_severity_static.py`.
- Task 8: `uv run pytest tests/audit` gave `1159 passed, 1 skipped, 5 warnings in 3.97s`. Re-pinned: the PASS and FAIL bullets in `test_nfr_conv_9_zero_trust.py`, and the Rule 6 text and block hash in `test_severity_floor_unweakened.py`.
- Task 9: `uv run pytest tests/skills/test_review_old_rule_scan.py` gave `4 passed in 0.13s`.

## What this package does not show

The stage 0 regrade is a lower bound. It regrades findings that were already filed as blocking, and it cannot show whether a reviewer would have found a defect. Its result, as its control test supports it, is only that the new text does not change grades on a table already filed as blocking (310 of 318 stay blocking under both texts, 82 of 82 panel blockers kept). Both arms carried the old rule through the same hook. Nothing in this note cites that regrade as evidence that the new text works. No seeded-defect experiment was run here.

## RT1 (the revert trigger)

The RT1 row of spec section 13.2 reads "Any real blocker found in a Medium list" (live spec line 988; `grep -c -i -F "any real blocker found in a Medium list"` prints 1). The words are the plan's, with a capital A in the spec. RT1 is a single event. It needs no sample size and acts through the safety rollback below.

## What you do after the switch

1. Let the first five runs finish. In each, read the Medium lists: the reviewers' `follow-up candidates` sections and the `notes.md` print at the end of `/sc:implement`.
2. Say in chat whether any real blocker sits in them.
3. The stage 4 go needs that statement and that RT1 did not trip.

## One small planted-defect check (part of the live RT1 audit, not a build task)

After the switch, plant a few known defects of the Decision, Missing and Safety kinds in one small deliverable (for example a wrong number an acceptance check uses, a required section left out, and a command that deletes data), run one fresh review on it, and confirm each is graded Blocking. No script is written. It covers what the stage 0 regrade cannot, because the regrade is a lower bound and cannot measure discovery.

## The safety rollback

Restore these files from the commit before this package's change, remove the files this package created, take `"fixcheck_cmd"` out of the tuple in `src/superclaude/cli/review/__init__.py`, run `make sync-dev`, then refresh each machine as in the next part.

Restore: `src/superclaude/output-styles/pragmatic.md`; the ten carriers `src/superclaude/agents/rf-qa.md`, `src/superclaude/agents/rf-qa-qualitative.md`, `src/superclaude/templates/documents/agent_template_qa.md`, `src/superclaude/templates/documents/skill_template.md`, `src/superclaude/templates/workflow/01_mdtm_template_generic_task.md`, `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` and the four `src/superclaude/rules/prompts/*_qa_prompt.md` files; `src/superclaude/agents/rf-analyst.md`; `src/superclaude/cli/review/__init__.py`; the re-pinned tests `tests/skills/test_review_severity_mapping.py`, `tests/skills/test_implement_severity_static.py`, `tests/audit/test_nfr_conv_9_zero_trust.py` and `tests/audit/test_severity_floor_unweakened.py` (the two fixtures and their plan tables were not changed).

Remove: `src/superclaude/cli/review/fixcheck.py`, `src/superclaude/cli/review/fixcheck_cmd.py`, `tests/review/test_review_fixcheck.py` and `tests/skills/test_review_old_rule_scan.py`.

## The refresh line

`make sync-dev` does not copy output styles, so the installed `~/.claude/output-styles/pragmatic.md` stays old until you refresh it. Run `superclaude install --force` from an install that holds this change (`install_output_styles` in `src/superclaude/cli/install_user_setup.py` takes the `force` flag and reports files it keeps). The check that it worked: `grep -c "asks the user once per run, and again at any escalation halt" ~/.claude/output-styles/pragmatic.md` prints 1.

Observed on this machine today, before any refresh: that command prints 0. The new rule is not live on a machine until it prints 1. Other installed copies stay old too, for example the package copy under `.venv/lib/python3.11/site-packages/superclaude/_src/` still holds the old sentence.

Also found: one Markdown file outside the scanned roots still holds the old sentence, `docs/developer-guide/review-severity-rule.md` line 24. The reverse scan does not cover `docs/`. It was not edited here (not in the plan).

The owner's go for stage 4 is given in chat and not by this file.
