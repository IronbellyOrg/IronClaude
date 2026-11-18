# Round 1 advocate statement: variant 1 (proposal A, scope folders with a lease)

Persona: architect (structure, dependencies, long-term impact). Line numbers below refer to the variant files in this folder as read on 2026-11-14.

Facts I checked myself (read-only, 2026-11-14):
- `git branch -a --list '*coordinator*'` in this worktree prints nothing: no `coordinators` branch exists locally or as a remote-tracking ref, so every variant starts from zero.
- `git log -200 --format='%an'` gives `Ironbelly` 128, `coder` 31, `Ryan wiancko` 24, `clayphi` 17. This matches the variants' fact lists and supports A-001: author names are not identities.
- `git worktree list` shows Orca worktree `brainstorm-reflect-panel` on branch `ironbelly/shadow-runs`, so the worktree folder name and the branch name do not always match. All three variants say the branch is "observed `<orca-prefix>/<name>`"; that observation has at least one exception.
- I did not open `merged-requirements.md`; the citations to spec 6.2 line 951 and XC-01 are the variants' own and are UNVERIFIED by me.

## Position summary

Variant 1 makes the scope (an epic or a release) the unit of decision authority: one folder, one ledger, at most one live coordinator per scope, held through a lease file `holder.md` whose fixed path turns a git push conflict into a lock (variant 1 lines 3, 59). Every ledger and grant entry is a new, never-edited file (lines 24 to 28, 66 to 67), so content conflicts cannot occur by construction.

Honest verdict from the architect seat: variant 1 is right about one structural principle that the other two lose (decisions about an epic need one authority and one record), and right about immutable one-file-per-entry storage. Variant 2 is better on most of the other points, chiefly because it matches the owner's "multiple developers with multiple coordinators will be working on the same project" and because its project-wide `claims/` catch collisions my per-scope lease cannot see (diff U-003). In the per-point table below variant 2 wins more points than mine. The design I would defend in Round 2 is variant 2's layout and claims, carrying over variant 1's immutable entry files and an optional single-holder mode for scopes whose decisions must not fork.

## Steelman of variant 2

Variant 2 is the only proposal that uses both axes the owner named ("Coordinators per developer, per epic or per release as sub-dir's"): scope first, developer second (variant 2 lines 3, 23 to 33). That gives one folder per (scope, developer) pair with a single writer, so the shared branch never has two writers in one folder (line 65), while still allowing several developers on one epic at the same time (line 102), which is exactly the owner's multi-developer case. Its lock is placed at the real point of harm: the outward write. `claims/issue-<N>.md`, `claims/pr-<N>.md` and `claims/item-<scope>-<id>.md` are project-wide, create-once, and must be pushed before dispatch (lines 19 to 22, 59, 67), so an epic coordinator and a release coordinator that both want to touch PR 539 collide in git, which no scope-local scheme can detect (diff U-003). Paths never move after creation (archive is a state row, line 87), so every citation stays valid. The ledger is one readable file per coordinator (line 27), so the owner can read a decision ledger with `git show` and no tooling (line 74). "Everything on epic X" is one folder and "everything developer Y runs" is one glob (line 76). The release/epic rule is explicit and covers release-only items (line 68), which variant 1 leaves open.

## Steelman of variant 3

Variant 3 removes shared mutable state entirely: each developer writes only `<dev>/coordinators` and only `.dev/coordinators/<dev>/` (variant 3 lines 3, 60). With no shared write target there is no lock to get wrong, no non-fast-forward retry loop, no force-push hazard to a shared lock, and no way for one developer's mistake to damage another's ledger. Its push grant is the narrowest of the three, one developer's own branch (line 71), which fits a project whose rules treat every outward write as needing an explicit grant. It follows a habit the project already has: developer-prefixed branches such as `ironbelly/...` and `origin/clayphi/433-ccsession-orca-resume` (line 9; diff U-006). Because folders are disjoint, a later combined view is a clean merge of all developer branches (line 63), so the design does not foreclose a shared view. It also admits an `adhoc` kind (line 46), which covers real coordinator work that is neither an epic nor a release (for example PR triage), and allows private coordinators (line 69).

## Strengths claimed

