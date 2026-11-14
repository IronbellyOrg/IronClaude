# R2 Idle-Shift Sweeper harness: operator quick start

Design: `DESIGN.md`. What was built and what is not met: `IMPLEMENTATION.md`.

All commands run from the repository root (`REPO`). Every command that starts reviewer, sweeper or judge sessions is
wrapped in the shared gateway lock.

## 1. Tests (no model calls)

```bash
uv run pytest .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r2-idle-shift-sweeper/tests -q
```

## 2. Gate 0 spikes

```bash
R2=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r2-idle-shift-sweeper
bash $R2/spikes/h3-base-check.sh                                  # no model
uv run --no-project python -I $R2/py/audits.py catalogue          # no model (R-07)
flock /tmp/collab-gateway.lock bash $R2/spikes/s0-hooks.sh
flock /tmp/collab-gateway.lock bash $R2/spikes/s2-resume.sh
flock /tmp/collab-gateway.lock bash $R2/spikes/sw1-sweeper.sh
flock /tmp/collab-gateway.lock bash $R2/spikes/reqs3-actrate.sh
flock /tmp/collab-gateway.lock bash $R2/spikes/spike4-values.sh EL2   # then SL2, HL2: 4 A1 runs x 3 packages each
flock /tmp/collab-gateway.lock bash $R2/spikes/s3-smoke.sh            # the one-package smoke test (6 rows)
```

Each spike appends one PASS/FAIL line to `spikes/RESULTS.md`; evidence is under `spikes/out/<spike>/`.

## 3. One panel on the three packages

Spike 4 must have written `config/values/<panel>/<pkg>.json` and re-pinned `config/manifest.json` first; without them
the launcher refuses (use `--planning-values` only for smoke rows, which are stamped `planning` and never counted).

```bash
flock /tmp/collab-gateway.lock env NOFALLBACK=1 PANEL_COLLAB=1 bash $R2/bin/launch-panel.sh --panel EL2 --row f4-el2-r1
flock /tmp/collab-gateway.lock env NOFALLBACK=1 PANEL_COLLAB=0 bash $R2/bin/launch-panel.sh --panel EL2 --row a1-el2-r1
```

Outputs: `runs/<row>/<pkg>/` (reviews, board copy, `collab.json`, merge, audit), `scoring/<opaque>/` (judge inputs and
`score.json`), `results/<row>.json`. A re-run with the same `--row` resumes; nothing is deleted.

## 4. Arm summary

```bash
uv run --no-project python -I $R2/py/summarize_arm.py --rows $R2/results/f4-el2-r*.json \
  --baseline-rows $R2/results/a1-el2-r*.json --out $R2/results/arm-f4-el2.json
```
