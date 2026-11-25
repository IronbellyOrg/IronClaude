# Synthesis 06: Conventions, Extension Guide, Tech Debt, Appendix B

**Sections:** 12, 13, 14, Appendix B
**Status:** Complete
**Date:** 2026-11-20

Snapshot: origin/master 61ac2c2e6 (read-only export). Removed code is labelled `@01e7a9e23^` (the parent of the removal commit). Path shorthand used in this file: `P` = `src/superclaude/cli/issue_watch/`; `T` = `tests/issue_watch/`; `GUARD` = `src/superclaude/hooks/scripts/launch-level-guard.sh`; `WCT` = `src/superclaude/core/WORKER-CONTRACT.md`; `OW` = `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`; `DES` = `docs/designs/issue-watcher.md`; `SET` = `docs/designs/issue-watcher-setup.md`. Status words are only BUILT-ON, BUILT-OFF (enabled:false), NOT BUILT, REMOVED. Tags are [CODE-VERIFIED], [CODE-CONTRADICTED], [UNVERIFIED] (plus [STALE DOC] for a doc statement that is out of date).

---

## 12. Conventions & Patterns

### 12.1 Code Conventions

| Convention | Rule | Where enforced | Pinned by test |
|---|---|---|---|
| Closed watcher vocabulary | Every reason is one of 59 names in `REASON_TABLE`, each mapped to `(kind, exit)`; `audit.line()` raises `ValueError` for an unknown kind, reason or key | `P/audit.py:26-104`; `exit_for` `P/cycle.py:480-482` | `T/test_audit.py:214` (names literal, in order), `:223` (every pair) |
| Closed guard words | 18 `LL-*` block words (16 classes plus `LL-NOBIND` and the default `LL-BROKEN`), printed as `Blocked:` / `Why:` / `You can:` | `GUARD:36-133` (`ll_say`), grid `:785-803` | `tests/hooks/test_launch_level_guard.py:1712` (`test_design_table_holds_all_eighteen_ids`; message texts read from the design doc at run time, `:72-85`) |
| Closed L2 and claim words | L2 words `L2-PROTECTED`, `L2-UNKNOWN`, `L2-MALFORMED`; claim STOP codes (13, prose) and warning codes (12) | `src/superclaude/hooks/scripts/launch-level-pre-push.sh:187-208`; `OW:230-239` (`WARNING_ORDER`), `:802-817` (`REMEDY`) | `tests/hooks/test_launch_level_pre_push.py` (T-01..T-24); `tests/skills/test_issue_protocol.py:350` (every warning code has a remedy line) |
| Write-ahead before launch | `pending` (launches = 1) is saved and fsynced before `orca agent launch`; a crash leaves `pending_orphan`, never a relaunch | `P/cycle.py:1082-1099` | `T/test_cycle.py:4737` (`test_a_failed_outcome_save_after_the_launch_never_relaunches__fr010_nfr005_c6`) |
| One subprocess module, `shell=False` | Only `runner.py` imports `subprocess`; argv lists only, closed stdin, mandatory timeout | `P/runner.py:10`, `:91-101` | `T/test_no_shell.py:150`, `:156` (AST scan); `T/test_module_boundaries.py:219-276` (exactly nine modules, import allow-list, four Protocol classes) |
| Hook exit codes | Claude Code hooks exit 0 (allow) or 2 (block), never 1; the L2 git pre-push hook is the only script in the area that exits 1 (`L2-PROTECTED`) | `GUARD:4`, `:138`; `launch-job-identity.sh:572-580`; pre-push `:9-10`, `:197-200` | guard grid tests `tests/hooks/test_launch_level_guard.py:3394`, `:3401`, `:3457`; `tests/hooks/test_launch_level_pre_push.py` |
| Level and identity travel by files | The level is read only from `~/.claude/state/launch-level/sessions/<session_id>`; the guard reads HOME only; the ccsession shim carries no level (zero grep hits in `skills/ccsession-tag`) | `GUARD:257-273`, `:23`; `launch-job-identity.sh:103` | no test pins "the shim carries no launch level" (research 05, Gap-fill c1 B-3 D; a negative search, not proof) |
| Plugin copies byte-identical | The three launch scripts under `plugins/superclaude/hooks/scripts/` equal the `src` copies; the two `hooks.json` files carry the same three launch registrations but are not identical as files | `cmp -s` identical (research 05 section 4.1) | `tests/hooks/test_launch_level_guard_l2_tokens.py:149`; `tests/cli/test_install_hooks.py:1086-1109`; `tests/hooks/test_launch_level_guard_registration.py:121` |
| GitHub text never reaches state, argv or prompt | Audit keys are a closed set; the prompt must match `^/sc:issue --claim [1-9][0-9]{0,8} --pipeline none$`; no argv builder asks `gh` for title, body or comments | `P/audit.py` `line()`; `P/launch.py:33`, `:84-92`; `P/github.py:175-262` | `T/test_no_text.py:530`, `:551`, `:599`, `:818`, `:939`; `T/test_security_invariants.py:462`, `:535`, `:652` |
| Read-only `gh`, fork fixed | Every REST call carries `--method GET`; GraphQL constants contain no `mutation`; repo is the literal `IronbellyOrg/IronClaude`; origin must match | `P/github.py:37`, `:206`, `:257`; `P/launch.py:233-251` | `T/test_security_invariants.py:652`, `:894`, `:912` |
| Governed sessions fail closed, ordinary sessions fail open | Governed = a `sessions/<id>` entry; anything unparseable for a bound id is `LL-BROKEN`; missing id or no record exits 0 | `GUARD:386-392`, `:218-237`, `:807-808` | `tests/hooks/test_launch_level_guard.py` ("ordinary sessions never blocked", "fail-closed resolution"); observed on 44 sandbox payloads (research 05) |
| Strict store shape | Exactly 7 top-level keys and 17-field entries; a field change needs a `MIGRATIONS` step | `P/record.py:120-131`, `:170-171`, `:247` | `T/test_record.py` (`the_pair_table_covers_every_state_and_trigger_once`) |
| Contract rules pinned as text | Each `WC-n` rule is a set of required phrases | `WCT`; `RULE_PHRASES` `tests/skills/test_worker_contract.py:25-436` | `tests/skills/test_worker_contract.py:876-878` (`test_contract_states_rule`) |
| Claim workers are read-only; the orchestrator alone writes | Workers write only under `.dev/issues/`; every git/gh write verb in skills, commands and agents is classified | `src/superclaude/agents/issue-worker-t1.md`..`t3.md`; write-verb audit | `tests/skills/test_issue_worker_agents.py`; `tests/skills/test_worker_contract.py:1840-3141` (`WRITE_VERB_RE` `:1863-1866`) |
| Tier pins are aliases | `claude-gw-tier*` text may appear only in allow-listed paths; the three worker pins are fixed | `tests/skills/test_model_alias_policy.py:29-33`, `:38-44` | `tests/skills/test_model_alias_policy.py:83-101`, `:104-119` |
| Claim marker has one literal | `predicates.CLAIM_MARKER` appears in both required copies; the template's last non-blank line is the marker | `P/predicates.py`; `refs/claim.md`; `templates/claim-comment.md` | `T/test_marker_contract.py:28-51` |

### 12.2 Architectural Patterns

| Pattern | Where Used | Description |
|---|---|---|
| Strict pipeline of closed decisions | Watcher cycle (`P/cycle.py`) | One `once` cycle is an ordered pipeline; every decision is a `REASON_TABLE` word; exit codes resolve by the fixed precedence 2, 6, 7, 5, 3, 4 (75 only alone), `P/cycle.py:466-477` |
| Single-writer store with write-ahead | `dispatch.json` (`P/record.py`) | Non-blocking `flock`, atomic replace, state saved before the outward effect (at-most-once launch) |
| Injected Protocols | Watcher modules | Exactly four Protocols (Runner, Store, Launcher, Clock); import allow-list per module (`T/test_module_boundaries.py:276`) |
| Nonce handoff to a bound session | Claim, then guard | `pending/<nonce>` is taken by one rename, hard-linked to `sessions/<sid>`; first binding wins (`GUARD:372-384`) |
| Prose protocol plus helper scripts | `/sc:issue --claim` | The orchestrating model follows `refs/claim.md`; three scripts do the mechanical parts; text is pinned by tests, not enforced by code |
| Two independent layers | L1 guard (Claude hooks) and L2 pre-push (git hook) | L2 covers pushes to `main`/`master` only; the commit/push/submit classes live only in L1 |

### 12.3 Anti-Patterns (Things to Avoid)

| Anti-Pattern | Why It's Wrong | Do This Instead |
|---|---|---|
| Importing `subprocess` outside `P/runner.py` | Fails the AST test and bypasses timeout and `shell=False` | Go through `Runner.run` |
| Reading a launch level from an env var or the shim | The level exists only as files; no code or test supports another channel | Read `sessions/<id>` as the guard does |
| Storing or printing GitHub text | Breaks the no-text tests and the closed audit keys | Keep only validated ids, closed words and times |
| Adding a Bash PreToolUse hook casually | `tests/hooks/test_freshness_subagent_start_policy.py:105-115` pins the exact set of three; the identity hook must stay last (`tests/hooks/test_launch_level_guard_registration.py:99`) | Update both tests in the same change |
| Treating `MAX_LAUNCHES_PER_CYCLE` as the cap | The constant is never read (`P/cycle.py:35`); the cap is the S1 halt (`:833-834`) | Cite the halt |
| Following design docs for `issue-pipeline`, `release-worker`, `stage-status` | Those commands are removed (see Appendix B) | Use the Section 14.1.2 table before trusting a design doc |

