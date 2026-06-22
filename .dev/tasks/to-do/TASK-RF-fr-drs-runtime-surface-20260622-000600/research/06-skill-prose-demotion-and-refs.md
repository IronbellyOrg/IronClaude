# R6 Research: SKILL.md Prose Demotion + refs (Doc Cross-Validator)

Status: Complete
Date: 2026-06-22
Researcher: R6 (of 8) — FR-DRS deterministic runtime-surface sweep
Topic: §6.1 4b/4b′ demotion + §9.1 contract block + PRESERVE safety sentences + refs/runtime-surface.md + sync workflow

## Source files (re-anchored line counts)

- `src/superclaude/skills/sc-reflect-protocol/SKILL.md` — **1894 lines**, 203KB [CODE-VERIFIED]
- `src/superclaude/skills/sc-reflect-protocol/refs/runtime-surface.md` — **100 lines** [CODE-VERIFIED]
- `src/superclaude/cli/reflect/ensemble.py` — version stamp at line 59 [CODE-VERIFIED]
- TDD: `.dev/reflect-hardening/issue-3-deterministic-runtime-surface-sweep/tdd.md` (1549 lines)

**RE-ANCHOR HEADLINE: the TDD-cited SKILL line numbers are CURRENT and CORRECT.** Every line the TDD cites (465/466/487/489/491, 671-672, 721-736, 390-391/402/412) matches the live source exactly. No staleness detected. [CODE-VERIFIED]

---

## 1. §6.1 step 4b/4b′ — CURRENT text + line numbers + DEMOTED replacement

### 1.1 The one-line step entries (the `find_referencing_symbols` chain block)

**SKILL.md:465** [CODE-VERIFIED] (inside the fenced chain at lines 458-481):
```
4b'. Runtime-surface tagger (UC-2 only): classify diff-hunk symbols by resolved symbol kind/decorator against `refs/runtime-surface.md` allowlist; emit `runtime_surface_requirements` (requirement_id optional/null) and one audit.log row
```

**SKILL.md:466** [CODE-VERIFIED]:
```
4b. Runtime-surface production-caller sweep (UC-2 only): extend the already-fetched step-4 referrers; partition production vs test/comment via `refs/runtime-surface.md`, consult degrade oracle + rootwalk before any UNREACHED, write `<output>/artifacts/runtime-surface-ledger.yaml`, and emit one audit.log row
```

### 1.2 The prose paragraphs that describe 4b′ / 4b / contract emission

**SKILL.md:487** [CODE-VERIFIED] — the 4b′ tagger paragraph (full current text):
> Step 4b' (FR-RSR.1) is the deterministic, LLM-free runtime-surface tagger. It runs in UC-2 only (never `--mode pre`) and keys off the diff hunk's resolved symbol kind/decorator from steps 2/2a/3 plus the `refs/runtime-surface.md` surface allowlist — **not** off a requirement id that may be mapped later in Wave 1B. It emits `runtime_surface_requirements: [<ids>]` when mapped ids exist; a surface hunk with no mapped requirement is still tagged with `requirement_id: null` and the sweep still runs. Non-surface diffs emit `runtime_surface_requirements: []`, `runtime_surface_sweep_ran: false`, and zero added runtime-surface cost. Kind-resolution failure routes to `DEGRADE` (FR-RSR.3/8 → §10.6 Grounding Gap), never silent-skip. It emits one `audit.log` row per the §4 convention with `{wave: 1, step: "4b'", timestamp, outcome, evidence_ref}`.

