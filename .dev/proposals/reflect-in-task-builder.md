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
