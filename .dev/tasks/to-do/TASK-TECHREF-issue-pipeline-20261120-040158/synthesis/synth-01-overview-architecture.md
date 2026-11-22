# Synthesis 01: Overview and Architecture

**Sections:** 1, 2
**Status:** Complete
**Date:** 2026-11-20

---

## 1. Overview

The issue-to-work pipeline takes a GitHub issue on `IronbellyOrg/IronClaude` from "approved by a person" to "claimed, with an accuracy check, a summary and next steps posted", and, when asked, on to a Claude agent session launched in an Orca worktree whose launch level is enforced by hooks. It is four cooperating pieces plus a fifth, the `issue-pipeline` package, that was removed in commit 01e7a9e23 (PR #682). As built, the watcher ships switched off and nothing in the snapshot schedules it, so only a person typing a command starts any part of the pipeline. The built-versus-not-built ledger is in Section 2.3.

**What it does:** a watcher polls GitHub read-only for approved issues and starts one Orca claim session per cycle; the claim session assigns the issue and posts two marked comments; optionally the claim creates a worktree and launches an agent bound to a launch level by guard hooks.

**Who uses it:** the repository owner (runs the five `issue-watch` verbs and types `/sc:issue --claim`), Claude Code sessions (claim orchestrator, tier workers, launched agents) and Orca (`agent launch`, `worktree create`). The repository literal is hard-coded in the watcher (`src/superclaude/cli/issue_watch/github.py:37`, `src/superclaude/cli/issue_watch/launch.py:50`).

**Where it lives:**

| # | Piece | What it is | Location |
|---|-------|------------|----------|
| 1 | Watcher | `superclaude issue-watch` Click group: poll cycle, read-only `gh` calls, local state, one fixed Orca launch | `src/superclaude/cli/issue_watch/` (registered at `src/superclaude/cli/main.py:577-579`) |
| 2 | Claim | `/sc:issue --claim`: command front, orchestrator skill, tier workers, helper scripts, templates | `src/superclaude/commands/issue.md`, `src/superclaude/skills/sc-issue-protocol/`, `src/superclaude/agents/issue-worker-t{1,2,3}.md` |
| 3 | Guard | L1 hook guard, job-identity command wrapper, L2 git pre-push hook, G2 rule 2, hook registration and install | `src/superclaude/hooks/scripts/launch-*.sh`, `src/superclaude/hooks/hooks.json`, `src/superclaude/cli/install_hooks.py` |
| 4 | Coordinator text | worker and coordinator contract; it holds no issue-pipeline duties | `src/superclaude/core/WORKER-CONTRACT.md` |
| 5 | Removed | `issue-pipeline` command group, rule WC-17, "Issue pipeline duties", guard rule 1 | absent in the snapshot; read at `01e7a9e23^` under `src/superclaude/cli/issue_pipeline/` |

**Two kinds of "level".** "L1" and "L2" name guard LAYERS, not pipeline levels: L1 is the Claude Code hook `src/superclaude/hooks/scripts/launch-level-guard.sh` (header :4-6) and L2 is the git `pre-push` hook `src/superclaude/hooks/scripts/launch-level-pre-push.sh` (header :4-5). The `--pipeline` levels (`src/superclaude/commands/issue.md:43-44`) are `worktree`, `full`, `full --submit` and `none`. The guard stores one level per bound session as W (worktree), WA (worktree, approved), F (full) or FS (full --submit) (`src/superclaude/hooks/scripts/launch-level-guard.sh:264-272`). `none` has no guard level because the claim ends before any launch (`src/superclaude/skills/sc-issue-protocol/SKILL.md:90`).

**Key statistics** (stated here once; later sections do not repeat them):

| Area | Figures | Counted at |
|------|---------|------------|
| Watcher package | 8 modules, 4,795 lines (cycle 1,406; github 960; record 865; audit 404; launch 370; cli 348; predicates 312; runner 130), plus an empty `__init__.py` | `src/superclaude/cli/issue_watch/` |
| Watcher surface | 5 verbs; 7 read-only `gh` calls (G1-G7); per-issue call cap 35 (32 ordinary plus 3 reserved) plus the two shared calls G1 and G2, so at most 37 `gh` calls per cycle (2 when idle); 59 reason words; exit codes 0, 1, 2, 3, 4, 5, 6, 7, 75; launch argv of 12 elements | `src/superclaude/cli/issue_watch/cli.py:111-348`, `.../github.py:175-262`, `.../audit.py:26-102`, `.../launch.py:95-116` |
| Watcher store | `dispatch.json` with 7 top-level keys, 17-field entries, 6 entry states, transitions T-1..T-13 | `src/superclaude/cli/issue_watch/record.py:120-130, 69-88, 34-36` |
| Watcher tests | 20 files in `tests/issue_watch/` (19 test modules plus `conftest.py`), 19,801 lines, 867 test functions (parametrisation not expanded), 19 `_assumed_shape` fixtures | `tests/issue_watch/` |
| Claim | `issue.md` 117 lines; `SKILL.md` 197 lines plus 5 refs; `orca_worktree.py` 1,906 lines; `origin_repo.py` 195; `clickup_claim.py` 270; 15 templates; 3 worker agents of 35 lines each; 4 `--pipeline` levels | `src/superclaude/commands/`, `skills/sc-issue-protocol/`, `agents/` |
| Claim tests | 10 test files (the 8 named for the claim path plus `tests/skills/test_clickup_claim.py` and `tests/skills/test_model_alias_policy.py`) | `tests/skills/`, `tests/commands/`, `tests/cli/` |
| Guard | `launch-level-guard.sh` 808 lines; `launch-job-identity.sh` 582; `launch-level-pre-push.sh` 208; `hooks.json` 192; 18 block words; 4 guard levels | `src/superclaude/hooks/` |
| Guard tests | 17 files, 24,388 lines, 921 test functions by plain `def test_` grep (920 strict): 14 table files plus 3 claim-side pin files (two of the three are also claim-side tests); the main file has 4,631 lines and 162 tests | `tests/hooks/`, `tests/cli/`, `tests/unit/`, `tests/core/`, `tests/skills/` |
| Coordinator text | `WORKER-CONTRACT.md` 339 lines; rules WC-2..WC-16 (15 rules; no WC-1, no WC-17); `tests/skills/test_worker_contract.py` 3,220 lines, 59 tests | `src/superclaude/core/`, `tests/skills/` |
| Removed package | 10 files, 1,597 lines, 10 verbs; 116 tests in 10 test files plus 1 registration test | `01e7a9e23^` |

PR 686 and the rewrite design are out of scope for this reference.

**Evidence limits.** The source is a snapshot of `origin/master` at 61ac2c2e6: it has no runtime state, no git history and no PR data. Therefore these statements stay [UNVERIFIED]: "never run live" and the PR numbers #447 and #448 (`docs/designs/issue-watcher.md:3`), the real reply shapes of `gh` and Orca (all `_assumed_shape` fixtures; no live-test record exists), the live observations OB-H1..3 and OB-CTX, the recorded FU-1 lines (`docs/designs/issue-pipeline-fu1.md:108-119`), the `enabled` value on any real machine, and whether anything runs `issue-watch once` on a schedule. Tests were read, not run. Of all components, only the L1 guard script was executed (44 sample payloads, sandbox HOME, observation run in the guard research). Removed code is labelled `@01e7a9e23^`. A pointer: Section 2.3 holds the ledger; Section 14 lists unwired, switched-off, retired and caller-less capabilities.

---

## 2. Architecture

Status words are only BUILT-ON, BUILT-OFF (enabled:false), NOT BUILT and REMOVED. Every statement below is [CODE-VERIFIED] against the 61ac2c2e6 snapshot unless it carries another tag. Paths are repository-relative; removed code is labelled `@01e7a9e23^`.

### 2.1 Whole-pipeline diagram

```
 TRIGGERS   (a scheduler, dispatcher or zero-setup install is "not found in snapshot")
  [A] a person or external scheduler runs   superclaude issue-watch once [--dry-run]
  [B] a person types                        /sc:issue --claim <N> [--pipeline worktree|full|none]
        |                                                         |
        v                                                         |
 +--------------------------------------------+                   |       GITHUB  IronbellyOrg/IronClaude
 | 1 WATCHER  cli/issue_watch/                |                   |       reads : gh calls G1-G7 (watcher only)
 |   BUILT-OFF (enabled:false)                |-- reads G1..G7 ---|--->   writes: none from the watcher
 |   enabled gate -> setup check -> lock      |                   |
 |   -> DISABLED -> store -> login (G1)       |   LOCAL STATE     |
 |   -> origin -> sweep -> discovery (G2)     |-> <state_dir>/dispatch.json, lock, DISABLED,
 |   -> candidates, reads G3-G7 -> `pending`  |                   audit.jsonl, dry-run.json
 |   -> ONE launch per cycle -> commit        |                   |
 +---------------------|----------------------+                   |
                       |  <orca> agent launch --agent claude --worktree path:<abs worktree>
                       |     --surface terminal --prompt "/sc:issue --claim <N> --pipeline none" --json
                       |  (this prompt has no [sc-launch:v1:<nonce>] marker: the guard never binds it)
                       v                                          v
 +-------------------------------------------------------------------------------------+
 | 2 CLAIM  /sc:issue --claim   BUILT-ON   waves 0-8 are prose run by the model       |
 |   W0 orca preflight | W1 scout (worker t3) | W3 assign + ClickUp | W4 check (t2/t1) |
 |   W6 post accuracy-check and claim comments (hidden markers)                       |
 |   --pipeline none : ends after W6; no worktree, no agent, no launch record        |
 |   worktree | full | full --submit : W7 worktree, W8 launch                         |
 +-----------|----------------------------------------|----------------------------------+
             | levels worktree/full/full --submit     | GITHUB WRITES (orchestrator only):
             v                                        |   gh issue edit --add-assignee @me
 +-----------------------------------------------+    |   gh issue comment | gh api -X PATCH
 | 3 orca_worktree.py (only code that calls orca)|    |   ClickUp assignee add (if env set)
 |  worktree: orca worktree create --no-parent   |    |   <-- the watcher re-reads the claim
 |            copy .dev/issues/<N>/ into it      |    |       marker comment through G4
 |  launch  : IR-4 preflight -> install_l2       |    +--------------------------------
 |            -> pending/<nonce> (level word)    |
 |            -> orca agent launch --prompt      |
 |               "[sc-launch:v1:<nonce>] Read     |
 |               .dev/issues/<N>/launch-prompt.md |
 |               and follow it." --json          |
 |            -> detect ccsession shim (warning) |
 +-------|-------------------------|-------------+
         |                         +--> <git-common-dir>/hooks/pre-push (+ data file)   = L2
         v
 +-------------------------------------------------------------------------------------+
 | 4 LAUNCHED AGENT (Orca terminal, ccsession-orca) reads launch-prompt.md level blocks |
 |   its first prompt carries the marker -> L1 guard binds pending/<nonce> -> sessions/<sid> |
 +--------------------------------------------|----------------------------------------+
                                              v
 5 GUARD HOOKS on every prompt and tool call of a bound session (Claude Code hooks.json):
     launch-level-guard.sh   UserPromptSubmit + PreToolUse: blocks implement / commit / push / submit by level;
                             G2 rule 2: `orchestration send|ask` allowed only with no --to
                               (matches the command word `orca` only; `orca-ide` is not constrained, Section 5.3, D-25);
                             a typed first line /sc:implement or /task at level worktree writes sessions/<sid>.ok
     launch-job-identity.sh  PreToolUse(Bash): wraps each Bash call so a git hook can name the actor
     pre-push (git, L2)      asks identity; refuses main/master pushes by governed or unknown actors

 NOT BUILT / REMOVED (see Section 14): hand-off from a `--pipeline none` claim to a started worker;
 coordinator release of a bound worker (REMOVED); a caller of `orca_worktree.py pending`; a scheduler.
```

### 2.2 Component relationship table

Watcher import rules are pinned by `tests/issue_watch/test_module_boundaries.py:241`.

| Component | Path | Role | Depends on | Depended on by |
|-----------|------|------|------------|----------------|
| cycle | `src/superclaude/cli/issue_watch/cycle.py` | config loader and validators (:34-483), one poll cycle `_Cycle` (:485-1222), status report and SLO reducer (:1225-1406) | runner, github, predicates, record, launch, audit | `src/superclaude/cli/issue_watch/cli.py` |
| github | `src/superclaude/cli/issue_watch/github.py` | the seven read-only `gh` calls, call budget, rate-limit handling | runner, predicates | `src/superclaude/cli/issue_watch/cycle.py` |
| record | `src/superclaude/cli/issue_watch/record.py` | `FileStore` for `dispatch.json`, flock, atomic write, DISABLED check, dry-run shadow, entry transitions | predicates; `swarm.atomic` inside functions only | `src/superclaude/cli/issue_watch/cycle.py`, `src/superclaude/cli/issue_watch/cli.py` |
| launch | `src/superclaude/cli/issue_watch/launch.py` | the one fixed `orca agent launch`, Orca discovery, origin check, reply mapping | runner; `_ORCA_CLIS` at `src/superclaude/cli/install_user_setup.py:36` | `src/superclaude/cli/issue_watch/cycle.py`, `src/superclaude/cli/issue_watch/cli.py` |
| predicates | `src/superclaude/cli/issue_watch/predicates.py` | pure eligibility checks (approval replay, owner, edits, project, marker window) | nothing from `superclaude` | cycle, record, github |
| audit | `src/superclaude/cli/issue_watch/audit.py` | `audit.jsonl` writer, reason table (:26-102), rotation | import table pinned at `tests/issue_watch/test_module_boundaries.py:241` | cycle, cli |
| cli | `src/superclaude/cli/issue_watch/cli.py` | Click group `issue-watch`, five verbs, exit-code mapping | cycle, record, audit, launch, runner, click | `src/superclaude/cli/main.py:577-579` |
| runner | `src/superclaude/cli/issue_watch/runner.py` | the only module that imports `subprocess` (`shell=False`) | none | github, launch, cli |
| command front | `src/superclaude/commands/issue.md` | flags, STOP rules, Activation (:104-110) | skill `sc-issue-protocol` | a person; the watcher prompt |
| orchestrator skill | `src/superclaude/skills/sc-issue-protocol/SKILL.md`, `refs/{claim,create,chains,tiers,labels}.md` | waves 0-8 run by the model; level rule at `src/superclaude/skills/sc-issue-protocol/refs/claim.md:81` | workers, three scripts, templates, `Skill sc-recommend` | `issue.md` |
| tier workers | `src/superclaude/agents/issue-worker-t{1,2,3}.md` | read-only lookups and drafts, write only under `.dev/issues/`; `model:` on line 6 (tier1b, tier2, tier2b) | `gh` reads, `git fetch` | SKILL.md waves 1 and 4 |
| origin script | `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py` | resolves the repo from `origin` only | `git` | wave 0 |
| ClickUp script | `src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py` | at most one ClickUp assignee add, only when env is set | ClickUp API | wave 3 |
| worktree script | `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` | preflight, worktree, prompt, launch, pending; the only code that calls `orca` for the claim | `orca`, `git`, `~/.claude/hooks/*`, launch-prompt template | waves 0, 5, 7, 8 |
| templates | `src/superclaude/skills/sc-issue-protocol/templates/` | posted comment bodies, summaries, level blocks (`src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md:11,20,25,28`) | none | SKILL.md; marker pinned by `tests/issue_watch/test_marker_contract.py:28-48` |
| L1 guard | `src/superclaude/hooks/scripts/launch-level-guard.sh` | binds a session to a level, blocks action classes, G2 rule 2 | `jq`; reads only `HOME`; store `~/.claude/state/launch-level/` | Claude Code events (`src/superclaude/hooks/hooks.json:63-71,115-124`); claim IR-4 preflight |
| job identity | `src/superclaude/hooks/scripts/launch-job-identity.sh` | wraps governed Bash calls; `identify` names the actor of a process | `uv`, Linux `/proc` | `src/superclaude/hooks/hooks.json:125-134`; L2 hook |
| L2 hook | `src/superclaude/hooks/scripts/launch-level-pre-push.sh` | git `pre-push` refusal for main/master | identity `identify` (:65) | git; installed by `orca_worktree.py` `install_l2` |
| registration | `src/superclaude/hooks/hooks.json`, `src/superclaude/cli/install_hooks.py` | merge registrations into `~/.claude/settings.json`; copy scripts (skip if present unless `force`) | `superclaude install` and `update` | `src/superclaude/cli/main.py:219, 412` |
| ccsession | `src/superclaude/skills/ccsession-tag/ccsession-orca`, `src/superclaude/cli/install_ccsession.py` | Orca's Claude command; carries NO launch level | none | detected, never required, by the claim (`src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1802-1811`) |
| coordinator text | `src/superclaude/core/WORKER-CONTRACT.md` | general coordinator and worker rules; no issue-pipeline duties | none | coordinator sessions (instruction text only) |

### 2.3 Live-versus-switched-off ledger

"BUILT-ON" means the code exists and is wired into a path that runs in a normal install; it does not say any machine has run it. Rows 1 to 8 are the eight pieces; rows 1b, 7b and 9 to 18 are additional rows. In row 12 the words "enabled:false" label a switched-off constant, not the `enabled` config key.

| Piece | Status word | Evidence (path:line) | Trigger | Writes to GitHub | Note |
|-------|-------------|----------------------|---------|------------------|------|
| 1 Watcher, real cycle (`issue-watch once`) | BUILT-OFF (enabled:false) | `src/superclaude/cli/issue_watch/cycle.py:228` (default `False`); `src/superclaude/cli/issue_watch/cycle.py:685-686` (`not_enabled`, exit 0); `src/superclaude/cli/main.py:577-579` | only a person or an external scheduler running `once`; none exists in the snapshot | none; seven read-only `gh` calls (`src/superclaude/cli/issue_watch/github.py:175-262`); its one outward effect is one `orca agent launch` | no config file ships; a real machine's `enabled` value is [UNVERIFIED]; the `DISABLED` file is a second kill switch and `once --dry-run` ignores `enabled` |
| 1b Watcher verbs and `once --dry-run` | BUILT-ON | `src/superclaude/cli/issue_watch/cli.py:111-137` (`once`), `:164-182` (`status`), `:185-198` (`check-config`), `:201-214` (`init-state`), `:282-348` (`reset`); `src/superclaude/cli/issue_watch/cycle.py:685` (dry-run skips the gate), `:1029-1035` (dry-run stops before any probe or launch); `src/superclaude/cli/issue_watch/cycle.py:712, 1063` (`DISABLED` file) | an operator by hand | none | the audit writer is not behind the gate (`src/superclaude/cli/issue_watch/cycle.py:691-693`) |
| 2 Claim (`/sc:issue --claim`) | BUILT-ON | `src/superclaude/commands/issue.md:104-110`; `src/superclaude/skills/sc-issue-protocol/SKILL.md:74`; `src/superclaude/skills/sc-issue-protocol/refs/claim.md:48, 91-92` | a person typing it; the watcher prompt (`src/superclaude/cli/issue_watch/launch.py:84-92`) | `gh issue edit <N> --repo <R> --add-assignee @me`; `gh issue comment` or `gh api -X PATCH` on two marked comments; ClickUp assignee add (`src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py:232-237`) | waves are prose run by the model, no program orders them; ClickUp runs only when its env is set (`src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py:164-169`); workers are read-only; labels, type and fields are never written |
| 3 L1 guard | BUILT-ON | `src/superclaude/hooks/hooks.json:63-71, 115-124`; `src/superclaude/hooks/scripts/launch-level-guard.sh:4-6, 257, 391` | Claude Code `UserPromptSubmit` and `PreToolUse` events | none | governs only a session a claim launch bound; every other session exits 0 (fail-open), a bound one fails closed; its orca checks (G2 rule 2) recognise the command word `orca` only, not `orca-ide` (row 6) |
| 4 L2 pre-push hook | BUILT-ON | `src/superclaude/hooks/scripts/launch-level-pre-push.sh:4-5, 187-208`; `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1386-1442, 1754`; `src/superclaude/cli/install_hooks.py:96` | git `pre-push` in a clone where `install_l2` placed it | none | installed by the claim at launch, not registered in `hooks.json`; refuses only `refs/heads/main` and `refs/heads/master` (`src/superclaude/hooks/scripts/launch-level-pre-push.sh:17`); only a claim at `worktree` or `full` installs it |
| 5 Job identity | BUILT-ON | `src/superclaude/hooks/hooks.json:125-134`; `src/superclaude/hooks/scripts/launch-job-identity.sh:430-505, 541-572` | Claude Code `PreToolUse` for `Bash`; `identify` called by the L2 hook | none | needs Linux and `uv`; fails closed for a bound session; not a sandbox (`src/superclaude/hooks/scripts/launch-job-identity.sh:2`) |
| 6 G2 rule 2 | BUILT-ON | `src/superclaude/hooks/scripts/launch-level-guard.sh:485, 496-537`; `src/superclaude/core/WORKER-CONTRACT.md:66`; `tests/hooks/test_launch_level_guard_worker.py:74, 187` | a bound session's Bash call `orca orchestration send` or `ask` | none | applies only to sessions bound by a claim marker; nothing binds a coordinator-started worker (rows 10 and 18); recognises the command word `orca` only: `orca-ide` is not constrained (observed exit 0), see Section 5.3 and Section 14 D-25 |
| 7 Coordinator text, issue-pipeline duties | NOT BUILT | `src/superclaude/core/WORKER-CONTRACT.md` (full read: no "Issue pipeline duties", no "WC-17", no "watcher", no "COORD-"); issue-related lines only at `:23, 57, 66, 242-243`; `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:268` | none found in snapshot | none | who starts a worker after a claim is not defined in any file read; the hand-off prose at `src/superclaude/commands/issue.md:85` has no code behind it |
| 7b Coordinator text, general rules | BUILT-ON | `src/superclaude/core/WORKER-CONTRACT.md:31-64, 72, 287`; `tests/skills/test_worker_contract.py:876-878` | read by a person-opened coordinator session; no code loads it (`docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:186`, [UNVERIFIED]) | none from the text; contract `:243` names issue comments as coordinator actions | rules WC-2..WC-16 are instruction text pinned only as text |
| 8 Removed package `issue_pipeline` | REMOVED | `src/superclaude/cli/issue_pipeline/` absent; present at `01e7a9e23^`; `CHANGELOG.md:17` (records the removal); old `src/superclaude/cli/main.py:581, 583` @01e7a9e23^ | none in code; ran only if a coordinator or worker session followed the removed contract text | none from its code: GitHub reads only, local rows and one local `.ok` file; the plan reply and label mirror were contract text, no command line | commit 01e7a9e23, PR #682, dated 2026-11-19 18:02 -0600 (2026-11-20 00:02 UTC); its message says nothing ran this code [CODE-VERIFIED as text, runtime [UNVERIFIED]] |
| 9 G2 rule 1 / route A (`release-worker`) | REMOVED | `src/superclaude/hooks/scripts/launch-level-guard.sh:496-497` (comment: retired); old TAMPER case at `src/superclaude/hooks/scripts/launch-level-guard.sh:441-444` @01e7a9e23^; zero hits for `release-worker` in `src`, `tests`, `plugins` | none | none | the only `.ok` writer left is the guard's typed-prompt branch (`src/superclaude/hooks/scripts/launch-level-guard.sh:347-359`); route B (signed file) is NOT BUILT (zero hits for signature terms) |
| 10 Caller of `orca_worktree.py pending` | NOT BUILT (binding and caller); the `pending` verb itself is BUILT-ON | verb at `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1515-1523, 1886-1893`; only test callers `tests/hooks/test_launch_level_guard_worker.py:287` and `tests/skills/test_issue_orca_worktree.py:2472-2498` | no trigger found in snapshot | none | the verb is BUILT-ON, the caller is absent; the launch-level guard design says it does not govern a coordinator-started worker (`docs/designs/sc-issue-launch-level-hook.md:23`) |
| 11 IR-3 `pipeline.json` | NOT BUILT | zero hits for `pipeline.json` in `src` and `plugins`; `docs/designs/sc-issue-claim-pipeline-flag.md:58` (documentation only) | none | none | the level travels by files under `~/.claude/state/launch-level/` only |
| 12 IR-7 refusal (L2 not owned) | BUILT-OFF (enabled:false) | `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:822` (`IR7_REFUSE = False`), `:1757-1758`; `tests/skills/test_issue_l2_install.py:639` | a claim launch at `worktree` or `full` | none | the switch is a constant, not the `enabled` key; a missing L2 hook only adds `W-L2-ABSENT` |
| 12b IR-4 enforcement preflight | BUILT-ON | `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:955-1045, 1730-1747` | a claim launch | none | refuses the launch with `W-ENFORCEMENT-ABSENT`; verifies the claim process only |
| 13 OB-H1..3 and OB-CTX live observations; ship gate | NOT BUILT | `tests/hooks/test_launch_level_observations.py:79-84` (every parametrised case skips); `src/superclaude/commands/issue.md:16`; `src/superclaude/skills/sc-issue-protocol/refs/claim.md:136` | none | none | the gate is prose; no code reads it; whether the observations passed is [UNVERIFIED] |
| 14 Scheduler for `issue-watch once` | NOT BUILT | `src/superclaude/cli/issue_watch/cli.py:98` ("Run `once` from a timer"); no timer, cron, systemd, launchd, GitHub Action or Orca automation artefact in the snapshot; `docs/designs/issue-watcher-setup.md:288` says this work installs none | none | none | deferred behind the live test by the design (`docs/designs/issue-watcher.md:33, 861`) |
| 15 Dispatcher, `COORD-<RepoName>` coordinator worktree, zero-setup install | NOT BUILT | not found in snapshot: `COORD-` has 0 hits outside `.git` and `.dev`; `dispatcher` hits are unrelated (swarm, Orca shim) | none | none | "grant row" exists only as prose (`src/superclaude/core/WORKER-CONTRACT.md:57`, `docs/designs/issue-pipeline-fu1.md:24, 26`); no store, verb or schema |
| 16 Live-test record | NOT BUILT | `docs/designs/issue-watcher-live-test.md` is absent; `docs/designs/issue-watcher.md:33` (the owner writes it); `tests/issue_watch/test_github.py:575-583` (fixtures still assumed) | none | none | gates enabling the watcher by design; no code checks the gate |
| 17 Hand-off from a `--pipeline none` claim to a worker | NOT BUILT | `src/superclaude/commands/issue.md:85`; `src/superclaude/skills/sc-issue-protocol/SKILL.md:140`; `src/superclaude/skills/sc-issue-protocol/refs/claim.md:96` (prose); no Python in `src` calls `worker-start` | none found in snapshot | none | the removed duties are row 8; see Section 14 |
| 18 Binding of coordinator-started workers | NOT BUILT (binding and caller); the `pending` verb itself is BUILT-ON | the only marker generator was `brief.build` @01e7a9e23^ (old `src/superclaude/cli/issue_pipeline/brief.py:71-73`); the contract brief template has no marker slot | none | none | G2 rule 2 (row 6) therefore runs only for claim-launched sessions |

### 2.4 Integration map

| # | Hand-off | Mechanism | Evidence (path:line) | Status word |
|---|----------|-----------|----------------------|-------------|
| 1 | watcher -> claim | `orca agent launch ... --prompt "/sc:issue --claim <N> --pipeline none" --json` in the operator's existing worktree; the level `none` is hard-coded; the claim ends after wave 6 | `src/superclaude/cli/issue_watch/launch.py:33, 84-92, 95-116`; `src/superclaude/commands/issue.md:48`; `src/superclaude/skills/sc-issue-protocol/SKILL.md:90`; pinned at `tests/issue_watch/test_launch.py:75` and `tests/issue_watch/test_security_invariants.py:936` | BUILT-OFF (enabled:false) |
| 2 | claim -> watcher (return path) | the claim comment ends with a hidden marker; the watcher reads it through G4 and moves the entry to `claimed` | `src/superclaude/skills/sc-issue-protocol/templates/claim-comment.md:23`; `src/superclaude/cli/issue_watch/github.py:223-225`; `src/superclaude/cli/issue_watch/cycle.py:848-865, 896-899`; `tests/issue_watch/test_marker_contract.py:28-48` | BUILT-OFF (enabled:false) |
| 3 | claim -> guard | files only: `pending/<nonce>` holds one level word; the launch prompt carries `[sc-launch:v1:<nonce>]`; the guard renames it to `sessions/<sid>` on the first prompt; only levels `worktree`, `full`, `full --submit` | `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1488-1512, 1759-1761, 1776-1779`; `src/superclaude/hooks/scripts/launch-level-guard.sh:318, 372-375` | BUILT-ON |
| 4 | claim -> L2 hook | `install_l2` hard-links the hook into `<git-common-dir>/hooks/pre-push` with a data file, after the IR-4 preflight; an existing hook is never replaced | `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1386-1442, 1754`; template copied by `src/superclaude/cli/install_hooks.py:96` | BUILT-ON |
| 5 | install -> guard registration | `superclaude install` and `update` merge `hooks.json` into `~/.claude/settings.json`; the claim refuses to launch if the guard is absent, stale or not registered | `src/superclaude/cli/main.py:219, 412`; `src/superclaude/hooks/hooks.json:63-71, 115-134`; `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:955-1045, 1730-1747` | BUILT-ON |
| 6 | guard -> orchestration commands (G2 rule 2) | a bound session may run `orca orchestration send` or `ask` only as one plain call with no `--to`; every other `orca` verb off the allow-list is blocked, but only for the command word `orca`: `orca-ide` is not constrained (observed exit 0), see Section 5.3 and Section 14 D-25 | `src/superclaude/hooks/scripts/launch-level-guard.sh:457, 480-491, 496-537`; `src/superclaude/core/WORKER-CONTRACT.md:66` | BUILT-ON |
| 7 | L2 hook -> job identity | the pre-push hook runs `identify $$` under a pinned `HOME` and `uv` directory to learn whether the pusher is governed | `src/superclaude/hooks/scripts/launch-level-pre-push.sh:52-101`; `src/superclaude/hooks/scripts/launch-job-identity.sh:215-260` | BUILT-ON |
| 8 | claim -> ccsession shim | detection only, by screen text or tab title; the shim carries no level; absence is a warning, not a refusal | `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1802-1811`; zero hits for `launch-level` under `src/superclaude/skills/ccsession-tag` | BUILT-ON |
| 9 | `--pipeline none` claim -> coordinator-started worker | prose only (run `orca_worktree.py worktree`, then `worker-start`); no code and no contract text | `src/superclaude/commands/issue.md:85`; `src/superclaude/core/WORKER-CONTRACT.md` (no such rule) | NOT BUILT |
| 10 | coordinator -> release of a bound worker | `release-worker` wrote `sessions/<sid>.ok`; the verb and guard rule 1 are gone | `src/superclaude/hooks/scripts/launch-level-guard.sh:496-497`; old `src/superclaude/cli/issue_pipeline/release.py:57-62` @01e7a9e23^ | REMOVED |

**Reading the map.** A watcher-launched session (hand-off 1) carries no marker, so the guard hand-offs do not apply to it: the guard exits 0 for a session with no marker and no bound record (`src/superclaude/hooks/scripts/launch-level-guard.sh:363-365`), and the watcher prompt must fully match a pattern with no marker (`src/superclaude/cli/issue_watch/launch.py:33`). Hand-offs 3, 4, 6 and 7 apply only to a session bound through a claim a person typed at `worktree`, `full` or `full --submit`; hand-off 5 is the install step they all rely on.

---

## Synthesis notes (for the assembler; not part of the document)

- Errata applied: agent files are 35 lines each; guard-stack tests are 14 table files plus 3 claim-side pin files (R05 gap-fill); templates are 15; the watcher modules sum to 4,795 lines. The 300 s value is the claim-marker tolerance (`src/superclaude/cli/issue_watch/predicates.py:17`) and the clock-skew warning threshold is 60 s (`src/superclaude/cli/issue_watch/cycle.py:44`); neither appears in Sections 1 or 2, they belong to the watcher subsystem section.
- The watcher test total (19,801 lines, 867 functions) is the sum of the per-file counts in R01 to R03; a read-only `wc -l` on the snapshot gave the same line total. The research-notes figures were not used.
- No contradiction between research files changes Sections 1 or 2. R05 states the watcher path creates no governed session on the strength of the notes; the code basis used here is `launch.py:33` (fixed prompt, no marker) plus `launch-level-guard.sh:363-365`.
- Remediation is not created here. Rows 7, 10, 13 to 18 of the ledger point to Section 14, which another synth file owns.
- Statistics appear only in Section 1; the single out-of-scope sentence appears only in Section 1.
- Not found in snapshot: dispatcher, `COORD-<RepoName>`, zero-setup install (ledger row 15).

