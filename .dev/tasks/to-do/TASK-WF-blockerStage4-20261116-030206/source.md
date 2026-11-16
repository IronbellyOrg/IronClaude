# Stage 4 plan request: propagate the new rule to the remaining carriers (issue #552)

Last of five plan packages (see `stage-requests/README.md`). Generate it only after the stage 3 package is done, one audit window has passed with no revert trigger tripped (the spec's section 13.2), the owner has read `./artifacts/stage3-summary-for-owner.md`, and the owner's go in chat is recorded in the stage ledger.

## Base text

Reuse Tasks 41 to 46 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` (Phase 5, stage 4; found by that folder name under `.dev/tasks/to-do/`), renumbered 1 onward, with its `## Constraints` (stage 4 parts). Earlier stages' evidence is read by package id.

## Changes to apply

- **Templates (the old Task 41).** The digest goes into four templates: `agent_template_qa.md`, `skill_template.md`, `01_mdtm_template_generic_task.md` and `02_mdtm_template_complex_task.md`. `agent_template_analysis.md` gets the merge-rule text only (no digest, no registry row, no fence). The registry keeps exactly 11 `digest` rows. Acceptance: "four template files hold exactly one digest", the analysis template holds none and no `more severe rating` text, and `agent_template_qa.md` holds none of the "Any CRITICAL or IMPORTANT issue exists" FAIL bullet unless it is listed as a kept mechanical gate in `refs/scale-map.md`. Remove `agent_template_qa.md` and `agent_template_analysis.md` from the scan allow-list in the same change.
- **Rule prompts, builders and researchers, consumer line (the old Tasks 42 to 44).** As the base text, with the two `pointer-only` rows left at `pointer-only` and the cap sentences kept by content.
- **Spec-panel (the old Task 45).** As the base text; the existing `src/superclaude/examples/...` mention in `commands/spec-panel.md` and its twins stays, since T3 does not check `pointer-only` rows for that path.
- **Plugin mirror (the old Task 46).** Order the work so the registry and the allow-list are correct BEFORE the copy: first add the plugin mirror of `refs/rule.md` to the `canonical` registry rows and to the allow-list in `refs/scale-map.md` (path only, no merge-rule phrases), then copy the skill folder to `plugins/superclaude/skills/sc-review-severity/`, then run T15 parity, strict T2 and the merge-rule scan. Acceptance includes `uv run pytest tests/skills/test_review_merge_rule_scan.py tests/skills/test_review_severity_plugin_parity.py tests/skills/test_review_severity_registry.py -v` passing, `make verify-sync` passing, and no `.claude/` path other than `.claude/settings.json` staged.
- **Constraints.** State this is stage 4 and the last package; strict T2 is switched on here. Acceptance lines that a later task of this package makes false get an end point.
- **New final task: stage 4 summary for the owner.** Write `./artifacts/stage4-summary-for-owner.md`: per carrier the digest state and the test that pins it, the final scan and parity results, and the revert command per row (the spec's three-step revert), ending with the sentence that a second audit window is observed by the owner or operator and is not a task of this package.

## Not to be done by the plan

No change to `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the severity code under `src/superclaude/cli/**/*.py`, the cap of 2 fix cycles or the 35 percent target. No Jev call, key or account.
