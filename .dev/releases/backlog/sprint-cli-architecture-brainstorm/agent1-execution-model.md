# Sprint Run CLI — Execution Model Deep Brainstorm

**Agent 1: Per-task process / agent-swarm vs single per-phase session**
Scope base: `src/superclaude/cli/sprint/`. Date: 2026-06-02.
Evidence standard: STEP 0 claims carry `file:line`. Proposals flag inference as INFERENTIAL.

---

## STEP 0 — VERDICT (grounded): the runner has TWO execution paths, selected at runtime

**The briefing's "one session per phase" is half-right and half-wrong. The truth is a runtime fork.** For each active phase, `execute_sprint` calls `_parse_phase_tasks(phase, config)` and *branches*:

```
executor.py:1261   tasks = _parse_phase_tasks(phase, config)
executor.py:1262   if tasks:
executor.py:1267       task_results, remaining, ... = execute_phase_tasks(...)   # PER-TASK PATH
            ...
executor.py:1303   # else: fall through to single ClaudeProcess              # PER-PHASE PATH
executor.py:1324       proc_manager = ClaudeProcess(config, phase, env_vars=_phase_env_vars)
```

### Path A — Per-PHASE single session (the `build_prompt` path)

- Taken when `_parse_phase_tasks` returns `None` — i.e. the phase file contains **no** `### T<PP>.<TT> -- Title` headings.
- `_parse_phase_tasks` (executor.py:1118-1132) delegates to `parse_tasklist`, which keys off `_TASK_HEADING_RE = ^###\s+(T\d{2}\.\d{2})\s*(?:--|-—|—)\s*(.+)` (config.py:374-377). If zero headings match, it returns `[]` → `None` → Path A.
- One `ClaudeProcess(config, phase)` is spawned (executor.py:1324). Its `build_prompt()` emits exactly one prompt: `/sc:task Execute all tasks in @{phase_file} --compliance strict --strategy systematic` (process.py:169-216). **One `claude --print` process executes ALL tasks of the phase inline**, driven by the `/sc:task` skill inside that single session.
- The base command is `claude --print --verbose <perm> --no-session-persistence --tools default --max-turns N --output-format stream-json [--model M]` (pipeline/process.py:79-95). Prompt is piped via **stdin**, not argv, to dodge the 128 KB `MAX_ARG_STRLEN` ceiling (pipeline/process.py:76-78, 140-146).

### Path B — Per-TASK subprocess loop (the `execute_phase_tasks` path)

- Taken when the phase file **does** contain `### T<PP>.<TT>` task headings.
- `execute_phase_tasks` (executor.py:927-1073) `for i, task in enumerate(tasks)` and spawns **one subprocess per task** via `_run_task_subprocess` (executor.py:1008, 1076-1115).
- Each per-task process is a `ClaudeProcess` built ad-hoc with a *thin* prompt: `f"Execute task {task.task_id}: {task.title}\nFrom phase file: {phase.file}\nDescription: {task.description}\n"` (executor.py:1087-1091) — note this is NOT `build_prompt()`; it bypasses the rich Sprint-Context/Execution-Rules/Checkpoints scaffolding entirely.
- Each per-task process writes its own transcript: `phase-{N}-task-{task_id}-output.txt` (models.py:502-503, wired at executor.py:1101). **This is the origin of the per-task `result`-bearing transcripts the briefing observed** — each is a separate `claude` invocation, so each emits its own terminal `result` event.

### Reconciling the briefing's paradox (per-phase prompt vs per-task `result` events vs ~1 sub-agent)

The briefing observed: per-task transcripts with their own `result` events, but tasks executing **inline** (~1 `Task` sub-agent call across ~22 tasks). These two observations point at **different runs / different phase-file formats**, not a contradiction within one run:

- **The "~22 tasks, ~1 sub-agent, inline" observation = Path A.** The `/sc:task` skill ran all tasks inside one session; `/sc:task` executes work inline and only occasionally spawns a `Task` sub-agent. One process → one `result` event for the whole phase. (INFERENTIAL on which specific run, but the mechanism is certain from process.py:169-216.)
- **The per-task `result`-bearing transcripts = Path B.** Only `_run_task_subprocess` produces `phase-N-task-TNN.MM-output.txt`, and it spawns a distinct `claude` per task → distinct `result` events. (Grounded: models.py:502, executor.py:1101.)

