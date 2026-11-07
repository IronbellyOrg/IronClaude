# Evidence validation (Wave 5 gate)

Validator: `evidence-validator` agent (read-only tools; it returned its result as text and could not write this file, so the orchestrator wrote it from the reply). Input: every citation in `adversarial/merged-verdict.yaml` (findings M-01..M-14, confirmations OK-1..OK-6) plus six report-body citations (`qa.md:9`, `qa.md:13-17`, `qa.md:21`, `handoff-routing.md:77`, `Makefile:48-50`, `.github/workflows/test.yml:99`). Mode: full re-read (not sampled), although the count is above 20.

## Counts
- Checked: 106
- Supported: 101
- Partial (narrowed): 3
- Dropped: 1
- Command results not re-run by the validator: 1 (M-01's read-only run; the orchestrator ran it twice, at about 12:20Z and in this gate's preparation, and the merge executor re-ran it at 12:24:50Z; `invariant-probe.md:18` records the same values)

## Dropped
- **OK-2, `variant-2-original.md:155`**: the line is V2's F-5 row (tier slices follow the brief's slicing pattern); it does not check anchors on disk. Dropped from OK-2. OK-2 stays supported by `variant-1-original.md:138` and `variant-3-original.md:133`.

## Narrowed
- **M-05**: `tests/skills/test_worker_contract.py:483-496` is `_unattended_section()` (the section-wide slice); the phrase check is `_check_unattended_section` at `:508-509`. Citation becomes `:483-496` and `:508-509`.
- **M-07**: `plan:156-157` give exit wording for `make sync-dev`, `make verify-sync` and `make lint`, but the pytest criterion says only "passing with no failure". The claim becomes: the pytest log has no exit-status criterion, and none of the logs is told to record an exit status.
- **M-14**: the previous report is `.dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-021737/REPORT.md`; its lines `:83` (M-13), `:84` (M-14), `:107` (INV-020) and `:108` (INV-021) support the four carried items; its `:82` (M-12) matches none of them and is removed. "Tier 1 card F-4" is this run's `reflection-card.yaml` finding F-4.

## Uncited or overstated claims, corrected in the report
- **M-03**: "the positive pins are shared by the old and the amended sentence" is overstated. The old sentence (`.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/source.md:217`) holds `lc10`, ``a `source: codebase` entry`` and ``neither `quality_tier` nor `source` records``, but not ``invokes `sc:analyze` `` (amended per `source:215`). Corrected: three of the four positive pins are also in the old sentence, so they cannot tell old from new; the fourth and the negative check can.
- **M-02**: "the workflow gate forbids numbered lines" is supported by `~/.claude/skills/sc-workflow-protocol/refs/quality-gates.md:29`; citation added.
- **M-04**: the regex test is recorded: the orchestrator ran `sed -n 45p <plan> | grep -cE 'only for a nested command that r[a]n'`, which printed 1 (the pattern matches the old literal).
- **OK-4**: "V1 and V3 could not run git or make" narrows to: V1 could not run git or make (`variant-1-original.md:152`), V3 could not run git (`variant-3-original.md:20`); "all three advocates accepted" is supported only for C-013 and C-016 (`debate-transcript.md:76`, `:79`), and the full scoring matrix records the rest.
- **M-01**: "Every current AC is a substring pin or a diff shape" narrows to: no current AC compares the whole text; the others are substring pins, diff shapes, existence checks or test runs (`plan:44`, `:47`, `:76`, `:77`).

## Weak but supported (validator's notes)
- `variant-2-original.md:153` covers Tasks 1-3 "in the prescribed forms", not byte-exact; OK-1's byte-exact claim rests on E-4 and on `variant-1-original.md:146` and `variant-3-original.md:140`.
- `analyze.md:98` adds nothing to M-10, which rests on `analyze.md:97`.
- `variant-3-original.md:137` backs OK-6 only on slicing soundness.

## Self-audit (validator)
Re-read all cited `source:` lines (34, 45, 63, 68-69, 71, 109-111, 159-161, 181, 213, 219, 223, 231-233, 239, 240-244), every cited `plan:` range plus `plan:136` and `:138`, `spec:62`, `:286`, `:296`, `lc10-result.md:13`, the full `invariant-probe.md`, `diff-analysis.md` and `coverage-matrix.yaml`, the cited variant lines, `SKILL.md:183` and its Wave 2A span (175-208), `handoff-routing.md:16-33` and `:77`, `brainstorm.md:157`, `analyze.md:97-98`, `test_worker_contract.py:286-288` and `:483-531`, `qa.md:9`, `:13-17`, `:21`, `Makefile:48-50`, `.github/workflows/test.yml:99`.

## Inferred requirement rows (D13)
The 45 INF rows in `artifacts/coverage-matrix.yaml` carry a line number, and their quote is by construction the first two sentences of that `source.md` line (`/tmp/p1_impl/coverage.py`), so every quote matches its cited line; no INF row was dropped. `coverage_pct_union`, `unmapped_requirements_union` and `S_dev_density` are unchanged.
