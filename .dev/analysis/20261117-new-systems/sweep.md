# The read-only Orca session sweep (`superclaude sweep`, `/sc:sweep`)

Date: 2026-11-17. Source: origin/master, read with `git show`. graph:stale (codegraph not used).

## 1. What it is
The sweep is a status report for people and coordinator sessions who run AI worker sessions in Orca (the local app that runs Claude sessions in separate git worktrees). One command reads Orca's records, the git state of each worktree, Claude Code transcripts and the ccsession tab files. It then sorts every session into one of eight classes (working, waiting on a person, finished, idle and so on), and writes one dated Markdown report plus prints one JSON summary. It changes nothing except that one report file, and it never recommends an action. Where it cannot prove something it says "could not determine" and lists what it could not read.

- PRs: #539 (feat, merged 2026-11-14 17:41 UTC, Phase 1 of orchestrator mode, issue 339). #579 (fix, merged 2026-11-17 00:29 UTC, restores the `working` class with the real Orca field names).
- Entry points:
  - CLI: `superclaude sweep run [--run <id>]... [--window <N>h|<N>d] [--root <dir>] [--output <dir>]` (registered in `src/superclaude/cli/main.py:571-573` on origin/master).
  - Command: `src/superclaude/commands/sweep.md` (`/sc:sweep`, allowed-tools `Skill` only).
  - Skill: `src/superclaude/skills/sc-sweep-protocol/SKILL.md`.
  - Package: `src/superclaude/cli/sweep/` (`commands.py`, `probes.py`, `classify.py`, `report.py`, `models.py`).
  - Tests: `tests/sweep/` (7 test files, 20 captured JSON fixtures) and `tests/commands/test_sweep_command.py`. PR #579 reports 649 passing in `tests/sweep` (PR body, not re-run here).
  - Rule text: WC-16 "Coordinator loop" in `src/superclaude/core/WORKER-CONTRACT.md:286`, routing rows in `src/superclaude/core/HOW-WE-WORK.md:335` and `:406`.
  - Design: `docs/designs/orchestrator-mode.md` and `-review-1/2/3.md`.

## 2. How it works
### 2.1 Data flow

```
sweep run (commands.py)
  check args -> bind Run (orca run-current) -> collect (probes) -> classify_all (pure) -> render (pure) -> _publish (the one write) -> print JSON
```

`commands.py:246-277` runs these stages in that order and tags failures with `[sweep <stage>]`. Exit 0 means the report was published, 1 is an internal error, 2 is a usage error (`commands.py:1-9`). `--window` is `<N>h` or `<N>d`, 1 to 9999, at most 720h or 30d, default 6h (`commands.py:27-52`). With no `--run` it uses the Run bound to the terminal; with none bound it exits 2 and asks for `--run <id>` (`probes.py:397-407`).

### 2.2 What the probes read (probes.py)

| Source | How | Used for |
|---|---|---|
| Orca `run-current`, `worker-list`, `worker-show`, `task-list` (ready and all), `worktree ps` | allowlisted `orca-ide` verbs, JSON | Dispatch rows, liveness, outcome, agent wait, ready Tasks, worktree paths (`probes.py:1114-1192`, `1322-1360`) |
| `git status` per worktree | one allowlisted call plus three config checks | uncommitted, unpushed, unsaved `.dev/tasks/` paths (`probes.py:1021-1048`) |
| `.dev/tasks/{to-do,done}/<pkg>/progress.md` and `.archiving` | file reads | package state (unfinished, archive-blocked, conflict, ...) (`probes.py:655-710`) |
| `return-contract.yaml` named in a Task brief | `yaml.safe_load`, max 1 MiB | worker status (blocked, failed, succeeded) (`probes.py:722-778`) |
| `~/.claude/projects/<key>/*.jsonl` | last 256 KiB, first partial line dropped | session id, last activity (`probes.py:786-867`, `1445-1476`) |
| `~/.local/state/ccsession/orca-tabs/*` | 3-line files | join Orca terminal handle to Claude session id (`probes.py:870-895`) |

Contract files are found only through paths or `--report-dir` values written in the Task brief text, and only if they resolve inside a known worktree (`probes.py:1092-1105`, `1399-1442`).

### 2.3 Why it is read-only (evidence)

