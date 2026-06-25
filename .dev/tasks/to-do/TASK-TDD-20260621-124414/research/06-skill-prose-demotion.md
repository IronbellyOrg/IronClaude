# Research 06 — SKILL Prose Demotion Scope (FR-DRS)

**Task:** TASK-TDD-20260621-124414 (FR-DRS — Deterministic Runtime-Surface Sweep)
**Investigation type:** Doc Analyst
**Topic:** The exact SKILL.md prose blocks that move from LLM-instruction to deterministic-sweep-output when the runtime_surface producer becomes Python.
**Primary file:** `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (component root: `src/superclaude/skills/sc-reflect-protocol/`)
**Date:** 2026-06-21

## Scope of this note

FR-DRS changes the **producer** of the six `runtime_surface_*` contract fields from "LLM hand-types the scalars while executing §6.1 step 4b/4b′" to "a deterministic Python module computes the scalars; the LLM narrates only the verdict in REPORT.md." This note pins, verbatim and line-anchored, which SKILL.md prose is (a) demoted to sweep-output narration, (b) preserved as safety behavior, and (c) the contract-emission prose that re-points to a Python producer, and answers whether §9.1's field set / `contract_version` changes.

All quotes below are `[CODE-VERIFIED]` against the file as read this turn (line numbers are exact as of this read; the task-prompt's approximate numbers were off by ~1–2 lines and are superseded here).

---

## 1. Current 4b′ / 4b prose (verbatim) and what it instructs the LLM to do

There are TWO surfaces per step: the **pseudo-code chain line** (the `1..7'` list at lines 458–481) and the **explanatory paragraph** (lines 487 / 489). Both are LLM-facing today.

### 1a. Step 4b′ — the tagger

**Chain line, line 465 `[CODE-VERIFIED]`:**

> `4b'. Runtime-surface tagger (UC-2 only): classify diff-hunk symbols by resolved symbol kind/decorator against `refs/runtime-surface.md` allowlist; emit `runtime_surface_requirements` (requirement_id optional/null) and one audit.log row`

**Explanatory paragraph, line 487 `[CODE-VERIFIED]`:**

> Step 4b' (FR-RSR.1) is the deterministic, LLM-free runtime-surface tagger. It runs in UC-2 only (never `--mode pre`) and keys off the diff hunk's resolved symbol kind/decorator from steps 2/2a/3 plus the `refs/runtime-surface.md` surface allowlist — **not** off a requirement id that may be mapped later in Wave 1B. It emits `runtime_surface_requirements: [<ids>]` when mapped ids exist; a surface hunk with no mapped requirement is still tagged with `requirement_id: null` and the sweep still runs. Non-surface diffs emit `runtime_surface_requirements: []`, `runtime_surface_sweep_ran: false`, and zero added runtime-surface cost. Kind-resolution failure routes to `DEGRADE` (FR-RSR.3/8 → §10.6 Grounding Gap), never silent-skip. It emits one `audit.log` row per the §4 convention with `{wave: 1, step: "4b'", timestamp, outcome, evidence_ref}`.

**What it instructs the LLM to do today:** the LLM (acting as orchestrator) must itself classify diff-hunk symbols against the allowlist, decide whether each is a runtime surface, and **emit** (hand-type) `runtime_surface_requirements`, `runtime_surface_sweep_ran`, and the audit row. Note the wording is already aspirational/deterministic — it *calls itself* "the deterministic, LLM-free runtime-surface tagger" — but the actual producer is the model executing the prose. FR-DRS closes that gap: the prose describes a deterministic algorithm; FR-DRS makes a Python module the literal executor of it.

### 1b. Step 4b — the production-caller sweep

**Chain line, line 466 `[CODE-VERIFIED]`:**

> `4b. Runtime-surface production-caller sweep (UC-2 only): extend the already-fetched step-4 referrers; partition production vs test/comment via `refs/runtime-surface.md`, consult degrade oracle + rootwalk before any UNREACHED, write `<output>/artifacts/runtime-surface-ledger.yaml`, and emit one audit.log row`