---

## 13. Extension Guide

All eight scenarios below name files, functions and tests that exist at 61ac2c2e6 (research 01 to 06). Skeletons are illustrative and use only names the research quotes. A scenario whose registration point the research does not give says so.

### 13.1 Common Extension Tasks

**13.1.1 Add a watcher skip or stop reason**

- Files: `P/audit.py` (`REASON_TABLE` `:26-102`, `REASONS` `:104`); the raise site in `P/cycle.py` (`_cond` `:587-588`, `_stopped` `:590-592`, `raise _Stop(...)` as at `:685-686`); exit comes from `exit_for` (`:480-482`) and `resolve_exit` (`:466-477`).
- Steps: add the name with its `(kind, exit)` pair; raise it where the decision is made; update the two literal pins in `T/test_audit.py`; add a cycle test in `T/test_cycle.py`.
```
# P/audit.py, inside REASON_TABLE (kinds: cycle, skip, entry, note; research 01 section 8)
"new_reason": ("<kind>", <exit>),
# P/cycle.py, where the decision is made
raise _Stop("new_reason")        # or self._cond("new_reason")
```
- Pinned by: `T/test_audit.py:214` (59 names, literal order), `:223` (pairs); the `df42_...` tests for `last_reason` words. Pitfall: the count 59 and the order are pinned; `DES` section 4.3 and its "59 reason names" line (`DES:716`) become stale; a `note` word must have kind `note` (`P/audit.py:229-243`).

**13.1.2 Add a watcher config key**

- Files: `P/cycle.py` (`_TOP_KEYS` `:58-69`, `Config` dataclass `:96-107`, `load_config` `:195-283`, unknown-key check `:216-220`); `P/cli.py:185-198` only if `check-config` should print it.
```
_TOP_KEYS = frozenset({..., "new_key"})      # cycle.py:58-69
# Config(..., new_key: <type>)               # cycle.py:96-107 (frozen)
# load_config: raw.get("new_key", <default>), validate, on failure raise _invalid("<fixed detail>")
```
- Pinned by: config and approvers rule tests in `T/test_cycle.py` (names not listed in research 03); `T/test_cli.py:351-452` (check-config). Pitfall: failures must use a fixed detail (details never echo file values); a key read by another consumer must be added here or `once` exits 2 `config_invalid` (the `orchestrator_repo` mismatch, row D-08); defaults such as `MAX_CANDIDATES` are module constants, not operator knobs (`P/cycle.py:33`).

**13.1.3 Add a read-only `gh` call**

- Files: `P/github.py` (argv builders `:175-262`; value checks `_issue_arg`, `_page_arg`, `_cursor_args`, `_trigger_arg`, `_login_arg`; `_call` `:557-577`; `classify`).
- Steps: one `argv_*` builder, REST path with `--method GET`; call through `_call` so the 5 s floor and `CallBudget` apply; return a typed `Read`; map failures to an existing `REASON_TABLE` word.
```
def argv_new(number, page):   # validate every caller value through the _*_arg helpers
    return ["gh", "api", "--method", "GET", "repos/IronbellyOrg/IronClaude/issues/<N>/<path>", "-F", "per_page=100", "-F", "page=<P>", "--jq", <JQ>]
```
- Pinned by: `T/test_github.py` (literal argv per builder; `CALL_CAP`, `RESERVED_CALLS`, `PAGE_CAP`); `T/test_security_invariants.py:712`, `:652`; `T/test_no_text.py:818`. Pitfalls: the per-issue budget is 32 plus 3 reserved (37 per cycle); a new fixture changes the count of 19 `_assumed_shape` files pinned at `T/test_github.py:575-583`; reply shapes stay assumed until a live test exists.

**13.1.4 Add a `--pipeline` level**

- Files: `src/superclaude/commands/issue.md` (option rows `:43`, STOP rule `:58`); `src/superclaude/skills/sc-issue-protocol/refs/claim.md:81` (level rule); `src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md` (a new block; names matched by `BLOCK_MARKER` `[a-z]+`, `OW:743`); `OW:1873`, `:1883`, `:1891` (`choices` of `prompt`, `launch`, `pending`); level word table `GUARD:264-269`; grid `GUARD:785-803`.
```
<!-- block:<name> -->                              # templates/launch-prompt.md; name is [a-z]+ and equals the level word (render_prompt keeps "common" + the level block, OW:756)
choices=["worktree", "full", "<name>"]            # OW:1873 (prompt), OW:1883 (launch); pending also lists "full-submit" at OW:1891
<name> | <name>$'\n') LL_LEVEL=<X> ;;              # GUARD:264-269 (read from the pending record)
<CLASS>:<X>) ll_deny "LL-<CLASS>" ;;               # one cell per class for the new level in the case at GUARD:785-803; a missing cell becomes LL-BROKEN
```
- Pinned by: `tests/skills/test_issue_protocol.py:295` (four-block assertion); `tests/commands/test_issue_command.py:84` (options table); the PR and LA tests in `tests/skills/test_issue_orca_worktree.py`. Pitfall: the level pick is prose run by the model (D-20); `pipeline.json` is not built (D-22).

**13.1.5 Add a guard level or classifier word and its matrix test**

- Files: `GUARD` (Skill classifier `:398-413`, IMPL pattern `implement | task | cleanup` at `:409`; Bash classifiers `:414-726`; precedence list `:783`; grid `:785-803`; words `:36-133`) and its byte-identical copy `plugins/superclaude/hooks/scripts/launch-level-guard.sh`; the design table of message texts in `docs/designs/sc-issue-launch-level-hook.md` (read by a test at run time).
```
# GUARD :783  precedence: BIG TAMPER MERGE GHWRITE PROTECTED ESCAPE MCP UNKNOWN SUBMIT REPO PUSH PUSHFORM COMMIT TURN IMPL SKILL <NEWCLASS>
# GUARD :785-803  one cell per level W WA F FS; a class with no cell becomes LL-BROKEN (:801)
#   <NEWCLASS>:W | <NEWCLASS>:WA | <NEWCLASS>:F | <NEWCLASS>:FS) ll_deny "LL-<NEWCLASS>" ;;     # or a `;;` with no action where the level allows it
# the classifier that sets the class in $LL_CLASSES (Skill :398-413, Bash :414-726): not determinable from research for a new class beyond these ranges
```
- Pinned by: `tests/hooks/test_launch_level_guard.py` `test_grid_policy` `:3394`, `test_grid_complete` `:3401`, `test_grid_level_steps` `:3457` (hand-written oracle), `test_skill_grid_matches_oracle` `:905`, `test_impl_name_spellings` `:927`, `test_lookalike_skill_names_stay_none` `:936`, `test_design_table_holds_all_eighteen_ids` `:1712`, `test_precedence_order` `:4520`; copy check `tests/hooks/test_launch_level_guard_l2_tokens.py:149`. Pitfalls: the design lists six IMPL skills but code has three (row KW-6 in 14.1.2); the guard matches the basename `orca` only (D-25).

**13.1.6 Register a new hook script**

- Files: `src/superclaude/hooks/scripts/<name>.sh`; `_FRESHNESS_SCRIPTS` in `src/superclaude/cli/install_hooks.py:42-97` (launch scripts at `:90`, `:93`, `:96`); `src/superclaude/hooks/hooks.json` (PreToolUse groups `:85-134`; identity hook must stay last, `:125-134`); `plugins/superclaude/hooks/hooks.json` (hand-kept; it already differs from `src` in three documented ways); byte-identical `plugins/superclaude/hooks/scripts/<name>.sh`.
```
# src/superclaude/hooks/hooks.json, inside the "PreToolUse" array (the identity group stays last, :125-134)
{ "matcher": "<tool regex>", "hooks": [ { "type": "command", "command": "~/.claude/hooks/<name>.sh", "timeout": 5 } ] }
# src/superclaude/cli/install_hooks.py, inside _FRESHNESS_SCRIPTS (:42-97), after the launch scripts at :90, :93, :96
"<name>.sh",
```
- Registration row: event, matcher, command `~/.claude/hooks/<name>.sh`, timeout (the guard and identity use 5), no `onFailure` key (pinned). A git hook (like the L2 pre-push) is not registered in `hooks.json`; it is installed by the claim.
- Pinned by: `tests/cli/test_install_hooks.py:1086`, `:1104` ("packaged, listed, executable, mirrored" pattern), `:897`; `tests/hooks/test_launch_level_guard_registration.py:45-121`; `tests/hooks/test_freshness_subagent_start_policy.py:91-115` (exact set of Bash PreToolUse commands). Pitfalls: a plain `superclaude install` skips an existing script (only `update` and `--force` refresh, `install_hooks.py:282-284`, `main.py:219`, `:412`); a registration collision is decided by command path (`:405-418`).

**13.1.7 Add a claim worker tier or template**