**Which path a phase takes is decided purely by whether `tasklist` headings match the `### TNN.MM -- Title` regex.** A heading-format drift (e.g. `### T01.01:` with a colon, or `#### `) silently demotes a phase from Path B to Path A. This is a latent, invisible mode-switch — a real architectural hazard independent of the swarm question.

### What `build_prompt` is parameterized by

Per **phase**, not per task (process.py:123-216). It reads `self.phase.number`, `self.phase.file`, prior-phase artifact/dirs derived from `pn`. There is **no per-task parameterization** of `build_prompt`; the per-task path deliberately does not use it.

### What `execute_phase_tasks` loops over and spawns

It loops over `tasks: list[TaskEntry]` (executor.py:971) and, per iteration: budget-guards via `TurnLedger.can_launch()` (executor.py:975), pre-debits `minimum_allocation` (executor.py:991), spawns via `_subprocess_factory` (tests) or `_run_task_subprocess` (real, executor.py:1008), classifies status from exit code (0→PASS, 124→INCOMPLETE, else→FAIL; executor.py:1015-1020), reconciles the ledger (executor.py:1022-1030), then runs the post-task **wiring** hook (executor.py:1043) and post-task **anti-instinct** hook (executor.py:1053). **It does NOT spawn tasks in parallel** — it is a strict sequential `for` loop, one `proc.start(); proc.wait()` at a time (executor.py:1109-1110).

### What the "4-layer isolation" actually isolates — AND that it is DEAD CODE

`IsolationLayers` (executor.py:106-147) defines four env overrides: `CLAUDE_WORK_DIR` (scoped work dir), `GIT_CEILING_DIRECTORIES` (git boundary), `CLAUDE_PLUGIN_DIR` (empty plugin dir), `CLAUDE_SETTINGS_DIR` (isolated settings dir). `setup_isolation()` (executor.py:150-182) constructs them under `results_dir/.isolation`.

**Critical finding: `setup_isolation()` has ZERO callers.** A repo-wide grep finds only the function's own `return IsolationLayers(...)` (executor.py:177) and the class definition — no call site anywhere in the live execution path. **The 4-layer isolation is fully implemented but never invoked.**

What the live paths actually inject:

- **Path A** injects only one var: `_phase_env_vars = {"CLAUDE_WORK_DIR": str(isolation_dir)}` (executor.py:1321-1324), where `isolation_dir = results_dir/.isolation/phase-{N}` holds a *copy* of just the phase file (executor.py:1304-1306). It does **not** use `IsolationLayers.env_vars`. So `CLAUDE_PLUGIN_DIR` and `CLAUDE_SETTINGS_DIR` are **never** set in Path A.
- **Path B** (`_run_task_subprocess`) passes **no `env_vars` at all** — the `_Base.__init__` call (executor.py:1098-1108) omits `env_vars`, so per-task children inherit the parent environment unmodified, including the shared `~/.claude` settings/config.

The base `build_env` only strips `CLAUDECODE` / `CLAUDE_CODE_ENTRYPOINT` to prevent nested-session detection (pipeline/process.py:107-112). **It does nothing to isolate the shared Claude config file.**

### Does config isolation for concurrent spawns already exist?

**No — not in any live path.** The machinery to do it (`CLAUDE_SETTINGS_DIR` via `IsolationLayers`) exists but is unwired (dead code). The briefing's observed failure — corrupted shared config under near-simultaneous `claude` starts — is therefore **completely unmitigated today**, and would be *immediately* relevant to any parallel swarm because:

1. Path B passes no settings isolation.
2. Even Path A's single var doesn't touch `CLAUDE_SETTINGS_DIR`.
3. `build_task_context()` / `compress_context_summary()` (process.py:257-385) — the per-task handoff/context-injection helpers — are **also dead code**: grep finds callers only in a docstring (process.py:8). The infrastructure for handoff between per-task processes exists but is not wired into `_run_task_subprocess`.

### STEP 0 bottom line (high confidence)

