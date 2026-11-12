# Synthesis 02: Directory Structure and Data Flow (template sections 3 and 4)

**Task:** TASK-TECHREF-orchestration-20261110-050239
**Output:** `.dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239/synthesis/synth-02-data-flow.md`
**Status:** Complete
**Date:** 2026-11-12
**Sections owned:** 3 Directory Structure (3.1 File Naming Conventions); 4 Data Flow (4.1 Primary Data Flow, 4.2 Data Sources, 4.3 Data Transformations)
**Template:** `.claude/templates/documents/technical_reference_template.md` (Heavyweight tier; read before writing; headings and table columns follow it)
**Primary research read:** `research/02-lifecycle.md`, `research/04-launchers.md`, `research/05-orca-provenance.md`, plus the routed `research/03-guards.md`, `research/06-distribution-evidence.md`, `research/gap-P3-G01.md`, `G03`, `G04`, `G05`, the register `gaps-and-questions.md` and `synthesis/evidence-routing.md`. Source lines quoted below were re-read from the live files on 2026-11-12 (batched read-only scripts); where a statement rests only on a research file it says so.

**Evidence classes and tags** are those of the legend in section 1 (Overview): INSTALLED-FILES means Orca build files under `/opt/Orca/resources/app.asar.unpacked/out/`; HOST-INSTALLED means the `~/.claude/` copies and host settings. ORCA-CHECKOUT here is `/home/coder/workspaces/IronOrca`, `main`, commit `dc57b3d6e81c9825446a520bf0aee8600a2f5586`, clean tree.

**Boundaries held in this file.** Subordinate (sub-orchestrator) mode is deferred and never shipped; no diagram or table here describes it as a flow. No installation rollout and no answer to the future-role question is claimed. The launch-level guard recognizing only the command word `orca` is a recorded DEFECT (section 4.1.3) linked to `.dev/tasks/to-do/TASK-FIX-launch-guard-orca-names-20261111-235205/TASK-FIX-launch-guard-orca-names-20261111-235205.md` (a documentation-only draft plan; not a fix). Checkout, installed copies, origin/master, Orca checkout and the running build are kept apart throughout.

---

## 3. Directory Structure

Four separate locations matter and they are not the same tree: the IronClaude checkout (source of truth), the host's installed copies (what `superclaude install` and Orca wrote), Orca's own sources, and runtime state directories that scripts create. Each tree below lists only paths that a cited source names; there are no file counts (template rule, key numbers live in Section 1). Tags in comments: [C] checkout, [I] installed host copy, [O] ORCA-CHECKOUT, [OI] Orca INSTALLED-FILES.

### 3.0 Checkout tree (CHECKOUT, HEAD `5bdb01681`, branch `ironbelly/design-doc-shim-title-check`)

```
IronClaude/ (worktree root)
├── CLAUDE.md                                   # project rules (NORMATIVE); ownership sentence is an uncommitted edit
├── src/superclaude/                            # source of truth for everything that is installed
│   ├── core/
│   │   ├── WORKER-CONTRACT.md                  # NORMATIVE: terms, WC rules, coordinator rules (sec. 4), brief template (sec. 5)
│   │   ├── CLAUDE.md                           # NORMATIVE: "Orca session launches", ownership wording; imports only the bash policy (@ line 3)
│   │   └── HOW-WE-WORK.md                      # routing guide; points at the contract; not auto-loaded
│   ├── commands/
│   │   ├── <name>.md                           # converted commands carry "## Unattended mode" (report dir, Contract bullet)
│   │   └── implement.md                        # no unattended text: no worker-contract producer today
│   ├── hooks/
│   │   ├── hooks.json                          # registrations: guards and ccsession hooks, installed paths under ~/.claude
│   │   └── scripts/
│   │       ├── require-orca-worktree-agent.sh  # PreToolUse(Bash): "orca worktree create" needs --agent
│   │       ├── launch-level-guard.sh           # L1 guard: UserPromptSubmit + PreToolUse
│   │       └── launch-job-identity.sh          # PreToolUse(Bash) identity adapter and job runner
│   ├── cli/
│   │   ├── main.py                             # install / update / doctor entry points
│   │   ├── install_core.py, install_hooks.py, install_user_setup.py, install_ccsession.py, doctor.py
│   │   ├── issue_watch/{launch.py, cycle.py, cli.py}   # watcher: non-worker launch path B (no worker start)
│   │   └── reflect/contract.py                 # reads reflect's OWN return-contract.yaml; ignores worker keys
│   └── skills/
│       ├── sc-issue-protocol/
│       │   ├── SKILL.md, refs/claim.md, templates/launch-prompt.md
│       │   └── scripts/orca_worktree.py        # claim path A: worktree create, agent launch, shim check
│       ├── ccsession-tag/
│       │   ├── ccsession, ccsession-orca, README.md
│       │   └── hooks/{session-start.sh, session-name.sh}
│       ├── sc-workflow-protocol/refs/return-contract.md    # workflow package contract + worker contract text
│       └── sc-implement-protocol/scripts/archive_workspace.py   # reads the PACKAGE contract only
├── tests/
│   ├── skills/{test_worker_contract.py, test_issue_orca_worktree.py}   # static text pins; fake orca
│   ├── hooks/{test_launch_level_guard.py, test_require_orca_worktree_agent.py, test_launch_job_identity.py, test_launch_level_observations.py}
│   └── issue_watch/, unit/{test_ccsession_tag.py, test_install_ccsession.py}, core/, cli/{test_install_user_setup.py}
├── docs/{designs/, getting-started/installation.md, developer-guide/}
├── plugins/superclaude/{hooks/, commands/, core/}   # mirror, NOT equivalent: core/ has no WORKER-CONTRACT.md or CLAUDE.md
├── .claude/                                    # gitignored sync-dev copy (NORMATIVE, project CLAUDE.md); settings.json is the only tracked file
└── .dev/{tasks/{to-do,done}/, orca-command-refactor/specs/, issues/<N>/}
```

Evidence: every file path above was checked for existence on 2026-11-12 (batched read-only existence script, no path missing; `plugins/superclaude/core/` exists and holds `BUSINESS_PANEL_EXAMPLES.md`, `BUSINESS_SYMBOLS.md`, `CODEGRAPH.md`, `PRINCIPLES.md`, `RESEARCH_CONFIG.md`, `RULES.md`, `__init__.py`, with no `CLAUDE.md` and no `WORKER-CONTRACT.md`; the plugin tree has no `ccsession-tag` README; Orca skill folders `orchestration`, `orca-cli`, `computer-use` are absent from `src/superclaude/skills/`). The plugin build carries `## Unattended mode` in only two commands, `recommend.md` and `workflow.md` (Grep of `plugins/superclaude`). `core/CLAUDE.md:3` is the only `@` import (`@BASH_INSPECTION_POLICY.md`), so the worker contract is never auto-loaded. [CODE-VERIFIED]

### 3.0.1 Installed host copies and runtime state (HOST-INSTALLED; the research host only)

```
$HOME
├── .claude/
│   ├── CLAUDE.md, WORKER-CONTRACT.md, HOW-WE-WORK.md     # [I] copied from src/superclaude/core by install_core
│   ├── hooks/{launch-level-guard.sh, launch-job-identity.sh, require-orca-worktree-agent.sh, launch-level-pre-push.sh}   # [I] flat copies of hooks/scripts/; the pre-push copy equals origin/master, HEAD has no such script
│   ├── settings.json                                     # [I] user-level hook registrations (re-read with jq 2026-11-12: guard on both events, gate, identity hook; see synth-04 9.1)
│   ├── skills/
│   │   ├── ccsession-tag/, sc-issue-protocol/scripts/orca_worktree.py      # [I] copied by the generic skill installer
│   │   ├── orchestration, orca-cli                       # symlinks into ../../.agents/skills/ (Orca-written, not shipped by IronClaude)
│   │   └── computer-use/                                 # real directory (Orca-written)
│   ├── state/launch-level/{pending/<nonce>, sessions/<session_id>[.ok], jobs/<kernel session id>.json}
│   ├── projects/<key>/topics/<name>.txt                  # ccsession name lists
│   └── ccsession.env
├── .agents/skills/<name>/SKILL.md                        # Orca writes the stubs here, then links them into ~/.claude/skills
├── .local/bin/{ccsession, ccsession-orca, orca-ide}      # first two link into the ccsession-tag skill; orca-ide links to /opt/Orca
├── .local/state/ccsession/orca-tabs/<pane key>           # tab record: session id, launch folder, terminal handle
├── .cache/ccsession/orca-titles/<terminal handle>        # title mark: the exact title ccsession set
└── .config/orca/linux-orca-cli-shim/                     # Orca's CLI shim directory
```

