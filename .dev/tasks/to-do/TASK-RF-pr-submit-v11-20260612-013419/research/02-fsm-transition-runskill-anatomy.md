# Research: FSM transition/run_skill Anatomy

- **Topic type:** Data Flow Tracer
- **Scope:** `src/superclaude/pr_submit/fsm.py` ONLY
- **Status:** Complete
- **Date:** 2026-06-12

> All line numbers verified against `src/superclaude/pr_submit/fsm.py` (33163 bytes, mtime Jun 11 13:53) as read this turn. **The builder MUST instruct the executor to RE-GREP every anchor at edit time** — line numbers drift on any prior edit to the file.

---

## 0. File shape & structure (high-level map)

`fsm.py` is **803 lines**, organized as a flat sequence of module-level pure functions + 4 dataclasses. There is **NO class-based FSM** — `transition()` is a free function, and `run_skill()` is a free function that *re-implements* the cycle inline (it does NOT call `transition()`). This is load-bearing for the build: **the spec's new edges live in `transition()`, but the actual runtime loop the tests assert on is `run_skill()` — both must be modified in lock-step or they drift.**

Section banners (grep anchors, stable-ish comment headers):
- `# Argument parsing` (fsm.py:42) → `SkillArgs` (47), `build_arg_parser` (69), `parse_args` (90)
- `# Gate predicates` (fsm.py:120) → `gate_arm` (125), `gate_edit` (130), `should_halt_rounds` (135), `evaluate_push_decision` (145), `push_fail_state` (179)
- `# L3 write-ahead push triad` (fsm.py:194) → `push_idempotency_key` (199), `build_push_triad` (210)
- `# Reply construction` (fsm.py:263) → `is_groundable`, `audit_validated_not_verified`, `is_trivial_fix`, `build_reply`
- `# Troubleshoot dispatch` (fsm.py:339) → `seed_troubleshoot`, `batch_by_file`, `DispatchPlan`, `plan_dispatch`
- `# §10 validation-gate driver` (fsm.py:409) → `VALIDATION_GATES`, `MANDATORY_GATES`, `run_validation_gates`, PR-target checks, `is_cross_cutting`
- `# Poll timing` (fsm.py:515) → `next_backoff`, `timed_out`, `poll_outcome`
- `# transition() — the transition table` (fsm.py:555) → **`transition()` (560)** ← EDIT TARGET 1
- `# run_skill() — the integration driver` (fsm.py:622) → `_noop` (627), `_default_verify` (631), `_default_apply_edits` (642), **`RunConfig` (653)** ← EDIT TARGET 3, **`run_skill()` (679)** ← EDIT TARGET 2

**Imports (fsm.py:19-27):** `argparse`, `dataclasses`, `typing.Callable`; `loop_guard.should_halt as loop_guard_should_halt`; `models.{Finding,MonitorState,PushDecision,SkillResult}`; `severity_router.{ROUTE_REPORT_ONLY,remap_severity,route}`. **No `subprocess`, `os`, `gh`, `git`, `anthropic` imports.**

---

## 1. `transition(state, event, context=None)` — the COMPLETE edge table

**Signature (fsm.py:560-562):** `def transition(state: MonitorState, event: str, context: dict | None = None) -> MonitorState:`

**STRUCTURE IS NOT A DICT.** It is a **flat sequence of `if edge == (...): ...` guards** over `edge = (state, event)` (fsm.py:577). This matters for the edit: each new edge is a NEW `if edge == (...)` block inserted into the chain — there is no table literal to append to. The chain ends with a defensive `return state` fallback (fsm.py:619). Items should describe edits as "insert `if` block after the `if edge == (X, "y"):` block at fsm.py:NNN" and instruct re-grep of the anchor `if edge == (MonitorState.RESOLVING, "resolved"):`.

