# Round 3 — Final arguments for Variant B (analyzer; root cause and evidence for architecture)

"Verified" means I re-read the line read-only in this worktree in this round, or re-ran the behaviour in throwaway repositories under `/tmp` (git 2.47.3), all removed afterwards. Upstream pre-commit source was read from `pre-commit/pre-commit` on `main` (`pre_commit/staged_files_only.py`, `pre_commit/commands/run.py`, `pre_commit/error_handler.py`) and searched with the GitHub code search. The real pre-commit framework is not installed here, so the hook experiments emulate it with the exact git commands of `staged_files_only.py`. Nothing in the repository was changed.

## Final position

1. Structure and surface stay as agreed: a `/sc:git` command plus the `sc-git-protocol` skill with per-group refs and a mirrored read-only skill script; status (default), add, commit (`--message` or `--smart-commit`), branch list/create/switch, cleanup as a route to `/sc:worktrees`, submodule status/update/commit-pointer; no push, pull, merge or `--interactive`.
2. Between-task commits need a person-typed `--commit-tasks`, checked once in Wave 0 and recorded as a `run` line in `commits.md` that carries `ledger-lines=` and `branch=` (A's Round 3 mechanism, with three corrections below).
3. A task is eligible for a commit only when the **first** `complete` line after its current `start` was written in a flagged segment. A due boundary is prepared late only when the crash explains it; any other due boundary means a run advanced without settling it, and it is never committed.
4. **Settle before advance** (A): no `start` line, all-complete step or archive gate while a boundary is unsettled. Every unsettled state, in every run, offers the owner `abandon`, and `adopt` when its precondition holds. So no state is a dead end.
5. **The person's files outside the commit set are always recoverable.** Immediately before each commit the agent pins a full worktree snapshot (the Q0 command). After every attempt a second snapshot is compared with it, and any path outside S that changed is reported with a restore command. This replaces A's `unstaged-outside` refusal, which misses assume-unchanged files and brings back the coarse `dirty` gate.
6. An interrupted commit (timeout or signal) writes no terminal line. The next run's reconcile classifies it, so it never races a hook that is still running.
7. Hooks are never bypassed. Nothing retries automatically inside a run. The owner's `abandon` and `adopt` answers are given in chat and recorded by the executor, never written by the owner.

## Resolution of the HIGH findings

### INV-001: a completed task whose boundary was never prepared — MODIFY

**A's mechanism is right.** The ledger is append-only (`refs/ledger.md:3`), so a line count at the moment the `run` line is appended is a stable segment boundary. It survives a crash because it is written before any task of that run. My Round 2 rule relied on the Q0 pin still existing, but Row 1 deletes that pin on any resume (`refs/ledger.md:157`, verified), so I withdraw it.

**Three defects in A's text, found by checking it against the ledger rules:**

1. **"Latest complete" revives ineligible tasks.** A re-review `complete` line repeats a task's `complete` with no new `start` (`refs/ledger.md:84-86`, verified). A task first completed in an unflagged run and re-reviewed during a later flagged run would have its latest `complete` in an `on` segment. A's HR-1.2 then makes it eligible and commits it after the fact, which is against X-006 and against the agreed INV-016 rule. The anchor must be the **first** `complete` after the member's current `start`. A post-ruling `complete` written by Row R in a later run (`refs/ledger.md:158`) is still that first `complete`, so a Ruling completed in a flagged run stays eligible.
2. **"Complete `\n`-terminated lines" puts a torn line in the wrong segment.** Step 6 stops only when the last line fails every regex (`refs/ledger.md:127`). A `complete` line torn inside its `files=` field still matches `files=(.+)$`. Counting only terminated lines puts that previous-run line at position k+1, inside the new run's segment. Counting every line, terminated or not, keeps each line in the segment of the run that wrote it.
3. **Nothing tells a crash from an out-of-protocol advance.** Settle before advance means a legal due boundary can only be the last thing before a crash: no other task's `start` line can follow its members' anchors. An installed copy older than this feature (INV-011) ignores the sidecar, writes no `off` line and keeps going, so its later `complete` lines fall into the old `on` segment. A's rule would then commit all of them in the next flagged run. The fix is to check whether a later `start` line exists.

**Requirement text.**

- **HR-1.1 Segment record.** Every `run` line (the A-003 form) adds `ledger-lines=<k> branch=<git symbolic-ref -q HEAD>`. `k` is the number of lines in the ledger when the `run` line is appended, right after Wave 0 step 6: the number of `\n` bytes, plus one when the file is not empty and does not end in `\n`. The revocation line (`commit-tasks=off reason=revoked`) carries its own `ledger-lines=`. Only the executor appends `run` lines.
- **HR-1.2 Anchor and eligibility.** A member's **anchor** is the first `complete` line after that member's latest `start` line. A ledger line at position `p` belongs to the latest `run` line whose `k` is less than `p`. A boundary is **eligible** only when every member's anchor lies in an `on` segment. Lines at or before the first `run` line's `k`, and lines in an `off` segment, are never eligible. Later `complete` lines for the same `start` never create or revive a boundary.
- **HR-1.3 Due, and crash-explained.** An eligible boundary with no line for its key in `commits.md` is **due**. It is **crash-explained** when no `start` line of any task appears in the ledger after any member's anchor. A due boundary that is not crash-explained is **out-of-protocol**: it is never prepared, and the STOP names the later `start` lines it found.
- **HR-1.4 Settle before advance** (A's HR-1.4, kept). A boundary is unsettled when it is due, pending, refused (its latest line is `refused`) or uncertain. While any boundary is unsettled, no run writes a `start` line, runs the legacy all-complete FINAL or stop (`refs/ledger.md:134`, `:139`), or enters the managed archive gate (`refs/managed-workspace.md:48`). Wave 0 order: step 6, then the `run` line, then (managed) the location and `PLAN:` pin checks, then reconcile, then steps 7-9, then task selection. Reconcile runs after the pin check so that a changed plan stops with `E-PLAN-CHANGED` before anything is committed.
- **HR-1.5 Behaviour per state.**

  | State | Flagged run | Any other run |
  |---|---|---|
  | due, crash-explained | Prepare now with the Q8a checks: HEAD equals the first member's `q0-head` (`refs/retry.md:28`), the branch check (INV-002), `foreign-change`, product paths equal to the accepted tree (INV-003) | STOP `E-COMMIT-REFUSED reason=unsettled` with the HR-3 choices |
  | due, out-of-protocol | STOP `reason=out-of-protocol` with the HR-3 choices | same |
  | pending (prepared, no terminal line, HEAD = parent), or refused with HEAD = parent | A new attempt only when the product paths equal the accepted tree or the `rewritten=` tree that the refusal showed. Otherwise append `refused reason=candidate-changed` and STOP with the choices | STOP `reason=unsettled` with the choices |
  | refused with HEAD ≠ parent | STOP with the choices | same |
  | uncertain | STOP `reason=uncertain` with the choices | same |
  | settled (`sha=`, `recovered`, `skipped`, `resolved`) | nothing | nothing |

  Two transient states write no line and only STOP with `E-RESUME-NEEDED`. `reason=index-locked` applies when `git rev-parse --git-path index.lock` exists. `reason=commit-interrupted` is HR-2.4.
- **HR-1.6 Pin lifetime.** The Q0 pin, the accepted pin and both boundary pins (`boundary/<hex12>` for the frozen candidate, `boundary-wt/<hex12>` for the worktree snapshot) stay until the boundary's settling line. The reviewed-tree refs can still be deleted at `complete` as today (`SKILL.md:129`), because the accepted pin holds the one tree the boundary needs. The Q7 cleanup and Row 1 are amended to that effect. The worktree pin's name is a sibling, not a child, of the candidate pin. Verified: with `refs/.../boundary/abc` present, `git update-ref refs/.../boundary/abc/wt` exits 128 ("'…/boundary/abc' exists; cannot create").
- **HR-1.7 Validation.** The helper refuses `sidecar-mismatch` in three cases: the `ledger-lines` values decrease between `run` lines, a value exceeds the ledger's current line count, or a `run` line's position contradicts its own `ledger-lines` value. An unparseable last sidecar line STOPs `E-COMMIT-REFUSED reason=sidecar-corrupt`. Like `E-LEDGER-CORRUPT` today (`SKILL.md:72`), it is the one unsettled state a person must repair by hand. This is a stated residual, not something the owner is asked to write as a record.
- **HR-1.8 Tests.**
  - A's (a)-(e).
  - (f) A task completed in an unflagged run, then re-reviewed during a flagged run, is not committed.
  - (g) A due boundary followed by another task's `start` line (written as an old copy would) STOPs `out-of-protocol` and is never committed.
  - (h) A ledger whose last line lacks `\n` at a flagged resume: that line is counted in the earlier segment.
  - (i) A managed resume with a changed plan stops `E-PLAN-CHANGED` before reconcile prepares anything.

### INV-021: an interrupted hook can lose the person's unstaged edits — MODIFY

**A's account of the framework holds.** I checked it independently:
- `run.py` enters `staged_files_only(store.directory)` and calls `install_hook_envs` inside that context. So a first-time environment install happens while the person's edits are set aside.
- `_unstaged_changes_cleared` runs `git write-tree` on the hook's index, then `git diff-index --ignore-submodules --binary … <tree> --` against the worktree. It saves the patch as `patch<time>-<pid>`, runs `git -c submodule.recurse=0 checkout -- .`, and re-applies the patch only in `finally`.
- `error_handler.py` catches only `Exception` and `KeyboardInterrupt`. A code search of the repository for `SIGTERM` returns nothing, and `signal` matches only an R template, the changelog and an xargs test. Python's default action for SIGTERM ends the process without running `finally`. So SIGTERM loses the edits just as SIGKILL does. This settles A's UNVERIFIED point, as of `main`.

**Experiments** (`/tmp`, git 2.47.3, a hook running the same commands). Outside S there were an unstaged edit `b`, a staged edit `c`, a `--skip-worktree` edit `s` and an `--assume-unchanged` edit `u`.

| Run | Result |
|---|---|
| R1, uninterrupted, `git commit --only -- a` | The hook stashed `b c`. After the commit: `b=b1 c=c1 s=s1`, but `u=u0`. The assume-unchanged edit was overwritten by the `checkout -- .` and was never in the patch. It was lost without any interruption. |
| R2, uninterrupted, plain `git commit` | Same: `u=u0`. The loss is the framework's, not caused by `--only`. |
| R3, SIGTERM to the commit's process group during the hook | git exit 143. Locks removed. `b=b0 c=c0 u=u0`, with `c` intact in the index. Nothing was restored. |
| R4, SIGKILL to the process group | git exit 137. `index.lock` and `next-index-<pid>.lock` left behind. Same worktree loss. |
| SIGTERM to git alone | git exit 143 with locks removed. The orphaned hook kept running and re-applied its patch 3 seconds later. |
| Recovery | In R3 and R4, `git restore --source=<snapshot pin> -- b u` and `git checkout -- c` restored every edit byte for byte. |

**Holes in A's `unstaged-outside` refusal.**
1. It misses assume-unchanged files. `git diff --name-only` on the real index listed only `a b`; `u` was invisible (`git ls-files -v` showed `h u`). Yet the hook's checkout overwrote `u` even in the normal path (R1).
2. It runs as a separate Bash call before the commit, so an edit saved in that window is unprotected.
3. It brings back, at every boundary, the coarse `dirty` gate that all three variants dropped in Round 2. Any unstaged tracked edit anywhere refuses every boundary, including an edit a test run makes to a lock file.
4. It runs after `git add`, so a refusal leaves S and `.dev/tasks` staged in the person's index.

**Root cause.** Hook managers move worktree content to a place outside git while hooks run, and an interruption, or a flag the manager cannot see, leaves it there. The fix that follows from the cause: before the commit, make sure every byte in the worktree also exists in a pinned git object; after the commit, check that nothing outside S changed. Q0 already takes exactly this snapshot for every task (`SKILL.md:124-126`, verified). The snapshot's private index is built from `read-tree HEAD`, so index flags cannot hide anything from it. That is why it captured `u=u1` and `git diff` could not.

**Requirement text.**

- **HR-2.1 Worktree snapshot before the commit.**
  - Timing: after the boundary's `git add` calls and immediately before its `git commit`.
  - Command: the agent runs the Q0 snapshot command (`SKILL.md:124`): private index, `read-tree HEAD`, `add -A`, `write-tree`.
  - Pin: a literal `git update-ref refs/superclaude/implement/<slug>/boundary-wt/<hex12> <tree>`.
  - If the snapshot or the pin fails: append `refused reason=snapshot-failed` and make no commit.
- **HR-2.2 Outside-S check after every attempt.**
  - `verify`, or the next run's reconcile for an interrupted attempt, takes a second snapshot the same way.
  - The helper lists `git diff --name-status <before> <after>` for paths outside S.
  - If the list is not empty: the terminal line gains `outside-changed=<n>`, and the report prints up to 20 entries with `git restore --source=refs/superclaude/implement/<slug>/boundary-wt/<hex12> -- <paths>` and the warning "compare first: this overwrites any newer edit".
  - In that case the pin is kept after the settling line, and the final summary lists it with its `git update-ref -d` line.
  - Nothing is restored automatically.
- **HR-2.3 Timeout.** The commit call uses the Bash tool's maximum, 600000 ms (A). C's 120-second limit is rejected, because hook environments install inside the stash. With HR-2.1 in place, the timeout affects only how often an attempt is interrupted, not data safety. Workers never run this step (`WORKER-CONTRACT.md:43`: "A command's own commit step stays off under `--unattended`"), so WC-10's four-minute split (`:46`) does not apply.
- **HR-2.4 Interrupted attempt.**
  - Trigger: the tool reports a timeout, or git exits with a status above 128.
  - `verify` writes no terminal line. It STOPs `E-RESUME-NEEDED reason=commit-interrupted`, prints the HR-2.2 list, and says: "check that no git or hook process is still running in this worktree before restoring anything or re-running."
  - Reason: an orphaned hook can still rewrite the worktree seconds later (experiment above), so a same-run classification would race it. The next run's reconcile classifies the `prepared` boundary as recovered, pending or uncertain (C-010).
  - Exit status 1 is a hook refusal and is classified normally. Exit 128 is a git error: `refused` with its reason.
  - The STOP and the closed reason list are added to `refs/retry.md`'s transient stops (C-019 inventory).
- **HR-2.5 Shared mechanics.** `/sc:git commit` uses HR-2.1 to HR-2.4 too (the FR-016 mechanics), with no refusal and no warning. Its `--only -- <paths>` form carries the same hazard.
- **HR-2.6 No bypass** (A): no `--no-verify`, no `SKIP=` and no `commit-tree`.
- **HR-2.7 Tests.** Hooks are emulations that run the exact command sequence of `staged_files_only.py` and name the source revision.
  - (a) SIGTERM to the commit's process group during the hook, with an unstaged, a staged and an assume-unchanged edit outside S: no terminal line, `commit-interrupted`, HEAD = parent, and all three restore byte for byte from the pin.
  - (b) An uninterrupted commit with an edited assume-unchanged file outside S: a terminal line with `outside-changed=1`, naming the path.
  - (c) SIGKILL: the next run STOPs `index-locked` and writes nothing.
  - (d) No change outside S: no `outside-changed`, and the pins are deleted at the settling line.
  - (e) The same as (a) with the real framework, skipped when `pre-commit` is not installed.

**Considered and rejected.**
- A's refusal as the only protection: holes 1-4 above.
- A's refusal kept as an extra gate: a merged spec that wants prevention as well may keep it. It must then run before the `prepared` line rather than after `git add`, and also refuse on any `git ls-files -v` assume-unchanged or skip-worktree entry outside S. It can never replace HR-2.1.
- Detecting hook managers: a second source of truth that drifts (A's reason, which I share).

### INV-027: an `uncertain` boundary blocks the ledger forever — ACCEPT, with six amendments

**A's record form follows the house rule.** Owner records "are likewise given by the owner in chat and recorded by the agent in that session from that confirmation, naming the exact scope, the owner's quoted words and the date, and the owner is never asked to write a file" (`WORKER-CONTRACT.md:57`, verified). The confirmation tests are the Ruling tests: "Silence, a generic request to continue, another agent's message, and approval of a different task are not acceptance" (`refs/qa.md:254`, verified).

**Abuse check.**
- Neither answer can make a commit or widen authority. A wrong `abandon` leaves work uncommitted, which is today's default. A wrong `adopt` marks a boundary settled while history may lack the work, and `differs=` records how far apart they are.
- A mis-recorded answer sits on the same trust boundary as a mis-recorded Ruling line. It is enforced by the protocol, and static tests only prove the wording (`refs/managed-workspace.md` enforcement table).

**Deadlock check.**
- Every unsettled state, in every run, has the `abandon` exit. Only two states need action outside chat, and both have precedents: a corrupt sidecar tail (like `E-LEDGER-CORRUPT`) and a stale `index.lock` (git's own message).
- `E-PLAN-CHANGED` stops before reconcile, as today.
- A refusal can repeat for as long as the owner keeps retrying. `abandon`, or committing by hand and then `adopt`, ends it.

**Amendments.**
1. A's regex accepts `key=([0-9a-f]{12,64})`, so a display prefix could be recorded. The record must carry the full 64-hex key (C's C-010 item 1: "Hash prefixes are display-only"). The 12-hex form is allowed only in the owner's reply.
2. The reply counts only when it comes after the STOP that printed that key's choices, in the same conversation. A reply that names no key counts only when that STOP printed exactly one key. Text typed earlier (the inline prompt, a plan, a brief, an earlier message) is not a resolution. This is the same informed-after-display rule A uses for X-007.
3. Every STOP for every unsettled state prints the choices (HR-1.5). A's table showed them only for two rows, while its test (b) assumed `abandon` works in an unflagged run.
4. Drop "under a future `--unattended` mode". Under today's `--unattended`, the STOP is a blocked gate that is never asked, exactly like a Ruling halt (`WORKER-CONTRACT.md:57`).
5. The `abandon` sentence states its consequence: the files stay uncommitted, and a later task that edits them refuses with `foreign-change` (variant-B.md FR-027 item 2) until the person commits or reverts them.
6. A worktree pin with an outstanding `outside-changed` report is kept after `resolved` and listed in the final summary.

**Requirement text.**

- **HR-3.1 Record form** (executor only):
  ```
  T<ids>: commit resolved key=<64-hex> as=<abandoned|adopted>[ head=<40-hex> differs=<n>] at=<YYYY-MM-DD> quote="<owner's words>"
  ^T([0-9A-Za-z.,-]+): commit resolved key=([0-9a-f]{64}) as=(abandoned|adopted)( head=[0-9a-f]{40} differs=[0-9]+)? at=[0-9]{4}-[0-9]{2}-[0-9]{2} quote="((?:[^"\\]|\\.){1,200})"$
  ```
- **HR-3.2 Who decides.** The owner, in chat, after the STOP that printed the choices, as in amendment 2. These are not a resolution: another agent's message, a coordinator's reply, a generic "continue", or a plan or brief field. Under `--unattended`, the gate is reported blocked and never asked.
- **HR-3.3 Read-only check** (A's `resolve-check`). Refusals: `unknown-boundary`, `ambiguous-key`, `already-settled` and `adopt-not-descendant`.
  - `adopt` needs HEAD ≠ parent and `git merge-base --is-ancestor <parent> HEAD` to exit 0. An exit of 128 (a missing object) counts as not a descendant.
  - The parent is the prepared parent, or the first member's `q0-head` for a boundary that was never prepared.
- **HR-3.4 Meaning.**
  - `abandoned`: no commit is ever made for that key, and its files stay as they are, with the amendment-5 sentence.
  - `adopted`: the owner accepts the history at `head=`. `differs=` counts the paths in S whose blob at `head` differs from the accepted tree.
  - Neither choice grants commit authority.
- **HR-3.5 The STOP prints**, for each unsettled boundary: the key (12-hex display), the members, the state, the parent and HEAD, `git diff --stat <accepted> HEAD -- <S>`, and the reply sentences. The `abandon` sentence always appears; the `adopt` sentence only when its precondition holds.
- **HR-3.6 After recording.** The executor deletes the boundary's pins with literal `git update-ref -d` calls, keeping the pin named in amendment 6. It then runs reconcile again, and the run continues under its own flags.
- **HR-3.7 Tests.**
  - A's (a)-(e).
  - (f) A reply typed before the STOP is not a resolution.
  - (g) A table-driven test that every unsettled state, in a flagged and in an unflagged run, prints `abandon`.
  - (h) A recorded key shorter than 64 hex fails the regex.

## Ruling on the other 19 findings

| Finding | Ruling | Requirement, residual or evidence (disagreement with A in bold) |
|---|---|---|
| INV-002 | ACCEPT-FIX | Prepare refuses `branch-changed` when `git symbolic-ref -q HEAD` differs from the `branch=` of the `run` line in force when the first member's `start` was written. When no `run` line was in force then, the boundary's own segment's `run` line is used. The `prepared` line repeats the branch. **A compared only with the latest `run` line, which a resume on another branch at the same commit rewrites.** |
| INV-003 | ACCEPT-FIX | The accepted tree is pinned at `complete` as `refs/superclaude/implement/<slug>/accepted/T<id>`. For a compliant `complete`, the pin points at the tree on the header of the review that gave the verdict (`refs/qa.md:178`). For a post-ruling `complete`, it points at a fresh snapshot, because a Ruling "accepts the tree as it stands" (`refs/retry.md:504`). If the start is not a tree (`tree=none`, `refs/qa.md:182`), the boundary refuses `no-snapshot`. **A pinned the worktree at `complete` for compliant tasks too. That freezes Q6 output into the accepted tree, so INV-025's refusal could never be retried.** |
| INV-004 | ACCEPT-FIX | Retries and late preparation compare only the product paths with the accepted tree or the disclosed `rewritten=` tree. Package evidence is always taken fresh, so the `codegraph.md` line each run appends (`SKILL.md:79`) never blocks a retry. Reconcile runs before steps 7-9 and after the managed pin check (HR-1.4). |
| INV-007 | ACCEPT-FIX | A `files=` path missing from the worktree but present in the index or HEAD is a deletion and is staged. Only a path missing from all three is `skipped why=absent`. With the flag on, Q1's touched set (`SKILL.md:132`) names deleted paths and both ends of a rename. My Round 2 A-001 reason was wrong. |
| INV-008 | ACCEPT-FIX | Any path equal to, or under, a mode-160000 entry of HEAD or the index (prefix match on `<path>/`) is `skipped why=gitlink` before the add. |
| INV-009 | ACCEPT-FIX | `update` checks `git -C <path> cat-file -e <gitlink>^{commit}`. If the object is missing, the state is `target-not-local`, which updates (with the fetch disclosed) only when the module is clean and its HEAD is on a local or remote-tracking branch. An `--is-ancestor` exit of 128 is never read as "diverged". Fast-forward-only was a stand-in for the real rule, "orphan no commit", and this states that rule directly. |
| INV-010 | ACCEPT-FIX | For an uninitialized module, `update` prints the `.gitmodules` URL and runs only when the typed line repeats it as `--url <url>`, byte for byte. An initialized module whose URL differs refuses `remote-mismatch` and prints `git submodule sync -- <path>` for the person to run. |
| INV-011 | ACCEPT-RISK | Verified: Wave 0 has no unknown-option STOP (`SKILL.md:57-59`). An old copy that ignores the flag makes no commit, which fails safe. The first Wave 0 line prints `commit-tasks=on run=<n>`, and the summary prints the commit count. HR-1.3 (`out-of-protocol`) also stops an old copy's later tasks from being committed after the fact. Installed old copies cannot be fixed. |
| INV-012 | ACCEPT-FIX | Every add and commit passes paths with `git --literal-pathspecs … --pathspec-from-file=<temporary file outside the tree> --pathspec-file-nul`. The guard's `( \|/git-\| git-)(merge\|pull) ` classifier (`launch-level-guard.sh:595-596`, verified) then never sees a path. To keep X-008's visibility, the prepare step prints the path list before the commit. |
| INV-014 | ACCEPT-FIX | A batch boundary is eligible only when every member's anchor is eligible. Otherwise it gets the settling line `skipped reason=mixed-authorization`, and the summary lists the batch's files. Membership is the overlapping-window set (`refs/retry.md:40`, verified). |
| INV-015 | ACCEPT-FIX | The 72-character limit counts Unicode code points of the decoded header, with no normalization. Drafting cuts at the last space at or before code point 72, and the helper counts the same way. |
| INV-018 | ACCEPT-FIX | A `files=` entry that is a directory refuses `directory-entry`. The package directory is expanded with `git ls-files -z --cached --others --exclude-standard -- <pkg-dir>` into the pathspec file. Residual: a file a person adds inside the package is committed with it. The package has one owner, and `git add .dev/tasks` stages that file anyway. |
| INV-020 | ACCEPT-FIX | Verified: `end-of-file-fixer`, `mixed-line-ending --fix=lf` and `--maxkb=1000` apply to package evidence (`.pre-commit-config.yaml:17-36`). A rewrite that touches only evidence is `hook-rewrite-evidence`, and the next flagged run retries it with fresh evidence and no product re-review. A file over the size limit is `hook-failed`, with the file named. Residual: one STOP per affected boundary where these hooks are installed; none are installed in this clone. Owner follow-up: exclude `^\.dev/tasks/.*/artifacts/` from the fixers. |
| INV-022 | ACCEPT-FIX | Settle before advance (HR-1.4): no task starts while a boundary is unsettled, and retries happen only in reconcile, so HEAD never moves under an open task. Test: an unflagged run after a refusal STOPs before task selection. |
| INV-023 | ACCEPT-FIX | Archive gate step 1 also STOPs `E-ARCHIVE-BLOCKED reason=unsettled-boundary`, as a second line of defence behind HR-1.4. |
| INV-024 | ACCEPT-FIX | `/sc:git commit` never widens the person's commit. With paths named, it stages them plus `.dev/tasks` and commits `--only` the named paths. With no paths named, it commits the index as the person staged it and runs `git add .dev/tasks` **after** the commit. It warns when the staged set holds a `commits.md` with an unsettled boundary. **A kept "stages `.dev/tasks`" with no order. My own FR-016 step 3 (variant-B.md) staged it before the commit, which puts every package into a no-path commit.** |
| INV-025 | ACCEPT-FIX | At prepare, the product paths must equal the accepted tree (INV-003). If Q6 extras rewrote a reviewed file, the boundary refuses `changed-after-review`, names the paths and prints `git restore --source=refs/superclaude/implement/<slug>/accepted/T<id> -- <paths>`. A later flagged run proceeds once the paths match again. |
| INV-029 | ACCEPT-RISK | Verified: no pre-commit hook is installed here. The boundary adds no new kind of exposure, because `.dev/tasks` is already committed by the person's commits and by the WC-9 worker commit (`WORKER-CONTRACT.md:43`), and nothing pushes. Drop C's "stop if evidence would expose secrets" claim, since nothing can detect that. |
| INV-030 | ACCEPT-FIX | Containment is checked only against the remote-tracking refs of the submodule remote whose `remote.<r>.url` equals the `.gitmodules` URL. If there is no such remote, the pointer commit refuses `submodule-unpublished reason=no-gitmodules-remote`. |

## Final concessions

1. **INV-001.** My Round 2 eligibility rule depended on pins that an unflagged resume deletes (my own E7). A's `ledger-lines` segments are the right mechanism; my changes to it are corrections.
2. **INV-006 and C-009.** My E1 success check compared the committed sidecar with the working-tree sidecar. A resume appends a `run` line first, so that check fails exactly when the commit was right (C's N2). C's frozen full-candidate test replaces it, and my C-009 vote moves from B to HYBRID.
3. **Unflagged runs.** My Round 2 C-010 item 5 ("an unflagged run prints the pending boundary and leaves it alone") was unsafe (INV-022, INV-023). Settle before advance replaces it.
4. **A-001.** My Round 2 reason, skip every absent path, drops real deletions (INV-007).
5. **INV-024.** My FR-016 shared step 3 staged `.dev/tasks` before every `/sc:git commit`. The order is fixed above.
6. **X-013.** Fast-forward-only was a stand-in. The real rule is "orphan no commit" (INV-009, A's fix).
7. **HR-2.3.** A is right that the timeout must be the tool's maximum, not C's 120 seconds.

## Per-point votes

| Point | Winner | Confidence | Reason |
|---|---|---|---|
| S-001 | A | 55 | Balanced density with verified citations; B's 522 lines repeat evidence; C omits test-pinned facts. |
| S-002 | B | 65 | Resolve column ties each alias to a repository file; A overloads `<pkg>`; C's single letters are opaque. |
| S-003 | HYBRID | 60 | A's verified baseline-facts table plus B's root causes: facts state what holds, causes explain the constraints. |
| S-004 | A | 50 | Gapped blocks absorb inserts; low stakes because the merged spec renumbers anyway. |
| S-005 | HYBRID | 70 | A's per-behaviour tests, B's existing-tests inventory, C's fault points, plus emulated-hook interruption and segment tests. |
| S-006 | HYBRID | 60 | B's runnable shell observations, each mapped to A's test ids; C's prose criteria cannot be run. |
| S-007 | B | 55 | Root-cause column ties each mitigation to its cause; otherwise the three tables are comparable. |
| S-008 | HYBRID | 75 | B's mirrored read-only skill script; A's module split, rules constants, contract version; C's closed outcome fields. |
| S-009 | HYBRID | 60 | A's registry, per-group refs and shared safety ref; B's rule that read operations load no ref. |
| S-010 | B | 60 | A distinct `refs/commit-step.md` avoids two different `refs/commit.md` files in two skills. |
| S-011 | HYBRID | 80 | B's sidecar; C's prepared line and frozen candidate; A's `ledger-lines` run lines; owner `resolved` lines; sibling worktree pin. |
| S-012 | A | 55 | D7 (merge removed) and D8 (package-only commit) settle the seed's two hardest tensions explicitly. |
| S-013 | HYBRID | 55 | A's single-source and version NFRs, B's size budgets, C's integrity, bounded execution and honest trust boundary. |
| C-001 | A | 60 | Today's advertised surface (`git.md:14`, `:17`) minus push, pull, merge, plus three submodule operations. |
| C-002 | A | 55 | `--message` gives the person's own words a one-turn path; `commit` without `--smart-commit` has no source today. |
| C-003 | B | 60 | Person-typed prefix plus a refusal that prints no replayable argv; A conceded its dry run. |
| C-004 | HYBRID | 70 | B's person-origin check once at Wave 0 is primary; A's static string test catches templates inserting the flag. |
| C-005 | HYBRID | 70 | A's Q8a, R0, L0 positions; reconcile after the managed pin check, before steps 7-9; settle before advance. |
| C-006 | HYBRID | 65 | A's before-step-6 placement minus `dirty`; B's `helper-missing`; per-path checks and branch recorded at the boundary. |
| C-007 | A | 60 | Two codes keep STOP columns single-valued; `commit-interrupted` and `index-locked` are transient `E-RESUME-NEEDED` reasons. |
| C-008 | HYBRID | 75 | B's per-path `foreign-change`; accepted tree from the compliant review or Ruling-time snapshot; worktree pin for outside-S paths. |
| C-009 | HYBRID | 80 | B's committed-tree comparison in C's frozen full-candidate form; B's own sidecar-blob check fails after a resume. |
| C-010 | HYBRID | 85 | C's prepared line, key, frozen check; B's pins; A's segments anchored on first complete; settle before advance; owner resolution. |
| C-011 | B | 70 | Keep Q0, accepted and boundary pins until the settling line; amend Row 1 and the Q7 cleanup. |
| C-012 | HYBRID | 60 | A's ten types and verdict trailer; 72 Unicode code points; B's `Implement-Plan:`; C's boundary-key trailer. |
| C-013 | B | 60 | Temporary message file outside the tree; A's in-package file would enter the next boundary commit. |
| C-014 | HYBRID | 65 | C's independent fields with unset versus false; A's single action state derived by fixed precedence. |
| C-015 | HYBRID | 65 | B's clean module; containment only against the `.gitmodules` remote; C's post-commit gitlink check; one-path set. |
| C-016 | C | 60 | Routes to `/sc:worktrees` and notes `archive` writes without `--apply`; no extra operation needed. |
| C-017 | HYBRID | 65 | Fixed set plus `origin/HEAD` per repository; a notice, not a block, when unset; `origin/HEAD` only adds names. |
| C-018 | HYBRID | 60 | B's preconditions, argv, result and undo hint plus C's statement of what HEAD, index and worktree did. |
| C-019 | HYBRID | 70 | A's routing and fixtures, B's write rows; amend `refs/retry.md:504`, Row 1, Q7 cleanup, archive gate, transient reasons. |
| C-020 | B | 70 | The plugin build copies only the plugin tree; a mirrored skill script ships everywhere, with `helper-missing`. |
| C-021 | C | 85 | `--literal-pathspecs` with `--pathspec-from-file` keeps paths literal and out of the guard's text; refuse ledger-unrepresentable names. |
| X-001 | HYBRID | 80 | Flag (A, B); person-origin check at Wave 0 (B); static scope test (A); run record and revocation (C). |
| X-002 | A | 90 | The seed forbids merge in `/sc:git`; A removes it and rewrites the routing row; B conceded. |
| X-003 | A | 75 | Fixture `:327` lists only `--smart-commit`; `--interactive`'s only example is the merge; B's reason was false. |
| X-004 | B | 75 | Sidecar leaves the resume regex and archive parser untouched; the archive digest covers only plan, source, `files=` paths. |
| X-005 | A | 70 | Stage all `.dev/tasks`, commit only the run's package expanded to literal files, as WC-9 stages then commits `--only`. |
| X-006 | B | 75 | No retroactive commits; `ledger-lines` segments anchored on each member's first complete make it computable after a crash. |
| X-007 | HYBRID | 65 | Never automatic; refusal pins and prints the rewritten tree; only a later flagged run commits that disclosed tree. |
| X-008 | HYBRID | 80 | Agent runs literal git writes the guard sees; helper read-only; path list printed before the commit; separate verify. |
| X-009 | A | 60 | Branch management is advertised today (`git.md:17`); clean-tree and no-force guards keep the risk low. |
| X-010 | C | 60 | Defaulting to read-only status is harmless; unknown operations still stop. |
| X-011 | A | 55 | The seed names the guide, whose lists hold `moderate` and `version-control`; practice drift is a follow-up. |
| X-012 | A | 65 | One non-nested submodule; report nested ones as not inspected; never recursive. |
| X-013 | HYBRID | 70 | B's intent, orphan no commit; a gitlink not yet fetched (exit 128) is `target-not-local`, updated only when nothing orphans. |
| X-014 | B | 65 | No downstream publication gate; refusal errs safe; containment only against the `.gitmodules` remote; last-fetch time printed. |
| X-015 | HYBRID | 65 | B and C admit the clone's network effect; the typed line repeats the `.gitmodules` URL; a sync hint for mismatches. |
| X-016 | A | 85 | Preflight before step 6 fits "no ledger writes"; B contradicted `SKILL.md:72` and conceded. |
| X-017 | HYBRID | 65 | Keep B's private-index trees; object writes only, as Q0 does; every pin is a literal `update-ref` by the agent. |
| X-018 | A | 75 | A plain total check of 72 Unicode code points; B's regex tail bound admits 81. |
| X-019 | B | 80 | `<pkg-dir>` names the task package; A overloads `<pkg>`. |
| X-020 | B | 85 | Verified: no pre-commit or commit-msg hook installed, hooksPath unset; the helper must validate the header itself. |
| X-021 | NONE | 80 | All misstate the tracked files (a cache yaml is tracked); correct the fact, keep settings-only automatic staging. |
| A-001 | NONE | 80 | Missing from the worktree but in the index or HEAD is a deletion to stage; skip only when missing from all three. |
| A-002 | HYBRID | 65 | All three right today: the FINAL reads current files (`refs/qa.md:311`); add a test that pins it. |
| A-003 | HYBRID | 80 | Person check once at Wave 0; bounded run line after step 6 with `ledger-lines` and `branch`; revocation; resume needs the flag. |
| A-004 | HYBRID | 60 | Never claim freshness: B's refusal errs safe; print last-fetch time (C's honesty); no fetch. |
| A-005 | NONE | 85 | Verified: the framework stashes every path outside S and ignores SIGTERM; fixed by the worktree pin and outside-S check. |
| A-006 | HYBRID | 65 | All three right: no test pins the K3 wording; still run worker-contract regressions. |
