# Research: Investigation topic 1 (research-notes did not contain an Agent 1 block — investigate broadly using the planning inputs).

**Investigation type:** Investigator
**Scope:** Reuse-map components and prior-art for PR Auto-Remediation V2.0 — `ClaudeProcess` (cli/pipeline/process.py), swarm loop-guard (cli/swarm/commands.py), auggie-review protocol (gh posting + severity rubric), V1.0 spec, gh wrapper conventions
**Status:** Complete
**Date:** 2026-06-11

---

## Greenfield confirmation

`src/superclaude/cli/remediate/` **does not exist** [CODE-VERIFIED via `ls`]. Every D*/R*/H* component in the spec's §2 inventory is genuinely **New**; only the four Reuse anchors (`ClaudeProcess`, swarm counter, severity rubric, auggie-review gh precedent) pre-exist. This is a from-scratch CLI group, not an edit of existing code.

---

## R2 — `ClaudeProcess` headless executor (`src/superclaude/cli/pipeline/process.py`)

The spec's single load-bearing reuse anchor. Read in full.

### What it does (the verified primitive)
- **`class ClaudeProcess`** is defined at **line 72** [CODE-VERIFIED] — the spec's `cli/pipeline/process.py:72` citation is **accurate**.
- Manages one `claude --print` subprocess with process-group signal handling (`os.setpgrp` → `os.killpg`) so the whole child tree dies on shutdown (`terminate()`, lines 278–323).
- **`build_command()` (121–143)** emits exactly what the spec §7 claims: `claude --print --verbose --dangerously-skip-permissions --no-session-persistence --tools default --max-turns N --output-format <fmt>` then `--model` (if set) then `extra_args`. Spec citation is **[CODE-VERIFIED]**.
- **Prompt via stdin, not argv (162–217, 221–258):** `start()` writes the prompt to child stdin in 64 KiB chunks with EINTR-retry and BrokenPipe capture, closing stdin in `finally` to deliver EOF. This is the "bypasses 128KB argv limit" property the spec relies on for large prompt envelopes (§7). **[CODE-VERIFIED]** — the comment at lines 124–125 and 194–197 confirms the MAX_ARG_STRLEN rationale.
- **Pre-spawn size guard:** `PromptTooLargeForArgv` raised when encoded prompt > `PROMPT_MAX_BYTES` (default 16 MiB, env-overridable via `SUPERCLAUDE_PROMPT_MAX_BYTES`, lines 56–58, 169–173).
- **Lifecycle hooks:** `on_spawn(pid)`, `on_signal(pid, sig)`, `on_exit(pid, rc)` — all optional. Useful for the spec's audit-log events (`claude_process_spawn`, §14) without subclassing.
- **`timeout_seconds` default 6300** (~105 min); `wait()` returns `124` on timeout (bash-compatible). The spec's `StuckRun` alert (§14) keys on `ClaudeProcess.timeout_seconds` — that attribute is real and instance-accessible (line 109). **[CODE-VERIFIED]**
- **`tool_write_mode`** (101, 176–178, 325–345): when True, the LLM writes the output file via the Write tool and stdout is redirected to `.log`; `validate_tool_write_output()` confirms the file exists + is non-empty. Relevant if the Runner emits its diff via a tool-written artifact rather than stdout.
- **`output_format`** default `"stream-json"` — matches spec §7's `stream-json` progress-capture requirement.

### ⚠️ Critical gap the spec correctly flags — `build_env()` is NOT an allowlist [CODE-VERIFIED]
`build_env()` (lines 145–160) does:
```python
env = os.environ.copy()          # full host environment
env.pop("CLAUDECODE", None)
env.pop("CLAUDE_CODE_ENTRYPOINT", None)
if env_vars:
    env.update(env_vars)         # callers can only ADD/override, never restrict
return env
```
This is **additive-only**. A caller passing `env_vars={...}` cannot *remove* inherited secrets — `GH_TOKEN`, `ANTHROPIC_AUTH_TOKEN`, `~/.aienv`-sourced vars, etc. all flow into the child via `os.environ.copy()`. The spec's §7 / INV-001 / SC-7 requirement ("`build_env()` MUST be wrapped with an explicit allowlist `env_vars` … No `GH_TOKEN`, no push credential in the Runner env") is therefore a **real, code-grounded change**, not a hypothetical. AC-7 (Runner `/proc/<pid>/environ` contains no token) **cannot pass against the primitive as-is** — the Runner wrapper (R2) must build a minimal env dict from scratch and the reuse must either (a) add an allowlist/replace-mode parameter to `build_env()`, or (b) have the wrapper bypass `build_env()` entirely. This is the single highest-leverage implementation finding for the V2 build.

