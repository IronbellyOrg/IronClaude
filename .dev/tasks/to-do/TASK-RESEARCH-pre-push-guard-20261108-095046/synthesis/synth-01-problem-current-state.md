# Synthesis 01: Problem Statement and Current State Analysis

**Topic:** git pre-push hook semantics for an L2 guard that refuses a governed AI agent's push to `refs/heads/main` or `refs/heads/master`
**Date:** 2026-11-08
**Sources:** `research/01-identity-selector-ancestry.md` (01), `research/02-l1-guard-push-bypass-coverage.md` (02), `research/03-design-and-claim-code-crossvalidation.md` (03), `research/04-empirical-git-prepush-experiments.md` (04), `gaps-and-questions.md` (GQ). All paths below are relative to the worktree root unless stated.
**Evidence rule used here:** Section 2 states as current architecture only facts traced to a source-code read (with file:line) or to recorded `/tmp` command output (with the experiment id). Design-document statements are carried only with their verification tag. Git behaviour is reported only as observed with git 2.47.3 in a disposable `/tmp` sandbox; it is not a claim about other git versions.

---

## 1. Problem Statement

### 1.1 The research question

The research question, as set for this task:

> Exact semantics of git's pre-push hook relevant to a guard that refuses an AI agent's push to `refs/heads/main` or `refs/heads/master`, with these sub-questions:
> (a) stdin records and arguments;
> (b) bypass paths;
> (c) hook lookup in linked worktrees;
> (d) process ancestry and environment;
> (e) no-replace atomic publication and the executable bit;
> (f) versions.

### 1.2 What is being solved

The project has a launch-level system for governed AI sessions (sessions started by `/sc:issue --claim`). It has two planned layers:

| Layer | What it is | State today (evidence) |
|---|---|---|
| L1 | A Claude Code PreToolUse/UserPromptSubmit text guard, `src/superclaude/hooks/scripts/launch-level-guard.sh`, that classifies the command text of a governed session's tool calls | Built. It refuses canonical pushes to `main`/`master` (LL-PROTECTED) and the non-canonical push spellings it recognises (LL-PUSH-FORM) (02 §5, guard lines 659-669, 731-732); known misses: underscore env prefix with an obfuscated subcommand, smart-HTTP `curl`, library and script pushes (see §2, 02 Gaps) |
| L2 | A git `pre-push` hook that sees the real ref-update records git is about to send, and refuses the push when a governed agent is the pusher and a record's destination is `refs/heads/main` or `refs/heads/master` | Not built. No source file installs, owns or verifies a git `pre-push` hook (03 §4, D19-8, D19-71, D19-81 [CODE-VERIFIED as absent]) |

L2 is needed because L1 reads only command text. By its own in-code admission it is a text-only shortcut ("variables and quoting tricks still pass, so the real fix is the L2 layer", guard lines 710-711, 02 §6), and the static reading in 02 found push spellings and configuration writes that pass it (02 §9; detailed in Section 2.1 below).

### 1.3 Why this research was done

This research is input to the issue #441 brainstorm (`.dev/brainstorms/20261108-094705-l2-pre-push-guard/`), which will spec:

1. the L2 pre-push layer itself (what the hook reads, how it selects the actor, what it refuses, how it is installed and verified); and
2. the IR-7 `W-L2-ABSENT` refusal: today the claim launcher only warns when no L2 hook is present and still starts the agent (`orca_worktree.py` lines 789-799, 1305-1312; 03 §3), while the design (IR-7 at design line 355 and section 19.2 line 514) says the governed launch should be refused. The brainstorm must decide what "an accepted L2 is present" means before that warning can become a refusal.

### 1.4 What prompted it

| Trigger | Evidence |
|---|---|
| The design's L2 contract (sections 19.2-19.5 of `docs/designs/sc-issue-launch-level-hook.md`) is almost entirely unverified: of 83 checkable section-19 statements, the L2-specific ones have no code behind them, and the 19.6 source artifacts (`.dev/brainstorms/20261106-l2-prepush-decisions/`) are absent from the checkout | 03 Summary; 03 §1; 03 §5 |
| Fourteen git-behaviour claims in the design were marked UNVERIFIED-GIT and needed a real-git cross-check | 03 Gaps, "Git-behaviour claims for the experiment cross-check" |
| The owner decided on 2026-11-08 that an `unknown` identity verdict refuses only pushes to `main`/`master` (with a diagnostic) and allows everything else; the L2 hook must be able to implement that decision | 01 §4 (seed brief line 73, "Orca answer to msg_60b98182bb31") |
| L1 has known holes for push spellings and hook/config tampering, so the brainstorm needs to know which of them a client-side pre-push hook can and cannot cover | 02 Summary; 02 §9 |

### 1.5 Scope boundaries

| In scope | Out of scope for this section |
|---|---|
| Git pre-push semantics as observed with git 2.47.3; the existing L1 guard; the job-identity selector; the `l2_status` probe; the Claude Code hook installer | Server-side branch protection on the hosting service; behaviour of other git versions or network transports (not tested; see GQ G-3, G-27); whether git libraries (pygit2, dulwich, GitPython, JGit) run pre-push (routed to web research, GQ G-2) |

---

## 2. Current State Analysis

### 2.1 L1 text guard push coverage (`launch-level-guard.sh`)

Source: `src/superclaude/hooks/scripts/launch-level-guard.sh` (747 lines), read statically by 02. The guard was not run; every verdict below comes from the regexes and branches at the cited lines.

**Who is checked.** Only a governed session (its `session_id` has a record under the launch-level store) is classified: tool branch `[ "$LL_GOVERNED" = 1 ] || exit 0` (line 394); session binding at lines 257-273. Only `Bash` and `Monitor` command text is classified as commands (line 417). An ordinary session is never checked [CODE-VERIFIED, line 394].

**How a refusal is produced.** `ll_deny <ID>` (lines 135-139) sets `LL_DENIED=1`, prints `Blocked:`/`Why:`/`You can:` text through `ll_say` (lines 36-133) to stderr, and exits 2. Line 59 is the `LL-PROTECTED` Blocked string ("a push to master or main."), not a check.

**Data flow (text only).**