| Question | Verdict | Evidence |
|---|---|---|
| One session/phase or one/task? | **Both exist; runtime fork on heading regex** | executor.py:1261-1324; config.py:374-377 |
| `build_prompt` granularity | **Per-phase only** | process.py:123-216 |
| Per-task path real today? | **Yes, but with a thin prompt, no turn counting, no isolation, no context handoff** | executor.py:1076-1115 |
| 4-layer isolation active? | **No — `setup_isolation` has zero callers (dead code)** | grep; executor.py:150-182 |
| Config isolation for concurrency? | **None in any live path** | pipeline/process.py:107-112; executor.py:1098-1108 |
| Context/handoff helpers active? | **No — `build_task_context` dead code** | grep; process.py:257-385 |
| Tasks parallel today? | **No — strict sequential loop** | executor.py:971, 1109-1110 |

**Implication for this brainstorm:** the per-task spawn model is not a greenfield idea — a *sequential, non-isolated, context-blind* version already ships (Path B). The real design space is (1) making per-task spawning the deliberate, isolated, context-aware default, and (2) deciding whether/how to parallelize it. The dead `IsolationLayers` + `build_task_context` are pre-built scaffolding we can wire up rather than write from scratch.

---

## Why per-task spawning is attractive (benefits, grounded where possible)

- **Context freshness.** Path A loads one session for an entire multi-hour phase; later tasks operate with a context window saturated by earlier tasks' output — the direct cause of the `"Prompt is too long"` failure that `monitor.py` greps for (`PROMPT_TOO_LONG_PATTERN = re.compile(r'"Prompt is too long"')`, monitor.py:34; consumed at executor.py:2093). A fresh process per task resets the window every task. **This is the single strongest argument** and it is evidence-backed: the prompt-too-long detector exists *because* this failure is observed.
- **Fault containment.** Path A: a crash mid-phase loses the whole phase (and journaling is unreliable, so recovery is guesswork). Per-task: a crash loses one task; `execute_phase_tasks` already classifies per-task status and continues (executor.py:1015-1063).
- **API-bound → parallel wall-clock win.** Briefing's profile: ~94% token-gen, ~3% tooling, ~3% runner overhead (~23 s/spawn). Sequential tasks serialize all the token-gen. Independent tasks run concurrently → near-linear wall-clock reduction bounded by the dependency DAG width and the API concurrency ceiling. (INFERENTIAL on speedup magnitude; the API-bound premise is the briefing's measurement.)
- **Clean per-task attribution / journaling.** The unreliable `task_complete` journaling (briefing) is a *consequence* of Path A: one session self-reports N tasks and frequently under-reports. Per-task processes give the **runner** authoritative per-task exit codes — exactly what `aggregate_task_results` (executor.py:296-335) is designed to consume. This directly fixes the journaling-reliability problem at the source.
- **Prompt-length relief.** Smaller per-task prompts; `build_task_context` compression (process.py:347-385) bounds carried context if wired in.

## Costs / risks (grounded)

- **Spawn overhead.** ~23 s/spawn × N tasks. A 22-task phase pays ~8.4 min of pure spawn latency sequentially; parallelism hides it but multiplies concurrent config access.
- **Shared-config corruption under concurrency.** The headline risk. Today there is **no** `CLAUDE_SETTINGS_DIR` isolation in any live path (STEP 0). A parallel swarm starting K `claude` processes against one `~/.claude/config.json` is the exact concurrent-writer contention the briefing observed. **Any parallel proposal MUST wire per-process settings isolation first** — and the code to do it already exists (`IsolationLayers`, executor.py:106-147).
- **Handoff fidelity / information loss.** Per-task processes don't share a context window; cross-task knowledge must be serialized into a handoff artifact. `build_task_context` exists but is unwired and lossy by design (compresses older tasks to one line, process.py:371-376). *(A separate agent is researching handoff mechanisms; treated here at the interface level only — see "Handoff coupling point" per proposal.)*
- **Inter-task dependency ordering.** `TaskEntry.dependencies` is already parsed (config.py:379-441; `_DEPENDENCY_RE`, `_TASK_ID_REF_RE`) but `execute_phase_tasks` **ignores it** — it iterates in file order. Parallelism needs this DAG honored.
- **max-turns / timeout sizing.** Today every per-task process gets the full phase budget: `max_turns` and `timeout = max_turns*120+300` (executor.py:1103-1106). A small task with a phase-sized budget wastes budget headroom and inflates timeouts. The `TurnLedger` machinery (executor.py:1199-1203, 989-1030) already exists to right-size this.
- **Debuggability.** N transcripts vs 1. Mitigated by deterministic naming (models.py:502-506) and runner-side aggregation (executor.py:296-335), but stall detection (`OutputMonitor`, monitor.py) is currently wired only into Path A's poll loop (executor.py:1340-1457); per-task processes get **no stall watchdog** today.

