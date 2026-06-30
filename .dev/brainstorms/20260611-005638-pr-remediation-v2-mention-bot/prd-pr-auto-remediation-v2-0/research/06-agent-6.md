# Research: Investigation topic 6 (research-notes did not contain an Agent 6 block — investigate broadly using the planning inputs).

**Investigation type:** Investigator
**Scope:** Broad — codebase reuse primitives + integration surfaces referenced by the V2.0 merged-requirements spec, scoped to fill gaps left by Agents 1–5
**Status:** Complete
**Date:** 2026-06-11

> **Differentiation note.** Agents 1, 3, and 7 all converge on verifying the same
> reuse-map primitives (ClaudeProcess existence, swarm loop-guard counter, severity
> rubric, gh-posting precedent). To avoid redundant coverage, this Agent-6 report
> deliberately targets the **integration / host-shape gaps** those reports do not reach:
> (a) where the new `remediate` CLI group actually slots into the existing command tree,
> (b) the precise mechanism of the `build_env` secret-isolation gap the spec flags,
> (c) the net-new GitHub reply/resolve GraphQL surface (does *any* precedent exist?),
> (d) the fork-only `--repo` enforcement precedent, and (e) V1.0 lineage / what is
> being replaced. Findings are tagged CODE-VERIFIED / CODE-CONTRADICTED / UNVERIFIED.

---

## A. CLI Host Integration — where `remediate` slots in

The spec (§2) declares a new `superclaude remediate` CLI group (D1) under
`src/superclaude/cli/remediate/`. I verified the current state and the registration
convention it must follow.

- **[CODE-VERIFIED]** `src/superclaude/cli/remediate/` **does not exist yet** — fully
  net-new, as the spec's "New" column claims. Current sibling groups under
  `src/superclaude/cli/`: `audit`, `cleanup_audit`, `cli_portify`, `eval`, `pipeline`,
  `prd`, `recommend`, `roadmap`, `sprint`, `swarm`, `task_builder`, `tasklist`.
- **[CODE-VERIFIED]** Registration convention (`src/superclaude/cli/main.py:400–438`):
  every group is registered via a **deferred import + `main.add_command(...)`** block at
  the bottom of `main.py`, each carrying the comment
  `# noqa: E402,I001 # intentional: deferred subcommand registration to avoid circular imports`.
  So `remediate` must add: `from superclaude.cli.remediate import remediate_group` +
  `main.add_command(remediate_group, name="remediate")`. This is a one-line-pair edit,
  but the build task **must** carry the same `# noqa` annotation or `make lint` will trip
  on E402 (module-level import not at top of file).
- **[CODE-VERIFIED]** Group-package shape precedent: `swarm/` is the closest structural
  analog to what `remediate/` needs — it has `commands.py` (the Click group),
  `config.py`, `state.py`, `logging_.py`, `dispatch.py`, `models.py`, `schema.py`,
  `transports/`, plus a `tui.py`. The spec's `remediate/` inventory (commands.py,
  dispatcher.py, ingest.py, grammar.py, authz.py, threading.py, runner.py, executor.py,
  envelope.py, sandbox.py, ledger.py, autonomy.py, push.py, reply.py, gh.py) is a
  **larger** but conventionally-consistent fan-out. The spec's claim that the host is "a
  CLI group, not a skill … mirroring how sprint/swarm/pipeline already wrap ClaudeProcess"
  is structurally accurate.
- **Gap flagged:** the spec does **not** mention the `main.py` registration edit or its
  mandatory `# noqa: E402,I001` annotation. This is a small but real omission for the
  build sequencing (§19) — D1 is listed as a component but the wiring step into `main.py`
  is implicit. A build task that creates `remediate_group` without registering it ships a
  dead group (no `superclaude remediate` entrypoint).

**Key Takeaways**
- `remediate/` is genuinely net-new; no name collision, no existing stub.
- The host-shape claim (CLI group à la swarm) is CODE-VERIFIED against the real tree.
- **Missing build step:** `main.py` deferred-import registration with the `# noqa`
  annotation — omitting it = dead command; getting the annotation wrong = lint failure.

---

## B. The `build_env` secret-isolation gap (§7 / INV-001 / SC-7) — mechanism is imprecise