```
tool_input.command (jq, line 195)
   |
   v
normalise (lines 421-438)
   T  = sed: drop quotes/backslashes, squeeze '/', backtick -> ' $;'   (line 431)
   G  = raw+T, lower-cased, non [a-z0-9._/~$@+:-] -> space             (line 433)
   W  = T, ';&|()' and newline -> ';' segments; '_' and others -> space (line 435)
   |
   +--> G-level regexes (lines 483-534): git word, gh word, URL hint,
   |       PUSH (' push | send-pack | http-push '), config-rewrite tokens
   +--> per-segment classifier on W (lines 535-657): command position,
   |       git subcommand table G3 (only at command position, line 637)
   +--> tamper tokens on T or edit path (line 706)
   |
   v
canonical push check (lines 659-669) -> PROTECTED / PUSHFORM
   |
   v
decision order (line 722): BIG TAMPER MERGE GHWRITE PROTECTED ESCAPE MCP
   UNKNOWN SUBMIT REPO PUSH PUSHFORM COMMIT ...  -> first blocked class wins
```

**The canonical push rule.** When `PUSH` is in the class list, the raw command must match `^[[:space:]]*git push( (-u|--set-upstream))? origin <src>(:<dst>)?[[:space:]]*$` (line 661). The destination (group 5, else group 3) loses one leading `refs/heads/` or `heads/` (line 664); an exact, case-sensitive `master | main` gives `PROTECTED`, `HEAD` gives `PUSHFORM` (line 665); a failed match gives `PUSHFORM` (line 667). `PROTECTED` is refused at every level (line 732); `PUSHFORM` is refused at every level (line 731); a plain `PUSH` is allowed only at `full --submit` (line 726). So at full --submit the only push L1 lets through is the canonical form with a destination that is not exactly `main`, `master` or `HEAD` (02 §5).

**Coverage of push and bypass spellings** (verdict at full --submit; an ALLOWED from "no class at all" holds at every level; 02 §8):

| Candidate | L1 verdict | Deciding line(s) |
|---|---|---|
| `git push origin main` / `HEAD:main` / `x:refs/heads/main` / `x:heads/main` | REFUSED (LL-PROTECTED) | 661-665, 732 |
| `git push --no-verify ...`, `--force`, `+main`, `:main`, `--delete main`, `--mirror`, `--all`, `--tags` | REFUSED (LL-PUSH-FORM) | 528-529, 661, 667, 731 |
| `git -c core.hooksPath=... push ...`, `git config core.hooksPath ...` | REFUSED (UNKNOWN, `hookspath` token) | 532-533, 651, 735 |
| `git send-pack`, `git http-push`, `git-push`, `/usr/lib/git-core/git-push` | REFUSED | 486-488, 528-529, 653, 661, 667 |
| `GIT_DIR=... git push`, `git -C <dir> push`, `git --git-dir=... push`, `HOME=... git push`, `env -i`/`env -u HOME git push`, `PATH=<no uv> git push` | REFUSED (PUSHFORM, anchored regex) | 661, 667 |
| `git config alias.*`, `remote.origin.pushurl`, `url.*.insteadOf` | REFUSED (UNKNOWN) | 532, 651, 735 |
| `gh api -X PATCH .../git/refs/heads/main`, `gh api --method POST .../git/refs` | REFUSED (LL-GH-WRITE) | 499-523, 734 |
| `curl` to literal `api.github.com/repos/.../git/refs...` | REFUSED (LL-GH-WRITE); ALLOWED if the host is hidden | 494, 565, 656, 734 |
| MCP tools named `*push*`, `*create_ref*`, `*update_ref*` | REFUSED (LL-MCP) | 688-699, 736 |
| Write/Edit to `.git/hooks/pre-push`; `rm`/`mv`/`chmod -x`/`ln -sf`/`printf >` on it | **ALLOWED** (no `.git/hooks` token; `.git/` does not set the git word) | 486, 679, 706, 743 |
| Config written without a git word or contiguous `.git/config` path (`cd .../.git && ... >> config`, `config.worktree`) | **ALLOWED** (PARTIAL) | 706, 738 |
| `curl -X POST https://github.com/<o>/<r>.git/git-receive-pack` | **ALLOWED** | 486, 494, 528, 637, 743 |
| `uv run python <script>` that pushes; library `.push(` calls | **ALLOWED** / PARTIAL | 528, 678, 743 |
| canonical `git push origin <b>` after `cd` into another checkout | ALLOWED (L1 has no notion of which repository) | 661-665, 726 |

**Defect found by static reading: command position moves off `git` behind an underscore env name.** W is built with `tr -c 'A-Za-z0-9._/=:@+~$;-' ' '` (line 435), which has no `_` (comment lines 440-441). So `GIT_DIR=/x git ...` reaches the command-position loop as `GIT`, `DIR=/x`, `git`; `GIT` does not match `LL_RE_NAME` (line 536) and becomes the command-position word (line 557). The subcommand table G3 runs only for the git word in command position (line 637), so an alias or obfuscated subcommand behind such a prefix is not refused. Unlisted wrappers (`chrt`, `taskset`, `find -exec`, `uv run`; list at line 549) have the same effect (02 §4). [CODE-CONTRADICTED] against the LL-UNKNOWN Why text at line 80 ("a renamed command or an alias cannot commit, push or merge") (02 Stale Documentation).

**Static evasions (derived from the regexes, none executed; 02 §9, GQ G-39):**

| Spelling | Why L1 passes it | Lines |
|---|---|---|
| `A_B=1 git $'\x70ush' --no-verify origin main` | T turns `$'\x70ush'` into `x70ush` (no ` push ` word); `_` dropped moves command position to `A`; G4 needs a `$` that T removed | 431, 435, 528, 556-557, 634-637, 743 |
| `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=$'core.hooks\x50ath' GIT_CONFIG_VALUE_0=/dev/null` before such a call | `hookspath` token matched as text; `hooks\x50ath` becomes `hooksx50ath` | 431, 532 |
| `cd <common-dir>/.git && printf '[remote "origin"]\n\tpush = refs/heads/<b>:refs/heads/main\n' >> config`, then canonical `git push origin <b>` | write has no git word and no contiguous `.git/config`; later push is canonical with a non-main destination; git maps it to `refs/heads/main` through `remote.origin.push` | 486, 525, 661-665, 706, 726 |
| unlisted wrapper before `git` (`chrt 0 git ...`) | wrapper becomes command position | 549, 557, 637 |

