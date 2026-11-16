# Round 1 advocate statement: variant 3 (proposal C)

Advocate: variant 3 (`variant-3-original.md`). Persona: qa (edge cases, failure scenarios). Depth: quick.

Facts I checked read-only on 2026-11-14 (from this worktree):
- `git branch -r --list 'origin/*coordinators*'` prints nothing: no branch named `coordinators` or `<dev>/coordinators` exists on the fork today.
- `git branch -r --list 'origin/*/*'` shows developer-prefixed branches on the fork, for example `origin/clayphi/433-ccsession-orca-resume`, `origin/clayphi/help-472-473`, `origin/ironbelly/codegraph-wording`.
- `git worktree list` shows Orca worktrees under `/home/coder/workspaces/worktrees/IronClaude/<name>` on `ironbelly/<name>` branches, and one (`issue-409-mvp`) on `409-Phase2`, so the `ironbelly/` prefix is not universal on this host.
- `ls .dev/coordinators` fails: the folder does not exist.
- `merged-requirements.md:951` says "one worktree never holds two live agents" and that the coordinator "never creates a worktree for its own use, and never switches a checkout's branch on its own"; `merged-requirements.md:954` says a top-level agent's worktree is created with `--base-branch origin/master`.
- Not verified by me: the XC-01 wording "committed only when the owner asks" (quoted by variants 1 and 2), Orca's branch-prefix rule, and whether Orca accepts a non-master base branch. These stay UNVERIFIED.

## Position summary

Variant 3 makes the developer the unit of write ownership: each developer writes only `.dev/coordinators/<dev>/` on their own `<dev>/coordinators` branch (variant 3, "In one sentence" and Layout). From a failure-scenario view this has the smallest blast radius of the three: no shared file, no shared branch, no lock that can get stuck, and no lock that a careless rebase or force push can silently break. Its real weakness is double dispatch across developers, which it handles only with an advisory, racy scan (variant 3, Concurrency, "Double dispatch is not prevented by structure"). My honest Round 1 position: variant 3 is the best write model, variant 2 is the best coordination model, and the strongest merge is likely variant 2's scope-first reading surface and project-wide claim keys with variant 3's per-developer write isolation where it can be kept. I argue for variant 3's isolation as the non-negotiable part.

## Steelman of variant 1

Variant 1's strongest case: it is the only design where double dispatch inside a scope is impossible by construction, because only one session may hold a scope at a time ("Inside one scope it cannot happen: one holder", variant 1, Concurrency). The lease is a single fixed path (`holder.md`), so git turns the race to take a free scope into a rebase conflict that the loser sees ("The path is the lock", Collision rule 2), and a lease counts only once pushed ("a local, unpushed lease is not a lease", Concurrency). Entries are one file each and never edited (U-002), so even a careless writer cannot lose a past row or cause a content conflict. The epic ledger survives a change of developer through handover (U-001), which is the one property the other two lack: a long epic keeps one continuous decision history no matter who coordinates it this week.

## Steelman of variant 2

Variant 2's strongest case: it is the only design that satisfies all three parts of the owner's wording at once: one shared "Coordinator branch" per project (X-001), "multiple developers with multiple coordinators ... on the same project" (several developers on one epic, variant 2, Cost and risk), and "allow multiple developers to share the same space" (scope folder with developer sub-folders, S-002). Its claim files are keyed by the thing that is actually written to the outside world (`issue-<N>`, `pr-<N>`, `item-<scope>-<id>`, Naming convention), so they catch an epic coordinator and a release coordinator both touching one issue (U-003), which a per-scope lease cannot. Its rule is fail-closed: "No pushed claim, no dispatch" (Concurrency). Reading is cheap: one folder for an epic, one glob for a developer (Visibility). Archive keeps paths stable (Lifecycle, archived row).

## Strengths claimed

1. **Smallest blast radius for any write failure.** "Nothing shared is ever written. Each developer branch and folder has one human owner; each coordinator sub-folder has one session writer" (variant 3, Concurrency). A bad rebase resolution, a whole-file rewrite or a `push --force` on `ironbelly/coordinators` can damage only ironbelly's own state. In variants 1 and 2 the same mistake on the shared `coordinators` branch can delete every developer's ledgers and every lock (A-003).
2. **No lock can be stuck, so a departed or crashed developer blocks nobody.** Variant 1 admits "a holder who disappears blocks the scope until the project owner forces a takeover" (Cost and risk). Variant 2 leaves "How a claim is reclaimed from a coordinator whose developer has left" unresolved (What stays unresolved). In variant 3 claims are advisory and the deletion of a departed developer's branch is already assigned to the project owner (Lifecycle, deleted row).
3. **No dependence on an agent reading a rebase conflict correctly.** Variants 1 and 2 make a git conflict the lock signal (variant 1 Collision rule 2; variant 2 Collision rule 3). An agent that resolves the conflict by keeping its own side, or that runs `git checkout --ours`, takes the lock silently. Variant 3 has no conflict-as-lock to misread, because two developers never touch one path.
4. **Narrowest push permission.** "a push grant per developer for their own branch only, narrower than a shared-branch grant" (variant 3, Visibility). A grant row that authorizes pushes is bounded to one developer's data (C-008).
5. **Matches existing practice on this fork.** Developer-prefixed branches already exist on `origin` (`origin/clayphi/...`, `origin/ironbelly/...`; checked above, and variant 3 Facts). No new shared-branch convention or protection is needed.
6. **Grants cannot be misread as another developer's.** "the path names the developer" (variant 3, Relation to existing rules, grant rows), and the coordinator id `<dev>:<kind>-<scope>` qualifies ledger and grant ids project-wide (Naming convention). This avoids variant 1's ambiguous `g0001` (X-002).
7. **Covers work that is neither an epic nor a release.** The `adhoc` kind (`adhoc-pr-539-triage`, Naming convention) gives PR triage and one-off coordination a home; variants 1 and 2 have only `epic` and `release` (C-009).
8. **Private coordinators are possible.** A developer may choose not to push (Visibility), so sensitive grant wording or captures need not leave the host (relevant to A-006).
9. **Disjoint folders make a later combined view clean.** "merging all `<dev>/coordinators` branches is also clean, because the folders are disjoint" (Concurrency). If the owner later wants one shared branch, variant 3 converts to it without conflict.

