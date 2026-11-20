4ae82798c25abbfd4f726e36c1f674f43fa00bfd
Review one task for spec compliance.

Task brief: ## Task 10: Update the claim command, the skill and the result file for the new prompts

Depends on: Task 6, Task 7

Apply the prompt decisions of Task 6 to the claim surface: `src/superclaude/commands/issue.md`, `src/superclaude/skills/sc-issue-protocol/SKILL.md`, `src/superclaude/skills/sc-issue-protocol/refs/claim.md` and `src/superclaude/skills/sc-issue-protocol/templates/next-steps.md` accept the new prompt forms, carry the Status command into the launch prompt, and make the last step of a launched agent's prompt the writing of its result file `.dev/issues/<N>/result.md` in the closed format of Task 6 (no GitHub write). The launch prompt tells the agent that only the coordinator writes to an issue, a label or a Project. The launch-level guard is not changed here (Task 13). Update every test and document outside `tests/issue_watch` that pins the old fixed prompt `/sc:issue --claim <N> --pipeline none`. The files that hold the literal today (checked with Grep on 2026-11-19, the seven `tests/issue_watch` files excluded because Task 7 owns them) are `src/superclaude/cli/issue_watch/launch.py` (Task 7), `src/superclaude/commands/issue.md`, `src/superclaude/core/WORKER-CONTRACT.md`, the three skill files named above, `tests/commands/test_issue_command.py`, `tests/skills/test_issue_protocol.py`, `docs/user-guide/commands.md`, `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` and `docs/designs/` files `issue-pipeline-fu1.md`, `issue-watcher-setup.md`, `issue-watcher.md`, `sc-issue-claim-pipeline-flag.md`, `sc-issue-command.md`, `sc-issue-launch-level-hook.md`. Run the Grep again before editing and list every hit in the commit message. Run `make sync-dev` and `make verify-sync`.

Acceptance criteria:
- T10.AC1: `grep -rn -- "--pipeline none" src tests docs plugins` has no hit that still presents it as the only watcher prompt.
- T10.AC2: `tests/commands/test_issue_command.py` and `tests/skills/test_issue_protocol.py` show each allowed prompt form is accepted, a prompt with extra text, an unknown level or `--submit` without `--pipeline full` is refused, and the launch prompt ends with the result-file step and contains no `gh` write or `issue-pipeline complete` call. The same tests show `/sc:troubleshoot` is limited (no `--fix`) in the Worktree launch prompt and carries `--fix` in the Full and Full Submit prompts.
- T10.AC3: `uv run pytest tests/commands tests/skills tests/hooks -q` passes.
- T10.AC4: `make verify-sync` is clean and no `.claude/` path is staged.
Global constraints: ## Constraints

- Scope is the IronClaude repository only. The Coder template work (requirements R1, R6, R9, R10, R17, R20, R21; Coder issues 515 and 516) is not implemented here; Task 27 hands it over with exact values.
- This plan applies requirement R33, which adopts the remediation proposal `.dev/remediation/watcher-plan-v3/remediation-proposal.md` with the owner's answers of 2026-11-19: the ship gate stays closed, the `updatedAt` observation is run, self-approval is warn-only, `~/.config/superclaude` joins the guard's tamper tokens, all four pipelines end at In review, and the extra guard refusals are confirmed. It also applies requirement R34, the five blocking corrections of the fourth review (P4-1 to P4-5): the coordinator's approval read names its repo (Tasks 15 and 16), an empty Pipeline has no time to compare (Tasks 3 and 5), the claim-time approval refusal is tested where it is enforced (Task 11), the guard pattern for `issue-pipeline complete` is anchored on the verb word (Task 13), and the worker brief is tested at level `none` only (Tasks 6, 10 and 11).
- This plan applies requirement R35 (owner decision of 2026-11-19): the approval is no longer the label `issue-watch:approved`. It is the organization issue field `Approved` (single select, one option `Yes`, field id 50144115 on `IronbellyOrg`) set to `Yes` by an allowed approver (IronBelly, Clay or a maintainer, the approvers file of today). The trigger label `issue-watch:trigger` stays. Who set the field and when comes from the issue's GraphQL timeline events `IssueFieldAddedEvent`, `IssueFieldChangedEvent` and `IssueFieldRemovedEvent` (each carries `actor`, `createdAt`, `issueField` and the value; verified read-only on 2026-11-19 against issue 675 with another field), because the REST events endpoint names the event but not the field or the value. Task 4a builds the read; the approval predicates, the approval-void rule and the claim-time refusal keep their logic and see the field events as label events named by `approval_label`. A real label with the old name never approves. Task 4 is amended to observe the field instead of the label; the plan was copied from `TASK-WF-requirements-20261119-143917` (Tasks 1 to 3 complete there) and edited by owner instruction, and `source.md` still carries the label wording of the requirements file (Task 28 updates the requirements file).
- Edit `src/superclaude/`, then run `make sync-dev` and `make verify-sync`. Never edit or stage anything under `.claude/` (only `.claude/settings.json` is tracked). The tracked plugin mirror `plugins/superclaude/hooks/scripts/launch-level-guard.sh` is changed together with its source.
- Python only through UV (`uv run pytest`, `uv run ruff`). Tests use the faked `gh` and Orca runners already in `tests/issue_watch/conftest.py`; no task runs the watcher against the real GitHub or Orca, except the read-only schema check of Task 3 and the read-only reads of Task 4.
- `src/superclaude/cli/issue_watch/github.py` stays read-only: no mutation, no POST to a REST path (security invariant NG-2, `tests/issue_watch/test_security_invariants.py`). The only modules that write to GitHub are two new ones outside `github.py`: `src/superclaude/cli/issue_pipeline/complete.py` (Task 12: result comment and Status move, run only by the coordinator) and `src/superclaude/cli/issue_watch/repo_init.py` (Task 20: labels).
- Only the coordinator writes to an issue, a label or a Project item (owner decision of 2026-11-19; `src/superclaude/core/WORKER-CONTRACT.md` lines 241 to 243 and 300), and only under that issue's grant row. An agent launched at Worktree, Full or Full Submit, and every worker, never runs `issue-pipeline complete`, never posts an issue comment and never changes a label or a Project field; it reports through its result file `.dev/issues/<N>/result.md`. The launch-level guard refuses every `gh issue`, `gh label` and `gh project` write at every level, Full Submit included (Task 13), and every `gh api` write at every level. This is a text check on `gh` commands only: a script or another HTTP client is not seen. The complete control is a token with no issues or projects write for launched agents (a Coder row, owner decision). This is the one place the plan goes beyond issue verbs.
- Governed means a session with a record in the launch-level store: the agents launched at Worktree, Full and Full Submit, and bound workers. Not governed: the watcher-launched `--pipeline none` claim session and the coordinator. The claim session's two marked comments are allowed by design, and it reads untrusted issue text under the launch login.
- The approval (the `Approved` issue field set to Yes, R35), the allowed Project Status, the approval-void rule of Task 5 and the "edited after approval" refusal (`predicates.py`) stay the gate. Nothing in this plan removes or auto-satisfies them. The plan-hash approval row (`src/superclaude/cli/issue_pipeline/approval_record.py`) is created only from a worker's `ask` that carries the plan hash (`WORKER-CONTRACT.md`, WC-17), never from claim-time fields. Approval by the launch account is accepted unless the owner sets the exclusion key `approval_excluded_ids` (Task 9, warn-first).
- The cron watcher may launch every Pipeline level as a capability (owner, 2026-11-19), but the ship gate of Task 8 is closed: until a reviewed commit flips `GOVERNED_LEVELS_ALLOWED` and un-skips the launch-level observations (`tests/hooks/test_launch_level_observations.py`), only Pipeline None launches and every other level ends `level_gated`. Full Submit commits, pushes a feature branch to `origin` and runs `/sc:pr-submit --monitor 3`; it never merges. For an issue the owner has put at Full Submit and approved with the `Approved` field after the last Project change, that setting is the person's go for that issue's push and pull request, and nothing else is pushed.
- `~/.config/superclaude` was not in the guard's tamper tokens (guard line 764); Task 13 adds it. Until that lands, the exclusion key and any future config key are as writable as the approvers file, so the exclusion limits an honest but injected session, not a hostile one.
- The term is "coordinator", never "orchestrator". The coordinator branch and worktree are both named `Coordinator`; the session is named `COORD-<RepoName>`.
- Tasks that edit the same file run in plan order, never in parallel: `cycle.py` (Tasks 4a, 5, 7, 8, 9, 16, 22), `launch.py` (Tasks 7, 8, 16), `github.py` (Tasks 3, 4a, 15), `predicates.py` (Tasks 1, 3, 5, 7, 9), `audit.py` (Task 8), `launch-level-guard.sh` (Task 13), `WORKER-CONTRACT.md` (Tasks 11, 14), `issue_pipeline/cli.py` (Tasks 14, 15, 16), `issue_pipeline/reads.py` (Task 15), `test_security_invariants.py` (Tasks 3, 4a, 7, 12, 15). Task 1 leaves `cycle.py` unchanged.
- Every new module that writes under the user's home takes an injectable base directory, and its tests run with every path inside `tmp_path` and assert nothing was written under the real home.
- Do not switch any real watcher on, claim a real issue, install a real cron entry, move a real issue's Status or start a worker for a real issue. Each generated config starts with `enabled: false` and only the automatic first-run check of Task 21 may turn it on.
Start sha: 4ae82798c25abbfd4f726e36c1f674f43fa00bfd
Diff against the start snapshot: diff --git a/docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md b/docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md
index 278a62975..2654b5e92 100644
--- a/docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md
+++ b/docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md
@@ -262,7 +262,7 @@ Diagram 2: where IronClaude code touches the picture. Every box below is CHECKOU
    /sc:issue --claim ─▶ orca_worktree.py worktree ─▶ `orca worktree create ... --no-parent --comment ...` (NO --agent)   [orca_worktree.py:666-682]
                      ─▶ orca_worktree.py launch   ─▶ pending launch record ─▶ `orca agent launch --agent claude ... --prompt "[sc-launch:v1:<nonce>] ..."`  [:1351-1355]
                               Orca starts its configured Claude command (ccsession-orca, if the host is set up so) ─▶ ccsession names the tab ─▶ shim check reads title/screen (advisory)