This is the highest-value cross-cut I found. The spec §7 says:
*"`build_env()` MUST be wrapped with an explicit allowlist `env_vars` (not the current
full `os.environ.copy()`)"* and AC-7 asserts the Runner's `/proc/<pid>/environ` contains
no `GH_TOKEN`/push token and no `ANTHROPIC_*` values.

- **[CODE-VERIFIED]** `ClaudeProcess.build_env` (`src/superclaude/cli/pipeline/process.py:145–160`):
  ```python
  env = os.environ.copy()
  env.pop("CLAUDECODE", None)
  env.pop("CLAUDE_CODE_ENTRYPOINT", None)
  if env_vars:
      env.update(env_vars)
  return env
  ```
  The docstring is explicit: *"env_vars … are **merged with override semantics after**
  `os.environ.copy()`."*
- **[CODE-CONTRADICTED]** (mechanism, not intent): passing `env_vars` to the **current**
  `ClaudeProcess` does **NOT** achieve the spec's isolation. `env_vars` is **additive** —
  it `update()`s on top of a full `os.environ` copy. It can *override* a key but cannot
  *remove* keys already present in the parent environment. So if the Dispatcher process
  holds `GH_TOKEN` / a push token / `ANTHROPIC_AUTH_TOKEN` in `os.environ`, those leak
  into every child `ClaudeProcess` regardless of what `env_vars` is passed. AC-7 cannot be
  satisfied by "wrap with allowlist env_vars" as literally written.
- **Two real fixes (the spec implies but does not disambiguate):**
  1. **Code change to `build_env`** — add an `allowlist`/`replace` mode that starts from
     `{}` (or filters `os.environ` down to an allowlist set) instead of `os.environ.copy()`.
     This is a change to a *shared verified primitive* (`pipeline/process.py`), so it must
     be back-compatible (default keep-copy behavior) and re-tested against existing
     sprint/swarm/pipeline callers.
  2. **Sandbox-level minimal environ** (§6) — the Runner runs in an ephemeral sandbox whose
     `os.environ` is *already* minimal (no host home, no `~/.aienv`, no `/config/.claude`),
     so `os.environ.copy()` copies almost nothing dangerous. This is the architecturally
     cleaner path and is consistent with §6, **but** it means the §7 sentence
     "wrap build_env with allowlist env_vars" is doing **no real work** — the isolation
     comes from the sandbox's environment, not from the `env_vars` parameter.
- **Recommendation for build:** treat the isolation guarantee as a property of the
  **sandbox environment construction** (R4) — explicitly build the Runner's environment
  from an empty/allowlist base — and do **not** rely on `ClaudeProcess.env_vars` for
  secret *removal*. If the build instead chooses to modify `build_env`, that edit touches a
  primitive shared by 3+ existing callers and needs its own regression gate.

**Key Takeaways**
- The spec's intent (no push/Anthropic secrets in Runner env) is sound and AC-7 is testable.
- But the cited mechanism (`env_vars` allowlist on current `build_env`) is **CODE-CONTRADICTED**:
  `env_vars` adds/overrides, it never subtracts. `os.environ.copy()` is the leak vector.
- Real isolation must come from a minimal sandbox environ **or** a back-compat `build_env`
  change — this is a design decision the spec leaves implicit and TDD must resolve.

---

## C. ⭐ MAJOR OMISSION — the V1.0 `pr_submit/` Python core (this feature's predecessor)

**This is the single highest-impact finding in this report.** The spec's frontmatter
declares `v1_spec: ../20260610-234750-pr-review-auto-remediation/merged-requirements.md`
and §20 says it replaces "V1.0's in-session Monitor-tool host." But the V1.0 work left
behind a **partially-built, tested Python package** — `src/superclaude/pr_submit/` — that
implements roughly half of V2.0's hardest decision logic, and **the V2.0 reuse map (§2 +
Reuse Map) never mentions it.** The spec lists every V2.0 component as **New** except the
generic primitives (ClaudeProcess, swarm counter, severity-rubric *markdown*).

