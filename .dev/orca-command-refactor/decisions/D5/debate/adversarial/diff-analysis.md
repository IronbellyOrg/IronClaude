# Diff Analysis: D5 Decision Option Comparison (Orca nesting depth)

## Metadata
- Generated: 2026-11-02T15:37:21Z
- Mode: A (compare), Step 1 diff analysis; analyst does not advocate for either variant
- Decision: D5, `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` lines 350-354
- Variants compared: 2 (Variant 1 = option a, keep depth 1; Variant 2 = option b, raise depth)
- Total differences found: 27 (plus 7 shared assumptions)
- Categories: structural (5), content (11), contradictions (3), unique (8), shared assumptions (7)

## Structural Differences

Variant 1 = `variant-1-original.md` (option a, keep depth 1). Variant 2 = `variant-2-original.md` (option b, raise depth). Line references are `V1:N` / `V2:N`. Tier: L1 surface, L2 structural, L3 state-mechanics.

| # | Area | Variant 1 | Variant 2 | Severity | Tier |
|---|------|-----------|-----------|----------|------|
| S-001 | Section ordering | Position, Safety, Reliability, Day to day, Cost (V1:7-19). | Inserts a leading "Strongest case for it" section before Safety (V2:7-10), then the same four sections. | Low | L1 |
| S-002 | Position framing | States the option as the spec's current recommendation and anchors it in the spec (`SPEC:352`, `SPEC:42`; V1:3). | Defines the option as enabling "the design section 1.3 rejects" (V2:3), so the variant argues for a setting while conceding its main use is already rejected. | Medium | L2 |
| S-003 | Decision criterion / exit condition | Has a conditional revisit trigger: raise later "if P0 smoke runs (`SPEC:181`) show coordinator-side splitting is inadequate" (V1:19). | States no condition under which option (b) should be chosen; ends with "No phase of the spec uses it" (V2:22). | Medium | L2 |
| S-004 | Requirement anchoring | Cites requirement IDs WC-8 and SA-2 and rejection reasons R2-R5 (V1:12-13). | Cites WC-10, SA-2, non-goal 1 and R2-R4 (V2:8, 16, 22); omits R5. | Low | L2 |
| S-005 | Size and evidence balance | 4 sections, 7 bullets; mostly `SPEC:` citations plus a direct profile-file citation. | 5 sections, 8 bullets; mostly `CAPS:` citations. Same citation key and heading depth. | Low | L1 |

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Severity | Tier |
|---|-------|-------------------|-------------------|----------|------|
| C-001 | Runaway fan-out protection | Depth 1 is Orca's default "fence against runaway fan-out"; a malformed value falls back to the default; a new Run does not reset depth (V1:8; `CAPS:97,100-101`). | Raising depth "Removes Orca's fence against runaway fan-out" (V2:13). Neither variant notes that a raised value moves the fence rather than removing it: the refusal still fires at the new maximum (`CAPS:99`), but the bound grows from one generation of workers to workers-of-workers (width multiplies per level). | High | L3 |
| C-002 | Scope of the setting (machine-wide profile vs per run) | "machine-wide, not per run", cited directly to `orca-data.json:1` `"nestedWorkerMaxDepth":1`; raising it "would raise it for every Orca run on the machine" (V1:9). | "per profile (`CAPS:98`), so it applies to every run on this machine, not only IronClaude workers" (V2:13). Same conclusion; neither cites evidence that no per-run override exists (no depth flag appears in the `worker-start` flag list at `CAPS:135`, which supports both). | Medium | L2 |
| C-003 | Per-unit Task records | Coordinator gets per-unit Task records "by splitting work into Tasks" (V1:12; `SPEC:42`); example fan-in plan N troubleshoot workers then one merge (V1:16; `SPEC:87`). | Depth 2 "would give each sub-unit its own Task and Dispatch" for a command's internal fan-out (V2:8; `CAPS:158`). | High | L3 |
| C-004 | Heartbeat gaps during Agent-tool fan-out | Not addressed. | Treats the WC-10 accepted gap (troubleshoot Tier 2 "+4-15 min", `SPEC:74`) as a cost depth 2 would remove (V2:8). Neither variant checks that a parent worker waiting on its own sub-workers would itself block (heartbeats are skipped while blocked in `ask` or `check --wait`, `CAPS:162`), so the gap moves to the parent rather than disappearing. | High | L3 |
| C-005 | Whether depth alone enables the rejected design (R1-R5) | No: the rejected design fails for R2, R3, R4 and R5, which depth does not fix (V1:13; `SPEC:37-40`). | No: commands would still hit R2, R3, R4 (V2:16; `SPEC:37-39`); adds that enforcement call sites are UNVERIFIED (`CAPS:103`). Omits R5 (second orchestrator). Both treat R1 as the only reason depth removes. | Medium | L2 |
| C-006 | Standalone use | Via R2: standalone use breaks without Orca (V1:13). | Via R2 plus SA-2: Orca calls "fail in other projects without Orca" (V2:16, 22). Same conclusion, different anchors. | Low | L2 |
| C-007 | Implementation cost | "Zero" for option (a) (V1:19). | Setting is "trivial"; real cost is "rewriting commands to call Orca, against SA-2 and non-goal 1"; "No phase of the spec uses it" (V2:22). The two are complementary: (b)'s cost is the command rewrite, not the setting. | Medium | L2 |
| C-008 | Reversibility | Raising later is "one desktop setting"; revisit after P0 (V1:19). | States the change is one setting (V2:10) but does not discuss reversing it. Neither variant addresses what happens to nested workers already running if the value is lowered again (UNVERIFIED in the sources). | Medium | L2 |
| C-009 | Day-to-day effect on a person | "No change" (V1:16). | "More workers and Tasks per run; more terminals to release" (V2:19; `CAPS:113`). | Low | L2 |
| C-010 | Which Orca guidance supports which option | Orca's advice at the limit, "Do the work in this terminal" (V1:8; `CAPS:99`). | Orca's provenance rule, "Never substitute a non-Orca subagent tool when Orca orchestration provenance was requested" (V2:9; `CAPS:158`). See X-001. | Medium | L2 |
| C-011 | Visibility of Agent-tool fan-out to Orca | Agent-tool subagents "are not counted by the fence" (V1:12; `CAPS:155`). | Agent-tool fan-out is "invisible to Orca: no Task, no liveness, no independent retry" (V2:8). Neither cites `CAPS:157`: Orca does show running subagents as UI child rows (display and stop targets, not Tasks); whether a child row affects the worker's liveness is UNVERIFIED. | Medium | L3 |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact | Tier |
|---|-------------------|-------------------|-------------------|--------|------|
| X-001 | Does Orca's provenance rule favour raising depth? | Per-unit records come from coordinator splitting: "the coordinator gets per-unit Task records by splitting work into Tasks (`SPEC:42`)" (V1:12). | "Orca's provenance rule prefers it" (V2:9, citing `CAPS:158`). The cited line itself concludes the opposite route: "the fan-out must be Orca workers from the coordinator, not Agent-tool subagents inside one worker" (`CAPS:158`), which matches V1. | High | L2 |
| X-002 | Is a command's internal Agent-tool fan-out adequately covered at depth 1? | "Nothing in the spec needs depth 2" (V1:12); fan-out stays inside a command or is split into Tasks (V1:3). | "Today a command's Agent-tool fan-out ... is invisible to Orca: no Task, no liveness, no independent retry, and a heartbeat gap the spec has to accept" (V2:8). The conflict is real for fan-out that cannot be lifted out of one command run (troubleshoot Tier 2); V1's Task split covers only fan-out the coordinator can plan as separate Tasks. | High | L3 |
| X-003 | Is there a concrete use for raised depth in this spec? (internal to V2, contrasted with V1) | Consistent: no use; revisit only on P0 evidence (V1:12, 19). | "Strongest case": "Depth 2 would give each sub-unit its own Task and Dispatch" (V2:8), versus its own "Depth alone does not make the rejected design work" (V2:16) and "No phase of the spec uses it" (V2:22). V2 does not reconcile its benefit claim with these concessions. | Medium | L2 |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | Variant 1 | Revisit trigger: raise depth only if P0 smoke runs (`SPEC:181`) show coordinator-side splitting is inadequate (V1:19). Turns D5 into a reversible, evidence-gated choice. | High |
| U-002 | Variant 1 | R5 (a second orchestrator below the coordinator competes with it, `SPEC:40`) as a reason depth does not fix (V1:13). | Medium |
| U-003 | Variant 1 | Orca's own refusal advice, "Do the work in this terminal" (`CAPS:99`), and the malformed-value fallback (`CAPS:100`) as evidence that depth 1 is a deliberate fence (V1:8). | Medium |
| U-004 | Variant 1 | Direct citation of the live profile value `orca-data.json:1` (V1:9), confirmed by re-read. | Low |
| U-005 | Variant 2 | Names the concrete benefit raised depth could buy: per-unit Task, Dispatch, liveness and retry for heavy in-command fan-out, tied to the WC-10 accepted heartbeat gap (V2:8). The only statement of what option (a) gives up. | High |
| U-006 | Variant 2 | Cost is located correctly: the setting is trivial, but using it requires rewriting commands against SA-2 and non-goal 1 (V2:22). | High |
| U-007 | Variant 2 | Flags that which call sites enforce the depth check is UNVERIFIED (`CAPS:103`) (V2:16), so the effect of either value is not fully known. | Medium |
| U-008 | Variant 2 | Day-to-day operator cost: more workers, Tasks and terminals to release (`CAPS:113`) (V2:19). | Medium |

