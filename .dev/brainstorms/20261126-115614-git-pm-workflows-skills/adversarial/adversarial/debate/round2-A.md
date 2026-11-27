# Round 2 — Rebuttal for Variant A (architect; maintainability and extension scaffolding)

"Verified" means I re-read the line or re-ran the check read-only in this worktree in this round. Four git behaviours were checked in throwaway repositories under `/tmp` (git 2.47.3), which were removed afterwards. Nothing in the repository was changed.

## Response to criticisms

| # | Criticism of A (raised by) | Response |
|---|---|---|
| 1 | No recovery when the session dies between the commit and its record (C-010; B, C) | **Concede.** The resolution is in the open-points section: a `prepared` line before each attempt, a boundary-key trailer, and a read-only reconcile at the start of every run. The protocol already uses git history this way: "Trust ledger + git history after compaction" (`refs/ledger.md:141`, verified). |
| 2 | The helper is missing in plugin-only installs (S-008, C-020; B, C) | **Concede.** Move the helper to a skill script mirrored into the plugin, run with `uv run --no-project python` (precedent `refs/managed-workspace.md:54`). Keep A's module split, the single constants file with its parity test, the registry-resolves test and the contract-version field. B is also right that A's U-004 point is moot after the move: the path `.../sc-git-protocol/scripts/...` contains `-git-`, which the guard's regex `( \|/)git(-[a-z][a-z-]*)? ` does not match (`launch-level-guard.sh:555`, verified). |
| 3 | The ledger grammar and archive parser change (X-004; B, C) | **Concede.** New evidence makes the sidecar strictly cheaper. The archive state digest covers plan, source and `files=` delivery paths, not `./artifacts/*` (`refs/managed-workspace.md:95`; `archive_workspace.py:233`, `:405`). The archive script checks `artifacts/` only for being a real directory (`:306-316`). So `artifacts/commits.md` changes no parser, no digest and no resume regex (`refs/ledger.md:127`). Precedent for a run-state file beside the ledger: `codegraph.md` (`SKILL.md:79`). |
| 4 | A resume silently includes hook rewrites nobody reviewed (X-007, FR-065; B, C) | **Concede the automatic part.** The merged rule: never retry automatically; the refusal prints the hook-changed paths and `git diff --stat`; a retry happens only in a new flagged run, whose Wave 0 prints those paths again before any attempt. The person's new typed line after seeing the diff is the renewed review. |
| 5 | The Wave 0 `dirty` refusal is too coarse and too weak (C-008; B, C) | **Concede.** Drop the `dirty` reason. Use B's per-path `foreign-change` against the Q0 pin, plus C's increment check: the S paths must equal the tree recorded on the task's last compliant review header (`refs/qa.md:178`). When that review recorded `tree=none` (`:182`), fall back to `foreign-change` alone and say so. Whether every completing review writes a tree header is UNVERIFIED. |
| 6 | Tasks from an unflagged resume get committed later (X-006; C) | **Concede.** The `COMMIT: on` marker goes. Only tasks completed in a flagged run get a boundary (A-003 resolution). |
| 7 | Hook outcome judged only by exit code and HEAD (C-009; B, C) | **Concede; adopt `pre_tree`.** A simplification: `pre_tree` is HEAD plus the S paths from the working tree, and `--only` commits exactly that, so success means `HEAD^` equals the recorded parent and `HEAD^{tree}` equals `pre_tree`. |
| 8 | The dry run hands an unauthorized caller ready-to-run commands (C-003; B) | **Concede.** Refuse with the reason and print no commands, as B does. |
| 9 | "Touches no remote" contradicts the submodule clone (X-015; B, C) | **Concede.** NFR-001 gets one stated exception: `submodule update` may clone or fetch from the configured URL, which the person's typed line authorizes. A concrete form of C's remote-identity rule: refuse `remote-mismatch` when `submodule.<name>.url` in the local config differs from `.gitmodules` (two `config --get` reads). |
| 10 | No ancestry check in `update`, and states can overlap (X-013; B) | **Concede.** Adopt B's fast-forward-only rule. The C-014 vote adds a fixed precedence. |
| 11 | `<pkg>` means two things (X-019; B) | **Concede.** Use `<pkg-dir>` for the task package. |
| 12 | The message file inside the package gets committed (C-013; B) | **Concede.** Write it to a temporary file outside the tree. Refusal logs stay in `artifacts/` as evidence. |
| 13 | A's marker is not per invocation (A-003; B) | **Concede.** It is replaced by per-run lines (open points). |
| 14 | `complexity: moderate` goes against repository practice (X-011; B) | **Partly concede.** Verified: `standard` appears in 8 command files (cleanup, closeout, explain, impact, implement, recommend, workflow, worktrees) and `moderate` in 1 (validate-tests). But the seed's success criterion says "matches the developer guide", whose lists are `simple, moderate, advanced, high` (`:278`) and include `version-control` (`:277`), both verified. No code reads these fields (B RC-5). I keep A at lower confidence; the gap between guide and practice is a follow-up. |
| 15 | Branch create and switch are extra mutations (C-001, X-009; C) | **Counter.** Today `git.md` lists "status, add, commit, push, pull, branch" (`:14`) and "Branch management and merge operations" (`:17`), verified. The seed removes push and merge (pull is fetch plus merge); it does not remove branch. A's guards are a clean tree with submodules included, no force, and refusing protected names on create. Git itself refuses to switch to a branch checked out in another worktree. |
| 16 | `--message` is unnecessary (C-002; C) | **Counter; low stakes.** Today `commit` without `--smart-commit` has no message source (B concedes this). `--message` gives the person's own words in one turn and goes in through `-F <file>`, as the guard advises (`launch-level-guard.sh:135`, verified). C's route (ask through `--interactive`) works but costs a turn, and the flag's only example was merge. |
| 17 | A static string ban is weaker than a runtime check (C-004; C) | **Agree it is secondary.** The person-origin check at Wave 0 is the primary guard. A's static test stays as a cheap second check: it catches a handoff template that inserts the flag. |
| 18 | No literal-path handling and no handling of vanished paths (C-021, A-001; C) | **Concede,** with new evidence N1 and N3: one absent path aborts the whole `git add`, and a file name with pathspec magic widens it. |
| 19 | Contiguous numbering is better (S-004; C) | Not persuaded. The merged spec will be renumbered anyway; low stakes. |
| 20 | Stop when evidence belongs to another live writer (X-005; C) | **Counter.** No liveness signal exists. The house precondition is "one `/sc:implement` invocation writes a given ledger at a time; there is no lock" (`refs/ledger.md:149`, verified). A's package-only commit keeps other packages out without having to detect liveness. |
| 21 | One closed state label hides facts that are true at the same time (C-014; C) | **Partly concede.** Report C's separate fields (unset distinguished from false; null when unknown). Derive one action state from them with a fixed precedence (conflict, dirty, detached-new-commits, uninitialized, ahead/diverged/pointer-moved, in-sync), so each refusal rule reads one value. |
| 22 | Keep `--interactive` for clarification (X-003; C) | **Counter.** Its only example is the merge (`git.md:72-77`), and the fixture lists only `--smart-commit` (`routing_refresh_cases.json:327`, verified). |
| 23 | A hardcoded protected set is unsafe in other repositories (C-017; C) | **Counter** with new evidence N5 (open points). |

