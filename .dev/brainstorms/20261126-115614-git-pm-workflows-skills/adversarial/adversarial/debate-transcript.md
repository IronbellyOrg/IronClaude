# Adversarial Debate Transcript

## Metadata
- Depth: deep
- Rounds completed: 3 (Round 1 statements, Round 2 rebuttals, Round 2.5 invariant probe, Round 3 final arguments)
- Convergence achieved: 100% (61 of 61 diff points have a majority; after Round 1: 90.2%, after Round 2: 100%, after Round 3: 100%)
- Convergence threshold: 75%
- Focus areas: All
- Advocate count: 3 (Variant A, Variant B, Variant C; blind mode: model identity withheld)
- Taxonomy coverage: L1 16/16, L2 14/14, L3 31/31 points agreed
- Invariant probe: 30 findings; 3 HIGH + UNADDRESSED blocked convergence after Round 2.5 and were resolved in Round 3 (see invariant-probe.md)
- Source files: debate/round1-*.md, debate/round2-*.md, debate/round3-*.md (full advocate statements are included below), invariant-probe.md, debate/consensus-round2.txt, debate/consensus-round3.txt

## Round 1: Advocate Statements

### Variant A Advocate

# Round 1 — Advocate for Variant A (architect; maintainability and extension scaffolding)

#### Position summary

Variant A gives the best maintainable skeleton for this work: one place for each rule (`rules.py` with a parity test), one place to add an operation (a registry plus a checklist and a test), a helper that never writes, and a scope that follows the seed brief exactly (no merge, routing row and fixtures updated in the same change). Its state handling is weaker than B's in three specific places (crash recovery, hook-rewrite detection, per-path protection of the person's edits). B's mechanisms for those fit into A's skeleton with almost no change, so the best merged result is A's structure with those B mechanisms added.

#### Steelman

### Variant B

B's strongest case: it is the only variant that starts from root causes (RC-1 to RC-7), and it finds repository facts the others missed. These are confirmed in this worktree. The launch-level guard has no `submodule` entry in its allow-table, so every `git submodule` call falls to `UNKNOWN` and is denied at every level (`launch-level-guard.sh:720`, `:724`, `:816`; U-009). The common hooks directory holds only `pre-push`, `pre-push.launch-level` and `*.sample` files, and `core.hooksPath` is unset, so no commit-msg hook runs in this clone (X-020).

Its state mechanics go furthest:
- a `pre_tree` snapshot compared with the committed tree, so a hook that rewrites a file and re-stages it is caught (`hook-rewrite-committed`, FR-021);
- a per-path `foreign-change` check that uses the Q0 pin, which already exists (FR-027);
- crash recovery from the commit trailers (`recovered sha=`, FR-029).

Its acceptance criteria are shell commands with pass conditions (AC-01 to AC-15), which are the easiest of the three to check. Its test-cost list is also the most exact: one classification row per new `WRITE_VERB_RE` hit, and the `-protocol` suffix rule in `install_skills.py:47-59`. B gets right that the hard part of this issue is the state around HEAD, not the command shape.

### Variant C

C's strongest case: it treats the commit boundary as a recoverability problem and is honest about trust. It writes a durable journal before each attempt, keyed by a stable boundary key. The outcomes are a closed set (`committed`, `already-committed`, `no-change`, `refused`, `failed`, `uncertain`), and fault-injection tests at five interruption points require "at most one commit per boundary key" (FR-021, FR-022, FR-034). It is the only variant that notices three things:
- a record written after a commit cannot be part of that commit, and this also applies to A's `COMMIT: sha=` lines (FR-023, U-017);
- paths need literal handling of spaces, leading dashes, pathspec magic and symlink escapes (FR-018, NFR-005);
- `/sc:worktrees archive` writes even without `--apply` (FR-029; confirmed at `worktrees.md:17`, `:37`).

Its trust statement (NFR-007), "neither is proof against a malicious same-user process", is the most accurate description of what prompt text can and cannot enforce. C gets right that a refusal must say exactly what changed and must never be "repaired" automatically.

#### Strengths claimed

1. **Verified baseline facts.** §1.5 lists 27 repository facts with line citations. The diff analysis spot-checked them and found nearly all correct (U-001, rated High). Other contributors can re-verify the spec without repeating the research.
2. **One extension point.** The operation registry in `SKILL.md` (FR-006) is the only list of what `/sc:git` can do. Each row names its class, the message prefix that authorizes it, its ref, its helper verb and its refusal tokens. The "Adding an operation" checklist (FR-008), NFR-004 and a static test that every registry row points to an existing ref and helper verb (T-13) mean that adding an operation changes no existing operation. Neither B nor C has a mechanical extension contract (U-002).
3. **One source for each safety rule.** `PROTECTED_BRANCHES`, `FORBIDDEN_FLAGS`, `DEV_MIRROR_ALLOW` and `MIN_GIT` are defined once in `rules.py`, and a parity test pins the prose copies to them (FR-013, NFR-003, U-003). The X-021 finding shows why this matters. `.gitignore:129-135` deliberately allows `.claude/cache/sc-recommend-lookup.yaml`, `sc-recommend-plugin.yaml` and `eval-runs/**` (verified, as a "user-authorized exception"). In A the fix is one constant plus one prose edit, and the test fails if only one of them changes. In B and C the same list is scattered through prose.
4. **Scope follows the seed.** The seed constraint says "`/sc:git` never pushes, merges or opens PRs". A removes `merge` (D7). It rewrites the routing row at `HOW-WE-WORK.md:293`, which today still says "branch or merge operations" (verified), and keeps the three phrases that S23 pins (FR-017). It also lists the test changes this forces: the S23 `activation` (`routing_refresh_cases.json:325`, verified `"self-contained"`), the merge example in the worker-contract scan, and the parity parametrization (T-14). B keeps merge (X-002). C says nothing about the fixtures (C-019).
5. **The helper never writes.** A's runner allow-list (FR-011) contains no verb that writes objects, so "the helper performs no write" (NFR-002) is literally true (X-017). Every repository write is a visible Bash call built from the argv the helper planned (FR-061). The guard sets `LL_GIT` only from the command text (`launch-level-guard.sh:555-557`, verified), so a visible call is the only way the guard and other host hooks can see a commit. C's helper appears to run the commit itself (X-008).
6. **Correct Wave 0 order.** The commit precondition check runs after step 5 and before step 6 ("Open or create ledger", `SKILL.md:72`), which matches its "no ledger writes" promise (FR-054). B contradicts itself on this point (X-016).
7. **Deterministic commit timing.** "Open" and "pending" are defined as predicates over the ledger on disk (FR-056). The three positions are named: Q8a after Q7, R0 at the start of a resume, and L0 before the whole-list review or FINAL. Each position rechecks "no task is open" from disk (FR-057). The same ledger and tree give byte-identical plans (NFR-006). This covers the last task and the resume case explicitly, which B covers only through a resume-row clause and C only in prose.
8. **`.dev/tasks` scope matches the house pattern.** The existing commit rules already stage `.dev/tasks` and then commit only explicit paths. `WORKER-CONTRACT.md:43`: "stages with `git add -- <paths>` plus `.dev/tasks`, commits with `git commit --only -- <paths>`". `:247`: "stages explicit paths plus `.dev/tasks` ... commits with `git commit --only -- <paths>`" (both verified). A does the same and adds only the run's own package directory to the commit (FR-062, D8). The always-staged rule and PR 288's evidence rule still hold, and other packages in flight stay out of the task commit (X-005).
9. **Behaviour tests for assumptions others trust.** T-05 checks that `git commit --only` really leaves other staged entries out of the commit (U-005). T-06 marks the hook's default type list UNVERIFIED until the test runs the pinned hook.
10. **Front matter follows the guide.** `category: version-control` and `complexity: moderate` are values the developer guide lists (`:276-278`). B's `standard` is not in that list (X-011).
11. **Rulings stay visible in history.** The trailer `Implement-Task: T<id> (<verdict>)` records a non-compliant verdict that the operator accepted (FR-067), while "a Ruling never authorizes a commit".
12. **Version coupling.** The helper prints `vcs_contract: "1"`, and both skills refuse any other value (NFR-009). A mismatch between installed skill text and an installed helper is refused with a clear message instead of failing in an unclear way.
13. **Real-environment findings.** In this clone `origin/HEAD` resolves to `origin/master` while the GitHub default branch is `integration` (U-006). Changing `archive_workspace.py` may trigger the Generator-Constraint CI check (U-007). Both shape the implementation.

#### Weaknesses identified in the others

### Variant B

1. **Keeps merge against the seed.** FR-006 and FR-013 keep a `merge` class with a yes/no chat confirmation. The seed constraint is "`/sc:git` never pushes, merges or opens PRs" (X-002).
2. **The reason given for keeping `--interactive` is false.** FR-002 says the fixture flag check requires `--interactive`. The S23 repeat has `"mode_flags": ["--smart-commit"]` only (`routing_refresh_cases.json:327`, verified; X-003).
3. **Internal contradictions.** Wave 0 runs "after step 6 (ledger)" yet stops "before the ledger is created" (X-016). The helper "writes nothing in the repository" yet allows `read-tree`, `add` and `write-tree`, which write objects (X-017). The header regex allows 81 characters against a 72-character limit (X-018).
4. **Commits all of `.dev/tasks`.** R12 accepts that other packages' changes enter a task commit and cites `WORKER-CONTRACT.md:247` as the reason. That line stages `.dev/tasks` but commits `--only -- <paths>`, so it supports A's narrower scope, not B's (X-005).
5. **Refusing unpublished pointer commits blocks a valid local order.** The research's order is: commit inside the submodule, commit the pointer, then push the submodule before the superproject. B refuses step 2 until step 3 is done, and it bases that refusal on remote-tracking refs that may be stale, with no fetch (X-014, A-004). Publication order belongs to `/sc:pr-submit`.
6. **Front matter value not in the guide.** `complexity: standard` is not in the guide's list (X-011).
7. **One STOP row with split columns.** B's single `E-COMMIT-REFUSED` row needs "Wave 0: No. Q7b: ..." inside its fixed columns. That makes the closed STOP table harder to parse and to test (C-007).

### Variant C

1. **The authorization switch cannot be tested.** C uses a current-session instruction with no flag (FR-011). The seed requires tests for authorization. A free-text instruction cannot be checked mechanically, can be lost on compaction, and has to be matched by interpretation ("Ambiguous language leaves the switch off") (X-001).
2. **The commit runs where the guard cannot see it.** The helper takes the message and the journal location, returns the commit ID and hook-modified paths, holds a lock "through read-back", and treats "a mutation timeout" as uncertain (FR-021, NFR-002, NFR-003). So the helper runs `git commit`. The guard classifies git only from the command text (`launch-level-guard.sh:555-557`, verified), so `LL-COMMIT` and host PreToolUse hooks would not see the commit (X-008).
3. **Test breakage it does not plan for.** C says nothing about S23 (`"activation": {"sc:git": "self-contained"}`, verified at `:325`), the worker-contract scan that pins the merge example, or the routing row (C-019). Its test file names are deferred (S-005). A refactor along C's lines would fail existing tests that its plan never lists.
4. **Scope wider than the seed.** It adds nested-submodule initialization and deepest-first commits (X-012) and multi-repository partial execution, while the repository has one non-nested, uninitialized submodule. It also drops `branch create` and `branch switch` (X-009), although the current `git.md` Triggers list "branch" (verified).
5. **STOP codes left open.** "No new code unless explicit and tested with its consumers" (FR-021, C-007). The implement STOP table is closed ("No other `E-*` codes besides the rows above", `SKILL.md:51`), so a refusal at the commit boundary still needs a defined code, and C does not give one.
6. **A protected-branch rule with no mechanism.** "Other repositories use their own verified branch policy" (FR-003) does not say how the policy is verified without network access (C-017).
7. **Machinery heavier than the local job needs.** A lock, a journal and a versioned request object are a lot for a local commit between tasks (NFR-002, FR-021). The same no-duplicate guarantee can be reached with commit trailers plus a parent check (B FR-021), which needs no new state directory.

#### Concessions

1. **No crash recovery (C-010).** If the session dies after `git commit` and before `COMMIT: sha=` is written, the next R0 plans again, finds no change in the committed paths and records `COMMIT: none ... reason=no-changes` for tasks that were in fact committed. There is no duplicate commit, but the record is wrong and FR-071's summary leaves that commit out. Fix: at R0, before re-planning, read HEAD with `cat-file commit HEAD` (already in A's allow-list, FR-011). When HEAD's parent and its `Implement-Ledger:` and `Implement-Task:` trailers match the pending tasks, record `COMMIT: sha=`. This is B's recover mode, built on trailers A already writes.
2. **A rewriting hook that re-stages files is not caught (C-009).** A judges the result by exit code and HEAD only. A hook that rewrites a file, re-adds it and exits 0 commits content that was never reviewed. B's `pre_tree` comparison should be adopted.
3. **The protection of the person's own edits is too coarse (C-008, Risk 4).** The Wave 0 `dirty` refusal blocks a whole run for any unrelated dirty file. It does not see edits made during the run. It also exempts paths named in an earlier `files=` set, which combines badly with X-006 below. B's per-path `foreign-change` check against the Q0 pin is better, and it needs B's later pin deletion (C-011).
4. **Tasks from an unflagged resume can be committed later (X-006).** A task that completed after the first `COMMIT: on` line, during a resume without the flag, is committed at the next flagged R0. The person may have edited those paths in between. B and C never commit such a task, which is safer.
5. **NFR-001 contradicts FR-041 (X-015).** `git submodule update --init` clones from the URL in `.gitmodules`. That URL is `https://github.com/anthropics/skills.git` for the one uninitialized submodule here. So "touches no remote" is false. NFR-001 needs a stated exception for that read, authorized by the person's typed line, as B and C both give.
6. **`<pkg>` means two things (X-019).** §1.1 defines `<pkg>` as `src/<package>/`, but FR-060, FR-061 and FR-064 use `<pkg>` for the managed task package. It needs a separate alias, as B's `<pkg-dir>`.
7. **The helper is missing in plugin-only installs, and A does not say so (C-020, S-008).** The plugin build copies only `plugins/<package>/` (`build_superclaude_plugin.py:16`, `:77`, verified), so a package CLI group is absent there and writes would refuse with `helper-missing`. One mitigating fact: the implement protocol already calls the package CLI (`superclaude review safety-scan`, `SKILL.md:198-201`, also in the plugin copy). That call, however, does not stop the run when the CLI is missing, and A's does. The better choice is to keep A's module split, `rules.py` and `vcs_contract`, and ship them as a mirrored skill script, as B and C do.
8. **Guard behaviour for submodules missed (U-009).** A does not say that `git submodule update` and `commit-pointer` are denied in every launched session.
9. **The hook baseline is overstated (X-020).** §1.5 says messages "are checked by" the commit-msg hook. That is true of the config, but no hook is installed in this clone. A's own `check-message` covers this gap, but Risk 2 is described as a live failure here.
10. **The dev-copy allow-list is wrong (X-021).** `DEV_MIRROR_ALLOW = ("settings.json",)` leaves out the tracked cache files that `.gitignore:129-135` allows.
11. **Smaller gaps.**
    - No literal pathspec handling (C-021): files named with pathspec magic need `--literal-pathspecs`.
    - No filter for `files=` paths that no longer exist (A-001).
    - `pointer-moved` and `detached-new-commits` can both apply, with no precedence rule and no ancestry check (X-013).
    - Two different files are both named `refs/commit.md` in two skills (S-010).
    - The dry-run downgrade prints exact argv, which an agent could then run by hand (C-003).

#### Shared assumptions

- **A-001: REJECT.** A path created and deleted inside a task, or mistyped, is in neither the index nor HEAD, so `git add -- <paths>` fails for the whole call. The planner must filter such paths into `skipped`.
- **A-002: ACCEPT.** It holds today. The managed FINAL reads "the current contents of every delivery file" (`refs/qa.md:311`, verified), so committing first hides nothing.
- **A-003: QUALIFY.** It holds only if the spec says the invocation line, checked once in Wave 0, is the authority for the whole invocation, Ruling turns included, and that every resume needs the flag again. No variant says this yet.
- **A-004: QUALIFY.** Remote-tracking refs can be stale without a fetch. That is acceptable only when the result is a warning or "unknown" and is never used to block a commit or to declare it safe.
- **A-005: QUALIFY.** No variant has verified it. It needs a test that runs the pinned pre-commit framework, with a hook that rewrites files, under `git commit --only` with unstaged edits present.
- **A-006: ACCEPT.** Verified: no file under `tests/` matches "wait for issue #326" or "K3", so rewriting `WORKER-CONTRACT.md:42` breaks no test.

