# Research: Investigation topic 3 (broad investigation of PRD reuse claims & host infrastructure)

**Investigation type:** Investigator
**Scope:** Verify the merged-requirements reuse map against real code — `ClaudeProcess`, swarm loop-guard, auggie-review severity rubric / gh-posting precedent, existing CLI host patterns (sprint/swarm/pipeline), and V1 spec lineage. Flag every claim as CODE-VERIFIED / CODE-CONTRADICTED / UNVERIFIED.
**Status:** Complete
**Date:** 2026-06-11

---

## Investigation framing — why this report differs from its siblings

Reading `research-notes.md` shows the fan-out never partitioned the eight agents: blocks 1, 2,
4, 6, 7, 8 (and this one) were all handed the identical broad scope "verify the spec's reuse
claims." To avoid producing the seventh near-identical reuse-verification report, this agent
(a) confirms the four load-bearing anchors tersely, then (b) spends most of its effort on the
seams the reuse-verification crowd tends to skip: the **`build_env()` allowlist contradiction**
(the spec's INV-001/SC-7 linchpin), the **CLI-group registration seam** (how `superclaude
remediate` actually wires up — the D1 question), **V1.0 spec lineage**, and **whether any `gh`
wrapper already exists** (H5 "New" claim). Findings are tagged CODE-VERIFIED / CODE-CONTRADICTED
/ UNVERIFIED per the staleness protocol.

---

## R2 — `ClaudeProcess` reuse (`cli/pipeline/process.py`) — and the env-allowlist contradiction

**Anchor location — [CODE-VERIFIED]:** `class ClaudeProcess` is defined at
`src/superclaude/cli/pipeline/process.py:72`. The spec's `:72` citation is exact.

**`build_command()` shape — [CODE-VERIFIED]:** `process.py:121-143` emits
`claude --print --verbose <permission_flag> --no-session-persistence --tools default
--max-turns N --output-format <fmt>` then appends `--model` (if set) and `extra_args`. This
matches §7 of the spec verbatim, **including** `--no-session-persistence` and `--tools default`.
`permission_flag` defaults to `--dangerously-skip-permissions` (`process.py:93`), so §6's "only
inside the sandbox" qualifier is a usage constraint, not a code change.

**Prompt-via-stdin — [CODE-VERIFIED]:** §7's claim that the prompt is delivered on stdin to
bypass the 128 KB argv ceiling is real and robustly implemented: `start()` (`process.py:162`)
sets `stdin=subprocess.PIPE` and `_write_prompt_to_stdin()` (`process.py:221-258`) does a
chunked `os.write` with EINTR retry, BrokenPipe capture, and `finally: stdin.close()` for EOF.
There is also a pre-spawn `PROMPT_MAX_BYTES` guard (default **16 MiB**, env-overridable via
`SUPERCLAUDE_PROMPT_MAX_BYTES`) raising `PromptTooLargeForArgv` (`process.py:56-69, 169-173`).
The envelope (R3) therefore has a generous size budget; the §6 "length-capped" opComment cap is
a product decision well under this ceiling, not a primitive limit.

**Constructor already supports the Runner's needs — [CODE-VERIFIED]:** `__init__`
(`process.py:85-116`) already accepts `env_vars: dict[str,str] | None`, `max_turns`,
`output_format`, `timeout_seconds` (default **6300** = 105 min), `model`, `extra_args`, and
lifecycle hooks `on_spawn/on_signal/on_exit`. So §3's Runner can set `max_turns≈30/60`,
`output_format="stream-json"`, and a `cwd`… **except** `ClaudeProcess` exposes **no `cwd`
parameter.** `subprocess.Popen` is called at `process.py:192` with `popen_kwargs` that set
`stdin/stdout/stderr/env` and optionally `preexec_fn=os.setpgrp` — **there is no `cwd=` key.**
The child therefore inherits the parent's working directory.

> **[CODE-CONTRADICTED] — GAP-A (cwd):** §7 says "`cwd` = sandbox checkout" and §3 step (h)
> runs `ClaudeProcess(...)` "inside an ephemeral PR-head checkout." The current primitive
> **cannot** set the child's working directory — `Popen` at `process.py:192` passes no `cwd`.
> Reuse "as-is" is impossible for this requirement. Either (1) add a `cwd` param to
> `ClaudeProcess` (small, clean), or (2) the Runner must `os.chdir()` into the checkout before
> spawning (works because the Runner is a one-shot disposable process). The spec's "Reuse
> as-is" framing in the Reuse Map under-states this — it is a small but real modification.

### The load-bearing finding — `build_env()` is merge-over-`os.environ`, NOT an allowlist

**[CODE-VERIFIED] — `build_env()` at `process.py:145-160`:**

```python
env = os.environ.copy()          # line 155 — FULL parent environment
env.pop("CLAUDECODE", None)
env.pop("CLAUDE_CODE_ENTRYPOINT", None)
if env_vars:
    env.update(env_vars)         # line 159 — ADD/OVERRIDE only, never restrict
return env
```

The docstring states env_vars are "merged with override semantics **after** `os.environ.copy()`."
This is **additive/override**, not **replace/allowlist**.

> **GAP-B — the INV-001/SC-7 linchpin is not satisfiable by passing `env_vars`:** §7 says
> "`build_env()` **MUST be wrapped** with an explicit allowlist `env_vars` (not the current
> full `os.environ.copy()`)" and AC-7 asserts the Runner's `/proc/<pid>/environ` contains **no**
> `GH_TOKEN`/push token and **no** `ANTHROPIC_*` token values. **The current `build_env()`
> cannot deliver this by configuration alone.** Passing `env_vars={...minimal...}` only *adds*
> keys; every variable already in the Dispatcher's `os.environ` — including any `GH_TOKEN`,
> `ANTHROPIC_AUTH_TOKEN`, SSH/proxy vars — **still flows through to the child.** To make AC-7
> pass you MUST change the primitive (or its invocation), not just call it with a dict. Three
> options, in increasing cleanliness:
> 1. **Add an allowlist mode to `ClaudeProcess`** (e.g. `env_mode="replace"` or a new
>    `env_allowlist: set[str]`) so `build_env()` starts from `{}` and copies only allowlisted
>    keys. This is the spec's intent and the right home for the invariant.
> 2. **Subclass/wrap** `ClaudeProcess` in `R2 executor.py`, overriding `build_env()`. Works, but
>    duplicates the CLAUDECODE-strip logic and risks drift.
> 3. **Sanitize `os.environ` in the Runner process before spawn** (the Runner is one-shot, so
>    `os.environ.clear(); os.environ.update(minimal)` is safe). Belt-and-braces but the env
>    construction still lives in the wrong layer.
>
> This is the single most important reuse finding: the spec's headline secret-isolation
> invariant (INV-001, SC-7, AC-7) is a **code change to a shared primitive**, not a
> configuration of it. The build plan (§19 step 5/§16 INV-001 row) should treat "allowlist-env
> for ClaudeProcess" as a first-class task with its own test, because the shared `pipeline`
> primitive is used by sprint/roadmap/swarm and any signature change touches them.

**Reuse caveat for shared-primitive edits:** `process.py` is the *generic* pipeline process
(docstring lines 1-10: "Extracted from sprint/process.py… NFR-007: no imports from
superclaude.cli.sprint or …roadmap"). It is deliberately dependency-free and shared. Adding an
allowlist param is backward-compatible (default to current behavior) but MUST keep that
contract — the remediate Runner must not become an import the generic primitive depends on.

**Key Takeaways**
- `ClaudeProcess:72`, `build_command()`, stdin-prompt delivery, and the `env_vars` constructor
  param are all CODE-VERIFIED and reusable.
- **GAP-A:** no `cwd` parameter — the "sandbox checkout cwd" requirement needs a code change or
  a Runner-side `os.chdir()`.
- **GAP-B (load-bearing):** `build_env()` is additive-merge over the full `os.environ`. The
  spec's secret-isolation invariant (INV-001/SC-7/AC-7) is **not** achievable by passing
  `env_vars` — it requires an allowlist/replace mode added to the primitive. This contradicts
  the Reuse Map's "wrapped with allowlist env, otherwise as-is" framing.

---

## ★ CENTERPIECE FINDING — the V2 Reuse Map omits its single most relevant prior art: `src/superclaude/pr_submit/`

This is the finding the reuse-verification crowd is most likely to miss, because the spec's
Reuse Map never names it and §20 actively says V1.0 is "fully replaced."

**What `pr_submit/` is — [CODE-VERIFIED] `src/superclaude/pr_submit/__init__.py:1-19`:** the
"**Deterministic core for the `sc:pr-submit` PR-review auto-remediation monitor**." This *is*
V1.0 — the predecessor the V2 spec frontmatter cites as `v1_spec:
../20260610-234750-pr-review-auto-remediation/merged-requirements.md` (that V1 brainstorm dir is
CODE-VERIFIED present). It is **not** a stale doc — the source files are dated **today**
(Jun 11 11:28–12:25), i.e. V1.0's Python core is being **landed incrementally right now**, in
parallel with this V2 PRD run. The `__init__.py` docstring says modules are "wired incrementally
as the modules land (see Step 4.3 / Step 5.1)."

**Present & importable today — [CODE-VERIFIED]:** `classifier.py`, `detection.py`, `fsm.py`
(17 KB), `models.py`, `severity_router.py`. **Referenced in the package docstring but NOT yet
created:** `loop_guard.py`, `run_log.py` (write-ahead JSONL run-log), `recovery.py`
(crash-window recovery) — the build is mid-flight. Backing tests already exist:
`tests/pr_submit/{test_autonomy_gates,test_detection_contract,test_monitor_arm,test_skill_parse}.py`.

### The module-to-V2-component overlap is near 1:1 — and it is dramatic

| V2 spec component (claimed **New**) | Already implemented in V1 `pr_submit/` | Evidence |
|---|---|---|
| **H2 Autonomy gate** (§8 lattice, `needs_human_decision` HALT) | `fsm.py` G-arm/G-edit/G-push ordinal gates + `needs_human_decision` pre-gate override; `tests/pr_submit/test_autonomy_gates.py` | `fsm.py:1-17` docstring |
| **H1 round/budget counter** (§9 default 2, cap 5) | `fsm.py` `DEFAULT_MAX_ROUNDS = 2`, `HARD_CAP_MAX_ROUNDS = 5` | `fsm.py` constants block (verbatim match to V2 §9) |
| **§13 poll ≥30s** | `fsm.py` `MIN_POLL_INTERVAL = 30`, `POLL_INTERVAL_ERROR = "minimum is 30 seconds"` | `fsm.py` constants |
| **S1 severity routing** (§17 rubric → troubleshoot depth) | `severity_router.py` `remap_severity()` + `route()`, encodes the rubric's category floor/ceiling table; "NEVER emits the `--depth quick --fix` conflict" | `severity_router.py:1-12` |
| **D6/§19.1 probe-first lock** | `detection.py` `DetectionContract` / `DetectionContractLocked` ("the **T-210** arm gate — probe first") | `detection.py:1-9` |
| **D3 detection 3-state** | `detection.py` `poll_augment_review()` → `polling`/`clean`/`findings`; `classifier.py classify()` | `__init__.py:21-23` |
| **§8 push-decision conjunction** | `fsm.py` `evaluate_push_decision()` + "INV-016 5-predicate G-push conjunction (§5.3)" | `fsm.py:4-6` |
| **Domain models** (Severity, Finding, etc.) | `models.py`: `EventType, Finding, MonitorState, PushDecision, Severity, SkillResult` | `__init__.py:24-31` |
| **H1 two-phase ledger** (§10 write-ahead JSONL) | `run_log.py` (write-ahead JSONL run-log) — *not yet landed but specified* | `__init__.py:9` |
| **§9 intent-without-outcome RESUME** | `recovery.py` (crash-window recovery) — *not yet landed but specified* | `__init__.py:10` |

**The architectural nuance that reconciles "fully replaced" with "huge overlap":** V1's core was
deliberately built with **NFR-6 core purity — "the modules in this package contain ZERO
`gh`/`git` tokens. All `gh`/`git` I/O lives in the skill's bash scripts… the core consumes
already-fetched, already-classified data and records DECISIONS only"** (`__init__.py:13-15`,
echoed in `fsm.py:7-13`, `severity_router.py`, `detection.py`). So V1 already implements the
**exact pure-decision-core / dirty-I/O-shell split** that V2 re-derives as
**Runner-decides / Dispatcher-does-I/O** — except V1 put the I/O in *skill bash*, and V2 wants
the I/O in a *Python systemd daemon*.

> **Therefore §20's "V1.0's in-session Monitor-tool host (fully replaced)" is true only of the
> HOST, not the LOGIC.** Replacing the in-session Monitor host with a systemd Dispatcher does
> **not** require rebuilding the decision core. V2's H1/H2/S1 (autonomy lattice, round/budget,
> severity routing, needs_human_decision HALT, push-decision conjunction) are **already written
> and tested** in `pr_submit/`. Rebuilding them from scratch under `cli/remediate/` would:
> 1. **duplicate** ~3 modules of tested pure logic (drift risk, double-maintenance);
> 2. **re-open settled decisions** — e.g. V2 OD-3 ("push-budget default 2 vs per-thread") is
>    already answered by `DEFAULT_MAX_ROUNDS=2 / HARD_CAP_MAX_ROUNDS=5`;
> 3. risk **divergent severity grading** between the `sc:pr-submit` skill and the `remediate`
>    daemon for the same Augment finding — two code paths, one rubric.
>
> **Recommendation for design/TDD:** Treat `pr_submit/` as the **decision-core dependency** of
> the V2 daemon. The V2 `cli/remediate/` tree should be predominantly the *I/O + host* layer
> (Dispatcher poll/authz/claim/push, Runner sandbox/envelope, gh-wrapper) wrapping the existing
> `pr_submit` pure core — `import superclaude.pr_submit` for `fsm`, `severity_router`, `models`,
> and the forthcoming `run_log`/`recovery`. The Reuse Map (§2, Reuse Map appendix) and §16
> invariant rows (002/005/006/009/018) should be re-pointed at `pr_submit` modules instead of
> "New." This is the highest-leverage correction available to the spec.

**Key Takeaways**
- `pr_submit/` is the **V1.0 implementation, actively landing today**, not a replaced relic.
- Its pure core (`fsm`, `severity_router`, `models`, + planned `run_log`/`recovery`) overlaps
  V2's H1/H2/S1/D3/D6 **near 1:1**; V2 marks all of them "New."
- V1 already embodies V2's pure-core/dirty-shell split (NFR-6 purity) — only the *host* changes.
- The Reuse Map's biggest omission; correcting it removes the most build work from V2.

---

## H1 reuse — swarm "bounded-counter idiom (`cli/swarm/commands.py:2269`)" is a CITATION MISMATCH

**[CODE-CONTRADICTED]:** The spec (§9, Reuse Map) cites `cli/swarm/commands.py:2269` for a
"monotonic, disk-authoritative, survives-restarts" round counter. The **current** line 2269 is
inside `swarm status --watch` and reads `if watch_max_iterations is not None and iterations >=
watch_max_iterations:` — a **watch-loop iteration cap**, not a persisted round/budget counter.
A grep of `commands.py` for `round/rounds/MAX_ROUND/budget/monotonic/disk-authoritative` finds
no matching counter; the nearest "bounded" idiom is the **model-pool wraparound guard**
(`ModelPoolTooSmallError`, ~line 639) which bounds *worker model slots*, not remediation rounds.

This is either stale line drift (the 134 KB file shifted since the spec was written) or a
mis-citation. **Either way the conceptual reuse is weak:** swarm's bounded loops are
in-process/per-invocation, whereas V2 §9 needs a *disk-authoritative, restart-surviving* counter
— which is exactly what V1's planned `pr_submit/run_log.py` + `recovery.py` provide. **The real
reuse target for H1 is `pr_submit`, not swarm.** Recommend re-pointing the §9 / Reuse-Map
citation away from `swarm/commands.py:2269`.

**Atomic-write precedent does exist for §10's "temp + `os.rename`" ledger — [CODE-VERIFIED]:**
`grep os.rename|O_APPEND|tempfile|atomic` finds precedent in `cli/sprint/recovery.py`,
`cli/sprint/rerun_tasks.py`, `cli/sprint/handoff.py`, `cli/sprint/resume/planner.py`,
`cli/recommend/cache.py`, `init_lite.py`. So the *mechanism* §10 wants (atomic temp+rename JSONL)
is well-established in-repo — just not in swarm. Cite one of these for the atomic-write idiom.

**Key Takeaways**
- `swarm/commands.py:2269` does **not** contain the described round counter (CODE-CONTRADICTED).
- Disk-authoritative counter belongs to `pr_submit` (planned `run_log`/`recovery`); atomic-write
  precedent is in `sprint/recovery.py` et al. Re-point both citations.

---

## D1 CLI-group registration seam — `superclaude remediate` wiring is a proven copy-paste — [CODE-VERIFIED]

The spec's D1 decision ("CLI group, not a skill — mirrors sprint/swarm/pipeline") is structurally
correct and the wiring path is trivial. `cli/main.py:400-438` registers **every** group via a
uniform deferred-import idiom at the bottom of the file:

```python
from superclaude.cli.swarm import swarm_group  # noqa: E402,I001  # intentional: deferred ... avoid circular imports
main.add_command(swarm_group, name="swarm")
```

identical lines for `sprint`, `roadmap`, `cleanup-audit`, `tasklist`, `cli_portify`, `prd`,
`eval`, `recommend`, `init-lite`. Adding `superclaude remediate` therefore requires exactly:
(1) a `remediate_group = click.group(...)` in `cli/remediate/commands.py` (matches D1 SoT path),
and (2) one appended `from superclaude.cli.remediate.commands import remediate_group` +
`main.add_command(remediate_group, name="remediate")` pair in `main.py`. The `# noqa: E402,I001`
+ deferred-import convention (to avoid circular imports) must be copied verbatim.

**Key Takeaway:** D1 "New" is correct; the registration seam is a verified, low-risk pattern.
No surprises here — the spec is right that the bot is a CLI group like sprint/swarm.

---

## H5 gh-wrapper — "New" is CORRECT; there is **no Python `gh` caller anywhere** to reuse — [CODE-VERIFIED]

A repo-wide grep (`"gh"`/`'gh'`/`gh api`/`gh pr`/`gh_call`) across `src/superclaude/**/*.py`
returns **zero actual `gh` subprocess invocations** — only a *comment* in `install_hooks.py:68`
("`gh pr create` Bash invocation") and a *docstring* in `pr_submit/classifier.py:25` describing
the shape of `gh pr view --json reviews` output it parses. `IronbellyOrg` appears in Python
**nowhere**; only in two skill/eval markdown files (`sc-pr-submit-protocol/SKILL.md`,
`sc-auggie-review-protocol/evals/evals.json`).

**Implication for C5/SC-4 (the fork-only `--repo` invariant):** today that invariant is enforced
**only by prose convention in skill markdown** (and by the CLAUDE.md rule + `pr-submit` bash
scripts), never by a code-level injector. So H5's promise — "every GitHub-mutating call routes
through `H5.gh_call()` which **unconditionally** injects `--repo IronbellyOrg/IronClaude`… no
code path can call `gh` without it" — is a **genuinely new guarantee with no existing Python
precedent to copy.** This raises a concrete risk the TDD must close:

> **GAP-C:** Because V1's `pr_submit` core is deliberately gh-free (NFR-6) and all its `gh` I/O
> lives in **bash scripts**, V2's Dispatcher/Runner will be the **first Python code in the repo
> to shell out to `gh`.** There is no shared wrapper, no lint rule, and no test ensuring `gh` is
> never called without `--repo`. H5 must ship with (a) a single chokepoint module, (b) a
> unit/integration test asserting injection on every code path (AC-4 covers this), and ideally
> (c) a grep-based CI guard forbidding raw `subprocess([... "gh" ...])` outside `gh.py`.

**Key Takeaways**
- H5 "New" is CODE-VERIFIED correct — no Python `gh` caller exists to reuse.
- C5/`--repo` is currently a *prose* invariant only; V2 makes it the first *code* invariant.
- GAP-C: add a chokepoint + injection test + (optional) CI grep-guard.

---

## S1 severity-rubric reuse — exists AND is already consumed by V1 — [CODE-VERIFIED]

`sc-auggie-review-protocol/refs/severity-rubric.md` exists at the SoT path
(`src/superclaude/skills/sc-auggie-review-protocol/refs/severity-rubric.md`; the earlier
"not found" was a cwd artifact, now corrected). Crucially, V1's `pr_submit/severity_router.py:1-12`
**already encodes this rubric by reference** ("the 5-step remap pipeline DEFINED BY the
auggie-review rubric … §Severity-remap algorithm, lines 63-101 … encodes the rubric's category
floor/ceiling table by reference, it does NOT fork the tier scheme"). So S1 is doubly safe to
reuse: the rubric ref exists, and there is a tested Python encoding of it (`remap_severity`/
`route`) ready to import — reinforcing the centerpiece recommendation.

**Key Takeaway:** S1 reuse is solid; prefer importing `pr_submit.severity_router` over
re-implementing the rubric in `cli/remediate/`.

---

## V1.0 spec lineage — confirms "only the HOST changes" — [CODE-VERIFIED]

`.dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-requirements.md` exists;
topic = **"PR Review Auto-Remediation Monitor (V1.0)"**. It is the `v1_spec` the V2 frontmatter
cites. Decisive lineage statements:

- V1 `FR-2.4`: "The monitor is hosted by the **Monitor tool**; the live session must remain open."
- V1 Out-of-Scope (lines 122-124): "**Detached / headless `claude -p` execution host**" and
  "**The @bot-mention → headless trigger (entire V2.0 — separate brainstorm)**" — explicitly
  deferred to V2.
- V1 Red-Team `R3`: "Session-longevity fragility (in-session host)… **this fragility is the core
  reason V2.0 moves to a headless host.**"

So V2.0 is V1.0's *sanctioned* successor, and the V1 spec itself frames the V2 delta as a **host
swap** (in-session Monitor → headless daemon), not a logic rewrite. This independently confirms
the centerpiece: the `pr_submit/` decision core is shared domain logic to **reuse/extend**, and
§20's "fully replaced" applies to the *Monitor-tool host*, not the FSM/severity/ledger logic.

**Key Takeaway:** V1's own spec says only the host changes for V2 → reuse the decision core.

---

## Gaps and Questions

- **GAP-B (HIGH, load-bearing):** `ClaudeProcess.build_env()` (`process.py:145-160`) is
  additive-merge over the full `os.environ`; passing `env_vars` cannot strip inherited secrets.
  INV-001/SC-7/AC-7 require an **allowlist/replace mode added to the primitive** (or Runner-side
  `os.environ` sanitization), not a config of it. *Question for TDD:* add `env_allowlist` to
  `ClaudeProcess` (touches the shared sprint/roadmap/swarm primitive — needs its own test) vs.
  override in a `remediate.executor` subclass?
- **GAP-A (MED):** `ClaudeProcess` has **no `cwd` parameter** (`Popen` at `process.py:192` omits
  `cwd=`); §7's "cwd = sandbox checkout" needs a code change or a Runner-side `os.chdir()`.
- **GAP-C (MED):** V2's Dispatcher/Runner will be the **first Python `gh` callers in the repo**;
  the C5 `--repo` invariant exists only as prose today. H5 needs a chokepoint module + injection
  test + (optional) CI grep-guard against raw `gh` outside `gh.py`.
- **CENTERPIECE (HIGH):** The Reuse Map omits `src/superclaude/pr_submit/` — the V1.0 decision
  core (fsm/severity_router/models + planned run_log/recovery) that overlaps V2's H1/H2/S1/D3/D6
  near 1:1. *Question for design:* should `cli/remediate/` `import superclaude.pr_submit` for the
  decision core and own only the I/O+host layer? (Strong recommend: yes.)
- **CITATION DRIFT:** `cli/swarm/commands.py:2269` does not contain the round counter the spec
  describes (it's a `swarm status --watch` iteration cap). Re-point §9/Reuse-Map to `pr_submit`
  (counter/ledger) + `sprint/recovery.py` (atomic-write idiom).
- **COORDINATION (process-level):** V1's `pr_submit/` is **landing today, in parallel** with this
  V2 PRD. `loop_guard.py`/`run_log.py`/`recovery.py` are specified but not yet created. *Open
  question:* are V1-core completion and V2-host build sequenced/owned to avoid two teams building
  overlapping ledger/round-counter logic? Not visible in the planning inputs.
- **UNVERIFIED:** `deploy/remediate-bot/` (S2 systemd units/sandbox image) — net-new, nothing on
  disk to verify; sandbox tech (OD-1 container vs microVM) and short-lived-token mechanism
  (OD-2 App vs PAT) remain genuinely open as the spec states.

## Stale Documentation Found

- **§20 "V1.0's in-session Monitor-tool host (fully replaced)"** is *imprecise rather than
  stale*: literally true of the host, but reads as "V1 logic is gone." The V1 *decision core*
  (`pr_submit/`) is alive, tested, and the right reuse target. Recommend rewording to
  "V1.0's in-session Monitor **host** is replaced; the V1 decision core (`pr_submit/`) is
  reused/extended."
- **Reuse Map / §9 citation `cli/swarm/commands.py:2269`** — CODE-CONTRADICTED (points at a
  watch-loop iteration cap, not a disk-authoritative round counter). Stale line number or
  mis-attribution.
- **No genuinely stale capability claims** were found in the spec against current code beyond the
  above; the `ClaudeProcess` line citation (`:72`) and `build_command` shape are exact.

## Summary

The merged-requirements spec is architecturally sound and its small-claim citations
(`ClaudeProcess:72`, `build_command` shape, stdin-prompt delivery, severity-rubric existence,
D1 CLI-group pattern, V1 spec lineage) are **CODE-VERIFIED**. Three reuse claims need
correction, one of them decisive:

1. **★ The Reuse Map omits `src/superclaude/pr_submit/`** — V1.0's deterministic decision core,
   *actively landing today*, whose modules (`fsm`, `severity_router`, `models`, + planned
   `run_log`/`recovery`) map **near 1:1** onto V2's H1 (round/budget, default 2/cap 5 — verbatim),
   H2 (autonomy + `needs_human_decision` HALT), S1 (severity routing), D3/D6 (detection +
   probe-lock). V1 already embodies V2's pure-core/dirty-shell split (NFR-6 "zero gh/git
   tokens"); only the *host* changes (V1's own spec confirms this). **V2 should depend on
   `pr_submit`, not rebuild it** — the single highest-leverage correction.
2. **GAP-B (load-bearing):** the headline secret-isolation invariant (INV-001/SC-7/AC-7) is a
   **code change** to `ClaudeProcess.build_env()` (add allowlist/replace mode), not the
   configuration the Reuse Map implies. Plus **GAP-A** (no `cwd` param) and **GAP-C** (first
   Python `gh` caller — H5 must build the `--repo` chokepoint from scratch; no precedent).
3. **Citation drift:** `swarm/commands.py:2269` is a watch-loop cap, not the described round
   counter; atomic-write precedent for the §10 ledger lives in `sprint/recovery.py` et al.

Net: the spec's *design* survives scrutiny, but its *build accounting* over-states "New" — the
hardest decision logic already exists in `pr_submit/`, and its single hardest invariant
(Runner secret isolation) is under-scoped as "reuse-as-is" when it is a shared-primitive edit.
Correcting the Reuse Map to (a) depend on `pr_submit`, (b) elevate allowlist-env to a first-class
`ClaudeProcess` task, and (c) re-point the swarm/atomic-write citations would materially shrink
and de-risk the V2 build.

---

**Status:** Complete