**Two short-circuits BEFORE the edge chain (fsm.py:570-575):**
1. `ctx = context or {}`; `ordinal = int(ctx.get("monitor_ordinal", 0))` (fsm.py:570-571)
2. **Pre-gate `needs_human_decision` override (fsm.py:574-575):** `if ctx.get("needs_human_decision"): return MonitorState.HALT_HUMAN` — evaluated FIRST, the ONLY ceiling short-circuit. New edges sit AFTER this, so a needs-human cycle still HALTs ahead of any S5A/S5B routing. (Builder: confirm S5B fallback is not meant to override this — spec §6.4 does not list a needs-human interaction, so leave the override first.)

### Current edge table (verbatim, every from-state → outcome → to-state)

| # | Line | From state | event/outcome | To state | Gate / note |
|---|------|-----------|---------------|----------|-------------|
| 1 | 579-580 | `S0_IDLE` | `"arm"` | `S2_CLASSIFY` if `gate_arm(ordinal)` (ordinal≥1) **else** `S0_IDLE` | G-arm |
| 2 | 581-582 | `S2_CLASSIFY` | `"no_review"` | `S2_CLASSIFY` | loop back (poll again) |
| 3 | 583-584 | `S2_CLASSIFY` | `"clean"` | `TERMINAL_CLEAN` | |
| 4 | 585-592 | `S2_CLASSIFY` | `"findings"` | `HALT_MAX_ROUNDS` if `should_halt_rounds(round_counter,max_rounds)` **else** `S2B_VERIFY` | round-budget gate evaluated inline (reads `ctx["round_counter"]`, `ctx["max_rounds"]`) |
| 5 | 593-594 | `S2B_VERIFY` | `"verified"` | `S3_DIAGNOSE` | |
| 6 | 595-596 | `S2B_VERIFY` | `"unverified"` | `REPORT_ONLY` | no round consumed |
| 7 | 597-599 | `S3_DIAGNOSE` | `"diagnosed"` | `S3_FIXING` if `gate_edit(ordinal)` (ordinal≥2) **else** `PROPOSED` | G-edit |
| 8 | 600-601 | `S3_FIXING` | `"edits_applied"` | `S7_VALIDATING` | |
| 9 | 602-604 | `S7_VALIDATING` | `"validated"` | `S4_PUSHING` | "G-push handled by evaluate_push_decision at caller; default edge" |
| 10 | 605-606 | `S7_VALIDATING` | `"validation_failed"` | `VALIDATION_FAIL` | |
| 11 | 607-608 | `S4_PUSHING` | `"pushed"` | `S6_REPLYING` | |
| 12 | 609-610 | `S6_REPLYING` | `"replied"` | `RESOLVING` | |
| 13 | **611-612** | `RESOLVING` | `"resolved"` | **`S5_AWAITING_REREVIEW`** | ← **[MOD] TARGET**: spec retargets to `S5A_RETRIGGER_REVIEW` |
| 14 | **613-614** | `S5_AWAITING_REREVIEW` | `"rereview_attributed"` | `S2_CLASSIFY` | **INV-001 EDGE — comment fsm.py:614 says "loop-guard increments at this edge (INV-001)"**. KEEP VERBATIM. |
| 15 | 615-616 | `S5_AWAITING_REREVIEW` | `"timeout"` | `TERMINAL_TIMEOUT` | |
| — | 618-619 | (any) | (unknown) | `state` | defensive fallback |

**CRITICAL on edge #14 (the INV-001 edge):** the from/event/to triple `(S5_AWAITING_REREVIEW, "rereview_attributed") → S2_CLASSIFY` is what INV-001 protects ("the S5→S2 edge"). The spec §6.4 adds `(S5_AWAITING_REREVIEW, "declined") → S5B_AUGGIE_FALLBACK` as a SIBLING edge — it does NOT touch edge #14. **The builder must add the `"declined"` edge as a new `if` block and leave the `"rereview_attributed"` block byte-identical.** The event string the V1.0 transition table uses for the attributed re-review is **`"rereview_attributed"`** (fsm.py:613) — note this differs from `run_skill()`'s spec-named `rereview_outcome` value `"attributed"`; the builder should reconcile (the transition-table event name and the run_skill outcome token are independent strings).