### Reuse-fit assessment
- **Fits as-is:** stdin delivery, process-group kill, timeout→124, max_turns, stream-json, lifecycle hooks.
- **Gap — no `cwd` parameter:** `start()` does **not** set `cwd` on the Popen call (lines 183–192); the child inherits the spawning process's cwd. Spec §7 says "`cwd` = sandbox checkout" but `ClaudeProcess` has **no `cwd` kwarg** [CODE-CONTRADICTED]. The Runner entrypoint must `os.chdir` into the checkout before instantiating, OR the primitive needs a new `cwd` parameter. Flag for TDD.
- **Needs change:** env isolation (above); optional `cwd` parameter.

**Key Takeaways**
- `ClaudeProcess` at `process.py:72` is real and matches the spec's command/stdin claims exactly.
- `build_env()` is additive-only (`os.environ.copy()`); the allowlist-env requirement (INV-001/SC-7/AC-7) is code-verified-necessary, not speculative.
- No `cwd` parameter exists — spec §7's "cwd = sandbox checkout" needs either a new kwarg or a chdir in the Runner; flag for TDD.
- Lifecycle hooks + `timeout_seconds` cleanly support the spec's audit events and `StuckRun` alert.

---

## V1.0 spec (`../20260610-234750-pr-review-auto-remediation/merged-requirements.md`)

The direct predecessor. V2.0 explicitly supersedes V1's in-session Monitor-tool host (V2 §20: "V1.0's in-session Monitor-tool host (fully replaced)").

### What carried forward vs. what changed
| V1.0 concept | V2.0 disposition |
|---|---|
| In-session **Monitor tool** host (FR-2.4); dies on session close (R3) | **Replaced** by split Dispatcher(systemd)+Runner(sandbox) headless host (V2 §1) |
| `--monitor {0,1,2,3}` ordinal autonomy (FR-4) | Reframed as **lattice** `propose<patch<fix<push<resolve`, default `propose` (V2 §8) |
| Severity→tier routing via reused rubric (FR-3) | **Unchanged** — same rubric reuse (V2 §17) |
| Loop-guard: monotonic capped round counter, `--max-rounds` 2/5 (FR-6.3) | Generalized to **per-PR push budget** (default 2, cap 5) + SHA-correlation (V2 §9) |
| Reply-to-thread + resolve (FR-6.1) | **Unchanged in intent**, hardened with `databaseId` matching (V2 §12) |
| `needs_human_decision` HALT even at top level (FR-4.4) | **Inherited verbatim** (V2 §8) |
| Probe-first discipline (R1, §8.1) | **Inherited** as V2 §19.1 gate-before-parser |
| Trigger = Augment review *posted* | Trigger = **@-mention reply** to a comment (the core V2 pivot) |

### V1 red-team risks still live in V2
- **R1 (detection is guesswork until probed):** V2 §19.1 keeps the throwaway-PR probe gate; the unknowns shifted from "Augment review emission shape" to "`in_reply_to_id` / `databaseId` / Augment bot login" — still must be locked from real data before parser code.
- **R2 (infinite remediation loop):** V2's per-PR push budget + exact-SHA-match round correlation (§9) is the hardened descendant of V1 FR-6.3. V1's warning ("key on reviews-observed-since-arm, not reviews-since-last-poll") maps to V2's "re-review counts as next round ONLY if PR head SHA == bot's recorded push SHA".
- **R3 (session-longevity fragility):** the explicit *reason* V2 exists — moving off the Monitor tool to a headless daemon.
- **R4 (auto-push blast radius):** V2 answers with credential-less propose sandbox + host-side short-lived push token + two-phase ledger.

**Key Takeaways**
- V2.0 is a host-architecture rewrite of V1.0, not a feature add: the *what* (severity routing, reply/resolve, HALT classes, probe-first) is largely conserved; the *how* (in-session→headless split host, ordinal→lattice, round counter→push budget+SHA correlation) is what changed.
- Every V1 red-team risk has a named V2 mitigation — useful as a coverage checklist when validating the V2 spec.
- V1's component naming (`sc:submit-pr` skill) is **abandoned**; V2 is a `superclaude remediate` CLI group (not a skill) because the host runs outside a Claude session.

