# Round 1 — Advocate for Variant A (architect; maintainability and extension scaffolding)

## Position summary

Variant A gives the best maintainable skeleton for this work: one place for each rule (`rules.py` with a parity test), one place to add an operation (a registry plus a checklist and a test), a helper that never writes, and a scope that follows the seed brief exactly (no merge, routing row and fixtures updated in the same change). Its state handling is weaker than B's in three specific places (crash recovery, hook-rewrite detection, per-path protection of the person's edits). B's mechanisms for those fit into A's skeleton with almost no change, so the best merged result is A's structure with those B mechanisms added.

## Steelman

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

## Strengths claimed

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

## Weaknesses identified in the others

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

## Concessions

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

## Shared assumptions

- **A-001: REJECT.** A path created and deleted inside a task, or mistyped, is in neither the index nor HEAD, so `git add -- <paths>` fails for the whole call. The planner must filter such paths into `skipped`.
- **A-002: ACCEPT.** It holds today. The managed FINAL reads "the current contents of every delivery file" (`refs/qa.md:311`, verified), so committing first hides nothing.
- **A-003: QUALIFY.** It holds only if the spec says the invocation line, checked once in Wave 0, is the authority for the whole invocation, Ruling turns included, and that every resume needs the flag again. No variant says this yet.
- **A-004: QUALIFY.** Remote-tracking refs can be stale without a fetch. That is acceptable only when the result is a warning or "unknown" and is never used to block a commit or to declare it safe.
- **A-005: QUALIFY.** No variant has verified it. It needs a test that runs the pinned pre-commit framework, with a hook that rewrites files, under `git commit --only` with unstaged edits present.
- **A-006: ACCEPT.** Verified: no file under `tests/` matches "wait for issue #326" or "K3", so rewriting `WORKER-CONTRACT.md:42` breaks no test.

## Per-point votes

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
