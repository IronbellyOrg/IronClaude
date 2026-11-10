# Research: Official git documentation for the pre-push hook, related behaviour, and the git version that introduced each behaviour

**Scope:** External (official git documentation, git release notes, documentation of other git tools and hosting APIs). Answers sub-questions (a)-(d) and (f), plus area "Pushes via other tools" (sub-question (b), design line 520 claim).
**Status:** Complete
**Date:** 2026-11-08
**Installed git (source of truth for current behaviour):** 2.47.3, kernel 6.8.0-147-generic (file 04)

WEB SEARCH PROVENANCE: provider=WebSearch/WebFetch reason=tavily-unavailable (no `mcp__tavily__*` tool is present in this agent's tool list at runtime).

Reliability scale used below: R1 = official git documentation or release notes (git-scm.com, git/git repository); R2 = official documentation of another tool or service; R3 = well-maintained repository or source code; R4 = blog or forum.

---

## Area A. githooks(5): the pre-push hook contract

### A1. The pre-push section (current web page and installed 2.47.3 man page agree word for word)

- **Source:** https://git-scm.com/docs/githooks (page header: "githooks last updated in 2.54.0"), R1. Cross-check: `MANWIDTH=200 MANPAGER=cat man githooks | col -b` on the installed git 2.47.3 (`git --version` printed `git version 2.47.3`). The pre-push text is identical in both.
- **Governing sentences (verbatim):**
  - "This hook is called by git-push(1) and can be used to prevent a push from taking place. The hook is called with two parameters which provide the name and location of the destination remote, if a named remote is not being used both values will be the same."
  - "Information about what is to be pushed is provided on the hook's standard input with lines of the form: `<local-ref> SP <local-object-name> SP <remote-ref> SP <remote-object-name> LF`"
  - "If the foreign ref does not yet exist the <remote-object-name> will be the all-zeroes object name. If a ref is to be deleted, the <local-ref> will be supplied as (delete) and the <local-object-name> will be the all-zeroes object name. If the local commit was specified by something other than a name which could be expanded (such as HEAD~, or an object name) it will be supplied as it was originally given."
  - "If this hook exits with a non-zero status, git push will abort without pushing anything. Information about why the push is rejected may be sent to the user by writing to standard error."
- **Relation to our findings:**
  - argv: SUPPORTS file 04 (argv1 = remote name or URL, argv2 = URL; "both values will be the same" when no named remote).
  - Record format and zero oid for create and delete: SUPPORTS E3/E4 (`(delete) <zero-oid> refs/heads/main <old>`).
  - "abort without pushing anything": SUPPORTS E19/E24/E26 (one nonzero exit aborts the whole push, atomic or not).
  - Field 1 is "supplied as it was originally given" when not an expandable name: EXTENDS. Field 1 is therefore NOT always a full ref (it can be `HEAD~`, a raw oid, or `(delete)`); only field 3 is documented as the remote ref. This supports design 19.3 treating field 3 as authoritative.
  - The documentation does NOT say field 3 is always fully qualified. File 04 observed that it is (E6, E20, E21, E11). That is an observed behaviour, not a documented guarantee. DISCREPANCY (gap in docs, not a contradiction): the guard relies on an undocumented-but-observed property.
  - The documentation is silent about record order, about up-to-date or rejected refs being omitted (E12, E23b, E27a), about dry-run, and about `--no-verify` (that flag is documented on git-push, see Area B).
- **Relevance:** HIGH.

### A2. The DESCRIPTION section: hook location, executable bit, working directory, environment

- **Source:** https://git-scm.com/docs/githooks (R1); same text in installed 2.47.3 man page.
- **Governing sentences (verbatim):**
  - "Hooks are programs you can place in a hooks directory to trigger actions at certain points in git's execution. Hooks that don't have the executable bit set are ignored."
  - "By default the hooks directory is $GIT_DIR/hooks, but that can be changed via the core.hooksPath configuration variable (see git-config(1))."
  - "Before Git invokes a hook, it changes its working directory to either $GIT_DIR in a bare repository or the root of the working tree in a non-bare repository. An exception are hooks triggered during a push (pre-receive, update, post-receive, post-update, push-to-checkout) which are always executed in $GIT_DIR."
  - "Environment variables, such as GIT_DIR, GIT_WORK_TREE, etc., are exported so that Git commands run by the hook can correctly locate the repository."
- **Relation to our findings:**
  - "Hooks that don't have the executable bit set are ignored": SUPPORTS E29 (non-executable hook fails open; the hint is `advice.ignoredHook`, see Area C).
  - Working directory: pre-push is not in the exception list, so it runs in the root of the working tree (the linked worktree's root when pushing from a linked worktree). EXTENDS file 04.
  - "$GIT_DIR/hooks": in a linked worktree $GIT_DIR is the worktree-private directory, yet E30 showed the common-dir hooks directory is used and the worktree-private `hooks/` is ignored. The githooks page does not resolve this; git-worktree(1) and gitrepository-layout(5) do (Area D). DISCREPANCY in wording only: "$GIT_DIR/hooks" read literally would point at the private dir; observed behaviour (E30) is the source of truth.
  - Environment: the page lists exported `GIT_*` variables but says nothing about PATH. E28 observed PATH with `/usr/lib/git-core` prepended; that is not documented on this page. EXTENDS, no contradiction.
- **Relevance:** HIGH.

### A3. What githooks(5) does NOT say (negative results)

- The phrase "after it has checked the remote status, but before anything has been pushed" does NOT appear in the current githooks page or in the installed 2.47.3 man page. The brief asked to reason from that wording; whether it appears in a release note is checked in Area F. The current page only says the hook "is called by git-push(1) and can be used to prevent a push from taking place".
- No statement about record order, about filtering of up-to-date or rejected refs, about dry-run, about SHA-256 oid length, or about malformed records.
- **Relevance:** HIGH (it fixes which design statements rest on documentation and which rest only on file 04 observation).

## Area B. git-push(1): refspec forms, options, and the hook

- **Source:** https://git-scm.com/docs/git-push (page header: "git-push last updated in 2.55.0"), R1. Cross-check: `MANWIDTH=180 MANPAGER=cat man git-push | col -b` on installed 2.47.3. All option texts quoted below are identical in both unless noted.

### B1. `--[no-]verify`

- **Governing sentence (verbatim, both versions):** "Toggle the pre-push hook (see githooks(5)). The default is --verify, giving the hook a chance to prevent the push. With --no-verify, the hook is bypassed completely."
- **Relation:** SUPPORTS E14. It is the only documented, intended bypass flag on `git push`. It is a per-invocation flag, so a guard cannot detect it (the hook simply never runs).
- **Relevance:** HIGH.

### B2. `-n, --dry-run`

- **Governing sentence (verbatim, both versions):** "Do everything except actually send the updates."
- **Relation:** SUPPORTS E13 by implication: running the pre-push hook is part of "everything", and file 04 observed the hook receiving the real would-be records with no remote ref moved. The page does not mention the hook explicitly for dry-run, so "the hook runs on dry-run" is OBSERVED (E13), not literally documented. Design line 534 ("Official Git documents dry-run as not sending updates") matches this sentence exactly.
- **Relevance:** HIGH.

### B3. `--atomic`

- **Governing sentence (verbatim):** "Use an atomic transaction on the remote side if available. Either all refs are updated, or on error, no refs are updated. If the server does not support atomic pushes the push will fail."
- **Relation:** `--atomic` is a remote-side transaction. The local whole-push abort on a nonzero pre-push exit comes from githooks ("git push will abort without pushing anything"), independent of `--atomic`. SUPPORTS E19/E24/E26.
- **Relevance:** MEDIUM.

### B4. `--mirror`, `--all`/`--branches`, `--tags`, `-d/--delete`, `--porcelain`

- `--mirror` (verbatim): "Instead of naming each ref to push, specifies that all refs under refs/ (which includes but is not limited to refs/heads/, refs/remotes/, and refs/tags/) be mirrored to the remote repository. Newly created local refs will be pushed to the remote end, locally updated refs will be force updated on the remote end, and deleted refs will be removed from the remote end. This is the default if the configuration option remote.<remote>.mirror is set." SUPPORTS E11 (mirror records are full refs, may include forced updates and deletes of refs/heads/main).
- `--all, --branches` (verbatim): "Push all branches (i.e. refs under refs/heads/); cannot be used with other <refspec>."
- `--tags` (verbatim): "All refs under refs/tags are pushed, in addition to refspecs explicitly listed on the command line."
- `-d, --delete` (verbatim): "All listed refs are deleted from the remote repository. This is the same as prefixing all refs with a colon." SUPPORTS E4 (same record shape as `:<name>`).
- `--porcelain` (verbatim): "Produce machine-readable output. The output status line for each ref will be tab-separated and sent to stdout instead of stderr. The full symbolic names of the refs will be given." No effect on hook input documented.
- **`remote.<name>.mirror` combined with an explicit refspec (routed question):** neither the 2.55.0 web page nor the 2.47.3 man page states whether `--mirror` (or `remote.<name>.mirror`) may be combined with an explicit refspec; the only restriction sentence ("cannot be used with other <refspec>") is on `--all`. NOT DOCUMENTED. This needs a local experiment (UNSETTLED). See Recommendations.
- **Relevance:** MEDIUM (mirror HIGH for the guard because it can delete or force-update `refs/heads/main`).

### B5. Refspec forms and destination expansion (web 2.55.0 wording)

- **Governing sentences (verbatim):**
  - "The format for a refspec is [+]<src>[:<dst>], for example main, main:other, or HEAD^:refs/heads/main."
  - "The <dst> determines what ref to update on the remote side. It must be the name of a branch, tag, or other ref, not an arbitrary expression."
  - "The + is optional and does the same thing as --force."
  - "<src> without a :<dst> means to update the same ref as the <src>, unless the remote.<repository>.push configuration specifies a different <dst>."
  - "If <dst> unambiguously refers to a ref on the <repository> remote, then expand it to that ref."
  - "If <src> resolves to a ref starting with refs/heads/ or refs/tags/, then prepend that to <dst>."
  - "If <src> is empty, it deletes the <dst> ref from the remote repository."
  - "If the refspec can't be expanded unambiguously, error out with an error indicating what was tried ..."
- The 2.47.3 man page has the older wording of the same rules (lines 41-77 of the rendered man page, e.g. "If <dst> doesn't start with refs/ (e.g. refs/heads/master) we will try to infer where in refs/* on the destination <repository> it belongs based on the type of <src> ..." and "Pushing an empty <src> allows you to delete the <dst> ref from the remote repository."). The DESCRIPTION/refspec section was rewritten between 2.47.3 and 2.55.0; the rules themselves are the same.
- **Relation:**
  - `+` is a refspec-parsing flag equivalent to `--force`; the hook record format has no place for it. SUPPORTS E5 (record carries no `+`).
  - Destination expansion happens before the hook (the rules say short `<dst>` names are expanded to `refs/...`), which is consistent with E6/E20/E21 (field 3 is fully qualified). The docs describe expansion of the refspec, not what the hook receives, so the link to field 3 is INFERRED, observed in file 04.
  - `HEAD:main` against a remote that has `refs/heads/main` expands via the "unambiguously refers to a ref on the remote" rule; if `main` existed as both a branch and a tag on the remote, the documented outcome is an error before any push. EXTENDS (an ambiguous name never reaches the hook as a short name).
- **Relevance:** HIGH.

### B6. Rejection statuses (why some refs never reach the hook)

- **Governing sentence (verbatim, both versions, OUTPUT section, status "rejected"):** "Git did not try to send the ref at all, typically because it is not a fast-forward and you did not force the update."
- Neither version documents the "fetch first" or "stale info" status texts, and neither says whether rejected refs are passed to pre-push.
- **Relation:** E23b and E27a (locally known non-fast-forward, stale lease) observed that such refs are removed from the hook's stdin; E23a ("fetch first", remote object not present locally) observed that the record still reaches the hook. The official docs neither confirm nor contradict that split: NOT DOCUMENTED. File 04 is the only evidence. Design D19-47 / line 534 ("not up-to-date/nonfastforward rejection") is consistent with E23b but not with E23a, and no official source settles which is intended.
- **Relevance:** HIGH.

### B7. Behaviour change after 2.47.3 visible in the 2.55.0 page

- The 2.55.0 web page has a "REMOTE GROUPS" section absent from the 2.47.3 man page (grep for `REMOTE GROUPS` on the installed man page returned nothing). Verbatim: "If any member remote fails whether due to a push rejection (e.g. a non-fast-forward update, a server-side hook refusing a ref) or a connection error ..., Git reports the error and continues pushing to the remaining remotes in the group." Also: "per-remote push mappings configured via remote.<name>.push and mirror mode (remote.<name>.mirror) are evaluated independently for each remote".
- **Relation:** EXTENDS. On a newer git a single `git push <group>` can push to several remotes; whether pre-push then runs once per member remote is not stated on the page. Not present in 2.47.3, so not a current-behaviour concern; it is a future-version risk for the "one nonzero exit aborts the whole push" property (E19), because the page says git "continues pushing to the remaining remotes". UNSETTLED for newer git.
- **Relevance:** MEDIUM.

## Area C. git-config(1) and git(1): core.hooksPath, `-c`, advice.ignoredHook, extensions.worktreeConfig

Source for all quotes in this area: installed 2.47.3 pages read with `MANWIDTH=180 MANPAGER=cat man git-config | col -b` and `... man git | col -b` (R1). Web counterpart: https://git-scm.com/docs/git-config and https://git-scm.com/docs/git.

### C1. core.hooksPath

- **Governing sentences (verbatim):** "By default Git will look for your hooks in the $GIT_DIR/hooks directory. Set this to different path, e.g. /etc/git/hooks, and Git will try to find your hooks in that directory, e.g. /etc/git/hooks/pre-receive instead of in $GIT_DIR/hooks/pre-receive." / "The path can be either absolute or relative. A relative path is taken as relative to the directory where the hooks are run (see the "DESCRIPTION" section of githooks(5))."
- **Relative-path semantics:** combined with githooks DESCRIPTION (A2), a relative core.hooksPath for pre-push resolves against the root of the working tree in which `git push` runs. In a linked worktree that is the linked worktree's root, so a relative value names a different directory per worktree. EXTENDS; consistent with E31 (per-worktree hooksPath changes which hook runs).
- core.hooksPath is a "pathname" variable, so "~/" and "%(prefix)/" expansion applies ("A variable that takes a pathname value can be given a string that begins with "~/" or "~user/", and the usual tilde expansion happens to such a string").
- **Relation:** SUPPORTS E15/E16 (`-c core.hooksPath=/dev/null` or any other directory replaces the hooks directory, so the guard does not run). The page has no "disable" semantics; `/dev/null` works because no file `/dev/null/pre-push` can exist.
- **Relevance:** HIGH.

### C2. How `-c` and environment configuration take precedence

- git(1), `-c <name>=<value>` (verbatim): "Pass a configuration parameter to the command. The value given will override values from configuration files."
- git-config(1) SCOPES (verbatim): "command: GIT_CONFIG_{COUNT,KEY,VALUE} environment variables ... the -c option".
- git-config(1) ENVIRONMENT (verbatim): "If GIT_CONFIG_COUNT is set to a positive number, all environment pairs GIT_CONFIG_KEY_<n> and GIT_CONFIG_VALUE_<n> up to that number will be added to the process's runtime configuration. ... These environment variables will override values in configuration files, but will be overridden by any explicit options passed via git -c."
- git(1) also documents `--config-env=<name>=<envvar>`: "Like -c <name>=<value>, give configuration variable <name> a value, where <envvar> is the name of an environment variable from which to retrieve the value."
- **Relation:** EXTENDS E15/E16. Besides `-c core.hooksPath=...`, two more documented per-process forms set core.hooksPath without touching any config file: `--config-env=core.hooksPath=VAR` and the `GIT_CONFIG_COUNT/KEY_<n>/VALUE_<n>` environment variables. Design line 520's "per-process hooksPath overrides" covers them; a text check (L1) sees them only when they are written in the command line (an exported environment variable set earlier is invisible). NOT TESTED in file 04 (only `-c` was).
- **Relevance:** HIGH.

### C3. advice.ignoredHook

- **Governing sentence (verbatim):** "ignoredHook: Shown when a hook is ignored because the hook is not set as executable."
- **Relation:** SUPPORTS E29 (non-executable hook: push proceeds, a hint is printed). The hint is advice only, so `-c advice.ignoredHook=false` silences it. A non-executable guard fails OPEN, by design of git.
- **Relevance:** MEDIUM.

### C4. extensions.worktreeConfig

- **Governing sentences (verbatim):** "If enabled, then worktrees will load config settings from the $GIT_DIR/config.worktree file in addition to the $GIT_COMMON_DIR/config file. Note that $GIT_COMMON_DIR and $GIT_DIR are the same for the main working tree, while other working trees have $GIT_DIR equal to $GIT_COMMON_DIR/worktrees/<id>/. The settings in the config.worktree file will override settings from any other config files."
- **Relation:** SUPPORTS E31 (with the extension on, a `core.hooksPath` in one worktree's `config.worktree` overrides the shared value, so that worktree's push uses a different hooks directory). "will override settings from any other config files" means a per-worktree value beats even the global and system values for that worktree. It does not beat command scope (`-c`, C2).
- **Relevance:** HIGH.

## Area E. git-hook(1) (`git hook run`) and the config-based hooks added after 2.47.3

### E1. Installed 2.47.3

- **Source:** `MANWIDTH=180 MANPAGER=cat man git-hook | col -b` (footer "Git 2.47.3 07/30/2025"), R1.
- **Governing sentences (verbatim):** SYNOPSIS "git hook run [--ignore-missing] [--to-stdin=<path>] <hook-name> [-- <hook-args>]"; DESCRIPTION "A command interface for running git hooks (see githooks(5)), for use by other scripted git commands."; "--to-stdin: For "run"; specify a file which will be streamed into the hook's stdin."
- **Relation:** EXTENDS. `git hook run --to-stdin=<file> pre-push -- <remote> <url>` lets a test invoke the installed guard with chosen records; that is the documented way to feed malformed or padded records (design 19.5 "Synthetic direct-hook inputs"). It does not make other tools run the hook; they must call it explicitly.
- **Relevance:** MEDIUM.

### E2. Newer git (web page "git-hook last updated in 2.55.0"): configuration-defined hooks

- **Source:** https://git-scm.com/docs/git-hook (R1). Its change list (verbatim): "2.55.0 — 2026-06-29", "2.54.0 — 2026-04-20", "2.43.1 → 2.53.0 no changes", "2.43.0 — 2023-11-20", "2.40.0 — 2023-03-12", "2.36.0 — 2022-04-18".
- **Governing sentences (verbatim):**
  - "Runs hooks configured for <hook-name>, in the order they are discovered during the config parse. The default <hook-name> from the hookdir is run last."
  - "hook.<friendly-name>.command: The command to execute for hook.<friendly-name>. ... The value can be an executable path or a shell oneliner."
  - "hook.<friendly-name>.enabled: ... Set to false to disable the hook without removing its configuration."
  - "hook.<event>.enabled: Switch to enable or disable all hooks for the <event> hook event. When set to false, no hooks fire for that event, regardless of any per-hook hook.<friendly-name>.enabled settings. Defaults to true."
  - "For pre-push hooks, which normally keep stdout and stderr separate, setting this to a value greater than 1 (or passing -j) will merge stdout into stderr ..."
- **Relation:** EXTENDS, future-version risk. (1) On a git with config-defined hooks, extra pre-push commands can be registered in any config scope and the hooks-directory file still runs "last". (2) The page text implies `hook.pre-push.enabled=false` would stop the hooks-directory hook too ("no hooks fire for that event"); if so, `-c hook.pre-push.enabled=false` is one more per-process bypass that design line 520 does not list. Whether `hook.<event>.enabled` also suppresses the traditional hookdir file is implied, not stated outright: UNSETTLED. None of this exists in 2.47.3 (E1 has no CONFIGURATION section). Version attribution is in Area F.
- **Relevance:** HIGH for the bypass list on newer git; LOW for current 2.47.3 behaviour.

## Area D. git-worktree(1), gitrepository-layout(5), git-rev-parse(1): where the hook lives

Source: installed 2.47.3 pages via `MANWIDTH=180 MANPAGER=cat man <page> | col -b` (R1); web counterparts https://git-scm.com/docs/git-worktree, https://git-scm.com/docs/gitrepository-layout, https://git-scm.com/docs/git-rev-parse.

### D1. The hooks directory is a common-dir (shared) path

- **gitrepository-layout(5), entry `hooks` (verbatim):** "Hooks are customization scripts used by various Git commands. ... This directory is ignored if $GIT_COMMON_DIR is set and "$GIT_COMMON_DIR/hooks" will be used instead."
- **gitrepository-layout(5), entry `worktrees/<id>/config.worktree` (verbatim):** "Working directory specific configuration file."
- **git-worktree(1) `add` (verbatim):** "The new worktree is linked to the current repository, sharing everything except per-worktree files such as HEAD, index, etc."
- **git-worktree(1) CONFIGURATION FILE (verbatim):** "By default, the repository config file is shared across all worktrees." and "In this mode, specific configuration stays in the path pointed by git rev-parse --git-path config.worktree. ... Older Git versions will refuse to access repositories with this extension."
- **git-worktree(1) DETAILS (verbatim):** "When extensions.worktreeConfig is enabled, the config file .git/worktrees/<id>/config.worktree is read after .git/config is." and "The rule of thumb is do not make any assumption about whether a path belongs to $GIT_DIR or $GIT_COMMON_DIR when you need to directly access something inside $GIT_DIR. Use git rev-parse --git-path to get the final path."
- **Relation:** CONFIRMS E30 from an official source: in a linked worktree `$GIT_COMMON_DIR` is set (via the `commondir` file), so `<common>/hooks` is used and a `hooks/` directory inside `.git/worktrees/<id>/` is ignored. This resolves the wording gap noted in A2. It also means one hook file serves every worktree of the repository, so the guard must decide per push which worktree (and which actor) it is serving (design 19.4 "shared hook file").
- **Relevance:** HIGH.

### D2. `git rev-parse --git-path`, `--path-format=absolute`, `--git-common-dir`

- **`--git-path <path>` (verbatim, 2.47.3):** "Resolve "$GIT_DIR/<path>" and takes other path relocation variables such as $GIT_OBJECT_DIRECTORY, $GIT_INDEX_FILE... into account."
- **`--path-format=(absolute|relative)` (verbatim):** "Controls the behavior of certain other options. If specified as absolute, the paths printed by those options will be absolute and canonical. ... This option may be specified multiple times and affects only the arguments that follow it on the command line".
- **`--git-common-dir` (verbatim):** "Show $GIT_COMMON_DIR if defined, else $GIT_DIR."
- **Documentation gap:** the 2.47.3 `--git-path` text does not mention core.hooksPath. The adjustment is observed, not documented on this page (see D3 local check).
- **Relevance:** MEDIUM (installer and doctor code need the effective hook path).

### D3. Local cross-check on installed 2.47.3 (disposable repo; not part of file 04)

Command run: one Bash call that created `mktemp -d /tmp/web01-exp.XXXXXXXX`, set `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1`, built `repo` (main checkout), a linked worktree `wt` and a local bare `remote.git` as the only remote, then removed the directory (printed `CLEANED=yes`). No network, no real remote. Results (verbatim output lines, path prefix `/tmp/web01-exp.PR24RB14`):

| Check | Command | Output | Meaning |
|---|---|---|---|
| D3a | `git -C wt rev-parse --path-format=absolute --git-path hooks` | `/tmp/web01-exp.PR24RB14/repo/.git/hooks` | linked worktree resolves hooks to the COMMON dir; agrees with D1 and E30 |
| D3b | `git -C wt rev-parse --path-format=absolute --git-dir` / `--git-common-dir` | `.../repo/.git/worktrees/wt` / `.../repo/.git` | private vs common dir |
| D3c | with `core.hooksPath=myhooks`: `git -C wt rev-parse --git-path hooks` | `myhooks` | `--git-path hooks` honours core.hooksPath (undocumented on the 2.47.3 page) |
| D3d | same, with `--path-format=absolute` | `/tmp/web01-exp.PR24RB14/wt/myhooks` | a relative core.hooksPath resolves against the linked worktree root, matching C1 |
| D3e | `git -C wt -c core.hooksPath=/abs/h rev-parse --git-path hooks/pre-push` | `/abs/h/pre-push` | `-c` override is reflected; a doctor can use this to report the effective path for a given invocation |

- **Relevance:** HIGH (`--path-format=absolute --git-path hooks` is the reliable way to locate the effective hooks directory, including core.hooksPath and worktree common dir; routed gap G-list "`--path-format=absolute --git-path`" answered for 2.47.3).

## Area G. Refnames, case, record order, mirror plus refspec (routed questions)

### G1. Is `refs//heads/main` a valid refname? (git-check-ref-format(1))

- **Source:** https://git-scm.com/docs/git-check-ref-format (R1); installed page read with `MANWIDTH=180 MANPAGER=cat man git-check-ref-format | col -b`; rules exercised with `git check-ref-format` in the D3 temp repo.
- **Governing rules (verbatim, installed 2.47.3, rules 6 and 1):** "6. They cannot begin or end with a slash / or contain multiple consecutive slashes (see the --normalize option below for an exception to this rule)." and "1. They can include slash / for hierarchical (directory) grouping, but no slash-separated component can begin with a dot . or end with the sequence .lock."
- **Local result (2.47.3):** `INVALID [refs//heads/main]`, `INVALID [refs/heads//main]`, `INVALID [refs/heads/main/]`, `INVALID [refs/heads/main.lock]`, `valid [refs/heads/Main]`. `git check-ref-format --normalize refs//heads//main` printed `refs/heads/main` (normalize collapses slashes). As a push destination, `git push --dry-run origin main:refs//heads/main` printed `fatal: invalid refspec 'main:refs//heads/main'` and no hook record.
- **Relation:** EXTENDS. git refuses the refspec before the hook runs, so a guard comparing field 3 exactly to `refs/heads/main` cannot be evaded with doubled slashes through `git push`. A hand-crafted record (only via `git hook run --to-stdin` or a direct hook call) could contain it; such input is "malformed" per design 19.3.
- **Relevance:** MEDIUM.

### G2. Case folding: `refs/heads/Main`

- `refs/heads/Main` is a valid, distinct refname (`git check-ref-format` accepted it). No official git page states that refnames are case-insensitive; git-check-ref-format lists no case rule. On a case-insensitive filesystem a loose ref file `refs/heads/Main` and `refs/heads/main` can collide in the local or remote ref store; that is a filesystem property, not a git refname rule, and no git page documents push-side folding. NOT DOCUMENTED; not testable on this Linux ext4 host. Hosting services may treat names differently (out of scope here).
- **Relation:** design 19.3 exact-match on `refs/heads/main`/`master` leaves `refs/heads/Main` unprotected; that is correct by git's rules on case-sensitive stores, and an open risk only for remotes on case-insensitive storage.
- **Relevance:** LOW-MEDIUM.

### G3. Order of stdin records

- No official page states an order (githooks A3 is silent).
- **Local result (2.47.3, `--dry-run`, all creates):** `git push --dry-run origin zz b1 main a2` gave records `zz, b1, main, a2`; `origin main a2 zz b1` gave `main, a2, zz, b1`. Records followed the command-line refspec order in this case. ARGS line: `ARGS: origin ../remote.git` (SUPPORTS file 04 argv).
- **Relation:** EXTENDS, but only one observation; order for pattern refspecs, `--mirror` and `--all` is not established. Design 19.3 "Stream until EOF; do not truncate" is the right defence because order is undocumented: a protected record can come last (design 19.5 already tests "protected last").
- **Relevance:** MEDIUM.

### G4. `--mirror` or `remote.<name>.mirror` combined with an explicit refspec

- Not documented on git-push (B4). **Local result (2.47.3):** `git push --mirror origin main` -> `fatal: --mirror can't be combined with refspecs`; with `remote.origin.mirror=true`, `git push origin main` -> `fatal: --mirror can't be combined with refspecs`. Both refused before any hook record. (The printed `exit=0` in the raw output is the exit of the `tail` pipe stage, not of git.)
- **Relation (G4):** EXTENDS. A mirror push therefore always pushes the whole `refs/` namespace (E11 record set) and cannot be narrowed by a refspec; a configured mirror remote turns every plain `git push origin <branch>` into an error, not a silent mirror. Answers routed question "remote.<name>.mirror combined with an explicit refspec" for 2.47.3.
- **Relevance:** MEDIUM.

### G5. git itself can send a record with more than four fields (local test, installed 2.47.3)

- **Documentary basis:** githooks(5): "If the local commit was specified by something other than a name which could be expanded (such as HEAD~, or an object name) it will be supplied as it was originally given." Source (Area I): field 1 is `r->peer_ref->name`, written with `"%s %s %s %s\n"` and no escaping.
- **Test:** one Bash call, `mktemp -d /tmp/web01-exp2.XXXXXXXX`, local repo with two commits, local bare `remote.git` as the only remote, `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1`, a pre-push hook that prints each line and its awk field count, all pushes `--dry-run`; directory removed (`CLEANED=yes`). Output (verbatim):
  - `git push --dry-run origin 'HEAD@{0 days ago}:refs/heads/main'` -> `REC[6]: HEAD@{0 days ago} bc3fd5c341908b53e64c68fdfc698ec8d7e25c17 refs/heads/main 0000000000000000000000000000000000000000`
  - `git push --dry-run origin 'HEAD~1:refs/heads/main'` -> `REC[4]: HEAD~1 5beba06e597e9ff396fec6eaa64f0c7dd7445271 refs/heads/main 0000...`
  - `git push --dry-run origin 'HEAD^{commit}:refs/heads/main'` -> `REC[4]: HEAD^{commit} bc3fd5c3... refs/heads/main 0000...`
  - `git push --dry-run origin 'main@{1}:main'` -> `error: The destination you provided is not a full refname (i.e., ...` (no record; a short `<dst>` with an expression source must be fully qualified).
- **Relation:** NEW, not in file 04, and it bears directly on design 19.3.
  - A guard that reads with POSIX `read local_ref local_oid remote_ref remote_oid` would get `remote_ref="ago}"` for the M1 record and would NOT see `refs/heads/main` in field 3: a protected push would pass a naive field-3 check. A guard that splits on whitespace and requires exactly four fields would refuse it as "malformed" (fail closed, but with the malformed-input diagnostic for a legitimate git record).
  - Robust parse that matches the source: take the LAST three space-separated fields as `<local-oid> <remote-ref> <remote-oid>` and everything before them as `<local-ref>` (for example Python `line.rstrip("\n").rsplit(" ", 3)`). Fields 2-4 never contain spaces (Area I), so this split is exact.
  - The design statement "A malformed governed stream (missing/extra fields) refuses" therefore needs either the right-split rule above or an explicit note that this legitimate git form is refused.
- **Relevance:** HIGH.

## Area H. Git's own lower-level push paths: send-pack, receive-pack, smart HTTP

### H1. git-send-pack(1)

- **Source:** https://git-scm.com/docs/git-send-pack (R1); installed page via `MANWIDTH=180 MANPAGER=cat man git-send-pack | col -b`.
- **Governing sentences (verbatim):** "Usually you would want to use git push, which is a higher-level wrapper of this command, instead. See git-push(1)." / "Invokes git-receive-pack on a possibly remote repository, and updates it from the current repository, sending named refs."
- `grep -i 'hook\|verify'` on the installed page found only server-side hook mentions ("to allow it to be checked by the hooks", "Pass the specified string as a push option for consumption by hooks on the server side"). No `--verify`/`--no-verify` option and no mention of pre-push.
- **Verdict:** does not run the local pre-push hook (documentation: githooks says pre-push "is called by git-push(1)" and send-pack lists no hook; observation: E17 rewrote main with no hook call). Documentation is silent rather than explicit; E17 is the definitive evidence.
- **Relevance:** HIGH.

### H2. git-receive-pack(1)

- **Governing sentences (verbatim):** "Invoked by git send-pack and updates the repository with the information fed from the remote end." / "This command is usually not invoked directly by the end user. The UI for the protocol is on the git send-pack side ..."
- **Relation:** receive-pack runs on the receiving (remote) side and runs the server-side hooks (pre-receive, update, post-receive per githooks). It never runs the client's pre-push. A push that reaches receive-pack by any route other than `git push` is checked only by server-side hooks and server settings.
- **Relevance:** HIGH.

### H3. Smart HTTP `git-receive-pack` endpoint (gitprotocol-http(5))

- **Source:** https://git-scm.com/docs/gitprotocol-http (and the older alias https://git-scm.com/docs/http-protocol), R1; installed page via `MANWIDTH=180 MANPAGER=cat man gitprotocol-http | col -b`.
- **Governing sentences (verbatim):** "SMART SERVICE GIT-RECEIVE-PACK ... Clients MUST first perform ref discovery with $GIT_URL/info/refs?service=git-receive-pack." followed by the request form "C: POST $GIT_URL/git-receive-pack HTTP/1.0 / C: Content-Type: application/x-git-receive-pack-request / C: ....0a53e9dd... 441b40d8... refs/heads/maint\0 report-status / C: 0000 / C: PACK....".
- **Verdict:** a client that builds this request itself (for example with curl) talks straight to the server's receive-pack; the protocol has no step that involves the client repository's hooks. Does NOT run the local pre-push hook (by construction: no `git push` process exists). Only documentation was read; nothing was sent.
- **Relevance:** HIGH (proves the bypass class exists independent of any third-party tool).

## Area J. Pushes via other tools (documentation reading only; nothing was installed, authenticated, or sent)

Method: WebFetch/WebSearch reads of each tool's official API documentation and, where the documentation is silent, the tool's own source file in its official repository (R3). No tool was run. The WebFetch tool caps verbatim quotes; where a full sentence could not be quoted, the short verbatim fragment is given in quotes and the rest is marked as paraphrase.

### J1. libgit2 `git_remote_push` (C library)

- **Source:** https://libgit2.org/docs/reference/main/remote/git_remote_push.html (R2); maintainer position https://github.com/libgit2/libgit2/issues/964 (R2/R3).
- **Governing text:** reference page: "Perform a push." The parameters are the remote, the refspecs and `const git_push_options *` (https://libgit2.org/docs/reference/main/remote/git_push_options.html). The page mentions no hook. Issue #964, "support for hooks (pre-commit / post-commit / post-merge)", maintainer comment (ethomson, 2015-06-08): "We will not be executing any hooks directly." In paraphrase, running hooks is the calling application's job.
- **Verdict:** does NOT run the local pre-push hook (explicit maintainer statement; the API documentation is silent). The closest feature is the `push_negotiation` callback in `git_remote_callbacks`. It is code inside the calling application, not `hooks/pre-push`.
- **Relevance:** HIGH. libgit2 is the engine under pygit2, Rugged, git2-rs (cargo) and LibGit2Sharp, so every one of them inherits this.

### J2. pygit2 `Remote.push`

- **Source:** https://www.pygit2.org/remotes.html (R2).
- **Governing text (verbatim fragment):** "Push the given refspec to the remote. Raises `GitError` on protocol error or unpack failure." The parameters are `specs`, `callbacks`, `proxy`, `push_options` and `threads`. The page's only hook text concerns REMOTE hooks: in paraphrase, a remote hook's rejection may not raise an error, so implement `RemoteCallbacks.push_update_reference`, and push options are passed to the server's pre-receive/post-receive hooks. There is no pre-push reference.
- **Verdict:** does NOT run the local pre-push hook. It is a libgit2 binding (J1), and its documentation mentions only server-side hooks.
- **Relevance:** HIGH. `uv run python -c "import pygit2; ..."` is a one-line programmatic push that an agent could write.

### J3. JGit `PushCommand` (Java)

- **Source:** `org.eclipse.jgit/src/org/eclipse/jgit/api/PushCommand.java`, `.../hooks/PrePushHook.java` and `.../transport/Transport.java` on https://github.com/eclipse-jgit/jgit (master; R3). The javadoc site URL tried (download.eclipse.org .../apidocs/.../PushCommand.html) returned HTTP 404, and javadoc.io returned no body, so the source javadoc is quoted.
- **Governing text:** `PrePushHook` class javadoc: "The <code>pre-push</code> hook implementation." It also carries `@since 4.2` and the constant `public static final String NAME = "pre-push";`. `Transport.push(...)` creates it with `Hooks.prePush(local, hookOutRedirect, hookErrRedirect)` before `pushProcess.execute(monitor)`. `PushCommand.setHookOutputStream` and `setHookErrorStream` redirect the output of the "pre-push" hook. Per the source, the stdin record is the same four fields: source ref, new id, remote ref name, and expected old id, or the zero id when there is none.
- **Verdict:** RUNS the repository's pre-push hook (since JGit 4.2; source-level evidence). Caveat: unknown. JGit runs hook scripts through its own `FS` abstraction. Whether it honours `core.hooksPath`, how `extensions.worktreeConfig` interacts, and what happens on platforms without a POSIX shell were not checked. Its argv/stdin parity with C git was also not checked beyond the field order.
- **Relevance:** MEDIUM. It is unlikely in an agent session (it needs a JVM program), and it is the one third-party tool here that does not bypass the hook.

### J4. isomorphic-git `push` (JavaScript)

- **Source:** https://isomorphic-git.org/docs/en/push (R2); `src/api/push.js` on https://github.com/isomorphic-git/isomorphic-git (R3).
- **Governing text (verbatim):** description "Push a branch or tag". Parameter `onPrePush`, type `PrePushCallback`: "optional pre-push hook callback" (identical in the source JSDoc). Neither the documentation nor the source excerpt says that `.git/hooks/pre-push` is executed.
- **Verdict:** does NOT run the on-disk pre-push hook (documentation: the only pre-push mechanism is an in-process JavaScript callback that the caller supplies). The on-disk script running is "not documented". A caller that omits `onPrePush` gets no check.
- **Relevance:** MEDIUM. It needs a Node program.

### J5. dulwich `porcelain.push` (pure Python)

- **Source:** https://github.com/jelmer/dulwich/blob/main/docs/c-git-compatibility.txt (R2, the project's own compatibility matrix). The page https://www.dulwich.io/docs/api/dulwich.porcelain.html returned HTTP 404.
- **Governing text (verbatim):** the hooks list has "* ✗ pre-push", with the legend "* ✗ - Not supported". The same list marks pre-commit, commit-msg, post-commit, pre-receive, update and post-receive as supported (from the search summary; the listing itself was not re-quoted).
- **Verdict:** does NOT run the local pre-push hook (explicit project documentation).
- **Relevance:** HIGH. It is pure Python, installable with `uv pip install dulwich`, and `dulwich push` also exists as a CLI. The same bypass class as pygit2.

### J6. GitPython `Remote.push`

- **Source:** `git/remote.py` on https://github.com/gitpython-developers/GitPython (main; R3). The reference page https://gitpython.readthedocs.io/en/stable/reference.html is 488 KB, and the `Remote.push` entry was not reached within the fetched window. Package doc: "The Git class manages communication with the Git binary."
- **Governing text:** `push` builds the command through the repository's Git wrapper (`_call_process_safe(` with the `push` subcommand, `--`, the remote and the refspecs, `porcelain=True`, `as_process=True`). Its docstring for `**kwargs` says, verbatim: "Additional arguments to be passed to :manpage:`git-push(1)`." `allow_unsafe_options` guards options such as `--receive-pack` and defaults to false. The `push` signature has no dedicated verify/no-verify keyword.
- **Verdict:** RUNS the local pre-push hook, because it executes the real `git push` binary. Caveat: GitPython turns keyword arguments into command-line flags, so in paraphrase `remote.push(..., no_verify=True)` becomes `git push --no-verify ...` and bypasses the hook as E14 does. This conversion rule is GitPython's general convention and was not tested here. The `git` child also inherits the caller's environment, so GIT_CONFIG_COUNT/KEY/VALUE (C2) applies too. A `git -c core.hooksPath=...` prefix would need `repo.git` options and was not checked.
- **Relevance:** HIGH. It is exactly as strong as `git push` itself: the hook runs, and every git-level bypass is reachable.

### J7. GitHub REST API: Git references

- **Source:** https://docs.github.com/en/rest/git/refs (R2).
- **Governing text (verbatim fragments):** "POST /repos/{owner}/{repo}/git/refs", "Creates a reference". "PATCH /repos/{owner}/{repo}/git/refs/{ref}" changes a ref to "point to a new SHA". The optional `force` boolean defaults to false, and in paraphrase false allows only fast-forward updates. Client-side hooks are not mentioned.
- **Verdict:** does NOT run the local pre-push hook. The request goes from an HTTP client to GitHub's servers, and no local `git push` process exists. Only server-side controls (branch protection/rulesets, token scope) apply. Related endpoints with the same property (merge, contents API commits) were not enumerated.
- **Relevance:** HIGH. It is the most direct non-git way to move `refs/heads/main` on a GitHub-hosted remote.

### J8. `gh api`

- **Source:** https://cli.github.com/manual/gh_api (R2).
- **Governing text (verbatim):** "Makes an authenticated HTTP request to the GitHub API and prints the response." Flag: "-X" / "--method": "The HTTP method for the request".
- **Verdict:** does NOT run the local pre-push hook. In paraphrase, `gh api -X PATCH repos/<o>/<r>/git/refs/heads/main -f sha=...` is J7 performed with the user's stored gh token, through an ordinary shell command.
- **Relevance:** HIGH. It is pre-authenticated in this environment and is a visible Bash command, so L1 (the PreToolUse layer) is the only local layer that can see it.

### J9. curl to smart-HTTP `git-receive-pack`

- Covered by H3. It does NOT run the local hook, by construction of the protocol. Relevance: HIGH (LOW likelihood: it needs a hand-built pkt-line body and pack).

### J10. Other-tools table

| Tool | Runs local pre-push | Governing sentence | Source URL | Relevance |
|---|---|---|---|---|
| `git push` (C git 2.47.3) | runs (unless `--no-verify`, hooksPath override, etc.) | "This hook is called by git-push(1) and can be used to prevent a push from taking place." | https://git-scm.com/docs/githooks | HIGH |
| `git send-pack` | does not run | "Usually you would want to use git push, which is a higher-level wrapper of this command" (no hook option documented); E17 | https://git-scm.com/docs/git-send-pack | HIGH |
| curl to `git-receive-pack` (smart HTTP) | does not run | "C: POST $GIT_URL/git-receive-pack HTTP/1.0" (no client-hook step in the protocol) | https://git-scm.com/docs/gitprotocol-http | HIGH |
| libgit2 `git_remote_push` | does not run | "We will not be executing any hooks directly." (maintainer, issue #964); API page: "Perform a push." | https://libgit2.org/docs/reference/main/remote/git_remote_push.html ; https://github.com/libgit2/libgit2/issues/964 | HIGH |
| pygit2 `Remote.push` | does not run | "Push the given refspec to the remote." (only server hooks mentioned) | https://www.pygit2.org/remotes.html | HIGH |
| JGit `PushCommand` | runs (since 4.2; hooksPath/worktree parity unchecked) | "The <code>pre-push</code> hook implementation." / `Hooks.prePush(local, hookOutRedirect, hookErrRedirect)` in `Transport.push` | https://github.com/eclipse-jgit/jgit/blob/master/org.eclipse.jgit/src/org/eclipse/jgit/hooks/PrePushHook.java | MEDIUM |
| isomorphic-git `push` | does not run the on-disk hook (in-process callback only); on-disk execution not documented | `onPrePush`: "optional pre-push hook callback" | https://isomorphic-git.org/docs/en/push | MEDIUM |
| dulwich `porcelain.push` | does not run | "* ✗ pre-push" with legend "* ✗ - Not supported" | https://github.com/jelmer/dulwich/blob/main/docs/c-git-compatibility.txt | HIGH |
| GitPython `Remote.push` | runs (shells out to `git push`); `no_verify=True` maps to `--no-verify` (convention, untested) | "Additional arguments to be passed to :manpage:`git-push(1)`." | https://github.com/gitpython-developers/GitPython/blob/main/git/remote.py | HIGH |
| GitHub REST "Create/Update a reference" | does not run | "POST /repos/{owner}/{repo}/git/refs" "Creates a reference"; PATCH ".../git/refs/{ref}" to "point to a new SHA" | https://docs.github.com/en/rest/git/refs | HIGH |
| `gh api` | does not run | "Makes an authenticated HTTP request to the GitHub API and prints the response." | https://cli.github.com/manual/gh_api | HIGH |

### J11. Verdict on design line 520

Design `docs/designs/sc-issue-launch-level-hook.md` line 520 (read 2026-11-08) says: "`--no-verify`, per-process hooksPath overrides, direct send-pack and API/programmatic ref writes can bypass local pre-push; visible forms remain checked by L1."

- **CONFIRMED** by official sources for each named class:
  - `--no-verify`: git-push(1), and E14.
  - per-process hooksPath override: C1/C2, E15/E16, and 2.50.0's documented `/dev/null` convention.
  - direct send-pack: H1, and E17.
  - API ref writes: J7/J8.
  - programmatic ref writes: J1, J2, J4 and J5, and H3.
- **Precision gaps:**
  1. "Programmatic" is not uniform. JGit (J3) and GitPython (J6) DO run the hook. GitPython is only as strong as `git push` and inherits its bypasses. Suggested wording: "libgit2-based tools (pygit2 and others), dulwich, isomorphic-git without `onPrePush`, raw smart-HTTP, and hosting APIs (GitHub REST via `gh api`/curl) do not run local pre-push".
  2. The bypass list omits forms found here:
     - `--config-env`/GIT_CONFIG_COUNT environment configuration (C2), which is not a visible `-c` argument.
     - per-worktree `core.hooksPath` through extensions.worktreeConfig (C4/E31).
     - the future `hook.pre-push.enabled=false` (F1, unreleased).
     - `git update-ref` on a local mirror followed by any of the above. Local ref writes never trigger pre-push; that follows from githooks, and the design already places no local restriction.
  3. "visible forms remain checked by L1" holds only for forms that show in the Bash command text. An in-process library call inside `uv run python script.py` is visible only as the script path, unless L1 inspects script contents.
- **Relevance:** HIGH.

## Area F. Release notes: the version that introduced each behaviour

**Method.** The raw `.txt` URLs under `raw.githubusercontent.com/git/git/master/Documentation/RelNotes/` return HTTP 404 because the files are now `.adoc`. To quote whole lines, a read-only, blobless, sparse, depth-1 clone of the public `https://github.com/git/git.git` was made in `mktemp -d /tmp/web01-relnotes.XXXXXXXX` (master at `fb255012acbcbe81189cb8014da0280b09c66ecc`, committed 2026-11-06; 543 release-note files), plus depth-1 fetches of tags `v1.8.2`, `v1.8.3`, `v1.8.3.1`, `v1.8.4`, `v2.47.3` and commits `ec55559f93…`, `90d32d1ffa…`. Nothing was pushed; the directory was removed afterwards. Quotes are `grep -n` output from `Documentation/RelNotes/<ver>.adoc`. Web URL form for each note: `https://github.com/git/git/blob/master/Documentation/RelNotes/<ver>.adoc`. Reliability R1 (release notes) and R3 (git source at a tag).

### F1. Findings per behaviour

- **pre-push hook, 1.8.2.** `1.8.2.adoc:167-168`: " * "git push" will stop without doing anything if the new "pre-push" hook exists and exits with a failure." CONFIRMS the 1.8.2 hint. Introducing commit `ec55559f937727bcb0fa8a3dfe6af68c188e968a` (Aaron Schrab, 2013-01-13), "push: Add support for pre-push hooks": "The hook is run with two arguments specifying the name and location of the destination repository. ... `<local ref> SP <local sha1> SP <remote ref> SP <remote sha1> LF` ... If the hook exits with a non-zero status, the push will be aborted."
- **`git push --no-verify`, 1.8.2 (code) / 1.8.4 (documentation).** No release note mentions it (`grep -- 'no-verify'` over all 543 notes finds only `git rebase`, `git commit` and generic `--no-` notes). Source evidence: `git show v1.8.2:builtin/push.c` line 439: `OPT_BIT(0, "no-verify", &flags, N_("bypass pre-push hook"), TRANSPORT_PUSH_NO_HOOK),`. Commit `90d32d1ffa36390177990cb92e4e2a68c5ec4092` (Thomas Rast, 2013-05-23), "Document push --no-verify": "ec55559 (push: Add support for pre-push hooks, 2013-01-13) forgot to add a note to git-push(1) about the new --no-verify option." `v1.8.3.1:Documentation/git-push.txt` has no `no-verify`; `v1.8.4:Documentation/git-push.txt` line 210 has "push. With \--no-verify, the hook is bypassed completely." The 1.8.2 hint is CONFIRMED for the option itself, with the citation being source code, not a release note.
- **core.hooksPath, 2.9.0.** `2.9.0.adoc:127-128`: " * A new configuration variable core.hooksPath allows customizing where the hook directory is." CONFIRMED.
- **`rev-parse --git-path hooks` honours core.hooksPath, 2.10.0.** `2.10.0.adoc:122-125`: " * "git rev-parse --git-path hooks/<hook>" learned to take core.hooksPath configuration variable (introduced during 2.9 cycle) into account." (Matches D3c/D3e; the 2.47.3 man page does not say it.)
- **core.hooksPath `/dev/null` as the documented way to disable hooks, 2.50.0.** `2.50.0.adoc:313-315`: " * Document the convention to disable hooks altogether by setting the hooksPath configuration variable to /dev/null." This is AFTER 2.47.3: the behaviour (E15) exists in 2.47.3, its official documentation is newer.
- **core.hooksPath clone protection added then reverted, 2.39.4 / 2.39.5 (and the matching 2.40.3, 2.41.2, 2.42.3, 2.43.5, 2.44.2 maintenance notes).** `2.39.4.adoc:55`: " * Defense-in-depth: core.hooksPath: add some protection while cloning." `2.39.5.adoc:20-22`: "Revert "core.hooksPath: add some protection while cloning" / tests: verify that `clone -c core.hooksPath=/dev/null` works again / clone: drop the protections where hooks aren't run". Net effect for 2.47.3: `-c core.hooksPath=/dev/null` is a supported, tested pattern.
- **`git worktree`, 2.5.0.** `2.5.0.adoc:45-50`: " * A replacement for contrib/workdir/git-new-workdir that does not rely on symbolic links and make sharing of objects and refs safer by making the borrowee and borrowers aware of each other. / Consider this as still an experimental feature; its UI is still likely to change." The note does not use the word "worktree"; the 2.5 hint is CONFIRMED by this bullet in substance (the `git worktree` command is this feature), but the literal command name is not quoted in the note. Mark: CONFIRMED-INDIRECT.
- **extensions.worktreeConfig / `config.worktree`, 2.20.0.** `2.20.0.adoc:159-163`: " * A fourth class of configuration files (in addition to the traditional "system wide", "per user in the $HOME directory" and "per repository in the $GIT_DIR/config") has been introduced so that different worktrees that share the same repository (hence the same $GIT_DIR/config file) can use different customization." CONFIRMED (the extension name itself is not in the bullet).
- **`git hook run`, 2.36.0.** No 2.36.0 bullet names `git hook` (`grep -c -i hook 2.36.0.adoc` = 1, the safe.directory bullet). Evidence: (1) `2.37.0.adoc:285-289`: " * In Git 2.36 we revamped the way how hooks are invoked. One change that is end-user visible is that the output of a hook is no longer directly connected to the standard output of "git" that spawns the hook, which was noticed post release. This is getting corrected." (2) The git-scm git-hook page change list starts at "2.36.0 — 2022-04-18" (https://git-scm.com/docs/git-hook). CONFIRMED-INDIRECT: 2.36.0 for the command and for the hook-execution rewrite (hook.c); 2.37.0 fixed a stdout regression of that rewrite; `2.38.0.adoc:295`: " * A follow-up fix to a fix for a regression in 2.36 around hooks."
- **Transport pre-push moved onto the hook API, 2.54.0.** `2.54.0.adoc:213-214`: " * Use the hook API to replace ad-hoc invocation of hook scripts via the run_command() API." Source comparison: `v2.47.3:transport.c` line 1293 calls `find_hook(the_repository, "pre-push")` and runs one child process; master `transport.c` line 1459 calls `run_hooks_opt(the_repository, "pre-push", &opt)` with a `pre_push_hook_feed_stdin` callback. The bullet does not name pre-push explicitly; the code change is the evidence (R3).
- **Configuration-defined hooks, 2.54.0.** `2.54.0.adoc:67-69`: " * Hook commands are now allowed to be defined (possibly centrally) in the configuration files, and run multiple of them for the same hook event."
- **Parallel configured hooks, 2.55.0.** `2.55.0.adoc:7-8`: " * Hook scripts defined via the configuration system can now be configured to run in parallel."
- **`hook.<event>.enabled` also disables hooks-directory hooks: unreleased (master draft).** `2.98.0.adoc:104-108`: " * The hook.<event>.enabled configuration variable has been extended to also disable traditional hookdir hooks in addition to configured hooks. In addition, the hook configuration parser has been updated to treat missing values for boolean variables like enabled and parallel as true." The 2.98.0 note's header says "This is meant to be the antepenultimate release to prepare for the long anticipated Git 3.0"; it is a draft on master, not a released version as of 2026-11-06. DISCREPANCY with the git-scm git-hook page (E2), whose `hook.<event>.enabled` text ("no hooks fire for that event") reads as if it already covers hookdir hooks in 2.55.0; per this note, in 2.54-2.56 it did not disable the traditional `hooks/pre-push`. Once released, `git -c hook.pre-push.enabled=false push` becomes an additional per-process bypass of a hooks-directory guard.

### F2. Version table

| Behaviour | Introduced in | Release-note URL and quoted line | Present in 2.47.3 |
|---|---|---|---|
| pre-push hook run by `git push`; nonzero exit aborts the push | 1.8.2 | https://github.com/git/git/blob/master/Documentation/RelNotes/1.8.2.adoc line 167: "\"git push\" will stop without doing anything if the new \"pre-push\" hook exists and exits with a failure." | yes (E1-E31) |
| `git push --no-verify` bypasses pre-push | 1.8.2 (code); documented in git-push(1) from 1.8.4 | No release note. Source `v1.8.2:builtin/push.c` line 439 `OPT_BIT(0, "no-verify", ..., N_("bypass pre-push hook"), TRANSPORT_PUSH_NO_HOOK)`; commit https://github.com/git/git/commit/90d32d1ffa36390177990cb92e4e2a68c5ec4092 "forgot to add a note to git-push(1) about the new --no-verify option." | yes (E14) |
| core.hooksPath | 2.9.0 | https://github.com/git/git/blob/master/Documentation/RelNotes/2.9.0.adoc line 127: "A new configuration variable core.hooksPath allows customizing where the hook directory is." | yes (E15/E16) |
| `rev-parse --git-path hooks/<hook>` honours core.hooksPath | 2.10.0 | .../RelNotes/2.10.0.adoc line 122: "\"git rev-parse --git-path hooks/<hook>\" learned to take core.hooksPath configuration variable (introduced during 2.9 cycle) into account." | yes (D3c-e) |
| core.hooksPath=/dev/null documented as "disable hooks" | 2.50.0 (documentation only) | .../RelNotes/2.50.0.adoc line 313: "Document the convention to disable hooks altogether by setting the hooksPath configuration variable to /dev/null." | behaviour yes (E15); that doc sentence no |
| core.hooksPath clone protection added then reverted | 2.39.4 added, 2.39.5 reverted | .../RelNotes/2.39.4.adoc line 55 "Defense-in-depth: core.hooksPath: add some protection while cloning."; 2.39.5.adoc line 20 "Revert \"core.hooksPath: add some protection while cloning\"" | reverted state: yes |
| `git worktree` (linked worktrees sharing refs, objects, hooks) | 2.5.0 | .../RelNotes/2.5.0.adoc line 45: "A replacement for contrib/workdir/git-new-workdir that does not rely on symbolic links and make sharing of objects and refs safer by making the borrowee and borrowers aware of each other." | yes (E30) |
| Per-worktree config (`config.worktree`, extensions.worktreeConfig) | 2.20.0 | .../RelNotes/2.20.0.adoc line 159: "A fourth class of configuration files ... has been introduced so that different worktrees that share the same repository ... can use different customization." | yes (E31) |
| `git hook run` and the hook.c execution rewrite | 2.36.0 | No 2.36.0 bullet. .../RelNotes/2.37.0.adoc line 285: "In Git 2.36 we revamped the way how hooks are invoked."; git-scm change list "2.36.0 — 2022-04-18" (https://git-scm.com/docs/git-hook) | yes (installed `git hook run` man page, Area E1) |
| Hook stdout regression fix after the rewrite | 2.37.0, 2.38.0 | .../RelNotes/2.37.0.adoc line 285 (above); 2.38.0.adoc line 295 "A follow-up fix to a fix for a regression in 2.36 around hooks." | yes |
| `transport.c` pre-push moved to the hook API (`run_hooks_opt`) | 2.54.0 | .../RelNotes/2.54.0.adoc line 213: "Use the hook API to replace ad-hoc invocation of hook scripts via the run_command() API." (pre-push not named; source diff is the evidence) | no (2.47.3 uses `find_hook` + `start_command`) |
| Hooks defined in configuration (`hook.<name>.command/event`) | 2.54.0 | .../RelNotes/2.54.0.adoc line 67: "Hook commands are now allowed to be defined (possibly centrally) in the configuration files, and run multiple of them for the same hook event." | no |
| Parallel configured hooks (`hook.jobs`, `-j`) | 2.55.0 | .../RelNotes/2.55.0.adoc line 7: "Hook scripts defined via the configuration system can now be configured to run in parallel." | no |
| `hook.<event>.enabled=false` also disables hooks-directory hooks | unreleased (master draft "2.98.0", pre-3.0) | .../RelNotes/2.98.0.adoc line 104: "The hook.<event>.enabled configuration variable has been extended to also disable traditional hookdir hooks in addition to configured hooks." | no |
| Remote groups in `git push` (continue to other members after a failure) | after 2.47.3 (exact version not located; present on the 2.55.0 git-push page) | not located in release notes by this search; page https://git-scm.com/docs/git-push "REMOTE GROUPS" | no (absent from installed man page) |

## Area I. Source-level explanation of observed filtering (R3, git source at tag v2.47.3)

- **Source:** `git show v2.47.3:transport.c`, function `run_pre_push_hook`, lines 1286-1341, and its call site lines 1404-1412 (from the temp clone above). Web: https://github.com/git/git/blob/v2.47.3/transport.c.
- **Governing code (verbatim):**
  - line 1293: `const char *hook_path = find_hook(the_repository, "pre-push");` and lines 1295-1296 `if (!hook_path) return 0;`
  - lines 1299-1300: `strvec_push(&proc.args, transport->remote->name);` / `strvec_push(&proc.args, transport->url);`
  - lines 1315-1319: `if (!r->peer_ref) continue;` / `if (r->status == REF_STATUS_REJECT_NONFASTFORWARD) continue;` / `if (r->status == REF_STATUS_REJECT_STALE) continue;` / `if (r->status == REF_STATUS_REJECT_REMOTE_UPDATED) continue;` / `if (r->status == REF_STATUS_UPTODATE) continue;`
  - lines 1322-1324: `strbuf_addf( &buf, "%s %s %s %s\n", r->peer_ref->name, oid_to_hex(&r->new_oid), r->name, oid_to_hex(&r->old_oid));`
  - lines 1327-1329: `/* We do not mind if a hook does not read all refs. */ if (errno != EPIPE) ret = -1;`
  - lines 1406-1412: `set_ref_status_for_push(remote_refs, flags & TRANSPORT_PUSH_MIRROR, flags & TRANSPORT_PUSH_FORCE);` then `if (!(flags & TRANSPORT_PUSH_NO_HOOK)) if (run_pre_push_hook(transport, remote_refs)) goto done;`
- **Relation to file 04:**
  - The hook runs after ref discovery, refspec matching (`match_push_refs`), lease checks (`apply_push_cas`) and local status checks (`set_ref_status_for_push`), and before any pack is sent. This is the code form of the brief's "after the remote status is checked and before anything is pushed" (that wording is not in githooks(5); see A3).
  - Skipped statuses are exactly non-fast-forward, stale lease, remote-updated and up-to-date. `REF_STATUS_REJECT_FETCH_FIRST` is NOT in the skip list, so a "fetch first" ref is written to the hook. EXPLAINS E12 (up-to-date: empty), E23b (non-fast-forward: empty), E27a (stale lease: empty) and E23a (fetch first: record delivered). This CONTRADICTS the general reading of design D19-47/line 534 that rejected non-fast-forward refs never reach pre-push: only some rejection kinds are filtered.
  - The hook is started even when every record is filtered (it is started before the loop), so an empty stdin is a normal input. SUPPORTS design 19.3 "Empty stream allows".
  - Field 3 is `r->name`, the name of the ref in the remote ref list built by `match_push_refs`; that is why it is always the fully qualified destination (E6, E20, E21, E11). Field 1 is `r->peer_ref->name`, the local ref (or the placeholder name `(delete)`, per githooks).
  - Records are written in the order of the `remote_refs` list after matching; the code does not sort them. G3 observed command-line order for simple refspecs; no documented guarantee.
  - `oid_to_hex` prints the repository's hash length, so SHA-256 repositories give 64 hex digits (file 04 SHA-256 run). Fields 3 (`r->name`, a remote refname) and 2/4 (hex oids) cannot contain a space or newline, because a refname cannot, per git-check-ref-format (installed 2.47.3 rule 4, verbatim: "They cannot have ASCII control characters (i.e. bytes whose values are lower than \040, or \177 DEL), space, tilde ~, caret ^, or colon : anywhere."; LF is a control character). Field 1 (`r->peer_ref->name`) has no such guarantee: for an expression source it is the text "as it was originally given" (githooks), and that text can contain spaces. Answer to routed question "whether git can ever send malformed records": YES on 2.47.3, through an ordinary `git push` (see G5); a record never has FEWER than four space-separated fields, but it can have more, and the extra ones are always at the start.
  - **Correction to the line above, from a local test (G5 below):** field 1 is NOT a refname when the source is an expression, and git does not validate it with check-ref-format. `git push --dry-run origin 'HEAD@{0 days ago}:refs/heads/main'` delivered a record with SIX space-separated fields. So `git push` itself CAN send a record that a whitespace split reports as malformed. Only fields 2-4 are guaranteed space-free.
  - SIGPIPE ignored and EPIPE tolerated: a guard may exit early (for example as soon as it sees `refs/heads/main`) without reading the rest of stdin, and its exit status still decides.
- **Master (post-2.54) differences:** `pre_push_hook_feed_stdin` keeps the same four skip statuses and the same `"%s %s %s %s\n"` format; the hook is run through `run_hooks_opt(the_repository, "pre-push", &opt)`, which runs configured hooks plus the hooks-directory hook (Area E2). The comment at master line 1452 reads "pre-push hooks keep stdout and stderr separate by default for backwards compatibility."
- **Relevance:** HIGH.

## Area K. Community pitfalls (short pass)

- A search for mailing-list threads on empty pre-push stdin, `--dry-run` and hooksPath in worktrees found no primary thread on hook behaviour. The closest hit, "[PATCH] push: improve consistency of output when 'up to date'" (2024-01-11, https://lore.kernel.ime.usp.br/git/d6161449aa19aebeb4c3bea1a751e8b5%40manjaro.org/T/, R1 mirror), concerns message wording only.
- A Stack Overflow question titled "git pre-push hook stdin is empty" (https://stackoverflow.com/questions/55112847/git-pre-push-hook-stdin-is-empty, R4) exists, but this tool cannot fetch stackoverflow.com, so its answer was not read.
- Net: Area I (source) and file 04 (E12/E13/E23/E27) are stronger evidence than anything the community pass found. Relevance: LOW.

## Key External Findings

- **Contract (HIGH, R1).** githooks(5) is identical in 2.47.3 and the current web page:
  - argv is the remote name and the URL; they are equal when no named remote is used.
  - stdin is `<local-ref> SP <local-oid> SP <remote-ref> SP <remote-oid> LF`.
  - A nonzero exit aborts the push.
  - Field 3 being fully qualified is guaranteed by the code (`r->name`, Area I), not stated in the documentation. File 04's observations agree.
- **Which refs reach the hook (HIGH, R3).** The 2.47.3 source skips exactly four statuses: non-fast-forward, stale lease, remote-updated and up-to-date. "Fetch first" is delivered.
  - This explains E12, E23a/b and E27a.
  - It corrects design D19-47/line 534, which assumed every rejected non-fast-forward ref is filtered.
  - Empty stdin is normal input.
  - EPIPE is tolerated, so an early exit is safe.
- **Malformed records come from git itself (HIGH, local test G5).** `git push origin 'HEAD@{0 days ago}:refs/heads/main'` produces a six-field record.
  - A naive four-variable `read` moves "ago}" into field 3 and lets a protected push through.
  - A strict four-field check refuses it as malformed, which fails closed but gives the wrong diagnostic.
  - Only fields 2-4 are guaranteed free of spaces.
- **Hook location (HIGH, R1 + D3).**
  - The hooks directory is a common-dir path, so linked worktrees use `$GIT_COMMON_DIR/hooks` (E30).
  - `git rev-parse --path-format=absolute --git-path hooks` resolves it and honours core.hooksPath (2.10.0).
  - A per-worktree `core.hooksPath` through extensions.worktreeConfig (2.20.0) changes it for a single worktree.
- **Per-process bypasses (HIGH, R1).**
  - `--no-verify`: code since 1.8.2, documented since 1.8.4.
  - `-c core.hooksPath=...`, `--config-env`, and GIT_CONFIG_COUNT/KEY/VALUE.
  - `core.hooksPath=/dev/null`: works in 2.47.3, documented in 2.50.0.
  - In future: `hook.pre-push.enabled=false`, from the unreleased 2.98.0 draft.
  - Config-defined hooks (2.54.0) and parallel hooks (2.55.0) are absent from 2.47.3.
- **Refnames (MEDIUM, R1 + local test).**
  - `refs//heads/main` is invalid both as a refname and as a refspec.
  - Refs are case-sensitive, so `refs/heads/Main` is not `refs/heads/main`. Case-insensitive filesystems are a separate storage concern.
  - `--mirror`, whether from the flag or from `remote.<name>.mirror`, cannot be combined with a refspec.
  - Record order followed the command line in tests, but no order is documented.
- **Version table (HIGH).** All five hint versions are confirmed with citations (F2):
  - pre-push 1.8.2
  - --no-verify 1.8.2 code / 1.8.4 docs
  - core.hooksPath 2.9.0
  - worktree 2.5.0 (indirect)
  - worktreeConfig 2.20.0
  - git hook run 2.36.0 (indirect)

  Changes after 2.47.3 that matter: the 2.54.0 hook API and config hooks, 2.55.0 parallel hooks, the 2.50.0 `/dev/null` documentation, and the future hookdir disable switch.
- **Other tools (HIGH, R2/R3).**
  - Do not run local pre-push:
    - libgit2 and its bindings (pygit2, per the maintainer: "We will not be executing any hooks directly.")
    - dulwich ("✗ pre-push", not supported)
    - isomorphic-git (in-process `onPrePush` callback only)
    - `git send-pack`
    - raw smart-HTTP `git-receive-pack`
    - the GitHub REST refs API, `gh api`
  - Run it:
    - JGit (`PrePushHook`, since 4.2)
    - GitPython (shells out to `git push`, so `no_verify=True` and the environment bypasses still apply)
  - **Line-520 verdict: CONFIRMED.** Every bypass class the design names is backed by official documentation or project statements. Three additions are recommended:
    - make "programmatic" precise (not JGit and GitPython)
    - add the environment-config and per-worktree-config bypasses
    - note that L1 sees an in-process library push only as `python script.py`

## Recommendations from External Research

1. **Parse by right-splitting.** Parse each stdin line as `local_ref, local_oid, remote_ref, remote_oid = line.rstrip("\n").rsplit(" ", 3)`, and decide only on `remote_ref`.
   - Treat "malformed" as fewer than four fields, or fields 2/4 that are not hex.
   - Do not refuse more than four fields, because git sends that legitimately (G5).
   - If the design keeps "extra fields refuse", it must say this legitimate form is refused and use a diagnostic that names it.
2. **Compare field 3 exactly and case-sensitively** against `refs/heads/main` and `refs/heads/master`. Do not normalise `//` or case; git rejects `refs//heads/main` before the hook runs.
3. **Handle empty stdin and early exit.** Treat empty stdin as allow. It is safe to exit nonzero as soon as a protected record is seen, because git tolerates EPIPE.
4. **Install and check through `git rev-parse --path-format=absolute --git-path hooks`**, run from the target worktree. It covers linked worktrees (common-dir) and core.hooksPath. Also check `git config --worktree --get core.hooksPath` when `extensions.worktreeConfig` is true.
5. **L1 coverage list.** L1 should match all of these command forms:
   - `--no-verify`
   - `-c core.hooksPath` and `-c hook.pre-push.*`
   - `--config-env`
   - environment assignments of `GIT_CONFIG_COUNT`/`GIT_CONFIG_KEY_*`/`GIT_CONFIG_VALUE_*` and `GIT_CONFIG_PARAMETERS`
   - `git send-pack`
   - `gh api` calls that write `git/refs`
   - `curl` to `git-receive-pack`

   An in-process library push inside a script (pygit2, dulwich, isomorphic-git) is invisible to both layers. Record it as a stated limitation rather than claiming coverage.
6. **Add tests** for:
   - the "fetch first" case (E23a: record delivered, so it is refused when protected)
   - the six-field `HEAD@{0 days ago}:refs/heads/main` record
   - a SHA-256 repository
   - a linked worktree
   - a `config.worktree` hooksPath override
7. **Pin the version assumption.** 2.47.3 has no config-defined hooks. When the runtime git is 2.54.0 or later, `hook.<name>.command` hooks run in addition to the hookdir guard. When `hook.<event>.enabled` is released for hookdir hooks (2.98.0 draft), `-c hook.pre-push.enabled=false` disables the guard, so L1 must cover it (item 5).
8. **Revise the design wording at line 534 (D19-47)** to say that only non-fast-forward, stale, remote-updated and up-to-date refs are filtered, and that "fetch first" rejections still reach the hook.