## Shared Assumptions

Only UNSTATED rows are promoted to `[SHARED-ASSUMPTION]` diff points. STATED rows are recorded, not promoted. CONTRADICTED rows are flagged for debate attention.

| # | Assumption | Source Agreement | Impact | Status | Tier |
|---|-----------|------------------|--------|--------|------|
| A-001 | Raising the depth setting removes or breaks the fan-out fence. | V2 states it ("Removes Orca's fence", V2:13); V1 implies it ("its fence against runaway fan-out", V1:8); spec D5 (b) says the same (`SPEC:353`). The sources show the fence still applies at whatever maximum is set (`CAPS:99`: refusal names `(max ${maxDepth})`; `CAPS:100`: invalid values fall back to the default). A raise widens the bound; it does not disable it. | High | CONTRADICTED | L3 |
| A-002 | **[SHARED-ASSUMPTION]** The only use of depth greater than 1 would be commands calling Orca (the section 1.3 design). | Neither variant considers a worker's top-level session (not the command) starting sub-workers under its brief. WC-8 binds commands only (`SPEC:72`), so that route would leave SA-2 intact and avoid R2-R4, while R5 (second orchestrator) and the provenance/record trade-offs would still apply. | High | UNSTATED | L2 |
| A-003 | **[SHARED-ASSUMPTION]** Depth is the binding control on whether a worker can cause more Orca workers. | Both reason as if depth 1 alone stops worker-driven fan-out. `CAPS:103` leaves open whether a depth-1 worker may `task-create`; if it may, a worker could create Tasks for the coordinator to start, an indirect fan-out route at depth 1 that WC-8 forbids only by contract. V2 flags the enforcement gap (V2:16) but neither draws this consequence. | Medium | UNSTATED | L3 |
| A-004 | The setting is machine-wide, with no per-run override. | Both state it (V1:9; V2:13). Supported by `CAPS:98` (`local-default` is the only profile) and by the absence of a depth flag in the `worker-start` flags (`CAPS:135`); absence of an override is inferred, not proven. | Medium | STATED | L2 |
| A-005 | Agent-tool subagents are not limited by Orca's depth fence. | V1 states it (V1:12, `CAPS:155`); V2 relies on it by treating Agent-tool fan-out as the status quo (V2:8). `CAPS:155` marks "Orca never limits them" UNVERIFIED. | Medium | STATED | L3 |
| A-006 | Raising depth is cheap and reversible at any time. | Both state the change is one desktop setting (V1:19; V2:10; `CAPS:99`). Neither checks the behaviour of already-running nested workers if the value is lowered. | Medium | STATED | L2 |
| A-007 | The effect on other Orca runs on this machine counts against option (b). | Both state it (V1:9; V2:13). | Low | STATED | L2 |

