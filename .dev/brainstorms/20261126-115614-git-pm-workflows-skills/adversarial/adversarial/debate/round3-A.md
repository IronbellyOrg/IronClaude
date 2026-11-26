# Round 3 — Final arguments for Variant A (architect; maintainability and extension scaffolding)

"Verified" means I re-read the line read-only in this worktree in this round, or re-ran the behaviour in a throwaway repository under `/tmp` (git 2.47.3, removed afterwards). Upstream pre-commit source was read from `pre-commit/pre-commit` (`main` branch: `pre_commit/staged_files_only.py`, `pre_commit/commands/run.py`, `pre_commit/commands/hook_impl.py`, `pre_commit/error_handler.py`). Nothing in the repository was changed.

## Final position

1. Structure stays as agreed: `/sc:git` is a command file plus the `sc-git-protocol` skill with per-group refs and a mirrored, read-only skill script. Operations: status (the default), add, commit (`--message` or `--smart-commit`), branch list/create/switch, cleanup as a route to `/sc:worktrees`, and submodule status/update/commit-pointer. There is no push, pull, merge or `--interactive`.
2. Between-task commits need a person-typed `--commit-tasks`, recorded in `run` lines in `commits.md`. Each `run` line now carries `ledger-lines=` and `branch=`, so "completed in a flagged run" can be computed from the files after a crash instead of from memory.
3. One new invariant closes all three HIGH findings: **settle before advance**. No run starts a task, runs the all-complete step or enters the archive gate while any boundary is unsettled. A flagged run settles a boundary by preparing or retrying it. Any other run STOPs and shows the owner two choices, `abandon` or `adopt`. The owner gives the choice in chat and the executor records it as a `resolved` line. The owner never edits a file.
4. Boundary safety:
   - At `complete`, the executor pins the accepted tree of the task.
   - The product paths must equal that accepted tree, or the hook-rewritten tree that an earlier refusal showed the person.
   - Package evidence is always re-read fresh.
   - Success is checked with C's frozen-candidate test.
   - A per-boundary `unstaged-outside` refusal ensures that a hook manager's stash can only hold content that the index also holds.
   - Paths go to git through `--pathspec-from-file`, run under `--literal-pathspecs`.
5. Hooks are never bypassed. The commit call uses the Bash tool's maximum timeout. Nothing retries automatically inside a run.
6. Submodules are handled one level deep. `update` runs when it orphans no commit. The pointer-commit containment check looks only at the remote whose URL equals the `.gitmodules` URL.

## Resolution of the HIGH findings

### INV-001: a completed task whose boundary was never prepared

**Check against the repository: the finding is correct.**
- Ledger lines carry no time and no run marker. The start line is `T<id>: start sha=…` and the verdict line has no run field (`refs/ledger.md:33-58`).
- The ledger is append-only (`:3`), and resume Row 1 deletes the Q0 pin and the `r<k>-<j>` refs on every resume, flagged or not (`:157`).
- A's own `COMMIT: on` ordering was dropped in Round 2. Without a replacement, the boundary of a task that completed in the crash window cannot be found.

**Requirement text.**

- **HR-1.1 Segment record.** Every `run` line in `commits.md` (the A-003 form) adds `ledger-lines=<k>`. `k` is the number of complete `\n`-terminated ledger lines at the moment the `run` line is appended, which is right after Wave 0 step 6. A torn last line already stops at step 6 with `E-LEDGER-CORRUPT` (`SKILL.md:72`), so `k` counts whole lines only. A revocation line (`commit-tasks=off reason=revoked`) carries its own `ledger-lines=`. Only the executor appends `run` lines.
- **HR-1.2 Eligibility.** The `run` lines divide the ledger into segments. A ledger line at 1-based position `p` belongs to the latest `run` line whose `k` is less than `p`. A boundary is **eligible** only when, for every member, the latest `complete` line for that member's current `start` lies in an `on` segment. Lines at or before the first `run` line's `k`, and lines in an `off` segment, are never eligible (X-006).
- **HR-1.3 Due state.** An eligible boundary with no line for its key in `commits.md` is **due**. Reconcile computes due boundaries from the ledger and the sidecar only.
- **HR-1.4 Settle before advance** (also closes INV-022, INV-023 and INV-027).
  - A boundary is **unsettled** when it is due, pending, refused (its latest line is `refused`) or uncertain.
  - While any boundary is unsettled, no run writes a `start` line, runs the legacy all-complete FINAL or stop (`refs/ledger.md:134`, `:139`), or enters the managed archive gate (`refs/managed-workspace.md:48`).
  - Order in Wave 0: step 6, then the `run` line, then reconcile, then steps 7-9, then task selection.