The `remote.origin.push` mapping named in the third row is confirmed for git 2.47.3 by experiment E20 (Section 2.5): the pre-push hook sees field 3 = `refs/heads/main` for such a push.

**Tamper coverage relevant to an L2 hook.** The tamper token list (line 706) is `*"$LL_S1/$LL_S2"* | *.claude/settings* | *.claude/hooks* | *disableAllHooks* | *.gitconfig* | *.git/config* | *.config/git*`. There is no `.git/hooks`, `hooks/pre-push` or `config.worktree` token [CODE-VERIFIED, line 706]. The config-rewrite tokens at line 532 (`alias.`, `pushurl`, `insteadof`, `hookspath`, `remote.`, `url.`, `include*`, `set-url`) run only when the command also contains a git word (line 525). The LL-TAMPER Blocked text (line 95, "a git configuration file") is [CODE-CONTRADICTED] (partial): only contiguous-path spellings are covered (02 Stale Documentation).

**What L1 cannot see at all.** A destination chosen by existing git configuration rather than by the command text, and which repository the current directory is (02 §5). L1 reads no git configuration.

### 2.2 Job-identity selector and process ancestry (`launch-job-identity.sh`)

Source: `src/superclaude/hooks/scripts/launch-job-identity.sh` (566 lines), read in full by 01, plus a real-git experiment in `/tmp/l2-ident.*` and `/tmp/l2-ident2.*` (both removed afterwards) using git `/usr/bin/git` and uv 0.11.8 (01 §7).

**Structure.** A bash wrapper whose body is a Python program in a quoted heredoc (line 55 to line 565), run by `exec uv run --no-project python -I -c "$launch_identity_code" "$0" "$@"` (line 566). `main()` receives the original bash arguments (line 560). The Python body is not importable from other modules (01 §6).

**Callable interface for a hook** (`main()` dispatch, lines 525-556):

| Invocation | Lines | Behaviour | Exit |
|---|---|---|---|
| `identify` | 530-537 | `pid = os.getpid()` (line 532) | 0 |
| `identify PID` | 530-537 | `pid = int(args[1])`; non-numeric -> `{"status": "unknown"}` (line 534) | 0 |
| `identify 1 2` (wrong arity) | 556, 561-564 | stderr `launch job: invalid invocation or unavailable private state` | 2 |
| any call with `uv` absent from `PATH` (except no-arg/`hook` adapter mode) | 25, 52-53 | stderr `launch job: UV is required for this invocation`, no stdout | 2 |

Output is one JSON line from `json.dumps(result)` with **default separators** (line 536), for example `{"status": "governed", "session_id": "<id>"}`; a hook must parse JSON, not compare compact text. The early `exit 0` for a missing store (lines 20-24) applies only to the no-argument/`hook` adapter mode, never to `identify` (01 §1).

**Selection data flow** (`identify(pid)`, lines 215-248):

```
git push
  -> pre-push hook (same kernel session; git does not setsid, 01 §7, 04 E1)
     -> launch-job-identity.sh identify          (no PID)
        -> uv (stays as parent, no setsid; 01 §7)
           -> python: pid = os.getpid()          (line 532)
              -> proc(pid): /proc/<pid>/stat field 6 = kernel session id  (lines 202-207, 219)
              -> HOME store: ~/.claude/state/launch-level/jobs/<sid>.json (lines 102-122, 220-223)
                   missing at any level -> {"status":"ordinary"}           (line 225)
              -> validate record: keys, pid == kernel_sid == sid,          (lines 227-237)
                 live supervisor (not zombie, same start ticks, same boot_id), same uid
                   any failure -> {"status":"unknown"}                     (lines 243-244)
              -> governed(root, session_id): sessions/<session_id> is      (lines 177-186, 239)
                 worktree | full | full-submit
                   missing -> {"status":"ordinary","reason":"released"}    (lines 240-241)
                   bad content -> unknown
              -> {"status":"governed","session_id":S}                      (line 242)
```

**Selection is by kernel session membership only.** Only field 6 (session) of `/proc/<pid>/stat` is used; the PPID chain is never read and there is no ancestry walk anywhere in the file (line 253) [CODE-VERIFIED]. `members()` (lines 251-265) is used only by the supervisor, not by `identify`. The supervisor creates the job's session with `os.setsid()` (line 292) and publishes `jobs/<sid>.json` for its own sid (line 301).

**Observed with real git** (01 §7; governed pushes via the real `prepare` + `run` path; local bare remote only):

| Case | Hook sid == git sid == supervisor sid? | `identify` / `identify $$` / `identify $PPID` | exit |
|---|---|---|---|
| ordinary terminal, no job | same as caller shell | ordinary x3 | 0 |
| governed `git push origin HEAD:refs/heads/main` | yes | governed sidA x3 | 0 |
| `setsid -w git push ...` | new session (git is leader) | **ordinary x3** | 0 |
| `HOME=<other valid dir> git push ...` | yes | **ordinary x3** | 0 |
| `env -u HOME git push ...` / `HOME=relative/x` | yes | unknown x3 | 0 |
| `PATH=/usr/bin:/bin git push ...` (no uv) | yes | **no verdict**, stderr `UV is required` | 2 |
| `sh -c 'git push ...' & wait` (background child) | yes | governed sidA x3 | 0 |
| `rm sessions/sidA` then push | yes | ordinary, reason released, x3 | 0 |
| `printf bogus > sessions/sidA` then push | yes | unknown x3 | 0 |

uv keeps Python as a child (it does not exec into Python) and does not call `setsid`, so `identify` with no PID resolves the hook's session; `identify`, `identify $$` and `identify $PPID` agreed in every case (01 §7).

**HOME handling** (`store()`, lines 102-122): HOME unset, empty or relative -> `ValueError('invalid home')` -> unknown; `/` or a `//`, `.` or `..` component -> unknown; absolute but non-existent -> ordinary; a symlinked component -> unknown; HOME foreign-owned or group/other-writable (`0o022`, line 109) -> unknown; missing `.claude`, `state`, `launch-level`, `jobs/` or `jobs/<sid>.json` -> ordinary (01 §2). `identify` never creates state (`subdir(..., create=False)`, line 222).