- **[CODE-VERIFIED]** `src/superclaude/pr_submit/` exists (1060 LOC across 6 modules) and is
  the *"deterministic core for the `sc:pr-submit` PR-review auto-remediation monitor"*
  (per its `__init__.py` docstring). The V1.0 skill `sc-pr-submit-protocol/` (SKILL.md +
  refs) and the v1_spec markdown both exist on disk. It carries **4 test files** under
  `tests/pr_submit/` (`test_autonomy_gates.py`, `test_detection_contract.py`,
  `test_monitor_arm.py`, `test_skill_parse.py`) — i.e. it is tested, not a sketch.

- **[CODE-VERIFIED] What already exists and maps near-1:1 to V2.0 requirements:**
  | V1.0 `pr_submit` artifact (real code) | V2.0 spec requirement it serves |
  |---|---|
  | `fsm.py::evaluate_push_decision` (5-predicate G-push gate) | §8 effective-autonomy cap + HALT short-circuits + AC-4 |
  | `fsm.py::should_halt_rounds` (`>=`, INV-5) | §9 round/budget counter predicate |
  | `fsm.py` `DEFAULT_MAX_ROUNDS=2`, `HARD_CAP_MAX_ROUNDS=5` | §9 / **OD-3** push-budget "default 2, cap 5" — V1.0 **already chose these numbers** |
  | `fsm.py::transition` + `MonitorState` enum (`HALT_HUMAN`, `HALT_MAX_ROUNDS`, `TERMINAL_CLEAN`, `REPORT_ONLY`, …) | §3 control-flow states, §8 HALT, §9 cap-summary |
  | `severity_router.py::remap_severity` / `route` (encodes the rubric by reference) | §17 severity→action matrix + S1 (spec only cites the *markdown* rubric) |
  | `classifier.py` / `detection.py` (3-state, keyed on `augment_bot_login`, probe-locked `DetectionContractLocked`) | §19.1 "probe first" gate + Augment-bot-login config constant |
  | `models.py` `Finding` (`needs_human_decision`, `remapped_severity`, `comment_id`, `in_diff`, `verification_status`) + `SkillResult` (`round_counter`, `push_count`, `reply_count`, `applied_edits`) + `PushDecision` | the exact data carriers for §8/§9/§14 |

- **[CODE-VERIFIED]** `evaluate_push_decision` (`pr_submit/fsm.py:138`) ANDs five predicates
  *immediately before push*: `(1) monitor_ordinal>=3; (2) validation_status=="validated";
  (3) needs_human_decision==false; (4) round_counter<max_rounds; (5) applied_edits>0`, and
  records each predicate independently as a write-ahead audit primitive. **Predicates 2–5
  are V2.0's push gate almost verbatim** (validation-pass, no-human-decision HALT,
  under-budget, real-work). Only predicate 1 (`monitor_ordinal>=3`) is V1.0-specific (an
  *autonomous* monitor needs N polls before acting) and drops out under V2.0's
  *mention-triggered* model.

- **[CODE-CONTRADICTED]** the spec's Reuse Map sends the round/budget counter to the **swarm**
  bounded-counter (`cli/swarm/commands.py:2269`). A *purpose-built* counter predicate for
  this exact feature already exists at `pr_submit/fsm.py::should_halt_rounds` with the
  `>=`-not-`>` semantics V2.0 §9 demands. The swarm counter is a generic idiom; the
  pr_submit one is the domain-correct prior art.

- **[CODE-VERIFIED] What V1.0 documented but did NOT build** (genuine net-new for V2.0):
  the `__init__.py` docstring names `loop_guard.py`, `run_log.py` (write-ahead JSONL), and
  `recovery.py` (crash-window recovery) as modules — **none exist on disk.** `fsm.py:132`
  confirms: *"Phase 8 `loop_guard.py` owns the canonical [predicate]"* — Phase 8 never
  landed. So V2.0's H1 two-phase ledger (§9), §10 JSONL state store, and §9 RESUME
  (intent-without-outcome) are legitimately new — but they were **already designed** in the
  V1.0 module layout and should be built *into* `pr_submit` (or a shared sibling), not
  reinvented under a parallel `remediate/ledger.py` with no awareness of the V1.0 contract.

