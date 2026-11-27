# Round 1: Advocate for Variant B (persona: analyzer)

Repository facts below were re-read read-only in this worktree on 2026-11-26. "Verified" means I read the line or ran the read-only command myself in this round.

## Position summary (1-3 sentences)

Variant B has the strongest root-cause-driven design for the risky half of the work. It makes the commit a literal Bash call the guard can see, uses a read-only helper script that ships in the plugin mirror, and adds three integrity checks built on existing pins: `pre_tree` for hook rewrites, `foreign-change` for the person's own edits, and trailer-based crash recovery. It keeps commit state in a sidecar, so the closed ledger grammar is untouched. B is wrong, though, on merge (it breaks the seed constraint), on the `--interactive` test claim, and on committing all of `.dev/tasks`, and it has several internal defects. The merged spec should take B's `/sc:implement` commit mechanics and hook and crash handling, and take most of A's `/sc:git` surface.

## Steelman (one sub-heading per opposing variant)

### Variant A

The strongest case for A is maintainability with fewer moving parts per decision:
- One operation registry (FR-006, FR-008) and one constants file, `rules.py`, with a parity test against the prose copies (FR-013, NFR-003). Each safety rule therefore has one source, and adding an operation follows a checklist.
- The helper plans the exact argv and "the executor never edits the argv" (FR-061). This removes agent improvisation at the one step where the research says prompt rules fail.
- A gets the seed right on merge: D7 removes it and rewrites the routing row (FR-017) and the classification row (T-14).
- A gets the evidence rule right. D8 and FR-062 stage all of `.dev/tasks` but commit only the run's package directory. That matches the worker contract's split between what is staged and what is committed: "stages with `git add -- <paths>` plus `.dev/tasks`, commits with `git commit --only -- <paths>`" (`WORKER-CONTRACT.md:43`, verified).
- T-05 tests the `--only` assumption instead of trusting it.
- The baseline-facts table has 27 entries, nearly all confirmed by the diff analysis's spot-check.
- Its named positions Q8a, R0 and L0 make the last-task and resume cases explicit.
- Two STOP codes match the STOP table's own columns (no ledger write vs. a `refused` line).
- A puts the task verdict in the trailer (FR-067), so history shows a Ruling's acceptance.

### Variant C

The strongest case for C is integrity under interruption, with the smallest new public surface:
- It writes a boundary journal before the attempt and gives each boundary a stable key. It specifies fault injection at five interruption points with the assertion "at most one commit per boundary key" (FR-022, FR-034). This is the most complete answer to a crash between `git commit` and its record.
- It is the only variant that refuses changes "outside the reviewed task increment" (FR-017). That covers edits made after Q0, which A and B both miss.
- It requires literal path handling: spaces, leading dashes, pathspec metacharacters and symlink escapes (FR-018, NFR-005).
- It requires renewed review after a hook rewrite (FR-020).
- It states its trust boundary honestly (NFR-007).
- It notes that `/sc:worktrees archive` writes even without `--apply` (FR-029).
- It notes that a post-commit record cannot be part of its own commit (FR-023, U-017).
- Its no-flag authorization has a real precedent. The worker contract has the owner give records "in chat and recorded by the agent in that session from that confirmation, naming the exact scope, the owner's quoted words and the date" (`WORKER-CONTRACT.md:57`, verified), and C records the quoted instruction in the same way (FR-011).
- C adds no flag, no merge and no new branch mutation.

## Strengths claimed (numbered, with evidence)

