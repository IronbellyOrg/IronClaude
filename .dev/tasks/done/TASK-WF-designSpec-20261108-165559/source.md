---
artifact: design-spec
type: architecture
format: spec
issue: 441
topic: L2 git pre-push layer of the launch-level guard, and the IR-7 W-L2-ABSENT refusal path (built, OFF)
source: merged-requirements.md (adversarially merged spec, 457 lines)
created: 2026-11-08
status: draft for review; no implementation code
---

# Design spec: L2 pre-push guard and IR-7 refusal path (issue #441)

## 1. Scope, owner decisions and conventions

This spec turns `merged-requirements.md` (called "the spec" below and cited by section or by requirement ID) into an architecture: the components, their interfaces, the flows between them, the file change map and the commit order. It adds no requirement. Where the spec and the code disagree, the disagreement goes in section 12, not in a design change.

**Binding owner decisions (2026-11-08), kept in effect exactly as the owner gave them:**

| ID | Decision | Where this design enforces it |
|---|---|---|
| OD-1 | L2 is built only for the tested local Bash surface. The B-CTX gaps (Monitor, a `setsid` child, a killed supervisor) are documented limits. | §2 boundary note; LIM-1..LIM-3 and LIM-10 in §9; the FR-101 leak pins in §10 |
| OD-2 | `unknown` refuses only pushes whose destination is `refs/heads/main` or `refs/heads/master`, with a diagnostic, and allows every other push. | Verdict table in §7.1; sequence 4.3; self-test step 4 in §3.2 |
| OD-3 | The IR-7 refusal path is built but OFF: `IR7_REFUSE = False`, so `W-L2-ABSENT` stays a warning until the #442 observations pass. It goes in its own clearly marked commit, after every L2 commit. | §5.3 constant; §6.4 `remedy()`; commit E in §8.2 |

**Binding constraints:**
- The design §19.2 placement: one shared, owned `hooks/pre-push` that git finds by its default lookup. No foreign hook is replaced, `core.hooksPath` is not migrated, nothing is forwarded and no stubs are installed.
- Files are published without replacing an existing file.
- A hook is owned only when both its version line and its bytes match exactly.
- Installed primitives name only `~/.claude/...` paths (NFR-003).
- `.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/` is read-only.
- Sources are edited under `src/superclaude/` and its `plugins/superclaude/` mirrors, then `make sync-dev` is run. `.claude/` is never staged.

**Conventions:**
- Every `file:line` citation was re-read in this worktree on 2026-11-08 unless it is marked UNVERIFIED.
- A pseudo-signature gives the name, the parameters, the return type and the contract. No function body is given.
- **NEW** marks a new symbol, **EXISTS** an existing symbol and **MODIFIED** an existing symbol whose contract changes.

## 2. Components and the push data flow

### 2.1 Component diagram

```text
                        install / update time                       claim time (governed launch)
 +-------------------------------------------+        +------------------------------------------------------+
 | superclaude install | update              |        | C3  orca_worktree.py  cmd_launch(args)               |
 |  install_hooks.py  _FRESHNESS_SCRIPTS     |        |   enforcement_preflight(wt)   (IR-4, EXISTS)          |
 |   _copy_scripts()  0755, force on update  |        |   install_l2(wt)        NEW --> publish_no_replace() |
 +---------------------+---------------------+        |   l2_status(wt)         MODIFIED (ownership oracle)  |
                       | copies                       |   IR7_REFUSE / remedy() NEW (commit E, OFF)          |
                       v                              |   session_report(wt, l2, inode)  MODIFIED            |
 ~/.claude/hooks/launch-level-pre-push.sh  <---- byte equality (D-3) ----+                                    |
 ~/.claude/hooks/launch-job-identity.sh    (C2, EXISTS; FR-025 line)     +------------+-----------------------+
 ~/.claude/hooks/launch-level-guard.sh     (C4, EXISTS; FR-050 tokens)                | publishes (no replace)
                                                                                     v
                                    <git-common-dir>/hooks/pre-push               (byte copy of C1, 0755)
                                    <git-common-dir>/hooks/pre-push.launch-level  (data file, 0644, 2 lines)
                                                                                     ^
 push time                                                                           | read via ${0%/*}
 +-----------+   exec   +---------------------------------------------+   env -i, cd /, timeout 10
 | git push  |--------->| C1 pre-push hook (#!/bin/bash -p, LC_ALL=C)  |------------------------------+
 |  ($1,$2,  |  stdin   |   l2_split(), L2_PROTECTED[], verdict       |                              v
 |  records) |--------->|   exit 0 / 1 / 2 + one stderr diagnostic    |   C2 launch-job-identity.sh identify $$
 +-----------+          +---------------------------------------------+     -> one JSON line, exit 0
                                                                            reads <pinned HOME>/.claude/state/launch-level
                                                                            (store(), launch-job-identity.sh:102-111)
 Claude Code PreToolUse --> C4 launch-level-guard.sh (L1): text tokens for .git/hooks, --no-verify, hooksPath ... -> TAMPER
```

| ID | Component | Owning path (source) | Installed path | Status |
|---|---|---|---|---|
| C1 | Pre-push hook | `src/superclaude/hooks/scripts/launch-level-pre-push.sh`, plus the byte-identical `plugins/superclaude/hooks/scripts/launch-level-pre-push.sh` | `~/.claude/hooks/launch-level-pre-push.sh`, copied as `<common>/hooks/pre-push` | NEW (both paths confirmed absent) |
| C2 | Actor selector | `src/superclaude/hooks/scripts/launch-job-identity.sh` (566 lines) plus its plugin mirror | `~/.claude/hooks/launch-job-identity.sh` (`IDENTITY_COMMAND`, `orca_worktree.py:803`) | EXISTS; MODIFIED only by FR-025 |
| C3 | Claim-side installer and status | `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` | Runs from the skill's installed copy | EXISTS; MODIFIED |
| C4 | L1 text guard | `src/superclaude/hooks/scripts/launch-level-guard.sh` plus its plugin mirror | `~/.claude/hooks/launch-level-guard.sh` | EXISTS; MODIFIED (FR-050..FR-054) |
| P | Packaging | `src/superclaude/cli/install_hooks.py` (`_FRESHNESS_SCRIPTS` at `:42`, last entry `"launch-level-guard.sh"` at `:93`; `_copy_scripts` at `:251`) | n/a | EXISTS; MODIFIED (one list entry) |

**Boundaries.**
- **C1 owns no policy.** It turns the selector's single answer into a verdict over the ref records. All store validation stays in C2 (D-6), so C1 never parses JSON beyond the anchored whole-line shapes.
- **C2 is unchanged except for its unknown line (FR-025).** It is the only authority on actors (FR-023). No environment variable, branch or path can change the actor.
- **C3 is the only writer of repository files** and the only ownership oracle (`l2_status`). `install_l2` writes; `l2_status` only reads (FR-042).
- **C4 is the only in-session text defence.** It catches the visible bypasses that skip C1 (`--no-verify`, hooksPath, config injection, hook edits).
- **OD-1 boundary.** Everything above holds only for pushes that git runs from the tested local Bash surface, with the hook in effect. Execution surfaces C2 cannot classify, and pushes that never run the hook, are listed in §9 and are not designed around.

### 2.2 Push data flow

```text
git push <remote> <refspec...>
  └─> git resolves refspecs, then execs <common>/hooks/pre-push "$1" "$2"  (only if X_OK; otherwise fails open, LIM-9)
        C1 step 1  LC_ALL=C; ignore $1/$2 for the verdict (FR-009)
        C1 step 2  read ${0%/*}/pre-push.launch-level      ─ invalid/missing ─> actor=unknown, why="no valid data file"
        C1 step 3  [ -x <HOME>/.claude/hooks/launch-job-identity.sh ]  ─ no ─> actor=unknown, why="identity script missing"
        C1 step 4  ( cd / && exec /usr/bin/env -i HOME=<HOME> PATH=<uvdir>:/usr/bin:/bin UV_NO_CONFIG=1
                       /usr/bin/timeout 10 <HOME>/.claude/hooks/launch-job-identity.sh identify "$$" ) </dev/null 2>/dev/null
                   exit 124 ─> unknown "identity check timed out";  other ≠0 ─> unknown "identity check failed"
                   exit 0 and exactly one line, matched whole-line against FR-022 shapes 1..5;  else unknown "identity unknown"
        C1 step 5  actor=ordinary ─> exit 0 (stdin NOT read, no output)                         (FR-003, NFR-001)
        C1 step 6  actor ∈ {governed, unknown}: while IFS= read -r line || [ -n "$line" ]; do l2_split; checks; done
                   track: first_malformed(n, check), first_protected(ref)
        C1 step 7  verdict precedence  malformed > protected > allowed                         (FR-007)
                   malformed           ─> exit 2, L2-MALFORMED
                   protected, governed ─> exit 1, L2-PROTECTED
                   protected, unknown  ─> exit 1, L2-UNKNOWN (+ second line)
                   otherwise           ─> exit 0, silent
  └─> git aborts the whole push on a nonzero exit; the remote is unchanged
```

Data the flow depends on, and where each item comes from:

