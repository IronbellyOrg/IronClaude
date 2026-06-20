# QA Report — Synthesis/Diff Validation (flag-completeness lens)

**Topic:** WS-0 bare-review CLI migration — `swarm run` flag completeness (B-1..B-4)
**Date:** 2026-06-16
**Phase:** report-validation (WS-0 diff structural verification)
**Lens:** CLI flag completeness/correctness
**Fix authorization:** false (REPORT ONLY)

---

## Overall Verdict: PASS

All FOUR flags (`--reviewers`, `--target-line-cap`, `--timeout-sec`, `--label`) exist as
optional Click options on `run_cmd`, carry the correct defaults, apply to the correct
`spec_dict` fields per R2 B-1..B-4, and have matching signature params + decorators. The
critical `--reviewers 4` survival path is proven both by code trace and by a live passing
e2e test. Every cross-file claim the diff makes (preflight call chain, recipe `caller_label`
read, dispatch kwargs, schema field names) was independently verified against source.

No CRITICAL or IMPORTANT defects found. Two MINOR observations (test-coverage gaps + an
untested lower-bound) are recorded; neither is a flag defect.

---

## Verification Points (the 5 required checks)

### Point 1 — All FOUR flags exist as Click options on `run_cmd`: VERIFIED

| Flag | Option decorator | Click param | Evidence (file:line, read directly) |
|---|---|---|---|
| `--reviewers` | `@click.option` | `reviewers` | commands.py:1385-1397 |
| `--target-line-cap` | `@click.option` | `target_line_cap` | commands.py:1398-1409 |
| `--timeout-sec` | `@click.option` | `timeout_sec` | commands.py:1410-1421 |
| `--label` | `@click.option` | `label` | commands.py:1422-1433 |

All four sit in the decorator stack immediately before `--force-relens` (commands.py:1434)
and `--detached` (commands.py:1452), inside the `run_cmd` decorator chain that terminates at
`@auto_inject_guard_option` (commands.py:1470) + `def run_cmd` (commands.py:1471).

### Point 2 — Each is OPTIONAL with the correct default: VERIFIED

- `--reviewers`: `type=int, default=None` (commands.py:1388-1389). Lens default 3 preserved on
  omission (the override block at commands.py:1637 is guarded by `if reviewers is not None`).
  Range [2,4] enforced; out-of-range raises `EXIT_USAGE` — see Point 5.
- `--target-line-cap`: `type=int, default=None` (commands.py:1401-1402). Lens default 4000
  preserved on omission (override guarded `if target_line_cap is not None`, commands.py:1659).
- `--timeout-sec`: `type=int, default=None` (commands.py:1413-1414). 180 preserved on omission
  (override guarded `if timeout_sec is not None`, commands.py:1670). Lens spec hardcodes
  `timeout_sec: 180` at commands.py:789 — confirmed.
- `--label`: `type=str, default=None` (commands.py:1425-1426). Empty/None preserved on omission
  (override guarded `if label is not None`, commands.py:1681).

`default=None` is the correct sentinel for "omitted" so the lens-default-preservation logic
(only mutate `spec_dict` when the value is non-None) is sound for all four.

### Point 3 — Each applies to the correct spec_dict field per R2 B-1..B-4: VERIFIED

- **B-1 `--reviewers`** → `workers.count = reviewers` (commands.py:1646) AND resizes
  `workers.models` to N placeholder slots (commands.py:1647-1649). The resize is load-bearing:
  the inline `run_preflight` call passes no `pool=` (commands.py:1688-1692), so the INV-005
  guard uses `pool_seq = list(job.workers.models)` (preflight.py:1808). Under the default
  `pool_policy="warn"` the guard CLAMPS `workers.count` down to `len(pool_seq)` when count
  exceeds the pool (preflight.py:1817-1828) rather than failing — so without resizing models to
  N, a `--reviewers 4` would be silently clamped back to 3 (lens default pool size). Resizing
  models to N entries makes `workers_exceed_pool(N, [N models])` False → no clamp. The
  placeholder pattern `lens-default-model-{i}` (commands.py:1648) mirrors the lens-spec builder
  exactly (commands.py:786). **Correct.**
- **B-2 `--target-line-cap`** → `target.truncation.line_cap` (commands.py:1660-1662). Field path
  matches the real `TruncationSpec.line_cap` (models.py:213). **Correct.**
- **B-3 `--timeout-sec`** → `workers.timeout_sec` (commands.py:1671) and threaded into dispatch
  via `worker_spec=inline_job.workers` (commands.py within the B-5 dispatch call). `WorkerSpec`
  is a real dataclass (models.py:156) and `dispatch_wave1` accepts `worker_spec` (dispatch.py:341).
  **Correct.**
- **B-4 `--label`** → `caller.invocation_label` (commands.py:1682) AND
  `normalization.recipe_args.caller_label` (commands.py:1683-1685). `CallerSpec.invocation_label`
  is a real field (models.py:1598). The recipe reads `args.get("caller_label", "")` at
  bare_review_v1.py:255 — exactly the field the diff stamps. `normalize_wave2` accepts and
  forwards `recipe_args` (normalize.py:504). The full chain (CLI flag → spec → recipe_args →
  recipe stamp) is structurally complete. **Correct.**

### Point 4 — run_cmd signature has the 4 params + decorators present: VERIFIED

