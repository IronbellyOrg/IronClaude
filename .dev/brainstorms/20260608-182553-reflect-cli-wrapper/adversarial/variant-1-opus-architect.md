# Variant 1 — Architect: `superclaude reflect run` thin gate-wrapper

> Persona lens: **integration architecture & clean boundaries.** Maximize reuse of
> the existing pipeline/sprint subprocess primitives; keep `sc-reflect-protocol`
> the single source of truth. The wrapper is an *invocation + contract-consumption*
> shell, not a reimplementation of reflect.

---

## Problem

Task-builder-generated MDTM tasklists end with a **POST reflection gate** (the
penultimate item of the final phase — `src/superclaude/skills/task-builder/SKILL.md:1994-1999`).
Today that item writes `reflect_post: PENDING` and **HALTs for a human** to run
`/sc:reflect --mode post …` in a fresh session. The HALT design is *correct* on
the property that matters — it is **executor-disjoint** (a fresh top-level frame,
not the biased executor frame) — but it is **fully manual**.

The obvious automation (executor spawns an Agent-tool subagent running
`/sc:reflect`) is **structurally broken**: an Agent-tool subagent cannot nest a
skill that itself fans out subagents, so reflect's **Tier 2** (heterogeneous-model
reviewer ensemble + `sc-adversarial-protocol` Mode-A merge — SKILL.md §4 Wave 3/4,
§7.1) never executes (memory `reference_subagent_cannot_nest_skill_fanout`). Tier 2
is *mandatory* for medium/complex tasklists (TCS ≥ 13 → `standard`/`deep`,
`task-builder/SKILL.md:2139-2150`), so the subagent path silently degrades to a
single-agent self-review — exactly the representational bias reflect's structural
mechanisms exist to neutralize.

**The escape hatch** is that a *CLI subprocess* (`claude -p`) is a **top-level
process**, not an Agent-tool subagent, and therefore does **not** hit the nesting
limit. A new tasklist item can shell out to a thin wrapper that launches reflect
as that top-level subprocess, lets Tier 2 actually fan out, captures the emitted
`return-contract.yaml`, maps it to a `reflect_post:` verdict block, and writes it
back to the task frontmatter — turning the manual HALT into an unattended gate
**without** weakening the executor-disjoint property and **without** copying any
reflect logic into Python.

---

## Functional Requirements

- **FR-1 — Top-level reflect launch.** The wrapper MUST run `/sc:reflect --mode post`
  as a **top-level `claude --print` subprocess** (reusing `ClaudeProcess`,
  `src/superclaude/cli/pipeline/process.py:24`), never as an Agent-tool subagent.
  This is the sole reason Tier 2 fan-out succeeds.

- **FR-2 — Skill is the single source of truth.** The subprocess prompt MUST be a
  single `/sc:reflect …` slash invocation. The wrapper MUST NOT compute coverage,
  deviation classes, tier decisions, the promotion gate, or any reflect verdict in
  Python. It only *builds the invocation* and *consumes the contract*.

