# Sprint CLI — Intra-Agent Communication & Task→Task Handoff (Deep Brainstorm)

**Agent 2 of 2** · Scope: handoff mechanism (mcp_agent_mail vs handoff `.md` files vs inlined prompt)
**Date:** 2026-06-02 · **Depth:** deep / research:deep / proposals:3
**Coupling note:** This decision is tightly coupled to Agent 1's execution-model choice (per-phase session vs per-task swarm). Read the COUPLING section before acting on any recommendation.

---

## 0. TL;DR / Ranked Recommendation

1. **WINNER — Middle roadmap: structured handoff schema on disk, with an optional agent-mail pilot gated behind real concurrency.** Start with a typed, append-only **handoff record** written by the runner (not the agent) per task, consumed by `build_prompt()` for the next task. This closes the `execution-log.jsonl` audit gap *and* unblocks within-phase resume, at a fraction of agent-mail's operational cost, and it does not introduce any new concurrent shared-mutable-state writer (the class of bug that corrupted the shared Claude config). Agent-mail becomes a *later, optional* substrate that only pays for itself once Agent 1 ships bounded-parallel/DAG execution at concurrency ≥ ~3.
2. **Conservative — `.md`-only handoff.** Acceptable MVP; least risk; but leaves structured audit/resume half-solved and forces re-parsing of prose.
3. **Aggressive — agent-mail-first.** Strong fan-in/fan-out and audit story *on paper*, but the cost/complexity (Python 3.14, a long-lived HTTP FastMCP server on port 8765, a second git repo, bearer-token auth, MCP wiring inside every spawned `claude`) is disproportionate to today's **sequential** execution, and it re-introduces a shared-mutable-state writer under exactly the concurrency conditions that already bit this project. Recommended only if Agent 1 picks an aggressive swarm AND multi-project agent coordination becomes a goal.

The cleanest framing: **the handoff substrate should be the simplest thing that (a) is runner-owned and append-only, (b) fixes the audit gap, and (c) survives the concurrency model Agent 1 actually ships.** A typed file/dir record clears that bar today; agent-mail clears it only at swarm scale and at much higher operating cost.

---

## 1. Research: what mcp_agent_mail *actually* is

**Source:** https://github.com/Dicklesworthstone/mcp_agent_mail (README fetched 2026-06-02 via GitHub web + raw README). All capability claims below are grounded in the README; items I could not confirm are flagged **UNVERIFIED**.