**Architectural tension worth surfacing to design/TDD:** V1.0 `pr_submit` is built on
**NFR-6 "core purity"** — the package contains *zero* `gh`/`git` tokens; all I/O lives in
the skill's bash glue, and the pure core consumes already-fetched data. V2.0 inverts the
host: an autonomous Python Dispatcher/Runner that does its *own* gh I/O. The clean reuse
boundary is therefore: **reuse the V1.0 pure decision core** (fsm / severity_router /
classifier / models) as the Dispatcher's decision layer, and **build new only the I/O layer
V1.0 deliberately externalized** (gh wrapper, ingest, push, reply/resolve, sandbox). The
spec implicitly rebuilds the decision layer too — that is the missed reuse.

**Key Takeaways**
- ⭐ The spec **omits its own predecessor's tested Python core** (`pr_submit/`, 1060 LOC,
  4 test files). ~Half of V2.0's decision logic (push gate, round counter, severity
  routing, state machine, data models) already exists.
- V1.0 **already chose** `default_max_rounds=2 / hard_cap=5` — V2.0's OD-3 "provisional
  pending probe" is partly already decided in code.
- `evaluate_push_decision` predicates 2–5 == V2.0's §8 push gate; reuse it.
- `loop_guard`/`run_log`/`recovery` were *designed* in V1.0 but never built → V2.0's ledger
  is genuinely new, but should extend the V1.0 module layout, not fork it.
- Reuse boundary = V1.0 pure core (decisions) + V2.0 new I/O layer; this aligns with V1.0's
  NFR-6 core-purity split.

---

## D. GitHub I/O surface — gh wrapper, reply, and resolve are near-zero prior art

The spec's Dispatcher (D2/H3/H4/H5) does substantial autonomous `gh` I/O. I checked what
Python-level GitHub I/O exists today.

- **[CODE-VERIFIED]** `grep -rn 'gh api|subprocess.*gh|"gh"' src/superclaude/ --include=*.py`
  returns **nothing**. There is **no Python `gh` subprocess wrapper anywhere** in the
  package. Every `gh` invocation in the repo today lives in **skill markdown / bash**
  (e.g. `sc-auggie-review-protocol/SKILL.md:307` posts inline comments via
  `gh api repos/<owner>/<repo>/pulls/<PR>/comments`), executed by Claude-in-session, **not**
  by autonomous Python. By design, `pr_submit` is *core-pure* and holds zero gh tokens.
