# Frozen authoritative planning input

Grounding: source-only. This is a retrospective/context-limited packet; historical research is unavailable to the generator and source revisions may contain later edits. No live implementation, baseline, rubric, research solution, execution result or QA verdict is supplied. Treat paths/line references within original specs as historical context, not verified current code. Build a plan against the substantive requirements; equivalent plan organization is acceptable. Human decision gates remain gates, not automatic approval.

## Verbatim source — .dev/proposals/reflect-in-task-builder.md

# Proposal: Incorporate `/sc:reflect` into the `/task-builder` Pipeline

**Status:** Design proposal (no code changes). Produced via `/sc:brainstorm` protocol (Socratic dialogue → candidate approaches → adversarial merge).
**Date:** 2026-06-04
**Author surface:** `src/superclaude/skills/task-builder/SKILL.md` (single-file skill, 2191 lines) + `src/superclaude/skills/sc-reflect-protocol/` + `src/superclaude/commands/reflect.md`.
**Scope:** Add a PRE reflect gate after tasklist creation, a POST reflect gate templated as the final MDTM item, a `--spec` thread, and a **deterministic** depth-complexity mapping. Spawned reflect agents use the default subagent model (no model-routing flag is introduced).

---

## 1. Executive Summary

`/task-builder` currently ends its pipeline at three rf-* quality gates (research gate A.8, structural validation A.10, qualitative validation A.10.5) and then presents the tasklist (A.11). All three gates are **same-frame structural/isolation checks** — they verify a unit is *present + internally correct*, not that it is *spec-literal-correct, reachable, and regression-free*. The constraining memory `feedback_sc_reflect_vs_inline_rfqa.md` documents this blindspot caught **three separate times** past clean rf-qa runs. `/sc:reflect` is the cheapest independent anti-bias check that closes it.

This proposal wires reflect into task-builder at **two** points and adds **one** flag:

1. **PRE gate (new step A.10.7)** — after the qualitative gate passes and **before** A.11 (present results), task-builder spawns `/sc:reflect --mode pre --remediate` against the just-built tasklist (and `--spec` if known). This is an **advisory-blocking** gate: a `fail`/low-coverage verdict annotates the tasklist with a `reflect_pre` frontmatter block + an `### Open Questions` entry and surfaces a remediation offer, but does **not** auto-mutate the tasklist (respecting `feedback_human_decision_items_must_halt.md`). Sign-off is recorded in frontmatter.
2. **POST gate (templated last MDTM item)** — the builder (A.9) is instructed to make the **final phase's last checklist item** a *fresh-session* `/sc:reflect --mode post --remediate` handoff. The item does **not** run reflect inline in the executor's biased context; it writes a `reflect_post` PENDING sentinel and surfaces a paste-ready `/sc:reflect --mode post ...` command for the operator to run in a new session. This preserves the executor-disjoint independence that makes reflect non-vacuous.
3. **`--spec <path>`** — task-builder captures the spec/PRD/TDD path (from the BUILD_REQUEST, an `@file` GOAL reference, or an explicit `--spec` flag) and threads it into the PRE call and into the POST item's templated command.
4. **Deterministic `depth`** — a computable **Tasklist Complexity Score (TCS)** derived from observable tasklist signals maps to reflect's `--depth quick|standard|deep`. Inference is used only as a documented tiebreaker on one band boundary.

The spawned reflect agents simply use the **default subagent model**; this proposal introduces no model-routing flag and no "sonnet-by-default" override. Reflect's own Tier-2 reviewer heterogeneity (disjoint model classes from env aliases) is unaffected by anything task-builder does.

---

## 2. Current-State Findings (cited)

### 2.1 task-builder pipeline shape

- task-builder is a **single-file skill** with no `refs/`, `rules/`, or `templates/` subdirs — the entire protocol lives in `src/superclaude/skills/task-builder/SKILL.md` (verified: `find` returns only `SKILL.md`). There is **no command wrapper** under `src/superclaude/commands/` for task-builder (only the skill); it is invoked directly via `/task-builder` (SKILL.md:84).
- The pipeline is **Stage A only** — it stops after task-file creation; the user runs `/task <path>` (SKILL.md:11-13, 145).
- Pipeline steps end at: A.8 research gate → A.9 spawn builder → A.10 structural validation → A.10.5 qualitative validation → **A.11 present results** (SKILL.md:155-162, 1398-1433).
- The three existing gates are `rf-analyst` + `rf-qa` (research, A.8:600), `rf-qa` task-integrity (A.10:1128), `rf-qa-qualitative` task-qualitative (A.10.5:1194). All run in the **same orchestrator frame** — no model-class-disjoint reviewer.
- The builder is the `rf-task-builder` agent spawned via the Agent tool with a structured **BUILD_REQUEST** (A.9:781-789). BUILD_REQUEST already carries `QA_GATE_REQUIREMENTS`, `VALIDATION_REQUIREMENTS`, `TESTING_REQUIREMENTS`, `EXECUTION_CONTEXT_REQUIREMENTS` (SKILL.md:804-847).
- Critical Rule #16 (SKILL.md:2030) already establishes the pattern that **`QA_GATE_REQUIREMENTS` drives QA gate checklist items in the generated tasklist** — i.e., the builder already knows how to emit QA-gate items into the MDTM file. The POST reflect gate reuses this machinery.