---

## ⭐ HEADLINE FINDING — `superclaude.pr_submit` deterministic core (the reuse the V2 spec's §2/Reuse-Map MISSES)

The V1.0 spec was **actually implemented** as the skill `sc-pr-submit-protocol` (note: spec calls it `sc:pr-submit`, V1 merged-requirements called it `sc:submit-pr` — naming drifted) backed by an **importable Python package `src/superclaude/pr_submit/`** built **today (Jun 11, untracked `??` on branch `fix/prd-advisory-gate`)**. The V2 spec §2 inventory and Reuse Map cite only `ClaudeProcess`, the swarm counter, the severity rubric, and the auggie-review gh precedent — it **does not mention `pr_submit` at all**, yet `pr_submit` is a far closer behavioral match to V2's deterministic core than any of those.

### Package state (partial build, in-flight)
Present: `models.py`, `severity_router.py`, `classifier.py`, `detection.py`, `fsm.py`, `__init__.py`.
**Referenced-but-absent** (in `__init__` docstring, not imported, not built): `loop_guard.py`, `run_log.py`, `recovery.py`. Tests present: `tests/pr_submit/{test_skill_parse,test_detection_contract,test_autonomy_gates,test_monitor_arm}.py`. So V1's decision core is ~60% built and uncommitted.

