<!-- Provenance: produced by /sc:adversarial (in-context fallback_mode) -->
<!-- Base: Variant 1 (C-canonical, FR-RH1 contracted-sink gate) -->
<!-- Merge date: 2026-06-20 ~06:15 UTC -->

# Decision: Canonical UC-2 Reachability Design for `sc-reflect-protocol`

## TL;DR

<!-- Source: Base (C-canonical) + base-selection.md combined 0.880 -->

**Keep both designs — they are complementary, not redundant — but they are NOT co-equal and MUST NOT share `contract_version: "1.6.0"`.**

1. **C (FR-RH1 contracted-sink reachability gate) is the canonical UC-2 reachability GATE and owns `1.6.0`.** It is the high-precision *blocking* design (real-boot-only Regression), the most complete artifact today, and it attacks sc-reflect's worst failure mode (false PASS on a claimed-but-never-executed durable effect).
2. **B (FR-RSR runtime-surface / UNREACHED) is REFACTORED, not discarded** — it becomes the complementary *advisory* detector (broad recall, degrade-only, does not force Tier 2), sequenced AFTER C.
3. **One `1.6.0` hosting both field families is technically possible but rejected.** Sequence as additive minors (`1.6.0` = `reachability_*`, `1.7.0` = `runtime_surface_*`) — or, cleaner, make B's fields advisory **telemetry** that needs no contract bump at all.
4. **Discard is rejected for both.** Neither is obsolete, unsafe, or value-free; each detects a different defect; both passed their own PRE reflect.

## Why this is not "pick one, discard the other"

The shared name "uc2-reachability" masks two **different detectors** (diff-analysis A-001, CONTRADICTED):

| | B — runtime-surface | C — contracted-sink gate |
|---|---|---|
| Question | Is this code symbol *wired* by production callers? | Did a *real boot* observe the *contracted durable sink*? |
| Strength | Broad recall (any unwired surface) | High precision (gate-grade) |
| Strongest verdict | DEGRADE / UNREACHED (does **not** force Tier 2) | **Regression** (real-boot only) |
| Trust level | Advisory by its own design | Blocking / authoritative |

A **gate** — a verdict that halts work — must be high-precision, because a false Regression destroys trust. C guarantees that; B is *explicitly* degrade-only precisely because it cannot. So C is the gate; B is the advisory detector. (base-selection: C 0.880 vs B 0.650 vs Coexist 0.485.)

## Resolution of the colliding matrix rows

| Row | Collision | Resolution |
|---|---|---|
| **M-028** | Both bump skill contract to `1.6.0`, incompatible field sets | C owns `1.6.0`; B re-points to `1.7.0` additive **or** advisory telemetry (no bump) |
| **M-029** | Both edit SKILL.md / `deviation-taxonomy.md` with different semantic models | B rebases its edits onto C's post-`1.6.0` baseline, additive, preserving C's real-boot-only Regression |
| **M-030** | C-040 leakage lens vs B's design mutually exclusive | C-040's *intent* re-expressed as a B-side guard ("runtime_surface_* never alters reachability_* verdicts"); B no longer "leaks" because it is a deliberately-separate later layer |
| **M-031** | Both append `uc2-*` cases to one `evals.json` (B hardcodes ids 37-41) | C registers first; B re-allocates ids (INV-003) |
| **M-042** | C disturbs the A-vs-B M-008 contract debate | M-008 debate must adopt: C owns skill `1.6.0`; A's CLI return-contract is a separate surface; B is `1.7.0`/telemetry |

## Two MANDATORY safety preconditions (invariant probe)

<!-- Source: Variant 2 (B) strengths incorporated under guard — invariant-probe INV-001/INV-002 -->

- **P-1 — Precedence invariant (HIGH).** When B and C eventually coexist, C's `unreachable`/Regression is authoritative and MUST NOT be softened to a B `degrade`/fail-open for the same root cause. An unwired feature whose annotated sink is unobserved must resolve to **Regression (C wins)**, never degrade-only. B-later must ship this guard + a falsifying eval. *This is why immediate coexistence (Variant 3) is unsafe and why sequencing is required.*
- **P-2 — Sufficiency closure (HIGH).** "Make C canonical" is *necessary but not sufficient*. It is complete only when all of refactor-plan changes #2–#6 are applied and each of M-028/M-029/M-030/M-031/M-042 is independently verified closed.

## Answer to your two explicit questions

- **Which to keep / refactor / discard?** Keep **C** as the canonical gate (owns `1.6.0`); **refactor B** into the advisory layer (sequence to `1.7.0` or telemetry); **discard neither**.
- **Can one `1.6.0` contract host both field families?** Technically yes (no name collision; both additive/optional) — **but do not.** Sequence them, or make B telemetry. A single union forces a 3-way merge, breaks C-040 as written, and is unsafe until P-1 ships.

## Open item (needs human decision)
B's packaging once C owns `1.6.0`: **(a)** additive `1.7.0` *stable* minor, or **(b)** advisory *telemetry* with no contract bump. Choose (b) unless a downstream consumer needs `runtime_surface_*` as a *stable* contract guarantee. (B-task owner's call.)

## Hand-off to the M-008 debate
The operator's in-flight `/sc:adversarial` on the three A-vs-B conflicts must treat the skill `1.6.0` contract as **C-owned**, A's CLI `return-contract.yaml` as a **separate surface**, and B's runtime-surface fields as **`1.7.0`/telemetry** — otherwise M-008 resolves a two-body framing of a three-body collision.