## Citation spot-check

Six decision-critical citations re-read on 2026-11-02 (sources: `orca-capabilities.md`, the spec, `orca-data.json` read-only, `nested-worker-depth.js` read-only).

| # | Citation (used by) | Short quote from source | Verdict |
|---|--------------------|-------------------------|---------|
| 1 | `CAPS:97` (V1:8) | "1 means a coordinator dispatches workers and those workers may not dispatch further"; `nested-worker-depth.js:11` `NESTED_WORKER_MAX_DEPTH_DEFAULT = 1` | CONFIRMED |
| 2 | `orca-data.json:1` / `CAPS:98` (V1:9, V2:13) | `"nestedWorkerMaxDepth":1` (re-read from the profile file); `local-default` "is the only profile" | CONFIRMED |
| 3 | `CAPS:100` (V1:8) | "falls back to the default rather than disabling the fence"; `nested-worker-depth.js:33` returns the default | CONFIRMED |
| 4 | `CAPS:155` (V1:12, "not counted by the fence") | "Agent-tool subagents are not Orca workers, so the depth limit does not count them ... UNVERIFIED that Orca never limits them" | OVERSTATED (V1 drops the UNVERIFIED caveat) |
| 5 | `CAPS:158` (V2:9, "Orca's provenance rule prefers it") | "Never substitute a non-Orca subagent tool when Orca orchestration provenance was requested." ... "the fan-out must be Orca workers from the coordinator, not Agent-tool subagents inside one worker" | OVERSTATED (quote accurate; rule is conditional on provenance being requested, and the same line points to coordinator-side fan-out, not depth 2) |
| 6 | `SPEC:74` (V2:8, WC-10 heartbeat gap) | "troubleshoot Tier 2 at "+4-15 min" ... that gap is accepted, not required away, because commands may not call Orca (SA-2)" | CONFIRMED |

