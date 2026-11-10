# Research Notes: git pre-push hook semantics for the L2 launch-level guard

**Date:** 2026-11-08
**Scenario:** A (explicit request: six sub-questions a-f plus named files)
**Depth Tier:** Standard (3 named source files, ~1900 lines; most of the question is external git/Linux semantics best answered by official docs plus real-git experiments)
**QA intensity:** standard (tier default)
**Status:** Complete

Research question (verbatim): "Exact semantics of git's pre-push hook relevant to a guard that refuses an AI agent's push to refs/heads/main or refs/heads/master: (a) stdin record format '<local ref> <local oid> <remote ref> <remote oid>' for create, update, delete (local oid all zeros), force (+refspec), HEAD:main, multiple refspecs, --mirror, --all, --tags; behaviour on empty stdin; arguments $1 remote name and $2 URL. (b) Which push paths skip the pre-push hook: --no-verify, -c core.hooksPath=/dev/null or another dir, git send-pack, push via other tools. (c) Where git looks up hooks in linked worktrees: the common dir vs per-worktree, git rev-parse --git-path hooks, core.hooksPath semantics, extensions.worktreeConfig. (d) The hook's process ancestry (git -> hook) and environment (GIT_DIR and others) when run from a linked worktree. (e) Atomic file publication without replacing an existing file on Linux (link(2)/O_EXCL vs rename), and the executable-bit requirement. (f) Which git version introduced each behaviour, and the git version installed here."

