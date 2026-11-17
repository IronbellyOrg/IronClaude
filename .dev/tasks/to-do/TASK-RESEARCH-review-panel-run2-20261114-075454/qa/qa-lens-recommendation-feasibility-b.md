# QA Report - Recommendation-Feasibility (instance b)

**Topic:** one unified central Review Panel (shared core plus thin modules) from E1, E2 and E3 (run 2, report only)
**Date:** 2026-11-15
**Phase:** report-qualitative, lens recommendation-feasibility, instance b
**Range reviewed:** lines 2115 to 5057 of `RESEARCH-REPORT-review-panel-unification-run2.md` (Sections 6 to 10, Appendix A pointer, Appendix B). Lines 1 to 2114 only via Grep.
**Fix cycle:** N/A (Gate 3)
**Grading:** grading override in `qa/grading-override.md` applies.
**Status: Complete** (see the end of the file for verdict and summary)

Scope notes: lens = recommendation-feasibility only. Range 2115 to 5057 read by section (6.1 options C and D, all Effort and Risk rows of Section 6 by Grep, 7.0 to 7.3, 8.2 (a) to (e)); other lines only by Grep. Verification was read-only at HEAD `50d4d2b9d`; the E2 tip was read only through `git show` and `git diff --name-only`. No file other than this report was modified. The independence rule was kept (the unify task folder and the QUEUED file were not touched).

## Verification log (lens checklist item a: at least 10 claims against code or tests)