1. **Every mechanism traces to a falsifiable root cause.** RC-3 identifies the coupled HEAD invariants: retry check 3 (`refs/retry.md:41`), the coordinator's condition (6) (`WORKER-CONTRACT.md:280`), the Q0 pin (`SKILL.md:123-129`) and the closed ledger grammar (`refs/ledger.md:127`). Q7b then follows directly: it sits after `complete` and before the next Q0, outside every window that checks HEAD, and the record goes into a sidecar. RC-1 explains why the test cost is guaranteed (S23 at `routing_refresh_cases.json:325`, verified: `"activation": {"sc:git": "self-contained"}`), and section 9.2 lists that cost.
2. **The commit is visible to the guard.** FR-016 makes `git commit --only -F` a literal Bash call. The guard sets `LL_GIT` only from the command text, with the regex `( |/)git(-[a-z][a-z-]*)? ` (`launch-level-guard.sh:555-557`, verified), and classifies `COMMIT` only from text (`:599-600`, `:713`). B's read-only helper call, `uv run --no-project python ".../sc-git-protocol/scripts/commit_plan.py" ...`, does not match that regex, because `-git-` is not preceded by a space or a slash. So the planning call is not classed as git at all, while the real commit is classed `COMMIT`. This also makes A's U-004 advantage (naming the CLI group `vcs` to avoid the word "git") unnecessary for B's layout.
3. **Only B states that launched sessions deny every submodule operation.** `submodule` is missing from the allow-table (`:720`), so it falls to `UNKNOWN` (`:724`), which is denied at every level (`:816`). All three verified. FR-037b defines the behaviour: report the refusal and never work around it. A and C both specify `git submodule update` without saying what happens in a launched session.
4. **Hook-rewrite detection has a concrete check.** `preflight` returns `pre_tree`, and `verify` compares the committed tree against it (FR-020, FR-021). That separates three cases: `hook-failed`, `hook-rewrite`, and `hook-rewrite-committed`, where a hook rewrites and re-adds files and then exits 0. A's `commit-failed` fires only on a non-zero exit (FR-064), so a formatter that re-adds its own fix and exits 0 would commit unreviewed content silently under A. The repo's formatter hooks can rewrite files (`.pre-commit-config.yaml:34-35`, `:86-91`, `:130-134`).
5. **The person's edits are protected per path, with existing machinery.** FR-027(2) compares each path's blob at `q0-head` with its blob in the Q0 start tree. The Q0 start tree already exists and is already pinned (`SKILL.md:123-126`, verified). This refuses only the overlapping path. A's Wave 0 `dirty` refusal (FR-054) blocks the whole run for any unrelated dirty path outside `.dev/` that is not named in `files=`. On a first run no verdict lines exist yet, so any dirty path blocks.
6. **Crash recovery needs no new ledger record.** The trailers `Implement-Plan:` and `Implement-Task:`, plus the `recovered` mode of `verify`, are anchored on `q0-head` (FR-021, FR-029). That anchor survives because the pin is deleted later than today (FR-029). This closes A's gap (C-010): after a crash, A's R0 would record `COMMIT: none ... reason=no-changes` for a task that was in fact committed.
7. **The ledger grammar, `E-LEDGER-CORRUPT` and `archive_workspace.py` stay unchanged (X-004).** The sidecar has a direct precedent: `codegraph.md` "is not the ledger and not a task notes file" (`SKILL.md:79`, verified). A's grammar change reaches the resume regex, the archive parser and, by A's own Risk 13, possibly the Generator-Constraint CI check.
8. **B checks commit hooks at runtime.** The common hooks directory holds only `pre-push`, `pre-push.launch-level` and `*.sample` files, and `core.hooksPath` is unset (verified with `ls` and `git config --get`). So `conventional-pre-commit` does not run in this clone, and B's `preflight` validates the header itself (R11, FR-028). A and C both assume the hook enforces the format.
9. **The helper exists in every install type.** It is a skill script mirrored into the plugin (FR-007), with a `helper-missing` refusal before any write (FR-023). A's package CLI is absent from plugin-only installs, because the plugin build copies only the plugin directory (C-020).
10. **Submodule rules target reachability, not a proxy for it.** `update` runs only from `-` or a fast-forwardable `+` (FR-034). That covers the common case after a superproject pull, without A's missing ancestry check and without C's blanket refusal. `commit-pointer` requires a published HEAD (FR-035), which is the actual cause of an unfetchable pointer. FR-034 also admits the network effect, which A's NFR-001 contradicts (X-015).
11. **The test cost is listed precisely.** One classification row for every new `WRITE_VERB_RE` hit, plus stale-row removal (FR-010). The `-protocol` suffix that the installer requires (`install_skills.py:47-59`, §3.1). A table of existing tests that must change (§9.2). C is silent on all three (C-019).
12. **The acceptance criteria are runnable observations with pass conditions** (`grep -c`, `cmp`, `wc -l`, `git ls-files`; AC-01..AC-15).
13. **The deferred pin deletion is safe under the guard.** `update-ref` is classed `COMMIT` only for `HEAD`, `--stdin` or `refs/heads/*` (`:714-717`, verified), so deleting `refs/superclaude/implement/...` later is unaffected (FR-044).