#### Per-point votes

| Point | Winner | Confidence | Reason |
|---|---|---|---|
| S-001 | A | 55 | Balanced density: verified citations without B's length or C's sparseness; easiest for an implementer to act on. |
| S-002 | B | 60 | B's how-to-resolve column is unambiguous; A overloads `<pkg>` (X-019); C's single letters are terse. |
| S-003 | HYBRID | 60 | A's verified baseline-facts table (U-001) plus B's root-cause section (U-008) for the reasons behind each design. |
| S-004 | A | 55 | Gapped per-section blocks take new requirements without renumbering; B already needed lettered inserts (FR-032a, FR-037a/b). |
| S-005 | HYBRID | 65 | A's per-behaviour test table with file names plus B's table of existing tests that must change. |
| S-006 | B | 65 | Shell observations with pass conditions can be checked directly; A maps to test ids, C is prose. |
| S-007 | B | 55 | Root-cause column adds traceability; A's residual column is comparable; C gives no residuals. |
| S-008 | HYBRID | 60 | B's mirrored skill-script placement, which keeps the helper in plugin installs, holding A's module split, `rules.py` and `vcs_contract`. |
| S-009 | A | 60 | Registry plus per-group refs and a shared safety ref give one tested extension point. |
| S-010 | B | 55 | Both load lazily; B's distinct name avoids two different `refs/commit.md` files across skills. |
| S-011 | B | 55 | A sidecar leaves the closed ledger and archive parsers untouched; trailers still allow recovery. |
| S-012 | A | 55 | A adds decisions the seed needs answered: merge removal (D7) and managed commit scope (D8). |
| S-013 | HYBRID | 55 | A's single-source, extension and version NFRs; B's size budgets; C's bounded execution and honest trust claims. |
| C-001 | A | 65 | Keeps the existing surface minus merge, per the seed; B adds merge; C drops branch create/switch. |
| C-002 | A | 60 | `--message` gives a path for a message the person writes; `--interactive` has no operation left once merge goes. |
| C-003 | B | 55 | Same prefix rule; B's plain refusal avoids A's dry run printing argv an agent could run by hand. |
| C-004 | HYBRID | 70 | A's static no-primitive-contains test plus B's runtime person-message check; cheap and complementary. |
| C-005 | A | 65 | Named Q8a/R0/L0 positions with an on-disk recheck cover the sequential, resume and last-task cases explicitly. |
| C-006 | A | 55 | Most complete precondition list (unattended, contract version, not-a-repo); replace its coarse dirty rule as C-008 says. |
| C-007 | A | 55 | Two codes keep each STOP row's product and ledger columns single-valued; B's single row splits them. |
| C-008 | B | 70 | Per-path foreign-change via the existing Q0 pin is precise and mechanical; A's whole-run dirty refusal is coarse. |
| C-009 | B | 75 | `pre_tree` comparison catches hook-rewrite-committed; A misses a hook that rewrites, re-stages and exits zero. |
| C-010 | B | 65 | Trailer-based recover mode is light and closes A's mislabel gap; C's journal is heavier for the same result. |
| C-011 | B | 55 | Keeping the pin longer is needed for the foreign-change check; a small, bounded lifecycle change. |
| C-012 | A | 60 | Ten common types; the verdict trailer records Ruling acceptance; B spends header characters on task ids. |
| C-013 | B | 55 | A temporary file outside the tree avoids committing a copy of the message as evidence clutter. |
| C-014 | HYBRID | 60 | A's closed state list with a defined precedence, plus C's unset-versus-false, null-unknown and empty-list rules. |
| C-015 | HYBRID | 55 | Require a clean module; accept a HEAD on a branch (A) or already published (B); refuse otherwise. |
| C-016 | C | 55 | Explaining the route with the archive-writes caveat (U-020) is accurate and needs no extra operation. |
| C-017 | B | 55 | Practical fixed set plus `origin/HEAD`, resolved per submodule; C's "verified policy" has no mechanism. |
| C-018 | B | 60 | Checked preconditions, exact argv, result and an undo hint make the most usable write report. |
| C-019 | HYBRID | 70 | A's row rewrite that drops merge plus B's classification row for every new `WRITE_VERB_RE` hit. |
| C-020 | B | 65 | Plugin build copies only `plugins/` (`:16`, `:77`, verified); a mirrored script keeps the helper in every install. |
| C-021 | C | 65 | Literal pathspec, leading-dash and symlink-escape handling closes gaps that A and B leave open. |
| X-001 | HYBRID | 75 | Flag (A and B agree), which is testable; B's person-message check plus A's static scope test. C's instruction cannot be tested. |
| X-002 | A | 85 | The seed forbids merge in `/sc:git`; A removes it and rewrites the routing row; B keeps it. |
| X-003 | A | 75 | The fixture lists only `--smart-commit` (`:327`, verified); dropping `--interactive` with merge is clean; B's reason is false. |
| X-004 | B | 55 | Closed ledger and archive grammars left untouched mean a smaller blast radius and avoid the Generator-Constraint check; A's change is tested but wider. |
| X-005 | A | 65 | Matches the house pattern (stage `.dev/tasks`, commit `--only` explicit paths, WORKER-CONTRACT `:43`, `:247`); keeps other packages out. |
| X-006 | B | 60 | Not retroactive; A's flagged resume could commit unflagged tasks, plus person edits the `files=` dirty exemption lets through. |
| X-007 | HYBRID | 55 | Re-plan only on a person-typed flagged resume (A), after showing hook-modified paths and diff (C). |
| X-008 | A | 75 | The helper never writes and the commit stays a visible Bash call the guard sees (B agrees); C hides it. |
| X-009 | A | 60 | Branch create/switch are existing surface (git.md Triggers "branch"); A's guards are tight; C drops them. |
| X-010 | C | 60 | Defaulting to read-only status is harmless and matches `/sc:graph`'s status default. |
| X-011 | A | 75 | The developer guide lists `moderate`; B's `standard` is not in the list (`:278`). |
| X-012 | A | 65 | The one submodule is not nested; reporting `nested-not-inspected` keeps scope minimal and safe. |
| X-013 | B | 70 | The ancestry check refuses ahead or diverged modules instead of silently detaching; A has no check and no precedence rule. |
| X-014 | A | 60 | Warn-only suits a local commit; push order belongs to `/sc:pr-submit`; B's refusal trusts stale refs. |
| X-015 | C | 60 | C (like B) admits the clone's network effect and also rejects a substituted remote identity; A contradicts itself. |
| X-016 | A | 80 | A runs the check before step 6, consistent with no ledger writes; B contradicts `SKILL.md:72`. |
| X-017 | A | 70 | A's allow-list has no object-writing verb, so "performs no write" holds; B's claim is false. |
| X-018 | A | 65 | A states a plain 72-character limit without B's regex, which allows longer headers. |
| X-019 | B | 80 | B uses `<pkg-dir>` for the task package; A overloads `<pkg>`. |
| X-020 | B | 80 | Verified: the hooks directory holds only pre-push files and `core.hooksPath` is unset; only B states this. |
| X-021 | NONE | 75 | `.gitignore:129-135` deliberately allows tracked cache files; all three wrongly allow only `settings.json`. |
| A-001 | NONE | 70 | No variant handles vanished or mistyped `files=` paths; the planner should move absent paths to `skipped`. |
| A-002 | HYBRID | 60 | All three equally right today (`refs/qa.md:311` reads current files); add a test that pins it. |
| A-003 | A | 55 | A per-invocation flag lasts through Ruling turns; B's current-message rule breaks after one; A must say so explicitly. |
| A-004 | C | 55 | Reporting readiness as unknown is honest about stale refs; A's warning is close; B's refusal relies on stale data. |
| A-005 | NONE | 70 | No variant verifies it; a test should run the pinned pre-commit framework with a rewriting hook under `--only`. |
| A-006 | HYBRID | 60 | All three equally right: no test matches the K3 wording (verified by grep), so there is no test impact. |

### Variant B Advocate

# Round 1: Advocate for Variant B (persona: analyzer)

Repository facts below were re-read read-only in this worktree on 2026-11-26. "Verified" means I read the line or ran the read-only command myself in this round.

#### Position summary (1-3 sentences)

Variant B has the strongest root-cause-driven design for the risky half of the work. It makes the commit a literal Bash call the guard can see, uses a read-only helper script that ships in the plugin mirror, and adds three integrity checks built on existing pins: `pre_tree` for hook rewrites, `foreign-change` for the person's own edits, and trailer-based crash recovery. It keeps commit state in a sidecar, so the closed ledger grammar is untouched. B is wrong, though, on merge (it breaks the seed constraint), on the `--interactive` test claim, and on committing all of `.dev/tasks`, and it has several internal defects. The merged spec should take B's `/sc:implement` commit mechanics and hook and crash handling, and take most of A's `/sc:git` surface.

#### Steelman (one sub-heading per opposing variant)

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

#### Strengths claimed (numbered, with evidence)

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

#### Weaknesses identified in the others (numbered, with evidence)

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

#### Concessions (own weaknesses)

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

#### Shared assumptions

- **A-001: QUALIFY.** It is false for paths created and then removed inside a task, or mistyped. Preflight must sort such paths into skip or refuse before `git add -- <paths>` aborts the whole call.
- **A-002: ACCEPT.** It holds today: the managed FINAL reads "the current contents of every delivery file" (`refs/qa.md:311`, verified). Committing before FINAL hides nothing.
- **A-003: QUALIFY.** B's current-message test fails after a Ruling turn. Authority should be bound at Wave 0, recorded for the invocation, and lapse when the run stops. A new session needs a new grant, as C says.
- **A-004: QUALIFY.** Stale remote-tracking refs give a false "unpublished", which is the safe direction. After a remote rewrite they can give a false "published", which is not safe. Report the age of the refs and leave the fetch to the person.
- **A-005: QUALIFY.** It is UNVERIFIED for all three variants. It is latent here because no `pre-commit` hook is installed (verified), and it needs a test with the pinned pre-commit framework before anyone claims it holds.
- **A-006: ACCEPT.** Verified: no file under `tests/` matches `K3` or `wait for issue #326`.

#### Per-point votes

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

### Variant C Advocate

#### Position summary

C is the strongest foundation for data integrity: its versioned results, prepared journal, exact candidate validation, and explicit uncertainty make interrupted local commits reconcilable rather than merely repeatable. I advocate retaining those contracts while adopting B's host-visible commit execution and mechanically parsed opt-in, and A's more explicit migration inventory; C is not safe to implement unchanged.

#### Steelman

### A

A offers the clearest implementation map. Its operation registry, extension checklist, safety-rule parity tests, explicit resume/last-task positions, and T-05 verification of unrelated staged entries turn a broad refactor into a maintainable, testable interface (FR-006–013, FR-057, T-05). Its strongest safety argument is that a read-only planner followed by visible Git writes preserves the host's existing permission checks, rather than replacing them with a new trust boundary (NFR-002). A also correctly removes merge despite the old example and explicitly inventories routing and packaging changes (D7, FR-015–017).

The strongest version of A is therefore not merely a simpler C: it is an integration-oriented design that makes existing enforcement visible and minimizes ambiguous agent decisions. Those are real advantages, even though its ledger changes and missing crash reconciliation create integrity gaps.

### B

B best explains the coupled invariants that made this work difficult: HEAD must remain fixed within a task, Q0 captures pre-existing changes, ledger parsing is closed, and installed components must actually ship their helper (RC-2, RC-3, RC-6). Its per-path `foreign-change` check and committed-tree comparison are concrete, executable checks rather than general assurances (FR-027, FR-020–021). Its sidecar avoids archive-parser churn, and its deferred pins preserve the evidence those checks require (FR-029).

B also identifies a decisive operational constraint: literal Git commands must remain visible to the launch-level guard (FR-016), and submodule commands remain denied in launched sessions (FR-037b). I independently re-read the guard and confirmed both facts. B's strongest argument is that new safety checks must compose with existing enforcement, not disappear inside a wrapper. That argument defeats C's current commit-execution design, even though B's merge operation violates the decided scope.

#### Strengths claimed

1. **A proper operation-result contract, not success inferred from an exit code.** C FR-021 defines a versioned request, rejects unknown fields, and returns exactly `committed`, `already-committed`, `no-change`, `refused`, `failed`, or `uncertain`. Only the first three permit continuation. NFR-001 requires validation of parent, changed paths, and candidate contents. This separates an observed commit from an attempted one and makes timeout or unexpected hook history a first-class failure to establish the outcome.

2. **Prepared evidence and stable identity address duplicate commits after interruption.** C FR-022 requires a journal before the attempt and reconciliation before task selection and the all-complete shortcut. It checks expected parent and exact authorized changes, not just matching task names in a message. FR-034 injects failures at five interruption points and repeats resume twice to assert at most one commit per boundary key. B's recovery is useful but weaker; A has no equivalent reconciliation protocol.

3. **The specification admits the post-commit evidence problem.** C FR-023 says a terminal record written after a commit cannot be included in that same commit. It keeps that evidence staged without inventing another housekeeping commit and does not pretend the journal's reported commit contains its own result. This applies equally to A's post-commit ledger line and B's sidecar line, neither of which makes this lifecycle explicit.

4. **Task isolation means content isolation, not merely a filename allowlist.** C FR-017 refuses same-file pre-existing changes and changes outside the reviewed increment; FR-018 freezes repository identity, expected parent, paths, and contents. NFR-005 explicitly covers leading dashes, pathspec metacharacters, traversal, and symlink escapes. A's initial dirty-tree check is too coarse and can trust old ledger paths; B has a valuable Q0 comparison but lacks C's complete literal-path contract.

5. **Concurrency claims are appropriately limited.** C FR-014 requires every writer to join before the batch boundary; NFR-002 serializes cooperating helpers but explicitly states that a lock cannot prevent editors, hooks, or arbitrary Git processes from changing state. Revalidation remains necessary. This is stronger than equating a completed ledger with a quiescent worktree.

6. **Submodule inspection models independent facts instead of forcing one label.** C FR-024 reports pointer change, tracked dirt, untracked dirt, initialization, conflicts, and attachment independently, with null/unknown states and deterministic order. A's single closed state can obscure simultaneous pointer movement and dirt. C FR-028 further states that multiple repositories have no atomic transaction: report completed, untouched, and failed paths with old/new IDs, without resetting earlier successes.

7. **Authority is scoped to effects, including network effects.** C FR-010–012 distinguishes implementation approval, local commit authority, selected submodule update authority, and publication. FR-026 explicitly acknowledges initialization may fetch and rejects substituted remote identities. A's absolute no-remote requirement contradicts its initialization operation. B acknowledges fetching but gives less detail about approved remote identity.

8. **Cleanup discovery does not silently acquire publication authority.** C FR-029 distinguishes inspection from the existing archive operation, which writes to the evidence repository without `--apply`. Independent repository verification confirms this in `/home/coder/workspaces/worktrees/IronClaude/issue-326/src/superclaude/commands/worktrees.md`, especially its Usage and Options sections. C correctly routes the person rather than invoking cleanup or exposing its private deletion function.

#### Weaknesses identified in the others

1. **A loses the distinction between a committed task and an empty task after a crash.** FR-061 writes the commit before `COMMIT: sha=`, but FR-060/R0 only replans the current changes. If the session stops between those writes, an empty tree becomes `COMMIT: none`, not a recovered commit. This is an audit-integrity failure even if no duplicate happens in that particular case (C-010).

2. **A introduces a new state grammar across multiple consumers unnecessarily.** FR-068–070 changes the ledger, archive parser, and STOP table. Its parity tests are genuinely useful, but B and C keep commit state outside the closed ledger grammar. A's persisted `COMMIT: on` also makes tasks completed during a later unflagged invocation eligible on a subsequent flagged resume (FR-056; X-006), violating the clearer per-invocation boundary.