| # | Claim in the report | Where | Check | Result |
|---|---|---|---|---|
| 1 | Contract 1.8.0, 110 stable names, 27 telemetry names, version reject at `panel_lint.py:312-314`, unknown-key reject `:316`, `LEGAL_MERGE_METHODS` at `:184` | 8.2 C1, G2, I-1 | Read `panel_lint.py:184,185,312-316`; `uv run python` import printed `110 27` | TRUE |
| 2 | 36-test verdict matrix; 0.80 constant at `contract.py:321`; trigger text `:309-326` | I-2, C3, G1 | Grep count of `def test_` in `tests/cli/reflect/test_verdict_mapping.py` = 36; Read `contract.py:300-331` | TRUE |
| 3 | `### 9.1` block byte-identical to HEAD (compares with `git show HEAD:`), allow-list `### 3.1 / 4.3a / 5.4 / 9.2` at `test_shadow_skill_contract.py:65` | I-1, C2, G3, G19 | Read `test_shadow_skill_contract.py:42-70` | TRUE |
| 4 | Pins `test_review_findings.py:113` (anchor 201) and `:117` (claim 301) assert `ok is False` | C17, CT-2 | Read `tests/review/test_review_findings.py:105-122` | TRUE |
| 5 | v1 `annotate` needs `finding["anchor"]` (`findings.py:346-349`), `merge_round` calls it (`ledger.py:127-138`), `anchor` limits 12..200 at `findings.py:104`; v2 accepts citation-only (`findings_v2.py:122-131`) | D9, element 1 | Read all four ranges | TRUE (the KeyError path exists as described) |
| 6 | `cluster_v2` cannot cluster anchor-only findings; pin `test_review_cluster.py:279-293`; `PRIMARY_ROLES` at `cluster.py:67-71` | axis 1, element 2 | Read `cluster.py:60-181` and the test | TRUE |
| 7 | Engine A is the production Tier 2 route (`runner.py:538-545`), reviewers see tasklist body only (`ensemble.py:601-630`), verdict via `derive_verdict(... promoting=...)` at `runner.py:573-580` | F-5, G5, C-04 | Read all three ranges | TRUE |
| 8 | `cli/review` and `cli/reflect` import each other nowhere in `src/`; the one cross import is a test (`test_shadow_skill_contract.py:14` imports `panel`) | I-8, D21, F-2 | Grep both directions (0 hits); Read test line 14 | TRUE |
| 9 | Review package has 25 tracked files, 16 `.py` files, 5,086 lines; optional-module loop at `__init__.py:14-36`; `lint_cmd` and `estimate_cmd` listed but absent; `verify-citations` is the real command name | 7.1, D20, (e) | `git ls-files`, `ls`, `wc -l` over `cat` of the files, Read `__init__.py`, Grep `@click.command(name=` | TRUE |
| 10 | E2 changed no file under `src/` or `tests/`; E2 launcher leaves Bash open (`run-reviewer.sh:48`, disallows only `Edit Write NotebookEdit`) | F-3, axis 5 | `git diff --name-only <merge-base> 6c0984326... -- src tests` printed nothing; `git show 6c0984326...:...run-reviewer.sh` line 48 | TRUE |
| 11 | Packaged `gateway.launch` is `{}`; `_REFLECT_LAUNCH = ("sonnet","opus","haiku")`; `validate_reflect_profile` at `panel.py:80`; template slot keys closed (`panel.py:46`, `:215-216`); six `review-panel.reflect-*.json` templates; nine files in `data/` | C20, element 6, D11, G8 | Read `review-tiers.default.json:25-30`, Grep `panel.py`, `ls data/` | TRUE (see M-5 on the word "templates") |
| 12 | `reflect-reviewer` is read-only by agent definition (`tools:` allow-list without Bash, Edit, Write) | axis 5, 7.2 | Grep of the frontmatter of `.claude/agents/reflect-reviewer.md` (dev copy of the `src/superclaude/agents/` file, which exists) | TRUE |
| 13 | `make verify-sync` demands a mirror for every skill directory while `sync-dev` skips one without `SKILL.md` (`Makefile:115` vs `:171-176`); CI runs `make sync-dev` (`test.yml:127`), `make verify-sync` (`:131`), lint-architecture (`:135`); pre-commit does not run `verify-sync` (`.pre-commit-config.yaml:117,132-138`) | C5, D1, G9 | Read the Makefile and workflow lines, Grep the pre-commit file | TRUE |
| 14 | Plugin tree hand-kept and partial: 4 skills, 28 commands, 125 tracked files, no `sc-reflect-protocol` | C8, I-9 | `ls plugins/superclaude/skills`, `git ls-files plugins/superclaude` counted, `ls plugins/superclaude/commands` counted | TRUE |
| 15 | Reviser brief id line pinned at `test_review_ledger.py:459-467`; `ledger.py:3-4` docstring | C18, element 3 | Read both | TRUE |
| 16 | Line counts and tests: `findings.py` 457, `findings_v2.py` 304, `ledger.py` 494, `panel.py` 707, `contract.py` 420, `panel_lint.py` 366, `ensemble.py` 895, `runner.py` 834, reflect SKILL 2033, `reflect_shadow_exit.py` 410, `fsm.py` 1257, pr-submit SKILL 376; `tests/review/` 19 files; `tests/cli/reflect/` 38 files; `pr_submit` 12 modules, 6,511 lines | (e), G4, G8 | `wc -l`, `ls | wc -l` | TRUE |
| 17 | 44 structured `subagent_type: rf-*` lines in 8 `SKILL.md` files; 31 command files with `## Unattended mode` | 7.1, (e), G13 | Grep with file list; Grep count | TRUE |
| 18 | `reflect_shadow_exit.py:313` empty-baseline comparison and `:59` card regex | D7, D26, G26 | Read both lines (`:59` is `_CARD = ^reviewer-(\d+)\.md$`; `:313` is `(s_rate or 0.0) > (l_rate or 0.0)`) | TRUE |
| 19 | Exit code 12 for the quorum refusal does not collide with existing review CLI codes | C-03 outcome | Grep `ledger_cmd.py:13` (`0/10/11`), `panel_cmd.py` (`1`) | TRUE (no collision) |
| 20 | Section 7.3 totals 60 / 161 / 23 = 244 | 7.3 | Summed the 15 rows by hand per column | TRUE |
| 21 | `scripts/reflect_verdict_replay.py`, `tests/review/test_reflect_consumer_inventory.py`, `scripts/reflect_consumer_inventory.py`, `card_convert.py`, `cluster_cmd.py`, `verify_cmd.py`, `manifest_cmd.py`, `telemetry_cmd.py` exist | (d), (e) | Existence loop | TRUE |

## Lens findings

### a. Feasibility against the codebase constraints (Section 2 and 8.2)

No recommended change targets a component that does not exist or is deprecated. Every constraint in 8.2 (a) to (c) that I re-checked (21 rows above) matches the code. The recommended design keeps contract 1.8.0, `derive_verdict` and its 36 tests untouched, keeps the v1 parser pins unmodified under the default (`repair=False`), keeps `cli/review` free of `cli/reflect` imports, and adds only files and CLI subcommands under the existing `review_group` loader. Exit code 12 is unused. The three places where the design touches a pin (C-02/C-03 rewrite of the clearing and quorum tests; the SKILL.md edit allow-list at `test_shadow_skill_contract.py:65`; the `ensemble.py:601-630` H1 edit) are each named as a condition or an open question (C15, C16, C18, CT-1, Q-41), not hidden.

