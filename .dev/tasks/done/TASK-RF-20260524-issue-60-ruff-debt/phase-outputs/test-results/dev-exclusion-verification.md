# `.dev/` Exclusion Verification

**Timestamp:** 2026-05-25 03:27
**Step:** Phase 2.2

## Result

| Metric | Value |
|--------|-------|
| Pre-exclusion count (Phase 1.4) | 441 |
| Post-exclusion count (this step) | 227 |
| Difference (errors removed by .dev/ exclusion) | 214 |
| Predicted reduction (from baseline summary) | 214 (182 releases + 29 eval-workspaces + 3 research) |
| `.dev/` errors in post-exclusion output | 0 |
| Verdict | **PASS** — exclusion took effect; reduction matches prediction exactly |

## Trailing Lines (Verbatim)

```
Found 227 errors.
[*] 61 fixable with the --fix option (108 hidden fixes can be enabled with the --unsafe-fixes option).
```

## Confirmation Commands

```bash
uv run ruff check . --output-format=concise > ruff-after-dev-exclusion.txt
uv run ruff check . 2>&1 | tail -3 >> ruff-after-dev-exclusion.txt
grep -c '^\.dev/' ruff-after-dev-exclusion.txt    # output: 0
```