3. **A's read-only helper placement weakens distribution completeness.** A places the helper in package CLI code while the plugin ships primitives from its plugin tree (S-008, C-020). Mirroring a skill is insufficient if its executable dependency is not available in plugin-only installations. B's skill-local script is the more complete distribution unit.

4. **A's hook handling does not prove the reviewed candidate was committed.** FR-064 distinguishes failures by exit and HEAD movement, but does not compare successful committed contents with a prepared candidate. FR-065 then includes hook rewrites on resume without explicitly requiring renewed review. B's tree verification and C's reviewed-candidate requirement are stronger (C-009, X-007).

5. **A cannot simultaneously promise no remote contact and initialize submodules.** NFR-001 forbids touching a remote; FR-041 initializes uninitialized modules. The diff analysis records the contradiction as X-015. The contract must acknowledge a possible clone/fetch and obtain appropriate scope, rather than make a false no-network guarantee.

6. **B retains an explicitly forbidden operation.** B FR-006/013 supports merge with preview and confirmation, and FR-002 preserves the merge example to avoid fixture churn. The seed Constraints explicitly say `/sc:git` never merges. A preview or extra confirmation cannot authorize expanding that decided scope; A and C correctly remove it (X-002).

7. **B overstates recovery and read-only behavior.** Its `recovered` classification checks parent and plan/task trailers, but the stated recovery predicate does not require an exact prepared candidate or a unique boundary generation (FR-021). Its private-index `add`/`write-tree` operations can write objects despite claiming to write nothing in the repository (FR-019; X-017). These checks are valuable, but their guarantees need narrower wording and stronger evidence.

8. **B's unpublished test is not proof of remote availability.** FR-035 refuses pointers absent from remote-tracking branches, but stale local refs can falsely imply publication after remote history changes. Conversely, safe local-only work is blocked even though publishing is outside scope. C's explicit unknown/not-ready report fits the local-only contract better; actual publication readiness remains with the publication workflow (A-004, X-014).

9. **B contains fixable but consequential contract inconsistencies.** FR-023 places preflight after ledger creation while promising no ledger writes (X-016). Its header regex permits more than its stated 72-character limit (X-018). Its assertion that S23 requires `--interactive` is contradicted by the diff's repository spot-check (X-003). These are not reasons to discard B, but precise interfaces cannot rely on its prose alone.

10. **Neither A nor B fully addresses accidental candidate drift and path ambiguity.** Both plan explicit path arguments, which is good, but neither specifies literal interpretation of all implementation `files=` entries. Neither resolves nonexistent/mistyped entries before a multi-path add. C improves literal handling but shares the missing nonexistent-path policy (C-021, A-001).

#### Concessions

1. **X-008 is a release-blocking defect in C, not a stylistic preference.** FR-006/021 and NFR-002 imply a helper that executes the mutation while holding its lock. I independently read `/home/coder/workspaces/worktrees/IronClaude/issue-326/src/superclaude/hooks/scripts/launch-level-guard.sh`: its Git-word detection and COMMIT classification inspect submitted command text, and its level rules deny COMMIT below the permitted level. C cannot claim compatibility while concealing the actual commit inside its script. Adopt A/B's literal host-visible Git execution; preserve C's prepared/result contracts through explicit prepare and verify phases. How lock ownership spans those calls must be designed and tested, not assumed solved.

2. **X-001: C's session instruction is a valid kind of human authority but an underspecified switch.** The seed explicitly permits considering it, so it is not intrinsically out of scope. However, a narrowly parsed flag on the person's invocation is easier to validate and explain. C does not define same-invocation authority across later turns or compaction. I prefer B's person-origin check and per-invocation opt-in, augmented by C's quoted scope, revocation, and fresh-session rules. A stored flag or quotation must never manufacture authority.

3. **X-012: nested mutation is more scope and complexity than this delivery needs.** C supplies sensible parent-first initialization and deepest-first commit ordering, but nested discovery, selection, remote approval, and partial-failure cases multiply the safety surface. Prefer A's bounded initial mutation scope and an explicit unsupported nested-operation result; retain C's visibility into nesting where safely available. Do not perform recursive updates of unselected modules.

4. **X-013: C makes update needlessly weak.** Refusing every initialized checkout that differs from the recorded pointer means a common legitimate recorded-target update cannot run. B's clean ancestor-only rule is a better default: distinguish advancement from ahead/diverged work and refuse the latter. The selected recorded target and preservation checks should remain explicit.

5. **C is less implementation-ready in its interface and migration details.** The boundary trailer token, concrete schema, deadline values, message-file location, implement-side lazy ref, and STOP integration are left open. A provides a better registry, test matrix, and concrete routing/fixture inventory; B identifies classification-table maintenance. These should be incorporated before implementation rather than left to incidental edits (S-005/006/010, C-007/012/013/019).

6. **C's unchanged Q0 lifetime needs a stronger handoff contract.** It commits after task cleanup and says retry restoration is unchanged, but it does not specify precisely when reviewed candidate evidence survives deletion of the task pin. FR-017's initial snapshot is not by itself proof of the reviewed task increment. B's deferred pin deletion is useful until C's prepared journal contains all required verifiable evidence. No pending boundary may depend on an already-deleted reference (C-011).

7. **C's journal adds real state-management work.** Atomic persistence, schema validation, movement during archive, and lock conflicts need executable tests. Including a prepared journal in mandatory evidence also requires a non-self-referential digest definition: the candidate fingerprint cannot recursively include its own fingerprint. FR-023 narrows reconciliation exclusions but does not fully specify this construction. Stable identity must distinguish new task generations without allowing a changed candidate to masquerade as an old attempt.

8. **X-020 and X-021 require separating policy from observation.** The diff reports that configured commit hooks are not installed in this clone; C must not imply that leaving hooks enabled proves the message was checked. Validate required message structure independently and test with deliberately installed hooks. The diff also reports another tracked development-cache file despite all three variants' settings-only factual claim. Correct that claim without automatically relaxing the user's explicit prohibition on staging other development-runtime paths; legitimate conflicting work requires a user decision.

9. **C is incomplete on shared assumptions.** It lacks a nonexistent-path rule (A-001), explicit same-invocation authorization lifetime (A-003), and a real pre-commit-framework test with `--only` and unrelated unstaged changes (A-005). Its local locks and post-read verification cannot promise protection against arbitrary same-user writers or malicious trusted hooks; NFR-007 correctly limits that guarantee.

#### Shared assumptions

- **A-001 — REJECT:** A ledger path is untrusted input; classify absent-both-before-and-after paths explicitly and refuse ambiguous or mistyped entries before staging anything.
- **A-002 — QUALIFY:** Current managed FINAL reads current delivery files, but preserve that reviewer input contract and verify the legacy whole-list route too.
- **A-003 — QUALIFY:** Bind authority to the same invocation across turns with explicit revocation rules; persisted evidence alone cannot authorize a new session.
- **A-004 — REJECT:** Remote-tracking refs are local observations, not fresh proof that another person can fetch the selected commit.
- **A-005 — QUALIFY:** Preserve edits as an acceptance requirement, but prove real framework stash/restore behavior under `--only`; plain-hook fixtures are insufficient.
- **A-006 — ACCEPT:** The diff found no test pinning the K3 wording; still run worker-contract regressions because behavioral requirements remain coupled.

#### Per-point votes

| Point | Winner | Confidence | Reason |
|---|---|---|---|
| S-001 | HYBRID | 88 | C's compact contract plus A's navigation tables preserves operational detail without B's repeated evidence burden. |
| S-002 | B | 90 | Explicit resolution instructions are clearer than C's single-letter aliases or A's overloaded package alias. |
| S-003 | B | 94 | Falsifiable root causes explain which existing invariants the new behavior must preserve. |
| S-004 | C | 90 | Contiguous identifiers simplify traceability; test obligations remain legitimate requirements. |
| S-005 | HYBRID | 95 | A's test mapping plus C's interruption and integrity scenarios gives navigable, behavior-focused coverage. |
| S-006 | A | 92 | Acceptance-to-test mapping is easier to audit than shell-text checks or broad FR ranges. |
| S-007 | B | 87 | Root cause and residual columns expose what mitigation does not establish. |
| S-008 | HYBRID | 98 | B's distributed skill-local planner and visible writes, with C's versioned preparation/result contracts. |
| S-009 | A | 85 | Registry and operation-specific references provide the clearest extension seam; omit branch mutation content outside scope. |
| S-010 | B | 90 | A lazy commit-step reference clearly isolates executor behavior without overloading its main protocol. |
| S-011 | C | 97 | Prepared durable journal supports reconciliation without changing the ledger grammar. |
| S-012 | A | 85 | Explicit merge-removal and evidence-scope decisions surface important policy choices for review. |
| S-013 | C | 96 | Integrity, bounded execution, uncertainty, and honest concurrency limits directly address operational failure. |
| C-001 | C | 91 | Narrow operation scope avoids introducing extra branch mutations; merge remains forbidden. |
| C-002 | C | 85 | Preserve existing flags with restricted meanings instead of adding a message-source interface unnecessarily. |
| C-003 | HYBRID | 93 | B's person-origin enforcement plus C's repository, path, target, and effect scope. |
| C-004 | B | 96 | Runtime provenance validation is stronger than banning a flag string in selected primitives. |
| C-005 | HYBRID | 95 | A's named entry points plus C's cleanup, writer-join, and pending-journal barriers. |
| C-006 | HYBRID | 94 | A's before-ledger placement plus C's initial state capture avoids writes before preconditions pass. |
| C-007 | B | 87 | One explicit tested refusal code is sufficient; C defers a necessary consumer contract. |
| C-008 | HYBRID | 97 | B's executable Q0 comparison plus C's same-file overlap and reviewed-increment refusal. |
| C-009 | HYBRID | 98 | B's prepared-tree comparison plus C's exact-path validation and uncertain-outcome handling. |
| C-010 | C | 98 | Durable preparation and exact reconciliation preserve commit identity across the crash window. |
| C-011 | B | 94 | Retain pins until boundary evidence is durable; unchanged deletion timing risks losing required proof. |
| C-012 | HYBRID | 90 | A's explicit message schema plus C's stable boundary-key trailer; independently enforce length and required attribution. |
| C-013 | B | 92 | An external temporary message file avoids unintended evidence churn and accidental message-file inclusion. |
| C-014 | C | 97 | Independent state fields preserve simultaneous dirt and pointer changes; null states avoid fabricated cleanliness. |
| C-015 | C | 91 | Explicit target equality and detached-new-target preservation make the intended pointer unambiguous. |
| C-016 | C | 96 | Correctly distinguishes archive writes from inspection and preserves person-selected cleanup authority. |
| C-017 | C | 95 | Verified repository-specific policy is safer than assuming three branch names protect every installation. |
| C-018 | HYBRID | 91 | B's exact commands plus C's before/after state and refusal reasons; omit generic history-changing undo advice. |
| C-019 | HYBRID | 97 | A's merge-removal and routing migration plus B's exhaustive write-classification updates. |
| C-020 | HYBRID | 96 | B's mirrored skill-local helper plus C's version mismatch and missing-helper failure contract. |
| C-021 | C | 98 | Literal paths, traversal checks, and symlink containment protect the actual write set. |
| X-001 | HYBRID | 93 | B's person-origin invocation flag plus C's scoped evidence, revocation, and new-session reauthorization. |
| X-002 | HYBRID | 100 | A and C remove merge, as the seed explicitly requires. |
| X-003 | C | 90 | Retain clarification-only compatibility; reject B's false fixture rationale and forbidden merge example. |
| X-004 | HYBRID | 98 | B and C keep commit state outside the closed ledger and archive-parser grammars. |
| X-005 | C | 94 | Stage mandatory evidence, show its full scope, and stop on live-writer conflicts rather than silently absorbing it. |
| X-006 | HYBRID | 94 | B and C reject retroactive commits without an attempt initiated under valid authority. |
| X-007 | C | 97 | Hook-modified files require renewed review, not merely a newly flagged invocation. |
| X-008 | HYBRID | 100 | A/B visible Git writes are mandatory; retain C's journal and verification without hiding mutations. |
| X-009 | C | 87 | New branch mutations are unnecessary to the decided scope and enlarge operational risk. |
| X-010 | C | 87 | Default read-only status is safe and useful; unknown operations still stop. |
| X-011 | A | 96 | Uses the developer guide's documented front-matter vocabulary, unlike B's unsupported complexity value. |
| X-012 | HYBRID | 85 | A's bounded initial mutation scope plus C's explicit nesting visibility and selected-path containment. |
| X-013 | B | 93 | Clean ancestor-only advancement is useful while preserving ahead or diverged local work. |
| X-014 | C | 94 | Local pointer recording need not require publication; report readiness unknown and leave publication checks downstream. |
| X-015 | HYBRID | 98 | B acknowledges possible clone/fetch; C additionally scopes authority to approved remote identity. |
| X-016 | A | 98 | Preflight before ledger creation satisfies the promised no-write refusal behavior. |
| X-017 | A | 95 | Its allowlist avoids object-writing verbs; B's private index does not make object writes read-only. |
| X-018 | A | 95 | A's explicit total-header limit avoids B's demonstrably overlong regex acceptance. |
| X-019 | B | 96 | Distinguishes source package from managed task package instead of overloading the same alias. |
| X-020 | B | 95 | Separates configured hook policy from actual installation and independently validates message structure. |
| X-021 | NONE | 96 | All misstate tracked files; actual tracking does not automatically override the user's staging prohibition. |
| A-001 | NONE | 97 | None defines invalid or vanished ledger-path handling before a multi-path add. |
| A-002 | HYBRID | 91 | A/B/C boundary timing fits managed current-file FINAL; preserve that input contract and check legacy review too. |
| A-003 | NONE | 94 | None fully defines authority lifetime across later turns and compaction within one invocation. |
| A-004 | C | 94 | Readiness remains unknown from stale local refs; B's publication gate claims more than its evidence proves. |
| A-005 | NONE | 96 | None tests actual pre-commit stash/restore behavior with temporary-index commits and unrelated unstaged edits. |
| A-006 | HYBRID | 91 | A/B/C wording change has no identified exact-text pin, but worker-contract behavioral regressions remain necessary. |

## Round 2: Rebuttals

### Variant A Advocate

# Round 2 — Rebuttal for Variant A (architect; maintainability and extension scaffolding)

"Verified" means I re-read the line or re-ran the check read-only in this worktree in this round. Four git behaviours were checked in throwaway repositories under `/tmp` (git 2.47.3), which were removed afterwards. Nothing in the repository was changed.

#### Response to criticisms

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

#### Updated assessment of B and C

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

#### New evidence

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

#### Proposed resolution for the six open points

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

#### Per-point votes

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

### Variant B Advocate

# Round 2 — Rebuttal for Variant B (analyzer; root cause and evidence for architecture)

"Verified" means I re-read the line or re-ran the check read-only in this worktree in this round. Two git behaviours were tested in a throwaway repository under `/tmp` (git 2.47.3), removed afterwards. Two git-scm documentation pages were read for E3. Nothing in the repository was changed. `<name>` is the package name, as in B's alias table.

#### Response to criticisms

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

#### Updated assessment of A and C

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

#### New evidence

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

#### Proposed resolution for the six open points

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

#### Per-point votes

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

### Variant C Advocate

#### Response to criticisms

C should not be implemented unchanged. My revised position is a hybrid: A's explicit integration map and bounded command surface; B's distributed planner, visible writes, and executable tree comparisons; C's prepared evidence, exact reconciliation, and honest failure states.

**Steelman first.** A's objection is not merely that C is complicated: C must fit existing permission checks, parser contracts, and installation surfaces. B's objection is not merely that local state is inconvenient: each promised safety property needs a check against evidence that actually survives a crash. Those objections are correct. Conversely, reducing the number of files does not remove the need to define prepared state, ownership, and recovery precisely.

1. **Hidden mutation defeats the guard — X-008, S-008. Concede without qualification.** C's original helper-executed commit is unacceptable. A and B are right that the actual add, commit, and ref writes must be literal, host-visible Git calls. Split preparation, agent execution, and verification. Internal helper reads are not individually gated; B's Round 2 E6 correctly narrows the claim. Implementation-side inspection ignores submodule contents and refuses gitlinks; person-requested submodule inspection has its separately disclosed trust boundary. Never switch execution context to escape a denial.

