# Scope review card

## Scope and evidence

Requested model: opus. Persona: refactorer. Read full plan, source, coverage matrix, governing workflow template, executor qa.md and real code/tests/docs. Codegraph state fresh. No commands, edits or test/model runs. All assigned source slice rows (INF-002, 003, 007, 008, 010, 011) substantively covered; independent report basename is form, not missing review. Red/green order, current two-producer scope, schema/preflight invariants, five test files and coverage dependency were checked.

## Findings

### F1: Task 4 does not stand alone for public-output acceptance

- Label: HIGH. Grade: Blocking (Missing). Category: drift from governing template stand-alone rule.
- Location: candidate Task 4 acceptance, lines 80 and 82.
- Evidence: line 82 says "with the same three CLI invocations as Task 2" and line 80 says "after their preserved pre-edit observations". Task 4 does not itself list the three public commands or baseline/red evidence paths.
- Governing rule: workflow template line 15 says each task must stand alone because its reviewer sees only that task and global Constraints. Executor `sc-implement-protocol/refs/qa.md:9` supplies a task brief (Ti text + AC ids + global constraints) and diff, not sibling tasks.
- Affected action: per-task review of Task 4 cannot verify identical pre/post public invocations and prior observations from its supplied brief. The command could be confused with only CliRunner rather than real `uv run superclaude` entrypoints.
- Narrow remedy: in Task 4 inline `uv run superclaude swarm validate-lenses --help`, `uv run superclaude swarm scaffold --help`, and `uv run superclaude swarm run --custom-prompt-dir <existing temporary directory>`. Name `./artifacts/public-before.txt`, `./artifacts/validate-help-red.txt`, `./artifacts/scaffold-help-red.txt` and `./artifacts/parser-before.txt` as comparison inputs. No product fix or redesign needed.

### F2: Other cross-task lookup shorthand

- Label: MEDIUM. Grade: Medium, nonblocking. Category: template stand-alone drift.
- Location: Task 2 body line 47 and Task 3 acceptance line 66.
- Task 2 refers to schema/preflight symbols named in Task 1 rather than naming them; Task 3 refers to Task 2's tests without file/node names. The reviewer grades this nonblocking because the checks are otherwise specified and evidence paths named.
- Suggested follow-up: inline `_apply_custom_prompt_dir` in `src/superclaude/cli/swarm/preflight.py`, `_custom_prompt_dir_lens_failures` in `src/superclaude/cli/swarm/schema.py`, and regression test file/node references. No Medium-only fix pass.

### F3: Negative help-token check can miss wrapped spelling

- Label: MEDIUM. Grade: Medium, nonblocking. Category: weak check.
- Location: Task 1 line 36 and Task 2 line 50.
- Evidence: historical validate-lenses-help.txt:12-13 wraps `--warning-` / `mode`; lines 16-17 wrap `opt-` / `in`. Therefore hyphenated help tokens can split. Normalizing whitespace by collapsing it can leave `--custom- prompt-dir`, which misses an exact-token negative assertion.
- Consequence: partial wrong wording could pass the negative assertion, though current red runs still fail on missing positive JobSpec/custom_prompt_dir guidance. Suggested follow-up: remove all whitespace or join hyphen-wrap splits before absence assertion.

### F4: Coverage receipt calls wrapping unverified

- Label: LOW. Grade: Note. Category: citation/status wording only.
- Location: coverage-matrix.md candidate-warning paragraph. Existing captured help already demonstrates hyphen wrapping; parent may retain receipt as historical belief but should not repeat it as current uncertainty without qualification.

## Verdict

FAIL: one Blocking (Missing), two Medium follow-up candidates and one Note. Six assigned source requirements are adherent; no product regression claimed. Narrow plan-only correction to Task 4's stand-alone acceptance is sufficient for the identified blocker, subject to independent re-review. This card authorizes no edit.

## Calibration

Independent fresh-context calibration: C=0.81; scores [0.85, 0.80, 0.75, 0.75, 0.90], five-dimension arithmetic mean. See ../reviewer-calibrations/reviewer-3.md. Calibrator model-class diversity degraded. F1's template and executor-input citations verified; F1/F2 grading distinction needs adjudication.