**Explanatory paragraph, line 489 `[CODE-VERIFIED]`:**

> Step 4b (FR-RSR.2/3/4/8) is a read-only production-caller sweep that **extends the already-fetched step-4 `find_referencing_symbols` result**; it does not add a second referrer-fetch call. For each tagged runtime-surface symbol, it partitions referrers into production vs test/comment using `refs/runtime-surface.md` (including inline-test markers such as Rust `#[cfg(test)]` and in-file `Test*`). It then writes `<output>/artifacts/runtime-surface-ledger.yaml` with one row per evaluated edge (`requirement_id`, `symbol`, `edge`, `status`, `production_referrers`, `evidence_ref`) and reduces edges to a per-symbol verdict under `DEGRADE-on-any-incompleteness > UNREACHED > REACHED`. The sweep MUST consult the degrade oracle (any row match → `DEGRADE`) and the entrypoint-rootwalk (`REACHED` from any enumerated root; partial enumeration → `DEGRADE`) before emitting any `UNREACHED`. It emits `runtime_surface_unreached` as a symbol count, `runtime_surface_degraded` when any symbol reduces to `DEGRADE`, and preserves `len(unreached_surfaces) == runtime_surface_unreached`. It reads the Wave-0 §0.5d availability surface rather than re-probing: `backend: none`, a chain-degraded availability report, Serena unavailable, or a `find_referencing_symbols` failure degrades the affected edge to §10.6 Grounding Gap, sets `runtime_surface_degraded: true`, appends `"runtime-surface:backend_unavailable"` to `degraded_components`, continues over remaining edges with no global abort, and NEVER STOPs. It writes only under `<output>/`, never emits a clean PASS for a tagged surface whose reachability could not be evaluated, and emits one `audit.log` row per the §4 convention with `{wave: 1, step: "4b", timestamp, outcome, evidence_ref}`.

**What it instructs the LLM to do today:** the LLM must (1) partition referrers production-vs-test, (2) consult the degrade oracle and rootwalk, (3) reduce edges to a per-symbol verdict under the stated precedence, (4) **write** the ledger YAML, and (5) **emit** the scalar fields `runtime_surface_unreached` / `runtime_surface_degraded` / `unreached_surfaces` while preserving the count invariant. Every one of those is currently a model-executed step.

---

## 2. Precisely which sentences become "deterministic sweep computes; LLM narrates verdict in REPORT.md only"

These are the **COMPUTE-AND-EMIT** clauses. Under FR-DRS each is reworded so the *producer* is the Python sweep module and the LLM's only residual job is to read the module's output and narrate the verdict in REPORT.md. Demotion targets, sentence-level:

| # | Source (line) | Clause that DEMOTES to sweep-output | New ownership |
|---|---------------|--------------------------------------|---------------|
| D1 | 465 (4b′ chain) | "...classify diff-hunk symbols by resolved symbol kind/decorator against allowlist; **emit `runtime_surface_requirements`** (requirement_id optional/null)" | Python tagger classifies + emits `runtime_surface_requirements`, `runtime_surface_sweep_ran` |
| D2 | 487 (4b′ para) | "It **emits** `runtime_surface_requirements: [<ids>]`...", "Non-surface diffs **emit** `runtime_surface_requirements: []`, `runtime_surface_sweep_ran: false`...", "Kind-resolution failure **routes to `DEGRADE`**" | All three emissions become deterministic module output; the kind-resolution→DEGRADE rule is the module's branch, not a model judgment |
| D3 | 466 (4b chain) | "...partition production vs test/comment...; consult degrade oracle + rootwalk before any UNREACHED; **write ledger**; emit audit row" | Python sweep partitions, consults oracle/rootwalk, writes ledger, emits audit row |
| D4 | 489 (4b para) | "It then **writes** the ledger...", "**reduces edges to a per-symbol verdict** under `DEGRADE-on-any-incompleteness > UNREACHED > REACHED`", "It **emits `runtime_surface_unreached`** as a symbol count, `runtime_surface_degraded`..., and **preserves** `len(unreached_surfaces) == runtime_surface_unreached`" | The reduction precedence, the three scalar emissions, and the count invariant are all computed by the module |
| D5 | 491 (contract para) | "**Map each per-symbol verdict ONLY through those fields** — a REACHED symbol is `runtime_surface_unreached: 0`...; a DEGRADE symbol is `runtime_surface_degraded: true`...; an UNREACHED symbol increments `runtime_surface_unreached`..." | The verdict→field mapping arithmetic becomes module logic; the prose stops being an instruction-to-the-LLM and becomes a description of the module's mapping table |
| D6 | 721–730 (§9.1 MANDATORY EMISSION comment) | The entire "Record the per-symbol verdict ONLY through these six fields: REACHED→... DEGRADE→... UNREACHED→..." bullet block + "The count invariant ... MUST hold every run." | These become the module's emission contract (enforced in code + asserted by grader), not a directive the LLM must remember to obey |