---

## Three concrete, distinct proposals

### Proposal A — Per-task SEQUENTIAL spawn (harden & promote Path B)

**Architecture.** Keep `execute_phase_tasks`'s sequential `for` loop. Make it the *deliberate default* for any phase with a task inventory, and fix its three gaps: thin prompt, no isolation, no turn counting / context handoff. No concurrency.

```
for task in topological_order(tasks):              # honor dependencies (DAG → linear order)
    env  = setup_isolation(config).env_vars        # WIRE the dead 4-layer isolation
    ctx  = build_task_context(prior_results, ...)   # WIRE the dead context helper
    proc = ClaudeProcess.for_task(config, phase, task, context=ctx, env_vars=env)
    proc.start(); poll-with-stall-watchdog(proc)    # reuse Path A's watchdog
    record TaskResult; write handoff(task)
```

**Maps onto current code.**
- Modify `_run_task_subprocess` (executor.py:1076-1115): pass `env_vars=setup_isolation(config).env_vars`; replace the thin prompt (1087-1091) with a task-scoped prompt that reuses `build_prompt`'s scaffolding narrowed to one task; capture real `turns_consumed` instead of the hardcoded `0` (executor.py:1114-1115).
- Wire `build_task_context` (process.py:257-319) into the loop, fed by `results` accumulated in `execute_phase_tasks` (executor.py:964).
- Lift the stall-watchdog block (executor.py:1366-1444) into a shared helper callable from both the phase poll loop and per-task waits.
- `_parse_phase_tasks` heading-regex fragility (STEP 0): add a fallback so a near-miss heading still routes to Path B (or warns loudly) — otherwise A silently degrades to per-phase.

**Config-isolation strategy.** Trivial — sequential means one `claude` at a time, so even a single shared `CLAUDE_SETTINGS_DIR` per task eliminates concurrent-writer corruption by construction. Wiring `setup_isolation` is sufficient and zero-risk here.

**Handoff approach (interface level).** After each task, write a handoff doc keyed `phase-N-task-TNN.MM-handoff.md`; next task's prompt ingests prior handoffs via `build_task_context`. **Coupling point:** the handoff *format/selection* is owned by the handoff-research agent; this proposal only commits to "runner writes one handoff artifact per task, injects predecessors' handoffs into successor prompts."

**Migration path.** Lowest-risk: (1) wire isolation + turn counting into `_run_task_subprocess` (internal, no surface change); (2) wire context/handoff; (3) add the heading-fallback router. All behind existing branch at executor.py:1262 — no new flags required. Reversible by reverting the wiring.

---

### Proposal B — Bounded PARALLEL pool over the task DAG

**Architecture.** Replace the sequential loop with a bounded worker pool (`--task-parallelism K`, default e.g. 3) that executes the `TaskEntry` dependency DAG: tasks whose dependencies are all `PASS` become runnable; a semaphore caps concurrent `claude` processes at K.

```
ready = tasks with no unmet deps
while ready or in_flight:
    while len(in_flight) < K and ready:
        t = ready.pop(); env = isolated_settings_dir(t)   # UNIQUE dir per worker
        spawn(t, env); in_flight.add(t)
    done = wait_any(in_flight)
    record TaskResult(done); unlock dependents; reschedule
```

