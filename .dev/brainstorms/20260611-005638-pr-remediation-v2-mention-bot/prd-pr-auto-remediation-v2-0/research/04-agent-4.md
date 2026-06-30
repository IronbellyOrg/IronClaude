# Research: Investigation topic 4 (broad investigation from planning inputs)

**Investigation type:** Investigator
**Scope:** Reuse-target verification + integration-surface investigation for the V2.0 Mention-Triggered Headless Remediation Bot spec. (No Agent 4 block existed in research-notes; scope chosen to cover the spec's load-bearing reuse claims and integration seams that other agents likely under-covered.)
**Status:** Complete
**Date:** 2026-06-11

---

## Investigation Plan — DIFFERENTIATED SCOPE

**Discovery that reshaped this report:** On reading the sibling research stubs (`01`–`08`), I found
that Agents 1, 2, 3, 5, 6, 7, and 8 **all independently chose the identical investigation** —
"verify the reuse claims" (`ClaudeProcess`, swarm loop-guard, severity rubric, gh-posting). That is
7-way redundant coverage of the *Reuse* primitives. To avoid an 8th duplicate, Agent 4 deliberately
pivots to the surfaces those reports structurally **miss**: the **net-new infrastructure** the spec
proposes (§2 marks ~16 of 18 components "**New**"). That is where the real build risk and the real
unknowns live — and nobody else is looking there.

**Agent 4's differentiated questions:**

1. **Greenfield audit** — for each net-new component (D2 dispatcher, D3 ingest/ETag, D6 parent-resolver,
   R4 sandbox, H1 ledger, H3 push, H4 reply/resolve, S2 systemd), does the repo have ANY adjacent
   precedent to reuse, or is it truly greenfield? (Determines effort honesty of §19.)
2. **GitHub API integration surface** — any existing `gh api` polling, ETag/304, comment ingest,
   `in_reply_to_id`, GraphQL `resolveReviewThread`, `reviewThreads` precedent? (§3, §4, §12, §13)
3. **Sandbox/isolation feasibility** — any Docker/Podman/Firecracker/container precedent in-repo? (§6, OD-1)
4. **State-store primitives** — atomic-write (`os.rename`), `flock`, JSONL append-only ledger,
   `O_APPEND` precedent the H1 ledger could reuse? (§9, §10)
5. **`gh --repo` enforcement** — does a `gh` wrapper that injects `--repo IronbellyOrg/IronClaude`
   already exist, or is H5 net-new? What does `.claude/settings.json` permit? (C5, H5)
6. **systemd/deploy precedent** — does `deploy/` exist? Any `.service`/`EnvironmentFile` units? (§15)
7. **Secondary check on the one already-spotted contradiction** — the swarm `:2269` citation.

**Reuse primitives (covered exhaustively by 7 sibling agents):** Agent 4 records only deltas/
corrections, not a full re-verification, to respect the no-duplication protocol.

---

## Finding 1 — Greenfield audit: `cli/remediate/` does NOT exist (spec's "New" markings are honest)

**[CODE-VERIFIED]** `ls src/superclaude/cli/remediate/` → `No such file or directory`. None of
D1–H5 exist today. The §2 inventory's ~16 "**New**" markings are accurate — this is a greenfield
CLI group. **No false-reuse risk** on the new components themselves.

But the greenfield framing **undersells two strong adjacent precedents the spec never cites** (see
Findings 2 and 5), so §19's effort profile is *pessimistic*, not optimistic — there is more to
reuse than the Reuse Map admits.

### Key Takeaways
- `cli/remediate/` is greenfield — confirmed, no collision.
- The spec's Reuse Map is **under-inclusive**: it lists 5 reuse items but misses `pr_submit/`
  (FSM monitor precedent) and `install_hooks.py` / `sprint/recovery.py` (atomic-write + replay).

---

## Finding 2 — MAJOR MISSED REUSE: `pr_submit/` FSM is a direct precedent for the Dispatcher (D2)

**[CODE-VERIFIED]** `src/superclaude/pr_submit/fsm.py` and `pr_submit/models.py` exist, plus the
`sc-pr-submit-protocol` skill (`src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`). This skill
already implements a **PR-monitoring FSM** with autonomy levels (`--monitor 0..L`, "the FSM never
leaves `S0_IDLE`"), and its **Wave 0** already encodes the exact `gh pr create --repo
IronbellyOrg/IronClaude` discipline, `git remote -v` origin check, rebase-if-behind, and
returned-URL-owner verification the V2.0 spec re-specifies from scratch in C5/§3.

**Why this matters for the PRD:** the V2.0 Dispatcher (D2) is described as a novel "poll → detect →
authz → claim → dispatch" state machine. `pr_submit/fsm.py` is a **pre-existing PR-event FSM with a
monitor loop and a level/autonomy ladder** — the same shape. The spec's §8 autonomy lattice
(`propose < patch < fix < push < resolve`) closely mirrors pr_submit's `--monitor` L0..Ln ladder.
**Recommendation:** the design phase should evaluate `pr_submit/fsm.py` as the skeleton for D2/H2
rather than treating the Dispatcher as fully net-new. At minimum it is prior art for the
state-machine + autonomy-level structure and for the C5 gh discipline.

### Key Takeaways
- `pr_submit/fsm.py` = an existing PR-monitoring finite-state machine with an autonomy ladder —
  **strong, uncited reuse candidate** for D2 (dispatcher) and H2 (autonomy gate).
- `sc-pr-submit-protocol` already codifies the C5 `--repo IronbellyOrg/IronClaude` + pre-PR-check
  discipline that §3/§5/H5 re-derive.
- Action for design: add `pr_submit/` to the Reuse Map; do not greenfield the FSM.

---

## Finding 3 — GitHub API integration surface (ETag/threading/GraphQL) is genuinely net-new

**[CODE-VERIFIED]** Grep across `src/superclaude/` for `If-None-Match | ETag | in_reply_to_id |
resolveReviewThread | reviewThreads | X-RateLimit` returns **zero code hits**. The only matches are
prose in `sc-auggie-review-protocol/SKILL.md:307` (`gh api repos/<owner>/<repo>/pulls/<PR>/comments`)
and `commands/auggie-review.md:50` (inline comments "via `gh api`").

**Implication:** D3 (ETag/304 cursor ingest), D6 (`in_reply_to_id` parent resolution), §13
(rate-limit `If-None-Match`/`Retry-After`/`X-RateLimit-Remaining`), and H4 (GraphQL
`resolveReviewThread` + `reviewThreads` pagination on `databaseId`) have **no in-repo precedent**.
The auggie-review skill posts *summary + inline* comments but never *polls*, never handles ETag,
and never resolves a thread. These are the **highest-novelty, highest-risk** components and they
correctly carry the §19.1 "probe-first" gate. This validates the spec's instinct to lock
`in_reply_to_id` / `databaseId` shapes against a throwaway fixture PR **before** writing parser code.

### Key Takeaways
- ETag polling, comment threading, and `resolveReviewThread` GraphQL = **truly greenfield**; the
  §19.1 probe-first gate is well-placed and should be treated as a hard prerequisite, not optional.
- Only posting precedent (`gh pr review --comment` / `gh api ... /comments`) exists — it is a
  *template* for H4's reply, but the **resolve** half (GraphQL thread-node matching) is brand new.

---

## Finding 4 — C5 (`--repo` injection) is enforced today by PROSE ONLY, not code

**[CODE-VERIFIED]** `--repo IronbellyOrg/IronClaude` appears only in skill/markdown docs
(`sc-pr-submit-protocol/SKILL.md:83,108`, `sc-auggie-review-protocol`) and in CLAUDE.md rules — there
is **no code-level wrapper** that injects `--repo` into `gh` calls. The `offer-pr-review.sh` hook
only *pattern-matches* `gh pr create` to surface a suggestion; it does not rewrite the command.

**Implication for H5 (the gh wrapper / fork-only `--repo` injector):** H5 would be the **first
code-level enforcement** of C5. Today C5 is a discipline (CLAUDE.md + memory
`feedback_pr_target_fork_only.md`) that the operator was previously burned by (PR landed on upstream).
The spec's claim in §3 that "no code path can call `gh` without it" is therefore a **net-new
guarantee**, not a reuse — a strengthening. This is a *positive* finding: H5 closes a real,
historically-exploited gap. Design should make H5 the **single** `gh` entry point (no raw
`subprocess.run(["gh", ...])` anywhere in `cli/remediate/`) and add a test that greps the package
for un-wrapped `gh` invocations.

### Key Takeaways
- No existing code injects `--repo`; C5 is convention-only today → H5 is a genuine hardening.
- Recommend a lint/test guard: zero raw `gh` calls in `cli/remediate/` outside `gh.py` (H5).

---

## Finding 5 — MISSED REUSE: atomic-write + JSONL-replay primitives already exist for H1 ledger

**[CODE-VERIFIED]** The §10 state-store design (atomic temp-write + `os.rename`, append-only JSONL,
replay-on-restart) has **multiple in-repo precedents the Reuse Map omits**:
- `cli/install_hooks.py:408,443` — *"Atomic write: tempfile in same dir + os.replace"* — exactly the
  §10 "temp + `os.rename`" pattern, already implemented and tested.
- `cli/recommend/telemetry.py` + `recommend/commands.py:27` — append-only **JSONL telemetry ledger**
  (`.claude/cache/sc-recommend-events.jsonl`).
- `cli/sprint/recovery.py:439` + `sprint/resume/planner.py:46,254` — `execution-log.jsonl` with
  **resume/replay semantics**: the planner reads the JSONL to reconstruct in-flight state after a
  crash. This is the closest analog to the spec's §9 **two-phase intent/outcome RESUME** invariant
  (intent-without-outcome ⇒ re-verify, don't re-execute).
- `cli/cli_portify/logging_.py:60,175` — **dual-format** `execution-log.{jsonl,md}` writer — directly
  parallels §14's "JSONL audit log distinct from the state ledger."

**Implication:** H1 (two-phase ledger) and §14 (audit log) should be built **on top of these
patterns**, not from scratch. In particular `sprint/recovery.py`'s replay logic is a working model
for "intent without matching outcome = RESUME." The spec's §10/§9 are sound but the build estimate
should drop because the atomic-write and JSONL-replay wheels already exist.

### Key Takeaways
- `install_hooks.py` atomic-write helper + `sprint/recovery.py` replay = direct H1/§9 reuse.
- `cli_portify/logging_.py` dual jsonl+md writer = direct §14 audit-log reuse.
- These belong in the Reuse Map; their omission makes §19 over-estimate the ledger work.

---

## Finding 6 — Sandbox runtime (OD-1) and systemd/deploy (S2) are fully greenfield

**[CODE-VERIFIED]** No `Docker run` / `podman` / `firecracker` / `--network none` / `seccomp` /
`bubblewrap` / `nsjail` runtime usage anywhere in `src/superclaude/`. `Dockerfile` appears only as a
*string literal* in audit/orchestration classifiers (`audit/profiler.py:61,149`,
`MODE_Orchestration.md`), not as a real container the project builds or runs. **`deploy/` directory
does not exist.** No `.service` / `.timer` / `WatchdogSec` / `EnvironmentFile` / `NoNewPrivileges`
anywhere (`grep` = 0).

**One partial precedent:** `cli/eval/isolation.py` implements a `ScratchRootViolation` /
scratch-root **filesystem** isolation model (eval sandboxes confined to a scratch root). That is
*filesystem confinement*, not *process/network* sandboxing — relevant to R4's "disposable clone of
PR head" workspace discipline, but it does **not** provide the container/VM, deny-by-default network,
or non-root base image the §6 sandbox requires.

**Implication:** §6 (sandbox), OD-1 (container vs microVM), and S2 (systemd units + sandbox image,
`deploy/remediate-bot/`) are **the largest genuinely-greenfield build surface** and carry the most
operational unknowns. The spec correctly flags OD-1 as an open decision. `eval/isolation.py` is worth
citing as prior art for the *scratch-root checkout* discipline only.

### Key Takeaways
- Container/microVM sandbox + systemd deploy = **zero in-repo precedent** → highest build risk + the
  bulk of the net-new work; OD-1 must be resolved early (it gates R4/S2/§15).
- `eval/isolation.py` scratch-root model = partial prior art for R4's filesystem confinement, not
  for network/process isolation.

---

## Finding 7 — HEADLINE: `sc:pr-submit` (`pr_submit/`) is a tested V1.5 of this exact bot

This is the most consequential finding of Agent 4's differentiated sweep, and it is **invisible to
the 7 agents verifying only the spec's cited reuse** (they check swarm:2269 + ClaudeProcess; they do
not search for *better, uncited* prior art).

**[CODE-VERIFIED]** `src/superclaude/pr_submit/fsm.py` + `pr_submit/models.py`, with a live test
suite (`tests/pr_submit/test_autonomy_gates.py`, `test_detection_contract.py`, `test_monitor_arm.py`,
`test_skill_parse.py`), already implement the **decision core** the V2.0 spec re-specifies as
net-new. Concrete 1:1 correspondences:

| V2.0 spec element | Already in `pr_submit` | Evidence |
|---|---|---|
| §9 per-PR push budget **default 2, cap 5** | `DEFAULT_MAX_ROUNDS = 2`, `HARD_CAP_MAX_ROUNDS = 5` | `fsm.py:38-39` |
| §13 **poll ≥30s** floor | `MIN_POLL_INTERVAL = 30`, `"minimum is 30 seconds"` | `fsm.py:40,42` |
| §9 bounded round counter + HALT | `should_halt_rounds(round_counter, max_rounds)` | `fsm.py:129` |
| §8 autonomy lattice `propose<patch<fix<push<resolve` | `--monitor {0,1,2,3}` ordinal "capability ceiling" + `MonitorState` lattice | `fsm.py:70`, `models.py:83` |
| §8 effective-autonomy 5-predicate cap (INV-016) | `evaluate_push_decision(...)` 5-predicate G-push conjunction | `fsm.py:138-156` |
| §8 `needs_human_decision` HALT short-circuit | `needs_human_decision` pre-gate override (§5.2) | `fsm.py:3-4`, `MonitorState.HALT_HUMAN` |
| §14 audit-log **event taxonomy** | `EventType` enum: `POLL_ATTEMPT, POLL_RESULT, API_BACKOFF, REVIEW_DETECTED, ROUND_INCREMENTED, ROUTE_DECISION, PUSH_DECISION, PUSH_INITIATED, PUSH_COMPLETED, REPLY_POSTED, THREAD_RESOLVED, IDEMPOTENCY_SKIP, TERMINAL_*` | `models.py:29-70` |
| §12 reply + resolve **states** | `MonitorState.S6_REPLYING` / `RESOLVING`; events `REPLY_POSTED` / `THREAD_RESOLVED` | `models.py`, `fsm.py:16` |
| §6/§7 Dispatcher/Runner secret split (decisions vs side-effects) | fsm.py core-purity: *"imports NO `anthropic` SDK… ZERO shell / version-control command tokens… records DECISIONS only"* | `fsm.py:9-15` |

**The architectural delta is real but narrow.** `sc:pr-submit` runs **in-session** as a skill FSM;
V2.0 runs **out-of-session** as a systemd daemon that spawns `claude -p`. That changes the *host*
(in-session vs daemon) and the *trigger* (own PR submission vs @-mention by a third party) — but the
**autonomy/round/push-decision/reply-resolve/event-taxonomy decision core is the same machine**, and
it is already tested. The V2.0 spec's §8/§9/§12/§14 should be re-grounded on `pr_submit/fsm.py` +
`models.py` instead of re-deriving them; the swarm:2269 citation for the counter is both wrong
(Finding 8) and unnecessary (pr_submit's `should_halt_rounds` is the real thing).

**Caveat — the genuinely-new half stands:** pr_submit's FSM *records decisions only*; the actual
`gh`/GraphQL side effects are NOT in `pr_submit` (no `.sh` scripts; grep for
`resolveReviewThread|in_reply_to_id|databaseId|ETag` across `sc-pr-submit-protocol/` = 0). So §3-§4
ingest, §12 GraphQL resolve, and §13 ETag remain net-new *implementation* (Finding 3). The reuse is
the **decision/state/event model**, not the I/O.

### Key Takeaways
- **`pr_submit/fsm.py` + `models.py` + `tests/pr_submit/` = a tested decision core for D2/H1/H2/H4**;
  this is the single largest reuse opportunity in the whole PRD and it is **absent from the Reuse Map**.
- The spec's §14 event taxonomy is ~80% already enumerated (and tested) in `models.py EventType`.
- Re-ground §8/§9/§12/§14 on pr_submit; keep §3/§4/§12-impl/§13 as the true net-new I/O surface.
- **Strong recommendation:** the design phase MUST reconcile V2.0 against `sc:pr-submit` — they are
  near-siblings, and shipping a parallel-but-divergent autonomy/round machine is exactly the kind of
  duplication the project's SoT discipline exists to prevent.

---

## Finding 8 — CORRECTION: the swarm `:2269` counter citation is wrong (twice over)

**[CODE-CONTRADICTED]** §9 and the Reuse Map cite the swarm "bounded-counter" at
`cli/swarm/commands.py:2269` as a *"monotonic, disk-authoritative, survives restarts"* round/budget
counter. **Line 2269 is not that.** It is the `--watch-max-iterations` guard of the `status`/`logs`
**watch-polling loop** (`iterations += 1; if … iterations >= watch_max_iterations: break`,
`commands.py:2267-2270`) — an in-memory loop bound for the test surface, explicitly described at
`commands.py:2028` as *"keeps the test surface fast,"* with no disk persistence and no round/budget
semantics.

The **real** swarm disk-authoritative state primitive is `cli/swarm/state.py:write_state` (line 137)
— atomic `.tmp` + `os.replace`, output-confined (`OutputConfinementError`), persisting
`.swarm-state.json` across restarts (`commands.py:697` `F-P3-3`). So the citation should be
**re-pointed** from `commands.py:2269` → `swarm/state.py:write_state` for the *persistence* idiom,
and the *counter* idiom should come from `pr_submit/fsm.py:should_halt_rounds` (Finding 7), not swarm
at all.

### Key Takeaways
- `commands.py:2269` = watch-loop iteration guard, **not** a round/budget counter → spec citation is
  incorrect.
- Persistence reuse = `swarm/state.py:write_state` (atomic, confined); counter reuse =
  `pr_submit/fsm.py:should_halt_rounds`. Fix both citations before TDD.

---

## Finding 9 — `_atomic_write_json` and bash-`flock` confirm §10's mechanics, but flock is Python-net-new

**[CODE-VERIFIED]** §10's atomic-write requirement is fully satisfied by existing code:
`install_hooks.py:443 _atomic_write_json` (tempfile in same dir, `os.replace`, cleanup in `finally`)
and `swarm/state.py:write_state` (same idiom). Reuse is direct.

**[CODE-VERIFIED, gap]** §9's *"Per-PR `flock` serializes tree mutations"* has a **bash** precedent
only: `flock` is used in the freshness hook scripts (`freshness-file-changed.sh:48-50` does a flocked
append to `changes.jsonl`; `freshness-pre-edit.sh:49-51`, `freshness-session-start.sh:40-42`,
`freshness-subagent-start.sh:14-18`). There is **no `fcntl.flock` in any Python module** in
`src/superclaude/`. So H1's per-PR lock is net-new in Python — trivial (`fcntl.flock(fd, LOCK_EX)`),
but worth flagging that the codebase has no Python file-locking pattern to copy; the bash hooks are
the only in-repo model, and they fail-open (`flock … || true`), which H1 must **not** do (a failed
lock acquisition for a *push* serializer should fail-closed, not fall through).

### Key Takeaways
- Atomic write: **fully reusable** (`install_hooks.py:443`, `swarm/state.py:137`).
- Python `flock`: **net-new**; only bash precedent exists, and it is fail-open — H1's push serializer
  must invert that to fail-closed.

---

## Gaps and Questions

1. **G-1 (highest priority): the spec does not reconcile against `sc:pr-submit`.** `pr_submit/`
   is a tested PR-monitoring autonomy/round/reply-resolve FSM — a near-sibling of V2.0 — and it is
   absent from the Reuse Map. Before any build, design MUST answer: *does V2.0 extend/wrap
   `pr_submit/fsm.py`, or does it justify a separate decision core?* Shipping a parallel-but-
   divergent autonomy machine would be a serious SoT/duplication violation. (Finding 7)
2. **G-2:** Two spec citations are wrong/weak — swarm `commands.py:2269` (Finding 8). Re-point to
   `swarm/state.py:write_state` (persistence) and `pr_submit/fsm.py:should_halt_rounds` (counter)
   before TDD freezes them as "verified reuse."
3. **G-3:** The largest net-new surface (sandbox runtime OD-1 + systemd S2, Finding 6) has **zero**
   in-repo precedent. OD-1 is on the critical path for R4/S2/§15 and should be resolved in design,
   not deferred to TDD — it determines whether the §19.1 probe spike even has a host to run on.
4. **G-4:** ETag/304 polling, `in_reply_to_id` threading, and GraphQL `resolveReviewThread` (D3/D6/
   H4-impl) have no code precedent (Finding 3). The §19.1 probe-first gate must be **mandatory**, and
   its captured shapes (`in_reply_to_id`, `databaseId`, Augment bot login) should become committed
   config constants/fixtures so the parser is built against real bytes.
5. **G-5:** H1's Python `flock` push-serializer must fail-**closed**; the only in-repo flock
   precedent (freshness bash hooks) fails-**open** and is the wrong model to copy (Finding 9).
6. **Q-1:** Is the Anthropic proxy reachable from inside the §6 sandbox's deny-by-default network
   without also opening `github.com` broadly? The egress allowlist (`:4000/cli` + `api.github.com` +
   single-repo git) is asserted (INV-015) but the *proxy host* (`~/.aienv` `ANTHROPIC_BASE_URL`,
   `:4000/cli`) must be on the allowlist too — confirm the proxy is network-reachable from the
   sandbox topology chosen in OD-1.
7. **Q-2:** Does the operator intend `sc:pr-submit` to be *superseded* by V2.0, or to *coexist*?
   §20 ("Out of scope: V1.0's in-session Monitor-tool host — fully replaced") suggests V2.0 replaces
   a V1.0 in-session host — but `pr_submit/` is itself an in-session monitor FSM. Clarify whether
   `pr_submit/` is the "V1.0" being replaced or an independent surface to preserve.

## Stale Documentation Found

- **§9 / Reuse Map → `cli/swarm/commands.py:2269`** — **[CODE-CONTRADICTED]**. That line is a
  `--watch-max-iterations` loop guard for the status/logs watch loop, not a monotonic disk-backed
  round/budget counter. The described semantics live elsewhere (`swarm/state.py:write_state` for
  persistence; `pr_submit/fsm.py:should_halt_rounds` for the bounded counter). (Finding 8)
- **§12 "Net-new (absent from repo today)"** for reply-to-thread + resolve — **partially
  [CODE-CONTRADICTED]**. The *decision/state/event model* is NOT absent: `pr_submit/models.py`
  defines `MonitorState.S6_REPLYING`/`RESOLVING` and `EventType.REPLY_POSTED`/`THREAD_RESOLVED`. Only
  the *GraphQL `resolveReviewThread` implementation* is genuinely absent. The spec overstates the
  novelty. (Findings 3, 7)
- **Reuse Map omissions (under-, not over-, claiming):** `pr_submit/fsm.py`+`models.py` (decision
  core), `install_hooks.py:443`/`swarm/state.py:137` (atomic write), `sprint/recovery.py`+
  `sprint/resume/planner.py` (JSONL replay/RESUME), `cli_portify/logging_.py` (dual jsonl+md log),
  `eval/isolation.py` (scratch-root confinement) are all real reuse the spec does not list. The Reuse
  Map is honest about what it claims but **incomplete** — §19's effort estimate is therefore
  pessimistic on the decision core and the ledger, and optimistic only on sandbox/systemd. (Findings
  2, 5, 6, 7)
- **§7 `build_env()` "current full `os.environ.copy()`"** — **[CODE-VERIFIED]** accurate.
  `process.py:155` (`env = os.environ.copy()`) does copy the full environment; the spec's mandate to
  pass an explicit allowlist via the existing `env_vars` param (`__init__` accepts `env_vars`,
  `build_env(*, env_vars=...)` at `process.py:145`) is correct and the hook point already exists.

## Summary

Agent 4 deliberately **avoided** the 7-way-redundant reuse-primitive verification the other agents
converged on, and instead audited the spec's **net-new infrastructure** and searched for *uncited*
prior art. Net assessment of the merged-requirements spec:

- **The spec is architecturally sound and its "New" markings are honest** — `cli/remediate/` is
  genuinely greenfield (Finding 1), and the highest-novelty pieces (sandbox, systemd, ETag polling,
  GraphQL resolve) correctly carry the §19.1 probe-first gate (Findings 3, 6).
- **But the spec under-reuses.** The dominant finding (Finding 7) is that `sc:pr-submit` /
  `pr_submit/fsm.py` + `models.py` + `tests/pr_submit/` already implement and **test** the V2.0
  autonomy lattice, round/budget counter (`DEFAULT_MAX_ROUNDS=2`/`HARD_CAP=5`), poll floor
  (`MIN_POLL_INTERVAL=30`), push-decision conjunction, reply/resolve states, and ~80% of the §14
  event taxonomy. V2.0 is, at its decision core, a **headless/daemon re-host of `sc:pr-submit`** — and
  the spec never says so. This is the #1 thing the design phase must reconcile.
- **Two citations are wrong** (swarm `:2269`) and several strong reuse targets are missing from the
  Reuse Map (atomic-write, JSONL-replay, dual-log, scratch-root). Fixing these makes the build
  estimate *more* favorable for the decision core/ledger and isolates the true cost to the
  sandbox/systemd/GitHub-I/O surfaces.
- **Net-new I/O remains the real risk:** ETag/304 cursor (D3), `in_reply_to_id` resolution (D6),
  GraphQL `resolveReviewThread`+`databaseId` pagination (H4-impl), the container/microVM sandbox
  (OD-1/R4), and systemd deploy (S2) have **no in-repo precedent** and concentrate the build risk.
- **One real hardening the spec delivers:** H5 (the `--repo` injector) would be the **first
  code-level enforcement** of C5, which today is prose-only discipline that has previously failed
  (PR mis-targeted to upstream). That is a genuine, valuable net-new guarantee (Finding 4).

**Bottom line for the PRD:** accept the architecture; before TDD, (1) reconcile V2.0 against
`sc:pr-submit` and add `pr_submit/` to the Reuse Map, (2) fix the swarm `:2269` and §12 citations,
(3) resolve OD-1 (sandbox tech) since it gates the largest greenfield surface, and (4) keep §19.1
probe-first as a hard prerequisite for the GitHub-I/O components.