### 1.1 Core abstractions
- **Agents** are named identities — "memorable adjective+noun, unique per project" (e.g. *GreenCastle*). Each agent has a persistent **inbox** and **outbox**.
- **Addressing is project-scoped** via a `project_key` (typically a repo's absolute path). Cross-project messaging requires an explicit **AgentLink** approval handshake (`request_contact` / `respond_contact`); otherwise the system "fails loud with `CONTACT_REQUIRED`" rather than silently queueing. This is a *human/agent collaboration* model, not a generic message bus.
- **File reservations / leases** are a first-class concept: an agent can reserve file paths as an *advisory* lease ("please don't modify overlapping surfaces"), TTL-based, visible and auditable. Conflicts are **reported but the reservation is still granted** — advisory, not enforced (a pre-commit guard can optionally block conflicting commits if installed).

### 1.2 MCP tool surface (verbatim names)
Granular tools: `ensure_project`, `register_agent`, `send_message`, `fetch_inbox`, `acknowledge_message`, `reply_message`, `summarize_thread`, `search_messages`, `file_reservation_paths`, `release_file_reservations`, `request_contact`, `respond_contact`, `set_contact_policy`, `whois`, `acquire_build_slot` ("advisory, per-project coarse locking" for long-running tasks).
Macro tools (bundled multi-step flows): `macro_start_session`, `macro_prepare_thread`, `macro_file_reservation_cycle`, `macro_contact_handshake`.

### 1.3 Storage backend & durability
**Dual persistence:**
- **SQLite + FTS5** — fast search, directory queries, and the reservation/lease ledger. DB operations are "short-lived and scoped to each tool call."
- **Per-project Git repo of human-readable Markdown** — every canonical message and per-recipient inbox/outbox copy. Default `STORAGE_ROOT` = `~/.mcp_agent_mail_git_mailbox_repo`. Layout: `messages/YYYY/MM/<msg-id>.md`, per-agent mailbox dirs, `file_reservations/<sha1-of-path>.json`. "Artifacts are written first, then committed as a cohesive unit."

### 1.4 Concurrency model (critical for this analysis)
- "**One request/task = one isolated operation.**"
- "Archive writes are guarded by a per-project **`.archive.lock`**."
- "Git index/commit operations are serialized … by a repo-level **`.commit.lock`**."
- So agent-mail *does* serialize its own writers with file locks against a **shared archive repo**. This is the relevant nuance for the corruption-class risk (see §3.4): it is engineered to be concurrency-safe *for its own files*, but it is **a single shared mutable store with a global commit lock** — meaning N concurrent agents contend on one `.commit.lock` and one git index. That is a contention point, not obviously a corruption point, *provided the locking is correct*. (Correctness of that locking is **UNVERIFIED** — I did not audit the implementation; the README asserts it.)

### 1.5 Setup / operational requirements
- **Python 3.14** venv, managed via `uv`. (Note: the Sprint CLI project targets Python ≥3.10; 3.14 is a *separate* runtime for the mail server, not a constraint on the CLI itself, but it is another toolchain to provision.)
- **HTTP-only FastMCP server (Streamable HTTP). No SSE, no STDIO.** Default port **8765**. Auth via static bearer token or JWT+JWKS.
- Launched via `scripts/run_server_with_token.sh` or `uv run python -m mcp_agent_mail.cli serve-http`. One-line curl installer sets up venv + an `am` shell alias.
- **Operational implication:** this is a *persistent daemon* with a lifecycle the Sprint CLI would have to own (start before sprint, health-check, tear down, handle crash/restart, manage the token). The Sprint CLI today spawns ephemeral `claude` subprocesses with **no long-lived sidecar** — adopting mail adds a new always-on dependency to the run.

### 1.6 Delivery / ordering guarantees
The README does **not** state at-least-once, exactly-once, or ordering guarantees. Messages are persisted atomically *per call* to git+SQLite; `fetch_inbox` "preserves thread_id where available." There is **no documented total order** across messages and **no documented redelivery / ack-retry protocol** beyond `acknowledge_message` marking acks. Treat ordering as **best-effort by write-time**, **UNVERIFIED** for anything stronger.

### 1.7 Maturity signals
~2k stars, 207 forks, **832 commits**, **0 open issues / 0 open PRs**, status "**Under active development.**" High activity and zero-issue hygiene are positive signals; but "0 open issues" on an actively-developed solo-ish project can also mean a small user base surfacing few bugs. No tagged releases were confirmed (**UNVERIFIED** — I did not enumerate the releases page). Bottom line: **promising and active, but young; not a battle-tested dependency** you'd bet a CI-critical handoff path on without a pilot.

---

## 2. Grounding in the Sprint CLI (where a handoff lives in the code)

Absolute base: `/config/workspace/IronClaude/src/superclaude/cli/sprint/`

- **`process.py::build_prompt()`** (`process.py:123`) builds the per-phase prompt: `/sc:task Execute all tasks in @{phase_file} --compliance strict --strategy systematic` + a **Sprint Context** block that *already* injects prior-phase artifact/results directories (`process.py:147-167`). There is already a context-injection seam: `build_task_context()` / `compress_context_summary()` (`process.py:257-385`) serialize prior `TaskResult`s to markdown for inlining. **This is the natural home for an inlined-prompt handoff** — but note it is keyed off `TaskResult` objects held *in memory by the runner*, not off any durable artifact.
- **`executor.py::execute_phase_tasks()`** (`executor.py:927`) is the per-task subprocess loop. It already constructs an authoritative `TaskResult` per task from the subprocess exit code (`executor.py:1032-1040`) — "constructed by the runner … not agent self-reported" (`models.py:162`). **This is where a handoff record would be *produced*.**
- **`executor.py::aggregate_task_results()`** (`executor.py:296`) folds `TaskResult`s into the runner-owned phase report — the existing pattern of *runner-owned* truth that any handoff design should extend, not bypass.
- **`executor.py::run_post_task_wiring_hook()`** (`executor.py:458`) is the existing post-task hook seam. A "write handoff record" step slots in right beside it (same call site, `executor.py:1043`).
- **`checkpoints.py`** is the existing **on-disk manifest baseline**: `write_manifest()` (`checkpoints.py:169`) writes JSON **atomically via temp-file + `replace()`** (`checkpoints.py:204-206`), and `recover_missing_checkpoints()` (`checkpoints.py:209`) already does failure-injection-style reconstruction from evidence. **Any `.md`/structured handoff should reuse this atomic-write + recovery idiom verbatim.**

### 2.1 The audit gap is real and specific
`logging_.py` has **no `task_complete` writer at all.** `SprintLogger` emits `phase_start`, `phase_interrupt`, `phase_complete`, `checkpoint_verification`, `checkpoint_manifest`, and `sprint_complete` (`logging_.py:59-201`), all via `_jsonl()` (`logging_.py:210-212`). The only per-task-ish event in the whole file is the `checkpoint_manifest` write at `executor.py:1713`. **`execute_phase_tasks()` builds a `TaskResult` for every task but never journals it.** So the briefing's "`task_complete` journaling is UNRELIABLE (only some tasks journaled)" is generous — *structurally there is no per-task ledger event being written by the logger at all*; per-task truth lives only in transient in-memory `TaskResult` lists and the aggregated phase report. **This is the single strongest argument for a durable, runner-owned handoff record: it would simultaneously become the missing per-task ledger.**

### 2.2 The `_jsonl` writer itself is not concurrency-safe
`_jsonl()` is a bare `open(path, "a"); f.write(json.dumps(...))` (`logging_.py:210-212`) — no lock, no `flush`/`fsync`, no atomic rename. Under today's **sequential** model that's fine (one writer). Under Agent 1's **bounded-parallel swarm**, N runner threads/processes appending to one `execution-log.jsonl` is exactly a concurrent-writer hazard. **Whatever handoff mechanism we pick must not make the ledger a contended shared writer** — which is the same lesson the shared-config corruption already taught (§3.4).

---

## 3. Three mechanisms, weighed across the axes

### Axis A — Setup / operational complexity
| | Inlined prompt | `.md` / structured-on-disk | agent-mail |
|---|---|---|---|
| New deps | none | none | Python 3.14 venv, FastMCP server, port 8765, bearer token |
| Lifecycle to own | none | none (just files) | start/health-check/teardown a daemon per run + crash handling |
| Wiring into spawned `claude` | already done (prompt string) | trivial (write/read files) | must register the MCP server + creds inside *every* isolated subprocess — and the 4-layer isolation (`executor.py:106-182`) deliberately strips plugin/settings dirs, so each child would need explicit, controlled re-injection of the mail MCP config |
**Winner: inlined / `.md` (tie).** agent-mail is the clear loser — it fights the isolation design.

### Axis B — Reliability & ordering guarantees
- **Inlined prompt:** ordering is whatever the runner inlines; no durable record; if the parent dies the handoff evaporates (it's only in the prompt string).
- **`.md`/structured:** runner writes atomically (reuse `checkpoints.py` temp+replace); ordering is explicit (filename/sequence index); durable on disk. Strong and *simple*.
- **agent-mail:** durable (git+SQLite), but ordering is **best-effort by write-time, UNVERIFIED** for total order; adds a network hop and a serialized global `.commit.lock` that can stall under contention.
**Winner: `.md`/structured** for the Sprint CLI's needs (it controls its own ordering deterministically and doesn't need a mailbox abstraction to do it).

### Axis C — Observability / auditability (the `execution-log.jsonl` gap)
- **Inlined prompt:** *worsens* the gap — handoff content lives transiently in prompt strings, invisible after the run.
- **`.md`/structured:** **directly fixes it.** A runner-owned `handoff/T<PP>.<NN>.json` (or `.md`) per task *is* the missing `task_complete` ledger. Add one `logger.write_task_complete(...)` call beside the wiring hook (`executor.py:1043`) and the audit gap closes regardless of which substrate you choose.
- **agent-mail:** good audit story (every message is a committed markdown file with frontmatter + searchable via FTS5), but it's a **parallel, external** audit trail in `~/.mcp_agent_mail_git_mailbox_repo`, divorced from the sprint's own `release_dir`. You'd be auditing across two stores.
**Winner: `.md`/structured** — fixes the actual gap *in place*, in the release dir, with the existing tooling.

### Axis D — Failure modes (esp. the shared-config corruption class)
The killer fact: **concurrent fresh `claude` spawns intermittently corrupted a SHARED CLAUDE CONFIG file via concurrent-writer contention.** The lesson is *single shared mutable file + N concurrent writers = corruption*.
- **Inlined prompt:** no shared mutable state at all — immune to this class. (Its failure mode is *information loss*, not corruption.)
- **`.md`/structured (done right):** **one file per task, runner-owned, atomic temp+replace** → no two writers ever touch the same file. Immune to the corruption class *by construction*. The anti-pattern to avoid is a *single* shared `handoff.md` that every task appends to (that would reproduce the bug); the design must be **one-record-per-task**, mirroring how `checkpoints.py` writes one manifest atomically.
- **agent-mail:** re-introduces a **single shared store** (the global mailbox git repo + one `.commit.lock`). The README claims correct locking, but: (1) that locking correctness is **UNVERIFIED**; (2) it's the *same shape* as the bug that already bit this project (one shared store, many concurrent agents); (3) it adds a serialized global commit lock as a throughput bottleneck. This is the axis where agent-mail is most dangerous for *this specific project*.
**Winner: per-task `.md`/structured** (immune by construction). Inlined is also immune but loses on audit.

### Axis E — Fit with a per-task swarm (Agent 1's direction), fan-in/fan-out, DAG deps
- **Inlined prompt:** **only works if a parent coordinator builds child prompts.** In a coordinator+workers hybrid, the coordinator can inline each child's upstream-dependency outputs into that child's prompt — clean fan-out. **Fan-in is awkward**: the coordinator must gather multiple child outputs and re-inline, and prompt size grows with fan-in width (token cost, Axis F).
- **`.md`/structured:** **fits a DAG naturally.** Each task writes `handoff/<task_id>.json`; a downstream task reads its declared upstreams' handoff files (pull-on-demand). Fan-in = read K files; fan-out = K readers of one file. No coordinator required for correctness — works for sequential, bounded-parallel pool, *and* coordinator+workers. Resume-friendly (the files persist).
- **agent-mail:** **purpose-built for fan-in/fan-out** (inboxes, threads, `summarize_thread`, `fetch_inbox`). This is where it shines — at *high* concurrency with *many* peers needing async coordination and file-reservation arbitration. But the Sprint CLI's DAG is a *known, declared* dependency graph the runner already owns; it doesn't need agents to *discover* each other via mailboxes. The mailbox model solves a coordination problem the runner can solve more cheaply by reading the DAG it already has.
**Winner: `.md`/structured for the likely swarm shapes (sequential/bounded-parallel/coordinator).** agent-mail wins *only* at aggressive, high-concurrency, peer-discovery scenarios — which is not where Agent 1 is starting.

### Axis F — Token cost
- **Inlined prompt:** **grows context every task** (already mitigated by `compress_context_summary()` at `process.py:347`, but fan-in compounds it). Worst on tokens.
- **`.md`/structured:** **pull-on-demand** — a task reads only the upstream handoffs it needs. Cheapest steady-state.
- **agent-mail:** also pull-on-demand (`fetch_inbox`/`search_messages`), but each fetch is an MCP round-trip with its own token overhead in the tool-call protocol.
**Winner: `.md`/structured.**

### Axis G — Resume / recovery value (the phase-granular resume gap)
Today resume is **phase-granular only**; the prompt carries **no skip-completed logic** (confirmed: `build_prompt()` has no completed-task filtering, `process.py:169-216`).
- **Inlined prompt:** no resume value — nothing durable.
- **`.md`/structured:** **high resume value.** On resume, the runner reads existing `handoff/<task_id>.json` files, marks those tasks done, and `build_prompt()` (or the per-task loop) skips them — enabling **within-phase task resume** for the first time. This is a concrete, independent win even if Agent 1 changes nothing.
- **agent-mail:** durable inbox could also drive resume, but you'd query an external store; more moving parts for the same outcome.
**Winner: `.md`/structured.**

---

## 4. Roadmaps (3 distinct rollouts) — code changes, tests, gates, rollback

All roadmaps share **Principle Z (non-negotiable):** the handoff record is **runner-owned, one-file-per-task, written atomically (temp + `os.replace`), append-only at the directory level.** No shared single mutable file. This is what makes every option immune to the corruption class. New artifacts live under `config.release_dir / "handoff" / "<task_id>.json"` and the per-task ledger event is added to `SprintLogger`.

### Roadmap 1 — CONSERVATIVE (`.md`-only)
**Thesis:** minimum change; fix audit + resume with plain markdown handoff files; never touch agent-mail.

- **Phase C1 — `.md` handoff MVP**
  - *Code:* In `execute_phase_tasks()` (`executor.py:927`), after each `TaskResult` is built (`executor.py:1040`) and beside `run_post_task_wiring_hook` (`executor.py:1043`), write `handoff/<task_id>.md` via a new `write_handoff(result, config)` (reuse `checkpoints.py` temp+replace idiom). Add `SprintLogger.write_task_complete(result)` → `_jsonl({"event":"task_complete", ...})` (the missing event).
  - *Tests:* **round-trip fidelity** (write `TaskResult` → read `.md` → assert no field loss); **failure-injection** (kill runner between two task writes → assert prior handoff intact, no partial file via temp+replace); **missing handoff** (downstream reads absent upstream → defined fallback, not crash).
  - *Gate to advance:* 100% of tasks in a real 3-phase sprint produce a `task_complete` event and a handoff file; audit-gap closed (every task journaled).
- **Phase C2 — Resume on handoff**
  - *Code:* In the runner's resume path and `build_prompt()` context section (`process.py:147`), read existing `handoff/*.md`, inject a "Completed tasks (skip): …" block, and have the per-task loop skip tasks with an existing handoff.
  - *Tests:* **within-phase resume** integration test (run phase, kill mid-phase, resume, assert completed tasks skipped, remaining run); **ordering** test (handoffs read in task-id order).
  - *Gate:* mid-phase kill+resume reaches phase completion without re-running completed tasks. **Rollback:** feature-flag `--handoff=off` restores today's behavior (handoff dir simply ignored).
- **Escape hatch:** the whole feature is additive + flag-guarded; disabling it leaves `execution-log.jsonl` exactly as today.

### Roadmap 2 — MIDDLE (structured schema → optional agent-mail pilot) ★ recommended
**Thesis:** make the handoff a **typed schema** (so it's machine-consumable for DAG fan-in and resume), keep it on disk and runner-owned, then *optionally* pilot agent-mail behind an adapter only when concurrency justifies it.

- **Phase M1 — Structured handoff schema (JSON)**
  - *Code:* Define a `HandoffRecord` dataclass (status, gate_outcome, turns, output_path, produced_artifacts[], consumed_upstreams[], started/finished) — extend `TaskResult` (`models.py:159`) serialization. Write `handoff/<task_id>.json` atomically beside the wiring hook (`executor.py:1043`). Add `write_task_complete` to `SprintLogger`. Introduce a thin `HandoffStore` interface (`write(record)`, `read(task_id)`, `list()`) with a `FileHandoffStore` impl — *this interface is the seam that lets agent-mail slot in later without touching the executor.*
  - *Tests:* schema **round-trip fidelity** (JSON write→read, all fields); **schema-version** test (forward-compat field added → old reader tolerates); failure-injection (partial write impossible via temp+replace); **lost-record** test (store.read of missing id → typed `None`, callers handle).
  - *Gate:* schema stable; audit gap closed; `HandoffStore` interface frozen.
- **Phase M2 — DAG fan-in + within-phase resume on the schema**
  - *Code:* `build_prompt()` / per-task loop consults `HandoffStore` for declared upstream task IDs and inlines (or references) only those records (pull-on-demand). Resume skips tasks with an existing record.
  - *Tests:* **fan-in** integration (task with 2 upstreams reads both records, no loss); **ordering** (topological order honored); **concurrency/race** test that *directly exercises the corruption class* — spawn N concurrent writers to `FileHandoffStore` for distinct task IDs, assert every file is well-formed and the shared `execution-log.jsonl` is not garbled (this also forces fixing `_jsonl()`'s lack of locking — add a per-process lock or one-writer discipline, `logging_.py:210`).
  - *Gate:* bounded-parallel writes (simulated, ≥4 concurrent) produce zero corrupted files/ledger lines across 100 runs.
- **Phase M3 — agent-mail PILOT behind the `HandoffStore` adapter (optional, concurrency-gated)**
  - *Trigger condition:* only enter if Agent 1 has shipped real bounded-parallel/DAG execution at concurrency ≥ ~3 **and** there's a concrete need agent-mail uniquely serves (e.g. file-reservation arbitration between concurrent writers via `file_reservation_paths`, or cross-project coordination).
  - *Code:* implement `MailHandoffStore(HandoffStore)` calling `register_agent`/`send_message`/`fetch_inbox`; stand up the FastMCP server lifecycle as a sprint-managed sidecar (start, health-check on 8765, token, teardown); inject the mail MCP config into each subprocess's controlled settings dir (working *with* the 4-layer isolation, `executor.py:106`, not bypassing it). **Run mail in SHADOW alongside `FileHandoffStore`** (dual-write, file remains source of truth).
  - *Tests:* **server-lifecycle** (start/health/teardown, crash-restart); **lost-message** test (send→fetch parity vs the file store — file store is the oracle); **concurrency/race** against the shared mailbox git repo + `.commit.lock` under N agents (the agent-mail analog of the corruption test — this is where you'd discover if the global commit lock corrupts or merely stalls); **failure-injection** (server down mid-sprint → fall back to file store, sprint continues); **e2e multi-agent** (3 workers + coordinator round-trip).
  - *Gate to "full adoption":* mail store matches file store byte-for-byte-semantically on ≥3 real sprints in shadow, zero corruption under the race test, and operational toil (server lifecycle) judged acceptable. **Rollback:** flip the `HandoffStore` impl back to `FileHandoffStore` (one config line) and kill the sidecar — because the file store was the source of truth the whole pilot, rollback is free and lossless.
- **Escape hatch at every phase:** the `HandoffStore` interface means the substrate is swappable; the file impl is always the safe default.

### Roadmap 3 — AGGRESSIVE (agent-mail-first)
**Thesis:** adopt agent-mail as the primary substrate early to get inbox/thread/reservation primitives for a high-concurrency swarm.

- **Phase A1 — Stand up agent-mail as the handoff substrate**
  - *Code:* sidecar lifecycle + per-subprocess MCP injection (as M3 but as the *primary*, no file oracle); `register_agent` per task; `send_message` as the handoff producer; `fetch_inbox` as the consumer; map `task_complete` to an acknowledged message.
  - *Tests:* full lifecycle, round-trip, lost-message, **and** the race test against the shared mailbox repo *as a blocking gate before any real sprint uses it* (because here there's no file fallback to mask corruption).
  - *Gate:* race test green at target concurrency, server stable across crash/restart.
- **Phase A2 — File reservations for concurrent-writer arbitration**
  - *Code:* use `file_reservation_paths`/`release_file_reservations` so concurrent tasks declare which files they'll touch (directly addressing the *write-contention* family of the corruption bug at the application layer).
  - *Tests:* reservation-conflict integration; advisory-vs-enforced behavior (remember conflicts are *reported, still granted* — assert the runner actually enforces, since mail won't); failure-injection on a crashed reservation holder (TTL expiry).
  - *Gate:* concurrent file-touching tasks never corrupt shared files in a 100-run stress test.
- **Phase A3 — Retire any disk handoff; agent-mail is canonical**
  - *Gate:* 5 real sprints, zero corruption, audit fully reconstructable from the mailbox repo. **Rollback:** *expensive* — there's no disk oracle; rollback means rebuilding the file path you skipped. This is the roadmap's core weakness.
- **Escape hatch:** weak. Once agent-mail is canonical with no shadow file store, backing out is a real migration, not a flag flip.

---

## 5. Adversarial comparison — mechanisms

| Axis | Inlined prompt | `.md` / structured-on-disk | agent-mail |
|---|---|---|---|
| Setup/ops complexity | **lowest** (already there) | low (plain files) | **highest** (Py3.14 daemon, port 8765, token, MCP wiring vs isolation) |
| Reliability & ordering | weak (transient) | **strong, runner-deterministic** | durable but ordering best-effort / UNVERIFIED |
| Observability / fixes audit gap | **worsens** it | **fixes it in place** (becomes the `task_complete` ledger) | good but a *second*, external store |
| Failure mode: corruption class | immune (no shared state) | **immune by construction** (1 file/task, atomic) | re-introduces a shared store + global commit lock (UNVERIFIED locking) |
| Fit w/ swarm, fan-in/out, DAG | only with a coordinator; fan-in awkward | **fits all swarm shapes**, DAG-native | **best at high-concurrency peer coordination** (overkill otherwise) |
| Token cost | **worst** (context grows) | **best** (pull-on-demand) | good (pull) but per-fetch MCP overhead |
| Resume/recovery value | none | **high** (enables within-phase resume) | high but via external query |
| Maturity / trust | n/a | uses proven local idiom (`checkpoints.py`) | young dep; active but unbattle-tested |

**Verdict:** `.md`/structured dominates on 6 of 8 axes for *this* project's current shape; inlined wins only on raw setup; agent-mail wins only on the high-concurrency-coordination axis that isn't yet in play.

## 6. Adversarial comparison — roadmaps

| | Conservative (`.md`-only) | **Middle (schema → optional mail)** | Aggressive (mail-first) |
|---|---|---|---|
| Closes audit gap | yes | yes | yes |
| Enables within-phase resume | yes | yes | yes |
| Machine-consumable for DAG fan-in | partial (prose) | **yes (typed schema)** | yes |
| Corruption-class risk added | none | none (file default) | **yes, early & unmasked** |
| Operational toil | none | none until pilot | high from day 1 |
| Rollback safety | trivial | **trivial (interface swap, file oracle)** | poor once canonical |
| Future-proof for swarm | limited | **high (swappable substrate)** | high but locked-in |
| Cost/benefit vs *today's sequential* | good | **best** | poor (pays for concurrency you don't have yet) |

---

## 7. COUPLING to Agent 1's execution-model decision (explicit)

The handoff choice is **not independent** of the execution model:

- **If Agent 1 keeps the per-phase single session (status quo):** handoff barely matters — there's one agent per phase, no intra-phase peers. Do **Conservative C1 only** (handoff files purely to close the audit gap + enable within-phase resume). agent-mail is pure overhead here. *Do not* build the schema/pilot.
- **If Agent 1 picks sequential per-task spawn:** **Middle M1–M2.** Typed handoff on disk gives clean task→task chaining and resume; no concurrency, so the corruption class isn't even in play, and agent-mail has nothing to offer. Skip M3.
- **If Agent 1 picks bounded-parallel DAG pool or coordinator+workers:** **Middle M1–M3.** Now fan-in/fan-out and concurrent writers are real. The schema + `HandoffStore` interface is essential; the **race test (M2) and file-reservation question become first-order**; and the agent-mail *pilot* (M3, shadow) is finally justified to evaluate for reservation arbitration — but only as a shadow against the file oracle.
- **Inlined-prompt handoff is viable ONLY under coordinator+workers** (a parent that builds child prompts). It is *not* a substrate choice so much as a *delivery* choice — and even then it should be backed by the durable schema for audit/resume, because the prompt string is not auditable. So: never inlined-*only*.
- **agent-mail only pays off at higher swarm concurrency** (≥~3 concurrent agents needing async coordination / file-reservation arbitration / cross-project links). Below that, its shared-store + global-commit-lock shape is a *liability* that echoes the exact corruption bug this project already suffered.

**Net coupled recommendation:** adopt **Middle**, scoped to whatever Agent 1 ships — file-backed typed handoff is the universal substrate; agent-mail is a *conditional, shadowed, reversible* upgrade that activates only when concurrency makes its primitives worth their operational cost. Whatever the choice, **add `SprintLogger.write_task_complete` immediately** — it closes the audit gap independently of every other decision and is the cheapest high-value change on the table.

---

## 8. Open questions / UNVERIFIED flags
- agent-mail's `.commit.lock` / `.archive.lock` **correctness under N concurrent agents is UNVERIFIED** (README-asserted, not code-audited). The M3/A1 race test exists specifically to verify it before trust.
- agent-mail **ordering guarantees beyond write-time are UNVERIFIED**; no documented redelivery protocol.
- agent-mail **release/tag maturity UNVERIFIED** (commit activity is high; tagged-release stability not confirmed).
- Whether Agent 1's swarm will need *file-reservation arbitration* (agent-mail's strongest unique feature) is **INFERENTIAL** — depends entirely on whether concurrent tasks can touch overlapping files, which the DAG dependency declarations may already prevent.
