# Sprint Run CLI — Coupled Architecture Synthesis

**Decisions synthesized:** (1) execution model — per-phase session vs per-task swarm; (2) handoff mechanism — agent-mail vs `.md` vs inlined prompt. The two are coupled and are answered together.

**Inputs:** `agent1-execution-model.md`, `agent2-handoff-mechanism.md` (both source-grounded). Two load-bearing claims independently re-verified by the orchestrator (greps below).

> **⚠ Pre-execution reflection amendment (2026-06-03).** A `/sc:reflect --mode pre --depth deep` audit (3-reviewer Tier 2, multi-vendor) re-verified the core thesis (7/9 code claims exact) but found **6 HIGH issues that block tasklist authoring**. **§6 resolves them and is authoritative — it supersedes the conflicting stage-table cells in §3 where they differ.** Inline corrections below are marked. Full report: `.dev/reflect/pre-sprint-cli-arch-20260603002500/REPORT.md`.

---

## 1. The briefing was wrong twice — and both errors point the same way

| Briefing claimed | Source truth | Evidence |
|---|---|---|
| "ONE Claude session executes ALL tasks in a phase" | **Runtime fork.** Path A (per-phase single session) when the phase file has no `### TNN.MM -- Title` headings; Path B (one subprocess **per task**) when it does. Selected purely by heading-regex match. | `executor.py:1261-1324` (`_parse_phase_tasks` → branch → `execute_phase_tasks` vs single `ClaudeProcess`); `config.py:374-377` (`_TASK_HEADING_RE`) |
| "`task_complete` journaling is UNRELIABLE (a few of N journaled)" | **There is no `task_complete` writer for the *main* execution path.** [CORRECTED] A per-task `task_rerun_complete` event *does* exist via `write_task_rerun_complete` (`logging_.py:205-211`) for the *rerun* path — the new writer must reconcile name/schema with it (see §6 · H3). | `logging_.py` grep: zero `task_complete`; `execute_phase_tasks` builds a `TaskResult` per task (`executor.py:1032-1040`) but never journals it |

Two more findings reframe the whole design space:

- **The "4-layer subprocess isolation" is dead code.** `setup_isolation` (executor.py:150) and the `IsolationLayers` it returns have **zero callers** (verified: only the `def` matches). The live paths inject at most `{"CLAUDE_WORK_DIR": …}` (Path A) or **no env at all** (Path B). **`CLAUDE_SETTINGS_DIR` is never set in any *live* path** [CORRECTED] (it is assigned only inside the dead `IsolationLayers`, `executor.py:133`).
- **`build_task_context` / `compress_context_summary` (the handoff/context helpers) are also dead** — zero callers (verified: only the `def` + a docstring reference).

**Consequence:** the observed shared-config corruption is **completely unmitigated today**, and a per-task execution path *already ships* but is sequential, isolation-less, turn-blind (`turns_consumed` hardcoded `0`, executor.py:1114-1115), and context-blind. The scaffolding to fix all of this (isolation + context-handoff helpers) is **already written and sitting dead.** This is a wiring job, not a greenfield build.

---

## 2. Coupled recommendation

> **Execution model:** Adopt the per-task spawn model in three deliberate stages — **A (harden & promote the existing Path B) → B (bounded-parallel DAG, opt-in) → C (coordinator+workers, deferred).** Do *not* jump to a parallel swarm first.
>
> **Handoff mechanism:** **Runner-owned, one-file-per-task, atomically-written typed handoff record** (`release_dir/handoff/<task_id>.json`) behind a thin `HandoffStore` interface — i.e. Agent 2's **Middle** roadmap. **agent-mail is deferred** to an optional, shadow-mode, reversible pilot that is only justified once parallel concurrency (≥~3) actually ships.
>
> **The two decisions converge on one artifact:** the handoff record *is* the missing `task_complete` ledger *is* the within-phase resume substrate *is* the per-task DAG fan-in channel. Build it once; it discharges four debts.

### Why this pairing (and not the alternatives)