Signature params at commands.py:1479-1482 — `reviewers: Optional[int]`,
`target_line_cap: Optional[int]`, `timeout_sec: Optional[int]`, `label: Optional[str]` — in the
correct order matching the decorator stack (reviewers→target_line_cap→timeout_sec→label, placed
after `transport_kind` and before `force_relens`). Decorators present at commands.py:1385-1433.
Type annotations match the Click `type=` declarations. **Correct.**

### Point 5 — [2,4] clamp matches legacy AC-1.4; `--reviewers 4` survives: VERIFIED

- Range check: `if reviewers < 2 or reviewers > 4` → `click.echo(... err=True)` +
  `raise click.exceptions.Exit(EXIT_USAGE)` (commands.py:1638-1644). `EXIT_USAGE = 2`
  (commands.py:190). This matches legacy `t2_preflight.sh` AC-1.4 `[2,4]` (research §1, line 67).
- `expand_lens_defaults` `count == 4` reset confirmed at preflight.py:523 (`if spec.workers.count
  <= 0 or spec.workers.count == 4:` → resets to `lens_entry.default_workers`), and the line_cap
  `== 4000` reset at preflight.py:527 — both live ONLY inside `expand_lens_defaults`.
- **Production-call-site verification (the key claim):** `expand_lens_defaults` has NO production
  call site. Grep over `src/superclaude/` (excluding tests) shows the symbol appears only in its
  own definition (preflight.py:424), its `__all__` export (preflight.py:2010), and docstring
  cross-references — never as a call. The inline path calls `run_preflight`, which calls
  `materialize_lens_defaults` (preflight.py:1735), NOT `expand_lens_defaults`.
  `materialize_lens_defaults` (preflight.py:324-335) only snapshots `ResolvedLensEntry.from_lens`
  and does NOT touch `count` or `line_cap`. The only callers of `expand_lens_defaults` are in
  `tests/swarm/test_lens_defaults.py` (test-only). **The diff comment's claim is accurate.**
- **Live proof:** `tests/swarm/test_e2e_user_guide.py::test_reviewers_flag_overrides_worker_count`
  (line 230) passes `--reviewers 4` and asserts `"workers=4, results=4"` (line 240) AND
  `manifest["preflight"]["workers_requested"] == 4` (line 242).
  `test_reviewers_flag_rejects_out_of_range` (line 245) passes `--reviewers 5` and asserts
  `EXIT_USAGE` (line 253). Both PASS (ran `uv run pytest -k 'reviewers or quickstart'` →
  5 passed). **`--reviewers 4` genuinely survives.**

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Four flags exist as Click options | PASS | commands.py:1385,1398,1410,1422 (read) |
| 2 | Optional + correct defaults (None sentinel; 3/4000/180/None) | PASS | commands.py:1388-1426; lens default 180 at :789 |
| 3 | Correct spec_dict field per B-1..B-4 | PASS | :1646-1649, :1660-1662, :1671, :1682-1685; field names cross-checked in models.py/normalize.py/bare_review_v1.py |
| 4 | run_cmd signature params + decorators | PASS | commands.py:1479-1482 (params), :1385-1433 (decorators) |
| 5 | [2,4] clamp = AC-1.4; `--reviewers 4` survives; expand_lens_defaults no prod call site | PASS | commands.py:1638-1644, EXIT_USAGE=2 at :190; preflight.py:523/527/1735/324; grep prod call sites = none; e2e test green |

## Summary
- Checks passed: 5 / 5
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 2 (test-coverage observations, not flag defects)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR | tests/swarm/ (absent) | No dedicated CLI test exercises `--target-line-cap`, `--timeout-sec`, or `--label`. All matching grep hits are spec-file/lens-default fixtures; none drive these CLI flags through `run_cmd`. The flags are correctly wired (verified by code trace), but B-2/B-3/B-4 have no behavioral regression guard, unlike B-1 which has two e2e tests. | Add e2e tests asserting `--target-line-cap N` lands in `target.truncation.line_cap`, `--timeout-sec N` reaches dispatch, and `--label X` appears in per-reviewer frontmatter (read the emitted `.final.md`). |
| 2 | MINOR | commands.py:1638 / tests/swarm/test_e2e_user_guide.py:245 | Out-of-range rejection is tested only for the UPPER bound (`--reviewers 5`). The LOWER bound (`--reviewers 1`, and `0`/negative) is rejected by the same `reviewers < 2` predicate but is not asserted by any test. The predicate itself is correct (verified at commands.py:1638). | Add `--reviewers 1` (and optionally `0`) case to `test_reviewers_flag_rejects_out_of_range` asserting `EXIT_USAGE`. |

## Actions Taken
None — `fix_authorization: false` (report-only). Both findings are MINOR test-coverage
observations; the flag surface under review is correct and complete.

## Confidence
**Verified:** 5/5 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence:** 100.0%
**Tool engagement:** Read: 4 | Grep: 6 | Glob: 0 | Bash: 7 (includes 1 live pytest run)

All five verification points were checked with direct source reads + grep cross-checks +
one runtime test execution. Every claim in this report cites a line read directly from
`src/superclaude/cli/swarm/commands.py` or a cross-referenced source file
(preflight.py, models.py, normalize.py, recipes/bare_review_v1.py, test_e2e_user_guide.py).
No external/web lookups were required (claims are all intrinsically local).

## QA Complete
