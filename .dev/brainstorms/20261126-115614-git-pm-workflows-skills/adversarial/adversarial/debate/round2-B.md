# Round 2 — Rebuttal for Variant B (analyzer; root cause and evidence for architecture)

"Verified" means I re-read the line or re-ran the check read-only in this worktree in this round. Two git behaviours were tested in a throwaway repository under `/tmp` (git 2.47.3), removed afterwards. Two git-scm documentation pages were read for E3. Nothing in the repository was changed. `<name>` is the package name, as in B's alias table.

## Response to criticisms

| # | Criticism of B (raised by) | Response |
|---|---|---|
| 1 | Keeps `merge` against the seed constraint (X-002, C-001, C-019; A, C, diff) | **Conceded in Round 1, kept conceded.** Adopt A's D7: drop the merge class, its preview and `git-too-old`; rewrite the routing row, which today says "branch or merge operations" (`HOW-WE-WORK.md:293`). |
| 2 | False reason for keeping `--interactive` (X-003; A, C, round2-A) | **Concede.** Line 327 of the S23 fixture lists only `--smart-commit`. C wants to keep the flag for clarification, but its only example is the merge (`git.md:72-77`), so it goes with merge. |
| 3 | Wave 0 "after step 6" contradicts "before the ledger is created" (X-016, C-006; A, C) | **Concede.** Order for the merged spec: step 5 → commit preflight (read-only; STOP `E-COMMIT-PRECONDITION` writes nothing) → step 6 opens or creates the ledger (`SKILL.md:72`, verified) → run line (A-003) → reconcile (C-010) → task selection. |
| 4 | "Writes nothing in the repository" is false (X-017; A, C) | **Concede the wording.** The private-index `read-tree`/`add`/`write-tree` writes loose objects, exactly as Q0 does (`SKILL.md:124`, verified). Correct claim: no ref, user index, working tree or config writes. The boundary pin (E2) is a literal `git update-ref` that the agent runs, as Q0 does, not the helper. |
| 5 | Header regex admits 81 characters (X-018; A, C) | **Concede.** Check the total header length (72 or fewer), not a tail quantifier. |
| 6 | Commits all of `.dev/tasks` (X-005; A, C) | **Conceded in Round 1.** WC-9 stages `.dev/tasks` but commits `--only -- <paths>` (`WORKER-CONTRACT.md:43`, re-verified). Commit only the run's package directory (A's D8). E5 shows this composes with literal pathspecs. |
| 7 | `complexity: standard` is not in the guide (X-011; A, C) | **Concede, low stakes.** The guide lists `category` values including `version-control` and `complexity: simple, moderate, advanced, high` (guide `:270-284`, verified). The seed's success criterion names the guide. The gap between guide and practice (8 commands use `standard`, per A) is a follow-up, not something this spec should settle. |
| 8 | One `E-COMMIT-REFUSED` row splits its own columns (C-007; A, round2-A) | **Concede.** Two codes: `E-COMMIT-PRECONDITION` (no product write, no ledger write) and `E-COMMIT-REFUSED` (no next task; sidecar gets a terminal line). |
| 9 | Recovery accepts any HEAD with a matching parent and trailers and cannot tell the prepared candidate from another commit (C-010, S-011; C, round2-A) | **Concede.** B never persisted `pre_tree`, so recovery could not compare content. Adopt the `prepared` line and the start-generation key. A's success predicate is itself broken for managed runs, though (E1), so the resolution below corrects it. |
| 10 | The "current message starts with `/sc:implement`" test fails at the next boundary after an in-chat Ruling (A-003; A, C, round2-A N6) | **Conceded in Round 1.** Verified the mechanism: after a HALT, a clear user confirmation lets the executor record the Ruling and continue, "T{i+1}? Yes" (`refs/qa.md:247-248`). Bind the grant once at Wave 0 (resolution below). |
| 11 | A resume re-runs Q7b with no review after a hook rewrite (X-007; C, round2-A) | **Conceded in Round 1.** Never retry automatically. A retry happens only in a new flagged run whose Wave 0 prints the diff of the hook-changed paths before any attempt. |
| 12 | Refusing an unpublished pointer commit blocks a valid local order and trusts stale refs (X-014, A-004; A in Round 1, C) | **Counter, with one concession.** No downstream step checks publication: `pr_submit` has exactly one submodule line, a halt on conflict (`conflicts.py:733`), and `.github/` has no `submodule` match (both verified). The one submodule points to a third-party repository (`.gitmodules:3`, verified), so a local commit inside it can probably never be published, and a pointer to it would break `submodule update` in every other clone. The research's push order still holds: the person pushes the submodule first. **Concession:** stale refs can give a false "published" after a remote rewrite. So the report prints the last-fetch time and never presents publication as a fresh fact. A now votes the same way. |
| 13 | No literal-pathspec rule, and nothing for absent `files=` paths (C-021, A-001; A, C) | **Concede.** Run every add and commit as `git --literal-pathspecs ...`. The guard still classes it as `COMMIT`, because it skips other global options (`launch-level-guard.sh:699`) before the subcommand table (`:713`), verified. The planner moves absent paths to `skipped why=absent` before building the add call (A's N1). |
| 14 | `foreign-change` misses edits made after the review (C-008; C) | **Concede.** Also compare S with the last compliant review's tree. That tree's ref is deleted at `complete` today (`SKILL.md:129`), so its lifetime moves to the boundary's terminal line, like the Q0 pin. |
| 15 | `/sc:git commit` without `--smart-commit` has no message source (C-002; A) | **Concede.** Adopt A's `--message`, written to a file outside the tree and passed with `-F`. |
| 16 | `update --init --recursive` widens the network effect (X-012; A) | **Concede.** Never recursive. Nested submodules are reported as not inspected. |
| 17 | Nothing defined for a bare `/sc:git` (X-010; C) | **Concede.** Default to read-only `status`, as C says. |
| 18 | The header spends characters on task ids, and only six types (C-012; A) | **Partly concede.** Move the task ids to the body and trailers. Adopt A's ten types. Keep `Implement-Plan:`, and add `Implement-Boundary:` (C-010). |
| 19 | Length and repetition (S-001; A) | **Concede.** |
| 20 | FR-037b says the skill "never works around" the guard's submodule denial (new, self-raised) | **Concede, new evidence E6.** The helper's internal git reads are invisible to the guard, so the claim was too strong. |

## Updated assessment of A and C

### A

**Steelman.** A turns every rule into something with one source and one test. That covers the registry and its resolve test, `rules.py` with its parity test, the contract-version field, and the scope test for the flag string. Its Round 2 concessions (helper placement, ledger grammar, dry run, coarse `dirty` check, retroactive commits, no-remote contradiction) remove every structural defect I raised. Its six resolutions are the most concrete text on the table.

**Arguments that changed my mind.**
- **C-019 / N10.** `refs/retry.md:504` says a Ruling after a halt "accepts the tree as it stands ... (no commit follows it)" (verified). With `--commit-tasks` on, a commit does follow it. None of the three variants listed this. Adopt it.
- **X-015.** A gives the remote-identity rule a mechanism: refuse when `submodule.<name>.url` in the local config differs from `.gitmodules`, using two `config --get` reads. My vote moves from C to HYBRID.
- **C-014.** C's independent fields, plus one action state derived by a fixed precedence, so that each refusal reads one value. My vote moves from C to HYBRID.
- **C-007, X-011, C-002.** These are listed above as concessions.

**Arguments that did not change my mind, or that need correction.**
- **A's C-010/S-011 success check, `HEAD^{tree} = pre_tree`, is self-referential in managed runs (E1).** C foresaw this in Round 1 (concession 7, "non-self-referential digest"). The corrected predicate is in the resolution below.
- **N5 ("the ref is missing in every repository set up with `remote add` and `fetch`") holds only up to git 2.47 (E3).** The C-017 conclusion still holds, for a better reason: `origin/HEAD` can be missing or stale, so it may add a name to the protected set but never stand in for the fixed names.
- **The A-003 run line "in Wave 0 step 1"** would break the no-write preflight that A itself won on X-016. It belongs after step 6.
- **`line="<invocation line as typed>"`** has no bound. An inline prompt can be long and can hold quotes and newlines. Record the option prefix plus the source token instead (`inline:<hash8>`, from the slug rule at `SKILL.md:68`).
- **The pending boundary in A's reconcile depends on objects nobody pins (E2), and row 1 deletes the Q0 pin on any resume (E7).** The retry must rest only on the prepared line and a pinned `pre_tree`.

### C

**Steelman.** C treats the boundary as a contract that has to survive interruption. It writes a record before the attempt, uses a start-generation key, defines closed outcomes including `uncertain`, injects faults at five points, handles paths literally, never repairs anything on its own and states its trust boundary honestly. It concedes its two largest defects: the hidden commit (X-008) and nested scope (X-012).

**Arguments that changed my mind.**
- **C-010.** A record written before the attempt is the only way to tell "this candidate was committed" from "a commit with these trailers exists". This is my concession 9.
- **U-017, extended.** A post-commit record cannot be part of its own commit. The converse is the trap in E1: the `prepared` record is part of its own commit, so the candidate fingerprint cannot cover it.
- **C-021.** I tested that `--literal-pathspecs` composes with a directory commit (E5). My confidence rises.
- **X-007** (renewed review before a retry) and **C-016** (`archive` writes even without `--apply`) stand.

**Arguments that did not change my mind.**
- **X-014, "readiness unknown, do not block".** C assigns the publication check to `/sc:pr-submit`, which has none (E9).
- **C-017, "verified policy, block when unknown".** No variant gives a mechanism for verifying the policy, and E3 shows that a missing or stale `origin/HEAD` is common. Blocking would refuse ordinary repositories for a local, undoable commit.
- **The lock (NFR-002).** The boundary spans three or more separate Bash calls, and the ledger rule is "there is no lock" (`refs/ledger.md:149`, verified). A lock that is never deleted for being old turns one crash into a permanent block.
- **Journal directory and versioned request.** One append-only sidecar plus a contract version gives the same guarantees with fewer states.
- **X-005, live-writer detection.** No liveness signal exists. Committing only the run's own package removes the need for one.

## New evidence

1. **E1 — A's success predicate fails on every managed boundary.**
   - Under X-005, the commit set includes the run's package directory. So `<pkg-dir>/artifacts/commits.md` is committed, and the `prepared` line, written before `git add`, sits inside the commit it describes.
   - If `pre_tree` is computed before that line is written, the committed `commits.md` differs and `HEAD^{tree} ≠ pre_tree` every time: a false `hook-rewrite-committed` on every managed boundary. If it is computed after, the line cannot hold the hash, because a file cannot name the hash of a tree that contains it.
   - Fix: `pre_tree` covers the commit set minus the sidecar file. Verify then checks four things:
     - `git diff --quiet <pre_tree> HEAD -- <S minus sidecar>`;
     - `git diff --name-only <parent> HEAD` lists only paths in S;
     - the sidecar's blob in HEAD equals `git hash-object` of the working-tree sidecar, before the terminal line is appended;
     - `HEAD^` = parent, and HEAD carries the key trailer.
   - Legacy runs never stage the sidecar (`refs/ledger.md:3`), so for them the check reduces to A's.
2. **E2 — `pre_tree` must be pinned.**
   - It is an unreferenced tree object. Q0 pins its own tree "so `git gc` cannot prune it before resume" (`SKILL.md:125-126`, verified).
   - Pin `pre_tree` as `refs/<name>/implement/<slug>/boundary/<hex12>`, and delete the pin with the terminal line. `update-ref` outside `HEAD`, `--stdin` and `refs/heads/*` is not classed `COMMIT` (`launch-level-guard.sh:714-717`, verified).
   - The final summary lists any leftover boundary pin with its `git update-ref -d` line, as `SKILL.md:129` does for sweep refs.
   - A retry when HEAD = parent needs no object: rebuild the tree the same way and compare the hashes.
3. **E3 — A's N5 is version-specific.**
   - The git-config documentation for 2.48.0 defines `remote.<name>.followRemoteHEAD` with the default `create`, which creates `remotes/<name>/HEAD` when it is missing locally "but will not touch an already existing local reference". The 2.47.0 page does not show the setting. So on git 2.48 or later, `remote add` plus `fetch` does set `origin/HEAD`.
   - The ref stays absent when it was never fetched, on 2.47 or earlier, or with `never`. It stays stale once it exists: here it names `origin/master` while the GitHub default is `integration` (U-006).
   - Conclusion: use the fixed names always. `origin/HEAD` only adds a name. A missing ref is a notice, not a block.
4. **E4 — Commit hooks have rewritten hash-pinned task evidence in this repository before, and none of the three variants plans for it.**
   - `.pre-commit-config.yaml:10-25` (verified) excludes named `.dev/tasks` files from `trailing-whitespace` and `end-of-file-fixer` under "Issue 501". One of them is `.dev/tasks/archive/.../source.md`, labelled a "hashed source-input snapshot". `mixed-line-ending --fix=lf` (`:34-36`) applies to all of `.dev/tasks`.
   - A boundary commit of the package exposes `<slug>.md` and `source.md`. Their bytes are pinned by the `PLAN:` line, so any later difference stops the run with `E-PLAN-CHANGED` (`refs/managed-workspace.md`, PLAN rule, verified).
   - Required fix: after any hook outcome, verify recomputes both hashes. On a mismatch it refuses with `hook-rewrite-pinned`, names the file and repairs nothing. This is also why `pre_tree` in E1 must cover the evidence paths and not only the product paths.
5. **E5 — `--literal-pathspecs` and the package-directory commit fit together.**
   - In `/tmp` (git 2.47.3), `git --literal-pathspecs add -- pkg b` staged every file under `pkg/`. `git --literal-pathspecs commit --only -- pkg b` committed exactly those files and left another staged file staged.
   - `git diff --quiet <private-index tree> HEAD -- b` worked tree-to-commit, which is the comparison E1 needs.
   - Because `:(exclude)` magic is off under `--literal-pathspecs`, the sidecar cannot be excluded by pathspec. That is another reason to handle it by comparison (E1) rather than by exclusion.
6. **E6 — The guard cannot see the helper's reads. This is a B concession.**
   - The helper path `.../sc-git-protocol/scripts/...` never matches `( |/)git(-[a-z][a-z-]*)? ` (`launch-level-guard.sh:555`), while a `git submodule ...` command typed by the agent is `UNKNOWN` and denied at every level (`:720`, `:724`, `:816`; all verified).
   - So in a launched session the helper could run `git status --ignore-submodules=none`, which starts git inside initialized submodules. That is the issue-547 exposure the sweep avoids (`probes.py:64-66`, verified).
   - Fix: `/sc:implement`'s preflight and verify use `--ignore-submodules=all`. They refuse gitlinks in S by mode `160000` anyway. Only the person-invoked `/sc:git status` and `submodule status` use `=none`. The spec says plainly that the guard does not gate the helper's reads.
7. **E7 — Row 1 deletes the pins on any resume.**
   - "Skip. Delete the Q0 pin and checkpoint refs if they still exist ... Also delete the task's `r<k>-<j>` refs" (`refs/ledger.md:157`, verified), whether or not the run is flagged.
   - So an unflagged resume strips a pending boundary's Q0 pin and reviewed-tree refs. The retry must depend only on the `prepared` line and the boundary pin, and row 1's amendment must say that it never deletes a `boundary/*` pin.
8. **E8 — A Ruling must stay informed when commits are on.**
   - Before asking for a Ruling, the executor must explain the "current outcome, proposed acceptance, reason and cost-if-wrong" (`refs/qa.md:254`, verified).
   - With `--commit-tasks` on, the cost-if-wrong must say that the accepted task will be committed at the next boundary. The Ruling still authorizes no commit (`refs/ledger.md:239`, verified).
9. **E9 — No downstream publication gate exists.** `conflicts.py:733` is the only submodule logic in `pr_submit`, `.github/` has no submodule reference, and the submodule URL is third-party (`.gitmodules:3`).
10. **E10 — Tracked dev-copy files.** `git ls-files .claude/` prints exactly `.claude/cache/sc-recommend-lookup.yaml` and `.claude/settings.json` (re-verified). This supports A's N13 for X-021.

## Proposed resolution for the six open points

### A-003 — authorization lifetime: accept A's proposal, with five amendments

The merged spec should say:
1. **Grant.** `--commit-tasks` counts only as a standalone token in the option prefix (`SKILL.md:57-59`) of a message the person typed that starts with `/sc:implement`. It is checked once, in Wave 0 step 1 (B). Otherwise STOP `E-COMMIT-PRECONDITION reason=not-person`, with no write. A's static test (no other primitive contains the string) stays as a second check.
2. **Run line, written right after step 6** (amendment: not in the read-only preflight): `run <n>: commit-tasks=<on|off> at=<ISO-8601> args="<option prefix>" source=<path|inline:<hash8>>`. It is written when the flag is present, and also when the sidecar exists but the flag is absent. A run without the flag on a ledger with no sidecar writes nothing (amendment: a bounded record instead of the full typed line).
3. **Lifetime.** The latest `run` line governs that run only. The run includes the in-chat Ruling continuation (`refs/qa.md:248`) and compaction, because the executor re-reads from disk (`SKILL.md:118`). A resume is a new run (`SKILL.md:76`) and needs the flag again.
4. **Informed continuation** (amendment): when the run line is `on`, every Ruling request states the commit consequence (E8). `refs/retry.md:504` drops "(no commit follows it)" for flagged runs.
5. **Pending boundaries are disclosed** (amendment): Wave 0 of a flagged run lists every `prepared` boundary with no terminal line before it attempts anything, so the flag the person typed covers boundaries they can see.
6. **Revocation.** Plain words can only narrow authority: `run <n>: commit-tasks=off reason=revoked`, appended before the next boundary. Rulings neither grant nor revoke.
7. **Mechanical check.** `preflight` refuses `not-authorized` unless the latest `run` line says `on`.
8. **Tests.** A's three tests, plus a fixture where a HALT and an in-chat Ruling continue to a committed boundary.
9. **Residual** (as A): an agent that resumes in a new session without running Wave 0 would read a stale `on`. The `args=` record makes this auditable, but nothing mechanical prevents it.

### C-010 — crash between the commit and its record: accept A's structure, replace its success predicate

The merged spec should say:
1. **Key.** `<slug>/<ids>/<first 12 hex of the first member's start sha>`. The start sha is reused on resume (`SKILL.md:122`, verified), and a restarted task gets a new start line, so it gets a new key.
2. **Before `git add`:**
   - build `pre_tree` from a private index: `read-tree <parent>`, then `git --literal-pathspecs add -A -- <S minus sidecar>` from the working tree, then `write-tree`;
   - pin it (E2);
   - append `T<ids>: commit prepared key=<key> parent=<40-hex> pre_tree=<40-hex>`.
3. **Trailers.** `Implement-Plan:`, `Implement-Task:` (one per member, with A's verdict) and `Implement-Boundary: <key>`.
4. **Success.** The four checks of E1, plus the pinned-file check of E4. Then append `commit sha=<40-hex> key=<key>`, and delete the boundary pin, the Q0 pins and the reviewed-tree refs.
5. **Reconcile.** It runs every run, flagged or not, after step 6 and before task selection and the all-complete stop. For each `prepared` line with no terminal line:
   - the success checks hold → append `recovered sha=`;
   - HEAD = parent → the boundary is pending:
     - a flagged run retries only if a fresh rebuild hashes to the recorded `pre_tree`; otherwise it appends `refused reason=candidate-changed`, which is terminal;
     - an unflagged run prints the pending boundary and leaves it alone;
   - anything else → append `uncertain` and STOP `E-COMMIT-REFUSED reason=uncertain`, printing the parent, HEAD and key. Nothing is repaired, and there is no history walk (fail closed).
6. **Tests.**
   - C's five interruption points (before `prepared`, after `prepared`, after staging, after the commit but before the terminal line, after the terminal line), each followed by resuming twice: at most one commit per key.
   - A managed fixture that must not produce a false `hook-rewrite-committed` (E1).
   - A `git gc --prune=now` between the crash and the resume (E2).
   - A person's commit on top of the boundary gives `uncertain`.
   - A hook that rewrites `source.md` gives `hook-rewrite-pinned` (E4).
7. No lock, no journal directory, no request schema.

### C-015 — when a pointer commit is allowed: accept A's proposal, with two clarifications

Accept A's rules 1-7, which combine B's clean-module and remote-tracking containment, C's post-commit gitlink check, A's one-path commit set and one-level scope. Two clarifications:
- The reads inside the submodule use the `--no-optional-locks -c core.fsmonitor=false` seam and run only on the person's typed line (E6).
- In a launched session, the pointer commit's `git add` and `git commit` are classed `COMMIT`, so they are allowed only at `full --submit`. The guard does not gate the helper's reads, and the spec says so.

### C-017 — protected branches elsewhere: accept A's proposal, with the E3 correction

The protected set is always `master`, `main` and `integration`, plus the target of `refs/remotes/origin/HEAD` when it resolves. Inside a submodule, the target is read from the submodule's own refs. `origin/HEAD` adds a name and never replaces or removes one.

When the ref is unset, print A's notice and its `git remote set-head origin <branch>` hint, then proceed. There is no block and no network call. A detached HEAD is refused everywhere.

The stated reason is that the ref can be absent (never fetched, git 2.47 or earlier, `never`) or stale (it is never updated once created). It is not that the ref is always missing. The residual stays: shared branches with other names are protected only by the server.

### S-011 — where commit state lives: accept A's proposal, with the E1, E2 and E7 changes

- **Location.** `commits.md` in the ledger directory:
  - legacy `.dev/implement/<slug>/commits.md`, never staged;
  - managed `<pkg-dir>/artifacts/commits.md`, staged with `.dev/tasks`.
- **Line forms.** A's line forms, with the `run` line bounded as in A-003. The closed reason list gains `candidate-changed`, `hook-rewrite-pinned`, `not-authorized` and `uncertain`. Each form has one regex, parsed by the helper and pinned by a parity test.
- **Unchanged.** The ledger grammar, `refs/ledger.md:127`, `E-LEDGER-CORRUPT` and `archive_workspace.py` stay as they are. The archive digest covers plan, source and the `files=` paths only, and the archive script checks `artifacts/` only for being a real directory (verified).
- **Self-description.** The `prepared` line is committed with its boundary, and the sidecar is checked by blob comparison (E1). The terminal line goes into the next boundary commit. The last one stays staged, and the final summary says so.
- **Pins.** The Q0 pin, the last reviewed-tree ref and the boundary pin are deleted after the terminal line. Row 1 never deletes a `boundary/*` pin (E7). Leftover pins are listed in the final summary.

### X-014 — a pointer to a commit that may not be published: accept A's proposal

- `commit-pointer` refuses `submodule-unpublished` when the target is on no remote-tracking branch of the submodule, according to local refs.
- It refuses `detached-new-commits` when the target is on no branch at all, and prints the `git -C <path> switch -c <name>` hint.
- The message gives the last-fetch time, read from the file time of `git -C <path> rev-parse --git-path FETCH_HEAD`, or "never". It says `/sc:git` never pushes or fetches.
- A success report prints "on `<remote-ref>` as of last fetch `<time>`".
- No override flag.
- Why: no downstream gate (E9), a third-party submodule, and the refusal errs on the safe side.

## Per-point votes

| Point | Winner | Confidence | Reason |
|---|---|---|---|
| S-001 | A | 55 | Balanced density with verified citations; B's 522 lines repeat evidence; C omits test-pinned facts. |
| S-002 | B | 65 | Resolve column ties each alias to a repository file; A overloads `<pkg>`; C's single letters are opaque. |
| S-003 | HYBRID | 60 | A's verified baseline-facts table plus B's root causes: facts state what holds, causes explain which invariants constrain design. |
| S-004 | A | 50 | Gapped blocks absorb inserts; low stakes because the merged spec renumbers anyway. |
| S-005 | HYBRID | 70 | A's per-behaviour test table, B's existing-tests-to-update table, C's five fault-injection points. |
| S-006 | HYBRID | 60 | B's runnable shell observations, each mapped to A's test ids; C's prose criteria cannot be run. |
| S-007 | B | 55 | Root-cause column ties each mitigation to its cause; otherwise the three tables are comparable. |
| S-008 | HYBRID | 75 | B's mirrored read-only skill script; A's module split, rules constants, contract version; C's closed outcome fields. |
| S-009 | HYBRID | 60 | A's registry, per-group refs and shared safety ref; B's rule that read operations load no ref. |
| S-010 | B | 60 | A distinct `refs/commit-step.md` avoids two different `refs/commit.md` files in two skills. |
| S-011 | HYBRID | 75 | B's `commits.md` sidecar; C's prepared line before attempt; pre_tree excludes the sidecar and is pinned (E1, E2). |
| S-012 | A | 55 | D7 (merge removed) and D8 (package-only commit) settle the seed's two hardest tensions explicitly. |
| S-013 | HYBRID | 55 | A's single-source and version NFRs, B's size budgets, C's integrity, bounded execution and honest trust boundary. |
| C-001 | A | 60 | Today's advertised surface (`git.md:14`, `:17`) minus push, pull, merge, plus three submodule operations. |
| C-002 | A | 55 | `--message` gives the person's own words a one-turn path; `commit` without `--smart-commit` has no source today. |
| C-003 | B | 60 | Person-typed prefix plus a refusal that prints no replayable argv; A conceded its dry run. |
| C-004 | HYBRID | 70 | B's person-origin check once at Wave 0 is primary; A's static string test catches templates inserting the flag. |
| C-005 | HYBRID | 65 | A's Q8a, R0, L0 positions plus C's reconcile before task selection and the all-complete stop. |
| C-006 | HYBRID | 65 | A's before-step-6 placement and reasons minus `dirty`; B's `helper-missing`; per-path checks move to the boundary. |
| C-007 | A | 60 | Two codes keep each STOP row's product and ledger columns single-valued; B's single row split them. |
| C-008 | HYBRID | 70 | B's per-path `foreign-change` on the Q0 pin plus C's reviewed-increment check on the last reviewed-tree ref. |
| C-009 | B | 75 | Committed content compared with pinned pre_tree catches rewrite-and-re-add exiting zero; A misses it; C names no check. |
| C-010 | HYBRID | 80 | B's trailers and recover mode, C's prepared line and start-generation key, corrected non-self-referential success check (E1). |
| C-011 | B | 65 | Keep pins until the boundary's terminal line; recovery, foreign-change and the increment check need them. |
| C-012 | HYBRID | 60 | A's ten types, verdict trailer and 72-character total; B's `Implement-Plan:`; C's boundary-key trailer. |
| C-013 | B | 60 | Temporary message file outside the tree; A's in-package file would enter the next boundary commit. |
| C-014 | HYBRID | 65 | C's independent fields with unset versus false; A's single action state derived by fixed precedence. |
| C-015 | HYBRID | 65 | B's clean plus remote-tracking containment; C's post-commit gitlink check; A's one-path commit set, one level. |
| C-016 | C | 60 | Routes to `/sc:worktrees` and notes `archive` writes without `--apply`; no extra operation needed. |
| C-017 | HYBRID | 65 | B's fixed set plus origin/HEAD per repository; A's notice, not a block, when unset; origin/HEAD only adds names. |
| C-018 | HYBRID | 60 | B's preconditions, argv, result and undo hint plus C's statement of whether HEAD, index and worktree changed. |
| C-019 | HYBRID | 70 | A's routing-row rewrite and fixture list, B's classification rows, plus amending `refs/retry.md:504`. |
| C-020 | B | 70 | The plugin build copies only the plugin tree; a mirrored skill script ships everywhere, with `helper-missing`. |
| C-021 | C | 80 | Verified: `--literal-pathspecs` disables pathspec magic yet still commits a literal directory; only C required literal handling. |
| X-001 | HYBRID | 80 | Flag (A, B); person-origin check at Wave 0 (B); static scope test (A); run record and revocation (C). |
| X-002 | A | 90 | The seed forbids merge in `/sc:git`; A removes it and rewrites the routing row; B conceded. |
| X-003 | A | 75 | Fixture `:327` lists only `--smart-commit`; `--interactive`'s only example is the merge; B's reason was false. |
| X-004 | B | 75 | Sidecar leaves the resume regex and archive parser untouched; the archive digest covers only plan, source, `files=` paths. |
| X-005 | A | 70 | Stage all `.dev/tasks`, commit only the run's package, as WC-9 stages then commits `--only`. |
| X-006 | B | 65 | No retroactive commits; only tasks completed in a flagged run get a boundary. |
| X-007 | HYBRID | 65 | Never automatic and show hook-changed paths (C); retry only in a new flagged run after Wave 0 prints their diff (A). |
| X-008 | HYBRID | 80 | Agent runs literal git writes the guard sees (A, B); helper read-only; C's verification as a separate call. |
| X-009 | A | 60 | Branch management is advertised today (`git.md:17`); clean-tree and no-force guards keep the risk low. |
| X-010 | C | 60 | Defaulting to read-only status is harmless; unknown operations still stop. |
| X-011 | A | 55 | The seed names the guide, whose lists hold `moderate` and `version-control`; practice drift is a follow-up. |
| X-012 | A | 65 | One non-nested submodule; report nested ones as not inspected; never recursive. |
| X-013 | B | 75 | Fast-forward-only update refuses ahead or diverged modules; A had no ancestry check; C refuses the common case. |
| X-014 | B | 65 | No downstream gate checks publication (E9); the submodule is third-party; refusal errs safe and prints last-fetch time. |
| X-015 | HYBRID | 65 | B and C admit the clone's network effect; A's concrete refusal when the config URL differs from `.gitmodules`. |
| X-016 | A | 85 | Preflight before step 6 fits "no ledger writes"; B contradicted `SKILL.md:72` and conceded. |
| X-017 | HYBRID | 65 | Keep B's private-index pre_tree; reword: object writes only, as Q0 does; no ref, user-index, worktree or config writes. |
| X-018 | A | 75 | A plain 72-character total check; B's regex admits 81 characters. |
| X-019 | B | 80 | `<pkg-dir>` names the task package; A overloads `<pkg>`. |
| X-020 | B | 85 | Verified: no pre-commit or commit-msg hook installed, hooksPath unset; the helper must validate the header itself. |
| X-021 | NONE | 80 | All misstate the tracked files (a cache yaml is tracked); correct the fact, keep settings-only automatic staging. |
| A-001 | NONE | 75 | One absent path makes `git add` exit 128 and stage nothing (A's N1); the planner must skip absent paths. |
| A-002 | HYBRID | 65 | All three right today: the FINAL reads current files (`refs/qa.md:311`); add a test that pins it. |
| A-003 | HYBRID | 75 | B's person check once at Wave 0; A's run line after step 6; C's revocation and new-session rule; informed Rulings. |
| A-004 | HYBRID | 60 | Never claim freshness: B's refusal errs safe; print last-fetch time (C's honesty); no fetch. |
| A-005 | NONE | 70 | Unverified everywhere and latent here; needs a pinned pre-commit framework test under `--only` with unstaged edits. |
| A-006 | HYBRID | 65 | All three right: no test pins the K3 wording; still run worker-contract regressions. |