- **HR-1.5 Behaviour per state.**

  | State | Flagged run | Any other run |
  |---|---|---|
  | due | Prepare the boundary now, with the Q8a checks: HEAD equals the first member's `<retries>/T<id>/q0-head`, the branch (INV-002), `foreign-change`, the accepted tree (INV-003) and `unstaged-outside` (HR-2.1) | STOP `E-COMMIT-REFUSED reason=unsettled` |
  | pending (HEAD = prepared parent), or refused with HEAD = parent | Start a new attempt only if the product paths equal the accepted pin or the `rewritten=` tree that the refusal showed. Otherwise append `refused reason=candidate-changed` and STOP | STOP `reason=unsettled` |
  | refused with HEAD ≠ parent (for example `hook-rewrite-committed`, `head-moved`) | STOP with the HR-3 choices | STOP with the HR-3 choices |
  | uncertain | STOP `reason=uncertain` with the HR-3 choices | same |
  | settled (`sha=`, `recovered`, `skipped`, `resolved`) | nothing | nothing |

  Every STOP prints each unsettled key with its members, state, parent and HEAD. It writes nothing except the `run` line, and a `recovered` or `uncertain` line when reconcile finds one.
- **HR-1.6 Pin lifetime.** The Q0 pin, the accepted pin (INV-003), the reviewed-tree refs and the boundary pin of every task in an unsettled boundary are deleted only after that boundary's settling line. The Q7 cleanup (`SKILL.md:129`) and Row 1 (`refs/ledger.md:157`) are amended to say so.
- **HR-1.7 Validation.** The helper refuses with `E-COMMIT-REFUSED reason=sidecar-mismatch` in two cases: the `ledger-lines` values decrease from one `run` line to the next, or a value exceeds the ledger's current line count (for example, the ledger was replaced).
- **HR-1.8 Tests.**
  - (a) Crash after the Q7 `complete` flush and before `prepared`, then a flagged resume: exactly one commit, and its product paths equal the accepted pin.
  - (b) The same crash, then an unflagged resume: STOP `reason=unsettled`, no pin deleted, no new `start` line.
  - (c) A task completed in an unflagged segment between two flagged runs is never committed.
  - (d) A revocation line makes every later `complete` ineligible.
  - (e) A `ledger-lines` value larger than the ledger refuses with `sidecar-mismatch`.

### INV-021: an interrupted hook can lose the person's unstaged edits

**Check against the repository and the hook framework: the finding is correct.** One detail is wrong. A's dropped `dirty` refusal ran once, at Wave 0, so it never protected edits made during the run. The protection has to sit at each boundary.

**How the framework behaves.** All of these were read in the upstream source:
- `run.py` enters `staged_files_only` whenever no file list is given (`stash = not args.all_files and not args.files`). `hook_impl._run_ns` gives no file list for the `pre-commit`, `commit-msg` and `post-commit` hook types.
- `install_hook_envs` runs inside that stash context, so a first-time environment install happens while the person's edits are set aside.
- `staged_files_only.py` runs `git write-tree` on the current index and then `git diff-index --binary --exit-code <tree> --` against the worktree. It saves the diff as `patch<time>-<pid>` in the store directory, runs `git -c submodule.recurse=0 checkout -- .`, and re-applies the patch only in a `finally` block.
- `error_handler.py` catches only `Exception` and `KeyboardInterrupt`. Ctrl-C therefore restores the edits, and SIGKILL cannot. I found no SIGTERM handler in the files I read; whether one exists anywhere else in pre-commit is UNVERIFIED.