## Weaknesses in other variants

1. **Variant 1: two developers cannot work one epic at once.** "a big epic either waits on handovers or is split into smaller epics" (variant 1, Cost and risk). This conflicts with "multiple developers with multiple coordinators will be working on the same project" when work clusters in one epic.
2. **Variant 1: cross-scope collisions are not caught.** "an item belongs to exactly one scope" (Concurrency) covers items, but two scopes can still write the same issue or PR (diff analysis U-003). Release-only items such as the changelog are unresolved (variant 1, What stays unresolved, last bullet).
3. **Variant 1: archive move breaks citations.** "the scope folder moves to `.dev/coordinators/archive/<kind>-<scope>/` ... (a move rewrites every path others may cite)" (Lifecycle). Every ledger row elsewhere that cites the old path breaks; the variant names the cost itself.
4. **Variant 1: grant ids are ambiguous.** "two holders never mint the same file even if both pick `g0001`" (Naming convention) leaves two grants with one id (X-002). A ledger row citing `g0001` cannot be resolved without the file name.
5. **Variant 1: the ledger the owner reads does not exist as a file.** "it is the sorted list of `ledger/*.md` (a reader script or `ls` makes the table)" (Layout). The variant names no existing reader script, so the owner's most-read document needs new tooling (C-010).
6. **Variants 1 and 2: the lock is void under force push or a wrong conflict resolution.** Both rely on git refusing the second push (variant 1 Concurrency, merge; variant 2 Concurrency, merge). Neither names branch protection on `coordinators`, and neither tells the losing agent what to do beyond treating the conflict as the signal (A-003).
7. **Variants 1 and 2: one shared branch is a single point of failure for every developer.** Both admit push races and retry loops (variant 1, Cost and risk, last bullet; variant 2, Cost and risk, last bullet). A corrupted or rewritten `coordinators` branch stops every coordinator in the project at once.
8. **Variant 2: claims depend on the coordinator listing every outward target.** The claim covers "the item (and ... each issue or PR the item writes to)" (Concurrency). An item that touches an issue the coordinator did not list escapes the lock; nothing checks the list.
9. **Variant 2: claim files are only safe if never edited.** "an agent that edits a claim instead of creating one breaks the lock" (Cost and risk). Claim release is deletion "done only by the coordinator named in it" (Concurrency), but nothing enforces it.
10. **Variant 2: first writer of `scope.md` wins silently.** "a second developer who meets an add/add conflict on `scope.md` drops their copy" (Collision rule 1). The second developer's scope wording (member epics, release-only items) can be lost without anyone reviewing it.
11. **Variant 2: dispatch stops when the fork is unreachable.** "No pushed claim, no dispatch" (Concurrency) is fail-closed; that is correct for safety, but a GitHub outage halts every coordinator. Variant 3 degrades to advisory instead.
12. **Variants 1 and 2: worktree names collide on a shared host.** Both use `coord-<kind>-<scope>` with no handle (Naming convention). Variant 2 marks the shared-host case UNVERIFIED (What stays unresolved); variant 1 relies on it silently (A-002).

## Concessions