- Core files: `install_core.py:14-29` lists the twelve known core names, including `WORKER-CONTRACT.md`, `CLAUDE.md` and `HOW-WE-WORK.md`; `install_core.py:70-72` skips an existing destination unless `force`. [CODE-VERIFIED, CHECKOUT]
- Hook scripts: `install_hooks.py:86-94` names the three guard scripts; `:264-273` pairs each with a flat destination name, `:279-281` skips an existing file unless `force`, `:284-285` copies with `copy2` then `chmod 0o755`; `hooks.json:110,120,130` register them as `~/.claude/hooks/<name>.sh`. A plain `superclaude install` therefore keeps an older installed script silently. [CODE-VERIFIED, CHECKOUT]
- Orca-written files: IronClaude ships no `orchestration`, `orca-cli` or `computer-use` skill; `install_user_setup.py:34` names them and `:243-245` builds `[orca, "skills", "install", "--agent", "claude-code", "--skill", ...]`. Orca owns the bytes and the link layout (`research/gap-P3-G03.md` A.5, F.1: shared folder `~/.agents/skills` first, then a link into each agent folder; ORCA-CHECKOUT, not re-read here). [CODE-VERIFIED for the request, CHECKOUT; Orca's write behavior ORCA-CHECKOUT via research]
- Runtime state: the pending record path is `$HOME/.claude/state/launch-level/pending/<nonce>` (`orca_worktree.py:51-53` docstring, `PENDING_PARTS` at `:773`); the guard reads `$LL_STORE/sessions/$LL_SID` (`launch-level-guard.sh:257`); the identity runner keeps job records in a `jobs` subdirectory of its store (`launch-job-identity.sh:222`). The ccsession state locations (`orca-tabs`, `orca-titles`, name lists) are from `research/gap-P3-G05.md` F2.2, F2.4, F8 (`ccsession:518-525`, `:564-572`, `:387`), not re-read. [CODE-VERIFIED for the first three; the rest research-sourced]
- Existence re-check 2026-11-12: all host paths in the tree above exist except those not checked (`state/launch-level/jobs/`, `projects/<key>/topics/`, the per-handle files). Host symlink targets and modification times are research observations (`research/gap-P3-G03.md` F.3, 2026-11-11), a moment-in-time fact about one host. [CODE-VERIFIED for existence; DEPLOYED-RUNNING unobserved]

### 3.0.2 Orca trees (ORCA-CHECKOUT and Orca INSTALLED-FILES; a different repository)

```
/home/coder/workspaces/IronOrca/            # [O] main at dc57b3d6e..., version 1.4.214, clean tree
└── src/
    ├── cli/specs/{orchestration.ts, orchestration-worker-specs.ts, core.ts}    # verb syntax and help text
    ├── shared/{nested-worker-depth.ts, orchestration-heartbeat.ts}             # depth and heartbeat settings
    └── main/runtime/
        ├── rpc/methods/orchestration/
        │   ├── worker/{workers.ts, worker-start-authority.ts, local-worker-start.ts, deliver-worker-dispatch-preamble.ts}
        │   └── messaging/{send-methods.ts, ask-methods.ts}
        └── orchestration/{preamble.ts, dispatch-report-mailbox.ts, lifecycle-reconciliation.ts, db/{dispatch-context/, tasks/}}

/opt/Orca/                                  # [OI] version 1.4.245-aidev02.9cfecdd30b2a, commit 9cfecdd30b2a...
├── resources/bin/orca-ide                  # launcher
└── resources/app.asar.unpacked/out/{package.json, cli/, shared/, main/chunks/}   # compiled; main/ is minified
```

Evidence: `/opt/Orca/resources/app.asar.unpacked/out/package.json` records `"name": "orca-compiled-output"`, `"version": "1.4.245-aidev02.9cfecdd30b2a"` and `"commit": "9cfecdd30b2a90c06e5178b1245cb31a97d11bac"` (read 2026-11-12); `git -C /home/coder/workspaces/IronOrca rev-parse HEAD` printed `dc57b3d6e81c9825446a520bf0aee8600a2f5586` and `git status --short` printed nothing. The checkout is an older snapshot (1048 commits behind the installed build's commit, `research/05-orca-provenance.md` section 1); a checkout-only fact is not a statement about the installed files and neither is about the running process. [CODE-VERIFIED]

### 3.0.3 Revision map: which source describes what

| Location | Revision observed 2026-11-12 | What it means for the citations in this file |
|----------|------------------------------|---------------------------------------------|
| CHECKOUT | HEAD `5bdb01681`; seven files carry uncommitted edits (` M`): `CLAUDE.md`, `src/superclaude/core/CLAUDE.md`, `src/superclaude/skills/ccsession-tag/README.md`, `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh`, `plugins/superclaude/hooks/scripts/require-orca-worktree-agent.sh`, `tests/core/test_orca_session_launch_guidance.py`, `tests/hooks/test_require_orca_worktree_agent.py` | `WORKER-CONTRACT.md` is unmodified, so its line numbers hold for HEAD. The ownership wording and the hook block message (`require-orca-worktree-agent.sh:354-355`) hold for the working tree only |
| HOST-INSTALLED (host `~/.claude`) | a mixed set, see the matrix below (`cmp` run 2026-11-12) | no single ref describes it; a statement about "the installed contract" holds for the installed bytes only |
| ORIGIN/MASTER | local ref `930c5ebc8` (committed 2026-11-11 20:32 -0500), read at about 02:14 UTC on 2026-11-12; HEAD is 2 ahead and 23 behind (`git rev-list --left-right --count HEAD...origin/master` printed `2 23`); never fetched by this work, and the local ref moves whenever the fork is fetched, by any actor | History of the earlier values of this ref: the ORIGIN/MASTER row of the legend in section 1. Of the eight repo paths of the matrix below, seven differ between HEAD and `origin/master` (only the Orca-worktree hook script does not), among them `WORKER-CONTRACT.md` (338 lines against 327; new subsection `### Before the first task-create for a command` at `:217`, commit `146be6fc3`) and `orca_worktree.py` (453 insertions and 42 deletions, 495 changed lines); `launch-level-pre-push.sh` (208 lines) exists only on `origin/master`. Anything about the L2 pre-push layer or the coordinator preflight is ORIGIN/MASTER only |
| ORCA-CHECKOUT | `dc57b3d6e81c9825446a520bf0aee8600a2f5586`, clean | source of the Orca citations (`IronOrca/src/...`); older than the installed build |
| Orca INSTALLED-FILES | `1.4.245-aidev02.9cfecdd30b2a` | cited as `/opt/Orca/resources/app.asar.unpacked/out/...`; agreement with the checkout is stated per fact |
| DEPLOYED-RUNNING | not observed | every behavior claim about the live Orca or Claude Code is [UNVERIFIED]: effective settings, hook order and live guard behavior included |

Installed copy against the three sources (read-only `git show <ref>:<path>` piped to `cmp` against the installed file, run at about 02:14 UTC on 2026-11-12). The installed files' ctime is 2026-11-12 01:59:25 UTC: another session installed or updated them after this synthesis was first written. The files keep the source mtime (the installer copies with `shutil.copy2`), so mtime does not show the refresh; `stat -c %z` does. An earlier run of this comparison, before the refresh, gave a different matrix (installed `CLAUDE.md` then equalled HEAD), so every cell is a moment-in-time fact:

| Installed file (`~/.claude/...`) | Repo path | Equals HEAD | Equals origin/master (`930c5ebc8`) | Equals worktree |
|----------------------------------|-----------|-------------|------------------------------------|-----------------|
| `hooks/launch-level-guard.sh` | `src/superclaude/hooks/scripts/launch-level-guard.sh` | no | yes | no |
| `hooks/launch-job-identity.sh` | `src/superclaude/hooks/scripts/launch-job-identity.sh` | no | yes | no |
| `hooks/require-orca-worktree-agent.sh` | `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh` | yes | yes | no (uncommitted message edit) |
| `skills/sc-issue-protocol/scripts/orca_worktree.py` | `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` | no | yes | no |
| `skills/ccsession-tag/README.md` | `src/superclaude/skills/ccsession-tag/README.md` | no | yes | no |
| `CLAUDE.md` | `src/superclaude/core/CLAUDE.md` | no | yes | no |
| `WORKER-CONTRACT.md` | `src/superclaude/core/WORKER-CONTRACT.md` | yes | no (the ref carries the 338-line contract) | yes |
| `HOW-WE-WORK.md` | `src/superclaude/core/HOW-WE-WORK.md` | no | no | no |

Reading: five installed files equal `origin/master` only (guard, identity hook, claim script, ccsession README and `CLAUDE.md`; the installed `CLAUDE.md` carries the LiteLLM rows that `origin/master` gained in commit `ed6074c47`, which HEAD lacks, and still carries the old ownership wording). An installed copy of `hooks/launch-level-pre-push.sh` also exists and equals `origin/master` (`cmp` 2026-11-12); its use as a git hook was not observed. The installed guard, identity hook, claim script and ccsession README are therefore the ORIGIN/MASTER versions, so on this host the claim script is the 1884-line version with the L2 additions, not this checkout's 1473-line file (`wc -l` of the checkout file printed 1473; the installed size is `research/04-launchers.md` F5). The installed `WORKER-CONTRACT.md` equals HEAD, so Flow B below describes the installed contract; it does not include the coordinator preflight that exists on origin/master. `HOW-WE-WORK.md` matched the older origin/master of 2026-11-11 (`research/06` F6, eighth file) and now matches no ref. [CODE-VERIFIED]

### 3.1 File Naming Conventions

Only conventions that a cited source shows are listed. No other naming rule is evidenced and none is invented.

| Pattern | Convention | Example | Evidence |
|---------|-----------|---------|----------|
| Task package id | `TASK-<TYPE>-<slug>-<YYYYMMDD>-<HHMMSS>`; the folder is named by the id and holds `<id>.md`; the folder sits in `.dev/tasks/to-do/` and moves to `done/` on archive | `.dev/tasks/done/TASK-WF-planTheExplicitl-20261110-024937/` (types seen: `WF`, `FIX`, `RESEARCH`, `TECHREF`) | Glob of that folder plus existence checks of the `TASK-FIX-` and `TASK-RESEARCH-` folders, 2026-11-12; archive move: `gap-P3-G04.md` section 2 step 7 (`refs/return-contract.md:33,51`, not re-read) |
| Package contents | `progress.md`, `return-contract.yaml`, `source.md`, `artifacts/final-*.log`, `artifacts/retries/T<n>/prompt-<n>-<k>.md`, `artifacts/retries/T<n>/q0-head` | the `TASK-WF-planTheExplicitl-...` folder above | Glob result, 2026-11-12 |
| Worker report file | fixed name `return-contract.yaml` inside the one report directory the brief names | `<report-dir>/return-contract.yaml` | `WORKER-CONTRACT.md:32` (WC-4) |
| Package contract versus worker contract | two files, same file name, different folders and vocabularies: `<pkg>/return-contract.yaml` (key `status`, read by code) and `<report-dir>/return-contract.yaml` (key `worker_status`, read by no code) | `archive_workspace.py` reads the first only | `research/gap-P3-G04.md` 4.2, 4.4, takeaway 4 |
| Worker handoff files | `<report-dir>/handoff/<n>-<command>.md`, written after each `Command:` line | WC-15 | `WORKER-CONTRACT.md:64` |
| Brief lines | fixed prefixes `Guard:`, `Chain:`, `On a blocked gate:`, `Local commit:`, `Report directory:`, `Worktree:`, `Outward actions:`, `P0 only:`, `Command:` | the text block in section 5 of the contract | `WORKER-CONTRACT.md:288-296`; `P0 only:` is removed on ORIGIN/MASTER (contract diff, 2026-11-12) |
| Contract-internal labels | rules `WC-<n>`; liveness states `S0` to `S11`; ladder steps `L0` to `L5`; ack steps `A1` to `A4`; run-notes labels `pending_ack` and `unacked-at-settlement` | `WC-6`, `S9` | `WORKER-CONTRACT.md:67-165` (states `:116-129`, acks `:131-138`, ladder `:146-155`, re-read 2026-11-12; tabulated in synth-03 5.2 tables B and C); the two run-notes labels appear only in the contract (`research/02-lifecycle.md` 4.2) |
| Issue claim directory | `.dev/issues/<N>/`; the claim copies it file by file into the worktree and keeps `worktree.json` and `launch-prompt.md` there | `<wt>/.dev/issues/<N>/launch-prompt.md` | `orca_worktree.py:20-22,39-40,51-56` |
| Claim worktree identity | Orca worktree name `issue-<N>` with comment `sc:issue <owner/repo>#<N>` | `issue-452` | `orca_worktree.py:674,679` |
| Launch marker and pending record | prompt starts `[sc-launch:v1:<32 hex>]`; the pending file is named by the same nonce | `pending/<nonce>` | `launch-level-guard.sh:318`; `orca_worktree.py:773,1354` |
| ccsession auto label | `<folder cut to 20>[-<up to 4 words, each cut to 12>]-<MMDD>-<HHMMSS>-<4 hex>`; the Orca tab title is `<label> · Claude Code` | `<folder>-sc-launch-v1-<12 hex>-<MMDD>-<HHMMSS>-<4 hex>` | `ccsession:645-662`, `:532`, `:1875` |
| Hook scripts | source `src/superclaude/hooks/scripts/<name>.sh`; installed flat as `~/.claude/hooks/<name>.sh` | `launch-level-guard.sh` | `hooks.json:110,120,130`; `install_hooks.py:264-273` |

---

## 4. Data Flow

### 4.1 Primary Data Flow

Two end-to-end flows exist and they must not be merged. **Flow A (claim flow)** starts a non-worker Claude session in a new Orca worktree and checks that it sits behind ccsession; it never starts a supervised worker. **Flow B (worker flow)** is the supervised path: a person-opened coordinator starts workers, workers report through `worker_done` and a `return-contract.yaml`, and the coordinator admits the result. Only hops that a cited source supports are drawn. Every hop carries one tag:

| Tag | Meaning |
|-----|---------|
| [CODE] | executable code in the CHECKOUT (HEAD plus uncommitted edits) |
| [TEXT] | NORMATIVE instruction text that an LLM session follows; no code runs it |
| [ORCA-SRC] | Orca source, ORCA-CHECKOUT `dc57b3d6e`; INSTALLED-FILES agreement is stated where checked |
| [HOST] | Claude Code or host configuration; not observable here, so [UNVERIFIED] for the running system |

#### 4.1.1 Flow A: claim flow (issue claim, worktree, agent launch, ccsession title, shim check)

```
FIRST HOP
person: /sc:issue --claim <N>  [TEXT]      (path B: timer -> issue-watch once -> the same prompt, no marker  [CODE])
   |
   v
claim session (Claude, Bash tool) runs scripts/orca_worktree.py:
   preflight  -> orca status --json                                                         [CODE]
   worktree   -> orca worktree list, create (no --agent), copy .dev/issues/<N>/, close plain first tab   [CODE]
   launch     -> gates -> write pending/<nonce> -> orca agent launch --prompt "[sc-launch:v1:<nonce>] Read ..."   [CODE]
   |
   v
Orca: opens a PTY tab in the worktree, sets ORCA_PANE_KEY and ORCA_TERMINAL_HANDLE,
      starts its configured Claude command with the prompt as the last argument      [ORCA-SRC; configured command: HOST, UNVERIFIED]
   |
   +--------------------------------+------------------------------------+
   v                                v                                    v
ccsession-orca -> ccsession     Claude Code runs hooks [HOST dispatch]   claim session keeps reading
  --auto-name makes the label     UserPromptSubmit: launch-level-guard     behind_ccsession(handle), 5 tries  [CODE]
  OSC title "<label> . Claude Code"   consumes pending/<nonce> and          orca terminal read --screen
  exec claude --name <label> ...      binds sessions/<sid>  [CODE]          orca terminal show (title)
                                  SessionStart: session-name.sh ->
                                    orca terminal rename (same title) [CODE]
   |
   v
LAST HOP
JSON {status: launched, warning: W-LAUNCH-NOT-CCSESSION when the check fails} read by the skill; "launch" entry
written to <D>/worktree.json; the agent keeps running; sessions/<sid> stays bound until a person deletes it
```

The three branches after the Orca spawn run concurrently; their relative timing (title write against the five reads) was not measured (`research/gap-P3-G05.md` R3). [UNVERIFIED]

| # | Hop | Tag | Evidence | Notes |
|---|-----|-----|----------|-------|
| A1 | First hop: a person runs `/sc:issue --claim <N>`; the skill drives Waves 0 to 8 and calls `orca_worktree.py` in Waves 0, 5, 7 and 8 | [TEXT] | `SKILL.md:84-92` | Waves 1 to 6 (GitHub and ClickUp work, summaries, comments) are outside the Orca data flow and were not traced here |
| A1b | Path B first hop: the watcher builds a 12-element `orca agent launch` with prompt `/sc:issue --claim <n>` in a configured checkout | [CODE] | `launch.py:95-116`; `research/04-launchers.md` F2 (`cli.py:111-137`, `cycle.py:1026-1112`) | The watcher prompt carries no `[sc-launch:v1:...]` marker, so that first session is ungoverned at that hop; it then runs Flow A. The chained run was not observed [UNVERIFIED] |
| A2 | `preflight`: `orca status --json` must exit 0 with `ok: true` and a reachable runtime | [CODE] | `orca_worktree.py:15-18` | Failure is `E-ORCA-REQUIRED`, a STOP before any GitHub or ClickUp write (`research/04-launchers.md` F1) |
| A3 | `worktree`: list, look up, else `orca worktree create --repo path:<main> --name issue-<N> --base-branch <base> --no-parent --comment "sc:issue <repo>#<N>" --json`. There is no `--agent` and no `--prompt` | [CODE] | `orca_worktree.py:666-682`; docstring `:25-31` | Design record: the create keeps no `--agent` because the claim must copy `<D>` and write the pending record before the agent starts (`docs/designs/sc-issue-claim-pipeline-flag.md:194`; amendment `:11`). An accepted exception recorded 2026-11-08; the unqualified rule text "every Orca worktree gets an agent" does not name it (owner question C1, open) |
| A4 | Copy `<D>` (`.dev/issues/<N>/`) file by file into the worktree, write `<D>/worktree.json`, then close Orca's plain first tab only when exactly one agent-less terminal is listed | [CODE] | `orca_worktree.py:20-22,31-37` | A tab that cannot be closed is the cosmetic warning `W-FIRST-TAB-LEFT` |
| A5 | `launch` gates before any agent: duplicate-launch guard, stale prompt, the IR-4 enforcement preflight (needs `jq`, `uv`, Linux, the installed guard and its registrations), L2 status | [CODE] | `orca_worktree.py:45-51`; gates `:1244-1336` (`research/04-launchers.md` F1) | IR-4 verifies the claim process only, not the environment of the agent Orca starts. A failed IR-4 is `W-ENFORCEMENT-ABSENT` and no agent. HEAD says L2 is a warning only (`W-L2-ABSENT`); the installed script adds an L2 step that this file did not trace |
| A6 | Write `$HOME/.claude/state/launch-level/pending/<nonce>` (32 hex), then `orca agent launch --agent claude --worktree path:<wt> --surface terminal --prompt "[sc-launch:v1:<nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it." --json` | [CODE] | `orca_worktree.py:51-53,773,1351-1355` | On failure the pending record is deleted and a hand command printed (`research/04-launchers.md` F1 step 7). The call uses the bare name `orca` |
| A7 | Orca spawns the tab, sets `ORCA_PANE_KEY` and `ORCA_TERMINAL_HANDLE`, and starts the configured Claude command with the prompt appended as the last argument (prompt mode `argv`) | [ORCA-SRC] | `research/gap-P3-G05.md` F6 and R1 (`tui-agent-config.ts:22-34`, `tui-agent-startup.ts:108-116`, `spawn-pane-env.ts:46-63`; read in the Orca checkout, not re-read) | Whether the host's Claude command is `ccsession-orca` is a user setting that no code writes (`install_ccsession.py` only links `~/.local/bin/ccsession-orca`; `research/gap-P3-G03.md` B.1). [UNVERIFIED] on every host |
| A8 | Guard binds the session on its first prompt: strict marker regex, nonce must be a regular non-symlink file in an owned `pending/`, one `mv` consumes it, `ln` publishes `sessions/<sid>` holding `worktree`, `full` or `full-submit` | [CODE] and [HOST] | `launch-level-guard.sh:318,334-337,375-378,304-305`; registrations `hooks.json:63-71` (UserPromptSubmit) and `:115-124` (PreToolUse) | Matching hooks run in parallel and completion order is non-deterministic (DOCUMENTED, https://code.claude.com/docs/en/hooks, `research/web-01-claude-code-hook-execution.md:45,76,93`). The 12 live observation tests in `tests/hooks/test_launch_level_observations.py` are skipped, so the guard in a live session is [UNVERIFIED] (`gaps-and-questions.md` section B) |
| A9 | `ccsession-orca` calls `ccsession --auto-name "<prompt>"`, then `exec ccsession --name "<label>" --shim --claude-args ...`; ccsession prints the OSC title `<label> · Claude Code`, then `exec claude ... --name "<label>" ... <prompt>` | [CODE] | `ccsession-orca:225-229,247`; `ccsession:645-662,1869,1875,1969-1973` | A prompt-carrying launch is never asked a name question (`research/gap-P3-G05.md` F1). `CCSESSION_NAME` set, a Claude `--name`, or an unwritable name list gives a label that does not fit the title pattern (same file, F9 causes 3) |
| A10 | `session-start.sh` then `session-name.sh` run `ccsession --sync-name`, which calls `orca terminal rename --terminal "$ORCA_TERMINAL_HANDLE" --title "<label> · Claude Code"`; it acts only when `CLAUDE_CODE_DISABLE_TERMINAL_TITLE=1` and `ORCA_PANE_KEY` is non-empty | [CODE] and [HOST] | `hooks.json:33-42,54-62,73-82`; `ccsession:527-539`; chain `research/gap-P3-G05.md` F3, F9 step 8 | Hook timeout is 5 s for all three registrations. The rename and the OSC title carry the same text, so either route yields the title |
| A11 | Shim check: up to 5 tries, `SC_ORCA_SHIM_INTERVAL` apart (default 2.0 s): `orca terminal read --terminal <h> --screen --json` for the markers `[ccsession]` or `Session name (Enter or Ctrl+C`, then `orca terminal show` for a title matching `sc-launch-v1-[0-9a-f]{1,12}-\d{4}-\d{6}-[0-9a-f]{4}\b` | [CODE] | `orca_worktree.py:774-782,1142-1161` | The second screen marker is stale against the current ccsession question text [CODE-CONTRADICTED] (`research/gap-P3-G05.md` F4.4; owner question C17). No test joins the `--auto-name` output to the title pattern (same file, R8). Worst case if every call hangs is 158 s, arithmetic from the constants and not a measurement |
| A12 | Last hop: result JSON `status: launched`; a failed check adds warning `W-LAUNCH-NOT-CCSESSION`; the `launch` entry is written to `<D>/worktree.json`; nothing closes or stops the agent | [CODE] | `orca_worktree.py:1389` (record_launch); warning block `:1377-1386` (`research/04-launchers.md` F1 step 8) | The warning's "close it" is an instruction to the person. The `sessions/<sid>` binding is released only by a person deleting `sessions/<sid>` and `.ok` (`research/03-guards.md` C.6 item 5) |

Neither launcher is a supervised-worker launcher: `orca_worktree.py` and `launch.py` contain no `orchestration`, `worker-start`, `dispatch` or `task-create` call. [CODE-VERIFIED] (negative result, `research/04-launchers.md` F1, F2, F4 B1). The worker-side bans on launching (WC-8, WC-13, never-as-worker) are instruction text with no code refusal on the launcher path (same file, B2).

#### 4.1.2 Flow B: worker flow (dispatch preamble, heartbeat, `worker_done`, `return-contract.yaml`, coordinator wait and sweep)

Role split in this flow: the coordinator is "an Orca coordinator session the person opened" (`WORKER-CONTRACT.md:69`); a worker is a session that received an Orca preamble carrying a Task ID and a Dispatch ID (`:11`). No IronClaude code implements the coordinator loop or any worker duty. The executable parts are Orca's (ORCA-CHECKOUT; installed-file agreement is stated per fact in 4.2) and the Python that touches nearby contracts (4.3). Subordinate or sub-orchestrator coordination is not a hop in this flow.

```
FIRST HOP
person opens a coordinator session; it reads ~/.claude/WORKER-CONTRACT.md (nothing loads it automatically)   [TEXT, HOST]
   |
   v
coordinator: task-create --spec "<brief>" (one brief per Task, unique report dir)                       [TEXT; verb: ORCA-SRC]
   |
   v
coordinator: worker-start (never --retry-of)                                                            [TEXT]
   Orca: workerStart handler -> resolveWorkerStartRun (coordinator path) -> createStartingWorkerDispatch   [ORCA-SRC]
   |
   v
Orca types the dispatch preamble + TASK into the worker's terminal (sendAgentTurn)                       [ORCA-SRC]
   |
   v
worker (top-level Claude session)                                                                       [TEXT]
   brief guard on each Command: line -> run each command through its Skill (WC-7)
   skill LLM writes <report-dir>/return-contract.yaml (+ handoff files)
   heartbeat per preamble (only when the setting is on)   ----> Orca records last_heartbeat_at           [ORCA-SRC]
   ask / check per preamble                               ----> run mailbox or creator mailbox          [ORCA-SRC]
   worker_done --outcome succeeded|failed --report-path <contract> (exactly once) -> Orca settles Task    [TEXT; settlement ORCA-SRC]
   |
   v
coordinator: check --wait --types <9 types> --timeout-ms 300000 ; handle batch ; run-notes ; --ack        [TEXT]
             sweep (<= every 5 min): worker-list, worktree ps --agent-wait, stat contract paths          [TEXT]
   |
   v
LAST HOP
coordinator opens return-contract.yaml, admits succeeded / partial / failed / blocked, then creates
dependents with --deps or retries as a NEW Task; commits and publishes only on the person's instruction  [TEXT]
```

| # | Hop | Tag | Evidence | Notes |
|---|-----|-----|----------|-------|
| B1 | First hop: the person opens the coordinator. The contract defines the coordinator as person-opened; nothing in the checkout loads the contract into that session (`core/CLAUDE.md:3` imports only the bash policy; `HOW-WE-WORK.md` is "not loaded automatically") | [TEXT] and [HOST] | `WORKER-CONTRACT.md:67-69`; `research/02-lifecycle.md` 6.1 | Hooks searched: only the three guard scripts and `hooks.json`; other injection paths [UNVERIFIED] (`gaps-and-questions.md` section B) |
| B2 | Task and brief: `task-create --spec` with the brief template; seven required brief contents; the Task's brief cannot change after creation (`task-update` changes only `--status` and `--result`) | [TEXT]; verb flags [ORCA-SRC] | `WORKER-CONTRACT.md:73,81-93,283-297`; `IronOrca/src/cli/specs/orchestration.ts:166-174` (via `research/02-lifecycle.md` section 2 table) | The installed contract lists the `P0 only:` brief line (`:295`); ORIGIN/MASTER removes it and adds a coordinator preflight before the first `task-create` for a command (`### Before the first task-create for a command`, commit `146be6fc3`). Neither is code |
| B3 | Brief guard: the worker checks each `Command:` line against its loaded command copies and refuses with a body starting `guard refused:` | [TEXT] | `WORKER-CONTRACT.md:16-22`; coordinator side `:244` | No code implements it; its behavior in a live worker was not observed (`gaps-and-questions.md` section B) |
| B4 | `worker-start`: the handler resolves the run from the bound coordinator, then starts the worker and its Dispatch. A caller that is not the bound coordinator is accepted only as a worker on an active Dispatch (helper path), which the contract bans (WC-13) | [TEXT] for the call; [ORCA-SRC] for the handler | `worker-start-authority.ts:20-48`; `workers.ts:42-47`; contract `:62,73` | Helper start is gated by `nestedWorkerMaxDepth`: default 1 in the ORCA-CHECKOUT (`nested-worker-depth.ts:4`, refuses a worker's helper start), default 2 in INSTALLED-FILES (`out/shared/nested-worker-depth.js:10`, allows one level); the running setting is [UNVERIFIED]. At the installed default the only barrier is WC-13, which is text |
| B5 | Preamble: `buildDispatchPreamble` builds the text with identity lines, `worker_done`, optional heartbeat, `ask`, `check` and `check --ack` commands; the terminal copy is typed with `sendAgentTurn`. The CLI word is `orca-dev` in dev mode, else the `cliCommand` value, else `orca` | [ORCA-SRC] | `preamble.ts:52-56,63-66,92-106`; `deliver-worker-dispatch-preamble.ts:100-109`; installed chunk agrees on the CLI word and verbs (`research/gap-P3-G01.md` S8, not re-read) | The preamble is "the authority for Orca verb syntax and heartbeat cadence" (`WORKER-CONTRACT.md:7`). It names no IronClaude file and no `return-contract.yaml` |
| B6 | Worker duties: top-level session only (WC-7), each `Command:` run through its Skill, no Orca fan-out (WC-13), handoff files after each command (WC-15), no turn ends between chain steps (WC-14) | [TEXT] | `WORKER-CONTRACT.md:60-64` | Contract-level only; the test file pins phrases, not behavior (`research/02-lifecycle.md` 6.2) |
| B7 | Result file: the command's skill has the LLM write `<report-dir>/return-contract.yaml` with the WC-4 keys on every outcome, in one of four layouts (4.3) | [TEXT] | `WORKER-CONTRACT.md:32-39` | No executable under `src/` writes, parses or routes on `worker_contract_version`, `worker_status` or `blocked_question` (`research/gap-P3-G04.md` 4.4) |
| B8 | Heartbeat: when the setting is on the preamble contains a heartbeat command (default every 5 minutes, range 1 to 60); a heartbeat is accepted only for the sender's own active Dispatch and stores `last_heartbeat_at` | [ORCA-SRC] | `preamble.ts:63-66`; `lifecycle-reconciliation.ts:159-161`; `dispatch-completion.ts:99-105`; `orchestration-heartbeat.ts:3-12` | With heartbeats off the preamble contains no heartbeat command, so no heartbeat is not a stall signal. Orca derives no verdict from heartbeat age on the live surface (`research/gap-P3-G01.md` S4, C12). The contract's deadline W is coordinator policy |
| B9 | `worker_done`: the worker sends it exactly once with `--outcome` from the contract's `worker_status` and passes the contract path as `--report-path`; Orca does not check the file | [TEXT] for the mapping; [ORCA-SRC] for transport | `WORKER-CONTRACT.md:39,59`; `preamble.ts:101-106` | Routing of the message to a mailbox is in 4.3 |
| B10 | Orca settles a Task on a valid `worker_done`, promotes dependents `pending` to `ready` when their deps are completed, and starts nothing itself | [ORCA-SRC] | `worker-report-settlement.ts:46-57`; `task-store.ts:208-214`; `research/gap-P3-G01.md` S7 (settlement and fence, not re-read here) | The retired automatic scheduler is fenced by CLI handlers and an admission fence in the checkout; the running process was not checked |
| B11 | Coordinator wait: `orca orchestration check --wait --types status,dispatch,worker_done,merge_ready,escalation,handoff,decision_gate,question,heartbeat --timeout-ms 300000`; handle the whole batch, write one run-notes line per message ID, then `--ack` | [TEXT]; flags [ORCA-SRC] | `WORKER-CONTRACT.md:99-104`; `IronOrca/src/cli/specs/orchestration.ts:91,116-120` | `--types` is the wake condition only; the whole FIFO batch is replayed until `--ack`; a notes-write failure means no ack; three empty waits lead to `worker-list`; per-type duties (heartbeat, status, `worker_done`, question, escalation, `decision_gate`, handoff, `merge_ready`, dispatch, unknown type, ID mismatch quarantine) are in synth-03 5.2 table A. The contract still labels "two consumers on one mailbox" UNVERIFIED while both Orca help texts answer it (owner question C11) |
| B12 | Sweep (at most every 5 minutes): `worker-list`, `worktree ps --agent-wait`, one `stat` per worker contract path; then classify the worker as one of S0 starting, S1 progressing, S2 long step, S3 idle at prompt, S4 blocked on a person prompt, S5 blocked in ask, S6 context exhausted, S7 unreachable, S8 exited, S9 finished but unreported, S10 settled or S11 unknown, and act on ladder L0 observe, L1 probe, L2 nudge, L3 ask, L4 restart with resume note, L5 report to the person (triggers, responses, caps and the Orca evidence per state: synth-03 5.2 tables B and C) | [TEXT] | `WORKER-CONTRACT.md:110-165` | `worktree ps --agent-wait` is accepted by the installed build files (`out/cli/specs/core.js:157-158`) and absent from the ORCA-CHECKOUT (`core.ts:154-155`): a source divergence, not a contract defect |
| B13 | Last hop: the coordinator opens the contract and admits the result; dependents are created only after all inputs are admitted; a failed attempt is retried only as a new Task (never `--retry-of`) and only after the old attempt is settled | [TEXT] | `WORKER-CONTRACT.md:73-79,237-246` | After an `/sc:implement` stop a freeze and Ruling check applies (`:248-269`); there is no `/sc:implement` worker-contract producer, a scope-decided P4 item (`gaps-and-questions.md` section D) |

#### 4.1.3 What the two flows enforce, and the recorded DEFECT

| Concern | Flow A (claim) | Flow B (worker) |
|---------|----------------|-----------------|
| Executable steps in the checkout | Yes: `orca_worktree.py`, `launch.py`, `ccsession`, the guard and identity hooks | No coordinator or worker step; only hooks that fire on Bash calls, Python that reads nearby contracts (reflect wrapper, workflow archive) and static text tests |
| Executable steps in Orca | Spawn of the tab and environment variables (ORCA-CHECKOUT, via research) | `worker-start`, preamble, mailbox routing, settlement, `check`/`ack` (ORCA-CHECKOUT; installed files agree on the points compared) |
| Instruction text | Skill waves and the ccsession README setting | The whole coordinator and worker contract (sections 3 to 5 of `WORKER-CONTRACT.md`) |
| Hook enforcement | Guard binds the launched session by nonce; worktree gate requires `--agent` on a Bash-typed `orca worktree create` | The worktree gate and, only inside a nonce-bound session, the guard's ESCAPE class. A supervised worker or a person-opened coordinator is not bound by the guard (`launch-level-guard.sh:6-7`) |
| Static test pins | Fake-`orca` tests pin argv, order and result mapping (`test_issue_orca_worktree.py`); no test joins the nonce handoff or the label to the title pattern | `test_worker_contract.py` pins phrases of the contract; nothing parses a produced contract |

**DEFECT (owner-confirmed 2026-11-11): the launch-level guard classifies the Orca CLI only under the command word `orca`.** The ESCAPE arm is `orca)` at `launch-level-guard.sh:458`, inside a test of the word's basename; `orca-ide`, `orca-dev`, `orca.cmd` and differently named links never reach it. The worktree gate has the same lexical limit (`require-orca-worktree-agent.sh:145`, `:349`), but its documented reach is the literal `orca worktree create`, so for the gate this is a recorded ceiling, not a defect. In 29 fixed-input probes (2026-11-11, `research/gap-P3-G02.md` 4.1; 19 re-run by the verifier) `orca-ide terminal send` and `orca-ide agent launch` returned 0 from the guard where the bare-name forms are ESCAPE. On Linux the installed CLI name is `orca-ide`, Orca's own recovery commands and discovery stubs use it, and the issue watcher resolves `orca-ide` first; the claim script and ccsession call the bare `orca`. In data-flow terms: hop A8's forgery guarantee holds for the name `orca` only, and a nonce-bound session that types `orca-ide orchestration worker-start ...` is not stopped by the guard. Which name a launched or supervised session actually types was not observed [UNVERIFIED]. Remediation is a documentation-only draft plan, three tasks, staged and not committed (`git status --short` of the plan prints `A ` while it is unedited since staging and `AM` when a later edit is unstaged; it printed `A ` at about 02:14 UTC on 2026-11-12), not yet reviewed: `.dev/tasks/to-do/TASK-FIX-launch-guard-orca-names-20261111-235205/TASK-FIX-launch-guard-orca-names-20261111-235205.md`. The guard is not fixed, deployed or merely accepted; no scope decision accepts the alternate names. Source of record: `gaps-and-questions.md` section D and owner question C6.

### 4.2 Data Sources

Columns follow the template. "Type" also names the evidence class of the location. A "(moment)" mark means the fact is an observation of this host on the date given and may change.

| Source | Type | Location | Description |
|--------|------|----------|-------------|
| Worker contract text | Static instruction (NORMATIVE) | `src/superclaude/core/WORKER-CONTRACT.md`, installed `~/.claude/WORKER-CONTRACT.md` | Read by the coordinator and worker LLMs; its line numbers hold for HEAD and for the installed copy (byte-identical, moment 2026-11-12). Not loaded automatically (`core/CLAUDE.md:3`) |
| Command `## Unattended mode` sections | Static instruction (NORMATIVE) | `src/superclaude/commands/<name>.md`; the brief guard reads the target worktree's `.claude/commands/sc/<name>.md` and `~/.claude/commands/sc/<name>.md` | Fix where the report directory lands and how a command maps its status (`WORKER-CONTRACT.md:15-22`; command bullets: `research/gap-P3-G04.md` 3.3). The plugin build carries the section for two commands only |
| Brief (Task spec) | User input composed by the coordinator LLM | Orca Task spec text; template at `WORKER-CONTRACT.md:283-297` | Carries the guard line, chain line, gate policy, report directory, worktree placement and the `Command:` lines. Immutable after `task-create` (`:73`) |
| Dispatch preamble and TASK block | Derived (generated by Orca per dispatch) | `buildDispatchPreamble` at `IronOrca/src/main/runtime/orchestration/preamble.ts:52`; typed into the terminal by `deliver-worker-dispatch-preamble.ts:102-107` | Task ID, Dispatch ID, coordinator and worker handles, verbs, heartbeat command or none, post-`worker_done` rule, optional sub-dispatch text. The installed build agrees on the compared points (`research/gap-P3-G01.md` S8) |
| Orca settings: heartbeat and nested depth | Configuration (Orca settings store) | defaults in `IronOrca/src/shared/orchestration-heartbeat.ts:3-12` and `nested-worker-depth.ts:3-4`; installed `out/shared/nested-worker-depth.js:10` | Heartbeat default on, 5 minutes, range 1 to 60. Depth default 1 (ORCA-CHECKOUT) and 2 (INSTALLED-FILES). The effective stored values of the running Orca were not read [UNVERIFIED] |
| Issue claim directory | Static files (written by the claim skill LLM) | `.dev/issues/<N>/` (`<D>`), copied to `<wt>/.dev/issues/<N>/`; `<D>/worktree.json` holds `{path, status, launch}` | Source of the launch prompt and the launch record; the duplicate-launch guard reads `launch` from it and from a mirror file in the git dir (`research/04-launchers.md` F1) |
| Launch-level store | Runtime state | `$HOME/.claude/state/launch-level/{pending,sessions,jobs}` | `pending/<nonce>` is written by the claim script; `sessions/<sid>` is written by the guard and holds a level word; `.ok` marks approval (`research/03-guards.md` C.1, C.2) |
| Orca CLI replies | API (Orca CLI, JSON) | stdout of `orca status`, `worktree list/create`, `terminal list/show/read/close/rename`, `agent launch` | Shapes are assumed from fixtures; the `agent launch` reply fields `receipt.operation_id` and the error text `agent_session_operation_unknown` are marked "PROPOSAL, UNVERIFIED" in the code itself (`launch.py:39-48`). No real Orca reply was recorded |
| Tab environment | Environment | `ORCA_PANE_KEY`, `ORCA_TERMINAL_HANDLE` set by Orca at spawn (`research/gap-P3-G05.md` F6: `spawn-pane-env.ts:46-63`); `CCSESSION_LAUNCH_ID`, `CCSESSION_LAUNCH_CWD`, `CLAUDE_TOPIC`, `CCSESSION_TOPIC_CWD` exported by `ccsession` (`ccsession:1889-1894`) | Drive the title writers and the hook ownership test. Full variable table (23 interface variables) is in `research/gap-P3-G05.md` F8 and belongs to Section 9.2 |
| ccsession state | Runtime state | name lists `~/.claude/projects/<key>/topics/<name>.txt`; tab records `~/.local/state/ccsession/orca-tabs/<pane key>`; title marks `~/.cache/ccsession/orca-titles/<handle>` | Name uniqueness, tab reopen, and "clear only a title ccsession set" (`research/gap-P3-G05.md` F2.3, F2.4) |
| Run mailbox and Deliveries | Runtime state (Orca database) | read through `orca orchestration check [--wait] [--ack]` | FIFO batch per Run inbox; the whole batch replays until `--ack` (`orchestration.ts:116-120`). A reply to `ask` is stored as an already-read `status` message (`research/gap-P3-G01.md` R5, C14) |
| Worker observation | API (Orca CLI) | `worker-show`, `worker-list`, `worker-read`, `terminal read`, `worktree ps --agent-wait` | Fleet liveness verdict with reason, PTY status, `agentWait`, raw `dispatch.lastHeartbeatAt`, transcript and screen text. Orca supplies evidence, not a stall verdict (`research/gap-P3-G01.md` S5, takeaway 2) |
| Worker report | Static file (written by the command's skill LLM) | `<report-dir>/return-contract.yaml`, `<report-dir>/handoff/<n>-<command>.md` | The only structured result a worker produces; the coordinator opens it after `worker_done` |
| Coordinator run notes | Coordinator LLM output | no file path is fixed in the contract lines read | Records per-message-ID handling, heartbeat records, usability of partial results and follow-up Tasks (`WORKER-CONTRACT.md:104,242,246`). Nothing validates them |
| Package ledger of a managed plan | Static files | `.dev/tasks/<state>/<id>/{progress.md, return-contract.yaml, artifacts/retries/T<n>/q0-head}` | Read by the executor skill and by the coordinator's freeze check for `/sc:implement`; the freeze logic is coordinator reasoning with no script (`research/02-lifecycle.md` 5.3) |
| Installed Orca guidance | Derived (Orca-written) | `~/.claude/skills/{orchestration,orca-cli,computer-use}`, text from `orca skills get <name>` | Stubs written by Orca, not shipped by IronClaude; the full guide is printed by the Orca binary on demand (`research/gap-P3-G03.md` F.1, F.2) |

### 4.3 Data Transformations

"Location" names where the rule is written; the executor column of each row is in the Description. [TEXT] rows are performed by an LLM session reading instruction text, so they are not guaranteed.

| Transformation | Input | Output | Location | Description |
|----------------|-------|--------|----------|-------------|
| Command status to `worker_status` | the command's own status: `success`, `partial`, `failed`, `stopped-precondition`; impact/graph flag-STOP `blocked` | `succeeded`, `partial`, `failed` (STOP or precondition kept in `reason`) | `WORKER-CONTRACT.md:36`; per-command `Contract.` bullets (`research/gap-P3-G04.md` 3.3) | [TEXT]. The contract line omits `dry-run` (mapped to `succeeded` by reflect and brainstorm) and the release-split values `split-approved`, `no-split`, `split-with-remediation`; each command maps its own status (owner question C14). `blocked` has two meanings: a person gate (`:31`) and, for impact and graph, a flag STOP mapped to `failed` (C15) |
| `worker_status` to `worker_done --outcome` | the contract's `worker_status`, or no contract | `--outcome failed` for `failed`, `blocked` or no contract; `--outcome succeeded` for `succeeded` or `partial`; any other value is treated as `failed` | `WORKER-CONTRACT.md:59`; command text at `preamble.ts:101-106` | [TEXT]. The worker never reads the command's own `status` for this. Orca then stores only `succeeded` or `failed` (`lifecycle-reconciliation.ts` validation, `research/02-lifecycle.md` 5.2) |
| `worker_status` to dependent admission | `succeeded`, `partial`, `failed`, `blocked`, or no contract with a `guard refused:` body | dependents start; start only after `report_path` is read and recorded as usable; do not start; fix the brief in a new Task (at most 2 fixes) | `WORKER-CONTRACT.md:241-246` | [TEXT]. Orca settles the Task on the `worker_done` but starts nothing itself (hop B10) |
| Return-contract layouts (four) | the command, and whether the caller passes `--output`/`--output-dir` or `--report-dir` | (a) worker keys merged into the command's own `<dir>/return-contract.yaml`; (b) a separate `<report-dir>/return-contract.yaml` listing the command's own contract in `artifacts`; (c) one full contract (existing fields plus worker keys) written to `<report-dir>` by impact and graph with `--report-dir`; (d) a worker-only file for the rest | `WORKER-CONTRACT.md:35` names (a) and (b) for brainstorm and reflect only; layouts (c) and (d): `commands/graph.md:65`, `commands/impact.md:61`, `research/gap-P3-G04.md` 3.3 and takeaway 3 | [TEXT]. The first research pass said three layouts; the gap file corrected it to four and that statement wins. Same file name, different folders: the workflow package contract (`status`, contract 1.1) is read by code (`archive_workspace.py:325-334`); the worker contract is read by no code |
| `report_path` forms | the main deliverable of a command | an absolute path (reflect: never a bare name), a repo-relative plan path re-resolved by id after archive (workflow), or null (graph, adversarial when no merge happened) | `WORKER-CONTRACT.md:33`; `commands/reflect.md:264`; `commands/graph.md:65`; `refs/return-contract.md:51` | [TEXT]. The contract fixes no form (owner question C13). The `artifacts` list leaves out gitignored paths and paths outside the repository (`:34`) |
| Mailbox routing of a worker's report | message type and the sending Dispatch | `dispatch:<creator id>` when the Dispatch has a live creator Dispatch in the same Run, else `run:<run id>` | `dispatch-report-mailbox.ts:5-13,31-37`; `send-methods.ts:143-153`; `ask-methods.ts:113,126-127` | [ORCA-SRC]. Only untyped, `worker_done`, `heartbeat`, `escalation` and `status` are reports; gates and handoffs stay with the coordinator. The route is recomputed on every send, so a helper's reports fall back to the Run when its creator settles. A coordinator-started worker has no creator (inference from `resolveCreatorDispatchId`, not run). This is Orca's helper capability, gated by the depth setting and banned for workers by WC-13; it is not a sub-orchestrator mode |
| Heartbeat setting to preamble text | `orchestrationHeartbeatsEnabled`, `orchestrationHeartbeatIntervalMinutes` | the heartbeat command with the interval, or no command at all when heartbeats are off; invalid or out-of-range intervals become 5 | `orchestration-heartbeat.ts:3-31` (via `research/gap-P3-G01.md` S2); `preamble.ts:63-66` | [ORCA-SRC]. The value is baked into each dispatch's preamble; changing the setting does not change running workers |
| Depth setting to preamble advertisement | `nestedWorkerMaxDepth` and the Dispatch depth | a SUB-DISPATCH section in the preamble only when `depth < max`; otherwise a helper start is refused with `nested_worker_depth_exceeded` | `coordinator-task-dispatch.ts:123`, `dispatch-depth.ts:165-179` (via `research/gap-P3-G01.md` S1, S8; `research/05-orca-provenance.md` 5.2) | [ORCA-SRC]. At the installed default (2) the preamble invites a depth-1 worker to start helpers while WC-13 forbids it; running setting [UNVERIFIED] |
| Raw evidence to liveness verdict | agent-hook status row, PTY provider verdict, stop/release records | `projection.liveness.verdict` of `exited` (durable proof) or `unverifiable` (with one of ten reasons) or `live`; and `observation.status` (PTY) | `orchestration-fleet-worker-projection.ts:53-100`; `agent-status-freshness.ts:4` (30 minutes) (via `research/gap-P3-G01.md` S5, S5a) | [ORCA-SRC]. `unverifiable` is absence of positive proof, never proof of death. The text printer shows only the fleet verdict word |
| Attempt facts to outcome | accepted `worker_report` fact, other attempt facets | `succeeded`, `failed`, `in_progress`, `outcome_unknown`, `finished_unverified` | `attempt-outcome-projection.ts:11,58-143` (via `research/gap-P3-G01.md` S3); only writer: `worker-report-settlement.ts:46-57` | [ORCA-SRC]. The only production writer records `worker_report`; the liveness, process-turn and outcome facets are written only in tests, so `finished_unverified` is not produced and the earlier "60 second window" reading of `unverifiable` is superseded |
| Evidence to coordinator state | heartbeat record, progress token, transcript, `agentWait`, liveness, open `question` | one of S0 to S11 (names in B12), then ladder L0 to L5 with caps (L1 at most 2 costly probes per triggered worker per sweep; L2 1 per incident and 2 per lineage; L3 1 per incident; L4 1 per rolling 60 minutes and 2 per lineage); deadline W = max(10 min, 2 x median heartbeat interval) or `expect_silence_min`, capped at 45 min | `WORKER-CONTRACT.md:112-165` | [TEXT]. `expect_silence_min` and the progress token are not Orca fields in either source. Starting values are declared "not a measured one" (`:97`). Full tables: synth-03 5.2 tables B and C |
| Prompt to ccsession label to tab title | launch prompt text | `<folder>-sc-launch-v1-<12 hex>-<MMDD>-<HHMMSS>-<4 hex>`, shown as `<label> · Claude Code` | `ccsession:645-662,1875,532` | [CODE]. Folder cut to 20 characters, four words cut to 12, so the 32-digit nonce is cut to its first 12 digits. The matching pattern is `orca_worktree.py:779` |
| Nonce to session binding | `[sc-launch:v1:<32 hex>]` in the first prompt, `pending/<nonce>` | `sessions/<sid>` holding `worktree`, `full` or `full-submit`; an unusable leading marker publishes `degraded` | `launch-level-guard.sh:318,334-337,375-378,303-306` | [CODE]. A `degraded` record is read as `worktree` by the guard but blocks every Bash call in the identity hook (`research/03-guards.md` E.3; owner question C12) |
| Hook payload to decision | tool name, command text, session level | class set (for example ESCAPE, COMMIT) and allow or exit-2 block by level `W`, `WA`, `F`, `FS` | `launch-level-guard.sh:393-742` (via `research/03-guards.md` C.4, C.5); `orca` arm `:458-478` | [CODE]. Text-level only; for the Orca CLI it applies to the name `orca` only (DEFECT, 4.1.3). Unbound sessions are never blocked |
| Terminal read/show JSON to shim verdict | `result.terminal.tail` (lines) and `result.terminal.title` | true on any marker in the tail or a title match within five tries; else warning `W-LAUNCH-NOT-CCSESSION`, status stays `launched` | `orca_worktree.py:774-782,1142-1161,1377-1386` | [CODE]. Advisory: nothing stops the agent |
| Watcher prompt gate | an issue number | exactly `/sc:issue --claim <n>` (integer 1 to 999999999) as the only text after `--prompt`; otherwise `ValueError` | `launch.py:84-102` (`PROMPT_PATTERN`, via `research/04-launchers.md` F2) | [CODE]. The watcher launch argv is 12 elements, no marker, no `[sc-launch:...]` binding |
| Source contract to installed copy | `src/superclaude/core/WORKER-CONTRACT.md` | `~/.claude/WORKER-CONTRACT.md`, skipped when the destination exists unless `force` | `install_core.py:14-29,70-72` | [CODE]. A plain install keeps an older installed file; `install_hooks.py:279-281` does the same for hook scripts. The set installed on this host is mixed (3.0.3) |

---

## Contradictions, corrections applied and open items (for the assembler)

| Item | Resolution used in this file | Where |
|------|------------------------------|-------|
| `origin/master` moved after the research (history in the section 1 legend; now `930c5ebc8`, 23 behind, at about 02:14 UTC on 2026-11-12; the local ref moves when the fork is fetched) | Cite the ref by hash and time; installed `WORKER-CONTRACT.md` equals HEAD, so Flow B describes HEAD and the installed bytes. The ORIGIN/MASTER contract adds a coordinator preflight and drops the `P0 only:` brief line, noted at hop B2 only | 3.0.3, B2 |
| Research 02 and 03 say the guard's ESCAPE arm covers "any non-allowlisted `orca` subcommand" | Gap file P3-G02 section 4.5 wins: the arm matches the word `orca` only; recorded as a DEFECT with the linked draft plan | 4.1.3 |
| Research 04 lists "Defects: none" | Superseded for the guard by the register (`gaps-and-questions.md` section D, owner answer C6, 2026-11-11); the agent-less claim worktree create stays an accepted exception, not a defect | 4.1.1 hop A3, 4.1.3 |
| Gap-fill G01 corrects research 02 on `unverifiable`, the `--types` waiter, the Dispatch-ID timing and the 60 s reading | G01 wins; the 60 s attempt window and `finished_unverified` are not produced in either Orca source | 4.3 |
| Return-contract layouts: three in the first pass, four in gap P3-G04 | Four | 4.3 |
| Nested-worker depth default: 1 (ORCA-CHECKOUT) against 2 (INSTALLED-FILES) | Both stated with provenance; neither is wrong for its own build; the running value is unobserved | B4, 4.2, 4.3 |
| `worktree ps --agent-wait`: absent in the ORCA-CHECKOUT, accepted by the installed files | A source divergence, not a contract defect | B12 |
| Installed `ccsession` header comment differs from the checkout (gap P3-G03 B.3 "differ", G05 F7 "comment only") | G05 wins: no code difference | not drawn in a flow |

Statements in this file that rest on a research file and were not re-read against source by this writer, marked "via" in the tables: the Orca fleet-projection and attempt-projection rows (`research/gap-P3-G01.md` S2, S3, S5, S5a), the Orca tab-environment and Claude-command join (`research/gap-P3-G05.md` F6, R1), the `worker-start` depth enforcement beyond `worker-start-authority.ts`, and the guard classifier table beyond lines `:303-306`, `:318`, `:334-337`, `:375-378`, `:456-478`. Everything else tagged [CODE-VERIFIED] here was re-read from the live file on 2026-11-12. The host-installed state and the ORIGIN/MASTER comparison are moment-in-time observations. Nothing here describes the running Orca, the running Claude Code process, a live guard session, or any other host.

Items left open on purpose (not decisions made here): owner questions C1 (name the claim-flow exception), C11 (drop the stale UNVERIFIED label on shared mailbox waits), C13 to C15 (`report_path` form, status mapping completeness, the two meanings of `blocked`), C17 and C19 (stale second screen marker, a joining test). The `/sc:implement` worker-contract producer is a P4 item; the future-role question and any installation rollout are unresolved and unclaimed.

## Routing dispositions

Every artifact that `synthesis/evidence-routing.md` routes to this output, and where it is used or why not.

| Artifact | Routed to template sections | Disposition |
|----------|-----------------------------|-------------|
| `research/02-lifecycle.md` | 4.1 | Used. Flow B hops B1 to B13, 4.3 status and admission rows; corrections of gap P3-G01 applied |
| `research/03-guards.md` | 3, 4.1 | Used. Hook registration and install facts in 3.0.1, hop A8, 4.1.3, 4.3 guard rows |
| `research/04-launchers.md` | 3, 4.1 | Used. Flow A hops A1 to A12, 3.1 naming rows, launcher-version note in 3.0.3 |
| `research/05-orca-provenance.md` | 4.1, 4.2 | Used. Orca provenance in 3.0.2, helper start and mailbox routing at B4 and in 4.3, depth settings in 4.2 |
| `research/06-distribution-evidence.md` | 3 | Used. Installed-copy comparison matrix in 3.0.3 (re-run live on 2026-11-12, result differs from the research for the moved ref) |
| `research/gap-P3-G01.md` | 4.1, 4.3 | Used. Preamble, heartbeat, liveness projection, scheduler fence at B5, B8, B10 and in 4.3 |
| `research/gap-P3-G02.md` | cited for 4.1 | Used only for the DEFECT paragraph 4.1.3 and the 4.3 guard row; its fuller treatment is routed to 03, 04 and 05 |
| `research/gap-P3-G03.md` | 3 | Used. Installer, Orca skills layout, ccsession wiring in 3.0.1 and 4.2 |
| `research/gap-P3-G04.md` | 4.1, 4.3 | Used. Result channel in B7 to B13 and the status, layout and `report_path` rows of 4.3 |
| `research/gap-P3-G05.md` | 4.1 | Used. ccsession title chain in A7 to A11, state paths in 3.0.1, label rows in 3.1 and 4.3 |
| `research/gap-P3-G06.md` | not routed to this output | Not read for this file; hook timeouts and fail-open rows belong to synth-04 (10.3, 11) |
| `research/web-01-claude-code-hook-execution.md` | not routed to this output | Read only for the sentence that matching hooks run in parallel with non-deterministic completion order (hop A8, DOCUMENTED, https://code.claude.com/docs/en/hooks); the rest belongs to synth-04 |
| `research/web-02-claude-code-subagent-hooks.md` | not routed to this output | Not read for this file; subagent hook behavior is routed to synth-03 and synth-04 |
| `gaps-and-questions.md` | cited for 4.1 | Used for the defect register, precedence block, owner questions and boundary statements; disposition of every row belongs to synth-05 |
| `.dev/tasks/to-do/TASK-FIX-launch-guard-orca-names-20261111-235205/` | linked for 4.1 | Link only (4.1.3); the plan is a draft, not a fix; its contents were not read for this file |
| `qa/*-decision.md`, `BUILD-REQUEST.md`, `research-notes.md`, earlier sub-orchestrator report | not routed to this output | Not used directly; the earlier report appears only through the research files that cite it |

Status: Complete

