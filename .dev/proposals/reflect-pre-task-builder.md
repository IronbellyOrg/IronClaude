# Reflect Pre-Execution Audit (UC-1) — `reflect-in-task-builder.md`

**Mode:** UC-1 (pre-execution coverage / gap / best-practice audit)
**Source proposal:** `.dev/proposals/reflect-in-task-builder.md` (286 lines)
**Driving spec:** user's 5-requirement requirement set (no separate spec file)
**Grounded against:** `src/superclaude/skills/task-builder/SKILL.md` (2191 lines), `src/superclaude/skills/sc-reflect-protocol/SKILL.md` + `refs/`, `src/superclaude/commands/reflect.md`
**Tier reached:** Tier 1 (single grounded pass; high citation density, no escalation trigger)
**Date:** 2026-06-04

---

## Verdict: **PARTIAL**

The proposal is unusually well-grounded — its citations into both task-builder and sc-reflect are accurate, it correctly honors all three constraining memories, and its honesty about what does/does not exist in reflect today is verbatim-correct. The depth-determinism design is structurally defensible and cross-aligned to reflect's own escalation rubric.

It does **not** pass clean because **three gaps are load-bearing on the required behavior** and must close before implementation:

- **G1 (CRITICAL):** the spawn mechanism the whole `--reflectagent` flag + PRE gate rests on (`model:` on the Agent/Task spawn) is asserted but never grounded, and contradicts every spawn example in task-builder.
- **G2 (HIGH):** `--executor-model` is misapplied in `--mode pre` — there is no executor pre-execution, so passing the reflect orchestrator's own class is a category error.
- **G3 (HIGH):** 5 of the 7 TCS signals have unspecified extraction rules, so "byte-reproducible determinism" is overstated; and the `--depth quick` path can actively *suppress* reflect's own regression escalation — dangerous when the same TCS is reused for the POST gate on executed code.

---

## Coverage Assessment — the 5 driving requirements

| # | Requirement | Status | Evidence |
|---|-------------|--------|----------|
| R1 | Incorporate `/sc:reflect --mode pre --remediate` into `/task-builder`, run after tasklist creation, validate + sign off | **PARTIAL** | Covered as new step **A.10.7** between A.10.5 (`SKILL.md:1194`) and A.11 (`SKILL.md:1398`), advisory-blocking with frontmatter sign-off (proposal §6.1). Insertion point is real and correctly placed. **Gap:** the spawn (`model:` + `Skill sc:reflect-protocol` via Agent/Task tool, proposal §6.1 step 3) is ungrounded — see G1. |
| R2 | Generated tasklist's LAST task = `/sc:reflect --mode post --remediate`, ideally in a new agent/session, run after all tasks complete | **COVERED** | Templated as **penultimate** final-phase item (before `Update task status to Done`, `SKILL.md:1930`) to honor anti-orphaning (Rule #15 `SKILL.md:2028`; validation criterion `SKILL.md:1969`). Reuses Rule #16 QA-gate-emission machinery (`SKILL.md:2030`). Fresh-session handoff + PENDING-sentinel HALT correctly preserves executor-disjoint independence (proposal §6.2). This is the strongest-designed part. Minor: "VERY LAST task" in the spec is interpreted as "last meaningful gate, before the bookkeeping Done item" — a justified deviation, but it is a deviation from the literal word "last." |
| R3 | `--spec` used with `--mode pre` IF a spec was used and path known | **COVERED** | Best-effort capture at A.2 (`SKILL.md:190`), priority order explicit `--spec` → `@file` in GOAL → BUILD_REQUEST `SPEC:/PRD:/TDD:` → none; graceful degrade to `verdict: skipped` when absent (proposal §6.3, Decision C2). Correctly matches reflect's hard STOP "`--mode pre` with no `--spec`" (`commands/reflect.md:32`). |
| R4 | `depth` invoked in BOTH instances, dynamically + deterministically set by tasklist complexity; not by inference where determinism achievable | **PARTIAL** | TCS formula + threshold table + overrides applied to both gates (proposal §5, §5.5). Arithmetic is deterministic and the band→tier mapping is correctly cross-aligned to reflect's §5.3 rubric. **Gap:** 5 of 7 signal *extraction rules* are unspecified (S1/S2/S3/S4/S6), so the "byte-reproducible" claim is overstated — the non-determinism just moves from the formula to the inputs. See G3 + arithmetic section. |
| R5 | Agents spawned to run reflect default to **sonnet**, with a new `--reflectagent` flag to override | **PARTIAL** | `--reflectagent <model>` default `sonnet`, correctly scoped to the *orchestrator/Tier-1* class only (NOT reviewers — preserving heterogeneity, proposal §6.4 / Decision E2). Semantics are right. **Gap:** depends entirely on G1 (can the spawn tool even set a per-agent model?) and G2 (the `--executor-model` pass-through is wrong for PRE). |

