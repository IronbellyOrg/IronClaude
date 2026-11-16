# Pre-pass timing, IMPLEMENTATION step 9 checkpoint (2026-11-14)

No model was started. Each number is the wall-clock seconds of one whole `sweep prepass` command (Python start-up and `uv run` included), measured by `bin/time-prepass.sh`, three runs per snapshot, median shown. Raw lines: `results/prepass-timing.tsv`; the console output is `results/implement/logs/T23-checkpoint.log`. The repository root was only read (the output of `git status --porcelain` hashed the same before and after).

Candidate for the three S1 figures: `fixtures/plans/p_basic.md` with `fixtures/plans/source.md`, seed 1, panel `primary`.

## S1 (three snapshots)

| Snapshot | Tracked files in scope (DD-5) | Runs (s) | S1 (median, s) |
|---|---|---|---|
| Repository root (`REPO`, 38,062 tracked files) | 1,464 | 0.51, 0.63, 0.59 | **0.59** |
| Medium: `git archive HEAD` of `src tests docs scripts` and five root files, committed in `/tmp/prepass-timing-snaps/medium` (2,319 tracked files) | 1,444 | 0.44, 0.43, 0.42 | **0.43** |
| Small: the F-REPO fixture (26 tracked files) | 12 | 0.40, 0.41, 0.39 | **0.40** |

Kill limit: `min(15 s, 0.10 b)` is 10 s at the smallest `b` (100 s). S1 on the repository root is 0.59 s, so the checkpoint passes by a wide margin (the planning figure was 8 s). Nothing to revisit in DD-5 or DD-10.

## Scope string used (DD-5), as `prepass.json` records it for the repository root

`tracked files under tests/, scripts/, docs/; root-level files; change-log style files anywhere (names: changelog, changes, history, news, release-notes, releases); directories of plan-named paths: docs, src/exporter, tests, workflow-plan; same-basename mirrors of plan-named files: 1.2, guide.md, notice.py, report.py, retention.py, source.md, test_retention.py; excluded: .dev/, dependency folders (node_modules, vendor, bower_components, jspm_packages, .venv, venv, site-packages, .tox, .eggs, __pycache__) and ground-truth files; files in scope: 1464`

## Limits of these numbers

- `p_basic.md` names a few paths and produces few search patterns, and its named directory `src/exporter` does not exist in this repository, so the DD-5 scope here is the fixed part only (the same 1,464 files as step 0.3, which matches).
- One supplementary run, not one of the three S1 figures: a real 483-line plan (this build's own plan file, read only, no source) as the candidate on the repository root, three runs: 0.97, 0.95, 0.95 s (median 0.95 s). Its path tokens name about 50 directories, so the scope is wider than the fixture's. S1 for a real plan is therefore about 1 s on this host, still about a tenth of the kill limit.
- The 12-lookup one-class attach of DD-10 was not isolated; the plans used did not force a one-class sheet. The sheet-selection constants are unchanged.
- One host, warm file cache. A cold cache or a slower disk will cost more; the 10 s limit leaves a factor of about 10 over the 0.95 s figure.
- `config/values.json`: `prepass_s` is now 0.59 (repository root, `p_basic.md`); the planning 8 is kept as `prepass_s_planning`; all three figures are in `prepass_measured`.
