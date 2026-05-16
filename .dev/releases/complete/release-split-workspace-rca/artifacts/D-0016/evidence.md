# D-0016 — Evidence: AC5 script runs against relocated workspace

All commands executed from repo root `/config/workspace/IronClaude/` on `2026-05-13`. `<agg>` and `<gen>` abbreviate the absolute plugin paths from `spec.md`.

## 0. Baseline integrity check (byte-identical benchmark across legacy / relocated)

```text
$ git show 6c84826:.claude/skills/sc-release-split-protocol-workspace/iteration-1/benchmark.json | sha256sum
9608eca3fa178eb65f48666b05410eaa97910e76defa3eaf51ca90c2b5fc5a22  -

$ sha256sum .dev/eval-workspaces/sc-release-split-protocol/iteration-1/benchmark.json
9608eca3fa178eb65f48666b05410eaa97910e76defa3eaf51ca90c2b5fc5a22  .dev/eval-workspaces/sc-release-split-protocol/iteration-1/benchmark.json
```

The relocation commit `86d2749` shows `benchmark.json` and `eval-review.html` both with `… | 0` lines in `git show --stat` (rename, no content change).

## 1. `aggregate_benchmark.py` — task-literal form (parent workspace path)

Command:

```bash
uv run python <agg> .dev/eval-workspaces/sc-release-split-protocol/ \
    --output .dev/releases/current/release-split-workspace-rca/artifacts/D-0016/agg-parent.benchmark.json
```

Result: **exit 0**.

stdout (`agg-parent.stdout.txt`):

```
No eval directories found in .dev/eval-workspaces/sc-release-split-protocol or .dev/eval-workspaces/sc-release-split-protocol/runs
Generated: .dev/releases/current/release-split-workspace-rca/artifacts/D-0016/agg-parent.benchmark.json
Generated: .dev/releases/current/release-split-workspace-rca/artifacts/D-0016/agg-parent.benchmark.md

Summary:
  Delta:         +0.00
```

stderr (`agg-parent.stderr.txt`): only the harmless `uv` venv-mismatch warning.

Generated `agg-parent.benchmark.json` schema (truncated):

```json
{
  "metadata": {
    "skill_name": "<skill-name>",
    "skill_path": "<path/to/skill>",
    "executor_model": "<model-name>",
    "analyzer_model": "<model-name>",
    "timestamp": "2026-05-13T05:12:00Z",
    "evals_run": [],
    "runs_per_configuration": 3
  },
  "runs": [],
  "run_summary": { "delta": { "pass_rate": "+0.00", "time_seconds": "+0.0", "tokens": "+0" } },
  "notes": []
}
```

**Interpretation:** the script exits 0 with a schema-valid (but empty `runs[]` / empty `evals_run`) artifact, because the workspace layout does not match the script's required `eval-N/` directory pattern. See `notes.md` §Layout for the script-vs-workspace contract gap; this gap is **pre-existing** (predates relocation — same workspace structure existed at the legacy path) and is not a regression.

## 2. `aggregate_benchmark.py` — probe at the actual runs subdirectory

Command:

```bash
uv run python <agg> .dev/eval-workspaces/sc-release-split-protocol/iteration-1/ \
    --output .dev/releases/current/release-split-workspace-rca/artifacts/D-0016/agg-iter1.benchmark.json
```

Result: **exit 1** (pre-existing script bug, see notes.md §Pre-existing-bug-1).

stderr (`agg-iter1.stderr.txt`):

```
Traceback (most recent call last):
  …
  File ".../aggregate_benchmark.py", line 101, in load_run_results
    for config_dir in sorted(eval_dir.iterdir()):
  File ".../pathlib.py", line 1056, in iterdir
    for name in os.listdir(self):
NotADirectoryError: [Errno 20] Not a directory: '.dev/eval-workspaces/sc-release-split-protocol/iteration-1/eval-review.html'
```

The script's `glob('eval-*')` matched `eval-review.html` (a file) and then attempted `iterdir()` on it. This bug exists in upstream `skill-creator` and is independent of the relocation — it would manifest identically against the legacy path.

## 3. `generate_review.py` — task-literal form (parent workspace path, `--static` to avoid serving)

Command:

```bash
uv run python <gen> .dev/eval-workspaces/sc-release-split-protocol/ \
    --static .dev/releases/current/release-split-workspace-rca/artifacts/D-0016/gen-review-parent.html
```

Result: **exit 1** (pre-existing script bug, see notes.md §Pre-existing-bug-2).

stderr (`gen-parent.stderr.txt`):

```
Traceback (most recent call last):
  …
  File ".../generate_review.py", line 64, in find_runs
    runs.sort(key=lambda r: (r.get("eval_id", float("inf")), r["id"]))
TypeError: '<' not supported between instances of 'int' and 'NoneType'
```

The sort key produces `(int, …)` for runs whose `eval_metadata.json` resolves a numeric `eval_id`, and `(None, …)` for runs without one — `<` then fails between the heterogeneous first elements. Pre-existing upstream bug; would manifest identically at the legacy path.

## 4. `generate_review.py` — probe at the actual runs subdirectory

Command:

```bash
uv run python <gen> .dev/eval-workspaces/sc-release-split-protocol/iteration-1/ \
    --static .dev/releases/current/release-split-workspace-rca/artifacts/D-0016/gen-review-iter1.html \
    --benchmark .dev/eval-workspaces/sc-release-split-protocol/iteration-1/benchmark.json
```

Result: **exit 0**.

stdout (`gen-iter1.stdout.txt`):

```
  Static viewer written to: .dev/releases/current/release-split-workspace-rca/artifacts/D-0016/gen-review-iter1.html
```

Output size: `gen-review-iter1.html` = 367 398 bytes (self-contained, embeds all run outputs + benchmark tab).

## Files captured

```
artifacts/D-0016/
├── agg-parent.stdout.txt      (370 bytes)  — task-literal aggregate run, exit 0
├── agg-parent.stderr.txt      (160 bytes)
├── agg-parent.benchmark.json  (417 bytes)  — schema-valid, empty runs[]
├── agg-parent.benchmark.md    (358 bytes)
├── agg-iter1.stdout.txt       (0 bytes)    — probe aggregate run, exit 1 (pre-existing bug)
├── agg-iter1.stderr.txt       (1 572 bytes)
├── gen-parent.stdout.txt      (0 bytes)    — task-literal review run, exit 1 (pre-existing bug)
├── gen-parent.stderr.txt      (909 bytes)
├── gen-iter1.stdout.txt       (119 bytes)  — probe review run, exit 0
├── gen-iter1.stderr.txt       (160 bytes)
└── gen-review-iter1.html      (367 398 bytes) — self-contained eval viewer
```