- **FR-3 — Deterministic input derivation.** The wrapper MUST derive, from the
  tasklist file + git, all reflect inputs:
  - `--diff <BASE>..HEAD` where `<BASE>` = frontmatter `start_commit`, else
    `git merge-base HEAD <integration-branch>` (mirrors `task-builder/SKILL.md:1996`).
  - `--tasklist <TASK_FILE>` (the path passed to the wrapper).
  - `--spec <SPEC_PATH>` when frontmatter `spec_path:` is present.
  - `--depth <DEPTH>` from the **TCS** (`task-builder/SKILL.md:2114-2150`), **floored
    at `standard`** per override O4 (POST never runs `--depth quick`).
  - `--executor-model <CLASS>` from frontmatter / `EXECUTOR_MODEL_CLASS`
    (feeds reflect's anti-self-confirmation exclusion, SKILL.md §7.1).

- **FR-4 — Pinned, deterministic output dir.** The wrapper MUST pass an explicit
  `--output <DIR>` (default `<task-dir>/reflect/post/`) so the
  `return-contract.yaml` location is **known** without scanning the default
  timestamped `.dev/reflect/<mode>-<slug>-<ts>/` path (SKILL.md §3.1, §9). It MUST
  reject an `--output` under `.claude/{skills,agents,commands}` (reflect STOP
  condition, SKILL.md:111) before launching.

- **FR-5 — Contract-driven verdict.** After the subprocess exits, the wrapper MUST
  parse `<output>/return-contract.yaml` (`contract_version: 1.3.0`, SKILL.md §9.1)
  and derive a single `verdict ∈ {pass, fail, partial, error}` from the contract
  fields (mapping in §"Verdict Write-back"). The wrapper MUST NOT invent a verdict
  the contract does not support.

- **FR-6 — Frontmatter write-back.** The wrapper MUST replace the `reflect_post:`
  frontmatter block of the tasklist with a structured block:
  `reflect_post: {verdict, run_id, report, contract, status, deviations}`
  (replacing the `PENDING`/`""` sentinel — `task-builder/SKILL.md:1942`, `:1999`).
  Write-back MUST be a surgical edit of the YAML frontmatter only (no body change).

- **FR-7 — Dual gate signal (exit code + contract).** The wrapper MUST exit with a
  **stable exit-code contract** AND leave the parsed contract on disk, so the
  completion-gate can consume *either*: `0` = pass (promotion-gate-clean),
  `10` = deviations present / HALT-for-human (drift/regression/grounding-gaps),
  `20` = reflect ran but `status: partial`, `124` = timeout (inherited from
  `ClaudeProcess.wait`, process.py:165), `30` = launch/parse error.

- **FR-8 — HALT on deviations, never auto-proceed.** When the contract carries any
  blocking signal — `unauthorized_deviation_present`, `regression_present`,
  `needs_human_decision`, `user_decision_required`, or `cannot_validate_without_user_input`
  (SKILL.md §9.1 asymmetric-cost flags) — the wrapper MUST write `verdict: fail`
  (or `verdict: partial`), surface the `report_path`, and exit non-zero so the
  Update-status-to-Done item stays HALTed (`feedback_human_decision_items_must_halt`).

- **FR-9 — Audit-only by default.** The wrapper MUST default to `--no-promote`
  (pass it through to reflect). Promotion (reflect Wave 7, SKILL.md §14.5) is
  opt-in via an explicit `--promote` flag on the wrapper. The wrapper itself MUST
  never `git add`/`git commit`/`mv` work-unit folders — promotion, if enabled, is
  done *inside reflect's own gated Wave 7*, not by the wrapper.

- **FR-10 — Headless MCP/model parity.** The subprocess env MUST inherit the
  operator's real `HOME`, MCP registration (Serena/auggie), and
  `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL` aliases so Tier-2 heterogeneity and
  grounding are not degraded (see §"Headless env parity" — this is the deliberate
  *opposite* of cliEval's `HomeIsolation`).

- **FR-11 — Resume / re-run.** Re-invoking the wrapper on the same tasklist MUST be
  safe and idempotent at the frontmatter level (overwrite the prior `reflect_post:`
  block with the new run). The wrapper MAY accept `--resume` to skip a completed
  clean run (verdict already `pass` for the current HEAD).

## Non-Functional Requirements

- **NFR-1 — Thinness.** New Python ≤ ~400 LOC across the subcommand. Zero
  reflect-logic duplication. Verified by: no deviation-taxonomy / tier-rubric /
  promotion-gate strings authored in the wrapper module.
- **NFR-2 — Reuse-first.** Subprocess lifecycle, signal handling, timeout, env
  scrubbing, stdout/stderr separation are **inherited** from `ClaudeProcess`, not
  re-coded (process.py:114-214).
- **NFR-3 — Reversibility.** The template change in task-builder is a **single
  opt-in item swap** behind an existing config flag; reverting restores the HALT
  item byte-for-byte.
- **NFR-4 — SoT discipline.** All edits land in `src/superclaude/`; `make sync-dev`
  mirrors to `.claude/`; never stage `.claude/` mirrors (CLAUDE.md ABSOLUTE RULE).
- **NFR-5 — Observability.** stdout (stream-json transcript) and stderr go to
  separate files under `<output>/` (process.py:120-123); the wrapper emits a
  one-line human summary (`verdict`, `run_id`, `report_path`, exit code).
- **NFR-6 — Bounded runtime.** A Tier-2 reflect run is 8-15 min; the wrapper MUST
  set a default timeout of **3600 s** (`--timeout` overridable) and surface `124`
  cleanly rather than hang the tasklist.
- **NFR-7 — No nesting violation.** The wrapper MUST be invoked from a tasklist
  item as a **Bash shell-out**, never via the Agent/Task tool (a test/lint guard
  documents this; see Risks R-4).

---

## Architecture & Reuse Map

The wrapper is a Click subcommand `superclaude reflect run` whose entire job is the
four arrows below. Each arrow reuses an existing primitive.

```
tasklist.md frontmatter ──derive──▶ reflect invocation (FR-3)
        │                                   │
        │                          ClaudeProcess.start()  ◀── REUSE pipeline/process.py:114
        │                          (top-level claude -p, FR-1)
        │                                   │
        │                          stream-json transcript + stderr files
        │                                   │  (REUSE process.py:120-123 separation)
        │                                   ▼
        │                          <output>/return-contract.yaml  ◀── reflect writes (SKILL.md §9)
        │                                   │
        └──write-back (FR-6) ◀──parse+map(FR-5)──┘
                                            │
                                   exit-code contract (FR-7) ──▶ completion-gate
```

### Reuse map (real anchors)

| Need | Reused primitive | Anchor |
|---|---|---|
| Spawn top-level `claude -p` with `--model`, `--print`, `--output-format`, timeout, env overlay, SIGTERM→SIGKILL, stdout/stderr split | `ClaudeProcess` (construct directly; pass `output_format="text"` or `stream-json`) | `src/superclaude/cli/pipeline/process.py:24`, `build_command` `:73`, `build_env` `:97`, `start` `:114`, `wait`/timeout-124 `:159-171`, `terminate` `:173` |
| `--model` per process (multi-vendor alias routing) | `ClaudeProcess.model` → `--model` | `process.py:92-93` |
| Env overlay merged over real `os.environ` (keeps Serena/auggie/`ANTHROPIC_DEFAULT_*`), strips `CLAUDECODE`/`CLAUDE_CODE_ENTRYPOINT` to dodge nested-session detection | `ClaudeProcess.build_env(env_vars=…)` | `process.py:97-112` |
| Optional **visible** detached window + attach + recover inner exit code via sentinel file | `launch_in_tmux` pattern (detached `new-session -d` → `attach-session` blocks → read `.sprint-exitcode`) | `src/superclaude/cli/sprint/tmux.py:81-173` |
| `<BASE>..HEAD` diff resolution helper | `get_git_diff_context` / `git merge-base` idiom | `src/superclaude/cli/sprint/process.py:371-393` |
| Subcommand registration (deferred import + `add_command`) | `main.add_command(<group>, name=…)` | `src/superclaude/cli/main.py:400-434` |
| Contract consumer precedent (null-`convergence_score` → `partial` → `halt-phase-for-review`) | sprint executor status routing | `sc-reflect-protocol/SKILL.md §8`, §11.0 |

### What the wrapper deliberately does NOT reuse

**`HomeIsolation` / `ClaudeProcessAdapter` are NOT used.** cliEval's adapter
(`src/superclaude/cli/eval/claude_process.py:107`) mkdtemp-s a **fresh isolated
HOME** to make evals hermetic — which would *strip* the operator's MCP servers,
`.claude/settings.json`, and `ANTHROPIC_DEFAULT_*` aliases. For the reflect gate
that is exactly wrong: it would silently kill Serena/auggie grounding and collapse
Tier-2 model diversity to a single class. The wrapper instead wants the operator's
**real** environment, so it uses bare `ClaudeProcess` with a small `env_vars`
overlay (FR-10). This is a load-bearing boundary decision, not an omission.

---

## Window Mechanic

**Decision: default = blocking foreground subprocess (no window); `--tmux` opt-in
for a visible/detachable run; the tasklist item uses the foreground default.**

Three candidate mechanics were on the table (seed OQ-1):

1. **Foreground `ClaudeProcess` (blocking, no window)** — the wrapper calls
   `proc.start(); rc = proc.wait()` (process.py:114,159) and parses the contract.
   The shelling tasklist item *blocks* on the Bash call until the wrapper returns.
   Simple, unattended, testable, exit-code is the wrapper's own return — no sentinel
   round-trip. **Chosen default.**

2. **tmux detached + attach + sentinel** (sprint's `launch_in_tmux`,
   tmux.py:81-173) — visible 3-pane TUI, detachable, recovers exit code from a
   `.reflect-exitcode` sentinel mirroring `.sprint-exitcode` (tmux.py:166). **Offered
   behind `--tmux`** for operators who want to watch the 8-15 min Tier-2 run live.
   Reuses the exact detached-session + attach-blocks + sentinel idiom; the wrapper
   writes its own exit code to `<output>/.reflect-exitcode` and the outer process
   reads it back.

3. **Printed single-line command** — degenerate (it *is* the current HALT). Kept
   only as the `--print-command` dry-run escape so an operator can paste-run the
   exact invocation. Not the automation path.

**Why foreground is the default for the tasklist item:** the gate must run
*unattended in the common path* (success criterion #1). A blocking foreground call
gives the tasklist a direct exit code and contract with no tmux dependency
(`is_tmux_available` can be false inside CI or another tmux session — tmux.py:50-55).
`--tmux` is purely an operator-ergonomics upgrade and reuses sprint's proven
machinery rather than inventing a new poller.

**Detached-and-poll** is intentionally *not* a third independent mode: the
foreground call already blocks the shelling item, and `--tmux` already provides the
detach/reattach affordance via tmux itself — adding a bespoke PID-poll loop would
be new machinery for no new capability (`feedback_prefer_simpler_proposals`).

---

## Verdict Write-back & Gate Consumption

### Verdict derivation (FR-5) — from the contract, never recomputed

Read `<output>/return-contract.yaml` and map (first match wins):

| Condition (contract fields, SKILL.md §9.1) | `verdict` | exit code |
|---|---|---|
| contract missing / unparseable / subprocess `rc==30/launch-fail` | `error` | 30 |
| subprocess `rc==124` (timeout, process.py:165) | `error` (timeout) | 124 |
| `status: failed` | `fail` | 10 |
| `status: partial` | `partial` | 20 |
| any of `regression_present`, `unauthorized_deviation_present`, `needs_human_decision`, `user_decision_required`, `cannot_validate_without_user_input` == true | `fail` | 10 |
| `deviation_count_by_class.drift > 0` OR `.regression > 0` | `fail` | 10 |
| `status: success` AND none of the above | `pass` | 0 |

This mirrors reflect's own 9-condition promotion gate (SKILL.md §14.5.2) **by
reading its outputs**, not by re-implementing the gate. `pass` corresponds to "all
asymmetric-cost flags clear and no blocking deviations"; it does **not** itself
promote (that is reflect's gated Wave 7, opt-in via FR-9).

### Write-back (FR-6)

Replace the tasklist frontmatter `reflect_post:` block (the `PENDING`/`""` sentinel
at `task-builder/SKILL.md:1942`,`:1999`) with:

```yaml
reflect_post:
  verdict: pass | fail | partial | error
  status: success | partial | failed        # raw contract status
  run_id: <slug-or-output-dirname>
  report: <task-dir>/reflect/post/REPORT.md  # contract report_path
  contract: <task-dir>/reflect/post/return-contract.yaml
  deviations: { drift: N, regression: N, authorized: N, necessary: N }
  head: <HEAD sha at run time>               # enables FR-11 resume staleness check
```

Surgical YAML edit of the frontmatter only — no checklist/body mutation.

### Gate consumption (FR-7)

The tasklist completion-gate (the "Update status to Done" item) consumes **both**:

- **Exit code** (cheap path): the shelling Bash item branches on the wrapper's exit
  code. `0` → proceed to Done. Non-zero → STOP and surface `report`.
- **Contract block** (rich path): the Done item's verification reads
  `reflect_post.verdict == pass`. Any other value → HALT for human review, routing
  the `report` + `deviations` into the tasklist's `### Open Questions`
  (`feedback_human_decision_items_must_halt`). This mirrors the existing sprint
  executor routing of a `partial` reflect contract to `halt-phase-for-review`
  (SKILL.md §8) — the wrapper produces the *same* routing signal sprint already
  consumes, so the completion-gate semantics are not novel.

**No silent auto-proceed; no auto-commit** (success criteria #4-5): a non-`pass`
verdict always HALTs, and promotion is reflect's own gated mutation, never the
wrapper's.

---

## Resolved Open Questions

1. **Window mechanic** → **Blocking foreground `ClaudeProcess` by default; `--tmux`
   opt-in reusing sprint's detached-session+attach+sentinel; `--print-command`
   dry-run.** Foreground keeps the gate unattended and tmux-independent; `--tmux`
   reuses proven machinery for live viewing without a bespoke poller.

2. **Wrapper home** → **New `superclaude reflect run` Click subcommand under
   `src/superclaude/cli/reflect/`**, registered in `main.py` exactly like sprint /
   roadmap / prd (`main.py:400-434`). *Rationale:* discoverability (`superclaude
   reflect --help`), unit-testability (Click `CliRunner` + monkeypatched
   `ClaudeProcess`), packaging parity, and it sits beside the primitives it reuses.
   A `scripts/` entrypoint is lighter but un-discoverable, un-versioned, and would
   re-implement argument parsing the Click groups already standardize — net more
   surface, not less.

3. **Input derivation** → `--diff` from frontmatter `start_commit` else
   `git merge-base HEAD <integration>`; `--tasklist` = the passed path; `--spec`
   from frontmatter `spec_path`; `--depth` from **TCS floored at `standard`** (O4);
   `--executor-model` from frontmatter / env. All deterministic, all read from
   artifacts the task-builder already writes (`task-builder/SKILL.md:1996`,
   `:2114-2150`, `:1942`). The wrapper computes TCS by **calling the same FER
   extraction** the skill specifies — or, to stay maximally thin, accepts a
   pre-computed `--depth` baked into the tasklist item by task-builder (preferred:
   the builder already knows the TCS at generation time, so it bakes `--depth` into
   the item's wrapper command, and the wrapper treats `--depth` as a passthrough).

4. **Verdict write-back + gate consumption** → **Both** an exit-code contract
   (FR-7) **and** a parsed `reflect_post:` block (FR-6). Cheap path = exit code;
   rich/auditable path = contract block. Deviations route to `### Open Questions`
   and HALT (FR-8). See §"Verdict Write-back".

5. **Headless MCP/model parity** → **Inherit the operator's real HOME/env via bare
   `ClaudeProcess.build_env(env_vars=…)` overlay (process.py:97-112); do NOT use
   `HomeIsolation`.** The overlay only adds reflect-specific vars (e.g.
   `EXECUTOR_MODEL_CLASS`) and never overrides `HOME`/MCP/`ANTHROPIC_DEFAULT_*`.
   `HomeIsolation`'s hermetic mkdtemp HOME would strip exactly the MCP + alias
   config Tier-2 and grounding depend on — so the eval adapter is explicitly the
   *wrong* reuse here (see Architecture §"What the wrapper deliberately does NOT
   reuse").

6. **Runtime/timeout/budget** → default `--timeout 3600` (NFR-6), surfaced as the
   inherited `ClaudeProcess` timeout → exit `124` (process.py:162-165); `--max-turns`
   passthrough; re-run is idempotent at the frontmatter (FR-11) with optional
   `--resume` skipping a still-clean HEAD. No bespoke budget engine — reflect owns
   its own TurnLedger (SKILL.md §4 Wave 0.6).

7. **Template integration** → **Opt-in, reversible swap behind an existing
   config flag.** Add `POST_REFLECT_MODE: wrapper|halt` (default `halt`) to the
   BUILD_REQUEST contract; when `wrapper`, task-builder emits the *same penultimate
   item* but its **Action** shells to `superclaude reflect run {TASK_FILE}` (Bash,
   not Agent-tool) instead of printing the manual command. The HALT item text stays
   the default and byte-identical when the flag is unset (NFR-3). This is a minimal,
   reversible edit to `task-builder/SKILL.md:1994-1999` gated by config — it does
   **not** replace the HALT path wholesale.

8. **Promotion** → **Default `--no-promote` (audit-only).** The wrapper passes
   `--no-promote` to reflect unless an explicit `--promote` flag is given, in which
   case it passes reflect's own default-on promotion through (still gated by
   reflect's 9-condition Wave-7 gate, SKILL.md §14.5.2). The wrapper itself performs
   **no** filesystem mutation outside the tasklist frontmatter + `<output>/`.

---

## Scope Boundaries

**In scope:**
- A `superclaude reflect run <TASK_FILE>` Click subcommand that builds the
  invocation, launches a top-level `claude -p` via `ClaudeProcess`, parses the
  pinned `return-contract.yaml`, writes `reflect_post:` back, and exits on the
  FR-7 code contract.
- `--tmux` / `--print-command` / `--no-promote`(default) / `--promote` /
  `--timeout` / `--depth`(passthrough) / `--output` flags.
- The opt-in `POST_REFLECT_MODE: wrapper` task-builder template branch.

**Explicitly out of scope (HARD non-goals respected):**
- ❌ No `sc:cli-portify` of reflect; no Python port of waves/tiers/taxonomy/
  promotion-gate. Reflect stays the single source of truth (FR-2, NFR-1).
- ❌ Never run reflect inside an Agent-tool subagent (FR-1, NFR-7).
- ❌ No auto-commit; default audit-only (FR-9, OQ-8).
- ❌ No second behavioral copy of reflect logic that could drift.
- ❌ No new isolation/budget/poller machinery where `ClaudeProcess` + tmux +
  reflect's TurnLedger already suffice.

---

## Integration Plan (file touch-list)

| Action | Path | What |
|---|---|---|
| **Add** | `src/superclaude/cli/reflect/__init__.py` | `reflect_group` Click group + deferred-import export (mirror `sprint/__init__.py`). |
| **Add** | `src/superclaude/cli/reflect/commands.py` | `run` subcommand: option parsing, input derivation (FR-3), `--output` STOP-guard (FR-4), invocation assembly. |
| **Add** | `src/superclaude/cli/reflect/launcher.py` | Thin orchestration: build prompt `"/sc:reflect --mode post …"`, construct `ClaudeProcess` (FR-1, FR-10 env overlay), foreground `start()/wait()` or `--tmux` detached+sentinel (reuse tmux idiom). |
| **Add** | `src/superclaude/cli/reflect/contract.py` | `parse_return_contract()` + `derive_verdict()` (FR-5 table) + `write_back_frontmatter()` (FR-6, surgical YAML). |
| **Edit** | `src/superclaude/cli/main.py:434` (after `init-lite`) | `from superclaude.cli.reflect import reflect_group; main.add_command(reflect_group, name="reflect")`. |
| **Edit** | `src/superclaude/skills/task-builder/SKILL.md:1994-1999` + `:2108` checklist | Add `POST_REFLECT_MODE: wrapper` branch (OQ-7); default HALT text unchanged. |
| **Add** | `tests/cli/reflect/test_run.py` | `CliRunner` tests with monkeypatched `ClaudeProcess` (fixture contract YAMLs → verdict/exit-code/write-back assertions); a guard test asserting the item shells via Bash, not Agent-tool (NFR-7). |
| **Run** | — | `make sync-dev` → mirror to `.claude/`; `make verify-sync`; `uv run pytest tests/cli/reflect`; `uv run ruff format --check src/ tests/` (`reference_make_lint_vs_ci_ruff_format`). |

*No `.claude/` paths are staged (CLAUDE.md ABSOLUTE RULE); only `src/` is edited and
synced.*

---

## Risks

- **R-1 — Contract drift (1.3.0 → future).** The verdict map reads §9.1 fields by
  name. *Mitigation:* gate on `contract_version`; on an unrecognized major,
  `verdict: error` + surface (fail-loud), never guess. The map lives in one
  `contract.py` function so a version bump is a single localized edit.

- **R-2 — Headless MCP not actually present.** If the operator's `claude` lacks
  Serena/auggie registration, Tier-2 grounding degrades inside reflect (reflect
  fail-opens, SKILL.md §6.5) — the wrapper would report a `degraded` but `pass`
  verdict. *Mitigation:* surface reflect's `t2_model_class_diversity` /
  `degraded_components` in the one-line summary so degradation is visible; do not
  hide it behind `pass`.

- **R-3 — `--output` collision across re-runs.** Pinning `<task-dir>/reflect/post/`
  means a re-run overwrites prior artifacts. *Mitigation:* default to a
  HEAD-suffixed subdir `reflect/post/<short-sha>/` and write the latest path into
  `reflect_post.contract`; keep the bare `post/` symlink/pointer for the gate.

- **R-4 — Someone wires the item via Agent/Task tool** (re-introducing the nesting
  bug). *Mitigation:* the template Action explicitly says "Bash shell-out"; the
  guard test + a SKILL note (`reference_subagent_cannot_nest_skill_fanout`) document
  why; the wrapper is a CLI, so the natural call site is Bash.

- **R-5 — Long Tier-2 run hits timeout mid-merge.** *Mitigation:* default 3600 s
  (NFR-6); `124` is surfaced as `verdict: error`, leaving the prior `reflect_post`
  block intact and the gate HALTed — never a false `pass`.

- **R-6 — TCS recomputation drift between builder and wrapper.** If both compute
  TCS they could disagree. *Mitigation (OQ-3 preference):* the builder bakes the
  resolved `--depth` into the item command; the wrapper treats `--depth` as a pure
  passthrough — single producer, no drift.

- **R-7 — Parallel sessions sharing the git index** could race the frontmatter
  write. *Mitigation:* the write-back is a single surgical frontmatter edit; run the
  gate from the tasklist's own worktree (`feedback_parallel_sessions_share_index`).
