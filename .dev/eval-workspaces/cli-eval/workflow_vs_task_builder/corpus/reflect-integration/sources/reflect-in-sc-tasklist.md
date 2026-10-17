# Proposal: Incorporate `/sc:reflect` into the `/sc:tasklist` Pipeline

> Produced via the `/sc:brainstorm` protocol (Socratic dialogue → candidate approaches per decision → adversarial merge). Design/proposal only — no skill/command files were edited. All citations are to files Read in this session.

---

## Executive Summary

`/sc:tasklist` is a **deterministic, multi-file roadmap-to-tasklist generator** (skill `sc-tasklist-protocol`). It emits `tasklist-index.md` plus one `phase-N-tasklist.md` per phase, then runs a mandatory 4-stage post-generation roadmap-validation chain (Stages 7-10). The user wants `/sc:reflect` wired into this pipeline at two points:

1. A **PRE gate** (`/sc:reflect --mode pre --remediate`) that validates each generated tasklist against its driving spec — running on a **parallel agent (parallel across phases)** so it never blocks generation throughput.
2. A **POST gate** — each tasklist's **very last task** becomes `/sc:reflect --mode post --remediate`, ideally spawned in a fresh session, to audit the work after all that tasklist's tasks execute.

Plus two threading requirements: `--spec` (when a spec/roadmap path is known) and a **deterministic `depth` complexity mapping** (1/2/3) computed from the structured signals the generator already produces.

### Recommended design in one paragraph

