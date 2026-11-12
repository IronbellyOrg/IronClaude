# Research 03: Hook guards (recognition, enforcement ceilings, identity)

**Topic:** Orca worktree agent guard, launch-level guard, launch-job identity helper, hook registration and installer
**Investigation type:** Integration mapper (source-traced; checkout source only)
**Scope:** `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh`, `launch-level-guard.sh`, `launch-job-identity.sh`, `src/superclaude/hooks/hooks.json`, `src/superclaude/cli/install_hooks.py`, `tests/hooks/`
**Date:** 2026-11-11
**Status:** Complete (see the final `Status: Complete` line)

Evidence class legend: all line citations are checkout source at the time of reading (repo root `/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test`). Installed copies under `~/.claude/hooks/`, effective settings and live hook ordering are UNVERIFIED (not inspected). Subordinate/sub-orchestrator mode is deferred and not implemented.

Verification methods used: direct Read of every source file below; fixed-input probes of the guard scripts run from a private `/tmp` directory (no repository writes, no pytest run, no live Orca). Probe results are cited as "probe Pnn" or "probe Gnn". Prefix definitions (added in fix cycle 1): `Pnn` = a fixed-input probe of `require-orca-worktree-agent.sh` (P01-P27) or of its scanner text (P28); `Gnn` = a fixed-input probe of `launch-level-guard.sh` run with a temporary HOME holding a session record. The catalogue of every ID, with the input as recorded and how far each can be reproduced, is section G at the end of this file ("Probe catalogue"). Tests were not run in this research file; research/06 ran the two files named there (744 passed in total); the `tests/hooks/` results are unrun.

---

## A. `require-orca-worktree-agent.sh` (PreToolUse Bash gate)

Source: `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh` (358 lines, working tree with uncommitted message change; see B.4).

### A.1 What it enforces and what it does not

- Purpose: block a Bash tool call that runs `orca worktree create` without `--agent` (`:2-5`). The header states plainly that "Only the --agent requirement is enforced here; 'no worktree for your own use' and 'the creator owns the agent' are instruction text" (`:7-8`). [CODE-VERIFIED] The script contains no role, session, worker or environment predicate: a grep of the file for `WORKER|ORCA_|CLAUDE_|role|coordinator|worker|supervis` hits only `:313` (sudo `--role` long-option table), `:355` and `:356` (block message lines); re-run in fix cycle 1: exactly these three lines (the earlier list also named `:60`, which has no hit). The hook therefore cannot distinguish a coordinator from a worker or a human-opened session; the sentence "workers cannot create worktrees or dispatch workers" in the block message (`:355`) is instruction text, not a predicate. ENFORCEMENT CEILING: the only machine-enforced rule is "a lexically recognised `orca worktree create` carries `--agent`".
- Registration: `src/superclaude/hooks/hooks.json:105-114`, event `PreToolUse`, matcher `"Bash"`, timeout 3 s. The script's comment says PreToolUse hooks also fire inside subagents (`:5-6`). That subagent claim is [UNVERIFIED] here (a Claude Code runtime behaviour, not exercised in this investigation).
- Decision contract (`:10-15`): allow = exit 0; block = one message on stderr + exit 2; never exit 1. The hook "itself runs no Python" (`:15`).

### A.2 Fail-open cases (all exit 0)

Each is cited to the code that implements it.

| Case | Code | Probe |
|---|---|---|
| `jq` missing | `:65-68` (message "allowing the command (fail open)") | not probed (would need PATH surgery) |
| `awk` missing | `:69-72` | not probed |
| empty stdin | `:342-343` `[ -n "$INPUT" ] \|\| exit 0` | P27 OK |
| input not valid JSON | jq fails inside the pipeline at `:345-347`; `WORD` ends empty; `[ "$WORD" = "orca" ] \|\| exit 0` at `:349` | P26 OK |
| tool is not `Bash` | jq program at `:346`: `if .tool_name == "Bash" then (...) else "" end`, so a Monitor call is never scanned | P15 OK (Monitor + bare create allowed) |
| missing/empty/non-string `tool_input.command` | `:346` `(.tool_input.command // "" \| strings)` | not probed (but tests `bash-no-command` and `bash-empty-command` cover the first two inputs: `tests/hooks/test_require_orca_worktree_agent.py:150-151`) |
| any scanner (awk) error | `:347` `\|\| WORD=""` | not probed |

The block decision requires the scanner to print exactly `orca` (`:349`). Anything else, including a scanner crash, is allow.

### A.3 The block predicate (exact)

Implemented in the stateful awk scanner embedded at `:74-340` (single-quoted heredoc assigned to `SCANNER`; the shell pipes jq output to `LC_ALL=C awk "$SCANNER"` at `:345-347`, via stdin, never `awk -v`, per header `:17-20`).

1. A simple command's command word is found by `endword()` (`:110-146`): leading `NAME=value` assignments are skipped (`:119`), wrappers `env sudo nice nohup time exec timeout command coproc` are skipped together with known options (`iswrap` `:82-85`; option tables `:306-315`), shell keywords are skipped when unquoted (`iskw` `:77-81`, `:133-139`), then `b = base(w)` (basename, `:86`, `:141`).
2. The command is tracked as an `orca` candidate when `b == "orca"` **or** `b ~ /^\$/` (`:145`). So a path ending in `/orca` matches, and a command word that starts with `$` (variable, `${...}`, `$(...)`) is treated as a possible orca (header `:47-51`; probe P08 `$ORCA worktree create` blocked, P19 `$(printf orca) worktree create` blocked, P17 `/usr/local/bin/orca ...` blocked).
3. Every later word of that same simple command goes to `track()` (`:94-98`, called from `:117`): `--agent` or a word starting `--agent=` sets `hasagent`; `--help` or `-h` sets `hashelp`; any other word not starting with `-` is counted as a non-option argument, the first two kept as `a1`, `a2`.
4. At each command separator (`;` `&` `&&` `||` `|` newline, `)` close of a substitution) `sep()`/`fin()` run (`:99-103`, `:108`, `:201-213`, `:241`). `fin()` prints `orca` and exits the scanner iff `a1 == "worktree" && a2 == "create" && !hasagent && !hashelp` (`:102`).
5. A flag in one command never satisfies another (header `:30-33`): probe P14 (`orca worktree create --name x; orca worktree create --name y --agent claude`) is blocked.
6. Substitutions (`$(...)`, backticks, process substitution, subshells) push a fresh command context, so `echo $(orca worktree create --name x)` is blocked (probe P21). The matching tokenizer features (quotes, `$'...'`, comments, continuation, arithmetic, heredocs, here-strings, case patterns, `[[ ]]`, function definitions, redirections) are listed in the header `:17-30`.

Observed recognised-and-blocked forms (all exit 2): bare `orca worktree create --name x` (P01), after `cd ... &&` (P10), `sudo orca ...` (P13), `timeout 5 nohup orca ...` (P24), `/usr/local/bin/orca ...` (P17), `orca --json worktree create ...` (P22, dash-options skipped), `--agents claude` (P20: only exact `--agent` or `--agent=` counts).
Observed allowed forms (exit 0): `--agent claude` (P02), `--agent=claude` (P03), `orca worktree list` (P04), `... create --help` (P11), `echo "orca worktree create"` (P06).

### A.4 Documented enforcement ceilings (creates that are NOT blocked)

The script lists these in its header (`:39-61`). Each is cross-checked against the scanner code and, where marked, a probe.