### What is directly reusable for V2 (high-value, code-verified)
| V1 `pr_submit` asset | V2 spec section it serves | Reuse fit |
|---|---|---|
| `severity_router.remap_severity()` + `route()` — **pure**, encodes the rubric's category floor/ceiling table, ZERO gh/git tokens (`severity_router.py:88-154`) | §17 Severity→Action Matrix | **Reuse-by-import as-is.** V2's "Critical/High→deep --fix; Medium→--fix; Low/Nit→report; unknown→Medium fail-safe" is *exactly* what `route()` + `_hint_to_severity()` already do. |
| `models.Severity` (5-tier), `models.Finding` with `fix_key = sha256(path+line+body)` comment_id-INDEPENDENT (`models.py:151-162`) | §9 idempotency, §17 | **Reuse with note:** V2 §5 keys idempotency on `(trigger_comment_id, parsed_flag_hash)` — *different* from V1's path+line+body `fix_key`. Both are useful; V2 needs the trigger-keyed claim mutex AND can keep the content-keyed `fix_key` for dedup-across-rounds. |
| `models.EventType` — 33-member **closed** run-log enum (`models.py:19-70`) | §14 audit-log event schema | **Mirror-shape.** V2's event list (`poll, trigger_seen, authz_check, parse_mention, intent, claude_process_spawn, validation, push, reply_posted, round_outcome, ...`) overlaps ~70% but adds authz/mention/intent events and drops the in-session ones. Adopt the closed-enum discipline; extend the member set. |
| `models.PushDecision` — 5-predicate G-push conjunction, each predicate independently assertable (`models.py:190-205`) | §8 autonomy "effective level" lattice-min | **Extract-shared / generalize.** V1's `evaluate_push_decision()` (`fsm.py:138-169`) is `p1 ordinal>=3 ∧ p2 validated ∧ p3 no_human ∧ p4 under_cap ∧ p5 applied_edits>0`. V2's `cap = min over lattice {flag, authz-projection, validation}` THEN off-lattice HALT (`needs_human_decision`, `pr_push_budget==0`) is a **superset** — the V1 conjunction is the L3-push special case. V2 must add the authz-projection predicate and the per-PR-budget predicate (V1's p4 is per-thread round, V2 wants per-PR push budget). |
| `fsm.transition()` table + `should_halt_rounds()` (`>=` fence-post, `fsm.py:129-135,192-246`) | §9 loop-safety, round counter | **Mirror-shape.** V1's monotonic `round_counter` increments at the single edge `S5_AWAITING_REREVIEW → S2_CLASSIFY` (`fsm.py:240-241, 406-407`). V2 generalizes to per-PR push budget + exact-SHA-correlation; the fence-post discipline (`>=` not `>`, increment-at-one-edge) transfers directly. |
| `detection.DetectionContract` + `DetectionContractLocked` (`locked==true` gate before downstream work) | §19.1 probe-first gate | **Mirror-shape.** Same "lock the detection constants from a real probe PR before writing the parser" discipline; V2's constants are `in_reply_to_id`/`databaseId`/Augment-bot-login instead of V1's review-emission shape. |

### ⚠️ The architectural seam that flips between V1 and V2 (critical for reuse)
V1 `pr_submit` enforces **NFR-6 core-purity: the package contains ZERO `gh`/`git` tokens** (`__init__.py:13-15`, `models.py:9-11`, `fsm.py:8-13`). All `gh`/`git` I/O lives in the **skill's bash scripts**; the Python core only *records decisions* via injected recording-only callable seams (`fsm.RunConfig.do_push/do_reply/do_resolve = _noop`). **V2 inverts this layering:** V2 is a `superclaude remediate` **CLI group that performs the gh/git itself** (H3 push, H4 reply/resolve, H5 gh-wrapper). So the reuse is the **pure decision core** (severity_router, models, transition table, push conjunction) — NOT the I/O-via-bash-seams pattern. The V2 implementer should import the pure functions and wire them to *real* H3/H4/H5 callables (replacing the `_noop` seams), keeping the core's purity boundary intact. This is the single most important reuse-architecture note: **V2 reuses the brain, replaces the hands.**

**Key Takeaways**
- `superclaude.pr_submit` is an in-flight (untracked, ~60% built) V1.0 decision core that the V2 spec's Reuse Map omits — it is the closest existing match to V2's §8/§9/§17 deterministic logic and should be added to the V2 reuse inventory.
- `severity_router.py` is reusable-by-import **as-is** for V2 §17 (pure, rubric-faithful). `models.py` enums + `Finding.fix_key` + `PushDecision` are reuse/mirror-shape.
- V1's `evaluate_push_decision()` 5-predicate conjunction is the L3-push special case of V2's lattice-min-plus-HALT; V2 generalizes it (adds authz-projection + per-PR-budget predicates).
- **Layering flips:** V1 keeps the Python core gh/git-free (I/O in bash seams); V2's CLI core does the I/O directly. Reuse the pure brain, supply real hands.
- V1's idempotency `fix_key` (content hash) ≠ V2's claim key (`trigger_comment_id, flag_hash`) — both belong in V2 for different jobs (cross-round dedup vs. trigger claim mutex).

---

## Swarm bounded-counter citation (`cli/swarm/commands.py:2269`) — IMPRECISE

The V2 spec §9 says the round/budget counter "mirrors swarm bounded-counter (`cli/swarm/commands.py:2269`): monotonic, disk-authoritative, survives restarts." **Line 2269 is actually the in-memory `--watch` iteration cap** (`iterations += 1` inside `status_cmd`'s watch loop, bounded by `watch_max_iterations`; `commands.py:2268-2270`) — it is NOT disk-authoritative and does NOT survive restarts. [CODE-VERIFIED]

The *disk-authoritative, restart-surviving* bounded discipline the spec describes actually lives in **`cli/swarm/state.py` (`SwarmState` persistence via `write_state`/`read_state`)** and the model-pool wraparound guard (`ModelPoolTooSmallError`, "preventing silent model reuse via wraparound (D2)", `commands.py:~639`). And the closest *monotonic round counter* idiom in the repo is actually **`pr_submit.SkillResult.round_counter`** (above), not swarm at all.

**Implication for V2:** the swarm:2269 citation is a stale/imprecise line anchor. The idiom (bounded monotonic counter) does exist in the codebase, but V2 should anchor its loop-guard reuse on (a) `pr_submit`'s round-counter fence-post and (b) `swarm/state.py`'s atomic disk-persistence pattern — not the `--watch` iteration cap at line 2269. Flag for the spec's Reuse Map to correct.

**Key Takeaways**
- Spec citation `commands.py:2269` points at the wrong construct (in-memory watch-loop cap, not a disk-authoritative round counter).
- Real reuse anchors: `swarm/state.py` (atomic `write_state`/`read_state`, the §10 atomic-write/flock pattern) + `pr_submit` round counter.

---

## gh posting precedent (auggie-review SKILL) & severity rubric (S1)

### gh posting precedent (template for H4, but reply/resolve are genuinely net-new)
`sc-auggie-review-protocol/SKILL.md` Wave 4 (lines 303-315) is the existing `gh` posting pattern V2 H4 templates from:
- Summary comment: `gh pr review <PR> --comment --body-file <output-dir>/REVIEW.md`
- Inline comment per finding: `gh api repos/<owner>/<repo>/pulls/<PR>/comments -f body=… -f commit_id=<head-SHA> -f path=<file> -F line=<LINE> -f side=RIGHT`
- Capture review URL: `gh pr view <PR> --json reviews -q '.reviews[-1].url'`
- Hard rule: **never `--approve`/`--request-changes`, strictly `--comment`** (line 315, 349) — V2 §20 inherits this verbatim ("Modifying merge state … humans merge").

**Confirmed net-new (spec §12 claim is CODE-VERIFIED):** a repo-wide grep for `resolveReviewThread`, `reviewThreads`, `in_reply_to_id`, and `/comments/.../replies` across `src/superclaude/` returns **0 hits**. The reply-to-thread (`pulls/<N>/comments/<parent_id>/replies`) and GraphQL `resolveReviewThread(threadId)` endpoints in V2 §12 are genuinely absent today — the auggie-review precedent only *posts top-level/inline comments*, it never *replies to a thread or resolves one*. V2 H4 is net-new code, correctly flagged.

### Severity rubric (S1) — confirmed reusable, already consumed
`sc-auggie-review-protocol/refs/severity-rubric.md` is the rubric V2 §17 reuses. It is **already consumed in-code** by `pr_submit.severity_router` (which encodes its category floor/ceiling table by reference, `severity_router.py:30-51`). So V2 doesn't need to re-read the rubric markdown at runtime — importing `pr_submit.severity_router.remap_severity()` gives it the rubric logic already compiled into Python. Strong reuse-by-import path.

### gh-wrapper `--repo` injection precedent (H5)
The fork-only `--repo IronbellyOrg/IronClaude` pin (V2 C5, H5 unconditional injector) has prior art in `sc-pr-submit-protocol/SKILL.md:83,108` (every `gh` call pins `--repo IronbellyOrg/IronClaude`) and in the project CLAUDE.md ABSOLUTE RULE. V2's H5 (a Python `gh_call()` that unconditionally injects `--repo`) is net-new *as code* but the contract is well-established. No existing Python `gh` wrapper enforces this — the precedent is skill-prose discipline, so H5's structural enforcement (no code path can omit `--repo`) is a genuine hardening, not a duplicate.

**Key Takeaways**
- H4's *summary/inline posting* has a clean template in auggie-review Wave 4; H4's *reply-to-thread + resolve* is genuinely net-new (0 repo hits — spec §12 verified).
- The severity rubric is reusable, and is **already compiled into `pr_submit.severity_router`** — V2 should import that rather than re-parse the markdown.
- `--repo` fork-pin is established as prose discipline (CLAUDE.md + pr-submit skill) but has **no Python enforcement primitive** — H5 is a legitimate net-new hardening.

---

## Gaps and Questions

1. **Reuse Map omits `pr_submit` (highest-impact gap).** The V2 spec §2 inventory + Reuse Map should add `superclaude.pr_submit` (`severity_router`, `models`, `fsm.evaluate_push_decision`/`transition`, `detection.DetectionContract`) as reuse anchors. As written, V2 marks H2 (autonomy), H1 (ledger/idempotency), and S1 (severity routing) as **New** when a ~60%-built decision core already exists. Recommend the V2 design/TDD explicitly decide: import-and-extend `pr_submit`, or fork it. (Note: `pr_submit` is untracked/uncommitted — coordinate so V2 work doesn't race or duplicate the in-flight V1 build.)
2. **`ClaudeProcess.build_env()` is additive-only** — INV-001/SC-7/AC-7 require an allowlist-env wrapper. Open design question: add a `replace_env`/allowlist parameter to the shared primitive (affects sprint/swarm/pipeline callers), or have the Runner build its env dict and bypass `build_env()`? The former is cleaner but touches a shared file; the latter keeps the blast radius in `remediate/`.
3. **`ClaudeProcess` has no `cwd` parameter** but spec §7 says "`cwd` = sandbox checkout." Resolve in TDD: add `cwd` kwarg vs. `os.chdir` in the Runner entrypoint.
4. **Idempotency key dual-definition.** V1 uses content hash `fix_key=sha256(path+line+body)`; V2 §5 uses `(trigger_comment_id, parsed_flag_hash)`. These serve different jobs (cross-round dedup vs. trigger claim mutex). The V2 ledger (H1) must implement BOTH and the spec should say so explicitly — currently §5/§9 only name the trigger key.
5. **Swarm citation `commands.py:2269` is wrong** (in-memory watch-loop cap, not disk-authoritative). Correct the Reuse Map anchor to `swarm/state.py` + `pr_submit` round counter.
6. **EventType enum divergence.** V1's 33-member closed enum and V2's §14 event list overlap but differ (V2 adds authz/mention/intent/claude_process_spawn; drops in-session events). Whoever builds V2's audit schema should start from `models.EventType` and extend, not author from scratch — but the member sets are not interchangeable.
7. **Probe-first constants unknown until run.** V2 §19.1 (and V1 R1) both gate on a real throwaway-PR probe to lock `in_reply_to_id`/`databaseId`/Augment-bot-login. None of these are in the repo yet — this remains the #1 build-blocking unknown. No code can substitute for the probe.
8. **`loop_guard.py`/`run_log.py`/`recovery.py` referenced but unbuilt in `pr_submit`.** V2's §9 (loop-safety) and §10 (two-phase ledger) overlap heavily with these unbuilt V1 modules. Decide whether V2 builds them under `remediate/` (its own two-phase ledger) and lets V1 stay stubbed, or whether a shared module emerges.

## Stale Documentation Found

- **V2 spec Reuse Map / §2 inventory — incomplete (not stale, but missing prior art):** omits `superclaude.pr_submit` entirely. Components H2/H1/S1 are marked **New** despite a substantial reusable core existing. [Evidence: `src/superclaude/pr_submit/*.py` present and tested; not in spec.]
- **V2 spec §9 citation `cli/swarm/commands.py:2269` — imprecise/stale anchor.** Line 2269 is an in-memory `--watch` iteration counter, not the "monotonic, disk-authoritative, survives restarts" construct described. [CODE-VERIFIED at `commands.py:2268-2270`.]
- **V2 spec §7 implies `ClaudeProcess` accepts `cwd`** ("cwd = sandbox checkout"); the primitive has no such parameter. [CODE-CONTRADICTED at `process.py:162-192`.]
- **V1 merged-requirements names the skill `sc:submit-pr`**; the built skill is `sc-pr-submit-protocol` / `sc:pr-submit`. Naming drifted between spec and implementation — minor, but worth noting when cross-referencing.
- All *positive* spec citations that were checkable were **accurate**: `ClaudeProcess` at `process.py:72`, the `build_command()` flag string, stdin-not-argv delivery, `timeout_seconds`, and the "reply/resolve are net-new" claim (§12) all CODE-VERIFIED.

## Summary

This investigation (run broadly, since no Agent 1 block existed in research-notes) traced the V2.0 PR Auto-Remediation spec's reuse anchors and prior art against the live codebase. **Headline:** the V2 spec's Reuse Map is materially incomplete — it omits `superclaude.pr_submit`, an in-flight (untracked, built today, ~60% complete) deterministic decision core that already implements V2's severity routing (`severity_router.py`, pure + rubric-faithful, reusable-by-import as-is), the 5-predicate push conjunction (the L3 special case of V2's lattice-min-plus-HALT), the single-FSM transition table with a monotonic round counter, the closed run-log EventType enum, and the detection-contract-lock probe gate. The single highest-leverage architectural note: **V2 should reuse `pr_submit`'s pure brain but replace its hands** — V1 deliberately keeps the Python core gh/git-free (I/O in bash seams, NFR-6), whereas V2 is a CLI group that performs gh/git directly, so the reuse is the pure decision functions wired to real H3/H4/H5 callables.

Three concrete code-grounded build risks surfaced: (1) `ClaudeProcess.build_env()` is additive-only `os.environ.copy()`, so the spec's allowlist-env requirement (INV-001/SC-7/AC-7) is verified-necessary and currently unsatisfiable without a primitive change or Runner-side env construction; (2) `ClaudeProcess` has no `cwd` parameter the spec assumes; (3) the swarm bounded-counter citation (`commands.py:2269`) points at the wrong construct. All positive, checkable spec citations (`ClaudeProcess` location, command flags, stdin delivery, reply/resolve being net-new, severity rubric reuse) were CODE-VERIFIED accurate. The probe-first unknowns (`in_reply_to_id`/`databaseId`/Augment-bot-login) remain the #1 build-blocking gap that no existing code can resolve.

EXIT_RECOMMENDATION: CONTINUE