- **Per-task sequential first, not parallel first.** The single biggest *risk* (config corruption) is a hard gate on any concurrency, and it is currently 100% unmitigated. Promoting Path B sequentially (Proposal A) captures the high-confidence wins — fixes `"Prompt is too long"` via context-freshness, gives runner-authoritative per-task attribution, contains faults — at **zero added corruption exposure** (one process at a time). It also fixes the silent **B→A demotion hazard** (a heading-format typo downgrades a phase to the monolithic path unnoticed).
- **Parallel is the biggest wall-clock lever but is gated.** The pipeline is ~94% token-gen and serial, so parallelizing independent tasks is *the* speedup. But it is only safe after per-worker `CLAUDE_SETTINGS_DIR`/`CLAUDE_PLUGIN_DIR` isolation (wire the dead `setup_isolation`, parameterized per slot), a thread-safe `TurnLedger`, and `O_EXCL` preliminary-result writes. Ship it behind `--task-parallelism K` defaulting to **K=1 (≡ Proposal A)**.
- **File-backed typed handoff, not agent-mail, not inlined.** Inlined-prompt handoff *worsens* the audit gap (prompt strings aren't auditable) and grows context cost; it's viable only under a coordinator (Proposal C) and even then must be backed by the durable record. agent-mail is real and active (~832 commits, dual SQLite+git store, MCP surface verified) but requires a **Python 3.14 long-lived HTTP daemon on :8765** whose lifecycle the CLI would own, it **fights the very isolation we need to wire**, and it **re-introduces a single shared store + one global `.commit.lock`** — the same *shape* as the corruption bug already suffered, with locking correctness UNVERIFIED. A per-task file (atomic temp + `os.replace`, reusing the `checkpoints.py:204-206` idiom) is **immune-by-construction** to that class (distinct paths, no shared mutable writer).
- **The one anti-pattern to forbid:** a single shared `handoff.md` (or the existing `_jsonl()` bare-append at `logging_.py:210-212`) written by N parallel workers. That *is* the corruption bug. One-file-per-task sidesteps it; the parallel stage must also make `_jsonl()` concurrency-safe.

---

## 3. Sequenced roadmap (coupled)

| Stage | Execution (Agent 1) | Handoff (Agent 2) | Gate to advance |
|---|---|---|---|
| **0 — Decoupled quick win (do now)** | Fix `turns_consumed=0` (executor.py:1114-1115); wire `setup_isolation` into both live paths (sets `CLAUDE_SETTINGS_DIR` → fixes corruption *today*, before any concurrency) | Add `SprintLogger.write_task_complete` + call it in `execute_phase_tasks` after each `TaskResult` (executor.py:~1040) | Per-task ledger events appear; corruption reproduction no longer occurs in serial reruns |
| **1 — Harden per-task serial** | **Proposal A:** replace thin per-task prompt (executor.py:1087-1091) with task-scoped scaffolding; wire `build_task_context`; lift the Path-A stall watchdog (executor.py:1366-1444) into per-task; heading-regex fallback to kill B→A demotion | **Middle M1:** typed `HandoffRecord` + `HandoffStore` interface + `FileHandoffStore` (atomic temp+replace under `release_dir/handoff/<id>.json`) | 100% tasks journaled on a real 3-phase sprint; schema + interface frozen |
| **2 — Within-phase resume** | `--start`/`--end` gain task-granular resume; loop skips tasks with an existing handoff record | **Middle M2 (resume half):** `build_prompt`/loop consult `HandoffStore`, inject skip-list + declared-upstream fan-in | Mid-phase kill+resume completes without re-running done tasks |
| **3 — Bounded parallel (opt-in)** | **Proposal B:** `--task-parallelism K` semaphore pool over the already-parsed-but-ignored `TaskEntry.dependencies` DAG (config.py:436-441); per-worker `CLAUDE_SETTINGS_DIR`; thread-safe `TurnLedger`; `O_EXCL` writes; per-worker stall timers; make `_jsonl()` concurrency-safe | **Middle M2 (concurrency half):** race test — N concurrent writers to distinct task IDs, assert zero corruption over 100 runs | ≥4 concurrent writers, zero corruption; measured wall-clock win on a DAG-wide phase |
| **4 — Optional agent-mail pilot** | (only if Stage 3 concurrency ≥~3 in routine use) | **Middle M3:** `MailHandoffStore` behind the same interface, **shadow/dual-write with file as source of truth**; FastMCP sidecar in the controlled settings dir | Byte-semantic parity vs file oracle on ≥3 sprints + acceptable operational toil → else **flip one line back to `FileHandoffStore`**, kill sidecar (free rollback) |
| **C — Coordinator+workers** | **Proposal C**, deferred: long-lived coordinator owns planning/handoff-synthesis/checkpoint contract, dispatches ephemeral workers; removes heading-regex routing entirely | Coordinator synthesizes worker handoffs (recovers sibling knowledge the edge-only DAG loses) | Only after A proven and handoff contract settled |

**Test strategy per stage** (from Agent 2): round-trip fidelity (write→read no loss); lost-record→typed `None` fallback; **concurrency/race** (Stage 3, directly exercises the corruption class); failure-injection (crashed producer / partial write / missing handoff); end-to-end multi-agent integration. Every stage has a flag-based escape hatch (`--handoff=off`, `--task-parallelism=1`, `FileHandoffStore` swap).

---

## 4. The single most important next action

**Stage 0 is decoupled from every architectural choice and discharges the two worst debts immediately:**

1. Wire the dead `setup_isolation` into the live paths → sets `CLAUDE_SETTINGS_DIR` → **fixes the shared-config corruption that is currently 100% unmitigated**, before a single new concurrent process is added.
2. Add `SprintLogger.write_task_complete` → **closes the structural audit gap** (there is no per-task ledger event today) at the cost of one method + one call site.

Neither requires committing to per-task-vs-coordinator or file-vs-mail. Both are high-value and low-risk — **but Stage 0 is _not_ behavior-neutral wiring** [CORRECTED]: wiring `setup_isolation` changes Path A's existing `CLAUDE_WORK_DIR` and the subprocess settings/MCP/hook surface, and the original gate did not exercise the *concurrent* failure it targets. Do Stage 0 first in its own PR **using the per-path merge semantics and corrected gate in §6 (H1, H2)**.

---

## 5. Open items / UNVERIFIED (carry forward)

- agent-mail `.commit.lock`/`.archive.lock` correctness under N agents is README-asserted, not code-audited — the Stage-4 shadow race test exists precisely to verify it before any trust.
- Whether the swarm needs file-reservation arbitration at all is INFERENTIAL — the DAG dependency declarations may already prevent overlapping writes, making agent-mail's headline feature moot for this workload.
- `TaskEntry.dependencies` is parsed (config.py:436-441) and ignored by the *execution* loop, **but it is NOT virgin** [CORRECTED]: `rerun_tasks.py:438-449` (`walk_dependencies` / `_dependencies_of`, cross-phase + transitive) already consumes it — so Stage 3 is **not** the first consumer. The scheduler must reuse that primitive, not re-derive one (see §6 · H6).

---

## 6. Pre-execution reflection amendments — 6 HIGH findings resolved (AUTHORITATIVE)

Source: `/sc:reflect --mode pre --depth deep` (Tier 2; reviewers gpt-5.5 / qwen3.6 / claude-opus-4-8). These resolutions **supersede the §3 stage-table cells where they conflict**. A tasklist author should treat §6 as the execution contract.

> **Anchor on symbols, not lines.** Every `file:line` in this spec has already drifted in the target worktree (+4 to +55 lines). Tasks must locate code by symbol name (`setup_isolation`, `_run_task_subprocess`, `_jsonl`, `execute_phase_tasks`, `_parse_phase_tasks`), not literal line numbers.

### H1 — Stage 0 isolation wiring is a behavior change; per-path merge semantics required

Wiring `setup_isolation` is **not** uniform across the two live paths:

| Path | Env today | Stage-0 change (REQUIRED semantics) |
|---|---|---|
| **A** (per-phase) | `{"CLAUDE_WORK_DIR": <release_dir>/.isolation/phase-{N}}` (phase-scoped copy dir) | **KEEP** the phase-scoped `CLAUDE_WORK_DIR`; **ADD only** `CLAUDE_SETTINGS_DIR` + `CLAUDE_PLUGIN_DIR` from `setup_isolation`. Do **NOT** let `setup_isolation`'s own `CLAUDE_WORK_DIR` (the whole release dir, `IsolationLayers.env_vars` @ `executor.py:127-133`) overwrite the phase scoping. |
| **B** (per-task) | none (inherits parent env) | Inject the full `setup_isolation(config).env_vars`. |

→ `setup_isolation` likely needs **per-phase/per-task parameterization** so Path A's work-dir scoping is preserved. The "decoupled, own PR, pure win" framing holds only once these merge semantics are explicit.

### H2 — Corrected Stage-0 gate (the original tests the wrong thing)

Replace gate "corruption reproduction no longer occurs in serial reruns" (serial cannot exercise a concurrent-writer race) with **two** gates:

1. **Serial isolation smoke** — after wiring, the isolated subprocess still invokes `/sc:task`, project hooks, allowed tools, and configured MCPs (settings-seed/merge policy verified); functionality intact.
2. **Concurrent-spawn corruption repro** — a controlled harness starts ≥4 near-simultaneous `claude` processes and proves per-process isolated `CLAUDE_SETTINGS_DIR` prevents the known shared-config corruption class.

### H3 — Reconcile the new `task_complete` writer with the existing `task_rerun_complete`

`write_task_rerun_complete` already emits `event: "task_rerun_complete"` (`logging_.py:205-211`; docstring cites "TDD line 94/95") with `phase / task_id / status / turns / duration_sec`. The new main-path writer MUST decide one of:

- **(preferred)** emit `event: "task_complete"` for first-run and keep `task_rerun_complete` for reruns, with a documented discriminator; OR
- unify both under one event with a `run_kind: first | rerun` field.

Freeze **both** schemas side-by-side; do not silently fork the ledger.

### H4 — Freeze the `HandoffRecord` schema (the Stage-1 gate already assumes it is frozen)

Derive from `TaskResult.to_dict()` (`models.py:194`) + exactly two delta fields + a version. Frozen v1:

```python
@dataclass
class HandoffRecord:
    schema_version: int            # = 1; forward-compat: readers tolerate unknown fields
    task_id: str                   # bare T<PP>.<TT>
    phase: int                     # REQUIRED — disambiguates the key (see H5)
    status: str                    # TaskStatus.value: "pass"/"fail"/"fail_recoverable"/"incomplete"/"skipped" (TaskResult.to_dict, models.py:206)
    gate_outcome: str              # [CORRECTED v2] GateOutcome.value: "pass"/"fail"/"deferred"/"pending" (models.py:207). NOT dict|None — the source TaskResult.gate_outcome is a GateOutcome ENUM (never None, never a dict). The H5 skip predicate uses GateOutcome(gate_outcome).is_success.
    turns_consumed: int
    exit_code: int
    output_path: str
    started_at: str
    finished_at: str
    produced_artifacts: list[str]  # NEW delta field
    consumed_upstreams: list[str]  # NEW delta field (declared upstream task_ids)
```

Tests: round-trip fidelity (all fields), forward-compat (unknown field round-trips unchanged), `read(missing)` → typed `None`.

### H5 — Resume contract (predicate + key + CLI surface, none of which exist yet)

1. **Skip predicate** = *validated successful* record: `status == PASS AND gate_outcome is success`. Mere file existence is unsafe — `FAIL_*`/`INCOMPLETE`/`SKIPPED` tasks also produce records. Test that each non-success state is **not** skipped on resume.
2. **On-disk key** = `handoff/phase-{N}-task-{task_id}.json` (mirror `task_output_file`, `models.py:562`). Bare `T<PP>.<TT>` is **not** sprint-unique and collides across phases.
3. **CLI surface** — `--start/--end` are phase-granular ints (`commands.py:75-83`) and there is **no `--resume` handler**, yet `resume_command()` already emits `--resume {halt_task_id}` (`models.py:877`). Stage 2 must (a) add a `--resume <task_id>` `click.option` + `SprintConfig` plumbing, (b) define its composition with phase `--start/--end`, (c) reconcile the dangling `resume_command()` output. Add a back-compat rule: resume against a pre-Stage-1 `release_dir` (no `handoff/`) degrades to today's phase-granular behavior.

### H6 — Stage-3 shared-state inventory + a testable isolation seam (and reuse the dep primitive)

- **Shared-state inventory (before the scheduler):** `execute_phase_tasks` mutates more than `TurnLedger` — also `results`, `remaining`, `gate_results`, TUI state, `shadow_metrics`, `remediation_log`, `sprint_result`, and the lock-free `_jsonl` (`logging_.py:265-267`). Each needs single-writer discipline or a lock under K>1. State explicitly that Stages 0-2 rely on the sequential single-writer invariant and the Stage-3 `_jsonl` fix must cover the `write_task_complete` writer added in Stage 0/1.
- **Test seam:** the existing `_subprocess_factory` returns the result tuple directly (`executor.py:1003-1004`), **bypassing `env_vars`** — so per-worker `CLAUDE_SETTINGS_DIR` isolation is untestable through it. Add an `_env_capture`/`_env_builder` injection point so a unit test can assert each worker gets a unique settings dir.
- **Reuse, don't re-derive:** build the DAG scheduler on `rerun_tasks.py`'s `walk_dependencies`/`_dependencies_of` (`rerun_tasks.py:438-449`), not a fresh parse of `TaskEntry.dependencies`.

### Reconciliation note (LOW, but author must not duplicate)

`executor.py:1117` comment "Turn counting is wired separately in T02.06" references an existing turn-counting task. Stage 0's "fix `turns_consumed=0`" must fold into / supersede T02.06, and its acceptance test must assert the *correct* turn count, not merely `!= 0`.

---

## 7. MEDIUM + LOW reflection findings resolved

Same audit as §6. **M1** is already resolved in §6 · H6 ("reuse, don't re-derive" the `rerun_tasks.py` dep primitive); **L1** in the Reconciliation note above. The remainder:

### MEDIUM

**M2 — `_jsonl` concurrency: make the ordering dependency explicit.** Stage 0/1 add a per-task `write_task_complete` writer through the lock-free `_jsonl` (`logging_.py:265-267`). Spec must state: Stages 0-2 are safe **only** under the sequential single-writer invariant; the logger concurrency architecture is *decided* in Stage 1 (runner-owned single-writer queue vs per-task event files merged deterministically) and *implemented* in Stage 3, which must cover every writer added in Stages 0-1.

**M3 — Per-task prompt composition table (Stage 1).** `build_prompt` is monolithic/phase-scoped (`process.py:169-216`). "Narrowed to one task" must specify, per section:

| `build_prompt` section | Per-task disposition |
|---|---|
| Sprint Context (prior-phase dirs) | KEEP, narrowed to this task's declared upstreams |
| Execution Rules | KEEP |
| `/sc:task Execute all tasks in @{phase_file}` | REWRITE → single-task directive |
| Checkpoints (scan phase file) | DROP (phase-terminal; runner/coordinator owns) |
| Scope Boundary | KEEP, scoped to the task |
| Result File / `EXIT_RECOMMENDATION` | DROP from worker — the runner (or Path-A coordinator) writes the phase result file by aggregating per-task handoffs |

Decision required: the **runner aggregates** per-task handoffs into `config.result_file(phase)` (recommended); workers do not each write it.

**M4 — Flag + config plumbing (name the owning stage).** Enumerate the new surface so it is not invented ad-hoc:

| Flag | `SprintConfig` field | `click.option` site | Stage |
|---|---|---|---|
| `--task-parallelism K` | `task_parallelism: int = 1` | `commands.py run()` | 3 |
| `--handoff on\|off` | `handoff_enabled: bool = True` | `commands.py run()` | 1 |
| store select | `handoff_store: str = "file"` | config/internal | 1 (file) · 4 (mail) |

The Stage-4 "one config line" rollback depends on `handoff_store`. Add the plumbing as explicit tasks.

**M5 — Migration / back-compat for in-flight sprints.** A `release_dir` created before Stage 1 has no `handoff/` dir and no `task_complete` events. Decision: resume against such a dir **degrades to today's phase-granular behavior** (documented default); `handoff/` is created lazily on first write; `--handoff=off` reproduces legacy behavior exactly. Add a back-compat regression task.

**M6 — Heading-regex fallback is a GLOBAL routing change (Stage 1).** The B→A demotion fix touches `_TASK_HEADING_RE` / `_parse_phase_tasks` (`config.py:380`; `executor.py:1264`), affecting **every** phase's path selection — including existing Path A phases. Decision: **warn-only, no reclassification** — a near-miss heading emits a loud WARN but does NOT auto-reroute. Acceptance: a ≥10-entry heading-variant corpus (correct · wrong level `####` · colon separator · extra whitespace · em-dash variants) with expected route + diagnostic, plus a regression over existing Path A phase files confirming zero reclassification.

**M7 — Stage-1 schema-freeze gate is premature.** Change the Stage-1 gate from "schema frozen" to "schema **versioned + migration-safe**." The H4 v1 record already carries `schema_version` + `consumed_upstreams`; add a migration test (old reader tolerates a newly-added field) and freeze only after Stage-2 resume/fan-in tests exercise the fields.

### LOW

**L2 — Stage-4 rollback reword.** "Flip one line, free rollback" → "**data** rollback is lossless (the file store remained source of truth the whole pilot)." Add an operational teardown checklist task: stop sidecar, remove per-subprocess MCP config injection, revoke token, archive mailbox repo.

**L3 — Crash-consistency asymmetry test.** Handoff file = atomic temp+replace; journal = bare `_jsonl`. A crash between the two yields a completed task with no journal event. Add a test: write handoff atomically → kill before `_jsonl` append → resume scan treats handoff files (not the JSONL) as the authoritative completion source.

**L4 — Remaining test gaps.** (a) Stage-3 wall-clock win needs a defined baseline + fixed-duration mock-subprocess harness (assert parallel < 0.5× serial at K=4). (b) DAG+resume: a task in-flight at kill time has no handoff file → its dependents must not launch on resume. (c) Stage-4 mail-server mid-sprint failover: kill server at task N/2 → all subsequent writes route to `FileHandoffStore`, sprint completes, zero handoff loss.

**L5 — Documentation tasks.** Each new user-visible surface (`--task-parallelism` / `--handoff` flags, the `handoff/` artifact, the new `task_complete` ledger event) gets a docs/changelog sub-task in the stage that ships it.