1. **One decision authority per scope.** Variant 1 gives each epic exactly one ledger and one live holder (lines 3, 66, 69). Decisions are scope-level, not item-level: "use design X for the TUI layout" governs every item in the epic. In variant 2, two coordinators on one epic keep two ledgers (lines 25 to 33) and claims guard only items (line 67), so they can record contradictory decisions for the same epic and nothing structural notices. In variant 3 the same split exists across branches (lines 35, 62). Long-term, a single decision record per epic is what a later reader (or a later merge to master) needs.
2. **Immutable entries, conflict-free by construction.** Every ledger and grant entry is a new file never edited after creation (lines 24 to 28, 66 to 67). A rebase onto another writer's commits cannot conflict on content (line 70). Variant 2 relies on writer discipline instead and admits that "a careless whole-file rewrite by the writer could drop rows" (variant 2 line 105); variant 3 has the same exposure (variant 3 line 61). Diff U-002 records this as a unique contribution.
3. **Small lock surface.** The only contended path is one `holder.md` per scope (lines 59, 70). The coordinator pushes it once per lease, not once per dispatch. Variant 2 needs a pushed claim before every dispatch (variant 2 line 103), and a delete to release it (line 66), which multiplies the number of contended writes.
4. **Handover is a first-class transition.** The ledger of an epic survives a change of developer: the holder record moves to `holders/` and the next developer takes `holder.md` (lines 22 to 23, 68, 88; diff U-001). In variant 2 a departed developer's claims have no reclaim path yet (variant 2 line 114), and in variant 3 a departed developer's branch is simply orphaned (variant 3 line 82).
5. **Matches the owner's "a Coordinator branch".** One shared `coordinators` branch per project (line 50), as the owner worded it; variant 3 departs from that wording and says so (variant 3 line 97; diff X-001). Variant 2 shares this strength.
6. **Lease must be pushed before dispatch.** "A local, unpushed lease is not a lease" (line 73), so the visibility lag can hide new ledger entries but never who holds a scope (line 78).

## Weaknesses in other variants

1. **Variant 2: decisions can fork inside one epic.** Claims lock items, issues and PRs (variant 2 lines 19 to 22, 67), but two coordinators on `epic-orchestrator-mode` each keep their own `ledger.md` (lines 27, 32). Nothing makes them agree on epic-wide decisions, and the owner then reads N ledgers for one epic.
2. **Variant 2: append-only single files depend on discipline.** Its own risk list says a whole-file rewrite could drop rows (line 105); an agent that edits a claim instead of creating one breaks the lock (line 104).
3. **Variant 2: `scope.md` race resolution is lossy.** The second creator "drops their copy and keeps the pushed one" (line 57), so the scope's member list is whatever the first pusher wrote, with no record that a second developer disagreed.
4. **Variant 2: stale claims.** Release is by deletion, only by the named coordinator or the project owner (line 66); reclaiming from a departed developer is unresolved (line 114). A stale claim blocks an item indefinitely, which is the same failure mode as a vanished lease holder, at item granularity and so in more places.
5. **Variant 3: double dispatch is not prevented.** Its own text: "the check is advisory and racy, and it depends on everyone pushing" (variant 3 lines 62, 96). It also allows private unpushed coordinators (line 69), whose claims nobody can see at all.
6. **Variant 3: departs from the owner's wording.** One branch per developer instead of one per project (line 97; diff X-001), and "everything on epic X" needs a scan of every developer branch (line 70).
7. **Variant 3: folder ownership is enforced only by review.** "No hook exists for this today" (line 54).
8. **Variant 3: grant ids are only unique inside one coordinator** (line 50); a cross-developer citation of `g0003` needs the coordinator id to disambiguate, the same class of problem as diff X-002 in my own variant.

## Concessions

1. **The lease serialises an epic.** Two developers cannot coordinate one epic at once (variant 1 line 104). The owner said "multiple developers with multiple coordinators will be working on the same project"; on one project that need not mean one epic, but a big epic must wait on handovers or be split, and splitting is a cost the owner did not ask for.
2. **Cross-scope collisions are not caught.** An item belongs to one scope (line 69), but an epic coordinator and a release coordinator can both write to the same issue or PR; my lease is per scope and cannot see that. Variant 2's project-wide claims catch it (diff U-003). This is the strongest point against variant 1.
3. **Grant ids are ambiguous.** "two holders never mint the same file even if both pick `g0001`" (line 54) keeps file names unique but lets two grants carry the same id (diff X-002). Fix: the grant id must be the file stem (stamp plus handle), or carry the handle as variant 2 does.
4. **Ledger readability.** The owner's ledger is "the sorted list of `ledger/*.md`" and needs `ls` or a reader script (line 40; diff C-010). A table in one file needs no tooling; mine adds tooling.
5. **Archive moves break citations.** Moving a scope to `archive/` "rewrites every path others may cite" (line 90); variants 2 and 3 keep the folder in place (variant 2 line 87; variant 3 line 81).
6. **Release-only items are unresolved** in my variant (line 114); variant 2 states a rule (variant 2 line 68).
7. **A vanished holder blocks the scope** until the project owner forces a takeover (line 106), and who the project owner is stays unresolved (line 112).
8. **The developer axis is only a field**, so "what is clayphi coordinating" needs a scan of every `holder.md` (line 105).
9. **Worktree branch naming is weaker than stated.** I found worktree `brainstorm-reflect-panel` on branch `ironbelly/shadow-runs`, so "observed `<orca-prefix>/<name>`" (line 52) is not a rule. This does not break variant 1 (the branch name is not used in any lock) but the table row should say so.