### 2.2 Generated MDTM structure (where the POST item lands)

- The generated MDTM file ends with `## Phase N: [Final Phase — includes completion items]`, whose last item is `**N.X — Update task status to Done**` (SKILL.md:1928-1935).
- "Task completion items inside final phase (anti-orphaning)" is an enforced validation criterion (SKILL.md:1969). So the POST reflect item must sit **inside the final phase, immediately before** the status-to-Done item (the Done item must remain last per anti-orphaning, OR the reflect item becomes the final pre-Done item — see §6.2 decision).
- Items follow the **B2 self-contained pattern**: Context / Action / Output / Verification / Completion gate (SKILL.md:1916-1921, 1959).
- Frontmatter carries `id`, `status`, `created_date`, `related_docs`, `tags` (SKILL.md:1866-1885) — the natural home for a `spec_path` and `reflect_pre`/`reflect_post` sign-off block.

### 2.3 sc-reflect surface

- Modes: `--mode pre` (UC-1 coverage/gap audit; **requires `--spec`**) and `--mode post` (UC-2 deviation audit; requires `--diff` OR `--task-log`) (reflect.md:27-28, 72-74; input-resolution.md STOP conditions).
- **Depth → tier** mapping is fixed: `--depth quick` = Tier 1 only; `standard` = Tier 1 then escalate by §5 rubric; `deep` = **force Tier 2** (reflect.md:78; input-resolution.md `--depth` line). There is **no `depth=tier-3` value** — Tier 3 is the `task-builder` remediation chain, gated by `--remediate` + explicit user accept (reflect.md:89, 123, 255-263). So the task's "depth tiers 1/2/3" requirement maps to: **depth quick/standard/deep selects T1/T1-esc/T2**, and `--remediate` opts into the T3 chain.
- `--remediate` is **audit-first, no auto-execute**: reflect produces the report, then *offers* the Tier 3 chain; the operator runs `/task` themselves (reflect.md:255-263; remediation-handoff.md:92-111).
- **Model routing**: reflect resolves `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL` aliases at Wave 0 step 0.5 (input-resolution.md "Environment"; SKILL.md:216). Tier-2 **reviewer** classes come from a fixed rotation table (reviewer-spec.md "Reviewer rotation table": 2→`sonnet,haiku`; 3→`sonnet,haiku,(qwen|kimi|deepseek else opus)`). There is **no single `--model` flag today** that selects a reviewer class; the only model-related flag is `--executor-model <class>` which *excludes* the executor's class from the reviewer pool for anti-self-confirmation (reviewer-spec.md "Executor-class exclusion rule"; SKILL.md:572-574). This proposal does **not** add any reflect-side model flag — the spawned reflect agents use the default subagent model, and `--executor-model` is used only on the POST gate (where an executor has actually run).
- Reflect can **self-resolve the post diff** from `--diff`/`--commit-range`/`--scope`/done-marker artifacts (input-resolution.md 6-rule mode selection rules 2-4), and accepts `--tasklist` for the per-task verdict matrix.
- Cost bands (cost-profile.yaml): T1 ≈ 3-8k Claude tokens / 1-3 min; T2 ≈ 35-70k / 8-15 min; T3 adds 20-40k. **This is why depth must be deterministic and conservative — an over-classified `deep` on every tasklist is a 10× cost multiplier.**

### 2.4 Constraining memories (must-honor)

- `feedback_sc_reflect_vs_inline_rfqa.md` — the load-bearing independence is **executor-disjoint reviewer classes**, not the orchestrator. The POST gate is only non-vacuous if it runs in a session where reflect's reviewers differ from the tasklist's executor. → POST must be a **fresh session**, and the executor model class (the model that ran `/task`) must be passed to reflect's `--executor-model` so it can exclude that class from the reviewer pool. (This is a POST-only concern — there is no executor at PRE time.)
- `feedback_human_decision_items_must_halt.md` — generated items that need a human ruling must **HALT (PENDING sentinel)**, never auto-apply a default that mutates a spec/gate. → PRE-gate remediation must not silently rewrite the tasklist; POST item must HALT rather than auto-run + auto-promote.
- `feedback-no-sctask-on-task-builder-tasklists.md` — never `/sc:task` a task-builder tasklist; use `/task`. → The POST item's paste-ready command and A.11 output must say `/task` for execution and `/sc:reflect` for the gate — **never** `/sc:task`.

---

## 3. Socratic Questions (Wave 1)