## Updated assessment of B and C

### B

**Steelman.** B places the commit where none of the HEAD rules can see it. It keeps the write a literal Bash call that the guard can classify, and it builds three integrity checks on pins that already exist: `pre_tree`, `foreign-change` and recovery from trailers. Its Round 1 concessions (merge, `--interactive`, step order, `.dev/tasks` scope, regex length) remove every seed conflict I raised.

**Arguments that changed my mind.**
- **X-014: commit time is the only guard point.** I verified that nothing downstream checks whether a submodule commit is published. In `/sc:pr-submit`, the only submodule logic is a halt on a submodule conflict (`<pkg>/pr_submit/conflicts.py:733`), and `.github/` has no submodule reference. The one submodule here points to a third-party repository (`.gitmodules:3`), so a local commit inside it can probably never be published by this project (an inference). My vote moves from A to B.
- **A-003, B's concession 8** (bind the grant at Wave 0 and record it in `commits.md`) matches my resolution below.
- **X-017.** The merged spec needs `pre_tree`, so the wording must change, not the verb list. My vote moves from A to HYBRID.

**Arguments that did not change my mind.** On its own, B's runtime "current message starts with `/sc:implement`" check fails at the next boundary after an in-chat Ruling (N6), and B conceded this. B's stated reason for keeping `--interactive` is false (verified line 327). B's single STOP row still splits its own columns.

