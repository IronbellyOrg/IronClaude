# AC-14 evidence

- `before.sha256` (taken 2026-11-13T21:30:28Z) and `after.sha256` (taken 2026-11-13T21:47:49Z): sha256 of every file under `REPO/src` and `EVAL` (`find -type f`, ignored files included, `__pycache__` excluded), 13,243 files each.
- Between the two: the three sandboxes were rebuilt from scratch (`bin/build-sandbox.sh` through `spikes/g0-h3/run.sh`), the full test suite ran (`spikes/test-run.log`, 89 passed), and one smoke run ran on real models (`runs/el2-c1-20261113T214437Z-42fb`, exit 0).
- `cmp before.sha256 after.sha256`: identical.
- Every Python step ran with `PYTHONDONTWRITEBYTECODE=1`.