**What the LLM still narrates (NOT demoted):** the REPORT.md verdict prose — "this surface is UNREACHED, here is the evidence and why it blocks a clean pass." The LLM reads the module-produced `runtime-surface-ledger.yaml` + the six scalars and **describes** them for the human reader. The model NEVER recomputes or re-emits the scalars. Recommended replacement framing for the two paragraphs (487/489): *"The deterministic runtime-surface sweep module (FR-DRS) computes `runtime_surface_requirements`, `runtime_surface_sweep_ran`, `runtime_surface_unreached`, `runtime_surface_degraded`, `unreached_surfaces`, and writes the ledger; the orchestrator MUST NOT hand-type these fields. The LLM's only runtime-surface task is to narrate the per-symbol verdict and its evidence in REPORT.md from the module's output."*

---

## 3. What MUST be PRESERVED (safety behavior — out of scope for demotion)

FR-DRS is narrowly scoped to making the **structured contract mirror reliable** (research 00, lines 63–65). The reachability *safety logic* — never clean-pass an unwired surface — is NOT being re-derived and MUST remain verbatim in the prose. Concretely preserve:

- **P1 — "never emits a clean PASS for a tagged surface whose reachability could not be evaluated"** (line 489, end of 4b para) `[CODE-VERIFIED]`. This is the load-bearing safety sentence. It stays; FR-DRS makes the module *honor* it deterministically rather than removing it.
- **P2 — DEGRADE-first reduction + oracle/rootwalk-before-UNREACHED** (line 489): "reduces edges to a per-symbol verdict under `DEGRADE-on-any-incompleteness > UNREACHED > REACHED`" and "MUST consult the degrade oracle ... and the entrypoint-rootwalk ... before emitting any `UNREACHED`." The *precedence semantics* are preserved as the safety contract; only the *executor* changes to Python. (The arithmetic that follows precedence is what's demoted in D4 — but the precedence RULE itself is preserved.)
- **P3 — fail-open / NEVER STOP envelope** (line 489): "backend: none ... degrades the affected edge to §10.6 Grounding Gap, sets `runtime_surface_degraded: true`, appends `"runtime-surface:backend_unavailable"` to `degraded_components`, continues over remaining edges with no global abort, and NEVER STOPs." Must remain; a deterministic module must inherit the same fail-open posture (a missing referrer engine degrades, never aborts).
- **P4 — dynamic/registry/decorator → DEGRADE, never bespoke "reachable: true"** (line 491): "The dynamic/registry/decorator/[project.scripts]/reflection cases resolve to DEGRADE (oracle, FR-RSR.3), never a bespoke 'reachable: true' — a confidently-traced dynamic path is still recorded as `runtime_surface_degraded: true` + Grounding Gap, because static reachability cannot soundly prove it." Soundness floor; preserved.
- **P5 — UC-2-only / never `--mode pre` scoping** (lines 465, 487, 489) and **read-only / writes only under `<output>/`** (line 489). Preserved unchanged.
- **P6 — §5.3 pre-filter coupling** (lines 402, 412, 734): the comment "drives §5.3 pre-filter" on `runtime_surface_unreached` and the pre-filter that forces Tier 2 on `runtime_surface_unreached ≥ 1` from a SUCCESSFUL sweep, plus the "degrade-only run does NOT force Tier 2 ... its Grounding Gap path independently prevents a clean PASS" carve-out. The CONSUMER side of the contract is unchanged by FR-DRS (it only changes the producer), so these stay verbatim. Demotion must not perturb the field that the pre-filter reads.

**Boundary statement:** demote the *who-computes-and-emits-the-scalars* sentences (§2); preserve the *what-the-verdict-means-and-why-it-blocks* sentences (§3). The semantic safety surface is identical before and after; only the producer is mechanized.

---

## 4. The contract-emission prose (line 491 + §9.1 comment) and how it changes when the producer is Python

**Current contract-emission paragraph, line 491 `[CODE-VERIFIED]`:**

> **Contract emission is mandatory and name-exact (FR-RSR.7).** Whenever the sweep ran (`runtime_surface_sweep_ran: true`), the §9.1 contract MUST carry ALL SIX `runtime_surface_*` fields by their exact names on EVERY path, including a fully-REACHED run. Map each per-symbol verdict ONLY through those fields — a REACHED symbol is `runtime_surface_unreached: 0` + `runtime_surface_degraded: false` + `unreached_surfaces: []`; a DEGRADE symbol is `runtime_surface_degraded: true` plus a §10.6 Grounding Gap (and is NOT added to `unreached_surfaces`); an UNREACHED symbol increments `runtime_surface_unreached` and adds one `unreached_surfaces[]` entry. Do NOT improvise alternative keys (`runtime_surface_reachable`, `reachability_path`, `static_caller_absent_is_expected`, etc.) — they are invisible to the §9.3 consumer map and break the contract. The dynamic/registry/decorator/[project.scripts]/reflection cases resolve to DEGRADE (oracle, FR-RSR.3), never a bespoke "reachable: true" — a confidently-traced dynamic path is still recorded as `runtime_surface_degraded: true` + Grounding Gap, because static reachability cannot soundly prove it.

**§9.1 MANDATORY EMISSION comment, lines 721–730 `[CODE-VERIFIED]`:**

> `# MANDATORY EMISSION (FR-RSR.7): whenever runtime_surface_sweep_ran is true, ALL SIX fields`
> `# below MUST be emitted with these EXACT names on EVERY path — REACHED, DEGRADE, and UNREACHED`
> `# alike. Do NOT invent alternative field names (e.g. runtime_surface_reachable,`
> `# reachability_path, static_caller_absent_is_expected); those are NOT contract fields and a`
> `# consumer keyed on §9.3 will not see them. Record the per-symbol verdict ONLY through these`
> `# six fields:`
> `#   • REACHED  → runtime_surface_unreached: 0, runtime_surface_degraded: false, unreached_surfaces: []`
> `#   • DEGRADE  → runtime_surface_degraded: true (+ a §10.6 Grounding Gap row); the symbol is NOT in unreached_surfaces`
> `#   • UNREACHED→ runtime_surface_unreached: <count ≥ 1>, with one unreached_surfaces[] entry per UNREACHED symbol`
> `# The count invariant len(unreached_surfaces) == runtime_surface_unreached MUST hold every run.`

**How it changes when the producer is Python:**

The *purpose* of this prose was to discipline an unreliable producer (the LLM, which improvised key names like `runtime_surface_reachable` — the exact failure FR-DRS exists to fix; research 00 line 63). Once a Python module is the producer, name-exactness and the count invariant are **guaranteed by construction**, not by the LLM remembering a rule. The prose should therefore be re-pointed, not deleted:

- Reframe **FR-RSR.7's "MUST carry ... by their exact names" / "Do NOT improvise alternative keys"** from a *directive to the LLM* into a *statement of the module's emission contract* — e.g., "The FR-DRS sweep module emits all six fields by exact name on every path; the contract names are the module's output keys, enforced by the grader's schema assertion (research 04)." The anti-improvisation warning is no longer the primary guard but should be kept as a defensive note for any residual narration path.
- The **verdict→field mapping bullets** (REACHED/DEGRADE/UNREACHED) and the **count invariant** become the module's unit-tested specification and the grader's assertion target — they migrate from "LLM emission rule" to "Python invariant + test oracle." Keep them in §9.1 as the canonical field spec, but the §9.1 comment can drop the "MANDATORY EMISSION ... MUST be emitted" imperative voice in favor of "the FR-DRS module emits ...".
- **Producer attribution must be added** somewhere in §6.1 / §9.1: a new sentence naming the deterministic module as the producer and explicitly forbidding the orchestrator from hand-typing the six fields (mirrors the replacement framing in §2). Research 02 covers the invocation site (OQ-DRS.2) where that module runs.

**Net:** §4 prose is *retargeted* (producer = Python, enforcement = code + grader), not removed. The exact field names, the mapping, and the invariant all survive verbatim as the field spec.

---

## 5. Does the §9.1 contract block field set or `contract_version` change?

**Field set: NO change.** The six fields already exist at lines 731–736 `[CODE-VERIFIED]`:

> `runtime_surface_requirements`, `runtime_surface_sweep_ran`, `runtime_surface_ledger_path`, `runtime_surface_unreached`, `runtime_surface_degraded`, `unreached_surfaces`.

FR-DRS adds no field, removes none, renames none, retypes none. It changes only the *producer* of the existing fields (LLM → Python).

**`contract_version`: almost certainly NO bump from `1.6.0` (resolves OQ-DRS.3).** `[CODE-VERIFIED]` line 669/672 — current value is `contract_version: "1.6.0"`. Mapping FR-DRS against the §9.4 versioning rule (lines 902–906 `[CODE-VERIFIED]`):

- **Patch (1.0.x)** = "typo, comment, or doc-only change in a field's description; no shape change." FR-DRS makes no shape change at all — same fields, same types, same semantics. The producer is implementation detail invisible to consumers.
- **Minor (1.x.0)** = purely *additive* new fields. FR-DRS adds none.
- **Major (X.0.0)** = rename/removal/retype/semantic change. FR-DRS does none. Critically, the §9.3 consumer rows (line 890, "Any UC-2 consumer (advisory, FR-RSR)") and the §5.3 pre-filter read the SAME fields with the SAME semantics — no consumer must change. Major is explicitly defined by consumer-breaking change; FR-DRS is consumer-transparent.

So the correct classification is **patch-or-nothing**. A bump is warranted ONLY if the producer-change is recorded in the `contract_version` inline comment as documentation (a patch `1.6.1`), but even that is optional: §9.4 patch covers "comment/doc-only change ... no consumer action required," and a producer swap that preserves shape and semantics arguably needs no version signal at all. Recommendation: **keep `1.6.0`**; optionally annotate the inline comment that the FR-RSR fields are now deterministically produced (FR-DRS), with no version change. This matches research 00 (line 102: "1.5.0/1.6.0 were ADDITIVE; FR-DRS changes the PRODUCER not the field set → likely no version bump") and the template-orientation note ("OQ-DRS.3: producer change, likely no version bump from 1.6.0").

**One caveat to flag for the spec author:** if FR-DRS also *tightens* a semantic — e.g., makes `runtime_surface_degraded` mean something subtly different, or changes when `runtime_surface_sweep_ran` is true on the bare `claude -p /sc:reflect` path that the module does NOT cover (OQ-DRS.2) — that WOULD be a semantic change and force a major bump. Per current scope (mirror-reliability only, same semantics), no such tightening is intended, so 1.6.0 holds. This is the single condition under which OQ-DRS.3 flips.

---

## Gaps and Questions

- **G1 (OQ-DRS.2 — coverage of the bare-skill path).** The demotion prose in §6.1 is read by BOTH `superclaude reflect run` (where a post-skill Python sweep can run) AND a bare `claude -p /sc:reflect` (no commands.py wrapper). If the deterministic module runs only in commands.py, the bare-skill path still has the LLM emitting the fields — meaning the 4b/4b′ prose CANNOT be fully demoted; it must retain an LLM-fallback emission branch. The demotion wording must be conditional ("when the FR-DRS module ran, the LLM narrates only; otherwise the legacy emission prose applies"). This is the biggest open dependency on research 02/03. Unresolved here by design.
- **G2 (refs/runtime-surface.md ownership).** The allowlist + degrade-oracle + inline-test markers currently live in `refs/runtime-surface.md` as an LLM-consumed reference. When the producer is Python, the module must consume the SAME ref as machine-readable data (or the ref's rules must be encoded in code with the .md kept as the human spec). Whether refs/runtime-surface.md is demoted from "LLM instruction" to "module data source" is adjacent to this note's scope and should be confirmed (research 01 covers the algorithm).
- **G3 (audit.log row producer).** Both steps emit one `audit.log` row "per the §4 convention." If the module emits these rows, the §4 per-step audit convention prose may need a producer note too. Not enumerated in the task's four target blocks; flag for the §4 owner.
- **G4 (REPORT.md template).** `refs/report-template.md` renders the contract fields (line 667 reference). If narration is the LLM's only residual job, the template's runtime-surface section may need a "narrate from ledger" instruction. Out of scope for the four named blocks but coupled.

## Stale Documentation Found

- **No stale prose within the four target blocks.** All four (4b′ line 487, 4b line 489, contract-emission line 491, §9.1 comment 721–730) are internally consistent and consistent with §5.3 (lines 402/412), §9.1 field defs (731–736), and §9.3 (line 890) as of this read.
- **Line-number drift in the TASK prompt (not in the doc):** the prompt's "~line 465/487 / 466/489 / 491 / 721–735" were approximations. Verified-exact anchors: 4b′ chain = **465**, 4b chain = **466**, 4b′ para = **487**, 4b para = **489**, contract-emission para = **491**, §9.1 MANDATORY EMISSION comment = **721–730** (the field defs it governs run **731–736**; "735" in the prompt lands mid-field-block, not at the comment's end). Future edits should anchor to 721–730 for the comment.
- **Minor wording mismatch to watch (not blocking):** line 487 self-labels the tagger "the deterministic, LLM-free runtime-surface tagger" while line 491 / the §9.1 comment instruct the LLM to do the emitting. That tension is exactly what FR-DRS resolves — but it means the word "LLM-free" at line 487 is currently *aspirational, not literal*. After FR-DRS it becomes literally true; before FR-DRS it is technically inaccurate. Worth a one-word note so a reader doesn't assume the tagger is already mechanized.

## Summary

FR-DRS swaps the **producer** of the six `runtime_surface_*` fields from the LLM (executing §6.1 step 4b/4b′ prose) to a deterministic Python module, with **no field-set change and no `contract_version` bump** (stays `1.6.0`; OQ-DRS.3 resolves "no bump" because the change is producer-only and consumer-transparent per §9.4 — major bumps are defined by consumer-breaking shape/semantic changes, of which FR-DRS makes none).

**Demote (§2):** the compute-and-emit clauses at lines 465/466 (chain), 487/489 (paragraphs), 491 (mapping arithmetic), and the §9.1 MANDATORY EMISSION imperative at 721–730 — i.e., "classify and emit," "write the ledger," "reduce edges to a verdict," "emit the scalars," "map each verdict through these fields," "the count invariant MUST hold." These become module output; the LLM's only residual runtime-surface job is to **narrate the verdict in REPORT.md** from the module's ledger + scalars.

**Preserve (§3):** the safety semantics — **"never emits a clean PASS for a tagged surface whose reachability could not be evaluated"** (line 489), the DEGRADE-first precedence + oracle/rootwalk-before-UNREACHED rule, the fail-open/NEVER-STOP envelope, the dynamic→DEGRADE soundness floor, UC-2-only scoping, and the §5.3 pre-filter coupling. The reachability *safety logic* is explicitly out of scope for demotion and must remain verbatim.

**The demote-vs-preserve boundary in one sentence:** demote the sentences about *who computes and hand-types the six scalars + ledger* (those become deterministic Python output the LLM merely narrates), and preserve the sentences about *what each verdict means and why an unevaluable/unwired surface must never clean-pass* (the safety contract, unchanged — with no field-set or `contract_version` change).