- Orca argv must equal one of 10 templates (7 verbs); ids must match `run_[0-9a-f]{12}` or `ctx_[0-9a-f]{12}`; `--include-remote` is rejected anywhere; the binary is `orca-ide`, never bare `orca` (`probes.py:43-62`, `226-238`). None of the verbs is a write verb; two `--agent-wait` forms and `worktree list/current` are allowed but not called in Phase 1 (`probes.py:56-59`).
- git argv must equal one of 4 exact tuples and is always prefixed with `--no-optional-locks -C <path> -c core.fsmonitor=false`, with `GIT_OPTIONAL_LOCKS=0` in the environment (`probes.py:68-81`, `315-358`). Before `git status`, three read calls check whether a configured git filter (clean or process) could run a program on a tracked path; if so the worktree is reported unscanned instead of risking it (`probes.py:967-1048`; this is the INV-008 fix named in open-decisions.md).
- Disk readers check the real path stays under the root (`_check_inside`), cap sizes, and retry once if file size or mtime changed during the read, else mark a conflict (`probes.py:572-604`).
- Subprocesses use `stdin=DEVNULL`, a 10 s per-call timeout, an 8 MiB output limit (checked after exit, a known shortcut noted in code at `probes.py:270-273`) and a 90 s total budget with a 50-show cap shared across Runs (`probes.py:85-89`, `124-208`).
- The only write is `_publish`: temp file with `O_EXCL`, then `os.link` to the first free name `<UTC stamp>-sweep.md` (suffix `-2` to `-99`), which cannot overwrite; output must be under `<root>/.dev/sweeps/` and must not overlap the folders the sweep reads (`commands.py:99-123`, `153-208`).
- `report.sanitize` strips terminal escape codes, control and bidi characters and neutralises `|`, `<`, `[` and backslashes so untrusted text in a brief or contract cannot forge table cells or links (`report.py:569-605`). The skill also says report text is data, not instructions (SKILL.md Boundaries).

### 2.4 How it classifies (classify.py)

Joins first. Orca rows are merged by Dispatch id (differing duplicates are flagged as a conflict, `classify.py:512-545`). A transcript is joined to a Dispatch by the tab-map: Orca's `dispatch.assigneeHandle` is matched to the tab-map terminal handle ("path B", `classify.py:38-40`, `609-683`), with a time-window check so a pane reused by a person later is not attributed to the worker (`classify.py:548-558`, `629-653`). A transcript with no Orca row is a person session; `person_started` is `True` only if no list-incompleteness guard fires (`classify.py:690-779`). Otherwise it is `None`.

Then the first matching rule wins (`classify.py:345-355`):

| # | Rule | Class | Condition (short) |
|---|---|---|---|
| 1 | blocked_contract | waiting on a person (a) | contract `worker_status: blocked` and Orca row settled, or policy "report blocked", or a Ruling halt code (`E-HALT-QA`, `E-NO-RULING`) (`classify.py:161-188`) |
| 2 | orca_exit_proof | stalled (proved) | Orca liveness `exited`, worker_done not seen, no fencing evidence (`classify.py:191-208`) |
| 3 | fenced | fenced | fenced evidence present (`classify.py:219-223`) |
| 4 | waiting_signal | waiting on a person (a or b) | non-null `agentWait`; or failed contract with a STOP code (frozen plan); or a ready Task with no observable creator (`classify.py:226-248`) |
| 5 | working | working | liveness `live`, outcome `in_progress`, `agentWait` present and null (`classify.py:251-269`) |
| 6 | finished | finished | brief body starts with `guard refused:`, or settled outcome plus a parsed contract with settled status (`classify.py:272-292`) |
| 7 | idle | idle | person session, transcript readable, last activity before the window start (`classify.py:295-311`) |
| 8 | person_active | person session (active) | person session, last activity inside the window (`classify.py:314-327`) |
| 9 | fallback | could not determine | nothing above matched (`classify.py:330-342`) |

After the walk: a worker with a `parent` gets the note "WC-13 violation, review"; an unreadable transcript, a duplicate-Dispatch conflict, or a join problem forces the class to "could not determine" while keeping the evidence (`classify.py:369-386`, `358-366`). So the class set only claims what an observed field proves. PR #579 fixed rule 5: it had tested `dispatch.status == in_progress`, but a running worker has status `dispatched` and `projection.outcome in_progress`, so nothing could ever be "working" (PR #579 body; current code above).