-   issue-watch once ─▶ cli/issue_watch/launch.py ─▶ `orca agent launch ... /sc:issue --claim <n> --pipeline none` (fixed 12-element argv; the `--pipeline none` level was added 2026-11-17, Plan B) in one configured checkout
+   issue-watch once ─▶ cli/issue_watch/launch.py ─▶ `orca agent launch ... /sc:issue --claim <n> --pipeline <level> --stage <stage>` (fixed 12-element argv; the level comes from the issue's Pipeline and the stage from its Status, `docs/designs/issue-watcher-status-pipelines.md`; the `--pipeline none` level was added 2026-11-17, Plan B, and is the only one that launches while the ship gate is closed) in one configured checkout
                        [per research 04 F2; Orca names tried: _ORCA_CLIS = ("orca-ide", "orca") defined at install_user_setup.py:35, imported at launch.py:22, looped at launch.py:193]
                        The watcher prompt carries no [sc-launch:v1:<nonce>] marker, so that session is NOT bound by the launch-level guard
                        at this hop; since 2026-11-17 the claim session it starts ends after its comments (`--pipeline none`) and launches no agent: a coordinator then runs `orca_worktree.py worktree` and starts a supervised worker with `worker-start` (that worker is bound by the guard only when its brief carries a launch marker; the first test issue runs without one). (Before 2026-11-17 the claim session could launch a second, marked agent; each hop read separately;
@@ -284,7 +284,7 @@ Seven subsystems, numbered and named to match Section 5. Section 5 owns the deta
 | 5.1 Roles and Authority | Defines the session kinds (person, person-opened coordinator, worker run, ordinary session, subagent), what each may do, and the owner decisions D1-D5 behind the rules. Authority is instruction text; the ownership paragraph names the creator-owns-the-agent rule and the "hook blocks `orca worktree create` without `--agent`" sentence. | `src/superclaude/core/` | `WORKER-CONTRACT.md` (`:11` worker run, `:62` WC-13, `:67-69` coordinator); `CLAUDE.md` (`:45-61` Orca session launches and ownership paragraph, uncommitted wording); `HOW-WE-WORK.md` (`:400` coordinator identity) |
 | 5.2 Coordinator Lifecycle and Orca Worker-Side Lifecycle | The coordinator loop (create Task, `worker-start`, wait, sweep, classify states S0-S11, escalate L0-L5, admit results, retry as a new Task) and the worker-side half Orca supplies (dispatch preamble, heartbeat, liveness projection, mailbox, retired scheduler). The loop is normative text; the Orca half is source. | `src/superclaude/core/` (contract sections 4-5); Orca: `IronOrca/src/main/runtime/orchestration/` and `IronOrca/src/shared/` | `WORKER-CONTRACT.md` (`:67-282` coordinator rules, `:283-327` brief template); `IronOrca/src/main/runtime/orchestration/preamble.ts` (`buildDispatchPreamble` `:52-152`); `IronOrca/src/shared/orchestration-heartbeat.ts` |
 | 5.3 Hook Guards and Job Identity | Three registered hook scripts: a lexical gate on `orca worktree create` without `--agent`; a launch-level guard for `/sc:issue --claim`-launched sessions; a Linux job-identity runner that rewrites governed Bash calls. Includes registration, timeouts, fail-open and fail-closed behavior, the DEFECT on alternate Orca names, and the documented Claude Code hook semantics. | `src/superclaude/hooks/` | `hooks/scripts/require-orca-worktree-agent.sh` (`:145` command-word test; `:351-358` block message); `hooks/scripts/launch-level-guard.sh` (`:455-478` `orca` arm); `hooks/hooks.json` (`:63-71,105-134`); `hooks/scripts/launch-job-identity.sh` (`:74` `LEVELS`) |
-| 5.4 Launchers | Start non-worker (not supervised) Claude sessions through `orca agent launch`: the `/sc:issue --claim` script (agent-less create, first-tab close, pending launch record, marked prompt, advisory ccsession shim check), the issue watcher (one fixed argv launching `/sc:issue --claim <n> --pipeline none`), and ccsession, which writes the tab title the shim check reads. | `src/superclaude/skills/sc-issue-protocol/scripts/`; `src/superclaude/cli/issue_watch/`; `src/superclaude/skills/ccsession-tag/` | `orca_worktree.py` (`:666-682` create, `:1274` `cmd_launch`, `:1351-1355` launch argv, `:779` `SHIM_TITLE`); `issue_watch/launch.py` (`:22,193` Orca name probe); `ccsession-tag/ccsession-orca` and `ccsession-tag/ccsession` |
+| 5.4 Launchers | Start non-worker (not supervised) Claude sessions through `orca agent launch`: the `/sc:issue --claim` script (agent-less create, first-tab close, pending launch record, marked prompt, advisory ccsession shim check), the issue watcher (one fixed argv launching `/sc:issue --claim <n> --pipeline <level> --stage <stage>`), and ccsession, which writes the tab title the shim check reads. | `src/superclaude/skills/sc-issue-protocol/scripts/`; `src/superclaude/cli/issue_watch/`; `src/superclaude/skills/ccsession-tag/` | `orca_worktree.py` (`:666-682` create, `:1274` `cmd_launch`, `:1351-1355` launch argv, `:779` `SHIM_TITLE`); `issue_watch/launch.py` (`:22,193` Orca name probe); `ccsession-tag/ccsession-orca` and `ccsession-tag/ccsession` |
 | 5.5 Orca-Side Enforcement (Development Source) | The machine-side controls Orca applies that bear on the contract: who may call `worker-start` and only as a same-Run local helper, where worker reports are routed, the narrow Run-binding refusal, and the nested-worker depth cap whose default differs by build. Read from the development checkout and compared with the installed files; the running process is unobserved. | `IronOrca/src/main/runtime/` and `IronOrca/src/shared/` (external to this repo); installed build `/opt/Orca/resources/app.asar.unpacked/out/` | `IronOrca/src/main/runtime/rpc/methods/orchestration/worker/worker-start-authority.ts` (`:12-20,51-55`); `IronOrca/src/main/runtime/orchestration/dispatch-report-mailbox.ts`; `IronOrca/src/main/runtime/orchestration/db/runs/worker-run-binding.ts`; `IronOrca/src/shared/nested-worker-depth.ts` and installed `out/shared/nested-worker-depth.js` (the two defaults and their lines: Section 5.5) |
 | 5.6 Installer, Orca Skills Install and Doctor | Copies the contract, hooks and ccsession to `~/.claude/`, registers hooks in settings, asks the Orca CLI to install its own skills (`computer-use`, `orca-cli`, `orchestration`; none are shipped by IronClaude), and checks ccsession health. Without `--force` existing destination files are kept, which is why the host-installed set is mixed. | `src/superclaude/cli/` | `install_hooks.py` (`:88,90,93` guard scripts in `_FRESHNESS_SCRIPTS`); `install_user_setup.py` (`:34-35` skill and CLI-name constants, `:198` `_find_orca`, `:230` `install_orca_skills`, `:449` `install_user_setup`); `install_core.py` (`:27` contract in the core file list); `install_ccsession.py` (`:11`); `doctor.py` |
 | 5.7 Worker Result Channel (`return-contract.yaml`) | The `<report-dir>/return-contract.yaml` that a worker command writes and the coordinator reads: field set, four file layouts, status mapping, nested-result rule, and the 31 per-command `## Unattended mode` sections. Writer and reader are LLM sessions; no executable parses the worker fields. | `src/superclaude/core/` (WC-4); `src/superclaude/commands/`; producer refs under `src/superclaude/skills/` | `WORKER-CONTRACT.md` (`:32-39` WC-4 field set and hand-off, `:59` WC-5); `commands/*.md` (31 `## Unattended mode` sections); `tests/skills/test_worker_contract.py` (static text pins, `RULE_PHRASES` `:25-374`) |
@@ -541,7 +541,7 @@ The three branches after the Orca spawn run concurrently; their relative timing
 | # | Hop | Tag | Evidence | Notes |
 |---|-----|-----|----------|-------|
 | A1 | First hop: a person runs `/sc:issue --claim <N>`; the skill drives Waves 0 to 8 and calls `orca_worktree.py` in Waves 0, 5, 7 and 8 | [TEXT] | `src/superclaude/skills/sc-issue-protocol/SKILL.md:84-92` | Waves 1 to 6 (GitHub and ClickUp work, summaries, comments) are outside the Orca data flow and were not traced here |
-| A1b | Path B first hop: the watcher builds a 12-element `orca agent launch` with prompt `/sc:issue --claim <n> --pipeline none` in a configured checkout | [CODE] | `launch.py:95-116`; `research/04-launchers.md` F2 (`cli.py:111-137`, `cycle.py:1026-1112`) | The watcher prompt carries no `[sc-launch:v1:...]` marker, so that first session is ungoverned at that hop; it then runs Flow A. The chained run was not observed [UNVERIFIED] |
+| A1b | Path B first hop: the watcher builds a 12-element `orca agent launch` with prompt `/sc:issue --claim <n> --pipeline <level> --stage <stage>` in a configured checkout | [CODE] | `launch.py:95-116`; `research/04-launchers.md` F2 (`cli.py:111-137`, `cycle.py:1026-1112`) | The watcher prompt carries no `[sc-launch:v1:...]` marker, so that first session is ungoverned at that hop; it then runs Flow A. The chained run was not observed [UNVERIFIED] |
 | A2 | `preflight`: `orca status --json` must exit 0 with `ok: true` and a reachable runtime | [CODE] | `orca_worktree.py:15-18` | Failure is `E-ORCA-REQUIRED`, a STOP before any GitHub or ClickUp write (`research/04-launchers.md` F1) |
 | A3 | `worktree`: list, look up, else `orca worktree create --repo path:<main> --name issue-<N> --base-branch <base> --no-parent --comment "sc:issue <repo>#<N>" --json`. There is no `--agent` and no `--prompt` | [CODE] | `orca_worktree.py:666-682`; docstring `:25-31` | Design record: the create keeps no `--agent` because the claim must copy `<D>` and write the pending record before the agent starts (`docs/designs/sc-issue-claim-pipeline-flag.md:194`; amendment `:11`). An accepted exception recorded 2026-11-08; the unqualified rule text "every Orca worktree gets an agent" does not name it (owner question C1, open) |
 | A4 | Copy `<D>` (`.dev/issues/<N>/`) file by file into the worktree, write `<D>/worktree.json`, then close Orca's plain first tab only when exactly one agent-less terminal is listed | [CODE] | `orca_worktree.py:20-22,31-37` | A tab that cannot be closed is the cosmetic warning `W-FIRST-TAB-LEFT` |
@@ -665,7 +665,7 @@ Columns follow the template. "Type" also names the evidence class of the locatio
 | Nonce to session binding | `[sc-launch:v1:<32 hex>]` in the first prompt, `pending/<nonce>` | `sessions/<sid>` holding `worktree`, `full` or `full-submit`; an unusable leading marker publishes `degraded` | `launch-level-guard.sh:318,334-337,375-378,303-306` | [CODE]. A `degraded` record is read as `worktree` by the guard but blocks every Bash call in the identity hook (`research/03-guards.md` E.3; owner question C12) |
 | Hook payload to decision | tool name, command text, session level | class set (for example ESCAPE, COMMIT) and allow or exit-2 block by level `W`, `WA`, `F`, `FS` | `launch-level-guard.sh:393-742` (via `research/03-guards.md` C.4, C.5); `orca` arm `:458-478` | [CODE]. Text-level only; for the Orca CLI it applies to the name `orca` only (DEFECT, 4.1.3). Unbound sessions are never blocked |
 | Terminal read/show JSON to shim verdict | `result.terminal.tail` (lines) and `result.terminal.title` | true on any marker in the tail or a title match within five tries; else warning `W-LAUNCH-NOT-CCSESSION`, status stays `launched` | `orca_worktree.py:774-782,1142-1161,1377-1386` | [CODE]. Advisory: nothing stops the agent |
-| Watcher prompt gate | an issue number | exactly `/sc:issue --claim <n> --pipeline none` (integer 1 to 999999999) as the only text after `--prompt`; otherwise `ValueError` | `launch.py:84-102` (`PROMPT_PATTERN`, via `research/04-launchers.md` F2) | [CODE]. The watcher launch argv is 12 elements, no marker, no `[sc-launch:...]` binding |
+| Watcher prompt gate | an issue number | exactly `/sc:issue --claim <n> --pipeline <none|worktree|full [--submit]> --stage <research|spec|plan|debug>` (integer 1 to 999999999) as the only text after `--prompt`; otherwise `ValueError` | `launch.py:84-102` (`PROMPT_PATTERN`, via `research/04-launchers.md` F2) | [CODE]. The watcher launch argv is 12 elements, no marker, no `[sc-launch:...]` binding |
 | Source contract to installed copy | `src/superclaude/core/WORKER-CONTRACT.md` | `~/.claude/WORKER-CONTRACT.md`, skipped when the destination exists unless `force` | `install_core.py:14-29,70-72` | [CODE]. A plain install keeps an older installed file; `install_hooks.py:279-281` does the same for hook scripts. The set installed on this host is mixed (3.0.3) |
 
 Rows marked "via" in Sections 4.1 to 4.3 rest on a research file and were not re-read against source when this reference was written: the Orca fleet-projection and attempt-projection rows (`research/gap-P3-G01.md` S2, S3, S5, S5a), the Orca tab-environment and Claude-command join (`research/gap-P3-G05.md` F6, R1), the `worker-start` depth enforcement beyond `worker-start-authority.ts`, and the guard classifier table beyond lines `:303-306`, `:318`, `:334-337`, `:375-378`, `:456-478`. Everything else tagged [CODE-VERIFIED] here was re-read from the live file on 2026-11-12. The host-installed state and the ORIGIN/MASTER comparison are moment-in-time observations. Nothing here describes the running Orca, the running Claude Code process, a live guard session, or any other host.
@@ -1071,7 +1071,7 @@ launch-job-identity.sh         : hook | execute SESSION TOOL_ID COMMAND | prepar
 4. **The launch call (`:1351-1355`).** `orca agent launch --agent claude --worktree path:<wt> --surface terminal --prompt "[sc-launch:v1:<nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it." --json`. When `orca agent launch` itself fails or does not report ok, the pending record is deleted and a hand command is printed with the warning that a hand-started agent is not governed (`:1357-1376`); an IR-4 refusal (`W-ENFORCEMENT-ABSENT`, `:1308-1325`) comes earlier, before the pending record is written, and prints no hand command. **A timeout is different** (CHECKOUT, re-read 2026-11-12): the `detail` reads "orca agent launch timed out; an agent may have started, check Orca before re-running" (`:1359-1360`); the launch call's timeout is `DEFAULT_TIMEOUT` = 120 s (`:80,124-126`); the pending record is still deleted (`:1358`), but nothing is recorded, because only `record_launch` (`:1389`, reached after a successful launch) writes the `launch` entry, so the duplicate-launch guard (`:1283-1299`) cannot stop a second launch. What happens to an agent that did start depends on when its first prompt reaches the guard (derived from source, not run): if the prompt arrives before the delete at `:1358`, the guard has already consumed the nonce with one `mv` (`launch-level-guard.sh:376-378`) and bound the session normally at its requested level, and only the launch record is missing; if it arrives after the delete, the nonce is gone, so a prompt that leads with the marker is published as `degraded` (`:380-382`), which blocks every Bash call in the identity hook (Section 5.3). The safe order is therefore the same in both cases: check Orca (`orca worktree ps`, the worktree's terminals) and close any stray agent before re-running the claim. The guard consumes the marker once (5.3).
 5. **Shim check (advisory).** After launch, `behind_ccsession(handle)` (`:1142`) tries `SHIM_TRIES = 5` times (`:780`), `SC_ORCA_SHIM_INTERVAL` seconds apart (default 2.0): `orca terminal read --terminal <h> --screen --json` for `SHIM_MARKERS = ("[ccsession]", "Session name (Enter or Ctrl+C")` (`:774`), then `orca terminal show --terminal <h> --json` and the title pattern `SHIM_TITLE = sc-launch-v1-[0-9a-f]{1,12}-\d{4}-\d{6}-[0-9a-f]{4}\b` (`:779`) against `result.terminal.title`. A miss, or no terminal handle, adds `W-LAUNCH-NOT-CCSESSION`; status stays `launched`, the `launch` entry is still written and nothing closes the agent. Each read has a 15 s cap; with every call hanging the worst case is 5 x (15 + 15) + 4 x 2 = 158 s, otherwise about 8 s of pauses (arithmetic from the constants).
 6. **Where the title comes from (ccsession).** `ccsession-orca` sees the claim prompt as one positional word, so no question is asked and `ccsession --auto-name "<prompt>"` builds `<folder>-sc-launch-v1-<12 hex>-<MMDD>-<HHMMSS>-<4 hex>` (words cut to 12 characters, folder to 20). The label is shown as `<label> · Claude Code` by an OSC escape at launch and by `orca terminal rename` from the SessionStart hook; both carry the same text. A valid `CCSESSION_NAME`, a Claude `--name`, `CCSESSION_AUTOSTART=0`, or an unwritable name-list directory yields a different or empty label and a false `W-LAUNCH-NOT-CCSESSION` (gap-P3-G05 F9, causes 1-5).
-7. **Watcher (`launch.py`).** `launch_argv` returns exactly 12 elements: `[orca, "agent", "launch", "--agent", "claude", "--worktree", "path:<worktree>", "--surface", "terminal", "--prompt", "/sc:issue --claim <n> --pipeline none", "--json"]` (`:95-116`). The prompt must match `^/sc:issue --claim [1-9][0-9]{0,8} --pipeline none$` (`:33`); `ORCA_AGENT = "claude"` is fixed (`:28`); origin must be `ironbellyorg/ironclaude` (`:50`, `check_origin` `:233`). `find_orca` probes `_ORCA_CLIS = ("orca-ide", "orca")` with `skills list --json` and accepts only an exit-0 reply whose `topics` include `orca-cli` (`:163`). The watcher never creates a worktree (it uses the configured checkout), writes no state itself, and records a pending entry before the call (`cycle.py` `_launch`). Its prompt carries no `[sc-launch:...]` marker, so the watcher-started session is ungoverned; since 2026-11-17 the prompt ends in `--pipeline none`, the claim it runs starts no agent, and a coordinator starts the worker (before that date it bound a second, marked agent only if that session ran the claim; Path B, inferred from two verified hops, not run end to end). **Off by default:** the config key `enabled` defaults to false (`cycle.py:228`) and a cycle that is not a `--dry-run` stops with `not_enabled` (`cycle.py:685-686`); the runbook says no cron entry is enabled and `enabled` stays false until an owner-run live test (follow-up FU-1) has passed (`docs/designs/issue-watcher-setup.md:5`), leaves the scheduler to the owner (`:202`) and treats the cron entry as follow-up FU-2, "this work does not enable it" (`:282`). The checkout ships no timer or service unit (`find` for `*.timer` and `issue-watch*.service`, 2026-11-12) and the live-test record that FU-1 is to produce (named `issue-watcher-live-test` in the runbook, `:5`, expected under `docs/designs/`) does not exist. Whether any scheduler runs `issue-watch once`, or the config on any host sets `enabled: true`, is [UNVERIFIED].
+7. **Watcher (`launch.py`).** `launch_argv` returns exactly 12 elements: `[orca, "agent", "launch", "--agent", "claude", "--worktree", "path:<worktree>", "--surface", "terminal", "--prompt", "/sc:issue --claim <n> --pipeline <level> --stage <stage>", "--json"]` (`:95-116`). The prompt must match `^/sc:issue --claim [1-9][0-9]{0,8} --pipeline none$` (`:33`); `ORCA_AGENT = "claude"` is fixed (`:28`); origin must be `ironbellyorg/ironclaude` (`:50`, `check_origin` `:233`). `find_orca` probes `_ORCA_CLIS = ("orca-ide", "orca")` with `skills list --json` and accepts only an exit-0 reply whose `topics` include `orca-cli` (`:163`). The watcher never creates a worktree (it uses the configured checkout), writes no state itself, and records a pending entry before the call (`cycle.py` `_launch`). Its prompt carries no `[sc-launch:...]` marker, so the watcher-started session is ungoverned; since 2026-11-17 the prompt ends in `--pipeline none`, the claim it runs starts no agent, and a coordinator starts the worker (before that date it bound a second, marked agent only if that session ran the claim; Path B, inferred from two verified hops, not run end to end). **Off by default:** the config key `enabled` defaults to false (`cycle.py:228`) and a cycle that is not a `--dry-run` stops with `not_enabled` (`cycle.py:685-686`); the runbook says no cron entry is enabled and `enabled` stays false until an owner-run live test (follow-up FU-1) has passed (`docs/designs/issue-watcher-setup.md:5`), leaves the scheduler to the owner (`:202`) and treats the cron entry as follow-up FU-2, "this work does not enable it" (`:282`). The checkout ships no timer or service unit (`find` for `*.timer` and `issue-watch*.service`, 2026-11-12) and the live-test record that FU-1 is to produce (named `issue-watcher-live-test` in the runbook, `:5`, expected under `docs/designs/`) does not exist. Whether any scheduler runs `issue-watch once`, or the config on any host sets `enabled: true`, is [UNVERIFIED].
 8. **Reply shapes.** `OPERATION_ID_PATHS` (`launch.py:42`) and `OP_UNKNOWN_TEXT` are marked "PROPOSAL, UNVERIFIED" in the code; whether real Orca replies carry `receipt.operation_id` is [UNVERIFIED]. Reply shapes of `agent launch`, `worktree create` and `terminal` in the claim script are fixture-only.
 
 **Public Interface:**
@@ -1413,7 +1413,7 @@ Columns follow the template (Endpoint, Method, Purpose, Request Shape, Response
 | `orca terminal read --terminal <h> --screen --json` and `orca terminal show --terminal <h> --json` | `behind_ccsession` / `ccsession_title` (`:1132`, `:1146`), 15 s `TERMINAL_READ_TIMEOUT` (`:82`) | Advisory ccsession shim check, up to `SHIM_TRIES = 5` (`:780`) | `--terminal <handle>` | Reads `result.terminal.tail` (list or string) for `SHIM_MARKERS` and `result.terminal.title` for `SHIM_TITLE` (`:1135-1139`, `:1150-1156`) |
 | `<orca-ide\|orca> skills list --json` | `_find_orca` (`install_user_setup.py:198-221`), 10 s per candidate (literal `:213`) | Prove a binary is Orca before using it (on Linux a bare `orca` is often the GNOME screen reader) | argv only | Exit 0 and a JSON object whose `topics` list holds a dict named `orca-cli` |
 | `<orca> skills install --agent claude-code --skill computer-use --skill orca-cli --skill orchestration` | `install_orca_skills` (`:243-253`), at most 25 s (`_ORCA_TIMEOUT`, `:39`) inside a shared 30 s budget (`_NETWORK_BUDGET`, `:40`) | Ask Orca to write its own discovery stubs; IronClaude ships none of them | no `--force`, `--json`, `--local` | Exit code used only for the message prefix; success is counted by three `SKILL.md` files existing under `~/.claude/skills` |
-| `<orca> agent launch --agent claude --worktree path:<dir> --surface terminal --prompt "/sc:issue --claim <n> --pipeline none" --json` (12 argv elements) | issue watcher `launch_argv` (`launch.py:95-116`), 120 s `LAUNCH_TIMEOUT_S` (`cycle.py:40`) | Unattended claim launch in one configured checkout, only when the watcher config sets `enabled` (off by default, Section 5.4 item 7) | `<n>` must match `^/sc:issue --claim [1-9][0-9]{0,8} --pipeline none$` (`launch.py:33`) | Only exit 0 with a JSON object holding a valid operation id at `receipt.operation_id` or `error.operation_id` gives `launched`; both paths are marked "PROPOSAL, UNVERIFIED" in the code (`launch.py:39-45`) |
+| `<orca> agent launch --agent claude --worktree path:<dir> --surface terminal --prompt "/sc:issue --claim <n> --pipeline <level> --stage <stage>" --json` (12 argv elements) | issue watcher `launch_argv` (`launch.py:95-116`), 120 s `LAUNCH_TIMEOUT_S` (`cycle.py:40`) | Unattended claim launch in one configured checkout, only when the watcher config sets `enabled` (off by default, Section 5.4 item 7) | `<n>` must match `^/sc:issue --claim [1-9][0-9]{0,8} --pipeline none$` (`launch.py:33`) | Only exit 0 with a JSON object holding a valid operation id at `receipt.operation_id` or `error.operation_id` gives `launched`; both paths are marked "PROPOSAL, UNVERIFIED" in the code (`launch.py:39-45`) |
 | `orca terminal rename --terminal <handle> [--title <text>]`, `orca terminal show --terminal <handle> --json` | `ccsession` (`orca_tab_name` `:527-539`, `orca_tab_clear` `:541-556`), run from the `session-name.sh` hook | Tab title writer for the claim shim check (see 8.2) | `--title "<label> · Claude Code"`; no `--title` resets | Output discarded; failures ignored |
 
 [CODE-VERIFIED] for every argv shown (CHECKOUT lines above). All reply shapes except the Orca-side `skills list` handler (`IronOrca/src/cli/handlers/skills.ts:8-19`) are known only from test fakes, not from a recorded real reply (`research/04-launchers.md` Gaps item 2); real Orca replies are [UNVERIFIED].
@@ -1442,7 +1442,7 @@ The retired automatic Task scheduler (`orchestration.run`, `orchestration.runSto
 | Job identity hook to launch-level guard | Same Bash call, two hooks | `launch-job-identity.sh` returns `hookSpecificOutput.updatedInput` that replaces the whole input with `/bin/bash <runner> execute <sid> <tool_use_id> <original command>`, without `permissionDecision` (`:475-483` per `research/03-guards.md` E.3; header `:14-15` re-read) | Order and combination of matching hooks are unspecified in the script (`:15`). DOCUMENTED: matching hooks run in parallel and several `updatedInput` rewrites are neither merged nor ordered (https://code.claude.com/docs/en/hooks-guide, "Limitations", re-fetched 2026-11-12 per `web-01`). If the guard ever saw the rewritten command it would block it as LL-TAMPER (the rewrite contains `.claude/hooks`; `tests/hooks/test_launch_level_guard_with_identity.py:135-154`); live order is [UNVERIFIED] (OB-H1 skipped). Whether the whole-input rewrite reaches the tool when Claude Code runs in auto permission mode was not observed: the hook header says live auto-mode rewrites need Task4 (`launch-job-identity.sh:17-18`, `research/03-guards.md:103`), and the documentation exempts a settings `command` hook that rewrites Bash with no `permissionDecision` from the auto-mode denial in the sessions that show that text, with residual cases (https://code.claude.com/docs/en/hooks, `web-01` Q2); DOCUMENTED, not observed on this host [UNVERIFIED]. A session record `degraded` makes the guard allow read-only commands while the identity hook exits 2 on every Bash call (`launch-job-identity.sh:74` `LEVELS` holds three words, re-read) |
 | Claim preflight (IR-4) to host settings and hooks | Outbound read-only | `enforcement_preflight` (`orca_worktree.py:925-1015`) reads `PATH`, `~/.claude/hooks/launch-level-guard.sh` (must contain `# launch-level-guard-version: 1`, `:810`), `CLAUDE_CONFIG_DIR` (`:959-967`, re-read), user, worktree and worktree-local `settings.json` for `disableAllHooks: true` (`:972-982`, re-read), and the guard and identity registrations | Refusal is `status: failed`, warning `W-ENFORCEMENT-ABSENT`, no record, no agent (`:1308-1325`). It never checks registration of `require-orca-worktree-agent.sh` (that name does not occur in the file) and verifies only the claim process, not the agent's environment (`:1318-1320`) |
 | ccsession to claim shim check (tab title) | Writer to reader through Orca | `ccsession --auto-name "<launch prompt>"` builds `<folder>-sc-launch-v1-<12 hex>-<MMDD>-<HHMMSS>-<4 hex>`; shown as `<label> · Claude Code` by an OSC 0 title (`ccsession:1875`) and by `orca terminal rename` from the SessionStart hook (`ccsession:537`, `session-name.sh:196-203`); read back by `SHIM_TITLE` (`orca_worktree.py:779`, re-read) | Advisory only. A miss yields `W-LAUNCH-NOT-CCSESSION`, status stays `launched`, nothing stops the agent (`:1378-1386`, re-read). Stale second screen marker `SHIM_MARKERS[1]` (`:774`) and no test joining producer to matcher are recorded debt (`gap-P3-G05.md` F4.4, F5; owner questions C17 and C19) |
-| Issue watcher to claim flow | Outbound launch, then the launched session runs the claim | `superclaude issue-watch once` runs `agent launch ... --prompt "/sc:issue --claim <n> --pipeline none"` in one configured checkout (`launch.py:95-116`; the `--pipeline none` level since 2026-11-17); that unmarked session then runs the claim, which ends after its comments with no worktree and no agent, and a coordinator that owns the issue creates the worktree and starts the worker (before 2026-11-17 the claim launched a marked second agent) | The watcher prompt carries no `[sc-launch:` marker, so the first session is not governed (`launch-level-guard.sh:366-368`, B9, per research 04). The combined chain was inferred from two verified hops and never run end to end (`research/04-launchers.md` Gaps item 4). Neither launcher calls `worker-start`, so neither starts a supervised worker |
+| Issue watcher to claim flow | Outbound launch, then the launched session runs the claim | `superclaude issue-watch once` runs `agent launch ... --prompt "/sc:issue --claim <n> --pipeline <level> --stage <stage>"` in one configured checkout (`launch.py:95-116`; the `--pipeline none` level since 2026-11-17); that unmarked session then runs the claim, which ends after its comments with no worktree and no agent, and a coordinator that owns the issue creates the worktree and starts the worker (before 2026-11-17 the claim launched a marked second agent) | The watcher prompt carries no `[sc-launch:` marker, so the first session is not governed (`launch-level-guard.sh:366-368`, B9, per research 04). The combined chain was inferred from two verified hops and never run end to end (`research/04-launchers.md` Gaps item 4). Neither launcher calls `worker-start`, so neither starts a supervised worker |
 | Installer to hooks, scripts, Orca and ccsession | Outbound install steps | `superclaude install` order: core files, commands, agents, skills, `wire_ccsession`, `install_hooks`, templates, `install_user_setup` (Orca skills, plugins), codegraph, retire step (`main.py:178-263`; `gap-P3-G03.md` D.1) | `install_hooks` lists the guards in `_FRESHNESS_SCRIPTS` (`install_hooks.py:88,90,93`), copies them flat to `~/.claude/hooks/` and merges registrations; without `--force` an older installed script or outdated matcher is kept (`:279-281`, `:417-419`, per research 03 B.3). `wire_ccsession` links `~/.local/bin/ccsession-orca` but never configures Orca's "Claude command" setting (a manual step: `ccsession-tag/README.md:211-226`) |
 | Worker result channel (`return-contract.yaml`) | Worker writes, coordinator reads | Instruction level only: the command's LLM writes `<report-dir>/return-contract.yaml`; the worker passes its path as `worker_done --report-path`; Orca "does not check the file" (`WORKER-CONTRACT.md:39`, re-read) | No executable in `src/` produces, parses, validates or routes on `worker_contract_version`, `worker_status` or `blocked_question` (negative grep, `gap-P3-G04.md` 4.4). Code that reads other contracts: `cli/reflect/contract.py:65-82` (read-and-ignore of unknown keys) and `sc-implement-protocol/scripts/archive_workspace.py:325-334` (package contract 1.1, not the worker contract). `/sc:implement` has no producer yet: deferred to P4 by a cited scope decision (`gaps-and-questions.md` D) |
 | Orca dispatch preamble to `WORKER-CONTRACT.md` | Text against text | When the depth cap allows, the preamble adds a `SUB-DISPATCH` section telling a worker it may run `worker-start`; WC-13 forbids that for an IronClaude worker (`preamble.ts:142-146,219-256`, per `gap-P3-G01.md` S1; `WORKER-CONTRACT.md:62`, re-read) | The two texts instruct opposite things; the only machine barrier is the depth cap (see 9.3). Orca's federated own-Run variant (`buildOwnRunSubDispatchSection`) is Orca text, not IronClaude sub-orchestration, and was not traced at runtime |
diff --git a/docs/designs/issue-watcher-status-pipelines.md b/docs/designs/issue-watcher-status-pipelines.md
deleted file mode 100644
index d3a332ef9..000000000
--- a/docs/designs/issue-watcher-status-pipelines.md
+++ /dev/null
@@ -1,104 +0,0 @@
-# Issue watcher: per-status commands, launch levels and completion
-
-**Status:** design note, decided 2026-11-19 (Task 6 of the zero-setup plan `TASK-WF-requirements-20261119-143917-2`). It records the owner's decisions of 2026-11-18 and 2026-11-19 (requirements R23, R24, R25, R29, R31, R32, R33, R34 and R35) and fixes every interface that Tasks 7 to 14 implement. Where a line of code or text is named, it was read on 2026-11-19.
-
-Terms: the **Status** is the Project 2 single-select field `Status`; the **Pipeline** is its single-select field `Pipeline` (`None`, `Worktree`, `Full`, `Full Submit`); the **stage** is the word the watcher derives from the Status (`research`, `spec`, `plan`, `debug`); the **level** is the launch level derived from the Pipeline (`none`, `worktree`, `full`, `full submit`). The **approval** is the issue field `Approved` set to `Yes` (R35, `docs/designs/issue-watcher.md`).
-
-## 1. What acts and what does not (R22, Task 1)
-
-Only an issue whose one live Project item has Status `Research`, `Spec`, `Plan` or `Debug` acts (`predicates.ALLOWED_STATUSES`). `Backlog`, `Ready`, `In progress`, `In review`, `Done`, an empty Status and any status added to the board later never act. **Ready triggers nothing**: no command, no launch.
-
-The Pipeline picks the level: `None` or empty is level `none`, `Worktree` is `worktree`, `Full` is `full`, `Full Submit` is `full submit`. Until the ship gate of Task 8 is opened by a reviewed commit, only level `none` launches; every other level ends `level_gated`.
-
-## 2. The decision table
-
-All four Status pipelines end at **`In review`** (owner, 2026-11-19; held in one named table in `complete.py`, Task 12). Only a `succeeded` outcome moves the Status.
-
-| Status | Command at the stage | Runs as the coordinator's worker? (level `none`) | Level `none` | Level `worktree` | Level `full` | Level `full submit` | End Status |
-|---|---|---|---|---|---|---|---|
-| Research | `/sc:research` | Yes: `src/superclaude/commands/research.md:117` has `## Unattended mode` | worker runs it unattended and reports | agent runs it, writes the report in the issue's worktree, halts, no commit | as `worktree` plus one local commit of the report on the issue branch | as `full` plus push of that branch to `origin` and `/sc:pr-submit --monitor 3` | In review |
-| Spec | `/sc:design` when the issue is well defined, else `/sc:brainstorm` with a handoff to `/sc:design` for high complexity or scope | Yes: `design.md:117` and `brainstorm.md:148` | as above | as above | as above | as above | In review |
-| Plan | `/sc:workflow` | Yes: `workflow.md:80` | as above; stops before `/sc:implement` and `/task` | as above | as above | as above | In review |
-| Debug | `/sc:troubleshoot` | Yes: `troubleshoot.md:169` | worker runs it **without `--fix`** | agent runs it **without `--fix`** (propose next steps, halt) | agent runs it **with `--fix`** (a remediation tasklist package, never an applied code change) | as `full` plus push and PR | In review |
-| Ready | none | not applicable | nothing | nothing | nothing | nothing | unchanged |
-
-None of the five commands is on the never-as-worker list (`src/superclaude/core/WORKER-CONTRACT.md:23`: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn`, `/sc:sweep`, `/sc:swarm-wizard`, and `/sc:pr-submit` while decision D3 holds). Each has an `## Unattended mode` section at the line shown, so no alternative is needed. `/sc:pr-submit` is never a worker command: at level `full submit` the launched agent runs it in its own top-level session, as D3 allows.
-
-**Debug at level `none`.** The coordinator's worker runs `/sc:troubleshoot` without `--fix`, because a level `none` worker stops before any code change; code-affecting remediation starts only at `full` and `full submit`. The worker brief is used only at level `none`; at the other levels the launched agent runs the command from its launch prompt, so the brief has no level slot.
-
-**What `--fix` does.** `src/superclaude/commands/troubleshoot.md:54`: `--fix` offers the Tier 3 remediation chain (`/sc:workflow` produces a tasklist package; the user runs `/sc:implement`); code changes never auto-apply. At `full` the agent therefore leaves a remediation package, not a code change.
-
-## 3. The launch prompt (decision 1)
-
-The watcher sends one of these prompts to `orca agent launch --prompt`. The stage is derived from the Status read by `_revalidate`; the level from the Pipeline.
-
-| Level | Prompt for stage `research` (the others replace the last word) |
-|---|---|
-| none | `/sc:issue --claim <N> --pipeline none --stage research` |
-| worktree | `/sc:issue --claim <N> --pipeline worktree --stage research` |
-| full | `/sc:issue --claim <N> --pipeline full --stage research` |
-| full submit | `/sc:issue --claim <N> --pipeline full --submit --stage research` |
-
-Stages: `research`, `spec`, `plan`, `debug`. `--stage` is a new claim-only option of `/sc:issue` (Task 10); `--submit` stays valid only after `--pipeline full`. The launch-level guard has no prompt allow-list, so the pin is the pattern in `launch.py`, which replaces `PROMPT_PATTERN` (line 33):
-
-```
-^/sc:issue --claim [1-9][0-9]{0,8} --pipeline (?:none|worktree|full(?: --submit)?) --stage (?:research|spec|plan|debug)$
-```
-
-`build_claim_prompt` (line 84) takes the issue number, the stage and the level and raises `ValueError` for any input that does not match, so no other text reaches `--prompt`. `launch_argv` (line 95) and `retry_argv` (line 119) keep refusing a prompt that does not fullmatch the pattern. The prompt is built from the item that `_revalidate` rereads (Task 7), so a Status or Pipeline moved between examine and launch cannot launch the old command.
-
-## 4. Which session runs the Status command (decision 3)
-
-- **Level `none`.** The watcher's claim session assigns the issue, posts its two marked comments and writes `.dev/issues/<N>/issue-summary.md` and `next-steps.md`; it creates no worktree and starts no agent. The coordinator then reads the claim's stage, creates the worktree and starts one worker from the worker brief, whose `Command:` line carries the stage's command (section 7).
-- **Levels `worktree`, `full`, `full submit`.** `/sc:issue --claim` creates the worktree and launches an agent in it. The stage command enters the agent's `launch-prompt.md` (written by the claim from `templates/next-steps.md`, Task 10): its first step is the stage command in the form of the table above, its last step is writing `.dev/issues/<N>/result.md`, and it states that only the coordinator writes to an issue, a label or a Project (section 8). The agent runs the command from that prompt.
-
-## 5. How the Status and Pipeline reach the coordinator (decision 4)
-
-A `--pipeline none` claim writes no worktree record. The watcher stores the stage and the level in the claim's `.dev/issues/<N>/next-steps.md` header lines (`stage: <word>` and `level: <word>`) next to the existing summary, and the coordinator reads them there, in the checkout that ran the claim, with the `claimed` entry of `dispatch.json` read-only. The coordinator never trusts a Status it remembers: it rereads the Project item through `stage-status` at each gate, which also reads the approval and the plan reply.
-
-## 6. "Well defined" for Spec (decision 5)
-
-The claim worker that writes `issue-summary.md` judges it, from the Complexity issue field and the summary text: `Simple` or `Medium` with a stated acceptance criterion is well defined (`/sc:design`); anything else, or `Complex`, is not (`/sc:brainstorm`, with a handoff to `/sc:design` for high complexity or scope). It records the verdict and the reason in one line of `issue-summary.md` (`spec-route: design|brainstorm — <reason>`). No code judges it and no issue text reaches the brief.
-
-## 7. The worker brief (levels `none` only)
-
-`src/superclaude/cli/issue_pipeline/templates/worker-brief.txt` and `brief.py` carry one row per allowed Status instead of one row per complexity. The brief's `Command:` line is the command of the Status (the table), built from a closed template; the issue number is a validated integer and the Status a closed set, so no issue text reaches the brief. The brief states that after the coordinator mirrors the Status or moves it to `In review`, the Project values have changed, so any relaunch needs a fresh approval (section 9). `brief.py` keeps the closed-set checks and refuses a bad Status, issue number or nonce with a closed reason. The Debug row at `none` has no `--fix`.
-
-## 8. The approval record (decision 6, R19, R29, R35)
-
-"Automatic approval record" of R19 means the **claim-time approval already kept in `dispatch.json`** (`approver_id`, `approval_event_id`, `approved_at`, now taken from the `Approved` field event) plus the **adoption row** (`adopt-create`). It is not the plan-hash approval row. The plan-hash row (`approval_record.py`, `record_create`) is created only from a worker's `ask` that carries the plan hash (WC-17, R29). A claim-time event is refused as plan approval in `src/superclaude/cli/issue_pipeline/stage_predicates.py` (rule `label-before-plan`, lines 161 to 170, through `stage-status`), because `approval_record.record_create` cannot tell the two events apart and is not changed. The coordinator calls `record-create` only with evidence that `stage-status` reports as accepted. Task 11 tests this where it is enforced, in `tests/issue_pipeline/test_stage_predicates.py` and `test_stage_status.py`.
-
-## 9. The completion update (R24, decision 7)
-
-Only the coordinator writes to an issue, a label or a Project item, and only under that issue's grant row (`WORKER-CONTRACT.md` lines 241 to 243 and 300). An agent launched at any level and every worker reports through its result file and never runs `issue-pipeline complete`.
-
-- **How the coordinator learns a run finished.** At level `none`: the worker's `worker_done` contract. At the other levels: the result file `.dev/issues/<N>/result.md` in the issue's worktree, noticed by the `/sc:sweep` report the coordinator already reads at each wake (WC-16).
-- **Closed format of `result.md`.** Four lines, no free text: `outcome: succeeded|failed|blocked|partial`, `artifacts: <repo-relative paths, comma separated, may be empty>`, `pull_request: <number or none>`, `run: <approval event id>`. The coordinator reads only these four keys; nothing else of the file is posted.
-- **The result comment.** One comment per run, carrying the per-run marker `<!-- sc:issue:result issue=<N> run=<approval_event_id> -->` and the outcome word, the artifact paths and the pull request number. The marker never contains the claim marker. The approval event id keys it because each relaunch needs a fresh approval, so a second run has a different id; a marker already written by the coordinator's own login for the same run suppresses a second comment (idempotency).
-- **Only `succeeded` moves the Status**, with a compare-and-set: the Status moves only from `Research`, `Spec`, `Plan` or `Debug`; any other current Status (for example a person moved it to `Done`) posts the comment and returns `status_moved_by_person` without a move. A `failed`, `blocked` or `partial` outcome posts the comment only. The end Status comes from one table keyed by the allowed Status (all four `In review`), so an exception is a one-line change. The read then write is not atomic; the module says so.
-- **Effect on the approval.** The coordinator's own comment never voids an approval (comments by the watcher's own login are skipped, `predicates.py` `unchanged_since`). Its move to `In review` changes the Status value time, so it voids the approval by design (R31): a retry or relaunch needs a fresh `Approved` set after the last Project change, and `In review` fails `project_check`, so the owner moves the Status back first. The same holds for the coordinator's mirror of the Status at line 298 of the duties.
-
-## 10. The Full Submit push rule (decision 8)
-
-`WORKER-CONTRACT.md` line 245 gets this sentence in place of the current one: "At Full Submit the launched agent pushes only its own feature branch to origin and opens the pull request through /sc:pr-submit; the owner's Pipeline value plus an approval later than the last Project change is the go for that issue only. The coordinator never pushes worker commits on that basis; for every other push the rule above stands." Task 11 applies it and tests that no coordinator push grant is tied to the Pipeline.
-
-## 11. Which sessions the guard governs (decision 10)
-
-Governed means a session with a record in the launch-level store: the agents launched at `worktree`, `full` and `full submit`, and bound workers. Not governed: the watcher-launched `--pipeline none` claim session and the coordinator. The claim session's two marked comments are allowed by design; it reads untrusted issue text under the launch login. The counted marker login is the **workspace's single `gh` login**, shared by the watcher, the coordinator and launched agents; the guard (Task 13) is a text check on `gh` commands and cannot tell them apart by login, so the complete control is a token without issues or projects write for launched agents (a Coder row, Task 27).
-
-## 12. Files that change in Tasks 7 to 14 (by path)
-
-| Task | Files |
-|---|---|
-| 7 | `src/superclaude/cli/issue_watch/launch.py`, `src/superclaude/cli/issue_watch/cycle.py`, `src/superclaude/cli/issue_watch/predicates.py`, and the seven test files `tests/issue_watch/test_cli.py`, `test_cli_e2e.py`, `test_crash_injection.py`, `test_cycle.py`, `test_launch.py`, `test_no_text.py`, `test_security_invariants.py` |
-| 8 | `src/superclaude/cli/issue_watch/launch.py`, `cycle.py`, `audit.py`, `tests/hooks/test_launch_level_observations.py`, `tests/issue_watch/test_cycle.py`, `test_audit.py` |
-| 9 | `src/superclaude/cli/issue_watch/predicates.py`, `cycle.py`, `cli.py`, tests under `tests/issue_watch/` |
-| 10 | `src/superclaude/commands/issue.md`, `src/superclaude/skills/sc-issue-protocol/SKILL.md`, `refs/claim.md`, `templates/next-steps.md`, `tests/commands/test_issue_command.py`, `tests/skills/test_issue_protocol.py`, and the docs that quote the old prompt |
-| 11 | `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/cli/issue_pipeline/templates/worker-brief.txt`, `brief.py`, `tests/skills/test_worker_contract.py`, `tests/issue_pipeline/test_brief.py`, `test_stage_predicates.py`, `test_stage_status.py` |
-| 12 | `src/superclaude/cli/issue_pipeline/complete.py` (new), `tests/issue_pipeline/test_complete.py` (new), `tests/issue_watch/test_security_invariants.py` |
-| 13 | `src/superclaude/hooks/scripts/launch-level-guard.sh`, `plugins/superclaude/hooks/scripts/launch-level-guard.sh`, `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`, the guard and issue-worktree tests |
-| 14 | `src/superclaude/cli/issue_pipeline/cli.py`, `src/superclaude/core/WORKER-CONTRACT.md`, `tests/issue_pipeline/test_complete_cli.py` (new), `tests/skills/test_worker_contract.py` |
-
-## 13. Ship-gate note (Task 8)
-
-`docs/designs/sc-issue-launch-level-hook.md` line 201 limits observation item 1 to `full` and `--submit`, while `refs/claim.md` line 133 asks for an observation of item 1 before any governed claim. One boolean, `GOVERNED_LEVELS_ALLOWED`, follows the stricter text (no governed level launches until the observations pass). A per-level split stays an owner option.
diff --git a/docs/designs/issue-watcher.md b/docs/designs/issue-watcher.md
index 7134a1f62..bbed0123b 100644
--- a/docs/designs/issue-watcher.md
+++ b/docs/designs/issue-watcher.md
@@ -40,13 +40,13 @@ The binding requirements are `.dev/brainstorms/20261107-064825-github-issue-watc
 
 **Superseded 2026-11-14: D2 "claim-only" (the owner's Q2 decision, option 3).** The watcher still launches `/sc:issue --claim <N>` with no `--pipeline` value, but the claim command's default level is `worktree`, not "stop at `next-steps.md`". So the claim session assigns the issue, posts two comments, writes its summary files, then creates the Orca worktree `issue-<N>` and starts a second, governed agent that stops at a plan for a person. No code change was made (`--pipeline none` is not added). The owner reversed their own 2026-11-07 decision knowingly; their words: "3 ... Yes, first test session runs with permission checks off ... Amend document re: option 3". The old D2 wording is kept in the table below for history. This change does not alter what the first live test (FU-1) requires.
 
-**Superseded again 2026-11-17 (Plan B, owner decision 6 = B): D2 is `claim-only again, with a coordinator handoff`.** The watcher's claim returns to `--pipeline none`: the prompt is now `/sc:issue --claim <N> --pipeline none` (`launch.build_claim_prompt`), the claim assigns the issue, posts its two comments and writes its summary files, and it creates no worktree and starts no agent. A person-opened coordinator then runs the claim script's worktree step and starts the plan-writing worker with `worker-start --worktree path:<that worktree>`; the poller still never assigns, comments or moves Project items, and it never reads the approval. Guard decision (owner Q34): `no launch-level guard for the one test issue` (G1, written acceptance included); the guard is changed for a bound worker (G2, `docs/designs/issue-pipeline-guard-g2.md`) before any other issue runs through this flow. Two inputs approve the plan, both read by the coordinator through `stage-status`: the approval label (the Status move on the Project item is its visible sign, reported and not required) and an `approved` comment under the comment rules of the issue pipeline (the issue's assignee or a listed approver, never edited, after the latest plan reply). Latency note (owner Q36, accepted): an approval given on GitHub waits until the coordinator's next gate or wake; an approval given in the coordinator session is immediate. Nothing starts while the coordinator is down, so this change merges only with or after the coordinator rules (`WORKER-CONTRACT.md` section 4) and a running coordinator. Separately, the claim command's own text (`src/superclaude/commands/issue.md`) says no governed claim (`worktree` or `full`) is used on a real issue until its hook checks OB-H1 item 1, OB-H2 and OB-H3 have passed, and that OB-H1 item 5 is needed before a claim at any level; those checks are that command's gate, not this design's.
+**Superseded again 2026-11-17 (Plan B, owner decision 6 = B): D2 is `claim-only again, with a coordinator handoff`.** The watcher's claim returns to `--pipeline none`: the prompt is now `/sc:issue --claim <N> --pipeline none` (`launch.build_claim_prompt`; since the zero-setup plan it also carries `--stage <stage>` and the level of the issue's Pipeline, `docs/designs/issue-watcher-status-pipelines.md`), the claim assigns the issue, posts its two comments and writes its summary files, and it creates no worktree and starts no agent. A person-opened coordinator then runs the claim script's worktree step and starts the plan-writing worker with `worker-start --worktree path:<that worktree>`; the poller still never assigns, comments or moves Project items, and it never reads the approval. Guard decision (owner Q34): `no launch-level guard for the one test issue` (G1, written acceptance included); the guard is changed for a bound worker (G2, `docs/designs/issue-pipeline-guard-g2.md`) before any other issue runs through this flow. Two inputs approve the plan, both read by the coordinator through `stage-status`: the approval label (the Status move on the Project item is its visible sign, reported and not required) and an `approved` comment under the comment rules of the issue pipeline (the issue's assignee or a listed approver, never edited, after the latest plan reply). Latency note (owner Q36, accepted): an approval given on GitHub waits until the coordinator's next gate or wake; an approval given in the coordinator session is immediate. Nothing starts while the coordinator is down, so this change merges only with or after the coordinator rules (`WORKER-CONTRACT.md` section 4) and a running coordinator. Separately, the claim command's own text (`src/superclaude/commands/issue.md`) says no governed claim (`worktree` or `full`) is used on a real issue until its hook checks OB-H1 item 1, OB-H2 and OB-H3 have passed, and that OB-H1 item 5 is needed before a claim at any level; those checks are that command's gate, not this design's.
 
 | Decision | Consequence in this design | Enforced by |
 |---|---|---|
 | D1 option A | No listener, inbound port or address registry. A pull poller run by cron in each workspace. | Package shape (section 5); NG-1 |
 | D2 claim-only (SUPERSEDED 2026-11-14 by option 3, then 2026-11-17 by `claim-only again, with a coordinator handoff`; see above) | Original wording: the job ends once the session has been asked to run `/sc:issue --claim <N>`. The claim stops at `next-steps.md`. **Still true:** the poller itself never assigns, comments or moves Project items; it only launches the claim session, and the claim session (not the poller) does the assigning and commenting. **History (2026-11-14, superseded):** the claim at its default `worktree` level also created worktree `issue-<N>` and started a governed agent that stopped at a plan for a person. **Now (2026-11-17):** the claim runs `--pipeline none` and ends after its comments; a coordinator starts the worker. The poller still makes one launch per approved issue, and it starts no agent beyond that claim session. | NG-2 test over every argv and GraphQL constant (section 12); unchanged, it covers the poller only |
-| D3 integer only | The prompt is built only by `launch.build_claim_prompt(n)`, which accepts an `int` (not `bool`) in 1..999999999 and returns `/sc:issue --claim <n> --pipeline none`. No other text reaches the prompt. | FR-012, NFR-001 property test (section 9) |
+| D3 integer only | The prompt is built only by `launch.build_claim_prompt(n, status, pipeline)`, which accepts an `int` (not `bool`) in 1..999999999, one of the four allowed Statuses and a Pipeline value, and returns `/sc:issue --claim <n> --pipeline <level> --stage <stage>` (`docs/designs/issue-watcher-status-pipelines.md`, section 3). No other text reaches the prompt. | FR-012, NFR-001 property test (section 9) |
 
 **Owner's review-and-approval flow (direction only; to be designed; not part of this change).** The owner intends that after the plan is ready it is posted as a reply on the issue, the issue moves to a review state, the assignee is mentioned and asked to approve, and the move to the next state counts as approval; the same approval could also be given inside Orca through the coordinator session or the TUI dashboard, with the risk of a double start between the two places reduced. Its mechanism is being explored separately and is not decided here.
 
@@ -697,7 +697,7 @@ The operation id regex is a design addition: the id is printed by `status` as pa
 
 ### 9.3 D3 enforcement path
 
-The prompt is built from the `int` held in the candidate's `DiscoveredIssue.number`, which `github.discover` produced with `type(v) is int and 1 <= v <= 999_999_999` (a `bool` fails `type(v) is int`). `build_claim_prompt` repeats the check and returns `f"/sc:issue --claim {n} --pipeline none"`. Nothing else is passed to `launch_argv` except constants, the resolved Orca path and the configured worktree. The property test draws `n` from integers, hostile strings, floats and booleans, and asserts every recorded `--prompt` matches `^/sc:issue --claim [1-9][0-9]{0,8} --pipeline none$`. Because hypothesis is not a dependency (C15), the property test is a seeded `random.Random(331)` loop of 2,000 draws plus the FR-012 edge list, tagged with the existing `property_based` marker (C12).
+The prompt is built from the `int` held in the candidate's `DiscoveredIssue.number`, which `github.discover` produced with `type(v) is int and 1 <= v <= 999_999_999` (a `bool` fails `type(v) is int`). `build_claim_prompt` repeats the check and returns `f"/sc:issue --claim {n} --pipeline {level} --stage {stage}"`. Nothing else is passed to `launch_argv` except constants, the resolved Orca path and the configured worktree. The property test draws `n` from integers, hostile strings, floats and booleans, and asserts every recorded `--prompt` matches `^/sc:issue --claim [1-9][0-9]{0,8} --pipeline (?:none|worktree|full(?: --submit)?) --stage (?:research|spec|plan|debug)$`. Because hypothesis is not a dependency (C15), the property test is a seeded `random.Random(331)` loop of 2,000 draws plus the FR-012 edge list, tagged with the existing `property_based` marker (C12).
 
 ## 10. Observability
 
diff --git a/src/superclaude/commands/issue.md b/src/superclaude/commands/issue.md
index b2be54a23..76357a376 100644
--- a/src/superclaude/commands/issue.md
+++ b/src/superclaude/commands/issue.md
@@ -6,7 +6,7 @@ category: workflow
 complexity: advanced
 mcp-servers: [litellm, auggie, codegraph]
 personas: [analyzer]
-argument-hint: "--claim <number|url> [--pipeline worktree|full|none] [--submit] | --create \"<description>\" [--depth quick|standard|deep] [--mode feature|bug] [--type <type>]"
+argument-hint: "--claim <number|url> [--pipeline worktree|full|none] [--submit] [--stage research|spec|plan|debug] | --create \"<description>\" [--depth quick|standard|deep] [--mode feature|bug] [--type <type>]"
 ---
 
 # /sc:issue: GitHub Issue Claim and Create
@@ -42,6 +42,7 @@ Explicit only: the user types `/sc:issue --claim ...` or `/sc:issue --create ...
 | `--type` | create | chosen by a worker when omitted | `cicd`, `command`, `skill`, `agent`, `hook`, `cli`, `core`, `docs`, `tests`, `install`, `other` | Area of the change; a feature in `tests` gets the issue type Test, otherwise the area is recorded in `flags.md`; no label is applied for it |
 | `--pipeline` | claim | `worktree` | `worktree`, `full`, `none` | How far the launched agent goes. `worktree` and `full` create the worktree and launch an agent; `none` creates no worktree and launches no agent |
 | `--submit` | claim | off | no value | Only with `--pipeline full`: the agent also commits, pushes a feature branch to `origin` and runs `/sc:pr-submit --monitor 3`. Never merges |
+| `--stage` | claim | none (the recommended chain) | `research`, `spec`, `plan`, `debug` | The Project Status the issue is in; the issue watcher sends it. Step 1 of the next steps becomes that stage's command (`/sc:research`, `/sc:design` or `/sc:brainstorm`, `/sc:workflow`, `/sc:troubleshoot`; `--fix` only with `--pipeline full`). Valid with every `--pipeline` value; the launched agent's last step is writing `.dev/issues/<N>/result.md` |
 
 There is no repository option (the repo is always `origin`), no dry-run option and no preview option.
 
@@ -55,6 +56,8 @@ There is no repository option (the repo is always `origin`), no dry-run option a
 - `--pipeline` or `--submit` together with `--create`: STOP `E-CLAIM-ONLY-FLAG` ("--pipeline and --submit apply to --claim only").
 - A `--pipeline` value that is not `worktree`, `full` or `none`, or `--pipeline` with no value: STOP and list those three values.
 - `--submit` with a value, or without `--pipeline full`: STOP `E-SUBMIT-NEEDS-FULL` ("--submit needs --pipeline full").
+- `--stage` together with `--create`: STOP `E-CLAIM-ONLY-FLAG` ("--stage applies to --claim only").
+- A `--stage` value that is not `research`, `spec`, `plan` or `debug`, or `--stage` with no value: STOP and list those four values.
 
 ## Examples
 
@@ -64,6 +67,7 @@ There is no repository option (the repo is always `origin`), no dry-run option a
 /sc:issue --claim 302 --pipeline none
 /sc:issue --claim 302 --pipeline full
 /sc:issue --claim 302 --pipeline full --submit
+/sc:issue --claim 302 --pipeline worktree --stage plan
 /sc:issue --create "The sync check misses deleted skill files" --mode bug --type cli --depth standard
 /sc:issue --create @notes/new-command.md --depth deep
 ```
diff --git a/src/superclaude/skills/sc-issue-protocol/SKILL.md b/src/superclaude/skills/sc-issue-protocol/SKILL.md
index a14a5e89b..e02a8607a 100644
--- a/src/superclaude/skills/sc-issue-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-issue-protocol/SKILL.md
@@ -14,7 +14,7 @@ mcp-servers: [litellm, auggie, codegraph]
 
 Two modes, chosen by the command (`~/.claude/commands/sc/issue.md`), which has already validated the flags:
 
-- **`--claim <number|url>`**: assign an existing issue of the origin repo to the current user on GitHub and, when one exists, on its ClickUp task; check whether the issue text is still accurate; write a summary cheatsheet and the next-step prompt; post two marked comments; then, unless `--pipeline none` (which creates no worktree, launches no agent and ends after the comments), create or reuse the Orca worktree `issue-<N>`, copy `.dev/issues/<N>/` into it and launch one agent there at the level `--pipeline` names: `worktree` (default) plans and waits for approval, `full` also implements without a commit or a push, `full` with `--submit` also commits, pushes a feature branch and opens a PR through `/sc:pr-submit --monitor 3`. Nothing ever merges. This skill never runs a step of `next-steps.md` itself (B2).
+- **`--claim <number|url>`**: assign an existing issue of the origin repo to the current user on GitHub and, when one exists, on its ClickUp task; check whether the issue text is still accurate; write a summary cheatsheet and the next-step prompt; post two marked comments; then, unless `--pipeline none` (which creates no worktree, launches no agent and ends after the comments), create or reuse the Orca worktree `issue-<N>`, copy `.dev/issues/<N>/` into it and launch one agent there at the level `--pipeline` names: `worktree` (default) plans and waits for approval, `full` also implements without a commit or a push, `full` with `--submit` also commits, pushes a feature branch and opens a PR through `/sc:pr-submit --monitor 3`. Nothing ever merges. With `--stage research|spec|plan|debug` (the watcher's prompt carries it, one stage per Project Status) the first step of `next-steps.md` is that stage's command and the launch prompt names it; the launched agent's last step is writing `.dev/issues/<N>/result.md` (three lines: `outcome`, `artifacts`, `pull_request`), because only the coordinator writes to an issue, a label or a Project. This skill never runs a step of `next-steps.md` itself (B2).
 - **`--create "<description>"`**: turn a description into a GitHub issue built from one of four templates, with a GitHub issue type, the Complexity issue field and a mode label, and post it. GitHub only: no ClickUp task and no self-assignment (B6).
 
 For issues filed through `/sc:issue --create`, its four templates replace the `ISSUE-HANDOFF.md` / `ISSUE-BACKLOG.md` instruction of rule 10 in the distributed `CLAUDE.md`; rule 10 itself is unchanged and still governs issues filed without `/sc:issue`.
@@ -86,7 +86,7 @@ Load `refs/claim.md` now. `<N>` is the issue number, `<D>` = `.dev/issues/<N>/`.
 3. **Wave 2, edge cases** from `scout.md`: a pull request is STOP `E-NOT-AN-ISSUE`; closed or assigned to someone else stops with the stated message and no write (B9); re-claim continues; earlier marked comment IDs are kept for Wave 6.
 4. **Wave 3, assign.** `gh issue edit <N> --repo <R> --add-assignee @me` (failure STOP `E-ASSIGN-FAILED`, before ClickUp and any comment), then `scripts/clickup_claim.py` with stdout to `<D>/clickup.json`; every ClickUp outcome except an argument error is non-fatal.
 5. **Wave 4, accuracy check and summary.** Spawn `issue-worker-t2`, or `issue-worker-t1` when `scout.md` says `complex`; it writes `<D>/accuracy-check.md`, `<D>/issue-summary.md` (effort in hours) and, when out of date, the analysis report as `<D>/analysis/analyze-<scope>.md` (`<scope>` in this file name is the last segment of the main path the issue touches). No file under `<D>/analysis/` has a name that starts with analysis, report, summary or findings.
-6. **Wave 5, next steps.** Load `refs/chains.md`. Invoke `Skill sc-recommend` with the goal format of `refs/chains.md`; save its output verbatim to `<D>/recommend.md` from `templates/recommend-record.md`. Write `<D>/next-steps.md` from `templates/next-steps.md`, starting with the `/model` tier line and carrying the `Plan boundary: after step <K>` line. Unless `--pipeline none`, render `<D>/launch-prompt.md` with `orca_worktree.py prompt` (the script keeps the existing prompt only while a launch entry's worktree still exists).
+6. **Wave 5, next steps.** Load `refs/chains.md`. Invoke `Skill sc-recommend` with the goal format of `refs/chains.md`; save its output verbatim to `<D>/recommend.md` from `templates/recommend-record.md`. Write `<D>/next-steps.md` from `templates/next-steps.md`, starting with the `/model` tier line and carrying the `Plan boundary: after step <K>` line (and, with `--stage`, the `Stage:` and `Level:` lines and the stage command as step 1, `refs/claim.md` Wave 5). Unless `--pipeline none`, render `<D>/launch-prompt.md` with `orca_worktree.py prompt` (passing `--stage <stage>` when given; the script keeps the existing prompt only while a launch entry's worktree still exists).
 7. **Wave 6, post.** Post or edit (by marker) the accuracy-check comment and the claim comment (`templates/claim-comment.md`). Then continue with Wave 7 and Wave 8, except for `--pipeline none`, which ends the claim here (print the final output and the return contract). A STOP in Waves 0 to 6 means no Orca call after the Wave 0 check. This skill never runs a step of `next-steps.md` (B2).
 8. **Wave 7, worktree.** Not for `--pipeline none`. `orca_worktree.py worktree --repo <R> --number <N> --base origin/<B> --source <D>` creates or reuses the worktree and copies `<D>` into it. Every failure is a warning: the claim `status` stays `success`.
 9. **Wave 8, launch.** Only when `--pipeline` is not `none` and Wave 7 `status` is `created` or `reused`: `orca_worktree.py launch --number <N> --source <D> --level <L> [--submit]` first checks that the launch-level guard would be effective (the IR-4 preflight; read only) and refuses the launch with `W-ENFORCEMENT-ABSENT` when the guard is missing or not effective (no agent starts and no launch record is written); otherwise it starts one agent in the worktree at the chosen level, behind the ccsession shim, and records the level for the enforcement hook, installs the L2 pre-push hook in the clone's shared hooks directory (`install_l2`) and adds the warning `W-L2-ABSENT` when that hook is not in effect (the launch still goes ahead: the IR-7 refusal arrives switched off in the separate last #441 commit, `IR7_REFUSE = False`, so this stays a warning). The agent, not this skill, runs the steps. Ship gate: no governed claim (`--pipeline worktree` or `full`) is used on a real issue until OB-H1 item 1 (parent `session_id` in subagent payloads), OB-H2 and OB-H3 have passed. In `sc-issue-launch-level-hook.md`, section 7 (U1) requires item 1 before a `full` or `--submit` claim and OB-H1 item 5 (self-started turns wrapped) before a claim at any level; OB-H2 and OB-H3 come from its sections 11 and 14. Every failure, a refusal included, is a warning. Then print the final output of `refs/claim.md` (worktree line, tracking note, launch result with its release instruction and L1/L2 layer status lines, every warning with its remedy line), the return contract, and STOP.
diff --git a/src/superclaude/skills/sc-issue-protocol/refs/claim.md b/src/superclaude/skills/sc-issue-protocol/refs/claim.md
index 553afdb6a..6a0285009 100644
--- a/src/superclaude/skills/sc-issue-protocol/refs/claim.md
+++ b/src/superclaude/skills/sc-issue-protocol/refs/claim.md
@@ -77,9 +77,9 @@ Effort is always recorded in hours.
 Load `refs/chains.md`.
 
 1. Invoke `Skill sc-recommend` with the goal format of `refs/chains.md`: issue URL, type, complexity, the summary path and the default chain row for that type and complexity as the suggested route. `/sc:recommend` picks the starting chain and depth (B4). Save its output verbatim to `<D>/recommend.md` from `templates/recommend-record.md`.
-2. Write `<D>/next-steps.md` from `templates/next-steps.md`: the `/model` tier line first (simple -> `claude-gw-tier2`, medium and complex -> `claude-gw-tier1b`, with the note to use `claude-gw-tier2` when `claude-gw-tier1b` is not in the user's `/model` list, default D6), then the commands in order with their flags and the inputs each needs (`@.dev/issues/<N>/issue-summary.md`), the effort estimate, and, when `/sc:recommend` chose differently from the default row, one line naming the default row and why it was not used (default D23). When `/sc:recommend` asks a question or finds no route, record that in `recommend.md` and use the default row, saying so.
+2. Write `<D>/next-steps.md` from `templates/next-steps.md`: the `/model` tier line first (simple -> `claude-gw-tier2`, medium and complex -> `claude-gw-tier1b`, with the note to use `claude-gw-tier2` when `claude-gw-tier1b` is not in the user's `/model` list, default D6), then the commands in order with their flags and the inputs each needs (`@.dev/issues/<N>/issue-summary.md`), the effort estimate, and, when `/sc:recommend` chose differently from the default row, one line naming the default row and why it was not used (default D23). When `/sc:recommend` asks a question or finds no route, record that in `recommend.md` and use the default row, saying so. With `--stage <stage>` (the watcher's per-Status prompt, `docs/designs/issue-watcher-status-pipelines.md`), step 1 is the stage's command instead of the recommended chain: `research` runs `/sc:research`, `spec` runs `/sc:design` (or `/sc:brainstorm` then `/sc:design`, by the `spec-route:` line the summary carries: `design` when the issue is well defined, else `brainstorm`, with the reason), `plan` runs `/sc:workflow` and stops at the tasklist package, and `debug` runs `/sc:troubleshoot` with `--fix` only at `--pipeline full` (at `worktree` without it). The file also carries the lines `Stage: <stage>` and `Level: <level>` so a coordinator can read them. The stage command never runs `/sc:implement` or `/task`.
 3. Set the plan boundary. `next-steps.md` carries the line `Plan boundary: after step <K>` under its title. `<K>` is the number of the last step before the first step whose command is `/sc:implement` or `/task` (default D7); when the first step is itself the implementation step the line reads `Plan boundary: before step 1`. Level `worktree` stops there until a human approves; `--pipeline full` ignores the line.
-4. Render the launch prompt, for `--pipeline` `worktree` or `full` (not `none`): `uv run --no-project python "<skill base>/scripts/orca_worktree.py" prompt --template "<skill base>/templates/launch-prompt.md" --level <L> [--submit] --number <N> --repo <R> --source "<D>" --out "<D>/launch-prompt.md"`, where `<L>` is the `--pipeline` value. It is written before Wave 7 so the copy into the worktree carries it. The script keeps an existing `<D>/launch-prompt.md` (it prints `status: kept`) only while `<D>/worktree.json` has a `launch` entry whose worktree still exists, because that agent reads the file; when the worktree was removed and replaced, it renders a fresh prompt for the new launch.
+4. Render the launch prompt, for `--pipeline` `worktree` or `full` (not `none`): `uv run --no-project python "<skill base>/scripts/orca_worktree.py" prompt --template "<skill base>/templates/launch-prompt.md" --level <L> [--submit] [--stage <stage>] --number <N> --repo <R> --source "<D>" --out "<D>/launch-prompt.md"`, where `<L>` is the `--pipeline` value. It is written before Wave 7 so the copy into the worktree carries it. The script keeps an existing `<D>/launch-prompt.md` (it prints `status: kept`) only while `<D>/worktree.json` has a `launch` entry whose worktree still exists, because that agent reads the file; when the worktree was removed and replaced, it renders a fresh prompt for the new launch.
 5. Do not run any of the steps of `next-steps.md` (B2): the launched agent runs them, at the level the user chose.
 
 ## Wave 6: post (orchestrator, directly, B1)
diff --git a/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py b/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
index 0f93d6f57..19aa12bba 100644
--- a/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
+++ b/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
@@ -743,17 +743,41 @@ def cmd_worktree(args: argparse.Namespace) -> int:
 BLOCK_MARKER = re.compile(r"^<!-- block:([a-z]+) -->[ \t]*$", re.M)
 
 
+STAGES = ("research", "spec", "plan", "debug")
+
+
 def render_prompt(
-    template: str, level: str, submit: bool, number: int, repo: str
+    template: str,
+    level: str,
+    submit: bool,
+    number: int,
+    repo: str,
+    stage: str | None = None,
 ) -> str:
-    """Keep ``common`` + the level block (+ ``submit``); drop markers and the rest.
-
-    ``<N>`` becomes the issue number and ``<R>`` the origin repository (validated as
-    ``owner/repo`` by the argument parser, so it carries no markup).
+    """Keep ``common``, the level block, ``submit``, the stage block and ``result``.
+
+    The stage block is the stage's own (``research``, ``spec`` or ``plan``), or for
+    ``debug`` the ``debugworktree`` block at level ``worktree`` (no ``--fix``) and
+    ``debugfull`` at level ``full`` with or without ``--submit`` (with ``--fix``).
+    ``result`` is always last: the launched agent's final step is its result file.
+    Markers and every other block are dropped. ``<N>`` becomes the issue number and
+    ``<R>`` the origin repository (validated as ``owner/repo`` by the argument
+    parser, so it carries no markup).
     """
+    if stage is not None and stage not in STAGES:
+        raise ValueError(f"unknown stage: {stage}")
     parts = BLOCK_MARKER.split(template)  # [preamble, name, body, name, body, ...]
     blocks = dict(zip(parts[1::2], parts[2::2]))
-    wanted = ["common", level] + (["submit"] if submit else [])
+    stage_block = (
+        []
+        if stage is None
+        else [("debugfull" if level == "full" else "debugworktree")]
+        if stage == "debug"
+        else [stage]
+    )
+    wanted = (
+        ["common", level] + (["submit"] if submit else []) + stage_block + ["result"]
+    )
     missing = [name for name in wanted if name not in blocks]
     if missing:
         raise ValueError(f"template has no block: {', '.join(missing)}")
@@ -777,7 +801,9 @@ def cmd_prompt(args: argparse.Namespace) -> int:
             return emit({"status": "kept", "path": str(args.out)})
     try:
         template = Path(args.template).read_text(encoding="utf-8")
-        text = render_prompt(template, args.level, args.submit, args.number, args.repo)
+        text = render_prompt(
+            template, args.level, args.submit, args.number, args.repo, args.stage
+        )
         atomic_write_text(Path(args.out), text)
     except (OSError, ValueError) as exc:
         return emit({"status": "failed", "detail": str(exc)})
@@ -1872,6 +1898,7 @@ def build_parser() -> argparse.ArgumentParser:
     pr.add_argument("--template", required=True)
     pr.add_argument("--level", required=True, choices=["worktree", "full"])
     pr.add_argument("--submit", action="store_true")
+    pr.add_argument("--stage", choices=list(STAGES))
     pr.add_argument("--number", required=True, type=issue_number)
     pr.add_argument("--repo", required=True, type=repo_name)
     pr.add_argument("--source", help="issue folder; keeps the prompt of a live launch")
diff --git a/src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md b/src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md
index 06bf9910d..0381353a8 100644
--- a/src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md
+++ b/src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md
@@ -17,6 +17,8 @@ Run each step of `next-steps.md`, in order, by invoking its command through the
 
 Never merge anything, and never push to `master` or `main`.
 
+Only the coordinator writes to an issue, a label or a Project. You never post an issue comment, never change an issue, a label or a Project field, and never run the coordinator's completion step; you report only through your result file (the last step below).
+
 <!-- block:worktree -->
 Level: worktree. Follow the steps of `next-steps.md` up to the line `Plan boundary: after step <K>` (the number after `after step` is the last step you may run before a human approves). If the line reads `Plan boundary: before step 1`, there is nothing to run yet. Do not run `/sc:implement`, `/task`, `git commit`, `git push` or `/sc:pr-submit`.
 
@@ -32,3 +34,29 @@ The owner asked for the commit and push by passing `--submit`. This replaces the
 2. Commit with `git commit` and a conventional-commit message. Stage `.dev/tasks` and the files you changed; never anything under `.claude/` and never `.dev/issues/`.
 3. Push the current feature branch with `git push origin <branch>`, never `master` or `main`.
 4. Run `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."` through the Skill tool. Never merge.
+
+<!-- block:research -->
+Stage: research. Step 1 of `next-steps.md` is `/sc:research` on `.dev/issues/<N>/issue-summary.md`. Keep its report under `.dev/issues/<N>/`.
+
+<!-- block:spec -->
+Stage: spec. Step 1 of `next-steps.md` is `/sc:design` when `issue-summary.md` has the line `spec-route: design`, otherwise `/sc:brainstorm`, followed by `/sc:design` for an issue of high complexity or scope.
+
+<!-- block:plan -->
+Stage: plan. Step 1 of `next-steps.md` is `/sc:workflow` on `.dev/issues/<N>/issue-summary.md`. Stop at the tasklist package it writes; never run `/sc:implement` or `/task` for this stage.
+
+<!-- block:debugworktree -->
+Stage: debug. Step 1 of `next-steps.md` is `/sc:troubleshoot` on `.dev/issues/<N>/issue-summary.md`, run without `--fix`. Report the cause and the next steps it proposes, then stop.
+
+<!-- block:debugfull -->
+Stage: debug. Step 1 of `next-steps.md` is `/sc:troubleshoot` on `.dev/issues/<N>/issue-summary.md`, run with `--fix`. It leaves a remediation tasklist package; never apply a code change by hand.
+
+<!-- block:result -->
+Last step, after every other step, whatever the outcome: write `.dev/issues/<N>/result.md` with exactly these three lines and nothing else:
+
+```text
+outcome: succeeded
+artifacts: <repo-relative paths, comma separated, or empty>
+pull_request: <the number, or none>
+```
+
+Use `failed`, `blocked` or `partial` in place of `succeeded` when that is the truth. The coordinator reads this file and does everything on GitHub itself.
diff --git a/src/superclaude/skills/sc-issue-protocol/templates/next-steps.md b/src/superclaude/skills/sc-issue-protocol/templates/next-steps.md
index cf5fa1f73..de00a2ae0 100644
--- a/src/superclaude/skills/sc-issue-protocol/templates/next-steps.md
+++ b/src/superclaude/skills/sc-issue-protocol/templates/next-steps.md
@@ -3,6 +3,7 @@
 # Next steps for #<N>
 
 Plan boundary: after step <K>
+<Only with --stage: the two lines "Stage: <research|spec|plan|debug>" and "Level: <none|worktree|full|full --submit>"; step 1 is then the stage's command (`refs/claim.md` Wave 5)>
 
 Run these in order, after the `/model` line. `/sc:issue` itself does not run them: the agent it launches does (up to the plan boundary at the default level), or you do after `--pipeline none`.
 
diff --git a/tests/commands/test_issue_command.py b/tests/commands/test_issue_command.py
index 7604e08d6..178745884 100644
--- a/tests/commands/test_issue_command.py
+++ b/tests/commands/test_issue_command.py
@@ -81,7 +81,7 @@ def test_st3_version_is_1_1_0():
     assert _frontmatter()["version"] == '"1.1.0"'
 
 
-def test_st1_options_table_lists_exactly_the_seven_flags():
+def test_st1_options_table_lists_exactly_the_eight_flags():
     assert sorted(_options_rows()) == sorted(
         [
             "--claim",
@@ -91,10 +91,67 @@ def test_st1_options_table_lists_exactly_the_seven_flags():
             "--type",
             "--pipeline",
             "--submit",
+            "--stage",
         ]
     )
 
 
+STAGES = ["research", "spec", "plan", "debug"]
+
+
+def test_r23_stage_option_is_claim_only_with_the_four_stages():
+    row = _options_rows()["--stage"]
+    assert row[1] == "claim"
+    assert re.findall(r"`([a-z]+)`", row[3]) == STAGES
+    assert "--stage research|spec|plan|debug" in _frontmatter()["argument-hint"]
+
+
+def test_r23_stage_stop_rules_follow_the_submit_rule():
+    text = _text()
+    stops = text.index("## STOP rules")
+    rules = text[stops : text.index("\n## ", stops + 1)]
+    submit = rules.index("E-SUBMIT-NEEDS-FULL")
+    stage_create = rules.index('"--stage applies to --claim only"')
+    stage_value = rules.index("A `--stage` value that is not")
+    assert submit < stage_create < stage_value
+    assert "`--stage` together with `--create`: STOP `E-CLAIM-ONLY-FLAG`" in rules
+    assert "with no value" in rules[stage_value:]
+
+
+@pytest.mark.parametrize("stage", STAGES)
+@pytest.mark.parametrize(
+    "level", ["none", "worktree", "full", "full --submit"], ids=str
+)
+def test_r23_every_prompt_form_the_watcher_sends_is_a_documented_form(stage, level):
+    """Each form the watcher can send (Task 7) parses under the documented rules:
+    one of the three --pipeline values, --submit only after full, one stage."""
+    from superclaude.cli.issue_watch import launch
+
+    prompt = f"/sc:issue --claim 12 --pipeline {level} --stage {stage}"
+    assert launch.PROMPT_PATTERN.fullmatch(prompt)
+    tokens = prompt.split()
+    assert tokens[tokens.index("--pipeline") + 1] in ("worktree", "full", "none")
+    assert ("--submit" in tokens) <= (tokens[tokens.index("--pipeline") + 1] == "full")
+    assert tokens[tokens.index("--stage") + 1] in STAGES
+
+
+@pytest.mark.parametrize(
+    "prompt",
+    [
+        "/sc:issue --claim 12 --pipeline none --stage research extra",
+        "/sc:issue --claim 12 --pipeline turbo --stage research",
+        "/sc:issue --claim 12 --pipeline worktree --submit --stage plan",
+        "/sc:issue --claim 12 --pipeline none --submit --stage plan",
+        "/sc:issue --claim 12 --pipeline full --stage ready",
+        "/sc:issue --claim 12 --stage plan",
+    ],
+)
+def test_r23_extra_text_an_unknown_level_and_submit_without_full_are_refused(prompt):
+    from superclaude.cli.issue_watch import launch
+
+    assert launch.PROMPT_PATTERN.fullmatch(prompt) is None
+
+
 @pytest.mark.parametrize("flag", sorted(ALLOWED))
 def test_options_table_allowed_values(flag):
     values_cell = _options_rows()[flag][3]
diff --git a/tests/skills/test_issue_orca_worktree.py b/tests/skills/test_issue_orca_worktree.py
index 8025e9873..5417b1943 100644
--- a/tests/skills/test_issue_orca_worktree.py
+++ b/tests/skills/test_issue_orca_worktree.py
@@ -1142,7 +1142,10 @@ def test_pr2_prompt_submit_adds_the_submit_block(tmp_path: Path) -> None:
     assert "/sc:pr-submit --monitor 3" in text
     assert text.index("Level: full.") < text.index("owner asked for the commit")
     plain = render(tmp_path, "full")[1].read_text()
-    assert text.startswith(plain.rstrip("\n"))
+    # The submit block sits before the closing result step (R23), which both end with.
+    body, result = plain.split("Last step, after every other step", 1)
+    assert text.startswith(body.rstrip("\n"))
+    assert text.rstrip("\n").endswith(result.rstrip("\n"))
 
 
 def test_pr3_prompt_submit_with_worktree_level_is_a_bad_argument(
diff --git a/tests/skills/test_issue_protocol.py b/tests/skills/test_issue_protocol.py
index f8e89060f..2e22c4401 100644
--- a/tests/skills/test_issue_protocol.py
+++ b/tests/skills/test_issue_protocol.py
@@ -277,9 +277,105 @@ def test_st5_launch_prompt_template_is_in_the_files_table_and_exists():
     assert len(list(REFS.glob("*.md"))) == 5
 
 
-def test_st8_launch_prompt_has_exactly_the_four_blocks():
-    assert list(_launch_blocks()) == ["common", "worktree", "full", "submit"]
-    assert len(_BLOCK_MARKER.findall(_text(LAUNCH_TEMPLATE))) == 4
+LAUNCH_BLOCKS = [
+    "common",
+    "worktree",
+    "full",
+    "submit",
+    "research",
+    "spec",
+    "plan",
+    "debugworktree",
+    "debugfull",
+    "result",
+]
+
+
+def test_st8_launch_prompt_has_exactly_the_ten_blocks():
+    assert list(_launch_blocks()) == LAUNCH_BLOCKS
+    assert len(_BLOCK_MARKER.findall(_text(LAUNCH_TEMPLATE))) == len(LAUNCH_BLOCKS)
+
+
+def _orca_module(name: str):
+    import importlib.util
+    import sys
+
+    spec = importlib.util.spec_from_file_location(name, ORCA_SCRIPT)
+    module = importlib.util.module_from_spec(spec)
+    sys.modules[spec.name] = module  # dataclasses need it
+    try:
+        spec.loader.exec_module(module)
+    finally:
+        sys.modules.pop(spec.name, None)
+    return module
+
+
+def _render(level: str, stage: str | None, submit: bool = False) -> str:
+    return _orca_module("orca_worktree_t10").render_prompt(
+        _text(LAUNCH_TEMPLATE), level, submit, 12, "owner/repo", stage
+    )
+
+
+CASES = [
+    ("worktree", False),
+    ("full", False),
+    ("full", True),
+]
+
+
+@pytest.mark.parametrize("stage", [None, "research", "spec", "plan", "debug"])
+@pytest.mark.parametrize(("level", "submit"), CASES)
+def test_r23_launch_prompt_ends_with_the_result_step_and_makes_no_github_write(
+    level, submit, stage
+):
+    text = _render(level, stage, submit)
+    assert "Last step" in text and ".dev/issues/12/result.md" in text
+    assert text.strip().endswith("does everything on GitHub itself.")
+    result = text.split("Last step", 1)[1]  # nothing follows the result step
+    assert "outcome: succeeded" in result and "pull_request:" in result
+    assert "artifacts:" in result
+    assert "Only the coordinator writes to an issue, a label or a Project" in text
+    for forbidden in ("issue-pipeline", "gh issue", "gh label", "gh project", "gh api"):
+        assert forbidden not in text, forbidden
+    if stage != "debug":
+        assert "--fix" not in text
+
+
+@pytest.mark.parametrize(("level", "submit"), CASES)
+def test_r23_troubleshoot_is_limited_at_worktree_and_carries_fix_at_full(level, submit):
+    text = _render(level, "debug", submit)
+    stage = text.split("Stage: debug.", 1)[1].split("\n\n", 1)[0]
+    assert "/sc:troubleshoot" in stage
+    if level == "worktree":
+        assert "without `--fix`" in stage
+        assert "with `--fix`" not in stage
+    else:
+        assert "with `--fix`" in stage
+        assert "without `--fix`" not in stage
+
+
+@pytest.mark.parametrize(
+    ("stage", "command"),
+    [
+        ("research", "/sc:research"),
+        ("spec", "/sc:design"),
+        ("plan", "/sc:workflow"),
+    ],
+)
+def test_r23_each_stage_names_its_command_in_the_launch_prompt(stage, command):
+    text = _render("worktree", stage)
+    assert f"Stage: {stage}." in text and command in text
+    assert "/sc:implement" not in text.split("Stage:", 1)[1].split("\n\n", 1)[0] or (
+        stage == "plan"
+    )
+
+
+def test_r23_the_prompt_command_takes_a_stage_and_refuses_an_unknown_one():
+    module = _orca_module("orca_worktree_t10b")
+    with pytest.raises(ValueError):
+        module.render_prompt(_text(LAUNCH_TEMPLATE), "full", False, 12, "o/r", "ready")
+    with pytest.raises(SystemExit):
+        module.main(["prompt", "--stage", "ready"])
 
 
 def test_st8_pr_tokens_live_only_in_the_submit_block_and_the_worktree_prohibition():
diff --git a/docs/designs/issue-watcher-status-pipelines.md b/docs/designs/issue-watcher-status-pipelines.md
new file mode 100644
index 000000000..f582fe76a
--- /dev/null
+++ b/docs/designs/issue-watcher-status-pipelines.md
@@ -0,0 +1,104 @@
+# Issue watcher: per-status commands, launch levels and completion
+
+**Status:** design note, decided 2026-11-19 (Task 6 of the zero-setup plan `TASK-WF-requirements-20261119-143917-2`). It records the owner's decisions of 2026-11-18 and 2026-11-19 (requirements R23, R24, R25, R29, R31, R32, R33, R34 and R35) and fixes every interface that Tasks 7 to 14 implement. Where a line of code or text is named, it was read on 2026-11-19.
+
+Terms: the **Status** is the Project 2 single-select field `Status`; the **Pipeline** is its single-select field `Pipeline` (`None`, `Worktree`, `Full`, `Full Submit`); the **stage** is the word the watcher derives from the Status (`research`, `spec`, `plan`, `debug`); the **level** is the launch level derived from the Pipeline (`none`, `worktree`, `full`, `full submit`). The **approval** is the issue field `Approved` set to `Yes` (R35, `docs/designs/issue-watcher.md`).
+
+## 1. What acts and what does not (R22, Task 1)
+
+Only an issue whose one live Project item has Status `Research`, `Spec`, `Plan` or `Debug` acts (`predicates.ALLOWED_STATUSES`). `Backlog`, `Ready`, `In progress`, `In review`, `Done`, an empty Status and any status added to the board later never act. **Ready triggers nothing**: no command, no launch.
+
+The Pipeline picks the level: `None` or empty is level `none`, `Worktree` is `worktree`, `Full` is `full`, `Full Submit` is `full submit`. Until the ship gate of Task 8 is opened by a reviewed commit, only level `none` launches; every other level ends `level_gated`.
+
+## 2. The decision table
+
+All four Status pipelines end at **`In review`** (owner, 2026-11-19; held in one named table in `complete.py`, Task 12). Only a `succeeded` outcome moves the Status.
+
+| Status | Command at the stage | Runs as the coordinator's worker? (level `none`) | Level `none` | Level `worktree` | Level `full` | Level `full submit` | End Status |
+|---|---|---|---|---|---|---|---|
+| Research | `/sc:research` | Yes: `src/superclaude/commands/research.md:117` has `## Unattended mode` | worker runs it unattended and reports | agent runs it, writes the report in the issue's worktree, halts, no commit | as `worktree` plus one local commit of the report on the issue branch | as `full` plus push of that branch to `origin` and `/sc:pr-submit --monitor 3` | In review |
+| Spec | `/sc:design` when the issue is well defined, else `/sc:brainstorm` with a handoff to `/sc:design` for high complexity or scope | Yes: `design.md:117` and `brainstorm.md:148` | as above | as above | as above | as above | In review |
+| Plan | `/sc:workflow` | Yes: `workflow.md:80` | as above; stops before `/sc:implement` and `/task` | as above | as above | as above | In review |
+| Debug | `/sc:troubleshoot` | Yes: `troubleshoot.md:169` | worker runs it **without `--fix`** | agent runs it **without `--fix`** (propose next steps, halt) | agent runs it **with `--fix`** (a remediation tasklist package, never an applied code change) | as `full` plus push and PR | In review |
+| Ready | none | not applicable | nothing | nothing | nothing | nothing | unchanged |
+
+None of the five commands is on the never-as-worker list (`src/superclaude/core/WORKER-CONTRACT.md:23`: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn`, `/sc:sweep`, `/sc:swarm-wizard`, and `/sc:pr-submit` while decision D3 holds). Each has an `## Unattended mode` section at the line shown, so no alternative is needed. `/sc:pr-submit` is never a worker command: at level `full submit` the launched agent runs it in its own top-level session, as D3 allows.
+
+**Debug at level `none`.** The coordinator's worker runs `/sc:troubleshoot` without `--fix`, because a level `none` worker stops before any code change; code-affecting remediation starts only at `full` and `full submit`. The worker brief is used only at level `none`; at the other levels the launched agent runs the command from its launch prompt, so the brief has no level slot.
+
+**What `--fix` does.** `src/superclaude/commands/troubleshoot.md:54`: `--fix` offers the Tier 3 remediation chain (`/sc:workflow` produces a tasklist package; the user runs `/sc:implement`); code changes never auto-apply. At `full` the agent therefore leaves a remediation package, not a code change.
+
+## 3. The launch prompt (decision 1)
+
+The watcher sends one of these prompts to `orca agent launch --prompt`. The stage is derived from the Status read by `_revalidate`; the level from the Pipeline.
+
+| Level | Prompt for stage `research` (the others replace the last word) |
+|---|---|
+| none | `/sc:issue --claim <N> --pipeline none --stage research` |
+| worktree | `/sc:issue --claim <N> --pipeline worktree --stage research` |
+| full | `/sc:issue --claim <N> --pipeline full --stage research` |
+| full submit | `/sc:issue --claim <N> --pipeline full --submit --stage research` |
+
+Stages: `research`, `spec`, `plan`, `debug`. `--stage` is a new claim-only option of `/sc:issue` (Task 10); `--submit` stays valid only after `--pipeline full`. The launch-level guard has no prompt allow-list, so the pin is the pattern in `launch.py`, which replaces `PROMPT_PATTERN` (line 33):
+
+```
+^/sc:issue --claim [1-9][0-9]{0,8} --pipeline (?:none|worktree|full(?: --submit)?) --stage (?:research|spec|plan|debug)$
+```
+
+`build_claim_prompt` (line 84) takes the issue number, the stage and the level and raises `ValueError` for any input that does not match, so no other text reaches `--prompt`. `launch_argv` (line 95) and `retry_argv` (line 119) keep refusing a prompt that does not fullmatch the pattern. The prompt is built from the item that `_revalidate` rereads (Task 7), so a Status or Pipeline moved between examine and launch cannot launch the old command.
+
+## 4. Which session runs the Status command (decision 3)
+
+- **Level `none`.** The watcher's claim session assigns the issue, posts its two marked comments and writes `.dev/issues/<N>/issue-summary.md` and `next-steps.md`; it creates no worktree and starts no agent. The coordinator then reads the claim's stage, creates the worktree and starts one worker from the worker brief, whose `Command:` line carries the stage's command (section 7).
+- **Levels `worktree`, `full`, `full submit`.** `/sc:issue --claim` creates the worktree and launches an agent in it. The stage command enters the agent's `launch-prompt.md` (written by the claim from `templates/next-steps.md`, Task 10): its first step is the stage command in the form of the table above, its last step is writing `.dev/issues/<N>/result.md`, and it states that only the coordinator writes to an issue, a label or a Project (section 8). The agent runs the command from that prompt.
+
+## 5. How the Status and Pipeline reach the coordinator (decision 4)
+
+A `--pipeline none` claim writes no worktree record. The watcher stores the stage and the level in the claim's `.dev/issues/<N>/next-steps.md` header lines (`stage: <word>` and `level: <word>`) next to the existing summary, and the coordinator reads them there, in the checkout that ran the claim, with the `claimed` entry of `dispatch.json` read-only. The coordinator never trusts a Status it remembers: it rereads the Project item through `stage-status` at each gate, which also reads the approval and the plan reply.
+
+## 6. "Well defined" for Spec (decision 5)
+
+The claim worker that writes `issue-summary.md` judges it, from the Complexity issue field and the summary text: `Simple` or `Medium` with a stated acceptance criterion is well defined (`/sc:design`); anything else, or `Complex`, is not (`/sc:brainstorm`, with a handoff to `/sc:design` for high complexity or scope). It records the verdict and the reason in one line of `issue-summary.md` (`spec-route: design|brainstorm — <reason>`). No code judges it and no issue text reaches the brief.
+
+## 7. The worker brief (levels `none` only)
+
+`src/superclaude/cli/issue_pipeline/templates/worker-brief.txt` and `brief.py` carry one row per allowed Status instead of one row per complexity. The brief's `Command:` line is the command of the Status (the table), built from a closed template; the issue number is a validated integer and the Status a closed set, so no issue text reaches the brief. The brief states that after the coordinator mirrors the Status or moves it to `In review`, the Project values have changed, so any relaunch needs a fresh approval (section 9). `brief.py` keeps the closed-set checks and refuses a bad Status, issue number or nonce with a closed reason. The Debug row at `none` has no `--fix`.
+
+## 8. The approval record (decision 6, R19, R29, R35)
+
+"Automatic approval record" of R19 means the **claim-time approval already kept in `dispatch.json`** (`approver_id`, `approval_event_id`, `approved_at`, now taken from the `Approved` field event) plus the **adoption row** (`adopt-create`). It is not the plan-hash approval row. The plan-hash row (`approval_record.py`, `record_create`) is created only from a worker's `ask` that carries the plan hash (WC-17, R29). A claim-time event is refused as plan approval in `src/superclaude/cli/issue_pipeline/stage_predicates.py` (rule `label-before-plan`, lines 161 to 170, through `stage-status`), because `approval_record.record_create` cannot tell the two events apart and is not changed. The coordinator calls `record-create` only with evidence that `stage-status` reports as accepted. Task 11 tests this where it is enforced, in `tests/issue_pipeline/test_stage_predicates.py` and `test_stage_status.py`.
+
+## 9. The completion update (R24, decision 7)
+
+Only the coordinator writes to an issue, a label or a Project item, and only under that issue's grant row (`WORKER-CONTRACT.md` lines 241 to 243 and 300). An agent launched at any level and every worker reports through its result file and never runs `issue-pipeline complete`.
+
+- **How the coordinator learns a run finished.** At level `none`: the worker's `worker_done` contract. At the other levels: the result file `.dev/issues/<N>/result.md` in the issue's worktree, noticed by the `/sc:sweep` report the coordinator already reads at each wake (WC-16).
+- **Closed format of `result.md`.** Three lines, no free text: `outcome: succeeded|failed|blocked|partial`, `artifacts: <repo-relative paths, comma separated, may be empty>`, `pull_request: <number or none>`. The coordinator reads only these three keys; nothing else of the file is posted. The run id (the approval event id) is not in the file: the agent cannot know it and must not choose it, so the coordinator takes it from the issue's entry in `dispatch.json` (Task 10 amended this from four lines).
+- **The result comment.** One comment per run, carrying the per-run marker `<!-- sc:issue:result issue=<N> run=<approval_event_id> -->` and the outcome word, the artifact paths and the pull request number. The marker never contains the claim marker. The approval event id keys it because each relaunch needs a fresh approval, so a second run has a different id; a marker already written by the coordinator's own login for the same run suppresses a second comment (idempotency).
+- **Only `succeeded` moves the Status**, with a compare-and-set: the Status moves only from `Research`, `Spec`, `Plan` or `Debug`; any other current Status (for example a person moved it to `Done`) posts the comment and returns `status_moved_by_person` without a move. A `failed`, `blocked` or `partial` outcome posts the comment only. The end Status comes from one table keyed by the allowed Status (all four `In review`), so an exception is a one-line change. The read then write is not atomic; the module says so.
+- **Effect on the approval.** The coordinator's own comment never voids an approval (comments by the watcher's own login are skipped, `predicates.py` `unchanged_since`). Its move to `In review` changes the Status value time, so it voids the approval by design (R31): a retry or relaunch needs a fresh `Approved` set after the last Project change, and `In review` fails `project_check`, so the owner moves the Status back first. The same holds for the coordinator's mirror of the Status at line 298 of the duties.
+
+## 10. The Full Submit push rule (decision 8)
+
+`WORKER-CONTRACT.md` line 245 gets this sentence in place of the current one: "At Full Submit the launched agent pushes only its own feature branch to origin and opens the pull request through /sc:pr-submit; the owner's Pipeline value plus an approval later than the last Project change is the go for that issue only. The coordinator never pushes worker commits on that basis; for every other push the rule above stands." Task 11 applies it and tests that no coordinator push grant is tied to the Pipeline.
+
+## 11. Which sessions the guard governs (decision 10)
+
+Governed means a session with a record in the launch-level store: the agents launched at `worktree`, `full` and `full submit`, and bound workers. Not governed: the watcher-launched `--pipeline none` claim session and the coordinator. The claim session's two marked comments are allowed by design; it reads untrusted issue text under the launch login. The counted marker login is the **workspace's single `gh` login**, shared by the watcher, the coordinator and launched agents; the guard (Task 13) is a text check on `gh` commands and cannot tell them apart by login, so the complete control is a token without issues or projects write for launched agents (a Coder row, Task 27).
+
+## 12. Files that change in Tasks 7 to 14 (by path)
+
+| Task | Files |
+|---|---|
+| 7 | `src/superclaude/cli/issue_watch/launch.py`, `src/superclaude/cli/issue_watch/cycle.py`, `src/superclaude/cli/issue_watch/predicates.py`, and the seven test files `tests/issue_watch/test_cli.py`, `test_cli_e2e.py`, `test_crash_injection.py`, `test_cycle.py`, `test_launch.py`, `test_no_text.py`, `test_security_invariants.py` |
+| 8 | `src/superclaude/cli/issue_watch/launch.py`, `cycle.py`, `audit.py`, `tests/hooks/test_launch_level_observations.py`, `tests/issue_watch/test_cycle.py`, `test_audit.py` |
+| 9 | `src/superclaude/cli/issue_watch/predicates.py`, `cycle.py`, `cli.py`, tests under `tests/issue_watch/` |
+| 10 | `src/superclaude/commands/issue.md`, `src/superclaude/skills/sc-issue-protocol/SKILL.md`, `refs/claim.md`, `templates/next-steps.md`, `tests/commands/test_issue_command.py`, `tests/skills/test_issue_protocol.py`, and the docs that quote the old prompt |
+| 11 | `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/cli/issue_pipeline/templates/worker-brief.txt`, `brief.py`, `tests/skills/test_worker_contract.py`, `tests/issue_pipeline/test_brief.py`, `test_stage_predicates.py`, `test_stage_status.py` |
+| 12 | `src/superclaude/cli/issue_pipeline/complete.py` (new), `tests/issue_pipeline/test_complete.py` (new), `tests/issue_watch/test_security_invariants.py` |
+| 13 | `src/superclaude/hooks/scripts/launch-level-guard.sh`, `plugins/superclaude/hooks/scripts/launch-level-guard.sh`, `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`, the guard and issue-worktree tests |
+| 14 | `src/superclaude/cli/issue_pipeline/cli.py`, `src/superclaude/core/WORKER-CONTRACT.md`, `tests/issue_pipeline/test_complete_cli.py` (new), `tests/skills/test_worker_contract.py` |
+
+## 13. Ship-gate note (Task 8)
+
+`docs/designs/sc-issue-launch-level-hook.md` line 201 limits observation item 1 to `full` and `--submit`, while `refs/claim.md` line 133 asks for an observation of item 1 before any governed claim. One boolean, `GOVERNED_LEVELS_ALLOWED`, follows the stricter text (no governed level launches until the observations pass). A per-level split stays an owner option.


Codegraph context
index_state: fresh
checked_at: 2026-11-19T15:32:25Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb
projectPath: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff (Grep, read): src/superclaude/core/WORKER-CONTRACT.md line 293 still names `/sc:issue --claim <N> --pipeline none` in the coordinator duties; the plan reserves that file to Tasks 11 and 14 (its same-file ordering constraint lists WORKER-CONTRACT.md for Tasks 11 and 14 only), and Task 11 rewrites that section to cover claims at every level, so this task leaves it. The remaining `--pipeline none` hits in docs and tests are examples of the command or negative cases, not claims that it is the only watcher prompt. render_prompt gained an optional stage argument; with no stage it renders the old blocks plus the common-block sentence and the closing result block. `make sync-dev` and `make verify-sync` are clean; no path under .claude/ is staged. tests/commands and tests/skills: 2532 passed, 2 skipped; tests/issue_watch and tests/issue_pipeline passed earlier in the task (the final wide run is still going). The design note section 9 now says result.md has three lines (the run id comes from dispatch.json).

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