**Verdict meaning under the owner's decision** (01 §4; decision DECIDED 2026-11-08, seed brief line 73):

| Verdict | Protected push | Other pushes |
|---|---|---|
| `governed` | refuse whole push, nonzero, diagnostic | allow |
| `ordinary` / `ordinary` + `released` | allow | allow (no stream inspection, design §19.3) |
| `unknown` | refuse, own diagnostic | allow |
| no verdict (non-zero exit, empty or unparseable stdout) | not mapped by code; 01 §4 item 3 says the hook must treat it as `unknown` | — |

**Limits found in the selector** (01 §2, §3, §4, §7):

| Limit | Effect on a protected push | Evidence |
|---|---|---|
| `setsid` anywhere between the supervisor and the identified PID | governed job selected `ordinary` -> allowed | lines 7-8, 219-225; observed |
| Different but valid absolute `HOME` for the push | governed job selected `ordinary` -> allowed (not listed in the seed brief or design) | lines 103-106, 224-225; observed |
| `uv` not on `PATH` | exit 2, no verdict, for agents **and humans** (the no-store early exit does not cover `identify`) | lines 20-25, 52-53; observed (01 §7); 04 E28c |
| Killed supervisor (`kill -9`) | `identify` -> unknown; record `jobs/<sid>.json` left behind forever (cleanup `finally` at lines 341-359 not run) | observed (01 §7) |
| Stale record + later PID reuse by a human session leader | human `identify` -> unknown -> human push to main/master refused | inferred from line 234, not reproduced (01 §7) |
| HOME unset/relative, group-writable home, `sudo` (different uid) | unknown -> protected push refused for humans too | lines 104-110, 236; observed for unset/relative |

Untested: PID-namespace sandboxes and containers (boot_id) [UNVERIFIED], non-dumpable/setuid Python [UNVERIFIED] (01 §5).

**`publish()` (lines 164-174)** is `openat(O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW, 0600)` on a hidden `.<uuid hex>` name, buffered write of compact JSON, `fchmod 0400`, `linkat` (fails with `EEXIST`, never replaces), then `unlinkat` of the temp name; no `fsync` (01 §6). It cannot install a hook unchanged: the payload is JSON-encoded (line 169) and the mode `0400` is not executable (line 171). The no-replace pattern can be copied with raw bytes and an executable mode (01 §6).

**Copies.** `plugins/superclaude/hooks/scripts/launch-job-identity.sh` and the installed `~/.claude/hooks/launch-job-identity.sh` (mode 0755) are byte-identical to the source (`cmp`, 2026-11-08) (01 §8; D19-58 [CODE-VERIFIED]).

**Wording drift (not behaviour).** Header line 4 says `run` waits for "descendants"; the code waits for non-zombie members of the kernel session (lines 263, 332, 338) [CODE-CONTRADICTED, wording only] (01 Gaps 9). Design line 557 omits that HOME problems alone produce `unknown` (01 Gaps 10).

### 2.3 L2 status probe and `W-L2-ABSENT` (`orca_worktree.py`)

Source: `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`, read by 03 (§2, §3), with `l2_status` also called for real against disposable `/tmp` repositories (git 2.47.3; removed afterwards).

**`l2_status(wt)` (lines 1012-1029).** One subprocess, no shell: `git -C <wt> rev-parse --git-path hooks/pre-push` (line 1020) through `run()` (lines 123-147), which never raises (timeout -> `timed_out`; `FileNotFoundError`/`PermissionError`/`OSError` -> `missing`; line 97 `ok` = rc 0 and neither flag).

```
cmd_launch (lines 1253-1388)
  already-launched check (1262-1278)
  stale-prompt check (1279-1281)
  IR-4 enforcement_preflight (1287-1304) --fail--> refuse, W-ENFORCEMENT-ABSENT, no agent
  l2 = l2_status(wt) (1311)
       git -C wt rev-parse --git-path hooks/pre-push  (1020)
       failed or empty -> "absent"                     (1022-1023)
       hook = Path(wt) / out                           (1024; absolute answer kept as is)
       is_file() and os.access(hook, X_OK) -> "present-unverified" else "absent"  (1025-1029)
  l2_notes = [W-L2-ABSENT] if l2 == "absent"           (1312)
  publish_pending (1315)
  orca agent launch ... "[sc-launch:v1:<nonce>] ..."   (1330-1334)   <-- agent starts regardless of l2
  ccsession screen check (1356-1365); record_launch (1368)
  session_report(wt, l2, inode) (1376)  -> "L2 pre-push:" layer line (1061-1067)
  launch_result("launched", notes + l2_notes, ...) (1377-1385)
```

**Observed results of the real `l2_status`** (03 §2):

| Case | Result |
|---|---|
| no `pre-push` file | `absent` |
| `pre-push` mode 0644 | `absent` |
| `pre-push` mode 0755 | `present-unverified` (main checkout and its linked worktree alike: they share the common dir) |
| `core.hooksPath` set with an executable hook there | `present-unverified`; an executable hook at the default path is then ignored |
| `pre-push` is a directory | `absent` |
| not a git repository | `absent` |
| `git` not on PATH | `absent` |

| Repo shape | `rev-parse --git-path hooks/pre-push` answer (git 2.47.3) |
|---|---|
| main checkout, default lookup | `.git/hooks/pre-push` (relative) |
| linked worktree | absolute path in the common git dir |
| `core.hooksPath=myhooks` | `myhooks/pre-push` (relative) |
| this worktree (`issue-441`) | `/home/coder/workspaces/IronClaude/.git/hooks/pre-push`, which does not exist today -> `absent` |

**What `l2_status` does not check.** It reads no file content, owner, version line or ownership marker and does not run the hook; any executable at git's hook path, including a foreign hook, gives `present-unverified` (docstring lines 1013-1019; call-site comment lines 1307-1308). It folds "git missing", "timeout" and "not a repository" into `absent`. A symlink named `pre-push` is followed by `is_file()` (03 §2). The test `test_ir6_l2_status_follows_the_git_hook_path` (`tests/skills/test_issue_orca_worktree.py:1686-1729`) pins five cases and asserts the hook file is never modified.

