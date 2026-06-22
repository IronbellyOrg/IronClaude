# Adversarial scoring seam decision

Status: Resolved
Date: 2026-06-20
Task step: 0.3

**DECISION: RESOLVED → Option (b) (working default; second top-level `ClaudeProcess` running `/sc:adversarial` Mode A, NFR-7-legal); launch site = ensemble.py; sub-fork b1 (literal `/sc:adversarial --compare … --suspect-source …`) to be confirmed against `sc-adversarial-protocol` at wiring time per Open-Question Q5/A-OQ4; on-disk return-contract path = a sibling dir `<output_dir>/t2-adversarial/return-contract.yaml` (preserving the §5.3 path-confinement invariant — reflect still parses ONLY the top-level contract); fallback = option (c) null-convergence DEGRADE on adversarial-child failure**

**Recommended:** Option (b)

## Verbatim source facts

Spec §2.2 step 3:

> `/sc:adversarial`  (sc-adversarial-protocol Mode A)  ── DOWNSTREAM SCORER ──
> consumes the N normalized per-reviewer artifacts (suspect-aware)
> adversarial merge verdict + convergence score

Spec §5.3 `phase_b_to_c` block:

```yaml
# Phase B -> Phase C: swarm reduce output -> sc-adversarial Mode A
phase_b_to_c:
  artifacts: output_files[].final_path   # N normalized per-reviewer artifacts (reduce.py normalize+merge)
  swarm_merged_path: merged.md           # mechanical concat ONLY -- NOT the verdict (merge.py:9-30)
  swarm_contract: return-contract.yaml   # swarm DM-012 contract + done.json sentinel
  scorer: "/sc:adversarial (sc-adversarial-protocol Mode A)"  # consumes final_path artifacts (suspect-aware)
```

Spec FR-RH2.3 acceptance bullets:

> The downstream merge step consumes swarm's per-reviewer `final_path` artifacts (suspect-aware).
>
> No scoring/ranking/dedup logic is added to `swarm/merge.py` (the LOC ceiling + boundary tests stay green).
>
> The adversarial merge produces a convergence score recorded on the reflect contract.

Spec §9 NFR-7 reconciliation states that external HTTP workers via `dispatch_wave1` are not the in-process Agent/Task surface NFR-7 targets, the guard extends to `ensemble.py`, and any amendment is recorded deliberately, never via `--no-verify`, `subagent_type`, or a silent exemption.

## Research conclusions

- `/sc:adversarial` is a Claude-inference skill, not an importable Python module; no `src/superclaude/cli/adversarial*` implementation exists.
- Therefore `ensemble.py` cannot compute a real adversarial convergence score in-process. It must use a Claude inference launch surface for a real score.
- Inside the reflect package, `ClaudeProcess` is the sanctioned inference launch. The NFR-7 guard bans `Task(`, `subagent_type`, `anthropic` imports, raw `subprocess.run`/`Popen`, and async patterns in the reflect package; it does not ban `ClaudeProcess`.
- The spec/TDD under-specify exactly how `ensemble.py` obtains `adversarial_convergence_score`; this record resolves that seam for implementation.

## Options considered

### Option (b) — second top-level `ClaudeProcess` adversarial scorer (selected working default)

Launch a second top-level `ClaudeProcess` from `ensemble.py` running `/sc:adversarial` Mode A over the swarm per-reviewer `final_path` artifacts, parse `convergence_score`, and map it to reflect's `adversarial_convergence_score`. This is NFR-7-legal because the launch is single-level and uses the sanctioned `ClaudeProcess` surface; the double-nesting defect is not recreated. Sub-fork b1 (literal `/sc:adversarial --compare … --suspect-source …`) is selected as the working default and must be confirmed against `sc-adversarial-protocol` at wiring time per Q5/A-OQ4.

On-disk scorer output contract path: `<output_dir>/t2-adversarial/return-contract.yaml`. Reflect still parses only the top-level `<output_dir>/return-contract.yaml`; `ensemble.py` consumes the scorer subdir and writes the top-level reflect contract.

### Option (a) — `/sc:reflect` child carries the score (rejected)

Rejected because it forces the child to read/use the `t2-swarm/` outputs and reintroduces the broken `/sc:reflect`-owned nested fan-out/scoring path, violating the path-confinement invariant and failing to resolve the headless nesting defect.

### Option (c) — leave score `None` (rejected as steady state; retained as fallback)

Rejected as the steady state because `adversarial_convergence_score: None` at Tier 2 triggers `null-convergence`, so faithful Tier-2 can never PASS. Retained only as the graceful fallback when the adversarial child fails.

## Downstream effect

This item informs (does not halt) Phase 3 Step 3.2 adversarial-handoff wiring. Unless a human edits this record before Step 3.2, implementation must use Option (b) with launch site `ensemble.py`, sub-fork b1, sibling scorer contract path `<output_dir>/t2-adversarial/return-contract.yaml`, and fallback option (c) null-convergence DEGRADE.

Override window: a human may edit this record before Step 3.2 to change option, sub-fork, or launch site. Absent that override, Option (b) ships.