WHY: input to a /sc:brainstorm on building the L2 pre-push layer of the launch-level guard (issue #441). Findings feed a spec decision on hook behaviour, placement/installer, ownership check and the IR-7 refusal.

OUTPUT_TYPE: system understanding + implementation constraints (facts a spec can cite), with options for placement/publication.

Environment facts (from commands run during scope discovery):
- `git --version` -> `git version 2.47.3`
- `uname -r` -> `6.8.0-147-generic` (Linux)
- Worktree: /home/coder/workspaces/worktrees/IronClaude/issue-441 (a linked worktree; `.git` is a file)

---

## EXISTING_FILES

| Path | Lines | Purpose / relevance |
|---|---|---|
| src/superclaude/hooks/scripts/launch-level-guard.sh | 747 | L1 Bash text guard. Line 528 regex `( |/git-| git-)(push|send-pack|http-push) ` (hidden push plumbing); line 532 regex includes `hookspath`, `alias\.`, `pushurl`, `insteadof`; line 661 canonical-push regex (only `git push [-u] origin <branch>[:<branch>]` passes); line 59 refusal text for push to master or main. No `.git/hooks` tamper token (seed brief). |
| src/superclaude/hooks/scripts/launch-job-identity.sh | 566 | Job identity selector. `identify(pid)` (line 215) reads `/proc/<pid>/stat` kernel session id (field 6, `proc()` line 202-207), looks up `jobs/<sid>.json`, validates pid/start ticks/boot_id/uid, then the origin session's level record; returns governed / ordinary / unknown. `publish()` (line 164-174) already uses the O_EXCL temp file + fchmod + `os.link` no-replace pattern. Supervisor calls `os.setsid()` (line 292). |
| docs/designs/sc-issue-launch-level-hook.md §19 (lines 489-578) | 90 | L2 contract: actor selection (19.1), placement (19.2), stream rules (19.3), release (19.4), tests (19.5), selector (19.7), status (19.8). Cites githooks, git-push, core config docs. |
| src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py | — | `l2_status()` line 1012-1029: runs `git -C wt rev-parse --git-path hooks/pre-push`, joins a relative answer to wt, reports present-unverified if executable file. `REMEDY["W-L2-ABSENT"]` line 789, `L2_ABSENT_WHY` line 796. Used at line 1311. |
| src/superclaude/cli/install_hooks.py | — | Hook installer for Claude Code hooks; no git-hook install path (U28). |

## PATTERNS_AND_CONVENTIONS

- No-replace publication already exists in the codebase: launch-job-identity.sh `publish()` = `open(O_CREAT|O_EXCL|O_NOFOLLOW)` temp name, write, `fchmod`, `link(tmp, name)` (fails with EEXIST if target exists), `unlink(tmp)`.
- Kernel process-session membership (not PPID chain) is the actor-selection basis (`identify`). A pre-push hook inherits the session of git, which inherits the shell's session, unless something calls setsid.
- Path resolution goes through git (`rev-parse --git-path`), never assumes `.git` is a directory (design §19.2, l2_status).

## SOLUTION_RESEARCH

Questions to answer with official docs + experiments:
- githooks(5) pre-push: arguments, stdin lines, zero-oid convention for delete/new, exit status semantics, `--no-verify`.
- git-push(1): refspec forms (`+`, `HEAD:main`, `:main`), `--mirror`, `--all`, `--tags`, `--dry-run`, `--atomic`, `--no-verify`, `--porcelain`.
- git-config core.hooksPath: relative path semantics, per-command `-c`, `/dev/null`.
- git-worktree(1) / gitrepository-layout(5): hooks shared in common dir; `extensions.worktreeConfig` and `config.worktree`.
- git-rev-parse(1) `--git-path` and its core.hooksPath adjustment; `--git-common-dir`.
- Environment given to hooks (githooks "environment" notes: GIT_DIR, GIT_PREFIX? GIT_EXEC_PATH, cwd at worktree root).
- Linux: link(2), open(2) O_EXCL, rename(2) replaces, renameat2(2) RENAME_NOREPLACE; git's hook executable check (run-command `find_hook` uses access(X_OK); "hook was ignored because it's not set as executable" advice, advice.ignoredHook).
- Version history: pre-push added git 1.8.2; core.hooksPath 2.9.0; worktree 2.5; extensions.worktreeConfig 2.20; `--no-verify` for push 1.8.2; hook.* config (2.36 `git hook run`)... all to be verified from release notes.

## RECOMMENDED_OUTPUTS

- research/01-identity-selector-ancestry.md
- research/02-l1-guard-push-bypass-coverage.md
- research/03-design-and-claim-code-crossvalidation.md
- research/04-empirical-git-prepush-experiments.md
- research/web-01-git-official-docs-and-versions.md
- research/web-02-linux-atomic-publication-and-exec-bit.md
- synthesis/synth-01-problem-current-state.md (S1, S2)
- synthesis/synth-02-target-gaps-external.md (S3, S4, S5)
- synthesis/synth-03-options-recommendation-plan.md (S6, S7, S8)
- synthesis/synth-04-questions-evidence.md (S9, S10)
- RESEARCH-REPORT-pre-push-guard.md

## SUGGESTED_PHASES

Phase 2 codebase agents (parallel):
1. Code Tracer — identity selector and process ancestry. Files: src/superclaude/hooks/scripts/launch-job-identity.sh (all, esp. lines 1-60 bash wrapper, 202-260 proc/identify/members, 291-400 supervise/run). Questions: how a pre-push hook would call `identify` (default PID = caller? hook's own PID?), what happens when git or a wrapper calls setsid, what `unknown` means for a protected push. Output research/01-identity-selector-ancestry.md.
2. Code Tracer — L1 coverage of push spellings and bypasses. File: src/superclaude/hooks/scripts/launch-level-guard.sh (lines 40-140 messages, 470-700 classifier). Questions: which of `--no-verify`, `-c core.hooksPath=`, `git send-pack`, `GIT_DIR=` tricks, `.git/hooks` edits, `git config core.hooksPath` the text layer refuses today. Output research/02-l1-guard-push-bypass-coverage.md.
3. Doc Analyst — design §19 and claim code cross-validation. Files: docs/designs/sc-issue-launch-level-hook.md lines 489-578; src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py (l2_status 1012-1029, REMEDY 780-800, line 1300-1320, cmd_launch IR-7 comment); src/superclaude/cli/install_hooks.py. Tag every doc claim CODE-VERIFIED / CODE-CONTRADICTED / UNVERIFIED. Output research/03-design-and-claim-code-crossvalidation.md.
4. Empirical tester (Code Tracer type, real git 2.47.3) — in a `mktemp -d` dir under /tmp only: bare remote, clone, linked worktree; a logging pre-push hook that dumps argv, stdin records, env (GIT_*), cwd, PID/PPID/SID/process tree. Run pushes: create, update, delete (`:main`, `--delete`), force (`+`, `--force`), `HEAD:main`, multiple refspecs, mixed, `--all`, `--tags`, `--mirror`, up-to-date (empty stdin?), `--dry-run`, `--no-verify`, `-c core.hooksPath=/dev/null`, `-c core.hooksPath=<other dir>`, `git send-pack`, non-executable hook, hook in worktree-private git dir, `extensions.worktreeConfig` + `config.worktree` hooksPath, `rev-parse --git-path hooks` with and without core.hooksPath. Record before/after remote refs. Never push to any real remote. Output research/04-empirical-git-prepush-experiments.md.

Phase 4 web agents (parallel):
- web-01: official git docs (git-scm.com/docs/githooks, git-push, git-config core.hooksPath, git-worktree, git-rev-parse, gitrepository-layout, git-send-pack, RelNotes on github.com/git/git/tree/master/Documentation/RelNotes) — semantics and version introduced for every behaviour in (a)-(d), (f). Added in the Gate 1 cycle 0 fix: also sub-question (b) "push via other tools": whether pygit2/libgit2, dulwich, GitPython and JGit pushes run the client-side pre-push hook, from each library's own documentation or source (named in 04 Gaps, "ROUTE web-01: (b) other tools").
- web-02: Linux man pages (man7.org link(2), open(2), rename(2)/renameat2) and git source for hook executable check (run-command.c / hook.c find_hook, advice.ignoredHook) — (e), (f).

Synthesis mapping: synth-01 <- 01,02,03,04; synth-02 <- all + web; synth-03 <- all; synth-04 <- all.

## TEMPLATE_NOTES

Template 02 (complex: discovery, parallel agents, QA gates, assembly).

## AMBIGUITIES_FOR_USER

None — intent is clear. Note: design §19 doc claims (e.g. "Official Git documents dry-run as not sending updates; Q artifacts report local hook invocation") are [UNVERIFIED] until the empirical agent and web-01 confirm them.
