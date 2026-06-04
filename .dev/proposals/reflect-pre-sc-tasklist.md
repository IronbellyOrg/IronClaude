# Reflect-Pre Report — `reflect-in-sc-tasklist.md`

> **Mode:** UC-1 (pre-execution coverage / gap / best-practice audit)
> **Protocol:** `sc:reflect-protocol` v1.0.0, Tier 1 grounded single-agent pass
> **Artifact under audit:** `.dev/proposals/reflect-in-sc-tasklist.md`
> **Driving spec:** the user's 5-requirement set (no separate spec file — requirements treated as the spec)
> **Date:** 2026-06-04
> **Verdict:** **PARTIAL** — design is fundamentally sound and well-grounded, but **3 load-bearing gaps must close before implementation** (one of them is a factual error in the central concurrency claim).

All findings below are **Grounded** (real `file:line` citations re-Read this session) unless tagged `[INFERRED]`.

---

## 1. Coverage Assessment — the 5 driving requirements

| # | Requirement | Status | Where addressed | Note |
|---|-------------|--------|-----------------|------|
| R1 | `/sc:reflect --mode pre --remediate` after EACH tasklist, via a **parallel agent** so it never slows generation | **PARTIAL** | Recommended Design §1(a), Decision B2, "Stage 6.5" | Insertion point + per-phase fan-out are correct. But the parallelism/throughput argument rests on a **factually wrong claim** that Stages 7-10 are a concurrent read-only wave (see Gap G1). The "does not slow generation" guarantee is real for the *generation* stages but the co-location target is mis-modeled. |
| R2 | Each tasklist's **VERY LAST task** = `/sc:reflect --mode post --remediate`, ideally a fresh agent/session, run after all tasks complete | **COVERED** (with 1 amendment risk) | Decision C1, Recommended Design §1(b) templated POST task | Templated as a conforming MDTM task placed after the end-of-phase checkpoint; requires amending structural gate #19 (confirmed at `sc-tasklist-protocol/SKILL.md:1114`). Amendment is viable but interacts with gate #20 + check #18 tooling (`_verify_checkpoints`/`build_manifest`) — see G2. |
| R3 | `--spec` used with `--mode pre` IF a spec was used and path is known | **PARTIAL** | Recommended Design §3, Socratic Q1 | Resolution-order logic is sound, but it **conflates surfaces**: it cites a `--tdd-file → --prd-file` precedence that does not exist on the `/sc:tasklist` *command* (only `--spec` exists there — `commands/tasklist.md:37`). `--tdd-file`/`--prd-file` are CLI-`validate` / `.roadmap-state.json` auto-wire flags, not command flags. See G3. |
| R4 | `depth` set in BOTH instances, **deterministically** (not by inference where accuracy is achievable) | **PARTIAL** | Recommended Design §4 (COMPLEXITY_SCORE) | Formula is deterministic and the threshold→reflect-rubric alignment is well-reasoned. BUT one of its six inputs (`multifile`) is **not a persisted/retrievable signal** in the generator today (see G4 + Arithmetic §3), and the `4-9 → --tier auto` band intentionally re-delegates to reflect's non-deterministic rubric (accepted trade-off, not a gap). |
| R5 | Reflect agents default **SONNET** (not opus); new `--reflectagent` flag to override | **PARTIAL → GAP** | Recommended Design §5 | The default-sonnet intent is correct and `--executor-model` exclusion exists in reflect (`reviewer-spec.md:572`). BUT **there is no reflect-side mechanism that pins the reviewer cost class**. `--reflectagent` as specified ("pins the primary reviewer class to `<model>`") has **no implementing surface in reflect today** — reflect's reviewer rotation is fixed and alias-driven. See G5 (the most under-specified requirement). |

**Coverage summary:** 1 covered, 4 partial, 0 outright-missing. No requirement is ignored — every one is engaged with citations. The partials are *integration-fidelity* gaps, not scoping gaps. `coverage_pct` ≈ **0.50 covered + 0.50 partial**; below the 0.90 T1 stop floor → **does not vacuously pass**; PARTIAL verdict is correct.

---

## 2. Best-Practice & Grounding Findings (the load-bearing gaps)

