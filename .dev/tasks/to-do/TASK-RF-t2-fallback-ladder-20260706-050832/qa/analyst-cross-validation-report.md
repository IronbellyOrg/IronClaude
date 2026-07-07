# Cross-Validation Report — Reflect Tier-2 Fallback Ladder Research

**Analysis type:** completeness-verification
**Lens:** cross-validation (zero-trust spot-check ~25% of file:line claims)
**Verdict:** PASS (see bottom) — 0 wrong citations, 0 true contradictions, 1 Important non-blocking cross-file note (I-1), 2 Minor
**Date:** 2026-07-06
**Files analyzed:** 01-reflect-seam-inventory.md, 02-swarm-transport-slot-inventory.md, 03-patterns-conventions.md, 04-test-surface.md, 05-template-and-examples.md
**Repo root:** /config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback

---

## Method

Zero-trust spot-check. I independently Read/grepped the actual source for every
load-bearing file:line claim behind the 6 assigned cross-checks — far exceeding
the 25% floor. **Every single spot-checked claim matched the current worktree
source exactly.** No code:line claim in any of the 5 files was found wrong.

Independently re-verified against source this turn:
- ensemble.py: `build_reflect_contract` def **L553–569**, returned dict **L599–638**,
  `compute_model_class_diversity` call **L615** + `compute_vendor_diversity` **L616**,
  `merge_method` **L585**, `tier_reached` **L584**, three additive kwargs
  `reviewer_isolation`/`audit_tree_dirty`/`reviewer_grounding_root` at **L564–566**
  (sig) + **L635–637** (emit).
- swarm/dispatch.py: `transport_for_slot(slot_index)` **L454**, `range(workers_requested)`
  **L471**, tasks comprehension **L464–472**.
- swarm/commands.py: `_factory(slot_index)` **L691**, `pool[slot_index % len(pool)]`
  **L692**, `ModelPoolTooSmallError` guard **L687–688**.
- reflect/contract.py: `_degraded_reason` def **L256**, T6 `degraded-tier1` **L271–272**,
  T10 `single-reviewer-fallback` **L288–289**.
- reflect/models.py: `reachability: bool = True` **L109** (last defaulted field),
  field-ordering comment **L82–83**, `contract_path` property **L111–114**.
- swarm/config.py: T2 constants **L51/52/57/63**, `SwarmConfig` `@dataclass(frozen=True)`
  **L66**, `t2_models` **L95** (followed by `dry_run`/`debug`/`log_level` L96–98),
  `_collect_t2_models` **L178–185**.
- swarm/transports/openai_compat.py: import block (4 T2 constants) **L98–103**,
  `read_env` **L159–202**, `__all__` (exports `read_env`) **L106–111**.
- Test tree: `tests/cli/swarm/` **does NOT exist**; `tests/swarm/{test_config.py,
  test_openai_compat.py}` **exist**; `tests/cli/reflect/test_contract.py` **does NOT
  exist**; `tests/cli/reflect/test_verdict_mapping.py` **exists**. Greenfield symbol
  grep (`t2_fallback`, `read_env_for_pool`, `make_fallback_slot_factory`, `T1Model`,
  `t1_models`) across `src/superclaude/cli` + `tests` → **zero hits**.

---

## Cross-Check Results (the 6 assigned)

### CC1 — 01 vs 03 on `build_reflect_contract` kwargs + additive pattern → AGREE ✓
Both files place the def at **ensemble.py:553–569** and the additive kwargs
`reviewer_isolation` (L564), `audit_tree_dirty` (L565), `reviewer_grounding_root`
(L566), emitted at dict L635–637. Source confirms all six lines exactly. Both
correctly identify the pattern: keyword-only, defaulted-CLEAN, appended after
existing kwargs, matching dict key at the tail of `return {...}`. 01's delta table
correctly flags the design's "L552" cite as +1 vs the actual L553. No divergence.

### CC2 — 02 vs 04 on F3 `read_env` location + T1/T2 constants → AGREE ✓
02 cites `read_env` at **openai_compat.py:159–202** with the T2 constants hard-coded
at config.py L51/52/57/63. 04 cites `read_env(openai_compat.py:159)` hard-coding the
same four constants at "openai_compat.py:179–204". Source: `read_env` spans L159–202;
the T2-constant reads are at L178/179/182/183/193. 04's "179–204" upper bound (204)
overshoots the function end (L202) by 2 lines — a trivially loose range, not a wrong
claim (the constant usages it points at are real and inside the function). Both agree
on the load-bearing facts: single T2-bound reader at L159, four T2 constants, dense
1-based slot loop. Consistent.