| Datum | Source | Never from |
|---|---|---|
| Pinned HOME | Line 1 of the data file | The pusher's `$HOME` (RC-5, T-22) |
| uv directory | Line 2 of the data file | The pusher's `$PATH` (RC-4, T-17) |
| Hooks directory | `${0%/*}` (git runs the hook by its path) | git config or the environment |
| Selected process | `$$`, the hook's own PID (a child of git in the pusher's kernel session) | `uv`'s child PID |
| Destination ref | Field 3 of the right-split record | `$1` or `$2` |

## 3. Install and claim flow

### 3.1 Two-stage installation (D-1)

| Stage | Trigger | Actor | Writes | Repository context |
|---|---|---|---|---|
| 1. Package | `superclaude install` / `superclaude update` | `install_hooks._copy_scripts()` (EXISTS, `:251`) driven by `_FRESHNESS_SCRIPTS` | `~/.claude/hooks/launch-level-pre-push.sh` (0755). An update refreshes it with `force=True`. No `hooks.json` registration. | none |
| 2. Repository | the claim's `launch` step: `cmd_launch` (EXISTS, `orca_worktree.py:1253`) | `install_l2(wt)` (NEW) | `<common>/hooks/pre-push.launch-level`, then `<common>/hooks/pre-push` | the launch worktree `wt` (D-2) |

### 3.2 `cmd_launch` order (after the change)

```text
cmd_launch(args)                                                       orca_worktree.py:1253
  1  ... existing argument and worktree checks (unchanged)
  2  absent = enforcement_preflight(wt)        IR-4, :1287; on refusal emit(failed, enforcement_hook="missing")
                                               -> install_l2 is never reached, so nothing is written (FR-031)
  3  hook = "installed"                        :1305
  4  (state_i, reason_i) = install_l2(wt)      NEW (FR-031); its result is advisory, l2_status is authoritative
  5  (l2, l2_reason)     = l2_status(wt)       MODIFIED tuple (FR-041); replaces :1311
  6  l2_notes = [("W-L2-ABSENT", L2_ABSENT_WHY(l2_reason))] if l2 != "owned" else []      FR-043; replaces :1312
  7  if IR7_REFUSE and l2_notes:               NEW, commit E only (FR-061); replaces the comment at :1307-1310
         return emit(launch_result("failed", l2_notes, enforcement_hook=hook))
  8  nonce, pending = publish_pending(word)    :1315 (unchanged); nothing above step 8 starts an agent
  9  ... orca agent launch ...
 10  release, layers = session_report(wt, (l2, l2_reason), inode)    :1376, MODIFIED parameter (Open conflict OC-2)
 11  emit(launch_result("launched", notes + l2_notes, ...))           :1379 ordering of notes unchanged
```

### 3.3 `install_l2(wt)` internal flow (FR-033..FR-038)

```text
install_l2(wt)
  env = clean_git_env()                          FR-032: drop GIT_DIR, GIT_COMMON_DIR, GIT_WORK_TREE,
                                                 GIT_CONFIG_PARAMETERS, GIT_CONFIG_COUNT, GIT_CONFIG_KEY_*/VALUE_*
  S1 safe case (FR-033); on any failure return the first failing state and reason, and write nothing
     1 git -C wt config --get core.hooksPath            exit 1 = unset; exit 0 -> unsupported; other -> failure "config-read-failed"
       git -C wt config --worktree --get core.hooksPath same rule
     2 git -C wt rev-parse --path-format=absolute --git-path hooks/pre-push
       == <git -C wt rev-parse --path-format=absolute --git-common-dir>/hooks/pre-push   else unsupported
     3 lstat(hooks dir): a dir, owned by euid, mode & 0o022 == 0     else unsupported "hooks-dir-unsafe"
       missing -> mkdir 0755
     4 ~/.claude/hooks/launch-level-pre-push.sh is a regular file containing L2_VERSION_LINE   else unavailable
     5 shutil.which("uv") -> uv_dir                     else unavailable
  S2 if lstat(<hooks>/pre-push) succeeds -> return ownership verdict (owned | conflict <reason>)    FR-034
  S3 publish_no_replace(hooks_fd, "pre-push.launch-level", f"{HOME}\n{uv_dir}\n", 0o644)
       EEXIST with equal bytes -> continue; EEXIST with other bytes -> conflict "data-file-differs"
  S4 stage: mkdir <hooks>/.<private-uuid>/ ; write the hook copy (0755) and a copy of the data file there
     self-test (FR-037), cwd=wt, argv=("origin","origin"):
       T1 empty stdin                               -> exit 0, empty stderr
       T2 the FR-021 selector line from the data file -> exit 0, one line matching an FR-022 shape  else "selector-env"
       T3 a main record, the claim process as actor  -> exit 0   (ordinary direction)
       T4 the staged copy with NO data file beside it -> main exit 1 L2-UNKNOWN, master exit 1 L2-UNKNOWN,
                                                        unprotected exit 0   (OD-2 direction)
     on failure: rm -r the private subdir only; keep the data file; return unavailable "<step>"
  S5 os.link(staged hook -> <hooks>/pre-push)   EEXIST -> fall to S6 (a racing installer or a foreign tool)
     remove the private subdir
  S6 (state, reason) = l2_status(wt); return ("installed" | "owned") only when it says owned, else its state
```

Order rationale: the data file is published first, so the hook is never visible without its data file (FR-036). The hook is linked from the tested staged inode, so the published bytes are exactly the bytes that were tested (FR-037). No rename is used anywhere (FR-035).

**Design note (T4 vs T2).** T4 depends on the data-file-missing path of C1, not on a stub selector, so the self-test needs no test double (FR-037: "the staged copy run with no data file beside it"). The copy of the data file sits next to the staged hook only for T1-T3. To run T4 it is removed, or T4 uses a second staging subdirectory. Either way stays inside the private subdirectory.

### 3.4 `l2_status(wt)` re-check (FR-041, read only)

```text
l2_status(wt) -> (state, reason)
  git rev-parse fails or prints nothing      -> ("absent", "git-failed")
  config read errors                         -> ("absent", "config-read-failed")
  hooksPath set (either scope) / paths differ -> ("unsupported", <reason>)
  hooks dir unsafe                           -> ("absent", "hooks-dir-unsafe")       note: install_l2 says unsupported (OC-9)
  no entry at <hooks>/pre-push               -> ("absent", "no pre-push hook")       reason text: UNVERIFIED wording
  entry is a symlink / not a regular file    -> ("conflict", "symlink")
  bytes != installed C1, no version line     -> ("conflict", "foreign")
  bytes != installed C1, version line present-> ("conflict", "stale")
  not X_OK                                   -> ("conflict", "not executable")
  data file missing / invalid / differs      -> ("absent", "data-file-differs")      FR-024 (absent, not conflict)
  otherwise                                  -> ("owned", "")
```

Every state other than `owned` produces `W-L2-ABSENT` with the reason. It stays a warning while `IR7_REFUSE` is `False` (OD-3).

## 4. Sequence diagrams

Participants used in all six diagrams:
- `G`: git
- `H`: the C1 hook
- `D`: the data file
- `S`: the C2 selector
- `St`: the launch-level store under the pinned HOME
- `R`: the bare remote

### 4.1 A governed agent pushes to main (refused)

```mermaid
sequenceDiagram
  participant A as Agent (Bash tool, governed session)
  participant G as git
  participant H as C1 pre-push hook
  participant D as pre-push.launch-level
  participant S as C2 identify
  participant St as store (pinned HOME)
  participant R as remote
  A->>G: git push origin HEAD:main
  G->>G: resolve the refspec to refs/heads/main
  G->>H: exec pre-push origin <url> (records on stdin)
  H->>D: read ${0%/*}/pre-push.launch-level (valid: HOME, uvdir)
  H->>S: env -i ... timeout 10 identify $$
  S->>St: jobs/<kernel sid>.json, sessions/<id>
  St-->>S: valid record, session live
  S-->>H: {"status": "governed", "session_id": "<id>"} exit 0
  H->>H: read all records to EOF; field3 == refs/heads/main -> protected
  H-->>G: exit 1; stderr "launch-level pre-push: L2-PROTECTED: ... refs/heads/main ..."
  G-->>A: error: failed to push some refs (nothing sent)
  Note over R: for-each-ref is unchanged (AC-1)
```

### 4.2 A human pushes from the same worktree (allowed)

```mermaid
sequenceDiagram
  participant U as Human terminal (own kernel session)
  participant G as git
  participant H as C1 hook
  participant S as C2 identify
  participant R as remote
  U->>G: git push origin HEAD:main
  G->>H: exec pre-push (records on stdin)
  H->>S: identify $$ (pinned HOME and uv from the data file; the human's PATH is irrelevant, T-17)
  S-->>H: {"status": "ordinary"} or {"status": "ordinary", "reason": "released"}
  H-->>G: exit 0 at once; stdin not read; no output (FR-003)
  G->>R: send pack; update refs/heads/main
```

### 4.3 Unknown identity: main/master refused, any other ref allowed (OD-2)