### G1 — CRITICAL (factual error): Stages 7-10 are a **sequential mutate-in-place chain**, not a concurrent read-only wave

The proposal's concurrency spine (Executive Summary; Decision B2; Recommended Design §1(a) "Concurrency contract") repeatedly asserts that Stage 6.5 pre-reflects run *"concurrently with Stages 7-10… both are read-only `Task` fan-outs… Wall-clock = max(reflect-ensemble, patch-chain), not sum."*

This is **contradicted by the actual skill**:

- Only **Stage 7** is a parallel `Task` fan-out (2N agents) — `sc-tasklist-protocol/SKILL.md:1174-1193`, `:1479`.
- **Stages 8-10 are a strict sequential dependency chain** that **mutates the phase files**:
  - `SKILL.md:1415-1420`: *"Stage 8 is blocked by Stage 7 / Stage 9 is blocked by Stage 8 / Stage 10 is blocked by Stage 9."*
  - **Stage 9 (`SKILL.md:1339-1357`) invokes `sc:task --compliance strict` to APPLY patches to the phase files** — i.e., it *rewrites the very content the pre-reflect is auditing.*
  - Stage 10 then re-verifies (`:1359-1386`).

**Why this is load-bearing:** If a per-phase pre-reflect is dispatched at Stage 6.5 and runs "concurrently with Stages 7-10," it audits `phase-P-tasklist.md` **while Stage 9 may be concurrently patching that same file** — a read/write race against a moving target. The reflect coverage matrix would be computed against pre-patch content that no longer exists post-Stage-10. This is *exactly* the staleness failure the proposal listed as Decision-B1's con ("a phase could be patched later, staling the reflect") and then silently reintroduced by co-locating B2 with a chain it mischaracterized as read-only.

**Must close:** Re-derive the concurrency model against the real chain. The correct, defensible placement is **after Stage 10** (post-patch, against final validated content) — which costs the pre-reflect its overlap with the patch chain but preserves correctness. If overlap with Stage 7 only (the genuinely read-only stage) is desired, the pre-reflect must be explicitly fenced from Stages 8-10's mutations (e.g., snapshot the phase file, or gate the pre-reflect to not start until Stage 9 patches for that phase land). The "max(reflect, patch-chain)" wall-clock claim should be withdrawn or reframed: generation (Stages 1-5) is untouched (the real Req-1 guarantee holds), but the validation chain is sequential and partly mutating, so honest wall-clock is closer to `generation + max(Stage7, …) + Stage8 + Stage9 + Stage10 + pre-reflect-if-fenced`.

### G2 — HIGH: Gate #19 amendment is viable but under-scopes the dependent tooling

Confirmed: structural gate #19 (`SKILL.md:1114`) reads *"the `### T<PP>.<NN> -- Checkpoint: End of Phase <PP>` task has the highest `<NN>` in its phase, with no regular task following it."* The proposal (Decision C1 / Open Question 1) correctly identifies the amendment and proposes validating against the sprint phase-discovery regex.

What it under-scopes: gate #19 is **not the only invariant** that assumes "checkpoint is last."
- **Check #18** (`SKILL.md:1113`) and **gate #20** (`SKILL.md:1115`) explicitly tie checkpoint emission/positioning to *"the sprint task scanner"* and *"Wave 2/3 tooling (`_verify_checkpoints`, `build_manifest`)."*
- The Self-Check check #6 (`SKILL.md:1073`) — *"Every phase file ends with an end-of-phase checkpoint task (per checks 18-20)"* — would itself fail once a post-reflect task follows the checkpoint, unless **check #6 is amended too**.

**Must close:** the amendment list must enumerate **check #6, check #18, gate #19, gate #20** as a set, and the verification step must confirm `_verify_checkpoints`/`build_manifest` (and the Sprint scanner regex) treat "highest-numbered task may be a reflect task, not a checkpoint" correctly. The proposal names the risk but scopes the fix to gate #19 alone — too narrow.

### G3 — MEDIUM: `--spec` resolution conflates the command surface with the CLI-validate surface

