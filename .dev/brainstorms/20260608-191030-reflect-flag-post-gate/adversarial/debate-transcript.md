# Adversarial Debate Transcript

## Metadata
- Depth: deep | Rounds completed: 3 (R1 parallel, R2 rebuttals, R2.5 invariant probe, R3 final)
- Convergence achieved: 0.82 | Threshold: 0.75
- Advocate count: 3 (V1 opus:architect, V2 opus:refactorer, V3 haiku:qa)
- Taxonomy coverage: L1 ✓ (field naming) · L2 ✓ (knob reconciliation, section layout) · L3 ✓ (none-semantics, nesting boundary, auto predicate)

## Round 1: Advocate Statements (parallel)

### V1 architect
- **Position**: Collapse three knobs into one ordinal dial `{none,1,2,auto}` + a retained back-compat `halt` position; `auto` reuses the existing TCS/S5/S6 so mode and depth share one producer; `reflect_post_mode` is the lone oracle.
- **Steelman of V2**: V2's "minimal reversible diff / degrade-to-existing-behavior" is the right risk posture; its diff-vs-current presentation is the clearest for implementers.
- **Steelman of V3**: V3's exhaustive assertion matrix is the strongest validation artifact; mode→assertion mapping is genuinely better than a prose rewrite.
- **Critique**: V2 conflates `none`/`DISABLED` with the manual HALT item (X-001) — today `DISABLED` emits *nothing*; V3 drops `S5>0` from auto, under-auditing low-TCS human-decision tasklists.
- **Concession**: My standalone `S2≥3` standard-band gate adds complexity TCS already captures via S2's ×4 weight.

### V2 refactorer
- **Position**: This is a single-emission-site template switch behind one flag + one pure `RESOLVE_POST_MODE`; default-2 and disabled paths restore today's behavior maximally; auto reuses the exact O1/O2/deep-band signals.
- **Steelman of V1**: V1's total old→new map + single-producer invariant is the cleanest long-term surface; the `none` vs `halt` distinction is more honest than my collapse.
- **Steelman of V3**: V3's acceptance tests make every FR falsifiable.
- **Critique**: V1's extra `S2≥3` gate and 7-value `reflect_post_mode` enum add surface; V3's build-time subagent detection is mostly infeasible.
- **Concession**: My `halt → Mode 1` alias is semantically backwards (halt means *manual disjoint*, Mode 1 is *inline non-disjoint*); my "DISABLED → manual item / zero delta" row is wrong (DISABLED = no item today). Both are bugs.

### V3 qa
- **Position**: Every requirement is a test surface; auto = simplest rule two implementers cannot disagree on (`TCS≥35 ∨ S6==1`); V1–V16 enumerated validation; build-time subagent catch.
- **Steelman of V1/V2**: Their runtime self-check is the only place the executor frame is actually known.
- **Critique**: V1/V2 validation is under-specified relative to a numbered assertion table.
- **Concession**: Dropping `S5>0` from the auto predicate is a gap — a 1-human-decision, low-TCS tasklist would get inline Mode 1 where executor-disjoint review matters most. Build-time `agent_tool_depth` is rarely available; the runtime check must be primary.

## Round 2: Rebuttals

- **On X-001 (none semantics)** — V2 concedes: `none`/`DISABLED` MUST emit no item (matches today). The manual fresh-session item is a *separate* `halt` state. **Resolved → V1 model.**
- **On C-001 (halt mapping)** — V2 and V3 both concede V1's mapping (legacy `POST_REFLECT_MODE: halt` → byte-identical manual item, `reflect_post_mode: halt`) is faithful to the sibling's semantics. **Resolved → V1.**
- **On C-002 (auto predicate)** — V3 concedes `S5>0` belongs in the predicate. V1 concedes the standalone `S2≥3` gate is redundant. **Resolved → `S6==1 ∨ S5>0 ∨ TCS≥35 → Mode 2; else Mode 1`** (V2's form).
- **On C-003 (subagent detection)** — consensus: runtime self-check primary (V1/V2); build-time `agent_tool_depth` best-effort defense-in-depth where the signal exists (V3). **Resolved → hybrid, runtime load-bearing.**
- **On U-001/U-002 (validation + diff presentation)** — unanimous: merge V3's V1–V16 matrix and V2's diff-vs-current presentation into the base. **Resolved → merge.**
- **On C-004 (field name)** — `REFLECT_POST_MODE` (mirrors frontmatter `reflect_post_mode`; legacy `POST_REFLECT_MODE` retired as deprecated alias so no live collision). **Resolved.**

## Round 2.5: Invariant Probe
See `invariant-probe.md`. One HIGH finding (INV-002, auto+wrapper-absent under a would-be-Mode-2 tasklist) — addressed by unifying the fallback ladder (resolve risk-mode first, then apply wrapper-availability degradation identically for fixed-2 and auto-2). No HIGH UNADDRESSED remain.

## Round 3: Final Arguments
- All advocates accept V1 as base with V2's presentation + V3's validation merged, the unified fallback ladder (INV-002), the 3-term auto predicate, and the advisory warning for fixed-1 on high-risk tasklists (INV-003).
- Remaining non-blocking disagreement: `reflect_post` for `none` — *absent* (V1) vs `null` (V3). Resolved to **`reflect_post:` key omitted** (V1) for `none`; rf-qa asserts absence.

## Scoring Matrix

| Diff point | Winner | Confidence | Evidence |
|---|---|---|---|
| X-001 none-semantics | V1/V3 | 95% | V2 conceded; matches today's DISABLED=no-item |
| C-001 halt mapping | V1 | 88% | V2/V3 conceded sibling-semantic fidelity |
| C-002 auto predicate | V2 | 85% | V3 conceded S5; V1 conceded S2 gate |
| C-003 subagent detect | V1/V2 | 80% | frame unknown at build; V3 conceded |
| U-001 validation | V3 | 90% | unanimous merge-in |
| U-002 diff presentation | V2 | 85% | unanimous merge-in |
| S-001/2/3 structure | V1 base | 75% | most complete, correct on high-stakes points |

## Convergence Assessment
- Points resolved: 16 / 17 (only `reflect_post`-for-none was a low-severity preference, resolved)
- Convergence: **0.82** | Threshold: 0.75 | Status: **CONVERGED**
- No HIGH-severity UNADDRESSED invariants. Taxonomy fully covered.
