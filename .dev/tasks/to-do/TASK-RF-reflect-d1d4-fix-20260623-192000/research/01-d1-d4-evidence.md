# Research: D1–D4 fix evidence + edit anchors

**Topic type:** File Inventory + Integration Points
**Scope:** reflect subsystem (ensemble.py, models.py, SKILL.md, reflect-reviewer.md, tests/cli/reflect/)
**Status:** Complete
**Date:** 2026-06-23
**Source:** /sc:reflect post-execution audit `.dev/reflect/post-reflect-reviewer-guard-20260623185200/REPORT.md` (all anchors re-grepped 2026-06-23, current)

---

## D1 — L2 swarm-worker snapshot grounding gap + telemetry overclaim (MEDIUM-HIGH, Drift)

**Authored spec (gold standard):** `src/superclaude/skills/sc-reflect-protocol/SKILL.md:268` (Step 0.5e item 4):
> "the text-in/out Tier-2 swarm workers hold NO repo CWD and instead receive review targets derived from `<snapshot>`."

**Implementation gap (CODE-VERIFIED):**
- `src/superclaude/cli/reflect/ensemble.py:218` — `"target": str(config.tasklist_path)` (the recipe target is the LIVE tasklist path).
- `src/superclaude/cli/reflect/ensemble.py:433-441` — `_load_review_target()` reads `config.tasklist_path` (`:438`, `:441`); never `reviewer_grounding_root`.
- `src/superclaude/cli/reflect/ensemble.py:415` — `build_worker_prompt()` builds the worker prompt from the same live source.
- `src/superclaude/cli/reflect/ensemble.py:315-316` — telemetry `"snapshot" if config.reviewer_grounding_root else "disabled"` reports full `snapshot` even though only the two ClaudeProcess children (Tier-1 audit child `runner.py:441-461`, adversarial scorer `ensemble.py:366`) are actually `cwd`-grounded in the snapshot.

**Result:** with `--isolate-reviewers` ON, the Tier-2 swarm workers' target is the live worktree path while `reviewer_isolation` reports `snapshot`. Bounded by default-OFF (opt-in). The mutation incident vector stays closed by L1 (read-only allowlist) + L1b (restricted profile) regardless — this is a read-isolation completeness + telemetry-honesty gap, not a reopened incident.

**Two fix designs (HALT — `needs_human_decision`):**
- **(a) Full grounding redirect:** when `config.reviewer_grounding_root` is set, derive the recipe `target` / `_load_review_target` / `build_worker_prompt` review target from the snapshot path so any file the workers are told to read resolves under `<snapshot>`. Closes the Step 0.5e item-4 guarantee fully. Larger blast radius (touches the worker-target plumbing).
- **(b) Telemetry-honesty narrowing:** keep children-only grounding; add a `reviewer_isolation` value `"snapshot-children-only"` (models.py `ReflectResult`/`ReflectConfig`, ensemble.py telemetry branch) reported when the ClaudeProcess children are snapshot-grounded but the swarm workers are not; update SKILL.md Step 0.5e item 4 to state the swarm-worker scope honestly. Smaller blast radius; makes the contract truthful. Research-recommended (non-binding) given the workers are text-in/out and the incident vector is already closed.

**Test (falsifier-disciplined, NEW):** under `tests/cli/reflect/` (sibling to `test_reviewer_isolation_gate.py`). For (a): assert that under `--isolate-reviewers` the recipe `target` / worker review target resolves under `reviewer_grounding_root`, not `tasklist_path`. For (b): assert `reviewer_isolation == "snapshot-children-only"` (a value that does not exist pre-fix → fails-before). Either way the test must FAIL on the current tree and PASS after the fix.

## D2 — per-phase QA bookkeeping inconsistency (MEDIUM, Necessary — reconciliation, not code)

**Evidence:** executed task file `.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-reflect-reviewer-guard-20260622-200400/...md` — 20 per-phase QA-lens spawn items (`- [ ]` at Phases 2/3/4) left unchecked while their `PG*.5` gate-verdict items are `[x]`; the operator substituted the Phase-8 final assembled-suite gate (6 lenses ALL PASS). No source code involved.

**Fix:** reconciliation/documentation only — record the substitution explicitly (mark the per-phase items as superseded-by-final-assembly-gate OR add an Open Question documenting it). NON-BLOCKING. NOTE: that task file is in the SIBLING worktree; editing it is optional and out-of-tree — encode as a documentation item the operator can apply where the task file lives.

## D3 — reflect-reviewer.md cites a non-existent doc (LOW, Drift)

**Evidence (CODE-VERIFIED):** `src/superclaude/agents/reflect-reviewer.md:133` names `.dev/analysis/pr199-reflect-hardening-proposal-2026-06-22.md` as the "primary source" for the layer ranking and demotes the PR#199 round-2 findings to "general round-2 context, NOT the ranking source." Task References (`POST-REFLECT-TASK.md:117`) state the `.dev/analysis/pr199-*` proposal docs "DO NOT EXIST" and instruct citing the round-2 findings in their place. Two OTHER pr199 docs DO exist (committed `188f731a`): `.dev/analysis/pr199-reflect-damage-report-20260622.md`, `.dev/analysis/pr199-reflect-subagent-forensics-2026-06-22.md` — but NOT the cited proposal.

**Fix (one edit + sync):** rewrite the `:133` "Rationale source" sentence to cite the resolvable sources — the round-2 findings under `.dev/reflect-hardening/pr199-round2-findings/` and/or the committed forensics docs `.dev/analysis/pr199-reflect-{damage-report,subagent-forensics}-*.md` and the BUILD_REQUEST — and drop the claim that the non-existent proposal is the primary source. Then `make sync-dev` + `make verify-sync`. Documentary; no behavioral/test impact (the existing `test_reviewer_readonly_tools.py` does not assert this prose).

## D4 — TST-4 finding-parity (LOW, AUTHORIZED — no fix)

**Evidence:** `tests/cli/reflect/test_reviewer_finding_parity.py:13-17` labels itself falsifier-EXEMPT as "a reachability INVARIANT over the seeded fixtures, not a layer-landing guard." Task Key Constraint (`POST-REFLECT-TASK.md:133`) explicitly authorizes "any invariant lock that passes on the current tree is falsifier-EXEMPT and MUST be labeled as such." The audit reclassified Reviewer-1's Drift → **Authorized**.

**Fix:** NONE required. Encode as a NON-BLOCKING verification item: confirm the EXEMPT label is correct and present; optionally record the live restricted-vs-all-tools recall comparison (the heavier alternative research/05 §4 deferred) as a Follow-Up, not a change in this task.

## Verification commands

- `env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE uv run pytest tests/cli/reflect/ -q`
- `uv run ruff format --check <changed files>`
- `make sync-dev && make verify-sync` (after any SKILL.md / agent edit)