- Worker: `src/superclaude/agents/issue-worker-tN.md` (line 5 `tools: Read, Grep, Glob, Write, Bash`; line 6 `model: claude-gw-tier...`); `WORKERS` dict `tests/skills/test_issue_worker_agents.py:21-26`; `ISSUE_WORKER_PINS` `tests/skills/test_model_alias_policy.py:29-33` and `TIER_TEXT_ALLOWED` `:38-44`; `SKILL.md:58-62`; `refs/tiers.md:11-15`; the tier key in `src/superclaude/skills/ccsession-tag/ccsession-models.json` (tier keys at lines 85, 93, 104, 113).
```
# src/superclaude/agents/issue-worker-tN.md, frontmatter (as in issue-worker-t3.md:1-8)
name: issue-worker-tN
tools: Read, Grep, Glob, Write, Bash
model: claude-gw-<tier>
# tests/skills/test_issue_worker_agents.py:21-26, WORKERS
"issue-worker-tN": ("claude-gw-<tier>", "<tier>"),
```
Which tier a new worker takes and how the orchestrator picks it (`SKILL.md:58-62`, `refs/tiers.md:11-15`) are prose rules: the selection logic is not determinable from research.
- Template: a file under `src/superclaude/skills/sc-issue-protocol/templates/` plus a row in the `SKILL.md` files table (`:36-50`); pinned by `tests/skills/test_issue_protocol.py:147` (two-way inventory). Posted templates must end with their marker.
- Pitfalls: `test_tier_ids_appear_only_in_allowed_paths` (`:104`) fails unless the new path is allowed; the scan does not cover `docs/designs/`, so a stale tier text there is not caught (KW-7).

**13.1.8 Add a coordinator contract rule**

- Files: `WCT` (rules are `**WC-n.` bullets in sections 2 to 4; section 4 starts `:68`); `tests/skills/test_worker_contract.py` `RULE_PHRASES` (`:25-436`, rule name to required phrases; consumed by the parametrized `test_contract_states_rule` `:876-878`). If the rule names a command that must never run as a worker, also the list at `:444-454` (`_check_never_as_worker` `:734`); if it names a git or gh write verb, classify it in the write-verb audit (`:1840-3141`).
```
RULE_PHRASES["<rule-name>"] = ["<required phrase 1>", "<required phrase 2>"]   # tests/skills/test_worker_contract.py
```
- Pitfalls: no test pins the absence of a removed rule (WC-17 has 0 hits anywhere in tests); `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:196`, `:285` quote rule counts and line ranges that drift (X-28); whether a plugin copy of the contract exists: not determinable from research.

### 13.2 Testing Requirements for Changes

| Change Type | Required Tests | Test Location |
|---|---|---|
| New or renamed reason word | literal name list and `(kind, exit)` pairs; one cycle path | `T/test_audit.py:214`, `:223`; `T/test_cycle.py` |
| New `gh` or Orca argv | literal argv, no-text, allowed-form scan | `T/test_github.py`, `T/test_launch.py:75`, `T/test_no_text.py:818`, `T/test_security_invariants.py:712` |
| Store field or state change | pair table, `MIGRATIONS`, key-set check | `T/test_record.py` |
| New module or import | module list and import allow-list; AST rule | `T/test_module_boundaries.py:219-276`, `T/test_no_shell.py:150-156` |
| Guard class, level, word | oracle grid, precedence, 18-id table, byte-identical copy | `tests/hooks/test_launch_level_guard.py`, `tests/hooks/test_launch_level_guard_l2_tokens.py:149` |
| Hook registration or install | registration pins, install pins, exact Bash hook set | `tests/hooks/test_launch_level_guard_registration.py`, `tests/cli/test_install_hooks.py`, `tests/hooks/test_freshness_subagent_start_policy.py:91-115` |
| Claim script, template or worker tier | inventory, warning-code remedies, tier pins, marker | `tests/skills/test_issue_protocol.py`, `tests/skills/test_issue_orca_worktree.py`, `tests/skills/test_issue_worker_agents.py`, `tests/skills/test_model_alias_policy.py`, `T/test_marker_contract.py` |
| Contract rule | required phrases; never-as-worker list; write-verb audit | `tests/skills/test_worker_contract.py` |

Evidence limit: these tests were read by name and selected bodies, not run (Q-22 in 14.3).

---

## 14. Known Limitations & Technical Debt

Scope note: every row below comes from the six research files, including their Gap-fill errata (which supersede earlier wording). The row about `DES:827` is not a contradiction: it is [CODE-VERIFIED] (see KW-1).

### 14.1 Current Limitations

#### 14.1.1 Limitations table

| Limitation | Impact | Workaround | Planned Fix |
|---|---|---|---|
| The real watcher cycle is BUILT-OFF: `enabled` defaults to false (`P/cycle.py:228`, stop `not_enabled` `:685-686`) and no scheduler artefact exists in the snapshot | No issue is claimed automatically | `once --dry-run` bypasses `enabled` and stops before the launch step | FU-2 cron entry, gated behind the live test (`DES:861`; `SET:676`); `SET:288`: "This work does not install or enable the entry" |
| All 19 `gh` and Orca reply fixtures are `_assumed_shape: true`; no live-test record exists | The reason a live failure produces (`gh_auth_failed`, `rate_limited`, `gh_non_json`, `launch_unknown`) is unverified | Owner-run live test (FU-1) | FU-1 (`DES:33`; `SET:272`): "You write that file; the implementation does not" |
| One launch step per cycle; `claimed` is terminal and `reset` refuses it (`P/record.py:448`) | A claimed issue is never dispatched again by the watcher | none documented | none (`DES:478`) |
| Stuck entries (`unknown`, `claim_not_observed`, `spawn_error`) cost at least one G4 call every cycle while the issue is discovered (`P/cycle.py:922-931`) | Budget use grows with stuck issues | `reset N --forfeit-guarantee` | none recorded (open question Q-02) |
| The edit check runs once before the re-read (`P/cycle.py:1006`) | A body edit between the G5 read and the launch is not seen | none | none recorded (Q-03) |
| Linux only for `once`, `check-config`, `init-state`, `reset` (`P/cli.py:88`, `:314`); `status` is not checked (`:169`); identity hook needs Linux and `uv` | Other platforms exit 2 | none | none |
| The guard governs only a session bound by a claim launch at `worktree` or `full`; a `--pipeline none` claim (the watcher launch) creates no pending record | The watcher's claim session and coordinator-started workers are outside the guard | none | none recorded (D-18) |
| L1, L2 and identity cover only the tested local Bash surface (limits LIM-1..LIM-20; identity returns 0 for any non-Bash tool, `launch-job-identity.sh:442-444`) | Monitor, `setsid`, a killed supervisor and some `git --no-verify` spellings are outside | none | declared limits, owner decision OD-1 (`docs/designs/sc-issue-launch-level-hook.md:534`) |
| After a `--pipeline none` claim no code or contract rule starts a worker (`docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:268`) | The claimed issue waits for a person | a person-opened coordinator by hand | none (D-16) |

#### 14.1.2 Doc-vs-code contradiction table

Part A: the eight known staleness warnings (BUILD-REQUEST), each confirmed or refuted by code.

| ID | Doc path:line | Doc claim | Code reality (path:line) | Tag | Research file |
|---|---|---|---|---|---|
| KW-1 | `DES:827` | "skew tolerance 300 s, equals the cadence" is a stale clock-skew value | NOT contradicted. 300 s is the claim-marker window `SKEW_TOLERANCE_S` (`P/predicates.py:17`, used `:295`); the clock-skew warning is 60 s, `SKEW_WARN_S` (`P/cycle.py:44`, used `:774`); `DES:510` says 60. The label "skew tolerance" is ambiguous, the number is right | [CODE-VERIFIED] (label ambiguous) | R01 row 22; R03 Gap-fill c1 F-1 |
| KW-2 | `DES:380`, `DES:819` | `max_launches_per_cycle` = 1 is a default | Behaviour exists (S1 halt `P/cycle.py:833-834`); the constant `MAX_LAUNCHES_PER_CYCLE` (`:35`) is never read (row D-01) | [STALE DOC] | R01 Gap-fill c1 B-1 |
| KW-3 | `SET:170`; `SET:616-619`; `SET:5`, `SET:270-274` | Cites `WCT` section 4 "Issue pipeline duties"; launch capture command is `--prompt '/sc:issue --claim <test issue>'`; a live-test file is a deliverable; no dispatcher or zero-setup step | `WCT` has 0 hits for "Issue pipeline duties" (section 4 is "Coordinator rules", `:68`); code prompt ends `--pipeline none` (`P/launch.py:33`, `:92`; `SET:170` and `:575` do mention it); `docs/designs/issue-watcher-live-test.md` absent; "dispatcher", `COORD-`, "zero-setup watcher": not found in snapshot | [CODE-CONTRADICTED] | R03; R02; R06 |
| KW-4 | `docs/designs/issue-pipeline-fu1.md:64-66` | Runbook runs `superclaude issue-pipeline plan-hash` / `check-approval`, cites `src/superclaude/cli/issue_pipeline/plan_hash.py` | Command group and directory absent (`src/superclaude/cli/main.py` has no registration; `CHANGELOG.md:17` records the removal). `:36` is accurate as history | [CODE-CONTRADICTED] | R03; R05; R06 |
| KW-5 | `docs/designs/issue-pipeline-guard-g2.md:13`, `:22`, `:9`, `:18`, `:45-51` | Allow-list lines `:471-474` and TAMPER `:703`; rule 1 / route A `release-worker` is live design; a coordinator calls `orca_worktree.py pending` | Lines now `GUARD:480-491`, `:760-762`; rule 1 retired (`GUARD:496`); zero hits for `release-worker`; `pending` exists (`OW:1515`, `:1886-1893`) but has no production caller (D-18) | [CODE-CONTRADICTED] (lines, route A); [UNVERIFIED] (caller) | R05 rows 5, 8, 9; R04 |
| KW-6 | `docs/designs/sc-issue-launch-level-hook.md:106`, `:179`, `:236`, `:391`; `:123` | IMPL skills are implement, task, improve, cleanup, spawn, build; row 34: a typed `approved` writes `.ok` | `GUARD:409` matches `implement \| task \| cleanup`; `improve`, `spawn`, `build` are absent from `src/superclaude/commands`; the design contradicts itself (`:189` says plain `approved` was removed); code accepts only a first line `/sc:implement` or `/task` (`GUARD:347`) | [CODE-CONTRADICTED] | R05 rows 1, 2 |
| KW-7 | `docs/designs/sc-issue-command.md:3`, `:58`, `:107`, `:129`, `:391`, `:423`, `:449`; `docs/designs/sc-issue-claim-pipeline-flag.md:21`, `:43`, `:66` | Status "Design only (nothing implemented)"; T3 pinned to `claude-gw-tier3`; default level is `worktree` | Command, skill, scripts, agents and tests exist; `src/superclaude/agents/issue-worker-t3.md:6` pins `claude-gw-tier2b`; the default is a prose pick at `refs/claim.md:81` (`full` for a person-typed bug or small feature, else `worktree`; the watcher passes `none`); no test scans `docs/designs/` | [CODE-CONTRADICTED] / [STALE DOC] | R04 |
| KW-8 | scope hint (no doc line) | The ccsession shim carries the launch level | Zero grep hits for launch-level text in `src/superclaude/skills/ccsession-tag`; the level travels by files only; the claim only detects the shim (`OW:1564-1583`, warning `W-LAUNCH-NOT-CCSESSION` `:1802-1811`) | [CODE-CONTRADICTED] | R05 section 5.2 |

