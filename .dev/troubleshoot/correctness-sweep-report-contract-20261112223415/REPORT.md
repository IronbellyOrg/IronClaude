# Troubleshoot report: two verified review findings on PR 539

- Caller: sc:pr-submit (diagnosis only; pr-submit applies the edits)
- Tier reached: 1, in a reduced run (see "Run limits")
- Findings: codex models.py:24 (relative report folder never matches), codex report.py:694 (report_path escaped in JSON)
- Verdicts source: `.dev/pr-monitor/pr-539-20261112222302/wave3/verdicts.md` (independent read-only validator)

## Diagnosis

### 1. models.py:24 `REPORT_DIR_RE` (verified)
Root cause: one regex, `models.py:22-24`, anchors the folder on a leading `/`. Both consumers use it:
`probes.py:995-996` (`_contract_candidates`, which decides which contract files `_read_contracts` opens) and
`classify.py:566` (`_contract_for`, which attaches a read contract to its row). A relative folder, which is the
documented WC-16 form (`--report-dir .dev/tdd/auth-1/` in `src/superclaude/core/WORKER-CONTRACT.md`), never
matches, so the contract is never read and a worker that wrote it is classified without it.
Neither consumer resolves a relative folder because neither knows the worker's worktree: it is
`OrcaObservation.worktree_path` (`probes.py:455`, from `terminal.worktreePath`).

Fix: one shared helper in `models.py` (where the regex already lives so the two cannot drift) that returns the
absolute folders a text names, resolving a relative one against `worktree_path`; both consumers call it.
A relative folder with no worktree path names nothing. The existing `_inside(candidate, allowed)` check at
`probes.py:1304` still bounds what is read, so a `..` folder cannot read outside the sweep roots.

### 2. report.py:694 `to_json` (verified)
Root cause: `"report_path": sanitize(report_path)`. `sanitize` (`report.py:569-599`) is Markdown/terminal
escaping (backslash, pipe, angle brackets, `[`, `]`). `json.dumps` already escapes for JSON, and the field is
a filesystem path that `sc-sweep-protocol` step 3 passes to Read. `/tmp/project[1]/x.md` becomes
`/tmp/project\[1\]/x.md`, which does not exist.
Fix: emit the real path. `sanitize` stays for every human-facing string.

## Report-only
Augment `probes.py:1047` (non-object worker entries, hasMore): unverified, see verdicts.md; no edit.

## Exact edits
1. `src/superclaude/cli/sweep/models.py`: add `import os`; keep `REPORT_DIR_RE` but accept a relative folder
   (`([^\s'\"`]+)`); add `report_folders(text, worktree)` after it.
2. `src/superclaude/cli/sweep/probes.py`: import `report_folders` in place of `REPORT_DIR_RE`;
   `_contract_candidates` loops `report_folders(text, obs.worktree_path)`.
3. `src/superclaude/cli/sweep/classify.py`: import `report_folders` in place of `REPORT_DIR_RE`;
   `_contract_for` builds `folders` from `report_folders(t, orca.worktree_path)`.
4. `src/superclaude/cli/sweep/report.py:694`: `"report_path": report_path,`.

## Tests to add (tests/sweep)
- `test_report.py`: `to_json` keeps `/tmp/project[1]/a|b.md` unchanged in `report_path`.
- `test_probes_allowlist.py`: `_contract_candidates` returns the worktree-resolved contract for a relative
  `--report-dir` and nothing for a relative folder with no worktree path.
- `test_classify.py`: `_contract_for` picks the contract in a relative `--report-dir` when two contracts sit
  under one worktree (the worktree fallback cannot choose between them).

## Run limits (disclosed)
This run did not execute the full tiered pipeline (documentation grounding, diagnosability audit, calibrator,
evidence-validator, adversarial debate). Both findings had already been checked by an independent read-only
validator against the real code, the fixes are a few lines each, and the caller applies and tests them itself.
Confidence is therefore not calibrated by the calibrator agent; the tests above are the real check.
Out of scope, noted only: the relative `--report-path` / contract-path form in the same WC-16 example is
not matched by `_CONTRACT_PATH_RE` (`probes.py:984`); the folder form covers the worked example.