### CC3 — 04's BLOCKING path corrections hold against the real tree → CONFIRMED ✓
- `tests/cli/swarm/` **does not exist** (verified `ls` → No such file or directory).
  04 Finding A is correct: swarm tests must land in `tests/swarm/` (extend existing
  `test_config.py` + `test_openai_compat.py`, both present).
- `tests/cli/reflect/test_contract.py` **does not exist** (verified `ls` → No such
  file). 04 Finding B is correct: the design's "test_contract.py (existing)" is a
  misnomer; builder must CREATE it or fold into `test_verdict_mapping.py` (which does
  exist). Both BLOCKING findings are accurate.

### CC4 — design.md §9 (patched) now matches 04's corrected paths → CONFIRMED ✓
The §9 revision is clean:
- Line 640/641 target the swarm tests at `tests/swarm/test_config.py` and
  `tests/swarm/test_openai_compat.py` (existing — extend). Correct.
- Line 624 still contains the token "tests/cli/swarm", but in the **corrected
  negation** form: "swarm tests live under `tests/swarm/` (NOT `tests/cli/swarm/`,
  which does not exist…)". This is a directive AGAINST the wrong path, not a residual
  wrong directive. Acceptable.
- Line 626 now reads "`tests/cli/reflect/test_contract.py` does NOT currently exist"
  — the stale "(existing)" claim is gone.
- `revision_note` (L9) records F1–F7 closure incl. "tests/cli paths (F7)".
No residual `tests/cli/swarm` **directive** and no residual "test_contract.py existing"
claim remain. The patch is confirmed.

### CC5 — F1 root cause (dispatch slot_index==0 for 1-worker) in 01 & 02 vs source → CONFIRMED TRUE ✓
01 §1 flags the positional `TransportFactory = Callable[[int], Transport]` seam; 02 §4
gives the full root cause. Source confirms: `dispatch_wave1` builds tasks over
`range(workers_requested)` (**L471**) and calls `transport_for_slot(slot_index)`
(**L454**) with that same index. A 1-worker `WorkerSpec(count=1)` ⇒ `workers_requested
== 1` ⇒ the only task is `index == 0` ⇒ factory always called with `slot_index == 0`
⇒ `_factory` maps `pool[0 % len] == pool[0] == T1Model01` (commands.py L692). A naive
second fallback re-selects `pool[0]`, so `T1Model02 → pool[1]` is mechanically
unreachable without slot-NAME keying. 01 and 02 agree; source proves it. design §4.3.1
(L295–330) and the `FallbackTransportFactory = Callable[[str], Transport]` name-keyed
factory (design L312) are the correct mitigation. Fully consistent.

### CC6 — T1Proxy* / T1Model0* env-var NAMES vs research-notes.md G1 → CONSISTENT ON NAMES; one DOCUMENTED design-vs-env tension (see Finding I-1)
Env-var **NAME** consistency (no values read, per `feedback_aienv_only_proxy_contract`):
- **Model slots:** research-notes G1, design (L467 `T1_MODEL_ENV_PREFIX = "T1Model0"`,
  L490 ladder `("T1Model01","T1Model02")`), 02, 03, 04 all agree the T1 model prefix is
  `T1Model0` → `T1Model01`/`T1Model02`. Fully consistent.
- **Proxy names:** research-notes.md **G1** (L44) states `T1ProxyUrl` + `T1ProxyKey`
  exist as distinct env-var names and **SUPERSEDE** the design §7.3 "reuse T2 proxy"
  default, routed to a `needs_human_decision` HALT. 04 (L246) is aware of the T1 proxy
  name (asserts `T1ProxyKey` must not leak). **02 (§2 L97) describes only the design
  §7.3 "reuse T2 proxy url/key" decision and does NOT echo G1's supersession.** This is
  a documented, gated tension — see Finding I-1 below.

---

## Contradictions & Consistency Findings