Part B: every other contradicted or stale row in the research files.

| ID | Doc path:line | Doc claim | Code reality (path:line) | Tag | Research file |
|---|---|---|---|---|---|
| X-1 | `DES:331`, `:362`, `:621` | `find_orca` result cached per cycle | "caches nothing" (`P/launch.py:6`, `:177`); `OrcaLauncher` holds only the runner (`:352-356`) | [CODE-CONTRADICTED] | R01; R02 |
| X-2 | `DES:360` | Step 10 local checks "Calls 0" | Entries in `launched`/`unknown`/`abandoned` read G4; tombstones and backoff entries read G4 and G3 (`P/cycle.py:922-935`) | [CODE-CONTRADICTED] | R01 |
| X-3 | `DES:173` | Exit 7 combines with 5 or 3 | Unreachable through `_Cycle` (halt `P/cycle.py:833-834`); only 7 with 6 occurs; `resolve_exit` accepts any set (`:466-477`) | [CODE-CONTRADICTED] | R01 |
| X-4 | `DES:406` | `audit.jsonl` written by every exit and read by `status` and the SLO reducer | Several exits write only stderr (`P/cli.py:79-81`, `:127`, `:219`; `P/cycle.py:1195-1196`); nothing reads the file (`:1279-1284`); `slo_numbers` has no caller | [CODE-CONTRADICTED] | R01; R03 |
| X-5 | `DES:722` | `clock_skew_s` always present on the cycle line | Optional (`P/audit.py:165`); absent without a parseable `Date` header (`P/cycle.py:770-773`) | [CODE-CONTRADICTED] | R01 |
| X-6 | `DES:15`, `:41` | Watcher prompt is `/sc:issue --claim <N>` | `/sc:issue --claim <N> --pipeline none` (`P/launch.py:33`, `:84-92`); `DES:43`, `:49` already say none | [CODE-CONTRADICTED] | R01; R03 |
| X-7 | `SET:616-619` | Capture-sheet launch lacks `--pipeline none` | The watcher always sends it (`P/launch.py:92`; `tests/issue_watch/test_security_invariants.py:936-1009`); a fixture captured this way records a launch the watcher cannot make | [CODE-CONTRADICTED] | R02; R03 |
| X-8 | `CHANGELOG.md:9`; `src/superclaude/skills/agent-work-report/scripts/common.py:22-40`; `tests/skills/test_agent_work_report.py:2979-3000` | The poll config carries `orchestrator_repo` for `agent-work-report` | `_TOP_KEYS` lacks it (`P/cycle.py:58-69`); unknown keys exit 2 `config_invalid` (`:216-220`) | [CODE-CONTRADICTED] (cross-consumer) | R01; R03 |
| X-9 | `DES:43`; `SET:170` | Two inputs approve the plan, "read by the coordinator through `stage-status`" | `stage-status` is removed (`CHANGELOG.md:17`; Appendix B) | [CODE-CONTRADICTED] | R03; R06 |
| X-10 | `DES:75` | Platform check omits `reset` | `P/cli.py:314` checks it for `reset` | [CODE-CONTRADICTED] | R03 |
| X-11 | `DES` section 4.1 (no line in research) | `once` exit list omits 1; `reset --rate-limit` list omits 2 | Per research 03 Gaps 6 | [CODE-CONTRADICTED] | R03 |
| X-12 | `DES:137`; `DES:154-155` | Label and approvers-file rules complete | Label bans on comma, quote, leading dash (`P/cycle.py:127-139`); 1 MiB and UTF-8 rules (`:75`, `:341-349`) | [CODE-CONTRADICTED] (incomplete) | R03 |
| X-13 | `DES` (no line) | `_ORCA_CLIS` at `install_user_setup.py:35` | Line 36 | [CODE-CONTRADICTED] (minor) | R03 |
| X-14 | `DES:103` | `--retry-launch` appears nowhere | `launch.retry_argv` contains it (`P/launch.py:119-132`) | [STALE DOC] | R03 |
| X-15 | `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:1059` | `issue-watch` registered at `cli/main.py:563-565` | Lines `:577-579` | [STALE DOC] | R03 |
| X-16 | `docs/user-guide/cli-groups.md` | Verbs and examples complete | No exit codes, no `enabled` default, no note that no timer is installed | [STALE DOC] (incomplete) | R03 |
| X-17 | `SET` section 8.5 | Relies on a "grant" and a coordinator handoff | No dispatcher, no zero-setup step; no code implements a grant or handoff | [STALE DOC] | R03 |
| X-18 | `DES:485` | T-1 only from "(none)" | `record.fail` also runs from `failed` (`P/record.py:511`) | [STALE DOC] (minor) | R02 |
| X-19 | `DES:640` | Operation id is a non-empty `str` | `^[A-Za-z0-9._:-]{1,128}$` (`P/launch.py:36`, `:287-289`, `:347-348`) | [STALE DOC] (code stricter) | R02 |
| X-20 | `tests/issue_watch/test_find_orca_parity.py:13-18` | Original `_find_orca` at `install_user_setup.py:216-219` | Now `:247-270`; behaviour unchanged | [STALE DOC] (lines) | R02 |
| X-21 | `src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md:23` | `/sc:task` is a releasing first line | `GUARD:347` accepts only `/sc:implement` and `/task`; no `sc:task` in the guard (row D-23) | [CODE-CONTRADICTED] | R04 |
| X-22 | `docs/designs/sc-issue-command.md:154-158` | Wave 0 has no Orca check and no `--limit 200` | `refs/claim.md:17`, `:28` | [STALE DOC] | R04 |
| X-23 | `refs/claim.md:125`; `SKILL.md:35`, `:92`; `refs/tiers.md:32`, `:44`; `docs/designs/sc-issue-claim-pipeline-flag.md:59` | L2 hook "in the new worktree"; IR-4 runs "before anything else"; `--git-path hooks/pre-push`; four subcommands; heading once | Shared `<git-common-dir>/hooks/pre-push` (`OW:1365`, `:1402`); record, already-launched and stale-prompt checks run first (`:1700-1724`); `--git-path hooks` (`:1357`); `pending` (`:1886`) unnamed in docs; heading appears twice | [STALE DOC] | R04 |
| X-24 | `docs/reference/model-aliases.md:12`, `:18` | Test lines "46-47 and 100-115", "36-40"; three allowed locations | `TIER_TEXT_DIRS` `:50`, `TIER_TEXT_ALLOWED` `:38-44`, test `:104-119`; a fourth location `src/superclaude/cli/review/data/` (`:43`) | [CODE-CONTRADICTED] (lines, omission) | R04 Gap-fill c1 F-2 |
| X-25 | `docs/designs/issue-pipeline-guard-g2-no-to.md:7`, `:48`, `:57` | Block at lines 500-549; rule WC-17 holds the no-`--to` sentence; `release-worker` | Block now `GUARD:496-537`; WC-17 removed, the sentence is the bullet "Messages carry no `--to`" (`WCT:66`); the guard change itself is built | [CODE-CONTRADICTED] | R05; R06 |
| X-26 | `docs/designs/sc-issue-launch-level-hook.md:23` vs `docs/designs/issue-pipeline-guard-g2.md:9` | "Not governed" versus "must be bound before any other issue runs" | Code binds only claim launches; the two docs disagree | [CODE-CONTRADICTED] between docs | R05 row 10 |
| X-27 | scope hint (no doc line) | Plugin `hooks.json` differs only by lacking ccsession-tag entries | Also lacks the `pragmatic-subagent.js` entry; `freshness-subagent-start.sh` has `async: true` in the plugin only | [CODE-CONTRADICTED] (hint) | R05 row 21 |
| X-28 | `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:196`, `:285`, `:1058`, `:1133` | "WC-2 to WC-15 in a 327-line contract"; ranges `:67-282`, `:283-327`; `orca_worktree.py` line counts | `WCT` is 339 lines with WC-2..WC-16 (ranges `:68-297`, `:299-339`); counts are for an older checkout; `:268` is accurate | [STALE DOC] | R06 |

### 14.2 Technical Debt

No remediation tasks were created because this run may write nowhere outside its task folder and the output file; the rows below are listed for the owner to decide. Where a decision for a removal is recorded in a file this reference cites, the row cites it (`CHANGELOG.md:17` for the removed items; `docs/designs/sc-issue-launch-level-hook.md:23` for the guard not governing a coordinator-started worker). A row with no cited decision has none in the files read; none is relabelled a "known gap".