### b. Per-option effort and risk attributes

The attributes are consistent with the evidence they cite (for example 6.1 Option A "L" rests on the `annotate` KeyError at `findings.py:346-349`, confirmed; 6.3 Option 3 "High" for keep-and-warn rests on the recovery of 0 lines; 6.8 Option 4 "L / Medium" matches the serializer, card writer and finalizer work with the checking code already present). One observation, not a defect: the per-axis ratings are not composed into a rating of the recommended composite (Option C "M" says "contract-level work only", while the adopted shape also carries the axis 4 rewrite rated "L"). The report states that it gives no estimate (8.2 scope statement), so this is consistent with its own rule.

### c. Dependencies of the gap analysis (Section 4) and unaddressed debate invariants (7.3)

The 15 debate rows of 7.3 are all carried as OPEN with a synth-10 question id and the totals add up. The weak spot is traceability from Section 4 to Section 7: lines 3544 to 4648 contain no `G-` or `SC-` identifier, so the 24 Critical gaps of 4.1 are not mapped one by one to a design element. Content-wise most are covered (verdict fail-open, dispatch, served model, input manifest, deterministic shadow steps, acceptance evidence). Four Critical gaps (G-20, G-42, G-43, G-44: two Tier 2 engines, count-derived tasklist-only convergence, dormant `--fix`, unapplied executor-class exclusion) stay open by the C-04 decision and are disclosed through the single-engine question (Q-09), and G-22 / G-137 (dead registrations, success criterion SC-20) get a destination only in FX-22, D20 and 8.2(e). See M-3 and M-4.

### d. Components that do not exist or are deprecated

None found. New names (`review record`, `review-run-event/1`, `review-rowcheck/1`, `rows-v1`) are marked as new or gated in the report; the existing-component names checked (rows 9, 11, 21) all resolve.

## Findings

Grading uses `qa/grading-override.md`. None of the findings below changes a decision, a recommendation, a value-inventory destination, a conflict outcome or a number the recommendation rests on, none is a missing required section, and none is a security or data-loss risk. All are therefore minor under the override and are notes for the follow-up list.