2. **An instruction is not a testable switch — X-001, C-003/004, A-003. Concede the underspecification, not the claim that chat can never convey authority.** The seed explicitly offered a session instruction as an option, and the worker contract explicitly recognizes scoped owner confirmation recorded from chat. B's Round 1 steelman acknowledges this. But a parsed person-origin invocation flag is clearer. Adopt it, checked once for the current run, with C's scoped evidence, revocation, and fresh-run rules. A flag is mechanically parseable; its human provenance remains a protocol check, not something an editable sidecar can prove.

3. **Certain migration/test failures omitted — C-019, S-005/006/010. Concede.** Incorporate A's routing-row and S23 migration, removal of the merge example and its stale classification row, plugin parity and legacy-command absence checks; incorporate B's one-row-per-new-write-pattern inventory. Add A's Round 2 discovery that the retry Ruling text currently says no commit follows it. Use a lazily loaded implement-side `refs/commit-step.md`. Give every behavior a named test and AC mapping in the merged spec; keep executable observations where meaningful. C's deferred filenames were acceptable for exploration, not sufficient for this final handoff.

4. **Necessary STOP contract deferred — C-007. Concede.** Adopt two explicit tested codes: `E-COMMIT-PRECONDITION` before commit-feature writes, and `E-COMMIT-REFUSED` at a prepared boundary. The latter stops before the next Q0, leaves the task complete, and records refusal/failure/uncertainty outside the ledger. Update the closed STOP sentence and every exact-text consumer. No implicit exception to the existing closed table.

5. **Nested mutation and multi-repository machinery exceed this delivery — X-012. Concede.** Initial mutation supports selected top-level registered modules only, never recursive update or nested content commits. Report nested state as unsupported/not inspected rather than silently claiming completeness. Retain per-selection old/new IDs and completed/untouched/failed reporting when several selected top-level updates partially succeed; that is an honest result, not an added transaction service. No rollback of earlier successes.

6. **C refuses the common recorded-target advancement — X-013. Concede.** Adopt B's clean ancestor-only update: an initialized HEAD may advance to the recorded gitlink only when ancestry is established locally. Ahead, diverged, dirty, conflicted, or unknown ancestry refuses. No remote-tip update, force, stash, or unselected recursion. Preserve C's approved-remote and exact-target revalidation.

7. **C removes advertised branch behavior — C-001, X-009. Changed view.** A's strongest evidence is the current command's explicit branch-management trigger, not merely a generic usage placeholder. That does not prove a precise create/switch API already existed, but retaining a bounded branch create/switch surface is reasonable for this refactor. Accept A's clean-tree, no-force, attached-state and protected-name guards. Cleanup remains routing only; no deletion implementation.

8. **Message source and compatibility flags — C-002, X-003. Concede.** A supplies a real missing contract: exactly one of a person's `--message` or `--smart-commit`, delivered through an external message file and `-F`. B's fixture rationale for `--interactive` was false, but C's clarification-only meaning still leaves an extra interface with little value. Accept dropping it and the forbidden merge example, with the changed interface documented. Preserve the supported smart-commit example.

9. **Protected policy has no discovery mechanism — C-017. Concede C's unspecified verification requirement.** A and B correctly distinguish local availability from ideal knowledge. Adopt a concrete conservative floor and a truthful unknown-default notice, not an imagined remote-policy query. See the six-point resolution. This explicitly accepts a residual for differently named shared branches; it does not claim local refs reproduce server rules.

10. **Live-writer evidence ownership cannot be detected — X-005. Concede the proposed detector and scope.** There is no general liveness oracle. Adopt A's split: stage all mandatory `.dev/tasks` evidence, commit only the expanded current package plus authorized product paths. Other packages remain staged, not committed. Within the current package, sole-writer operation and joined delegates remain preconditions; known ownership conflict stops. Do not infer exclusive access from an old timestamp. This preserves the always-staged rule without pretending it mandates committing every other package.

11. **Lock cannot span visible calls and can survive a crash — NFR-002. Partly concede.** A lock file could span processes, so the claim that no process can hold a lock is not a proof that serialization is impossible. Also, never deleting a lock merely because it is old is not the same as forbidding owner-confirmed cleanup: the existing managed archive has such a recovery rule. Nevertheless, a new lock protocol is unnecessary here. Drop C's extra lock, retain one executor per ledger/worktree as an explicit unsupported-concurrency boundary, join writers, and revalidate state. No claim of protection from arbitrary same-user writers.

12. **Journal directory/request schema are heavier than needed — S-011, FR-021/022. Concede the container, defend the information.** Accept one append-only sidecar, not a new journal directory. Use small fixed prepare/verify interfaces and a versioned output; no general request-envelope framework. But the prepared parent, exact paths, candidate identity, task generations, durable result, and malformed-state refusal remain necessary. A version field alone cannot substitute for validating the actual fields. A and B now explicitly accept prepared evidence, so this is mostly agreement.

13. **Q0 cleanup destroys required proof — C-011. Concede.** Preserve Q0/review evidence until boundary preparation has captured and pinned the necessary candidate, and amend both completion cleanup and resume row 1. A pending prepared boundary must not depend on references a later unflagged resume deletes. B's dedicated boundary pin is useful, but retain it through unresolved or uncertain outcomes, not just through success. A terminal attempt failure is not proof that boundary recovery no longer needs evidence.

14. **Self-reference and weak crash reconciliation — C-010, S-011. Concede the unresolved construction; strengthen the amendments.** B correctly identifies that A's whole-tree hash cannot include a line naming that same tree hash. C already warned about this in Round 1. B's exclusion of the sidecar helps, but comparing a committed sidecar with its *current* working copy fails once a resume appends a run line. The resolution below freezes the prepared sidecar independently of later appends and pins the final candidate outside the sidecar.

15. **Deadlines, trailer spelling, results and message validation left open — C-012/013, NFR-003. Concede.** Use `Implement-Boundary:` with plan/task/verdict trailers; independently enforce a 72-character subject and required session attribution. Use B's external temporary message file. Specify per-Git-read timeout of 10 seconds and per-mutation timeout of 120 seconds, bounded captured diagnostics, and no automatic retry after timeout. These are proposed acceptance limits, not measured hook compatibility. A timeout or signal requires read-back and yields `uncertain` until proved otherwise; never disable signing or hooks to meet the deadline.

16. **Configured hooks are not installed hooks; runtime-directory claims are false — X-020/021. Concede factual errors while preserving policy.** Follow B's separation of configured policy from observed installation. Validate messages independently and install hooks deliberately in fixtures. All three misstate which runtime files are tracked; an existing tracked cache does not waive the user's explicit staging ban. Automatic staging remains settings-only there, with scoped explicit authorization for that exception, and no force-add. Conflicts require a person, not a widened allowlist.

17. **Missing shared-assumption coverage — A-001/002/004/005/006. Concede missing rules/tests.** Refuse ambiguous or unrepresentable ledger paths before staging; skip a proven transient create-then-delete path only with evidence, never every absent typo. Preserve current-file FINAL inputs and test legacy as well as managed review. Local remote refs are not current remote proof. Run a real pinned pre-commit-framework fixture with `--only`, partial staging and unrelated unstaged edits; a plain shell hook is insufficient. Keep worker-contract regressions even where no exact K3 wording test exists. No tests or Git experiments were executed in this round.

#### Updated assessment of A and B

### A

**Steelman.** A has become much more implementation-ready after accepting a skill-local helper, sidecar state, prepared evidence, per-path integrity checks, visible mutations, and no automatic retry. Its registry, parity tests and integration inventory are now useful scaffolding rather than a competing state machine.

**Arguments that changed my mind:**

- Existing branch-management wording supports retaining a narrow create/switch interface; C's categorical exclusion was unnecessarily disruptive.
- `--message` resolves an actual message-source hole in one turn. Keeping clarification-only `--interactive` is not worth preserving that ambiguity.
- Stage-all/commit-current-package is both narrower and more implementable than C's attempt to discover live owners of all evidence.
- A single sidecar can carry prepared and terminal evidence. C does not need a directory or an additional cooperating-helper lock.
- The concrete routing, fixture, and retry-Ruling inventory should be part of the requirements, not left to the implementation author.

**Arguments that did not change my mind:**

- A new flagged invocation typed *before* its Wave 0 prints a hook diff cannot logically prove that the person reviewed that later-displayed diff. C requires actual renewed review, not a temporal fiction. A protocol reviewer may review the changed candidate; a Ruling can accept a precisely explained gap, but neither is inferred from an earlier flag.
- A missing reviewed-tree header must not silently weaken candidate integrity to a pre-Q0 check. B's same-file check proves a different property. Without an accepted candidate snapshot, refuse the boundary, not the completed quality verdict.
- A's proposed 12-hex start-tree key is not a unique start generation. Content identity is not execution identity.
- A server rule does not necessarily stop a local commit on a differently named shared branch. Accepting the fallback is a stated limitation, not equivalent protection.

### B

**Steelman.** B gives the strongest operational corrections: prepared tree comparisons, durable pinning, no helper-hidden writes, no unnoticed submodule inspection in implementation, and explicit detection of hooks modifying hash-pinned plan/source evidence. B's Round 2 analysis improves the merged design substantially.

**Arguments that changed my mind:**

- E1/E2 establish the need for both a non-self-referential candidate definition and a reachable tree object through recovery. Adopt those requirements with the correction below.
- E4 means hook outcome verification must recompute plan/source byte hashes even when the Git commit succeeds. Changed pinned evidence is not a harmless formatter result.
- E6 means visible commit enforcement cannot be advertised as enforcement of every helper subprocess. Implementation inspection must avoid entering submodules.
- The absence of a downstream publication check removes C's claimed safety net. I change X-014 to a conservative local-ref eligibility gate, while explicitly rejecting its description as verified publication.
- B's bounded authority record is safer than storing a full inline prompt, which may contain secrets, newlines or misleading command text.

**Arguments that did not change my mind:**

- A last-fetch timestamp does not prove the selected remote-tracking ref was refreshed. It cannot repair the false-positive case after a remote rewrite. Report the observation as local, not current publication.
- Comparing the sidecar in a recovered commit with its current working copy is insufficient once the resume itself writes an `off`/`on` run record. Freeze and compare the prepared version instead.
- `refused` being a terminal attempt record must not make a hook-failed boundary permanently disappear. Distinguish attempt termination from boundary satisfaction.
- "Last compliant review" excludes valid non-compliant tasks completed under a scoped Ruling. The required snapshot is the latest reviewed-and-accepted candidate, including that path.

#### New evidence

All paths in the following source citations are relative to `/home/coder/workspaces/worktrees/IronClaude/issue-326/`. Repository checks were read-only. Logical counterexamples below are deductions, not executed tests.

1. **N1 — The start SHA is a tree, not a unique run generation.** `src/superclaude/skills/sc-implement-protocol/SKILL.md` defines Q0 by snapshotting content with `write-tree`; `refs/ledger.md` defines a start line as only task ID plus SHA and reuses it on resume. Two distinct starts with identical contents can have the same tree SHA, even before considering a 12-hex truncation collision. A/B's key therefore does not prove a new start occurrence differs. Bind the key to ledger identity, source identity, full task IDs and the ordinal of each actual start record, plus its full SHA; never invent a new start on resume.

2. **N2 — A/B's resume run-line order breaks B's sidecar success comparison.** Both Round 2 proposals append a run line before reconciliation. B's E1 then compares the sidecar blob in HEAD with the working-tree sidecar before appending the terminal line. On a crash after commit, the working copy already contains the *new run line*, which that prior commit could not include. The comparison necessarily fails even when the commit was exactly right. Compare against immutable prepared bytes/tree, not today's sidecar. Add this exact managed crash → unflagged resume scenario to acceptance tests.

3. **N3 — Accepted non-compliant tasks have no required last compliant review.** `src/superclaude/skills/sc-implement-protocol/refs/ledger.md` explicitly preserves a non-compliant verdict on a post-Ruling complete line; `refs/qa.md` permits that completion after scoped user acceptance. A/B's latest-*compliant*-review condition can select no snapshot, or an obsolete one, for a legitimate task. Capture the exact candidate the reviewer inspected and the person accepted. Re-review if its bytes change, without changing the accepted verdict to compliant.

4. **N4 — Re-review may append another complete line without a new start.** The ledger's "Re-review complete line" section explicitly allows this after a defective saved-prompt FINAL recovery. Therefore a new complete line is not automatically a new boundary generation and must not trigger another product commit. Tie eligibility to start occurrence and existing satisfied boundary identity; later evidence remains staged unless separately authorized.

5. **N5 — Literal Git arguments do not fix the ledger's path encoding.** `src/superclaude/skills/sc-implement-protocol/refs/ledger.md` defines `files=` as comma-separated repo-relative paths and expressly disallows commas in evidence paths. A real filename containing a comma is ambiguous before Git receives it. Do not widen the ledger grammar in this feature: refuse an unrepresentable/ambiguous touched path before staging, naming the encoding limitation. Also reject newline/control-character encodings that the line grammar cannot faithfully carry.

6. **N6 — Step 5 preflight cannot promise absolutely no earlier repository writes.** The currently read Wave 0 step 3 persists inline prompt `source.md` before step 5. A and B's preflight placement is right relative to ledger creation, but "before any write" is stronger than the existing intake order supports. State "before ledger creation, product edits, or commit-feature state writes; existing inline-source intake may already have occurred", or explicitly move commit-only identity checks ahead of intake. Do not claim to have changed ordinary unflagged intake by accident.

7. **N7 — No downstream publication gate is present in the checked implementation.** A targeted search of `src/superclaude/pr_submit/` for submodule/publication-related terms found only the conflict halt. This corroborates A/B's narrow claim about that package; it is not proof about every external user publication route. C must remove its assertion that the existing publication command checks availability.

8. **N8 — Refusal/pin cleanup needs an explicit distinction.** B deletes the boundary pin after a terminal line, but also declares candidate-change refusal terminal. A retry after hook review is still required by all three revised positions. If refusal means both "attempt ended" and "boundary settled forever", the resume either skips needed work or loses its prepared proof. Keep unsuccessful attempts auditable; retain needed pins while unresolved, and require an explicit reprepare under fresh authority/review for changed contents. Never retry an uncertain outcome.

#### Proposed resolution for the six open points

### A-003 — Authorization lifetime

**Accept A's run-scoped flag and revocation proposal; accept B's bounded record, after-step-6 write, and informed-Ruling amendments. Reject treating a sidecar as independent human authority.**

The merged spec shall say:

1. Parse `--commit-tasks` only from the option prefix of the person's own `/sc:implement` invocation. Other origins refuse before commit-feature writes. Off by default; off under unattended execution. The static no-auto-insertion check is secondary to runtime provenance.
2. Check provenance once for this run. After preflight and ledger opening, record a bounded option/source identity, repository/worktree identity, monotonically increasing run number and on/off state. Never store a full inline prompt or credential-bearing text. A run without opt-in and without existing commit state creates no sidecar.
3. That grant covers continuation turns and compaction of the same active run. It expires at run stop, new invocation or new session; resume always runs Wave 0 and requires fresh opt-in for mutations. A stored `on` is evidence only; helper state validation is necessary, not proof of personhood.
4. A plain-language revocation takes effect before the next attempt. A Ruling neither grants nor renews commit authority. When authority is still active, explain the commit consequence before asking for acceptance.
5. Reconciliation of an already-created commit does not require commit authority, but writing recovery evidence is still an evidence write, not a read-only operation. Do not run add/commit merely to reconcile. An unflagged resume may record and stage recovery evidence under the normal evidence rule.
6. Show pending boundary identities and intended paths. For a changed/re-written candidate, obtain actual renewed review *after* showing the changes; the already-typed flag alone is insufficient. Test later-turn Rulings, compaction, revocation, unflagged resume, stale run records and fresh-session default-off.

### C-010 — Crash between commit and record

**Accept A's prepared-before-add structure, strict expected parent and fail-closed HEAD-only recovery. Accept B's non-self-reference, pinning and pinned-file checks. Reject their start-SHA-only key and current-sidecar recovery comparison.**

The merged spec shall say:

