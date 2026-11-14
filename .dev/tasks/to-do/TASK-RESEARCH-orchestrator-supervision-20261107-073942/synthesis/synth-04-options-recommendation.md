# Synthesis 04: Options Analysis and Recommendation

**Research question context:** Orchestrator mode Phase 1 for issue #339 is a read-only, coordinator-only `/sc:sweep`. It classifies sessions as waiting on a person, working, stalled (proved), could not determine, finished, or idle: the research question's six. Section C adds fenced as a seventh class (`research/research-notes.md:188`); six versus seven is an open question (Section 9). Safe-to-close is a separate dimension. A default 6 h window bounds activity only. The sweep writes a dated static report on the #409 layout and adds a WC-14 coordinator-loop rule to `src/superclaude/core/WORKER-CONTRACT.md`. `/sc:close`, resume, the trust layer, an orchestrator of orchestrators and the management-server relay are later phases and are only recorded here.

**Inputs (all under `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/`):**

- `research/scope-01-contract.md`
- `research/scope-02-orca-recovery.md`
- `research/scope-03-cli-patterns.md`
- `research/scope-04-409-layout.md`
- `research/05-orca-row-schema.md`
- `research/06-orca-open-questions.md`
- `research/web-01-agent-supervisor-session-health.md`
- `research/web-02-static-status-report-conventions.md`
- `gaps-and-questions.md`
- `research/research-notes.md` SOLUTION_RESEARCH (`:147-229`)

The NB-4 fix is in effect (`qa/qa-nb4-fix-log.md`). The default Orca read allowlist (`research/scope-03-cli-patterns.md:99`) includes task-list, run-list, run-current and gate-list. `inbox` stays forbidden.

**Evidence labels:** [CODE-VERIFIED] means confirmed in code or captured output. [CODE-CONTRADICTED] means the claim is refuted by code. [UNVERIFIED] means documented or inferred but not proven; these claims are carried to Open Questions.

---

## 6. Options Analysis

### Constraints every option must meet

| # | Constraint | Source |
|---|---|---|
| K-1 | Read-only, and run by the coordinator only (the sweep goes on the never-as-worker list) | `seed-brief.md:53,57` via `research-notes.md:229`; `WORKER-CONTRACT.md:23`, `RULE_PHRASES["never-as-worker"]` / `NEVER_AS_WORKER` (`scope-01-contract.md`, `:245-254`) [CODE-VERIFIED] |
| K-2 | No new store; extend the contract instead | `seed-brief.md:54,56` via `research-notes.md:229` |
| K-3 | WC-10: a missing signal is never treated as death. Stalled requires positive proof only | `WORKER-CONTRACT.md:45` (`scope-01-contract.md`) [CODE-VERIFIED] |
| K-4 | Deterministic classification that can be tested with mocks | `seed-brief.md:62,68` via `research-notes.md:155-162` |
| K-5 | Every Orca call stays inside the read allowlist. Forbidden: `check` in any form by default, `--ack`, `--wait`, `--unread`, reply, ask, send, `inbox`, `--agent-wait` | `scope-03-cli-patterns.md:99` (NB-2 plus NB-4); `message-check-handler.js:17,:30,:33-34,:58-71` [CODE-VERIFIED] (`06-orca-open-questions.md` Q2) |
| K-6 | Report on the #409 DERIVED skeleton. The sweep must add its own sort and omission count, because the #409 code has neither | `scope-04-409-layout.md:268-304`; `agent_focus.py:46` [CODE-CONTRADICTED vs the #409 docs] |

### Option A1: Python CLI `superclaude sweep` plus a thin `/sc:sweep` command and `sc-sweep-protocol` skill

**Description:** All classification and probing lives in a new Python package under `src/superclaude/cli/`, which follows the `cli/reflect` split. The `/sc:sweep` command and the `sc-sweep-protocol` skill run `superclaude sweep`, read its JSON and write the dated report. The skill gathers no evidence itself (`research-notes.md:157`).

**How it works:**