| ID | Capability | Declaring doc path:line | Code evidence | Class | Status word | Note |
|---|---|---|---|---|---|---|
| D-01 | `max_launches_per_cycle` = 1 as a named default | `DES:380`, `:819`; `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:1740` | `MAX_LAUNCHES_PER_CYCLE = 1` at `P/cycle.py:35`, no other hit in `src/` or `tests/`; the cap is `_Cand.launching` plus `halt` (`:1028`, `:833-834`) | DEFECT CANDIDATE (dead constant) | NOT BUILT (constant unread; the cap itself works) | No decision found; low severity |
| D-02 | `status` reads `audit.jsonl` | `DES:406` | `status_report` takes `audit` "accepted for the fixed signature and not read" (`P/cycle.py:1279-1281`); only writers elsewhere | DEFECT CANDIDATE | NOT BUILT (reader) | No decision found |
| D-03 | SLO numbers (p95 approval-to-launch, exit-0 share, claimed share, stale count) as a report | `DES:750-752`, `:869`; `SET:455-478`, `:684` | `slo_numbers` (`P/cycle.py:1359`) and `SloNumbers` (`:1339`) have no caller; only `T/test_slo_helper.py` and an owner-run snippet (`SET:467-475`) | NOT BUILT | NOT BUILT | `DES:752`: "a library function with a fixture test, not a verb" records "no verb", not "no caller"; FU-10 |
| D-04 | Scheduled trigger for `issue-watch once` (cron every 5 min, FU-2) | `DES:15`, `:30`, `:861`; `SET:198`, `:286-290`, `:676`; `P/cli.py:98` | No timer, installer or action in `P`, `.github`, `.claude`, `plugins`, `scripts`, Makefile, pyproject, package.json | NOT BUILT | NOT BUILT | Decision: `DES:28`, `:30` out of scope; `SET:288`; ordering behind FU-1 (`DES:33`, `:861`) means "later", not "out of scope" |
| D-05 | Owner-run live-test record and replacement of every `_assumed_shape` fixture (FU-1) | `DES:33`, `:775`, `:860`; `SET:5`, `:270-274`, `:586-625`, `:675` | `docs/designs/issue-watcher-live-test.md` absent; 19 fixtures assumed (`T/test_github.py:575-583`); no code checks the gate | NOT BUILT | NOT BUILT | Decision: `DES:33` ("neither this design nor its implementation writes it"); `SET:272`, `:625` |
| D-06 | The whole real watcher cycle | `DES:3`, `:33` | `P/cycle.py:228`, `:685-686`; no shipped config file | BUILT-OFF by design | BUILT-OFF (enabled:false) | Decision: `DES:33` deployment gate |
| D-07 | `prompt_invalid` entry for a bad issue number | `DES:362`, `:170` | Only reachable for a non-int or out-of-range number (`P/launch.py:90-91`), which `github.discover` rejects first (`P/github.py:827-828`); reached only by `T/test_cycle.py:3348` | DEFECT CANDIDATE (unreachable path) | BUILT-ON (unreachable in practice) | No decision found; low |
| D-08 | One config file read by two consumers | `src/superclaude/skills/agent-work-report/scripts/common.py:22-25`, `:40`; `CHANGELOG.md:9`; `tests/skills/test_agent_work_report.py:2979-3000` | `_TOP_KEYS` lacks `orchestrator_repo` (`P/cycle.py:58-69`); unknown keys exit 2 (`:216-220`); without the key the skill exits "the orchestrator repo is unknown" unless `AWR_ROOT` is set | DEFECT CANDIDATE (cross-consumer) | BUILT-ON (consumers contradict) | No decision found |
| D-09 | `record.disabled_present(state_dir)` | `DES:228` | Defined `P/record.py:748-750`; only `T/test_record.py:861`, `:870` call it; the cycle uses `FileStore.disabled()` (`P/cycle.py:712`, `:1063`) | DEFECT CANDIDATE (dead code) | BUILT-ON (no production caller) | No decision found; low |
| D-10 | `LaunchOutcome.detail` (8 words, `LAUNCH_DETAILS`) | `DES:634-641` (details are code-only, `P/launch.py:58-70`) | No read of `.detail`; `_launch` uses `kind` and `operation_id` only (`P/cycle.py:1101-1112`); the reason an `unknown` happened is lost | DEFECT CANDIDATE (dead field) | BUILT-ON (set, never read) | No decision found; low |
| D-11 | `launch_login`, `launch_account_id` | `DES:437-438` | Written (`P/record.py:548-568`) and validated (`:180`, `:185`); no reader in `src` | DEFECT CANDIDATE (write-only) | BUILT-ON (write-only) | Informational |
| D-12 | Automatic retry of an `unknown` launch (FU-8) | `DES:867`; `SET:682` | `retry_argv` (`P/launch.py:119-132`) is only printed by `status_report` (`P/cycle.py:1308-1312`) | NOT BUILT | NOT BUILT | Deferred "after FU-1 confirms the C20 argv" |
| D-13 | Cleanup of orphan `dispatch.json.*.tmp` | `DES` C2 row (about `:535`) | No unlink beyond the in-exception one (`swarm/atomic.py:33-38`) | NOT BUILT | NOT BUILT | Decision: the orphan "is ignored" (`DES` about `:535`) |
| D-14 | Bound or pruning rule for finished entries (FU-11) | `SET:685`; `DES:870` | Only `reset_entry` removes `abandoned`/`unknown` (`P/record.py:706-720`) | NOT BUILT | NOT BUILT | Deferred "when the store is above 1 MiB" |
| D-15 | Alerting FU-4, ETag FU-5, per-actor checks FU-6, approver role check FU-9, local-FS allow-list FU-12 | `DES:862-871`; `SET:673-686` | No code (`status` only prints a retry command) | NOT BUILT | NOT BUILT | Listed as follow-ups: "None of these is built by this work" |
| D-16 | Coordinator hand-off after a claim (adopt, create the issue worktree, `worker-start`); dispatcher, `COORD-<RepoName>` worktree, zero-setup install | `DES:43`; `SET:170`; `docs/designs/issue-pipeline-fu1.md:9-12`; `src/superclaude/commands/issue.md:85`; `refs/claim.md:96` | `WCT` has no "Issue pipeline duties", `adopt`, `watcher` or `claim` (0 hits); `COORD-` 0 hits; no Python in `src/` calls Orca `worker-start` or `task-create`; `/sc:issue` is never-as-worker (`WCT:23`); "dispatcher", `COORD-`, "zero-setup watcher": not found in snapshot | NOT BUILT | NOT BUILT | No file records this as out of scope or a replacement as built; `CHANGELOG.md:17` records removal of the old duties; who starts a worker after a claim is undefined (Q-10) |
| D-17 | `issue-pipeline` CLI, WC-17, "Issue pipeline duties" (plan-hash binding, approval record, edit detection, revocation, adoption row, `release-worker`, fixed brief) | `CHANGELOG.md:17`; `docs/user-guide/cli-groups.md:25`; named as live by `DES:43`, `SET:170`, `:274` | `src/superclaude/cli/issue_pipeline/`, `tests/issue_pipeline/`, `tests/cli/test_issue_pipeline_registered.py` absent; only trace: comment `GUARD:496` | REMOVED (deliberate) | REMOVED | Decision: `CHANGELOG.md:17`; commit 01e7a9e23 (PR 682) |
| D-18 | Binding of coordinator-started workers: `orca_worktree.py pending` plus a marker line `[sc-launch:v1:<nonce>]` in the brief | `OW:7-9`, `:1516`; `docs/designs/issue-pipeline-guard-g2.md:9`, `:18`; `WCT:66` | `pending` defined (`OW:1488-1523`, `:1886-1893`) and tested (`tests/skills/test_issue_orca_worktree.py:2472-2498`; `tests/hooks/test_launch_level_guard_worker.py:287`), no production caller; the only marker generator `brief.build` was removed; the contract template (`WCT:303-311`) has no marker slot | DEFECT CANDIDATE | NOT BUILT (binding and caller); the `pending` verb itself is BUILT-ON | No decision found in the files this reference cites; the guard design says it does not govern such a worker (`docs/designs/sc-issue-launch-level-hook.md:23`); the "bound worker" sentences describe a path no code starts |
| D-19 | IR-7 refusal when L2 is not owned | `src/superclaude/commands/issue.md:16`; `SKILL.md:92`; `refs/claim.md:134`; `docs/designs/sc-issue-launch-level-hook.md:34`, `:355`, `:516`, `:615` | `IR7_REFUSE = False` (`OW:822`); branch `:1757-1758`, `:829-831` unreachable; `tests/skills/test_issue_l2_install.py:639` | BUILT-OFF (a constant) | BUILT-OFF (`IR7_REFUSE = False`; not `enabled:false`) | Decision: `OW:818-822` ("owner decision OD-3", "2026-11-08": on only after the #442 observations pass); listed for visibility |
| D-20 | Default `--pipeline` pick from type, complexity, hours | `issue.md:43`; `refs/claim.md:81`; `sc-issue-claim-pipeline-flag.md:21`, `:43` | Prose only; no function computes it; tests pin text (`tests/skills/test_issue_protocol.py:774`, `:791`; `tests/commands/test_issue_command.py:182`) | DEFECT CANDIDATE | NOT BUILT (as code) | No decision found that prose-only is deliberate |
| D-21 | Ship gate "no governed claim until OB-H1 item 1, OB-H2, OB-H3 pass" and the live observations OB-H1..3 and OB-CTX | `issue.md:16`; `SKILL.md:92`; `refs/claim.md:136`; `sc-issue-launch-level-hook.md:6`, `:625` | 0 hits for `OB-H1..3` in `src/superclaude` code; `cmd_launch` (`OW:1696-1834`) never reads a record; 12 tests skip unconditionally (`tests/hooks/test_launch_level_observations.py:79-84`); `--pipeline worktree` or `full` can run today | NOT BUILT | NOT BUILT (mechanism; prose gate) | Design `:625` says "Pending, none run"; no decision lets the gate stay unenforced in code |
| D-22 | IR-3 `pipeline.json` level file | `sc-issue-claim-pipeline-flag.md:58`; `sc-issue-launch-level-hook.md:34`, `:351`, `:615` | 0 hits in `src/` and plugins | NOT BUILT | NOT BUILT | Decision: `pipeline-flag.md:58`, `:4` (documentation only); hook design `:34` |
| D-23 | Approval by a first line `/sc:task` | `templates/launch-prompt.md:23` | `GUARD:347` accepts only `/sc:implement` and `/task` | DEFECT CANDIDATE | NOT BUILT | No decision found (which side is intended: Q-14) |
| D-24 | Automatic action on `W-LAUNCH-NOT-CCSESSION` | `refs/claim.md:130` | `OW:1803-1811` adds a note and continues; no close call | NOT BUILT | NOT BUILT (warning only) | Remedy asks a person to close it |
| D-25 | L1 recognition of the Orca CLI under its real name `orca-ide` | `sc-issue-launch-level-hook.md:119`, `:175` | Guard matches basename `orca` only (`GUARD:457`); observed exit 0 for `orca-ide terminal send` and `orca-ide orchestration send --to run:run_1`; `orca-ide` is the default in `src/superclaude/cli/sweep/probes.py:43` | DEFECT CANDIDATE (observed) | NOT BUILT (recognition of `orca-ide`) | No decision found; the architecture reference `:83` records it as a DEFECT with a draft plan that "is not a fix" |
| D-26 | G2 route B (signed approval file) | `issue-pipeline-guard-g2.md:24` | 0 hits for signature, hmac or openssl in guard and identity | NOT BUILT | NOT BUILT | `guard-g2.md:26` recommends route A, itself REMOVED (D-27) |
| D-27 | G2 rule 1 / route A: coordinator releases a bound worker (`release-worker`) | `issue-pipeline-guard-g2.md:22`, `:45-51` | 0 hits; package deleted; guard comment `:496-497` says retired; only a person's typed `/sc:implement` or `/task` line releases (`GUARD:347-359`) | REMOVED | REMOVED | Decision: `CHANGELOG.md:17` records the removal; guard comment `GUARD:496-497` |
| D-28 | FU-1 runbook commands | `issue-pipeline-fu1.md:64` | Command group absent | DEFECT CANDIDATE (doc names removed commands) | REMOVED (the commands) | Runbook text not updated |
| D-29 | L2 and identity cover more than the tested local Bash surface | `sc-issue-launch-level-hook.md:536-557` | Identity `hook()` returns 0 for non-Bash tools (`launch-job-identity.sh:442-444`) | DEFECT CANDIDATE (declared limits) | BUILT-ON (with limits) | Decision: design `:534` "Limits (OD-1)" |
| D-30 | Capture sheet records the real watcher launch | `SET:616-619` | Lacks `--pipeline none`; watcher sends it (`P/launch.py:92`) | DEFECT CANDIDATE (doc, low) | BUILT-ON | No decision found |
| D-31 | "Grant row": per-issue owner record gating each issue write and live test | `WCT:57` (one mention, undefined); `issue-pipeline-fu1.md:24`, `:26` | No file, verb, path or schema in the snapshot; the removed contract text also used the phrase twice (old `WCT` l.57 and l.300 @01e7a9e23^) | RETIRED | REMOVED (the flow); phrase still in live text | No decision found in the files this reference cites |

### 14.3 Future Considerations

| Item | Deferred Because | Revisit When |
|---|---|---|
| FU-1 live test, then enable the watcher | Gate before `enabled: true` (`DES:33`) | Owner runs the live test and writes the record |
| FU-2 cron entry | Gated behind FU-1 and the shadow run (`DES:861`; `SET:588`, `:676`) | After FU-1 |
| FU-8 auto-retry, FU-10 SLO review, FU-11 pruning, FU-4/5/6/9/12 | "None of these is built by this work" (`DES:856-871`; `SET:669-686`) | FU-8 after FU-1 confirms the argv; FU-10 "after 7 days live"; FU-11 "when the store is above 1 MiB" |
| Binding coordinator-started workers (D-18) | No decision found in the files this reference cites (D-18); the guard design says it does not govern such a worker (`docs/designs/sc-issue-launch-level-hook.md:23`) | No revisit trigger found in the files read (Q-11) |
| The OB-H gate as code (D-21) | No decision found that leaves the gate prose-only (D-21); the one related owner decision (OD-3) keeps the IR-7 refusal off (`IR7_REFUSE = False`, `OW:818-822`) until the #442 observations pass | After the #442 observations pass, for the IR-7 refusal (`OW:822`); none recorded for the OB-H gate as code |

#### 14.3.1 Evidence limits and open questions [UNVERIFIED]

| ID | Question or limit | Why it cannot be resolved from files |
|---|---|---|
| U-1 | PRs #447, #448 ("merged, never run live", `DES:3`) and #425, #394, #441, #442 | A snapshot has no history, PR data or runtime state; `enabled` ships false and no schedule is installed ARE [CODE-VERIFIED] |
| U-2 | Real `gh` replies and error strings (`GH_ERROR_SIGNS` `P/github.py:267-278`, `EDITS_QUERY`/`PROJECT_ITEMS_QUERY` `:71-72`) and the Orca launch reply (`OPERATION_ID_PATHS` `P/launch.py:39-45`, `OP_UNKNOWN_TEXT` `:47`) | All 19 fixtures are `_assumed_shape`; the shapes are `_assumed_shape` in tests and `[UNVERIFIED]`/`[PROPOSAL, UNVERIFIED]` in source; no live-test record |
| U-3 | Whether `enabled` is true in the owner's real config; whether any Coder cron, dispatcher, coordinator, external scheduler or person runs `issue-watch once` | No config or scheduler artefact in the snapshot; "dispatcher", `COORD-`, "zero-setup watcher": not found in snapshot (the `grep COORD-` over the snapshot excluding `.git` and `.dev` has 0 matches) |
| U-4 | OB-H1 item 1, OB-H2, OB-H3, OB-CTX (12 skipped tests) | Never run; design `:625` "Pending, none run" |
| U-5 | Orca CLI flags valid in the installed Orca; tier model order; Claude Code model resolution and the proxy's HTTP 400 text; `skills list --json` side-effect free; interactive mode of the launched session; six-field cron; runbook shell commands | External behaviour; no real `orca` run; tests use a fake `orca` (`tests/skills/test_issue_orca_worktree.py:1-6`) |
| U-6 | Who calls `orca_worktree.py pending`; how a coordinator learns a worker's session id; whether `brief.build` had any caller besides tests | No production caller found; only `git show` of named paths was allowed for the removed tree |
| U-7 | FU-1 recorded lines a to k (`docs/designs/issue-pipeline-fu1.md:108-119`); L2 cost "about 100 ms" (`sc-issue-launch-level-hook.md:617-623`); shim screen text visible "1-2 s" (`OW:793-794`) | Live or timing results written in text; nothing can re-run them |
| U-8 | "739 tests" for `tests/skills/test_worker_contract.py` (architecture reference `:208`); contract installed by `install_core.py:27` and not `@`-imported; location of the Orca `orchestration` skill; formats of `dispatch.json` and the approvers file as read by the removed `stage-status` | The file has 59 `def test_`; other items are outside the files read; no `orchestration*` path under `src/` |
| U-9 | Issue #384, #315 and review-panel PN1 decisions cited by `tests/skills/test_model_alias_policy.py:1`, `:35-37`, `:42`; whether two other docs pin T3 to tier3 | Issues and docs not read |
| U-10 | Owner-policy questions: stuck-entry cost (Q-02); unseen edit window (Q-03); `LaunchOutcome.detail` (Q-04); `launch_login` (Q-05); orphan tmp (Q-06); retry argv uses bare `orca-ide` (Q-07, `P/cycle.py:1262-1267`); `status` shows `disabled since: no` for a dangling `DISABLED` (Q-08); `reset --rate-limit --forfeit-guarantee` silently ignored (Q-09, `P/cli.py:309-313`); `degraded` session blocks every Bash call via identity (Q-18); claim does not refuse without `ccsession-orca` (Q-19); two meanings of "shim" (Q-20); `session-start.sh` uses bare `python3 -c` (Q-21, `:20-21`) | No file states the intent |
| U-11 | Evidence limits: tests were read by name and selected bodies, not run; counts are `grep` counts that do not expand parametrisation; large parts of some files were not read; a negative grep means only "no hit for these terms". The guard was run once in a sandbox HOME on 44 payloads (all matched the code reading); identity, L2, install and claim paths were not executed | Read-only research (Q-22 to Q-24) |

#### 14.3.2 Architectural risks (evidenced by the research only)

| Risk | Evidence |
|---|---|
| Enforcement is bound only by claim launches; the watcher launch and coordinator-started workers are ungoverned | `GUARD:391`; D-18; research 05 "Not defects but worth stating" |
| Several controls are prose run by the model (default level, ship gate, STOP rules, hand-off) | D-16, D-20, D-21; `refs/claim.md:81` |
| Guard misses the real Orca binary name | D-25 (observed exit 0) |
| Every outward reply shape is assumed; failure reasons are unverified | U-2; 19 fixtures |
| Unbounded or unread state: no `audit.jsonl` reader, no store pruning, orphan temp files, write-only fields | D-02, D-11, D-13, D-14 |
| Design docs still instruct removed commands and no test scans `docs/designs/` | 14.1.2 (KW-3, KW-4, X-9); `tests/skills/test_model_alias_policy.py:50` |

---

## Appendix B: Removed on 2026-11-20

Everything in this appendix is read from commit 01e7a9e23^ (the parent of the removal commit) with read-only `git show`. These files do not exist at 61ac2c2e6. Every line citation is labelled @01e7a9e23^. The removal commit is 01e7a9e23 (PR 682), committed 2026-11-19 18:02 -0600, which is 2026-11-20 00:02 UTC. Its message says: "Nothing ran this code: the issue watcher has enabled: false and never ran live. issue_watch is unchanged." Status word for every piece below: REMOVED.

### B.1 What was removed

Directory `src/superclaude/cli/issue_pipeline/` @01e7a9e23^ (10 files, 1,597 lines):

| File | Lines @01e7a9e23^ | Purpose |
|---|---|---|
| `__init__.py` | 5 | Docstring only: the approval core for a coordinator-started plan-writing worker; imports from `issue_watch`, never the reverse (boundary pinned by `tests/issue_watch/test_module_boundaries.py`) |
| `approval_line.py` | 62 | The only two accepted approval texts and the check against a recomputed plan hash |
| `approval_record.py` | 416 | Approval record and adoption record store (local JSON rows, flock) |
| `brief.py` | 74 | Builds the fixed worker brief from a template and a validated issue number |
| `cli.py` | 395 | Click group `issue-pipeline` with 10 verbs |
| `plan_hash.py` | 90 | One SHA-256 over a named list of plan files |
| `reads.py` | 161 | Read-only `gh` projections of comments, events, edits |
| `release.py` | 66 | Writes the `.ok` file that releases a guard-bound worker |
| `stage_predicates.py` | 301 | Pure functions that decide plan-reply, label and comment approval state |
| `templates/worker-brief.txt` | 27 | Brief template with head, marker and three complexity rows |

The same commit also changed: `CHANGELOG.md` (+4); `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` (one line, `:268`); `docs/user-guide/cli-groups.md` (10 lines); `src/superclaude/cli/main.py` (-4: the import at old `:581` and `main.add_command(issue_pipeline_group, name="issue-pipeline")` at old `:583`); `WORKER-CONTRACT.md` (+1/-12, 350 to 339 lines); `launch-level-guard.sh` and its plugin copy (5 lines removed, 2 added each); the removed tests (B.8).

### B.2 The CLI verbs

Group `issue_pipeline_group` (`click.group(name="issue-pipeline")`, `cli.py:56-58` @01e7a9e23^). Exit codes: `_EXIT_REFUSED = 1`, `_EXIT_CONFIG = 2`, `_EXIT_LOCK_HELD = 75` (`cli.py:29-32`). No verb printed file or GitHub text.

| # | Verb (line) | Arguments and options | Output and exit | Read or wrote |
|---|---|---|---|---|
| 1 | `plan-hash` (`:61`) | `REPORT_DIR`, `NAMES...` | `file: <name>` per sorted name, then `plan-sha256: <hex>`; `refused:<reason>` exit 1 | read plan files |
| 2 | `check-approval` (`:76`) | `REPORT_DIR`, `NAMES...`, `--line` (required), `--issue N` | `ok` exit 0, or the refusal word, exit 1 | read plan files |
| 3 | `init` (`:96`) | `APPROVALS_DIR` | `ok`; `refused:<reason>` exit 1 | wrote dir 0700 and `lock` 0600 |
| 4 | `adopt-create` (`:108`) | + `--issue`, `--stage` (default `plan`) | JSON `created`; `refused:already-started` or `refused:uncertain-launch` exit 1; `lock-held, retry` exit 75 | wrote adoption row |
| 5 | `adopt-mark` (`:117`) | + `--state started\|uncertain`, `--dispatch-id` | JSON `marked` | wrote adoption row |
| 6 | `record-create` (`:134`) | + `--plan-hash`, `--channel label\|comment\|reply`, `--evidence-id`, `--actor` | JSON `created` or `exists` | wrote approval row |
| 7 | `record-show` (`:161`) | + `--plan-hash` | JSON row | read |
| 8 | `record-mark` (`:179`) | + `--plan-hash`, `--state instructed\|acked\|revoked` | JSON `marked` | wrote approval row |
| 9 | `release-worker` (`:200`) | `SESSION_ID`, `--store` (default `~/.claude/state/launch-level`) | `released` or `already-released`; `refused:<reason>` exit 1 | wrote `<store>/sessions/<session_id>.ok` |
| 10 | `stage-status` (`:335`) | `ISSUE`, `--json`, `--config` (default `~/.config/superclaude/issue-watch.json`), `--approvals-dir`, `--plan-dir`, `--plan-file` | one sorted JSON object; config error exit 2; read failure exit 1 | read `gh`, rows, plan files |

### B.3 Approval record format and plan hash

| Item | Rule @01e7a9e23^ |
|---|---|
| Accepted texts | `approved` (comment channel only) or `approved ap-<issue>-plan-<12 hex> plan-sha256=<64 hex>`; whole-text match, no trimming (`approval_line.py:18-21`, `:33-40`) |
| Check results | `ok`, `refused:bare`, `refused:mismatch`, `refused:malformed`, or `refused:<plan-hash reason>` (`:43-62`) |
| Plan hash | SHA-256 over sorted names; per name: `len(name)` 8 bytes big-endian, name, `len(data)` 8 bytes big-endian, bytes; 11 refusal words `no-names`, `bad-dir`, `absolute-name`, `dotdot-name`, `bad-name`, `duplicate-name`, `symlink`, `missing`, `outside-dir`, `not-a-file`, `unreadable` (`plan_hash.py:24-36`, `:77-90`) |
| Store | Caller-named directory (no default in code), mode 0700, `lock` 0600, symlink refused (`approval_record.py:81-98`) |
| Adoption row | `adoption-<issue>-<stage>.json`; keys `kind`, `issue`, `stage`, `state`, `dispatch_id`, `created_at`, `updated_at`; states `reserved`, `started`, `uncertain` (`:126-139`, `:44`) |
| Approval row | `approval-<issue>-<stage>-<64 hex>.json`; keys `kind`, `record_id`, `issue`, `stage`, `plan_hash`, `state`, `evidence`, `created_at`, `updated_at`; states `recorded`, `instructed`, `acked`, `revoked`; evidence keys `channel`, `id`, `actor`, `time` (`:132-153`) |
| Writes | JSON via `swarm.atomic.write_prepared_bytes`, chmod 0600, directory fsync; every mutation holds the `FileStore` flock; a second caller gets `lock-held` (exit 75) (`:108-123`, `:225-229`) |
| Plan reply marker | `<!-- sc:stage:plan id=<record id> plan=<64 hex> -->` (`reads.py:42`) |

### B.4 The release-worker action and GitHub writes

- `release.release(session_id, store=None)` created the zero-length file `<store>/sessions/<session_id>.ok` with `O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`, mode 0600 (`release.py:57-62`). Refusals: `bad-session-id`, `no-store`, `not-bound`, `not-worktree-level`; a second call gave `already-released`. The guard already read that file: a worktree-level session with it became level `WA`, whose IMPL and TURN classes are allowed (snapshot `GUARD:270-272`, `:786`).
- Who could run it: the coordinator (docstring `release.py:3-4`: "The coordinator calls this after it has recorded a plan approval"); a bound worker could not (guard rule 1, B.6). The old contract text never named the verb or `.ok`.
- GitHub writes: none by the package. Its only `gh` lines were reads: `gh api user --include`; `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N> --jq <REREAD_JQ>`; `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N>/events -F per_page=100 -F page=<P> --jq <EVENTS_JQ>`; `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N>/comments -F per_page=100 -F page=<P> --jq <COMMENTS_JQ>`; `gh api graphql -f query=<EDITS_QUERY> -F number=<N>` (a POST whose query only reads) (argv builders in `P/github.py:175-262`, used by `reads.py`). `test_the_command_only_reads_and_never_calls_orca` (`tests/issue_pipeline/test_stage_status.py:451` @01e7a9e23^) pinned that `stage-status` calls no `orca`.
- The contract text told the coordinator model to write to GitHub without a command line: "Post the plan reply with the hash and file list and mention the assignee" and "mirror the label and Status" (old `WCT:298`); "post an issue write without that issue's grant row" was forbidden (old `WCT:300`).

### B.5 WC-17 and "Issue pipeline duties"

Old `WORKER-CONTRACT.md` (350 lines) @01e7a9e23^.

**WC-17**, "Plan approval is the reply to the worker's own ask" (old `:59`, section 3). Trigger: a brief carrying the `Plan approval:` line. Steps: (1) `superclaude issue-pipeline plan-hash <report-dir> <names>`; (2) `ask` once with path, file list and hash; (3) wait (resume the same message on timeout); (4) `superclaude issue-pipeline check-approval <report-dir> <names> --line <reply>`; (5) `ack <message_id> applied|refused`; (6) continue only on `applied`. A bare `approved`, or any text that is not the reply to its own ask, is never approval; a mismatch is refused and reported in `worker_done`. The sentence "`ask` and `send` carry no `--to`" was kept in the snapshot as `WCT:66`.

**"### Issue pipeline duties"** (old `:291-300`, section 4). Scope: an issue the watcher claimed with `/sc:issue --claim <N> --pipeline none` that this coordinator now owns.

| # | Duty (old line) | Content |
|---|---|---|
| 1 | Adopt (`:295`) | Read only the watcher's `claimed` entry in `dispatch.json` and `.dev/issues/<N>/issue-summary.md`, `next-steps.md` |
| 2 | Reserve before starting (`:296`) | `adopt-create` before `worker-start`; mark `started` with the Dispatch id or `uncertain`; never start again for an `uncertain` row |
| 3 | Worktree, then worker (`:297`) | `orca_worktree.py worktree ...` then `worker-start --worktree path:<path> --agent claude --spec <brief>` |
| 4 | Plan approval (`:298`) | Post the plan reply; read GitHub through `stage-status`; `record-create` only when the worker's `ask` carries the hash; reply `approved <record-id> plan-sha256=<hash>`; mirror label and Status; mark `instructed`, then `acked` |
| 5 | No exception (`:299`) | Route B adds no exception to "never answer a person prompt"; nothing is typed into a worker terminal |
| 6 | Never (`:300`) | Tell a worker to pass its plan boundary without an approval row; act on a Status move alone; relaunch a dead worker alone; "post an issue write without that issue's grant row" |

Facts about names: the duties named `adopt-create`, `adopt-mark`, `stage-status`, `record-create`, `record-mark` (and WC-17 named `plan-hash`, `check-approval`), never `release-worker` or `brief`. "COORD-" was absent from the old contract (0 hits). "grant row" appeared twice (old `:57` and `:300`) and was defined nowhere. In the snapshot `WCT:57` contains "grant row" once, undefined; "dispatcher", `COORD-` and "zero-setup watcher": not found in snapshot.

### B.6 The guard's G2 rule 1 TAMPER case

Old `launch-level-guard.sh` (811 lines) @01e7a9e23^, comment at `:441-444` and the case at `:444`: any Bash text (normalised, `:428`) containing `release-worker`, `release_worker`, `issue-pipeline` followed later by `adopt-` or `record-`, `issue_pipeline` followed later by `release`, or `issue_pipeline` followed later by `approval_record` added the class TAMPER. The decision table (snapshot `GUARD:799`, unchanged) denies TAMPER at levels W, WA, F and FS with `LL-TAMPER` (exit 2). `plan-hash` and `check-approval` stayed allowed. After the removal: G2 rule 2 (`orchestration send`/`ask` with no `--to`, `GUARD:496-537`) and the generic store TAMPER (`GUARD:761`, a forged `.ok` is still `LL-TAMPER`, `tests/hooks/test_launch_level_guard_worker.py:262-270`) remain; the only way to create `.ok` is a person's typed first prompt line `/sc:implement` or `/task` at level W (`GUARD:347-359`). One comment is left at `GUARD:496`.

### B.7 Data flow and safety properties

```
issue-watch once (enabled:false) -> claim: /sc:issue --claim N --pipeline none  [comments, issue-summary.md, next-steps.md, no agent]
        |
        v  (LLM text, coordinator, old WCT:295)  read dispatch.json (read-only) + .dev/issues/N/*
 init APPROVALS_DIR -> adopt-create (row `reserved`, flock) -> orca_worktree.py worktree -> worker-start --spec <brief>
        |                                                           (brief.build: not called by any verb)
        v                         adopt-mark started|uncertain
 worker writes plan -> plan-hash -> ask(path, files, hash)
        |
        v  coordinator posts plan reply with marker <!-- sc:stage:plan id=.. plan=.. --> (GitHub write, LLM text, no command line)
 approver: label or `approved` comment  -> stage-status N (read-only gh) says approved
        |
        v  record-create (row `recorded`) -> reply "approved <id> plan-sha256=<hash>" -> record-mark instructed
 worker: check-approval ok -> ack applied -> record-mark acked
        |
        v  release-worker <sid> -> sessions/<sid>.ok  (level WA)   [which text told a coordinator to call it: UNVERIFIED]
```

Safety properties the package enforced (old code places): exact-text approval (`approval_line.py:18-21`, `:33-40`); plan binding by content, refusing links, `..`, absolute and duplicate names (`plan_hash.py:39-90`; the approval key includes the hash, `approval_record.py:132-134`); no self-approval by a bare word (`approval_line.py:50-51`); approver identity, order and edit detection with fail-closed reads (`stage_predicates.py:145-244`, `reads.py:138-139`); revocation (`stage_predicates.py:171-177`, `approval_record.py:389-416`); at-most-once worker start by write-ahead row (`approval_record.py:235-265`); no GitHub text stored or printed (`reads.py:1-11`; every stored value pattern-checked); a worker could not forge release or rows (guard rule 1); a fixed brief with no issue text (`brief.py:5-8`).

### B.8 Removed tests and test edits

116 tests in 10 files under `tests/issue_pipeline/` (2,391 lines; counts are `def test_` definitions) plus `tests/cli/test_issue_pipeline_registered.py` (15 lines, 1 test):

| File @01e7a9e23^ | Lines | Tests | What it pinned |
|---|---|---|---|
| `test_approval_concurrency.py` | 78 | 2 | one winner for concurrent `record_create` and `adopt_create` |
| `test_approval_crash.py` | 88 | 3 | killed `record_create` leaves `recorded`; kill between `worker-start` and `adopt-mark` blocks a second start; duplicate approval plus crash gives at most one instruction |
| `test_approval_line.py` | 135 | 9 | two accepted texts; variants rejected; mismatch; bare refused; CLI exit codes |
| `test_approval_record.py` | 424 | 21 | store creation, forward-only moves, revoke and reopen, adoption paths, fixed patterns, corrupt rows, exit 75 on a held lock |
| `test_brief.py` | 224 | 12 | golden briefs; only template characters; bug type refused; no row runs implement, commit, push or submit; one marker line |
| `test_plan_hash.py` | 116 | 10 | ordered list and hash; one byte, rename or added file changes it; refusals; symlink refused |
| `test_reads.py` | 295 | 10 | typed projection; approval forms; hostile body never reaches output; page and call caps; failure gives a closed reason |
| `test_release.py` | 89 | 7 | `.ok` is one empty private file; second release no-op; refusals |
| `test_stage_predicates.py` | 466 | 29 | label and comment channels, ordering, edits, revocation, `status_seen` never approves alone |
| `test_stage_status.py` | 476 | 13 | closed keys through an injected runner; reads only, never calls `orca` |
| `__init__.py` and `fixtures/recorded/` (issue 452 responses) | 0 and fixtures | n/a | the recorded issue had no label event, plan reply or approval comment, so every approval case ran on hand-built evidence |
| `tests/cli/test_issue_pipeline_registered.py` | 15 | 1 | `issue-pipeline` and `issue-watch` in `main.commands`; `--help` prints `plan-hash` |

Edits to surviving test files:

| File | Before @01e7a9e23^ | After the commit | Change |
|---|---|---|---|
| `tests/skills/test_worker_contract.py` | 3,181 lines, 61 tests | 3,135 lines (+8/-54); 59 tests | 3 tests dropped (`test_adoption_names_only_sources_that_exist_after_pipeline_none`, `test_adoption_check_fails_when_worktree_json_is_named`, `test_issue_pipeline_duties_allow_no_typing_into_a_worker_prompt`) and `RULE_PHRASES` entries `issue-pipeline-duties` and `wc17-plan-approval` removed; 1 added (`test_the_no_to_rule_sits_in_the_worker_session_duties`); at 61ac2c2e6 the file has 3,220 lines |
| `tests/hooks/test_launch_level_guard_worker.py` | 330 lines, 13 tests | 300 lines (-30 net); 11 tests | `test_a_bound_worker_cannot_run_the_coordinator_side_pipeline_verbs` (old `:270-287`, 6 commands expecting `LL-TAMPER`) and `test_a_bound_worker_may_still_run_plan_hash_and_check_approval` (old `:290-299`) dropped; the chain test now types `/sc:implement plan.md` (current `:255-257`) instead of calling `release.release(SID, store)` (old `:254`); the nonce test no longer imports `brief` |

Research 06 B13 states "-56 net" for the guard worker test; the file lengths (330 to 300) and the commit figures give -30, which is the stronger evidence. The record of research 06 is used for all other figures.

### B.9 What replaced each removed duty

| Removed duty | Replacement at 61ac2c2e6 | 14.2 row |
|---|---|---|
| Approval record, plan-hash binding, approver identity, edit detection, revocation, WC-17 worker wait | no replacement found in snapshot | D-17 |
| Write-ahead adoption row (at-most-once worker start) | no replacement found in snapshot; the watcher's own `dispatch.json` covers the claim launch only | D-16, D-17 |
| Coordinator release of a bound worker (`release-worker`) | a person's typed first line `/sc:implement` or `/task` (`GUARD:347-359`); no coordinator verb | D-27 |
| Fixed worker brief with launch marker (`brief.build`) | no replacement found in snapshot; `pending` exists with no production caller | D-18 |
| Adopt, worktree and `worker-start` sequence ("Issue pipeline duties") | no replacement found in snapshot; `WCT` has general rules WC-2..WC-16 only | D-16 |
| Guard rule 1 (TAMPER on coordinator-side verbs) | generic store TAMPER (`GUARD:761`) and G2 rule 2 remain | D-27 |
| "Grant row" gating each issue write | no replacement found in snapshot; the phrase survives at `WCT:57` | D-31 |