1. Boundary identity is SHA-256 over a canonical tuple of repository/worktree identity, stable ledger/source identity, ordered full task IDs, and each task's start-record ordinal plus full start SHA. Persist that binding; resume reuses it. Repeated complete lines for the same start do not create new boundaries. Hash prefixes are display-only.
2. Prepare while task proof still exists. Validate no pre-Q0 product delta and equality with the latest reviewed-and-accepted candidate. Expand the exact commit set to literal files; include authorized deletions and both rename endpoints. Reject ambiguous/missing proof, absent typos and encoding limitations. An unchanged transient deleted file may be skipped only when its lifecycle is established.
3. Compute a tree from the expected parent plus selected contents **excluding only the sidecar**. Durably append a prepared record with that tree ID, exact selected paths, expected parent, boundary identity, source/plan hashes and attempt number. No user-index/ref/working-tree mutation by a helper is hidden in this claim; sidecar persistence and object creation are disclosed effects.
4. After that prepared append, build the **full final candidate tree**, including the frozen prepared sidecar bytes for managed runs. Have the agent visibly pin this full tree under the boundary identity before add/commit. The sidecar never names this full tree's own hash, so there is no self-reference. The deterministic ref points to it externally. Its sidecar blob freezes the prepared bytes even if future run/result records are appended to disk. If interruption leaves a prepared record without its required pin, return `uncertain`; never infer permission to commit from incomplete preparation.
5. The visible commit carries `Implement-Boundary:` plus plan and ordered task/verdict trailers. Verify exactly one parent equals the prepared parent, the full committed tree equals the pinned final candidate, changed paths equal the authorized changed subset, the key matches, and managed plan/source hashes still match. No exclusion of arbitrary evidence changes. Legacy sidecar stays outside the commit set.
6. Reconcile before task selection, all-complete return, or archive short-circuit. HEAD exactly proves success → `already-committed` and append recovered evidence. HEAD still equals parent → pending; an authorized attempt may proceed only with unchanged validated inputs. Changed candidate requires renewed review and a new prepared attempt under the same unsatisfied boundary. Other history, absent proof, duplicate/conflicting evidence or uncertain effects → stop, no retry or repair. Inspecting only HEAD is conservative: a person's later commit produces uncertainty, not a history search or duplicate.
7. Stage terminal evidence without a housekeeping commit. Preserve a boundary pin through pending/uncertain state; delete only after verified committed/recovered/no-change satisfaction, or explicit owner-resolved abandonment. Failed attempt versus satisfied boundary are distinct. Tests include C's five crash points, two resumes, unflagged managed recovery with a new run line, pin loss/GC, changed hooks, pinned plan/source changes and repeated complete lines.

This is a small extension of B's pin: point it at the final frozen candidate, rather than relying on a live sidecar to reconstruct prepared bytes. It adds no journal directory or daemon.

### C-015 — Pointer commit eligibility

**Accept A's clean/registered/one-level/exact-path checks and B's inspection-boundary clarifications. Accept detached-at-referenced-target behavior; reject C's unconditional attached-branch requirement. Add C's exact target binding.**

The merged spec shall say:

- Only explicitly selected top-level registered gitlinks, with initialized clean indexes/worktrees, no conflicts, and an exact full target object ID captured in the authorized plan. Revalidate that module HEAD still equals that target immediately before and after parent commit.
- A detached HEAD at a target contained in a local remote-tracking branch is eligible; no invented preservation branch is needed. A detached target contained in no local or remote-tracking branch refuses `detached-new-commits`. An attached but non-remote-contained target refuses the conservative X-014 check below.
- Parent preconditions, literal isolated path set, hook verification and normal message rules apply. Commit only the selected gitlink changes, no `.gitmodules`/config change and no inner dirty content. Existing mandatory evidence staging remains separate.
- Multiple selected pointer targets in the same parent may use one authorized parent commit with its explicit set; no nested traversal or inner-repository content commit is implied. A zero pointer delta is `no-change`.
- Helper inspections do not bypass a denied operation. Report that direct `git submodule` calls are denied in launched sessions and that helper subprocess reads are not separately gated. No workaround for a denied mutation.

### C-017 — Other repositories' protected branches

**Accept A's practical fallback and B's additive-default correction. Reject C's unresolved-policy blanket block as insufficiently operationalized.**

The merged spec shall say:

- Always refuse local-history mutation on detached HEAD and on `master`, `main`, `integration`, plus any locally resolved `origin/HEAD` target. Resolve per actual target repository, including a module when operating inside it. Never remove a fixed name because the local default differs.
- Incorporate additional protected names explicitly established by the current repository's verified instructions or a scoped person-confirmed policy; report the source. No remote query or parent-repository inference.
- If `origin/HEAD` is absent, show `default unknown` and the enforced names, then allow an otherwise authorized local operation. If instructions conflict or explicitly protect the target, refuse; missing discovery is not permission to override known policy.
- Do not state that fetch always creates or never creates this ref; B correctly identifies version/config differences. A local default ref may also be stale. Do not present server protection as protection against local commits. Differently named unknown shared branches are an accepted, visible residual.

### S-011 — Commit-state location and grammar

**Accept A/B's single sidecar locations, unchanged ledger/archive grammar, lazy ref and post-commit evidence lifecycle. Accept B's boundary-pin exception to resume cleanup. Reject current-working-sidecar comparisons and deletion of unresolved proof.**

The merged spec shall say:

- Use `commits.md`: managed `<package>/artifacts/commits.md`; legacy `<run>/commits.md`, unstaged like legacy evidence. Preserve state through archive movement by stable package identity, not an absolute old package path.
- Document versioned `run`, `prepared` and `result` record forms once, with bounded, unambiguous escaping for option/source/path data. The parser rejects unknown versions, malformed records and truncated tails; no silent repair. One writer, flushed durable appends before side effects. Record attempt number separately from stable boundary identity.
- Preparation stores exact paths and immutable candidate binding as C-010 specifies. Terminal result fields are outside their own commit; keep managed evidence staged and report final outstanding evidence honestly. A later run line is not part of an earlier prepared candidate.
- `committed`, `already-committed`, `no-change` satisfy a boundary. `refused`, `failed`, `uncertain` end an attempt and stop advancement; they do not implicitly erase eligibility or permit retry. Uncertainty requires resolution. An unchanged-input retry still needs active authority; changed contents need renewed review and preparation.
- Q0/review refs survive until required proof has been durably transferred; pending boundary refs survive ordinary complete-task cleanup even on unflagged resume. No new lock, directory or ledger record. Ref/helper schema, atomicity, corrupt-tail, archive, and pin-cleanup tests are required.

### X-014 — Target absent from remote-tracking branches

**Change my vote: accept A/B's conservative refusal, reject their description of containment or FETCH_HEAD time as proof of publication. Reject C's reliance on an existing downstream availability gate.**

The merged spec shall say:

- A selected pointer target must be contained in at least one local remote-tracking branch of that module, otherwise refuse `submodule-unpublished` and make no parent pointer commit. No override is added here. This is a conservative *local-ref eligibility condition*, not verified publication.
- Print matching local ref names and, if available, FETCH_HEAD file modification time labelled exactly as a local fetch-file observation. Do not say every displayed ref was fetched then, that every absent ref is genuinely unpublished, or that a contained commit is still downloadable remotely.
- No automatic push/fetch, including to remedy the refusal. Any separate person-performed publication/fetch remains subject to repository permission and remote-identity policy; do not promise the person can push a third-party module.
- State both residuals: stale refs can falsely refuse a locally safe target, and remote rewrite/deletion can falsely suggest availability. The current publication workflow has no checked module-availability gate; adding one is out of scope. The local gate reduces a common failure without claiming to eliminate it.

#### Per-point votes

| Point | Winner | Confidence | Reason |
|---|---|---|---|
| S-001 | HYBRID | 88 | C's compact contracts with A's navigation tables; retain essential evidence without B's repetition. |
| S-002 | B | 94 | Explicit alias resolution prevents A's package ambiguity and C's opaque single letters. |
| S-003 | HYBRID | 94 | A's verified baseline plus B's falsifiable root causes explains facts and preservation obligations. |
| S-004 | C | 82 | Contiguous identifiers simplify final traceability; renumber once after merging. |
| S-005 | HYBRID | 98 | A's named test matrix, B's existing-consumer inventory, C's fault injection and integrity assertions. |
| S-006 | HYBRID | 94 | A's acceptance-to-test mapping plus B's runnable observations; behavior tests outrank text counts. |
| S-007 | B | 90 | Root cause and residual columns distinguish mitigation from proof. |
| S-008 | HYBRID | 99 | B's mirrored planner and visible execution, A's shared constants, C's versioned results and durable preparation. |
| S-009 | HYBRID | 91 | A's registry and safety reference, B's lazy read-path loading. |
| S-010 | B | 96 | Dedicated lazy commit-step reference makes implementation integration concrete. |
| S-011 | HYBRID | 98 | B's sidecar, C's prepared evidence, A's unchanged-parser discipline; freeze sidecar bytes and retain unresolved pins. |
| S-012 | A | 91 | Merge-removal and explicit evidence-scope decisions prevent silent scope drift. |
| S-013 | HYBRID | 98 | C's integrity and uncertainty, A's parity/version rules, B's bounded distribution and execution budgets. |
| C-001 | A | 90 | Retain advertised branch management with tight guards; remove forbidden publication and merge; add bounded submodule operations. |
| C-002 | A | 92 | Explicit message or smart drafting closes the message-source gap; remove ambiguous interactive compatibility. |
| C-003 | HYBRID | 96 | B's person-origin refusal plus C's repository, path and target scope; no replayable unauthorized write plan. |
| C-004 | HYBRID | 96 | B's provenance check once per run, A's static anti-insertion check; neither sidecar nor flag proves personhood. |
| C-005 | HYBRID | 99 | A's named resume/last-task positions plus C's writer barrier and pre-short-circuit reconciliation. |
| C-006 | HYBRID | 95 | A's before-ledger preflight plus C's state capture; acknowledge existing inline-source intake writes. |
| C-007 | A | 95 | Two explicit STOP codes preserve precondition versus boundary effects; update all closed-table consumers. |
| C-008 | HYBRID | 99 | B's Q0 comparison plus C's reviewed-and-accepted candidate equality; no missing-proof fallback. |
| C-009 | HYBRID | 99 | B's frozen-tree comparison plus C's exact scope, pinned-evidence checks and uncertainty classification. |
| C-010 | HYBRID | 99 | C's stable prepared boundary and fault tests, B's pinned candidate, A's strict parent recovery; correct sidecar comparison. |
| C-011 | B | 97 | Defer cleanup until durable proof transfer; unresolved boundary pins survive unflagged resumes. |
| C-012 | HYBRID | 97 | A's validated subject/verdict schema, B's plan trailer, C's full boundary identity and attribution preservation. |
| C-013 | B | 97 | External temporary message file avoids accidental evidence inclusion. |
| C-014 | HYBRID | 97 | C's independent nullable facts plus A's explicitly derived action-state precedence. |
| C-015 | HYBRID | 93 | B's clean referenced target, C's exact gitlink binding, A's isolated top-level parent commit. |
| C-016 | C | 98 | Person-selected cleanup route correctly distinguishes archive writes from inspection. |
| C-017 | HYBRID | 90 | A/B conservative floor and additive local default, C's repository-policy sources and truthful limitations. |
| C-018 | HYBRID | 96 | B's commands and preconditions, C's before/after effects; no automatic or blanket history-changing undo advice. |
| C-019 | HYBRID | 99 | A's routing/fixture migration, B's write classifications, C's regression boundaries; include retry-Ruling correction. |
| C-020 | HYBRID | 98 | B's mirrored skill-local distribution plus C's missing/version-mismatch refusal without installation fallback. |
| C-021 | C | 99 | Literal path containment is essential; separately refuse ledger-unrepresentable names. |
| X-001 | HYBRID | 97 | A/B parsed flag and person provenance, C's scope, revocation and fresh-run authority limits. |
| X-002 | HYBRID | 100 | A/C remove merge; the seed explicitly forbids it. |
| X-003 | A | 92 | Remove interactive and merge example; false fixture rationale cannot justify preserving an unnecessary interface. |
| X-004 | HYBRID | 99 | B/C external commit state preserves ledger and archive-parser contracts. |
| X-005 | A | 96 | Stage all mandatory evidence; commit current package and authorized paths only, avoiding other packages without a liveness oracle. |
| X-006 | HYBRID | 98 | B/C prohibit retroactive unflagged-task commits; only an authorized boundary generation is eligible. |
| X-007 | C | 99 | Changed hook contents need actual renewed review after disclosure, not merely an earlier flagged invocation. |
| X-008 | HYBRID | 100 | A/B visible Git mutations preserve guard enforcement; C's preparation and verification remain separate. |
| X-009 | A | 90 | Preserve advertised branch management through clean-tree and no-force guarded create/switch operations. |
| X-010 | C | 95 | Bare invocation defaults to read-only status; unknown operations still stop. |
| X-011 | A | 96 | Developer-guide vocabulary meets the explicit seed criterion; practice drift is separate. |
| X-012 | HYBRID | 95 | A's top-level-only mutation plus C's explicit unsupported nesting and selected-path containment. |
| X-013 | B | 98 | Clean ancestor-only recorded-target advancement preserves ahead/diverged work and supports the common update. |
| X-014 | HYBRID | 91 | B's conservative containment gate, C's honest stale-ref limitations; no claim of fresh remote availability. |
| X-015 | HYBRID | 97 | B/C disclose clone/fetch effects; A's concrete URL comparison supports C's approved-identity scope. |
| X-016 | A | 98 | Preflight precedes ledger creation; qualify absolute no-write claims for existing inline intake. |
| X-017 | HYBRID | 98 | B's private-index comparison is useful; C's honest effects distinguish object/evidence writes from visible repository mutations. |
| X-018 | A | 99 | Check total subject length directly; B's regex tail bound violates its own limit. |
| X-019 | B | 98 | Distinct source-package and task-package aliases avoid incorrect destinations. |
| X-020 | B | 98 | Configured hooks are not installed enforcement; independently validate and test deliberately installed fixtures. |
| X-021 | NONE | 99 | All misstate tracking; preserve explicit staging policy rather than infer authorization from tracked caches. |
| A-001 | NONE | 99 | None originally defines safe absent-path policy; refuse typos, skip only proven transient deletions. |
| A-002 | HYBRID | 95 | A/B/C current-file final review remains valid; pin both legacy and managed reviewer inputs in regressions. |
| A-003 | HYBRID | 97 | A's run lifetime, B's bounded provenance record, C's revocation and fresh-session rule; stored records cannot manufacture authority. |
| A-004 | C | 98 | Local refs and fetch-file timestamps cannot establish current remote availability, even with a conservative eligibility gate. |
| A-005 | NONE | 99 | No original fixture exercises real pre-commit stash/restore with partial staging and temporary-index commits. |
| A-006 | HYBRID | 94 | A/B/C identify no exact K3 text pin; behavioral worker-contract regressions still apply. |

## Round 2.5: Invariant Probe

Full results are in `invariant-probe.md` (30 findings; 3 HIGH UNADDRESSED blocked convergence until Round 3).

## Round 3: Final Arguments

### Variant A Advocate

# Round 3 — Final arguments for Variant A (architect; maintainability and extension scaffolding)

"Verified" means I re-read the line read-only in this worktree in this round, or re-ran the behaviour in a throwaway repository under `/tmp` (git 2.47.3, removed afterwards). Upstream pre-commit source was read from `pre-commit/pre-commit` (`main` branch: `pre_commit/staged_files_only.py`, `pre_commit/commands/run.py`, `pre_commit/commands/hook_impl.py`, `pre_commit/error_handler.py`). Nothing in the repository was changed.

#### Final position

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

#### Resolution of the HIGH findings

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

#### Ruling on the other 19 findings

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

#### Final concessions