## Weaknesses identified in the others (numbered, with evidence)

1. **C's helper runs the commit where the guard cannot see it (X-008).** C's helper takes the message and the journal location, returns the commit ID, holds a lock "through read-back", and treats "a mutation timeout" as uncertain (FR-021, NFR-002, NFR-003). Because the guard classifies only from command text (`launch-level-guard.sh:555-557`, `:599-600`), a commit made inside a Python process is never classed `COMMIT`. In a launched session below `full --submit`, where `COMMIT` is denied (`:808`), C's commit would go through. This is a security regression against a mechanical gate the repository already ships.
2. **A has no crash recovery (C-010).** Nothing reconciles a commit that exists without its `COMMIT: sha=` record. The next R0 runs `stage-plan`, finds no change, and writes a false `COMMIT: none ... reason=no-changes` (FR-060).
3. **A's helper is absent in plugin-only installs (C-020).** It lives in `<pkg>/cli/vcs/`. A plugin-only user gets `helper-missing` on every `/sc:git` write and every `--commit-tasks` run, and A never says so.
4. **A changes the closed ledger grammar (X-004, FR-068, FR-069).** It edits the resume regex (`refs/ledger.md:127`) and the archive parser (`archive_workspace.py`) in one change. A's own Risk 3 rests on "None if they land together". That is a coupling cost the sidecar avoids entirely.
5. **A commits unreviewed hook rewrites on resume (X-007, FR-065).** "R0 plans again from the current tree, so any hook rewrites in the same paths are included". So content no reviewer saw lands in history. This contradicts the implement protocol's "Do not trust the implementer's report" stance (`SKILL.md:144`, verified).
6. **A's `dirty` refusal is both too strict and too weak (C-008).** It blocks a run because of unrelated work in progress, yet it misses edits made after Wave 0. A's own Risk 4 lists those edits as residual.
7. **A's dry-run downgrade gives an unauthorized caller a ready-to-run argv (FR-020).** The research's root cause is that prompt rules are advisory. Printing "the exact commands" to an agent that was not authorized invites that agent to run them by hand. B refuses and prints no plan (FR-012).
8. **A contradicts itself on the network (X-015).** NFR-001 says "no new code ... touches a remote". FR-041 runs `git submodule update --init`, which clones from `.gitmodules` (the one submodule is uninitialized here).
9. **A's submodule `update` has no ancestry check, and its states can collide (X-013).** A clean `pointer-moved` submodule whose HEAD is ahead of the recorded gitlink is moved back to the older commit and detached. A row can also be both `pointer-moved` and `detached-new-commits`, and A never says which state wins.
10. **A uses `<pkg>` for two different things (X-019).** It means the source package in §1.1, but the task package in FR-060, FR-061 and FR-064.
11. **C's switch cannot be tested and has no flag (X-001).** "Ambiguous language leaves the switch off" (FR-011) cannot be checked by a static or behaviour test. Also, a Ruling never authorizes a commit, which A cites at `refs/ledger.md:239`, so the authority source for a commit must be stronger than conversational text.
12. **C leaves out test obligations that will certainly fail (C-019).** It never mentions S23's `self-contained` activation (verified at `:325`), the `test_worker_contract.py` classification rows or the routing row. Each one breaks on the first edit.
13. **C refuses the common fast-forward submodule update (X-013, FR-026).** After `git pull` in the superproject, the checkout trails the new pointer. C stops there "for a separate resolution".
14. **C widens the scope to nested submodules (X-012, FR-025-027).** The repository has one submodule, and it is not nested.
15. **C's policy and liveness rules have no mechanism (C-017).** "Other repositories use their own verified branch policy" (FR-003) never says how policy is verified. Likewise "another live writer's evidence" (FR-016) has no liveness signal to detect.
16. **C defers its test file names and states its acceptance criteria as prose (S-005, S-006).** A reviewer cannot run any of them.

## Concessions (own weaknesses)