**Maps onto current code.**
- Rewrite the body of `execute_phase_tasks` (executor.py:971-1073) from a `for` loop into a scheduler. Reuse `TaskEntry.dependencies` (already parsed, config.py:436-441) — currently ignored.
- `TurnLedger` (executor.py:1199-1203): its `can_launch` / debit / credit logic (executor.py:975-1030) must become thread-safe (add a lock) since K workers debit concurrently.
- Post-task hooks (`run_post_task_wiring_hook` executor.py:458; `run_post_task_anti_instinct_hook` executor.py:803) run per worker on completion — already per-task, so they slot in unchanged except for thread-safety of shared `shadow_metrics` / `remediation_log`.
- `_write_preliminary_result`'s docstring already flags the TOCTOU hazard under parallelism (executor.py:1969-1973) — must switch to `O_EXCL` atomic writes as it warns.
- Per-worker stall watchdog: needs the shared watchdog helper from Proposal A, one timer per in-flight process.

**Config-isolation strategy (mandatory, load-bearing).** Each worker gets a **unique** `CLAUDE_SETTINGS_DIR` (and `CLAUDE_PLUGIN_DIR`) — i.e. parameterize `setup_isolation` per worker slot (`results_dir/.isolation/worker-{k}/settings`) rather than the current single dir (executor.py:168-181). This is the *direct fix* for the observed corruption and is the precondition for any concurrency. Without it, B reproduces the corruption at scale.

**Handoff approach (interface level).** Harder than A: concurrent siblings can't see each other's handoffs. Only **dependency-edge** handoffs are guaranteed available (a task starts after its deps finish, so it can ingest their handoffs). Sibling discoveries are lost until a join. **Coupling point:** the handoff agent must define edge-scoped handoff semantics (predecessor→successor only), not global running context. Flag: parallelism *reduces* achievable handoff fidelity vs A.

**Migration path.** (1) Land Proposal A's wiring first (isolation + per-task prompt + turn counting) as the substrate. (2) Add per-worker settings dirs. (3) Introduce the DAG scheduler behind `--task-parallelism K` with **default K=1** (== Proposal A behavior, fully reversible). (4) Make `TurnLedger` + shared metrics thread-safe. (5) Raise default K only after the corruption fix is validated under load.

---

### Proposal C — Hybrid phase-coordinator + task-workers

**Architecture.** A long-lived **coordinator** `claude` session per phase owns planning, dependency reasoning, handoff synthesis, and the checkpoint/result-file contract. It dispatches **ephemeral task-worker** processes (sequential or bounded-parallel) for the actual code+evidence generation, then ingests their handoffs to maintain a coherent phase narrative and write the authoritative result/checkpoint files.

```
coordinator = ClaudeProcess(build_prompt(phase))    # Path A's rich prompt, but as planner not executor
  └─ emits a task plan + dispatch order
runner spawns task-workers per coordinator plan (A- or B-style)
  └─ each worker: fresh context, isolated settings, writes handoff
coordinator ingests handoffs → writes checkpoints + EXIT_RECOMMENDATION result file
```

**Maps onto current code.**
- `build_prompt` (process.py:123-216) is **repurposed**: today it tells the session to *execute* all tasks; in C it tells the coordinator to *plan and supervise*. The Checkpoints/Result-File/Scope-Boundary sections (process.py:187-216) stay with the coordinator — which is actually the natural owner of `config.result_file(phase)` and the `EXIT_RECOMMENDATION` contract that `_determine_phase_status` reads (executor.py:2113-2138).
- Task-workers reuse Proposal A/B `_run_task_subprocess` machinery.
- The runner becomes a thinner orchestrator: it brokers coordinator↔worker, but the *intelligent* sequencing moves into the coordinator session. This reduces the heading-regex fragility (STEP 0) because the coordinator, not a regex, decides task decomposition.
- `aggregate_task_results` (executor.py:296-335) still produces the runner-authoritative report as a cross-check against the coordinator's self-report — defense in depth against the unreliable-journaling problem.

**Config-isolation strategy.** Workers need isolation exactly as in B (unique settings dirs if parallel; single isolated dir if sequential). The coordinator is one stable session — low corruption risk. So C's corruption exposure equals its chosen worker concurrency (inherits A's safety if workers are sequential, B's requirements if parallel).