**Experiment** (`/tmp`, git 2.47.3; a hook ran the same command sequence as `staged_files_only.py`, then the commit's process group was sent SIGKILL during the hook):
- Under `git commit --only -- a`, the hook's `GIT_INDEX_FILE` was `.git/next-index-<pid>.lock`.
- `diff-index` exited 1. The patch held every tracked path outside the commit set S that differed from HEAD: the unstaged edit to `b` and the staged `c`.
- After the kill:
  - the edit to `b` existed only in the patch;
  - `c` was reverted in the worktree but still intact in the real index;
  - `index.lock` and `next-index-<pid>.lock` were left behind.
- With only a staged change outside S, nothing was lost.
- With no tracked change outside S, `diff-index` exited 0 and nothing was touched.

**Requirement text.**

- **HR-2.1 `unstaged-outside` refusal.** The check runs immediately before the boundary's `git commit` call, after the boundary's own `git add` calls. The helper lists tracked paths outside S whose worktree differs from the index (`git --no-optional-locks diff --name-only -z --ignore-submodules=all`). If the list is not empty:
  - append `refused reason=unstaged-outside` and STOP `E-COMMIT-REFUSED`;
  - print up to 20 of the paths, then: "stage, commit or set these edits aside yourself, then run the same `/sc:implement … --commit-tasks` line again; /sc:implement never stashes";
  - run no `git commit`.
- **HR-2.2 What can still be stashed.** After HR-2.1, a hook manager's stash can hold only paths that are staged outside S, such as other packages under `.dev/tasks`. Their content stays in the real index, so an interrupted hook loses nothing.
- **HR-2.3 Timeout.** The commit Bash call uses the Bash tool's maximum timeout (600000 ms), because hook environments are installed inside the stash. C's 120-second mutation timeout is not adopted.
- **HR-2.4 After an interruption** (a timeout, a signal or a killed session):
  - The boundary is `uncertain` unless the success test holds.
  - The verify step, and the next run's reconcile, print three things: the leftover `.git/index.lock` and `next-index-*.lock` files, to be removed only after confirming that no git process is running; every path outside S whose worktree blob equals HEAD's while its index blob differs, with `git checkout -- <paths>` to restore the worktree copy from the index; and the hook manager's patch location when it is known (pre-commit: `~/.cache/pre-commit/patch*`).
  - This is a report. Nothing is repaired.
- **HR-2.5 `/sc:git commit`.** The person chose the paths, so the same check prints a warning instead of refusing. The command also uses the maximum timeout.
- **HR-2.6 No bypass.** No `--no-verify`, no `SKIP=` and no `commit-tree`. The check makes the stash harmless; it does not avoid it.
- **HR-2.7 Tests** (`/tmp` repositories, with a hook that runs the exact command sequence of `staged_files_only.py` and names the pre-commit version it was copied from):
  - (a) An unstaged edit outside S is refused before any `git commit`; the hook's log is never created.
  - (b) Only a staged change outside S, plus SIGKILL during the hook: every staged blob is still in the index, and reconcile prints the reverted path and the lock files.
  - (c) No change outside S: the emulated `diff-index` exits 0.
  - Plus one test that runs the real framework, skipped when `pre-commit` is not installed. This repository has no pre-commit dependency.

**Considered and rejected.**
- Committing with `commit-tree` and `update-ref` skips the hooks, which is forbidden.
- Committing from the real index loses `--only` and the X-005 split (stage all of `.dev/tasks`, commit only the run's package).
- Refusing only when a hook is detected needs a second source of truth: the hooks directory, `core.hooksPath`, husky, lefthook. That would drift.

### INV-027: an `uncertain` boundary blocks the ledger forever

**Check against the repository: the finding is correct.** The owner may not be asked to write a file (`WORKER-CONTRACT.md:57`), and nothing defines how an `uncertain` boundary gets resolved. The same line also supplies the mechanism: "other owner records … are likewise given by the owner in chat and recorded by the agent in that session from that confirmation, naming the exact scope, the owner's quoted words and the date".

**Requirement text.**

- **HR-3.1 Record form.** Appended to `commits.md` by the executor only:
  ```
  T<ids>: commit resolved key=<key> as=<abandoned|adopted>[ head=<40-hex> differs=<n>] at=<YYYY-MM-DD> quote="<owner's words>"
  ^T([0-9A-Za-z.,-]+): commit resolved key=([0-9a-f]{12,64}) as=(abandoned|adopted)( head=[0-9a-f]{40} differs=[0-9]+)? at=[0-9]{4}-[0-9]{2}-[0-9]{2} quote="((?:[^"\\]|\\.){1,200})"$
  ```
  The quote is limited to 200 characters, with `"` and `\` escaped and no newline.
- **HR-3.2 Who decides, and how.** The owner replies in chat, in the session where the STOP printed the choices, naming the key and the word `abandon` or `adopt`. The 12-hex display form of the key is enough when it is unique. The executor records the reply under the Ruling confirmation rules (`refs/qa.md:254`): the reply must be clear, scoped and from the person. These do not count as a resolution: another agent's message, a coordinator's reply, a generic "continue", or a plan or brief field. Under a future `--unattended` mode, an unsettled boundary makes the run `blocked` with the question.
- **HR-3.3 Read-only check.** The helper verb `resolve-check --key <key> --as <abandon|adopt>` prints either the exact line to append or one of these refusals:
  - `unknown-boundary`;
  - `ambiguous-key`;
  - `already-settled`;
  - `adopt-not-descendant`. `adopt` needs HEAD ≠ parent and `git merge-base --is-ancestor <parent> HEAD`. The parent is the prepared parent or, for a boundary that was never prepared, the first member's `q0-head`.
- **HR-3.4 Meaning.**
  - `abandoned`: no commit is ever made for that key, and its files stay as they are.
  - `adopted`: the owner accepts the history at `head=` as settling the boundary. `differs=` counts the paths in S whose blob at `head` differs from the boundary pin; the STOP printed those paths before the owner answered.
  - Neither choice grants commit authority or makes a commit.
- **HR-3.5 What the STOP prints.** For each unsettled boundary: the key, the members, the state, the parent and HEAD, `git diff --stat <pin> HEAD -- <S>`, and the reply sentences. The `adopt` sentence appears only when its precondition holds.
- **HR-3.6 After recording.** The executor deletes the boundary's pins with literal `git update-ref -d` calls and runs reconcile again. The run then continues according to its own flags. `resolved` is a settling line, so Row 1, the all-complete step and the archive gate can be reached again.
- **HR-3.7 Tests.**
  - (a) Crash after `prepared`, then the person runs their own `git commit`. The resume STOPs as `uncertain` with both sentences. Recording `adopt` appends the line and deletes the pins, and the next resume and the archive gate both pass.
  - (b) `abandon` on a refused boundary during an unflagged run lets that run start the next task.
  - (c) A static protocol test that a resolution taken from another agent's message is refused.
  - (d) The refusals `unknown-boundary`, `already-settled` and `adopt-not-descendant`.
  - (e) `hook-rewrite-committed`, resolved with `adopt`.

## Ruling on the other 19 findings

| Finding | Ruling | Requirement, residual or evidence |
|---|---|---|
| INV-002 | ACCEPT-FIX | The `run` line records `branch=<git symbolic-ref -q HEAD>`, and the `prepared` line repeats it. Prepare refuses `branch-changed` when the current symbolic ref differs. |
| INV-003 | ACCEPT-FIX | Before any `complete` line in an `on` segment, the executor pins the private-index worktree tree as `refs/superclaude/implement/<slug>/accepted/T<id>`. That pin is the accepted candidate for compliant tasks and for tasks a Ruling accepted (`refs/retry.md:504`: "accepts the tree as it stands"). A missing pin refuses `no-accepted-tree`. |
| INV-004 | ACCEPT-FIX | Retries and late preparation compare only the product paths (the `files=` union) with the accepted pin or the disclosed `rewritten=` tree. Package evidence is always taken fresh, so the `codegraph.md` line every run appends (`SKILL.md:79`) never blocks a retry. Reconcile runs before steps 7-9. |
| INV-007 | ACCEPT-FIX | A `files=` path that is missing from the worktree but present in the index or HEAD is a deletion and is staged. Only a path missing from all three goes to `skipped why=absent`. With the flag on, Q1's touched set (`SKILL.md:132`) names deleted paths and both ends of a rename. |
| INV-008 | ACCEPT-FIX | Before the add, any path equal to or under a mode-160000 entry of HEAD or the index (prefix match on `path/`) goes to `skipped why=gitlink`. |
| INV-009 | ACCEPT-FIX | `update` first runs `git -C <path> cat-file -e <gitlink>^{commit}`. If the object is missing, the state is `target-not-local`. That state updates (with the fetch disclosed) only when the module is clean and its HEAD is contained in a local or remote-tracking branch, so nothing is orphaned. An `--is-ancestor` exit of 128 is never read as "diverged". |
| INV-010 | ACCEPT-FIX | For an uninitialized module, `update` prints the `.gitmodules` URL and runs only when the typed line repeats it as `--url <url>`, byte for byte. An initialized module whose URL differs refuses `remote-mismatch` and prints `git submodule sync -- <path>` for the person to run. |
| INV-011 | ACCEPT-RISK | The finding is correct: Wave 0 has no unknown-option STOP (`SKILL.md:57-59`, verified). A stale copy that ignores the flag makes no commit, which is today's behaviour, so it fails safe. Mitigation: the first Wave 0 line prints `commit-tasks=on run=<n>`, and the final summary prints the commit count. Old copies cannot be fixed. |
| INV-012 | ACCEPT-FIX | Every add and commit passes its paths with `git --literal-pathspecs … --pathspec-from-file=<temporary file outside the tree> --pathspec-file-nul`. Verified on 2.47.3: `d/how to merge.md` was committed under `--only`, and another staged entry stayed staged. The guard's `( \|/git-\| git-)(merge\|pull) ` classifier (`launch-level-guard.sh:595-596`, verified) then never sees a path. |
| INV-014 | ACCEPT-FIX | Membership is already defined as the overlapping-window set (`refs/retry.md:40`, verified). A batch boundary is eligible only when every member is eligible. Otherwise it gets the settling line `skipped reason=mixed-authorization`, and the summary lists the batch's files. |
| INV-015 | ACCEPT-FIX | The 72-character limit counts Unicode code points of the decoded header. Drafting cuts at the last space at or before code point 72, and the helper counts the same way. |
| INV-018 | ACCEPT-FIX | A `files=` entry that is a directory refuses `directory-entry`. The package directory is expanded with `git ls-files -z --cached --others --exclude-standard -- <pkg-dir>` and passed through the pathspec file. Stated residual: a file a person adds inside the package is committed with it. The package has a single owner (`refs/managed-workspace.md:94`), and `git add .dev/tasks` stages that file anyway. |
| INV-020 | ACCEPT-FIX | Verified: the repository's hook config excludes `.md` files from `trailing-whitespace` only, and `end-of-file-fixer`, `mixed-line-ending` and the 1000 KB limit apply to package evidence (`.pre-commit-config.yaml:9-36`). A rewrite that touches only evidence (not plan, source or product files) is classed `hook-rewrite-evidence`. The next flagged run retries it with fresh evidence and no product re-review. A file over the size limit is `hook-failed`, with the file named. Owner follow-up, not part of this work: exclude `^\.dev/tasks/.*/artifacts/` from the fixers. |
| INV-022 | ACCEPT-FIX | HR-1.4: no task starts while a boundary is unsettled, and retries happen only in reconcile, so HEAD never moves under an open task. Test: an unflagged run after a refusal STOPs before task selection. |
| INV-023 | ACCEPT-FIX | Archive gate step 1 also STOPs `E-ARCHIVE-BLOCKED reason=unsettled-boundary`. HR-1.4 already prevents this state; this check is a second line of defence. |
| INV-024 | ACCEPT-FIX | `/sc:git commit` stages `.dev/tasks` as the house rule requires, but never adds it to its commit pathspec. With no paths named, it commits the index as the person staged it, and warns when that index holds a `commits.md` with an unsettled boundary. |
| INV-025 | ACCEPT-FIX | For a compliant `complete`, the product paths of the accepted pin must equal the last review header's tree (`refs/qa.md:178`). If they differ (Q6 extras rewrote a reviewed file), the boundary refuses `changed-after-review` and names the paths. |
| INV-029 | ACCEPT-RISK | Verified: no pre-commit hook is installed here. No workflow under `.github/workflows/` runs pre-commit or detect-secrets. `superclaude review safety-scan` scans for words, not credentials (`safety_cmd.py:1`). The boundary adds no new kind of exposure: `.dev/tasks` is already always staged and committed by the person's commits and by the WC-9 worker commit (`WORKER-CONTRACT.md:43`), and `/sc:implement` never pushes. Drop C's "stop if evidence would expose secrets" claim, because nothing can detect it. |
| INV-030 | ACCEPT-FIX | Containment is checked only against the remote-tracking refs of the submodule remote whose `remote.<r>.url` equals the `.gitmodules` URL. If there is no such remote, the pointer commit refuses `submodule-unpublished reason=no-gitmodules-remote`. |

## Final concessions

1. **C's N1 (boundary key).** The key must bind the ledger position of each member's `start` line, not only the tree hash. The hash records content; the position records which start it was.
2. **INV-006.** C's frozen full-candidate success test replaces both A's and B's success predicates.
3. **X-007 (renewed review), C's objection.** A person can only have reviewed a diff that was shown before they typed the new flagged line. The `rewritten=` pin, shown in the refusal, is what makes that true.
4. **INV-021.** A's dropped `dirty` refusal did protect something real. It returns as a narrow check at each boundary, not at Wave 0.
5. **Unflagged runs and pending boundaries.** The Round 2 text "an unflagged run prints the pending boundary and leaves it alone" (A and B) was unsafe (INV-022, INV-023). HR-1.4 replaces it. This is the one place where my final position changes the Round 2 consensus.
6. **C-010 item 7.** C was right that owner-resolved abandonment needs a defined record. HR-3 supplies it.

## Per-point votes

| Point | Winner | Confidence | Reason |
|---|---|---|---|
| S-001 | A | 55 | Balanced density with verified citations; B repeats evidence, C omits test-pinned facts. |
| S-002 | B | 65 | Resolve column maps each alias to the repository; A overloads `<pkg>`; C's letters are opaque. |
| S-003 | HYBRID | 60 | A's verified baseline-facts table plus B's root causes: facts say what holds, causes say why. |
| S-004 | A | 50 | Gapped blocks absorb inserts without renumbering; low stakes, the merge renumbers anyway. |
| S-005 | HYBRID | 65 | A's per-behaviour table, B's existing-tests-to-update table, C's fault-injection points. |
| S-006 | B | 60 | Runnable shell observations with pass conditions; keep A's AC-to-test mapping beside them. |
| S-007 | B | 55 | Root-cause column ties each mitigation to its cause; otherwise comparable. |
| S-008 | HYBRID | 75 | B's mirrored read-only skill script; A's module split, rules constants, contract version; C's outcome fields. |
| S-009 | A | 60 | Operation registry, per-group refs and shared safety ref; read operations load no ref (B). |
| S-010 | B | 60 | Distinct `refs/commit-step.md` avoids two different `refs/commit.md` files across skills. |
| S-011 | HYBRID | 75 | B's sidecar, C's prepared line and frozen candidate; run lines gain `ledger-lines`; owner `resolved` line settles blocked boundaries. |
| S-012 | A | 55 | D7 (merge removed) and D8 (package-only commit) settle the seed's two hardest tensions. |
| S-013 | HYBRID | 55 | A's single-source, extension, version NFRs; B's size budgets; C's bounded execution and honest trust boundary. |
| C-001 | A | 60 | Existing advertised surface (`git.md:14`, `:17`) minus push, pull, merge, plus submodule operations. |
| C-002 | A | 55 | One-turn path for the person's own message; today `commit` without `--smart-commit` has no source. |
| C-003 | B | 60 | Prefix rule plus a refusal with no replayable argv; A's dry run handed argv to unauthorized callers. |
| C-004 | HYBRID | 65 | B's person-origin check at Wave 0 is primary; A's static test catches templates inserting the flag. |
| C-005 | HYBRID | 70 | A's Q8a, R0, L0 positions; reconcile before selection, all-complete and archive; settle before advance. |
| C-006 | HYBRID | 65 | A's before-step-6 placement minus `dirty`; B's `helper-missing`; branch recorded in the run line. |
| C-007 | A | 60 | Two codes keep each STOP row's columns single-valued; `unsettled` is one more `E-COMMIT-REFUSED` reason. |
| C-008 | HYBRID | 75 | B's per-path `foreign-change`, an accepted-tree pin at complete, and the per-boundary `unstaged-outside` refusal. |
| C-009 | HYBRID | 75 | B's committed-tree comparison in C's frozen-candidate form; refusal pins the hook-rewritten tree for disclosure. |
| C-010 | HYBRID | 80 | C's prepared line, position key, frozen check; B's pins; `ledger-lines` segments find unprepared boundaries; owner adopt or abandon. |
| C-011 | B | 70 | Keep Q0, accepted and reviewed-tree pins until the boundary settles; amend Row 1 and the Q7 cleanup. |
| C-012 | HYBRID | 60 | A's ten types and verdict trailer; 72 Unicode code points total; B's `Implement-Plan:`; C's boundary trailer. |
| C-013 | B | 60 | Temporary file outside the tree; A's in-package message file is committed clutter. |
| C-014 | HYBRID | 65 | C's independent fields with unset-versus-false; A's single action state derived by fixed precedence. |
| C-015 | HYBRID | 65 | B's clean module and containment against the `.gitmodules` remote only; C's post-commit gitlink check; one-path set. |
| C-016 | C | 60 | Explains the route and that `archive` writes without `--apply`; no extra operation. |
| C-017 | B | 65 | Fixed set plus `origin/HEAD`; a notice, not a block, when it is unset or stale. |
| C-018 | HYBRID | 60 | B's preconditions, argv, result and undo hint plus C's statement of what HEAD, index, worktree did. |
| C-019 | HYBRID | 70 | A's routing rewrite and fixtures, B's classification rows; amend `refs/retry.md:504`, Row 1, Q7 cleanup, archive gate. |
| C-020 | B | 70 | Plugin build copies only the plugin tree; a mirrored script ships everywhere with `helper-missing`. |
| C-021 | C | 85 | Verified: `--literal-pathspecs` with `--pathspec-from-file` commits literal paths and keeps path words from the guard. |
| X-001 | HYBRID | 80 | Flag (A, B); person-origin at Wave 0 (B); static scope test (A); bounded run record and revocation (C). |
| X-002 | A | 90 | The seed forbids merge in `/sc:git`; A removes it and rewrites the routing row. |
| X-003 | A | 75 | Fixture lists only `--smart-commit` (`:327`); `--interactive`'s only example was the merge. |
| X-004 | B | 70 | Sidecar leaves the resume regex and archive parser untouched; the archive digest excludes `artifacts/`. |
| X-005 | A | 65 | Stage all `.dev/tasks`, commit only the run's package expanded to literal files; no liveness signal exists. |
| X-006 | B | 75 | No retroactive commits; `ledger-lines` segments make "completed in a flagged run" computable after a crash. |
| X-007 | HYBRID | 70 | Never automatic; the refusal pins and prints the hook-rewritten tree; a later flagged run commits only that disclosed tree. |
| X-008 | HYBRID | 80 | Agent runs literal git writes the guard sees (A, B); helper read-only; C's verification as a separate call. |
| X-009 | A | 60 | Branch management is advertised today (`git.md:17`); clean-tree, no-force guards keep risk low. |
| X-010 | C | 60 | Defaulting to read-only status is harmless; unknown operations still stop. |
| X-011 | A | 55 | Seed criterion names the guide (`:277-278`); practice favours `standard`, but no code reads it. |
| X-012 | A | 65 | One non-nested submodule; report nested as not inspected; never recursive. |
| X-013 | HYBRID | 65 | B's fast-forward rule; a gitlink not yet fetched (exit 128) is `target-not-local`, updated only when nothing is orphaned. |
| X-014 | B | 60 | No downstream publication gate; the refusal errs safe; containment only against the `.gitmodules` remote; last-fetch time printed. |
| X-015 | HYBRID | 65 | B and C admit the clone's network effect; the typed line repeats the `.gitmodules` URL; a sync hint covers mismatches. |
| X-016 | A | 85 | Check before step 6 fits "no ledger writes"; B contradicts `SKILL.md:72`. |
| X-017 | HYBRID | 65 | Keep B's `pre_tree`; reword: objects only, as Q0 does (`SKILL.md:124`); no ref, index or worktree writes. |
| X-018 | A | 70 | A plain total check of 72 Unicode code points; B's regex admits 81. |
| X-019 | B | 80 | `<pkg-dir>` for the task package; A overloads `<pkg>`. |
| X-020 | B | 85 | No commit-msg hook installed here; the helper must validate the header itself. |
| X-021 | NONE | 75 | All misstate tracked files; correct the fact, keep settings-only automatic staging per the project rule. |
| A-001 | NONE | 80 | Missing from the worktree but in the index or HEAD is a deletion to stage; skip only when missing from all three. |
| A-002 | HYBRID | 60 | All equally right: FINAL reads current files (`refs/qa.md:311`); add a pinning test. |
| A-003 | HYBRID | 75 | Flag checked once at Wave 0; bounded run line after step 6 with `ledger-lines` and `branch`; revocation; resume needs the flag. |
| A-004 | HYBRID | 60 | Never claim freshness: B's refusal errs safe; print last-fetch time (C's honesty); no fetch. |
| A-005 | NONE | 85 | No variant handled it; verified that pre-commit stashes every path outside S under `--only`; fixed by the `unstaged-outside` refusal. |
| A-006 | HYBRID | 60 | All equally right; no test pins the K3 wording. |
