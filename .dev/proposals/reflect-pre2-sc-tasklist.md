# sc:reflect UC-1 Pre-Execution Audit (Pass 2 / Re-verification) — `reflect-in-sc-tasklist.md`

> Mode: UC-1 (`--mode pre`). Driving spec: the 4-requirement + 5-revision-criteria brief supplied by the caller.
> Grounding: every claim below is checked against the on-disk proposal text and the cited source files (Read this session).
> Tier: Tier-1 grounded single-agent pass (re-verification of an already-revised artifact; no escalation triggers present).

---

## 0. Grounding ledger (citations re-Read this session)

| Proposal claim | Source verified | Verdict |
|---|---|---|
| Stages 8-10 are a sequential chain; Stage 9 mutates phase files via `sc:task --compliance strict` | `sc-tasklist-protocol/SKILL.md:1339-1357` (Stage 9 delegates edits to sc:task), `:1415-1420` (dependency chain 7←8←9←10) | **GROUNDED** |
| Checkpoint-is-last invariant encoded in check #6, #18, #19, #20 | `SKILL.md:1073` (check 6 "ends with end-of-phase checkpoint task, per checks 18-20"), `:1113` (#18 scanner tie-in), `:1114` (#19 highest NN, no regular task following), `:1115` (#20 `_verify_checkpoints`/`build_manifest` path presence) | **GROUNDED — all four lines exact** |
| `/sc:tasklist` command exposes only `--spec` (no `--tdd-file`/`--prd-file`) | `commands/tasklist.md:37` (Arguments table: `--spec` is the sole supplementary flag) | **GROUNDED** |
| `--tdd-file`/`--prd-file` exist only in `.roadmap-state.json` auto-wire / CLI-validate | `SKILL.md:196-211` (auto-wire from state file) | **GROUNDED** |
| Stage 7 already fans out 2N parallel agents via `Task` | `SKILL.md:1479` (Tool Usage row), `:1180-1193` (per-phase Agent A/B spawn) | **GROUNDED** |
| Reflect `--executor-model` is an exclusion flag; default rotation `sonnet, haiku, (qwen\|kimi\|deepseek\|opus)` | `sc-reflect-protocol/refs/reviewer-spec.md:72-96`, `:80-84` | **GROUNDED** |
| Reflect cost bands T1 3-8k / T2 35-70k / T3 +20-40k | `refs/cost-profile.yaml:33-66` | **GROUNDED** |
| Reflect `--remediate` is audit-first, never auto-mutates | `commands/reflect.md:255-263` | **GROUNDED** |
| Reflect zero-task guard STOPs UC-1 empty tasklist | `sc-reflect-protocol/SKILL.md` §4.1 Step 1B.1 (proposal cites :300) | **GROUNDED (mechanism present)** |

**Citation-path note (non-blocking, informational):** the proposal labels the reflect skill citations as `reflect SKILL.md:NNN`. The live skill directory is `src/superclaude/skills/sc-reflect-protocol/`. The *content* at the cited sections is correct (verified above); only the bare filename label omits the `sc-reflect-protocol/` path segment. This is a cosmetic citation-label imprecision, not a factual gap — it does not affect any requirement verdict.

---

## 1. Per-requirement coverage (R1-R4)

### R1 — Pre-reflect `--mode pre --remediate` after each tasklist, parallel agent — **COVERED**

The proposal inserts a **Stage 10.5 "Pre-Reflect Sign-off"** (§1(a), Decision B2 merge §107) that fans out one `/sc:reflect --mode pre --remediate` agent **per phase file** via the `Task` tool, in a single parallel wave (§140-149, §156). The `--remediate` flag is present in the spawned invocation (§143). Parallelism is genuine (parallel across phases, reusing the verified Stage-7 `Task` primitive at `SKILL.md:1479`). The non-throughput-blocking guarantee is satisfied by placement *after* generation (Stages 1-5 untouched). **Covered.**

### R2 — Last task = `/sc:reflect --mode post --remediate`, fresh session — **COVERED**