Also checked in passing, not counted above: `SPEC:37-40` (R2-R5) and `SPEC:42`, `SPEC:87`, `SPEC:181` match V1's use; `CAPS:103` and `CAPS:113` match V2's use.

## Summary
- Total structural differences: 5
- Total content differences: 11
- Total contradictions: 3
- Total unique contributions: 8
- Total shared assumptions surfaced: 7 (UNSTATED: 2, STATED: 4, CONTRADICTED: 1)
- Citation spot-check: 6 checked; 4 CONFIRMED, 2 OVERSTATED, 0 WRONG
- Tier counts across S/C/X/A (26 rows): L3 = 8 (C-001, C-003, C-004, C-011, X-002, A-001, A-003, A-005); L2 = 16; L1 = 2 (S-001, S-005)
- Highest-severity items: C-001, C-003, C-004, X-001, X-002, A-001, A-002 (High); highest-value unique contributions U-001, U-005, U-006
- Similarity check: comparable items = 16 (S + C rows). Items where both variants reach the same substance: 2 (C-002 scope, C-006 standalone use). Differing items: 14 of 16 (87.5%), well above the 10% threshold, so the variants are NOT substantially identical and the debate should proceed. Note that the two variants agree on most facts (machine-wide scope, depth alone not enabling the rejected design, the cost lying in the command rewrite); the live disagreement concentrates in X-001, X-002, C-001, C-003 and C-004, plus the unexplored worker-session route in A-002.
