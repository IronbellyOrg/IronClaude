---
needs_human_decision: true
status: RESOLVED
---

# D1 Design Decision — L2 swarm-worker grounding gap + telemetry overclaim

**This is a `needs_human_decision` HALT.** The executor MUST NOT auto-pick. Phase 3 (implementation) is blocked until a human records an explicit `Chosen design: a` or `Chosen design: b` and flips `status` to `RESOLVED`. Recording the research recommendation below does NOT authorize adoption.

## The gap (from the /sc:reflect audit, D1)

`SKILL.md` Step 0.5e item 4 (gold-standard spec, authored by the parent task) states the text-in/out Tier-2 swarm workers "receive review targets derived from `<snapshot>`." But with `--isolate-reviewers` ON, only the two `ClaudeProcess` children are actually snapshot-grounded:
- Tier-1 audit child — `runner.py:441-461` `cwd=config.reviewer_grounding_root` ✓
- Adversarial scorer — `ensemble.py:366` `cwd=config.reviewer_grounding_root` ✓

The swarm-worker review target is the LIVE path, and the telemetry overclaims:
- `ensemble.py:218` `"target": str(config.tasklist_path)` (live)
- `ensemble.py:433-441` `_load_review_target()` reads `config.tasklist_path` (live)
- `ensemble.py:315-316` reports `reviewer_isolation == "snapshot"` purely from non-null `reviewer_grounding_root`
- `runner.py:682` `result.reviewer_isolation = "snapshot"` — the operator-visible `ReflectResult` value persisted to `reflect_post`

Bounded by default-OFF (opt-in). The mutation incident vector stays closed by L1 (read-only allowlist) + L1b (restricted profile) regardless — this is a read-isolation completeness gap + telemetry overclaim, NOT a reopened incident.

## Three-site classification (verbatim)

LIVE-path sourced (the gap):
1. Swarm-worker recipe `target` — `ensemble.py:218`
2. `_load_review_target()` — `ensemble.py:433-441`
3. `build_worker_prompt()` — `ensemble.py:415` (consumes the live target source)

Genuinely snapshot-`cwd`-grounded (correct):
- Tier-1 audit child — `runner.py:441-461`
- Adversarial scorer — `ensemble.py:366`

## Design (a) — Full grounding redirect

Make the swarm-worker review target resolve under `config.reviewer_grounding_root` when set (fall back to `config.tasklist_path` when grounding is disabled), so the workers actually read the snapshot. Closes the Step 0.5e item-4 guarantee fully.

**Edit sites:** `ensemble.py` recipe `target` (`:218`), `_load_review_target()` (`:433-441`), `build_worker_prompt()` (`:415`).
**Caveat:** `config.tasklist_path` is absolute-resolved → requires REBASING the tasklist path onto the snapshot root (compute path relative to repo/worktree root, then join under `reviewer_grounding_root`), NOT a naive `grounding_root / tasklist_path` join. The falsifier asserts the rebased target resolves under `reviewer_grounding_root`.
**Blast radius:** LARGER — touches worker-target plumbing; behavioral change to what the workers read under isolation.

## Design (b) — Telemetry-honesty narrowing

Keep children-only grounding; stop overclaiming. Add a `reviewer_isolation` value `"snapshot-children-only"` reported when the ClaudeProcess children are snapshot-grounded but the swarm workers are not. Makes the contract truthful without changing what the workers read.

**Edit sites:**
- `models.py` doc comment for `ReflectResult`/`ReflectConfig` `reviewer_isolation` (`:139-141`) — add `snapshot-children-only` to the enumerated value list.
- `ensemble.py:315-316` contract-telemetry branch — emit `"snapshot-children-only"` (not `"snapshot"`) when `reviewer_grounding_root` is set.
- **`runner.py:682`** `result.reviewer_isolation = "snapshot"` → `"snapshot-children-only"` — REQUIRED: this is the operator-visible `ReflectResult` value; without it the design-(b) falsifier (asserting `ReflectResult.reviewer_isolation == "snapshot-children-only"`) has no source and the fix is a no-op.
- `tests/cli/reflect/test_reviewer_isolation_gate.py:84` — sanctioned correctness update of the existing assertion from `"snapshot"` to `"snapshot-children-only"` (an edit to a pre-existing telemetry assertion; NOT a new falsifier, NOT EXEMPT-labeled).
- `SKILL.md` Step 0.5e item 4 — rewrite to honestly state the swarm-worker scope (only the ClaudeProcess children are snapshot-`cwd`-grounded; the text-in/out workers receive their target from the live path, reflected by `reviewer_isolation: "snapshot-children-only"`). Requires `make sync-dev` + `make verify-sync`.
**Blast radius:** SMALLER — telemetry + doc only; no change to what the workers read.

## Research recommendation (NON-BINDING — does NOT authorize adoption)

Design **(b)** is recommended as the smaller-blast-radius, honest-contract option: the swarm workers are text-in/out and the mutation incident vector is already closed by L1+L1b, so the practical risk of the workers reading the live tree under isolation is low, and an honest telemetry value is the proportionate fix. Design (a) is the fuller fix if read-isolation for swarm workers is a hard requirement.

**Recording this recommendation does NOT authorize the executor to adopt it. Only an explicit operator choice below authorizes Phase 3.**

## OPERATOR DECISION

```
Chosen design: b      # Telemetry-honesty narrowing
Decided by: operator (via AskUserQuestion during /task execution)
Decided at: 2026-06-24
```

**DECISION RECORDED: design (b). Phase 3 is AUTHORIZED.** Implement the telemetry-honesty narrowing: add `"snapshot-children-only"` to the `reviewer_isolation` enum (models.py), emit it at both telemetry sites (`ensemble.py:315-316` + `runner.py:682`), update the existing `test_reviewer_isolation_gate.py:84` assertion, and rewrite SKILL.md Step 0.5e item 4 honestly (with sync). The swarm workers continue to read the live path (behavior unchanged); only the telemetry stops overclaiming.

(Top `status` set to `RESOLVED`. Note: the line/anchor numbers above — `ensemble.py:315-316`, `runner.py:682` — are the PRE-edit anchors the operator decided against; after the multi-line→single-line ternary edit + added comments the live emit lines are `ensemble.py:319` and `runner.py:686`. The edits landed and are verified in `d1-verify.md` / `anchor-confirmation.md`.)