**`W-L2-ABSENT` today.** Remedy text (lines 789-792): "the L2 layer is not built yet and the limits are enforced by the L1 guard only; the agent was started". Why text `L2_ABSENT_WHY` (lines 796-799): "the worktree has no executable pre-push hook at git's hook path, so no L2 pre-push layer checks this session's pushes". It fires only when `l2 == "absent"` (line 1312), never changes the outcome (status stays `launched`), and when a ccsession warning is also present it appears only in `detail`, because `launch_result` (lines 1203-1220) puts the first note in `warning` (pinned at `tests/skills/test_issue_orca_worktree.py:1554`). The in-code comment at lines 1309-1310 gives the one-line change that would make it the design's refusal: `if l2_notes: return emit(launch_result("failed", l2_notes, enforcement_hook=hook))`.

**Design vs code** (03 §5):

| Design statement | Tag | What the code does |
|---|---|---|
| IR-7 (line 355) and §19.2 line 514: refuse a governed launch when accepted L2 is absent (D19-18) | [CODE-CONTRADICTED], deliberate | warns and launches (lines 794-795, 1311-1312, 1315-1388); design §19.8 line 574 records the warning choice "the owner had not answered" |
| §19.2 line 514: on conflict or unsupported lookup, preserve files and report `W-L2-ABSENT` with the reason (D19-16) | [CODE-CONTRADICTED] | a foreign executable hook gives `present-unverified` and **no** warning (test rows at `tests/skills/test_issue_orca_worktree.py:1691, 1727`); one fixed reason; unsupported lookup never detected |
| §19.2 line 510: resolve hook paths through git, never assume `.git` is a directory (D19-11) | [CODE-VERIFIED], read side only | line 1020 |
| §19.2 line 512: publish without replacing, recheck owned version/content, header alone not ownership proof (D19-14) | [UNVERIFIED] — no installer exists | `l2_status` checks no ownership |
| Ordinary/no-pipeline claims unaffected (D19-19) | [CODE-VERIFIED] | sole call site is inside `cmd_launch` (line 1311) |

### 2.4 Hook installer (`install_hooks.py`)

Source: `src/superclaude/cli/install_hooks.py` (612 lines), read in full by 03 §4. Public entry `install_hooks(target_path=None, force=False)` (lines 153-243).

| What it installs | Where | Lines |
|---|---|---|
| Hook scripts in `_FRESHNESS_SCRIPTS` (lines 42-94, includes `launch-job-identity.sh` line 90 and `launch-level-guard.sh` line 93) plus `_LEGACY_SCRIPTS` | `hooks_dir = target_path.parent / "hooks"` (line 173), i.e. `~/.claude/hooks/`; `shutil.copy2` then `chmod 0o755` (lines 284-285); existing file skipped unless `force` (lines 279-281) | 251-290 |
| Claude Code `settings.json` registrations from `src/superclaude/hooks/hooks.json` | `~/.claude/settings.json`, timestamped backup, atomic write; ownership by exact command string (`_owns_command` lines 123-129, `_owns_registration` lines 132-139) | 298-523 |
| Seed file `auggie-projects.txt.example` | `~/.claude/auggie-projects.txt`, only when absent | 556-587 |

**No git-hook code path.** Every write target derives from `target_path` and its parent (lines 173, 228, 335-337, 477). The file never runs `git`, never imports `subprocess`, never reads or writes `.git/hooks`, `core.hooksPath` or `extensions.worktreeConfig`. A Grep of `src/` for `hooksPath|worktreeConfig|pre-push|prepush` finds no installer; the only L2-related hits are `orca_worktree.py` (`l2_status`, `W-L2-ABSENT`) and the issue skill docs [CODE-VERIFIED as absent] (03 §4; D19-71, D19-81).

**Fit for an L2 installer.** `install_hooks.py` is user-global (`~/.claude`), while a git pre-push hook is per repository (common git dir or `core.hooksPath`). Design line 565 places installation in "a future claim launcher", i.e. next to `cmd_launch` in `orca_worktree.py`, between the IR-4 preflight (line 1287) and the `l2_status` probe (line 1311). A hook body could still live in `src/superclaude/hooks/scripts/` and ship through `_FRESHNESS_SCRIPTS`, because `make verify-sync` requires every script there to be listed (comment lines 62-64) (03 §4).

**The only real-git pre-push code in the repository is a test policy:** `LocalPushFixture` in `tests/hooks/test_launch_job_identity.py:1175-1232`, self-labelled "Disposable TEST POLICY, not the production O-22 pre-push installation". It writes `.git/hooks/pre-push` directly, compares field 3 exactly (line 1205), reads the stream for every actor (line 1203) and would crash with a `ValueError` on a malformed record (line 1204) (03 §5 D19-21, D19-23, D19-26, D19-40).

### 2.5 Observed git 2.47.3 pre-push behaviour

Source: file 04 only. Every row is recorded `/tmp` output from two disposable sandboxes (`/tmp/prepush-research.ERbSguv9`, then `/tmp/prepush-followup.0OZWoyIi`), each with a local bare repository as the only remote, both removed afterwards (04 "Sandbox removal", "Follow-up sandbox removal"). Only **git 2.47.3** was run (E0, F0); all pushes used the local file transport. Tags in this subsection are file 04's.

```
 git push (from main checkout or linked worktree)
   |
   +-- refs already up to date / locally known non-ff / stale lease --> dropped from stdin (E12, E23b, E9, E27a)
   |
   v
 hook lookup: $(git rev-parse --git-path hooks/pre-push)
   default            -> <common git dir>/hooks/pre-push   (E1, E18, E30a/b)
   core.hooksPath     -> <that dir>/pre-push (relative = per worktree root) (E16b, E30c/d)
   worktreeConfig     -> per-worktree override             (E31)
   not executable     -> skipped, hint only, push proceeds (E29)
   |
   v
 pre-push <remote-name-or-URL> <URL>   cwd = top of pushing checkout
   stdin: <local-ref> <local-oid> <remote-ref> <remote-oid>   (0..n lines, order undocumented, seen both ways)
   |
   +-- exit != 0 --> whole push aborted, no ref moves (E19, E24, E26a, E27b, F1)
   +-- exit 0    --> git sends; remote may still reject (E3b, E23a)
```