Insert both gates **at the skill level** (the CLI `superclaude tasklist` surface is validate-only — it cannot generate, so there is nothing to gate there; see Current-State Findings). Add a new **Stage 10.5 "Pre-Reflect Sign-off"** that, **after Stage 10 completes**, **fans out one `/sc:reflect --mode pre` agent per phase file in parallel via the `Task` tool** (parallel across phases, so it does not serialize per-phase). It is fenced to start only after generation + the Stage 8-10 patch chain have finished, because **Stage 9 mutates the phase files** (`sc:task --compliance strict`) and a concurrent pre-reflect would race a file being patched. The **POST gate is templated into generation**: the generator appends a final, fixed `/sc:reflect --mode post` MDTM task to every phase file as the new highest-numbered task (placed *after* the existing end-of-phase checkpoint), carrying a self-contained spawn directive. **`depth` is computed deterministically** from a per-tasklist complexity score built from tier distribution, task count, phase blast-radius, FR/NFR (R-###) coverage, and Critical-Path-Override count — no LLM inference. The spawned reflect agents use the **default subagent model**; this proposal introduces no model-routing flag and does not pin reflect's reviewer cost class.

---

## Current-State Findings (with citations)

### Finding 1 — `/sc:tasklist` is a skill, the CLI `tasklist` is a *different* surface (validate-only)

This is the single most load-bearing finding for insertion-point selection.

- The skill `sc-tasklist-protocol` contains the **entire generation algorithm** and runs 10 stages (Stages 1-6 generate; Stages 7-10 validate against the roadmap). `src/superclaude/skills/sc-tasklist-protocol/SKILL.md:14-17`, `:1170-1172` (Stages 7-10), `:1394-1405` (the 10-stage table).
- The command file `src/superclaude/commands/tasklist.md` does **no generation** — it parses args, validates inputs, derives `TASKLIST_ROOT`, and invokes `Skill sc:tasklist-protocol`. `commands/tasklist.md:28-31` ("The command itself does not execute any generation logic"), `:74-84` (mandatory Skill activation).
- The **CLI** `superclaude tasklist` is a Click group whose **only** subcommand is `validate` — a *fidelity* checker that runs a single Claude subprocess against `build_tasklist_fidelity_prompt` and exits 1 on HIGH-severity deviations. It does **not** generate tasklists. `src/superclaude/cli/tasklist/commands.py:15-28` (group docstring: "Validate generated tasklists…"), `:31-96` (`validate` is the lone command), `src/superclaude/cli/tasklist/executor.py:191-218` (`_build_steps` builds one `tasklist-fidelity` step), `:251-277` (`execute_tasklist_validate`).
- The skill itself explicitly draws this line: "Generation enrichment … is a **skill-protocol behavior** … It is NOT triggered by the CLI `superclaude tasklist validate` command, which only performs fidelity validation … The CLI `validate` subcommand uses `build_tasklist_fidelity_prompt`; the skill protocol uses `build_tasklist_generate_prompt`." `SKILL.md:129`.

**Consequence:** Reflect insertion lands **in the skill protocol**, not the CLI. There is no generation CLI stage to instrument. (If a future `superclaude tasklist generate` CLI is added, the pre-gate would mirror as a parallel pipeline step using the same `Step`/`ClaudeProcess` machinery in `executor.py:130-140`, which already accepts a per-step `model` — see `executor.py:136`. That is out of scope here but the design is forward-compatible.)

### Finding 2 — The generator already runs a parallel agent fan-out (Stage 7)

Stage 7 spawns **2N parallel validation agents** (Agent A + Agent B per phase file) via the `Task` tool, all in parallel, then merges/dedupes. `SKILL.md:1174-1226`, `:1479` (Tool Usage: "`Task` (Agent) | Spawn 2N parallel validation agents"). This proves the skill **already has a parallel-agent fan-out primitive** the pre-reflect can reuse — the pre-gate does not invent a new concurrency primitive. Note it **reuses the primitive, not the wave**: the pre-reflect fan-out runs as its own stage *after* Stage 10 (Stages 8-10 mutate the phase files, so the pre-reflect cannot run inside that wave — see Decision B).

### Finding 3 — Rich deterministic structured signals already exist per tasklist

The generator computes, deterministically, for every task and every phase:

- **Compliance tier** STRICT/STANDARD/LIGHT/EXEMPT with priority order `STRICT(1) > EXEMPT(2) > LIGHT(3) > STANDARD(4)`. `SKILL.md:539-543`, `:5.3.*`.
- **Tier Distribution per phase** surfaced in the index "Phase Files" table (e.g., `STRICT: 2, STANDARD: 5, LIGHT: 1, EXEMPT: 0`). `SKILL.md:707-718`.
- **Total Phases / Total Tasks / Total Deliverables / Complexity Class (LOW|MEDIUM|HIGH)** in index metadata. `SKILL.md:681-684`.
- **Effort (XS..XL)** and **Risk (Low/Medium/High)** deterministic scores. `SKILL.md:488-534`.
- **Critical Path Override (Yes/No)** triggered by `auth/ security/ crypto/ models/ migrations/` paths. `SKILL.md:425-435`.
- **Roadmap Item registry `R-###`** (one per FR/requirement/bullet) and a **Traceability Matrix** mapping `R-### → T<PP>.<TT> → D-####`. `SKILL.md:161-164`, `:647-653`, `:759-773`.
- **File-touch signal** via the tier context booster ("Task affects >2 files: +0.3 toward STRICT"). `SKILL.md:596-604`.

These are exactly the signals reflect's own rubric consumes as `S_scope` (touched-file/item count), `S_domains` (distinct domains), and `S_dev_density`. `reflect SKILL.md:374-377`. So the tasklist generator can compute a depth tier **deterministically** and hand reflect a pre-decided `--depth`/`--tier` — no inference needed (see Recommended Design §4).

### Finding 4 — Reflect's surface: modes, depth, spec, model routing

- **UC-1 (`--mode pre`)** requires `--spec`; `--tasklist` recommended. Builds a spec→tasklist coverage matrix + gap registry *before* execution spend. ROI 200-500 tokens to save 5k-50k. `reflect SKILL.md:39`, `:99-100`, `command reflect.md:27`, `:160-169`.
- **UC-2 (`--mode post`)** requires `--diff` OR `--task-log`; audits completed work under the 4-category deviation taxonomy (authorized/necessary/drift/regression). `reflect SKILL.md:40`, `command reflect.md:28`.
- **`--depth quick|standard|deep`** maps to Tier-1-only / Tier-1-then-rubric / force-Tier-2. `reflect SKILL.md:73`, `:361-362`. **`--tier 1|2|auto`** is an explicit pin overriding the rubric. `reflect SKILL.md:74`, `:357-360`.
- **`--remediate`** offers the Tier-3 `task-builder` remediation chain (audit-first; never auto-executes). `reflect SKILL.md:78`, `command reflect.md:255-263`.
- **`--spec <path>`** is the driving spec/PRD. `reflect SKILL.md:67`, `command reflect.md:72`.
- **Model routing**: Tier-2 reviewers are heterogeneous **by model class**, resolved from `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL` env aliases via the Wave-0 0/1/2/3+ alias-routing table. `reflect SKILL.md:115-119`, `:216-228`. The **executor model class is excluded** from the reviewer pool via `--executor-model <class>` / `EXECUTOR_MODEL_CLASS` env / log heuristic. `refs/reviewer-spec.md:72-96`. Default reviewer rotation is `sonnet, haiku, (qwen|kimi|deepseek|opus)`. `refs/reviewer-spec.md:80-84`.
- **Cost bands**: T1 ≈ 3-8k Claude tokens / 1-3 min; T2 ≈ 35-70k / 8-15 min; T3 adds 20-40k. `refs/cost-profile.yaml:33-66`. This is why the **deterministic depth map** matters: keeping most phases at `quick`/`standard` (T1) instead of forcing `deep` (T2) on every phase is the primary cost lever. Reviewer model class is left to reflect's own env-alias routing — this proposal does not pin it.
- Reflect already accepts a **`--budget-remaining`** hint and will auto-downgrade tier — useful when the tasklist pre-gate fans out many phases at once. `reflect SKILL.md:82`, `:286-296`.

### Finding 5 — The POST task must be a real Sprint-CLI-compatible MDTM item

Phase files end with a **mandatory end-of-phase checkpoint as the last numbered task** (`### T<PP>.<last_num> -- Checkpoint: End of Phase <PP>`), and "No regular task may appear after the end-of-phase checkpoint." `SKILL.md:356-359`, `:1011-1027`, structural gate #19 (`SKILL.md:1114`). Every task carries a fixed metadata table (Tier, Verification Method, Sub-Agent Delegation, etc.) and a `### T<PP>.<TT>` heading that the Sprint task scanner discovers. `SKILL.md:862-916`. So the POST reflect item must be templated as a **conforming MDTM task** — and its placement must respect (or deliberately amend) the "checkpoint is last" invariant.

### Finding 6 — Memory constraints that bind this design

- **`feedback_sc_reflect_vs_inline_rfqa.md`**: sc:reflect's *independent heterogeneous ensemble* catches what same-context structural QA misses (spec-literal enum tokens, invariant arithmetic, parent-vs-head test state, orphaned/untested modules). The post gate's value depends on reviewer classes being **disjoint from the executor** — confirmed even when the orchestrator was Opus, because the load-bearing independence was sonnet/haiku reviewers. This motivates threading reflect's existing `--executor-model` exclusion (so the generator/orchestrator class is excluded from the reviewer pool); reviewer heterogeneity itself stays under reflect's own env-alias routing.
- **`feedback_human_decision_items_must_halt.md`**: "Always run `/sc:reflect --mode pre` on a freshly-built corrective tasklist before executing." Validates the PRE-gate placement (immediately post-generation). Also: `--remediate` Tier-3 output that contains `needs_human_decision` items must HALT, not auto-default.
- **`feedback_dryrun_skips_subskills.md`**: `--dry-run` on these pipelines hard-skips sub-skill invocations. The tasklist `--dry-run` path (if added) must explicitly state whether the reflect gates run — default: skip both, print "would run N pre-reflects + templated post-reflect".

---

## Socratic Questions (surfaced, then resolved)

1. **Where does "the spec" come from?** The generator is roadmap-driven and *optionally* spec-driven. `/sc:tasklist` exposes exactly **one** supplementary driving-doc flag — `--spec <path>` (`commands/tasklist.md:37`) — which accepts whatever the driving doc is (spec / PRD / TDD / roadmap); richer TDD/PRD paths can also be auto-wired from `.roadmap-state.json` (`SKILL.md:196-211`). There are **no** `--tdd-file`/`--prd-file` flags on the command. → *Resolved:* the `--spec` passed to reflect-pre is the **richest known driving doc** — the explicit `--spec` value when provided, else an auto-wired TDD/PRD from `.roadmap-state.json`, else the **roadmap itself** (always present, always the authoritative source-of-truth per `SKILL.md:57`) — while the specific `phase-<P>-tasklist.md` becomes reflect's `--tasklist` driver. See Recommended Design §3.
2. **Per-phase tasklist or per-bundle?** The generator emits *many* phase files. → *Resolved:* one pre-reflect **per phase file** (matching Stage 7's per-phase fan-out, `SKILL.md:1180-1193`), and one post-reflect task **per phase file** (each phase is a self-contained execution unit, `SKILL.md:846-848`).
3. **Does the pre-gate block generation?** Requirement #1 says no. → *Resolved:* generation (Stages 1-5) and the Stage 8-10 patch chain complete first — **no reflect runs while phase files are being generated or patched**. The pre-reflects fan out as a **new Stage 10.5**, *after* Stage 10, **in parallel across all N phase files at once**. Requirement #1 is satisfied because the fan-out is parallel across phases (it does not serialize per-phase) and runs after generation + patching, not interleaved with the mutation chain. Stage 9 patches the phase files via `sc:task --compliance strict` (`SKILL.md:1339-1357`), so a pre-reflect co-located with Stages 8-10 would race a file being patched — hence the fence to after Stage 10.
4. **What does a pre-reflect FAIL/remediate verdict do mid-bundle?** → *Resolved:* non-blocking-by-default. A FAIL annotates the index + writes a `reflect-pre/` finding artifact; `--remediate` offers a Tier-3 task but never auto-mutates the phase file (audit-first, `command reflect.md:255-263`). The bundle still ships; the operator sees a per-phase sign-off table.
5. **Is `depth` inferable deterministically, or must we ask the model?** → *Resolved:* fully deterministic from Finding 3 signals. Inference is not needed and is explicitly avoided.
6. **Fresh session for post-reflect — how, given it's an MDTM task?** → *Resolved:* the templated task's spawn directive instructs the Sprint executor to run reflect via `Skill`/subprocess with a fresh context; because reflect's post gate audits the *committed diff*, it is naturally cross-session-safe (it reads git state, not in-memory state). `reflect SKILL.md:469` notes cross-session reflect degrades only the optional `summarize_changes` corroboration, not the main verdict.

---

## Candidate Approaches per Decision

### Decision A — Insertion point: CLI pipeline vs skill protocol

| Approach | Pros | Cons |
|---|---|---|
| **A1. Skill-level only** (Stage 10.5 pre + templated post task) | Matches where generation actually happens (Finding 1); reuses existing `Task` fan-out (Finding 2); no CLI surface to touch | Skill-protocol behavior is inference-mediated, not Python-deterministic |
| A2. CLI-level | Deterministic Python orchestration | **Impossible today** — CLI `tasklist` is validate-only; no generation stage exists (`commands.py:15-96`) |
| A3. Hybrid (skill now, CLI later) | Forward-compatible | Adds spec surface for a CLI stage that doesn't exist |

**Merge → A1**, with an A3 forward-compatibility note. The CLI cannot host a pre-gate on generation because it does not generate.

### Decision B — Pre-reflect concurrency model

| Approach | Pros | Cons |
|---|---|---|
| B1. Co-located with Stages 7-10 — fan out the pre-reflects concurrently with the validation chain | Would overlap reflect with the validation chain | **Unsafe:** Stages 8-10 are a *sequential* chain and **Stage 9 mutates the phase files** (`sc:task --compliance strict`, `SKILL.md:1339-1357`, `:1415-1420`). A pre-reflect reading a phase file while Stage 9 patches it races a moving target; the coverage matrix is computed against pre-patch content that no longer exists. Rejected. |
| **B2. Fan-out-all-after-Stage-10** — generate, self-check, and run the entire Stage 7-10 validation+patch chain first, then fan out one pre-reflect per phase in a single parallel wave | Reflects run against *final, patched, validated* phase content; single clean join; no read/write race | Pre-reflects don't overlap the validation chain (but that chain is the part that mutates; overlap would be unsafe). Generation (the throughput-sensitive part) is still untouched. |
| B3. One bundle-level pre-reflect over all phases | Cheapest (1 agent) | Loses per-phase depth tuning; a single coverage matrix over a 9-phase bundle is exactly the "multi-domain single reviewer" case reflect's rubric escalates against (`reflect SKILL.md:388`) |

**Merge → B2.** Run the pre-reflect fan-out as **Stage 10.5**, a parallel wave (parallel across all N phase files) that starts only **after Stage 10 completes**. This is fenced after the patch chain because **Stage 9 rewrites the phase files** — the very content the pre-reflect audits — so co-locating with Stages 8-10 would race a file being patched (the staleness failure mode). Honest wall-clock: generation (Stages 1-5) is untouched (the real Req-1 guarantee), the Stage 7-10 chain runs as it already does, and the pre-reflects add a **bounded parallel stage after Stage 10** (one T1-ish pass per phase, fanned out at once — bounded by the slowest single phase's reflect, not the sum). The earlier "wall-clock = max(reflect, patch-chain)" / free co-location claim is **withdrawn**: there is no free overlap with the validation chain, because that chain mutates the files. Req #1 ("parallel agent so it doesn't slow tasklist creation") is still satisfied — the fan-out is parallel across phases and runs after generation, not interleaved with mutation.

### Decision C — Post-reflect placement in the phase file

| Approach | Pros | Cons |
|---|---|---|
| **C1. New highest-numbered task AFTER the end-of-phase checkpoint** | Reflect audits *everything including* the checkpoint; unambiguous "very last task" (Req #2) | Amends structural gate #19 ("checkpoint is last", `SKILL.md:1114`) — needs an explicit rule carve-out |
| C2. Fold reflect INTO the end-of-phase checkpoint task | No gate amendment | Checkpoints are LIGHT/100%-confidence read-only sanity checks (`SKILL.md:961-971`); overloading one with a heterogeneous-ensemble post-audit breaks its semantics |
| C3. One bundle-level post-reflect task in the last phase only | Single audit | Misses per-phase interaction effects; a phase that completes early waits for the whole bundle |

**Merge → C1 with an explicit gate amendment covering the full checkpoint-is-last invariant set.** The post-reflect becomes the new terminal task `### T<PP>.<final> -- Post-Execution Reflection (sc:reflect --mode post)`, emitted *after* `…Checkpoint: End of Phase <PP>`. The "checkpoint is last" assumption is encoded in **four** places, not just gate #19 — all must be amended together: **Self-Check check #6** (`SKILL.md:1073`, "every phase file ends with an end-of-phase checkpoint task"), **structural check #18** (`SKILL.md:1113`, sprint-scanner tie-in), **structural gate #19** (`SKILL.md:1114`, "checkpoint has the highest `<NN>`, no regular task following"), and **structural gate #20** (`SKILL.md:1115`, `_verify_checkpoints`/`build_manifest` tie-in). The amended invariant across all four becomes: "the end-of-phase **checkpoint** is the last *checkpoint*; the post-reflection task, when enabled, is the sole task permitted to follow it and is the absolute last task." This keeps the checkpoint's gating role intact while making reflect the true final action — and it audits the checkpoint's own output too. The verification step must confirm `_verify_checkpoints`/`build_manifest` and the Sprint phase-discovery regex tolerate "highest-numbered task may be a reflect task, not a checkpoint."

### Decision D — `depth` determination

| Approach | Pros | Cons |
|---|---|---|
| **D1. Deterministic complexity score → tier map** (from Finding 3 signals) | Reproducible; same input→same depth; no token cost; aligns with the skill's "no discretionary choices" mandate (`SKILL.md:33-38`) | Requires defining + justifying thresholds |
| D2. LLM infers complexity per phase | Flexible | Violates determinism; non-reproducible; the user explicitly wants deterministic |
| D3. Reuse the index "Complexity Class LOW/MEDIUM/HIGH" verbatim | Already computed | That field is bundle-level, not per-phase; too coarse for per-tasklist depth |

**Merge → D1.** Define a concrete per-phase `COMPLEXITY_SCORE` and a threshold table (Recommended Design §4). Inference is explicitly not used.

---

## Recommended Design

### 1. Insertion points (skill-level)

Two changes to `sc-tasklist-protocol`, plus one new flag on both `commands/tasklist.md` and the skill argument-hint.

**(a) New Stage 10.5 — "Pre-Reflect Sign-off" (parallel across phases, fenced after the patch chain).**
Inserted **after Stage 10** (the final roadmap re-verification, `SKILL.md:1359-1386`) — *not* concurrent with Stages 7-10. Stages 8-10 are a sequential chain and **Stage 9 mutates the phase files** (`sc:task --compliance strict`, `SKILL.md:1339-1357`, `:1415-1420`); running a pre-reflect concurrently would audit a file mid-patch. Stage 10.5 therefore starts only once the patch chain has landed, so every pre-reflect reads the final, validated phase content.

For each of the N phase files, dispatch one `Task` agent (in parallel — same primitive as Stage 7's 2N fan-out, `SKILL.md:1479`) that invokes:

```
/sc:reflect --mode pre --remediate \
  --tasklist TASKLIST_ROOT/phase-<P>-tasklist.md \
  --spec <RESOLVED_SPEC_PATH> \
  --depth <DETERMINISTIC_DEPTH_for_phase_P> \
  --tier <DETERMINISTIC_TIER_for_phase_P> \
  --output TASKLIST_ROOT/validation/reflect-pre/phase-<P>/
```

(The spawned reflect agents use the **default subagent model** — no model-routing flag is passed.)

Concurrency contract (satisfies Req #1):
- Stages 1-5 (generation) complete first; **no reflect runs during generation**, so generation throughput is untouched.
- The Stage 7-10 validation + patch chain then runs as it already does (Stage 9 mutates the phase files). **No pre-reflect overlaps this chain** — co-location would race a file being patched.
- At Stage 10.5, all N pre-reflects fan out **at once** as a single parallel wave across phases (the same `Task` primitive as Stage 7's 2N fan-out), writing only under `TASKLIST_ROOT/validation/reflect-pre/`. This adds a **bounded parallel stage after Stage 10** — its wall-clock is the slowest single phase's pre-reflect (a T1-ish pass), not the sum across phases, and not free overlap with the patch chain. Req #1 holds because the fan-out is parallel across phases and runs after generation, not interleaved with mutation.

Verdict handling (per phase, non-blocking):
- **PASS** → record `reflect_pre: PASS (depth=<d>, coverage=<pct>)` in a new index "Pre-Reflect Sign-off" table column.
- **PARTIAL/FAIL** → record the verdict + link the reflect REPORT.md; the bundle **still ships** (audit-first). Because `--remediate` is passed, reflect *offers* a Tier-3 `task-builder` remediation but never auto-mutates the phase file (`command reflect.md:255-263`). Any `needs_human_decision` item in that remediation HALTs per `feedback_human_decision_items_must_halt.md`.
- A bundle-level `reflect_pre_summary: {pass: x, partial: y, fail: z}` is written to the index metadata.

**(b) Templated POST task — generated into every phase file.**
During Stage 5 (File Emission), after the end-of-phase checkpoint, the generator appends one fixed terminal task. The checkpoint-is-last invariant set — **check #6, check #18, gate #19, and gate #20** — is amended together (Decision C1). Template:

```
### T<PP>.<final> -- Post-Execution Reflection: sc:reflect --mode post

| Field | Value |
|---|---|
| Roadmap Item IDs | <all R-### in this phase, comma-separated> |
| Why | Independent post-execution deviation audit of every task in Phase <PP>, in a fresh session, after all phase work completes. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT  (* reflect is the auditor; it is not itself tier-verified *) |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification (reflect IS the verification) |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | Required (fresh-session reflect ensemble) |
| Deliverable IDs | D-RF<PP> |

**Reflect Report Path:** `TASKLIST_ROOT/validation/reflect-post/phase-<PP>/REPORT.md`

**Spawn Directive (fresh session):** Spawn a NEW agent/session and run:
`/sc:reflect --mode post --remediate --tasklist TASKLIST_ROOT/phase-<PP>-tasklist.md --diff <phase-commit-range> --depth <DETERMINISTIC_DEPTH_for_phase_PP> --tier <DETERMINISTIC_TIER_for_phase_PP> --executor-model <EXECUTOR_CLASS> --output TASKLIST_ROOT/validation/reflect-post/phase-<PP>/`
(The reflect agent uses the default subagent model; `--executor-model` is the reflect-native exclusion flag naming the class that ran the phase's work, so reflect removes it from the reviewer pool — it does not select a model.)

**Steps:**
1. **[VERIFICATION]** Resolve `<phase-commit-range>` = the git range covering all of Phase <PP>'s task commits.
2. **[VERIFICATION]** Spawn a fresh session and invoke the Spawn Directive above (reflect audits the committed diff — cross-session-safe per reflect SKILL.md:469).
3. **[COMPLETION]** Confirm `REPORT.md` exists at the Reflect Report Path and surface its deviation counts (authorized/necessary/drift/regression).

**Acceptance Criteria:** (exactly 4 bullets)
- File `TASKLIST_ROOT/validation/reflect-post/phase-<PP>/REPORT.md` exists with a deviation-taxonomy summary.
- Zero `regression`-class deviations, OR a `--remediate` Tier-3 task was authored for each.
- Reflect ran with executor-disjoint reviewers (the `<EXECUTOR_CLASS>` passed via `--executor-model` was excluded from the reviewer pool).
- Report includes the per-task verdict matrix for Phase <PP>.

**Validation:**
- Manual check: reviewer confirms the deviation counts in REPORT.md.
- Evidence: the generated reflect REPORT.md.

**Dependencies:** all regular + checkpoint tasks in Phase <PP>.
**Rollback:** N/A (reflect is read-only audit; promotion is gated separately).
```

Why fresh session: reflect's UC-2 audits the **committed diff** (`--diff`), reading git state, not in-memory state — so a brand-new session has full fidelity. The only thing a cross-session reflect loses is the optional `summarize_changes` corroboration, which leaves the main verdict unchanged (`reflect SKILL.md:469`). This is precisely the independence the `feedback_sc_reflect_vs_inline_rfqa.md` memory shows is load-bearing.

### 2. Multi-tasklist handling

- **Pre gate:** one reflect agent **per phase file**, all in one parallel wave (Decision B2) at Stage 10.5 — after the Stage 7-10 patch chain, not sharing it. N phases → N pre-reflect agents fanned out at once.
- **Post gate:** one templated reflect task **per phase file** (Decision C1), each spawned fresh when that phase finishes — so an early-finishing phase is audited immediately, not blocked on the whole bundle.
- **Per-tasklist depth:** each phase gets its **own** deterministic depth (§4), because phase complexity varies wildly (a 3-task LIGHT docs phase vs an 18-task STRICT migration phase).

### 3. `--spec` threading (what counts as "the spec")

`/sc:tasklist` exposes exactly one supplementary driving-doc flag — `--spec <path>` (`commands/tasklist.md:37`) — which accepts whatever the driving doc is (spec / PRD / TDD / roadmap). There are no `--tdd-file`/`--prd-file` command flags; those exist only on the `superclaude tasklist validate` CLI and as `.roadmap-state.json` auto-wire keys consumed by the skill (`SKILL.md:196-211`).

Resolution order (deterministic), threaded into both gates, expressed in terms of what `/sc:tasklist` actually has:

1. **Reflect `--spec`** = the **richest available driving doc**, in precedence: the explicit command `--spec <path>` value when provided → an auto-wired TDD/PRD resolved from `.roadmap-state.json` (`SKILL.md:196-211`) → the **roadmap path itself** (always present; the generator's sole source-of-truth, `SKILL.md:57`).
2. **Reflect `--tasklist`** = the specific `phase-<P>-tasklist.md` under audit.

Rationale: reflect-pre needs *something more authoritative than the artifact it's grading* to compute a coverage matrix. The roadmap is that authority for tasklist generation, and a TDD/PRD (when wired via `--spec` or `.roadmap-state.json`) is richer still. If only the roadmap exists, `--spec roadmap.md --tasklist phase-P.md` is a valid UC-1 invocation (`reflect SKILL.md:100`, rule 5: `--spec` + `--tasklist` → UC-1). The generator already knows all these resolved paths at Stage 1, so threading is free.

> **Future extension (out of scope):** first-class `--tdd-file`/`--prd-file` flags on the `/sc:tasklist` command (mirroring the CLI-validate surface) are a possible future addition, but are explicitly **not** part of this proposal — `--spec` is the sole driving-doc flag used here.

### 4. Deterministic `depth` complexity formula (the core)

Computed **per phase file**, from signals the generator already produces (Finding 3). No inference.

**Per-phase signals** (all already computed/persisted during Stages 3-5, retrievable from the emitted artifacts):
- `n_strict` = count of STRICT-tier tasks in the phase (from the phase's Tier Distribution, `SKILL.md:707-718`).
- `n_tasks` = regular task count in the phase (excludes checkpoints + the post-reflect task).
- `n_cpo` = count of tasks with `Critical Path Override: Yes` (auth/security/crypto/models/migrations, `SKILL.md:425-435`).
- `n_high_risk` = count of tasks with `Risk: High` (`SKILL.md:529-531`).
- `n_R` = distinct `R-###` roadmap items traced into this phase (from the Traceability Matrix, `SKILL.md:759-773`, via a deterministic task-ID→phase join) — the FR/requirement coverage signal.

> **Dropped signal — `multifile`.** The earlier formula included a `1·multifile` term (count of tasks that tripped the ">2 files affected" tier booster, `SKILL.md:596-598`). That booster is a **transient input to tier scoring** — the generator computes a file count during Stage-4 enrichment but **does not persist** a "this task tripped the multifile booster" flag in any phase-file or index field (no such field in the task metadata table `SKILL.md:862-916` or the index registries `:707-773`). Recomputing it post-hoc would re-derive per-task file counts from task descriptions — the exact inference this formula avoids. It is therefore **dropped**: the signal is not reproducible from existing artifacts, and it is largely redundant with `n_strict` anyway (the >2-files booster pushes a task *toward* STRICT, so most multi-file blast radius is already captured by the `3·n_strict` term).

**COMPLEXITY_SCORE (integer, deterministic):**

```
COMPLEXITY_SCORE =
    3 * n_strict          # STRICT tasks dominate — security/data/breaking-change surface
  + 3 * n_cpo             # critical-path overrides are non-negotiable blast radius
  + 2 * n_high_risk       # High-risk tasks
  + 1 * ceil(n_tasks / 5) # raw size, bucketed by the checkpoint cadence (1 pt per 5 tasks)
  + 1 * ceil(n_R / 5)     # requirement coverage breadth, bucketed
```

(`n_strict`, `n_cpo`, `n_high_risk`, `n_tasks`, `n_R` are all non-negative integers retrievable from the emitted artifacts; the formula is a pure weighted sum, so it is fully reproducible — same bundle → same score.)

**Score → reflect tier map (per phase):**

| COMPLEXITY_SCORE | reflect `--depth` | reflect `--tier` | Rationale (tied to reflect's own rubric) |
|---|---|---|---|
| `0-3` | `quick` | `1` | Narrow, single-domain, no STRICT/CPO — reflect's rule-1 T1-stop case (`reflect SKILL.md:385`). T1 ensemble is sufficient. |
| `4-9` | `standard` | `auto` | Moderate — let reflect's §5.3 rubric decide T1-vs-T2 from its calibrated confidence (`reflect SKILL.md:381-393`). |
| `≥10` | `deep` | `2` | High blast radius (multiple STRICT/CPO or broad requirement coverage) — force the heterogeneous T2 ensemble. Mirrors reflect rubric rule 3/4 (regression/multi-domain MUST be debated, `reflect SKILL.md:387-388`). |

**Hard overrides (deterministic, applied before the table):**
- If `n_cpo ≥ 1` **OR** `n_strict ≥ 2` → floor the phase at `--depth deep --tier 2` regardless of score. (A security/migration/auth phase always gets the full ensemble — this is the asymmetric-cost rule from `reflect SKILL.md:420`: a missed regression on a critical-path phase is far worse than T2 tokens.)
- If `n_tasks == 0` (an empty/checkpoint-only phase) → **skip reflect entirely** for that phase (reflect's zero-task guard would STOP anyway, `reflect SKILL.md:300`).

**Band re-check after dropping `multifile`.** The dropped term had weight 1 and only ever *added* to the score, so its removal can only move a phase to a *lower* band — never a higher one — and it cannot affect the override (which keys on `n_cpo`/`n_strict`, not `multifile`). The override is therefore unchanged. The band **edges** also stay at `0-3 / 4-9 / ≥10`: they were calibrated against reflect's escalation rubric on the strict/cpo/risk/size/coverage axes, not on `multifile`. The only phases the drop moves downward are those that reached a band *purely* via the multifile term with zero STRICT/CPO/high-risk — and those are exactly the degenerate cases the >2-files→STRICT booster already routes into `n_strict` (×3). Worked checks unchanged by the drop: `n_cpo=1` alone → 3 → table `quick`, override rescues to `deep/T2` ✓; `n_strict=2` alone → 6 → table `standard`, override lifts to `deep/T2` ✓; a 10-task moderate phase (`n_strict=1, n_high_risk=1, n_tasks=10, n_R=5`) → `3+2+2+1 = 8` → `standard/auto` ✓ (was 9 with one multifile task — same band). No band edge needs adjustment.

**Why no inference:** every input is an integer the generator computes deterministically under its "no discretionary choices" mandate (`SKILL.md:33-38`). The formula is a fixed weighted sum with fixed thresholds. Two runs over the same roadmap produce identical depths. The thresholds are *justified* against reflect's own escalation rubric (the `≥10 → tier 2` band intentionally lines up with reflect's "multi-domain / regression must be debated" rules) so the tasklist-side decision and reflect-side rubric agree rather than fight. The composite is also written to `TASKLIST_ROOT/validation/reflect-pre/depth-map.yaml` for audit (mirroring reflect's own `tier_decision.yaml` recording convention, `reflect SKILL.md:396-413`).

### 5. Reflect agent model (no model-routing flag)

This proposal introduces **no** model-routing flag. The reflect agents spawned at the pre gate (Stage 10.5) and surfaced in the templated post task use the **default subagent model**. Reflect's reviewer heterogeneity is left entirely to its own env-alias routing (`reflect SKILL.md:216-228`, `refs/reviewer-spec.md:80-84`) — the tasklist orchestrator does not pin or select a reviewer cost class.

The one model-related flag that *is* threaded is reflect's existing **`--executor-model <class>`**, used only on the **post** gate. It is an *exclusion* flag, not a *selection* flag: it names the class that generated/executed the phase's work so reflect removes it from the reviewer pool (`refs/reviewer-spec.md:72-96`), preserving the executor-disjoint independence the memory (`feedback_sc_reflect_vs_inline_rfqa.md`) proves is load-bearing. The pre gate passes no `--executor-model` (no executor has run pre-execution).

Cost control is instead handled by the **deterministic depth map** (§4) — keeping most phases at `quick`/`standard` (T1) rather than forcing `deep` (T2) everywhere — plus `--budget-remaining` threading (`reflect SKILL.md:286-296`).

### 6. Flag/stage summary (exact surface changes)

- `commands/tasklist.md` Arguments table + skill `argument-hint`: add a `--no-reflect` escape hatch (default off; skips both gates — e.g. for `--dry-run`, per `feedback_dryrun_skips_subskills.md`). No model-routing flag is added (reflect agents use the default subagent model).
- Skill: **Stage 10.5** inserted (pre-gate fan-out, fenced after Stage 10); **Stage 5** templating extended (post task); the **checkpoint-is-last invariant set — check #6, check #18, gate #19, gate #20** — amended together (post-reflect may follow the end-of-phase checkpoint); **10-stage table → 11 stages**; new `depth-map.yaml` + `reflect-pre/`, `reflect-post/` under `TASKLIST_ROOT/validation/`.
- `--dry-run` (if/when added to tasklist) must explicitly print "would run N pre-reflects + template N post-reflect tasks" and run neither, per the dry-run-skips-subskills memory.

---

## Open Questions / Risks

1. **Checkpoint-is-last amendment risk (4-invariant set).** Making the post-reflect task follow the end-of-phase checkpoint changes a structural invariant encoded in **four** places — Self-Check check #6 (`SKILL.md:1073`), structural check #18 (`SKILL.md:1113`), gate #19 (`SKILL.md:1114`), and gate #20 (`SKILL.md:1115`) — which the Sprint CLI scanner and `_verify_checkpoints`/`build_manifest` tooling rely on. All four must be amended together (not gate #19 alone). Must confirm the Sprint executor treats "checkpoint is last *checkpoint*" vs "reflect is last *task*" correctly — i.e., that the manifest builder doesn't assume the highest-numbered task is always a checkpoint. **Mitigation:** gate the post-reflect task behind `--no-reflect`-off and validate against the sprint phase-discovery regex before shipping.
2. **`<phase-commit-range>` resolution.** The post-reflect template references a git range "covering all of Phase <PP>'s task commits," but the generator cannot know commit SHAs at generation time. **Mitigation:** the templated step resolves it at execution time (Sprint executor knows the phase's commit boundary); the generator emits a placeholder + resolution instruction, never a fabricated SHA (consistent with the skill's non-invention rule, `SKILL.md:933`).
3. **Cost amplification.** A 9-phase bundle now spawns up to 9 pre-reflect agents *and* 9 post-reflect ensembles. With the deterministic depth map (most phases land in `quick`/`standard` T1), this stays bounded, but a bundle full of STRICT/CPO phases forces T2 everywhere via the hard override — i.e., the override that makes the design *safe* is also the cost multiplier. **Mitigation:** thread `--budget-remaining` (reflect already honors it and auto-downgrades, `reflect SKILL.md:286-296`); make the pre-fan-out emit an estimated aggregate cost (sum the per-phase depth→cost-band from `cost-profile.yaml`) into the index as a **pre-dispatch gate**, not just a surfaced line, before fanning out.
4. **Pre-reflect on roadmap-only `--spec`.** When no TDD/PRD is wired, reflect-pre grades the phase against the roadmap — but the phase was *generated from* that roadmap, so coverage may look vacuously complete. **Mitigation:** this is still non-vacuous — reflect-pre checks best-practice compliance + gap registry, not just coverage (`reflect SKILL.md:39`), and the `feedback_human_decision_items_must_halt.md` instance shows pre-reflect catching spec-contradiction/human-decision issues even against the driving doc. Where a richer spec exists, wiring it as `--spec` strictly improves the signal.
5. **Pre-reflect placement vs the mutating patch chain.** The pre-reflect must NOT co-locate with Stages 8-10: Stage 9 rewrites the phase files via `sc:task --compliance strict` (`SKILL.md:1339-1357`, `:1415-1420`), so a concurrent pre-reflect would audit a file mid-patch (a read/write race against a moving target). **Mitigation (adopted in §1(a)):** fence the pre-reflect fan-out to **Stage 10.5**, after the patch chain lands, so every pre-reflect reads the final validated content. This costs the pre-reflect any overlap with the validation chain (the earlier "free co-location / max(reflect, patch-chain)" claim is withdrawn), but generation throughput (Stages 1-5) is still untouched, satisfying Req #1.
6. **Determinism of the depth map vs reflect's internal `--tier auto`.** For the `4-9` band we pass `--tier auto`, handing the final T1/T2 call to reflect's calibrated-confidence rubric — which is *not* deterministic (it depends on the model's calibrated score). **Trade-off accepted:** the *tasklist-side* depth decision is fully deterministic; we deliberately defer the *borderline* band to reflect's own rubric rather than over-fitting tasklist-side thresholds. The hard overrides (CPO/STRICT → forced deep) keep all high-stakes phases deterministic; only the genuinely-moderate middle band is delegated.