1. **What is the PRE gate's authority?** Pure advisory (annotate + continue), hard-blocking (refuse to present until coverage ≥ floor), or advisory-blocking (annotate + surface remediation, never auto-mutate)? Memory says human-decision items must halt, not auto-fix → leans advisory-blocking.
2. **Does the PRE gate get the spec?** UC-1 *requires* `--spec` (it STOPs without one). If task-builder has no spec path, can it run UC-1 at all? → Need a coverage-only fallback or a graceful skip.
3. **Who runs the POST gate — task-builder or the tasklist?** task-builder ends at file creation; it never sees execution. So the POST gate can only be a **templated instruction** the executor encounters. But the executor *is* the biased frame reflect must avoid. → POST must be a fresh-session handoff, not an inline run.
4. **What context does POST need that only exists at build time?** The spec path, the tasklist path, and the intended diff range. The executor won't remember the spec. → These must be **baked into the templated command** at build time.
5. **Deterministic depth from what?** Which tasklist signals are (a) observable without inference, (b) monotonic in true complexity, (c) cheap to compute from the finished MDTM file? → §5 evaluates candidates.
6. **Cost ceiling?** Reflect at `deep` is ~10× `quick`. Running it on every build doubles task-builder's cost if mis-tiered. → The deterministic depth formula must bias toward the cheapest correct tier; reviewer heterogeneity and reviewer cost are left to reflect's own env-alias routing (task-builder does not pin reflect's model class).

---

## 4. Candidate Approaches (Wave 2 — parallel proposals per decision)

### Decision A — PRE gate authority

- **A1 — Hard-blocking gate.** Refuse A.11 until `reflect --mode pre` returns coverage ≥ floor. *Pro:* strongest guarantee. *Con:* violates `feedback_human_decision_items_must_halt` (auto-loop could rewrite the tasklist unattended); reflect UC-1 STOPs without a spec, so specless builds would deadlock; adds an unbounded loop.
- **A2 — Pure advisory.** Run reflect, print findings, always continue. *Pro:* simple, never blocks. *Con:* findings get ignored; loses the "sign-off" the requirement asks for.
- **A3 — Advisory-blocking with sign-off (CHOSEN).** Run `reflect --mode pre --remediate`; on `pass` → stamp frontmatter `reflect_pre: {verdict: pass, coverage_pct, run_id, ts}` and proceed to A.11. On `fail`/coverage-below-floor → stamp `reflect_pre: {verdict: fail, ...}`, append the `unmapped_requirements` list to the tasklist's `### Open Questions`, and surface (not auto-run) the `--remediate` Tier-3 offer at A.11. The build still **completes** (tasklist is presented) but is **marked not-signed-off**, and the operator decides. *Pro:* honors halt-don't-auto-mutate; records sign-off; no deadlock on specless builds (degrades — see Decision C). *Con:* a careless operator can run an unsigned tasklist (mitigated by loud A.11 banner).

### Decision B — POST gate delivery

- **B1 — Pipeline-orchestrated post-run.** task-builder itself schedules reflect after `/task` finishes. *Con:* task-builder has no execution phase and no hook into `/task` completion (SKILL.md:11-13). Architecturally impossible without a new daemon. Rejected.
- **B2 — Inline final item that runs reflect in-context.** Last MDTM item calls reflect inside the executor's session. *Con:* destroys executor-disjoint independence — the memory's core finding is that the *executor's frame* is exactly what reflect must escape. Rejected.
- **B3 — Templated fresh-session handoff item (CHOSEN).** The builder emits a final-phase item that (1) writes a `reflect_post: PENDING` sentinel to frontmatter, (2) computes the post diff range, (3) surfaces a paste-ready `/sc:reflect --mode post --remediate ...` command for the operator to run **in a new session**, and (4) HALTs (does not mark Done) until the operator records the verdict. *Pro:* preserves independence; honors halt; needs no daemon. *Con:* relies on the operator actually running the surfaced command — mitigated by making it the explicit completion gate of the item.

### Decision C — `--spec` capture when absent

- **C1 — Require `--spec`.** *Con:* most task-builder invocations are natural-language goals with no spec; would block the common path. Rejected.
- **C2 — Best-effort capture + graceful degrade (CHOSEN).** Capture spec path from, in priority order: explicit `--spec <path>` flag → `@file` reference in the GOAL → a `SPEC`/`PRD`/`TDD` field in a BUILD_REQUEST file → none. If a spec path resolves, run PRE as full UC-1. If none, run PRE in reflect's **coverage-only** mode using `--tasklist` alone is *not* valid (UC-1 STOPs without `--spec`) — so when no spec exists, **skip the UC-1 coverage audit and instead run a lighter `reflect --mode pre` self-consistency pass only if a spec later appears**, otherwise record `reflect_pre: {verdict: skipped, reason: no-spec}` and proceed. (Honest: PRE's coverage value is spec-dependent; no spec ⇒ no coverage audit, only the structural rf-* gates apply.)