1. **X-002, merge.** The seed says verbatim "`/sc:git` never pushes, merges or opens PRs". B's `merge` class (FR-006, FR-013), the `merge-tree` preview and NFR-009's `git-too-old` all go. A's D7 and FR-017 should be adopted: rewrite the `HOW-WE-WORK.md:293` row, which today says "branch or merge operations" (verified), and drop the merge example and its classification row.
2. **X-003, `--interactive`.** B's stated reason is false. S23's repeat at `:327` lists only `"mode_flags": ["--smart-commit"]`, and the test at `test_routing_refresh.py:306-317` checks only the flags the fixture lists (both verified). Once merge is removed, `--interactive` has no remaining use.
3. **X-016, Wave 0 order.** "After step 6" contradicts "before the ledger is created", because step 6 is "Open or create ledger" (`SKILL.md:72`, verified). The check belongs after step 5 and before step 6, as in A.
4. **X-017, "writes nothing".** `read-tree`, `add` and `write-tree` under a private `GIT_INDEX_FILE` write loose objects, as Q0 already does (`SKILL.md:124`). Correct wording: "writes no ref, user index, working-tree or config file".
5. **X-018, header length.** `\S.{0,70}$` after `refactor: ` admits 81 characters. A total-length check is needed.
6. **X-005, scope of `.dev/tasks`.** Committing all of `.dev/tasks` pulls other packages' evidence into a task commit. WC-9 stages `.dev/tasks` but commits `-- <paths>` (`WORKER-CONTRACT.md:43`, verified). B's R12 reads the coordinator rule (`:247`) too broadly. A's package-only commit (D8) is better. The same flaw makes B's `/sc:git commit` widen the paths the person named by adding `.dev/tasks` (FR-016 step 3). It should be staged, not committed.
7. **X-021, tracked dev-copy files.** `git ls-files .claude/` lists `.claude/cache/sc-recommend-lookup.yaml` as well as `settings.json` (verified). B's `dev-copy-path` refusal would wrongly block a task that legitimately edits that file. All three variants share this error.
8. **A-003, the "current message" test.** FR-022's runtime test, "the person's own current message starts with `/sc:implement`", stops being true after a mid-run Ruling reply. The fix: evaluate it once at Wave 0, record `commit-tasks: on` for this invocation in the header of `commits.md`, and let it lapse when the invocation stops.
9. **X-007, review after a hook rewrite.** After a `hook-rewrite*` refusal, B's resume clause re-runs Q7b without a new review. C's rule (renewed review before any new attempt) is right and should be adopted.
10. **C-008 and C-021, gaps in the path checks.** `foreign-change` catches only edits that predate the task, not edits made after review. The reviewed tree is already pinned as `refs/superclaude/implement/<slug>/retry/T<rid>/r<k>-<j>`, with its 40-hex on the review header (`refs/qa.md:178`, verified). So `preflight` could refuse when `pre_tree` differs from the last compliant review's tree for S. That is C's FR-017 idea built on existing refs. B also lacks a literal-pathspec rule (for example `git --literal-pathspecs`) for `files=` entries.
11. **C-002, message source.** `/sc:git commit` without `--smart-commit` has no defined message source.
12. **X-010, no operation.** B never says what `/sc:git` does when no operation is given.
13. **X-012, recursive update.** FR-034 allows `--init --recursive`, which widens the network effect. A's never-recursive rule fits the one non-nested submodule better.
14. **A-001, invalid paths.** Preflight does not handle a `files=` path that `git add --` will reject.
15. **S-001, length.** At 522 lines, B is the longest variant, and some evidence is repeated across sections.

## Shared assumptions

- **A-001: QUALIFY.** It is false for paths created and then removed inside a task, or mistyped. Preflight must sort such paths into skip or refuse before `git add -- <paths>` aborts the whole call.
- **A-002: ACCEPT.** It holds today: the managed FINAL reads "the current contents of every delivery file" (`refs/qa.md:311`, verified). Committing before FINAL hides nothing.
- **A-003: QUALIFY.** B's current-message test fails after a Ruling turn. Authority should be bound at Wave 0, recorded for the invocation, and lapse when the run stops. A new session needs a new grant, as C says.
- **A-004: QUALIFY.** Stale remote-tracking refs give a false "unpublished", which is the safe direction. After a remote rewrite they can give a false "published", which is not safe. Report the age of the refs and leave the fetch to the person.
- **A-005: QUALIFY.** It is UNVERIFIED for all three variants. It is latent here because no `pre-commit` hook is installed (verified), and it needs a test with the pinned pre-commit framework before anyone claims it holds.
- **A-006: ACCEPT.** Verified: no file under `tests/` matches `K3` or `wait for issue #326`.