1. **Double dispatch across developers is not prevented.** Variant 3 says so itself: "Between the fetch and the other side's push there is a window in which both can claim one item; the check is advisory" (Concurrency). For a qa reviewer this is the largest single failure scenario in any of the three variants, and variant 2's pushed claim is strictly better on it (C-003).
2. **A developer who never pushes is invisible, including their claims.** "A developer who never pushes is invisible ... nobody else can see its claims" (Visibility). Private coordinators (strength 8) and claim visibility pull against each other.
3. **It departs from the owner's wording.** "The owner asked for 'a Coordinator branch' per project; this gives one per developer" (Cost and risk). This is a real cost, not a technicality (X-001).
4. **Cross-developer views need a scan of many branches.** "Everything on epic X" needs `git for-each-ref` plus `git ls-tree` on each branch (Visibility); no tool for it exists (C-007).
5. **No release-versus-epic rule.** Variant 3 is silent on what a release coordinator may dispatch (diff analysis C-004). Variant 2's rule should be adopted.
6. **Pushes still race inside one developer.** Variant 3 says the merge back into `<dev>/coordinators` is clean (Layout note, Concurrency), but two coordinators of one developer pushing at once still need fetch, rebase and retry. The variant does not name the publish command; spec 6.2 forbids switching a checkout's branch (`merged-requirements.md:951`), so it must be a push of `HEAD` to `<dev>/coordinators` after a rebase, which variant 3 should state.
7. **`profile.md` "hosts, how to reach them" is a privacy risk once pushed** (Layout). It should hold only the handle.
8. **Leaf-name rule.** `<dev>/coordinators` blocks any branch `<dev>/coordinators/...` (Collision rule 1). Orca's `<dev>/coord-...` branches do not clash (checked: no `coordinators` branches exist), but the rule is a new constraint on every developer's namespace.

## Shared assumption responses

| # | Response | Reason |
|---|---|---|
| A-001 | QUALIFY | The GitHub login is the only usable handle (`user.name` is `coder`), but it must be read from `gh api user` at session start, the session must refuse to start when `gh` is unauthenticated, and the handle is frozen at creation because a GitHub rename would otherwise orphan a folder or branch. |
| A-002 | QUALIFY | True on this host today, but all three worktree names omit the handle; adding `<dev>-` to the worktree name is cheap insurance for a shared Coder host. |
| A-003 | QUALIFY | Required for variants 1 and 2 (their locks are void after a force push) and needs branch protection on `coordinators` (UNVERIFIED that the fork has or allows it); for variant 3 a force push damages only the pusher's own branch. |
| A-004 | REJECT | A worktree based on an unmerged coordinators branch does not see master code or documents committed after its base; every variant must read program documents with `git show origin/master:<path>` (or the owning branch) and record the revision, rather than assume the checkout is current. |
| A-005 | ACCEPT | Spec 6.2 already says the coordinator "never creates a worktree for its own use" (`merged-requirements.md:951`), so the developer launching it with `orca worktree create --agent` is the consistent reading; it should still be confirmed by the owner. |
| A-006 | QUALIFY | The fork is private per project `CLAUDE.md`, but grant wording and captures should be sanitized before push, and variant 3's `profile.md` should hold no host or contact detail. |

## Per-point verdicts

| point | superior variant | reason |
|---|---|---|
| S-001 | tie | All three use the same 8 sections. |
| S-002 | 2 | Scope then developer gives the epic view as one folder and the developer view as one glob, and fits "share the same space". |
| S-003 | tie (2, 3) | With one writer per file, an append-only file cannot conflict with other writers and is readable as is; git history recovers a careless rewrite. |
| C-001 | 3 | Per-developer branches remove cross-developer push races and limit a force push to one developer's data; the owner-wording cost is scored at X-001. |
| C-002 | 2 | Several coordinators per scope, kept apart by claims, serves multi-developer epics without variant 1's handover wait or variant 3's blind overlap. |
| C-003 | 2 | A pushed create-once claim is a git-enforced lock with "no pushed claim, no dispatch"; variant 3's scan is racy and variant 1 misses cross-scope writes. |
| C-004 | 2 | The only variant with an explicit rule that also covers release-only items. |
| C-005 | tie (2, 3) | A state row keeps every cited path valid; variant 1's move breaks citations. |
| C-006 | 2 | The handle inside the grant id keeps ids unique even when quoted out of their folder; variant 3 needs the coordinator id prefix, variant 1 is ambiguous (X-002). |
| C-007 | 2 | One fetch and one known path, against variant 3's scan over every developer branch. |
| C-008 | 3 | A push grant for the developer's own branch only is the narrowest authority. |
| C-009 | 3 | `adhoc` gives PR triage and one-off coordination a home without inventing a fake epic. |
| C-010 | tie (2, 3) | One readable file per coordinator; variant 1 needs a reader script that it does not name. |
| X-001 | tie (1, 2) | Both keep one shared branch per project as the owner worded it; variant 3 departs from it. |
| X-002 | 2 | Its grant id carries the handle, so the ambiguity in variant 1 cannot arise. |
| X-003 | tie | All three base on a non-master branch against spec 6.2 (`merged-requirements.md:954`) and all mark Orca support UNVERIFIED. |
| A-001 | tie | All three use the same handle source and none states the unauthenticated or renamed-login case. |
| A-002 | 2 | The only variant that names the shared-host case as UNVERIFIED instead of relying on it silently. |
| A-003 | 3 | No shared branch and no git-conflict lock, so a force push or wrong conflict resolution cannot break another developer's lock. |
| A-004 | tie | All three share the stale-base problem equally and none addresses it. |
| A-005 | tie | All three have the developer launch the coordinator worktree the same way. |
| A-006 | 3 | It is the only variant that allows a coordinator to stay unpushed, though its `profile.md` needs trimming. |