§1(b) templates a fixed terminal MDTM task `### T<PP>.<final> -- Post-Execution Reflection: sc:reflect --mode post` emitted *after* the end-of-phase checkpoint (Decision C1, §117). The spawn directive (§188-190) carries `--mode post --remediate` and an explicit fresh-session instruction; cross-session safety is correctly justified (reflect UC-2 audits the committed diff, not in-memory state — proposal §211, grounded in reflect's cross-session note). The task is a conforming Sprint MDTM item (full metadata table §169-184, four acceptance bullets §197-201). **Covered.**

### R3 — `--spec` used with `--mode pre` if a spec path is known — **COVERED**

§3 (§219-228) defines a deterministic resolution order: explicit command `--spec` → auto-wired TDD/PRD from `.roadmap-state.json` → roadmap path itself (always present). `--spec` is threaded into the pre-gate invocation (§145). The "spec is always knowable" reasoning is sound because the roadmap is the generator's mandatory source-of-truth, so `--spec` is *always* populated, satisfying the "if known" condition maximally. **Covered.**

### R4 — `depth` in BOTH instances, deterministic, not inference — **COVERED**

`--depth` appears in both the pre invocation (§146) and the post spawn directive (§189). §4 defines a pure-integer `COMPLEXITY_SCORE` weighted sum over `n_strict, n_cpo, n_high_risk, n_tasks, n_R` (§248-254) — all signals grounded as deterministically computed (Finding 3, `SKILL.md:707-718`, `:425-435`, `:759-773`). Threshold bands `0-3/4-9/≥10` map to `quick/standard/deep`, plus hard overrides. Inference is explicitly rejected (§82, §271). **Covered.** (One residual nuance: the `4-9` band passes `--tier auto`, deferring the final T1/T2 call to reflect's non-deterministic rubric — but the proposal flags this openly as a deliberate trade-off in Risk #6, and the *tasklist-side* depth decision remains fully deterministic. R4 asks for deterministic depth determination "where possible"; the proposal maximizes determinism and the one delegated band is disclosed. Not a gap.)

---

## 2. Revision-round acceptance criteria (5 specific fixes)

### AC-1 — Pre-reflect fan-out AFTER Stage 10; no free-co-location claim — **LANDED**

The proposal places the fan-out at **Stage 10.5, after Stage 10** (§18, §107, §138, §156). The mutation rationale is grounded: Stage 9 mutates phase files (verified `SKILL.md:1339-1357`), so co-location with Stages 8-10 would race a file mid-patch. The prior `"wall-clock = max(reflect, patch-chain)"` / free-co-location claim is **explicitly withdrawn** in three places (§107, §156, §296) — confirmed by grep (every hit is a withdrawal, zero live claims). Parallelism across phase files is retained (§156). **Landed.**

### AC-2 — Depth formula has NO `multifile` term; bands + override sane; band re-check shown — **LANDED**

The `COMPLEXITY_SCORE` block (§248-254) contains five terms, none `multifile` (grep-confirmed absent from the formula block). A dedicated "Dropped signal — `multifile`" subsection (§243) justifies the removal: the booster is a transient tier-scoring input never persisted to any phase-file/index field (consistent with the verified task-metadata table `SKILL.md:862-916` carrying no such flag), so recomputing it would require the inference the formula avoids. The bands stay `0-3/4-9/≥10`; the override `n_cpo≥1 OR n_strict≥2 → forced deep/T2` is intact (§267). The band re-check (§270) is present and arithmetically sound (see §3 below). **Landed.**

### AC-3 — `--spec` is the SOLE driving-doc flag; phantom `--tdd-file`/`--prd-file` gone except as out-of-scope note — **LANDED**

grep confirms `--tdd-file`/`--prd-file` appear only as: (a) negations ("There are **no** `--tdd-file`/`--prd-file` flags on the command" §78; "There are no `--tdd-file`/`--prd-file` command flags" §221), and (b) one explicit out-of-scope future-extension note (§230). The actual threaded flag is `--spec` only (§145, §221). Grounded against `commands/tasklist.md:37` (sole supplementary flag) and `SKILL.md:196-211` (the auto-wire keys are correctly attributed to the state file / CLI-validate, not the command). **Landed.**

### AC-4 — Structural-gate amendment covers #6 + #18 + #19 + #20 (not #19 alone) — **LANDED**

The amendment set is stated as the four-invariant set in five locations: §164, §117 (Decision C1 merge), §285 (surface-change summary), Risk #1 (§292), and the Executive Summary intent. All four line references verified exact against source: #6=`:1073`, #18=`:1113`, #19=`:1114`, #20=`:1115`. The amended invariant ("checkpoint is the last *checkpoint*; the post-reflection task is the sole task permitted to follow it") is coherent and preserves the checkpoint's gating role. **Landed.**

### AC-5 — Zero residual `--reflectagent` / "sonnet default" (as routing) / model-routing — **LANDED**

grep confirms: no `--reflectagent` token anywhere. Every "model-routing" hit is a **negation** ("introduces no model-routing flag" §18, §276, §284). Every `sonnet, haiku` / `sonnet` hit is a citation of reflect's **own existing env-alias rotation** (§60, §276), correctly grounded in `refs/reviewer-spec.md:80-84` — not a new "sonnet default" routing decision imposed by this proposal. §5 (§274-280) is unambiguous: "introduces **no** model-routing flag … use the **default subagent model**." The only model-related flag threaded is reflect's native `--executor-model` *exclusion* (post gate only), correctly characterized as exclusion-not-selection. **Landed.**

---

## 3. Depth-formula arithmetic sanity check (post-multifile-drop)

Formula: `SCORE = 3·n_strict + 3·n_cpo + 2·n_high_risk + 1·ceil(n_tasks/5) + 1·ceil(n_R/5)`.

Independently recomputing the proposal's three worked checks (§270):

| Scenario | Inputs | Computed | Band | Override | Final | Proposal claim | Match |
|---|---|---|---|---|---|---|---|
| CPO-only | n_cpo=1, rest 0 | 3·1 = **3** | `0-3 → quick/T1` | n_cpo≥1 → forced **deep/T2** | deep/T2 | quick→override→deep/T2 ✓ | **✓** |
| STRICT-pair | n_strict=2, rest 0 | 3·2 = **6** | `4-9 → standard/auto` | n_strict≥2 → forced **deep/T2** | deep/T2 | standard→override→deep/T2 ✓ | **✓** |
| 10-task moderate | n_strict=1, n_high_risk=1, n_tasks=10, n_R=5 | 3+2+ceil(10/5)+ceil(5/5) = 3+2+2+1 = **8** | `4-9 → standard/auto` | none (n_strict<2, n_cpo=0) | standard/auto | "8 → standard/auto (was 9 with one multifile, same band)" ✓ | **✓** |

All three match. The monotonicity argument is also sound: the dropped term had weight +1 and only ever added, so removal can only push a phase to a *lower or equal* band — never higher — and cannot touch the override (which keys solely on `n_cpo`/`n_strict`). The band edges `0-3/4-9/≥10` are unaffected because they were calibrated on the strict/cpo/risk/size/coverage axes, not on multifile. **Arithmetic is internally consistent and the post-drop re-check holds.**

Minor observation (non-blocking): the 10-task example's "(was 9 with one multifile)" footnote is internally consistent — adding back a single `1·multifile` term would yield 9, still in the `4-9` band — confirming the drop is band-neutral for that case.

---

## 4. Parallel-model soundness + cost-amplification note

**Soundness — strong.** The concurrency model is now correct. The single load-bearing fix from the prior round (placement vs. the mutating Stage-9 patch) is properly resolved: the fan-out is fenced to Stage 10.5, eliminating the read/write race against a file being patched, while preserving cross-phase parallelism. The Req-1 guarantee ("parallel agent so it doesn't slow tasklist creation") is honestly re-scoped — generation throughput (Stages 1-5) is the protected surface, and the pre-reflects add a bounded post-Stage-10 wave whose wall-clock is the slowest single phase, not the sum. This is a defensible, accurate framing.

**Cost amplification — disclosed and mitigated.** The proposal correctly identifies (Risk #3, §294) that the safety override (`n_cpo≥1 OR n_strict≥2 → deep/T2`) is also the cost multiplier: a bundle of STRICT/CPO phases forces T2 (35-70k Claude tokens/phase, grounded `cost-profile.yaml:33-66`) across all N phases, *plus* N post-reflect ensembles. For a 9-phase all-STRICT bundle this is a material spend. Mitigations are concrete and grounded: (a) the deterministic depth map keeps most phases at T1; (b) `--budget-remaining` threading (reflect auto-downgrades, grounded `reflect SKILL.md:286-296`); (c) a **pre-dispatch cost gate** that sums per-phase depth→cost-band from `cost-profile.yaml` into the index *before* fanning out (§294 upgrades this from "surfaced line" to "gate"). This is sound. **One residual sharpening (advisory, not a gap):** the proposal does not specify the pre-dispatch gate's *threshold or halt behavior* (what aggregate cost triggers a halt-for-confirmation vs. auto-proceed). That is an implementation detail appropriately deferred to the build task, but worth flagging so the eventual tasklist encodes a concrete ceiling.

---

## 5. Residual gaps / observations

All are **advisory** (none block a PASS; none is a coverage gap against R1-R4 or the 5 ACs):

1. **G1 (cosmetic) — citation label path.** Reflect-side citations read `reflect SKILL.md:NNN`; the live path is `sc-reflect-protocol/SKILL.md`. Content verified correct at every cited section; only the label omits the directory. Harmless, but a reader copy-pasting the path would miss.
2. **G2 (advisory) — pre-dispatch cost-gate threshold unspecified.** §294 mandates the gate but not its trip point. Defer to build, but the build task should name a concrete aggregate-cost ceiling + halt-vs-proceed rule.
3. **G3 (advisory) — `--tier auto` non-determinism in the 4-9 band.** Openly disclosed (Risk #6). Compliant with R4's "where possible" phrasing; flagged only so downstream reviewers know the middle band's final T1/T2 split is reflect-rubric-driven, not reproducible.
4. **G4 (advisory) — `<phase-commit-range>` resolution.** Correctly deferred to execution time (Risk #2, generator emits a placeholder + resolution instruction, never a fabricated SHA — consistent with the non-invention rule `SKILL.md:933`). The mechanism (Sprint executor knows the phase commit boundary) is asserted but not verified against executor code in this proposal; acceptable for a design doc, but the build task should confirm the executor can supply that range.
5. **G5 (advisory) — gate #20 / `build_manifest` tolerance is an assumption.** The proposal correctly identifies (Risk #1) that `_verify_checkpoints`/`build_manifest` and the Sprint phase-discovery regex must tolerate "highest-numbered task may be a reflect task, not a checkpoint," and proposes validating against the regex before shipping. This is the *single highest-risk* structural change in the proposal and is honestly flagged as requiring confirmation — not yet confirmed against the manifest-builder code. The mitigation (gate behind `--no-reflect`-off + validate against the scanner) is the right posture for a proposal stage.

No requirement is uncovered. No revision criterion is unmet. No forbidden token survives.

---

## 6. Verdict

**PASS.**

All four driving requirements (R1-R4) are **Covered**. All five revision-round acceptance criteria are **Landed**, each verified by direct grep + source-grounded re-Read:
- Pre-reflect correctly fenced to Stage 10.5 after the mutating patch chain; free-co-location claim withdrawn (3 sites).
- Depth formula clean of `multifile`; bands + override intact; band re-check arithmetically sound (3/3 worked checks reproduce).
- `--spec` is the sole driving-doc flag; phantom flags appear only as negations + one out-of-scope note.
- Gate amendment covers the full #6/#18/#19/#20 set (all four line refs exact).
- Zero residual `--reflectagent` / model-routing / "sonnet-default-as-routing" references.

The prior round's load-bearing error (pre-reflect placement co-located with the mutation chain) is fully corrected and the correction is grounded in the actual Stage-9 mutation semantics. The five residual items (G1-G5) are advisory implementation-stage concerns appropriately surfaced as Open Questions/Risks in the proposal itself — they do not represent coverage or correctness gaps in the design. The proposal is ready to proceed to a build task; the build task should carry G2-G5 forward as explicit confirmation items.

> Note on the deliberately-removed 5th requirement: the absence of any `--reflectagent` flag and any model-routing is **correct by design** per the caller's spec and was not treated as a gap.
