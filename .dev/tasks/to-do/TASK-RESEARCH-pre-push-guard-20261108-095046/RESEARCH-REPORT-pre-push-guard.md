# Technical Research Report: git pre-push hook semantics for the L2 launch-level guard

**Date:** 2026-11-08
**Depth:** Standard
**Research files:** 4 codebase + 2 web research
**Scope:** src/superclaude/hooks/scripts/launch-level-guard.sh, src/superclaude/hooks/scripts/launch-job-identity.sh, docs/designs/sc-issue-launch-level-hook.md section 19, src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py, src/superclaude/cli/install_hooks.py, installed git 2.47.3 (sandbox experiments), official git docs and Linux man pages

---

## Table of Contents

1. [Problem Statement](#1-problem-statement) (1.1-1.5)
2. [Current State Analysis](#2-current-state-analysis) (2.1 L1 text guard, 2.2 identity selector, 2.3 L2 status probe, 2.4 hook installer, 2.5 observed git 2.47.3 behaviour, 2.6 summary)
3. [Target State](#3-target-state) (3.1-3.6)
4. [Gap Analysis](#4-gap-analysis) (4.1 G-1 to G-45, 4.2 bypasses, 4.3 L1 verdicts, 4.4 contradicted and stale findings, 4.5 cross-file contradictions)
5. [External Research Findings](#5-external-research-findings) (5.1 git docs, 5.2 Linux primitives, 5.3 version table, 5.4 recommendations, 5.5 summary)
6. [Options Analysis](#6-options-analysis) (6.1 Option A, 6.2 Option B, 6.3 Option C, 6.4 publication, 6.5 identity, 6.6 comparison)
7. [Recommendation](#7-recommendation)
8. [Implementation Plan](#8-implementation-plan) (8.1-8.7 Phases 1-7, 8.8-8.9 gap mapping, 8.10 integration checklist)
9. [Open Questions](#9-open-questions) (9.1 decisions, 9.2 unverified claims, 9.3 resolved items, 9.4 contradictions)
10. [Evidence Trail](#10-evidence-trail) (10.1 codebase research, 10.2 web research, 10.3 synthesis, 10.4 QA, 10.5 task files and gaps log)

---

**Source key used throughout.** Research files are cited by number: 01 = `research/01-identity-selector-ancestry.md`, 02 = `research/02-l1-guard-push-bypass-coverage.md`, 03 = `research/03-design-and-claim-code-crossvalidation.md`, 04 = `research/04-empirical-git-prepush-experiments.md`, web-01 = `research/web-01-git-official-docs-and-versions.md`, web-02 = `research/web-02-linux-atomic-publication-and-exec-bit.md`, GQ = `gaps-and-questions.md`. `ow:` = `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`. "Design" = `docs/designs/sc-issue-launch-level-hook.md`. Paths are relative to the worktree root.

**Tags.** [CODE-VERIFIED] = confirmed in this repo's code or observed with real git 2.47.3 in a `/tmp` sandbox (file 04 uses the tag for observed git behaviour). [CODE-CONTRADICTED] = code or observation disagrees with the claim. [STALE DOC] = a document disagrees with the code. [UNVERIFIED] = nothing confirmed it. [EXTERNAL] = web research, with source URL. [OBSERVED 2.47.3] = file 04 or a web-file sandbox run on the installed git. Git behaviour is reported only as observed with git 2.47.3; it is not a claim about other git versions.

---

## 1. Problem Statement

### 1.1 The research question

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
| L1 | A Claude Code PreToolUse/UserPromptSubmit text guard, `src/superclaude/hooks/scripts/launch-level-guard.sh`, that classifies the command text of a governed session's tool calls | Built. It refuses canonical pushes to `main`/`master` (LL-PROTECTED) and the non-canonical push spellings it recognises (LL-PUSH-FORM) (02 §5, guard lines 659-669, 731-732); known misses: underscore env prefix with an obfuscated subcommand, smart-HTTP `curl`, library and script pushes (see §2.1) |
| L2 | A git `pre-push` hook that sees the real ref-update records git is about to send, and refuses the push when a governed agent is the pusher and a record's destination is `refs/heads/main` or `refs/heads/master` | Not built. No source file installs, owns or verifies a git `pre-push` hook (03 §4, D19-8, D19-71, D19-81 [CODE-VERIFIED as absent]) |

L2 is needed because L1 reads only command text. By its own in-code admission it is a text-only shortcut ("variables and quoting tricks still pass, so the real fix is the L2 layer", guard lines 710-711, 02 §6), and the static reading in 02 found push spellings and configuration writes that pass it (02 §9; detailed in Section 2.1).

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

| In scope | Out of scope |
|---|---|
| Git pre-push semantics as observed with git 2.47.3; the existing L1 guard; the job-identity selector; the `l2_status` probe; the Claude Code hook installer | Server-side branch protection on the hosting service; behaviour of other git versions or network transports (not tested; see GQ G-3, G-27); runtime behaviour of git libraries (pygit2, dulwich, GitPython, JGit), which was routed to web research (GQ G-2; Section 5) |

---

## 2. Current State Analysis

**Evidence rule.** This section states as current architecture only facts traced to a source-code read (with file:line) or to recorded `/tmp` command output (with the experiment id). Design-document statements are carried only with their verification tag.

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
| no verdict (non-zero exit, empty or unparseable stdout) | not mapped by code; 01 §4 item 3 says the hook must treat it as `unknown` | allow |

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

**`W-L2-ABSENT` today.** Remedy text (lines 789-792): "the L2 layer is not built yet and the limits are enforced by the L1 guard only; the agent was started". Why text `L2_ABSENT_WHY` (lines 796-799): "the worktree has no executable pre-push hook at git's hook path, so no L2 pre-push layer checks this session's pushes". It fires only when `l2 == "absent"` (line 1312), never changes the outcome (status stays `launched`), and when a ccsession warning is also present it appears only in `detail`, because `launch_result` (lines 1203-1220) puts the first note in `warning` (pinned at `tests/skills/test_issue_orca_worktree.py:1554`). The in-code comment at lines 1309-1310 gives the one-line change that would turn it into the design's refusal: return `launch_result("failed", l2_notes, ...)` when `l2_notes` is non-empty.

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

Isolation and environment (04 E0, lines 9-13): every Bash call set `HOME=$S/home` and `GIT_CONFIG_NOSYSTEM=1`, so no user or system git config applied. The calling shell's ambient variables were deliberately left in place, as a governed agent's push inherits them: `GIT_CONFIG_COUNT=2` with `GIT_CONFIG_KEY_0/1` = `credential.interactive`, `credential.guiPrompt` (values `false`), `GIT_ASKPASS=`, `GIT_EDITOR=true`, `GIT_TERMINAL_PROMPT=0`, and `CLAUDECODE` and `CCSESSION_LAUNCH_ID` set. They add only `credential.*` config, no `core.hooksPath` (04 line 13). The helper scripts the experiments call, `x.sh` and `hook-logging.sh`, are defined in 04 lines 83-147.

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
| Hosting-service API / programmatic ref writes; libraries (pygit2/libgit2, dulwich, GitPython, JGit) | not testable locally [UNVERIFIED], routed to web-01 (Section 5) | 04 Gaps, Step 2.5 D19-30 (API part) |

#### (c) Hook lookup in linked worktrees

| Behaviour | Evidence |
|---|---|
| A linked worktree's default `hooks/pre-push` resolves to the **common** git dir (`clone/.git/hooks/pre-push`) | E0, E1, E30a |
| A hook in the worktree-private git dir (`clone/.git/worktrees/wt/hooks/pre-push`) is ignored | E30b |
| `--git-path hooks/pre-push` prints a relative path (`.git/hooks/pre-push`) in the main checkout and an absolute one in a linked worktree; file 04 did not exercise `--path-format=absolute` (see the note below this table) | E30a |
| From the main checkout `$0` is relative and `GIT_DIR` is not exported; from a linked worktree `$0` is absolute and `GIT_DIR` = worktree-private dir; cwd = top of the pushing checkout | E18 |
| Absolute `core.hooksPath` honoured exactly; relative `core.hooksPath` resolves against each pushing worktree's root (a different, in-tree hook per worktree) | E30c, E30d |
| Plain `git worktree remove` deletes the private git dir (a marker file included); the shared hook stays and still runs for the remaining worktree (Orca removal not tested) | F2 |

**`--path-format=absolute --git-path hooks/pre-push` on 2.47.3 (verified locally, not by file 04).** File 04 did not run the flag. It was run on the installed git 2.47.3 three times, each in a `mktemp -d` sandbox under `/tmp` with `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1`, a main checkout `repo`, a linked worktree `wt` and a local bare `remote.git` as the only remote, removed afterwards (`CLEANED=yes`):

| Run | Setup | Result |
|---|---|---|
| web-01 D3a-e (web-01 lines 193-205) | `git -C wt ...`; then `git config core.hooksPath myhooks` | Linked worktree: `<common-dir>/hooks` (D3a); with `core.hooksPath=myhooks`: `<wt root>/myhooks` (D3d); `-c core.hooksPath=/abs/h` gives `/abs/h/pre-push` (D3e). Main checkout not run. |
| Domain-accuracy QA re-run (`qa/qa-lens-domain-accuracy.md` finding 1) | same shape | `<common-dir>/hooks/pre-push` from both the main checkout and a linked worktree; `<worktree-root>/myhooks/pre-push` with `core.hooksPath=myhooks` |
| Gate 3 fix run X1 (`qa/qa-fix-log.md`, cycle 0) | same shape; commands and verbatim output recorded there | main: `$S/repo/.git/hooks/pre-push`; wt: `$S/repo/.git/hooks/pre-push`; with `core.hooksPath=myhooks`: main `$S/repo/myhooks/pre-push`, wt `$S/wt/myhooks/pre-push` |

The flag therefore returns the effective absolute path from both the main checkout and a linked worktree on 2.47.3. Other git versions remain untested (Phase 6.10).

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

**Unverified items excluded from the architecture above.** synth-01 lists nine [UNVERIFIED] items; each is carried as an open question in Section 9:

| synth-01 item | Topic | Section 9 row |
|---|---|---|
| 1 | API writes and git libraries vs client-side pre-push | R4, R5, row 36 |
| 2 | other git versions and SSH/HTTPS transports | row 24 |
| 3 | `--path-format=absolute --git-path` in the main checkout | Resolved for 2.47.3: R9 (web-01 D3 for the linked worktree; the main checkout was verified by the QA re-run and fix run X1, Section 2.5(c)) |
| 4 | `refs/heads/Main` on a case-insensitive remote | row 23 |
| 5 | stdin order rule | row 22 |
| 6 | Orca worktree removal vs plain `git worktree remove` | row 28 |
| 7 | install-integrity check at install only or before every governed launch | row 3 |
| 8 | pure shell hook vs fixed PATH holding the install-time uv directory | row 1 |
| 9 | no code for no-replace publication, ownership recheck, conflict reporting; §19.6 artifacts absent | rows 14, 16 |

---

## 3. Target State

### 3.1 Goal

When a governed agent pushes, the L2 guard is a git `pre-push` hook. It refuses the whole push, with a nonzero exit, whenever any stdin record has field 3 (the remote ref) exactly equal to `refs/heads/main` or `refs/heads/master`. This holds for an update, a forced update, a create and a delete, and for every push form that reaches the hook. Every other push is allowed. The L2 layer is not built today: there is no production hook and no installer (file 03 section 4; D19-8, D19-71, D19-81 [CODE-VERIFIED] absence). Everything in this section is the target, not the current state (Section 2).

### 3.2 Behaviour the guard must have

| # | Target behaviour | Evidence that makes it achievable | Tag |
|---|---|---|---|
| T-1 | Refuse a governed update, forced update, create or delete of `refs/heads/main` / `refs/heads/master` | Field 3 is always the fully qualified destination: `feature:main` (E2), `HEAD:main` (E6), `+alt:main` and `--force` with no force marker (E5a/E5b), `:main` and `--delete main` as `(delete) <zero-oid> refs/heads/main <old>` (E3b, E4b), create of `refs/heads/master` (E25), `remote.origin.push` mapping (E20), `push.default=upstream` (E21), `--mirror` (E11) | [CODE-VERIFIED] (file 04) |
| T-2 | One protected record refuses the whole push, mixed or not | E19, E24a/E24b (protected last or first), E26a (`--atomic`), E27b, F1 (fast-forward update and delete forms): exit 1 and remote refs unchanged | [CODE-VERIFIED] (file 04) |
| T-3 | Compare field 3 exactly and case-sensitively. Do not normalize `//` or case | `refs//heads/main` is rejected by git as `fatal: invalid refspec` before the hook runs (web-01 G1). `refs/heads/Main` is a valid, distinct ref (E25, web-01 G2). Look-alikes `refs/heads/mainline`, `refs/heads/feature/main`, `refs/heads/main2`, `refs/tags/main`, `refs/heads/ma` reach the hook as their own field 3 (E25, F3a), and the design leaves them unprotected (D19-27) | git part [CODE-VERIFIED]; design choice [UNVERIFIED] (no code) |
| T-4 | Parse each record by right-splitting into four fields (`rsplit(" ", 3)` on the line without its newline). Decide only on field 3 | git itself sends a six-field record for `'HEAD@{0 days ago}:refs/heads/main'` (web-01 G5; re-run as fix run X2: `REC[6]: HEAD@{0 days ago} <oid> refs/heads/main <zero-oid>`). A naive four-variable `read` hook saw `ago}` as field 3, exited 0, and the real push created `refs/heads/main` on the bare remote (fix run X3: remote had no refs before, `refs/heads/main <oid>` after, push `rc=0`). Only fields 2-4 are guaranteed free of spaces (git-check-ref-format rule 4; web-01 Area I). Runs X2 and X3, with commands, hook bodies and output, are in `qa/qa-fix-log.md` cycle 0 | [OBSERVED 2.47.3] local sandbox (web-01 G5; fix runs X2, X3) |
| T-5 | Empty stdin allows (exit 0) | The hook runs with EMPTY stdin for an up-to-date push (E12), a locally known non-fast-forward (E23b) and a stale lease (E27a). transport.c starts the hook before its filtering loop (web-01 Area I) | [CODE-VERIFIED] (file 04) |
| T-6 | Stdin rule (one rule for every file): governed, unknown and no-verdict paths read stdin to EOF before an allow; a refusal may exit as soon as it sees a protected record; ordinary and released verdicts exit 0 without reading (T-10) | Design D19-24 "Stream until EOF". 01 §4 says reading to EOF is needed to know whether the push is protected. Early refusal exit is safe because git tolerates EPIPE (web-01 Area I, transport.c lines 1327-1329). Gap G-42: a hook that never reads stdin exited 0 with 3001 branches | design [UNVERIFIED]; git part external |
| T-7 | `--dry-run` is refused the same way when protected | `--dry-run +alt:main` delivered the real record and moved no refs (E13b). git-push documents dry-run as "Do everything except actually send the updates" (web-01 B2) | [CODE-VERIFIED] (file 04) |
| T-8 | A "fetch first" non-fast-forward to main is refused by the hook | E23a: the `refs/heads/main` record reached the hook before git rejected the push. `REF_STATUS_REJECT_FETCH_FIRST` is not in transport.c's skip list (web-01 Area I) | [CODE-VERIFIED] (file 04); corrects D19-47 |
| T-9 | Hash-length independent | SHA-256 create, update and delete gave 64-hex oids with the same field 3 text (E22) | [CODE-VERIFIED] (file 04) |
| T-10 | Allow ordinary and released pushes with no output and no stream inspection: exit 0 without reading stdin (the T-6 rule) | Design D19-26; 01 §4 mapping: ordinary/released exit 0 silently without reading stdin | design [UNVERIFIED] (no code) |
| T-11 | Restrict pushes only. Local commits and merges stay unaffected | F4: a commit and a `--no-ff` merge into local main succeeded under a refusing hook, which never ran (D19-29 git part) | [CODE-VERIFIED] (file 04) |

### 3.3 Actor selection and the unknown policy (DECIDED)

The hook calls `~/.claude/hooks/launch-job-identity.sh identify` (01 §8). That command prints one JSON line `{"status": "..."}` and exits 0, and a nonzero exit means no verdict (01, `launch-job-identity.sh` lines 530-537) [CODE-VERIFIED].

**Unknown handling is DECIDED, not open.** On 2026-11-08 the owner decided that `unknown` refuses only pushes to `main` or `master`, with its own diagnostic, and allows everything else. Source: file 01 line 186, citing `.dev/brainstorms/20261108-094705-l2-pre-push-guard/seed-brief.md` line 73 ("Orca answer to msg_60b98182bb31").

| `identify` result | Protected push (field 3 = `refs/heads/main` or `refs/heads/master`) | Other pushes | Reads stdin |
|---|---|---|---|
| `{"status": "governed", "session_id": "<id>"}` | refuse | allow | to EOF before an allow; a refusal may exit at the first protected record (EPIPE tolerated) |
| `{"status": "ordinary"}` or `{"status": "ordinary", "reason": "released"}` | allow | allow | no; silent exit 0 |
| `{"status": "unknown"}` | refuse, with a diagnostic distinct from the governed one (DECIDED) | allow (DECIDED) | to EOF before an allow; a refusal may exit at the first protected record (EPIPE tolerated) |
| No verdict: nonzero exit (for example exit 2 when uv is absent), empty or unparseable output, unexpected status | treat as `unknown` (01 §4 target requirement; not yet written in the design, gap G-7) | allow | to EOF before an allow; a refusal may exit at the first protected record (EPIPE tolerated) |

```text
git push  ──►  pre-push hook (common-dir hooks/pre-push, also for linked worktrees)
                   │
                   ▼
        launch-job-identity.sh identify   (kernel session sid -> HOME store jobs/<sid>.json)
                   │
     ┌─────────────┼───────────────────────────┬─────────────────────────────┐
     ▼             ▼                           ▼                             ▼
 governed     ordinary / released          unknown                 no verdict (exit != 0,
     │             │                           │                    empty, bad JSON, other)
     │        exit 0, no read                  │                             │
     │                                         ◄─────── mapped to unknown ───┘
     ▼                                         ▼
 read stdin record by record; rsplit(" ", 3) each line; field 3 in {refs/heads/main, refs/heads/master}?
 (allow only after EOF; a refusal may exit at the first protected record, EPIPE tolerated)
     │ yes                                     │ yes
     ▼                                         ▼
 exit nonzero (governed diagnostic)       exit nonzero (unknown diagnostic)
     │ no                                      │ no
     ▼                                         ▼
 exit 0                                    exit 0
```

Sources for the diagram: 01 §4 (verdict mapping), 01 §7 (the hook, git and supervisor share one kernel session; `identify`, `identify $$` and `identify $PPID` agreed in every case), E1/E30 (common-dir hook), web-01 G5 (right-split).

Consequences the target accepts or must decide (detail in Section 4):

- The DECIDED policy means some humans are refused main/master: HOME unset or relative, a group-writable home, a stale record after a killed supervisor, and no uv on PATH (01 §4; G-11). This narrows design line 493, "never restricted" (D19-1 [UNVERIFIED]).
- The no-uv human case needs a remedy. File 01 §4 item 5 offers three options: (i) the hook sets a fixed PATH holding the uv directory recorded at install time; (ii) the hook applies the no-store early exit itself, which does not help a human on a machine that also has a store; (iii) a pure-shell hook. An absolute uv path alone is not enough, because the script resolves uv through PATH twice (lines 25 and 566) (corrected G-6 remedy, N-3). synth-02 leaves the choice open (G-6); Section 7 recommends (i), and Section 9 row 1 keeps the owner confirmation open.

### 3.4 Hook location and publication

| # | Target | Evidence | Tag |
|---|---|---|---|
| L-1 | git finds the hook from a linked worktree | A linked worktree runs `<common-dir>/hooks/pre-push`; a hook in the worktree-private git dir is ignored (E30, E1). gitrepository-layout: "This directory is ignored if $GIT_COMMON_DIR is set and "$GIT_COMMON_DIR/hooks" will be used instead" (web-01 D1). transport.c finds the hook through `find_hook`, and path.c lists `hooks` in `common_list` (web-02 Area 1c) | [CODE-VERIFIED] (file 04) + external |
| L-2 | The installer resolves the target path with git, run from the target worktree: `git rev-parse --path-format=absolute --git-path hooks/pre-push` | It returns the common dir, honours `core.hooksPath`, resolves a relative value against the worktree root, and reflects `-c` (web-01 D3, local check in `/tmp/web01-exp.PR24RB14`). `--git-path` has honoured hooksPath since 2.10.0. Never use `--git-dir`/hooks (04 Key Takeaways). Design D19-11 "never assume `.git` is a directory" ([CODE-VERIFIED] read side only, `orca_worktree.py` line 1020) | external + [CODE-VERIFIED] read side |
| L-3 | The installer also checks a per-worktree `core.hooksPath`: `git config --worktree --get core.hooksPath` when `extensions.worktreeConfig` is true | E31: a per-worktree hooksPath moved the lookup for that worktree only (web-01 recommendation 4, C4) | [CODE-VERIFIED] (file 04) + external |
| L-4 | Publish without replacing an existing hook | Temp file opened with `O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`, write, `fchmod`, `fsync`, `linkat` to the final name (EEXIST if it exists), `unlinkat` the temp, `fsync` the directory. This is the `publish()` shape of `launch-job-identity.sh` lines 164-174, plus an executable mode and fsync (01 §6; web-02 recommendation 1; web-02 experiment 8) | pattern [CODE-VERIFIED] in 01; recipe external, sandbox-tested |
| L-5 | Set the executable bit with `fchmod` (0755 or 0700), not with the open mode | Under umask 077 an open mode of 0755 became 0700; `fchmod` gave 0755 (web-02 experiments 1a/1b). `publish()` uses mode 0400, which is not executable, so it cannot be reused unchanged (01 §6) | external, sandbox-tested |
| L-6 | Do not use `rename`/`os.replace`. Do not depend on `O_TMPFILE` or `renameat2` | `rename` replaced the existing file silently (web-02 experiment 5). `O_TMPFILE` returned ENOTSUP on overlayfs (experiment 4x; overlayfs support needs kernel 6.10). `renameat2 RENAME_NOREPLACE` is not in Python `os` (web-02 Area 2) | external, sandbox-tested |
| L-7 | On EEXIST: compare full content, `O_NOFOLLOW` regular-file type, same dev/ino, owner and mode, and run a self-test. Identical owned content is reused. Anything else is preserved and reported as `W-L2-ABSENT` with the reason | 01 §6; design line 514 (D19-16); web-02 recommendation 4 | design [UNVERIFIED]; current code [CODE-CONTRADICTED] (D19-16) |
| L-8 | After install, verify `access(X_OK)` as the pushing user, including a noexec-mount check | git skips a hook that fails `access(X_OK)` and the push goes through (fail-open; `hook.c` lines 13-49 at v2.47.3; E29c). A noexec mount gives EACCES (web-02 Area 1b, recommendation 5) | [CODE-VERIFIED] (E29) + external |
| L-9 | Leave other hooks untouched; do not enable `extensions.worktreeConfig` or migrate `core.hooksPath` | D19-12 and D19-15 | [CODE-VERIFIED] (vacuous/absence; no code writes git hooks today) |
| L-10 | Never set `advice.ignoredHook=false` | It silences the only signal that a non-executable hook was skipped (E29b; web-02 recommendation 7) | [CODE-VERIFIED] (file 04) + external |

### 3.5 Success criteria (testable pass/fail)

Each criterion runs against a disposable local bare remote in a `mktemp -d` sandbox (design D19-45; file 04 method). "Refused" means push exit status nonzero AND the remote ref unchanged. "Allowed" means exit 0 AND the remote ref changed (or `--dry-run` exit 0).

| ID | Criterion | Pass condition | Evidence basis |
|---|---|---|---|
| SC-1 | Governed agent, linked worktree, `git push origin feature:main` | refused; stderr carries the governed diagnostic | E1, E2, E19 |
| SC-2 | Governed: `HEAD:main`, `+alt:main`, `--force feature:main`, `:main`, `--delete main`, create `refs/heads/master`, `--force-with-lease` matching | each refused | E3b, E4b, E5a, E5b, E6, E25, E27b |
| SC-3 | Governed: bare `git push origin` with `remote.origin.push=feature:main`; `-c push.default=upstream push origin` with upstream `origin/main` | each refused | E20, E21 |
| SC-4 | Governed: `--mirror` to a remote holding `refs/heads/main` that would change | refused | E11 |
| SC-5 | Governed: mixed push with a protected ref first and last, with and without `--atomic` | refused; the unprotected ref also unchanged | E24a/E24b, E26a, F1 |
| SC-6 | Governed: "fetch first" non-fast-forward to main | refused by the hook (record observed in hook log) | E23a |
| SC-7 | Governed: `--dry-run +alt:main` | exit nonzero | E13b |
| SC-8 | Governed: `'HEAD@{0 days ago}:refs/heads/main'` (six-field record) | refused, not mis-parsed | web-01 G5; fix runs X2-X4 |
| SC-9 | Governed, SHA-256 repository: create, update and delete of main | each refused | E22 |
| SC-10 | Governed: `feature:refs/heads/side`, `refs/heads/mainline`, `refs/heads/feature/main`, `refs/heads/main2`, `refs/tags/main`, `refs/heads/Main`, `refs/heads/ma` | each allowed | E25, F3a, D19-27 |
| SC-11 | Governed: up-to-date push (empty stdin) | exit 0 | E12, D19-23 |
| SC-12 | Governed: 3001-branch push with no protected ref | exit 0, and the hook read stdin to EOF before allowing (T-6 rule) | G-42, D19-24 |
| SC-13 | Ordinary (no record in the store) and released (`rm sessions/<id>`): push to main | allowed, no hook output, stdin not read (T-6/T-10 rule) | 01 §4, §7; D19-26 |
| SC-14 | Unknown (for example `env -u HOME`, bogus level content, killed supervisor): push to main | refused with the unknown diagnostic, different from the governed one | 01 §4, §7; seed-brief line 73 |
| SC-15 | Unknown: push to `refs/heads/side` | allowed | seed-brief line 73 (DECIDED) |
| SC-16 | `identify` exits nonzero, prints nothing, prints non-JSON, or prints an unexpected status | treated as unknown (SC-14 and SC-15 behaviour) | 01 §4 |
| SC-17 | `git rev-parse --path-format=absolute --git-path hooks/pre-push` from a linked worktree prints the installed path, and a push from that worktree runs the hook | both hold | E30, web-01 D3 |
| SC-18 | Each installer conflict and failure case (Phase 2.1-2.6, 4.2), including each `pre-push.uv-dir` failure of step 2.5(b) at install and at a later launch | nothing outside the temp file changes (foreign file bytes, mode and inode unchanged; `core.hooksPath` value unchanged), `l2_status` returns `absent` with exactly one of these reason strings, and the launch carries `W-L2-ABSENT` whose detail names it: `no-hook`, `foreign-pre-push`, `hookspath-set`, `not-executable`, `not-owned`, `self-test-failed`, `guard-source-missing`, `uv-dir-missing`, `git-missing`, `timeout`, `not-a-repo` | 01 §6, D19-14, D19-16, web-02 experiment 3a; Phase 4.2 |
| SC-19 | Installing twice | the second install reuses the identical owned file; no temp file remains | web-02 experiment 8 |
| SC-20 | Installed hook mode under umask 077 | `access(X_OK)` true for the pushing user (mode 0700 or 0755) | web-02 experiments 1a/1b, 7 |
| SC-21 | `pre-commit`, `commit-msg` and other hooks before/after install | byte-identical | D19-12 |
| SC-22 | Governed: local commit and merge into local main | succeed (L2 restricts pushes only) | F4, D19-29 |
| SC-23 | Human whose PATH lacks uv, no store record, push to main, with the owned uv-directory file `<hooks-dir>/pre-push.uv-dir` (proposal, Phase 1.2 and 2.1) present | allowed (the hook bytes equal the packaged source and the uv directory comes from the file). This holds under identity variant A-i; if the brainstorm picks A-iii instead (Section 9 row 1), this row is replaced by that variant's row | E28c, 01 §4 item 5; Phase 1.2 |
| SC-24 | (a) The uv-directory file is missing, unreadable, not one absolute path, or its directory holds no executable `uv`. (b) After a good install, the file is replaced by a symlink, rewritten to name a different directory (one holding a stub `uv` that prints `{"status": "ordinary"}`), made group- or other-writable, or its named directory or `uv` is made group- or other-writable | (a) the hook treats the call as "no verdict" (`unknown`): a push to main is refused with the unknown diagnostic naming the cause `uv-dir-missing`, a push to `refs/heads/side` is allowed; `l2_status` returns `absent` with reason `uv-dir-missing`. (b) at the next launch `l2_status` returns `absent` with reason `uv-dir-missing` (symlink, other directory) or `not-owned` (group- or other-writable), and the launch carries `W-L2-ABSENT` naming it | Phase 1.2, 1.4, 2.1, 2.5(b), 4.2 (proposal) |
| SC-25 | L1 hook-file tamper: PreToolUse JSON for `Write` with `file_path` `<repo>/.git/hooks/pre-push` and with `file_path` `<repo>/.git/hooks/pre-push.uv-dir`, and for `Bash` with `chmod -x .git/hooks/pre-push`, `rm .git/hooks/pre-push` and `printf x >> .git/config.worktree`, fed on stdin to `launch-level-guard.sh` in a bound governed session (the `_bind`/`_payload`/`_hook` harness of `tests/hooks/test_launch_level_guard_with_identity.py` lines 67-103) | each exits 2 and stderr names `LL-TAMPER` (`ll_deny` exits 2, guard lines 135-138; TAMPER maps to `LL-TAMPER`, line 738) | Phase 5.1 |
| SC-26 | L1 config-route push bypasses, same harness: `git --config-env=core.hooksPath=V push origin main`, `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.hooksPath GIT_CONFIG_VALUE_0=/x git push origin feature`, `GIT_CONFIG_PARAMETERS="'core.hookspath'='/x'" git push origin feature`, `git -c hook.pre-push.enabled=false push origin feature` | each exits 2 with `LL-TAMPER` or `LL-PUSH-FORM` (either denial passes; exit 0 fails) | Phase 5.4; 04 E15/E16; web-01 C2, F1 |
| SC-27 | L1 ANSI-C spelling, same harness, each in the escaped and the plain spelling: `git -c $'core.hooks\x50ath'=/x push origin feature` / `git -c core.hooksPath=/x push origin feature`, and `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=$'core.hooks\x50ath' GIT_CONFIG_VALUE_0=/dev/null git push origin feature` / the same with `core.hooksPath` | all four exit 2 with an `LL-*` denial (exit 0 fails) | Phase 5.4(b); 02 line 249 |
| SC-28 | L1 unlisted wrappers, same harness: `chrt 0 git $'\x70ush' --no-verify origin main`, `taskset 1 git $'\x70ush' --no-verify origin main`, `find . -maxdepth 0 -exec git $'\x70ush' --no-verify origin main \;`, `uv run git $'\x70ush' --no-verify origin main` | each exits 2 with an `LL-*` denial (exit 0 fails) | Phase 5.3; guard line 549; 02 line 251 (the first three; `uv run` is the same line-549 case, not listed by 02) |
| SC-29 | IR-7 switch, launch with L2 absent: `L2_REFUSAL_ENABLED = False` (default) and `True` (monkeypatched) | off: launch JSON `status` is `launched` and `W-L2-ABSENT` is present; on: `status` is `failed`, `warning` is `W-L2-ABSENT`, and no agent is launched | Phase 4.4, 6.11 (proposal) |
| SC-30 | `core.hooksPath` set (repository config, and `config.worktree` with `extensions.worktreeConfig=true`) at launch | nothing installed; config value and every file unchanged; `l2_status` returns `absent` with reason `hookspath-set` | Phase 2.3, 4.3; web-01 C4 |
| SC-31 | Recheck before each launch: after a good install, clear the exec bit (`chmod -x`), set `core.hooksPath`, rewrite `pre-push.uv-dir` to name another directory, or `chmod g+w` it, then launch again | the second launch reports `W-L2-ABSENT` with reason `not-executable`, `hookspath-set`, `uv-dir-missing` or `not-owned` respectively; the first launch reported no `W-L2-ABSENT` | Phase 4.1, 2.5(b); G-8; 04 E29 |

### 3.6 Constraints from design section 19 (`docs/designs/sc-issue-launch-level-hook.md` lines 489-578)

The verification tags come from file 03's claim table, as updated by file 04 Step 2.5 and web-01.

| D19 | Line | Constraint | Verification status |
|---|---|---|---|
| D19-1 | 493 | Ordinary human push in the same worktree is never restricted by launch policy | [UNVERIFIED] (no L2 code). Narrowed by the DECIDED unknown policy (G-11) |
| D19-2 | 493 | git's inputs are remote name/URL and ref records; no Claude session id from git | [CODE-VERIFIED] (04 E1, E11, E18, E28) |
| D19-3 | 493 | A marker is only an eligibility hint; env values, pane key, branch or path are never authority | [UNVERIFIED] (no L2 selector). The environment passes through unchanged (E28) |
| D19-11 | 510 | Resolve git paths with git; never assume `.git` is a directory | [CODE-VERIFIED] read side only (`orca_worktree.py` line 1020) |
| D19-12 | 510 | Other hooks remain untouched | [CODE-VERIFIED] (vacuous) |
| D19-13 | 512 | Install only at default lookup, no foreign pre-push, publication and self-test succeed | [UNVERIFIED] (no installer) |
| D19-14 | 512 | Publish a complete executable without replacing an existing file; recheck owned content; a header alone is no proof of ownership | [UNVERIFIED] (no installer); recipe tested externally (web-02 experiment 8) |
| D19-15 | 512 | Do not enable worktreeConfig, migrate hooksPath, shadow, stub or replay foreign hooks | [CODE-VERIFIED] (absence) |
| D19-16 | 514 | Conflict or unsupported lookup: preserve, report `W-L2-ABSENT` with the reason | [CODE-CONTRADICTED] (foreign hook gives `present-unverified`, no warning) |
| D19-18 | 514 | Do not launch a governed pipeline advertised as protected when L2 is absent | [CODE-CONTRADICTED] (code warns and launches); design IR-7 line 355 and line 514 [STALE DOC] |
| D19-19 | 514 | Ordinary/no-pipeline claim unaffected | [CODE-VERIFIED] |
| D19-20, 22, 25 | 518 | Record format; zero oids and `(delete)` ordinary; no SHA-1 length | [CODE-VERIFIED] (04 Step 2.5) |
| D19-21 | 518 | Refuse the entire push if field 3 is exactly main/master | git part [CODE-VERIFIED] (E19, E24, E26a, F1); guard [UNVERIFIED] |
| D19-23 | 518 | Empty stream allows; malformed governed stream refuses with a distinct diagnostic | empty part [CODE-VERIFIED]; malformed part [UNVERIFIED]; must be reconciled with the six-field form (web-01 G5, recommendation 1) |
| D19-24 | 518 | Stream until EOF; no truncation | [UNVERIFIED] |
| D19-26 | 518 | Unselected ordinary pushes allowed without output or stream inspection | [UNVERIFIED] |
| D19-27 | 520 | `refs/tags/main`, `mainline`, `ma`, `feature/main` not protected | git part [CODE-VERIFIED] (E25, F3a) |
| D19-28 | 520 | A mapped source-only refspec is protected because field 3 is authoritative | [CODE-VERIFIED] (E20, E21, E6) |
| D19-29 | 520 | No local commit/merge restriction | git part [CODE-VERIFIED] (F4) |
| D19-30 | 520 | `--no-verify`, hooksPath overrides, send-pack and API writes bypass pre-push | local forms [CODE-VERIFIED] (E14-E17); API part: documented externally (web-01 H/J); not confirmed at runtime |
| D19-31 | 520 | Visible bypass forms remain checked by L1 | [CODE-VERIFIED] partial (`launch-level-guard.sh` lines 528, 532); file 02 lists ALLOWED/PARTIAL forms |
| D19-32 | 520 | Same-user modification and detachment remain limitations | [CODE-VERIFIED] (disclaimer, `launch-job-identity.sh` lines 2, 7-9) |
| D19-35 | 524 | The shared hook may remain installed after one worktree is removed | [CODE-VERIFIED] (F2) |
| D19-36 | 526 | Deleting level/approval files is the release route | [CODE-VERIFIED] (identity side only) |
| D19-37, 39 | 526 | A retained marker must not restrict humans; no shared-hook deletion on single-session release | [CODE-VERIFIED] (absence) |
| D19-46 | 534 | Check effective hook presence, executable ownership and process membership | [UNVERIFIED]; `l2_status` covers presence and X_OK only |
| D19-47 | 534 | Fixture refs must reach pre-push (not up-to-date/non-fast-forward rejection) | [CODE-CONTRADICTED] in part (E23a "fetch first" reaches the hook) |
| D19-48 | 534 | Dry-run supplements, does not replace, ref-state assertions | [CODE-VERIFIED] (E13) |
| D19-59 | 549 | Identity body runs through uv on Linux | [CODE-VERIFIED] (`launch-job-identity.sh` line 566) |
| D19-66 | 557 | `identify [PID]` emits governed/ordinary/unknown | [CODE-VERIFIED] |
| D19-67 | 559 | Fresh Bash shell; `cd` does not persist; `setsid` escapes | [CODE-VERIFIED] |
| D19-81 | 576 | The L2 layer is pending and needs its own plan | [CODE-VERIFIED] (absence) |

Other §19 claims (D19-4 to D19-10, D19-17, D19-33, D19-34, D19-38, D19-40 to D19-45, D19-49 to D19-58, D19-60 to D19-65, D19-68 to D19-80, D19-82, D19-83) are about history, process, the identity adapter or L1 rather than L2 push behaviour. Their tags are in file 03's claim table and are not repeated here. D19-82 (no governed claim on a real issue until OB-H1 item 1, OB-H2 and OB-H3 pass) is [UNVERIFIED]: `cmd_launch` has no OB check.

---

## 4. Gap Analysis

**Severity rule.** Gaps G-1 to G-43 keep the severity recorded in `gaps-and-questions.md`, unchanged. Rows added from the research (prefixes BP, L1, DOC) are rated as follows. Critical: a governed push to main or master succeeds with no layer refusing it, and needs no capability beyond ordinary same-user file access or an ordinary command. Important: the target needs a decision, code or a doc correction, or a layer still refuses the push. Minor: a precision or wording issue, or a future-version risk. No G-row is rated Critical in `gaps-and-questions.md`; the Critical rows below are new ratings by synth-02, based on file 02 verdicts and file 04/web results. G-44 and G-45 were added at the Gate 3 report review and are rated by the same rule: G-44 is Critical (its `--no-verify` form passes both layers, like L1-5) and G-45 is Important. Where each gap is closed (a step in Section 8 or an entry in Section 9) is given in Sections 8.8 (G-1 to G-45) and 8.9 (BP-, L1- and DOC- families).

### 4.1 Gaps compiled in `gaps-and-questions.md`

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| G-1: API/programmatic ref writes (hosting ref API, `gh api`, curl to smart-HTTP `git-receive-pack`) | No local test (04 D19-30 API part [UNVERIFIED]) | Recorded as an L2 limitation; L1 refuses the visible forms | Important | **Documented externally (web-01 H/J); not confirmed at runtime.** Per the documentation none of them runs pre-push (gitprotocol-http, GitHub REST refs docs, gh api manual); web-01 J11 rates design line 520 CONFIRMED on that documentary basis. Nothing was run |
| G-2: Do pygit2/libgit2, dulwich, GitPython, JGit run pre-push? | Untested locally; none installed (04 Gaps) | Each library classified; in-process pushes recorded as a stated limitation | Important | **Documented externally (web-01 H/J); not confirmed at runtime.** Per the documentation and source reading, libgit2, pygit2, dulwich, isomorphic-git do not; JGit (since 4.2) and GitPython (shells out to `git push`) do. No library was installed or run. See BP-9 |
| G-3: git version of each behaviour | Hints only | Version table with release-note citations | Important | **Answered by web-01 F2** (Section 5.3 version table) |
| G-4: Linux no-replace publication | `publish()` pattern exists (`launch-job-identity.sh` lines 164-174) but is mode 0400 and inside a heredoc (01 §6) | `O_EXCL` temp, `fchmod` 0755/0700, `fsync`, `linkat`, `unlinkat`, directory `fsync` | Important | **Answered by web-02** Areas 2-3, experiment 8 (Section 5.2) |
| G-5: git's executable check | E29 observed the fail-open | Source-level explanation | Important | **Answered by web-02 Area 1:** `find_hook` in `hook.c` line 21 uses `access(X_OK)`; `transport.c` lines 1295-1296 return 0 when no hook path is found |
| G-6: Human whose PATH lacks uv | `identify` exits 2 (lines 25, 52-53, 566), which maps to unknown, so the human is refused main/master (E28c) | That human can push to main/master (D19-1) | Important | Options: fixed PATH with the install-time uv directory, a hook-side no-store exit (does not help on a machine with a store), or a pure-shell hook. An absolute uv path alone is not enough (corrected remedy, N-3). Design choice open |
| G-7: "No verdict" maps to unknown, but this is not written in the design | 01 §4 states it as a hook requirement only | Design states it; the hook implements it | Important | `identify` prints default-separator JSON (`{"status": "ordinary"}`, with a space after the colon) while `publish()` uses compact separators. The hook must parse JSON rather than compare compact text (01 line 44) |
| G-8: Install-integrity holes with no push flag: exec bit cleared (E29) and per-worktree `core.hooksPath` (E31) | `l2_status` checks only `is_file` and `X_OK` (`orca_worktree.py` lines 1012-1029), and only before a launch | Integrity checked at install AND before each governed launch (open decision) | Important | web-02 recommendation 8: the executable bit makes L2 easy to disable, so a pre-flight X_OK check or another layer is needed. See BP-5, BP-6 |
| G-9: Ordinary escapes: `setsid` and a different valid HOME | Both give `ordinary` (01 §7); HOME escape listed nowhere | Escape acknowledged in the design, or closed | Important | `setsid` is listed (header lines 7-8, design 559, seed brief line 45); L1 refuses `HOME=` and `env -u HOME` (02) |
| G-10: Stale job records after a killed supervisor are never pruned | After `kill -9`, the verdict is unknown and `jobs/<sid>.json` stays (01 §7) | Prune, or accept and document | Important | PID reuse turning a human into unknown is inferred, not observed |
| G-11: Humans restricted by unknown | HOME unset/relative, group-writable home, stale record, no uv on PATH give unknown (01 §4) | Accepted consequence of the DECIDED policy, documented against design line 493 | Important | The DECIDED policy (seed brief line 73) makes this a documentation gap, not a policy question |
| G-12: No git-hooks tamper token in L1 | Line 706 tokens omit `.git/hooks`; Write/Edit/rm/chmod/ln on `pre-push` ALLOWED (02) | Token added at line 706 | Important | See L1-3, L1-4 |
| G-13: L1 command-position bypass via an underscore env prefix | W has no `_` (lines 421-438), so `A_B=1 git ...` moves command position off `git` (line 637) | Prefix handled | Important | Contradicts LL-UNKNOWN Why line 80 (DOC-2). See L1-5 |
| G-14: Config written without a git word | `.git/config`, `config.worktree`, `/etc/gitconfig` writes set `core.hooksPath`, `alias.*`, `remote.origin.push` unrefused | Refused, or L2 covers the result | Important | Line 532 config tokens apply only when LL_GIT=1. See L1-1 |
| G-15: Destination from configuration invisible to L1 | L1 canonical regex (line 661) sees only the command text | L2 sees it as field 3 (E20) | Minor | Resolved for L2; L1 gap stays |
| G-16: Smart-HTTP `git-receive-pack` on `github.com` and non-literal API hosts | L1 ALLOWED/PARTIAL (02) | Refused by L1, or stated as a limitation | Important | web-01 H: a smart-HTTP POST does not run pre-push. See BP-7, L1-6, L1-7 |
| G-17: IR-7/D19-18 refusal vs warning | Code warns `W-L2-ABSENT` and launches (`orca_worktree.py` lines 1305-1312, Remedy 789-792) | Default DECIDED by the owner (seed-brief line 77): off, so `W-L2-ABSENT` stays a warning; the refusal path is built behind a switch in a separate, clearly marked commit and is tested (seed-brief line 68); the change is one line (comment at the call site). Proposed mechanism: module constant `L2_REFUSAL_ENABLED = False` in `orca_worktree.py` (step 4.4), tested by Phase 6.11 with the constant monkeypatched in-process. Open: only when it turns on (after #442?; Section 9 row 12) | Important | DOC-5 |
| G-18: D19-16 foreign executable hook gives `present-unverified`, no warning | `test_issue_orca_worktree.py` lines 1691, 1727 | `W-L2-CONFLICT` or a reason field | Important | [CODE-CONTRADICTED] |
| G-19: `l2_status` cannot tell an owned guard from any executable | No marker, version line or hash; git-missing, timeout and not-a-repo fold into `absent` | Full-content ownership check (01 §6) | Important | L1 has a version line, `GUARD_VERSION_LINE` (`orca_worktree.py` line 804), as a precedent |
| G-20: `install_hooks.py` has no git-hook path | 612 lines, no pre-push code (03) | New per-repo install code; natural point in `cmd_launch` before `l2_status` (design 565) | Important | The whole L2 layer is unbuilt (D19-81) |
| G-21: §19.6 artifacts absent | `.dev/brainstorms/20261106-l2-prepush-decisions/` missing; D19-10, 17, 33, 49, 52-56 unverifiable | Committed, or the citations removed | Minor | DOC-6 |
| G-22: Line-487 corpus wrongly reported absent | Resolved in Gate 1 | — | Important (resolved) | `.dev/brainstorms/20261105-170229-launch-level-hook/` is present |
| G-23: 04 lacked Key Takeaways | Resolved in Gate 1 | — | Important (resolved) | 04 lines 2233-2245 |
| G-24: Stdin record order | Undocumented; observed both ways: command-line order in E7 and web-01 G3 (one `--dry-run` run of creates), not command-line order in E9, E19 and E24 (E24: two runs, same stream whichever position the protected ref had) | Guard scans every record and does not depend on order | Minor | web-01 G3/Area I: no documented order; code does not sort. Design §19.3 already says not to depend on order. Resolved only in that sense |
| G-25: Case folding of `Main` | Distinct field 3 (E25) | Compare case-sensitively | Minor | web-01 G2: valid and distinct ref. Hosting-service folding not answered [UNVERIFIED] |
| G-26: `--path-format=absolute --git-path` not exercised in 04 | 04 measured plain `--git-path` only | Installer uses the absolute form | Minor | **Answered for 2.47.3**: web-01 D3a-e (linked worktree) plus the QA re-run and fix run X1 (main checkout); see the note under Section 2.5(c) |
| G-27: Network transports | File transport only | — | Minor | Open [UNVERIFIED] |
| G-28: Malformed governed stream | 04: git never produced one | Guard handles git's legitimate more-than-four-field record | Minor | **Contradicted in part by web-01 G5** (six-field record from `git push`). See DOC-8. Severity of the six-field risk is higher than this row: see BP-14 |
| G-29: `refs//heads/main` passes the L1 regex | — | — | Minor | **Answered by web-01 G1:** `fatal: invalid refspec`, hook never runs |
| G-30: `remote.<name>.mirror` with an explicit refspec | — | — | Minor | **Answered by web-01 G4:** `fatal: --mirror can't be combined with refspecs` |
| G-31: Is `extensions.worktreeConfig` enabled in this repo? | Not checked | Known | Minor | Open (local read-only check) |
| G-32: §19.1 actor selection lifecycle variants | One data point (E1) | — | Minor | 01 §7 adds real-git cases (setsid, HOME, background child, release, kill -9) |
| G-33: PID namespace / container boot_id | [UNVERIFIED] | Scope decision | Minor | 01 §5 |
| G-34: Non-dumpable/setuid Python making `/proc/<sid>` root-owned | [UNVERIFIED] | Scope decision | Minor | 01 Gaps 6 |
| G-35: Self-test scope of the installed hook | Undecided | Decided (governed fixture or ordinary only) | Minor | 01 Gaps 7 |
| G-36: Script lookup and missing-script behaviour from the hook | Undecided | A missing script gives no verdict, which maps to unknown (G-7) | Minor | 01 Gaps 8 |
| G-37: Orca's worktree-removal path | Plain `git worktree remove` tested (F2) | — | Minor | D19-34 self-declared unverified |
| G-38: `cd` persistence between Bash calls; mid-session `~/.bashrc` edits | [UNVERIFIED] | — | Minor | D19-67 [CODE-VERIFIED] says `cd` does not persist inside the identity adapter's fresh shell |
| G-39: L1 section 9 evasions are static readings | Not executed | Confirmed in the L1 test suite | Minor | See L1-5, BP-11 |
| G-40: Local-path remotes changed by `update-ref`/`fetch` in the remote dir | — | — | Minor | Not relevant to GitHub (02 Gap 14) |
| G-41: The only real-git pre-push code is a TEST policy that crashes on malformed records | `tests/hooks/test_launch_job_identity.py` lines 1175-1232 (ValueError at 1204) | Production hook with right-split parsing | Minor | — |
| G-42: Large push, hook never reads stdin | Exit 0 with 3001 branches (QA sandbox, not in 04) | The T-6 rule: governed, unknown and no-verdict paths read stdin to EOF before an allow; a refusal may exit at the first protected record; ordinary and released exit 0 without reading | Minor | web-01 Area I: EPIPE tolerated, so an early refusal exit is safe |
| G-43: Unverified design statements | D19-1, 3, 9, 13, 14, 21, 23, 24, 26, 27, 29, 35, 38 have no code; others untested or uncheckable | — | Minor | git parts of 21, 23, 27, 29, 35, 41 settled by 04 Step 2.5 |
| G-44: L1 command-position bypass via an unlisted wrapper word (added at Gate 3 QA; not in `gaps-and-questions.md`) | The wrapper skip list at guard line 549 names `env`, `sudo`, `nohup`, `timeout`, `setsid`, `nice` and others, but not `chrt`, `taskset`, `find` or `uv`, so `chrt 0 git $'\x70ush' --no-verify origin main` puts the wrapper word in command position (line 637) and the unknown-subcommand check never runs (02 line 251, static reading) | Wrapper forms handled like the listed wrappers, or refused | Critical (rated at Gate 3 under the rule above: the example carries `--no-verify`, which removes L2, and L1 lets it through, so a governed push to main succeeds with no layer refusing it, using only an ordinary command; L1-5, the underscore-prefix form of the same bypass, is also Critical) | Same class as G-13 / L1-5; `uv run` is this report's addition, not in 02 |
| G-45: `W-L2-ABSENT` is hidden in `detail` when another launch warning comes first (added at Gate 3 QA; not in `gaps-and-questions.md`) | `launch_result` (`orca_worktree.py` lines 1203-1220) puts only the first note code in `warning`; later codes become "also …" text in `detail`. The test at `tests/skills/test_issue_orca_worktree.py` line 1554 asserts this for `W-LAUNCH-NOT-CCSESSION` + `W-L2-ABSENT` | The L2 state is readable from the launch JSON whatever other warning comes first | Important (rated by this QA: a consumer reading only `warning` misses the absent L2 hook) | Phase 4.3a adds an `l2` field |

### 4.2 Bypasses that skip the pre-push hook

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| BP-1: `git push --no-verify` | Hook not run, remote changed (E14) | L1 refuses | Important | L1 REFUSED (02). Documented "the hook is bypassed completely" (web-01 B1). Code 1.8.2, docs 1.8.4 |
| BP-2: `-c core.hooksPath=/dev/null` or a directory without pre-push | Hook not run (E15, E16) | L1 refuses | Important | L1 REFUSED `-c core.hooksPath` and `git config core.hooksPath` (02) |
| BP-3: `--config-env` and `GIT_CONFIG_COUNT`/`GIT_CONFIG_KEY_n`/`GIT_CONFIG_VALUE_n`, `GIT_CONFIG_PARAMETERS` | Not tested in 04; documented (web-01 C2) | L1 refuses these forms (web-01 recommendation 5) | Critical | 02 §9 static evasion `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=$'core.hooks\x50ath' GIT_CONFIG_VALUE_0=/dev/null` was not executed (G-39) |
| BP-4: Persistent `core.hooksPath` written to `.git/config` or `config.worktree` | Effective for the next push (E31 for config.worktree) | L1 refuses; install-integrity check detects it | Critical | L1 PARTIAL (02, line 706). See L1-1, G-8, G-14 |
| BP-5: Per-worktree `core.hooksPath` via `extensions.worktreeConfig` | Lookup moved for that worktree only (E31a) | Detected before each governed launch | Important | web-01 C4. G-8 |
| BP-6: Executable bit cleared on the hook | Hook skipped with a hint; real push to main succeeded (E29c). `-c advice.ignoredHook=false` silences the hint (E29b) | Detected (X_OK pre-flight) | Critical | L1 ALLOWED for `chmod -x` (02). `hook.c` line 21 `access(X_OK)` (web-02). See L1-4 |
| BP-7: Raw smart-HTTP POST to `.../git-receive-pack` | Does not run pre-push (web-01 H, gitprotocol-http) | L1 refuses `curl` to `git-receive-pack` | Critical | L1 ALLOWED for `github.com/<o>/<r>.git/git-receive-pack` (02) |
| BP-8: `git send-pack` | Hook not run; `--force alt:refs/heads/main` rewrote main (E17c) | L1 refuses | Important | L1 REFUSED (02) |
| BP-9: In-process library push (libgit2/pygit2, dulwich, isomorphic-git) | Does not run pre-push (web-01 J) | Stated limitation (web-01 recommendation 5) | Critical | L1 PARTIAL for `uv run python -c` with these libraries; ALLOWED for `uv run python <script>` (02, line 678) |
| BP-10: GitHub REST refs API / `gh api` | Does not run pre-push (web-01 J) | L1 refuses; server-side protection | Important | L1 REFUSED `curl` to api.github.com, `gh api -X`/`--method`; PARTIAL for hidden host and `gh $'\x61pi'` (02). See L1-7, L1-8 |
| BP-11: Hook file removed, replaced or symlinked | Not tested; L1 ALLOWED `rm`, `mv`, `ln -sf`, `printf >`, Write/Edit (02) | Detected by the ownership check; L1 token at line 706 | Critical | G-12. L1-3, L1-4 |
| BP-12: `hook.pre-push.enabled=false` (future) | Not in 2.47.3; in the unreleased 2.98.0 draft it also disables hooks-directory hooks (web-01 F) | L1 covers `-c hook.pre-push.*` | Minor | Future-version risk |
| BP-13: Config-defined hooks (2.54.0) and parallel hooks (2.55.0); remote groups (on the 2.55.0 git-push page) | Absent from 2.47.3 | Version assumption pinned (web-01 recommendation 7) | Minor | Remote groups: git "continues pushing to the remaining remotes" after a failure (web-01 B7) |
| BP-14: Naive parsing of a more-than-four-field record | Six fields for `'HEAD@{0 days ago}:refs/heads/main'` (web-01 G5; fix run X2). A four-variable `read` hook let the push to main through: rc 0, remote `refs/heads/main` created (fix run X3, `qa/qa-fix-log.md`) | Right-split parsing into four fields (T-4) | Important | Not a hook skip but a guard bypass if the hook parses with a four-variable `read` |

### 4.3 L1 verdicts of ALLOWED or PARTIAL (file 02)

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| L1-1: Persistent `core.hooksPath` via a direct config-file write (`cd .git && >> config`, `config.worktree`) | PARTIAL (line 706) | Refused | Critical | BP-4, G-14 |
| L1-2: `cd <dir>`, then a canonical push | ALLOWED | L2 refuses if the destination is main/master | Important | L2 sees field 3 regardless of `cd` |
| L1-3: Write or Edit of `.git/hooks/pre-push` | ALLOWED (lines 679, 706, 743) | Refused (`.git/hooks` token) | Critical | G-12 |
| L1-4: `rm`, `mv`, `chmod -x`, `ln -sf`, `printf >` on the hook | ALLOWED | Refused | Critical | G-12, BP-6, BP-11 |
| L1-5: Alias by file write, then `<VAR_WITH_UNDERSCORE>=1 git <x> origin main` | ALLOWED (lines 435, 556-557, 637, 706) | Refused | Critical | G-13; unlisted-wrapper form G-44 (line 549). 02 §9: `A_B=1 git $'\x70ush' --no-verify origin main` passes at every level (static reading, G-39) |
| L1-6: `curl` POST to `github.com/<o>/<r>.git/git-receive-pack` | ALLOWED | Refused | Critical | BP-7, G-16 |
| L1-7: `curl` to `api.github.com` with the host hidden | PARTIAL | Refused or stated limitation | Important | BP-10 |
| L1-8: `gh $'\x61pi'` hidden api | PARTIAL | Refused | Important | BP-10 |
| L1-9: `uv run python -c` with pygit2, dulwich or GitPython | PARTIAL | Stated limitation | Important | BP-9. GitPython goes through `git push`, so L2 sees it unless `no_verify=True` (web-01 J) |
| L1-10: `uv run python <script>` that pushes | ALLOWED (line 678) | Stated limitation | Critical | BP-9 |

### 4.4 [CODE-CONTRADICTED] and [STALE DOC] findings

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| DOC-1: D19-47 (design line 534) says non-fast-forward refs are rejected before pre-push | [CODE-CONTRADICTED] in part: a "fetch first" non-ff reaches the hook (E23a) | Line 534 says only non-fast-forward, stale, remote-updated and up-to-date refs are filtered (web-01 recommendation 8) | Important | Source: `transport.c` lines 1315-1319 skip list (web-01 Area I). 04 calls the sentence "incomplete rather than wrong" |
| DOC-2: LL-UNKNOWN Why text (`launch-level-guard.sh` line 80): "an alias cannot commit, push or merge" | [CODE-CONTRADICTED]/[STALE DOC] (G-13) | Text corrected or the bypass closed | Important | 02 Stale Documentation |
| DOC-3: LL-TAMPER Blocked text (line 95): "a git configuration file" | [CODE-CONTRADICTED] (partial): only some config paths are tokens | Text matches the tokens | Minor | 02 Stale Documentation |
| DOC-4: `launch-job-identity.sh` header line 4 "descendants" | [CODE-CONTRADICTED] (wording): the code uses kernel session membership | Header says session membership | Minor | 01 Gaps 9 |
| DOC-5: Design IR-7 line 355 and §19.2 line 514 say refuse | [STALE DOC]: code warns `W-L2-ABSENT` and launches (D19-18 [CODE-CONTRADICTED]) | Design and code agree: the design records the DECIDED default (off; warning stays; refusal path built, tested and switched off, seed-brief lines 68, 77) | Important | G-17. §19.8 line 574 itself records the warning choice (D19-79) |
| DOC-6: Design §19.6 lines 538-543 cite `.dev/brainstorms/20261106-l2-prepush-decisions/` | [STALE DOC]: absent | Present, or citation removed | Minor | G-21 |
| DOC-7: D19-16 (design line 514) conflict reported as `W-L2-ABSENT` | [CODE-CONTRADICTED]: `present-unverified`, no warning | Conflict reported | Important | G-18 |
| DOC-8: D19-42 (design line 530) "Git does not normally send malformed or padded records" and D19-23 "malformed governed stream refuses" | file 04 F3: CONFIRMED for the tested scope. web-01 G5: `git push` sends a six-field record for an expression source (re-run as Gate 3 fix run X2, `qa/qa-fix-log.md`; a naive four-variable hook let the push to main through in fix run X3) | Design accepts more than four fields when fields 2-4 are valid (web-01 recommendation 1), or names this form in a distinct refusal diagnostic | Important | **Contradiction between files.** web-01 G5 is stronger evidence here: a direct local test of an input form that file 04 never tried. File 04's result remains true for the refspecs it tested |
| DOC-9: LL-PUSH-FORM text (line 56) omits `--set-upstream` | Canonical regex (line 661) accepts `-u|--set-upstream` | Text lists both | Minor | 02 Stale Documentation |
| DOC-10: Design line 493 "never restricted" (D19-1) | The DECIDED unknown policy restricts some humans (G-11) | Line 493 narrowed | Important | 01 §4. No code contradicts it today because no L2 code exists |
| DOC-11: git-scm git-hook page (2.55.0) on `hook.<event>.enabled` vs the 2.98.0 draft release note | The page reads as if it already disables hookdir hooks; the release note says that is unreleased | — | Minor | External discrepancy (web-01 F). Relevant to BP-12 |

### 4.5 Other cross-file contradictions

| Topic | File A | File B | Stronger evidence |
|---|---|---|---|
| Is `--path-format=absolute --git-path hooks/pre-push` verified? | 04 Gaps: not exercised | web-01 D3: exercised locally from a linked worktree; returned the common dir and honoured `core.hooksPath`. The main checkout was run by the domain-accuracy QA re-run and fix run X1 (`qa/qa-fix-log.md`) and also returned the common dir | web-01 D3 plus the QA runs (direct later tests on 2.47.3). G-26 resolved |
| Do API, smart-HTTP and library pushes bypass pre-push? | 04 Gaps: [UNVERIFIED], not testable locally | web-01 Areas H and J: official docs and maintainer statements | web-01. Status: documented externally (web-01 H/J); not confirmed at runtime |
| Which rejected refs reach the hook | Design D19-47 (line 534) | 04 E23a and web-01 Area I (`transport.c` skip list) | 04 + web-01 (observation plus source). See DOC-1 |
| Malformed records from git | 04 D19-42: none observed, "CONFIRMED for the tested scope" | web-01 G5: six fields from `'HEAD@{0 days ago}:refs/heads/main'` | web-01 G5. See DOC-8 |

---

## 5. External Research Findings

Everything in this section is **external context**. The sources are web pages, man pages, git source at tag v2.47.3, and two local sandbox checks run by the web researchers (`/tmp/web01-exp.*` and `/tmp/web02-sandbox.pVSjes6U`, both removed). web-01 used WebSearch and WebFetch because tavily was unavailable (web-01 header). The "Relation to 04" column says whether a finding SUPPORTS, EXTENDS or CONTRADICTS what file 04 observed on git 2.47.3.

### 5.1 git official documentation and release notes (web-01)

| # | Finding | Source URL | Relevance | Relation to 04 |
|---|---|---|---|---|
| W1-1 | githooks pre-push contract. argv holds the remote name and the URL. stdin holds `<local-ref> SP <local-oid> SP <remote-ref> SP <remote-oid> LF`. A nonzero exit aborts the push "without pushing anything". The installed 2.47.3 man page matches the web page | https://git-scm.com/docs/githooks | HIGH | SUPPORTS E19, E24, E26 |
| W1-2 | Docs say field 1 is "supplied as it was originally given". They do not say field 3 is fully qualified. The code guarantees it: `transport.c` writes `r->name` in field 3 (lines 1322-1324) | https://git-scm.com/docs/githooks; https://github.com/git/git/blob/v2.47.3/transport.c | HIGH | EXTENDS (explains 04's "field 3 is authoritative") |
| W1-3 | "Hooks that don't have the executable bit set are ignored" | https://git-scm.com/docs/githooks | HIGH | SUPPORTS E29 |
| W1-4 | The wording "after it has checked the remote status, but before anything has been pushed" is not in githooks. The code shows the same timing: the hook runs after ref matching and the lease and status checks, and before any pack is sent | https://github.com/git/git/blob/v2.47.3/transport.c | MEDIUM | EXTENDS |
| W1-5 | `transport.c` lines 1315-1319 skip four statuses: non-fast-forward, stale lease, remote-updated and up-to-date. "Fetch first" is not skipped. The hook starts before the loop, so empty stdin is normal. EPIPE is tolerated (lines 1327-1329) | https://github.com/git/git/blob/v2.47.3/transport.c | HIGH | SUPPORTS E12, E23b, E27a; EXPLAINS E23a; CONTRADICTS design D19-47 |
| W1-6 | `--no-verify`: "the hook is bypassed completely" | https://git-scm.com/docs/git-push | HIGH | SUPPORTS E14 |
| W1-7 | `--dry-run`: "Do everything except actually send the updates" | https://git-scm.com/docs/git-push | HIGH | SUPPORTS E13 |
| W1-8 | `--atomic` is a remote-side transaction. The local whole-push abort comes from githooks and does not depend on `--atomic` | https://git-scm.com/docs/git-push | MEDIUM | SUPPORTS E19, E24, E26 |
| W1-9 | git-push says "rejected: Git did not try to send the ref at all". It does not document the E23a/E23b split | https://git-scm.com/docs/git-push | MEDIUM | EXTENDS (source code, W1-5, is the stronger evidence) |
| W1-10 | REMOTE GROUPS appear on the 2.55.0 page: git "continues pushing to the remaining remotes". The section is absent from 2.47.3 | https://git-scm.com/docs/git-push | MEDIUM | EXTENDS (future risk, BP-13) |
| W1-11 | `core.hooksPath`; a relative path resolves against the worktree root | https://git-scm.com/docs/git-config | HIGH | SUPPORTS E15, E16, E30 |
| W1-12 | `-c`, `--config-env` and `GIT_CONFIG_COUNT`/`KEY`/`VALUE` set config for one process | https://git-scm.com/docs/git-config | HIGH | EXTENDS (not tested in 04; BP-3) |
| W1-13 | `advice.ignoredHook` controls the skipped-hook hint | https://git-scm.com/docs/git-config | MEDIUM | SUPPORTS E29b |
| W1-14 | `extensions.worktreeConfig` lets `config.worktree` override shared config | https://git-scm.com/docs/git-config, https://git-scm.com/docs/git-worktree | HIGH | SUPPORTS E31 |
| W1-15 | gitrepository-layout: the private hooks dir "is ignored if $GIT_COMMON_DIR is set and "$GIT_COMMON_DIR/hooks" will be used instead". git-worktree says to use `rev-parse --git-path` | https://git-scm.com/docs/gitrepository-layout, https://git-scm.com/docs/git-worktree | HIGH | SUPPORTS E30 |
| W1-16 | Local check: from a linked worktree, `git rev-parse --path-format=absolute --git-path hooks` returns the common dir. It honours `core.hooksPath`, resolves a relative value against the worktree root, and reflects `-c` | https://git-scm.com/docs/git-rev-parse (+ local test) | HIGH | EXTENDS (closes 04 gap G-26) |
| W1-17 | `git hook run --to-stdin` exists in 2.47.3 and can feed synthetic stdin in tests | https://git-scm.com/docs/git-hook | MEDIUM | EXTENDS |
| W1-18 | Config-defined hooks (2.54.0) and parallel hooks (2.55.0). Whether `hook.<event>.enabled=false` acts as a bypass is not settled | https://git-scm.com/docs/git-hook | MEDIUM | EXTENDS (future risk; see W1-27) |
| W1-19 | `refs//heads/main` is an invalid ref. `git push` fails with `fatal: invalid refspec` and the hook never runs (local test) | https://git-scm.com/docs/git-check-ref-format | MEDIUM | EXTENDS (closes G-29) |
| W1-20 | `refs/heads/Main` is valid and distinct from `main` (local test) | https://git-scm.com/docs/git-check-ref-format | LOW-MEDIUM | SUPPORTS E25 |
| W1-21 | In one dry-run test of creates, records came in command-line order. No order is documented and the code does not sort | https://github.com/git/git/blob/v2.47.3/transport.c | MEDIUM | Agrees with 04 E7; CONTRADICTS the order seen in 04 E9, E19 and E24 (E24 is the stronger evidence: two runs, same stream whichever position the protected ref had). Order is undocumented and was observed both ways, so the guard must scan every record and not depend on order |
| W1-22 | `--mirror` together with a refspec, or with `remote.origin.mirror=true`, fails: `fatal: --mirror can't be combined with refspecs` (local test) | https://git-scm.com/docs/git-push | MEDIUM | EXTENDS (closes G-30) |
| W1-23 | `'HEAD@{0 days ago}:refs/heads/main'` produces a six-field record. Only fields 2-4 are free of spaces. The fix is to right-split each line into four fields (`rsplit(" ", 3)`) (local test) | https://git-scm.com/docs/githooks, https://git-scm.com/docs/git-check-ref-format | HIGH | CONTRADICTS 04's "four fields every time" for an input 04 did not test (DOC-8) |
| W1-24 | `git send-pack` does not run pre-push. receive-pack runs on the server. A smart-HTTP POST to `$GIT_URL/git-receive-pack` does not run it | https://git-scm.com/docs/git-send-pack, https://git-scm.com/docs/gitprotocol-http | HIGH | SUPPORTS E17; EXTENDS (smart-HTTP untested in 04) |
| W1-25 | These do not run pre-push: libgit2 ("We will not be executing any hooks directly."), pygit2, dulwich ("✗ pre-push"), isomorphic-git (`onPrePush` callback only), the GitHub REST refs API and `gh api`. These do: JGit (`PrePushHook`, since 4.2) and GitPython (it shells out to `git push`, and `no_verify=True` maps to `--no-verify`) | https://github.com/libgit2/libgit2/issues/964; https://www.pygit2.org/remotes.html; https://github.com/jelmer/dulwich/blob/main/docs/c-git-compatibility.txt; https://isomorphic-git.org/docs/en/push; https://github.com/eclipse-jgit/jgit/blob/master/org.eclipse.jgit/src/org/eclipse/jgit/hooks/PrePushHook.java; https://github.com/gitpython-developers/GitPython/blob/main/git/remote.py; https://docs.github.com/en/rest/git/refs; https://cli.github.com/manual/gh_api | HIGH (JGit and isomorphic-git MEDIUM) | EXTENDS (04 could not test libraries; G-2) |
| W1-26 | The bypass list at design line 520 is CONFIRMED (J11) but imprecise. "Programmatic" pushes are not uniform, since JGit and GitPython run the hook. The list omits `--config-env`/`GIT_CONFIG_COUNT`, a worktreeConfig hooksPath and `hook.pre-push.enabled` | web-01 Area J (sources above) | HIGH | SUPPORTS D19-30 local forms (E14-E17); EXTENDS the list |
| W1-27 | Discrepancy: the 2.55.0 git-hook page reads as if `hook.<event>.enabled` already disables hookdir hooks. The 2.98.0 draft release note says that change is unreleased | https://git-scm.com/docs/git-hook; https://github.com/git/git/blob/master/Documentation/RelNotes/2.98.0.adoc | MEDIUM | EXTENDS (future bypass BP-12; DOC-11) |
| W1-28 | Community search: no primary mailing-list thread on hook behaviour. The closest hit is about message wording. A Stack Overflow question on empty pre-push stdin exists but could not be fetched | https://lore.kernel.ime.usp.br/git/d6161449aa19aebeb4c3bea1a751e8b5%40manjaro.org/T/; https://stackoverflow.com/questions/55112847/git-pre-push-hook-stdin-is-empty | LOW | Neither (source code and 04 are stronger) |

### 5.2 Linux publication primitives and git's executable check (web-02)

| # | Finding | Source URL | Relevance | Relation to 04 |
|---|---|---|---|---|
| W2-1 | git v2.47.3 decides that a hook is present only through `access(path, X_OK)` (`hook.c` line 21). A missing or non-executable hook makes `find_hook` return NULL, and `transport.c` lines 1295-1296 return 0 so the push proceeds | https://github.com/git/git/blob/v2.47.3/hook.c; https://github.com/git/git/blob/v2.47.3/transport.c | HIGH | SUPPORTS and EXPLAINS E29 |
| W2-2 | The `advice.ignoredHook` hint prints only on EACCES with the advice enabled, once per hook name per process (`hook.c` lines 34-44). Turning the advice off never changes the outcome. A missing hook prints nothing | https://github.com/git/git/blob/v2.47.3/hook.c; https://github.com/git/git/blob/v2.47.3/Documentation/config/advice.txt | HIGH | SUPPORTS E29a, E29b |
| W2-3 | `access()` checks the real UID/GID. Root needs at least one execute bit. A noexec mount gives EACCES. Mode 0700 owned by a different user also fails open | https://man7.org/linux/man-pages/man2/access.2.html | HIGH | EXTENDS E29 (further fail-open causes) |
| W2-4 | An executable hook that exits nonzero, or that git cannot start, aborts the push (`transport.c` lines 1305-1307; line 1410 is `TRANSPORT_PUSH_NO_HOOK`). Failures inside the hook fail closed. Only the path and X_OK check fails open | https://github.com/git/git/blob/v2.47.3/transport.c | HIGH | SUPPORTS E19 |
| W2-5 | The hook path is the git-path `hooks/pre-push`. `core.hooksPath` redirects it (`path.c` lines 402-405); otherwise `path.c` line 104 (`common_list`) sends it to the common dir | https://github.com/git/git/blob/v2.47.3/path.c | HIGH | SUPPORTS E30, E31 |
| W2-6 | On ENOEXEC git retries the hook with `sh` (`run-command.c` lines 415-419 and 850-854). The `.exe` fallback applies only on Windows (`config.mak.uname`) | https://github.com/git/git/blob/v2.47.3/run-command.c; https://github.com/git/git/blob/v2.47.3/config.mak.uname | MEDIUM | EXTENDS |
| W2-7 | `link`/`linkat`: "If newpath exists, it will not be overwritten." Errors include EXDEV across mounts and EPERM where hard links are unsupported | https://man7.org/linux/man-pages/man2/link.2.html | HIGH | EXTENDS (publication is not covered by 04) |
| W2-8 | Writing in place with `O_CREAT|O_EXCL` gives EEXIST on a lost race, but readers can see a partly written file | https://man7.org/linux/man-pages/man2/open.2.html | MEDIUM | EXTENDS |
| W2-9 | `O_TMPFILE` + `linkat` needs Linux 3.11 and, on overlayfs, kernel 6.10. It returned ENOTSUP on this host's overlay `/tmp` (kernel 6.8.0-147) | https://man7.org/linux/man-pages/man2/open.2.html; https://lkml.iu.edu/hypermail/linux/kernel/2405.2/05667.html | HIGH | EXTENDS |
| W2-10 | `rename`/`os.replace` replaces an existing file silently, so a lost race gives no error | https://man7.org/linux/man-pages/man2/rename.2.html; https://docs.python.org/3/library/os.html | HIGH | CONTRADICTS the no-replace requirement (not a 04 observation) |
| W2-11 | `renameat2 RENAME_NOREPLACE` needs kernel 3.15 and glibc 2.28. It worked on this host's overlay. Python `os` does not expose it | https://man7.org/linux/man-pages/man2/rename.2.html; https://docs.python.org/3/library/os.html | MEDIUM | EXTENDS |
| W2-12 | The creation mode is `mode & ~umask`, while `fchmod` sets the mode exactly. Observed: 0755 under umask 077 became 0700, and `fchmod(0755)` gave 0755 | https://man7.org/linux/man-pages/man2/chmod.2.html; https://man7.org/linux/man-pages/man2/umask.2.html | HIGH | EXTENDS |
| W2-13 | Crash durability needs `fsync` of the file before publication and `fsync` of the directory after. `publish()` does neither. For a hook, a name lost in a crash is an E29-style fail-open | https://man7.org/linux/man-pages/man2/fsync.2.html; https://lwn.net/Articles/323412/; https://lwn.net/Articles/323170/; https://www.kernel.org/doc/mirror/ols2009.pdf | MEDIUM | EXTENDS |
| W2-14 | Discrepancy: open(2) BUGS says kernels without `O_TMPFILE` return EISDIR or ENOENT, but the glibc manual says EINVAL. Any use of `O_TMPFILE` must treat all of these, plus EOPNOTSUPP, as "unsupported" | https://man7.org/linux/man-pages/man2/open.2.html; https://snapshots.sourceware.org/glibc/trunk/latest/manual/html_node/Open_002dtime-Flags.html | LOW | Neither |
| W2-15 | End-to-end sandbox on git 2.47.3. Publication was temp file with `O_EXCL`, `fchmod 0755`, `fsync`, `link`, unlink, then directory `fsync`, and it installed the hook. A second install raised EEXIST, left the hook unchanged and left no temp file. A push to main was refused with rc 1 and "L2 guard: push to refs/heads/main refused". A feature push succeeded with rc 0. The same hook at mode 0644 was skipped with the hint, and main was pushed. web-02's driver was not kept and its output shows exit codes only, no remote-ref listing; the remote-ref state was shown by Gate 3 fix run X4 (`qa/qa-fix-log.md`): the bare remote had no refs before and after both refused main pushes, and `refs/heads/feature` after the allowed feature push | local experiment (`/tmp/web02-sandbox.pVSjes6U`, removed); fix run X4 | HIGH | SUPPORTS E19, E29c |

Primitive comparison (condensed from web-02's primitive comparison table):

| Primitive | Replaces existing target | Atomic for readers | Lost-race error | Requirement |
|---|---|---|---|---|
| `open(final, O_CREAT|O_EXCL)` in place | no | no | EEXIST | any Linux |
| temp `O_EXCL` + `link`/`linkat` (the `publish()` pattern) | no | yes | EEXIST | same mount; hard-link support |
| `O_TMPFILE` + `linkat` | no | yes | EEXIST | Linux 3.11+; overlayfs 6.10 |
| `rename` / `os.replace` | yes, silently | yes | none | any |
| `renameat2 RENAME_NOREPLACE` | no | yes | EEXIST | Linux 3.15, glibc 2.28; ctypes from Python |
| `fchmod(fd, mode)` | n/a | n/a | EPERM, EROFS | umask does not apply |

### 5.3 Version table

Release-note URLs have the form `https://github.com/git/git/blob/master/Documentation/RelNotes/<version>.adoc` (web-01 F2).

| Behaviour | Introduced in | Release-note URL | Present in 2.47.3 |
|---|---|---|---|
| pre-push hook run by `git push`; a nonzero exit aborts the push | 1.8.2 | https://github.com/git/git/blob/master/Documentation/RelNotes/1.8.2.adoc (line 167) | yes (E1-E31) |
| `git push --no-verify` bypasses pre-push | 1.8.2 in code; documented from 1.8.4 | No release note. Source `v1.8.2:builtin/push.c` line 439; commit https://github.com/git/git/commit/90d32d1ffa36390177990cb92e4e2a68c5ec4092 | yes (E14) |
| `git worktree` (linked worktrees share refs, objects and hooks) | 2.5.0 (inferred: the note does not name the command) | https://github.com/git/git/blob/master/Documentation/RelNotes/2.5.0.adoc (line 45) | yes (E30) |
| `core.hooksPath` | 2.9.0 | https://github.com/git/git/blob/master/Documentation/RelNotes/2.9.0.adoc (line 127) | yes (E15, E16) |
| `rev-parse --git-path hooks/<hook>` honours `core.hooksPath` | 2.10.0 | https://github.com/git/git/blob/master/Documentation/RelNotes/2.10.0.adoc (line 122) | yes (web-01 D3) |
| Per-worktree config (`config.worktree`, `extensions.worktreeConfig`) | 2.20.0 | https://github.com/git/git/blob/master/Documentation/RelNotes/2.20.0.adoc (line 159) | yes (E31) |
| `git hook run` and the hook.c execution rewrite | 2.36.0 (inferred: no 2.36.0 bullet) | https://github.com/git/git/blob/master/Documentation/RelNotes/2.37.0.adoc (line 285); https://git-scm.com/docs/git-hook change list | yes |
| Fixes for hook stdout regressions after the rewrite | 2.37.0, 2.38.0 | https://github.com/git/git/blob/master/Documentation/RelNotes/2.38.0.adoc (line 295) | yes |
| `core.hooksPath` clone protection added, then reverted | added 2.39.4, reverted 2.39.5 | https://github.com/git/git/blob/master/Documentation/RelNotes/2.39.4.adoc (line 55); https://github.com/git/git/blob/master/Documentation/RelNotes/2.39.5.adoc (line 20) | reverted state: yes |
| `core.hooksPath=/dev/null` documented as "disable hooks" | 2.50.0 (documentation only) | https://github.com/git/git/blob/master/Documentation/RelNotes/2.50.0.adoc (line 313) | behaviour yes (E15); doc sentence no |
| pre-push in `transport.c` moved to the hook API | 2.54.0 | https://github.com/git/git/blob/master/Documentation/RelNotes/2.54.0.adoc (line 213) | no (2.47.3 uses `find_hook` + `start_command`) |
| Hooks defined in configuration | 2.54.0 | https://github.com/git/git/blob/master/Documentation/RelNotes/2.54.0.adoc (line 67) | no |
| Parallel configured hooks | 2.55.0 | https://github.com/git/git/blob/master/Documentation/RelNotes/2.55.0.adoc (line 7) | no |
| Remote groups in `git push` (keep pushing after a failure) | after 2.47.3 (exact version not found) | not found; https://git-scm.com/docs/git-push "REMOTE GROUPS" | no |
| `hook.<event>.enabled=false` also disables hooks-directory hooks | unreleased (master draft 2.98.0) | https://github.com/git/git/blob/master/Documentation/RelNotes/2.98.0.adoc (line 104) | no |

### 5.4 External recommendations and where this report uses them

| Source | Recommendation (short) | Used in |
|---|---|---|
| web-01 R1 | Parse by right-splitting. Do not refuse records with more than four fields, or name that form in the diagnostic | T-4, SC-8, BP-14, DOC-8 |
| web-01 R2 | Compare field 3 exactly and case-sensitively; no normalisation | T-3, SC-10 |
| web-01 R3 | Empty stdin allows; an early nonzero exit is safe | T-5, T-6, SC-11 |
| web-01 R4 | Install and check through `rev-parse --path-format=absolute --git-path`, and check `git config --worktree` | L-2, L-3, SC-17 |
| web-01 R5 | L1 coverage list: `--no-verify`, `-c core.hooksPath`, `-c hook.pre-push.*`, `--config-env`, `GIT_CONFIG_*`, `send-pack`, `gh api` writes to refs, curl to `git-receive-pack`; in-process library pushes recorded as a limitation | 4.2 and 4.3 |
| web-01 R6 | Tests for "fetch first", the six-field record, SHA-256, a linked worktree and a `config.worktree` hooksPath | SC-6, SC-8, SC-9, SC-17 |
| web-01 R7 | Pin the git version assumption | BP-12, BP-13 |
| web-01 R8 | Revise design line 534 | DOC-1 |
| web-02 R1 | `publish()` shape with an executable `fchmod` and fsync of the file and the directory | L-4, SC-19 |
| web-02 R2 | Set the mode with `fchmod`, not with the open mode | L-5, SC-20 |
| web-02 R3 | Resolve the path with `rev-parse --path-format=absolute`; fail if the directory is missing | L-2 |
| web-02 R4 | Treat `FileExistsError` as "compare", never as success | L-7, SC-18 |
| web-02 R5 | Verify X_OK after install and check for noexec | L-8, SC-20 |
| web-02 R6 | No rename or replace; do not depend on `O_TMPFILE` or `renameat2` | L-6 |
| web-02 R7 | Never set `advice.ignoredHook=false` | L-10 |
| web-02 R8 | The executable bit makes L2 easy to disable, so a pre-flight check is needed | G-8, BP-6 |

### 5.5 External Research Summary

- **The contract is confirmed at source level.** githooks(5) for 2.47.3 matches the web page. `transport.c` at v2.47.3 explains file 04's observations:
  - Field 3 is `r->name`, so it is always fully qualified.
  - Exactly four rejection statuses are filtered, so "fetch first" reaches the hook. This corrects D19-47.
  - The hook starts even when there are no records.
  - EPIPE is tolerated.

  An exact, case-sensitive compare of field 3 is enough. The one parsing trap is that git itself can send more than four fields for an expression source, so the guard must right-split (web-01 G5, against D19-42/D19-23).
- **Placement uses a path that git resolves.** `rev-parse --path-format=absolute --git-path hooks/pre-push` covers linked worktrees, `core.hooksPath` (since 2.10.0) and the per-worktree override (since 2.20.0).
- **The hook is easy to skip.** Ways around it:
  - For one command: `--no-verify`, or a hooksPath set through `-c`, `--config-env` or `GIT_CONFIG_*`.
  - Persistently: a hooksPath in a config file, or a cleared executable bit. git fails open on the second and prints a hint that can be silenced.
  - Outside the git CLI: `send-pack` (observed, E17), and, documented externally (web-01 H/J) but not confirmed at runtime, smart-HTTP POSTs, the GitHub REST refs API, `gh api`, and in-process libraries (libgit2/pygit2, dulwich, isomorphic-git). Per the same documentation JGit and GitPython do run the hook.

  Several of these are ALLOWED or PARTIAL in L1 (4.3). So L1 plus L2 does not refuse "every push form" from a same-user agent, which matches design D19-32 and file 02's conclusion that server-side protection is the real control.
- **Publication has a tested standard-library recipe.** It is the existing `publish()` shape with `fchmod` to an executable mode and fsync of the file and the directory. It never replaces an existing file, and it was proven end to end on git 2.47.3 (W2-15 by exit codes; the remote refs before and after are shown by Gate 3 fix run X4, `qa/qa-fix-log.md`). `rename`/`os.replace` must not be used, and `O_TMPFILE` fails on this host's overlay `/tmp`.
- **Version risk.** All of the above was tested on 2.47.3 only; it is not claimed for later versions. Re-run the Phase 6 real-git suite (Section 8) before relying on any version at or above 2.54.0 (the pre-push hook API rewrite and configured hooks, 5.3; parallel configured hooks from 2.55.0) and when 2.98.0 ships (its draft makes `hook.pre-push.enabled=false` another bypass, which L1 would then have to cover). The guard tests record `git --version`.

---

## 6. Options Analysis

The design constraint is `docs/designs/sc-issue-launch-level-hook.md` lines 510-514 (re-read 2026-11-08 by synth-03). Line 510: "one owned shared `hooks/pre-push` plus a private-worktree marker, no config change, and no push-hook forwarding". Line 512: "Do not enable `extensions.worktreeConfig`, migrate `core.hooksPath`, shadow foreign hooks, generate name-only stubs, or buffer/replay someone else's push hook in this increment." Line 514: "Conflict or unsupported lookup: preserve all existing files/configuration; report `W-L2-ABSENT` with the reason." Evidence tags in Sections 6-8: `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, `[UNVERIFIED]` (only in Open Questions), `[EXTERNAL]` (web research, with source URL), `[OBSERVED 2.47.3]` (file 04 or a web-file sandbox run on the installed git). These are proposals for a brainstorm; nothing here changes code.

The options differ on three axes: **where the hook lives** (placement), **how it is published** (no-replace install) and **how it identifies the actor** (selector call). Placement is the axis that decides design 19.2 compliance; publication and identity are shared sub-choices described once after the three placement options.

```
                      git push (from main checkout or linked worktree)
                                        |
            git resolves hooks/pre-push through the git-path machinery
            (path.c line 104 common dir; lines 402-403 core.hooksPath)  [EXTERNAL web-02]
                                        |
      +---------------------------------+----------------------------------+
      |                                 |                                  |
 Option A                          Option B                           Option C
 default lookup                    core.hooksPath set (global/local)  extensions.worktreeConfig=true
 <common>/.git/hooks/pre-push      <dir>/pre-push, e.g. under         + core.hooksPath in
 (E30: linked worktree uses it;    ~/.claude/hooks                    .git/worktrees/<id>/config.worktree
 private-dir hooks/ ignored)       (E15/E16, web-01 C1)               (E31, web-01 C4)
      |                                 |                                  |
 19.2 COMPLIANT                    EXCLUDED by 19.2                   EXCLUDED by 19.2
```

### 6.1 Option A: Owned shared hook in the default common-dir lookup

**Placement.** One owned `pre-push` at the path printed by `git rev-parse --path-format=absolute --git-path hooks/pre-push`, run from the target worktree, installed only when `core.hooksPath` is unset (the "supported default" of design line 512).

| Evidence | Source |
|---|---|
| A linked worktree's default lookup is the common dir `clone/.git/hooks/pre-push`; a hook in the worktree-private git dir is ignored (Section 2.5(c)) | [OBSERVED 2.47.3] 04 E30; [EXTERNAL] gitrepository-layout(5) `hooks` entry, https://git-scm.com/docs/gitrepository-layout (web-01 D1) |
| `--path-format=absolute --git-path hooks` resolves the common dir from a linked worktree and honours `core.hooksPath` (since 2.10.0) | [OBSERVED 2.47.3] web-01 D3a, D3c-e; [EXTERNAL] RelNotes 2.10.0 line 122, https://github.com/git/git/blob/master/Documentation/RelNotes/2.10.0.adoc |
| `--git-path` is relative in the main clone and absolute in a linked worktree; `l2_status` joins a relative answer to the worktree (Section 2.3) | [OBSERVED 2.47.3] 04 E30; [CODE-VERIFIED] `orca_worktree.py` lines 1012-1029 (03) |
| `git worktree remove` deletes a private-dir marker; the shared hook stays | [OBSERVED 2.47.3] 04 F2 |
| One hook file serves every worktree, so the hook decides per push which actor it serves | [EXTERNAL] web-01 D1 (design 19.4 "shared hook file") |

**Publication.** A new raw-bytes, executable-mode variant of the `publish()` pattern (see 6.4). **Identity.** `~/.claude/hooks/launch-job-identity.sh identify` with no PID (see 6.5).

| Criterion | Assessment | Evidence |
|---|---|---|
| Effort | Medium. New code: hook body, raw-bytes publisher, ownership check, self-test, reason-bearing `W-L2-ABSENT`; `install_hooks.py` has no git-hook path today (Section 2.4) | [CODE-VERIFIED] 03 "Design gaps for an L2 installer"; 01 §6 |
| Risk | Medium. Same-user agent can still edit, delete or `chmod -x` the hook file (no `.git/hooks` tamper token in L1 line 706, Section 2.1), and per-process bypasses remain | [CODE-VERIFIED] 02 Gap 1; [OBSERVED 2.47.3] 04 E14-E17, E29, E31 |
| Reuse: `publish()` | Pattern reused, function not: `publish()` JSON-encodes the payload, sets mode 0400 and sits inside the heredoc, so it is not importable (Section 2.2) | [CODE-VERIFIED] 01 §6, `launch-job-identity.sh` lines 164-174; web-02 Discrepancy 1 |
| Reuse: `identify` | Reused unchanged; selector returns governed/ordinary/unknown on stdout with exit 0; hook must map "no verdict" to `unknown` | [CODE-VERIFIED] 01 §4 items 1-3 (lines 225, 241, 242, 244, 536) |
| Reuse: `l2_status` | Reused as the probe; it already resolves the path with `rev-parse --git-path hooks/pre-push` | [CODE-VERIFIED] 03, ow:1020 |
| Files affected | `src/superclaude/hooks/scripts/` (new hook body), `src/superclaude/cli/install_hooks.py` (`_FRESHNESS_SCRIPTS`), `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` (`cmd_launch`, `l2_status`, `L2_ABSENT_WHY`), `src/superclaude/hooks/scripts/launch-level-guard.sh` (line 706 token), plugin mirrors, tests | 01 §8; 03 Summary; 02 line 168 |
| Pros | Matches the git default with no config change; covers linked worktrees through the common dir; probe code already uses the same path resolution; no-replace publish proven end to end | 04 E30; web-02 Area 3 steps 8a-8f (exit codes); Gate 3 fix run X4 (remote refs before/after, `qa/qa-fix-log.md`) |
| Cons | Shared with the person's own pushes in every worktree of the repository; fails open when the exec bit is cleared; bypassed by `--no-verify`, `-c core.hooksPath`, `send-pack`, library and API pushes; L1 does not protect the file | 04 Key Takeaways; web-02 Area 1; 02 Summary; historical rejection at `.dev/brainstorms/20261105-170229-launch-level-hook/adversarial/adversarial/refactor-plan.md:1158` (03) |
| **Design 19.2 compliance** | **Compliant.** One owned shared hook in the default lookup; no `extensions.worktreeConfig`; no `core.hooksPath` migration; no forwarding or shadowing (a foreign `pre-push` or a set `core.hooksPath` leads to `W-L2-ABSENT`, never to installation) | design lines 510-514 |

### 6.2 Option B: Dedicated `core.hooksPath` directory (for example under `~/.claude/hooks`)

**Excluded by design 19.2; would reopen the decision.** Kept only as a comparison point.

**Placement.** Set `core.hooksPath` (repository or global scope) to a directory owned by the installer, for example under `~/.claude/hooks/`, and put the guard there.

| Criterion | Assessment | Evidence |
|---|---|---|
| Effort | Medium-high. Needs the same hook body and publisher as A, plus a config write and a plan for every other hook name that the redirected directory would now hide | [EXTERNAL] git-config(1) core.hooksPath: hooks are looked up "in that directory ... instead of in $GIT_DIR/hooks", https://git-scm.com/docs/git-config (web-01 C1) |
| Risk | High for coexistence: redirecting the hooks directory hides every existing hook (`pre-commit`, `commit-msg`) unless they are forwarded, which 19.2 forbids. Per-process `-c core.hooksPath=` still overrides it | web-01 C1, C2; [OBSERVED 2.47.3] 04 E15/E16 |
| Reuse: `publish()` | Same as A (pattern only) | 01 §6 |
| Reuse: `identify` | Same as A | 01 §4 |
| Files affected | As A, plus a git-config writer (new code) | 03 "Design gaps" |
| Pros | The existing L1 `*.claude/hooks*` tamper token (line 706) would already protect the hook files from Edit/Write and spelled Bash paths, and the `hookspath` token (line 532) already refuses changing `core.hooksPath` through git | [CODE-VERIFIED] 02 line 169 |
| Cons | Config migration; hides other hooks; a relative `core.hooksPath` resolves per worktree root inside the agent-editable working tree; `hookspath` token applies only when a git word is present (line 525), so a direct config-file write escapes it | [OBSERVED 2.47.3] 04 E30d, web-01 D3d; [CODE-VERIFIED] 02 Gap 3 |
| **Design 19.2 compliance** | **Not compliant: "migrate `core.hooksPath`" is forbidden (line 512). Excluded by design 19.2; would reopen the decision.** | design line 512 |

### 6.3 Option C: Per-worktree `core.hooksPath` with `extensions.worktreeConfig`

**Excluded by design 19.2; would reopen the decision.** Kept only as a comparison point.

**Placement.** Enable `extensions.worktreeConfig` and write `core.hooksPath` into the governed worktree's `config.worktree`, so only that worktree uses the guard directory.

| Criterion | Assessment | Evidence |
|---|---|---|
| Effort | High. Enabling a repository extension plus per-worktree config writes and cleanup on release | [EXTERNAL] git-worktree(1) CONFIGURATION FILE: "Older Git versions will refuse to access repositories with this extension", https://git-scm.com/docs/git-worktree (web-01 D1) |
| Risk | High. The extension changes how every git in the repository reads config; a per-worktree value "will override settings from any other config files", which is also the very bypass an agent can use against Option A | [EXTERNAL] git-config(1) extensions.worktreeConfig (web-01 C4); [OBSERVED 2.47.3] 04 E31 |
| Reuse: `publish()` | Same as A (pattern only) | 01 §6 |
| Reuse: `identify` | Same as A; per-worktree placement would not remove the need for actor selection because a human can push from the same worktree (design 19.5 actor cases) | 01 §4; design line 532 |
| Files affected | As A, plus extension enablement and `config.worktree` writer (new code) | 03 "Design gaps" |
| Pros | Scopes the guard to one worktree; human pushes from sibling worktrees and the main checkout are untouched | [OBSERVED 2.47.3] 04 E31 |
| Cons | `config.worktree` is not an L1 tamper token (line 706), so the agent can rewrite it; enabling the extension is repository-wide | [CODE-VERIFIED] 02 Gap 10, Stale Documentation (LL-TAMPER partial) |
| **Design 19.2 compliance** | **Not compliant: "Do not enable `extensions.worktreeConfig`" and "migrate `core.hooksPath`" (line 512). Excluded by design 19.2; would reopen the decision.** | design line 512 |

### 6.4 Shared sub-choice 1: how the hook is published (applies to A, B and C)

| Primitive | Replaces an existing file | Reader-atomic | Verdict for the hook | Evidence |
|---|---|---|---|---|
| Copy of `publish()` pattern with raw bytes, `fchmod` to an executable mode, `fsync` file and directory, `linkat` no-replace, temp unlink in `finally` | no (EEXIST) | yes | **Use.** Proven on this host: installed mode 0755 with X_OK, second install raised EEXIST and left the hook unchanged, no temp left, push to main refused (rc 1), feature push allowed (rc 0); the bare remote's refs unchanged by the refused pushes | [OBSERVED 2.47.3] web-02 Area 3 steps 8a-8f (exit codes); Gate 3 fix run X4 (`for-each-ref` before/after, `qa/qa-fix-log.md`); [CODE-VERIFIED] `publish()` lines 164-174 (01 §6) |
| `publish()` unchanged | no | yes | **Do not use.** Mode 0400 fails `access(X_OK)`, so git skips the hook (fail-open); payload is JSON-encoded | web-02 Area 3 step 7; 01 §6 |
| `os.rename` / `os.replace` | yes, silently | yes | **Do not use** (violates "without replacing an existing file", design line 512) | web-02 Area 3 step 5; [EXTERNAL] https://man7.org/linux/man-pages/man2/rename.2.html |
| `O_TMPFILE` + `linkat` | no | yes | **Do not depend on it.** EOPNOTSUPP on this host's overlay `/tmp` (overlayfs needs 6.10; kernel is 6.8) | web-02 Area 3 step 4x; [EXTERNAL] https://man7.org/linux/man-pages/man2/open.2.html |
| `renameat2(RENAME_NOREPLACE)` | no | yes | **Not needed.** Worked here, but needs ctypes and can return EINVAL on unsupported filesystems; no gain over `linkat` | web-02 Area 3 step 6a/6b, Recommendation 6 |

Mode must be set with `fchmod` on the fd, because creation mode is masked by umask (0755 under umask 077 became 0700) [OBSERVED] web-02 Area 3 steps 1a/1b.

### 6.5 Shared sub-choice 2: how the hook identifies the actor

The verdict mapping is DECIDED by the owner (2026-11-08, seed brief line 73, recorded in 01 §4; Section 3.3): governed refuses protected; ordinary and released allow without reading the stream; `unknown` refuses only `main`/`master` with a distinct diagnostic and allows the rest. The hook must also map "no verdict" (non-zero exit, empty or unparseable stdout, unexpected `status`) to `unknown` [CODE-VERIFIED] 01 §4 item 3.

| Variant | How | Human without uv on PATH | Effort / reuse | Evidence |
|---|---|---|---|---|
| A-i: uv-backed `identify` with a fixed PATH | Hook sets PATH to include the uv directory recorded at install time, then calls `~/.claude/hooks/launch-job-identity.sh identify` with no PID | Covered (uv resolvable at script lines 25 and 566) | Lowest: selector reused unchanged; uv and Python start per push (cost not measured) | 01 §4 item 5 option (i), §8; 04 E28c |
| A-ii: hook-side no-store early exit | Hook treats an absent `$HOME/.claude/state/launch-level` as `ordinary` without calling `identify` | Covered only on machines with no store; does NOT help a human on a machine that also runs governed sessions | Small, but insufficient alone | 01 §4 item 5 option (ii) |
| A-iii: pure-shell hook | Hook does not depend on uv | Covered | Highest: research gives no design for re-implementing the selector's validation in shell; the three byte-identical copies of the selector would need a second implementation kept in step | 01 §4 item 5 option (iii), §8 Key Takeaways |
| Absolute uv path only | Hook calls uv by absolute path | **Not covered:** the script itself resolves uv through PATH at lines 25 and 566 | n/a | 01 §4 item 5; gaps note N-3 (superseded sentence at 04 line 1530) |

**Note on the stdin parser (applies to every variant).** git can itself send a record with more than four space-separated fields: `git push --dry-run origin 'HEAD@{0 days ago}:refs/heads/main'` gave a six-field record [OBSERVED 2.47.3] web-01 G5, re-run with recorded commands, hook body and output as Gate 3 fix run X2 (`qa/qa-fix-log.md`, cycle 0: `REC[6]`). A four-variable `read` puts `ago}` in field 3 and lets the protected push through [OBSERVED 2.47.3] fix run X3: the naive hook printed `field3=[ago}]` and exited 0, the real push returned rc 0, and the local bare remote had no refs before and `refs/heads/main` after. Fields 2-4 never contain spaces (`r->name` and hex oids, git v2.47.3 `transport.c` lines 1322-1324, [EXTERNAL] https://github.com/git/git/blob/v2.47.3/transport.c, web-01 Area I), so the exact parse is a right-split into four parts. This **contradicts** design 19.3's "A malformed governed stream (missing/extra fields) refuses" for the extra-fields case: web-01 G5 (local run) is the stronger evidence; file 04 never produced a malformed record (04 Gaps; its F3 follow-up tested space/tab/trailing-space in destination names only, which git refuses before the hook). See also DOC-8 in Section 4.4.

### 6.6 Options Comparison

| Criterion | Option A: default common-dir hook | Option B: dedicated `core.hooksPath` dir | Option C: per-worktree `core.hooksPath` + `extensions.worktreeConfig` |
|---|---|---|---|
| **Design 19.2 compliance** | **Compliant** (lines 510-514) | **Excluded by design 19.2; would reopen the decision** (migrates `core.hooksPath`) | **Excluded by design 19.2; would reopen the decision** (enables `extensions.worktreeConfig`, migrates `core.hooksPath`) |
| Config change | None | Repository or global `core.hooksPath` | Repository extension + `config.worktree` |
| Effect on existing hooks (`pre-commit`, `commit-msg`) | Untouched (design line 510) | Hidden unless forwarded (forwarding forbidden) | Hidden in that worktree unless forwarded |
| Linked worktree coverage | Yes, common dir (E30) | Yes for an absolute path; a relative path resolves per worktree root (E30d, web-01 D3d) | Only the configured worktree (E31) |
| Path resolution already in code | Yes, `l2_status` uses `rev-parse --git-path hooks/pre-push` (ow:1020) | Same call honours `core.hooksPath` (2.10.0) | Same call honours it (web-01 D3c-e) |
| Publication | Raw-bytes executable variant of `publish()` pattern (web-02 Area 3 step 8) | Same | Same |
| Actor identification | `identify` + fixed PATH (A-i) | Same | Same (still needed: human and agent can share a worktree, design line 532) |
| L1 protection of the hook file today | None (no `.git/hooks` token, line 706) | Yes, `*.claude/hooks*` token and `hookspath` token (02 line 169) | None (`config.worktree` not a token) |
| Per-process bypass (`--no-verify`, `-c core.hooksPath=`, `--config-env`, `GIT_CONFIG_COUNT`) | Bypassable (E14-E16, web-01 C2) | Bypassable | Bypassable (`-c` beats `config.worktree`, web-01 C4) |
| Exec-bit fail-open (E29) | Yes | Yes | Yes |
| `send-pack`, libgit2/pygit2, dulwich, isomorphic-git, REST/`gh api`, raw smart-HTTP | Bypass (E17, web-01 J10) | Bypass | Bypass |
| Effort | Medium | Medium-high | High |
| Coexistence risk | Low (refuses to install on conflict) | High | High |

Reading of the table: A and B have the same bypass surface for pushes; B's only advantage is that L1 already protects `~/.claude/hooks`. That advantage can be obtained for A by adding `*.git/hooks*` and `*hooks/pre-push*` to L1 line 706 (02 line 168), without a config migration. C adds risk (repository extension) and gains only per-worktree scoping, which the identity selector already provides by actor.

---

## 7. Recommendation

**Recommended: Option A (owned shared hook in the default common-dir lookup), with identity variant A-i (uv-backed `identify` called under a fixed PATH that holds the install-time uv directory, read at run time from an owned sibling file so the hook bytes stay identical to the packaged source; Phase 1.2) and the raw-bytes executable `publish()`-pattern installer.** No reopening of design 19.2 is recommended.

| Reason | Comparison-table row (6.6) | Evidence |
|---|---|---|
| A is the only option that complies with 19.2; B and C would reopen it | "Design 19.2 compliance" | design lines 510-514 |
| A, B and C have an identical push-bypass surface, so B and C buy no extra protection for the push itself | "Per-process bypass", "Exec-bit fail-open", "`send-pack` ... smart-HTTP" | 04 E14-E17, E29; web-01 J10 |
| B's one real advantage (L1 already protects `~/.claude/hooks`) is reachable for A by a token change in L1, not a config migration | "L1 protection of the hook file today" | 02 lines 168-169 |
| A leaves `pre-commit`, `commit-msg` and every other hook untouched; B and C hide them unless forwarded, which 19.2 forbids | "Effect on existing hooks" | design line 510, 512 |
| A already matches the path resolution the claim code uses | "Path resolution already in code" | `l2_status` ow:1012-1029 [CODE-VERIFIED] |
| A's installer pattern is proven end to end on this host: `publish_exec` installs at 0755 and refuses to replace (EEXIST), and the installed right-split guard refuses both main pushes with the bare remote's refs unchanged before and after, while a feature push succeeds | "Publication" | web-02 Area 3 steps 8a-8f (exit codes); Gate 3 fix run X4 (`qa/qa-fix-log.md`, `for-each-ref` before/after) |
| A-i is the only identity variant that covers a human without uv on PATH with no second selector implementation | 6.5 table | 01 §4 item 5; 04 E28c |

**Status of the identity choice.** G-6 lists the uv-PATH remedy as "design choice open: brainstorm decision". The recommendation is A-i; the brainstorm owns the final pick between A-i and A-iii (Section 9 row 1).

**What L2 under Option A does NOT stop, and who must close it.** The design already accepts that "`--no-verify`, per-process hooksPath overrides, direct send-pack and API/programmatic ref writes can bypass local pre-push; visible forms remain checked by L1" (line 520). The research confirms each class and adds more.

| Bypass | L2 result | L1 today | Proposed owner | Evidence |
|---|---|---|---|---|
| `git push --no-verify` | hook never runs | refused (not canonical form) | L1 (keep) | 04 E14; 02 Summary; [EXTERNAL] git-push(1), https://git-scm.com/docs/git-push |
| `git -c core.hooksPath=...`, `--config-env=core.hooksPath=VAR`, `GIT_CONFIG_COUNT/KEY/VALUE` env | hook never runs | `-c` form refused (`hookspath` token); `\x50` spelling and env forms evade (02 line 249) | L1 (extend: `--config-env`, `GIT_CONFIG_*`, `GIT_CONFIG_PARAMETERS`; refuse `-c` values containing `$'`, Phase 5.4(b)) | 04 E15/E16; [EXTERNAL] web-01 C2, https://git-scm.com/docs/git-config |
| Unlisted wrapper before `git` (`chrt 0 git $'\x70ush' --no-verify origin main`, `taskset`, `find -exec`; `uv run` is the same case): the wrapper skip list at guard line 549 names none of them, so the wrapper word becomes command position and the unknown-subcommand check never runs | `--no-verify` part removes L2 | allowed (G-44) | L1 (Phase 5.3) | guard line 549; 02 line 251 (lines 549, 557, 637); Section 2.1 table |
| `git send-pack` | hook never runs; force-rewrote main | refused | L1 (keep) | 04 E17; [EXTERNAL] web-01 H1 |
| Edit/Write/rm/mv/ln on `.git/hooks/pre-push` | guard removed or replaced | **allowed** (no token at line 706) | L1 (add `*.git/hooks*`, `*hooks/pre-push*`) | 02 Gap 1 |
| Edit/Write on `<hooks-dir>/pre-push.uv-dir` (proposal, step 1.2) so that it names a directory holding a fake `uv` that answers `ordinary` | hook runs, but the fake selector's `ordinary` allows the push | **allowed** (no token at line 706; the file does not exist today) | L1 (the step 5.1 tokens `*.git/hooks*`, `*hooks/pre-push*` match it) + launch-time recheck of owner, mode and content (steps 2.5(b), 4.2; SC-24, SC-31) | guard line 706; Phase 1.2, 2.5(b) |
| Same-user rewrite of a user-owned `uv` binary in the directory the file names | hook runs the rewritten `uv` | allowed (no tamper token at line 706 names a `uv` path) | **Accepted limit** (Section 9 row 41): the owner and mode checks of step 2.5(b) cannot tell the owner's own rewrite from an upgrade. On this host on 2026-11-08 `uv` is `/usr/local/bin/uv`, owned by root, mode 0755, so the case does not arise here | step 2.5(b); `qa/qa-fix-log.md` cycle 1 |
| `chmod -x` on the hook (+ `-c advice.ignoredHook=false`) | git skips it (fail-open) | allowed | L1 token above + launch-time `access(X_OK)` recheck (L2 installer) | 04 E29; web-02 Area 1 (`hook.c` lines 21, 34-46) |
| Per-worktree `core.hooksPath` via `config.worktree` | different hooks dir | allowed (`config.worktree` not a token) | L1 (add `*config.worktree*`) + launch-time effective-path recheck | 04 E31; 02 Gap 10 |
| Direct write to `.git/config` without a git word (`cd .git && >> config`) setting `core.hooksPath`, `alias.*`, `remote.origin.push` | `core.hooksPath` removes L2; `remote.origin.push` is still seen as field 3 (E20) | allowed | L1 (move `hookspath`/`alias.` out of the `LL_GIT` gate, line 525) | 02 Gap 3, line 170 |
| Underscore env prefix moving command position off `git` (`A_B=1 git $'\x70ush' --no-verify origin main`) | `--no-verify` part removes L2 | allowed at every level | L1 (fix W/command-position at lines 435, 556-557) | 02 Gap 2, Summary |
| `setsid` or a different valid HOME | selector returns `ordinary`, push allowed | n/a | Accepted limit (design 19.7 line 559 lists `setsid`; HOME escape listed nowhere) | 01 §4 item 4, Gaps 2 |
| libgit2/pygit2, dulwich, isomorphic-git (no `onPrePush`) in a script | hook never runs | allowed (library and script pushes pass) | Stated limitation; only server-side protection covers in-process pushes | [EXTERNAL] web-01 J1, J2, J4, J5 (https://github.com/libgit2/libgit2/issues/964, https://github.com/jelmer/dulwich/blob/main/docs/c-git-compatibility.txt); 02 Gap 6 |
| GitHub REST refs API / `gh api` | hook never runs | `gh api` writes and literal `api.github.com` refused; non-literal hosts not | L1 (keep; extend hosts) + server-side | [EXTERNAL] web-01 J7/J8, https://docs.github.com/en/rest/git/refs; 02 Gap 5 |
| `curl` to smart-HTTP `git-receive-pack` on `github.com` | hook never runs | **allowed** | L1 (add) | [EXTERNAL] web-01 H3, https://git-scm.com/docs/gitprotocol-http; 02 Gap 5 |
| GitPython `Remote.push(no_verify=True)` | hook never runs (maps to `--no-verify`, convention untested) | allowed (script) | Stated limitation | [EXTERNAL] web-01 J6 |
| Future git: `-c hook.pre-push.enabled=false` (unreleased 2.98.0 draft) | would disable hookdir hook | no token | L1 (add when the runtime git has it) | [EXTERNAL] web-01 F1, RelNotes 2.98.0 line 104 |

Neither layer closes the in-process library push or the API write in general; 02's Summary and web-01 J11 both conclude that server-side branch protection is the only control that does. The design's own disclaimer ("Neither layer guarantees universal AC-6 or a hostile-agent sandbox", line 520) stands.

**Launch refusal versus warning.** Design lines 355 and 514 say the governed launch must not proceed when accepted L2 is absent; the code warns and continues (`W-L2-ABSENT`, ow:1311-1312) by a documented choice (design line 574) [CODE-CONTRADICTED vs design: D19-18]. The owner has DECIDED the default (seed brief line 77): it stays off, so `W-L2-ABSENT` remains a warning. The refusal path must still be built in its own clearly marked commit, tested, and shipped switched off (seed brief line 68). This report proposes the switch mechanism (a proposal for the brainstorm, not a decision): a module constant `L2_REFUSAL_ENABLED = False` in `orca_worktree.py` that guards the refusal line now commented at ow:1309-1310, turned on in tests by monkeypatching it (Phase 4.4, 6.11). The criterion for turning it on (after #442) stays open (G-17; Section 9 row 12). Phase 4.4 in Section 8 builds the refusal behind that switch.

---

## 8. Implementation Plan

Proposed steps for the brainstorm; nothing here has been changed. File paths marked **(new)** do not exist today. Every other path was cited as existing by research files 01-03 [CODE-VERIFIED]. Line numbers are those the research recorded on 2026-11-08 and must be re-read before any edit. References of the form "Section 9 row N" point to the Open Questions table in Section 9.

```
 cmd_launch (orca_worktree.py 1253-1388)
   |
   +-- IR-4 enforcement_preflight ............ 1287-1304   (unchanged)
   +-- [new] l2_install(worktree)  ........... Phase 4.1
   |       resolve  git rev-parse --path-format=absolute --git-path hooks/pre-push
   |       check    core.hooksPath unset (repo + --worktree)       --> conflict: keep files, W-L2-ABSENT(reason)
   |       check    no foreign pre-push                            --> conflict: keep files, W-L2-ABSENT(reason)
   |       publish  O_EXCL temp -> fchmod 0755 -> fsync -> link -> unlink -> fsync dir
   |       verify   full bytes == installed source, X_OK, owner, mode, not noexec
   |       selftest ordinary+protected -> 0 ; empty stream -> 0
   +-- l2_status (1012-1029), now reason-bearing ............ Phase 4.2
   +-- W-L2-ABSENT note (1311-1312) / refusal, switch off by default ... Phase 4.3 / 4.4
   +-- publish_pending (1315) -> launch (1330-1334) -> session_report (1376)

 git push (any actor)  -->  <common-dir>/hooks/pre-push  (Phase 1 body)
   fixed PATH -> ~/.claude/hooks/launch-job-identity.sh identify
   verdict: governed | unknown | no-verdict(=unknown) -> refuse if any field 3 == refs/heads/main|master
            ordinary | released                       -> allow
```

### 8.1 Phase 1: Hook body

**Goal:** a packaged `pre-push` guard script that refuses a restricted actor's push to `refs/heads/main` or `refs/heads/master` and allows everything else, with bytes that never vary per machine.
**Dependencies:** none (first phase). Step 2.7 (installer registration) is done right after step 1.1, because `make verify-sync` fails while the new script is unregistered.

| Step | Action | Files | Details | Done when |
|---|---|---|---|---|
| 1.1 | Create the guard script source | `src/superclaude/hooks/scripts/launch-pre-push-guard.sh` **(new)**; mirror `plugins/superclaude/hooks/scripts/launch-pre-push-guard.sh` **(new)** | The name is a proposal. Mirrors the three-copy layout of `launch-job-identity.sh` (src, plugin, installed; 01 §5). The bytes of this file are what the publisher writes as `pre-push` (Phase 2), so the ownership check compares against them; nothing machine-specific is written into it (step 1.2). | Both files exist with identical bytes (`cmp` exits 0), and step 2.7 has registered the script. |
| 1.2 | Set a fixed PATH before any lookup, with the uv directory read at run time | same file; data file `<hooks-dir>/pre-push.uv-dir` **(new, proposal)** written by step 2.1 | Variant A-i. The hook bytes stay identical to the packaged source; the machine-specific uv directory lives in a separate owned file next to the hook (proposal; this report's resolution of the CRITICAL finding that a substituted `PATH=` line could never match the full-byte ownership check of 2.4). The hook reads `"$(dirname "$0")/pre-push.uv-dir"`, accepts it only if it holds exactly one absolute directory path in which `uv` is an executable file, and then sets `PATH=<that dir>:/usr/bin:/bin`. If the file is missing, unreadable, malformed or the directory holds no executable `uv`, the hook does not call `identify` and treats the call as "no verdict" with cause `uv-dir-missing` (step 1.4: maps to `unknown`). Reason for a fixed PATH: with `PATH=/usr/bin:/bin` uv is absent and `identify` exits 2 (04 E28c; 01 lines 25, 52-53). An absolute uv path alone is not enough (01 §4 item 5). Resolves G-6 if the brainstorm accepts A-i (Section 9 row 1). | SC-23 and SC-24 pass. |
| 1.3 | Call the selector by its installed entry point (proposed; conditional on Section 9 row 2) | same file | Proposed location: `~/.claude/hooks/launch-job-identity.sh identify` (01 §5; ow:803 `IDENTITY_COMMAND`). The environment reaches the hook unchanged (04 E28), so the selector sees the pusher's session. Bound the call with a timeout; a timeout is "no verdict". Missing script is "no verdict" (G-36). | Phase 6.3 cases for a missing script and a timeout each give the unknown diagnostic. |
| 1.4 | Map verdicts | same file | `governed` and `unknown` restrict; `ordinary` and `released` allow (01 lines 225, 241-244). "No verdict" (exit 2, bad args line 564, missing script, timeout, `uv-dir-missing`) maps to `unknown` (01 Gaps 1; G-7). Owner decision 2026-11-08: `unknown` refuses main/master only, with a diagnostic, and allows every other ref (seed brief line 73, cited by 01). | SC-13 to SC-16 pass. |
| 1.5 | Parse stdin records by right-splitting | same file | Split each line from the right into 4 fields (`rsplit(" ", 3)` semantics) because field 1 can contain spaces: `HEAD@{0 days ago}:refs/heads/main` produced a 6-field record (web-01 G5; Gate 3 fix run X2, `qa/qa-fix-log.md`). A naive four-variable `read` hook then saw `ago}` as field 3 and the push to `refs/heads/main` went through: exit 0, and the bare remote went from no refs to `refs/heads/main` (fix run X3, executed). Malformed = fewer than 4 fields, or fields 2/4 not hex object names → refuse when restricted. This replaces design 19.3's "extra fields refuse" (line 518), which would refuse a legitimate push. | SC-8 passes, and a Phase 6.2 malformed-line case is refused with the malformed diagnostic. |
| 1.6 | Compare field 3 exactly | same file | Refuse the whole push if any field 3 is byte-equal to `refs/heads/main` or `refs/heads/master`. Field 3 is fully qualified by code (`r->name`, transport.c v2.47.3 1322-1324; [EXTERNAL] web-01) and authoritative for every spelling tried (04 E3-E6, E11, E20, E21). Case-sensitive (web-01 G2; 04 E25); prefix names such as `refs/heads/ma` are not protected (04 F3a). One nonzero exit aborts the whole push (04 E19, E24, E26, F1). | SC-1 to SC-10 pass. |
| 1.7 | Apply the stdin rule per verdict | same file | `governed`, `unknown` and "no verdict" read stdin to EOF before any allow, so every record is checked (design 19.3 "stream until EOF"). A refusal may exit as soon as it sees a protected record; git tolerates the resulting EPIPE (transport.c 1327-1329, [EXTERNAL] web-01 Area I). `ordinary` and `released` exit 0 without reading the stream (T-10; D19-26). A hook that never read stdin still exited 0 with 3001 branches (G-42, QA sandbox). | SC-12 and SC-13 pass. |
| 1.8 | Empty stdin allows | same file | Empty streams occur for up-to-date pushes (04 E12, E23b, E27a; web-01: the hook starts even with empty stdin). Matches design line 518. | SC-11 passes. |
| 1.9 | Distinct diagnostics on stderr, and an L2 version line | same file; `orca_worktree.py` (new constant) | One message for `governed`, one for `unknown` (naming the "no verdict" cause), one for malformed. The script carries its own version header, `# launch-pre-push-guard-version: 1`, held in a new constant `L2_GUARD_VERSION_LINE` in `orca_worktree.py` (names are proposals). It is separate from the L1 constant `GUARD_VERSION_LINE` (ow:804, `"# launch-level-guard-version: 1"`), which `enforcement_preflight` checks at ow:950-951; reusing it would tie the L1 and L2 versions together. `l2_status` (Phase 4.2), not `enforcement_preflight`, checks the L2 line. The header is not ownership proof by itself (design line 512); the full-byte check of 2.4-2.5 is. | The three diagnostics differ in Phase 6.3 output, and `l2_status` returns `absent` with reason `not-owned` for an otherwise identical hook whose version line differs. |

### 8.2 Phase 2: Publisher and ownership check

**Goal:** install the Phase 1 script as the `pre-push` hook git will run, only in the safe case, never replacing a file, and prove the installed bytes are the owned ones.
**Dependencies:** Phase 1 (the script bytes are the ownership reference). Step 2.7 has no dependency besides step 1.1 and is done immediately after it.

| Step | Action | Files | Details | Done when |
|---|---|---|---|---|
| 2.1 | Add an executable no-replace publisher | `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` (new function, proposed name `publish_pre_push`) | **Source of the bytes:** the installed copy `~/.claude/hooks/launch-pre-push-guard.sh`, which `_copy_scripts` (`install_hooks.py` 251-290) writes once step 2.7 registers the script. If that file is missing or unreadable, publish nothing and report reason `guard-source-missing`. **Publication:** web-02 step 8 (`publish_exec`): `O_CREAT\|O_EXCL\|O_NOFOLLOW` temp at 0600 in the hooks dir → write → `fchmod 0755` → `fsync` → `link` to `pre-push` → `unlink` temp → `fsync` the directory. `link`/`linkat` fails with EEXIST and never replaces; readers see all or nothing ([EXTERNAL] web-02 primitives table, https://man7.org/linux/man-pages/man2/link.2.html). Re-run on git 2.47.3 by Gate 3 fix run X4 (`qa/qa-fix-log.md`): first install `ok mode 0o755`, second install EEXIST with the file unchanged; with a right-split test guard installed, both main pushes exited 1 and the bare remote listed no refs before and after, while a feature push exited 0 and created `refs/heads/feature`. `fchmod` is not masked by umask (web-02 1a/1b). Do not use `rename` (replaces) or `O_TMPFILE` (ENOTSUP on overlay /tmp, kernel 6.8; web-02). `publish()` in `launch-job-identity.sh` (164-174) cannot be reused unchanged: it writes JSON at 0400, has no fsync and sits in a heredoc, so it is not importable (01 §3). **uv-directory file (proposal, step 1.2):** the same publisher writes `<hooks-dir>/pre-push.uv-dir` at mode 0644 holding the directory of `shutil.which("uv")` in the launching process; an existing file is never replaced, and a stale one (no executable `uv` in the named directory) is reported as reason `uv-dir-missing`, not rewritten. Owner, mode and content of the file, its directory and its `uv` are checked by step 2.5(b) at install and before every launch. If `uv` cannot be found at install time, nothing is published and the reason is `uv-dir-missing`. | SC-18 (`guard-source-missing`, `uv-dir-missing`), SC-19 and SC-20 pass. |
| 2.2 | Resolve the target path with git | same | `git rev-parse --path-format=absolute --git-path hooks/pre-push` from the worktree: resolves the common dir and honours `core.hooksPath`. Verified on 2.47.3 from a linked worktree ([EXTERNAL] web-01 D3a-e, web-01 lines 193-205) and from the main checkout (`qa/qa-lens-domain-accuracy.md` finding 1; Gate 3 fix run X1, `qa/qa-fix-log.md`): both print `<common-dir>/hooks/pre-push`; with `core.hooksPath=myhooks` the main checkout prints `<repo>/myhooks/pre-push` and the linked worktree `<wt>/myhooks/pre-push`. rev-parse honours hooksPath since 2.10.0. Shared placement in the common dir is what git runs from every linked worktree (04 E30). `l2_status` already calls `rev-parse` (ow:1020, 03). Resolves G-26. | SC-17 passes from both the main checkout and a linked worktree. |
| 2.3 | Refuse unsupported lookup | same | If `git config --get core.hooksPath` is set, or `extensions.worktreeConfig` is on and `git config --worktree --get core.hooksPath` is set, do not install: report reason `hookspath-set` (web-01 rec 4; C4: `config.worktree` overrides everything but `-c`). A relative hooksPath resolves per worktree root (04 E30d), so any set value is unsupported. Never migrate or forward (design 512). | SC-30 passes. |
| 2.4 | Handle an existing `pre-push` (marker proposed; conditional on Section 9 row 14) | same | Proposed marker: full-byte equality with the installed guard source of 2.1 (a hash is the alternative, Section 9 row 14). The bytes contain no machine-specific value (step 1.2), so the plan's own installs match. On EEXIST: if the file is an `O_NOFOLLOW` regular file whose full bytes equal the installed guard source, reuse it; if it matches a known earlier owned version, upgrade it (step 2.8); otherwise keep it and report reason `foreign-pre-push` (01 §3 ownership check; web-02 rec "treat FileExistsError as already there, then compare"). Never shadow, wrap, stub or replay (design 512). | SC-18 (`foreign-pre-push`) and SC-19 pass. |
| 2.5 | Verify the file git will run (content check conditional on Section 9 row 14) | same | On the path from 2.2: full-content equality (proposed marker, Section 9 row 14), regular file, same dev/ino as opened, owner = current user, mode not group/other-writable, `access(X_OK)` true as the pushing user, mount not `noexec` (01 §3; web-02: `find_hook` in hook.c v2.47.3 lines 13-49 uses only `access(X_OK)`; missing, non-executable, wrong-owner or noexec hooks are skipped and the push proceeds). Failure reason `not-executable` or `not-owned`. **(b) The uv-directory file (proposal, step 1.2), on every run of this step (install and each pre-launch recheck, step 4.1):** the hook puts the directory named in `<hooks-dir>/pre-push.uv-dir` first on PATH before it calls `identify`, so the file is a trust input and is checked like the hook. Require: (1) a regular file opened with `O_NOFOLLOW`; (2) owned by the current user and not group- or other-writable; (3) content exactly one absolute directory path equal to the directory of `shutil.which("uv")` resolved by the launching process at this check (the same rule step 2.1 uses to write it, so no second record is kept); (4) the named directory and its `uv` each owned by the current user or by root and not group- or other-writable, and `uv` executable. A missing file, a symlink, unreadable or malformed content, a content mismatch or no executable `uv` gives reason `uv-dir-missing`; a wrong owner or a group- or other-writable file, directory or `uv` gives reason `not-owned`. The file is never rewritten here (step 2.1). Limit: these checks cannot detect a same-user rewrite of a `uv` binary that the user owns; that is an accepted limit (Section 7 bypass table; Section 9 row 41). | SC-18 (`not-executable`, `not-owned`, `uv-dir-missing`), SC-20 and SC-24 pass. |
| 2.6 | Self-test the installed hook | same | Run the installed hook with a synthetic ordinary actor: a protected record → exit 0, empty stream → exit 0 (01 §3). Feeding records via `git hook run --to-stdin` (2.36+) is an option ([EXTERNAL] web-01 E1). Governed self-test scope is open (G-35). Failure reason `self-test-failed`. | A Phase 6.4 case with a hook that exits 1 on every input gives reason `self-test-failed`. |
| 2.7 | Register the guard source for global install (do immediately after step 1.1) | `src/superclaude/cli/install_hooks.py` | Add `"launch-pre-push-guard.sh"` to `_FRESHNESS_SCRIPTS` (lines 42-94, next to identity at line 90 and the L1 guard at line 93) so `_copy_scripts` (251-290) installs it to `~/.claude/hooks/`, and update the verify-sync listing comment (62-64) (03). This step is required, not optional: the `Makefile` "Installer Registration" check (lines 307-323) compares every `src/superclaude/hooks/scripts/*.sh` with `_FRESHNESS_SCRIPTS` and prints `MISSING from _FRESHNESS_SCRIPTS` and sets drift for any unlisted script, so step 3.2 fails without it. `install_hooks()` stays user-global; it gains no per-repo git-hook code (G-20, design 565). Which command performs the per-repo install stays open (Section 9 row 15). | `make verify-sync` prints no `MISSING from _FRESHNESS_SCRIPTS` line, and Phase 6.8 passes. |
| 2.8 | Upgrade an earlier owned version (proposal) | `orca_worktree.py` (new constant, proposed name `L2_EARLIER_OWNED_SHA256`) | Without this, a hook from an older packaged version stops matching byte for byte, is reported foreign and is never replaced. Keep a tuple of the SHA-256 hashes of every earlier released guard script in `orca_worktree.py`, next to `L2_GUARD_VERSION_LINE` (step 1.9); each release that changes the script appends the previous script's hash. On EEXIST (2.4), a regular, owned file whose SHA-256 is in that tuple is replaced through the same no-replace path: publish the new bytes to a temp name with 2.1's sequence, then `rename` the temp over `pre-push` only after re-reading the target and confirming that its hash is still in the tuple (the only replacing operation in the plan, limited to files this plan wrote). Any other content stays `foreign-pre-push`. | A Phase 6.4 case installs a copy whose hash is in the tuple and, after a launch, finds the current bytes with no temp file left; a one-byte-changed copy whose hash is not in the tuple is kept with reason `foreign-pre-push`. |

### 8.3 Phase 3: Registration and mirrors

**Goal:** the new script and its plugin mirror are in sync with the dev copies, and the decision that it needs no Claude Code hook entry is recorded.
**Dependencies:** steps 1.1 and 2.7.

| Step | Action | Files | Details | Done when |
|---|---|---|---|---|
| 3.1 | Record that the guard needs no `hooks.json` entry | `src/superclaude/hooks/hooks.json` (identity at line 130), `plugins/superclaude/hooks/hooks.json` (identity at line 100) | The pre-push body is a git hook, not a Claude Code hook; it needs no PreToolUse entry. Only the identity entry is registered for this feature today (01 line 267). The existing PreToolUse matcher at src hooks.json:116 already includes MCP `update_ref`/`create_ref` tools (03 D19-31), so MCP ref writes stay with L1. Record "no entry" explicitly so `make verify-sync` and reviewers do not expect one. | Neither `hooks.json` contains `launch-pre-push-guard` (Grep finds no match), and the change description states that no entry is needed. |
| 3.2 | Run `make sync-dev` and `make verify-sync` | `.claude/` (generated, never staged) | Per project CLAUDE.md; stage only the `src/` and `plugins/` sides. | `make verify-sync` exits 0, and `git status` shows no staged `.claude/` path other than `.claude/settings.json`. |

### 8.4 Phase 4: `cmd_launch` integration and conflict handling

**Goal:** every governed launch installs or rechecks L2, reports a named reason when L2 is not in place, keeps that signal visible, and has a tested refusal path that ships switched off.
**Dependencies:** Phase 2 (publisher, ownership check, reason values) and Phase 1 (the L2 version line read by `l2_status`).

| Step | Action | Files | Details | Done when |
|---|---|---|---|---|
| 4.1 | Call the installer before `l2_status` (proposed install point; conditional on Section 9 row 15) | `orca_worktree.py`, `cmd_launch` (1253-1388) | Proposal (the install command and target repository are open, U28, Section 9 row 15): insert between IR-4 `enforcement_preflight` (1287-1304) and the `l2_status` call (1311) (03 order; design 565 "next integration"). Runs on every governed launch, so an exec-bit clear, a later hooksPath or a changed `pre-push.uv-dir` (step 2.5(b)) is caught before each launch (G-8 recommended answer: before each launch, not only at install). | SC-31 passes. |
| 4.2 | Make `l2_status` reason-bearing | `orca_worktree.py` `l2_status` (1012-1029) | Today `l2_status(wt: str) -> str` returns `absent` or `present-unverified` from `is_file` + `X_OK` and folds git-missing, timeout and not-a-repo into `absent` (03; G-19). **New signature (proposal):** `l2_status(wt: str) -> tuple[str, str \| None]`, a closed set: `("present-owned", None)` only after the Phase 2.4-2.5 checks (including the `pre-push.uv-dir` checks of step 2.5(b), run on every call) and the L2 version line (step 1.9) pass; otherwise `("absent", reason)` with `reason` exactly one of `no-hook`, `foreign-pre-push`, `hookspath-set`, `not-executable`, `not-owned`, `self-test-failed`, `guard-source-missing`, `uv-dir-missing`, `git-missing`, `timeout`, `not-a-repo` (the SC-18 list). `present-unverified` is removed, so a foreign hook stops being a silent pass (fixes D19-16 [CODE-CONTRADICTED], G-18). Consumers to change, one sub-step each: **4.2a** `session_report` L2 line (ow:1061-1067; `present-unverified` text at ow:1065) prints the state and the reason; **4.2b** `cmd_launch` (ow:1311-1312) unpacks the tuple and builds `l2_notes` from `state == "absent"`, carrying the reason (step 4.3); **4.2c** `src/superclaude/skills/sc-issue-protocol/refs/claim.md` line 120 (the L2 line with `present-unverified`) and lines 127-129 (the `W-L2-ABSENT` row and the ordering paragraph); **4.2d** `src/superclaude/commands/issue.md` line 16; **4.2e** `src/superclaude/skills/sc-issue-protocol/SKILL.md` lines 92, 136 and 150; **4.2f** `docs/user-guide/commands.md` line 381; **4.2g** `docs/designs/sc-issue-launch-level-hook.md` lines 6, 34, 355, 514 and 574; **4.2h** `docs/designs/sc-issue-claim-pipeline-flag.md` lines 4, 60, 135, 291, 349 and 381; **4.2i** `tests/skills/test_issue_orca_worktree.py` assertions at lines 1672 (`present-unverified` in the wave-8 text), 1691-1692 (`foreign-executable` and `hooks-path` expecting `present-unverified`) and 1726-1727 (`W-L2-ABSENT` exactly when absent), plus the `W-L2-ABSENT` warning assertions at 1483, 1521, 1533, 1554, 1623 and 1743; **4.2j** `tests/skills/test_issue_protocol.py` line 485 (the code list). Each path and line was found by Grep on 2026-11-08 and must be re-read before editing; the plugin mirrors of the skill files change with them (`make sync-dev`). | Grep for `present-unverified` in `src/`, `docs/` and `tests/` finds no match, the 4.2i/4.2j tests pass, and SC-18 passes. |
| 4.3 | Put the reason into W-L2-ABSENT, and keep it visible next to another warning | `orca_worktree.py` REMEDY 789-792, WHY 796-799, call 1311-1312, `launch_result` 1203-1220 | **Conflict case "foreign pre-push present":** keep the foreign file and all configuration unchanged; emit `W-L2-ABSENT` with reason `foreign-pre-push` and the resolved path. **Conflict case "core.hooksPath already set":** keep the config and every file unchanged; emit `W-L2-ABSENT` with reason `hookspath-set` and the configured value. No migration, no forwarding, no stub (design line 514 "preserve all existing files/configuration; report `W-L2-ABSENT` with the reason"; line 512). A separate `W-L2-CONFLICT` code is the alternative raised by G-18; the reason field covers it without a new code. **4.3a Visibility (G-45):** `launch_result` puts only the first note code in `warning` and the rest into `detail` as `also <code>: ...` (ow:1205-1207), so when `W-LAUNCH-NOT-CCSESSION` is also present `W-L2-ABSENT` appears only inside `detail` (pinned by `tests/skills/test_issue_orca_worktree.py:1554`). Proposal: add a field `l2` to the launch JSON (via `launch_result(..., l2={"state": ..., "reason": ...})`, which `base.update(fields)` at ow:1219 already accepts) so the L2 state is machine-readable whatever warning comes first; the ordering of `warning` is unchanged. | SC-18 and SC-30 pass, and a Phase 6.11 case with both warnings present finds `data["l2"]["state"] == "absent"` with its reason. |
| 4.4 | Build the launch refusal behind a switch that defaults off, in its own clearly marked commit | `orca_worktree.py` 1309-1310 (new constant `L2_REFUSAL_ENABLED`, proposal) | Owner decision (seed brief lines 68, 77): the refusal path must exist, be tested and ship off. **Mechanism (proposal for the brainstorm):** a module constant `L2_REFUSAL_ENABLED = False` in `orca_worktree.py`, next to the other launch constants (ow:789-804); the commented line at ow:1309-1310 becomes `if L2_REFUSAL_ENABLED and l2_notes: return emit(launch_result("failed", l2_notes, enforcement_hook=hook))`. A constant keeps the decided default in code, cannot be flipped by an agent's environment, and is turned on by one reviewed edit. When it is off (default): keep the `W-L2-ABSENT` warning (design 574). The turn-on criterion (after #442) stays open (Section 9 row 12). Tests turn it on in-process: load the script with the `importlib.util.spec_from_file_location` pattern already used at `tests/skills/test_issue_orca_worktree.py` lines 1954-1957, then `monkeypatch.setattr(module, "L2_REFUSAL_ENABLED", True)` and run the launch through that module (the subprocess helper `run_launch`, line 1289, cannot see a patched constant) (Phase 6.11). Phase 7.5 documents it. | SC-29 passes, and the constant reads `False` in the shipped file. |
| 4.5 | Leave release and worktree removal alone | none | The shared hook stays on release; no whole-hook deletion (design 524-526). `git worktree remove` deletes the private marker and keeps the shared hook (04 F2). Orca's removal path is untested (G-37, Phase 6.9). | Phase 6.9 passes, and the diff touches no release or removal code. |

### 8.5 Phase 5: L1 hardening (closes the bypasses in Section 7)

**Goal:** the L1 text guard refuses the visible forms that remove or skip the L2 hook, so L2 cannot be switched off by a governed agent's own command.
**Dependencies:** none on Phases 1-4 for the code (it edits only the L1 guard); the test cases land in Phase 6.7. Issue #440 edits `tests/hooks/test_launch_level_guard.py` in another worktree (seed brief line 59), so Phase 5 adds no case to that file.

| Step | Action | Files | Details | Done when |
|---|---|---|---|---|
| 5.1 | Add hook-file tamper tokens | `src/superclaude/hooks/scripts/launch-level-guard.sh` line 706 | Add `*.git/hooks*`, `*hooks/pre-push*`, `*config.worktree*` (02 Gap 1, Gap 10, line 168). Covers Write/Edit/rm/mv/ln/chmod on the hook and the per-worktree config route (04 E29, E31). The same two hook tokens also cover the uv-directory file `<hooks-dir>/pre-push.uv-dir` (step 1.2), whose path contains `.git/hooks` and whose name begins with `pre-push`, so rewriting it to point at another `uv` is refused by L1 as well as caught by the recheck of step 2.5(b). Closes G-12 and the L1 part of G-8. | SC-25 passes, including its `pre-push.uv-dir` case. |
| 5.2 | Ungate config tokens | same, lines 525, 532 | Move the `hookspath` and `alias.` tokens out of the `LL_GIT=1` gate so `cd .git && >> config` and `/etc/gitconfig` writes are seen (02 Gap 3, line 170). Closes G-14. | A Phase 6.7 case `cd .git && printf '[core]\n\thooksPath = /x\n' >> config` exits 2. |
| 5.3 | Fix command-position detection, including unlisted wrappers | same, line 435 (W drops `_`), 549 (wrapper skip list), 556-557 | (a) Underscore env prefixes move the command position off `git` (02 Gap 2). Closes G-13. (b) The wrapper skip list at line 549 (`env \| sudo \| nohup \| exec \| command \| builtin \| timeout \| xargs \| setsid \| time \| nice \| stdbuf \| ionice \| doas \| unbuffer \| eval \| if \| then \| else \| elif \| do \| while \| until \| coproc`) does not name `chrt`, `taskset`, `find` (with `-exec`) or `uv` (`uv run`), so the wrapper word becomes command position and the unknown-subcommand check at line 637 never sees the `git` word (02 line 251). Because any finite list can be extended by another wrapper, refuse instead when a `git` word appears at any word position of a segment that is not command position and the segment carries an unknown subcommand or a push-bypass token, and add the four names to line 549. Closes G-44. | SC-28 passes and the existing `tests/hooks/test_launch_level_guard*.py` suites still pass. |
| 5.4 | Extend push-bypass coverage | same, push regex 661, PROTECTED 663-665 | (a) Add `--config-env`, `GIT_CONFIG_COUNT/KEY/VALUE`, `GIT_CONFIG_PARAMETERS`, `-c hook.pre-push.*`, `curl` to `git-receive-pack` on `github.com`, non-literal API hosts (L1-7), and the obfuscated `gh` subcommand `gh $'\x61pi'` (L1-8, PARTIAL in 02 §5) (web-01 rec 5; 02 Gap 5). Closes G-16, L1-7 and L1-8. (b) ANSI-C quoting: T turns `$'core.hooks\x50ath'` into `core.hooksx50ath` (sed at line 431), so the `hookspath` token never matches (02 line 249). Refuse any Bash call whose raw command text (before the line-431 rewrite) contains `$'` inside a `-c` value, a `--config-env` value or a `GIT_CONFIG_KEY_<n>=` / `GIT_CONFIG_PARAMETERS=` assignment; decoding ANSI-C escapes in shell text is the larger alternative and is not proposed. `remote.origin.push` (G-15) stays an L1 gap but L2 sees it as field 3 (04 E20). | SC-26 and SC-27 pass. |
| 5.5 | Correct the stale texts | same, line 80 (LL-UNKNOWN Why), line 95 (LL-TAMPER Blocked), line 56 (LL-PUSH-FORM) | Lines 80 and 95 are [CODE-CONTRADICTED]; line 56 omits `--set-upstream`, which the regex at line 661 accepts (DOC-9) (02 Stale Documentation). | Line 56 names `--set-upstream`; lines 80 and 95 no longer claim coverage the code lacks (an alias or an unlisted wrapper, and the hook files of 5.1 are named); the existing L1 suites that match message text still pass. |
| 5.6 | Keep the self-declared limit | same, lines 710-711 | L1 is text-only and advisory (02 Summary); in-process library pushes are a stated limitation (web-01 J11). | The comment at lines 710-711 is unchanged in the diff. |

### 8.6 Phase 6: Tests

**Goal:** real-git and hook-harness tests pin every success criterion of Section 3.5, with the remote refs checked before and after each refusal.
**Dependencies:** Phases 1, 2, 4 and 5 (each test exercises the code its step names). New tests go into new files where possible, because issue #440 edits `tests/hooks/test_launch_level_guard.py` in another worktree (seed brief line 59).

| Step | Action | Files | Details | Done when |
|---|---|---|---|---|
| 6.1 | New hook tests in a pytest temp bare remote | `tests/hooks/test_launch_pre_push_guard.py` **(new)** | Bare remote + clone + linked worktree in `tmp_path`; assert remote refs before/after (design 530-534). | `uv run pytest tests/hooks/test_launch_pre_push_guard.py` passes, and each refusal case asserts `git for-each-ref` output on the bare remote is identical before and after. |
| 6.2 | Record-shape cases | same | Protected refspec spellings (04 E3-E6, E11, E20, E21), `HEAD@{0 days ago}:refs/heads/main` 6-field record (web-01 G5; fix runs X2-X3), empty stream, malformed line, `refs/heads/Main` allowed, `refs/heads/ma` allowed, mixed push refused whole (04 F1), dry-run runs the hook (04 E13), "fetch first" record delivered (04 E23a), 3001-branch push under each stdin rule of Phase 1.7 (G-42), SHA-256 repo (web-01 rec 6). | SC-1 to SC-12 each have a passing case. |
| 6.3 | Verdict cases | same | `governed`, `unknown`, `ordinary`, `released`, and each "no verdict" cause (missing or stale `pre-push.uv-dir`, no uv on PATH with the uv-directory file in place, exit 2, missing script, timeout) (01; 04 E28c). | SC-13 to SC-16, SC-23 and SC-24 each have a passing case. |
| 6.4 | Publisher cases | `tests/skills/test_issue_orca_worktree.py` | Fresh install 0755 and reuse on identical bytes; foreign `pre-push` kept and reason `foreign-pre-push`; `core.hooksPath` set (repo and `config.worktree`) kept and reason `hookspath-set`; mode 0644 → `not-executable` (web-02 step 8f); no temp file left (web-02 step 8); missing installed source → `guard-source-missing`; failing self-test → `self-test-failed`; earlier owned version upgraded and a near-copy kept (step 2.8); each `pre-push.uv-dir` case of step 2.5(b) (symlink, other directory with a stub `uv`, group-writable file, group-writable directory or `uv`) → `uv-dir-missing` or `not-owned` at the next launch. Extend `test_ir6_l2_status_follows_the_git_hook_path` (1696-1729). | SC-18 to SC-20, SC-24(b) and SC-31 each have a passing case for every reason string. |
| 6.5 | Linked-worktree placement | same | Hook in common dir runs from every worktree (04 E30); relative hooksPath resolves per worktree root (04 E30d); `config.worktree` override (web-01 C4). | SC-17 and SC-30 pass from the main checkout and a linked worktree. |
| 6.6 | Replace the crashing test policy | `tests/hooks/test_launch_job_identity.py` 1175-1232 (`LocalPushFixture`) | It crashes on malformed records (03; G-41). **Chosen:** point `LocalPushFixture` at the real guard script `src/superclaude/hooks/scripts/launch-pre-push-guard.sh` instead of its own policy, so the fixture and the shipped hook cannot drift; making the copy refuse malformed input would keep two policies. | `LocalPushFixture` contains no record-parsing code of its own, and its existing tests plus a malformed-record case pass (the malformed case is refused, not crashed). |
| 6.7 | L1 token tests | `tests/hooks/test_launch_level_guard_l2_bypass.py` **(new)** | One case per new token and form in Phase 5 (SC-25 to SC-28: hook-file tamper, ungated config write, underscore prefix and unlisted wrappers, `--config-env`, `GIT_CONFIG_*`, `GIT_CONFIG_PARAMETERS`, `-c hook.pre-push.*`, and the ANSI-C spelling in both its escaped and plain forms), plus the evasions 02 read statically (G-39). It reuses the bound-session harness of `tests/hooks/test_launch_level_guard_with_identity.py` (`_bind`, `_payload`, `_hook`, lines 67-103). `tests/hooks/test_launch_level_guard.py` is the main L1 suite but issue #440 edits it in another worktree (seed brief line 59), so no case is added there; `test_launch_level_guard_with_identity.py` covers L1 together with the identity hook and stays unchanged. | `uv run pytest tests/hooks/test_launch_level_guard_l2_bypass.py` passes, and each case fails when the matching Phase 5 change is reverted. |
| 6.8 | Install script list | `tests/cli/test_install_hooks.py` (934-1003) | Assert the new script is installed with identity and guard. | The test passes and fails if `"launch-pre-push-guard.sh"` is removed from `_FRESHNESS_SCRIPTS`. |
| 6.9 | Orca worktree removal | `tests/skills/test_issue_orca_worktree.py` | Shared hook survives Orca's removal path (G-37); plain `git worktree remove` is already observed (04 F2). | After the removal path runs, `<common-dir>/hooks/pre-push` still exists with the owned bytes. |
| 6.10 | Pin the git version assumption | test module docstring or a skip guard | Tested on 2.47.3 only (04); version floors from web-01 F2 (pre-push 1.8.2, hooksPath 2.9.0, worktreeConfig 2.20.0, `git hook run` 2.36.0). The guard tests record `git --version` in their output. Re-run the Phase 6 real-git suite before relying on any version at or above 2.54.0 (hook API rewrite, configured hooks; parallel hooks 2.55.0) and when 2.98.0 ships (`hook.pre-push.enabled`) (web-01 rec 7, F1). | The test output shows the `git --version` line, and the docstring names the versions above. |
| 6.11 | IR-7 switch states and warning visibility | `tests/skills/test_issue_orca_worktree.py` | One case per switch state with L2 absent: `L2_REFUSAL_ENABLED` False (default) → launch proceeds with `W-L2-ABSENT`; True (set in-process with `monkeypatch.setattr` after loading the script as at lines 1954-1957) → `launch_result("failed", ...)` and no agent launched (Phase 4.4; seed brief line 68). One case with both `W-LAUNCH-NOT-CCSESSION` and L2 absent (the scene of the test at line 1546) asserts the `l2` field of step 4.3a. | SC-29 passes, and the both-warnings case finds `l2.state == "absent"`. |

### 8.7 Phase 7: Design document updates

**Goal:** the design document and the identity header describe the built behaviour, its limits and the switch, so every document that describes `W-L2-ABSENT` stays accurate (seed brief line 69).
**Dependencies:** Phases 1, 4 and 5 (the text describes their behaviour); the per-consumer document edits of step 4.2 (4.2c-4.2h) are done with Phase 4, not here.

| Step | Action | Files | Details | Done when |
|---|---|---|---|---|
| 7.1 | Rewrite the malformed-record rule | `docs/designs/sc-issue-launch-level-hook.md` line 518 | Right-split into 4 fields; "extra fields refuse" is wrong (web-01 G5; fix runs X2-X3). | Line 518 no longer says "missing/extra fields" refuse; it says each record is split from the right into 4 fields and is malformed only with fewer than 4 fields or non-hex object names. |
| 7.2 | Correct the non-fast-forward statement | same, line 534 | "Fetch first" records reach pre-push (04 E23a; D19-47 [CODE-CONTRADICTED] in part; web-01 rec 8). | Line 534 states that "fetch first" records are delivered to pre-push. |
| 7.3 | Extend the bypass list | same, line 520 | Add `--config-env`, `GIT_CONFIG_*` env, exec-bit clear, `config.worktree`, smart-HTTP, library pushes, future `hook.pre-push.enabled` (web-01 line-520 verdict "CONFIRMED with three precision additions"; 04 E29, E31). | Line 520 names each of the seven forms. |
| 7.4 | Record the "no verdict" → `unknown` mapping and its human exceptions | same, lines 493, 557 | Line 493 "never restricted" conflicts with humans restricted by `unknown` (G-11). **Replacement text for line 493's first sentence (proposal, under A-i):** "An ordinary human push in the same worktree is not restricted by launch policy when the selector answers `ordinary`. A push the selector cannot classify (`unknown`, or no verdict: the selector missing, timing out, exiting nonzero, or the uv-directory file missing) is refused only for `refs/heads/main` and `refs/heads/master`, with a diagnostic, and allowed for every other ref (owner decision 2026-11-08). A human can therefore be refused a push to main when the selector cannot run; the diagnostic names the cause." **Addition after line 557's `unknown` sentence:** "The pre-push hook treats a missing or failing selector the same as `unknown`." If the brainstorm picks A-iii instead of A-i (Section 9 row 1), the uv-directory clause is replaced by that variant's cause. | Line 493 no longer says "never restricted", and both quoted sentences (or the A-iii variant) are present. |
| 7.5 | Settle IR-7 wording | same, lines 355, 514, 574 | State that the refusal path exists, is tested, and ships switched off through `L2_REFUSAL_ENABLED = False` (proposal, step 4.4), so `W-L2-ABSENT` stays a warning by default (seed brief lines 68, 77); add the turn-on criterion once Section 9 row 12 is answered. | Lines 355, 514 and 574 agree that the refusal exists, ships off and is turned on by the named constant. |
| 7.6 | Fix the identity header wording | `src/superclaude/hooks/scripts/launch-job-identity.sh` line 4 (+ plugin mirror) | "descendants" vs session membership ([CODE-CONTRADICTED] wording, 01 Gaps 9). | Line 4 says session membership, not descendants, in both copies, and `make verify-sync` passes. |
| 7.7 | Note the absent 19.6 artifacts | `docs/designs/sc-issue-launch-level-hook.md` lines 538-543 | They cite `.dev/brainstorms/20261106-l2-prepush-decisions/`, which does not exist ([STALE DOC], 03); wording depends on G-21. | Lines 538-543 either point at an existing path or say the artifacts were not produced. |
| 7.8 | Record the tested git version and re-test triggers | `docs/designs/sc-issue-launch-level-hook.md` §19 | Tested on 2.47.3; re-run the Phase 6 real-git suite before relying on any version at or above 2.54.0 (hook API rewrite, configured hooks) and when 2.98.0 ships (web-01 F1, rec 7). | §19 names 2.47.3, 2.54.0 and 2.98.0 as described. |

### 8.8 Gap mapping (G-1 to G-45)

| Gap | Disposition | Where |
|---|---|---|
| G-1 | Documented externally (web-01 H/J); not confirmed at runtime: API writes, `gh api`, smart-HTTP bypass the hook | Section 7 bypass table; Phase 5.4; Phase 7.3 |
| G-2 | Documented externally (web-01 H/J); not confirmed at runtime (libraries not installed): libgit2/pygit2, dulwich, isomorphic-git do not run it; JGit and GitPython do | Section 7 bypass table; Phase 5.6 (stated limitation) |
| G-3 | Resolved by web research (web-01 F2 version table) | Phase 6.10 |
| G-4 | Resolved by web research (web-02 primitives table, step 8) | Phase 2.1 |
| G-5 | Resolved by web research (`find_hook`, hook.c 13-49) | Phase 2.5, 4.1 |
| G-6 | Recommendation A-i; final pick is a brainstorm decision | Phase 1.2; Section 9 row 1 |
| G-7 | Mapping proposed (no verdict = `unknown`) | Phase 1.4, 7.4; Section 9 row 2 (confirm) |
| G-8 | Proposed: recheck before each governed launch, plus L1 tokens | Phase 4.1, 5.1; Section 9 row 3 (confirm) |
| G-9 | Accepted limit unless decided otherwise | Section 7; Section 9 row 4 |
| G-10 | Deferred | Section 9 row 5 |
| G-11 | Deferred; design text change follows the decision | Phase 7.4; Section 9 row 6 |
| G-12 | Step | Phase 5.1, 6.7 |
| G-13 | Step | Phase 5.3, 6.7 |
| G-14 | Step | Phase 5.2, 6.7 |
| G-15 | L2 part resolved (04 E20); L1 part left as an L1 gap covered by L2 | Phase 5.4 note |
| G-16 | Step (bypass confirmed by web-01 H3) | Phase 5.4 |
| G-17 | Default DECIDED off (seed brief line 77); switch proposed as `L2_REFUSAL_ENABLED = False`; turn-on criterion open | Phase 4.4, 6.11, 7.5; Section 9 row 12 |
| G-18 | Step proposed (reason field); new code `W-L2-CONFLICT` left as the alternative | Phase 4.2, 4.3; Section 9 row 13 |
| G-19 | Step | Phase 4.2 |
| G-20 | Step | Phase 2.7, 4.1 |
| G-21 | Deferred (ask owner) | Phase 7.7; Section 9 row 16 |
| G-22 | Resolved in Gate 1 | none |
| G-23 | Resolved in Gate 1 | none |
| G-24 | Order is undocumented (web-01 Key Findings) and was observed both ways: command-line order in 04 E7 and web-01 G3, not command-line order in 04 E9, E19, E24. Resolved only in the sense that the hook scans every record and does not depend on order | Phase 1.6 (check every record) |
| G-25 | Git side resolved (case-sensitive, web-01 G2); hosting-service behaviour deferred | Phase 1.6; Section 9 row 23 |
| G-26 | Resolved on 2.47.3: web-01 D3a-e (linked worktree) plus the QA re-run and fix run X1 (main checkout) | Phase 2.2 |
| G-27 | Partly resolved (FETCH_FIRST delivered, transport.c 1315-1319); real SSH/HTTPS remote untested | Phase 6.2; Section 9 row 24 |
| G-28 | Partly resolved: field 1 can hold spaces (web-01 G5), so the parser right-splits and treats fewer than 4 fields as malformed; that git never emits a short record in any version or transport stays unproven (D19-42) | Phase 1.5, 7.1 |
| G-29 | Resolved by web research: git refuses `refs//heads/main` before the hook (web-01 G1) | none needed for L2 |
| G-30 | Resolved by web research: `--mirror` with a refspec is fatal (web-01 G4) | none needed for L2 |
| G-31 | Deferred (local read-only check not run here) | Phase 2.3 handles either value; Section 9 row 26 |
| G-32 | Deferred | Section 9 row 27 |
| G-33 | Deferred (scope) | Section 9 row 18 |
| G-34 | Deferred (scope) | Section 9 row 18 |
| G-35 | Deferred | Phase 2.6; Section 9 row 17 |
| G-36 | Proposed: missing script = no verdict = `unknown` | Phase 1.3; Section 9 row 2 |
| G-37 | Step | Phase 6.9 |
| G-38 | Deferred | Section 9 row 19 |
| G-39 | Step | Phase 6.7 |
| G-40 | Not relevant to GitHub remotes; no step | none |
| G-41 | Step | Phase 6.6 |
| G-42 | Step | Phase 1.7, 6.2 |
| G-43 | The git-behaviour parts of D19-21, 23, 27, 29, 35, 41 are settled by 04; the rest stay unverified design statements | Phase 6 covers the testable ones; Section 9 row 33 |
| G-44 | Step (rated Critical in Section 4.1, the same rating as L1-5) | Phase 5.3, 6.7; SC-28; Section 9 row 8 |
| G-45 | Step | Phase 4.3a, 6.11 |

### 8.9 Gap mapping (BP-, L1- and DOC- families, Sections 4.2-4.4)

| Gap | Disposition | Where |
|---|---|---|
| BP-1 `--no-verify` | No step: L1 already refuses (02) | Section 7 bypass table ("L1 (keep)") |
| BP-2 `-c core.hooksPath` | No step: L1 already refuses (02) | Section 7 bypass table |
| BP-3 `--config-env`, `GIT_CONFIG_*` | Step | Phase 5.4, 6.7, 7.3 |
| BP-4 persistent `core.hooksPath` | Covered by G-8, G-14 | Phase 2.3, 4.1, 5.2 |
| BP-5 `extensions.worktreeConfig` | Covered by G-8 | Phase 2.3, 5.1, 6.5 |
| BP-6 executable bit cleared | Covered by G-8 | Phase 2.5, 4.1, 5.1 |
| BP-7 raw smart-HTTP | Covered by G-16 | Phase 5.4 |
| BP-8 `git send-pack` | No step: L1 already refuses (02) | Section 7 bypass table |
| BP-9 in-process library push | Covered by G-2 (stated limitation) | Phase 5.6 |
| BP-10 REST refs API / `gh api` | Covered by G-1; L1 refuses, PARTIAL forms in L1-7, L1-8 | Phase 5.4 |
| BP-11 hook file removed or replaced | Covered by G-12 | Phase 2.4-2.5, 5.1 |
| BP-12 `hook.pre-push.enabled=false` (future) | Step | Phase 5.4 (`-c hook.pre-push.*`), 6.10, 7.3, 7.8 |
| BP-13 config-defined and parallel hooks, remote groups | Version pin | Phase 6.10, 7.8 |
| BP-14 more-than-four-field record | Covered by G-28 | Phase 1.5, 6.2 |
| L1-1 config-file write of `core.hooksPath` | Covered by G-14 | Phase 5.2 |
| L1-2 `cd`, then canonical push | No L1 step: L2 refuses by field 3 | Phase 1.6 |
| L1-3 Write/Edit of the hook | Covered by G-12 | Phase 5.1 |
| L1-4 `rm`/`mv`/`chmod -x`/`ln -sf` on the hook | Covered by G-12 | Phase 5.1 |
| L1-5 underscore env prefix with alias | Covered by G-13; the unlisted-wrapper form of the same bypass is G-44 (both Critical) | Phase 5.3, 6.7 |
| L1-6 `curl` to `git-receive-pack` | Covered by G-16 | Phase 5.4 |
| L1-7 hidden `api.github.com` host | Step | Phase 5.4 |
| L1-8 `gh $'\x61pi'` | Step | Phase 5.4, 6.7 |
| L1-9 `uv run python -c` with push libraries | Covered by G-2 (stated limitation) | Phase 5.6 |
| L1-10 `uv run python <script>` that pushes | Covered by G-2 (stated limitation) | Phase 5.6 |
| DOC-1 design line 534 (D19-47) | Step | Phase 7.2 |
| DOC-2 LL-UNKNOWN text line 80 | Covered by G-13 | Phase 5.5 |
| DOC-3 LL-TAMPER text line 95 | Step | Phase 5.5 |
| DOC-4 identity header line 4 | Step | Phase 7.6 |
| DOC-5 IR-7 design text | Covered by G-17 | Phase 7.5 |
| DOC-6 §19.6 artifacts | Covered by G-21 | Phase 7.7 |
| DOC-7 D19-16 conflict reporting | Covered by G-18 | Phase 4.2, 4.3 |
| DOC-8 D19-42 malformed rule | Covered by G-28, BP-14 | Phase 1.5, 7.1 |
| DOC-9 LL-PUSH-FORM text line 56 | Step | Phase 5.5 |
| DOC-10 design line 493 | Covered by G-11 | Phase 7.4 |
| DOC-11 git-hook page vs 2.98.0 note | Covered by BP-12 (external discrepancy, no repo text to change) | Phase 6.10, 7.8 |

### 8.10 Integration Checklist

- [ ] Guard source exists in `src/superclaude/hooks/scripts/` and the plugin mirror, byte-identical (Phase 1.1; `make verify-sync`).
- [ ] Install command and target repository settled (Section 9 row 15); if the proposal stands, `_FRESHNESS_SCRIPTS` lists the guard, and `tests/cli/test_install_hooks.py` asserts it installs to `~/.claude/hooks/` (Phase 2.7, 6.8).
- [ ] Identity-script location settled (Section 9 row 2); hook calls the selector (proposed: `~/.claude/hooks/launch-job-identity.sh identify`) under a fixed PATH; "no verdict" maps to `unknown` (Phase 1.2-1.4).
- [ ] Parser right-splits to 4 fields, compares field 3 exactly, allows empty stdin; `governed`/`unknown`/no-verdict read stdin to EOF before an allow, a refusal may exit at the first protected record, `ordinary`/`released` exit 0 without reading (Phase 1.5-1.8).
- [ ] Publisher uses `O_EXCL` temp + `fchmod 0755` + `fsync` + `link` + `unlink` + directory `fsync`; never `rename` (Phase 2.1).
- [ ] Target path comes from `git rev-parse --path-format=absolute --git-path hooks/pre-push` (Phase 2.2).
- [ ] `core.hooksPath` set (repo or `config.worktree`): nothing changed, `W-L2-ABSENT` reason `hookspath-set` (Phase 2.3, 4.3).
- [ ] Foreign `pre-push`: nothing changed, `W-L2-ABSENT` reason `foreign-pre-push` (Phase 2.4, 4.3).
- [ ] Ownership marker settled (Section 9 row 14); proposed ownership = full bytes + regular file + owner + mode + `X_OK` + not noexec + self-test (Phase 2.5-2.6).
- [ ] Installer runs in `cmd_launch` after IR-4 and before `l2_status`, on every governed launch (Phase 4.1).
- [ ] `l2_status` returns a reason; a foreign hook is no longer `present-unverified` (Phase 4.2).
- [ ] IR-7 refusal built behind a switch that defaults off, in its own clearly marked commit, tested in both states, and documented as shipping off (Phase 4.4, 6.11, 7.5; seed brief lines 68, 77).
- [ ] No `core.hooksPath` write, no `extensions.worktreeConfig`, no forwarding, no other hook touched (design 510-512).
- [ ] L1 tokens and ungating land with tests (Phase 5, 6.7).
- [ ] All git tests run in pytest temp dirs with a local bare remote only (design 530-534).
- [ ] Design text updated (Phase 7).
- [ ] Only `src/`, `plugins/`, `tests/`, `docs/` and `.dev/tasks/` staged; never `.claude/` except `settings.json` (project CLAUDE.md).

---

## 9. Open Questions

The `#` column is the row number cited as "Section 9 row N" elsewhere in this report. Each row names its `gaps-and-questions.md` gap (G-n). Tags [UNVERIFIED], [CODE-CONTRADICTED] and [STALE DOC] are carried over from the research files. Rows drawn from web-01 or web-02 are external context (official documentation and upstream source), not observations in this repository.

### 9.1 Brainstorm and owner decisions the research could not make

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| 1 | Which identity variant does the hook use when the pusher's PATH has no `uv`? Today `identify` exits 2 (no verdict), which maps to `unknown`, so such a human cannot push to main/master. An absolute uv path alone does not fix it (Gate 1 qualitative F1; corrected remedy in gap G-6, not 04 line 1530). Options: (i) fixed PATH with the install-time uv dir, (ii) hook-side no-store exit, (iii) pure-shell hook. G-6. | Human pushes to main/master refused on hosts or shells without uv on PATH. | Brainstorm decision (owner). Section 7 recommends (i). Before deciding, run a `/tmp` sandbox experiment: a local bare remote, the candidate hook, and `env -i PATH=/usr/bin:/bin git push` as an ordinary user, recording the verdict. |
| 2 | How does the hook find the identity script at run time, and what does it do when the script is missing, times out or returns no verdict? The design does not say that "no verdict" (exit 2) maps to `unknown` (01 Gaps 1). The question stays open in seed-brief line 78. G-7, G-36. | Decides whether the guard fails open or closed for protected pushes when its dependency is gone. | Brainstorm decision for seed-brief line 78. Section 8 (Phases 1.3-1.4) proposes treating a missing script, a timeout and exit 2 as `unknown`, which refuses only main/master. Then write that mapping into design §19.1 of `docs/designs/sc-issue-launch-level-hook.md`. |
| 3 | Is install integrity checked only at install time, or before every governed launch? A same-user agent can open two holes with no push flag. (a) Clearing the exec bit makes git skip the hook silently: `find_hook` checks `access(X_OK)` (web-02, git v2.47.3 `hook.c` line 21), and `-c advice.ignoredHook=false` hides the hint (04 E29). (b) A per-worktree `core.hooksPath` through `extensions.worktreeConfig` (04 E31). G-8. | The guard can be switched off between install and push without any push-time flag. | Brainstorm decision. Section 8 (Phase 4.1) proposes a check before each launch: X_OK, owner and content, plus the effective `git rev-parse --path-format=absolute --git-path hooks/pre-push`, as in web-02 recommendation 8. Add L1 tokens for `chmod` and `config.worktree` (rows 7 and 9). |
| 4 | Accept the `setsid` and different-HOME escapes, which make a governed push classify as `ordinary`, and list the HOME escape in the design? It is listed nowhere (01 Gaps 2). G-9. | A governed agent can push to main/master as `ordinary`. | Brainstorm decision. If the escapes are accepted, add both to the limits list in design §19 (the B-CTX limits that seed-brief line 74 records as accepted). |
| 5 | Prune stale job records left by a killed supervisor, or accept that PID reuse can turn an unrelated human into `unknown`? The PID-reuse consequence is inferred, not observed (01 Gaps 3) [UNVERIFIED]. G-10. | A false refusal of a human's main/master push. | Brainstorm decision. To settle the inference, run a `/tmp` sandbox experiment: write a stale record whose PID is the session id of a fresh `setsid` shell, then run `identify` from that shell. |
| 6 | Which human cases restricted by `unknown` are acceptable, given design line 493 ("never restricted")? The cases are: HOME unset or relative, a group-writable home, stale records, and no uv on PATH (01 Gaps 4 and 10; qualitative verification N-2). G-11. | Design line 493 is not true for these cases. | Owner decision. Then revise line 493 of `docs/designs/sc-issue-launch-level-hook.md` to list the accepted cases. |
| 7 | Add an L1 tamper token for git hooks? Today Write, Edit, `rm`, `chmod` and `ln` on `.git/hooks/pre-push` are allowed by `src/superclaude/hooks/scripts/launch-level-guard.sh` (02 Gaps 1). G-12. | An agent can delete or replace the L2 hook through L1. | Brainstorm decision. Pair it with the integrity recheck in row 3, and add a test to `tests/hooks/test_launch_level_guard_l2_bypass.py` (new file, Phase 6.7; issue #440 edits `test_launch_level_guard.py`, seed brief line 59). |
| 8 | Close the L1 command-position bypass? An environment prefix with an underscore name moves the command position off `git`, so aliases and obfuscated subcommands pass. An unlisted wrapper word before `git` (`chrt`, `taskset`, `find -exec`, `uv run`) does the same, because the wrapper skip list at guard line 549 does not name it (02 line 251; G-44). This contradicts the LL-UNKNOWN Why text at guard line 80 [CODE-CONTRADICTED] [STALE DOC] (02 Gaps 2). G-13, G-44. | L1's claim that aliases cannot push is false. L2 is then the only push-time layer. | Brainstorm decision: fix the guard (Phase 5.3), or reword line 80. Either way, add regression tests for both forms to `tests/hooks/test_launch_level_guard_l2_bypass.py` (new file, Phase 6.7; SC-28). |
| 9 | Refuse config writes that contain no git word? Editing `.git/config`, `config.worktree` or `/etc/gitconfig` can set `core.hooksPath`, `alias.*` and `remote.origin.push` without a refusal. LL-TAMPER Blocked text (guard line 95, "a git configuration file") is only partly true [CODE-CONTRADICTED partial] (02 Gaps 3 and 10). G-14. | hooksPath redirection bypasses L2 without any push flag. | Brainstorm decision: extend the L1 tamper tokens, or reword line 95 to say what it covers. |
| 10 | L1 cannot see a destination that comes from configuration (`remote.origin.push`). L2 sees it as stdin field 3 (04 E20), so the L2 side is resolved; the L1 side is open. G-15 (L1 part). | L1-only enforcement misses config-driven destinations. | Owner decision to document this as an L1 limit in design §19. No new code is needed for L2. |
| 11 | Should L1 refuse more of the push paths that bypass pre-push? web-01 documents that these never run the local hook (documented externally; not confirmed at runtime): smart-HTTP `git-receive-pack`, the GitHub REST refs API, `gh api` (Area J7/J8/H3), and libgit2/pygit2, dulwich and isomorphic-git (Area J table). L1 refuses neither smart-HTTP on `github.com` nor non-literal API hosts (02 Gaps 5). G-16, plus the L1 coverage list in web-01 recommendation 5. | Each uncovered path pushes to main/master with no L1 or L2 refusal. Only server-side branch protection applies. | Brainstorm decision on the L1 coverage list (web-01 recommendation 5). Document the remaining in-process library pushes as a stated L1 and L2 limit in design §19. |
| 12 | Once L2 exists, does IR-7 become a refusal of the governed launch, as design lines 355 and 514 say, or stay the `W-L2-ABSENT` warning the code emits (`orca_worktree.py` line 1312)? [STALE DOC] (03). The default is DECIDED off (seed-brief line 77). This report proposes the mechanism: a module constant `L2_REFUSAL_ENABLED = False` in `orca_worktree.py` guarding the refusal at the call site (step 4.4), tested by Phase 6.11 with the module loaded in-process and the constant monkeypatched. Only the turn-on criterion (after #442?) is open. G-17. | Design and code disagree until this is decided. | Owner decision for seed-brief line 77: confirm the proposed constant and set the turn-on criterion. Then update design lines 355, 514 and 574 (Phase 7.5). 03 shows the one-line refusal to add after the `l2_notes` line. |
| 13 | A foreign executable `pre-push` gives `present-unverified` with no warning (D19-16 [CODE-CONTRADICTED], 03). Add a new `W-L2-CONFLICT` code, or a reason field in `W-L2-ABSENT`? G-18. | A hook that is not the guard passes as present. | Brainstorm decision. Section 8 (Phase 4.3) prefers the reason field. |
| 14 | What is the ownership and version marker, and how is the content compared: byte equality with the packaged hook, or a hash? `l2_status` (`orca_worktree.py` line 1012) cannot tell an owned guard from any executable. It also folds git-missing, timeout and not-a-repo into `absent` (03). This is open in seed-brief line 76. G-19. | Without a marker, rows 3 and 13 cannot be implemented. | Brainstorm decision for seed-brief line 76. |
| 15 | Which command installs the hook: `superclaude install`, the claim's `launch`, or a dedicated subcommand? `src/superclaude/cli/install_hooks.py` is user-global only and has no git-hook path. 03 names `cmd_launch` before `l2_status` (design line 565) as the natural point. The question is U28, open in seed-brief line 75. G-20. | Nothing installs L2 today. | Brainstorm decision for seed-brief line 75. Install into the common dir resolved with `git rev-parse --path-format=absolute --git-path hooks/pre-push` (web-01 G-26 answer). |
| 16 | Were the design §19.6 source artifacts (`.dev/brainstorms/20261106-l2-prepush-decisions/`) committed elsewhere, or never written? Design lines 538-543 cite them [STALE DOC] (03). G-21. | D19-10, 17, 33, 49 and 52-56 cannot be verified. | Ask the owner. If the artifacts were never written, remove or reword design lines 538-543. |
| 17 | Self-test scope for the installed hook: a governed fixture, or ordinary only? (01 Gaps 7). G-35. | The install-time self-test may never exercise the refusal path. | Brainstorm decision. |
| 18 | Are PID-namespace and container behaviour, `boot_id` inside containers, and non-dumpable or setuid Python (which makes `/proc/<sid>` root-owned) in scope? All [UNVERIFIED] (01 Gaps 5 and 6). G-33, G-34. | Identity may misclassify in containers. | Brainstorm scope decision. seed-brief line 74 limits the build to the tested local Bash surface, so the default is to document these as limits. |
| 19 | Does `cd` persist between Bash calls in a governed session, and are mid-session `~/.bashrc` edits (for example `GIT_CONFIG_PARAMETERS`) picked up? [UNVERIFIED] (02 Gaps 7 and 12; N16). G-38. | Affects which repository a push targets, and whether hidden config reaches git. | Brainstorm decision on scope. If it is in scope, observe both in a governed Orca session that writes only under `/tmp`. |
| 20 | Design D19-47 (line 534) says non-fast-forwards are rejected before pre-push [CODE-CONTRADICTED in part]. A "fetch first" rejection reaches the hook (04 E23a), and `transport.c` v2.47.3 lines 1315-1319 filter only non-fast-forward, stale-lease, remote-updated and up-to-date refs (web-01 Area I, external). | The design text misstates git behaviour that the guard relies on. | Owner approval of web-01 recommendation 8: reword design line 534 (Section 8 Phase 7.2). |
| 21 | Header line 4 of `src/superclaude/hooks/scripts/launch-job-identity.sh` says "descendants", but the selector uses kernel session membership [CODE-CONTRADICTED wording] (01 Gaps 9). | Misleads readers about how identity is chosen. | Wording fix in the same change that builds L2 (Section 8 Phase 7.6). The decision owner is whoever reviews that PR. |
| 41 | (Added at Gate 3, cycle 1; numbered after row 40 so earlier row references stay valid.) Accept that the variant A-i hook trusts the `uv` binary named by `<hooks-dir>/pre-push.uv-dir`? Step 2.5(b) checks the file, the directory and `uv` for owner, mode and content before every launch, and the step 5.1 L1 tokens cover writes to the file, but when `uv` and its directory are owned by the pushing user, a same-user rewrite of `uv` itself passes every check. G-6 (variant A-i). | If `uv` is user-owned, a same-user writer can make the selector answer `ordinary` and push to main/master. On this host `uv` is root-owned (`/usr/local/bin/uv`, 0755), so the case does not arise here. | Owner decision: accept and list it among the design §19 limits, or require in step 2.5(b) that `uv` and its directory be root-owned (refusing user-owned installs with `not-owned`), or choose variant A-iii (row 1). |

### 9.2 [UNVERIFIED] git, platform and test claims (experiments or documents needed)

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| 22 | Stdin record order. git does not document it (web-01 Key Findings), and it was observed both ways: command-line order in 04 E7 and web-01 G3 (simple creates), not command-line order in 04 E9, E19 and E24 (E24: two runs gave the same stream, existing remote ref first). See the contradiction row in 9.4. G-24 (resolved only as "the hook scans every record"). | Low, provided the hook checks every record. | No decision needed: the hook checks every line and does not rely on order (Section 8 Phase 1.6). |
| 23 | Does the hosting service treat `refs/heads/Main` as `main`? git is case-sensitive (04 E25; web-01 G2, external). GitHub behaviour was not checked. G-25. | A push to `Main` passes the exact-match guard. Whether GitHub then aliases it to `main` is unknown. | Read GitHub's branch-naming documentation, or test on a throwaway GitHub repository, which needs explicit owner approval because this task forbids pushing to real remotes. |
| 24 | Network transports (SSH, HTTPS): hook timing, filtering after the remote advertisement, and whether "fetch first" is delivered over the network. Only local transports were run (04). The source shows FETCH_FIRST is delivered (web-01 Area I). G-27 (partly resolved). | The guard's view of the stdin set over a real remote is not observed. | Experiment: a sandbox `git daemon` or `ssh localhost` bare remote under `/tmp`, re-running the 04 E23 cases. |
| 25 | D19-42: can git ever send a malformed or padded record? See the contradiction note in 9.4. G-28 (partly resolved). | If the hook refuses more than four fields, legitimate pushes break. | Settled by web-01 recommendation 1: parse with `rsplit(" ", 3)` and decide only on field 3. Add web-01 G5's six-field `HEAD@{0 days ago}:refs/heads/main` record to the test plan (Section 8 Phase 6.2). |
| 26 | Is `extensions.worktreeConfig` enabled in this repository? [UNVERIFIED] (02 Gaps 10). G-31. | Decides whether the E31 per-worktree hooksPath hole is live here. | One read-only check, `git config --get extensions.worktreeConfig`, in the main checkout. Section 8 Phase 2.3 handles both answers. |
| 27 | Design §19.1 actor selection by process ancestry (B-CTX) has one data point (04 E1) and no lifecycle variants [UNVERIFIED]. G-32. | Identity under resume, nested shells and subagents is unobserved. | B-CTX is DECIDED as a documented limit (seed-brief line 74). Re-run identity observations alongside `tests/hooks/test_launch_level_observations.py` if the scope widens. |
| 28 | Orca's worktree-removal path is untested. Only plain `git worktree remove` was run (04 F2). G-37. | Stale hook or config after an Orca removal is unobserved. | Experiment: `orca worktree rm` on a throwaway worktree created with an agent, then inspect the common dir hooks. This needs owner approval, since this task may not create worktrees. |
| 29 | The L1 section 9 evasions are static readings of the guard, not executed (02 Gaps 13). G-39. | L1 coverage claims may be wrong in either direction. | Add each evasion as a case in `tests/hooks/test_launch_level_guard_l2_bypass.py` (new file, Phase 6.7; issue #440 edits `test_launch_level_guard.py`, seed brief line 59) and run `uv run pytest tests/hooks/test_launch_level_guard_l2_bypass.py`. |
| 30 | Local-path remotes can be changed by `update-ref` or `fetch` run in the remote directory (02 Gaps 14). G-40. | Not relevant to GitHub remotes. | Document as out of scope in design §19. No experiment needed. |
| 31 | The only real-git pre-push code is a TEST policy (`tests/hooks/test_launch_job_identity.py` lines 1175-1232) that crashes on malformed records (03). G-41. | Not reusable as the production hook. | Write a new hook using web-01 recommendation 1 (the right-split). Keep or fix the test policy in the same PR (Section 8 Phase 6.6). |
| 32 | A large push with a hook that never reads stdin: a Gate 1 QA sandbox run (3000 refs) exited 0 and created 3001 branches on 2.47.3 (qualitative F8). This is not in 04. web-01 cites `transport.c` lines 1327-1329, which tolerate EPIPE. G-42. | On 2.47.3, an early exit is tolerated (EPIPE is ignored) and the push outcome follows the hook's exit code. | Confirm the stdin rule used throughout this report (Section 8 Phase 1.7): `governed`, `unknown` and no-verdict paths read stdin to EOF before an allow; a refusal may exit at the first protected record (EPIPE tolerated); `ordinary` and `released` exit 0 without reading (T-10, D19-26). Add a 3000-ref case to the sandbox tests in Section 8 Phase 6.2. |
| 33 | Remaining design §19 statements with no code, tests or observations: no code D19-1, 3, 9, 13, 14, 24, 26, 38; no tests D19-40, 41, 43-46, 50; uncheckable D19-6, 34, 51, 57, 82; partial D19-31, 65, 70, 72, 77 (03). The git parts of D19-21, 23, 27, 29, 35 and 41 are settled by 04 Step 2.5. G-43. | Design claims with no evidence behind them. | Write a test or observation for each testable item in Section 8 Phase 6. Mark the uncheckable ones as design intent in the design text. |
| 34 | Remote groups: on newer git, `git push <group>` continues to the remaining remotes after a failure. Whether pre-push runs once per member is not stated. The feature is absent from 2.47.3 (web-01 lines 113-114 and 411, external: https://git-scm.com/docs/git-push). | A future-version risk to "one nonzero exit aborts the whole push" (04 E19). | Record the version as tested on 2.47.3; re-run the Phase 6 real-git suite before relying on any version at or above 2.54.0 (hook API rewrite, configured hooks) and when 2.98.0 ships; the guard tests record `git --version` (web-01 recommendation 7; Section 8 Phase 6.10). Re-test with a remote group when the runtime git gains the feature. |
| 35 | `hook.<event>.enabled=false` will also disable hooks-directory hooks. This is in an unreleased 2.98.0 draft (web-01 line 410, external: https://github.com/git/git/blob/master/Documentation/RelNotes/2.98.0.adoc). Config-defined hooks arrive in 2.54.0. | `-c hook.pre-push.enabled=false` would disable the guard. | Add it to the L1 coverage list now (web-01 recommendation 5), and re-check when 2.98.0 is released. |
| 36 | JGit runs pre-push (since 4.2), but its `core.hooksPath` and worktree parity with C git were not checked (web-01 line 295, external: https://github.com/eclipse-jgit/jgit). GitPython's `no_verify=True` mapping to `--no-verify` is by convention and untested (web-01 line 349). | Library pushes may bypass the hook in ways not covered. | Experiment in a `/tmp` sandbox once the libraries are installed with `uv pip install` in a throwaway venv. Gate 1 fix-log B2 routed this because the libraries are not installed. |
| 37 | `--config-env=core.hooksPath=VAR` and `GIT_CONFIG_COUNT/KEY/VALUE` set hooksPath per process. They are documented (web-01 lines 133-135, external: https://git-scm.com/docs/git-config, https://git-scm.com/docs/git) but not tested locally; 04 tested only `-c`. | Further per-process L2 bypasses. L1 sees them only when they are written in the command. | Add both forms to the 04-style sandbox experiments and to the L1 coverage list (web-01 recommendation 5). |
| 38 | GitHub endpoints that move refs without `git push` (merge, contents API commits) were not enumerated (web-01 line 323, external: https://docs.github.com/en/rest/git/refs). The Stack Overflow answer on empty pre-push stdin was not read (web-01 line 438). | The list of server-side bypasses is incomplete. Only branch protection covers them. | Document in design §19 that branch protection or rulesets are the control for API writes. The full enumeration is optional reading of the GitHub REST docs. |
| 39 | `O_TMPFILE` on ext4 on this host (the git common dir is on ext4 under `/home/coder`) was not tested. It failed on the overlay `/tmp` under kernel 6.8 (web-02 line 321). | Only matters if `O_TMPFILE` publication is chosen. web-02 recommends against it. | No experiment needed if web-02 recommendation 6 is adopted (no `rename` or `O_TMPFILE`; use the O_EXCL temp, fchmod 0755, fsync, link, then fsync the directory). |
| 40 | overlayfs support for `RENAME_NOREPLACE` has no documented kernel version (web-02 line 218, external: https://man7.org/linux/man-pages/man2/rename.2.html). The distro build flags for the `.exe` fallback (web-02 line 154, LOW). `find_hook` in git versions other than 2.47.3 (web-02 line 179). google/renameio issue 39 was not read (web-02 line 237). | Low. These matter only if renameat2, a non-upstream git build, or an older git is used. | Adopt web-02 recommendation 6 (no renameat2). git is tested on 2.47.3 only; re-run the Phase 6 real-git suite before relying on any version at or above 2.54.0 (hook API rewrite, configured hooks) and when 2.98.0 ships, with the guard tests recording `git --version` (web-01 recommendation 7). Re-read `hook.c` `find_hook` when the minimum version changes. |

### 9.3 Resolved items (listed for traceability)

| # | Item | Resolution | Where resolved |
|---|------|------------|----------------|
| R1 | Unknown identity: what happens to a push when the verdict is `unknown` | DECIDED by the owner, 2026-11-08: refuse only pushes to main or master, with a diagnostic, and allow everything else | `.dev/brainstorms/20261108-094705-l2-pre-push-guard/seed-brief.md` line 73, recorded in research file 01 §4. Rows 1 and 2 cover only the open implementation details. |
| R2 | Scope given B-CTX FAIL | DECIDED: build for the tested local Bash surface; document the B-CTX gaps as limits | seed-brief line 74 |
| R3 | IR-7 default | DECIDED off: `W-L2-ABSENT` stays a warning, built in a separate, clearly marked commit. Proposed mechanism: the module constant `L2_REFUSAL_ENABLED = False` (step 4.4), tested by Phase 6.11. Only the turn-on timing stays open (row 12). | seed-brief line 77 |
| R4 | G-1 / D19-30 API part: do API and smart-HTTP writes bypass pre-push? | Resolved by documentation: they bypass it. Documented externally (web-01 H/J); not confirmed at runtime. | web-01 J7, J8, H3 |
| R5 | G-2: do libraries run the hook? | Resolved by documentation: libgit2/pygit2, dulwich and isomorphic-git do not; JGit (4.2+) and GitPython do. Documented externally (web-01 H/J); not confirmed at runtime (the libraries are not installed; runtime confirmation is row 36). | web-01 J1-J6, J10 table |
| R6 | G-3: the git version that introduced each behaviour | Version table | web-01 F2 |
| R7 | G-4: Linux no-replace publication | `link`/O_EXCL with EEXIST; never `rename`/`os.replace`; `publish()` uses mode 0400 and no fsync, so it is not reusable unchanged | web-02 |
| R8 | G-5: git's exec-bit check | `find_hook` `access(X_OK)`, `hook.c` line 21; the hint appears only on EACCES | web-02 |
| R9 | G-26: `--path-format=absolute --git-path hooks/pre-push` | Documented; honours hooksPath (2.10.0+). Verified on 2.47.3 from a linked worktree (web-01 D3a-e) and from the main checkout (`qa/qa-lens-domain-accuracy.md` finding 1; fix run X1 in `qa/qa-fix-log.md`); see the note under Section 2.5(c). | web-01 D3a-e; QA re-runs |
| R10 | G-29: `refs//heads/main` | An invalid refspec, refused before the hook | web-01 G1 (git-check-ref-format rule 6) |
| R11 | G-30: `--mirror` with an explicit refspec | Fatal | web-01 G4 |
| R12 | G-15 (L2 part): a destination from config | L2 sees it as field 3 | 04 E20 (the L1 part is row 10) |
| R13 | G-22: line-487 corpus wrongly reported absent | Fixed | Gate 1, `qa/qa-research-fix-log.md` B3 |
| R14 | G-23: 04 lacked Key Takeaways | Fixed | Gate 1, `qa/qa-research-fix-log.md` B1 |
| R15 | G-6 documentation (no-uv human) | Documented; the design choice is row 1 | Gate 1, `qa/qa-research-fix-log.md` B4 |

### 9.4 Contradictions between research files

| Topic | Side A | Side B | Stronger evidence |
|-------|--------|--------|-------------------|
| D19-42: git never sends a malformed record | 04 Step 2.5 (line 1796): "CONFIRMED for the tested scope". Every record in E1-E31 and F1-F3 had four fields, and space-padded destinations are refused before the hook (F3). | web-01 G5 (lines 236-246, 430, 453): `git push --dry-run origin 'HEAD@{0 days ago}:refs/heads/main'` delivered a SIX-field record on the installed 2.47.3, because field 1 is not validated as a refname. | web-01: a verbatim local test plus a source citation. 04's claim is limited to its own runs and is not wrong within that scope. Use web-01 for the parser (row 25). |
| D19-47: non-fast-forwards are rejected before pre-push | Design line 534 | 04 E23a (a fetch-first record is delivered) and web-01 Area I (`transport.c` lines 1315-1319) | 04 and web-01 agree, against the design text (row 20). |
| No-uv remedy | 04 line 1530 (an absolute uv path) | Gate 1 qualitative F1 and gap G-6: an absolute path is not enough | Gate 1 / G-6. 04 line 1530 is superseded (editorial note N-3). |
| Stdin record order (G-24) | 04 E7 (line 549) and web-01 G3: records arrived in command-line order for simple creates | 04 E9 (line 702), E19 and E24 (line 1339): not command-line order; in E24 two runs gave the same mixed-order stream, existing remote ref first | 04 E24 (two runs, mixed order). Order is undocumented (web-01 Key Findings), so neither side is a guarantee. Resolution: the hook scans every record and does not depend on order (row 22; Section 8 Phase 1.6). |
| Evidence citation for "one nonzero exit aborts the whole push" | Earlier text cited "E9-E11" | Gate 1 fix-verification M4 / N21: cite E19 | E19, per `gaps-and-questions.md` editorial notes. |

---

## 10. Evidence Trail

All paths are relative to `.dev/tasks/to-do/TASK-RESEARCH-pre-push-guard-20261108-095046/`.

### 10.1 Codebase Research

| File | Topic | Status | Key finding |
|------|-------|--------|-------------|
| `research/01-identity-selector-ancestry.md` | Identity selector and process ancestry (`src/superclaude/hooks/scripts/launch-job-identity.sh`) | Complete | Selection is by kernel session membership, with no PPID walk. The verdicts are governed, ordinary, released and unknown. The owner's unknown-identity decision is recorded in §4. With no uv on PATH, the script exits 2 (no verdict), which must map to `unknown`. `setsid` and a different HOME escape to `ordinary`. `publish()` (O_EXCL temp, fchmod 0400, link, unlink, no fsync) is not reusable unchanged for an executable hook. |
| `research/02-l1-guard-push-bypass-coverage.md` | L1 guard coverage of push spellings and bypasses (`src/superclaude/hooks/scripts/launch-level-guard.sh`) | Complete | L1 has no git-hooks tamper token. The underscore env-prefix command-position bypass contradicts LL-UNKNOWN line 80. Config writes with no git word go unrefused (LL-TAMPER line 95 is partial). L1 cannot see `remote.origin.push` destinations. Smart-HTTP and non-literal API hosts are not refused. The section 9 evasions are static readings. |
| `research/03-design-and-claim-code-crossvalidation.md` | Design §19 (`docs/designs/sc-issue-launch-level-hook.md`) cross-validated against the claim code (`src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`, `src/superclaude/cli/install_hooks.py`) | Complete | `l2_status` (line 1012) has no ownership marker and folds failures into `absent`. IR-7 is a `W-L2-ABSENT` warning in `cmd_launch` (line 1312), not the refusal that design lines 355 and 514 describe. D19-16 and D19-18 are contradicted. `install_hooks.py` is user-global only. The §19.6 artifacts are absent. The only real-git pre-push policy is a test (`tests/hooks/test_launch_job_identity.py` lines 1175-1232) that crashes on malformed records. |
| `research/04-empirical-git-prepush-experiments.md` | Real-git pre-push experiments (E1-E31, F1-F3) on git 2.47.3 in `/tmp` sandboxes with local bare remotes | Complete | The argv and stdin record contract was confirmed. Empty stdin is valid (E12, E23b, E27a). "Fetch first" reaches the hook (E23a, contradicting D19-47 in part). One nonzero exit aborts the whole push (E19). Bypasses: `--no-verify`, `-c core.hooksPath`, a non-executable hook (E29), and per-worktree hooksPath (E31). Refs are case-sensitive (E25). In Step 2.5, 15 of 17 rows are CONFIRMED. |
| `research/research-notes.md` | Scope discovery and agent assignments for this task | Complete | Defines the research question, the existing-file list and the web-01 / web-02 scopes that the gaps were routed to. |

### 10.2 Web Research

All rows are external context, not observations in this repository.

| File | Topic | Main sources |
|------|-------|--------------|
| `research/web-01-git-official-docs-and-versions.md` | Official git documentation for pre-push and related behaviour; the git version that introduced each behaviour; libraries and APIs that bypass the hook | https://git-scm.com/docs/githooks, https://git-scm.com/docs/git-push, https://git-scm.com/docs/git-config, https://git-scm.com/docs/git-hook, https://git-scm.com/docs/git-send-pack, https://git-scm.com/docs/gitprotocol-http, https://git-scm.com/docs/git-check-ref-format, https://github.com/git/git/blob/v2.47.3/transport.c, https://github.com/git/git/blob/master/Documentation/RelNotes/ (per version), https://libgit2.org/docs/reference/main/remote/git_remote_push.html, https://github.com/libgit2/libgit2/issues/964, https://www.pygit2.org/remotes.html, https://github.com/eclipse-jgit/jgit (PrePushHook.java), https://isomorphic-git.org/docs/en/push, https://github.com/jelmer/dulwich/blob/main/docs/c-git-compatibility.txt, https://github.com/gitpython-developers/GitPython/blob/main/git/remote.py, https://docs.github.com/en/rest/git/refs, https://cli.github.com/manual/gh_api |
| `research/web-02-linux-atomic-publication-and-exec-bit.md` | Linux atomic no-replace file publication; git's executable-bit requirement for hooks | https://man7.org/linux/man-pages/man2/link.2.html, https://man7.org/linux/man-pages/man2/open.2.html, https://man7.org/linux/man-pages/man2/rename.2.html, https://man7.org/linux/man-pages/man2/chmod.2.html, https://man7.org/linux/man-pages/man2/umask.2.html, https://docs.python.org/3/library/os.html, https://lkml.iu.edu/hypermail/linux/kernel/2405.2/05667.html, git v2.47.3 `hook.c`, `path.c`, `transport.c` and `config.mak.uname` (https://github.com/git/git/blob/v2.47.3/) |

### 10.3 Synthesis Files

Each synthesis file also carries its own source-coverage table; those meta tables are not reproduced here.

| File | Report sections |
|------|-----------------|
| `synthesis/synth-01-problem-current-state.md` | 1 Problem Statement, 2 Current State Analysis |
| `synthesis/synth-02-target-gaps-external.md` | 3 Target State, 4 Gap Analysis, 5 External Research Findings |
| `synthesis/synth-03-options-recommendation-plan.md` | 6 Options Analysis, 7 Recommendation, 8 Implementation Plan (G-1 to G-43 mapping; its OQ-1 to OQ-20 are carried as Section 9 rows) |
| `synthesis/synth-04-questions-evidence.md` | 9 Open Questions, 10 Evidence Trail |

### 10.4 QA Reports

Files under `qa/` at assembly time (24):

| File | Gate |
|------|------|
| `qa/qa-task-validation-structure-report.md` | Task file validation (structure) |
| `qa/qa-task-validation-b2-report.md` | Task file validation (B2) |
| `qa/qa-task-validation-fix-cycle1.md` | Task file validation fix, cycle 1 |
| `qa/qa-task-validation-verify-cycle1.md` | Task file validation verification, cycle 1 |
| `qa/qa-task-validation-consolidated.md` | Task file validation, consolidated |
| `qa/qa-task-research-alignment-report.md` | Task and research alignment |
| `qa/qa-task-research-alignment-fix.md` | Task and research alignment fix |
| `qa/qa-qualitative-operational-report.md` | Qualitative review (operational) |
| `qa/qa-qualitative-sufficiency-report.md` | Qualitative review (sufficiency) |
| `qa/qa-qualitative-fix.md` | Qualitative review fix |
| `qa/analyst-completeness-report.md` | Gate 1 research completeness (FAIL: I-1, I-2, m-1 to m-14) |
| `qa/qa-research-qualitative-report.md` | Gate 1 research qualitative (FAIL: F1 to F8) |
| `qa/qa-research-gate-report.md` | Gate 1 research gate (FAIL: 1 IMPORTANT, 8 MINOR) |
| `qa/qa-consolidated-findings-phase3-cycle0.md` | Gate 1 consolidated findings, cycle 0 |
| `qa/qa-research-fix-log.md` | Gate 1 fix log, cycle 0 (B1 to B4) |
| `qa/qa-research-fix-verification-cycle0.md` | Gate 1 fix verification, cycle 0 (PASS: M1 to M4) |
| `qa/qa-research-fix-verification-qualitative-cycle0.md` | Gate 1 qualitative fix verification, cycle 0 (PASS: N-1 to N-4) |
| `qa/qa-synthesis-qualitative-report.md` | Synthesis gate, qualitative review |
| `qa/analyst-synthesis-review.md` | Synthesis gate, analyst review |
| `qa/qa-synthesis-gate-report.md` | Synthesis gate report |
| `qa/qa-consolidated-findings-phase5-cycle0.md` | Synthesis gate consolidated findings, cycle 0 |
| `qa/qa-synthesis-fix-log.md` | Synthesis gate fix log |
| `qa/qa-synthesis-fix-verification-cycle0.md` | Synthesis gate fix verification, cycle 0 |
| `qa/qa-synthesis-fix-verification-qualitative-cycle0.md` | Synthesis gate qualitative fix verification, cycle 0 |

Later gate, validation and reflect reports: see `qa/` and `reflect/post/`; the final list is in the Task Log of the task file.

### 10.5 Task Files and Gaps Log

| File | Role |
|------|------|
| `TASK-RESEARCH-pre-push-guard-20261108-095046.md` | The task file (checklist and Task Log) |
| `BUILD-REQUEST.md` | The build request that defined this research task |
| `gaps-and-questions.md` | 43 gaps (G-1 to G-43), the [UNVERIFIED] and [CODE-CONTRADICTED] claims table, and the editorial notes. Section 9 accounts for every gap: each is either an open row (9.1, 9.2) or a resolved row (9.3) that names where it was resolved; Sections 8.8 and 8.9 give the step or row for each gap. |
| `.dev/brainstorms/20261108-094705-l2-pre-push-guard/seed-brief.md` (repository path) | Owner decisions cited as "seed brief line N" (lines 68, 73-78) |