### Decision D — depth determination

- **D1 — LLM infers complexity.** *Con:* the user explicitly wants deterministic; inference is non-reproducible and drifts.
- **D2 — Single signal (item count) → depth.** *Pro:* trivially deterministic. *Con:* item count alone misranks (40 trivial doc items vs 8 cross-subsystem refactor items).
- **D3 — Weighted multi-signal score with fixed thresholds (CHOSEN).** A computable **Tasklist Complexity Score (TCS)** over 6 observable signals → `quick`/`standard`/`deep`. Fully reproducible from the finished MDTM file + BUILD_REQUEST. Inference used only as a one-boundary tiebreaker (§5.4).

---

## 5. Recommended Design — Deterministic Depth (the hard part)

### 5.1 Signal selection (what to count and why)

Computed **after** the tasklist is built (A.10.5 complete) so all signals are observable from the finished MDTM file + the BUILD_REQUEST. Each signal is chosen for monotonicity in *audit* complexity (how hard the tasklist is to independently verify), not raw size.

Each signal below carries a **frozen extraction rule** (FER) — an exact, testable procedure so two implementers compute the same integer from the same MDTM file + BUILD_REQUEST. The arithmetic was already deterministic; these FERs make the *inputs* deterministic too (closing the audit's R4 / "byte-reproducible" gap).

| # | Signal | Frozen extraction rule (deterministic) | Why it predicts audit complexity | Weight |
|---|--------|----------------------------------------|----------------------------------|--------|
| S1 | **Distinct files touched** | Apply regex `(?:[\w.-]+/)+[\w.-]+\.[\w]+` to the MDTM body **excluding fenced code blocks** (```` ``` ```` … ```` ``` ````) and excluding the `### Open Questions` section; lowercase, strip a trailing `:\d+` line suffix, then dedupe by exact string. S1 = count of the deduped set. | Breadth of the surface reflect must re-ground and re-Read | ×3 |
| S2 | **Distinct subsystems** | From the S1 deduped set, take **exactly the first 2 path segments** (or all segments if the path has <2 dir segments) as the subsystem key; dedupe. S2 = count of distinct keys. The "first 2 segments" count is fixed (no 1-or-2 discretion). | Cross-cutting changes are where drift/regression hide | ×4 |
| S3 | **FR/NFR count in spec** | If `--spec` known: extract all `FR-\d+`/`NFR-\d+` tokens from the spec file and count **distinct IDs** (not raw occurrences — `FR-1` cited 5× counts once). Else 0. | Each requirement is a coverage row reflect must map | ×2 |
| S4 | **Inter-task dependencies** | Count occurrences of the **fixed dependency-token set** `{after Phase \d+, blockedBy:, depends on N\.\d+, after N\.\d+}` (case-insensitive, anchored to those literal forms only — no open-ended "explicit item ref" inference) across all items. | Dependency depth → more verdict-matrix coupling | ×2 |
| S5 | **Human-decision / Open-Question-blocked items** | Count the **distinct Open-Question indices that are referenced from an item's Context field** — i.e. the TB-Add-3 pattern "each blocked item references its blocking Open Question by index in Context" (validation checklist SKILL.md:1974; rule SKILL.md:1168). Concretely: count distinct `OQ-\d+` (or `Open Question \d+`) tokens that appear in a checklist item's Context line AND have a matching entry under the tasklist's `### Open Questions` section. If the tasklist emits a `### Open Questions` section but no in-Context index references, fall back to the count of non-empty `### Open Questions` entries. (The prior `needs_human_decision` flag does **not** exist in generated output — `grep` returns 0 — so it is replaced by this real, emitted pattern.) | Each is a halt-point reflect must check did NOT auto-resolve (per memory) | ×5 |
| S6 | **Risk/security/regression annotations** | Read the tasklist's single frontmatter `type:` field (a **file-level** field, SKILL.md:1871, real emitted values include `type: "🔧 Refactor"`); S6 = **1 if `type` is a refactor/remediation-class value** (`🔧 Refactor`, `♻️ Refactor`, `🔨 Refactor`, `🔧 Remediation`, or `Code Remediation` — the verified real-corpus refactor variants), **else 0**. This is a 0-or-1 file-level signal, not a per-item count. (Replaces the prior per-item `type`/`tags` test: `type` is a single frontmatter field, not a per-item attribute, and the `{security,risk,regression,breaking-change}` `tags:` set is **not** confirmed in generated output — frontmatter `tags` are free-form placeholders, SKILL.md:1882-1884 — so anchoring S6 to `tags` would be inert.) | Regression-class deviations force reflect Tier-2 escalation anyway (remediation-handoff.md:122) | ×4 |

**Dropped candidates (with rationale):** *Checklist item count* alone (D2) — non-monotonic, folded in only via the §5.3 cap rule; *estimated LOC* — not deterministically derivable from an MDTM file (no code yet); used the dependency/subsystem signals instead. *Parallel-wave / subagent-spawn markers* (the former **S7**, ×2) — **dropped**: the `spawn in SAME message` marker it counted is a task-builder *research-orchestration* instruction (SKILL.md:418, 485) and a Content-Rules table-cell description (SKILL.md:1991), **not** content emitted into the generated MDTM file. Verified against three real generated tasklists (`.dev/tasks/.../TASK-RF-*.md`): the literal `spawn in SAME message` has **0 occurrences** in tasklist bodies, so S7 computed to 0 on every real tasklist and was inert. Concurrency breadth is already partially captured by S1/S2. The 2·S7 term is removed from the formula (§5.2); since the operand was always 0, the band thresholds are unaffected (see §5.3 re-check).

### 5.2 The TCS formula

```
TCS = 3·S1 + 4·S2 + 2·S3 + 2·S4 + 5·S5 + 4·S6
```

All S* are non-negative integers read directly from the tasklist/spec. The formula is pure arithmetic — no inference. Weights encode "audit-difficulty per unit," with human-decision (S5) and risk (S6) weighted highest because they are exactly the classes that flip reflect to Tier 2 / make it non-vacuous. (The former S7 parallel-wave term was dropped — see §5.1 "Dropped candidates" — because its marker is never emitted into generated tasklists.)

### 5.3 Threshold table (TCS → reflect `--depth`)

| TCS range | reflect `--depth` | reflect tier reached | Rationale |
|-----------|-------------------|----------------------|-----------|
| **TCS ≤ 12** | `quick` | Tier 1 only | Small, single-subsystem, no human-decision/risk items. A single grounded pass suffices. |
| **13 ≤ TCS ≤ 34** | `standard` | Tier 1, escalate-by-rubric | Moderate breadth; let reflect's own §5 rubric decide if it needs T2. |
| **TCS ≥ 35** | `deep` | Tier 2 (forced) | Cross-subsystem, dependency-heavy, or carries human-decision/risk items — heterogeneous ensemble required. |

**Band re-check after dropping S7.** The thresholds (≤12 / 13–34 / ≥35) are **unchanged** by the S7 removal. The dropped term `2·S7` contributed 0 to TCS on every real tasklist (the `spawn in SAME message` marker is never emitted — see §5.1), so the computed TCS for any actual MDTM file is identical before and after the drop; the three bands therefore partition exactly as before. The remaining live signals span a realistic envelope: the worked TASK-RF-20260602-135209 tasklist yields S1≈8 distinct files (×3=24), S2=1 subsystem (first-2-segment key `src/superclaude`; ×4=4), S3≈8 distinct FR/NFR IDs from its spec (×2=16), S4≈2 dependency tokens (×2=4), S5=5 OQ-indexed items (referenced `OQ-1`..`OQ-5`; ×5=25), S6=0 (`type: 📝 Documentation`, not refactor) → TCS≈73 ⇒ `deep`, with O1 (S5>0) independently flooring ≥ `standard` — a dependency-heavy, multi-OQ tasklist correctly lands in `deep`. A trivial single-file doc fix (S1=1→3, all else 0) yields TCS=3 ⇒ `quick`. Boundaries remain contiguous and non-overlapping.

**Hard overrides (deterministic, take precedence over the band):**

- **O1 — Any `S5 > 0` (human-decision item) ⇒ floor `--depth standard`.** A halt-point must get at least the rubric-escalation path (honors `feedback_human_decision_items_must_halt`).
- **O2 — `S6 = 1` (file-level `type:` is a refactor/remediation-class value) ⇒ force `--depth deep`.** Matches reflect's own unconditional-T2 rule for regression-class surfaces (remediation-handoff.md:122). (S6 is a 0-or-1 file-level signal per §5.1, so "any S6 > 0" ≡ "S6 = 1".)
- **O3 — Item-count cap:** if checklist item count > 40 (single-track > 50; TB-Add-2 bounds, SKILL.md:1973) ⇒ floor `--depth standard` even if TCS low (a large tasklist is never "quick" to audit).
- **O4 — POST-gate depth floor (HARD RULE, no exceptions):** the **POST gate depth ∈ {standard, deep}** — it may **NEVER** be `quick`. `--depth quick` is a hard override that disables reflect's regression-escalation rubric (reflect §5.1: quick = "STOP at T1, skip Wave 3+"); the POST gate audits *executed code*, which is exactly where regression-escalation matters most and exactly the blindspot class `feedback_sc_reflect_vs_inline_rfqa.md` documents. So when the TCS band yields `quick`, the **POST** command is emitted with `--depth standard` (the PRE call may still use `quick`, since no diff exists pre-execution). This floor takes precedence over the band and over O3's "low TCS" path for the POST gate only.

### 5.4 Where inference still enters (and why it's bounded)

Given the frozen extraction rules (FERs) in §5.1, the TCS is **deterministic at both the input and arithmetic levels** — two implementers reading the same MDTM file + BUILD_REQUEST + spec produce the same integer. The S2 FER ("exactly the first 2 path segments") removes the prior 1-or-2-segment discretion, so subsystem counting is now itself frozen. The only residual judgement is *interpretive*: whether two FER-distinct subsystem keys (e.g. `src/superclaude` for `cli/` vs `execution/` — same package, arguably one logical subsystem) "should" collapse. S2 has weight ×4, so a ±1 disagreement here moves TCS by ±4 and can flip a band.

**Resolution (bounded to S2's actual leverage):** within **±4 TCS of a threshold** (8–16 around the 12 edge, 31–39 around the 35 edge) — the span an S2 ±1 disagreement can actually traverse — the orchestrator may apply a single bounded inference: "are these N FER-distinct dirs truly distinct *logical* subsystems?" recorded as `tcs_boundary_inference: {applied: true, from: standard, to: deep, reason: ...}` in the sign-off block for auditability. Outside the ±4 band, **no inference is permitted**. Every classification is therefore **deterministic given the frozen FERs**, with interpretive inference confined to the explicit ±4 windows around each band edge.

### 5.5 Both gates use the same TCS (POST floored at standard)

The PRE gate (A.10.7) and the templated POST command both derive `--depth` from the same TCS. **The PRE call carries the raw TCS-derived depth (`quick`/`standard`/`deep`); the POST command carries `max(tcs-derived, standard)` per O4** — so a low-TCS tasklist still gets `--depth quick` at PRE but `--depth standard` at POST, never `quick`. The POST diff at execution time may be larger than predicted, but TCS computed at build time is the best deterministic estimate; reflect's own `--budget-remaining`/rubric can still up-grade at run time (and the O4 floor guarantees it is never *down*-pinned below `standard` for executed code).

---

## 6. Recommended Design — Pipeline Wiring

### 6.1 PRE gate — new step **A.10.7** (between A.10.5 and A.11)

**Insertion point:** immediately after the qualitative gate (A.10.5:1194) passes and before A.11 present-results (SKILL.md:1398). New pipeline-overview bullet between current steps 12 and 13 (SKILL.md:160-162).

**Behavior:**

1. Resolve `spec_path` per Decision C2. Compute TCS per §5 → `pre_depth`.
2. Spawn reflect via the **Agent/Task tool** (default subagent model), invoking `Skill sc:reflect-protocol` with:
   ```
   --mode pre --remediate
   [--spec <spec_path>]            # omitted ⇒ verdict: skipped (no-spec)
   --tasklist <TASK_FILE>
   --depth <pre_depth>            # raw TCS-derived depth; quick permitted at PRE
   --output ${TASK_DIR}reflect/pre/
   ```
   **No `--executor-model` is passed at PRE** — in `--mode pre` no executor has run, so excluding an executor class is a category error (the audit's G2). `--executor-model` is a POST-only concern (§6.2). (Direct skill invocation, mirroring how `/sc:brainstorm` Wave 3 invokes `Skill sc-adversarial-protocol` — brainstorm SKILL.md:278.)
3. **Consume the reflect return contract** (`status`, `coverage_pct`, `unmapped_requirements`, `run_id`).
4. **Verdict routing (advisory-blocking, Decision A3):**
   - `coverage_pct ≥ coverage-floor` (default 0.90) AND `status` not failed → stamp frontmatter and proceed to A.11.
   - else → stamp `verdict: fail`, append `unmapped_requirements` to the tasklist's `### Open Questions` (via Edit, additive — **never** rewrite existing items, per halt-don't-mutate), and carry the `--remediate` Tier-3 offer into A.11. Build still completes; tasklist flagged not-signed-off.
   - no spec → `verdict: skipped`, proceed (the rf-* gates remain the only coverage check).
5. **Sign-off recording** — add to the generated tasklist frontmatter:
   ```yaml
   reflect_pre:
     verdict: pass | fail | skipped
     coverage_pct: <float | null>
     depth: quick | standard | deep
     tcs: <int>
     run_id: <reflect run id>
     report: ${TASK_DIR}reflect/pre/report.md
     reviewed_at: <ISO-ts>
   ```
6. **Loop policy:** max **0 auto-loops** — the PRE gate never re-invokes the builder automatically (avoids the unattended-mutation failure mode). A `fail` verdict is surfaced for operator action only. (Contrast: rf-* gates have bounded auto-fix; reflect's findings are spec-level and may require human judgment.)

### 6.2 POST gate — templated final MDTM item

**Threaded via BUILD_REQUEST (A.9).** Add a new BUILD_REQUEST field and a new Critical Rule so the `rf-task-builder` agent emits the item deterministically (reusing the Rule #16 QA-gate-emission machinery, SKILL.md:2030):

New BUILD_REQUEST field (strictly-additive, after `EXECUTION_CONTEXT_REQUIREMENTS`):
```
POST_REFLECT_GATE: ENABLED
  SPEC_PATH: <spec_path or NONE>
  DEPTH: <max(tcs-derived depth, standard)>   # POST floor per O4 — never quick
  TASK_FILE: ${TASK_FILE}
```

New Critical Rule (companion to #16/#17/#18): *"When `POST_REFLECT_GATE: ENABLED`, the builder MUST emit, as the penultimate item of the final phase (immediately before the `Update task status to Done` item, preserving anti-orphaning per the validation checklist), a fresh-session reflect handoff item. The item MUST NOT run reflect inline; it writes a `reflect_post: PENDING` sentinel and HALTs until the operator records the verdict."*

**Templated item shape** (B2 self-contained, lands at `Phase N`, position `N.(X-1)`):

```markdown
- [ ] **N.{X-1} — Independent post-execution reflection gate (fresh session)**
  - **Context**: All implementation/test/QA items above are complete. The inline
    rf-qa gates ran in THIS executor's frame and cannot perform an executor-disjoint
    audit. Per project memory `feedback_sc_reflect_vs_inline_rfqa`, an independent
    `/sc:reflect --mode post` ensemble catches spec-literal-token, invariant-arithmetic,
    and integration/orphan blindspots that same-frame QA misses.
  - **Action**: Do NOT run reflect inside this session. Write `reflect_post: PENDING`
    to this file's frontmatter, then STOP and surface this paste-ready command for the
    operator to run in a NEW session:
    `/sc:reflect --mode post --remediate --diff <BASE>..HEAD --tasklist {TASK_FILE} [--spec {SPEC_PATH}] --depth {DEPTH} --executor-model {EXECUTOR_CLASS}`
    where <BASE> is the commit recorded at task start (frontmatter `start_commit`,
    or `git merge-base HEAD <integration>` if unset), and `{DEPTH}` is floored at
    `standard` per O4 (the POST gate never runs `--depth quick`). The spawned reflect
    agent uses the default subagent model — no model-routing flag is passed.
  - **Output**: Frontmatter `reflect_post: PENDING`; paste-ready reflect command surfaced.
  - **Verification**: `reflect_post` is PENDING and the operator has been given the
    exact `/sc:reflect` command. Item does NOT self-resolve.
  - **Completion gate**: Operator has run `/sc:reflect --mode post` in a fresh session
    and recorded its verdict (`reflect_post: {verdict, run_id, report}`). Only THEN may
    the next item mark the task Done. (HALT per `feedback_human_decision_items_must_halt`.)
```

**Why a templated command and not an inline run:**
- *Fresh session* — the operator runs it in a new Claude session, so reflect's reviewers are disjoint from the tasklist's executor (the load-bearing independence).
- *`--executor-model {EXECUTOR_CLASS}`* — the executor's model class (the model that ran `/task`) is passed so reflect's executor-exclusion rule (reviewer-spec.md) removes it from the reviewer pool. `{EXECUTOR_CLASS}` is left as a literal placeholder the operator fills (or `EXECUTOR_MODEL_CLASS` env), since the build-time skill cannot know which model the operator will use for `/task`.
- *`--diff <BASE>..HEAD`* — gives reflect the work to audit; reflect self-resolves UC-2 from `--diff` (input-resolution.md rule 2).
- The command uses `/sc:reflect` for the **gate** and the surrounding tasklist is run with `/task` — **never `/sc:task`** (per `feedback-no-sctask-on-task-builder-tasklists`).

### 6.3 `--spec` capture (Decision C2)

task-builder resolves `spec_path` at A.2 (parse & triage, SKILL.md:190) in priority order: explicit `--spec <path>` → `@file` in GOAL → `SPEC:`/`PRD:`/`TDD:` field in a BUILD_REQUEST file → none. The resolved path is stored in the task folder state, written to tasklist frontmatter as `spec_path:`, threaded into the A.10.7 PRE call's `--spec`, and into the POST item's `{SPEC_PATH}` placeholder. If none resolves, both gates degrade per C2 (PRE `verdict: skipped`; POST omits `--spec`, running UC-2 diff-only).

### 6.4 Reflect agent model

No model-routing flag is introduced. The reflect agents spawned at the PRE gate (and surfaced in the POST command) use the **default subagent model**. `--executor-model` on the POST command is *not* a model-selection flag — it merely names the executor's class so reflect *excludes* it from the reviewer pool (reviewer-spec.md). Reflect's Tier-2 reviewer heterogeneity (disjoint classes from env aliases) is unaffected by task-builder.

### 6.5 A.11 present-results additions

Add a `REFLECT GATES` block to the A.11 output (SKILL.md:1404-1433):
```
REFLECT GATES:
  PRE  (--mode pre):  [PASS coverage=0.94 depth=standard tcs=22] | [FAIL ...] | [SKIPPED no-spec]
  POST (--mode post): TEMPLATED as final-phase item N.{X-1}  (operator runs in fresh session)
```
If PRE `verdict: fail`, A.11 surfaces the literal `/sc:reflect --mode pre --remediate ...` re-run command and the Tier-3 `--remediate` offer (operator-run, never auto).

---

## 7. Open Questions / Risks

1. **`{EXECUTOR_CLASS}` is unknown at build time.** The operator may run `/task` with any model. The POST command leaves it as a placeholder + falls back to reflect's `EXECUTOR_MODEL_CLASS` env / log-heuristic (reviewer-spec.md fail-open). Risk: if the operator omits it, reflect emits `executor_class_resolved: false` (weakened but not broken). *Mitigation:* the item's Context names the env var.
2. **PRE on specless builds adds little.** Without `--spec`, UC-1 coverage is N/A and PRE degrades to `skipped`. The value-add for the common natural-language build is then only the POST gate. Acceptable — the POST gate is where the documented blindspots were caught.
3. **TCS weight calibration is initial, not empirical.** The weights (S1..S6 = ×3/×4/×2/×2/×5/×4) and thresholds (12/34) are reasoned, not measured. They should be tuned against a corpus of past TASK-RF folders (count TCS vs. whether reflect actually escalated/found issues). Recommend shipping behind the deterministic formula and recording `tcs`/`depth`/actual-tier-reached in the sign-off block to build that corpus.
4. **Cost of always-on PRE.** Even a `quick` PRE adds ~3-8k tokens/1-3 min per build (cost-profile.yaml T1). For trivial Template-01 builds this may be unwanted. *Option:* gate A.10.7 behind a `--reflect-pre/--no-reflect-pre` toggle (default on); out of scope for this proposal's required flags but a cheap addition.
5. **Anti-orphaning interaction.** The validation checklist requires completion items inside the final phase (SKILL.md:1969). Placing the reflect item as penultimate (before Done) is compatible, but the A.10 structural validator's rule set may need a companion check that the reflect item, when `POST_REFLECT_GATE: ENABLED`, is present and correctly positioned — otherwise a builder that drops it is silently non-compliant (mirror Rule #16's "MALFORMED if QA gate omitted").
6. **Two-track / multi-track builds** each get their own PRE gate and their own templated POST item (per-track TCS). The A.11 multi-track format (SKILL.md:1436) needs a per-track `REFLECT` row.

---

## 8. Implementer Checklist (concrete deltas)

1. `src/superclaude/skills/task-builder/SKILL.md`:
   - Add `--spec` to the Input/flags surface.
   - A.2: spec_path resolution (§6.3).
   - New **A.10.7 PRE reflect gate** between A.10.5 and A.11 (§6.1) + pipeline-overview bullet.
   - A.9 BUILD_REQUEST: add `POST_REFLECT_GATE` block (§6.2) + new Critical Rule (companion to #16).
   - Output Structure: add `reflect_pre`/`reflect_post`/`spec_path` frontmatter; add the penultimate reflect item to the `Phase N` example (§6.2).
   - Task File Validation Checklist: add "POST reflect item present + positioned when enabled" (promote the Rule #16-style MALFORMED guard from a risk note — see §7 risk 5).
   - A.11: `REFLECT GATES` block (§6.5).
   - Add the deterministic TCS formula (with frozen extraction rules) + threshold table + overrides (incl. the O4 POST-depth floor) as a new `## Reflect Depth (Deterministic TCS)` section (§5).
2. Honor SoT: edit `src/superclaude/` only, then `make sync-dev` + `make verify-sync`. Never stage `.claude/`.
3. **No change required to `sc-reflect-protocol`.** This proposal uses only reflect's existing surface: `--mode pre/post`, `--spec`, `--tasklist`, `--depth`, `--diff`, and `--executor-model` (POST only). No reflect-side model-routing flag is introduced; spawned reflect agents use the default subagent model.
```


## Verbatim source — .dev/proposals/reflect-in-sc-tasklist.md

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


## Binding human supplement (selected source excerpts only)

Source excerpt: .dev/tasks/done/TASK-RF-20260604-042055/research-notes.md, line 22

- **S4 TOKEN-SET TRIM (in-scope cleanup, user-mandated):** S4 dependency-token set in the proposal is `{after Phase \d+, blockedBy:, depends on N\.\d+, after N\.\d+}`. TRIM to **drop `blockedBy:` and `after N\.\d+`, KEEP `after Phase \d+` and `depends_on:`** → final S4 set = `{after Phase \d+, depends_on:}`. (Rationale: blockedBy:/after N.N are not real emitted patterns, mirroring the proposal's own S7/multifile drops.) Note `depends_on:` (underscore) replaces the proposal's prose `depends on N.\d+`.