#### (a) Arguments and stdin records

| Behaviour | Evidence |
|---|---|
| argv1 = remote name (`origin`), argv2 = URL | E1, E18 |
| argv1 = the URL itself when pushing to a URL with no remote name | E11 (`--mirror` to `remote2.git`) |
| One `<local-ref> <local-oid> <remote-ref> <remote-oid>` line per ref; one invocation per push, also for several refspecs | E1, E7 |
| Create: field 4 is the zero oid | E1, E25 (`refs/heads/master` create) |
| Delete (`:ref` and `--delete`): field 1 literal `(delete)`, field 2 zero oid | E3a, E3b, E4a, E4b, E8, F1b |
| Forced update (`+src:main`, `--force`, matching `--force-with-lease`): an ordinary record, **no force marker** | E5a, E5b, E27b |
| `HEAD:main`: field 1 is literal `HEAD`; field 3 `refs/heads/main` | E6 |
| Field 3 is the fully qualified destination even when the command never names it: `remote.origin.push=feature:main` with bare `git push origin`; upstream mapping with `push.default=upstream` | E20, E21 |
| `--mirror` sends heads, remote-tracking refs and tags; only `refs/heads/main` has field 3 equal to the protected name | E11 |
| Look-alikes arrive as distinct, case-preserved field 3 values: `refs/heads/mainline`, `refs/heads/feature/main`, `refs/heads/main2`, `refs/tags/main`, `refs/heads/Main`, `refs/heads/ma` | E25, F3a |
| SHA-256 repository: every oid, including the zero oid, is 64 hex characters; record shape and `(delete)` unchanged | E22 |
| Stdin record order is undocumented and was observed both ways: command-line order in E7 and web-01 G3 (one `--dry-run` run of creates); not command-line order in E9, E19 and E24a/b (E24: two runs with the protected ref last and first gave the same stream, existing remote ref first). The hook must scan every record and must not depend on order | E7, E9, E19, E24a/b; web-01 G3, Area I |
| Empty stdin with the hook still running: up-to-date push (also `HEAD:main`), locally known non-fast-forward, stale lease | E12, E12b, E23b, E27a |
| A "fetch first" non-fast-forward (remote object not known locally) **does** deliver its `refs/heads/main` record; git rejects it after the hook | E23a |
| `--all` with a behind local `main`: `main` filtered before the hook; other refs updated | E9 |
| Destinations with a space, trailing space or tab die with `fatal: invalid refspec` (exit 128) before the hook; no run produced a malformed record | F3b, F3c |
| `--dry-run` runs the hook with the real would-be records (including a forced `refs/heads/main`) and moves no refs | E13, E13b, E28 |
| One nonzero exit aborts the whole push (no per-ref status lines; git prints hook stderr then `error: failed to push some refs`), for create, forced, fast-forward and delete forms mixed with unprotected refs, `--atomic` or not | E19, E24a/b, E26a, E27b, F1a, F1b |
| Hook exit 0 with `--atomic` applies both updates | E26b |
| A remote-side refusal can still stop a push the hook allowed (`receive.denyDeleteCurrent`) | E3b |

#### (b) Bypass paths (hook not run, push succeeds)

| Path | Result | Evidence |
|---|---|---|
| `git push --no-verify` | hook not run; ref created | E14 |
| `-c core.hooksPath=/dev/null` or a directory without `pre-push` | no hook, no warning | E15, E16a |
| `-c core.hooksPath=<dir with pre-push>` | only that hook runs; installed common-dir hook skipped | E16b |
| `git send-pack` | never runs pre-push; E17c force-rewrote `refs/heads/main` with no hook call | E17a-c |
| Non-executable `pre-push` | skipped (fail-open) with a two-line `hint:`; `-c advice.ignoredHook=false` silences the hint; a real push went through | E29a-c |
| `extensions.worktreeConfig=true` plus `git config --worktree core.hooksPath` | redirects only that worktree's hook; main checkout keeps the common-dir hook | E31a/b |
| Hosting-service API / programmatic ref writes; libraries (pygit2/libgit2, dulwich, GitPython, JGit) | not testable locally [UNVERIFIED], routed to web-01 | 04 Gaps, Step 2.5 D19-30 (API part) |

#### (c) Hook lookup in linked worktrees

| Behaviour | Evidence |
|---|---|
| A linked worktree's default `hooks/pre-push` resolves to the **common** git dir (`clone/.git/hooks/pre-push`) | E0, E1, E30a |
| A hook in the worktree-private git dir (`clone/.git/worktrees/wt/hooks/pre-push`) is ignored | E30b |
| `--git-path hooks/pre-push` prints a relative path (`.git/hooks/pre-push`) in the main checkout and an absolute one in a linked worktree; `--path-format=absolute` not exercised [UNVERIFIED] | E30a |
| From the main checkout `$0` is relative and `GIT_DIR` is not exported; from a linked worktree `$0` is absolute and `GIT_DIR` = worktree-private dir; cwd = top of the pushing checkout | E18 |
| Absolute `core.hooksPath` honoured exactly; relative `core.hooksPath` resolves against each pushing worktree's root (a different, in-tree hook per worktree) | E30c, E30d |
| Plain `git worktree remove` deletes the private git dir (a marker file included); the shared hook stays and still runs for the remaining worktree (Orca removal not tested) | F2 |

#### (d) Environment and process ancestry seen by the hook

| Behaviour | Evidence |
|---|---|
| git adds only `GIT_DIR` (linked worktree), `GIT_EXEC_PATH=/usr/lib/git-core`, empty `GIT_PREFIX`, and prepends `/usr/lib/git-core` to PATH | E1, E18, E28 |
| Everything else is the pusher's: HOME as given or unset, arbitrary marker variables, `CLAUDECODE`, `CCSESSION_LAUNCH_ID`, `CLAUDE_PID`, `CLAUDE_CODE_SESSION_ID`, `ORCA_*`, harness `GIT_CONFIG_*` | E1, E28a, E28b |
| With `PATH=/usr/bin:/bin`, `uv` is not resolvable in the hook (`UV-ABSENT`) | E28c |
| Ancestor chain `pre-push -> git -> timeout -> x.sh -> bash -> claude`; the hook's session id equalled the Bash tool shell's session (303569), while `claude` ran in a different session (3624918) | E1 |