**SKILL.md:489** [CODE-VERIFIED] — the 4b sweep paragraph (full current text — CONTAINS the load-bearing safety sentence):
> Step 4b (FR-RSR.2/3/4/8) is a read-only production-caller sweep that **extends the already-fetched step-4 `find_referencing_symbols` result**; it does not add a second referrer-fetch call. For each tagged runtime-surface symbol, it partitions referrers into production vs test/comment using `refs/runtime-surface.md` (including inline-test markers such as Rust `#[cfg(test)]` and in-file `Test*`). It then writes `<output>/artifacts/runtime-surface-ledger.yaml` with one row per evaluated edge (`requirement_id`, `symbol`, `edge`, `status`, `production_referrers`, `evidence_ref`) and reduces edges to a per-symbol verdict under `DEGRADE-on-any-incompleteness > UNREACHED > REACHED`. The sweep MUST consult the degrade oracle (any row match → `DEGRADE`) and the entrypoint-rootwalk (`REACHED` from any enumerated root; partial enumeration → `DEGRADE`) before emitting any `UNREACHED`. It emits `runtime_surface_unreached` as a symbol count, `runtime_surface_degraded` when any symbol reduces to `DEGRADE`, and preserves `len(unreached_surfaces) == runtime_surface_unreached`. It reads the Wave-0 §0.5d availability surface rather than re-probing: `backend: none`, a chain-degraded availability report, Serena unavailable, or a `find_referencing_symbols` failure degrades the affected edge to §10.6 Grounding Gap, sets `runtime_surface_degraded: true`, appends `"runtime-surface:backend_unavailable"` to `degraded_components`, continues over remaining edges with no global abort, and NEVER STOPs. It writes only under `<output>/`, **never emits a clean PASS for a tagged surface whose reachability could not be evaluated**, and emits one `audit.log` row per the §4 convention with `{wave: 1, step: "4b", timestamp, outcome, evidence_ref}`.

**SKILL.md:491** [CODE-VERIFIED] — the contract-emission paragraph (full current text):
> **Contract emission is mandatory and name-exact (FR-RSR.7).** Whenever the sweep ran (`runtime_surface_sweep_ran: true`), the §9.1 contract MUST carry ALL SIX `runtime_surface_*` fields by their exact names on EVERY path, including a fully-REACHED run. Map each per-symbol verdict ONLY through those fields — a REACHED symbol is `runtime_surface_unreached: 0` + `runtime_surface_degraded: false` + `unreached_surfaces: []`; a DEGRADE symbol is `runtime_surface_degraded: true` plus a §10.6 Grounding Gap (and is NOT added to `unreached_surfaces`); an UNREACHED symbol increments `runtime_surface_unreached` and adds one `unreached_surfaces[]` entry. Do NOT improvise alternative keys (`runtime_surface_reachable`, `reachability_path`, `static_caller_absent_is_expected`, etc.) — they are invisible to the §9.3 consumer map and break the contract. The dynamic/registry/decorator/[project.scripts]/reflection cases resolve to DEGRADE (oracle, FR-RSR.3), never a bespoke "reachable: true" — a confidently-traced dynamic path is still recorded as `runtime_surface_degraded: true` + Grounding Gap, because static reachability cannot soundly prove it.

### 1.3 PRECISE DEMOTED REPLACEMENT (narration-only WITH conditional fallback, keyed on `runtime_surface_sweep_ran` presence — I6)

The demotion is **surgical**: it flips *who produces the six scalars + ledger* from the LLM to the FR-DRS module, while preserving every safety meaning. It MUST be expressed as a conditional keyed on the **presence/absence of `runtime_surface_sweep_ran` in `return-contract.yaml`** (I6 detection signal — TDD:1193).

**Recommended demotion shape (the builder should write a Phase-4 item with these exact intents):**

- **SKILL.md:465 (4b′ entry)** — KEEP the step's algorithm description AS-IS (tagger logic, kind/decorator classification, allowlist) but add the producer flip: *"On any runner-driven path the deterministic FR-DRS sweep module (`cli/reflect/runtime_surface.py`) computes `runtime_surface_requirements` and writes them to the contract; the LLM does NOT hand-type this field when the sweep ran."*
- **SKILL.md:466 (4b entry)** — KEEP the algorithm (partition, oracle, rootwalk, ledger write) but flip the producer: *"the deterministic FR-DRS sweep writes `runtime-surface-ledger.yaml` and the six `runtime_surface_*` scalars; the LLM narrates the verdict in REPORT.md only."*
- **SKILL.md:487 (4b′ paragraph)** — UNCHANGED in algorithm; add one producer sentence (see below).
- **SKILL.md:489 (4b paragraph)** — UNCHANGED in algorithm + **all safety sentences PRESERVED VERBATIM** (see §2); add one producer sentence.
- **SKILL.md:491 (FR-RSR.7 paragraph)** — RETARGETED, not deleted (see §3.3): from "the LLM MUST carry the six fields" to "the module emits the six fields by exact name by construction; the anti-improvisation warning is retained as a defensive note for the residual bare-skill fallback path."