Policy and removal: `policy_of` marks a row "frozen" (failed or blocked with a STOP code, or a blocked `sc:implement`) and a worktree hosting a frozen row is not removable (`classify.py:389-401`, `455-476`). Worktrees get `removable` of `no` (with first blocking reason) or `could not determine`, never `yes`. `Safe to close` likewise never prints `yes` in Phase 1 (`classify.py:479-504`, `report.py:46-49`).

### 2.5 Outputs

- Markdown report with sections in this order: header, source coverage, waiting on a person (a), waiting (b) with ready Tasks needing ownership review, could not determine, retained problems, sessions (with the nine #409 dashboard dimensions plus policy), worktrees, historical (idle) sessions, shift brief, what I could not determine, footer ending `Report complete` (`report.py:545-558`).
- JSON v1 on stdout: `schema_version`, `observed_at`, `scope`, `window`, `orca_available`, `sources`, `rows` (class, rule, evidence, notes, policy, safe_to_close), `worktrees`, `waiting.a/b`, `summary.counts`, `bound_reached`, `visible`, `historical`, `total`, `total_is_lower_bound`, `report_path` (`report.py:613-695`). `total_is_lower_bound` is always true in Phase 1 because remote hosts are never scanned (`classify.py:986-989`).
- Each row carries a fixed "next inspection" text saying what to read next, not what to do (`report.py:54-68`).

### 2.6 The slash command and skill

`/sc:sweep` only loads `sc-sweep-protocol`, which runs `superclaude sweep run <args>` with a 120 s Bash timeout, falls back to `uv run --frozen --no-sync superclaude sweep run` only on "command not found", reads the report in chunks of at most 150 lines until `Report complete`, and prints counts with a `(not observed in Phase 1)` mark on stalled and fenced (SKILL.md steps 1-4, lines 21-27). Its tools are limited to those two Bash forms and Read. It is on the never-as-worker list, so a dispatched worker never runs it (sweep.md line 18). A narrow chat-format exception lets a session with an explicit coordinator assignment print only counts and path (SKILL.md "Final reply").

## 3. Where it could be integrated in future
The sweep is a pattern more than a product: "allowlisted read-only probes, then a pure rule list that refuses to guess, then a sanitized report". Where else that shape helps:

- **Coordinator loop and later orchestrator phases.** WC-16 says the coordinator runs `/sc:sweep` on every wake, at most every 5 minutes, and reads the report before it acts (WORKER-CONTRACT.md:286). Later phases (the program in `.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/open-decisions.md`) add a coordinator that manages work end to end and a handoff from the issue watcher. They need a trusted "what is every worker doing" input. The JSON v1 is that input.
- **Dashboards and TUIs** (the `superclaude observe` observer): they can reuse the classes and the `unscanned` source rows instead of inventing their own state words.
- **Decision gates.** The report names "waiting on a person (a)" with the blocked question and an age. A gate router (approval flow, Q02 in the decision records) can read `waiting.a` and `waiting.b` from the JSON rather than parsing prose.
- **Cleanup and close tooling.** A future `/sc:close` (named out of scope in design section 1) needs `removable` and `safe_to_close` facts. The sweep already computes the blockers (uncommitted, unpushed, unsaved `.dev/tasks`, frozen plan, shared package) and says "could not determine" when unsure.
- **Any multi-agent runner with per-worker folders and a status file**, for example sprint or swarm runs: the same "contract file plus transcript plus process state" join applies.
- **Crash and outage recovery**: the report already tells you which sources were unreadable, which is the first thing a recovery pass needs.
- **Scheduled health checks** (cron or issue-watch cycles) that want a bounded, no-side-effect snapshot. Phase 1 has no scheduler by design.

## 4. Integration guide
**Best route: call it, do not import it.** Treat `superclaude sweep run` as a process with a stable JSON contract.

1. Run `superclaude sweep run --run <run_id> [--window 6h]` (or let it bind the terminal's Run). Capture stdout (one JSON object). Exit 0 means a report exists; 1 and 2 print one stderr line and no JSON (`commands.py:279-288`).
2. Check `schema_version == 1` first; refuse unknown versions.
3. Read `summary` and `rows`. Branch on `rows[].class` and `rows[].rule`, not on prose. Use `waiting.a` and `waiting.b` for human-needed items, `sources[].unscanned` to know what was not seen, `summary.total_is_lower_bound` and `bound_reached` to know if counts are partial.
4. Treat every string as untrusted data. Values are sanitized but come from briefs and contracts (`report.py:569-605`). Never put them into a prompt as instructions.
5. Respect the cadence: at most once every 5 minutes (WC-16). A run can take up to the 90 s budget plus git time, so run it from a loop, not on every keystroke.
6. Do not wrap it in a worker. It is on the never-as-worker list.

**What to reuse if you build a sibling tool** (inside this repo only):
- `probes.check_orca_argv` and `ALLOWED_ORCA` as the pattern for a read-only Orca adapter, including the `runtime_unavailable` and first-call-failed handling (`probes.py:266-312`, `369-394`).
- `probes.Budget` for call, show and time limits.
- `report.sanitize` and `report.cell` for any text that goes into Markdown.
- `commands._publish` (temp plus `os.link`, no overwrite) for any "write one report" step.
- The `SourceCoverage` idea: every failed read becomes a row, never a silent gap.

**Pitfalls**
- Zero in stalled or fenced means "not observed", not "none" (report.py:42-45).
- `working` depends on `agentWait` being present and null; a non-null `agentWait` was never captured, so such a row is treated as waiting (classify.py:251-269 comment).
- `person_started: null` is common; do not read it as false.
- Reports are gitignored operator-local files (`.dev/sweeps/`, design section 10); never post them and never stage them. UNVERIFIED that the `.gitignore` line is on master; design says it should be.
- It needs the `orca-ide` binary (or `$ORCA_CLI_COMMAND`); the report is tested against Orca version 1.4.245 (`report.py:23`).
- The tab-map join only works for sessions launched through `ccsession`; others become "could not determine" (design 2.1 facts).

**Tests to add in a consumer**
- A fixture JSON per class, including a run with Orca unavailable (`orca_available: false`, all rows could-not-determine).
- A test that your consumer rejects `schema_version != 1`.
- A test that a `truncated` or `total_is_lower_bound` run never triggers an "all clear" message.
- If you extend the allowlist: copy the pattern of `tests/sweep/test_probes_allowlist.py` and `tests/sweep/test_readonly.py` (recorded-argv and before/after snapshot checks). Any new Orca verb needs an owner note (design NFR-014).

## 5. IronClaude fit
Files read on origin/master for this section: the file lists of `src/superclaude/cli/observe/` and `issue_watch/`, and the first lines of `observe/adapter.py` and `observe/collector.py`. I did not read the issue-watch cycle or the observer render code in full, so those proposals are marked where they rest on that.

**1. Share the Orca read adapter between `sweep` and `observe` (highest value).**
- Target: `src/superclaude/cli/observe/adapter.py` and `src/superclaude/cli/sweep/probes.py`.
- Change: both already carry their own allowlisted `orca-ide` caller (observe: `WORKER_LIST_TEMPLATE = ("orchestration", "worker-list", "--json", "--limit", "100")`, adapter.py:29; sweep: `ALLOWED_ORCA`, probes.py:49-60). Extract one small read-only adapter module (allowlist check, timeout, output limit, `runtime_unavailable` handling) that both import.
- Value: one place to audit the "never writes to Orca" promise; fewer drifting copies when Orca changes names (PR #579 was exactly such a drift). Effort: medium (about 2 days; both have heavy tests that must stay green). Risk: medium; observe has different paging and caps (`collector.py:33`), so the adapter must stay parameterised. UNVERIFIED how much code is truly duplicate.

**2. Let the observer show the sweep's classes (read the JSON, do not re-derive).**
- Target: `src/superclaude/cli/observe/` (render/view/export).
- Change: optionally run or read the latest `.dev/sweeps/*.md` JSON for the same Run and show class, rule and unscanned reasons beside each worker; keep the observer read-only.
- Value: one vocabulary for people and the coordinator; "could not determine" stops looking like "fine". Effort: medium. Risk: low to medium (two tools could disagree; show the sweep timestamp). UNVERIFIED that observe wants this; the observer's coordinator-questions panel status is documented as a separate decision.

**3. Use the sweep as the "worker state" input of the coordinator and the planned close step.**
- Target: `src/superclaude/core/WORKER-CONTRACT.md` (WC-16 already there), `src/superclaude/core/HOW-WE-WORK.md` ("Orca coordination", line 406), and a future close command.
- Change: no new code now. When `/sc:close` or the issue-watch to coordinator handoff is built, require it to consume `rows[].safe_to_close`, `worktrees[].removable` and `waiting.*` from the JSON and to refuse when `could not determine`.
- Value: avoids closing a worktree with unsaved `.dev/tasks/` or a frozen plan. Effort: low for the rule, larger when the command exists. Risk: low.

**4. Reuse `sanitize` and the publish pattern in other report writers (lower value).**
- Target: any CLI that writes Markdown from untrusted text. I did not audit which ones (UNVERIFIED).
- Change: move `report.sanitize` and `commands._publish` into a shared helper only when a second consumer actually exists.
- Value: consistent injection hygiene. Effort: low. Risk: low, but do it only on demand (the repo rule against speculative additions).

**No good fit found** for sprint, roadmap, tasklist or the eval pipelines: they run their own subprocesses and have their own state files, not Orca Runs. A sweep-style class list there would be new work, not integration.

## 6. Limits, open questions, UNVERIFIED items
**How it fits Phase 2 and later of orchestrator mode.** Phase 1 (this system) is "see": a read-only snapshot with no scheduler, no write verbs, no `/sc:close`, no `gh` reads, no remote hosts, no report retention (design section 1, "Out of scope"). The decision records (merged in PRs #587, #588, #589 on 2026-11-17) describe the intended chain: issue watcher, then a coordinator that starts and supervises workers, then the sweep for status, then the observer dashboard, then a later knowledge layer ("Orchestrator v2", issue 423, not started) (open-decisions.md "The program in plain words"). The same file says the handoff from the watcher to a coordinator, a coordinator that manages work end to end, and any screen where a person approves plans are NOT built. The sweep is therefore the status input that those later phases are expected to read. The exact content of Phase 2 plans is not in the files I read; UNVERIFIED.

**Known limits (stated in the code or PR)**
- Stalled (proved) and fenced are not observed in Phase 1 (report.py:42-45, SKILL.md step 4). Fenced evidence is only ever "unreadable" or from fields the code does not populate; I did not find where it is set to `present` (UNVERIFIED).
- A non-null `agentWait` was never captured; its meaning is UNVERIFIED (models.py:97-99, design open item 6).
- `agent_wait_since` is reserved and never set, so the "waiting since" age for agent waits is always unknown (models.py:111-112).
- Output buffering: `subprocess.run` reads all output and checks the 8 MiB limit after the child exits; the 10 s timeout is the guard (probes.py:270-273, owner ruling 2026-11-12).
- Known gap: a worker-list row with a missing Dispatch id is dropped and only leaves an unscanned source row, so a Run with all such rows could look complete (classify.py:690-696; real Orca emitting such rows is unverified).
- `worker-list` paging is not captured: 100 rows sets `truncated` (probes.py:89, report.py:32).
- `total_is_lower_bound` is hard-coded true (classify.py:986-989).
- Remote hosts are never scanned (probes.py:1381).
- Report checked against Orca 1.4.245 only (report.py:23); other versions print an UNVERIFIED lock line per design open item 15.
- Merge guard for PRs #539 and #579 used the draft guard; whether reviews and CI behave on a draft or ready transition is unverified until a run on a disposable PR (both PR bodies).
- The chat-summary format exception depends on an installed output style copy that has the sweep exception; an older install gets ordinary formatting (SKILL.md "Final reply").

**Open questions**
- Will observe and sweep share an adapter, or stay as two audited copies?
- Will Phase 2 add a scheduler, and does WC-16's "not more than every 5 minutes" cadence stay?
- Who sets `fenced_evidence` to `present`, and when will stalled proofs be observed?
- Should `Safe to close` ever print `yes`, and what evidence would allow it (the code requires a read of the result and an open-PR check that it cannot observe: classify.py:88-90)?

**Not verified by me:** I did not run the CLI, the tests (649 passing is the PR #579 claim), or Orca. I did not read `tests/sweep/test_*.py` bodies except the head of `test_readonly.py`, nor design reviews 1 to 3, nor most of the decision records. The three `.dev/brainstorms/20261113-orchestrator-tui-alignment/` PRs were identified by title and merge time only. `.dev/brainstorms/.../open-decisions.md` lives under `owner-questions/`, not at the folder top.

Footer: graph:stale. Companion file: `/home/coder/workspaces/IronClaude/.dev/analysis/20261117-new-systems/sweep-explain.md`.
