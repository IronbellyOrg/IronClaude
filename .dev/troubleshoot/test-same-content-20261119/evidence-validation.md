# Evidence Validation Report (persisted by the parent from the `evidence-validator` agent's returned report)

**Report under validation**: REPORT.md.draft (this folder)
**Timestamp**: 2026-11-19T01:28:45Z
**Total citations**: 14 | **Verified**: 10 | **Dropped**: 1 | **Passed through (command, no re-execution)**: 3
**Suggested report status**: partial

## Verified citations
1. `src/superclaude/cli/install_keep.py:21` `return filecmp.cmp(a, b, shallow=False)` verified.
2. `install_keep.py:19` docstring "True only when both files are readable and byte-identical." verified (cited as the contract).
3. `install_keep.py:22-23` `except OSError: return False` verified.
4. `install_keep.py:42` `if same_content(shipped, target):` in `backup_if_differs` verified.
5. `tests/cli/test_install_keep.py:41-43` verified (41 assert same_content, 42 rewrite "y", 43 assert not same_content).
6. `src/superclaude/cli/install_core.py:121-125` private `_same_content`, same call, verified.
7. `src/superclaude/cli/install_user_setup.py:90` `if stale is not None and not same_content(src, target):` verified.
8. `src/superclaude/cli/install_commands.py:61` `if not same_content(command_file, target_file):` verified.
9. behaviour-definition row 1 verified (non-empty Status `fetched:raw-source`; quoted source present).
10. `docs/getting-started/upgrading.md` "keeps no backup" verified at line 29.

## Dropped citations
1. Draft sentence "`install_keep.py` and the test were last changed by commit `5fa680778` (#480)". The validator has no git access and could not verify it by Read; two research files name `5fa680778` as a base commit before another squash. Recommended action: remove the hash and "last changed by". The parent restated the claim from captured command output (see Parent resolution).

## Passed-through commands (matched against tier1-observation.md; not re-run)
1. `uv run pytest tests/cli/test_install_keep.py -q -k same_content` (1 failed at line 43, five of six runs).
2. `PYTHONPATH=/tmp uv run pytest ... -p probe_plugin` (six runs; the validator notes runs 2-6 are summarized "same pattern" with their mtimes, run 1 shown line by line).
3. `uv run python /tmp/probe_same_content.py` (188 of 200; the validator Read the script and confirmed its per-run assertion).

## Structural assertions
| id | fired | evidence |
|---|---|---|
| A1 | no | producers.md observation-kind string; calibrated 1.00; probes are captured failing-run output |
| A2 | skipped | input absent: diff_path (null) |
| A3 | no | draft has no Timestamp/Date/pushed_at line |
| A4 | no | no pipeline_hardening_verdict token; Wave 4.5 not applicable |
| A5 | no | Tier 2 not run; no consensus claim |
| A6 | skipped | no probe table; first_instrumented_run unknown |
| A7 | no | execution-locus.md gives a concrete RUN-SITE |
| A8 | no | OBSERVE-VIA same-shell; failing arm is local pytest, not CI |
| A9 | skipped | no reference-arm value in the draft |
| A10 | skipped | input absent: tasklist_path (null) |

No A-rule fired; the only status contribution is the dropped citation.

## Notes from the validator, and the parent's disposition
- "Not caused by 606": the validator could not establish "606 touched neither" by Read. Parent resolution: captured `git log` and `git log --oneline origin/master..HEAD` output is in tier1-observation.md (empty range: the branch did not change the three files; #480 is in the branch). The first attempt compared against local `master`, which is behind, and showed the files as new; that comparison was discarded and replaced by the origin/master one. Report sentence rewritten to cite the command output.
- "No architecture doc describes `filecmp`": too absolute (orchestrator-mode.md mentions it in a test). Report reworded to "none describes `same_content` or its caching".
- "Window tiny in real installs": an inference, contradicted in spirit by 188 of 200 same-tick runs on this machine. Report reworded to say the real-install frequency is not measured.
- Runs 2-6 of probe 3 are summarized in the observation file, not shown verbatim (only run 1 is). Left as is, with the file stating "same pattern" and each run's mtime.
- Skipped inputs: A2, A6, A9, A10. `candidate-fixes.md` is absent (no Tier 2), so A5's first clause was not evaluated.
- Not checked by the validator: the Grounding Gaps statement about the harness flag.