| # | Severity | Section | Finding | Evidence | Proposed Fix |
|---|---|---|---|---|---|
| M-1 | MINOR (minor under grading override) | 7.1 PR code review row, 8.2 G14, 8.2 (e), 6.11 Option 2 Risk | "50 test files under `tests/pr_submit/`" is a miscount: there are 47 `test_*.py` files. Section 7.2.1 row 5 says "50 files, 47 `test_*.py`", so the report disagrees with itself. The conclusion (the adapter route leaves those tests untouched) is unaffected. | `find tests/pr_submit -name 'test_*.py'` counted 47; `git ls-files tests/pr_submit` counted 91 (fixtures included). | Say "47 test files" everywhere, or "50 files" only where the count includes `__init__.py`, `conftest.py` and the fixtures directory, and say so. |
| M-2 | MINOR (minor under grading override) | 7.1 element 1 (Modules supply cell), 6.2 Option 2 Risk, 7.1 task-id family row | The second copy of the reference-token regex is cited as `telemetry.py:23`, "copied" from `_REF_TOKEN` (`findings.py:29`). In `telemetry.py` the line is the assignment to `_ID_TOKEN` (the same character pattern, `[A-Z]{1,4}-[0-9]+...` or `P[0-9]`); the name `_REF_TOKEN` does not occur in that file. The regex text is the same, so the claim of a second copy is true; only the identifier differs. | Read `telemetry.py:18-29`; Grep `_REF_TOKEN` in `telemetry.py` returned no match; Read `findings.py:29`. | Write "`_ID_TOKEN` at `telemetry.py:23` (same regex as `_REF_TOKEN`)". |
| M-3 | MINOR (minor under grading override) | 7.1 defect-ownership table (after the invariants table) | The table header says CORE owns 75 register rows, but the family rows list only 63 CORE ids. Twelve CORE rows of `research/17-defect-register.md` appear in no family: DR-010, 019, 042, 052, 064, 066, 070, 072, 073, 080, 090, 100. Several are covered in prose elsewhere (DR-010 in element 2; the tier-registry rows by C-09), but DR-042 (dead `lint_cmd` / `estimate_cmd` registrations, behind Critical gaps G-22 and G-137 and success criterion SC-20) is not mentioned in Section 7 at all. Its destination exists in FX-22 ("remove the dead names or add the modules"), D20, 8.2(e) and value-inventory row VL-24-252 (CORE), so the recommendation, the inventory destination and the conflict outcome are all still correct. | Awk over the register's owner column gave 75 CORE ids; comparison with the ids printed in the table gave the 12 above. Grep for `estimate_cmd` in report lines 3544-4208 returned no hit. | Add the 12 ids to the families they belong to (or one "other CORE rows" line), with DR-042 under "Persistence and CLI". |
| M-4 | MINOR (minor under grading override) | Section 7 (whole) against Section 4.1 | Section 7 never cites a gap id or a Section 3.3 success criterion, so a reader cannot see which of the 24 Critical gaps the design closes and which it leaves open. Four (G-20, G-42, G-43, G-44) are left open on purpose by C-04 and are covered by Q-09; SC-20 is not satisfied by any element. Nothing the recommendation rests on is wrong. | `awk 'NR>=3544 && NR<=4648'` over the report, then grep for `G-NN` and `SC-NN`: 0 hits for all 24 Critical ids. | Add a short table "Critical gaps: closed by element / left open and why" to 7.1 or 7.0.1. |
| M-5 | MINOR (minor under grading override) | 8.2 D11 | "The nine `data/*.json` templates carry no `lens` key" counts the tier file as a template: `data/` holds eight panel templates plus `review-tiers.default.json` (G8 lists the nine files correctly; D11's own evidence says "24 hits over 8 templates"). | `ls src/superclaude/cli/review/data/`. | Say "the eight panel templates". |
| M-6 | MINOR (minor under grading override) | 7.1 axis 8 trade-off cell and 7.0.1 CT-1 (reflect helper placement) | The helper placement is listed as "`cli/reflect/` registered on `review_group`" against "`cli/review/<name>_cmd.py`". `review_group` registers only submodules named in the loop at `cli/review/__init__.py:14-36` (`importlib.import_module(f"{__name__}.{_name}")`), so a helper in `cli/reflect/` cannot be registered there without a new import inside `cli/review`, which invariant I-8 forbids. The report already carries the placement as an open sub-dispute (Q-41), so this is a detail to add to that question, not an unflagged defect. | Read `__init__.py:14-36`; Grep `cli.reflect` in `cli/review` (0 hits). | Add one sentence to Q-41: registering a `cli/reflect/` helper needs a registration path other than the current loop, or the placement `cli/review/<name>_cmd.py`. |

## Observations that need no fix

- The effort and risk attributes carry a basis for every row; no row is unsupported.
- The 8.2 (b) gates name a command for every pinned behaviour and say honestly which were read and which were run (R18 ran none of the make targets, R06 ran the reflect tests).
- 7.2 verdicts (PR review NO, rf-qa NO, later reviewers NO) each state the condition that keeps them unblocked and mark the unread candidates as carrying no verdict.

## Self-Audit

**(a) Reliance list:** The spawn prompt carried no `## Inherited Structural Verdict`; standalone mode applied. No rf-qa PASS item was relied on.

**(b) Independent semantic checks (at least 1 required):**
- Re-derived the contract-pin facts (log rows 1 to 4) from code and tests with my own Read, Grep and `uv run python` calls.
- Re-derived the E2 facts (row 10) from git objects, not from the research files.
- Recomputed the 7.3 totals (row 20) and the register-to-family coverage (M-3) from the research files with awk.
- Checked the loader constraint for helper placement (M-6) in `cli/review/__init__.py`.

**Counts:** about 60 distinct factual claims were checked against code, tests, git objects or the research files (the 21 rows above plus the line, count and name checks inside them). Files read: the report (sections 6.1, 7, 8.2, 4.1 and the Section 6 Effort and Risk rows), `research/17-defect-register.md` (awk), `synthesis/synth-08-value-inventory.md` and `synth-06-conflict-log.md` (Grep), and the code and test files named in the log. Web research: none was needed (Tavily not used, no fallback).

## Summary

- Lens items passed: 4 / 4 (a, b, c, d), with 6 minor notes.
- Blocking findings under the grading override: 0.
- Minor findings (all marked "minor under grading override"): 6 (M-1 to M-6).
- Claims verified: 21 log rows, all true; no false claim carries a decision.
- Confidence: Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement (approximate): Read: 17 | Grep: 17 | Glob: 0 | Bash: 10
- Limits: I did not re-run the test suites or the make targets (read-only rule), so the 352-pass baseline and the CI behaviour of the make targets rest on the research files and static reading. I read lines 1 to 2114 of the report only by Grep.

## Overall Verdict: PASS

Zero findings are blocking under the grading override.

**Status: Complete**