- **Implication:** the spec's **H5 `gh` wrapper (fork-only `--repo` injector)** is not a
  "reuse" — it is a foundational net-new primitive with no Python precedent. The §2 claim
  "every GitHub-mutating call routes through `H5.gh_call()`" is sound but means H5 must be
  built and tested *first* (the spec's §19.2 sequencing correctly front-loads it). The
  fork-only `--repo IronbellyOrg/IronClaude` rule (C5) is enforced today only by **CLAUDE.md
  prose + human discipline**, never by code — H5 would be the *first* mechanical
  enforcement of it. High value, but also high blast radius if wrong (autonomous pushes to
  the wrong repo). Recommend a dedicated unit test that asserts *no* code path can construct
  a `gh` argv lacking `--repo IronbellyOrg/IronClaude`.
- **[CODE-VERIFIED]** `resolveReviewThread`, `reviewThreads`, and any `gh api graphql`
  usage: **zero** occurrences across the entire package. §12's reply-to-thread + resolve
  (matching on `databaseId`, paginating `reviewThreads`) is **100% net-new GraphQL** with
  no in-repo template — the spec's "net-new (absent from repo today)" claim is
  **CODE-VERIFIED**. This is the riskiest unproven surface and correctly depends on the
  §19.1 throwaway-fixture-PR probe to lock the real `databaseId`/`in_reply_to_id` shapes.
- **[CODE-VERIFIED]** `pr_submit/classifier.py:_login_of` already handles **both** GitHub
  payload shapes (`gh pr view --json reviews` → `{"author":{"login"}}` vs REST
  `/pulls/<N>/reviews` → `{"user":{"login"}}`). V2.0's D3 ingest will hit the same dual-shape
  problem; this helper is directly reusable and already tested.

**Key Takeaways**
- No Python `gh` wrapper exists — H5 is foundational net-new, not reuse; build+test first.
- Fork-only `--repo` is enforced today only by prose (CLAUDE.md); H5 is its first code gate.
- reply/resolve GraphQL = zero precedent; highest-risk surface; gated correctly on §19.1 probe.
- `classifier._login_of` dual-shape login parser is reusable, tested prior art for D3.

---

## E. V1.0 → V2.0 lineage — trigger model is the real delta, remediation core is shared

- **[CODE-VERIFIED]** V1.0 (`pr_submit` + `sc-pr-submit-protocol`) is an **autonomous
  monitor**: it *polls* Augment review state, classifies `polling|clean|findings`, and
  auto-remediates findings (hence `monitor_ordinal>=3` before acting — it self-arms). V2.0
  is **mention-triggered**: a human write-collaborator @-mentions the bot on a specific
  review comment, and the *parent* comment is the op-input (§4). The detection layer is
  therefore genuinely different (review-state classification → @-mention detection + parent
  resolution + live authz), but the **remediation, push-gating, counter, severity, and
  audit layers are shared** with V1.0.
- This reframes the spec's novelty honestly: V2.0's *new* surface is (a) mention grammar +
  parent resolution (D4/D6), (b) live per-trigger authz (D5), (c) the split
  Dispatcher/Runner host + sandbox (D2/R4), (d) host-side short-lived-token push (H3), and
  (e) reply/resolve (H4). Its *reusable* surface is the V1.0 decision core (§C). The spec
  treats (a)–(e) as new (correct) **and** treats the decision core as new (incorrect — §C).
- **[UNVERIFIED]** the spec's `needs_human_decision` classes are said to "inherit V1.0 FR-4.4"
  (§8). The *code* carrier (`Finding.needs_human_decision: bool`) exists and is honored in
  `evaluate_push_decision` predicate 3, but the *taxonomy* of what sets that flag lives in
  the V1.0 spec/skill, not obviously in `pr_submit` Python — TDD should confirm whether the
  classifier that *populates* `needs_human_decision` exists in code or only in skill prose.

**Key Takeaways**
- The honest V1→V2 delta is the **trigger model** (autonomous-poll → human-@-mention),
  authz, split host, and reply/resolve — not the remediation/push/counter core.
- `Finding.needs_human_decision` is a real, gated field; the *populating* classifier may be
  prose-only (TDD must verify) — a possible hidden gap behind §8's HALT guarantee.

**Resolution of the UNVERIFIED flag above:** **[CODE-VERIFIED]** `needs_human_decision` is
*consumed* in 5+ places in `pr_submit/fsm.py` (pre-gate HALT at `fsm.py:204` and `:353`,
push-gate predicate 3 at `:158`, propagated at `:384`) and defaults `False` in
`models.py:149` — but `grep 'needs_human_decision = True'` across all of `src/superclaude/`
returns **nothing**. **No Python code sets the flag.** The HALT machinery is built and
tested; the *populator* (the V1.0 FR-4.4 taxonomy: ambiguous intent / security trade-offs /
API-contract changes / multiple valid fixes) is **agent/skill-driven, not code**. For V2.0's
*autonomous* Dispatcher this is a concrete risk: §8's "structurally prevents shipping a
needs_human_decision item as a push" is only as strong as whatever sets the flag — and that
classifier does not exist in code today. TDD must decide whether V2.0 builds a deterministic
populator or continues to trust the in-sandbox agent to self-report it.

---

## Gaps and Questions

1. **Predecessor core omitted from reuse map (HIGH).** `src/superclaude/pr_submit/` (1060
   LOC, 4 test files) implements V2.0's push gate, round counter, severity routing, state
   machine, and data models, yet appears nowhere in §2 or the Reuse Map. Should V2.0's
   H1/H2/S1/§8/§9 *extend* `pr_submit` rather than rebuild under `remediate/`?
2. **`build_env` cannot subtract secrets (HIGH).** §7/AC-7 isolation is unachievable via
   `ClaudeProcess.env_vars` (additive merge over `os.environ.copy()`). Is the isolation a
   sandbox-environ property (preferred) or a back-compat `build_env` change (touches 3+
   callers)? Spec leaves it implicit.
3. **`needs_human_decision` has no code populator (MEDIUM-HIGH).** The §8 HALT guarantee
   rests on a flag nothing in Python sets. Build a deterministic classifier or document the
   agent-self-report dependency explicitly.
4. **`main.py` registration step unspecified (MEDIUM).** D1 needs a deferred-import +
   `add_command` edit in `main.py` carrying `# noqa: E402,I001`; omitted from §19. Without
   it, `superclaude remediate` does not exist.
5. **Round/budget counter mis-routed (MEDIUM).** Reuse Map points at the *swarm* counter;
   the domain-correct `pr_submit/fsm.py::should_halt_rounds` (`>=`, INV-5) is a better base.
6. **OD-3 partly pre-decided (LOW).** V1.0 already chose `default=2 / cap=5`; the spec's
   "provisional pending probe" can cite this as prior art rather than an open question.
7. **reply/resolve GraphQL is the riskiest unproven surface (MEDIUM).** Zero in-repo
   precedent; entirely dependent on the §19.1 probe landing real `databaseId`/`in_reply_to_id`
   shapes. No fallback if the probe is skipped.
8. **H5 `gh` wrapper is the first *code* enforcement of fork-only `--repo` (MEDIUM).**
   Today C5 is prose-only (CLAUDE.md). High value, high blast radius — needs a test asserting
   no argv can omit `--repo IronbellyOrg/IronClaude`.

## Stale Documentation Found

- **`src/superclaude/pr_submit/__init__.py` docstring (lines 5–10)** describes
  `loop_guard.py`, `run_log.py`, and `recovery.py` as constituent modules of the package.
  **[CODE-CONTRADICTED]** — none of the three files exist on disk; only `classifier`,
  `detection`, `fsm`, `models`, `severity_router`, `__init__` are present. The docstring
  hedges ("wired incrementally as the modules land … Step 4.3 / Step 5.1") and `fsm.py:132`
  calls `loop_guard.py` a "Phase 8" module — so this is *aspirational* documentation of a
  partially-built package, not a description of current state. Anyone reading the docstring
  as ground truth would over-estimate V1.0 completeness.
- **Spec §7 (merged-requirements)** "wrap `build_env()` with an explicit allowlist
  `env_vars`" — **[CODE-CONTRADICTED]** in mechanism: `env_vars` cannot remove inherited
  env keys (§B). The *intent* is correct; the *cited mechanism* is stale relative to the
  real `build_env` implementation.

## Summary

Approaching topic 6 as the unassigned/broad investigator, I deliberately avoided the
reuse-map verification that Agents 1, 3, and 7 already cover and instead probed the
**integration and host-shape seams** of the V2.0 spec. The dominant finding is that the
spec **omits its own predecessor's tested Python core** (`src/superclaude/pr_submit/`, 1060
LOC, 4 test files) — which already implements the V2.0 push-decision gate (4 of its 5
predicates are V2.0's gate verbatim), the round-counter predicate, the severity router, the
state machine, the dual-shape login parser, and the `Finding`/`SkillResult`/`PushDecision`
data models, and even pre-chose the §9/OD-3 budget numbers (`default=2 / cap=5`). V2.0's
genuine novelty is the **trigger model** (autonomous-poll → human-@-mention), live authz,
the split Dispatcher/Runner host + sandbox, host-side short-lived-token push, and the
net-new reply/resolve GraphQL — all of which have near-zero Python prior art (there is **no**
`gh` subprocess wrapper anywhere in the package; all gh I/O is skill-bash today). Two
correctness traps stand out: (1) the §7/AC-7 secret-isolation requirement is **not**
satisfiable through `ClaudeProcess.env_vars` because `build_env` merges additively over
`os.environ.copy()` — isolation must come from a minimal sandbox environ; and (2) the §8
HALT guarantee rests on `needs_human_decision`, a flag that **no Python code sets** today.
The clean reuse boundary the spec should adopt: **reuse the V1.0 pure decision core, build
new only the I/O layer V1.0 intentionally externalized** — which also honors V1.0's NFR-6
core-purity split.

**Status:** Complete — EXIT_RECOMMENDATION: CONTINUE