| Ceiling (header line) | Status |
|---|---|
| string arguments to another interpreter: `bash -c`, `sh -c`, `eval`, `env -S`, `ssh host '...'` (`:40-41`) | [CODE-VERIFIED] quoted content is accumulated as word characters (`qchar` `:272-290`), never tokenized as a command; probes P05 (`bash -c`), P16 (`env -S`), P18 (`eval`) allowed |
| commands started by another program: `xargs orca`, `find -exec orca` (`:42`) | [CODE-VERIFIED] `xargs` is not in the wrapper list (`:82-85`), so the command word is `xargs`; probe P12 allowed |
| heredoc body piped/redirected into a shell (`cat <<'EOF' \| bash`) (`:43-44`) | [CODE-VERIFIED] heredoc bodies are skipped except for `$(`/backtick substitutions (`hdocchar` `:297-304`); probe P23 allowed |
| quoted value equal to `--agent` counts as the flag (`:45-46`) | [CODE-VERIFIED] `track()` compares the already-unquoted word (`:95`); probe P09 (`--prompt "--agent"`) allowed |
| command word assembled from pieces (`o$(printf rc)a ...`) (`:47`) | [CODE-VERIFIED] probe P25 allowed. Counter-case: a command word that *starts* with `$` is blocked (`:145`, probes P08/P19) |
| nested backticks written with `\` escapes (`:52`) | [UNVERIFIED] by probe; scanner handles backtick open/close at `:176-179` without an escape level |
| global orca options that take a separate value before `worktree` (`:53-54`) | [CODE-VERIFIED] the value is counted as `a1` (`:97`), so `orca --repo foo worktree create` has `a1=foo`, `a2=worktree`; probe P07 allowed |
| wrapper options with a value that are not in the tables (`:55`) | [CODE-VERIFIED] tables are `:306-315` only; an unknown option value would be read as the command word |
| shell commands run by tools other than Bash, e.g. Monitor (`:56`) | [CODE-VERIFIED] `:346` filters on `tool_name == "Bash"`; probe P15 |
| hosts without jq or awk (`:57`) | [CODE-VERIFIED] `:65-72` |
| `claude --bare` sessions, which skip settings hooks (`:58`) | [UNVERIFIED] Claude Code runtime behaviour, not exercised; stated by the script header only |
| humans and other agent tools that create worktrees themselves (`:59`) | [CODE-VERIFIED] by construction: the hook only sees Bash tool calls |
| scripts that call Orca as a subprocess; `orca_worktree.py` runs Orca itself, not through the Bash tool (`:60-61`) | [CODE-VERIFIED] by construction (Bash tool only); `orca_worktree.py` call sites belong to research file 04 |

False-positive direction (blocks something that is not a real create): a `$`-led command word with `worktree create` as its first two non-option arguments and no `--agent` is blocked even if it is not orca (`:145`, P08). Not a safety defect; recorded for completeness.

### A.5 Scanner provenance

The header says the tokenizer is "the block-bare-python.sh tokenizer ... copied here because installed hooks are standalone files" (`:21-25`). Comparison probe P28: the scanner block of this file is 267 lines vs 254 lines in `block-bare-python.sh`, with 25 differing lines. [CODE-CONTRADICTED] as a literal "copy": it is a derivative with extra per-command collection (`track`, `fin`, `isorca`), not a byte copy. Semantically consistent with the header's "Unlike block-bare-python.sh it does not stop at the command word" (`:26-28`).

### A.6 Message emitted on block

`:351-357`: states the rule, the exact form `orca worktree create --name <name> --agent claude --prompt "<task>"`, "The eligible session that creates the worktree owns that agent", "A supervised coordinator is person-opened; workers cannot create worktrees or dispatch workers", and "Supervised workers use `orca orchestration worker-start`". All role sentences are advisory text shown to the model after a block. Exit 2 at `:358`.

## B. Registration (`hooks.json`) and installer (`install_hooks.py`)

### B.1 What `src/superclaude/hooks/hooks.json` (192 lines) registers for the guards

[CODE-VERIFIED] all entries use `"type": "command"` with `~/.claude/hooks/<name>.sh` (the installed flat path, not `hooks/scripts/`).

| Event | Matcher | Command | Timeout | Source lines |
|---|---|---|---|---|
| UserPromptSubmit | none (fires for every prompt) | `launch-level-guard.sh` | 5 | `hooks.json:63-71` |
| PreToolUse (index 1) | `Bash` | `block-bare-python.sh` | 3 | `:95-104` |
| PreToolUse (index 2) | `Bash` | `require-orca-worktree-agent.sh` | 3 | `:105-114` |
| PreToolUse (index 3) | `^(Bash\|Skill\|Agent\|Task\|Edit\|Write\|NotebookEdit\|Monitor\|Workflow\|RemoteTrigger\|SendMessage\|Cron[A-Za-z]*\|Schedule[A-Za-z]*)$\|^mcp__.*(merge\|push\|commit\|pull_request\|create_or_update_file\|delete_file\|update_ref\|create_ref\|create_branch)` | `launch-level-guard.sh` | 5 | `:115-124` |
| PreToolUse (index 4) | `Bash` | `launch-job-identity.sh` | 5 | `:125-134` |

(PreToolUse index 0 is `Edit\|Write` -> `freshness-pre-edit.sh`, `:85-94`.)

Facts that bound enforcement:
- No hook in this file is registered on `SubagentStart`/`SubagentStop` for the guards (those events carry only the freshness and pragmatic hooks, `:159-190`). Guards act on PreToolUse and UserPromptSubmit only.
- Three PreToolUse hooks match a Bash call (`require-orca...`, `launch-level-guard`, `launch-job-identity`) plus `block-bare-python`. The registration gives an array order, but `launch-job-identity.sh` states that other hooks' rewrite ordering is "unspecified" (`launch-job-identity.sh:15`) and that live auto-mode rewrites are unverified (`:17-18`, `:481`). [UNVERIFIED] whether Claude Code runs the matching hooks serially or in parallel, and which `updatedInput` wins; not exercised here.
- `launch-level-guard.sh` is not registered on SessionStart; a governed session is established only by its first prompt carrying the launch marker (see C.2).
- The guard's tool coverage matches `orca_worktree.py:811-837` `GOVERNED_TOOLS` (the claim-time preflight uses that list to confirm the registered matcher fires for each tool, `orca_worktree.py:995-1006`). [CODE-VERIFIED]
- No project-level registration: a grep of the project `.claude/settings.json` for `launch-level|require-orca|launch-job` returns 0 hits (probe). So in this repository the guards run only if the user-level `~/.claude/settings.json` registers them (installed by `superclaude install`).

### B.2 Plugin mirror

`plugins/superclaude/hooks/hooks.json` registers the same five guard-related commands with identical matchers and timeouts (probe: PreToolUse indexes 1-4 match; UserPromptSubmit index differs only because the plugin file has fewer earlier entries). The plugin file is not identical to the source `hooks.json` (it lacks SessionEnd, the ccsession SessionStart entry, `pragmatic-subagent.js`, the `async` flag on the Read hook, and has a narrower auggie matcher; 49 differing lines). `plugins/superclaude/hooks/scripts/{require-orca-worktree-agent,launch-level-guard,launch-job-identity}.sh` are byte-identical to the source scripts in this working tree (probe `cmp`). The plugin's installation path is out of scope here (marked "not yet available" in project `CLAUDE.md`).

### B.3 `install_hooks.py` behaviour (611 lines)

- The three scripts are members of `_FRESHNESS_SCRIPTS`: `require-orca-worktree-agent.sh` `install_hooks.py:88`, `launch-job-identity.sh` `:90`, `launch-level-guard.sh` `:93`. `make verify-sync` requires every `hooks/scripts/*.sh` to be in this list (comment `:62-64`).
- Copy: `_copy_scripts` (`:251-290`) copies each listed script flat into `<settings dir>/hooks/` (`:173`, `:264-265`), `shutil.copy2` then `chmod 0o755` (`:283-286`). A missing source is recorded as `failed` (`:275-277`). An existing destination is skipped unless `force` (`:279-281`). [CODE-VERIFIED] consequence: without `--force`, an older installed script is kept silently (reported as "Skipped ... use --force to overwrite", `:202-207`).
- Registration merge: `_merge_settings` (`:298-491`). Ownership is by exact command identity, never matcher alone (`:402-403`); an already-registered managed command is skipped unless `force` (`:417-419`), refreshed in place when `force` (`:421-455`); otherwise it is inserted before the first registration owned by a later source entry so "launch-job-identity.sh stays last" (`:457-471`). [CODE-VERIFIED] consequence: without `--force` a previously installed registration with an outdated matcher is not updated; `orca_worktree.py:925-1015` tells the operator to run `superclaude install --force` for exactly that case (`stale`/`restale` strings `:932-933`).
- Safety: backs up an existing settings file first (`:333-343`, `_backup_path` `:526-529`), refuses to write a malformed or non-object target (`:345-364`), writes atomically (`_atomic_write_json` `:507-523`). Pure stdlib (module docstring `:16`).
- Does NOT: verify that `jq`, `awk` or `uv` exist, verify the script runs, or check `disableAllHooks`. Those are checked only by the sc:issue claim preflight (`orca_worktree.py:935-944`, `:977-982`), and only for the launch-level guard path.
- Callers: `superclaude install` passes `force=force` (`main.py:217`); `superclaude update` passes `force=True` (`main.py:394`); the eval hook adapter passes `force=False` into a per-eval HOME after refusing the real home (`eval/hook_adapter.py:218`, `:230`).

### B.4 Source-vs-host drift observed (host observation, not deployed truth)

Observed 2026-11-11 on this host; evidence class "host observation of one machine", not proof about any other install.

| Item | Observation |
|---|---|
| Working tree state | Branch `ironbelly/design-doc-shim-title-check`, HEAD `5bdb01681`. In-scope files with **uncommitted** changes: `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh` and `tests/hooks/test_require_orca_worktree_agent.py` (`git status`/`git diff HEAD`): the block message changed from "The session that creates the worktree becomes its orchestrator (or a coordinator under another orchestrator) and owns that agent." to the two lines now at `require-orca-worktree-agent.sh:354-355` ("The eligible session that creates the worktree owns that agent." / "A supervised coordinator is person-opened; workers cannot create worktrees or dispatch workers."). The test constant `BLOCK_MESSAGE` was changed to match. Everything in section A therefore describes the working tree; HEAD still carries the old wording. |
| Local ref `origin/master` | `9e2608b03`, 19 commits ahead of HEAD (HEAD is 2 ahead of it). It contains an L2 git pre-push layer that this checkout does not: new `launch-level-pre-push.sh` (208 lines), 8 changed lines in `launch-level-guard.sh` (adds a tamper class `FR-050..FR-052` for `.git/hooks`, `pre-push`, `--no-verify`, `hookspath`), 22 changed lines in `launch-job-identity.sh` (FR-025 `reason`/`record` fields on `unknown`), +3 lines in `install_hooks.py`, 453 insertions and 42 deletions in `orca_worktree.py` (1473 to 1884 lines; `git diff --numstat HEAD origin/master`, re-run in fix cycle 1), and new tests `test_launch_level_pre_push.py`, `test_launch_level_pre_push_records.py`, `test_launch_level_guard_l2_tokens.py`. Commit `5f8a1ea2d` "feat: add tested L2 pre-push protection with refusal activation gated (#441) (#469)" (2026-11-10). The `origin/master` ref was not fetched in this investigation, so it may lag the true remote. |
| Local branch `master` | `80f361804`, HEAD is 33 commits ahead of it; it is an older ref and not the integration target of the `origin/master` comparison. |
| Installed copies in `~/.claude/hooks/` on this host | CORRECTED in fix cycle 1 (the first pass said all three equal `origin/master`): `launch-level-guard.sh` and `launch-job-identity.sh` are byte-identical to the `origin/master` version and DIFFER from HEAD and from this working tree; `require-orca-worktree-agent.sh` is byte-identical to BOTH HEAD and `origin/master` (the L2 change did not touch it) and DIFFERS from this working tree only by the uncommitted message change. The installed `require-orca` therefore carries the old ownership wording (357 lines vs 358). Per-file table of all seven installed files (including `CLAUDE.md`, `WORKER-CONTRACT.md`, `orca_worktree.py`, the ccsession README): research/06 section F6 (read-only `git show <ref>:<path> \| cmp - <installed file>`). |
| Registrations in `~/.claude/settings.json` on this host | UserPromptSubmit `launch-level-guard.sh` (no matcher, timeout 5); PreToolUse `require-orca-worktree-agent.sh` (`Bash`, 3); PreToolUse `launch-level-guard.sh` with the same long matcher as `hooks.json:116` (5); PreToolUse `launch-job-identity.sh` (`Bash`, 5). `disableAllHooks` is unset. `~/.claude/state/launch-level` exists. `jq` 1.7, `mawk`, `uv` present. |

Consequence for the reference: statements about the L2 pre-push layer are true of `origin/master` and of the host-installed `launch-level-guard.sh` and `launch-job-identity.sh` but NOT of this checkout, and the installed set on this host is mixed (research/06 F6); and the "workers cannot create worktrees" message text is true of this working tree but NOT yet of any commit or of the installed hook on this host. The final reference must state which revision it documents. [CODE-CONTRADICTED] `orca_worktree.py:800-805` ("this plan builds no L2 layer ... the claim warns instead") describes this checkout only; `origin/master` has a `launch-level-pre-push.sh` and an `orca_worktree.py` with 453 insertions and 42 deletions (1473 to 1884 lines), which were not read here (outside the assigned file list; research 04 F5 states the same figures and read the header lines of the newer script; `launch-level-pre-push.sh` itself was read by no research file).

## C. `launch-level-guard.sh` (L1 launch-level guard)

Source: `src/superclaude/hooks/scripts/launch-level-guard.sh` (747 lines, identical to HEAD; the host-installed copy is the newer `origin/master` version, see B.4). Normative design: `docs/designs/sc-issue-launch-level-hook.md` (cited by the script at `:3`). Design status line says "built: L1 guard script, its two registrations, installer entry ...; pending: OB-H1 items 1 to 9, OB-H2, OB-H3, OB-CTX and the L2 pre-push layer" (`sc-issue-launch-level-hook.md:6`) and "no governed claim on a real issue until OB-H1 item 1, OB-H2 and OB-H3 pass" (`:10`). [CODE-VERIFIED] the L1 script and both registrations exist (B.1); the L2 pre-push layer is absent from this checkout (B.4).

Scope relation to supervised orchestration: this guard is the `/sc:issue --claim` launch-level control, a separate mechanism from supervised worker identity (`orca orchestration worker-start`). Within the assigned files there is no code path that binds a supervised worker or coordinator to a level. The only producer of the launch marker `[sc-launch:v1:<nonce>]` in checkout source is `orca_worktree.py:1354` (grep of non-test, non-`.dev` files finds only that script, this guard, the plugin mirror and two design docs). [CODE-VERIFIED]

### C.1 Which sessions are governed

- Governed = a valid top-level `session_id` (regex `^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$`, `:33`, `:201`) for which a file of any kind exists at `$HOME/.claude/state/launch-level/sessions/<sid>` (`:257`). The store path is assembled from three literals so the script text never names it joined (`:19-23`). Everything else is "ordinary" and is never blocked (`:6-7`, FR-L-53).
- Level word in that file (`:262-269`): exactly one of `worktree`, `full`, `full-submit` (optional trailing newline); any other content, a directory/symlink, or an unreadable file gives level `W` plus the LL-STATE note (`:268`; probe G23/G24: file content `bogus` -> commit blocked, `git status` allowed). `sessions/<sid>.ok` (a regular file, not a symlink) lifts `W` to `WA` "worktree (approved)" (`:270-272`).
- Level semantics (labels at `:115-120`, effect in C.5): `W` worktree, `WA` worktree approved, `F` full, `FS` full-submit.
- Fast exit: if `$LL_STORE/sessions` does not exist and the input has no `[sc-launch:`, exit 0 before parsing (`:168-173`; probe G73: even a bound-looking id is allowed when the store dir is absent).
- Identity loss is a declared fail-open (`:390-392`): no `session_id`, or an invalid one, means ordinary (probe G45). `agent_id` is never read on PreToolUse and there is no cwd fallback (`:181`, `:391-392`). [UNVERIFIED] whether Claude Code reports the parent's `session_id` in subagent and nested-subagent tool payloads; the design makes this a ship gate ("Ship gate U1 (FR-L-13) ... OB-H1 item 1", `sc-issue-launch-level-hook.md:198-201`). Observation fixtures exist under `tests/hooks/fixtures/launch_level/ob_h1/` (see D.2).

### C.2 Binding on the first prompt

Prompt branch `:314-388`:
- B5: a prompt event with a non-empty `agent_id` (subagent) exits 0 and never binds or approves (`:315`; design `:199`; probe G46).
- Marker detection `:317-330`: strict `[sc-launch:v1:<32 hex>]` anywhere in the prompt, or a "loose" `[sc-launch:` marker at the start after whitespace/BOM.
- A nonce is usable only if `pending/` is a real directory owned by the user and `pending/<nonce>` is a regular non-symlink file (`:334-337`). The pending record is written by the claim script (`PENDING_PARTS` `orca_worktree.py:773`).
- Already governed (B8): the level never changes; a supplied nonce record is consumed (`:338-340`).
- Unbound and no marker: exit 0 (B9, `:366-368`).
- Marker present: from here any failure is LL-NOBIND (`:369`). No usable `session_id` -> deny (B7, `:370`; probe G55). `sessions/` must be a real owned directory (`:371-374`). The nonce is consumed with one `mv` to `sessions/.take-<sid>` (`:375-378`), then published with a hard link `ln`, which cannot replace an existing binding (`ll_link_take` `:299-313`, `ll_publish` `:289-297`).
- A leading marker whose nonce is missing or used publishes a `degraded` record (`:380-382`); `degraded` is not a level word, so it reads as `W` with the LL-STATE note (`:264-268`). Probes G53/G53b/G54: bogus nonce with leading marker -> binding file contains `degraded`, later `git commit` blocked. So a forged marker can only bind a session at the strictest level.
- A non-leading strict marker whose nonce is missing/used is blocked as LL-NOBIND (`:383-387`; probe G52: `hi [sc-launch:v1:<used nonce>] x` -> rc 2 "Blocked: this launch prompt.").
- Successful bind (probes G50/G50b/G51): record `full` created, nonce file consumed, later commit blocked at level `F`.
- Approval (FR-L-15..17, `:341-364`): only at level `W`. Granted when the first line starts with `/sc:implement`, `/sc:task` or `/task` as a whole word (`LL_RE_APR` `:347`), or the whole trimmed prompt lower-cased matches `^approved[.!]?$` (`:353`). It creates `sessions/<sid>.ok` with no-replace semantics if `sessions/` is an owned non-symlink directory (`:359-362`). A failed write still allows the prompt. Probes G56-G60: `Skill sc:implement` blocked at `W`, prompt `  Approved! ` creates `.ok`, then the skill is allowed (level `WA`) but `git commit` still blocked; at level `F` an `approved` prompt creates no `.ok`.

### C.3 Failure behaviour (fail-closed for governed, fail-open for ordinary)

- EXIT trap `ll_on_exit` (`:147-163`): any exit other than 0 or a deliberate deny is an internal failure. If the session is governed it becomes LL-BROKEN (tool branch) or LL-NOBIND (prompt branch), exit 2; if not governed, exit 0 (`:153-155`).
- jq failure branch (`:208-238`): a payload containing `"tool_name"` scans every `session_id` value for one with a record; a bound id found -> governed -> falls to the last line LL-BROKEN. A marker prompt without `tool_name` -> LL-NOBIND deny. Anything else -> allow ("identity loss"). Declared limit: any bound id anywhere in the broken text counts, even a nested one (`:212-216`). Probes: G47 (bound id in broken JSON) rc 2; G48 (ordinary) rc 0; G49 (marker + broken JSON) rc 2; no-jq PATH: bound session rc 2, ordinary rc 0, marker prompt rc 2, plain prompt rc 0.
- Default deny: last line `ll_deny LL-BROKEN` (`:746-747`); unknown class/level pairs also LL-BROKEN (`:740`).
- A tool field that is not a string, or contains NUL, or a non-object `tool_input`, is an "input error": governed -> LL-BROKEN (`:196-197`, `:395`; probes G43 rc 2, G44 ordinary rc 0).
- Never exits 1 (`:4-5`).

### C.4 Classifiers (tool branch, `:393-718`)

Each tool call is assigned zero or more classes; none = allowed.

| Tool / input | Class(es) | Source |
|---|---|---|
| `Skill` name (first word, lower-cased, one leading `/`, text after last `:`, one leading `sc-`, one trailing `-protocol`) | `implement\|task\|improve\|cleanup\|spawn\|build` -> IMPL; `pr-submit` -> SUBMIT; `issue` -> ESCAPE; unreadable/empty name -> SKILL | `:401-416` |
| `Bash`/`Monitor` command > 65536 bytes | BIG (nothing else checked) | `:422-423` (probe G72) |
| line continuation inside a word | UNKNOWN | `:428-429` |
| tamper tokens: `install_hooks`, any word ending `.claude` or `.claude/`, `superclaude ... install`, plus `.claude/state`, `.claude/settings`, `.claude/hooks`, `disableAllHooks`, `.gitconfig`, `.git/config`, `.config/git`, and dot-segment/double-slash forms after `.claude` | TAMPER | `:443`, `:451-452`, `:705-714` (probe G26 `cd ~/.claude/state` blocked; G35 Edit of `.claude/settings.json` blocked) |
| word basename `ccsession*`, `tmux`, `screen`, `xdotool`, `ydotool` | ESCAPE | `:457` (probe G25) |
| `claude`/`claude-code` word AND a launch-flag word (`-p --print --continue --resume --bare --settings --dangerously-skip-permissions --fork-session --session-id --permission-mode`) anywhere in the command | ESCAPE | `:453-454`, `:482` (probe G11) |
| `orca` word: next two non-option words are not one of `status`, `help`, `--version`, `worktree current\|list\|show`, `terminal list\|show\|read`, `orchestration check\|inbox\|run-current\|task-list\|worker-show` (unless the command ends in `--help`/`-h`) | ESCAPE | `:458-478` (probes G12 `worktree create`, G14 `orchestration worker-start` blocked; G13 `worktree list`, G15 `orchestration check` allowed) |
| `gh api ...` that is not one plain GET (anchored regex, no method/field/input word, endpoint not empty/graphql/merge) | GHWRITE | `:495-523` (probes G27, G28) |
| `git` subcommand table: commit/cherry-pick/revert/am/commit-tree/update-ref(HEAD,refs/heads) -> COMMIT; merge/pull -> MERGE; push -> PUSH; unknown subcommand, alias/pushurl/insteadof/hookspath/url configs, variable-built subcommand -> UNKNOWN | as listed | `:525-534`, `:611-654` (G22 `git frobnicate` UNKNOWN) |
| canonical push: only `git push [-u\|--set-upstream] origin <branch>[:<branch>]` passes; destination `master`/`main` -> PROTECTED; `HEAD` or any other form -> PUSHFORM | PROTECTED / PUSHFORM | `:659-669` (G05 PROTECTED, G06 allowed, G07 PUSHFORM) |
| `gh` group/action: `merge/update-branch/sync` -> MERGE; `pr create/edit/comment/ready`, `issue create/edit/comment` -> SUBMIT; `alias`, `extension`, unknown -> UNKNOWN; each `pr create` needs a non-empty `--repo`/`-R` operand in its own segment else REPO | as listed | `:568-608` (G09/G10) |
| merge endpoint (`repos/.../merge[s]`) or `api.github.com`/`uploads.github.com` in any word | MERGE / GHWRITE | `:559-566` |
| `Edit`/`Write`/`NotebookEdit` | tamper check on the path only; contents never read; `..` segments -> TAMPER | `:672-680` |
| `Agent`/`Task` with `isolation: "remote"` | ESCAPE; local/background = none; the prompt is never scanned | `:681-683` (G33, G34) |
| `Cron*` / `Schedule*` | TURN | `:684-685` (G37) |
| `RemoteTrigger`, `Workflow`, `SendMessage` | ESCAPE | `:686-687` (G17) |
| `mcp__*`: name after last `__`, lower-cased, containing merge/push/commit/pull_request/create_or_update_file/delete_file/update_ref/create_ref/create_branch; `list_*`/`get_*`/`search_*`/`read_*` exempt; `*merge*` -> MERGE else MCP | MERGE / MCP | `:688-699` (G39-G41) |
| any other tool the matcher lets through | none | `:700-702` |

Bash/Monitor text handling: a sed + `tr` normalisation produces T, G and W views (`:431-437`); no `${var//...}` substitution is run over the command text (`:420`). The classification works on text, not on parsed shell: `bash -c "git commit -m x"` and `echo "git commit"` are both treated as a commit (probes G19, G20); the block message explains this (`:130-132`, LL-TEXT note shown for every Bash/Monitor call that blocks, `:716-718`).

### C.5 Decision matrix (`:720-742`)

Classes are checked in this precedence order and the first blocked class produces the message: `BIG TAMPER MERGE GHWRITE PROTECTED ESCAPE MCP UNKNOWN SUBMIT REPO PUSH PUSHFORM COMMIT TURN IMPL SKILL` (`:722`).

| Class | W | WA | F | FS | Message |
|---|---|---|---|---|---|
| IMPL, TURN | block | allow | allow | allow | LL-IMPL, LL-TURN (`:725`, `:727`) |
| SUBMIT, COMMIT, PUSH, SKILL | block | block | block | allow | `:726`, `:728-729` |
| REPO, PUSHFORM, PROTECTED, MERGE, GHWRITE, UNKNOWN, MCP, ESCAPE, TAMPER, BIG | block | block | block | block | `:730-739` |

Observed (probes): `SKILL` at FS is allowed (G42c, `Skill` with no name at `full-submit` rc 0) and blocked at W (G42b). Commit blocked at `full` (G04) and allowed at `full-submit` (G03); `push origin main` blocked at every level (G05).

### C.6 Declared enforcement ceilings of this guard

1. Text-level only. "shortcut: text only; variables and quoting tricks still pass, so the real fix is the L2 layer" (`:710-711`). Quoted text that merely names `git` with `commit/push/merge/pull`, or `gh` with `api`, counts as the action (`:130-132`).
2. Only sessions bound by the launch marker are governed; `claim` output states "an agent started by hand is not governed by the launch-level hook" (`orca_worktree.py:1366`). Human sessions and ordinary Claude sessions are never restricted.
3. Identity loss (missing or invalid `session_id`) allows (`:390-392`), as does a bound id that is not visible in the hook payload.
4. `Monitor` is classified (same Bash text path, `:417`) but the identity helper does not adapt it (`launch-job-identity.sh:427-428`, section E).
5. Tamper detection is textual and covers the store, Claude settings/hooks, git config files and the installer (`:703-714`); the host-installed (origin/master) version adds git pre-push hook tokens. A person releases a session by deleting `sessions/<sid>` and `.ok` in their own terminal (the LL-TAMPER message, `:97`).
6. Registration and tool coverage depend on `~/.claude/settings.json` (B.1); the claim preflight refuses a governed launch when jq/uv/coreutils are missing, the settings disable hooks, or the registered matchers do not fire for the governed tool list (`orca_worktree.py:925-1015`). The claim only inspects its own process environment and settings files, not the environment of the agent Orca starts (`orca_worktree.py:925-930` docstring).
7. For supervised orchestration: a governed session cannot run any `orca` mutation outside the read-only allow-list at `:475-476` (so no `orca orchestration worker-start`, no dispatch/send), cannot use `SendMessage`, and cannot start `claude`/`ccsession`. This is a restriction on claim-launched agents, not a mechanism that identifies workers or coordinators.

## D. `tests/hooks/` (what the tests pin, and what they do not)

All files below were read (headers and the cited cases); the test suite was NOT run (running pytest would write `__pycache__`/cache files into the checkout). Counts are source counts of `def test_` and parametrised tables, not pass/fail results.

### D.1 Orca guard tests

- `tests/hooks/test_require_orca_worktree_agent.py` (201 lines). Runs the real script with `HOME` in `tmp_path` (`:41-48`). Tables: `BLOCKED` 30 commands (`:57-99`), `ALLOWED` 21 (`:101-125`), `FAIL_OPEN` 5 (`:144-152`), plus tests for missing jq (`:172-176`), missing awk (`:179-183`), an awk that prints `orca` but exits 3 must not block (`:186-194`), and "script is executable and runs no Python" (`:197-201`). The block message is asserted byte-for-byte (`BLOCK_MESSAGE` `:31-38`; stderr must equal it, `:133`) so the message change in the working tree (B.4) is pinned in the same uncommitted edit.
  - Allowed forms that matter for orchestration: `orca orchestration worker-start --name x` (`:115`), `orca worktree rm ...` (`:113`), `orca terminal list ...` (`:114`), `orca worktree list --name create` (`:112`). Pinned ceiling: `bash -c "orca worktree create --name x"` allowed (`:122`, id "bash-c-ceiling").
  - Blocked forms include command words built by substitution/variable (`:95-98`), a subshell, `if`, `||`, backgrounding, assignment prefix, redirection, continuation, a global `--json` option before `worktree`, and `bash <<'EOF'` with the create inside the shell's own heredoc (`:93`).
  - NOT covered by tests (but observed by probes in A.3/A.4): `--repo <value>` before `worktree`, `xargs`, `eval`, `env -S`, nested backtick escapes, non-Bash tool (`Monitor`) with a bare create (the `read-tool` case at `:147` covers `Read`, not `Monitor`).
- `tests/hooks/test_require_orca_worktree_agent_governed.py` (56 lines): one test feeding a governed-session event (`session_id` `old`, record `worktree`) with a bare create; expects exit 2 and the block text (`:31-56`). The docstring states the limit: the guard sees the ORIGINAL command; "whether the live order ever shows it the rewritten command is not verified here" (`:7-9`). Task artifact `.dev/tasks/done/TASK-WF-enforceTheOwnerP-20261108-031809/artifacts/t2-launch-identity-interaction.md` explains: if the Orca gate saw the identity hook's rewritten command, `orca worktree create` would sit inside one quoted argument and the scanner would allow it ("a known ceiling, the same quoted-execution family", `:28-30` of that artifact); the live check is listed as pending in that package's `t8-delivery.md`.

### D.2 Launch-level guard tests

- `tests/hooks/test_launch_level_guard.py` (4592 lines, 161 test functions, most parametrised). Runs the real script with `HOME` in `tmp_path`, `CLAUDE_CONFIG_DIR` unset and a PATH holding a temporary bin dir (`:3-7`, `_bin` `:98-108`); expected message texts are read from design section 9, not copied (`:6-7`, `_design_table` `:77-85`). Two test-only routes: running the `>>> printer` block alone and the `>>> normalise` block alone, and a copy of the script with one line changed to `exit 7` to drive the EXIT trap (`:8-15`). Coverage groups visible from the test names: empty/unbound/other-event fast paths (`:296-346`), trap behaviour (`:376-405`), binding B1..B13 including concurrency and nonce single-use (`:426-751`), Skill grid and name spellings (`:892-982`), speed budgets (`:992-1444`; the 3.5 s per-run limit is asserted on every run including xdist workers, `:998-1008`, commit `085afc8d1` / #440), ordinary-session-never-blocked and isolation (`:1493-1576`), subagents (`:1585-1598`), identity loss (`:1605`), jq missing (`:1624`), not-JSON (`:1664`), raw-id scan limit (`:1671-1683`), message texts (`:1700-1728`, `:4431-4530`), normalisation NRM1..7 (`:1867-2202`), git/push/gh grids (`:2421-3030`), tamper/escape (`:3179-3309`), policy grid (`:3382-3445`), TURN/ESCAPE/MCP (`:3457-3595`), accepted leaks (`:3602-3622`), approval flow (`:3722-3901`), regression corpora (`:4087-4391`), acceptance-map presence (`:4582`).
  - Pinned accepted leaks (T-GAP-1, design row 33, residual risk R1, owner decision O-7; `:3602-3622`): `G=gi; ${G}t push origin main`, `GH=gh; $GH pr merge 5`, `$'\x67it' push origin main`, `/usr/bin/gi[t] push origin main` (and the same with `HEAD:main`), `bash ./push.sh`, each allowed at every level. Probe confirmation (this investigation, fake HOME): all five allowed at `worktree`, `full` and `full-submit` (15/15 rc 0).
  - Subagent tests `test_subagent_governed` (`:1585-1590`) and `test_nested_subagent_governed` (`:1593-1598`) use hand-written payload shapes; their docstrings say "pending OB-H1: hand-written shape; agent_id is never read on PreToolUse". So they prove the script's behaviour for a payload that carries the parent's `session_id`, not that Claude Code sends such a payload.
- `tests/hooks/test_launch_level_guard_registration.py` (127 lines): guard registered exactly once on UserPromptSubmit and PreToolUse in both `hooks.json` trees, timeout 5, no matcher on the prompt registration (`:44-51`); not registered on other events (`:54-60`); no `onFailure` key (`:63-65`); PreToolUse matcher equals the string in design section 13 (`:68-71`); matcher matches the 14 guarded tool names and not `Read`/`Grep`/`Glob`/`TaskCreate` (`:74-95`); the Bash registrations are exactly `block-bare-python`, `require-orca-worktree-agent`, `launch-job-identity`, with identity last and the guard second to last (`:98-118`); guard entries identical in both trees (`:121-127`). The test does not assert timeouts of `require-orca` or `block-bare-python`, and does not assert execution order (only array position).
- `tests/hooks/test_launch_level_guard_with_identity.py` (212 lines): runs the guard and the identity hook one after the other on the same Bash payload. Pins: at `full-submit`, `git status` -> guard allows, identity rewrites only `command` (`:115-132`); a rewrite handed to the guard would trip LL-TAMPER because it contains the installed `.claude/hooks` path (`:135-154`); at `worktree`, `git commit` -> guard blocks while identity still rewrites (`:157-175`); ordinary session -> both silent (`:178-183`); a `degraded` record -> guard allows `git status` but the identity hook blocks every Bash call with "launch job: governed Bash call cannot be wrapped safely" (`:186-212`). Docstring: "Not observed here: the order in which Claude Code runs two matching PreToolUse hooks and how it combines a block with an updatedInput" (`:11-13`).
- `tests/hooks/test_launch_level_observations.py` (84 lines): the live observations OB-H1 items 1-9, OB-H2, OB-H3 and OB-CTX are `pytest.skip(...)` tests with the reason "needs a real governed session and has not been run" (`:79-84`). Also tests the log-only probe `fixtures/launch_level/ob_h1/log-only-probe.sh`. [CODE-VERIFIED] these 12 observations are explicitly unperformed in the checkout.
- `tests/hooks/fixtures/launch_level/ob_h1/` (README.md, 9 JSON fixtures, `log-only-probe.sh`) and `fixtures/launch_level/live_probe.py` (352 lines). The README states the fixtures are synthetic, "None of them was captured from a real session ... they are not evidence that any observation has been made" (`README.md:3`).

### D.3 Identity helper tests

- `tests/hooks/test_launch_job_identity.py` (1521 lines, 56 test functions; Linux only, `pytestmark` `:18`; module docstring "Real Linux session tests; deliberate setsid escape is NOT containment", `:1`). Pins, by name: single-use token consumption under concurrency (`:300-315`), the identify classification (`governed` / `ordinary` / `unknown`, reason `released`) including an orphaned background descendant keeping the origin while a new ordinary process and forged environment variables (`CLAUDE_SESSION_ID`, `CCSESSION_LAUNCH_ID`, `LAUNCH_LEVEL`) do not (`:318-355`), corrupt or stale job records give `unknown` and never "human" (`:359-411`), release while a job is live (`:421-437`), signal cleanup touching only ordinary descendants (`:441-458`), "intentional new-session escape explicitly unselected" (`:473-`), hook rewrites the whole input without a permission decision (`:644`), non-Bash tools are out of scope (`:701`), top-level session id only with no parent inference (`:840-859`), conflicting wrapper refused (`:872`), fresh-shell cwd contract (`:940`), missing UV cases (`:995`, `:1106-1166`), real-git scenarios (`:1292-1458`).
- Not covered by any test in `tests/hooks/`: a worker or coordinator session of the supervised-orchestration system; any `orca orchestration ...` command other than the read-only/escape classification in the launch-level guard and the `worker-start` allow-case in the Orca gate tests. [CODE-VERIFIED] by reading the test lists above.

### D.4 Related tests outside the assigned folder (listed for completeness, not read in full)

`tests/cli/test_install_hooks.py` pins: the three scripts are in `_FRESHNESS_SCRIPTS` and mirrored in `plugins/` (`:849-856`, `:930-936`, `:1085-1091`), real `hooks.json` registers each hook (`:828`, `:896`), real-install idempotence and policy preservation (`:943`, `:1098`), and upgrade insertion "guard lands before launch identity" (`:1160`). `tests/skills/test_issue_orca_worktree.py` references the guard names (4 hits; belongs to research file 04). `tests/unit/test_cli_install.py` has 1 reference.

## E. `launch-job-identity.sh` (job identity adapter and runner)

Source: `src/superclaude/hooks/scripts/launch-job-identity.sh` (566 lines; a bash header plus an embedded Python program run as `exec uv run --no-project python -I -c "$launch_identity_code" "$0" "$@"`, `:55-566`). The host-installed copy is the newer `origin/master` version (22 lines differ, FR-025 `reason`/`record` fields on `unknown`, B.4).

### E.1 Declared nature and limits (header `:1-19`)

"Linux same-user job identity, not a sandbox or controller-PID binding" (`:1`). `identify [PID]` prints `governed` / `ordinary` / `unknown` and "never command text" (`:4-5`). "Release is deletion of sessions/SESSION; malformed live state is unknown" (`:5`). "shortcut: deliberate setsid/daemonization escapes selection; upgrade to OS containment if hostile isolation is required. Killing the supervisor leaves unknown stale state, not trusted human identity. Monitor/pipelines unsupported" (`:7-9`). "updatedInput replaces the WHOLE input; omit permissionDecision so ordinary permission checks still apply. Other hooks' rewrite ordering is unspecified" (`:14-15`). "Each call uses a fresh bash: cd is local ... Always use an explicit cwd/cd in each governed call; persistent Claude Bash cwd tracking and live auto-mode rewrites need Task4" (`:16-18`).

### E.2 Modes (`main`, `:525-556`)

| Invocation | Behaviour | Source |
|---|---|---|
| no args or `hook` | PreToolUse(Bash) adapter (E.3) | `:526-527`, `hook()` `:414-489` |
| `execute SESSION TOOL_ID COMMAND` | accepted execution: re-validates, publishes one private request, then `run` | `:492-522`, `:528-529` |
| `prepare SESSION COMMAND [TOOL_USE_ID]` | prints a single-use 32-hex token after `governed()` | `:538-553` |
| `run TOKEN` | consumes the request, supervises the job | `:554-555`, `run()` `:362-398` |
| `identify [PID]` | classifies a process; default PID = itself | `:530-537`, `identify()` `:215-248` |
| anything else | "launch job: invalid invocation or unavailable private state", exit 2 | `:556`, `:559-564` |

### E.3 Hook mode (what it does to a governed session's Bash calls)

Shell pre-checks before Python:
- Missing `HOME`, or `~/.claude/state/launch-level` absent -> exit 0 before needing `uv` (`:20-24`; probe: no store -> rc 0).
- No `uv` on PATH, hook mode (`:25-54`): needs `jq` (absent -> exit 0, `:30`); then parses the top-level `session_id` (`:31-36`), walks `HOME` ancestors refusing symlinks (`:40-44`), requires the store directories and the record file owned by the user, non-symlink (`:45-50`). Only when ALL of that holds does it print "launch job: UV is required for this invocation" and exit 2 (`:52-53`); any failed precondition exits 0 (probes: bound session without uv -> rc 2 with that message; ordinary session without uv -> rc 0; without both uv and jq the script exits at `:30` before reading stdin, so the driver pipe's rc 141 is pipefail noise, not a script status).

Python `hook()` (`:414-489`):
1. Reads at most 1 MiB; over the cap, bad JSON or a non-object -> return 0 (`:417-425`).
2. `tool_name` present and not `Bash` -> 0 ("Monitor and other named tools have no adapter here", `:426-428`; probe: bound session + Monitor -> rc 0, empty output).
3. `session_id` invalid -> 0 ("do not guess from agent_id, parent fields, cwd or environment", `:429-431`); `HOME` not absolute -> 0; session file does not exist (`os.path.lexists`) -> 0 (`:432-437`). So an unbound session is untouched (probe: ordinary -> rc 0, no output).
4. A record exists, so the call is validated; any failure from here exits 2 with "launch job: governed Bash call cannot be wrapped safely" (`:484-486`): unsafe store permissions (`store()` `:102-122`: dirs owned by user, not group/other-writable, final store dir `0o077` clear), level word not one of `worktree|full|full-submit` (+ optional newline) (`governed()` `:177-186`), duplicate JSON keys or non-JSON constants (`:443`, `json_object` `:401-407`), event not `PreToolUse`/`Bash` (`:444-445`), raw envelope > 65536 bytes (`:446-447`), non-string `agent_id`/`agent_type` (`:448-450`), non-object `tool_input` (`:451-453`), command > 32768 bytes or containing NUL (`request()` `:189-199`), a command that itself invokes this runner (`reserved` regex `:456-460`), non-Linux/no `fcntl` (`:461-462`), no pidfd/subreaper support (`:463-468`), runner script or `/bin/bash` unavailable (`:469-472`).
5. On success it prints `hookSpecificOutput.updatedInput` = the original `tool_input` with `command` replaced by `shlex.join(['/bin/bash', <runner path>, 'execute', <sid>, <tool_use_id or ''>, <original command>])`, plus an `additionalContext` note; NO `permissionDecision` (`:475-483`; probe: `hasUpdated: true`, `hasPermissionDecision: false`, command begins `/bin/bash <path>...`).

Probe results for the degraded record: a session file containing `degraded` (which the guard writes itself for a leading marker with a missing/used nonce, C.2) makes the identity hook exit 2 for every Bash call, while the guard treats the same record as level `worktree` and allows read-only commands (probe; pinned by `test_launch_level_guard_with_identity.py:186-212`). A forged or replayed leading marker therefore leaves that session unable to run Bash while both hooks are installed. Fails closed; recorded as a mismatch with a proposed fix (add `degraded` to `LEVELS`) in `.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/hook-order.md:50-69`, which this checkout does not apply (`LEVELS` at `launch-job-identity.sh:74` is still the three words).

### E.4 Run/supervise (`run()` `:362-398`, `supervise()` `:291-359`)

- `run` consumes the request file once (`read_file(..., consume=True)`: `flock`, owner/mode checks, `st_nlink == 1`, size cap, unlink `:140-161`), re-checks `governed()`, creates `jobs/`, blocks termination signals, forks a dedicated child (`:365-383`).
- The child `setsid`s, sets `PR_SET_CHILD_SUBREAPER`, verifies pidfd support, writes the job record `jobs/<kernel-session-id>.json` with `{pid, start, boot, kernel_sid, session_id}` (`:292-305`, `publish` `:164-174`), then forks `bash -c <command>` (`:313-321`).
- It waits for the main shell and all non-zombie members of that kernel session, forwards SIGINT/SIGTERM/SIGHUP/SIGQUIT through pidfds with start-time checks (`forward` `:268-288`), escalates to SIGKILL after 1 s, exits with the shell's status (128+n for signals), and on exit kills survivors and unlinks the record only if no members remain (`:322-359`). Survivors leave the stale record, which `identify` reports as `unknown`.
- `identify(pid)` (`:215-248`): reads `/proc/<pid>/stat` for the kernel session id; no `jobs/<sid>.json` -> `ordinary`; otherwise validates the record (exact key set, `pid == kernel_sid == sid`, supervisor alive and not zombie, same start time and boot id, same uid, `:226-237`), then `governed()` on the recorded session id: record file gone -> `ordinary` with `reason: released`; otherwise `governed` with `session_id`. Any error -> `unknown` (`:243-244`). Probe: `identify` on an unrelated process in a store with no job record -> `{"status": "ordinary"}`.

### E.5 Who consumes it in this checkout

`grep` of non-test, non-docs, non-plugin sources for `launch-job-identity` finds only: registration `hooks.json:130`, installer list `install_hooks.py:90` (+ order comment `:460`), the claim preflight constant `orca_worktree.py:809` (checks the registration fires for Bash, `:1007-1014`), and the claim reference `sc-issue-protocol/refs/claim.md:120`. [CODE-VERIFIED] In this checkout nothing at runtime calls `identify`, `prepare` or `run` except the hook rewrite itself (which calls `execute`). The `identify` mode is called by `launch-level-pre-push.sh` (the L2 layer), which exists only on `origin/master` (probe: `git show origin/master:.../launch-level-pre-push.sh` lines 59, 65 call `launch-job-identity.sh identify "$$"`); it is not part of this checkout.

## F. Cross-cutting integration: what the guards do and do not enforce for supervised orchestration

Normative text under test: `src/superclaude/core/WORKER-CONTRACT.md:62` (WC-13: "The worker's top-level session never calls `worker-start`, `dispatch` or `task-create`, Orca's low-level dispatch, or `orca-cli` `worktree create --agent` or `agent launch`") and `:69` ("the coordinator: an Orca coordinator session the person opened"). Current ownership guidance in `src/superclaude/core/CLAUDE.md` ("A supervised orchestrator's coordinator is person-opened; ownership does not authorize a supervised worker to create worktrees or dispatch workers. A hook blocks `orca worktree create` without `--agent`.") agrees with the working-tree hook message (A.6) and with the hook's own header (`require-orca-worktree-agent.sh:6-8`). Project `CLAUDE.md:312` says the same in its own words ("An Orca coordinator is person-opened; ownership does not authorize a supervised worker to create worktrees or dispatch workers", not the `core/CLAUDE.md` wording "A supervised orchestrator's coordinator is person-opened"): the hook blocks a create without `--agent` and "the other parts of this rule are instructions only". [CODE-VERIFIED] consistent in meaning; the two wordings differ.

| Rule (source) | Machine enforcement in the assigned files | Evidence |
|---|---|---|
| Every Orca worktree create carries `--agent` (project/core `CLAUDE.md`) | YES, lexical, Bash tool only, fail-open (A.2-A.4) | `require-orca-worktree-agent.sh:99-103`, probes P01/P02 |
| A worker never runs `worktree create --agent` (WC-13) | NO. A create WITH `--agent` is exactly what the gate allows; the gate has no role input | probe P02 rc 0; `:97-103` |
| A worker never runs `orca orchestration worker-start` / `dispatch` / `task-create` (WC-13) | NO in the assigned hook files ("within the hook scope"): the Orca gate inspects only `worktree create` (test `test_require_orca_worktree_agent.py:115` pins `worker-start` as allowed). Machine-side control exists in Orca source, outside these files: worker-start scope and the nested-worker depth cap (checkout default 1 refuses a worker's helper start, installed-file default 2 allows one level; effective running setting UNVERIFIED), see research/01 section C.1 and research/05 section 5.2. Only inside a launch-level governed session are they blocked, as ESCAPE, because they are outside the read-only `orca` allow-list (`launch-level-guard.sh:475-478`; probes G12, G14). A supervised worker is not bound to a level by anything in the assigned files (C intro) | tests `:115`; probes |
| The coordinator is person-opened (`WORKER-CONTRACT.md:69`) | NO within the hook scope. No predicate in the assigned files reads session origin, role or Orca worker identity (Orca-side Run-binding refusal is narrow: research/05 section 4.2) | grep of `require-orca...sh` (A.1); `launch-level-guard.sh` reads only `session_id`, tool fields and the store (C.1) |
| The creator owns the agent it created | NO within the hook scope. Instruction text in the block message only | `:7-8`, `:354-355` |
| Launch-level limits for `/sc:issue --claim` agents | YES for bound sessions, text-level, with accepted leaks (C.4-C.6, D.2) | probes G01-G73; test pins |

Interaction of the three scripts on one Bash call (all registered PreToolUse; array order `block-bare-python`, `require-orca...`, `launch-level-guard`, `launch-job-identity`, B.1):
- Order of execution and the combination of one hook's block with another's `updatedInput` are UNVERIFIED (identity header `:14-15`; tests `test_launch_level_guard_with_identity.py:11-13`; artifacts `t2-launch-identity-interaction.md` and `hook-order.md`).
- Documented consequence if a later hook sees the identity hook's rewritten command: for the Orca gate, `orca worktree create` inside one quoted argument is not seen (known ceiling, `t2-launch-identity-interaction.md`); for the launch-level guard, the rewritten command contains the installed `.claude/hooks` path and would be blocked as LL-TAMPER at every level (`test_launch_level_guard_with_identity.py:135-154`). Both are scenario analyses pinned by direct script runs, not live observations.
- A session bound at `degraded` can run no Bash at all (E.3).

Evidence classes used in this file: normative = design doc and `WORKER-CONTRACT.md`/`CLAUDE.md` text; checkout source = the scripts read at the cited lines (working tree, B.4); probes = fixed-input runs of those scripts in a private temp directory, repeated at will; host observation = installed copies and settings on this machine (B.4); historical = task artifacts under `.dev/tasks/`; unverified = anything requiring a live Claude Code or Orca session.

---

## Key takeaways

1. Within the assigned hook files, the only role-related machine check is "`orca worktree create` carries `--agent`" (Orca source has its own worker-start, depth-cap and Run-binding controls, which are outside these files and build-dependent: research/01 section C.1). It is a bounded lexical check on Bash tool calls, fail-open on every input it cannot judge (A.2), with a documented list of unblocked forms (A.4). Role sentences in the block message and WC-13 are instruction text. WC-13 (workers never `worker-start`/`dispatch`/`task-create`/`worktree create --agent`) has no hook enforcement in the assigned files.
2. The launch-level guard is a separate control for `/sc:issue --claim` agents: it governs only sessions bound by a launch marker (C.1-C.2), is text-level (accepted leaks pinned and probe-confirmed, D.2), fails closed for governed sessions and open for ordinary ones (C.3). It also forbids a governed session from any `orca` call outside a read-only list and from `SendMessage` (C.4, C.6 item 7).
3. The job identity helper is a Linux-only foundation: it rewrites governed Bash calls through a supervised runner and can classify a process as governed/ordinary/unknown (E). In this checkout nothing calls `identify` at runtime; its consumer, the L2 pre-push hook, exists only on `origin/master`.
4. Revision matters. The working tree has an uncommitted block-message change in the Orca hook and its test; `origin/master` (local ref, 19 commits ahead) has an L2 pre-push layer and FR-025 identity reasons absent here; on this host the installed guard and identity hooks equal `origin/master` and the installed Orca-worktree hook equals HEAD and `origin/master`, none equals this tree (B.4, research/06 F6). The reference must name the revision it documents.
5. The live behaviours that decide real enforcement are all unobserved: hook execution order and `updatedInput` propagation, subagent `session_id` in payloads, self-started-turn wrapping (OB-H1 items 1-9, OB-H2, OB-H3, OB-CTX are skipped tests; fixtures are synthetic).

## Gaps and unverified claims

- [UNVERIFIED] Claude Code runs PreToolUse hooks inside subagents (`require-orca...sh:5-6`); `claude --bare` skips settings hooks (`:58`); whether matching PreToolUse hooks run serially/in parallel and which `updatedInput` wins (identity header `:14-15`).
- [UNVERIFIED] Whether subagent and nested-subagent payloads carry the parent's top-level `session_id` (design ship gate U1; tests `test_launch_level_guard.py:1585-1598` use hand-written shapes; OB-H1 item 1 unrun, `test_launch_level_observations.py:79-84`).
- [UNVERIFIED] The nested-backtick-with-`\` ceiling (`require-orca...sh:52`) was not probed; jq-missing and awk-missing branches of the Orca hook were read and are covered by tests (`:172-183`) but not run here.
- [UNVERIFIED] Installed-copy parity on any host other than this one; effective merged settings (project/local settings were checked only for `disableAllHooks` by the claim preflight code, not by this investigation).
- [UNVERIFIED] Test-suite pass/fail state: pytest was not run (it would write caches into the checkout). Test statements here are about what the tests assert, not that they pass.
- [CODE-CONTRADICTED] Header claim that the Orca hook's tokenizer is "copied" from `block-bare-python.sh` (`:21-25`): scanner blocks differ in 25 lines (A.5). Low impact.
- Ship gate is policy, not mechanism: `sc-issue-protocol/refs/claim.md:131` says no governed claim on a real issue until OB-H1 item 1, OB-H2 and OB-H3 pass, but a grep of `sc-issue-protocol` finds `OB-H1` only in docs, not in `orca_worktree.py`; the claim launches governed agents without checking that gate. Not recorded as DEFECT: the L1 guard IS wired (B.1, C) and the gate is documented as a usage rule, not as a shipped check.
- No in-scope capability documented as shipped/enabled but unwired at runtime was found, so no DEFECT is recorded. Closest items, deliberately not relabelled: (a) `identify`/`prepare`/`run` have no runtime consumer in this checkout (documented as a "foundation", `sc-issue-launch-level-hook.md:6`); (b) the L2 pre-push layer is documented as pending (`:6`, `claim.md:127`) and is absent here (present on `origin/master`; not read).
- Not read (outside the assigned list): `launch-level-pre-push.sh` (read by no research file) and the `origin/master` version of `orca_worktree.py` (research 04 F5 read only its header lines and grep hits; no file read it in full); `block-bare-python.sh` beyond its scanner block; `tests/cli/test_install_hooks.py` beyond a grep. `origin/master`'s `src/superclaude/core/CLAUDE.md` was read in fix cycle 1: it carries the old ownership wording and differs from HEAD only in MCP rows and core rules 3 and 8 (research/06 F6).
- Five `tests/hooks/` modules were not mentioned above and are unrelated to the guards: `test_auggie_first.py`, `test_auggie_flag_clear_mcp_prefix.py`, `test_freshness_pre_edit_create_case.py`, `test_freshness_subagent_start_policy.py` and `test_block_bare_python.py`; only `test_block_bare_python.py` bears on this file, through the tokenizer-provenance claim in A.5 (the Orca hook's scanner is derived from `block-bare-python.sh`, not a byte copy). None of the five was read in this research.
- Subordinate/sub-orchestrator mode: nothing in the assigned files implements, enforces or tests it; the Orca hook message says a supervised coordinator is person-opened (`:355`), which is the opposite of an automatic subordinate coordinator. It is deferred, not shipped.

### Gap fields: why it matters, closure, reference wording (fix cycle 1)

The bullets above are numbered GAP-1 to GAP-10 in order here (GAP-n is not a probe ID). Each row gives why it matters, how it closes, and the sentence the reference should use if it stays an accepted limit.

| ID | Gap (short) | Why it matters | Closure (read-only command or file, or "needs live ..., out of scope") | Sentence for the reference if it stays an accepted limit |
|---|---|---|---|---|
| GAP-1 | Subagent hook firing, `claude --bare`, serial vs parallel hook order, `updatedInput` winner | Decides whether the guards ever see a subagent's or a rewritten command | Needs a live Claude Code session (out of scope); the OB-H1 observation tests are skipped by design (`test_launch_level_observations.py:79-84`) | "Whether PreToolUse hooks fire inside subagents, and the order and combination of matching hooks, were not observed; the hook headers state them as unverified." |
| GAP-2 | Parent `session_id` in subagent payloads | A governed session's subagents would be ungoverned if the id is absent | Needs a live governed session (OB-H1 item 1; out of scope) | "Whether subagent payloads carry the parent's session id is unobserved; the tests use hand-written payloads." |
| GAP-3 | Nested-backtick `\` ceiling not probed | Could hide a bypass form | Re-run a probe only if the original command is known; it is not (probe not catalogued), so a new probe would need an owner-approved command; accepted limit | "The nested-backtick escape form listed in the hook header was not probed." |
| GAP-4 | Installed-copy parity on other hosts; merged settings | A reference could assert deployment that exists only here | This host closed by research/06 F6 (per-file `cmp`); other hosts need each host (out of scope) | "Installed parity was checked on the research host only; the installed set there is mixed (research/06 F6)." |
| GAP-5 | Test pass/fail state in this file | A reader could think the pins were run | research/06 ran two test files (744 passed); `tests/hooks/` results are unrun and running them writes caches into the checkout (needs authorization) | "Tests in `tests/hooks/` were read, not run; the statements describe what they assert." |
| GAP-6 | Header says the tokenizer is "copied" | Low; a literal-copy claim is wrong | Closed: P28 reproduced (254 vs 267 lines, 25 changed lines) | n/a (closed) |
| GAP-7 | Ship gate is policy, not mechanism | Readers may assume the claim refuses without OB-H1 items | Closed as an observation (a grep of `sc-issue-protocol` finds `OB-H1` only in docs); an owner decision decides whether to wire it | "The ship gate is documented as a usage rule; the claim script does not check it." |
| GAP-8 | Closest candidates for a DEFECT not relabeled | C8 forbids relabeling without a cited scope decision | The L2 absence on HEAD is documented as pending (`:6`, `claim.md:127`); `identify`/`prepare`/`run` consumer absence documented as a "foundation"; no change | "The L2 layer is absent from this checkout and present on `origin/master`; `identify` has no runtime consumer in this checkout." |
| GAP-9 | Files not read | A reference could cite them as read | `launch-level-pre-push.sh` and the `origin/master` `orca_worktree.py` are read by no research file; read-only `git show` can close it in a later cycle; accepted limit for this cycle | "The L2 pre-push script was not read by this research." |
| GAP-10 | Subordinate mode absent | It must not be described as shipped | Closed: no code, test or hook implements it | "Subordinate/sub-orchestrator mode is deferred and not implemented." |
| GAP-11 (added, N-13) | The degraded-record mismatch: a session record `degraded` makes the guard treat the level as `worktree` but makes the identity hook exit 2 for every Bash call (E.3) | A forged or replayed leading marker can leave a session unable to run Bash while both hooks are installed; the proposed fix (add `degraded` to `LEVELS`) is not applied | Read `.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/hook-order.md:50-69` (the proposal) and `launch-job-identity.sh:74` (`LEVELS` still three words); applying it is an owner decision, out of scope | "A `degraded` session record is allowed by the guard and blocked by the identity hook for every Bash call; the proposed alignment is not applied." |
| GAP-12 (added, N-13) | Twelve live observations are skipped tests (OB-H1 items 1-9, OB-H2, OB-H3, OB-CTX) | They decide hook order, subagent identity, rewrite behavior | Needs a live governed session (out of scope) | "The twelve live observations OB-H1 items 1-9, OB-H2, OB-H3 and OB-CTX were not performed; their tests are skipped with the reason 'needs a real governed session and has not been run'." |

## Stale or inconsistent documentation list

1. `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:800-805` and `refs/claim.md:127,129` ("L2 layer is not built yet"): true for this checkout, stale against `origin/master` (L2 landed in `5f8a1ea2d`, 2026-11-10).
2. `docs/designs/sc-issue-launch-level-hook.md:6,10` status line ("pending: ... L2 pre-push layer", ship gates) and `:355` (IR-7 says refuse) vs the code, which only warns (`orca_worktree.py:800-801`); the code comment acknowledges the deviation.
3. `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh:21-25` "copied" wording (A.5); `src/superclaude/cli/install_hooks.py:31-33` and the name `_FRESHNESS_SCRIPTS` still describe the list as freshness scripts although it holds the guards and many unrelated hooks (minor).
4. The installed `require-orca-worktree-agent.sh` on this host (and the committed HEAD version) still say "The session that creates the worktree becomes its orchestrator (or a coordinator under another orchestrator) and owns that agent" (B.4); the working tree no longer does. Historical research report wording is the older form; not re-checked here.
5. `src/superclaude/hooks/README.md` has no mention of any of these guards (grep count 0), so no developer-facing hook README documents their contracts; the contracts live in script headers, `docs/designs/sc-issue-launch-level-hook.md` and `refs/claim.md`.

## G. Probe catalogue (added in fix cycle 1)

Why this section exists: the file cites probe IDs `P01`-`P28` and `G01`-`G73` but the first pass recorded no catalogue and did not record most inputs. Rule applied here (B-16): inputs are listed only as recorded in this file or as an exact row of a test table that matches the recorded shape; nothing is invented. Where the full input was not recorded the cell says so, and the claim keeps its cited source line and is retagged as below. Status words: FULL = command or payload fully recorded in this file; RECONSTRUCTED (test row) = only the shape is recorded here, and the named test row is an exact command of that shape taken from the tests; it is a reconstruction from a cited source, and the original probe may have used other arguments (names, prompts); PARTIAL = command shape known, no matching test row, tail or payload not recorded; ID-ONLY = the ID appears only in a range or a count, no individual input. Every probe result below is "as reported by the first pass"; no probe was re-run for a result in this cycle (the original harness output was not kept).

Harness for the `P` series (known from the hook and the tests, not from the first pass): stdin is the JSON `{"tool_name": "Bash", "tool_input": {"command": "<cmd>"}}` (`tests/hooks/test_require_orca_worktree_agent.py:51-54`), the hook runs as `bash <hook>` with `HOME` set to a temporary directory (`:41-48`); expected for a block: exit 2, nothing on stdout, stderr equal to the block message (`:128-133`); for an allow: exit 0, empty stdout and stderr (`:136-141`).

### G.1 `P` series (`require-orca-worktree-agent.sh`)

| ID | Input as recorded in this file | Exact matching test row (`tests/hooks/test_require_orca_worktree_agent.py`) | Reported rc | Status |
|---|---|---|---|---|
| P01 | bare `orca worktree create --name x` | `BLOCKED["bare-create"]` `:58` | 2 (block) | FULL |
| P02 | create with `--agent claude` | `ALLOWED["create-with-agent"]` `:107`: `orca worktree create --name x --agent claude --prompt t` | 0 | RECONSTRUCTED (test row) |
| P03 | create with `--agent=claude` | `ALLOWED["create-with-agent-equals"]` `:108` | 0 | RECONSTRUCTED (test row) |
| P04 | `orca worktree list` | `ALLOWED["worktree-list"]` `:111` | 0 | FULL |
| P05 | `bash -c` wrapping a create | `ALLOWED["bash-c-ceiling"]` `:122`: `bash -c "orca worktree create --name x"` | 0 | RECONSTRUCTED (test row) |
| P06 | `echo "orca worktree create"` | `ALLOWED["quoted-echo"]` `:116` | 0 | FULL |
| P07 | `orca --repo foo worktree create` (tail not recorded) | none (03 D.1 says not covered by tests) | 0 | PARTIAL |
| P08 | `$ORCA worktree create` (tail not recorded) | `BLOCKED["variable-command-word"]` `:96`: `$ORCA worktree create --name x` | 2 | RECONSTRUCTED (test row) |
| P09 | `--prompt "--agent"` on a create (rest not recorded) | none | 0 | PARTIAL |
| P10 | create after `cd ... &&` | `BLOCKED["after-cd-and"]` `:60`: `cd /x && orca worktree create --name x` | 2 | RECONSTRUCTED (test row) |
| P11 | `... create --help` | `ALLOWED["create-help"]` `:109`: `orca worktree create --help` | 0 | RECONSTRUCTED (test row) |
| P12 | `xargs orca ...` (rest not recorded) | none | 0 | PARTIAL |
| P13 | `sudo orca ...` | `BLOCKED["sudo-wrapper"]` `:65`: `sudo orca worktree create --name x` | 2 | RECONSTRUCTED (test row) |
| P14 | `orca worktree create --name x; orca worktree create --name y --agent claude` | `BLOCKED["bare-first-agent-second"]` `:74-77` (same shape, different names) | 2 | FULL (recorded in this file) |
| P15 | Monitor tool carrying a bare create (command text not recorded) | none (the `read-tool` row `:147` covers `Read`, not Monitor) | 0 | PARTIAL |
| P16 | `env -S ...` (rest not recorded) | none | 0 | PARTIAL |
| P17 | `/usr/local/bin/orca ...` | `BLOCKED["abs-path"]` `:63`: `/usr/local/bin/orca worktree create --name x` | 2 | RECONSTRUCTED (test row) |
| P18 | `eval ...` (rest not recorded) | none | 0 | PARTIAL |
| P19 | `$(printf orca) worktree create` | `BLOCKED["subst-command-word"]` `:95`: `$(printf orca) worktree create --name x` | 2 | RECONSTRUCTED (test row) |
| P20 | `--agents claude` on a create (rest not recorded) | none | 2 | PARTIAL |
| P21 | `echo $(orca worktree create --name x)` | `BLOCKED["dollar-subst"]` `:61` | 2 | FULL |
| P22 | `orca --json worktree create ...` | `BLOCKED["global-option-first"]` `:92`: `orca --json worktree create --name x` | 2 | RECONSTRUCTED (test row) |
| P23 | `cat <<'EOF' \| bash` with a create in the body (body not recorded) | none (`BLOCKED["shell-heredoc"]` `:93` is the case where the create is inside `bash <<'EOF'`, a different shape) | 0 | PARTIAL |
| P24 | `timeout 5 nohup orca ...` (tail not recorded) | none | 2 | PARTIAL |
| P25 | `o$(printf rc)a ...` (tail not recorded) | none | 0 | PARTIAL |
| P26 | input that is not valid JSON | `FAIL_OPEN["non-json"]` `:145` (`b"this is not json"`; the probe's actual bytes were not recorded) | 0 | PARTIAL |
| P27 | empty stdin | `FAIL_OPEN["empty-stdin"]` `:146` | 0 | FULL |
| P28 | Not a hook run: scanner text comparison. Reproduced read-only in fix cycle 1: scanner heredoc of `require-orca-worktree-agent.sh` is lines 74-340 (267 lines, from `read -r -d '' SCANNER <<'AWK'` to `AWK`); of `block-bare-python.sh` lines 76-329 (254 lines); `diff` of the two ranges prints 25 changed lines (6 removed, 19 added) | n/a | n/a | FULL and re-verified |

### G.2 `G` series (`launch-level-guard.sh`)

Harness: a temporary HOME holding `.claude/state/launch-level/sessions/<sid>` with a level word (`worktree`, `full`, `full-submit`, or another content), per 03 C.1 and `launch-level-guard.sh:257-272`; the exact payload JSON of each probe was not recorded. The real script and a temporary HOME are the method the test file uses (`tests/hooks/test_launch_level_guard.py:3-7`, helpers `:98-108`); no test row is claimed to be the same input. Reported rc is the first pass's statement; "block" = rc 2.

| ID | Input as recorded | Reported result | Status |
|---|---|---|---|
| G01 | named only inside the range "G01-G73" (section F table) | n/a | ID-ONLY |
| G03 | `git commit` at level `full-submit` (message not recorded) | allowed | PARTIAL |
| G04 | `git commit` at level `full` | blocked | PARTIAL |
| G05 | `git push origin main` at every level | blocked (PROTECTED) | PARTIAL |
| G06 | canonical `git push [-u\|--set-upstream] origin <branch>` | allowed | PARTIAL |
| G07 | `git push` with `HEAD` or another non-canonical form | blocked (PUSHFORM) | PARTIAL |
| G09 | a `gh pr create` form (flags not recorded) | REPO class (G09/G10 together) | PARTIAL |
| G10 | a `gh pr create` form (flags not recorded) | REPO class (G09/G10 together) | PARTIAL |
| G11 | `claude` word plus a launch-flag word | blocked (ESCAPE) | PARTIAL |
| G12 | `orca worktree create` | blocked | PARTIAL |
| G13 | `orca worktree list` | allowed | PARTIAL |
| G14 | `orca orchestration worker-start` | blocked | PARTIAL |
| G15 | `orca orchestration check` | allowed | PARTIAL |
| G17 | `RemoteTrigger`, `Workflow`, `SendMessage` tools | blocked (ESCAPE) | PARTIAL |
| G19 | `bash -c "git commit -m x"` | treated as a commit | FULL (command recorded) |
| G20 | `echo "git commit"` | treated as a commit | FULL |
| G22 | `git frobnicate` | blocked (UNKNOWN) | FULL |
| G23, G24 | session record content `bogus`; a commit and a `git status` (which ID is which was not recorded) | commit blocked, `git status` allowed (level treated as `W`) | PARTIAL (group) |
| G25 | a word with basename `ccsession*`, `tmux`, `screen`, `xdotool` or `ydotool` | blocked (ESCAPE) | PARTIAL |
| G26 | `cd ~/.claude/state` | blocked (TAMPER) | FULL |
| G27 | a `gh api ...` form (not recorded) | GHWRITE class (G27/G28 together) | PARTIAL |
| G28 | a `gh api ...` form (not recorded) | GHWRITE class (G27/G28 together) | PARTIAL |
| G33, G34 | `Agent`/`Task` with `isolation: "remote"`, and local or background (which ID is which was not recorded) | remote: blocked (ESCAPE); local/background: no class | PARTIAL (group) |
| G35 | `Edit` of `.claude/settings.json` | blocked (TAMPER) | PARTIAL |
| G37 | `Cron*` / `Schedule*` tool | TURN class | PARTIAL |
| G39, G40, G41 | named only as the range "G39-G41" next to the `mcp__*` classifier row (C.4); tool names not recorded | outcomes stated for the row: `*merge*` MERGE, else MCP, `list_*`/`get_*`/`search_*`/`read_*` exempt | ID-ONLY (range) |
| G42b | `Skill` with no name at level `worktree` | blocked | PARTIAL |
| G42c | `Skill` with no name at level `full-submit` | allowed (rc 0) | PARTIAL |
| G43 | a payload with a non-string tool field, governed session | rc 2 | PARTIAL |
| G44 | same input, ordinary session | rc 0 | PARTIAL |
| G45 | payload without a usable `session_id` | ordinary (allowed) | PARTIAL |
| G46 | a prompt event with a non-empty `agent_id` | exit 0, no bind | PARTIAL |
| G47 | broken JSON containing a bound session id | rc 2 | PARTIAL |
| G48 | broken JSON, ordinary session | rc 0 | PARTIAL |
| G49 | marker prompt plus broken JSON | rc 2 | PARTIAL |
| G50, G50b, G51 | a successful bind (marker prompt with a fresh nonce) and a later commit (which ID is which was not recorded) | record `full` created, nonce file consumed, later commit blocked at level `F` | PARTIAL (group) |
| G52 | `hi [sc-launch:v1:<used nonce>] x` | rc 2, "Blocked: this launch prompt." | FULL (shape; nonce placeholder) |
| G53, G53b, G54 | a leading marker with a bogus nonce and a later commit (which ID is which was not recorded) | binding file contains `degraded`, later `git commit` blocked | PARTIAL (group) |
| G55 | a marker prompt without a usable `session_id` | deny | PARTIAL |
| G56-G60 | named as the range "G56-G60" (the prompt `  Approved! ` is recorded verbatim; the individual assignment of IDs is not) | `Skill sc:implement` blocked at `worktree`; prompt `  Approved! ` creates `.ok`; the skill is then allowed (level `WA`) while `git commit` stays blocked; at level `full` an `approved` prompt creates no `.ok` | PARTIAL (range) |
| G72 | a Bash command longer than 65536 bytes | BIG class (nothing else checked) | PARTIAL |
| G73 | session store directory absent, a bound-looking id | allowed | PARTIAL |

### G.3 Probes without an ID, counts, and how claims are retagged

- Unlabelled probes cited by result only: identity-helper hook runs (rc 0/2 cases in E.3, `identify` output in E.4), the no-jq and no-uv PATH cases in C.3 and E.3, the plugin-mirror `cmp`, and the plugin/source `hooks.json` comparison (B.2: "49 differing lines"). Their inputs were not recorded; they are PARTIAL or ID-ONLY by the same rule.
- Count "15/15 rc 0" (D.2 accepted leaks): five commands, listed in D.2 (`G=gi; ${G}t push origin main`, `GH=gh; $GH pr merge 5`, `$'\x67it' push origin main`, `/usr/bin/gi[t] push origin main`, `bash ./push.sh`), each at three levels (`worktree`, `full`, `full-submit`) = 15 runs. The inputs are known; the result was reported, not kept. Retag: the claim "allowed at every level" is [CODE-VERIFIED as pinned by the test source] (`tests/hooks/test_launch_level_guard.py:3602-3622`, not run) and the "15/15 rc 0" run result is [UNVERIFIED as a reproduction].
- Retag rule applied to every `Pnn` / `Gnn` citation in this file: the claim stays [CODE-VERIFIED] where the same row cites a source line that states the behavior (most rows do: for example the classifier table in C.4 cites `launch-level-guard.sh` lines); the probe ID is corroboration only. A claim that has no source line and rests only on a PARTIAL or ID-ONLY probe is [UNVERIFIED] as a probe result. Rows affected: the `Observed` sentences at C.5 (`SKILL` at FS allowed at G42c, commit at `full` and `full-submit`, `push origin main` at every level), the "forged marker" results in C.2 (G50-G54), and the approval-flow results (G56-G60), each of which also cites source lines in the same paragraph.

## Summary

This file maps three PreToolUse/UserPromptSubmit guards, their registration, installer and tests, from source read at exact lines plus fixed-input probes. The Orca worktree gate blocks only a lexically recognised `orca worktree create` without `--agent`, on Bash calls only, and fails open on missing jq/awk, bad input, other tools and scanner errors; it has no role input, so WC-13 and "coordinator is person-opened" are instruction text. The launch-level guard governs only sessions bound by a launch marker, classifies commands by text with pinned accepted leaks, fails closed for governed sessions and open for ordinary ones, and blocks governed sessions from `orca` mutations and `SendMessage`; the identity helper is a Linux-only runner/classifier whose `identify` mode has no runtime consumer in this checkout. The working tree carries an uncommitted message change, `origin/master` is ahead with an L2 pre-push layer, and the host-installed hook set is mixed (guard and identity equal `origin/master`, the Orca-worktree hook equals HEAD and `origin/master`), so the final reference must state its revision; hook ordering, subagent `session_id` and the OB-H1/H2/H3 observations remain unobserved.

Status: Complete

