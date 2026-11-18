persona: refactorer
model_class: opus
model: claude-gw-tier1a[1m] (pinned by the spawn override; self-report below agrees)
agent_type: reflect-reviewer

## Verdict: NEEDS-REVISION

## First-review findings
- F1: fixed, PLAN:125. It now has the end point "Until Task 10 adds an importer" and names the allowed importers. The grep it relies on still cannot pass as written; see R3-F1.
- F2: fixed, PLAN:64, 70, 223, 230-231. The stoprule and `finding-grader` row is `installed-only`, names two `~/.claude/` paths, and is exempt from the exists check and from T4. Task 3 and Task 15 use the same word.
- F3: fixed, PLAN:66, 73. `remediate_parser.py` and `fmea_classifier.py` are listed as `allowed`, and `stage3-request.md:14` names both.
- F4: fixed, PLAN:120, 124. The plan states the version 1 decision ("separate file, no mapping"), names the ledger adapters, and Task 16 reports the audit verdict.
- F5: fixed, PLAN:62, 144, 182, 221. Columns, path root and the `none` label value are fixed, and Tasks 9, 12 and 15 depend on Task 3. A design gap remains in the `labels` format; see R3-F2.
- F6: fixed, PLAN:157. Task 10 depends on Task 7 and Task 9.
- F7: fixed, PLAN:146, 159, 171, 196. `run_questions` is built in Task 9 and `questions_to_ask` in Task 10, and the safety-route half of T12 moved to Task 13.
- F8: fixed with a small leftover, PLAN:56, 184. The grep uses the full path and `lint`/`estimate` are described correctly, but one subcommand name is wrong (`verify`); see R3-F6.
- F9: fixed, PLAN:81, 87. `sweep-flagged` is defined as a ninth state and its passage names no rollout stage.

## Findings

### R3-F1 [BLOCKING] Task 7's grep also lists `.pyc` files, so "lists only `follow_ups.py`" can never be met
**Evidence:**
- PLAN:125: "`grep -rln "follow_ups" src/superclaude/cli/review` lists only `follow_ups.py`. From Task 10 on, the only other files it may list are `classifier_inputs.py`, `classify_cmd.py` and `safety_route.py`".
- The `__pycache__` folder already exists in `src/superclaude/cli/review/` and holds compiled copies of the existing modules: `__pycache__/ledger.cpython-311.pyc` and `ledger.cpython-311-pytest-9.2.0.pyc` (Glob, this review).
- `grep -r -l` lists any matching file, including compiled `.pyc` files.
- PLAN:123 runs `uv run pytest tests/review/test_review_follow_ups.py` first, which imports `follow_ups` and writes `__pycache__/follow_ups.cpython-311*.pyc`. That compiled file contains the module's file path, so it matches "follow_ups".
- `.gitignore:2` is `__pycache__/`, so these files are always present after a test run but are never part of the code.

**Consequence:** After the executor runs Task 7's own first acceptance command, the grep prints `follow_ups.py` plus at least one `__pycache__/follow_ups*.pyc`. The literal check fails. From Task 10 on it also prints the compiled copies of the three allowed importers, which are not on the allowed list. The executor either halts or quietly ignores the extra lines, which means the check stops being a real check.

**Fix:** Change both sentences at PLAN:125 to `grep -rln --include='*.py' "follow_ups" src/superclaude/cli/review`.

### R3-F2 [NON-BLOCKING] The scale map's `labels` format has no family key and cannot hold the spec's conditional mappings, yet code reads it
**Evidence:**
- PLAN:62 defines `labels` as "`LABEL=Outcome` pairs" with outcomes Blocking, Medium or Note.
- PLAN:146 says `ReviewerJudge` reads "the reviewer's own label read through the scale map", and PLAN:184 prints the disagreement matrix "read through the scale map". Neither says which family's row a finding's label is looked up in.
- The same word maps to different outcomes in different rows:
  - SPEC:742: tasklist "Medium: Blocking today".
  - SPEC:744: `card_convert.py` maps "`important` and `medium` to non-blocking".
  - SPEC:211: "an rf-qa IMPORTANT reads as blocking".