**The conditional producer sentence to inject (the I6 branch — the heart of the demotion):**

> **Producer (FR-DRS).** On any runner-driven path the deterministic FR-DRS sweep module (`src/superclaude/cli/reflect/runtime_surface.py`, invoked at `runner._audit_once`) computes the six `runtime_surface_*` scalars and writes `runtime-surface-ledger.yaml` BEFORE any consumer reads the contract. **Detection (I6):** if `return-contract.yaml` already carries the `runtime_surface_sweep_ran` key (whether `true` on a swept path or `false` on the non-surface fast path — the field being PRESENT means the module ran and decided), the LLM narrates the verdict in REPORT.md ONLY and MUST NOT hand-type any of the six scalars. **Fallback:** only when the `runtime_surface_sweep_ran` key is fully ABSENT from the contract — i.e. a bare `claude -p /sc:reflect` that never entered the Python wrapper — does the LLM fall back to the legacy emission of the six scalars + ledger described in the paragraphs above. Absence of the key, not a sentinel file or heuristic, is the sole fallback trigger.

This is the **exact I6 contract** from TDD:1193 and TDD:1390/1391: `runtime_surface_sweep_ran: false` on the fast path still means "narrate-only" because the field is PRESENT; only a fully-absent key triggers the legacy fallback. [CODE-VERIFIED against TDD §19.1 / §23.2 Phase 4]

---

## 2. PRESERVE LIST — verbatim safety sentences the demotion MUST NOT ALTER

These are the load-bearing safety sentences. The demotion changes *who computes the scalars*, NEVER *what a verdict means or why an unwired surface must not clean-pass*. ALL are [CODE-VERIFIED] at the current line numbers below. (TDD §19.1 PRESERVE, P1–P6, TDD:1189.)

| ID | Verbatim sentence/clause (PRESERVE EXACTLY) | Current line |
|----|---------------------------------------------|--------------|
| P1 | "It writes only under `<output>/`, **never emits a clean PASS for a tagged surface whose reachability could not be evaluated**, …" — the FR-S9-04 load-bearing sentence | **SKILL.md:489** [CODE-VERIFIED] |
| P2 | "The sweep MUST consult the degrade oracle (any row match → `DEGRADE`) and the entrypoint-rootwalk (`REACHED` from any enumerated root; partial enumeration → `DEGRADE`) **before emitting any `UNREACHED`**." — DEGRADE-first / oracle+rootwalk-before-UNREACHED | **SKILL.md:489** [CODE-VERIFIED] |
| P3 | "… degrades the affected edge to §10.6 Grounding Gap, sets `runtime_surface_degraded: true`, appends `\"runtime-surface:backend_unavailable\"` to `degraded_components`, continues over remaining edges with no global abort, and **NEVER STOPs**." — fail-open / NEVER-STOP envelope | **SKILL.md:489** [CODE-VERIFIED] |
| P4 | "reduces edges to a per-symbol verdict under `DEGRADE-on-any-incompleteness > UNREACHED > REACHED`" — reduction precedence | **SKILL.md:489** [CODE-VERIFIED] |
| P5 | "The dynamic/registry/decorator/[project.scripts]/reflection cases resolve to DEGRADE (oracle, FR-RSR.3), never a bespoke \"reachable: true\" — a confidently-traced dynamic path is still recorded as `runtime_surface_degraded: true` + Grounding Gap, because static reachability cannot soundly prove it." — dynamic→DEGRADE soundness floor | **SKILL.md:491** [CODE-VERIFIED] |
| P6 | "It runs in UC-2 only (never `--mode pre`) …" (4b′) and "(UC-2 only)" scoping on both step entries (465/466) — UC-2-only scoping | **SKILL.md:487** (+ 465, 466) [CODE-VERIFIED] |
| P7 | "Kind-resolution failure routes to `DEGRADE` (FR-RSR.3/8 → §10.6 Grounding Gap), never silent-skip." — tagger-failure→DEGRADE | **SKILL.md:487** [CODE-VERIFIED] |
| P8 | "preserves `len(unreached_surfaces) == runtime_surface_unreached`" — count invariant (now guaranteed by construction, but the SENTENCE stays as the contract) | **SKILL.md:489** [CODE-VERIFIED] |