1. **C's N1 (boundary key).** The key must bind the ledger position of each member's `start` line, not only the tree hash. The hash records content; the position records which start it was.
2. **INV-006.** C's frozen full-candidate success test replaces both A's and B's success predicates.
3. **X-007 (renewed review), C's objection.** A person can only have reviewed a diff that was shown before they typed the new flagged line. The `rewritten=` pin, shown in the refusal, is what makes that true.
4. **INV-021.** A's dropped `dirty` refusal did protect something real. It returns as a narrow check at each boundary, not at Wave 0.
5. **Unflagged runs and pending boundaries.** The Round 2 text "an unflagged run prints the pending boundary and leaves it alone" (A and B) was unsafe (INV-022, INV-023). HR-1.4 replaces it. This is the one place where my final position changes the Round 2 consensus.
6. **C-010 item 7.** C was right that owner-resolved abandonment needs a defined record. HR-3 supplies it.

#### Per-point votes

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

### Variant B Advocate

# Round 3 — Final arguments for Variant B (analyzer; root cause and evidence for architecture)

"Verified" means I re-read the line read-only in this worktree in this round, or re-ran the behaviour in throwaway repositories under `/tmp` (git 2.47.3), all removed afterwards. Upstream pre-commit source was read from `pre-commit/pre-commit` on `main` (`pre_commit/staged_files_only.py`, `pre_commit/commands/run.py`, `pre_commit/error_handler.py`) and searched with the GitHub code search. The real pre-commit framework is not installed here, so the hook experiments emulate it with the exact git commands of `staged_files_only.py`. Nothing in the repository was changed.

#### Final position