```mermaid
sequenceDiagram
  participant P as Pusher (unclassifiable)
  participant G as git
  participant H as C1 hook
  participant S as C2 identify
  participant R as remote
  P->>G: git push origin HEAD:main
  G->>H: exec pre-push
  H->>S: identify $$
  S-->>H: {"status": "unknown", "reason": "stale", "record": "/abs/.../jobs/<sid>.json"}
  H->>H: why = "job record stale at <P>"; record is protected
  H-->>G: exit 1; line 1 "L2-UNKNOWN: could not classify this push (job record stale at <P>) and it targets refs/heads/main ..."
  Note over H: line 2 (stale only) "... a person removes the record with: rm '<P>'"
  Note over H: for orphaned, foreign or unreadable, line 2 says to keep the record as evidence
  G-->>P: push refused; remote unchanged; record unchanged byte for byte
  P->>G: git push origin HEAD:feature
  G->>H: exec pre-push
  H->>S: identify $$ -> unknown (same reason)
  H->>H: field3 = refs/heads/feature, not in L2_PROTECTED
  H-->>G: exit 0, silent
  G->>R: refs/heads/feature created
```

Other ways to reach `unknown` follow the same path, and each `why` comes from a fixed table in C1:
- data file missing or invalid
- identity script missing
- exit 124
- another nonzero exit (for example 2 when uv is missing)
- output that is not a single line or does not match a shape
- the plain `{"status": "unknown"}` line

### 4.4 A malformed record (exit 2)

```mermaid
sequenceDiagram
  participant X as Synthetic caller (test) or git
  participant H as C1 hook
  participant S as C2 identify
  X->>H: stdin record 1 "refs/heads/x <oid> refs/heads/main <oid>"
  X->>H: stdin record 2 "a b c" (fewer than three spaces)
  H->>S: identify $$ -> governed (or unknown)
  H->>H: record 1 protected; record 2 malformed (n=2, check="fewer than four fields")
  H->>H: precedence malformed > protected (FR-007, T-19a)
  H-->>X: exit 2; "launch-level pre-push: L2-MALFORMED: git sent pre-push record 2 that this hook cannot read (<check>); the whole push was refused."
  Note over H: the raw record is never echoed. For ordinary, stdin is never read, so the result is exit 0.
```

### 4.5 Install on claim (fresh repository)

```mermaid
sequenceDiagram
  participant C as cmd_launch
  participant I as install_l2
  participant Gt as git (clean env)
  participant FS as <common>/hooks
  participant SH as staged hook (private subdir)
  participant L as l2_status
  C->>C: enforcement_preflight(wt) passes (IR-4)
  C->>I: install_l2(wt)
  I->>Gt: config --get core.hooksPath (exit 1), config --worktree --get (exit 1)
  I->>Gt: rev-parse --path-format=absolute --git-path hooks/pre-push == common-dir/hooks/pre-push
  I->>FS: lstat dir (owner, mode); lstat pre-push -> ENOENT
  I->>FS: publish_no_replace("pre-push.launch-level", "HOME\nuvdir\n", 0644)
  I->>SH: mkdir .<uuid>/ ; write hook 0755 and data copy
  I->>SH: T1 empty stdin / T2 selector line / T3 ordinary main / T4 unknown main, master, other
  SH-->>I: all pass
  I->>FS: os.link(staged hook, "pre-push", follow_symlinks=False); fsync(dir)
  I->>SH: rm -r private subdir
  I->>L: l2_status(wt)
  L-->>I: ("owned", "")
  I-->>C: ("installed", "")
  C->>L: l2_status(wt) -> owned, so l2_notes = []
  C->>C: publish_pending, agent launch, session_report "L2 pre-push: owned (...)"
```

The same shape covers the race: the losing installer gets EEXIST at `os.link`, re-checks with `l2_status`, gets `owned` and returns `("owned", "")` (FR-038).

### 4.6 Upgrade: the stale hook after `superclaude update`

```mermaid
sequenceDiagram
  participant U as superclaude update
  participant HC as ~/.claude/hooks/launch-level-pre-push.sh
  participant C as cmd_launch (next claim)
  participant I as install_l2
  participant L as l2_status
  participant FS as <common>/hooks/pre-push (old bytes)
  U->>HC: _copy_scripts(force=True) writes new bytes (version 1 or 2)
  C->>I: install_l2(wt)
  I->>FS: lstat pre-push succeeds
  I->>L: ownership verdict
  L-->>I: ("conflict", "stale: ... rm <hooks>/pre-push <hooks>/pre-push.launch-level")
  Note over I,FS: nothing is replaced and nothing is removed (D-4)
  I-->>C: ("conflict", "stale ...")
  C->>C: l2_notes = [W-L2-ABSENT, "...: stale ..."]
  alt IR7_REFUSE == False (shipped, OD-3)
    C->>C: launched, with the W-L2-ABSENT warning and remedy text
  else IR7_REFUSE == True (a later FR-065 commit only)
    C->>C: emit failed, enforcement_hook="installed"; no pending record; no agent
  end
  Note over FS: meanwhile pushes still run the OLD owned hook, which still refuses governed main/master
```

The machine-drift variant (LIM-5) has the same shape. After uv moves or HOME changes, the data file no longer equals what would be written now, so `l2_status` reports `("absent", "data-file-differs")` and nothing is rewritten.

## 5. Interface definitions: files, data file and constants

### 5.1 Files

| Path | Owner | Mode | Content contract | Status |
|---|---|---|---|---|
| `src/superclaude/hooks/scripts/launch-level-pre-push.sh` | C1 | 0755 in the package | Line 1 is exactly `#!/bin/bash -p`; line 2 is exactly `# launch-level-pre-push-version: 1`. Only bash builtins plus `/usr/bin/env` and `/usr/bin/timeout`. No jq, no Python, no git (FR-001, FR-010). | NEW |
| `plugins/superclaude/hooks/scripts/launch-level-pre-push.sh` | C1 mirror | 0755 | Byte-identical to the source (NFR-002) | NEW |
| `~/.claude/hooks/launch-level-pre-push.sh` | Packaging | 0755 | Copied by `_copy_scripts`; the reference bytes for D-3(a) | NEW (installed) |
| `<git-common-dir>/hooks/pre-push` | C3 (written), C1 (bytes) | 0755 | A byte copy of the installed C1; regular file, not a symlink | NEW per repository |
| `<git-common-dir>/hooks/pre-push.launch-level` | C3 | 0644 | See §5.2 | NEW per repository |
| `<git-common-dir>/hooks/.<private>/` | C3 (transient) | 0700 (proposed) | The staged hook and its data copy for the self-test; removed on success and on failure. A crash leaves it behind (LIM-20). Naming: dot-prefixed; the exact scheme is open (`uuid4().hex` follows the FR-035 temp-name precedent). | NEW, transient |
| `src/superclaude/hooks/scripts/launch-job-identity.sh` (+ `plugins/...` mirror) | C2 | unchanged | Only the unknown output line changes (FR-025) | MODIFIED |
| `src/superclaude/hooks/scripts/launch-level-guard.sh` (+ mirror) | C4 | unchanged | A second tamper `case` on the lowercased `LL_TT` (FR-050); LL-TAMPER text (FR-054) | MODIFIED |
| `src/superclaude/cli/install_hooks.py` | Packaging | n/a | `_FRESHNESS_SCRIPTS` gains `"launch-level-pre-push.sh"` after `:93` | MODIFIED |
| `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` | C3 | n/a | §6 | MODIFIED |

### 5.2 Data file `pre-push.launch-level`

| Field | Line | Type | Writer value | Reader validation (C1: FR-020; C3: FR-024) |
|---|---|---|---|---|
| `home` | 1 | absolute directory path, newline-terminated | `home_dir()` (EXISTS, `orca_worktree.py:874`, `$HOME` or `Path.home()`). See OC-8. | Starts with `/`. C1 checks only that it is absolute; C3 checks that it is equal to what would be written now. |
| `uv_dir` | 2 | absolute directory path, newline-terminated | `dirname(shutil.which("uv"))` in the claim process | Starts with `/`. C3 also checks that `<uv_dir>/uv` is an executable regular file (FR-024). |

File-level rules, for both readers:
- A regular file, not a symlink. C3 opens it with `O_RDONLY|O_NOFOLLOW`.
- Owned by the effective uid.
- `mode & 0o022 == 0`.
- Exactly two lines, each ending in `\n`, and no other bytes.
- No encoding beyond bytes. C1 compares under `LC_ALL=C`.

C1's validation is weaker than C3's (it has no executable check and no "equals now" check). That is intended: C1 resolves at run time and fails to `unknown`, while C3 is the ownership oracle.

**Path characters.** The data-file HOME is interpolated into the `env -i HOME=...` argument and into `<HOME>/.claude/hooks/...` as a quoted bash word, never evaluated. A HOME that contains a newline cannot be represented and is rejected by the two-line rule.

### 5.3 Constants