```
/sc:sweep  (src/superclaude/commands/sweep.md, name: sweep)          [proposed]
   |  Skill call (blocking, per CLAUDE.md)
   v
sc-sweep-protocol  (src/superclaude/skills/sc-sweep-protocol/SKILL.md,
                    name: sc:sweep-protocol)                          [proposed]
   |  Bash: superclaude sweep ...          (PATH form first)
   |        uv run superclaude sweep ...   (dev checkout only; both in allowed-tools, B-19/NB-3)
   v
superclaude sweep  (Click group, two-line deferred import after main.py:561)
   |-- models.py          dataclasses
   |-- <pure classifier>  "No Click, no subprocess" (reflect/contract.py:7 pattern)
   |-- <probe module>     single _orca(*args) and _git(*args) seams,
   |                      timeout=10, fail-closed (reflect/config.py:64-78,103-109 pattern)
   `-- commands.py        JSON echo; "[sweep ...]" stderr prefix + sys.exit(1) on error
   |
   v  read-only sources (allowlisted argv only)
   orca-ide orchestration worker-list --run --include-remote --json (paged, page.nextCursor)
   orca-ide orchestration worker-show / worker-read
   orca-ide orchestration task-list --ready --run / run-list / run-current / gate-list
   orca-ide worktree ps --json (no --agent-wait)
   <report-dir>/return-contract.yaml, progress.md ledger
   git status / log / branch / rev-parse / stash list
   ccsession topics/*.txt and orca-tabs read as files (never ccsession --list)
   |
   v
skill renders the dated static report under .dev/ on the #409 DERIVED skeleton
```

Classification precedence, implemented in the pure module (`research-notes.md` Section C; `05-orca-row-schema.md:169-178`):

```
contract read (blocked -> waiting on a person)
  -> stalled (proved)        positive proof only, and no consumer_fenced evidence
  -> fenced                  (WC-12)
  -> waiting on a person     (a) non-null agentWait  (b) frozen plan / policy / foreign ready Task
  -> working
  -> finished                Orca outcome settled AND contract read
  -> could not determine     everything else
idle: person-started sessions only.  safe-to-close: separate REVIEW dimension.
Never inputs: resource.terminalState, projection.stage.activity
```

| Aspect | Assessment |
|---|---|
| Effort | **L**. New work: a package with four modules; a CliRunner test suite with the `_git` seam fixture (`tests/cli/reflect/conftest.py:58-80` pattern); a second `_orca` argv-allowlist test (B-13, `scope-03-cli-patterns.md:99`); a read-only proof test (`test_contract_status_cli.py:44-66` pattern); the registry entries listed under Files/systems affected; and the WC-14 text with its `RULE_PHRASES` pin |
| Risk | **Medium-low.** Read-only is provable: AssertionError side effects run inside `isolated_filesystem`, and the argv allowlist is asserted at one seam. Open risks: (1) the bare PATH form under pipx is [UNVERIFIED] (GQ-25, `scope-03-cli-patterns.md:208`); (2) `make lint` lint-architecture check 11 means contract constants must be imported from `superclaude.contracts` and never re-declared (`Makefile:362-489`); (3) it departs from the sc-issue "No CLI" decision (`docs/designs/sc-issue-command.md:384`) |
| Reuse of existing code | `cli/reflect` module split (`reflect/contract.py:7,:397`; `reflect/config.py:64-78,103-109`) [CODE-VERIFIED]. Test fixtures and read-only proof (`tests/cli/reflect/conftest.py:58-80`; `test_contract_status_cli.py:44-66`) [CODE-VERIFIED]. Imports `superclaude.contracts` constants directly. Skill-calls-CLI precedent: `sc-reflect-protocol/SKILL.md:63-64` calls `superclaude reflect contract-status`. Allowed-tools precedent: `sc-swarm-wizard-protocol/SKILL.md:7`. From crash-recovery it reuses only the report shape and vocabulary, not its scripts: SAFE/REVIEW (`sc-crash-recovery/SKILL.md:91,93-97`), "What I could not determine" with `unscanned:` markers (`:139-150`; `report-template.md:127-129`), the conflicts section (`:120-125`) and the running-pipeline guard (`:137`). The transcript reader re-implements a tailing variant of `parse_session_log.py`, which today reads the whole file (`scope-02-orca-recovery.md`) |
| Files/systems affected | **New:** `src/superclaude/cli/sweep/` package; `src/superclaude/commands/sweep.md`; `src/superclaude/skills/sc-sweep-protocol/SKILL.md`; tests under `tests/sweep/` (optional `tests/sweep/test_cli_registration.py`) and `tests/commands/test_sweep_command.py` (optional), per `scope-03-cli-patterns.md`. **Edited:** `src/superclaude/cli/main.py` (after `:561`, before the `__main__` guard at `:564-565`); `src/superclaude/core/WORKER-CONTRACT.md` (`:23` never-as-worker list; WC-14 after `:156` or `:129`); `tests/skills/test_worker_contract.py` `RULE_PHRASES` / `NEVER_AS_WORKER` (`:163`, `:245-254`); `_POST_REFRESH_ADDITIONS` (`tests/recommend/test_routing_refresh.py:33`, asserted `:647-648`); `src/superclaude/core/HOW-WE-WORK.md` "Other commands" (`:314-337`) plus `_OTHER_COMMANDS` (`tests/core/test_how_we_work_routing_table.py:27-40,291-311`); plugin byte copy (`tests/commands/test_routing_plugin_parity.py:38`); `docs/user-guide/commands.md:105` UTILITIES table (whether a test pins it is [UNVERIFIED]). **Suite scans the new files must pass:** `test_model_alias_policy.py:81-100`, `test_graph_command.py:219-225`, the write-verb audit (`test_worker_contract.py:1090-1094`), `_check_no_unattended_sections` |
| Pros | Deterministic and mock-testable, as K-4 requires. Matches the house CLI pattern used by reflect and recommend. The single `_orca` seam is the natural home for the B-13 argv-allowlist test. Paging and one worker-show per row run in one process, not one model round trip per call (`research-notes.md:157`; batching policy). It can import contract constants (lint check 11). JSON output is reusable by later phases (`/sc:close`, resume) without re-parsing prose |
| Cons | Largest registry footprint: CLI registration plus routing and parity tests. The pipx PATH form is [UNVERIFIED]. It goes against the newest command precedent (sc-issue chose "No CLI", `docs/designs/sc-issue-command.md:384`). The lazy-vs-eager package init is still undecided (GQ-23: `recommend/__init__.py:12-20` lazy vs `reflect/__init__.py:17-30` eager) |

### Option A2: Skill only (shell commands from the skill)

**Description:** `/sc:sweep` plus `sc-sweep-protocol` and no Python code. The skill calls each `orca-ide` verb, each git read and each file read through its own Bash or Read tool calls, and the model applies the Section C classification rules from the skill text. sc-crash-recovery is the precedent (`research-notes.md:158`).

**How it works:**

```
/sc:sweep -> sc-sweep-protocol/SKILL.md   (allowed-tools lists each read form)
   |
   |  model loop, one tool call per probe:
   |    Bash  orca-ide orchestration worker-list ... (repeat per page)
   |    Bash  orca-ide orchestration worker-show --dispatch <id>   (x N rows)
   |    Bash  git status / log ... per worktree
   |    Read  return-contract.yaml, progress.md per worktree
   v
model applies the Section C precedence in prose, then writes the report
```

| Aspect | Assessment |
|---|---|
| Effort | **M**. No package and no CLI registration. It still needs the command, the skill, the WORKER-CONTRACT never-as-worker and WC-14 edits with their `RULE_PHRASES` pin, the HOW-WE-WORK and plugin-parity registry entries, and the suite scans listed for A1 |
| Risk | **High.** (1) Classification is done by the model, is not deterministic and cannot be unit-tested with mocks, which breaks K-4 (`seed-brief.md:68`, `research-notes.md:158`). (2) Read-only rests only on the allowed-tools patterns. The direct precedent fails that test: `sc-crash-recovery/SKILL.md:4` allows `Bash(git stash *)` while `:13`/`:155` claim "pure read-only" (C3, S-08) [CODE-CONTRADICTED]. (3) The argv allowlist (K-5) can't be asserted at a seam; only glob patterns in allowed-tools constrain it. (4) Cost: worst case is ceil(N/100) worker-list calls plus N worker-show calls (`05-orca-row-schema.md:165`), and each one is a model round trip. Five or more serial known inspections fall under the batching policy, which moves them into a generated `/tmp` script. That script is an unreviewed classifier with no tests |
| Reuse of existing code | Skill shape, report template and SAFE/REVIEW vocabulary from `sc-crash-recovery` (`SKILL.md:91,93-97,:120-125,:139-150`; `report-template.md:127-129`). Allowed-tools precedent `sc-swarm-wizard-protocol/SKILL.md:7`. It cannot import `superclaude.contracts` constants, so it repeats them as prose |
| Files/systems affected | **New:** `src/superclaude/commands/sweep.md`; `src/superclaude/skills/sc-sweep-protocol/SKILL.md` (plus `refs/`). **Edited:** `src/superclaude/core/WORKER-CONTRACT.md`; `tests/skills/test_worker_contract.py`; `src/superclaude/core/HOW-WE-WORK.md` with `tests/core/test_how_we_work_routing_table.py`; `tests/recommend/test_routing_refresh.py`; `tests/commands/test_routing_plugin_parity.py`; `docs/user-guide/commands.md:105` |
| Pros | Cheapest to write. No Python package, no CLI registry entry, no pipx PATH question. Matches crash-recovery, the skill closest in purpose |
| Cons | Fails K-4, the seed brief's mock-testable requirement. The read-only and allowlist guarantees are weaker. It scales poorly with session count. Repeated sweeps can classify the same evidence differently, which defeats a status report. Its only precedent is the skill whose read-only claim is [CODE-CONTRADICTED] |

### Option A3: Skill plus a skill-local standard-library script (sc-issue precedent)

**Description:** `/sc:sweep` plus `sc-sweep-protocol`, with the classifier and probes in a standard-library Python script under `src/superclaude/skills/sc-sweep-protocol/scripts/`. The script is installed to `~/.claude/skills/sc-sweep-protocol/scripts/` and run by the skill. The script layout follows `docs/designs/sc-issue-command.md:355-363`: SKILL.md under 500 lines, `refs/`, and `scripts/*.py` in the standard library only, tested directly (`:362-363,:395-396`).

**How it works:**

```
/sc:sweep -> sc-sweep-protocol/SKILL.md
   |  Bash: python3 ~/.claude/skills/sc-sweep-protocol/scripts/<sweep script> --json
   |        (.claude/skills/... copy in a dev checkout; dual-surface rule)
   v
<sweep script>  (stdlib only; cannot import superclaude.*)
   |-- hand-rolled subprocess seam for orca-ide / git   (no _git helper to reuse)
   |-- classifier functions (Section C precedence)
   v
JSON -> skill writes the dated report
tests: import the script through a sys.path shim from the skill directory
```

| Aspect | Assessment |
|---|---|
| Effort | **M-L**. The classifier, paging, the argv-allowlist test and the read-only proof are the same work as in A1. It saves the CLI registration (`main.py:561`), but adds a test path shim and a hand-rolled subprocess seam. The registry edits are the same as A2 |
| Risk | **Medium.** Deterministic and testable, so it meets K-4. (1) The script cannot import package code (`research-notes.md:159`), so contract constants and vocabulary are copied. Whether lint-architecture check 11 (`Makefile:362-489`) scans skill scripts is [UNVERIFIED]; if it does not, the copies can drift silently from `superclaude.contracts`. (2) It runs from `~/.claude/skills/...`, which depends on the install copy and sync-dev being current. (3) The `_orca`/`_git` seam must be hand-rolled, with no `reflect/config.py` timeout and fail-closed pattern to inherit. (4) Interpreter choice: CLAUDE.md requires `uv run` for Python, and how a skill-local script is invoked outside a uv project is not settled by any research file [UNVERIFIED] |
| Reuse of existing code | sc-issue layout and testing approach (`docs/designs/sc-issue-command.md:355-363,:395-396`). Crash-recovery report shape and vocabulary, as in A1. It can't reuse the `cli/reflect` fixtures (`tests/cli/reflect/conftest.py:58-80`) or `superclaude.contracts` |
| Files/systems affected | **New:** `src/superclaude/commands/sweep.md`; `src/superclaude/skills/sc-sweep-protocol/SKILL.md`, `refs/`, `scripts/<sweep script>.py`; tests with a path shim. **Edited:** the same registry and contract files as A2 (`src/superclaude/core/WORKER-CONTRACT.md`, `tests/skills/test_worker_contract.py`, `src/superclaude/core/HOW-WE-WORK.md`, `tests/core/test_how_we_work_routing_table.py`, `tests/recommend/test_routing_refresh.py`, `tests/commands/test_routing_plugin_parity.py`) |
| Pros | Testable and deterministic. No CLI registration. Matches the newest command precedent, sc-issue's "No CLI" (`docs/designs/sc-issue-command.md:384`). Ships inside the skill, so `superclaude` does not have to be on PATH, which avoids the pipx PATH question |
| Cons | No package imports, so constants are duplicated and can drift. A test path shim is needed. The seam is hand-rolled. The python3 vs `uv run` invocation is unsettled. Later phases (`/sc:close`, resume) would need their own scripts or would read this one's JSON. There is no shared module to extend |

### Option A4: Extend sc-crash-recovery (REJECTED, [CODE-CONTRADICTED])

**Description:** Add sweep behaviour to `src/superclaude/skills/sc-crash-recovery/`, reusing its investigators, `scripts/bootstrap_scan.sh` and its report template (`research-notes.md:160`).

**How it would work:** `/sc:crash-recovery --all`, or a new mode, would run `bootstrap_scan.sh` over the worktree root and fan out to investigators, then fill `report-template.md`.

**Why it is rejected.** Each reason below is a code fact that contradicts the claims the option relies on:

| # | Claim the option relies on | What the code shows | Evidence |
|---|---|---|---|
| R-1 | crash-recovery is read-only | allowed-tools includes `Bash(git stash *)`, and `:4` names a script under `~/workspace/IronClaude`. The "pure read-only, enforced by allowed-tools" claim at `:13`/`:155` is false | `sc-crash-recovery/SKILL.md:4,:13,:155` (C3, S-08, GQ-21) [CODE-CONTRADICTED] |
| R-2 | It scans where the worktrees are | It hardcodes `~/workspace/...` with a 72 h default. This host uses `~/workspaces/...`, and the sweep needs a 6 h activity window | `SKILL.md:25-27,:53` (C4, S-09) [CODE-CONTRADICTED] |
| R-3 | `bootstrap_scan.sh` finds Orca worktrees | It mis-encodes paths (`:31`), treats `.git` as a directory and so skips worktrees whose `.git` is a file (`:73`), and builds JSON by hand without escaping (`:136`) | `scope-02-orca-recovery.md` Q6 `:228`; K2/GQ-19 [CODE-VERIFIED bugs] |
| R-4 | Recovery and supervision fit one skill | Crash recovery is a post-crash, person-run tool. The sweep is coordinator-only (K-1) and goes on the never-as-worker list. Merging them mixes the two trigger models | `research-notes.md:160`; `WORKER-CONTRACT.md:23` |

| Aspect | Assessment |
|---|---|
| Effort | **M** to adapt, plus fixes to R-1 to R-3 that change crash-recovery for its existing users |
| Risk | **High.** Every read-only and path assumption is contradicted (R-1 to R-3) |
| Reuse of existing code | High on paper. In practice only the report shape and SAFE/REVIEW vocabulary are safe to reuse, and A1, A2 and A3 already take those without the scripts |
| Files/systems affected | `src/superclaude/skills/sc-crash-recovery/SKILL.md`, `scripts/bootstrap_scan.sh`, `report-template.md`, plus the contract and registry files |
| Pros | Investigators and report template already exist |
| Cons | Not read-only (R-1). Wrong root and window (R-2). Broken worktree scan (R-3). Mixes concerns (R-4) |

A4 is excluded from the comparison below. What it would have reused (the report shape, SAFE/REVIEW, "What I could not determine", the running-pipeline guard) is carried into every remaining option as text, not as scripts.

### Options Comparison

| Criterion | Option A1 (CLI + thin skill) | Option A2 (skill only) | Option A3 (skill + local script) |
|---|---|---|---|
| Effort | L: package, CLI registration, tests, registries | M: skill text and registries only | M-L: same classifier and tests as A1; no CLI registration; adds a path shim and a hand-rolled seam |
| Risk | Medium-low: read-only and argv allowlist provable at one seam. Open: pipx PATH form [UNVERIFIED] | High: not deterministic, fails K-4, allowlist enforced only by allowed-tools globs, one round trip per probe | Medium: testable, but constants are copied with no import and lint check 11 coverage is [UNVERIFIED]; interpreter invocation unsettled |
| Maintainability | High: pure classifier split from the single probe module (reflect pattern); imports `superclaude.contracts` | Low: rules live in prose and drift goes undetected by tests | Medium: tested, but duplicated vocabulary and constants must be kept in sync by hand |
| Integration complexity | Highest registry count: `main.py`, routing tests, HOW-WE-WORK, plugin parity, contract pins. All are known, test-pinned paths | Lowest: command and skill plus the shared registries | Medium: shared registries plus install-path dependency (`~/.claude/skills/...` vs `.claude/skills/...` dual surface) |
| Reuse potential | High: JSON CLI and modules can be imported by later phases (`/sc:close`, resume) and by other CLI groups | Low: nothing callable is produced | Medium: script JSON is reusable; the code cannot be imported by package code |
| Meets K-1..K-6 | All, with K-4 and K-5 enforced by tests | Fails K-4; K-5 weak | All, with K-4 and K-5 by tests; contract constants duplicated (against the intent of lint check 11) |

---

## 7. Recommendation

**Recommended option: A1.** It is a Python CLI `superclaude sweep` with a pure classifier and one probe module, called by a thin `/sc:sweep` command and the `sc-sweep-protocol` skill. It reuses crash-recovery's report shape and SAFE/REVIEW vocabulary, but not its scripts.

### Rationale (from the comparison)

| Deciding criterion | Why A1 wins on it | Runner-up and gap |
|---|---|---|
| K-4 mock-testable (hard requirement) | Same reflect pattern already proven: CliRunner, single `_git` seam, read-only proof in `isolated_filesystem` (`tests/cli/reflect/conftest.py:58-80`; `tests/cli/reflect/test_contract_status_cli.py:44-66`) [CODE-VERIFIED] | A3 also meets it, at the cost of a path shim. A2 fails it and is out |
| K-5 argv allowlist (read-only safety) | One `_orca(*args)` seam, so a single test can assert every argv against the NB-4 allowlist (`scope-03-cli-patterns.md:99`) | A3 can do the same, but the seam is hand-rolled |
| Risk | Medium-low. The only open runtime item is the pipx PATH form (GQ-25), and it has a dev-checkout fallback already in allowed-tools | A3 is Medium because constants are copied with no import |
| Maintainability | Imports `superclaude.contracts` (lint check 11). The classifier is pure and separate from probes | A3 duplicates vocabulary and constants |
| Reuse potential | Later phases (`/sc:close`, resume) get an importable module and a JSON CLI | A3 offers only script JSON |

**Trade-offs accepted:**

| Trade-off | Accepted because | Mitigation |
|---|---|---|
| Highest effort (L) and registry count | Every registry is a known, test-pinned path. Effort over A3 is mostly registration, not logic | Follow the scope-03 checklist: `main.py:561`; `tests/recommend/test_routing_refresh.py:33`; `tests/core/test_how_we_work_routing_table.py:27-40`; `tests/commands/test_routing_plugin_parity.py:38` |
| Departs from sc-issue "No CLI" (`docs/designs/sc-issue-command.md:384`) | sc-issue has no Orca probe surface needing an argv allowlist or contract-constant imports. The sweep needs both (K-5, lint check 11) | Record the departure and its reason in the plan |
| pipx PATH form [UNVERIFIED] | The decision is already made (B-19/NB-3: PATH first, `uv run` in a dev checkout, both in allowed-tools) | Run `superclaude sweep --help` once outside a uv project before release (GQ-25) |

**Contradictions this choice depends on, with the stronger evidence:**

| # | Conflict | Stronger evidence | Effect on A1 |
|---|---|---|---|
| X-1 | crash-recovery says "pure read-only" (`SKILL.md:13,:155`), but `Bash(git stash *)` is allowed (`:4`) | Code (`:4`) [CODE-CONTRADICTED claim] | A1 reuses no crash-recovery scripts or allowed-tools. Its git list allows `stash list` only |
| X-2 | `~/workspace` in crash-recovery vs `~/workspaces` on this host (C4) | Host layout | A1 takes worktree paths from Orca and git, not from a hardcoded root |
| X-3 | sc-issue "No CLI" vs A1's CLI | Not a factual conflict. A design choice, decided by K-4/K-5 above | See trade-offs |
| X-4 | Help: null `agentWait` = "looked, found no wait". Guide: null = "absence seen again" (`06-orca-open-questions.md` Gap 19) | Open. The help is code-verified text; the guide's reading is the safer one for stop decisions | The classifier uses the split rule: null is valid input for working but never stall proof, and absent means could not determine |
| X-5 | `scope-03-cli-patterns.md:99` writes bare `worker-list`; C13 requires `orca-ide orchestration <verb>` | C13 (`research-notes.md:331`) | The allowlist test asserts the full `orca-ide orchestration <verb>` argv |
| X-6 | Resolved, not a live conflict: `gaps-and-questions.md:125` reads "Open: 75. Resolved: 25" with GQ-03 counted as resolved | `gaps-and-questions.md:125` | None on the option choice |

### Implementation steps (for the later `/sc:workflow` plan; all files as named in research)

| Step | Work | Files |
|---|---|---|
| 1 | Package: models; pure classifier (Section C precedence, no Click, no subprocess); probe module with `_orca`/`_git` (timeout 10, fail-closed); Click commands with JSON output and error prefix | `src/superclaude/cli/sweep/` (new) |
| 2 | Register the group with a two-line deferred import | `src/superclaude/cli/main.py` (after `:561`, before `:564-565`) |
| 3 | Tests: classifier unit tests; `_git` seam fixture; `_orca` argv-allowlist test (allowlist plus forbidden list, K-5); read-only proof | `tests/sweep/` (new), patterned on `tests/cli/reflect/conftest.py`, `tests/cli/reflect/test_contract_status_cli.py` |
| 4 | Command and skill. The skill calls `superclaude sweep` (PATH form, then `uv run` form) and renders the #409 DERIVED skeleton, with its own sort and `shown/total` counts (K-6) | `src/superclaude/commands/sweep.md`, `src/superclaude/skills/sc-sweep-protocol/SKILL.md` (new) |
| 5 | Contract: add `/sc:sweep` to never-as-worker, add the WC-14 coordinator-loop rule (no runnable code spans, repo-setup gate `:446`), and pin both | `src/superclaude/core/WORKER-CONTRACT.md` (`:23`; after `:156` or `:129`); `tests/skills/test_worker_contract.py` (`:163`, `:245-254`) |
| 6 | Registries and docs | `tests/recommend/test_routing_refresh.py:33`; `src/superclaude/core/HOW-WE-WORK.md:314-337` + `tests/core/test_how_we_work_routing_table.py`; plugin copy + `tests/commands/test_routing_plugin_parity.py:38`; `docs/user-guide/commands.md:105` |
| 7 | Gates: `make lint` (lint-architecture checks 1, 2, 3/4, 6, 8, 9, 11), `make sync-dev`, `make verify-sync`, `uv run pytest` | `Makefile:362-489` |

### External context (option-neutral)

These web findings shape the vocabulary and report rules that every option would implement. They do not separate A1 from A3.

| Finding | Source (external context) | Applies as |
|---|---|---|
| "Unknown" is a first-class state, separate from unhealthy | https://kubernetes.io/docs/reference/node/node-status/ ; https://github.com/grpc/grpc-proto/blob/master/grpc/health/v1/health.proto ; https://nagios-plugins.org/doc/guidelines.html | "could not determine" stays its own class. The cause is split between evidence absent and a source unreadable (web-01 rec. 1) |
| Act on positive exit proof, never on silence | https://www.erlang.org/doc/system/sup_princ.html ; https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/ ; https://nightlies.apache.org/pekko/docs/pekko/1.1.3/docs/typed/failure-detector.html | Supports WC-10. Heartbeat or progress age is a note column only, never a class (web-01 rec. 2) |
| Waiting for a person is healthy and is excluded from time budgets | https://docs.camunda.io/docs/next/components/agentic-orchestration/evaluate-agents/detect-off-rail-agents/ | Person-wait time is excluded from the 6 h activity window (web-01 rec. 4) |
| Oldest first; unknown age goes in a labelled group | https://kanbanguides.org/the-kanban-guide/2025.5/pdf/kanban-guide.v2025.5.en.pdf | The sweep's own sort (K-6) |
| `shown/total`; "at least N, truncated" when the total is unknown | https://github.com/cli/cli/issues/12196 | Extends #409, which has no unknown-total form |
| Grafana's no-data-as-OK mapping | (web-02 finding 2) | Rejected, because it conflicts with WC-10 |
| Restart, kill, evict and retry patterns | web-01 finding 7, rec. 5 | Later phases only, not Phase 1 |

## Open Questions (UNVERIFIED items that affect the option or its build)

| # | Question | Source | Blocks |
|---|---|---|---|
| OQ-1 | Does the bare `superclaude sweep` PATH form work under a pipx install? | GQ-25; `scope-03-cli-patterns.md:208` | Release check only |
| OQ-2 | Lazy (`recommend/__init__.py:12-20`) or eager (`reflect/__init__.py:17-30`) package init? | GQ-23, K4 | Step 1 detail |
| OQ-3 | What does a populated worker-list row carry? Until it is captured, plan for ceil(N/100) list calls plus N worker-show calls | `05-orca-row-schema.md:186`; G-A, C10 | Probe cost, not the option |
| OQ-4 | Is there a non-consuming question read? Today: Orca question enumeration is "could not determine", and the header states partial message coverage | `06-orca-open-questions.md` Gaps 17-18; G-B, C11 | The sweep stays on the contracts-only fallback |
| OQ-5 | Does the `--agent-wait` / `agentWait` probe send anything to the agent's terminal? | `06-orca-open-questions.md` Gap 10 | `--agent-wait` stays excluded |
| OQ-6 | Is the `docs/user-guide/commands.md:105` UTILITIES table test-pinned? | `scope-03-cli-patterns.md` | Step 6 |
| OQ-7 | How do command-level and skill-level allowed-tools combine? | `scope-03-cli-patterns.md` OQ | Step 4 |
| OQ-8 | Does `inbox` mark rows read at runtime? | `06-orca-open-questions.md` Gap 4 | `inbox` stays forbidden |
| OQ-9 | `gate-list` status to Approval mapping | GQ-34; `scope-04-409-layout.md:345` | Report column only |
| OQ-10 | Fix `bootstrap_scan.sh` or write a new scanner? (A1 writes its own probes; this concerns crash-recovery only) | GQ-19, K2 | Not A1 |

## Coverage and exclusions

| Input | Key findings reflected | Excluded here, and why |
|---|---|---|
| `scope-01-contract.md` | Never-as-worker list, WC-10, WC-14 placement and pinning, repo-setup gate | WC-3/6/8/9/12/13 rule text and G1-G7 gap detail belong to the contract synthesis section, not the option choice |
| `scope-02-orca-recovery.md` | Crash-recovery reuse limits, bootstrap bugs, the `parse_session_log.py` tail change | Orca failure-mode handling (`runtime_unavailable` banner, `source_changed` restart) applies to every option equally |
| `scope-03-cli-patterns.md` | Module split, registration, seams, allowlist, registries, lint, open questions | None |
| `scope-04-409-layout.md` | DERIVED skeleton, missing sort and omission count, partial message coverage | Field names and buckets are not fixed and do not separate the options |
| `05-orca-row-schema.md` | Worst-case cost, Section C Orca half, no `terminalState` or `stage.activity` | Liveness reason codes (guide-only, [UNVERIFIED]) |
| `06-orca-open-questions.md` | `check` is a mutation call, `--unread` forbidden, `inbox` unused, `--agent-wait` excluded, null vs absent `agentWait` | Peer-session `reference find` detail is option-neutral |
| `web-01`, `web-02` | External context table above | None |
| `gaps-and-questions.md` | GQ-03 (resolved), GQ-19, GQ-21, GQ-23, GQ-25, GQ-34, GQ-60, K2-K4, C3/C4, S-08/S-09 | Rows unrelated to where the logic lives |
| `research-notes.md` SOLUTION_RESEARCH | A1-A4 table, B/C/D data, provisional recommendation `:227`, constraint alignment `:229` | None |