### Finding I-1 (Important, NON-BLOCKING) — proxy-binding divergence: 02 states design default; research-notes G1 supersedes it
- **Source A — research-notes.md G1 (L44):** T1ProxyUrl/T1ProxyKey exist; recommends
  `read_env_for_pool(model_prefix="T1Model0", proxy_url_env="T1ProxyUrl",
  proxy_key_env="T1ProxyKey")`; explicitly SUPERSEDES design §7.3; gated behind a
  `needs_human_decision` HALT (rollout step 5) before real dispatch.
- **Source B — design.md §7.3 (L539, L733) + Research 02 (§2, L97 / §3 / §7.3
  references):** reuse the SAME T2 proxy endpoint/key, vary only the model id.
- **Why not fatal:** (1) every code:line fact in 02 is correct — 02 accurately reports
  what the design says; (2) the divergence is a **recommendation** difference, not a
  factual contradiction; (3) research-notes.md G1 — the authoritative consolidation the
  task-builder reads — has ALREADY reconciled it: T1 proxy names exist, recommend using
  them, but HALT for human confirmation vs `~/.aienv`. This aligns with
  `feedback_human_decision_items_must_halt` (needs_human_decision must HALT, not
  auto-default) and `feedback_aienv_only_proxy_contract`.
- **Builder action:** do NOT silently wire the design §7.3 "reuse T2 proxy" default from
  02 for the **real-dispatch** path. Honor G1's `needs_human_decision` HALT: the
  stub-transport rollout (steps 1–4) proceeds proxy-agnostic; the T1 proxy binding
  (T1ProxyUrl/T1ProxyKey vs reuse-T2) is a gated human decision before step 5. 02's
  proxy statement should be read as "design default, SUPERSEDED by G1", not as settled.

### Finding M-1 (Minor) — Research 05 has a contradictory internal Status field
05 header (L3) reads `**Status: In Progress**` while its trailing line (L199) reads
`**Status: Complete**`. Same file, two different status values. The body IS complete
(all 5 sections present with a full builder handoff summary), so this is a stale header
field, not incomplete work. Fix: set the header to `Complete`. Non-blocking.

### Finding M-2 (Minor / informational) — 04's `read_env` range upper bound is loose
04 cites the T2-hardcoded body as "openai_compat.py:179–204"; the function actually ends
at L202. The constant usages 04 points at are real and in-function; the "204" is a
2-line overshoot of the function boundary. No wrong claim, just an imprecise range.

### No true contradictions in code claims
Cross-file, the 5 files describe the SAME symbols identically wherever they overlap:
`build_reflect_contract` location/signature (01≡03≡source), the diversity helpers
(01≡03≡source), the T2 constant family (02≡03≡04≡source), the F1 slot_index root cause
(01≡02≡source), `_collect_t2_models` (02≡03≡source), `read_env` (02≡04≡source), the
test-tree corrections (04≡source≡design§9-patched). No divergent line numbers for any
shared symbol beyond the ±1/loose-range items already noted, all of which 01's delta
table pre-empts.

---

## VERDICT: PASS

Cross-validation integrity holds. All 6 assigned cross-checks pass: 01≡03 on the
additive-kwarg seam, 02≡04 on the F3 `read_env` surface, 04's two BLOCKING path
corrections confirmed against the real tree, design §9 confirmed patched clean, the F1
`slot_index==0` root cause independently proven in dispatch.py + commands.py, and the
T1Model0N / T2 env-var NAMES consistent across all files. Every load-bearing file:line
claim I independently spot-checked matched current source exactly — zero wrong
citations, zero true contradictions.

**Non-blocking items for the builder (do NOT block task-build):**
- **I-1 (Important):** proxy binding — 02 reports the design §7.3 "reuse T2 proxy"
  default; research-notes.md G1 SUPERSEDES it (T1ProxyUrl/T1ProxyKey exist) and routes
  the decision to a `needs_human_decision` HALT before real dispatch. Builder must honor
  the G1 HALT, not auto-wire 02's design default. Already surfaced by G1 — flagged here
  for cross-file awareness.
- **M-1 (Minor):** Research 05 header Status says "In Progress" while its footer says
  "Complete"; body is complete. Cosmetic.
- **M-2 (Minor):** 04's `read_env` range "179–204" overshoots the function end (L202) by
  2 lines; no factual error.

No CRITICAL gaps. No fabrication. No BLOCKING contradictions. Research is
cross-consistent and code-accurate; safe to proceed to task-build with the I-1 HALT
awareness carried forward.