| Name | Owning file | Value | Status | Contract |
|---|---|---|---|---|
| `L2_PROTECTED` | C1 | `(refs/heads/main refs/heads/master)` (a bash array) | NEW | The only protected list (FR-005, §11 extension point) |
| hook version line | C1 line 2 | `# launch-level-pre-push-version: 1` | NEW | Must equal `L2_VERSION_LINE` (T-23, NFR-008) |
| `L2_VERSION_LINE` | `orca_worktree.py`, next to `GUARD_VERSION_LINE` (`:804`) | `"# launch-level-pre-push-version: 1"` | NEW | D-3(b); the installed C1 must contain it |
| packaged-hook sha256 pin | `tests/cli/test_install_hooks.py` or the new hook test file | the sha256 of the packaged C1 | NEW (test-only) | A byte change without a version bump fails (T-23). Owning test file: UNVERIFIED (the spec says "a test"). |
| `IR7_REFUSE` | `orca_worktree.py`, next to `REMEDY` (`:778`) | `False  # IR-7: turn on only after the #442 observations pass (owner decision 2026-11-08)` | NEW, commit E | D-5; changed only by a reviewed commit (FR-065) |
| `REMEDY["W-L2-ABSENT"]` | `orca_worktree.py:789` | `"the L2 pre-push hook is not in effect for this worktree, so the limits are enforced by the L1 guard only; the agent was started"` | MODIFIED (FR-045) | It names no bypass (FR-008) |
| IR-7 refusal remedy text | `orca_worktree.py` (inside `remedy()` or a sibling constant; the placement is a design choice) | `"the launch was refused and no agent was started; clear the reason above (the claim reference gives the exact rm command), then claim the issue again"` | NEW, commit E | FR-062 |
| `L2_ABSENT_WHY` | `orca_worktree.py:796` | Becomes a prefix: `"the owned L2 pre-push hook is not in effect for this worktree: "`, with the reason appended at the call site | MODIFIED (FR-043) | Keeping the name as a str prefix keeps its import surface unchanged. A callable is an alternative; this design chooses the prefix plus concatenation in `cmd_launch`. |
| `IDENTITY_COMMAND` | `orca_worktree.py:803` | `"~/.claude/hooks/launch-job-identity.sh"` | EXISTS | C1 uses the same relative path under the pinned HOME (D-7) |
| `GUARD_VERSION_LINE` | `orca_worktree.py:804` | `"# launch-level-guard-version: 1"` | EXISTS | Precedent only |
| `_FRESHNESS_SCRIPTS` | `install_hooks.py:42` | `+ "launch-level-pre-push.sh"` | MODIFIED | FR-030 |
| `DEFAULT_TIMEOUT` | `orca_worktree.py:79` | `120.0` | EXISTS | Default for `run()`. A self-test step should pass a shorter timeout (above the 10 s selector bound); the value is UNVERIFIED and a design choice. |

## 6. Interface definitions: functions

### 6.1 C1, the hook (bash; one file; contracts only)

| Function | Pseudo-signature | Contract |
|---|---|---|
| (entry) | `pre-push <remote> <url>` with records on stdin | `$1` and `$2` are ignored for the verdict and never printed (FR-009). Exit codes: 0, 1 or 2 only (§7.1). It writes no file and calls no git (FR-010). |
| `l2_data` (name proposed) | `l2_data` sets globals `L2_HOME`, `L2_UVDIR`; returns 0 when valid, 1 when not | Implements the FR-020 validity rules using only builtins. On failure, why = `no valid data file`. |
| `l2_actor` (name proposed) | `l2_actor` sets `L2_ACTOR` ∈ {governed, ordinary, unknown} and `L2_WHY` | Runs the FR-021 command line exactly, then the FR-022 anchored `[[ =~ ]]` shape table. It runs once, before stdin is read (FR-002). |
| `l2_split` | `l2_split "<line>"` sets `F1 F2 F3 F4`; returns 0 when split, 1 when there are fewer than three spaces | The name is fixed by FR-004. Right split by parameter expansion only (`${line##* }`, `${line% *}`); field 1 keeps its spaces (D-9). |
| `l2_check` (name proposed) | `l2_check` sets `L2_CHECK` (the name of the failed check) or leaves it empty | The FR-006 strict checks: empty field; field 2 or 4 not `^[0-9a-f]{40}$` or `^[0-9a-f]{64}$`; fields 2 and 4 of different lengths; a tab, CR or NUL; a blank line; field 3 not `refs/<nonempty>/...` or containing whitespace or control characters. |
| `l2_die` (name proposed) | `l2_die <code> <ref-or-n> <why-or-check>` prints the fixed diagnostic and exits 1 or 2 | Emits only the FR-008 fixed text. The session id is never printed and selector output is never forwarded. |

The names other than `l2_split` and `L2_PROTECTED` are proposals. The spec fixes only those two (FR-004, FR-005), so the other helpers may merge as long as the "one parser function" rule (NFR-008) holds.

### 6.2 C2, the selector (one change)

| Symbol | Location | Today | After FR-025 |
|---|---|---|---|
| `identify(pid)` | `launch-job-identity.sh:215-248` | Returns `{'status': 'unknown'}` for every exception (`:243-244`). One `ValueError('stale supervisor')` covers zombie, other sid, other start ticks and other boot (`:234-235`). `ValueError('foreign supervisor')` (`:236-237`). | Returns `{'status': 'unknown', 'reason': R, 'record': P}` once the record path `P = <store>/jobs/<sid>.json` is known (after `store()`/`subdir()` succeed). R is mapped as follows: zombie or pid gone → `orphaned`; other start ticks or other boot → `stale`; uid mismatch → `foreign`; any other exception after `P` is known → `unreadable`. Before `P` is known (for example `store()` raising `invalid home`/`unsafe home`), it stays plain `{'status': 'unknown'}`. |
| output | `:536` `print(json.dumps(result))` | `json.dumps` default separators give `{"status": "unknown"}` | Unchanged printer. The key order `status, reason, record` comes from dict insertion order and must match FR-022 shape 5 exactly (T-20). |
| `proc(pid)`, `boot()` | `:202`, `:210` | EXISTS | Used unchanged. "pid gone" is the `OSError` from `proc(value['pid'])`, which today falls into the generic except, so the split needs that call's error isolated. OC-3 covers the `actual_sid != sid` case. |

### 6.3 C3, `orca_worktree.py`

| Function | Pseudo-signature | Status | Contract |
|---|---|---|---|
| `run` | `run(argv: list[str], timeout: float = DEFAULT_TIMEOUT, cwd: str \| None = None, env: Mapping[str, str] \| None = None) -> Result` | MODIFIED (`:123-125`; `env` is NEW) | Verified: there is no `env` parameter today. When `env` is `None` the behaviour is identical (existing callers are untouched). FR-032 adds the parameter instead of a second runner. |
| `clean_git_env` (name proposed) | `clean_git_env() -> dict[str, str]` | NEW | Returns `os.environ` minus `GIT_DIR`, `GIT_COMMON_DIR`, `GIT_WORK_TREE`, `GIT_CONFIG_PARAMETERS`, `GIT_CONFIG_COUNT`, `GIT_CONFIG_KEY_*` and `GIT_CONFIG_VALUE_*` (FR-032). It is shared by `install_l2` and `l2_status`. |
| `publish_no_replace` | `publish_no_replace(dir_fd: int, name: str, data: bytes, mode: int) -> bool` | NEW | Returns True when it linked and False on `FileExistsError` (already present, so the caller re-checks). Any other `OSError` propagates. Steps: temp `.<name>.<uuid4 hex>` with `O_WRONLY\|O_CREAT\|O_EXCL\|O_NOFOLLOW` and `dir_fd`; write all bytes; `fchmod(mode)`; `fsync(fd)`; `os.link(..., src_dir_fd, dst_dir_fd, follow_symlinks=False)`; the temp file is always unlinked; `fsync(dir_fd)`. It never calls `rename`, `os.replace` or `shutil.copy*` (FR-035). |
| `install_l2` | `install_l2(wt: str) -> tuple[str, str]` | NEW | `state` ∈ {`installed`, `owned`, `conflict`, `unsupported`, `unavailable`}; `reason` is a human string and is empty for `installed`/`owned`. Flow in §3.3. It writes only in the safe case. A config-read error is reported as a failure, not as "unset" (FR-033 item 1; the exact state for that failure is OC-10). |
| `l2_status` | `l2_status(wt: str) -> tuple[str, str]` | MODIFIED (`:1012`, today `-> str`) | `state` ∈ {`owned`, `absent`, `conflict`, `unsupported`}. Read only: it never runs the hook or the selector (FR-042). It uses `--path-format=absolute` (FR-033 item 2) where today it joins `Path(wt) / out` (`:1020-1024`). Flow in §3.4. |
| `l2_data_expected` (name proposed) | `l2_data_expected() -> bytes \| None` | NEW | Returns `f"{home_dir()}\n{uv_dir}\n".encode()`, or `None` when `uv` is not found. It is the "what the installer would write now" used by both `install_l2` and `l2_status` (FR-024, D-3(d)), so both apply one rule. |
| `session_report` | `session_report(wt: str, l2: tuple[str, str], inode: int \| None = None) -> tuple[str, list[str]]` | MODIFIED (`:1032`) | Keeps its two-line contract. The `l2_line` (today `:1061-1067`) becomes the FR-044 text: owned → `L2 pre-push: owned (the launch-level pre-push hook, version 1, refuses this session's pushes to main and master)`; otherwise `L2 pre-push: <state> (<reason>; the limits are enforced by the L1 guard only)`. The parameter type change is OC-2. |
| `remedy` | `remedy(code: str) -> str` | NEW, commit E | Returns the IR-7 refusal text when `code == "W-L2-ABSENT" and IR7_REFUSE`, else `REMEDY[code]`. It replaces both `REMEDY[...]` lookups in `launch_result` (`:1206-1207`) (FR-062). |
| `launch_result` | `launch_result(status: str, notes: list[tuple[str, str]], **fields: object) -> dict` | EXISTS (`:1203`), lookups only | Its JSON keys and `emit` behaviour are unchanged (FR-063). |
| `cmd_launch` | `cmd_launch(args: argparse.Namespace) -> int` | MODIFIED (`:1253`) | The order is in §3.2. Commit B adds `install_l2`, the tuple `l2_status` and the new `l2_notes` rule. Commit E adds only the `IR7_REFUSE` line and removes the `:1307-1310` comment. |
| `home_dir` | `home_dir() -> Path` | EXISTS (`:874`) | The source of the data-file HOME (OC-8). |
| `enforcement_preflight` | `enforcement_preflight(wt: str) -> list[str]` | EXISTS (`:919`) | Unchanged. It runs before `install_l2`. |
| `publish_pending` | `publish_pending(word: str) -> tuple[str, Path]` | EXISTS (`:1071`; called at `:1315`) | Unchanged. The IR-7 refusal returns before it. |