**Handoff approach (interface level).** Strongest fidelity: the coordinator is a *living aggregation point* that reads every worker handoff and reconciles them into phase-level state — recovering the sibling-knowledge that B loses. **Coupling point:** worker→coordinator handoff contract is the critical interface; the handoff agent should design for a *consumer that synthesizes*, not just a successor that reads. Highest coupling of the three.

**Migration path.** Most invasive. (1) Land A (substrate). (2) Split `build_prompt` into `build_coordinator_prompt` / `build_worker_prompt`. (3) Introduce a coordinator-dispatch protocol (how the coordinator signals "spawn task T"; likely a structured file the runner polls, reusing the existing poll-loop pattern at executor.py:1340-1457). (4) Gate behind `--coordinator` flag; default off (== Path A/A'). Reversible but the coordinator-dispatch protocol is net-new surface.

---

## Adversarial comparison

| Dimension | A: Sequential per-task | B: Bounded parallel DAG | C: Coordinator + workers |
|---|---|---|---|
| Wall-clock | No speedup (serial); fixes context-freshness only | **Best** — concurrency to DAG width × K | Good if workers parallel; coordinator adds one extra session of latency |
| Fault containment | Good (per-task) | Good per-task; scheduler is a new failure point | Good; coordinator crash loses orchestration but workers' handoffs survive |
| Complexity | **Lowest** — mostly wiring dead code | High — scheduler + thread-safe ledger + atomic writes | **Highest** — new dispatch protocol + prompt split |
| Config-corruption risk | **Lowest** — one process at a time; isolation trivial | Highest IF unmitigated; **acceptable only with per-worker `CLAUDE_SETTINGS_DIR`** | = worker concurrency (A-safe or B-risky); coordinator itself low-risk |
| Dependency handling | Linearized DAG (correct, not parallel) | **Native DAG** (uses existing `dependencies` field) | Coordinator-reasoned (most flexible, least deterministic) |
| Handoff fidelity | **Highest deterministic** (full prior context, serial) | Lower — edge-scoped only, sibling loss | **Highest semantic** (coordinator synthesizes) — but most coupled |
| Migration cost | **Lowest** — internal wiring, no new flags | Medium-high — new scheduler behind flag | Highest — new protocol + prompt refactor |

---

## Ranked recommendation

**1st — Proposal A, immediately and unconditionally.** It is not really a "proposal" so much as *finishing the half-built feature that already ships*: the per-task path exists (executor.py:1076-1115) but is thin-prompted, turn-blind, isolation-less, and context-blind, while `setup_isolation` (executor.py:150-182) and `build_task_context` (process.py:257-319) sit **dead** waiting to be wired in. A captures the highest-confidence wins — context-freshness (fixes `"Prompt is too long"`), per-task attribution (fixes unreliable `task_complete` journaling), fault containment — at the **lowest** risk and **zero** config-corruption exposure (sequential). It also fixes the latent STEP 0 hazard (silent Path B→A demotion on heading drift). Do this first regardless of whether B or C ever lands; it is the substrate for both.

**2nd — Proposal B, as an opt-in built on A.** The biggest measured lever is parallelizing API-bound tasks, and the `TaskEntry.dependencies` DAG is *already parsed and currently ignored* — so B is the natural payoff. But it is **gated on the config-corruption fix**: per-worker `CLAUDE_SETTINGS_DIR` isolation (parameterizing `setup_isolation`) is a hard precondition, plus thread-safe `TurnLedger` and `O_EXCL` writes (the code already warns about the TOCTOU at executor.py:1969-1973). Ship with default `K=1` (== A) and raise only after load-testing the isolation fix.

**3rd — Proposal C, longer horizon.** C has the best handoff *semantics* and removes the regex-routing fragility by moving decomposition into a coordinator, but it is the most invasive (new dispatch protocol, `build_prompt` split) and most tightly coupled to the in-flight handoff-mechanism research. Defer until A is proven and the handoff contract is settled; C is where you go if edge-scoped handoff (B's weakness) proves insufficient in practice.

**Cross-cutting, do-before-anything:** wire `setup_isolation` into the live paths and fix the per-task path's hardcoded `turns_consumed=0` (executor.py:1114-1115) — these are pure bug-fixes that every proposal depends on, and the absence of settings isolation is the root cause of the observed corruption today, *already*, even before adding concurrency.