**§5.3 pre-filter coupling (PRESERVE — not in the 4b region, but the demotion must NOT touch it):**

| ID | Pre-filter clause (PRESERVE) | Current line |
|----|------------------------------|--------------|
| P9 | STOP rows 1 & 2 carry `… AND NOT surface_unreached` | **SKILL.md:390** (row 1), **SKILL.md:391** (row 2) [CODE-VERIFIED] |
| P10 | Table-wide pre-filter precedence (D13): "when … `surface_unreached` is set from a SUCCESSFUL runtime-surface sweep with `runtime_surface_unreached ≥ 1`, NO STOP row … may fire and the run routes to Tier 2" + "for `surface_unreached`, the pinned run also forces `status: partial`" + degrade-only does NOT force T2 | **SKILL.md:402** [CODE-VERIFIED] |
| P11 | `surface_unreached: <string> \| null # "runtime_surface_unreached" when the FR-RSR successful-sweep pre-filter forced T2 …` (tier_decision.yaml schema literal) | **SKILL.md:412** [CODE-VERIFIED] |

**CRITICAL builder note:** the demotion is confined to §6.1 (lines ~465-491). The §5.3 pre-filter (R3's territory) and the §9.1 contract field set (R6 §3 below) are NOT rewritten by the demotion — only the §6.1 *producer prose* changes.

---

## 3. §9.1 contract block — 1.6.0 declaration + producer-only note + FR-RSR.7 retarget

### 3.1 Current §9.1 contract block (re-anchored) [CODE-VERIFIED]

**SKILL.md:669** — section header: `### 9.1 Stable contract (contract_version: 1.6.0)`

**SKILL.md:671-672** — the fenced yaml block opens at 671; the version declaration is line **672** (TDD cited ~671-672; exact = 672):
```
contract_version: "1.6.0"   # 1.4.0 added remediation_task_path (FR-8); 1.5.0 (D13) ADDITIVE ONLY: +coverage_pct_union, +coverage_degraded, +unmapped_requirements_union; coverage_pct and unmapped_requirements keep parsed-only semantics; 1.6.0 (FR-RSR) ADDITIVE ONLY: +runtime_surface_* (6 fields)
```

**SKILL.md:720-736** — the canonical six-name block (TDD cited ~721-736; the MANDATORY-EMISSION comment header begins at 720/721, the six fields are 731-736) [CODE-VERIFIED]:
- 720: `# Runtime-surface reachability (FR-RSR — UC-2)`
- 721-730: the MANDATORY EMISSION (FR-RSR.7) comment block — REACHED/DEGRADE/UNREACHED mapping + anti-improvisation warning + count invariant
- **731** `runtime_surface_requirements: [<list str>]          # FR-RSR.1`
- **732** `runtime_surface_sweep_ran: <bool>                   # FR-RSR.2 (true only when ≥1 tagged surface triggered the sweep)`
- **733** `runtime_surface_ledger_path: <abs path> | null      # FR-RSR.2`
- **734** `runtime_surface_unreached: <int>                    # FR-RSR.2/6 (… drives §5.3 pre-filter)`
- **735** `runtime_surface_degraded: <bool>                    # FR-RSR.3/8`
- **736** `unreached_surfaces: [<list of UnreachedSurface>]    # FR-RSR.6`

The §9.3 consumer map entry is at **SKILL.md:890** ("Any UC-2 consumer (advisory, FR-RSR)" — NON-GATING advisory read of all six fields). [CODE-VERIFIED]

### 3.2 Producer-only change — NO contract_version bump (OQ-DRS.3 resolved "no bump")

**The §9.1 field set does NOT change.** FR-DRS changes the PRODUCER (LLM → deterministic module), not the field set — no field is added/removed/renamed/retyped. Therefore (TDD §19.2, TDD:1199):

- **`contract_version` STAYS `1.6.0`.** No bump. §9.4 reserves major bumps for consumer-breaking shape/semantic changes; FR-DRS makes none. The builder MUST NOT change line 672's version string.
- **OPTIONAL** (Should-Have, not required): annotate the inline comment at line 672 or the 720-730 comment block that the six fields are now *deterministically produced by `cli/reflect/runtime_surface.py`*. No version signal required.
- **Reconcile the stale ensemble stamp:** `ensemble.REFLECT_CONTRACT_VERSION = "1.0"` at **ensemble.py:59** [CODE-VERIFIED] (used at ensemble.py:501 `"contract_version": REFLECT_CONTRACT_VERSION`). Two minor generations behind the skill's `1.6.0`. The consumer gates only `major == "1"`, so NOT breaking today, but stamping the six fields `1.0` while the skill calls the schema `1.6.0` is an internal inconsistency. **This is a CODE change in ensemble.py, NOT a SKILL change** — it belongs in the product-path phase (or carried as Open Question Q4), NOT the Phase-4 prose demotion. The builder should keep this OUT of the Phase-4 SKILL item. (TDD §19.2 bullet 2, TDD:1200; G3 at TDD:335.)

### 3.3 FR-RSR.7 "exact names" retargeting (NOT deletion)

The contract-emission prose (SKILL.md:491 + the 721-730 comment) is **retargeted, not deleted** (TDD §19.2 bullet 3, TDD:1201):
- "MUST carry … by exact names" → becomes a statement of the **module's emission contract** (name-exactness guaranteed by construction + asserted by the eval grader).
- The anti-improvisation warning (the `runtime_surface_reachable` / `reachability_path` forbidden-key list) is **KEPT as a defensive note for the residual narration / bare-skill fallback path** — because on the bare-`claude -p` path the LLM still emits the fields, so the warning still has a live target.
- The 720-730 §9.1 comment block can stay verbatim; optionally append "(deterministically produced by the FR-DRS sweep on runner-driven paths; the LLM-emission rules below apply only to the bare-skill fallback)".

---

## 4. Does refs/runtime-surface.md need an edit during demotion? → NO. It stays as the SPEC.

[CODE-VERIFIED] `refs/runtime-surface.md` is **100 lines** and is the complete behavior SPEC the FR-DRS module PORTS (R1 owns the algorithm depth). It contains: §1 surface allowlist; §2 language test/comment partition table; §3 degrade oracle (categories a–d, incl. the in-repo `[project.scripts]` case at line 45); §4 entrypoint-rootwalk algorithm (depth bound 1); §5 ledger schema + `RuntimeSurfaceLedgerRow` TypedDict + reduction precedence + count invariant + guard note.

**Verdict: refs/runtime-surface.md STAYS AS-IS during the demotion.** Rationale:
1. TDD Non-Goal **NG1** (TDD:219): "Keep `refs/runtime-surface.md` oracle as-is … FR-DRS changes the producer, not the policy." The REACHED-vs-DEGRADE policy for `[project.scripts]` etc. is explicitly NOT re-litigated.
2. TDD §2.3 (TDD:191): refs/runtime-surface.md is the "Behavior source of truth to port" — the module is built FROM it; editing it would change the spec the module must match.
3. The demotion is about WHO produces the scalars (LLM→module), orthogonal to the algorithm/policy refs/ specifies. The module reads refs/ as its spec; the §6.1 prose references refs/ as the allowlist/oracle source — both references remain valid after demotion.

**One caveat for the builder:** an OPTIONAL Should-Have doc-crosslink ("now implemented by `cli/reflect/runtime_surface.py`") is permissible but NOT required and NOT part of the Phase-4 deliverable. Default: leave refs/ untouched. [CODE-VERIFIED against TDD NG1/§2.3]

---

## 5. Sync workflow item the builder MUST include in Phase 4

[CODE-VERIFIED] The edit lands in `src/`, is copied to `.claude/` by `make sync-dev`, and `make verify-sync` confirms parity:

1. **Edit ONLY** `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (source of truth).
2. **NEVER edit** `.claude/skills/sc-reflect-protocol/SKILL.md` directly — it is the gitignored sync-dev OUTPUT. [CODE-VERIFIED: file exists at 203707 bytes, currently `diff -q` IN SYNC with src/]
3. Run `make sync-dev` → copies `src/superclaude/{skills,agents,commands}` → `.claude/` (Makefile:109 target). [CODE-VERIFIED]
4. Run `make verify-sync` → CI-friendly drift check; must be clean before commit (Makefile:166; drift message at Makefile:351). [CODE-VERIFIED]
5. **Staging discipline (CLAUDE.md ABSOLUTE RULE):** stage ONLY the `src/` side. NEVER `git add .claude/skills/...` (gitignored except `settings.json`); a required `-f` is the violation siren.

TDD §23.2 Phase 4 deliverable list (TDD:1390-1393) matches: demote §6.1 4b/4b′ to narration-only WITH conditional LLM-fallback (R2/I6), preserve all safety sentences, then `make sync-dev` + `make verify-sync` clean. (AC-6's `ruff format --check` gates the new MODULE, not SKILL.md — so the SKILL item only needs sync-dev + verify-sync.) [CODE-VERIFIED]

---

## SUMMARY (for the builder — precise Phase-4 item)

1. **Scope:** SKILL.md §6.1 only (lines ~465-491). Flip the PRODUCER of the six `runtime_surface_*` scalars + ledger from LLM to the FR-DRS module, via a **conditional keyed on `runtime_surface_sweep_ran` PRESENCE in `return-contract.yaml`** (I6): key present (true OR false) → narrate-only in REPORT.md; key ABSENT (bare `claude -p`) → legacy LLM emission fallback. Exact branch wording in §1.3.
2. **PRESERVE VERBATIM (P1–P8, plus don't touch P9–P11):** especially SKILL.md:489 "never emits a clean PASS for a tagged surface whose reachability could not be evaluated"; oracle/rootwalk-before-UNREACHED; NEVER-STOP fail-open envelope; `DEGRADE>UNREACHED>REACHED` precedence; dynamic→DEGRADE soundness floor (491); UC-2-only scoping (487/465/466); count invariant (489). Do NOT touch §5.3 (390/391/402/412 — R3's territory) or the §9.1 field set.
3. **§9.1:** NO `contract_version` bump — stays `1.6.0` at SKILL.md:672 (OQ-DRS.3 "no bump"; producer-only, consumer-transparent). FR-RSR.7 "exact names" (SKILL.md:491 + 721-730) is RETARGETED to "module emits by construction; anti-improvisation warning kept for the bare-skill fallback," NOT deleted. The ensemble.py:59 `"1.0"` reconciliation is a CODE change → keep OUT of the Phase-4 SKILL item (product-wire phase / Q4).
4. **refs/runtime-surface.md:** STAYS AS-IS (NG1 — it's the SPEC the module ports; editing it would move the target). No edit during demotion.
5. **Sync:** edit `src/superclaude/skills/sc-reflect-protocol/SKILL.md` ONLY → `make sync-dev` → `make verify-sync` clean. Never edit/stage `.claude/` (currently IN SYNC). Stage src/ side only.

**Re-anchor confirmation:** ALL TDD-cited SKILL line numbers (465/466/487/489/491, 672, 721-736, 390/391/402/412) are CURRENT and CORRECT against live source. ensemble.py:59 confirmed. [CODE-VERIFIED]