### 6.4 Packaging and C4

| Symbol | Location | Status | Contract |
|---|---|---|---|
| `_copy_scripts` | `install_hooks.py:251` | EXISTS | Unchanged. It copies every `_FRESHNESS_SCRIPTS` entry with mode 0755 and `force` on update. |
| tamper `case` | `launch-level-guard.sh:705-707` (pattern list at `:706`) | EXISTS | Unchanged. |
| second tamper `case` | next to `:706`, on `${LL_TT,,}` (a lowercased copy of `LL_TT`, which is set at `:400`, `:442`, `:679`) | NEW | Adds `TAMPER` for the ten FR-050 tokens (§7.4). |
| `ll_deny LL-TAMPER` | `:738` (all four levels) | EXISTS | Unchanged; TAMPER has message precedence (`:722`). |
| LL-TAMPER text `b=` | `:95` | MODIFIED (FR-054) | Verified: the current text says "touching the launch-level state, the Claude Code settings or hooks, a git configuration file, or reinstalling the hooks". "the Claude Code ... hooks" does not cover git hook files, so the text gains "or the git pre-push hook". |

## 7. Interface definitions: exit codes, output shapes, diagnostics, states and tokens

### 7.1 Hook exit codes and verdict (FR-007)

| Actor | Stream | Exit | stderr |
|---|---|---|---|
| ordinary | not read | 0 | nothing |
| governed | empty, or only unprotected well-formed records | 0 | nothing |
| governed | any protected record and no malformed record | 1 | `L2-PROTECTED` (1 line) |
| unknown | empty, or only unprotected well-formed records | 0 | nothing |
| unknown | any protected record and no malformed record | 1 | `L2-UNKNOWN` (2 lines) |
| governed or unknown | any malformed record, anywhere in the stream | 2 | `L2-MALFORMED` (1 line) |

Precedence: malformed > protected > allowed. The hook always reads to EOF before deciding (NFR-010).

### 7.2 Selector output shapes accepted by C1 (FR-022)

Anchored whole-line matches, with exit 0 and exactly one stdout line:

| # | Line | Actor | why |
|---|---|---|---|
| 1 | `{"status": "ordinary"}` | ordinary | n/a |
| 2 | `{"status": "ordinary", "reason": "released"}` | ordinary | n/a |
| 3 | `{"status": "governed", "session_id": "<id>"}`, where `<id>` matches `[A-Za-z0-9][A-Za-z0-9_-]{0,127}` | governed | n/a |
| 4 | `{"status": "unknown"}` | unknown | `identity unknown` |
| 5 | `{"status": "unknown", "reason": "<R>", "record": "<P>"}`, where R ∈ {stale, orphaned, foreign, unreadable} and P is absolute | unknown | `job record <R> at <P>` |

Other results:
- Any other line, more than one line, or empty output: unknown, why `identity unknown`.
- Exit 124: why `identity check timed out`.
- Any other nonzero exit (including 2 when uv is missing, `launch-job-identity.sh:25` and `:53`): why `identity check failed`.
- A data file that is not valid: why `no valid data file`.
- No script, or a script that is not executable: why `identity script missing`.
- `identity check unreadable` is listed in FR-008. Its trigger is not defined in FR-022 (OC-11).

The characters allowed in P are not specified. A record path that contains `"` or `\` would be JSON-escaped by `json.dumps`, so it would fail a literal anchored match and fall to shape "other" (`identity unknown`). That is safe (still unknown) but loses the reason. It is recorded as risk R-6.

### 7.3 Diagnostic IDs

| ID | Emitter | Severity | Fixed text (owner: the spec, FR-008 / FR-043..FR-045 / FR-062) |
|---|---|---|---|
| `L2-PROTECTED` | C1, exit 1 | refusal | `launch-level pre-push: L2-PROTECTED: a governed launch session may not push to <ref>; the whole push was refused. A person releases the session as the claim's launch result describes.` |
| `L2-UNKNOWN` | C1, exit 1 | refusal | Line 1: `launch-level pre-push: L2-UNKNOWN: could not classify this push (<why>) and it targets <ref>; the whole push was refused, and pushes to other refs are allowed.` Line 2 names the routes: fix the cause (check `<hooks-dir>/pre-push.launch-level` and `~/.claude/hooks/launch-job-identity.sh`) or release the session. For R=`stale` only it says `no launch job owns this session any more; a person removes the record with: rm '<P>'`. For the other R values it says the record is kept as evidence. |
| `L2-MALFORMED` | C1, exit 2 | refusal | `launch-level pre-push: L2-MALFORMED: git sent pre-push record <n> that this hook cannot read (<check>); the whole push was refused.` The raw record is never echoed. |
| `W-L2-ABSENT` | C3, `launch_result` notes | warning (OD-3); refusal only when `IR7_REFUSE` | Note text: `L2_ABSENT_WHY` prefix + reason. Remedy: `REMEDY["W-L2-ABSENT"]` (FR-045), or the IR-7 refusal text through `remedy()` (FR-062). The code name never changes. |
| `LL-TAMPER` | C4, exit 2 | deny | The existing text (`launch-level-guard.sh:94-97`) plus "or the git pre-push hook" (FR-054) |

Global rule (FR-008, T-24): no diagnostic and no remedy names `--no-verify`, `core.hooksPath`, `-c`, `--config-env` or `GIT_CONFIG_`. The session id is never printed.

### 7.4 States and reasons

| Function | State | Reasons (exact strings where the spec fixes them) |
|---|---|---|
| `install_l2` | `installed`, `owned` | empty |
| `install_l2` | `conflict` | `foreign`, `stale`, `symlink`, `not executable`, `data-file-differs`; each ends with `rm <hooks-dir>/pre-push <hooks-dir>/pre-push.launch-level` and says the claim never deletes it (FR-034) |
| `install_l2` | `unsupported` | hooksPath set (wording UNVERIFIED), hook path not the common one (wording UNVERIFIED), `hooks-dir-unsafe` |
| `install_l2` | `unavailable` | `the packaged pre-push hook is not installed (run superclaude install)`; uv not found (wording UNVERIFIED); self-test step names, with `selector-env` for step 2 |
| `l2_status` | `owned` | empty |
| `l2_status` | `absent` | `git-failed`, `config-read-failed`, `hooks-dir-unsafe`, `data-file-differs`, no hook entry (wording UNVERIFIED) |
| `l2_status` | `conflict`, `unsupported` | as for `install_l2` |
| `launch_result` | `launched`, `failed` | EXISTS. `enforcement_hook` is `installed` on the IR-7 refusal (FR-061, FR-103). |

The word `present-unverified` is removed from `src/` and `tests/` (AC-6).

### 7.5 L1 tokens (C4, FR-050..FR-052)

All tokens are matched by a `case` on the lowercased `LL_TT` and add `TAMPER`, which is denied at W, WA, F and FS (`:738`):

| Token pattern | Covers | Today |
|---|---|---|
| `*.git/hooks*` | edits or `rm`/`chmod` of the hooks directory | not covered (`:706` has no such token) |
| `*hooks/pre-push*` | a hook path not spelled with `.git` (for example the common dir) | not covered |
| `*pre-push.launch-level*` | the data file | not covered |
| `*--no-verify*` | `git push --no-verify` and also `git commit --no-verify` (LIM-16) | only indirectly through PUSHFORM (`:658-669`) |
| `*hookspath*` | `-c core.hooksPath=`, `git config core.hooksPath` | UNKNOWN only (`:532-533`) |
| `*--config-env*` | `--config-env=core.hooksPath=V` | not covered |
| `*hook.pre-push*` | git 2.54+ config hooks (LIM-12) | not covered |
| `*git_config_count*`, `*git_config_parameters*`, `*git_config_key_*` | environment config injection | not covered |

`send-pack` is unchanged: it already adds PUSH (`:528-529`) and UNKNOWN (`:653`) (FR-053).

## 8. Module and file change map; delivery commit order

### 8.1 Change map

