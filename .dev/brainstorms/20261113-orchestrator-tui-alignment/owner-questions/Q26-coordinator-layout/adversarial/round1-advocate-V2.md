# Round 1 advocate statement: variant 2 (proposal B)

Advocate persona: backend (data integrity, concurrency, fault tolerance). Depth: quick. Line numbers below refer to `variant-1-original.md` (V1), `variant-2-original.md` (V2), `variant-3-original.md` (V3) and `diff-analysis.md` (DA) as read on 2026-11-14.

Facts I checked read-only on 2026-11-14:
- `git worktree list` shows every Orca worktree on this host under `/home/coder/workspaces/worktrees/IronClaude/<name>`, nearly all on `ironbelly/<name>` branches (one, `issue-409-mvp`, is on `409-Phase2`). So the observed prefix is not universal.
- `git branch -r --list 'origin/*coordinators*'` prints nothing: no coordinators branch of any shape exists yet.
- `ls .dev/coordinators` fails: the folder does not exist.
- Everything else about Orca (base branch support, prefix rule) stays UNVERIFIED, as all three variants say.

## Position summary

Variant 2 is the only layout that carries both axes the owner named ("Coordinators per developer, per epic or per release as sub-dir's under .dev/coordinator") at once, and the only one that stops double dispatch with a git-enforced lock keyed on the thing that actually collides in practice: the issue, the PR or the item (V2 lines 19 to 22, 52, 59). Variant 1 is safer inside one scope but forbids the case the owner described, several developers on one epic (V1 line 104). Variant 3 is the cleanest for isolation but leaves double dispatch advisory and racy (V3 lines 62, 96). Variant 2 keeps V1's "git conflict is the lock, counted only once pushed" rule and V3's "one writer per developer folder" rule, and adds the project-wide claim key. Its real weaknesses (single append-only files, a grant id that may repeat across one developer's coordinators, a lock that depends on conflict discipline) are fixable inside the design; I list them in Concessions.

## Steelman of variant 1

Variant 1's strongest case is integrity by construction. Inside a scope there is exactly one writer at a time (V1 line 66), every ledger and grant entry is a new file that is never edited (V1 lines 24 to 31, 67), so even a careless writer cannot drop another entry by rewriting a file (DA U-002), and the only possible git conflict is on one known path, `holder.md`, where the conflict is the intended signal (V1 line 70). Double dispatch inside a scope cannot happen at all, not merely "is detected" (V1 lines 69, 103). The ledger belongs to the epic, not the person, so a developer change does not fork the history: one ledger per epic survives a handover (DA U-001, V1 line 68). Entry names have an explicit same-second rule (`-2`, `-3`, V1 line 60). For a backend reviewer this is the model with the fewest moving parts that can corrupt state.

## Steelman of variant 3

Variant 3's strongest case is that the safest shared state is no shared state. No developer ever writes a file or branch another developer writes (V3 lines 3, 60), so a bad rebase, a careless rewrite or even a force-push by one developer can damage only that developer's own branch; the blast radius of every failure is one person. Permissions are the narrowest of the three: a push grant for one's own branch only (V3 line 71, DA C-008). It matches the developer-prefixed branch habit already on the remote (V3 line 9, DA U-006), it allows private and `adhoc` coordinators (V3 lines 46, 69, DA U-005), and because the folders are disjoint, a later combined view is a clean merge of all developer branches (V3 line 63). It also has no lock to get wrong, so A-003 (no force-push) cannot void a guard it does not have.

## Strengths claimed

1. **Matches the owner's requirement in full.** The owner wants one branch per project, sub-folders per developer, per epic or per release, and "multiple developers with multiple coordinators ... on the same project". V2 has one `coordinators` branch (V2 line 49), scope folders of kind `epic` or `release` (V2 line 46), and a developer level under each scope (V2 lines 23 to 33), so "two or more developers can coordinate one epic at once" (V2 line 102). V1 gives up the multi-developer epic (V1 line 104) and V3 gives up the single branch (V3 line 97).
2. **The lock is keyed on what collides.** Claims are project-wide, keyed `issue-<N>`, `pr-<N>`, `item-<scope>-<item-id>` (V2 lines 19 to 22, 52), and a coordinator claims "each issue or PR the item writes to" (V2 line 67). That catches an epic coordinator and a release coordinator both writing to one PR, which V1's per-scope lease cannot see (DA U-003, rated High).
3. **The lock is enforced by git and counted only once pushed.** "The path is the lock; a claim counts only once pushed" (V2 line 59) and "No pushed claim, no dispatch" (V2 line 67). This is the same guarantee V1 uses for its lease (V1 line 73), not V3's advisory scan with a known race window (V3 line 62).
4. **Single writer per folder.** Only the coordinator whose id is the folder writes in it, and its ledger, grants and results are append-only with corrections as new rows (V2 line 65). Developer handles are unique on GitHub, so two developers never share a folder (V2 line 58).
5. **The shared conflict surface is tiny and every conflict means something.** Shared files are create-once (V2 line 66); the only possible conflicts are on `claims/*.md` or `scope.md`, "and each one is the intended 'someone got there first' signal" (V2 line 69).
6. **A clear release versus epic rule.** A release coordinator claims only release-only items such as the changelog or tag, and reads epic items it gates (V2 line 68, DA U-004). V1 leaves release-only items unresolved (V1 line 114); V3 has no rule (DA C-004).
7. **Archive never breaks a citation.** Archiving appends a state row and the folder stays (V2 line 87), so no path cited in a ledger, grant or worker contract goes stale. V1 moves the folder and admits it "rewrites every path others may cite" (V1 line 90).
8. **Both views are cheap.** "Everything on epic X" is one folder; "everything developer Y runs" is one glob `*/<dev>/` (V2 line 76), readable with `git show` or `git ls-tree` and no checkout (V2 line 74). V1 needs a scan of every `holder.md` for the developer view (V1 line 105); V3 needs a scan of every branch for the epic view (V3 lines 70, 98).
9. **Stale reads are bounded.** Each ledger row records the `origin/coordinators` revision read, and a coordinator re-fetches before every claim (V2 line 70).
10. **Ownership transfer is recorded, not inferred.** Closing a coordinator releases every claim or hands it over by a ledger row naming the new coordinator (V2 line 86); only the coordinator named in a claim, or the project owner, may delete it (V2 line 66).

## Weaknesses in other variants

1. **V1 forbids concurrent developers on one epic.** "Two developers cannot work one epic at the same time; a big epic either waits on handovers or is split into smaller epics" (V1 line 104). That conflicts directly with the owner's "multiple developers with multiple coordinators will be working on the same project" when the work is one epic, and splitting an epic to fit a lock model distorts the program's own structure.
2. **V1's guard has a blind spot across scopes.** V1 prevents double dispatch only by "an item belongs to exactly one scope" (V1 line 69). An issue or PR is not an item; two epics, or an epic and a release, that both write to one PR are not stopped (DA U-003).
3. **V1's absent holder blocks the whole scope.** "A holder who disappears blocks the scope until the project owner forces a takeover" (V1 line 106), and who the project owner is stays unresolved (V1 line 112). Under V2 a missing developer blocks only the items it claimed.
4. **V1's grant ids are ambiguous.** Two holders may both pick `g0001` (V1 line 54), so any ledger row or graph edge that cites `g0001` is ambiguous (DA X-002).
5. **V1's archive breaks paths** (V1 line 90) and its ledger is not a file but a directory listing that needs `ls` or a script to read (V1 line 40, DA C-010).
6. **V3's double-dispatch check is advisory and racy.** "Between the fetch and the other side's push there is a window in which both can claim one item; the check is advisory" (V3 line 62); V3 itself calls this the "weakest protection" (V3 line 96). For a backend reviewer, a known race on the one shared resource (an issue or PR receiving outward writes) is the most serious defect in the set.
7. **V3 makes invisible claims legal.** "A developer who never pushes is invisible. That is allowed" (V3 line 69). A private coordinator's claims cannot be seen, so the advisory check silently passes against it.
8. **V3 departs from the owner's wording** of one coordinator branch per project (V3 line 97, DA X-001).
9. **V3's folder discipline is enforced by nothing.** "A commit touching another developer's folder is refused by review (no hook exists for this today)" (V3 line 54).
10. **V3's epic and release view needs multi-branch tooling** (V3 lines 70, 98, 104), and V3 expects Orca's prefix to equal the handle (V3 line 9), which my `git worktree list` check shows is not universal (`issue-409-mvp` sits on `409-Phase2`).

## Concessions

1. **The lock holds only if conflicts are honoured.** The add/add conflict appears during `git pull --rebase`, not at push (V2 line 69). An agent that resolves it by keeping its own copy, or a rebase run with an automatic strategy option, steals the claim silently. V2 needs an explicit rule it does not yet state: any conflict under `claims/` aborts the rebase, drops the local claim commit and counts as a lost claim. Also, git raises no conflict if both bodies are byte-identical; V2's bodies carry the coordinator id and stamp (V2 line 20), so they differ, but that should be a stated rule, not an accident.
2. **Single append-only files are less safe than one file per entry.** V2 admits "a careless whole-file rewrite by the writer could drop rows" (V2 line 105). V1's one-file-per-entry shape (DA U-002) removes that risk; on integrity grounds V1 is better on S-003.
3. **Grant ids can repeat for one developer.** `<dev>-g<4 digits>` keeps two developers apart (V2 line 54), but one developer with two coordinators (for example `epic-orchestrator-mode/ironbelly` and `release-v5-1-0/ironbelly`) can mint `ironbelly-g0001` twice unless the counter runs per developer across all their coordinators. V2 does not say which. The same gap exists for ledger row ids `<dev>-<YYYYMMDD-HHMMSS>` (V2 line 53): V2 has no same-second rule, while V1 does (V1 line 60).
4. **A push before every dispatch costs latency and needs the network** (V2 line 103); an offline coordinator cannot dispatch. That is the price of a real lock, but it is a price.
5. **Stale claims from departed developers are unresolved** (V2 line 114), as are who the project owner is (V2 line 112) and who writes grants (V2 line 113).
6. **The worktree name omits the developer** (V2 line 50) and so relies on A-002 (one developer per host), which V2 at least marks UNVERIFIED (V2 line 111).
7. **The `<dev>-2` rule is under-specified.** "Only when the first is still active" (V2 line 48) does not say what happens to the `-2` folder when the first closes, or whether a later third coordinator reuses `-2`.
8. **No single ledger per epic.** With several developers on one epic, the epic's history is split across developer folders; reading "every decision on epic X" means reading several `ledger.md` files. V1's single scope ledger (DA U-001) is better for that one question.

## Shared assumption responses

| # | Response | Reason |
|---|---|---|
| A-001 | QUALIFY | `gh api user --jq .login` is the right identity source and commit metadata is not, but each session must read the login once at start and record it in `coordinator.md`, and a session without an authenticated `gh` must refuse to create a folder or claim. |
| A-002 | QUALIFY | Holds on this host (one human, Orca worktrees in one folder), but if two developers ever share a host the worktree name must include the handle; V2 already marks it UNVERIFIED (V2 line 111). |
| A-003 | QUALIFY | Required, not just assumed: V1's and V2's locks are void after a force-push, so "never force-push `coordinators`" must be a written rule, ideally enforced by branch protection on the fork (whether the fork allows that is UNVERIFIED). |
| A-004 | QUALIFY | A real gap for all three: a coordinator on an unmerged branch must read current code and program documents from `origin/master` or the program branch with `git show`, never from its own checkout; rebasing the shared branch to catch up would be a rewrite and break A-003. |
| A-005 | QUALIFY | The owner's "create and maintain a Coordinator branch and worktree" points to developer-launched Orca sessions counting as person-opened, but it should be confirmed in the ledger before any layout is built. |
| A-006 | QUALIFY | The fork is private per project `CLAUDE.md`, but grants quote owner wording and briefs may quote captures, so everything pushed must be sanitized (no tokens, no secrets); a private fork is not a licence to push raw captures. |

## Per-point verdicts

| point | superior variant | reason |
|---|---|---|
| S-001 | tie | All three use the same 8 sections. |
| S-002 | 2 | Scope then developer gives the epic view as one folder and the developer view as one glob, and allows several developers per epic. |
| S-003 | 1 | One file per entry cannot lose rows to a careless rewrite (DA U-002); V2 concedes this. |
| C-001 | tie (1, 2) | One shared branch matches the owner's wording and is what makes a shared lock possible. |
| C-002 | 2 | One coordinator per developer per scope meets the owner's multi-developer case; V1 blocks it, V3 has no awareness at all. |
| C-003 | 2 | Pushed create-once claims keyed on issue, PR or item are git-enforced and project-wide; V1 misses cross-scope writes, V3 is racy. |
| C-004 | 2 | A stated release-only claim rule; V1 leaves release-only items unresolved, V3 has none. |
| C-005 | tie (2, 3) | Archiving by a state row keeps every cited path valid; V1's move breaks them. |
| C-006 | 3 | The developer's own branch and folder make grant ownership unambiguous by path; V2's handle-prefixed id can still repeat across one developer's coordinators. |
| C-007 | 2 | One branch, one folder per scope, one glob per developer, no checkout. |
| C-008 | 3 | A push grant limited to one's own branch is the narrowest permission. |
| C-009 | 3 | An `adhoc` kind covers coordinator work that belongs to no epic or release. |
| C-010 | tie (2, 3) | One ledger file per coordinator is readable without a script. |
| X-001 | tie (1, 2) | Both keep the owner's one branch per project; V3 departs from it. |
| X-002 | 3 | Ids qualified by the coordinator id cannot collide; V1's `g0001` can, and V2's `<dev>-g` id can within one developer. |
| X-003 | tie | All three base on a non-master branch against spec 6.2 and all mark Orca support UNVERIFIED. |
| A-001 | tie | All three use the GitHub login and none says how a session proves it. |
| A-002 | 2 | Only V2 states the one-developer-per-host assumption as UNVERIFIED. |
| A-003 | 3 | V3 has no lock a force-push could void, though only because it has no lock. |
| A-004 | tie | All three are equally exposed to a stale unmerged base. |
| A-005 | tie | All three rely on the same unconfirmed reading of "person-opened". |
| A-006 | 3 | V3 lets a developer keep a coordinator unpushed, so less leaves the host. |