### Spec §6.4 edge deltas to apply (merged-spec-v1.1-addendum.md:248-253)

| Action | Edge | Insert relative to |
|--------|------|--------------------|
| **[MOD]** | `(RESOLVING, "resolved") → S5A_RETRIGGER_REVIEW` (was `→ S5_AWAITING_REREVIEW`) | replace RHS of edge #13 (fsm.py:611-612) |
| ADD | `(S5A_RETRIGGER_REVIEW, "retriggered") → S5_AWAITING_REREVIEW` | new block after #13 |
| ADD | `(S5_AWAITING_REREVIEW, "declined") → S5B_AUGGIE_FALLBACK` | new block alongside #14/#15 (sibling of `rereview_attributed`/`timeout`) |
| ADD | `(S2_CLASSIFY, "declined") → S5B_AUGGIE_FALLBACK` | new block alongside #2/#3/#4 |
| ADD | `(S5B_AUGGIE_FALLBACK, "fallback_findings") → S2_CLASSIFY` | new block (re-enter, fallback budget) |
| ADD | `(S5B_AUGGIE_FALLBACK, "fallback_skip") → HALT_MAX_ROUNDS \| TERMINAL_CLEAN` | new block (conditional terminal — builder must define the selector; spec leaves it as a disjunction) |

**Dependency:** all 6 edges reference `MonitorState.S5A_RETRIGGER_REVIEW` / `S5B_AUGGIE_FALLBACK` which DO NOT YET EXIST in the enum (verified absent in models.py:93-113). **models.py edit (§6.1) is a hard prerequisite** for the transition() edits to import-resolve — sequence the enum-add item BEFORE the fsm edge items.

---

## 2. `run_skill(config, **overrides)` — loop control flow + the :793 increment

**Signature (fsm.py:679):** `def run_skill(config: RunConfig | None = None, **overrides) -> SkillResult:`

### Config resolution (fsm.py:689-693)
- `if config is None: config = RunConfig(**overrides)` (689-690)
- `elif overrides: for k,v in overrides.items(): setattr(config, k, v)` (691-693) — overrides MUTATE a passed config.

### Pre-loop linear scaffold (fsm.py:695-712)
1. `result = SkillResult(state=MonitorState.S0_IDLE)` (695); `ordinal = config.monitor_ordinal` (696)
2. **G-arm early return (fsm.py:699-701):** `if not gate_arm(ordinal): result.state = S0_IDLE; return result` — L0 byte-identical (AC-1).
3. `config.arm_monitor(config.pr_number)` (702); `result.state = S2_CLASSIFY` (703)
4. `review_state == "polling"` → return at `S2_CLASSIFY` (705-707)
5. `review_state == "clean"` → `TERMINAL_CLEAN` + `summary_posted=True`, return (708-712)

### The multi-round cycle loop (fsm.py:717-800) — THE CORE

```
cycles = [config.findings] + list(config.rereview_findings)          # fsm.py:717
for cycle_index, cycle_findings in enumerate(cycles):                # fsm.py:718
```

The loop models each Augment round as one entry in `cycles`. **`rereview_findings` is the residual-set sequence that drives the next iteration** (the V1.1 spec adds a *parallel* `rereview_outcome` sequence so the harness can mark each round `"attributed" | "declined" | "timeout"` — see §3 RunConfig).