1. Structure and surface stay as agreed: a `/sc:git` command plus the `sc-git-protocol` skill with per-group refs and a mirrored read-only skill script; status (default), add, commit (`--message` or `--smart-commit`), branch list/create/switch, cleanup as a route to `/sc:worktrees`, submodule status/update/commit-pointer; no push, pull, merge or `--interactive`.
2. Between-task commits need a person-typed `--commit-tasks`, checked once in Wave 0 and recorded as a `run` line in `commits.md` that carries `ledger-lines=` and `branch=` (A's Round 3 mechanism, with three corrections below).
3. A task is eligible for a commit only when the **first** `complete` line after its current `start` was written in a flagged segment. A due boundary is prepared late only when the crash explains it; any other due boundary means a run advanced without settling it, and it is never committed.
4. **Settle before advance** (A): no `start` line, all-complete step or archive gate while a boundary is unsettled. Every unsettled state, in every run, offers the owner `abandon`, and `adopt` when its precondition holds. So no state is a dead end.
5. **The person's files outside the commit set are always recoverable.** Immediately before each commit the agent pins a full worktree snapshot (the Q0 command). After every attempt a second snapshot is compared with it, and any path outside S that changed is reported with a restore command. This replaces A's `unstaged-outside` refusal, which misses assume-unchanged files and brings back the coarse `dirty` gate.
6. An interrupted commit (timeout or signal) writes no terminal line. The next run's reconcile classifies it, so it never races a hook that is still running.
7. Hooks are never bypassed. Nothing retries automatically inside a run. The owner's `abandon` and `adopt` answers are given in chat and recorded by the executor, never written by the owner.

#### Resolution of the HIGH findings

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

#### Ruling on the other 19 findings

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

#### Final concessions

1. **INV-001.** My Round 2 eligibility rule depended on pins that an unflagged resume deletes (my own E7). A's `ledger-lines` segments are the right mechanism; my changes to it are corrections.
2. **INV-006 and C-009.** My E1 success check compared the committed sidecar with the working-tree sidecar. A resume appends a `run` line first, so that check fails exactly when the commit was right (C's N2). C's frozen full-candidate test replaces it, and my C-009 vote moves from B to HYBRID.
3. **Unflagged runs.** My Round 2 C-010 item 5 ("an unflagged run prints the pending boundary and leaves it alone") was unsafe (INV-022, INV-023). Settle before advance replaces it.
4. **A-001.** My Round 2 reason, skip every absent path, drops real deletions (INV-007).
5. **INV-024.** My FR-016 shared step 3 staged `.dev/tasks` before every `/sc:git commit`. The order is fixed above.
6. **X-013.** Fast-forward-only was a stand-in. The real rule is "orphan no commit" (INV-009, A's fix).
7. **HR-2.3.** A is right that the timeout must be the tool's maximum, not C's 120 seconds.

#### Per-point votes

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

### Variant C Advocate

#### Final position

1. Merge the agreed bounded command surface: `/sc:git` plus `sc-git-protocol`, lazy operation references and a mirrored mechanical planner; default status, explicit add/commit, guarded branch create/switch, cleanup routing and top-level submodule operations only.
2. Keep push, pull, merge, PR creation, remote deletion, recursive module mutation and unattended between-task commits out of scope.
3. Person-origin `--commit-tasks` authorizes one active run, not future sessions; durable segment records establish which first completions were eligible, but never manufacture human authority.
4. Adopt A's **settle before advance**, with B's first-complete anchor, moved-on check and managed plan-check ordering; no unresolved boundary may be bypassed by task selection, FINAL or archive.
5. Retain C's full boundary identity, prepared-before-add evidence and externally pinned frozen candidate; distinguish a finished attempt from a satisfied boundary.
6. Prefer B's worktree recovery snapshot to A's `unstaged-outside` refusal, with immutable per-attempt pins, an outside-path comparison and a stop after detected damage; never overwrite recovery evidence on retry.
7. Adopt B's informed chat resolution amendments: full recorded key, reply after disclosure, `abandon` always available, conditional `adopt`, and no executor-invented acceptance.
8. State the limits honestly: one writer, Git-representable snapshot contents, local rather than fresh remote observations, package ownership and unscanned evidence are not magically proven by a helper.

#### Resolution of the HIGH findings

Repository verification in this round was read-only. I read all requested debate/probe inputs and the relevant live ledger, retry, QA, managed-workspace, worker-contract, hook-policy and launch-guard text. I also checked current Git status, hook configuration and the hooks directory. I ran no tests, hook emulations or Git mutation experiments. A's and B's experiments are supplied evidence, not experiments I independently executed.

All new field names, reason tokens and pin layouts below are proposed requirements, not claims that they already exist. References to source files are evidence for this debate, not instructions to installed primitives to look inside a checkout.

### INV-001 — Eligible completion lost before preparation

**Decision: ACCEPT B's version over A's version, with the explicit serialization and proof-retention details below.**

**Where A and B still disagree.** A uses the latest `complete`; B uses the first `complete` after a particular `start`. I vote B: the live ledger expressly permits another `complete` without another `start` in its re-review-complete section. A would retroactively authorize an unflagged completion. B also counts an unterminated final logical line and refuses late preparation after the run has moved on; both corrections prevent previous-run work from falling under a later grant. A and B agree on segment offsets and settle-before-advance.

**Evidence.** The live `src/superclaude/skills/sc-implement-protocol/refs/ledger.md` start and verdict forms have no run identity; its re-review-complete section permits repeated completions. Its resume Row 1 and the live protocol's Q0 cleanup currently delete pins at completion. The live protocol runs Q6 extras before Q7 writes completion, while managed invocation appends codegraph evidence each run. These facts require persistent eligibility, accepted-candidate proof and reconciliation before ordinary cleanup/evidence updates. The retry reference derives batch membership from overlapping start-to-first-verdict windows, not the order tasks happen to resume.

**Final numbered requirement text.**

1. **State location and write order.** Store commit state only in `commits.md`: legacy `.dev/implement/<slug>/commits.md`, unstaged; managed `<pkg-dir>/artifacts/commits.md`, staged with `.dev/tasks`. Preserve existing task-ledger record forms. Every invocation with the flag, and every later invocation where this sidecar already exists, appends a bounded `run` record after ledger validation, before any new task record or ordinary run-evidence append. The record contains monotonically increasing `run`, `commit-tasks=on|off`, `ledger-lines=<k>`, the full symbolic `branch=`, bounded option/source identity, timestamp and repository/worktree identity. A first unflagged invocation with no sidecar creates none. Revocation appends an `off reason=revoked` record with its current offset before another attempt.
2. **Counting and validation.** Define `k` as newline count plus one for a nonempty unterminated final logical line. A position `p` belongs to the last sidecar-ordered `run` record with `k < p`; equal offsets are resolved by sidecar order. Positions at/before the first offset have no grant. Reject decreasing offsets, offsets beyond the current ledger and inconsistent record bindings with `E-COMMIT-REFUSED reason=sidecar-mismatch`; reject an unparseable sidecar tail with `reason=sidecar-corrupt`, without silent repair. Never concatenate a new ledger record onto an unterminated tail: stop for ledger recovery, rather than moving that existing logical line into a new segment. Counting an existing line is not permission to repair it.
3. **Stable anchor and key.** A task generation is its actual start-record occurrence, not its tree's contents alone. Its anchor is the **first** valid `complete` following that start. Eligibility requires every boundary member's anchor to lie in an `on` segment. Later complete/re-review lines cannot create, revive or reauthorize that generation. Retain C's SHA-256 identity over canonical repository/worktree and ledger/source identity, ordered task IDs, each start-record ordinal and full start SHA. All stored keys and machine references use the full 64 hex characters; prefixes are display-only. Batch membership comes from the original overlapping windows and does not change on resume. A wholly unflagged/pre-feature completion is never retroactively committed.
4. **Proof before completion.** For an eligible first completion, pin the accepted candidate before flushing `complete`: compliant completion binds the tree of the review that supplied its verdict; a scoped Ruling binds a fresh snapshot of the accepted current outcome. Bind that pin to the same start occurrence. A missing tree is `no-accepted-tree`/`no-snapshot`, never permission to weaken the check. Keep Q0, original branch/HEAD and accepted proof through every unsettled state, including a due boundary with no prepared line. Amend both Q7 cleanup and resume Row 1. Review refs may be removed only after their required proof has been durably transferred to the accepted pin.
5. **Due versus moved-on.** An eligible all-complete boundary without preparation or a settling record is `due`. Late preparation is crash-explained only if no other task's `start` follows any member's anchor and no task remains open. Otherwise stop `E-COMMIT-REFUSED reason=out-of-protocol`, name the later start records and offer the resolution choices. Never automatically commit those later tasks. Missing preserved proof also refuses; absence of a prepared line is not proof that no eligibility existed.
6. **Reconciliation order.** Resolve managed location and verify existing plan/source pins before any recovery commit. After ledger validation, take any pending outside-S recovery observation described under INV-021 **before appending a new run line**; then append the run line and reconcile. This narrow pre-append observation prevents the executor's own new legacy sidecar line from becoming a false outside-S damage report. Reconcile precedes steps 7–9, task selection, complete-task cleanup, legacy all-complete return, FINAL and archive. The fresh run line never changes the frozen sidecar bytes against which an earlier commit is verified.
7. **Settle before advance.** `due`, pending, refused and uncertain boundaries are unsettled; a terminal failed/refused attempt does not satisfy its boundary. No new task/Q0, all-complete return, FINAL or archive is allowed while any boundary is unsettled. A flagged run may prepare a crash-explained due boundary or retry a proved HEAD-equals-parent pending/refused boundary, only after the original branch/HEAD, accepted product contents and current authority checks pass. Rebuild package evidence fresh for a new attempt; freeze it anew, never compare a new attempt with the entire old package snapshot. A changed product candidate needs actual review/acceptance after disclosure, not just a previously typed flag. There is no same-run automatic retry. An unflagged run may record a proved existing commit but makes no commit; otherwise it stops `reason=unsettled`. Uncertain or moved-history states never auto-retry. Every unsettled STOP offers the INV-027 choices.
8. **Exact recovery predicate.** Keep C's prepared-before-add record, recording attempt number, full key, expected parent/branch, exact S, accepted binding and plan/source hashes. After the prepared append, pin the full final candidate including the managed sidecar's frozen prepared bytes; its full tree hash lives in the external ref, not inside the sidecar it hashes. Only one-parent HEAD with that parent, full tree, key/trailers and authorized changed subset, with unchanged managed plan/source bytes, proves `committed`/`recovered`. HEAD equal to parent is pending, not success. Other history or incomplete proof is uncertain. A person's later commit is not a reason to walk history or create a duplicate.
9. **Acceptance tests.** Crash after accepted-pin creation and completion flush but before preparation; resume flagged twice and obtain exactly one commit. Resume unflagged first and assert no new start, no commit and no lost pin. Cover unflagged completion followed by flagged re-review, revocation, equal segment offsets, an unterminated parseable tail, decreasing/out-of-range offsets, a later task start written by a stale copy, changed managed plan, repeated complete records, a resumed batch and GC between crash/resume. Also crash after commit before result in both managed and legacy runs: the new run record must not cause false recovery failure or false outside-S damage.

### INV-021 — Hook interruption can remove unrelated worktree edits

**Decision: OWN VERSION, based on B's snapshot-and-compare resolution. I vote B over A on the substantive disagreement.**

**Where A and B still disagree.** A refuses tracked unstaged edits outside S; B saves a separate worktree tree and compares after every attempt. B's supplied experiment identifies an assume-unchanged edit that A's real-index diff misses and the hook overwrites even without interruption. A's refusal therefore cannot establish its advertised protection. A dirty-outside gate also needlessly refuses ordinary unrelated work. B's snapshot is the better recovery primitive. However, B's per-key pin name must not be overwritten by a second attempt, and detection of outside changes must not be silently treated as permission to advance.

**Evidence.** The live protocol's Q0 already builds a private index from HEAD, adds worktree files and pins a tree against GC. The retry reference explicitly says these snapshots include `.dev/` evidence. A and B independently report the hook manager's stash/checkout behavior; B additionally reports orphaned hooks continuing after Git exits. The live worker contract keeps the command's own commit step off under unattended execution, so the attended commit need not adopt the worker heartbeat limit. I accept A/B's maximum tool timeout, but not a claim that a timeout proves child processes have stopped.

**Final numbered requirement text.**

1. **Two independent proofs.** A candidate tree proves what the commit may contain; a worktree tree preserves content outside S. Never substitute one for the other. The prepared attempt identifies deterministic sibling refs `refs/superclaude/implement/<slug>/boundary/<full-key>-a<n>` and `refs/superclaude/implement/<slug>/boundary-wt/<full-key>-a<n>`. Each attempt number is durable and monotonic. Pins are create-once: an existing different target refuses `pin-conflict`; retry never overwrites an earlier recovery pin. Prefix collisions cannot alias stored evidence.
2. **Capture before commit.** After mandatory visible add calls and immediately before the visible commit, build the worktree snapshot using the Q0 private-index method, starting from HEAD rather than copying real-index flags. Visibly pin it before any commit call. A failed/incomplete snapshot or pin appends `refused reason=snapshot-failed` and makes no commit. A prepared attempt lacking either required pin is incomplete proof and cannot be retried as though preparation succeeded. No hidden commit, ref write or user-index mutation is performed by the planner.
3. **Accurate guarantee.** Cover tracked worktree contents and nonignored additions represented by the snapshot, including real-index assume-unchanged/skip-worktree cases; preserve unrelated staged entries separately through `--only` semantics. This is not a backup of ignored files, empty directories, filesystem metadata or submodule interiors. The implementation must not claim raw-byte recovery for transformations it cannot reverse; an unsupported/non-lossless snapshot configuration refuses `snapshot-unsupported` before commit. Do not force-add ignored data. Same-worktree concurrent writers and arbitrary trusted hook/filter behavior remain outside the single-writer guarantee.
4. **Compare every attempt.** After any normally finished attempt, snapshot again before appending result/log evidence and compare all paths outside exact S with the before tree, including additions, deletions, modes and symlinks. For a resumed attempt, capture the comparison before the new run/evidence append, as INV-001 requires. A failed or incomplete comparison stops `E-COMMIT-REFUSED reason=outside-unverified` and retains the before pin; it is never interpreted as no changes. Compare the entire set; printing at most 20 entries is only a presentation limit, with total count and a truncation notice.
5. **Detected damage and records.** A normal result line records `outside-changed=<n>` when nonzero and names its attempt's worktree ref; detailed paths belong in the bounded attempt diagnostics. Keep the before pin after any result, `resolved` line or package archive while such a report is outstanding. Stop the invocation with `E-COMMIT-REFUSED reason=outside-changed`, even if the commit itself independently verifies as committed. Do not relabel that proved commit as pending or create another one. The next invocation reports the saved recovery pin before proceeding under its own flags; this damage report is not a second unsatisfied commit boundary. It never silently deletes the recovery pin.
6. **Recovery is explicit, not destructive automation.** Show the saved ref and selected-path restoration instructions, including `git restore --source=<saved-ref> -- <literal-paths>` only for applicable saved paths, with a prominent instruction to compare first because restoration overwrites newer edits. A newly created path absent from the before snapshot needs separate operator handling, not a blanket restore/delete. Report real-index content and known hook patch/lock locations as additional evidence, not the only backup. Never automatically restore, reset, stash, delete a lock or delete a saved patch. Preserve the pin until the owner explicitly directs its release after recovery or knowingly retaining current contents.
7. **Timeout, interruption and quiescence.** Use the tool maximum of 600000 ms for the commit call; do not disable hooks/signing to meet it. A reported timeout or signal leaves the prepared attempt open, writes no terminal classification and stops `E-RESUME-NEEDED reason=commit-interrupted`. Read-only observations may be shown as provisional, because a hook may still run. A later invocation must establish that the earlier Git/hook processes have stopped before final comparison, classification, restoration, retry or owner resolution. An index lock stops `reason=index-locked`; absence of a lock alone is not quiescence proof. If process cessation is not established, remain stopped; never kill an orphan or reclaim a lock automatically. Extend the transient-reason inventory and STOP consumers explicitly.
8. **Shared scope.** Apply snapshot/compare and interruption behavior to `/sc:git commit` and pointer commits too. For a pathless index commit, S is the exact pre-call index change set, frozen before the call; mandatory `.dev/tasks` staging must not widen it. This safety behavior grants no additional operation or permission and does not weaken any host denial. Hooks always run normally; no bypass, alternate hooks path, `commit-tree` or hidden wrapper commit.
9. **Acceptance tests.** Require isolated hook-manager emulations pinned to a named source revision, plus a real-framework fixture when available. Cover normal success, rejection, SIGTERM to the process group, SIGTERM to Git alone with an orphan hook, SIGKILL, timeout, stale locks, staged/unstaged/assume-unchanged/skip-worktree edits outside S, deletion and mode changes, snapshot failure and unsupported transformations. Prove outside edits remain recoverable from the saved evidence and unrelated index entries retain meaning. Test a second failed attempt cannot overwrite the first recovery pin, GC cannot prune it, a success with outside damage stops without duplicating the commit, and legacy resume's own new run line causes no false damage report.

### INV-027 — Uncertainty has no reachable exit

**Decision: ACCEPT B's amendments to A's resolution, with semantic record validation and safe missing-proof handling made explicit.**

**Where A and B still disagree.** I vote B on all six amendments: full 64-hex stored key, reply after the displayed STOP, choices at every unsettled state, today's unattended blocked behavior, the consequence of abandonment, and retaining outstanding worktree recovery pins. A's 12–64-character record pattern weakens C's display-only-prefix rule. A's resolution table omits choices in states its own tests need to escape. A and B agree that the owner responds in chat and the executor records the decision; no owner-written record is required.

**Evidence.** The live worker contract's owner-record rule expressly permits chat confirmation recorded by the agent and forbids executor-invented approval. The live QA Halt table requires a scoped, informed current-conversation confirmation and rejects generic continuation and other agents' messages. Neither currently defines commit-boundary resolution. C's Round 2 `explicit owner-resolved abandonment` therefore was an incomplete interface, not an implemented escape hatch.

**Final numbered requirement text.**

1. **Resolution record.** The executor appends one validated line to the same `commits.md`, never to the task ledger:
   ```text
   T<ids>: commit resolved key=<64-hex> as=abandoned at=<YYYY-MM-DD> quote="<owner words>"
   T<ids>: commit resolved key=<64-hex> as=adopted head=<40-hex> basis=<candidate|accepted> differs=<n> at=<YYYY-MM-DD> quote="<owner words>"
   ```
   These are two distinct semantic forms: `head`, `basis` and `differs` are required for adoption and forbidden for abandonment. The decoded quote is 1–200 Unicode code points, escapes quotes/backslashes, contains no raw newline/control character and is not silently truncated. If the reply cannot be represented safely, request a short scoped reply rather than inventing a quote. Store the full key; prefixes are never serialized as identity.
2. **Information before choice.** Every STOP for every valid unsettled boundary displays its full key, a unique short display label, task members, state, prepared parent or original Q0 parent when known, current HEAD, exact intended S, and a bounded changed-path/count summary. It always offers `abandon`; it offers `adopt` only when requirement 4 holds. A missing comparison pin is displayed as unavailable, never as zero differences. Missing proof does not prevent abandoning a known boundary whose identity/member binding is intact.
3. **Who may answer.** Accept only the person's own reply after that disclosure in the same conversation. A unique displayed prefix may select a key; a reply without a key is sufficient only when exactly one key was displayed and its choice is unambiguous. Reject earlier prompt text, an inline source, plan/brief fields, generic `continue`, other agents' messages and a coordinator's answer. A coordinator session may record its own user's qualifying chat confirmation under the existing owner-record rule; an agent-to-agent relay is not that confirmation. Under unattended execution report the gate blocked, never ask or apply an automated default. Persisted grant/resolution data is evidence, not proof of human provenance.
4. **Read-only resolution check.** `resolve-check` resolves the displayed key to a full known unsettled identity and validates sidecar state. Return `unknown-boundary`, `ambiguous-key` or `already-settled` without an append on failure. Abandon needs no ancestry or candidate pin. Adopt requires known parent, HEAD different from parent, ancestry exit 0, proved quiescence and an available disclosed comparison tree. Use the frozen full candidate when prepared, otherwise the accepted tree for the due boundary; record `basis=` accordingly. Count `differs` over S by object identity, mode and absence, not only blob text. Missing ancestry/object evidence refuses `adopt-not-descendant`/`adopt-unverifiable`; exit 128 is never success. These failures still leave `abandon` available. Re-read HEAD and basis immediately before recording; if disclosure changed, redisplay and obtain a new reply.
5. **Meaning and limits.** `abandoned` settles the key permanently without making a commit or changing any file; later automatic attempts for the key are prohibited. State that remaining uncommitted product edits can cause a later overlapping task to refuse `foreign-change` until the person separately resolves them. `adopted` records the owner's acceptance of the displayed history as settlement, even when `differs` is nonzero; it is **not** a verified automatic commit, a changed QA verdict, retroactive commit authorization or a waiver of plan integrity, FINAL, archive or permission checks. Neither answer authorizes restoration, history repair or publication.
6. **Idempotent continuation and cleanup.** After the durable resolution append, a repeated reply or resumed reconciliation recognizes settlement and makes no commit or duplicate resolution line. Cleanup occurs only after the append and can resume after a crash; failure to delete a pin does not undo settlement. Release ordinary boundary proof with visible ref deletions, but keep every attempt pin protecting an outstanding outside-S recovery report, including through archive. Rerun reconciliation, then continue only if all other gates pass under the invocation's own flags. No boundary resolution overrides corrupt sidecar/ledger recovery, live processes, a stale lock or `E-PLAN-CHANGED`.
7. **Acceptance tests.** Test every unsettled state in flagged and unflagged runs always offers abandonment. Test a person's post-crash commit, hook-rewrite-committed and out-of-protocol due state; adopt when justified and then resume/archive without duplicate commits. Reject early or agent-origin replies, ambiguous prefixes, short stored keys, adoption fields on abandonment, missing adoption fields, changed HEAD after disclosure, unrelated history and unavailable comparison proof. Abandon a known boundary whose candidate pin is missing. Crash after the resolution append but before cleanup; resume twice and prove exactly one settlement. Keep prior outside-S recovery pins after both abandonment and adoption.

#### Ruling on the other 19 findings

Each finding has exactly one ruling below. ACCEPT-FIX rows are the final one-line requirements; tests are part of the behavior they specify, not claims of executed verification.

| Finding | Ruling | Final requirement or accepted residual; position on A/B |
|---|---|---|
| INV-002 | ACCEPT-FIX | Capture the full symbolic Q0 branch beside `q0-head` before each new start, bind it in run/prepared state and refuse `branch-changed` against that original value; missing historical branch proof refuses `branch-unproven`, not B's completion-run fallback; vote B over A's latest-run comparison. |
| INV-003 | ACCEPT-FIX | Before first eligible completion, pin the compliant verdict's reviewed tree or the current scoped-Ruling snapshot, bound to its start occurrence; missing proof refuses `no-accepted-tree`/`no-snapshot`; vote B over A's compliant-completion worktree snapshot. |
| INV-004 | ACCEPT-FIX | Retry compares accepted/disclosed product paths only, rebuilds and freezes package evidence for a new attempt, and reconciles before ordinary run-evidence writes but after managed identity/PLAN validation; agree A/B, with B's plan-check order. |
| INV-007 | ACCEPT-FIX | Include deletions and both rename endpoints in `files=`; stage worktree-absent paths present in index/HEAD as deletions, skip only paths absent from all three and report them; agree corrected A/B, replacing C's unnecessarily strict original transient-only skip. |
| INV-008 | ACCEPT-FIX | Filter paths equal to or descending from a mode-160000 path in HEAD, index or retained Q0 proof before staging, reporting `skipped why=gitlink`; agree A/B's prefix correction and retain the Q0 source too. |
| INV-009 | ACCEPT-FIX | Distinguish missing target objects as `target-not-local`, never divergence; a disclosed selected update may fetch only under the approved-URL grant, clean/no-orphan conditions and exact-target revalidation; agree A/B, replacing unconditional local fast-forward proof. |
| INV-010 | ACCEPT-FIX | Uninitialized update requires the person to repeat the disclosed `.gitmodules` destination with `--url`, revalidated before mutation; initialized URL mismatch refuses `remote-mismatch` with a person-run sync hint; agree A/B, never print credential-bearing URLs. |
| INV-011 | ACCEPT-RISK | Agree A/B: an already-installed old copy cannot be repaired by this specification; it may ignore the flag, while new copies print the on/off state and commit count and refuse moved-on recovery rather than claiming the old copy implemented commits. |
| INV-012 | ACCEPT-FIX | Pass exact NUL-delimited literal paths through an external pathspec file for add/commit and display the complete intended set separately; agree A/B, but a host denial remains authoritative and this transport is not permission to hide a forbidden target. |
| INV-014 | ACCEPT-FIX | Derive the original batch from overlapping windows, retain all member start occurrences in its key, require all first-complete anchors eligible, and settle an all-complete mixed batch as `skipped reason=mixed-authorization` without a partial commit; agree A/B. |
| INV-015 | ACCEPT-FIX | Validate the decoded entire header at no more than 72 Unicode code points without normalization, using the same word-boundary truncation and length rule for drafting and checking; agree A/B, including B's no-normalization clarification. |
| INV-018 | ACCEPT-RISK | A/B fix product-directory widening by refusing directory entries and expanding the current package to literal files, but their package exception still cannot identify a person's addition; accept that explicit sole-owner-package residual, not their claim that this finding is fully fixed. |
| INV-020 | ACCEPT-FIX | Classify evidence-only rewrites separately and retry only in a new authorized attempt with fresh evidence; product or pinned plan/source changes retain stricter gates, oversized evidence names the file and stops without deletion/bypass; agree A/B, with no hook-config change bundled in. |
| INV-022 | ACCEPT-FIX | Settle before advance and forbid any late preparation/retry while a task remains open; an out-of-protocol later start stops for explicit resolution rather than moving HEAD under it; agree A/B and test unflagged-resume refusal. |
| INV-023 | ACCEPT-FIX | Add a commit-state check at the existing managed archive gate that refuses `E-ARCHIVE-BLOCKED reason=unsettled-boundary` before movement, including due/refused/uncertain states; agree A/B without adding commit record kinds to the task ledger. |
| INV-024 | ACCEPT-FIX | Pathful `/sc:git commit` stages named paths plus mandatory evidence but commits only named paths; pathless commit freezes/uses the preexisting index and stages `.dev/tasks` afterwards even on refusal, warning about unsettled sidecars; vote B over A's unspecified staging order. |
| INV-025 | ACCEPT-FIX | Prepare must match product paths to the verdict's reviewed/accepted tree, refuse `changed-after-review` after Q6 rewrites, and require restoration or actual renewed review/Ruling before retry; vote B over A's completion-time pin, preserving C's after-disclosure review rule. |
| INV-029 | ACCEPT-RISK | Agree A/B on no new scanner or hook installation in scope, but reject “no new exposure”: automatic evidence commits can enter unscanned history; disclose missing enforcement and never promise secret safety or bypass a known-secret refusal. |
| INV-030 | ACCEPT-FIX | Accept pointer eligibility only from remote-tracking refs belonging to a module remote whose URL matches `.gitmodules`, otherwise refuse `submodule-unpublished reason=no-gitmodules-remote`; agree A/B while labeling containment and fetch-file time as local observations, not availability proof. |

For INV-018, the accepted risk does not relax path containment, plan/source hashes, exact frozen-candidate verification, mandatory evidence staging or the ban on other packages entering implement commits. It admits that an agent cannot distinguish another person's package-local file from intended evidence using the proposed metadata. Known concurrent ownership conflicts still stop. For INV-029, absence of an automatic push reduces outward effect but does not erase the local-history exposure.

#### Final concessions

1. **C's earlier designs were too heavy in the wrong places.** Keep the single sidecar, no new lock/request-envelope service, visible writes, skill-local distribution and the agreed bounded interface. C's information requirements survive without its original containers.
2. **A supplies the missing progress rule.** Settle-before-advance is necessary even on unflagged resumes and before archive. C's earlier “uncertainty requires resolution” was not a complete recovery contract.
3. **B corrects the eligibility semantics.** First completion, original batch identity and moved-on refusal replace both pin-existence inference and A's latest-complete rule. Original branch identity must nevertheless be captured, not reconstructed from a later run.
4. **Withdraw C's 120-second mutation deadline.** A/B's 600000 ms attended call better accommodates hook environment installation. Recovery proof and confirmed process cessation, not timeout length, provide safety.
5. **Prefer recovery evidence to the returned dirty gate.** A's hook research establishes a real hazard; B's broader snapshot closes more of it. C insists on per-attempt immutable pins and honest snapshot coverage, rather than “every byte” claims.
6. **B's resolution amendments are accepted.** The owner can answer in chat after the explained choice; full keys and semantic checks make that auditable without pretending a sidecar verifies personhood.
7. **Keep C's remaining integrity objections.** Review must follow disclosure for changed product contents; missing proof never degrades silently; attempt failure is not boundary satisfaction; local ref containment is not fresh remote publication proof.
8. **Explicit residuals replace impossible guarantees.** Product edits made by another writer during the review window, package-local additions under sole-owner assumptions, uninstalled secret hooks, ignored data and arbitrary trusted hooks are not solved by wording. No extra scanner, global lock, cleanup engine or worker-authority expansion is added.
9. **Verification limit.** This final argument is a read-only requirements assessment. The listed crash, real-framework, filter, signal, archive and idempotency tests must be implemented and observed before claiming the proposed mechanisms work.

#### Per-point votes

| Point | Winner | Confidence | Reason |
|---|---|---|---|
| S-001 | HYBRID | 88 | C's compact contracts with A's navigation; retain decisive evidence without repeating the full investigation. |
| S-002 | B | 94 | Explicit alias resolution avoids source-package and task-package confusion. |
| S-003 | HYBRID | 94 | A's baseline facts plus B's falsifiable root causes explain preservation obligations. |
| S-004 | C | 82 | Renumber contiguously once after merging for clear final traceability. |
| S-005 | HYBRID | 98 | A's test matrix, B's consumer inventory and C's fault injection; add segments, orphan hooks and resolution tests. |
| S-006 | HYBRID | 94 | Map acceptance criteria to executable observations and behavioral tests, not wording counts alone. |
| S-007 | B | 90 | Root causes and residuals separate mitigation from proof. |
| S-008 | HYBRID | 99 | Mirrored planner, shared constants, versioned results and visible mutations; snapshots do not become hidden commits. |
| S-009 | HYBRID | 91 | A's registry and shared safety reference with B's lazy read-path loading. |
| S-010 | B | 96 | Dedicated lazy commit-step reference makes implement integration concrete. |
| S-011 | HYBRID | 99 | Sidecar segments, prepared attempts, frozen candidates and informed resolutions; immutable recovery pins survive settlement when needed. |
| S-012 | A | 91 | Explicit merge-removal and package-scope decisions prevent scope drift. |
| S-013 | HYBRID | 98 | Integrity, honest trust boundaries, parity/version rules and bounded execution; no fabricated enforcement guarantees. |
| C-001 | A | 90 | Preserve guarded branch management; exclude publication and merge; add bounded submodule operations. |
| C-002 | A | 92 | Explicit message or smart drafting closes the message-source hole without an ambiguous interactive mode. |
| C-003 | HYBRID | 96 | B's person-origin refusal plus C's repository/path/target scope; no unauthorized replayable mutation plan. |
| C-004 | HYBRID | 96 | Person provenance checked once per run; static insertion checks supplement rather than replace it. |
| C-005 | HYBRID | 99 | Named commit positions, managed pin validation, pre-append recovery observation and settle-before-advance protect all dispatch exits. |
| C-006 | HYBRID | 95 | Before-ledger commit preflight, durable original identity and explicit existing inline-intake effects. |
| C-007 | A | 95 | Separate precondition and boundary stops; extend transient interruption reasons and all closed consumers explicitly. |
| C-008 | HYBRID | 99 | Per-product Q0 checks, accepted-review equality and outside-path snapshots protect different failure surfaces. |
| C-009 | HYBRID | 99 | Exact frozen-candidate verification plus plan/source checks and independent outside-path comparison. |
| C-010 | HYBRID | 99 | Full stable key, prepared attempts, first-complete segments, pinned candidates, strict recovery and defined owner settlement. |
| C-011 | B | 97 | Retain required proof through unresolved states; cleanup only after settlement or durable proof transfer. |
| C-012 | HYBRID | 97 | A's message schema, B's plan trailer, C's full identity and session attribution; count Unicode code points. |
| C-013 | B | 97 | External temporary messages avoid accidental evidence commits. |
| C-014 | HYBRID | 97 | Independent nullable facts plus explicitly derived action-state precedence. |
| C-015 | HYBRID | 94 | Clean selected gitlinks, exact target binding and containment only through the declared module remote. |
| C-016 | C | 98 | Cleanup remains routing, accurately distinguishing archive writes from inspection. |
| C-017 | HYBRID | 90 | Conservative floor, additive local default and verified repository instructions, with explicit unknown-policy limitations. |
| C-018 | HYBRID | 96 | Report checked scope, before/after effects and bounded diagnostics; restoration advice never authorizes destructive repair. |
| C-019 | HYBRID | 99 | Routing, fixtures, write classifications, cleanup, transient stops, Ruling text and archive gates change together. |
| C-020 | HYBRID | 98 | Mirrored skill-local planner with missing/version-mismatch refusal; no implicit installation or source-tree escape. |
| C-021 | C | 99 | Literal path safety remains essential; pathspec files solve transport, not ledger encoding or authority. |
| X-001 | HYBRID | 97 | Parsed flag, person provenance, bounded run segments, revocation and fresh-session limits. |
| X-002 | HYBRID | 100 | A/C remove merge; the seed expressly forbids it. |
| X-003 | A | 92 | Drop interactive and the forbidden merge example; no verified compatibility requirement justifies them. |
| X-004 | HYBRID | 99 | Sidecar preserves task-ledger grammar; archive gate checks unsettled boundaries without adding task record kinds. |
| X-005 | A | 96 | Always stage mandatory evidence; implement commits only its own package and authorized product paths. |
| X-006 | HYBRID | 99 | No retroactive unflagged-task commits; first-complete segment anchors and moved-on refusal make eligibility durable. |
| X-007 | C | 99 | Changed product contents require actual review after disclosure, not a flag typed before the diff. |
| X-008 | HYBRID | 100 | Visible mutations preserve host enforcement; planner preparation and verification do not hide writes. |
| X-009 | A | 90 | Preserve bounded branch create/switch with clean-tree, no-force and protected-name guards. |
| X-010 | C | 95 | Bare invocation is read-only status; unknown operations stop. |
| X-011 | A | 96 | Follow the developer-guide vocabulary required by the seed; broader practice drift stays separate. |
| X-012 | HYBRID | 95 | Top-level-only mutation, explicit unsupported nesting and selected-path containment. |
| X-013 | HYBRID | 96 | Preserve commits, distinguish missing targets from divergence and revalidate exact recorded-target updates. |
| X-014 | HYBRID | 94 | Conservative declared-remote containment gate with honest stale-ref and availability limitations. |
| X-015 | HYBRID | 97 | Disclose clone/fetch effects and bind approved destination; never silently substitute remotes. |
| X-016 | A | 98 | Preflight precedes ledger creation; qualify absolute no-write claims for existing inline intake. |
| X-017 | HYBRID | 98 | Private-index object creation is disclosed; actual ref/index/history mutations remain visible. |
| X-018 | A | 99 | Validate total decoded header length directly, consistently counting Unicode code points. |
| X-019 | B | 98 | Distinct source-package and task-package aliases prevent wrong destinations. |
| X-020 | B | 98 | Configured hooks are not installed enforcement; independent message validation and deliberate fixtures remain required. |
| X-021 | NONE | 99 | Tracking does not establish staging authority; preserve the explicit runtime-directory policy. |
| A-001 | NONE | 99 | Correct all originals: preserve tracked deletions; skip only paths absent from worktree, index and HEAD. |
| A-002 | HYBRID | 95 | Current-file FINAL review remains required; preserve legacy and managed reviewer-input regressions. |
| A-003 | HYBRID | 99 | Run-scoped grant, bounded provenance, ledger offsets, original branch and revocation; stored state cannot manufacture authority. |
| A-004 | C | 98 | Local refs and fetch-file timestamps do not establish current remote availability. |
| A-005 | HYBRID | 97 | Round-three snapshot and comparison address the original gap; per-attempt retention and orphan-hook tests remain mandatory. |
| A-006 | HYBRID | 94 | No exact K3 wording pin was identified; worker-contract behavioral regressions still apply. |

## Scoring Matrix

Final-round winners per diff point (majority label of the three advocates' votes; confidence is the mean of the majority voters' confidence; HYBRID means a combination whose elements are named in the evidence summary and in the advocates' Round 3 text).

| Diff Point | Level | Winner | Confidence | Votes (A/B/C advocates) | Evidence Summary |
|------------|-------|--------|------------|-------------------------|------------------|
| S-001 | L1 | A | 55% | A/A/HYBRID | Balanced density with verified citations; B repeats evidence, C omits test-pinned facts. |
| S-002 | L1 | B | 75% | B/B/B | Explicit alias resolution avoids source-package and task-package confusion. |
| S-003 | L1 | HYBRID | 71% | HYBRID/HYBRID/HYBRID | A's baseline facts plus B's falsifiable root causes explain preservation obligations. |
| S-004 | L1 | A | 50% | A/A/C | Gapped blocks absorb inserts without renumbering; low stakes, the merge renumbers anyway. |
| S-005 | L1 | HYBRID | 78% | HYBRID/HYBRID/HYBRID | A's test matrix, B's consumer inventory and C's fault injection; add segments, orphan hooks and resolution tests. |
| S-006 | L1 | HYBRID | 77% | B/HYBRID/HYBRID | Map acceptance criteria to executable observations and behavioral tests, not wording counts alone. |
| S-007 | L1 | B | 67% | B/B/B | Root causes and residuals separate mitigation from proof. |
| S-008 | L2 | HYBRID | 83% | HYBRID/HYBRID/HYBRID | Mirrored planner, shared constants, versioned results and visible mutations; snapshots do not become hidden commits. |
| S-009 | L2 | HYBRID | 76% | A/HYBRID/HYBRID | A's registry and shared safety reference with B's lazy read-path loading. |
| S-010 | L2 | B | 72% | B/B/B | Dedicated lazy commit-step reference makes implement integration concrete. |
| S-011 | L3 | HYBRID | 85% | HYBRID/HYBRID/HYBRID | Sidecar segments, prepared attempts, frozen candidates and informed resolutions; immutable recovery pins survive settlement when needed. |
| S-012 | L1 | A | 67% | A/A/A | Explicit merge-removal and package-scope decisions prevent scope drift. |
| S-013 | L1 | HYBRID | 69% | HYBRID/HYBRID/HYBRID | Integrity, honest trust boundaries, parity/version rules and bounded execution; no fabricated enforcement guarantees. |
| C-001 | L2 | A | 70% | A/A/A | Preserve guarded branch management; exclude publication and merge; add bounded submodule operations. |
| C-002 | L2 | A | 67% | A/A/A | Explicit message or smart drafting closes the message-source hole without an ambiguous interactive mode. |
| C-003 | L3 | B | 60% | B/B/HYBRID | Prefix rule plus a refusal with no replayable argv; A's dry run handed argv to unauthorized callers. |
| C-004 | L3 | HYBRID | 77% | HYBRID/HYBRID/HYBRID | Person provenance checked once per run; static insertion checks supplement rather than replace it. |
| C-005 | L3 | HYBRID | 80% | HYBRID/HYBRID/HYBRID | Named commit positions, managed pin validation, pre-append recovery observation and settle-before-advance protect all dispatch exits. |
| C-006 | L3 | HYBRID | 75% | HYBRID/HYBRID/HYBRID | Before-ledger commit preflight, durable original identity and explicit existing inline-intake effects. |
| C-007 | L2 | A | 72% | A/A/A | Separate precondition and boundary stops; extend transient interruption reasons and all closed consumers explicitly. |
| C-008 | L3 | HYBRID | 83% | HYBRID/HYBRID/HYBRID | Per-product Q0 checks, accepted-review equality and outside-path snapshots protect different failure surfaces. |
| C-009 | L3 | HYBRID | 85% | HYBRID/HYBRID/HYBRID | Exact frozen-candidate verification plus plan/source checks and independent outside-path comparison. |
| C-010 | L3 | HYBRID | 88% | HYBRID/HYBRID/HYBRID | Full stable key, prepared attempts, first-complete segments, pinned candidates, strict recovery and defined owner settlement. |
| C-011 | L3 | B | 79% | B/B/B | Retain required proof through unresolved states; cleanup only after settlement or durable proof transfer. |
| C-012 | L1 | HYBRID | 72% | HYBRID/HYBRID/HYBRID | A's message schema, B's plan trailer, C's full identity and session attribution; count Unicode code points. |
| C-013 | L1 | B | 72% | B/B/B | External temporary messages avoid accidental evidence commits. |
| C-014 | L2 | HYBRID | 76% | HYBRID/HYBRID/HYBRID | Independent nullable facts plus explicitly derived action-state precedence. |
| C-015 | L3 | HYBRID | 75% | HYBRID/HYBRID/HYBRID | Clean selected gitlinks, exact target binding and containment only through the declared module remote. |
| C-016 | L2 | C | 73% | C/C/C | Cleanup remains routing, accurately distinguishing archive writes from inspection. |
| C-017 | L3 | HYBRID | 78% | B/HYBRID/HYBRID | Conservative floor, additive local default and verified repository instructions, with explicit unknown-policy limitations. |
| C-018 | L1 | HYBRID | 72% | HYBRID/HYBRID/HYBRID | Report checked scope, before/after effects and bounded diagnostics; restoration advice never authorizes destructive repair. |
| C-019 | L2 | HYBRID | 80% | HYBRID/HYBRID/HYBRID | Routing, fixtures, write classifications, cleanup, transient stops, Ruling text and archive gates change together. |
| C-020 | L2 | B | 70% | B/B/HYBRID | Plugin build copies only the plugin tree; a mirrored script ships everywhere with `helper-missing`. |
| C-021 | L3 | C | 90% | C/C/C | Literal path safety remains essential; pathspec files solve transport, not ledger encoding or authority. |
| X-001 | L3 | HYBRID | 86% | HYBRID/HYBRID/HYBRID | Parsed flag, person provenance, bounded run segments, revocation and fresh-session limits. |
| X-002 | L2 | A | 90% | A/A/HYBRID | The seed forbids merge in `/sc:git`; A removes it and rewrites the routing row. |
| X-003 | L2 | A | 81% | A/A/A | Drop interactive and the forbidden merge example; no verified compatibility requirement justifies them. |
| X-004 | L3 | B | 72% | B/B/HYBRID | Sidecar leaves the resume regex and archive parser untouched; the archive digest covers only plan, source, `files=` paths. |
| X-005 | L3 | A | 77% | A/A/A | Always stage mandatory evidence; implement commits only its own package and authorized product paths. |
| X-006 | L3 | B | 75% | B/B/HYBRID | No retroactive commits; `ledger-lines` segments make "completed in a flagged run" computable after a crash. |
| X-007 | L3 | HYBRID | 68% | HYBRID/HYBRID/C | Never automatic; the refusal pins and prints the hook-rewritten tree; a later flagged run commits only that disclosed tree. |
| X-008 | L3 | HYBRID | 87% | HYBRID/HYBRID/HYBRID | Visible mutations preserve host enforcement; planner preparation and verification do not hide writes. |
| X-009 | L2 | A | 70% | A/A/A | Preserve bounded branch create/switch with clean-tree, no-force and protected-name guards. |
| X-010 | L2 | C | 72% | C/C/C | Bare invocation is read-only status; unknown operations stop. |
| X-011 | L1 | A | 69% | A/A/A | Follow the developer-guide vocabulary required by the seed; broader practice drift stays separate. |
| X-012 | L3 | A | 65% | A/A/HYBRID | One non-nested submodule; report nested as not inspected; never recursive. |
| X-013 | L3 | HYBRID | 77% | HYBRID/HYBRID/HYBRID | Preserve commits, distinguish missing targets from divergence and revalidate exact recorded-target updates. |
| X-014 | L3 | B | 62% | B/B/HYBRID | No downstream publication gate; refusal errs safe; containment only against the `.gitmodules` remote; last-fetch time printed. |
| X-015 | L3 | HYBRID | 76% | HYBRID/HYBRID/HYBRID | Disclose clone/fetch effects and bind approved destination; never silently substitute remotes. |
| X-016 | L3 | A | 89% | A/A/A | Preflight precedes ledger creation; qualify absolute no-write claims for existing inline intake. |
| X-017 | L3 | HYBRID | 76% | HYBRID/HYBRID/HYBRID | Private-index object creation is disclosed; actual ref/index/history mutations remain visible. |
| X-018 | L1 | A | 81% | A/A/A | Validate total decoded header length directly, consistently counting Unicode code points. |
| X-019 | L1 | B | 86% | B/B/B | Distinct source-package and task-package aliases prevent wrong destinations. |
| X-020 | L3 | B | 89% | B/B/B | Configured hooks are not installed enforcement; independent message validation and deliberate fixtures remain required. |
| X-021 | L3 | NONE | 85% | NONE/NONE/NONE | Tracking does not establish staging authority; preserve the explicit runtime-directory policy. |
| A-001 | L3 | NONE | 86% | NONE/NONE/NONE | Correct all originals: preserve tracked deletions; skip only paths absent from worktree, index and HEAD. |
| A-002 | L3 | HYBRID | 73% | HYBRID/HYBRID/HYBRID | Current-file FINAL review remains required; preserve legacy and managed reviewer-input regressions. |
| A-003 | L3 | HYBRID | 85% | HYBRID/HYBRID/HYBRID | Run-scoped grant, bounded provenance, ledger offsets, original branch and revocation; stored state cannot manufacture authority. |
| A-004 | L3 | HYBRID | 60% | HYBRID/HYBRID/C | Never claim freshness: B's refusal errs safe; print last-fetch time (C's honesty); no fetch. |
| A-005 | L3 | NONE | 85% | NONE/NONE/HYBRID | No variant handled it; verified that pre-commit stashes every path outside S under `--only`; fixed by the `unstaged-outside` refusal. |
| A-006 | L1 | HYBRID | 73% | HYBRID/HYBRID/HYBRID | No exact K3 wording pin was identified; worker-contract behavioral regressions still apply. |

Winner tally: A=14, B=12, C=3, HYBRID=29, NONE=3

## Convergence Assessment

- Points resolved: 61 of 61
- Alignment: 100%
- Threshold: 75%
- Status: CONVERGED (taxonomy levels all covered; invariant gate clear after Round 3: HIGH + UNADDRESSED = 0)
- Unresolved points: none
- Warnings: 16 MEDIUM and 3 LOW invariant findings were ruled ACCEPT-FIX (16) or ACCEPT-RISK (3) in Round 3; they do not block convergence