| # | Path | New / Modified | What changes | Commit |
|---|---|---|---|---|
| 1 | `src/superclaude/hooks/scripts/launch-level-pre-push.sh` | NEW | The C1 hook | A |
| 2 | `plugins/superclaude/hooks/scripts/launch-level-pre-push.sh` | NEW | Byte mirror of #1 | A |
| 3 | `src/superclaude/hooks/scripts/launch-job-identity.sh` | MODIFIED | `identify()` unknown line with reason and record (FR-025) | A |
| 4 | `plugins/superclaude/hooks/scripts/launch-job-identity.sh` | MODIFIED | Byte mirror of #3 | A |
| 5 | `src/superclaude/cli/install_hooks.py` | MODIFIED | One `_FRESHNESS_SCRIPTS` entry (FR-030) | A |
| 6 | `tests/cli/test_install_hooks.py` | MODIFIED | `_FRESHNESS_SCRIPTS` pin (`:104-105`) gains the name; a new packaging, mirror and executable test modelled on `:930`; it asserts `#!/bin/bash -p\n` (OC-5); sha256 pin (T-23) | A |
| 7 | `tests/hooks/test_launch_job_identity.py` | MODIFIED | Tests that assert the plain unknown line where a record exists move to the FR-025 shape (candidates `:387`, `:408`, `:429`; per-line list UNVERIFIED) | A |
| 8 | `tests/hooks/test_launch_level_pre_push.py` | NEW | FR-100 matrix, FR-101 leak pins, T-20..T-24 | A (installer placement switched in B) |
| 9 | `tests/hooks/test_launch_level_pre_push_records.py` | NEW | Direct-hook subgroup T-D1..T-D5 | A |
| 10 | `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` | MODIFIED | `run(env=)`, `clean_git_env`, `publish_no_replace`, `l2_data_expected`, `install_l2`, `L2_VERSION_LINE`, `l2_status` tuple, `session_report` parameter and line, `L2_ABSENT_WHY`, `REMEDY["W-L2-ABSENT"]`, the `:794-795` comment, the docstring `:49-51`, `cmd_launch` steps 4-6 | B |
| 11 | `tests/skills/test_issue_l2_install.py` | NEW | FR-102 (plus the forgery and publication subgroups) | B |
| 12 | `tests/skills/test_issue_orca_worktree.py` | MODIFIED | `test_ir6_l2_status_follows_the_git_hook_path` (`:1686-1730`), the remedy assertion at `:1728`, the `present-unverified` claim.md assertion at `:1672` (OC-4), the `W-L2-ABSENT` text assertions | B |
| 13 | `src/superclaude/hooks/scripts/launch-level-guard.sh` | MODIFIED | The second tamper `case` (FR-050) and the LL-TAMPER text (FR-054) | C |
| 14 | `plugins/superclaude/hooks/scripts/launch-level-guard.sh` | MODIFIED | Byte mirror of #13 | C |
| 15 | `tests/hooks/test_launch_level_guard_l2_tokens.py` | NEW | FR-104 | C |
| 16 | `docs/designs/sc-issue-launch-level-hook.md` | MODIFIED | §19.1 `:493`, §19.2 `:508-514`, §19.3 `:516-520`, §19.5 `:528-534`, §19.8 `:567-578`, and `:6`, `:34`, `:355` (spec §8) | D |
| 17 | `docs/designs/sc-issue-claim-pipeline-flag.md` | MODIFIED (conditional) | `:4`, `:60`, `:135`, `:291`, `:349`, `:381`, only where they claim no L2 exists (UNVERIFIED) | D |
| 18 | `src/superclaude/skills/sc-issue-protocol/refs/claim.md` | MODIFIED | `:127` remedy row, `:129` paragraph | D (OC-4: `:1672` forces it into B or a joint B+D) |
| 19 | `src/superclaude/skills/sc-issue-protocol/SKILL.md` | MODIFIED | `:92`, `:136`, `:150` | D |
| 20 | `src/superclaude/commands/issue.md` | MODIFIED | `:16` | D |
| 21 | `docs/user-guide/commands.md` | MODIFIED | `:381` | D |
| 22 | `.dev/tasks/<L2 plan package>/artifacts/final-check-retest.md` (name proposed) | NEW | The `final-check.md` limits re-test table (AC-11) | D |
| 23 | `orca_worktree.py` (same file as #10) | MODIFIED | `IR7_REFUSE = False`, `remedy()`, the two `launch_result` lookups, the IR-7 line in `cmd_launch` replacing the `:1307-1310` comment | E |
| 24 | `tests/skills/test_issue_l2_install.py` (same file as #11) | MODIFIED | FR-103 in both switch positions, plus the source assertion `IR7_REFUSE is False` | E |

Not touched:
- `tests/hooks/test_launch_level_guard.py` (#440, NFR-009)
- `.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/`
- every `.claude/` mirror (regenerated by `make sync-dev`, never staged)
- `hooks.json`
- any git configuration

Installed-primitive path check: the new hook, `orca_worktree.py`, the selector and the guard name only `~/.claude/hooks/...` and `${0%/*}` paths (NFR-003). `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` must gain no hit.

### 8.2 Commit order

```text
A  hook + FR-025 selector line + packaging + hook tests      (feat(hooks): ...)
B  install_l2 / publish_no_replace / l2_status / report       (feat(issue): ...)
C  L1 tokens                                                 (feat(hooks): ...)
D  docs + final-check re-test table                          (docs: ...)
---------------------------------------------------------------- every L2 commit above this line
E  IR-7 refusal path, SWITCHED OFF  (IR7_REFUSE = False)     feat(issue): add the IR-7 W-L2-ABSENT refusal path, switched off
```

Ordering rules:
- **A and B** may be swapped or joined if the hook tests cannot run without the installer (spec §9 item 1). Before B, the tests in A place the hook with a direct, test-local copy, then switch to `install_l2` in B. Both A and B must come before D.
- **C** is independent of A and B. It is coordinated with #440 if that issue edits `launch-level-guard.sh` (UNVERIFIED).
- **E is last and separate (OD-3, FR-064):**
  - The body states that E changes no behaviour while `IR7_REFUSE` is `False`.
  - The body lists the FR-065 turn-on preconditions: owner-recorded PASS for #442 OB-H1 item 1, OB-H2 and OB-H3, including the real-claim disposable-bare-remote check; owner approval; the docs moved from warning to refusal in the same commit; and an upgrade path for stale hooks, or the owner's acceptance of the re-claim cost.
  - A source test pins `IR7_REFUSE is False`.
- **Turn-on** (`IR7_REFUSE = True`) is out of scope: a later, explicit, owner-authorized and marked commit.

After every commit: `make sync-dev`, then `make verify-sync`. Only `src/`, `plugins/`, `tests/`, `docs/` and `.dev/tasks/` paths are staged.

## 9. Limits and risks

### 9.1 Documented limits (spec §6; this design adds none)

L2 is a same-user guard for the tested local Bash surface, not a sandbox (OD-1).

| ID | Limit (short) | Covered at L1 by | Impact |
|---|---|---|---|
| LIM-1 | Monitor reports `ordinary` (B-CTX) | Monitor text (`:716`) | High |
| LIM-2 | A `setsid` or daemonized child escapes the kernel session (B-CTX) | `setsid` text | High |
| LIM-3 | Killed supervisor → `unknown`/`orphaned` (B-CTX) | n/a; still fails closed for main/master | Low |
| LIM-4 | `--no-verify`, `-c core.hooksPath`, `--config-env`, `GIT_CONFIG_*` skip or redirect the hook | FR-050..FR-052 | High |
| LIM-5 | uv moves or HOME changes after install → `absent`/`data-file-differs`; manual `rm` | n/a | Low |
| LIM-6 | Per-worktree `core.hooksPath` set after install | `git config` writes are UNKNOWN (`:651`) | Medium |
| LIM-7 | `send-pack`, `receive-pack`, libgit2, dulwich | send-pack text | High |
| LIM-8 | `gh api`, REST, `orca terminal send` ref writes | GHWRITE / ESCAPE | High |
| LIM-9 | A missing or non-executable hook fails open | FR-050; next claim's `l2_status` | Medium |
| LIM-10 | Same-user modification of any link in the selector chain; check/use race | tokens only | High |
| LIM-11 | An agent whose job record lives under another HOME | PUSHFORM rejects `HOME=... git push` | Medium |
| LIM-12 | git 2.54+ `hook.<name>.command` / `hook.pre-push.enabled=false` | `hook.pre-push` token | High |
| LIM-13 | Wrong remote (only the ref name is checked) | canonical push allows `origin` | Medium |
| LIM-14 | A stale job record refuses a human's main/master until the `rm` | n/a | High |
| LIM-15 | A human with another uid → `unreadable` → main/master refused | n/a | Medium |
| LIM-16 | L1 over-block (`ls .git/hooks`, `git commit --no-verify`) | n/a | Low |
| LIM-17 | Any template byte change → every repository reads `conflict`/`stale` | n/a | Medium |
| LIM-18 | A case-folding remote | none | Low |
| LIM-19 | No hook-wide time bound beyond the 10 s selector | none | Low |
| LIM-20 | An orphaned self-test private subdirectory | hooks-dir tokens | Low |

### 9.2 Architectural risks found by this design (no requirement change; mitigation inside the spec's bounds)

| ID | Risk | Likelihood / impact | Mitigation (within the spec) |
|---|---|---|---|
| R-1 | Per-push latency: every push, including every human push, pays one `uv run` start (NFR-005). At scale (many pushes, slow disks) this is the dominant cost. | High / Low | Measured, not asserted (AC-12). The ordinary path still pays it, because the hook has to ask C2 first (FR-002). Caching the answer is out of scope: a cache would be a second policy authority (D-6). |
| R-2 | Skew across the three byte-identical copies (source, plugin mirror, installed) and every claimed repository's copy. A single template edit marks every repository `stale` (LIM-17). | Medium / Medium | `L2_VERSION_LINE` plus the sha256 pin (T-23) make a silent edit impossible. The upgrade path is an extension point (spec §11). With IR-7 on, the blast radius would be every launch (FR-065 (d)). |
| R-3 | Self-test T2 runs the real selector in the claim process. A host that needs an extra variable under `env -i` fails as `selector-env` and leaves L2 unavailable on that host (UNVERIFIED). | Low / Low (OD-3 keeps it a warning) | Reported precisely by reason. No widening of `env -i`, which is the INV-001 control. |
| R-4 | The pinned uv comes from the claim process's `shutil.which("uv")`. If that is a different uv from the human's, a broken claim-side uv turns humans into `unknown` (main/master refused). | Low / Medium | FR-024 checks that `<uv_dir>/uv` is executable at every claim. Whether it is the same uv is UNVERIFIED (spec §12). |
| R-5 | `install_l2` publishes the data file before linking the hook. A crash between the two leaves an inert data file; the next claim sees "equal bytes", continues, and links. | Low / None | This is the intended order (FR-036). |
| R-6 | A record path P with JSON-escaped characters fails the literal shape-5 match and falls to `identity unknown`. That is safe, but the `rm` hint is lost. | Very low / Low | Store paths are under the pinned HOME. The test HOME should use plain characters; an escaped-path test is optional. |
| R-7 | C2 change ripple: other callers of `identify` that parse `{"status": "unknown"}` exactly. Only C1 and the tests are known (FR-022 consumes it in C1). | Low / Medium | T-20 pins the shapes. A repository grep for `"status": "unknown"` consumers is part of commit A (UNVERIFIED that none exist outside tests). |
| R-8 | `run()` gains an `env` parameter. Every existing caller keeps `env=None`, so nothing changes for them. | Low / Low | The default keeps the existing behaviour; there is no second runner (FR-032). |
| R-9 | 10x growth in linked worktrees per repository costs nothing extra: there is one shared hook and data file per common dir (D-2). 10x growth in repositories is linear: one install per repository at claim time; no global registry. | n/a | This is by design. |

## 10. Test matrix and traceability

### 10.1 Test placement

| File | Status | Groups | Requirements |
|---|---|---|---|
| `tests/hooks/test_launch_level_pre_push.py` | NEW | T-01..T-24, T-16a/b/c, T-STALE-1, FR-101 leak pins | FR-001..FR-010, FR-020..FR-025, FR-101 |
| `tests/hooks/test_launch_level_pre_push_records.py` | NEW | T-D1..T-D5 | FR-003, FR-004, FR-006, FR-010, FR-022 |
| `tests/skills/test_issue_l2_install.py` | NEW | FR-102 (with its forgery and publication subgroups), FR-103 | FR-024, FR-030..FR-045, FR-060..FR-064 |
| `tests/hooks/test_launch_level_guard_l2_tokens.py` | NEW | FR-104 | FR-050..FR-055 |
| `tests/skills/test_issue_orca_worktree.py` | MODIFIED | FR-105 | FR-041, FR-043..FR-045 |
| `tests/cli/test_install_hooks.py` | MODIFIED | packaging, mirror, sha256 pin | FR-030, NFR-002, NFR-008 |
| `tests/hooks/test_launch_job_identity.py` | MODIFIED | unknown-line shape | FR-025 |
| `tests/skills/test_issue_protocol.py:471-487` | unchanged, must stay green | `W-L2-ABSENT` still listed | FR-062 (code name kept) |

Fixtures:
- Real git, with `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM` set to `/dev/null`.
- A temporary HOME and `git worktree add` in tmp.
- Remote state checked with `for-each-ref` before and after each push.
- The governed actor comes from the selector's `prepare`/`run` with a fake store. This is modelled on `LocalPushFixture` (`tests/hooks/test_launch_job_identity.py:1175-1283`) and is defined in the new files, not imported.

### 10.2 Test matrix by requirement

| Requirement | Tests |
|---|---|
| FR-001 (shebang, version line, builtins) | packaging test (`#!/bin/bash -p\n`), T-21(a)(b), T-23 |
| FR-002, FR-003 (actor first; ordinary silent) | T-D3, every "Human" column of T-01..T-17, T-19 (human stdin not read) |
| FR-004, FR-006 (right split; strict checks) | T-10, T-19, T-D2, T-D4 |
| FR-005 (protected exact names) | T-01..T-06, T-07 |
| FR-007 (precedence, exit 2) | T-19, T-19a |
| FR-008 (diagnostic text; no bypass named) | T-09, T-16, T-16a, T-STALE-1, T-24 |
| FR-009, FR-010 (args ignored; no side effects) | T-D5; a remote named like an option (in T-D group, proposed) |
| FR-020, FR-021 (data file; hardened call) | T-17, T-18, T-21, T-22 |
| FR-022 (shapes) | T-20, T-D1 |
| FR-025 (selector reason and record) | T-16, T-16a, T-16c, T-STALE-1, T-20, and the moved tests in `test_launch_job_identity.py` |
| FR-030 (packaging) | `test_install_hooks.py` pin plus the new packaging test |
| FR-031..FR-038 (install) | FR-102, including its forgery and publication subgroups |
| FR-039 (no other hooks touched) | FR-102 (directory listing: `pre-commit` and sample hooks unchanged; proposed assertion) |
| FR-040 (release) | T-15 |
| FR-024, FR-041..FR-045 (status, notes, report, remedy) | FR-102, FR-105 |
| FR-050..FR-055 (L1) | FR-104 |
| FR-060..FR-064 (IR-7) | FR-103, including the source pin `IR7_REFUSE is False` |
| NFR-002 (mirror parity) | packaging tests; `make verify-sync` |
| NFR-005 (latency) | measurement recorded in design §19.8, not a test (AC-12) |
| NFR-009 (#440 file untouched) | AC-10 `git diff --stat` check |

### 10.3 Traceability (spec §13, with this design's sections added)

| ID | Requirements | Design section | Tests | Limits | Status |
|---|---|---|---|---|---|
| RC-1 | FR-001..FR-008, FR-050..FR-052 | §2.2, §6.1, §7.1, §7.5 | T-01..T-13, FR-104 | LIM-4 | closed for the hook's surface |
| RC-2 | FR-024, FR-041..FR-045 | §3.4, §6.3 `l2_status` | FR-102 forgery, FR-105 | LIM-9 | closed |
| RC-3 | FR-004, FR-006 | §6.1 `l2_split`, `l2_check` | T-10, T-19, T-D2, T-D4 | — | closed |
| RC-4 | FR-020, FR-021 | §2.2 data table, §5.2 | T-17, T-18 | LIM-5 | closed |
| RC-5 | FR-020, FR-021 | §5.2, seq. 4.1 | T-22 | LIM-11 | closed for pusher redirection |
| RC-6 | FR-035 | §6.3 `publish_no_replace` | FR-102 publication | LIM-9 | closed |
| RC-7 | FR-050..FR-052 | §7.5 | FR-104 | LIM-4, LIM-16 | closed for visible spellings |
| RC-8 | FR-060..FR-065 | §3.2 step 7, §6.3 `remedy`, §8.2 E | FR-103 | — | built, OFF (OD-3) |
| INV-001 | FR-001, FR-021, FR-037 | §2.2 step 4, §3.3 S4 | T-21 | LIM-10 | closed; same-user residual |
| INV-002 | FR-008, FR-022, FR-025 | §6.2, §7.2, seq. 4.3 | T-16, T-16a, T-STALE-1, T-20 | LIM-3, LIM-14 | closed by reason, path and `rm` |
| INV-003 | FR-025 | §6.2 (`foreign`/`unreadable`) | T-16c | LIM-15 | accepted (OD-2 cost) |
| INV-005 | FR-020, FR-021 | §5.2 | T-22 | LIM-11 | pusher redirection closed |
| INV-007 | NFR-008, FR-065 | §5.3 sha256 pin, seq. 4.6 | T-23 | LIM-17 | closed by pin; upgrade path open |
| INV-011 | FR-005 | §7.1 | — | LIM-18 | unresolved by debate |
| INV-012 | spec §1, FR-050 | §2.1 OD-1 boundary | FR-104 | LIM-6, LIM-9, LIM-10 | out of scope (OD-1) |
| INV-013 | NFR-010 | §2.2 step 6 | T-D3 (ordinary only) | LIM-19 | unresolved by debate |
| INV-016 | FR-007 | §7.1 | T-19, T-19a | — | closed |
| INV-017 | FR-037 | §3.3 S4 | FR-102 (no private subdir left) | LIM-20 | unresolved by debate |
| OD-1 | spec §1, FR-021 | §1, §2.1 | FR-101 | LIM-1, LIM-2, LIM-3, LIM-10 | kept |
| OD-2 | FR-005, FR-007, FR-008, FR-025 | §7.1, seq. 4.3, §3.3 T4 | T-16, T-16a, T-16c, T-STALE-1, T-18, T-19 | LIM-14, LIM-15 | kept |
| OD-3 | FR-060..FR-065 | §5.3, §6.3, §8.2 E, seq. 4.6 | FR-103 | LIM-5, LIM-17 | kept: E last, `IR7_REFUSE = False` |

### 10.4 Acceptance criteria to evidence

| AC | Evidence |
|---|---|
| AC-1 | T-01..T-06, T-09..T-13, T-21, T-22 (governed), with `for-each-ref` unchanged |
| AC-2 | the Human column of T-01..T-17 |
| AC-3 | T-16, T-16a, T-16c, T-STALE-1, T-18 |
| AC-4 | T-07, T-08, T-10, T-19, T-19a |
| AC-5 | FR-102 |
| AC-6 | FR-102, FR-105; `grep -rn present-unverified src tests` is empty |
| AC-7 | FR-104, FR-101 |
| AC-8 | FR-103; commit E, last |
| AC-9 | spec §8 docs; `make verify-sync`; the mirror tests; the NFR-003 grep |
| AC-10 | the pytest command line in spec AC-10 |
| AC-11 | the re-test table in the plan package `artifacts/`; OB-H3 listed as pending |
| AC-12 | the §19.8 measurement |

## 11. UNVERIFIED register

Each item below could not be confirmed from the code or the requirements. Implementation must settle it, and must not assume an answer.

| # | Item | Where it matters | How to settle |
|---|---|---|---|
| U-1 | The minimum git version that supports `rev-parse --path-format=absolute --git-path`. The local git is 2.47.3 (verified); the floor is not. | §3.3 S1, §6.3 `install_l2`, §6.3 `l2_status` | Check the git release notes; pin the floor in the installer reason text. |
| U-2 | Whether #440 edits `launch-level-guard.sh` in a way that conflicts with the FR-050 token edit (NFR-009). | §7.5, §8.2 commit C | Rebase onto the merged #440 before commit C; run the AC-10 `git diff --stat` check. |
| U-3 | Per-push latency of the selector call (`env -i` + `uv run`). | NFR-005, AC-12 | Measure; record in design §19.8. |
| U-4 | Whether `env -i HOME PATH UV_NO_CONFIG` is enough for `uv run` to resolve its cache, or whether more variables (for example `UV_CACHE_DIR`, `XDG_*`) are needed. | §5.2, FR-021 | T-17 / T-18 on a clean HOME. |
| U-5 | Whether the `uv` directory recorded at claim time is the same `uv` a human pusher has on PATH. | §5.2 data file line 2, LIM-5 | Observe on the owner's machine; document if they differ. |
| U-6 | The exact kernel rule that makes the stale `rm` remedy safe (pid reuse versus start-time check). | §7.3 FR-008 text, T-STALE-1 | Confirm against `launch-job-identity.sh` `proc()`/`boot()` (:202, :210) semantics on the target kernel. |
| U-7 | Whether CI has a second uid available for the foreign-owner tests (T-16c, FR-102 forgery). | §10.1 | Check the CI runner; otherwise mark these tests `skipif` with a reason. |
| U-8 | Whether `cmd_launch` sets the agent's HOME, or whether the agent inherits the claimant's HOME. | §3.2, §5.2 (data-file HOME), OC-8 | Read the Orca launch path; observe one live launch. |
| U-9 | Whether any remote treats `refs/heads/Main` or `refs/heads/MAIN` as `main` (case folding). | LIM-18, FR-005 | Out of scope to fix; record the observation. |
| U-10 | OB-H3 (the #442 observation) is still pending. | OD-3, commit E, AC-11 | Wait for #442; list it as pending in the AC-11 table. |
| U-11 | Whether the doc lines for the claim-pipeline flag currently say that no L2 exists. | spec §8 docs, commit D | Grep the docs during commit D. |
| U-12 | The exact selector test lines in `tests/hooks/test_launch_job_identity.py` that assert the old `{'status':'unknown'}` shape. Candidates are :387, :408, :429, and possibly :533, :544, :1474, :1481. | FR-025, §8.1 | Grep `"unknown"` in that file before editing. |
| U-13 | The reason wording for the states the requirements do not specify: `core.hooksPath` set, path mismatch, `uv` missing, and no hook entry. | §7.4 | Propose wording in commit B; the owner reviews it. |
| U-14 | Three open points: (a) which test file owns the sha256 pin; (b) whether any consumer outside the tests reads `"status": "unknown"` from the selector; (c) the self-test timeout value. | §5.3, FR-025, §3.3 S4 | (a) and (b): grep the repo. (c): pick a value under `DEFAULT_TIMEOUT` (120.0, `orca_worktree.py:79`) and document it. |

Resolved during design (no longer UNVERIFIED):
- `run()` (`orca_worktree.py:123-125`) has no `env` parameter, so the self-test needs its own subprocess call.
- The LL-TAMPER `b=` text (`launch-level-guard.sh:94-97`) does not mention git hook files.
- The local git is 2.47.3.
- The store path is `$HOME/.claude/state/launch-level` (`launch-job-identity.sh:102-111`).

## 12. Open conflicts

These are conflicts between the requirements and the current code or docs. The design does not resolve any of them on its own; the owner decides. Each entry gives a proposed resolution that keeps OD-1..OD-3 unchanged.

| ID | Conflict | Evidence | Proposed resolution | Severity |
|---|---|---|---|---|
| **OC-1** | Two docs say an absent L2 refuses the launch: design §19.2 and the IR-7 definition. OD-3 keeps W-L2-ABSENT a warning (`IR7_REFUSE = False`) until the #442 observations pass. | design doc §19.2 :514, IR-7 definition :355; `orca_worktree.py:789-796` (W-L2-ABSENT, IR-7 comment, `L2_ABSENT_WHY`) | In commit D, reword both lines: refusal is built but OFF until #442. Commit E only flips the constant, and only with owner approval. | High: the docs would otherwise promise a refusal that does not happen. |
| OC-2 | `session_report` takes `l2: str` (:1032, `l2_line` at :1061-1067). FR-044 needs the `(state, reason)` tuple, and is silent on the signature change. | `orca_worktree.py:1032`, `:1061-1067`, `:1311-1312` | Change the parameter to the tuple in commit B; update every caller (`:1376`). | Medium |
| OC-3 | `identify` has one 'stale supervisor' branch (:234-235) covering Z state, sid mismatch, start mismatch and boot mismatch. FR-025 needs `orphaned` (Z or pid gone) split from `stale` (start/boot). `actual_sid != sid` has no FR-025 class. | `launch-job-identity.sh:224-244` | Split the branch; classify the sid mismatch as `stale`. The owner confirms. | Medium |
| OC-4 | `tests/skills/test_issue_orca_worktree.py:1672` asserts "present-unverified" in claim.md, but FR-105 does not list it. AC-6 removes that state, which forces the claim.md edit into commit B. | test :1672; AC-6 | Add the test and claim.md to the commit B change list (done in §8). | Medium |
| OC-5 | The existing guard packaging test asserts the shebang `#!/bin/bash\n`. The new hook's FR-001 shebang is `#!/bin/bash -p\n`. | `tests/cli/test_install_hooks.py` (guard pin) | Give the new hook a separate assertion; leave the guard pin alone. | Low |
| OC-6 | test_ir6's `core.hooksPath` case changes from `present-unverified` to `unsupported`, which is a behaviour change. Its remedy assertion expects "L2 layer is not built yet". | `tests/skills/test_issue_orca_worktree.py:1728` | Update both assertions in commit B, and record the behaviour change in the PR body. | Medium |
| OC-7 | RC-5 cites `launch-job-identity.sh:100-102` for `store()`. The function actually starts at :102. | `launch-job-identity.sh:102-111` | Correct the citation in the requirements (doc only). | Low |
| OC-8 | The data file's HOME should come from `home_dir()` (env HOME, `orca_worktree.py:874`), not the passwd home. The requirements leave the source unstated, and U-8 is open. | FR-020; `orca_worktree.py:874` | Use `home_dir()`, the same source the selector's `store()` uses. | Medium |
| OC-9 | An unsafe hooks directory is `unsupported` in `install_l2` (FR-033) but `absent` in `l2_status` (FR-041). | FR-033, FR-041 | Use one state for both; propose `unsupported`. | Medium |
| OC-10 | FR-033 and FR-041 do not say which `install_l2` state a git config read error produces. | FR-033, FR-041 | Propose `unsupported`, with the reason "git config unreadable". | Low |
| OC-11 | FR-008 lists the why "identity check unreadable", but FR-022 defines no shape that triggers it. | FR-008, FR-022 | Either map it to FR-022 shape 5 (unparseable output) or drop it from FR-008. | Low |
| OC-12 | A data file that differs is `conflict` in `install_l2` (FR-034) but `absent` in `l2_status` (FR-024, FR-041, LIM-5). | FR-024, FR-034, FR-041 | Keep `install_l2` = `conflict` (it does not overwrite), and make `l2_status` report `conflict` too, so the notes match. | Medium |

Count: 12. The most important is OC-1.