- Some spec mappings are conditional and do not fit one pair:
  - SPEC:739: MAJOR is "Blocking only when it names a concrete wrong outcome, else Medium".
  - SPEC:740: "B1, B2 and B3 together: Blocking; otherwise Note or Medium".

**Consequence:** Whoever writes Tasks 9 and 12 has to invent a lookup key (for example from the ledger `source` or `origin` column) and has to collapse the conditional rows into one fixed outcome. The shadow disagreement numbers would then depend on choices the spec never made. No acceptance line catches this.

**Fix:**
- In Task 9, name the key: "the family is taken from the protocol name in the ledger row's `origin`/`source` cell and matched to the `family` column".
- In Task 3, allow a conditional outcome token (for example `MAJOR=Blocking-if-concrete-else-Medium`) and say that `ReviewerJudge` returns UNSET for a conditional pair.

### R3-F3 [NON-BLOCKING] REQ-09 (cross-run matching) is not assigned in this plan or any other stage plan
**Evidence:**
- SPEC:396 (REQ-09): "A new run on the same deliverable matches earlier `declined`, `filed` and `resolved` rows by the identity tuple without the run namespace, and does not offer or file them again."
- PLAN:120 lists REQ-07, REQ-08 and REQ-10 and the identity tuple, but not REQ-09.
- A Grep for `REQ-09|across runs|cross-run` over all four `TASK-WF-blockerStage*` plans finds nothing.
- SPEC:1185 records INV-002 as resolved only by REQ-09.

**Consequence:** The one reader and writer (REQ-10) is built without matching rows across runs. Unless a later stage plan adds it, no stage ever implements REQ-09, and earlier declined or filed rows get offered again.

**Fix:** Add to Task 7 "a lookup of earlier `declined`, `filed` and `resolved` rows by the identity tuple without the run namespace (REQ-09)", with one test in `test_review_follow_ups.py`. Alternatively, name it explicitly as owned by the stage 2 offer task.

### R3-F4 [NON-BLOCKING] Task 4's copy of section 6.6 breaks Task 5's grep over the whole skill folder
**Evidence:**
- PLAN:81 tells Task 4 to copy "from spec sections 6.1 to 6.7 … the location rule (REQ-07)".
- SPEC:485, in the REQ-07 exceptions table, reads "`.dev/pr-monitor/` is gitignored".
- PLAN:97 requires `grep -rn "\.dev/\|artifacts/" src/superclaude/skills/sc-review-severity` to print nothing.

**Consequence:** An executor who copies the location table faithfully in Task 4 then fails Task 5 and has to go back and edit Task 4's file.

**Fix:** In Task 4, add "copy the pr-submit exception without the gitignored path".

### R3-F5 [NON-BLOCKING] Task 8 points code at a standalone script but does not say how to call it or fake it
**Evidence:**
- PLAN:132: "the target comes from the `origin_repo.py` script of `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py`".
- `origin_repo.py:7-9` is a command-line program ("Usage: origin_repo.py … Print `owner/repo` parsed from `git remote get-url origin`").
- Its folder `sc-issue-protocol` has a hyphen, so it cannot be loaded with a normal import.
- PLAN:137 refers to "the resolver", but only the `gh` call is said to be injected.

**Consequence:** The implementer must choose between running it as a subprocess and loading it from its file path, and must invent a way to fake it in T8 tests. The T8 case "a repository other than the verified one is targeted" needs exactly that fake.

**Fix:** In Task 8, say "the resolver is also an injected function; the default runs `origin_repo.py` as a subprocess; tests pass a fake resolver".

### R3-F6 [NON-BLOCKING] Small wording and ordering defects
**Evidence:**
- PLAN:184 lists `verify` as a review subcommand present today. The real name is `verify-citations` (`src/superclaude/cli/review/verify_cmd.py:76`, `@click.command(name="verify-citations")`).
- PLAN:223 has a stray ", ;" after the T3 pointer text.
- PLAN:223 also says `installed-only` rows "are checked for pointer order only" and that "the test never reads `~/.claude`". Those files exist only under `~/.claude`, so that check does nothing.
- PLAN:36-40: Task 1 creates `SKILL.md` before its acceptance lines check that the owner said go and that `stage0-summary-for-owner.md` exists. The entry gate runs after the work, not before it.
- PLAN:52: "prints nothing outside the one fenced digest's own text (the digest does not quote the old sentence either)" cancels itself out; it simply means "prints nothing".