Per-iteration body, in order:
1. **Round-budget HALT gate (fsm.py:720-725):** `if should_halt_rounds(result.round_counter, config.max_rounds):` → `HALT_MAX_ROUNDS`, set `result.findings`, `summary_posted=True`, `break`. **This is the `>=` INV-001 gate at the TOP of the loop (delegates to loop_guard).**
2. `result.findings = cycle_findings` (727); `if not cycle_findings: state=TERMINAL_CLEAN; break` (728-730)
3. **needs_human pre-gate (fsm.py:739-741):** `if ordinal >= 3 and any(f.needs_human_decision ...): state=HALT_HUMAN; break`
4. **S2b_VERIFY (fsm.py:744-747):** `verified = [f for f in cycle_findings if config.verify(f)]`; `if not verified: state=REPORT_ONLY; break`
5. **S3_DIAGNOSE → G-edit (fsm.py:750-755):** `if not gate_edit(ordinal):` → `PROPOSED`, `applied_edits=0`, `proposal=PROPOSE_PROMPT`, `break` (L1 ceiling)
6. **S3_FIXING (fsm.py:758):** `result.applied_edits = config.apply_edits(verified)`
7. **S7_VALIDATING (fsm.py:761-764):** `result.validation_status = config.run_validation(findings=verified)`; `if != "validated": state=VALIDATION_FAIL; break`
8. **G-push INV-016 conjunction (fsm.py:767-782):** build `decision = evaluate_push_decision(...)`; `result.push_decision = decision`; `if not decision.authorized:` → `S4_HALT_BEFORE_PUSH` (ordinal<3) else `push_fail_state(decision)`; `break`
9. **L3 push triad side-effects (fsm.py:785-790):**
   - `config.do_push(pre_push_sha=None)` (785); `result.push_count += 1` (786)
   - `config.do_reply(applied_edits=..., findings=verified)` (787); `result.reply_count += 1` (788)
   - `config.do_resolve(findings=verified)` (789)
   - `result.state = MonitorState.S5_AWAITING_REREVIEW` (790)

### ★ THE :793 OPTIMISTIC INCREMENT (the [MOD]/REMOVE target) ★

