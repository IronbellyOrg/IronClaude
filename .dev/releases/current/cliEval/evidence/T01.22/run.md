# T01.22 evidence — execution log

Date: 2026-05-20
Task: T01.22 — Implement FR-CLI3 `eval describe` subcommand
Deliverable: D-0019

## Commands

```
$ uv run pytest tests/cli/eval/test_describe.py -v
============================== 25 passed in 0.33s ==============================

$ uv run pytest tests/cli/eval/ -q
============================= 299 passed in 0.81s ==============================
```

Full eval suite expanded 274 → 299 passing (25 new `test_describe.py`
cases). No prior tests regressed.

## CLI smoke

```
$ cp tests/cli/eval/fixtures/valid_suite.yaml /tmp/reference.yaml

$ uv run superclaude eval describe --suite reference --suites-dir /tmp
name: reference
version: '1.0'
description: Reference v1 manifest exercising every DM-011 field including parameterize.
defaults:
  per_eval_timeout_sec: 120
  ...
evals:
- id: E1
  ...
- id: E2.1     ← post-parameterize expansion
- id: E2.2
- id: E2.3
$ echo $?
0

$ uv run superclaude eval describe --suite reference --eval E1 --suites-dir /tmp
id: E1
title: auggie-first sticky lifecycle — set then clear
category: hook-lifecycle
...
$ echo $?
0

$ uv run superclaude eval describe --suite ghost --suites-dir /tmp
eval describe: SuiteNotFound: no manifest matched --suite 'ghost' in /tmp
$ echo $?
2
```

## AC mapping → tests

Detailed AC → test mapping is in `artifacts/D-0019/evidence.md`.

## Implementation surface

New code in `src/superclaude/cli/eval/commands.py`:

- Click handler: `eval_describe` (registered on `eval_group`).
- Function API: `describe_suite`, `resolve_suite_manifest`,
  `_evalspec_to_dict`, `_parsed_suite_to_dict`,
  `render_describe_yaml`, `render_describe_json`.
- Typed errors: `SuiteNotFound`, `EvalNotFound`.
- Exit-code constants: `SUITE_NOT_FOUND_EXIT_CODE`,
  `EVAL_NOT_FOUND_EXIT_CODE` (both `2`).

New tests: `tests/cli/eval/test_describe.py` (25 cases).

New artifacts: `artifacts/D-0019/{spec,notes,evidence}.md`.