The proposal's §3 resolution order (`--tdd-file → --prd-file → auto-wired TDD/PRD → roadmap`) describes flags that **do not all exist on `/sc:tasklist`**:
- `commands/tasklist.md:37` exposes exactly one supplementary flag: `--spec`. There is no `--tdd-file`/`--prd-file` on the command.
- `--tdd-file`/`--prd-file` exist as (a) `superclaude tasklist validate` CLI flags (`cli/tasklist/commands.py:62-72`) and (b) `.roadmap-state.json` auto-wire keys consumed by the skill (`SKILL.md:196-211`).
- The skill treats `--spec` as a **TDD-format supplementary input** (`SKILL.md:166-172`, Step 4.1a).

**Net effect:** the *intent* (pass the richest known driving doc as reflect's `--spec`, fall back to roadmap) is achievable and correct, but the proposal's stated precedence chain isn't literally wireable from the command's flag set. **Must close:** restate the resolution order in terms of what `/sc:tasklist` actually has — `--spec` (when provided) and the auto-wired `.roadmap-state.json` `tdd_file`/`prd_file`, else the roadmap path — and confirm the reflect `--spec` is fed from those resolved values, not from non-existent command flags.

### G4 / G5 are detailed in §3 and §4 below.

---

## 3. Arithmetic / Sanity Check — the deterministic depth formula (R4)

`SCORE = 3·n_strict + 3·n_cpo + 2·n_high_risk + 1·multifile + ceil(n_tasks/5) + ceil(n_R/5)`
Bands: `0-3 → quick/T1`, `4-9 → standard/auto`, `≥10 → deep/T2`.
Hard override (pre-table): `n_cpo ≥ 1 OR n_strict ≥ 2 → deep/T2`; `n_tasks == 0 → skip`.

**Boundary mapping — sane:**
- `n_cpo = 1` alone scores 3 → table says `quick/T1`. The override correctly **rescues** it to `deep/T2`. This is load-bearing: without the override a single auth/security/migration phase would get the cheapest gate. Override is **correct** and mirrors reflect's asymmetric-cost rule (`reflect SKILL.md:420`). ✓
- `n_strict = 2` alone scores 6 → table says `auto`. Override lifts it to `deep/T2`. Intentional and consistent with reflect rubric rules 3/4 (`reflect SKILL.md:387-388`). ✓
- All terms non-negative + monotonic ⇒ same inputs → same score. Reproducibility holds **conditional on all six inputs being retrievable** (see G4).

**The `4-9 → --tier auto` band is NOT a gap — it is an honest, bounded delegation.** The proposal (Risk 6) explicitly accepts that this band hands the T1/T2 call to reflect's calibrated-confidence rubric, which is non-deterministic. Given the hard overrides already force every high-stakes phase (CPO / ≥2 STRICT) to deterministic `deep`, only the genuinely-moderate middle is delegated. This is defensible: over-fitting tasklist-side thresholds to replicate reflect's internal rubric would be worse. **Acceptable.**

**G4 — HIGH: `multifile` is not a persisted/retrievable signal.**
The formula treats `multifile` as a signal "the generator already has" (Recommended Design §4, Finding 3). It does **not**. The ">2 files affected: +0.3 toward STRICT" booster (`SKILL.md:597`, `:1153`) is a **transient input to tier scoring** — the generator computes a file count during Stage-4 enrichment but **does not surface "this task tripped the multifile booster" as any persisted phase-file or index field** (confirmed: no such field in the task metadata table `SKILL.md:862-916` region or the index registries `:707-773`). Recomputing `multifile` post-hoc means re-deriving per-task file counts from task descriptions — the exact inference the proposal claims to avoid. **Must close:** either (a) drop `multifile` from the formula (the `n_strict` term already absorbs most multi-file blast radius, since >2 files boosts toward STRICT), or (b) add a generator change that persists the per-task multifile flag so the signal is genuinely deterministic-retrievable. As written, the formula is **not fully reproducible from existing artifacts.**

**Double-counting (minor, non-blocking):** `n_strict` and `multifile` partially correlate — a task that is STRICT *because of* >2 files contributes `3 + 1 = 4`. The proposal presents the six terms as orthogonal; two of them are not independent. Not fatal (still deterministic, still monotonic) but the weighting rationale should acknowledge the correlation. Same softer note applies to `n_strict` vs `n_high_risk` (STRICT security tasks often also score Risk:High).

**`n_R` per-phase retrievability (minor):** the Traceability Matrix (`SKILL.md:759-773`) maps `R-### → Task IDs` at **bundle level**, not grouped by phase. Deriving per-phase `n_R` requires a deterministic join (task ID → phase). Doable, but the proposal's "already computed" is slightly overstated; flag that the join is part of the work.

---

## 4. `--reflectagent` mechanism soundness (R5) — G5, the deepest gap

**The default-sonnet intent is correct** and the cost rationale is grounded: T2 is the expensive band (`cost-profile.yaml:46-56`: T2 claude 35-70k vs T1 3-8k), so pinning reviewers to sonnet/haiku instead of opus is the right lever.

**The threading mechanism, however, does not exist in reflect today:**
- The proposal §5 says `--reflectagent` *"pins the primary reviewer class to `<model>` and lets reflect fill remaining heterogeneous slots."* **There is no reflect-side flag that pins a reviewer class.** Reflect's reviewer rotation is **fixed** (`reviewer-spec.md:80-84`: `sonnet, haiku, (qwen|kimi|deepseek|opus)`) and the *count* is driven by the env-alias routing table (`reflect SKILL.md:216-228`). The reflect command surface (`commands/reflect.md:10`) has `--reviewers N` but **no reviewer-model-selection flag**.
- `--executor-model` (which the proposal also leans on) **excludes** a class from the pool (`reviewer-spec.md:572-576`); it does **not select** the reviewer cost class. The proposal's Executive Summary claim that `--reflectagent` "threads into reflect's reviewer rotation via the existing `EXECUTOR_MODEL_CLASS`/alias-routing surface" is therefore **mechanically incorrect** — that surface excludes, it doesn't select.
- **Heterogeneity tension (proposal's own Risk 5):** even if such a flag were added, pinning *all* reviewers to sonnet would collapse reflect's heterogeneous ensemble (the anti-bias property `feedback_sc_reflect_vs_inline_rfqa.md` shows is load-bearing). The proposal mitigates by pinning "only the primary/cost-anchor class" — but with no implementing surface, this is aspiration, not design.

**Must close:** R5 requires a **reflect-side change** (a new flag or alias-routing parameter that lets a caller cap the reviewer pool's model classes to a cheap set *without* collapsing heterogeneity), then `--reflectagent` on `/sc:tasklist` threads into it. The proposal must either (a) specify that reflect-side flag as in-scope work, or (b) reduce R5 to what the existing surface *can* do: set the env aliases (`ANTHROPIC_DEFAULT_*_MODEL`) so the fixed rotation resolves to cheaper classes, and document that "default sonnet" means "ensure the resolved alias set is sonnet/haiku-weighted." As written, R5 is the **most under-specified requirement** and the proposal overstates that it threads into an existing surface.

---

## 5. Parallel-Execution-Model Soundness & Cost Amplification

**Throughput (Req-1):** The genuine guarantee — *no reflect runs during generation (Stages 1-5)* — **holds** and is the part of Req-1 that matters most; generation latency is untouched. The *failure* is the claim that the pre-reflect overlaps the validation chain for free (G1). Reframe and the requirement is still satisfiable, just with honest wall-clock accounting.

**Cost amplification (proposal Risk 3) — real and partially mitigated:** A 9-phase bundle spawns up to 9 pre-reflect agents + 9 post-reflect ensembles. The deterministic depth map keeps most phases at quick/standard-T1 (3-8k each), but a STRICT/CPO-heavy bundle forces `deep/T2` (35-70k each) on every phase via the hard override — i.e., the override that makes the design *safe* is also the cost-amplification multiplier. `--budget-remaining` threading (`reflect SKILL.md:286-296`) is a correct mitigation and is honored by reflect. **Recommendation:** make the pre-fan-out emit the estimated aggregate cost (sum the per-phase depth→cost-band from `cost-profile.yaml`) into the index *before* dispatch, and gate the fan-out on a budget ceiling — the proposal mentions an "estimated-cost line" but should make it a **pre-dispatch gate**, not just a surfaced line, given the override can force T2 everywhere.

**Post-gate cross-session safety:** Confirmed sound — reflect `--mode post` audits the committed diff (`--diff`), and cross-session only degrades the optional `summarize_changes` corroboration, not the main verdict (`reflect SKILL.md:469`). The fresh-session POST design is well-grounded. ✓ One open dependency: `<phase-commit-range>` resolution (proposal Risk 2) is correctly deferred to execution time — but the design depends on the Sprint executor actually committing per-phase in a way that yields a resolvable range. That assumption should be verified against the sprint executor before relying on it; flag as a confirm-before-build item.

---

## 6. Verdict & Required Closures

### Verdict: **PARTIAL** (proceed to design refinement, not yet to implementation)

The proposal is high-quality, honestly self-critical (its Open Questions already name G1's staleness seed, G2, the commit-range, cost amplification, and the heterogeneity tension), and its reflect-side citations are accurate. It fails the pre-execution gate on **integration fidelity**: three claims about how the *tasklist* side actually works are wrong or unbacked, and they are load-bearing.

### Must close before implementation (blocking):

1. **G1 (CRITICAL):** Withdraw the "Stages 7-10 are a concurrent read-only wave" model. Stages 8-10 are a sequential chain and **Stage 9 mutates the phase files** (`SKILL.md:1339-1357`, `:1415-1420`). Re-place the pre-reflect after Stage 10 (or explicitly fence it from the patch chain) and restate the wall-clock claim.
2. **G5 (HIGH):** Specify the **reflect-side** mechanism for `--reflectagent`. No flag pins reviewer model class today; `--executor-model` excludes, it does not select. Either scope a new reflect flag in, or redefine R5 in terms of env-alias weighting.
3. **G4 (HIGH):** `multifile` is not a retrievable signal. Drop it from the formula or add a generator change that persists it. The "fully reproducible from existing artifacts" claim is false as written.

### Should close (non-blocking but fix before shipping):

4. **G2:** Expand the gate-amendment set to **check #6 + check #18 + gate #19 + gate #20**, and verify `_verify_checkpoints`/`build_manifest`/Sprint-scanner tolerance — not gate #19 alone.
5. **G3:** Restate `--spec` resolution using flags `/sc:tasklist` actually exposes (`--spec` + `.roadmap-state.json` auto-wire), not the non-existent `--tdd-file`/`--prd-file` command flags.
6. **Cost gate:** make the pre-dispatch estimated-cost a **budget gate**, not just a surfaced line (the hard override can force T2 on every phase).
7. **Minor:** acknowledge `n_strict`/`multifile` and `n_strict`/`n_high_risk` correlation; note `n_R` per-phase needs a deterministic join; confirm `<phase-commit-range>` resolvability against the sprint executor.

### What is already sound (no change needed):
- Insertion point = skill, not CLI (Finding 1, confirmed `cli/tasklist/commands.py:15-96`, `executor.py:191-218`). ✓
- Per-phase fan-out granularity, one pre + one post per phase. ✓
- Depth bands + hard overrides arithmetic (CPO/≥2-STRICT → deep is correct and load-bearing). ✓
- `4-9 → auto` delegation to reflect's rubric (honest, bounded trade-off). ✓
- Fresh-session POST audits committed diff, cross-session-safe (`reflect SKILL.md:469`). ✓
- Audit-first `--remediate` (never auto-mutates), `needs_human_decision` HALT discipline. ✓

---

### Grounding ledger (files Read this session)
- `.dev/proposals/reflect-in-sc-tasklist.md` (full)
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (§3-6, rubric, steps 300/385-420/469, executor-exclusion 572)
- `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md` (rotation 80-84, executor exclusion 72-96/572)
- `src/superclaude/skills/sc-reflect-protocol/refs/cost-profile.yaml` (T1/T2 bands)
- `src/superclaude/commands/reflect.md` (surface — no `--reflectagent`)
- `src/superclaude/commands/tasklist.md` (surface — only `--spec`, no reflect flags)
- `src/superclaude/cli/tasklist/commands.py` + `executor.py` (CLI validate-only; per-step `model` at executor.py:136)
- `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (gate #19@1114, checkpoint rules 1011-1027, Stage 7 fan-out 1174-1193, Stage 9 mutate 1339-1357, dependency chain 1415-1420, signals 425-435/488-604/707-773)