**Coverage summary:** 1 covered, 4 partial, 0 gap. No requirement is entirely missing — every requirement has a concrete, correctly-placed design. The partials are all blocked on the same small cluster of unverified mechanisms, not on missing scope.

---

## Grounding verification — proposal claims vs. real surface

Every claim the proposal makes about the two skills was checked against source. Findings:

### Claims that are ACCURATE (verified)
- task-builder is a single-file skill, no `refs/`; pipeline ends A.8→A.9→A.10→A.10.5→A.11 (`SKILL.md:155-162`). ✓
- Rule #16 already drives QA-gate items into generated tasklists; "omits required QA gates ⇒ MALFORMED" (`SKILL.md:2030`). The POST item reuses this exactly. ✓
- Anti-orphaning: completion items inside final phase; Done item at `N.X` (`SKILL.md:1930`, Rule #15 `:2028`, validation `:1969`). Penultimate placement is compatible. ✓
- BUILD_REQUEST carries `QA_GATE_REQUIREMENTS` / `VALIDATION_REQUIREMENTS` / `TESTING_REQUIREMENTS` / `EXECUTION_CONTEXT_REQUIREMENTS` (`SKILL.md:804-847`); strictly-additive `POST_REFLECT_GATE` block is consistent with the M1-frozen-schema posture. ✓
- TB-Add-2 item-count bounds (≤40 / single-track ≤50) and TB-Add-3 clarification-adjacency exist (`SKILL.md:1167-1168, 1973-1974`) — the O3 override and S5 signal cite these correctly. ✓
- reflect `--depth quick|standard|deep` = T1-only / T1-then-rubric / force-T2 (`input-resolution.md:16`). ✓
- reflect `--executor-model` exists, resolves at Wave 0 step 0.5b, does executor-class exclusion, fail-open with `executor_class_source: flag|env|log-heuristic|unknown` and `executor_class_resolved: false` WARN (`reviewer-spec.md:72-76`, `SKILL.md:572-574`). ✓ — proposal §7 OQ-1 describes this precisely.
- Reviewer rotation 2→`sonnet,haiku`; 3→`sonnet,haiku,(qwen|kimi|deepseek else opus)` (`reviewer-spec.md:80-84`). ✓
- Cost bands T1 3-8k/60-180s, T2 35-70k/480-900s, T3 +20-40k (`cost-profile.yaml:34-66`). ✓
- Regression class **unconditionally** forces T2 (`remediation-handoff.md` default-remediation table, §5.3 rule 3). ✓ — O2/S6 grounding is correct (the proposal's "remediation-handoff.md:122" line anchor has drifted but the content is real).
- `--remediate` is audit-first, no auto-execute: "Reflect will NOT execute /task — you run it yourself" (`remediation-handoff.md` opt-in prompt). ✓
- **NO `--reflectagent` or single `--model` flag exists in reflect today** (grep across the whole reflect surface = zero hits). ✓ — proposal §2.3 + §8.3 are honest about this; `--reflectagent` is a task-builder-side flag only. Good.
- Direct skill invocation precedent (`Skill sc-adversarial-protocol`, "not command — per sc:roadmap pattern") is real (`sc-brainstorm-protocol/SKILL.md:278`). ✓ — the proposal's §6.1 analogy is valid.

### Claims that are UNVERIFIED or WRONG (the gaps)

**G1 — CRITICAL: the `model:`-on-spawn mechanism is ungrounded and contradicts task-builder's own spawn convention.**
The proposal §6.1 step 3 says: *"Spawn reflect via the Agent/Task tool with `model: <reflect_model>` … invoking `Skill sc:reflect-protocol`."* But every spawn in task-builder uses **Rigorflow's Agent tool with `subagent_type: "<agent>"` + `mode: "bypassPermissions"`** — researchers (`SKILL.md:416,427`), rf-analyst (`:608`), rf-qa (`:640,1132`), rf-task-builder (`:789,1040`). **None carries a `model:` field**, and the project's own subagent-routing memory states a subagent's *model is selected by its `subagent_type`*, not by a per-spawn `model:` arg. There is also no agent type defined for "run an arbitrary skill." So the central delivery vehicle for R1 (PRE spawn) and R5 (`--reflectagent` → `model:`) rests on a capability that (a) is never demonstrated in task-builder, and (b) may not exist on the Agent tool at all. **This is the single biggest pre-implementation risk and must be resolved first** — verify whether the Agent/Task spawn accepts a model override and can target a skill, OR redesign R5 (e.g. via a purpose-built reflect-runner agent whose `subagent_type` encodes the model class).

**G2 — HIGH: `--executor-model` is misapplied in the PRE gate.**
Proposal §6.4 + §6.1 step 3 pass `--executor-model <reflect_model>` into the **PRE** (`--mode pre`) call "so reflect knows the build orchestrator class." But `--executor-model` names *the model that produced the work under review*, and reflect *excludes* that class from its reviewer pool (`reviewer-spec.md:72`). In `--mode pre` **no executor has run** — the tasklist is unexecuted. Passing the reflect orchestrator's own class as `--executor-model` would cause reflect to exclude the wrong class from the PRE reviewer pool for the wrong reason (and on a specless build PRE is skipped anyway, so it is also dead). `--executor-model` is meaningful **only for the POST (UC-2) gate**, where it should carry the *tasklist executor's* class (the model that ran `/task`) — which the POST item already handles correctly via the `{EXECUTOR_CLASS}` placeholder (§6.2). **Fix:** drop `--executor-model` from the PRE call entirely; keep it only on the POST command.

**G3 — HIGH: TCS signal-extraction determinism is overstated; `--depth quick` can suppress reflect's safety escalation.** See arithmetic section below.

---

## Arithmetic / sanity check — the deterministic depth formula

`TCS = 3·S1 + 4·S2 + 2·S3 + 2·S4 + 5·S5 + 4·S6 + 2·S7`; bands ≤12 quick / 13–34 standard / ≥35 deep; overrides O1 (S5>0⇒floor standard), O2 (S6>0⇒force deep), O3 (items>40⇒floor standard).

**Band reachability is sane.** Worked examples: 2-file doc task (S1=2,S2=1) → TCS 10 → quick ✓. 7-file/3-subsystem task (S1=7,S2=3,S4=2,S7=2) → 41 → deep ✓, and `deep` here is *consistent with* reflect's own §5.3 rule 4 (`S_domains≥3 ⇒ escalate`). The band→tier mapping is genuinely cross-aligned to reflect's internal rubric — this is good design.

**Finding A — the two highest-weighted signals are largely redundant with the overrides.** Whenever `S6>0`, O2 forces `deep` *regardless of TCS*, so S6's ×4 contribution to the sum never changes the depth decision — it only affects the audit trail. Same for S5 at low counts (O1 floors standard). The ×4/×5 weights on S5/S6 are therefore mostly cosmetic for the actual decision; not wrong, but the proposal's framing oversells their role in the weighted sum.

**Finding B — the boundary-inference window is too narrow for the leverage it's meant to bound.** Inference is permitted only within "±2 of a threshold," and only on S2 ambiguity. But S2 has weight ×4, so a ±1 miscount of S2 moves TCS by ±4 — which can flip a band even when the pre-inference TCS sits *outside* the ±2 window (e.g. TCS=37 with S2 possibly overcounted by 1 → true 33, crossing the 35 boundary, but 37 is outside the 33–36 window). The escape hatch (defined on the ±2 TCS axis) does not capture all the S2-leverage cases (which live on a ±4 TCS span). Either widen the window to ±4 (= S2's unit leverage) or define the ambiguity check on the S2 axis (±1 subsystem) rather than the TCS axis. Also a minor off-by-one: "12 ± 2" = 10–14, but the proposal writes the lower window as "11–14."

**Finding C — signal extraction is under-specified (the determinism gap for R4).** Of 7 signals, only **S5** (needs_human_decision / TB-Add-3 blocked items — a defined structural feature) and mostly **S7** (literal "spawn in SAME message" markers) are cleanly deterministic. The other five each hide an unspecified extraction rule:
- **S1** "regex over file:line/path tokens in prose" — what is a path token? `src/foo.py` vs `foo.py` vs a path inside a code fence vs inside an Open Question; dedup rule undefined. Two implementers → two S1 values. This is the *same* class of non-determinism the proposal rejects for "estimated LOC."
- **S2** "first 1-2 path segments" — 1 *or* 2 is itself undefined (`src/superclaude` vs `src/superclaude/cli`); the proposal admits this is why the boundary-inference exists, but the ambiguity is definitional, not just boundary-local.
- **S3** FR/NFR count — token count vs distinct-ID count (`FR-1` cited 5×) undefined.
- **S4** "after Phase N / blockedBy / explicit item refs" — the ref-pattern set is open-ended ("explicit item refs").
- **S6** "refactor touching shared **gate objects**" — "gate object" requires semantic judgment; not deterministic.
So the *arithmetic* is deterministic but the *inputs* are not fully specified — "byte-reproducible outside the boundary window" is overstated. To satisfy R4's "deterministic AND accurate, not by inference," each signal needs a frozen, testable extraction rule (e.g. exact regex, exact segment count, exact dedup policy).

**Finding D — calibration is admittedly unmeasured (acceptable for v1).** Proposal §7 OQ-3 honestly states weights (×3/×4/×2/×2/×5/×4/×2) and thresholds (12/34) are "reasoned, not measured," and proposes recording `tcs`/`depth`/actual-tier in the sign-off block to build a tuning corpus. For a pre-execution proposal this is a reasonable posture — not a blocker, but R4's "accurate" clause stays PARTIAL until the corpus tunes them.

**Finding E (most important behavioral risk) — `--depth quick` is a HARD override that *disables* reflect's escalation.** Per reflect §5.1, `--depth quick` = "STOP at T1, skip Wave 3+." So a mis-low TCS does not merely under-estimate cost — it *pins reflect at Tier 1 and prevents the regression-escalation* that reflect's own §5.3 rule 3 would otherwise force. Tolerable for PRE (no diff yet), but §5.5 **reuses the same build-time TCS for the POST command**, where suppressing escalation on *executed code* is exactly the blindspot reflect exists to catch (and exactly the failure class `feedback_sc_reflect_vs_inline_rfqa.md` documents). **Recommendation:** never let TCS emit `--depth quick` for the POST gate — floor the POST depth at `standard` so reflect's rubric/regression-escalation is never suppressed on real executed work. (PRE may keep `quick`.)

---

## Best-practice / coherence findings

- **BP1 — Memory honoring is correct.** All three constraining memories are honored: executor-disjoint independence via fresh-session POST (`feedback_sc_reflect_vs_inline_rfqa`); HALT-don't-auto-mutate for both PRE remediation (additive `## Open Questions` only) and the POST PENDING sentinel (`feedback_human_decision_items_must_halt`); `/task` not `/sc:task` in surfaced commands (`feedback-no-sctask-on-task-builder-tasklists`). Verified against the proposal's §2.4 + §6.2 + §6.5.
- **BP2 — Add the Rule #16-style MALFORMED guard for the POST item.** The proposal raises this itself (§7 risk 5) but leaves it optional. Without a companion structural-validation check (mirroring Rule #16's "MALFORMED if QA gate omitted"), a builder that silently drops the `POST_REFLECT_GATE` item is non-compliant and undetected. Given A.10's structural validator already enforces QA-gate presence, this should be a *required* delta, not a risk note — promote it into the Implementer Checklist.
- **BP3 — Multi-track / partition surfaces under-specified.** The proposal notes per-track PRE+POST (§7 risk 6) but the A.8/A.10 synthetic-dnsp partition merge machinery (`SKILL.md:671,1185`) and the `LIVE_TB_ADD` dynamic-enumeration freshness rules (`SKILL.md:1331-1337`) are adjacent to where A.10.7 inserts. Confirm A.10.7 sits *after* A.10.5's verdict gate cleanly and does not perturb the DM-005 halt-before-A.10.5 contract (`SKILL.md:1192`). Low risk but should be explicitly checked at implementation.
- **BP4 — `--reflect-pre/--no-reflect-pre` toggle.** Proposal §7 risk 4 flags always-on PRE cost (3-8k/build even at quick) on trivial Template-01 builds and suggests an opt-out. Reasonable; out of the required-flag scope but cheap. Not a gap.

---

## Gaps that MUST close before implementation

1. **G1 (CRITICAL):** Verify the Agent/Task spawn can (a) set a per-agent `model:` and (b) target a skill (`Skill sc:reflect-protocol`). If not, redesign R5's delivery (purpose-built reflect-runner agent keyed by `subagent_type`, or a different model-routing path). The entire `--reflectagent` flag and the PRE spawn depend on this.
2. **G2 (HIGH):** Remove `--executor-model` from the PRE (`--mode pre`) call — it is a category error pre-execution. Keep it only on the POST command, carrying the tasklist executor's class.
3. **G3a (HIGH):** Freeze a testable extraction rule for each of S1–S4, S6 (exact regex / segment count / dedup policy) so "deterministic" is true at the input level, not just the arithmetic level.
4. **G3b (HIGH):** Floor the POST gate depth at `standard` (never `quick`) so a mis-low TCS cannot disable reflect's regression escalation on executed code.
5. **G3c (MEDIUM):** Reconcile the boundary-inference window with S2's ×4 leverage (widen to ±4 TCS or define the check on the S2 axis) and fix the 11-vs-10 off-by-one.
6. **BP2 (MEDIUM):** Promote the POST-item MALFORMED structural guard from "risk note" to a required validation-checklist delta.

Addressing G1, G2, G3a, G3b lifts the four PARTIAL requirements to COVERED. G3c + BP2 are coherence-hardening.

---

*Hallucination contract: every `file:line` / `§` citation above was re-Read from source during this pass. The proposal's "remediation-handoff.md:122" anchor was found content-accurate but line-shifted; flagged inline rather than dropped.*
