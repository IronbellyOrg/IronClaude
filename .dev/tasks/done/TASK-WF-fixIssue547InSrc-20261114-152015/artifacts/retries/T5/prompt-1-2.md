53f08dfada9b1e87d0fdb92f483f1eb8a8d18de0
Review one task for spec compliance.

Task brief: ## Task 5: Update the design document where the git call is described and commit T2

Depends on: Task 4

Edit `docs/designs/orchestrator-mode.md` only where a sentence became false: line 67 (GQ-110 says exactly one `git status` per worktree: it now runs up to three read-only inspection calls and then one status, with fsmonitor disabled and submodules ignored), line 542 (the `ALLOWED_GIT` listing), lines 255 and 310 (the argv shown in the diagrams) and line 613 only if it still reads true. Do not touch `docs/designs/orchestrator-mode-review-1.md` (a dated review). Then run `uv run ruff format` and `uv run ruff check` on the changed Python files, `uv run pytest tests/sweep -q`, stage named paths (`src/superclaude/cli/sweep/probes.py`, `tests/sweep/test_git_config_hole.py`, `tests/sweep/test_probes_allowlist.py`, `tests/sweep/test_readonly.py`, `tests/sweep/conftest.py`, `docs/designs/orchestrator-mode.md`, and `.dev/tasks`) and commit locally with the subject `fix(sweep): stop git calls from running repository-configured programs (issue 547)`, a body listing each pinned test edited and why, and the Co-Authored-By line. Save the green run output to `./artifacts/t2-green.log`.

Acceptance criteria:
- `git show --stat HEAD` lists only the named paths and the plan package; no `.claude/` path is staged.
- `uv run pytest tests/sweep -q` passes and `uv run ruff check` reports no error on the changed files; ./artifacts/t2-green.log holds the output.
- docs/designs/orchestrator-mode.md no longer says "exactly one `git status`" without the added inspection calls, and still names no JSON key that does not exist.