**Consequence:** Cosmetic, except the Task 1 order, which leaves a created file behind when the gate fails.

**Fix:**
- Change `verify` to `verify-citations`.
- Delete the ", ;".
- Say "installed-only rows are not checked by T3 (excluded from CI, SPEC:725)".
- Move the go and stage 0 checks to the first sentence of Task 1's body.
- Reword PLAN:52 to "prints nothing".

## Checked and found sound
- Task numbering 1 to 16 is continuous. Every `Depends on:` names only lower task numbers, and the dependencies match what each task reads: Task 10 needs 7 and 9, Task 11 needs 9 and 10, Task 12 needs 3, 7, 9 and 10, Task 13 needs 7 and 9, Task 15 needs 2, 3 and 6.
- Exactly 11 files under `src` and `plugins` hold "Grade every review finding as blocking or minor", and they are the 11 `digest` rows of Task 6. `skills/task/SKILL.md` does not hold it, so T2 (not yet strict) passes with no row for it.
- None of the 11 digest carriers contains `src/superclaude`, so T3 on `legacy` rows passes (PLAN:227).
- The merge-rule phrases appear in 13 files under src. Task 3's allow-list plus the stage 3 carriers (rf-qa, rf-qa-qualitative, rf-analyst) cover all 13. Section 6 of the spec holds none of the phrases.
- The cap sentence quoted at PLAN:49 equals `pragmatic.md:227` word for word, and it is the last sentence of REQ-01 (SPEC:207).
- These paths exist: `test_review_cli.py`, `test_cli_doctor.py`, `test_install_retired_mcp.py` (the named test at line 579), `test_update_command.py`, `agents/reuse-auditor.md`, the sketch, `07-classifier/truth_table.py`, `08-test/results.md` and `09-plan-input.md`. The 6,400-combination count matches SPEC:551.
- `review/__init__.py` loads its subcommands optionally, so adding `"classify_cmd"` to the tuple is safe. `test_review_help_lists_the_subcommands` checks only four names.
- The wheel includes `src/**` (pyproject:79-81), so the packaged `scale-map.md` and `registry.yaml` can be read at runtime.
- No existing test that loops over all skills is broken by a new skill folder (`test_graph_command.py`, `test_model_alias_policy.py`).
- Against `revision2-brief.md`, shared decisions 1, 2, 4 and 5 are reflected at PLAN:24-26 and 120, there is no plugin mirror or parity test, and the registry counts are 11/1/2/5.
- The spec's stage 1 exit tests are all mapped (T1-T4, T14 in Task 15; T6, T11, T12a in Task 11; T12b and T17 in Task 13; T7 in Task 7; T8 in Task 8; T13 in Task 14). The skill folder has the 6 files SPEC:877 names.

## Self-reported confidence: 0.80
reviewer_model_self_report: claude-gw-tier1a (Claude, refactorer persona)

Not checked: I did not run any command, so R3-F1 is based on how `grep -r -l` and Python's compiled-file cache behave plus the `.pyc` files already in that folder, not on a live run. I also did not check whether code written later in `doctor.py` would trip T2's scan for digest fence lines.


## Blind calibration (confidence-calibrator, opus class; appended by the orchestrator)

```yaml
calibration: {persona: refactorer, model_class: opus, calibrated_confidence: 0.83, per_dimension: {citation_grounding: 0.85, coverage_completeness: 0.82, deviation_classification_clarity: 0.80, risk_surface_coverage: 0.80, recommendation_actionability: 0.90}, per_finding: {R3-F1: 0.80, R3-F2: 0.70, R3-F3: 0.65, R3-F4: 0.75, R3-F5: 0.72, R3-F6: 0.78}, self_reported: 0.80, adjustment: 0.03}
```