## Per-point votes

| Point | Winner | Confidence | Reason |
|---|---|---|---|
| S-001 | A | 60 | Balanced density; B's 522 lines repeat evidence, C's 121 lines omit test-pinned facts. |
| S-002 | B | 65 | B's resolve column maps every alias back to the repository; A's placeholders lack it, C's letters are opaque. |
| S-003 | HYBRID | 60 | A's verified baseline-facts table plus B's root-cause section: facts say what holds, causes say why. |
| S-004 | A | 55 | Per-section blocks leave room for inserts; B needed lettered FR-032a/037a/037b; C mixes tests into FRs. |
| S-005 | HYBRID | 65 | A's broader T-01..T-18 coverage plus B's table of existing tests that must change. |
| S-006 | B | 65 | Shell observations with pass conditions run directly; A maps to tests; C is prose. |
| S-007 | B | 55 | Root-cause column ties each mitigation to its cause; otherwise the tables are comparable. |
| S-008 | B | 70 | Skill script ships in the plugin mirror, read-only, agent commits; A's CLI is absent plugin-only; C's helper commits unseen. |
| S-009 | HYBRID | 55 | A's operation registry and separate safety ref, with B's rule that read operations load no ref. |
| S-010 | HYBRID | 55 | A and B are equivalent: a lazily loaded implement-side ref; C names none. |
| S-011 | HYBRID | 65 | B's sidecar outside the closed ledger grammar plus C's journal record written before the attempt. |
| S-012 | A | 60 | D7 (merge removed) and D8 (package-only commit) settle the two hardest seed tensions explicitly. |
| S-013 | C | 55 | Integrity, concurrency and honest trust-boundary NFRs target real failure modes; A and B are more budgetary. |
| C-001 | A | 65 | No merge, per the seed; keeps existing branch create/switch; adds submodule ops. B's merge breaks the seed. |
| C-002 | A | 60 | Exactly one of `--message` or `--smart-commit` defines the message source; B leaves it undefined. |
| C-003 | B | 60 | Refusal gives an unauthorized caller nothing to replay; A's dry run prints a ready argv; C's grant is untestable. |
| C-004 | HYBRID | 70 | A's static containment test plus B's runtime person check; each catches what the other misses. |
| C-005 | A | 55 | Named Q8a, R0 and L0 positions make resume and the last task explicit; B is equivalent but implicit. |
| C-006 | A | 65 | Runs before ledger creation, consistent with a no-write STOP, and includes unattended; B is misordered (X-016). |
| C-007 | A | 60 | Two codes match the STOP-table columns (no ledger vs. refused line); B's single row splits columns. |
| C-008 | HYBRID | 65 | B's per-path blob check on the existing pin plus C's post-Q0 increment check; A's run-wide refusal is too coarse. |
| C-009 | B | 70 | Comparing with `pre_tree` catches a rewrite-and-re-add that exits 0; A misses it; C has the concept but no check. |
| C-010 | HYBRID | 65 | B's trailer recovery with persisted `q0-head` plus C's fault-injection tests at five points; A has no recovery. |
| C-011 | B | 55 | Deferring the pin keeps `q0-head` for recovery and `foreign-change`; a small, scoped amendment to SKILL.md:129. |
| C-012 | A | 60 | Verdict in the trailer exposes Ruling acceptance; wider valid type set; B's regex has a length bug (X-018). |
| C-013 | B | 60 | A temp file outside the tree adds no repository clutter; A's message files get swept into later commits. |
| C-014 | C | 55 | Booleans avoid A's state-precedence ambiguity and separate unset from false; B's raw prefixes are less structured. |
| C-015 | B | 60 | Publication (reachability) is the root risk; branch attachment (A) and an explicit target (C) are proxies. |
| C-016 | C | 55 | Accurate route that notes `archive` writes without `--apply` (`worktrees.md:17`, `:37`); A adds an operation. |
| C-017 | HYBRID | 60 | Hardcoded master/main/integration plus origin/HEAD (A, B) with C's rule that an unresolved policy blocks mutation. |
| C-018 | HYBRID | 60 | B's report of argv, preconditions and undo plus C's statement of whether HEAD, index and worktree changed. |
| C-019 | A | 70 | Rewrites the routing row without merge and updates S23 and the classification table; B keeps merge; C is silent. |
| C-020 | B | 65 | The mirrored skill script exists in plugin installs, with an explicit `helper-missing` refusal; A's CLI does not. |
| C-021 | C | 75 | Only C requires literal handling of spaces, leading dashes, pathspec magic and symlink escapes. |
| X-001 | HYBRID | 75 | The per-invocation flag from A and B (testable), plus C's revocation and new-session-needs-new-grant rules. |
| X-002 | A | 85 | The seed says "/sc:git never pushes, merges or opens PRs"; A removes merge with an explicit D7 and a row rewrite. |
| X-003 | A | 75 | Fixture line 327 lists only `--smart-commit`, so B's reason is false; `--interactive` has no use once merge goes. |
| X-004 | B | 70 | Ledger grammar and archive parser untouched, with the codegraph.md sidecar precedent; C agrees but is less concrete. |
| X-005 | A | 70 | WC-9 stages `.dev/tasks` but commits only the listed paths; committing only the run's package keeps other packages out. |
| X-006 | B | 65 | No retroactive commits, and the consequence (`foreign-change`) is stated; A commits work completed without authorization. |
| X-007 | C | 80 | Renewed review before any new attempt after a rewrite; A includes unreviewed rewrites; B resumes without review. |
| X-008 | HYBRID | 75 | The agent's literal Bash commit (A, B) is visible to the guard's text regex; A's helper-planned argv reduces improvisation. |
| X-009 | A | 65 | Keeps the existing branch surface, and switch requires a clean tree including submodules; C drops an existing capability. |
| X-010 | C | 60 | The operation is optional in the current usage; defaulting to read-only status fits S23; B is unspecified. |
| X-011 | A | 55 | The success criterion names the guide's values; repo practice favors `complexity: standard` (implement, workflow, worktrees). |
| X-012 | A | 65 | The one submodule is not nested; never-recursive limits network and scope; C overreaches; B allows a recursive init. |
| X-013 | B | 70 | A fast-forward-only update covers the post-pull case safely; A has no ancestry check; C refuses the common case. |
| X-014 | B | 55 | /sc:git controls no push, so commit time is its only guard point; stale refs (A-004) err on the safe side. |
| X-015 | C | 65 | The grant must acknowledge the network effect and reject a substituted remote; B acknowledges it; A contradicts itself. |
| X-016 | A | 85 | Running before step 6 fits "no ledger writes"; B's "after step 6" contradicts its own STOP row. |
| X-017 | HYBRID | 60 | Keep B's private-index `pre_tree` but reword the claim: no ref, user-index, worktree or config writes; objects only. |
| X-018 | A | 75 | A enforces 72 characters with a test; B's regex admits 81; fix it with a total-length check. |
| X-019 | B | 80 | B separates the task package (`<pkg-dir>`) from the source package (`<pkg>`); A uses `<pkg>` for both. |
| X-020 | B | 85 | Verified: the hooks dir holds only pre-push, pre-push.launch-level and samples; hooksPath unset; the helper must check itself. |
| X-021 | NONE | 85 | Verified: `.claude/cache/sc-recommend-lookup.yaml` is tracked, so all three would wrongly refuse it. |
| A-001 | NONE | 70 | All three assume `files=` paths are valid pathspecs; none handles create-then-delete or mistyped paths. |
| A-002 | HYBRID | 80 | All three are equivalent and correct: the FINAL reads current files (`refs/qa.md:311`). |
| A-003 | C | 55 | C records the quoted grant and requires a new one per session; B's current-message test fails mid-run; A's marker is not per invocation. |
| A-004 | NONE | 65 | All rely on local remote-tracking refs and none states a freshness rule; B's refusal is merely the safer direction. |
| A-005 | NONE | 65 | Unverified in all three; no test runs the pre-commit framework with `--only`; latent here because no hook is installed. |
| A-006 | HYBRID | 80 | All three are equivalent and correct: no test under `tests/` matches K3 or "wait for issue #326". |