### C

**Steelman.** C treats the boundary as a recoverability contract. It writes a record before the attempt, binds the key to the task's start generation, defines a closed set of outcomes including `uncertain`, and requires fault injection with "at most one commit per boundary key". It handles paths literally, never repairs a refusal on its own, and states plainly what prompt text cannot enforce. Its Round 1 concessions on X-008 (the hidden commit), X-012 (nested submodules) and X-013 (update) remove its largest defects.

**Arguments that changed my mind.**
- **C-010 and S-011.** B's recovery accepts any HEAD whose parent and trailers match. Without a record of the prepared candidate, it cannot tell the prepared commit from a different commit that carries the same trailers (for example, a hook rewrote and re-added files). C's `prepared` line, which records the parent and `pre_tree`, closes that gap at the cost of one appended line. Both votes move from B to HYBRID.
- **C-021.** Confirmed by experiment N3. My confidence rises.
- **C-014.** Separate fields are right for the report.
- **X-007.** Renewed review before any retry is right.

**Arguments that did not change my mind.**
- **The lock (NFR-002).** The ledger rules say "there is no lock" (`refs/ledger.md:149`). The boundary spans three separate Bash calls (prepare, the agent's own `git commit`, verify), so no single process can hold a lock across them. It would have to be a lock file, and C forbids deleting an old lock, so one crash would block every later boundary until a person removed it.
- **The versioned request object.** A contract version in the helper's output (A NFR-009) gives the same mismatch refusal without a request schema.
- **C-017, "verified policy".** Experiment N5 shows that `refs/remotes/origin/HEAD` is often absent, so "block when unknown" would block most repositories that were not cloned.
- **X-005, live-writer detection.** There is no signal to detect it with.

## New evidence

1. **N1, A-001.** `git add -- a c gone`, where `gone` does not exist, exits 128 and stages nothing, not even `a` or `c`. The planner must put absent paths in `skipped` (with `why=absent`) before building `add_argv`.
2. **N2, U-005.** After `git add b`, the command `git commit --only -- a` commits only `a`, and `b` stays staged. A's T-05 assumption holds on 2.47.3 without hooks. A-005 (the pre-commit framework under `--only`) is still unverified.
3. **N3, C-021.** I created a file literally named `:(glob)*` and ran `git add -- ':(glob)*'`. Git read the name as a glob and also staged the untracked `c`. With `git --literal-pathspecs add -- ':(glob)*'`, only that file was staged. A leading dash after `--` (`-n`) is safe. The merged spec should run every add and commit as `git --literal-pathspecs ...`.
4. **N4, X-008.** The guard skips any other global option (`-*) j=$((j + 1))`, `launch-level-guard.sh:699`) and then classes `commit` as `COMMIT` (`:713`). So `git --literal-pathspecs commit --only -F <f> -- <paths>` is still visible to the guard and still gated by it.
5. **N5, C-017.** On git 2.47.3, `git remote add origin <url>` followed by `git fetch` leaves `refs/remotes/origin/HEAD` unset (`symbolic-ref` exits 128). Only `clone` sets it.
6. **N6, A-003.** The person gives a Ruling in chat, and the agent records it (`WORKER-CONTRACT.md:57`). An accepted Ruling continues to the next task (`refs/qa.md:248`, "T{i+1}? Yes"). So the next boundary runs in a turn whose message does not start with `/sc:implement`.
7. **N7, per-run state precedents.**
   - "A resume is a new run and does its own single check" (`SKILL.md:76`).
   - Per-run state already lives in `codegraph.md` beside the ledger, which "is not the ledger" (`SKILL.md:79`).
   - "Re-read the ledger from disk ... Do not trust session memory" (`SKILL.md:118`).
   - "Trust ledger + git history after compaction" (`refs/ledger.md:141`).
8. **N8, against C's lock.** "One `/sc:implement` invocation writes a given ledger at a time; there is no lock" (`refs/ledger.md:149`).
9. **N9, S-011.** The FINAL digest does not cover `artifacts/` (`refs/managed-workspace.md:95`), and the archive script checks `artifacts/` only for being a real directory (`archive_workspace.py:306-316`). A sidecar there needs no archive change.
10. **N10, missed by all three.** `refs/retry.md:504` says that a Ruling after a halt "accepts the tree as it stands ... (no commit follows it)". With `--commit-tasks`, a commit does follow at the next boundary. The merged spec must amend that parenthesis and add it to the C-019 inventory.
11. **N11, X-011.** The usage counts in row 14 above. The guide lists are at `:277-278`.
12. **N12, X-014.** There is no downstream publication check (row "Arguments that changed my mind" under B), and the submodule's remote is third-party (`.gitmodules:3`).
13. **N13, X-021.** `git ls-files .claude/` prints `.claude/cache/sc-recommend-lookup.yaml` and `.claude/settings.json`. `.gitignore:129-135` marks the cache entries as a "user-authorized exception". The project rule allows staging only `settings.json` without an explicit instruction in the session. So the merged spec should correct the factual claim but keep automatic staging limited to `settings.json`. A `dev-copy-path` refusal names the file and says the person may stage it themselves.
14. **N14, X-009.** `git.md:14` and `:17` advertise branch management today.

## Proposed resolution for the six open points

### A-003: how long the between-task commit authorization lasts

The merged spec should say:
1. **Grant.** `--commit-tasks` counts only as a standalone token in the option prefix (the rule at `SKILL.md:57-59`) of a message the person typed that starts with `/sc:implement`. It is checked once, in Wave 0 step 1. If the protocol is reached through another command or an agent's own invocation, it STOPs with `E-COMMIT-PRECONDITION reason=not-person` before any write.
2. **Run record.** Wave 0 appends `run <n>: commit-tasks=<on|off> at=<ISO-8601> line="<invocation line as typed>"` to `commits.md`. It writes this line when the flag is present, and also when `commits.md` already exists but the flag is absent, so an older `on` can never govern a newer run. A run without the flag, on a ledger that has no `commits.md`, writes nothing, which is today's behaviour.
3. **Lifetime.** The latest `run` line governs, for that run only. A run includes every later turn the protocol treats as the same run: the in-chat Ruling that continues to the next task (N6) and any compaction (the executor re-reads from disk, `SKILL.md:118`). A resume is a new run (`SKILL.md:76`) and needs the flag again.
4. **Revocation.** If the person asks, during the run, to stop committing, the executor appends `run <n>: commit-tasks=off reason=revoked` before the next boundary. Plain words may narrow authority, never widen it.
5. **Rulings** neither grant nor revoke the authorization (`refs/ledger.md:239`).
6. **Mechanical check.** The helper's `preflight` reads the latest `run` line and refuses `not-authorized` unless it says `on`.
7. **Tests.**
   - Helper test: a missing line, an `off` line, and `on` followed by `off` all refuse.
   - Fixture: a flagged run followed by an unflagged resume makes no second commit.
   - Static test of the protocol text.
8. **Residual, stated in the spec.** An agent that resumes the protocol in a new session without running Wave 0 would read a stale `on`. The protocol text forbids that, and the quoted `line=` makes it auditable, but nothing mechanical prevents it.

### C-010: a crash between the commit and its record

The merged spec should say:
1. **Boundary key:** `<slug>/<ids>/<first 12 hex of the first member's start sha>`. The start sha is reused on resume (`SKILL.md:122`), so the key stays the same across resumes and changes when a task restarts with a new `start` line.
2. **Before `git add`,** append `T<ids>: commit prepared key=<key> parent=<HEAD 40-hex> pre_tree=<40-hex>`.
3. **The message** carries `Implement-Boundary: <key>` next to `Implement-Plan:` and `Implement-Task:`.
4. **Success,** as checked by `verify`, means `HEAD^` = parent, `HEAD^{tree}` = `pre_tree`, and HEAD's trailer carries the key. Then append `commit sha=<40-hex> key=<key>`.
5. **Reconcile.** At the start of every run, flagged or not (it only reads git and appends a record), and before task selection and the all-complete stop (`refs/ledger.md:134`, `:139`), check each `prepared` line that has no terminal line:
   - HEAD carries the key, `HEAD^` = parent and `HEAD^{tree}` = `pre_tree`: append `recovered sha=`.
   - HEAD = parent: nothing was committed. The boundary stays pending and is retried only by an authorized run (A-003), and only if the S paths still equal `pre_tree`. Otherwise refuse with `hook-rewrite` or `foreign-change`, under the X-007 rule.
   - Anything else: append `uncertain` and STOP `E-COMMIT-REFUSED reason=uncertain`, printing the parent, HEAD and key. Nothing is repaired.
6. **Only HEAD is inspected,** with no history walk, because no Q0 runs between a boundary and its record.
7. **Tests.** Interrupt after `prepared`, after the commit but before the terminal line, and after the terminal line. Resume twice each time. Assert at most one commit per key and a correct record. Also test that a person's commit on top gives `uncertain`.
8. **No lock, no journal directory, no request schema** (N8).

### C-015: when a pointer commit is allowed

`/sc:git submodule commit-pointer <path>` runs only when all of these hold:
1. The superproject passes the write preflight: not detached, not a protected branch, no operation in progress, no index lock.
2. The submodule is registered, initialized and free of conflicts, and it is clean (`m` = `.`, `u` = `.`). Otherwise refuse `submodule-dirty` with the message "commit inside the submodule first".
3. The submodule HEAD differs from the recorded gitlink. Otherwise the result is `in-sync`.
4. The submodule HEAD is contained in at least one remote-tracking branch of the submodule (`git -C <path> branch -r --contains HEAD` is not empty). Otherwise:
   - `detached-new-commits` when it is in no branch at all, printing `git -C <path> switch -c <name>`;
   - `submodule-unpublished` when it is only on a local branch (X-014).

   This replaces A's "HEAD on a branch" rule. That rule would refuse the normal state of a vendored submodule, which is detached at a fetched remote tip.
5. The commit set is exactly `{<path>}`. `.gitmodules` and the config are not changed. The message is `chore(submodule): bump <path> to <short-sha>` (B).
6. After the commit, `verify` checks that `git ls-tree HEAD -- <path>` names the sha that was printed in the plan (C). A mismatch is `uncertain`.
7. Only one level is handled. Nested submodules are reported as not inspected (X-012).

### C-017: protected branches in other repositories

The merged spec should say:
1. The protected set is `master`, `main` and `integration` (the guard's `LL-PROTECTED` names, `launch-level-guard.sh:58`, `:812`), plus the target of `refs/remotes/origin/HEAD` when it resolves. Inside a submodule it is resolved from the submodule's own refs (B).
2. When `refs/remotes/origin/HEAD` is not set, proceed with the fixed names. Print `default branch unknown: refs/remotes/origin/HEAD is not set; protected names: master, main, integration`, plus the local fix the person may run: `git remote set-head origin <branch>`. There is no network lookup and no block.
3. A detached HEAD is refused everywhere.
4. A residual is recorded: shared branches with other names are protected only by the server's rules.

Why not block: N5 shows that the ref is missing in every repository set up with `remote add` and `fetch`, so blocking would refuse every write there. A local commit can be undone (`git reset --soft <parent>`) and publishes nothing.

### S-011: where commit state lives

The merged spec should say:
1. **Location.** Commit state lives in `commits.md` in the ledger's directory:
   - legacy: `.dev/implement/<slug>/commits.md` (`refs/ledger.md:7`), never staged, like the legacy ledger (`:3`);
   - managed: `<pkg-dir>/artifacts/commits.md`, staged with `.dev/tasks`.
2. **Line forms.** One regex each, documented once in `refs/commit-step.md`, parsed by the helper, and pinned by a parity test (A's single-source rule):
   - `run <n>: commit-tasks=(on|off) at=<ISO-8601>[ reason=revoked] line="<text>"`
   - `T<ids>: commit prepared key=<key> parent=<40-hex> pre_tree=<40-hex>`
   - `T<ids>: commit (sha|recovered)=<40-hex> key=<key>`
   - `T<ids>: commit skipped key=<key> reason=empty`
   - `T<ids>: commit (refused|uncertain) key=<key> reason=<token>`
3. **Unchanged.** The ledger grammar, its resume regex (`refs/ledger.md:127`), `E-LEDGER-CORRUPT` and `archive_workspace.py` stay unchanged. The sidecar is archive-safe (N9).
4. **Post-commit record.** A terminal line written after a commit is not part of that commit (C). It stays staged and goes into the next boundary commit. After the last boundary it is left staged, and the final summary says so.
5. **Pin lifetime.** The Q0 pin and the task's last reviewed-tree ref are deleted after the boundary's terminal line, not at `complete` (B). This amends `SKILL.md:129` and resume row 1 (`refs/ledger.md:157`).

### X-014: a pointer commit to a commit that may not be published

The merged spec should say:
1. `commit-pointer` refuses `submodule-unpublished` when the target is on no remote-tracking branch of the submodule, according to local refs.
2. The refusal message: "`<short-sha>` is not on any remote-tracking branch of `<path>` (local refs; last fetch: `<FETCH_HEAD time or never>`). Push it first, or run `git -C <path> fetch` if it is already pushed, then retry. `/sc:git` never pushes or fetches." The time is the file time of `git -C <path> rev-parse --git-path FETCH_HEAD`, which is a read-only lookup.
3. When the target is found, the commit proceeds and the report prints "on `<remote-ref>` as of last fetch `<time>`". It never presents publication as a fresh fact (A-004).
4. There is no override flag in this work.

Why (my vote changed): no downstream check exists (N12); stale refs err in the safe direction (a false "unpublished" is fixed by a fetch); and the repository's only submodule is third-party.

## Per-point votes

| Point | Winner | Confidence | Reason |
|---|---|---|---|
| S-001 | A | 55 | Balanced density with verified citations; B repeats evidence, C omits test-pinned facts. |
| S-002 | B | 65 | Resolve column maps each alias to the repository; A overloads `<pkg>`; C's letters are opaque. |
| S-003 | HYBRID | 60 | A's verified baseline-facts table plus B's root causes: facts say what holds, causes say why. |
| S-004 | A | 50 | Gapped blocks absorb inserts without renumbering; low stakes, the merge renumbers anyway. |
| S-005 | HYBRID | 65 | A's per-behaviour table, B's existing-tests-to-update table, C's three fault-injection points. |
| S-006 | B | 60 | Runnable shell observations with pass conditions; keep A's AC-to-test mapping beside them. |
| S-007 | B | 55 | Root-cause column ties each mitigation to its cause; otherwise comparable. |
| S-008 | HYBRID | 75 | B's mirrored read-only skill script; A's module split, rules constants, contract version; C's outcome fields in verify output. |
| S-009 | A | 60 | Operation registry, per-group refs and shared safety ref; read operations load no ref (B). |
| S-010 | B | 60 | Distinct `refs/commit-step.md` avoids two different `refs/commit.md` files across skills. |
| S-011 | HYBRID | 70 | B's `commits.md` sidecar plus C's `prepared` line before each attempt; no journal directory, no lock. |
| S-012 | A | 55 | D7 (merge removed) and D8 (package-only commit) settle the seed's two hardest tensions. |
| S-013 | HYBRID | 55 | A's single-source, extension, version NFRs; B's size budgets; C's bounded execution and honest trust boundary. |
| C-001 | A | 60 | Existing advertised surface (`git.md:14`, `:17`) minus push, pull, merge, plus submodule operations. |
| C-002 | A | 55 | One-turn path for the person's own message; today `commit` without `--smart-commit` has no source. |
| C-003 | B | 60 | Prefix rule plus a refusal with no replayable argv; A's dry run hands argv to unauthorized callers. |
| C-004 | HYBRID | 65 | B's person-origin check at Wave 0 is primary; A's static test catches templates inserting the flag. |
| C-005 | HYBRID | 65 | A's Q8a, R0, L0 positions plus C's reconcile before task selection and the all-complete stop. |
| C-006 | HYBRID | 60 | A's before-step-6 placement and reasons minus `dirty`; B's `helper-missing`; per-path checks move to the boundary. |
| C-007 | A | 55 | Two codes keep each STOP row's product and ledger columns single-valued. |
| C-008 | HYBRID | 70 | B's per-path `foreign-change` on the Q0 pin plus C's check against the last reviewed tree. |
| C-009 | B | 75 | `HEAD^{tree}` must equal `pre_tree`; catches a hook that rewrites, re-adds and exits zero. |
| C-010 | HYBRID | 75 | B's trailers and recover mode; C's prepared line before attempt, start-generation key, fault-injection tests. |
| C-011 | B | 60 | Keep the Q0 pin until the boundary's terminal line; recovery and `foreign-change` need it. |
| C-012 | HYBRID | 60 | A's ten types, verdict trailer, 72-character total; B's `Implement-Plan:`; one `Implement-Boundary:` key trailer. |
| C-013 | B | 60 | Temporary file outside the tree; A's in-package message file is committed clutter. |
| C-014 | HYBRID | 65 | C's independent fields with unset-versus-false; A's single action state derived by fixed precedence. |
| C-015 | HYBRID | 65 | B's clean plus remote-tracking containment; C's post-commit gitlink revalidation; A's one-path commit set. |
| C-016 | C | 60 | Explains the route and that `archive` writes without `--apply`; no extra operation. |
| C-017 | B | 65 | Fixed set plus `origin/HEAD`; a notice, not a block, when unset (2.47.3 fetch never creates it). |
| C-018 | HYBRID | 60 | B's preconditions, argv, result and undo hint plus C's statement of whether HEAD, index, worktree changed. |
| C-019 | HYBRID | 70 | A's routing-row rewrite and fixture list, B's classification rows, plus amending `refs/retry.md:504`. |
| C-020 | B | 70 | Plugin build copies only the plugin tree; a mirrored script ships everywhere with `helper-missing`. |
| C-021 | C | 80 | Verified: a file named `:(glob)*` staged everything; `git --literal-pathspecs` staged only it. |
| X-001 | HYBRID | 80 | Flag (A, B); person-origin at Wave 0 (B); static scope test (A); quoted run record and revocation (C). |
| X-002 | A | 90 | The seed forbids merge in `/sc:git`; A removes it and rewrites the routing row. |
| X-003 | A | 75 | Fixture lists only `--smart-commit` (`:327`); `--interactive`'s only example was the merge. |
| X-004 | B | 70 | Sidecar leaves the resume regex and archive parser untouched; the archive digest excludes `artifacts/`. |
| X-005 | A | 65 | Stage all `.dev/tasks`, commit only the run's package; no liveness signal exists for C's rule. |
| X-006 | B | 65 | No retroactive commits; only tasks completed in a flagged run get a boundary. |
| X-007 | HYBRID | 60 | Never automatic and show hook paths and diff (C); retry only in a new flagged run (A). |
| X-008 | HYBRID | 80 | Agent runs literal git writes the guard sees (A, B); helper read-only; C's verification as a separate call. |
| X-009 | A | 60 | Branch management is advertised today (`git.md:17`); clean-tree, no-force guards keep risk low. |
| X-010 | C | 60 | Defaulting to read-only status is harmless; unknown operations still stop. |
| X-011 | A | 55 | Seed criterion names the guide (`:277-278`); practice favours `standard`, but no code reads it. |
| X-012 | A | 65 | One non-nested submodule; report nested as not inspected; never recursive. |
| X-013 | B | 70 | Fast-forward-only update; refuses ahead or diverged; precedence from the C-014 action state. |
| X-014 | B | 60 | Changed: no downstream gate checks publication; refusal errs safe; print the last-fetch time. |
| X-015 | C | 65 | Admits the clone's network effect (B, C) and refuses when the config URL differs from `.gitmodules`. |
| X-016 | A | 85 | Check before step 6 fits "no ledger writes"; B contradicts `SKILL.md:72`. |
| X-017 | HYBRID | 65 | Keep B's `pre_tree`; reword: objects only, as Q0 does (`SKILL.md:124`); no ref, index or worktree writes. |
| X-018 | A | 70 | Plain 72-character total check; B's regex admits 81. |
| X-019 | B | 80 | `<pkg-dir>` for the task package; A overloads `<pkg>`. |
| X-020 | B | 85 | No commit-msg hook installed here; the helper must validate the header itself. |
| X-021 | NONE | 75 | All misstate tracked files; correct the fact, keep settings-only automatic staging per the project rule. |
| A-001 | NONE | 75 | Verified: one absent path makes `git add` exit 128 and stage nothing; the planner must skip absent paths. |
| A-002 | HYBRID | 60 | All equally right: FINAL reads current files (`refs/qa.md:311`); add a pinning test. |
| A-003 | HYBRID | 70 | Flag checked once at Wave 0, recorded as a run line; covers in-chat Ruling turns and compaction; resume needs it again. |
| A-004 | HYBRID | 60 | Never claim freshness: B's refusal errs safe; print last-fetch time (C's honesty); no fetch. |
| A-005 | NONE | 70 | Unverified everywhere and latent here; needs a pinned pre-commit framework test under `--only`. |
| A-006 | HYBRID | 60 | All equally right; no test pins the K3 wording. |