Global constraints: 
- Owner design A (2026-11-14): `--ignore-submodules=all` goes into the status template; a submodule's own changes are no longer reported. No new JSON key and no new file other than this package and tests; the refusal reuses the existing `unscanned` source row (`SourceCoverage(name, "unscanned", None, reason)` built by `_failed_worktree` in `src/superclaude/cli/sweep/probes.py`).
- The owner-signed git allow-list (`ALLOWED_GIT`) may change only by the three read-only entries named in Task 2; any other allow-list change is not authorized. `ALLOWED_ORCA` and `FORBIDDEN_TOKENS` stay untouched.
- The git-status scope stays separate from the contract allow-list and the transcript scans: `_worktree_paths` and the shared `paths` list in `collect` are not filtered.
- Out of scope: `CLAUDE.md`, `tests/core/test_claude_md_worktree_rule.py`, anything under `.claude/`, wording or alignment edits, new JSON keys, sidecar files.
- Python only through UV: `uv run pytest tests/sweep -q`, `uv run ruff check`, `uv run ruff format`. Never `python -m`, bare `python`, or `pip`.
- Stage named paths only (`git add -- <paths>`, never `git add -A` or `git add .`); the plan package under `.dev/tasks/` is staged with the T2 commit. Commit locally on the current branch with conventional messages ending with the line `Co-Authored-By: Claude Code <noreply@anthropic.com>`. The executor commits only; it never pushes, opens a PR or writes to GitHub (the owner's session pushes afterwards).
- T2 (Tasks 1 to 5) and T1 (Task 6) are two separate commits. The sweep tests forbid a real subprocess unless a test carries the `integration` mark (`tests/sweep/conftest.py` autouse guard); real-git tests must carry that mark.


Start sha: 53f08dfada9b1e87d0fdb92f483f1eb8a8d18de0
Diff against the start snapshot: diff --git a/docs/designs/orchestrator-mode.md b/docs/designs/orchestrator-mode.md
index 96be24bf5..de5235221 100644
--- a/docs/designs/orchestrator-mode.md
+++ b/docs/designs/orchestrator-mode.md
@@ -41,10 +41,10 @@ Out of scope for Phase 1 (unchanged from SPEC section 2): any write verb, `/sc:c
 Decision: `--no-optional-locks` is built into the `_git` seam, so no caller can build a git argv without it. `probes._git(cwd, *args)` is the only function in the package that starts git. It builds the argv as
 
 ```
-["git", "--no-optional-locks", "-C", str(cwd), *args]
+["git", "--no-optional-locks", "-C", str(cwd), "-c", "core.fsmonitor=false", *args]
 ```
 
-and starts the child with `env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"}`. `args` must equal the single `ALLOWED_GIT` template exactly, else the seam raises `ValueError` before any process starts (exit 1). Callers pass only `cwd`; they never pass the prefix, so a missing flag cannot be expressed.
+and starts the child with `env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"}`. Fsmonitor is always off because a command named by repository configuration or the environment would otherwise run during status (issue 547). `args` must equal one of the four `ALLOWED_GIT` templates exactly, else the seam raises `ValueError` before any process starts (exit 1). Callers pass only `cwd`; they never pass the prefix, so a missing flag cannot be expressed.
 
 Ordering: this seam and its recorded-argv test (NFR-002) are the first code commit and the first test of the build (step 1.4a in section 15.2), before any other probe code. Anchors: SPEC section 15 line 552, NFR-002 (line 131), section 8 lines 282-292 and 299; GAPS line 126. The `GIT_OPTIONAL_LOCKS` variable comes from git's documentation and stays UNVERIFIED here (SPEC line 299); the flag alone carries the guarantee and the variable is belt and braces.
 
@@ -64,7 +64,7 @@ Each row takes the SPEC section 15 proposal (SPEC lines 553-563) and fixes the c
 | GQ-107 | `sanitize()` escapes `|` as `\|`, in addition to the FR-016 stripping and HTML neutralizing. The injection fixture gets one pipe case. | `report.sanitize` | SPEC FR-016 (line 110), line 560; GAPS line 130 |
 | GQ-108 | Person-started is a transcript under a scanned project key that the tab map joins to no Orca row. The join is fixed in section 7.2 (`SessionRow`) as two paths: (A) an Orca row field that holds a Claude session id, matched to the transcript `sessionId`; (B) an Orca row field that holds a pane key or terminal handle, matched to a tab-map file name or line 3, whose line 1 is the session id. Both Orca-side fields are UNVERIFIED until step 1.0a (section 17). Until 1.0a shows at least one of them, no transcript can be proved unjoined, so `person_started` is None for every unmatched transcript and those rows print could not determine with note `tab map join not observable`. This is the FR-010 completeness guard applied, not a weakening. | `probes` tab-map and transcript readers; `SessionRow.person_started` | SPEC FR-010 (line 104), line 561; GAPS line 131 |
 | GQ-109 | `gate-list`, `worker-read` and every `git stash` form are absent from both allowlists and from step 1.0a. `--include-remote` is the only forbidden token, checked in every argv; `worktree ps --agent-wait` is allowed (R5, owner 2026-11-08). | `probes.ALLOWED_ORCA`, `probes.FORBIDDEN_TOKENS` | SPEC line 562, NFR-014 (line 143); GAPS line 132 |
-| GQ-110 | Exactly one `git status --porcelain=v1 -z --branch --untracked-files=all` per worktree, parsed once into `WorktreeState`. The recorded-argv test asserts one git argv per discovered worktree. | `probes.read_worktree`, `probes.ALLOWED_GIT` | SPEC line 563, section 8 lines 325-336; GAPS line 133 |
+| GQ-110 | Exactly one `git status --porcelain=v1 -z --branch --untracked-files=all --ignore-submodules=all` per worktree, parsed once into `WorktreeState`. Before it, up to three read-only inspection calls (`config --show-origin --list -z`, then `ls-files -z` and `check-attr --stdin -z filter` only when a filter driver with a command is defined) decide whether a git filter selected by a tracked path could run a program; if so status is not run and the worktree is `unscanned` ("git filter could run a program"). Every git call runs with `-c core.fsmonitor=false` (issue 547). The recorded-argv test asserts one status argv per discovered worktree. | `probes.read_worktree`, `probes.ALLOWED_GIT` | SPEC line 563, section 8 lines 325-336; GAPS line 133 |
 
 Two details of the git parse that the SPEC left open are fixed here (M7):
 
@@ -179,7 +179,7 @@ The allowlist miss (SPEC section 11 line 447) and every collection, classificati
  |   _orca seam               RULES (9)             sanitize                         |
  |   _git seam                classify              render, SECTIONS                 |
  |   ALLOWED_ORCA (10)        policy_of             CHECKED_ORCA_VERSION             |
- |   ALLOWED_GIT (1)          package_state                                          |
+ |   ALLOWED_GIT (4)          package_state                                          |
  |   FORBIDDEN_TOKENS         mark_shared_packages                                   |
  |   Budget                   safe_to_close                                          |
  |   disk readers             classify_all                                           |
@@ -253,7 +253,8 @@ skill        commands.run            probes                 Orca / git / disk
   |              |                       |                          |                         |
   |              |== GIT READS (per worktree: root + worktree ps paths) ==                    |
   |              |                       | _git(path) status --porcelain=v1 -z --branch --untracked-files=all
-  |              |                       |   (--no-optional-locks, GIT_OPTIONAL_LOCKS=0, 10 s, Budget)
+  |              |                       |        --ignore-submodules=all (after config/ls-files/check-attr inspection)
+  |              |                       |   (--no-optional-locks, -c core.fsmonitor=false, GIT_OPTIONAL_LOCKS=0, 10 s, Budget)
   |              |                       |                          |                         |
   |              |== DISK READS =========| progress.md, .archiving, contracts, transcripts,  |
   |              |                       | orca-tabs/, Orca package.json (bounded, resolve()) |
@@ -307,8 +308,9 @@ Symbols: R selected Runs (after deduplication), D distinct Dispatch rows returne
                                                       v
                              +----- git argv, exactly W --------------------------+
                              | status --porcelain=v1 -z --branch                  |
-                             |        --untracked-files=all                       |
-                             | one per worktree, no retry                         |
+                             |  --untracked-files=all --ignore-submodules=all     |
+                             | one per worktree, no retry (a filter refusal makes |
+                             | none; up to 3 read-only inspection calls before it)|
                              +------------------------+---------------------------+
                                                       v
                              +----- disk reads (no subprocess) -------------------+
@@ -340,7 +342,7 @@ Counts that tests pin:
 | Orca argv total | at most `1 + 3R + 1 + 50`; every argv equals one template | NFR-003 recording test |
 | `worker-show` | `min(D, 50)` when time allows; 2 Runs of 40 rows get 25 each | FR-020 (60-row, 50-row, 2-Run fixtures) |
 | `worktree list`, `worktree current` | 0 in Phase 1 | NFR-003 recording test (section 7.3) |
-| git argv | exactly W, each with `--no-optional-locks` at index 1 | NFR-002, GQ-110 |
+| git status argv | exactly W (up to three read-only inspection calls precede each), each git argv with `--no-optional-locks` at index 1 | NFR-002, GQ-110 |
 | Session rows | `N = D + U` | FR-005 (3 workers, 1 person session: 4 rows) |
 | Reconciliation | `summary.total = summary.visible + summary.historical`; `summary.bound_reached <= summary.visible` | FR-005, FR-020 |
 | Lower bound | `total_is_lower_bound` is true when any list is truncated (a full 100-row page) or unscanned | FR-005, section 8 paging |
@@ -381,7 +383,7 @@ class BindingError(Exception)               # carries the exit-2 message; comman
 
 def orca_binary() -> str                                     # $ORCA_CLI_COMMAND, else "orca-ide"
 def check_orca_argv(args: tuple[str, ...]) -> None           # ValueError unless an exact template match
-def check_git_args(args: tuple[str, ...]) -> None            # ValueError unless == ALLOWED_GIT[0]
+def check_git_args(args: tuple[str, ...]) -> None            # ValueError unless args is an ALLOWED_GIT entry
 def _orca(*args: str, timeout: float) -> OrcaResult
 def _git(cwd: Path, *args: str, timeout: float) -> str       # raises GitCallFailed on nonzero, timeout, > 8 MiB
 class GitCallFailed(Exception)
@@ -539,8 +541,12 @@ ALLOWED_ORCA: tuple[tuple[str, ...], ...] = (
 FORBIDDEN_TOKENS = frozenset({"--include-remote"})   # rejected in any position
 
 ALLOWED_GIT: tuple[tuple[str, ...], ...] = (
-    ("status", "--porcelain=v1", "-z", "--branch", "--untracked-files=all"),
-)                                            # the seam prepends git --no-optional-locks -C <path>
+    ("status", "--porcelain=v1", "-z", "--branch", "--untracked-files=all",
+     "--ignore-submodules=all"),
+    ("config", "--show-origin", "--list", "-z"),
+    ("ls-files", "-z"),
+    ("check-attr", "--stdin", "-z", "filter"),
+)                                            # the seam prepends git --no-optional-locks -C <path> -c core.fsmonitor=false
 
 ORCA_VERSION_FILE = Path("/opt/Orca/resources/app.asar.unpacked/out/package.json")
 OUTPUT_LIMIT = 8 * 1024 * 1024               # subprocess stdout + stderr

=== committed so far (HEAD, to be amended with the doc fix after this review) ===
14ff732fc56918f7eb7c8b06d15d5f1c5c4aa0f2
fix(sweep): stop git calls from running repository-configured programs (issue 547)

 .dev/tasks/to-do/TASK-WF-fixIssue547InSrc-20261114-152015/TASK-WF-fixIssue547InSrc-20261114-152015.md | 108 ++++++++++++++++++++++
 .dev/tasks/to-do/TASK-WF-fixIssue547InSrc-20261114-152015/artifacts/codegraph-grounding.md            |  28 ++++++
 .dev/tasks/to-do/TASK-WF-fixIssue547InSrc-20261114-152015/artifacts/codegraph.md                      |   1 +
 .dev/tasks/to-do/TASK-WF-fixIssue547InSrc-20261114-152015/artifacts/reflect-pre/REPORT.md             |  29 ++++++
 .dev/tasks/to-do/TASK-WF-fixIssue547InSrc-20261114-152015/artifacts/t1-red.log                        |  76 ++++++++++++++++
 .dev/tasks/to-do/TASK-WF-fixIssue547InSrc-20261114-152015/artifacts/t2-green.log                      |  25 ++++++
 .dev/tasks/to-do/TASK-WF-fixIssue547InSrc-20261114-152015/artifacts/validation.md                     |  66 ++++++++++++++
 docs/designs/orchestrator-mode.md                                                                     |  18 ++--
 src/superclaude/cli/sweep/probes.py                                                                   | 109 +++++++++++++++++++---
 tests/sweep/conftest.py                                                                               |  47 +++++++---
 tests/sweep/test_git_config_hole.py                                                                   | 276 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/sweep/test_probes_allowlist.py                                                                  | 206 ++++++++++++++++++++++++++++++++++++++++--
 tests/sweep/test_readonly.py                                                                          |  18 ++--
 36 files changed, 3326 insertions(+), 39 deletions(-)
=== git status --short ===
 M docs/designs/orchestrator-mode.md
?? .dev/tasks/to-do/TASK-WF-fixIssue547InSrc-20261114-152015/artifacts/retries/T5/probe-1-1.md
?? .dev/tasks/to-do/TASK-WF-fixIssue547InSrc-20261114-152015/artifacts/retries/T5/prompt-1-1.md
?? .dev/tasks/to-do/TASK-WF-fixIssue547InSrc-20261114-152015/artifacts/retries/T5/review-1.md
=== evidence ./artifacts/t2-green.log tail ===
.............                                                            [100%]

============================= 635 passed in 4.90s ==============================

Delta diff from the previous reviewed tree (empty on the first review): diff --git a/docs/designs/orchestrator-mode.md b/docs/designs/orchestrator-mode.md
index c44966632..de5235221 100644
--- a/docs/designs/orchestrator-mode.md
+++ b/docs/designs/orchestrator-mode.md
@@ -41,10 +41,10 @@ Out of scope for Phase 1 (unchanged from SPEC section 2): any write verb, `/sc:c
 Decision: `--no-optional-locks` is built into the `_git` seam, so no caller can build a git argv without it. `probes._git(cwd, *args)` is the only function in the package that starts git. It builds the argv as
 
 ```
-["git", "--no-optional-locks", "-C", str(cwd), *args]
+["git", "--no-optional-locks", "-C", str(cwd), "-c", "core.fsmonitor=false", *args]
 ```
 
-and starts the child with `env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"}`. `args` must equal the single `ALLOWED_GIT` template exactly, else the seam raises `ValueError` before any process starts (exit 1). Callers pass only `cwd`; they never pass the prefix, so a missing flag cannot be expressed.
+and starts the child with `env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"}`. Fsmonitor is always off because a command named by repository configuration or the environment would otherwise run during status (issue 547). `args` must equal one of the four `ALLOWED_GIT` templates exactly, else the seam raises `ValueError` before any process starts (exit 1). Callers pass only `cwd`; they never pass the prefix, so a missing flag cannot be expressed.
 
 Ordering: this seam and its recorded-argv test (NFR-002) are the first code commit and the first test of the build (step 1.4a in section 15.2), before any other probe code. Anchors: SPEC section 15 line 552, NFR-002 (line 131), section 8 lines 282-292 and 299; GAPS line 126. The `GIT_OPTIONAL_LOCKS` variable comes from git's documentation and stays UNVERIFIED here (SPEC line 299); the flag alone carries the guarantee and the variable is belt and braces.
 
@@ -179,7 +179,7 @@ The allowlist miss (SPEC section 11 line 447) and every collection, classificati
  |   _orca seam               RULES (9)             sanitize                         |
  |   _git seam                classify              render, SECTIONS                 |
  |   ALLOWED_ORCA (10)        policy_of             CHECKED_ORCA_VERSION             |
- |   ALLOWED_GIT (1)          package_state                                          |
+ |   ALLOWED_GIT (4)          package_state                                          |
  |   FORBIDDEN_TOKENS         mark_shared_packages                                   |
  |   Budget                   safe_to_close                                          |
  |   disk readers             classify_all                                           |
@@ -342,7 +342,7 @@ Counts that tests pin:
 | Orca argv total | at most `1 + 3R + 1 + 50`; every argv equals one template | NFR-003 recording test |
 | `worker-show` | `min(D, 50)` when time allows; 2 Runs of 40 rows get 25 each | FR-020 (60-row, 50-row, 2-Run fixtures) |
 | `worktree list`, `worktree current` | 0 in Phase 1 | NFR-003 recording test (section 7.3) |
-| git argv | exactly W, each with `--no-optional-locks` at index 1 | NFR-002, GQ-110 |
+| git status argv | exactly W (up to three read-only inspection calls precede each), each git argv with `--no-optional-locks` at index 1 | NFR-002, GQ-110 |
 | Session rows | `N = D + U` | FR-005 (3 workers, 1 person session: 4 rows) |
 | Reconciliation | `summary.total = summary.visible + summary.historical`; `summary.bound_reached <= summary.visible` | FR-005, FR-020 |
 | Lower bound | `total_is_lower_bound` is true when any list is truncated (a full 100-row page) or unscanned | FR-005, section 8 paging |
@@ -383,7 +383,7 @@ class BindingError(Exception)               # carries the exit-2 message; comman
 
 def orca_binary() -> str                                     # $ORCA_CLI_COMMAND, else "orca-ide"
 def check_orca_argv(args: tuple[str, ...]) -> None           # ValueError unless an exact template match
-def check_git_args(args: tuple[str, ...]) -> None            # ValueError unless == ALLOWED_GIT[0]
+def check_git_args(args: tuple[str, ...]) -> None            # ValueError unless args is an ALLOWED_GIT entry
 def _orca(*args: str, timeout: float) -> OrcaResult
 def _git(cwd: Path, *args: str, timeout: float) -> str       # raises GitCallFailed on nonzero, timeout, > 8 MiB
 class GitCallFailed(Exception)

Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B2 ac=T5.AC3 at=docs/designs/orchestrator-mode.md:47 anchor=src/superclaude/cli/sweep/probes.py:243 chk=n,y,n,n family=design-doc-stale-allowlist first=A1 origin=new: section 2.1 still says one ALLOWED_GIT template and an argv without -c.
F1.2 sev=blocking trigger=B2 ac=T5.AC3 at=docs/designs/orchestrator-mode.md:386 anchor=src/superclaude/cli/sweep/probes.py:242-243 chk=n,y,n,n family=design-doc-stale-allowlist first=A1 origin=new: line 386 ValueError unless == ALLOWED_GIT[0]; line 182 ALLOWED_GIT (1).

Saved-probe re-check hit locations (may be empty): 44:["git", "--no-optional-locks", "-C", str(cwd), "-c", "core.fsmonitor=false", *args]
47:and starts the child with `env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"}`. Fsmonitor is always off because a command named by repository configuration or the
67:| GQ-110 | Exactly one `git status --porcelain=v1 -z --branch --untracked-files=all --ignore-submodules=all` per worktree, parsed once into `WorktreeState`. 
182: |   ALLOWED_GIT (4)          package_state                                          |
386:def check_git_args(args: tuple[str, ...]) -> None            # ValueError unless args is an ALLOWED_GIT entry
543:ALLOWED_GIT: tuple[tuple[str, ...], ...] = (
797:| FR-015 | `mark_shared_packages`; `--untracked-files=all` in `ALLOWED_GIT` (2.2 GQ-101, 7.3) | `sweep/test_classify.py` |
940:| 1.4a | | `probes._git`, `ALLOWED_GIT`, `check_git_args`, and `tests/sweep/test_readonly.py` with the NFR-002 recorded-argv, env and real-git tests, plus t


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