#### (e) Executable bit (no-replace publication not tested by git)

| Behaviour | Evidence |
|---|---|
| Removing only the executable bit makes git skip the hook, exit 0 and push; the hint can be suppressed per command | E29 |
| File 04 did not exercise an O_EXCL/`linkat` no-replace publication; that part of sub-question (e) rests on 01 §8 and 03 (Sections 2.2 and 2.4 above) | 04 scope |

#### (f) Versions

| Behaviour | Evidence |
|---|---|
| Only git 2.47.3 was run, over the local file transport; SSH/HTTPS hook timing and filtering not tested [UNVERIFIED] | E0, F0, 04 Gaps |
| Local pre-push restricts only pushes: a local commit and a no-ff merge into local `main` succeeded with a refusing hook, which never ran | F4 |

#### Design claims checked against these runs (04 Step 2.5)

| D19 ID | Design line | Result |
|---|---|---|
| D19-2, D19-20, D19-22, D19-23, D19-25, D19-28, D19-41, D19-48 | 493-534 | [CODE-VERIFIED] (record shape, zero oids, empty stream, SHA-256, field 3 authoritative, dry-run) |
| D19-21 | 518 | [CODE-VERIFIED]: one nonzero exit refuses create, update, delete and force (F1 filled update and delete) |
| D19-27 (git part), D19-42 | 520, 530 | [CODE-VERIFIED] within the tested scope (F3); "never in any version or transport" not provable locally |
| D19-29 (git part) | 520 | [CODE-VERIFIED] (F4) |
| D19-30 (local forms) | 520 | [CODE-VERIFIED] (E14-E17) |
| D19-30 (API part) | 520 | Documented externally (web-01 H/J); not confirmed at runtime |
| D19-33, D19-35 | 524 | [CODE-VERIFIED] for plain `git worktree remove` (F2) |
| D19-47 | 534 | [CODE-CONTRADICTED] in part: a "fetch first" non-ff reaches pre-push with its record (E23a); the design sentence is incomplete rather than wrong |

**Corrections to file 04's own text.** (1) 04's Gaps list still marks `refs/heads/ma` and worktree removal [UNVERIFIED]; both were later settled by F3a and F2 (04 Gaps notes this itself, and the Step 2.5 table is the stronger record). (2) The E28 uv bullet cites "a nonzero exit refuses (E9-E11)"; the refusal experiment is E19 (gaps-and-questions N21/M4). (3) The E31 paragraph names "E7/E8 (per-process `-c core.hooksPath`)"; the per-process override experiments are E15/E16. (4) The uv remedy is the corrected one: an absolute uv path alone is not enough, because `launch-job-identity.sh` resolves uv through PATH at lines 25 and 566 (04 E28 correction; gaps-and-questions N-3).

### 2.6 Current State Summary

| Component | Exists today | What it does for a push to `main`/`master` | Strongest evidence | Main limit |
|---|---|---|---|---|
| L1 text guard (`launch-level-guard.sh`) | yes | refuses literal non-canonical pushes and canonical pushes to `main`/`master`; refuses `--no-verify`, `-c core.hooksPath`, `send-pack`, `http-push`, `gh api` writes | source read, 02 | text only: underscore env prefix plus obfuscated subcommand or alias passes [CODE-CONTRADICTED vs line 80]; no `.git/hooks` tamper token (line 706); smart-HTTP `curl` to `git-receive-pack`, library and script pushes pass |
| Job-identity selector (`launch-job-identity.sh identify`) | yes | answers governed / ordinary / ordinary+released / unknown by kernel session (stat field 6), no ancestry walk | source read plus real-git runs, 01 §7 | `setsid` or a different valid HOME turns a governed push `ordinary`; PATH without uv gives exit 2 (no verdict -> `unknown`, so main/master refused under the owner decision) |
| `publish()` no-replace pattern | yes (for JSON job records) | none for hooks | 01 §6 | JSON payload and mode 0400; pattern reusable only with raw bytes and an executable mode |
| `l2_status` probe (`orca_worktree.py:1012-1029`) | yes | reports `absent` / `present-unverified` from git's hook path and the X bit | source read plus real calls, 03 §2 | no ownership or content check; foreign hook passes silently |
| `W-L2-ABSENT` | yes, as a warning | none: launch proceeds | 03 §3 | design IR-7 refusal is [CODE-CONTRADICTED] by deliberate choice; one-line change at lines 1309-1310 |
| L2 pre-push hook body | **no** | none | Grep of `src/`, 03 §4 | nothing to run |
| L2 hook installer / doctor | **no** | none | `install_hooks.py` has no git-hook path, 03 §4 | user-global installer is the wrong scope; design puts install in the claim launcher |
| git 2.47.3 pre-push itself | yes (platform) | field 3 is authoritative; one nonzero exit aborts the whole push; empty stdin is real | 04 E1-E31, F1-F4 | silently bypassed by `--no-verify`, per-process or per-worktree `core.hooksPath`, `send-pack`, a cleared X bit; inherits the pusher's whole environment |

```
 agent command text --> [L1 guard] --refuse--> blocked
                          | allow (text it cannot read: alias, $'\x70ush', curl receive-pack, library)
                          v
                     git push --> [pre-push hook at git-path]   <-- does not exist today
                          |            (l2_status sees only "is there an executable file")
                          v
                     remote (no server-side protection in scope)
```

**Net position.** Today a push to `refs/heads/main` or `refs/heads/master` by a governed agent is stopped only by L1 text classification. No L2 hook body or installer exists in the source tree (03 §4); the one real checkout probed, this worktree, resolves to `/home/coder/workspaces/IronClaude/.git/hooks/pre-push`, which does not exist (03 §2); and `cmd_launch` warns rather than refuses. Even a built L2 is a same-user client-side control that the agent can bypass without any git error (04 E14-E17, E29, E31) unless L1 refuses those forms and something checks install integrity before each governed launch. Research files 02 (Summary) and 01 (Summary) therefore point the design at three additions: treat L1 as advisory and add a `.git/hooks` tamper token at line 706; verify ownership by full-content comparison of the file git will actually run (plus type, owner, mode and a self-test), which `l2_status` does not do; and rely on server-side protection for `refs/heads/main` and `refs/heads/master`. Server-side protection itself is out of scope for this report (Section 1.5).