## Shared assumption responses

| # | Response | Reason |
|---|---|---|
| A-001 | QUALIFY | The GitHub login is the right handle, but it must be read from `gh api user --jq .login`, never from git metadata (the log shows `coder` 31 times), and the design needs a stated failure when `gh` is not authenticated. |
| A-002 | QUALIFY | True for today's per-person Coder hosts, and collision rule 4 (`orca worktree list` before create) already covers one host; it should still be written down, as variant 2 does. |
| A-003 | ACCEPT | Git conflict locks (variants 1 and 2) are void after a force push, so the rule "never force-push `coordinators`" must be stated in `README.md` and, if the fork's plan allows it, enforced by branch protection (UNVERIFIED). |
| A-004 | REJECT | False as written: a worktree based on `origin/coordinators` lacks master code and documents committed after its base, so every variant needs a rule (read program documents with `git show origin/master:<path>`, or merge `origin/master` into `coordinators` on a schedule). |
| A-005 | QUALIFY | The owner's "create and maintain a Coordinator branch and worktree" points that way, but whether an Orca `--agent` launch counts as "person-opened" is an owner decision, not a design fact. |
| A-006 | QUALIFY | The fork is private per project `CLAUDE.md`, but grant entries quote owner wording and may hold captures; the layout needs a "no secrets, sanitised captures only" rule before routine pushes. |

## Per-point verdicts

| point | superior variant | reason |
|---|---|---|
| S-001 | tie | All three use the same 8 sections. |
| S-002 | 2 | Scope then developer serves both axes the owner named and lets several developers share one epic. |
| S-003 | 1 | One immutable file per entry makes content conflicts and dropped rows impossible, not just unlikely. |
| C-001 | tie (1, 2) | Both keep the one shared project branch the owner asked for; 3 departs from it. |
| C-002 | 2 | One coordinator per developer per scope matches the multi-developer brief; a lease serialises an epic. |
| C-003 | 2 | Project-wide pushed claims keyed by issue, PR and item catch cross-scope collisions; my lease is scope-local and 3 is advisory. |
| C-004 | 2 | It states a rule for release-only items; variant 1 leaves them unresolved and 3 has no rule. |
| C-005 | tie (2, 3) | A state row keeps every cited path valid; moving to `archive/` breaks citations. |
| C-006 | 2 | Grant ids carry the handle, which avoids the X-002 ambiguity and keeps grants per coordinator. |
| C-007 | 2 | One branch, one folder per scope and one glob per developer; 3 needs a scan of many branches. |
| C-008 | 3 | A grant to push only one's own branch is the narrowest outward-write permission. |
| C-009 | 3 | `adhoc` covers real coordinator work that is neither an epic nor a release, at almost no cost. |
| C-010 | tie (2, 3) | One ledger file per coordinator is readable with `git show` and no tooling. |
| X-001 | tie (1, 2) | Both match the owner's "a Coordinator branch"; 3 gives one per developer. |
| X-002 | 2 | Handle-prefixed grant ids (`ironbelly-g0001`) are unique project-wide; variant 1's `g0001` can repeat. |
| X-003 | tie | All three base the worktree on a non-master branch and all mark Orca support UNVERIFIED. |
| A-001 | tie | All three use the GitHub login and none states the unauthenticated-`gh` failure. |
| A-002 | 2 | Only variant 2 names the shared-host assumption and marks it UNVERIFIED. |
| A-003 | 3 | No correctness property of 3 depends on a git conflict lock, so a force push voids nothing that was a guarantee. |
| A-004 | tie | All three share the stale-base gap and none addresses it. |
| A-005 | tie | All three rely on the same unstated reading of "person-opened". |
| A-006 | 3 | It allows private, unpushed coordinators, so a developer can keep sensitive coordinator state off the fork. |

Tally: variant 2 superior or co-superior on 12 points, variant 3 on 6, variant 1 on 3 (S-003 alone, C-001 and X-001 shared), and 5 plain ties (S-001, X-003, A-001, A-004, A-005).
