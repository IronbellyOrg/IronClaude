# Anchor confirmation — D1 edit sites (re-grepped 2026-06-24, current tree)

All anchors verified against live source by Read/Grep. No drift from research/01-d1-d4-evidence.md.

## D1 — reviewer_isolation assignment sites (THREE — all confirmed)

| # | Site | Line | Exact matched line | Role |
|---|------|------|--------------------|------|
| 1 | `src/superclaude/cli/reflect/ensemble.py` | 315-316 | `reviewer_isolation=(` / `"snapshot" if config.reviewer_grounding_root else "disabled"` | Contract telemetry branch (build_reflect_contract input) |
| 2 | `src/superclaude/cli/reflect/runner.py` | 518 | `reviewer_isolation="stopped-precondition",` | STOP-path result (not a design-(b) edit site) |
| 3 | `src/superclaude/cli/reflect/runner.py` | 682 | `result.reviewer_isolation = "snapshot"` (inside `if snapshot_path is not None:`) | **Operator-visible `ReflectResult` write persisted to `reflect_post` — design (b) MUST edit this** |

Other references (read-only context): `ensemble.py:500` (`build_reflect_contract` param default), `ensemble.py:562` (contract dict key), `runner.py:229` (sidecar dict key).

## D1 — swarm-worker target sites (design (a) edit sites)

| Site | Line | Exact | Role |
|------|------|-------|------|
| `ensemble.py` recipe `target` | 218 | `"target": str(config.tasklist_path),` | normalize_wave2 recipe target — LIVE path |
| `ensemble.py` `_load_review_target()` | 433-441 | reads `Path(config.tasklist_path).read_text()` at :441; header `Tasklist: {config.tasklist_path}` at :438 | swarm-worker review-target source — LIVE path |
| `ensemble.py` `build_worker_prompt()` | 415 | builds worker prompt | worker prompt builder |

NOTE: `config.tasklist_path` is absolute-resolved (`Path(tasklist_path).resolve()` in config.py) → design (a) requires REBASING onto the snapshot root, not a naive join.

## D1 — enum value set (models.py)

`src/superclaude/cli/reflect/models.py`:
- `:139-140` doc comment: `reviewer_isolation: "disabled" (flag off) | "snapshot" (grounded in a snapshot) | "stopped-precondition" (gate STOPped before launch)`
- `:141` `reviewer_isolation: str = "disabled"` (ReflectResult default)
- `ReflectConfig.reviewer_grounding_root: Path | None = None` (`:~105`)

Current accepted values: **`disabled | snapshot | stopped-precondition`** (design (b) adds `snapshot-children-only`).

## ClaudeProcess children that ARE correctly snapshot-grounded (read-only confirmation)

- Tier-1 audit child: `runner.py:441-461` `cwd=config.reviewer_grounding_root` ✓
- Adversarial scorer: `ensemble.py:366` `cwd=config.reviewer_grounding_root` ✓

These are the two children whose grounding is real; the swarm workers (above) are the gap.

## Baseline test state

143 passed, 1 xpassed (see `../test-results/baseline-summary.md`). `test_reviewer_swarm_target_grounding.py` does not yet exist.