**Contradictions surfaced in Section 2** (observed output or code outranks design text):

| Item | Design / doc says | Code or observation shows | Where |
|---|---|---|---|
| IR-7 / D19-18 | refuse a governed launch when L2 is absent (design lines 355, 514) | warns and launches (ow:1311-1312) | 2.3 |
| D19-16 | conflict or unsupported lookup reported as `W-L2-ABSENT` with reason | foreign executable hook gives `present-unverified`, no warning | 2.3 |
| LL-UNKNOWN Why text (L1 line 80) | "a renamed command or an alias cannot commit, push or merge" | an underscore env prefix moves command position off `git` (line 435), so an alias or obfuscated subcommand passes | 2.1 |
| LL-TAMPER Blocked text (L1 line 95) | writes to "a git configuration file" are blocked | only contiguous-path spellings are covered (line 706); partial contradiction. Separately, `.git/hooks` has no token at all | 2.1 |
| D19-47 (design line 534) | non-fast-forward rejected before pre-push | "fetch first" non-ff reaches pre-push with its record (04 E23a) | 2.5 |
| `launch-job-identity.sh` header line 4 | waits for "descendants" | waits for non-zombie kernel-session members (wording only) | 2.2 |

**Items for Open Questions (Section 9)** — [UNVERIFIED] in the research and excluded from the architecture above:

| # | Question | Source |
|---|---|---|
| 1 | Do hosting-service API writes and git libraries (pygit2/libgit2, dulwich, GitPython, JGit) run, or bypass, client-side pre-push? Status: documented externally (web-01 H/J); not confirmed at runtime. Per the documentation, `send-pack`, smart-HTTP `git-receive-pack`, libgit2/pygit2, dulwich, isomorphic-git, the GitHub REST refs API and `gh api` do not run it; JGit and GitPython do (web-01 J10). Remaining action: runtime confirmation | 04 Gaps (ROUTE web-01), D19-30 API part; 02 Gap 6; web-01 H1-H3, J1-J11 |
| 2 | Does behaviour hold on other git versions and on SSH/HTTPS transports (hook timing, "fetch first" vs non-ff filtering)? | 04 Gaps; GQ G-3, G-27 |
| 3 | Does `git rev-parse --path-format=absolute --git-path hooks/pre-push` give an absolute path in the main checkout? | 04 E30, Gaps |
| 4 | Would `refs/heads/Main` collide with `main` on a case-insensitive remote or hosting service? | 04 E25, Gaps |
| 5 | Is there any stdin order rule? Order is undocumented and was observed both ways (command-line order in 04 E7 and web-01 G3; existing remote refs first in 04 E9, E19, E24). Not needed, because the guard scans every record and does not depend on order. | 04 E7, E9, E19, E24, Gaps; web-01 G3 |
| 6 | Does Orca's worktree removal behave like plain `git worktree remove` (private dir gone, shared hook kept)? | 04 F2 |
| 7 | Does the install-integrity check (executable bit, effective `core.hooksPath` per worktree, ownership) run only at install or before every governed launch? | 04 Gaps open question (E29, E31) |
| 8 | Should the L2 hook be pure shell, or set a fixed PATH holding the install-time uv directory, given `launch-job-identity.sh` resolves uv through PATH (lines 25, 566)? | 04 E28c correction; 01 §4 item 5 |
| 9 | The design's no-replace publication, ownership recheck and conflict reporting (D19-14) have no code; the `20261106-l2-prepush-decisions/` artifacts that back §19.6 are absent | 03 §1, §5, Summary |

**Key-finding coverage check** (Summary and Key Takeaways of each research file, read before finalizing):

| Research file | Key finding | Where reflected |
|---|---|---|
| 01 Summary | selection by kernel session only, no PPID walk; hook can call `identify` with no PID | 2.2 |
| 01 Summary | missing state -> `ordinary`; validation failure or bad HOME -> `unknown`; `setsid` / other HOME -> `ordinary`; no-uv exit 2 -> `unknown` policy | 2.2, 2.6 |
| 01 Summary | `publish()` is no-replace but JSON and 0400; ownership needs full-content comparison, type, owner, mode, self-test | 2.2, 2.6 |
| 02 Summary | canonical-form rule and protected-destination rule; refused bypass list | 2.1 |
| 02 Summary | no `.git/hooks` token; `curl` receive-pack, library, script pushes and config without a git word pass; underscore prefix plus obfuscated subcommand passes | 2.1, 2.6 |
| 02 Summary | treat L1 as advisory, add tamper token, rely on server-side protection | 2.6 (server-side protection itself out of scope, 1.5) |
| 03 Summary | 83 statements; L2 does not exist; `install_hooks.py` has no git-hook path | 1.2, 2.4 |
| 03 Summary | `l2_status` behaviour; `W-L2-ABSENT` non-blocking, contradicting design lines 355 and 514 | 2.3 |
| 03 Summary | §19.6 artifacts absent; line-487 corpus present but backs no section-19 row | 1.2 (absence), Open Question 9; the line-487 corpus detail is excluded from Section 2 because it describes documentation provenance, not current code |
| 03 Summary | 14 git-behaviour claims sent to the experiment cross-check | 2.5 (design claims table) |
| 04 Key Takeaways / Summary | field 3 authoritative; empty stdin real; one nonzero exit aborts all; dry-run runs the hook; bypass set; common-dir placement; environment pass-through; uv PATH gap; push-only restriction | 2.5 (a)-(f), 2.6 |
| 04 Step 2.5 | 15 confirmed, D19-47 contradicted in part, D19-30 API part to web-01 | 2.5 design claims table, contradictions table |

No research Key Takeaway or Summary finding is omitted; the only exclusion is the 03 line-487 historical corpus detail, for the reason given in the table.

