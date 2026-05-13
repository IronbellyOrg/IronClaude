# D-0016 — AC5: aggregate_benchmark + generate_review against relocated workspace

**Task:** T05.05 (phase-5-tasklist.md)
**Acceptance criterion:** AC5 — eval scripts run against the relocated workspace (`.dev/eval-workspaces/sc-release-split-protocol/`) with no regression vs the legacy workspace location (`.claude/skills/sc-release-split-protocol-workspace/`, deleted by commit `86d2749`).

## Scripts under test

Both scripts are owned by the Anthropic `skill-creator` plugin and live outside the IronClaude repo (read-only marketplace install):

- `aggregate_benchmark.py` — `/config/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/aggregate_benchmark.py`
- `generate_review.py` — `/config/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/eval-viewer/generate_review.py`

Both accept a positional `<benchmark_dir>` / `<workspace>` path per their `argparse` definitions (matches merged-thesis §Acceptance).

## Invocations executed

1. `uv run python <agg> .dev/eval-workspaces/sc-release-split-protocol/ --output …/agg-parent.benchmark.json` (the literal task form for aggregate_benchmark)
2. `uv run python <agg> .dev/eval-workspaces/sc-release-split-protocol/iteration-1/ --output …/agg-iter1.benchmark.json` (probe at the actual runs subdirectory)
3. `uv run python <gen> .dev/eval-workspaces/sc-release-split-protocol/ --static …/gen-review-parent.html` (the literal task form for generate_review)
4. `uv run python <gen> .dev/eval-workspaces/sc-release-split-protocol/iteration-1/ --static …/gen-review-iter1.html --benchmark …/iteration-1/benchmark.json` (probe at the actual runs subdirectory)

`--static` is passed to `generate_review.py` so it writes standalone HTML and exits 0 rather than starting the HTTP server (the script's only non-server exit path).

## Baseline used for comparison

The on-disk `iteration-1/benchmark.json` is **byte-identical** to its legacy-location ancestor:

- legacy: `git show 6c84826:.claude/skills/sc-release-split-protocol-workspace/iteration-1/benchmark.json` → SHA-256 `9608eca3fa178eb65f48666b05410eaa97910e76defa3eaf51ca90c2b5fc5a22`
- relocated: `.dev/eval-workspaces/sc-release-split-protocol/iteration-1/benchmark.json` → SHA-256 `9608eca3fa178eb65f48666b05410eaa97910e76defa3eaf51ca90c2b5fc5a22`

Relocation commit `86d2749` is a `git mv`-equivalent move (`stat 0 / 0` per `git show --stat`); no benchmark or workspace content was altered. This gives a strict non-regression baseline: any script run that depends only on workspace contents (not absolute path) **must** produce identical output across legacy and relocated locations.

See `evidence.md` for full captured outputs and `notes.md` for the comparison + classification.