**CONFIRMED at fsm.py:792-793** (spec's "line 793" is exact):

```python
792:        # Re-review attributed to our push: tick the monotonic round counter (INV-001).
793:        result.round_counter += 1
```

This sits **immediately after** the `do_resolve` + `result.state = S5_AWAITING_REREVIEW` block (fsm.py:789-790), **inside the `for cycle_index` loop, BEFORE** the terminal check. It is "optimistic" because it ticks unconditionally after a push/resolve, ASSUMING the push caused an attributed re-review — it never waits for an observed re-review. **Spec FR-8.2 (addendum:161) + §6.4 (addendum:254): REMOVE this line; tick only on an injected attributed-re-review outcome** (the new `rereview_outcome[cycle] == "attributed"` seam). T-PUSH-WITHOUT-REREVIEW-NO-TICK asserts a push with no subsequent attributed re-review does NOT advance the counter.

**The cycle tail AFTER :793 (fsm.py:797-800):**
```python
797:        if cycle_index + 1 >= len(cycles):
798:            result.state = MonitorState.TERMINAL_CLEAN
799:            result.summary_posted = True
800:            break
```
So when the increment is removed/relocated, the builder must ensure the **`round_counter` tick happens BEFORE the top-of-loop `should_halt_rounds` gate of the NEXT iteration (fsm.py:720)** — that ordering is what makes `max_rounds=N ⇒ N pushes` hold. If the increment is moved to depend on `rereview_outcome[cycle_index]`, it must still be applied before the loop re-tests the budget, or monotonicity / the N-push invariant breaks. **This is the single highest-risk edit for INV-001.**

**`break` inventory (every loop exit):** budget-halt (725), empty-findings (730), needs-human (741), no-verified (747), L1-propose (755), validation-fail (764), push-not-authorized (782), final-clean (800). The loop has **no `continue`** — it either `break`s or falls through to the next iteration naturally.

---

## 3. `RunConfig` — current fields + the injected-callable seam pattern

**Dataclass (fsm.py:653-676).** Two helper defaults precede it: `_noop(*_args, **_kwargs) -> None: return None` (fsm.py:627-628), `_default_verify` (631-639), `_default_apply_edits` (642-650).

### Current fields (verbatim, fsm.py:657-676)

**Data inputs:**
| Field | Default | Line |
|-------|---------|------|
| `monitor_ordinal: int` | `0` | 657 |
| `max_rounds: int` | `DEFAULT_MAX_ROUNDS` (2) | 658 |
| `poll_interval: int` | `MIN_POLL_INTERVAL` (30) | 659 |
| `timeout: int` | `DEFAULT_TIMEOUT` (1800) | 660 |
| `pr_number: int \| None` | `None` | 661 |
| `resume: str \| None` | `None` | 662 |
| `findings: list[Finding]` | `field(default_factory=list)` | 663-664 |
| `rereview_findings: list[list[Finding]]` | `field(default_factory=list)` | 665-667 |
| `review_state: str` | `"findings"` (`"polling"\|"clean"\|"findings"`) | 668 |

**Side-effect SEAMS (the injected-callable pattern — fsm.py:669-676):**
| Seam | Type | Default | Line |
|------|------|---------|------|
| `arm_monitor` | `Callable[..., None]` | `_noop` | 670 |
| `verify` | `Callable[[Finding], bool]` | `_default_verify` | 671 |
| `apply_edits` | `Callable[[list[Finding]], int]` | `_default_apply_edits` | 672 |
| `run_validation` | `Callable[..., str]` | `staticmethod(lambda **_: "validated")` | 673 |
| `do_push` | `Callable[..., None]` | `_noop` | 674 |
| `do_reply` | `Callable[..., None]` | `_noop` | 675 |
| `do_resolve` | `Callable[..., None]` | `_noop` | 676 |

### THE SEAM PATTERN (new seams MUST match this exactly)

1. **All side-effecting seams default to `_noop`** (or a pure recording-only default like `_default_verify`). The default makes the core record-only / test-pure — production injects the real I/O callable.
2. **`Callable[..., None]` for fire-and-forget side effects** (`arm_monitor`, `do_push`, `do_reply`, `do_resolve`); `Callable[[X], Y]` for value-returning seams (`verify→bool`, `apply_edits→int`, `run_validation→str`).
3. **GOTCHA — `staticmethod` wrapper for lambda defaults (fsm.py:673):** `run_validation` uses `staticmethod(lambda **_: "validated")`. A bare `lambda` as a dataclass default would bind as an instance method and receive `self`. **`do_push`/`do_reply`/`do_resolve` avoid this by referencing the module-level `_noop` function (not a lambda)** — module-level `def` names are safe as dataclass defaults without `staticmethod`. **New seams (`do_retrigger`, `invoke_auggie_review`) should follow the `_noop` module-function pattern, NOT inline lambdas**, to avoid the self-binding trap.
4. **Seams are CALLED with keyword args** in `run_skill`: `config.do_push(pre_push_sha=None)` (785), `config.do_reply(applied_edits=..., findings=verified)` (787), `config.do_resolve(findings=verified)` (789), `config.run_validation(findings=verified)` (761), `config.arm_monitor(config.pr_number)` (702). New seams should be called with explicit kwargs.

### Spec §6.4 RunConfig deltas (addendum:255-258)
- ADD `do_retrigger: Callable[..., None] = _noop` (the S5A re-trigger comment-post seam)
- ADD `invoke_auggie_review: Callable[..., None] = _noop` (the S5B fallback `> Skill sc:auggie-review-protocol` seam)
- ADD a per-cycle `rereview_outcome` sequence — token values `"attributed" | "declined" | "timeout"`. **Builder note:** mirror the `rereview_findings: list[list[Finding]]` shape → likely `rereview_outcome: list[str] = field(default_factory=list)`, indexed by `cycle_index` so the harness drives R1/R2 deterministically and the deferred increment ticks only when `rereview_outcome[cycle_index] == "attributed"`.
- Spec §6.1 also adds `SkillResult` fields (`fallback_round_counter`, `effective_max_rounds`, etc.) — those live in models.py, NOT RunConfig (R3's scope), but `run_skill` will read/write `result.fallback_round_counter` for the §3.5 fallback sub-loop.

### New pure helper (addendum:259)
`clamp_max_rounds(effective, hard=1) -> int = min(effective, hard)` — a NEW module-level pure function. Place it among the gate predicates (near `should_halt_rounds`, fsm.py:135) to match the "pure ordinal check" grouping. Pattern-match `gate_arm`/`gate_edit` (one-line pure functions, fsm.py:125-132).

### Fallback sub-loop (addendum:260)
Uses `loop_guard.should_halt(fallback_round_counter, 1)` — **reuses the ALREADY-IMPORTED** `loop_guard_should_halt` (fsm.py:25, aliased). The cap is the literal `1` (single-shot). No new import needed. The fallback `round_counter` (`fallback_round_counter`) is INDEPENDENT of INV-001's `round_counter` — frozen at fallback entry (addendum:183, FR-10.3).

---

## 4. NFR-6 / AC-9 core-purity check (gh/git/token scan)

**RESULT: CLEAN.** `grep -niE "subprocess|os\.system|gh |git |run\(|popen|shell|token|credential"` over fsm.py returns **only docstring/comment mentions**, ZERO executable shell/VC code:
- fsm.py:9 — docstring "contains ZERO shell / version-control command tokens"
- fsm.py:351 — docstring "the core never shells out"
- fsm.py:435 — docstring "the core stays free of shell tokens"
- fsm.py:458 — docstring "no version-control command tokens"
- fsm.py:735 — comment "L1 ceiling prevents the push" (the word "push", prose only)

No `import subprocess`/`os`/`anthropic`; no `gh`/`git` subprocess calls; no token/credential literals. **The push/reply/resolve/retrigger/auggie-review side effects are ALL behind `_noop` seams** — the SKILL.md bash scripts + VAL validator do the real I/O. **The V1.1 additions (`do_retrigger`, `invoke_auggie_review`) MUST preserve this: they are `_noop`-defaulted seams, and the actual `gh api` comment-post + `> Skill sc:auggie-review-protocol` call live in SKILL.md (addendum:261-263), never fsm.py.** Builder should add a core-purity assertion item (T-N50 extended per addendum:263) and instruct the executor to re-run the grep after editing.

---

## 5. INV-001 preservation map (what MUST stay verbatim)

INV-001 has FOUR sub-claims (addendum:347). Their literal anchors in fsm.py:

| INV-001 claim | Anchor in fsm.py | Edit rule |
|---------------|------------------|-----------|
| **The S5→S2 edge** | `transition()` edge #14: `(S5_AWAITING_REREVIEW, "rereview_attributed") → S2_CLASSIFY` (fsm.py:613-614) | KEEP byte-identical. Add `"declined"` as a SIBLING edge; do not alter `"rereview_attributed"`. |
| **`>=` gate (not `>`)** | `should_halt_rounds` (fsm.py:135-142) → delegates to `loop_guard_should_halt`; consumed at top-of-loop (fsm.py:720) and in `evaluate_push_decision` p4 `round_counter < max_rounds` (fsm.py:166) | DO NOT change the predicate or its `>=`/`<` direction. The fallback uses the SAME `loop_guard.should_halt` with cap `1` — a separate call, same fence-post. |
| **Monotonicity** | `result.round_counter += 1` — currently fsm.py:793 (only increment site; grep confirms no other `round_counter +=` / `round_counter =` in file) | After REMOVING :793, the relocated increment must still be monotonic (only `+= 1`, never reset) AND gated on `rereview_outcome == "attributed"`. `fallback_round_counter` is a SEPARATE counter (never folded into `round_counter`). |
| **`max_rounds=N ⇒ N pushes`** | ordering: increment (793) happens AFTER push (786) and BEFORE the next iteration's budget gate (720) | The deferred-increment relocation MUST preserve this ordering or the N-push invariant breaks. This is the deviation `/sc:reflect --mode pre` is called out to catch (addendum:373). |

**There is exactly ONE `round_counter` mutation site in the file** (fsm.py:793) — verified by reading the full file. The `evaluate_push_decision` and `should_halt_rounds` callers only READ it. This makes the [MOD] surgically localizable: the builder can describe the edit as "delete fsm.py:792-793, add a conditional `if config.rereview_outcome[cycle_index] == 'attributed': result.round_counter += 1` at the point where the attributed re-review is observed (after the S5_AWAITING_REREVIEW state set, gated by the injected outcome)."

---

## 6. Builder action summary (per-item guidance)

**Edit-site sequencing (dependency order):**
1. **models.py FIRST** (R1/R3 scope): add `S5A_RETRIGGER_REVIEW`, `S5B_AUGGIE_FALLBACK` to `MonitorState` (models.py:93-113), omit from `TERMINAL_STATES` (models.py:117-126). Hard prereq — fsm edits won't import-resolve otherwise.
2. **fsm.py `transition()` edges** (fsm.py:577-619): MOD edge #13 RHS; add 5 new `if edge ==` blocks. Re-grep anchor `if edge == (MonitorState.RESOLVING, "resolved"):`.
3. **fsm.py `RunConfig`** (fsm.py:653-676): add `do_retrigger`, `invoke_auggie_review` (`_noop` defaults), `rereview_outcome` list. Re-grep anchor `do_resolve: Callable[..., None] = _noop`.
4. **fsm.py `clamp_max_rounds`** pure helper near fsm.py:135.
5. **fsm.py `run_skill()`** (fsm.py:717-800): REMOVE :792-793 optimistic increment; add deferred attributed-outcome tick; add fallback sub-loop using `loop_guard_should_halt(fallback_round_counter, 1)`. Re-grep anchor `result.round_counter += 1` and the comment `# Re-review attributed to our push:`.

**Mandatory executor instructions per item:**
- RE-GREP every anchor at edit time (line numbers WILL drift after item 1-2 land).
- After ALL fsm edits: re-run the NFR-6 grep (`grep -niE "subprocess|os\.system|gh |git |popen|token|credential" fsm.py` → must show docstring-only).
- Keep `transition()` edge #14 and the `should_halt_rounds`/`>=` gate byte-identical (INV-001).
- `run_skill()` does NOT call `transition()` — edits to one do not propagate to the other; both must be done.

---

## Summary

`fsm.py` (803 lines) is a flat pure-function module: `transition()` (fsm.py:560) is a **chain of `if edge == (state,event)` guards, NOT a dict** (15 edges + defensive fallback, table at §1); `run_skill()` (fsm.py:679) **re-implements the cycle inline** as a `for cycle_index, cycle_findings in enumerate(cycles)` loop (fsm.py:718) and does NOT call `transition()`. **The optimistic increment is CONFIRMED at fsm.py:792-793** (`result.round_counter += 1`, the ONLY round_counter mutation in the file), sitting right after the do_resolve/S5_AWAITING_REREVIEW block and before the final-clean tail (797-800) — spec FR-8.2/§6.4 removes it and defers the tick to an injected `rereview_outcome == "attributed"`. **RunConfig** (fsm.py:653-676) uses an injected-callable seam pattern: side-effects default to module-level `_noop` (NOT inline lambdas — `run_validation` needs `staticmethod` to dodge self-binding), called with explicit kwargs; new `do_retrigger`/`invoke_auggie_review` seams must match. **NFR-6 is CLEAN** — zero shell/gh/git/token executable code (docstring mentions only). INV-001's four sub-claims map to: edge #14 (fsm.py:613-614, keep verbatim), the `>=` gate via `should_halt_rounds`→`loop_guard` (fsm.py:135-142/720), the single increment site (fsm.py:793), and the push/increment/budget-gate ordering. The highest-risk edit is relocating the deferred increment without breaking `max_rounds=N ⇒ N pushes`. The 6 new edges depend on a models.py enum-add that must land first.
