# Refactoring Plan: Merge into Base (Variant 1)

## Overview

- Base: Variant 1 (architect persona: one release line cut from `master`, story branches, local merges by the coordinator, one pull request into `master`). Selected in `base-selection.md` (final score 0.9351 against V3 0.9203; tiebreaker Level 1, 27 of 41 debate points).
- Incorporating strengths from: Variant 2 (4 items), Variant 3 (7 items), Variant 4 (9 items), the debate itself (4 items), and the invariant probe (changes 25, 26 and 30), plus three answers this plan adds: hotfix and special releases (27), the ref-name rule (28), the fit with the owner's decisions of 2026-11-23 (29).
- Planned changes: 30 (changes 1 to 24 are the listed strengths; 25 to 30 are the must-answer items).
- Approach mix: 8 replace (changes 1, 3, 10, 20, 21, 22, 27, 28), 9 append (4, 5, 6, 9, 11, 12, 15, 16, 24), 12 insert (2, 7, 8, 13, 14, 17, 18, 19, 23, 26, 29, 30), 1 restructure (25).
- Risk level (overall): Medium. One change is new design with no precedent in any variant (change 25, the size budget and records rule); two touch many lines of the base (changes 1 and 10, the names).
- Status of the invariant gate: INV-017 (HIGH, UNADDRESSED in the probe) is answered by change 25. Changes 26 and 30 answer the 10 MEDIUM and 7 LOW unaddressed findings. The orchestrator should re-run the invariant gate on the merged text; this plan does not lift `BLOCKED_BY_INVARIANTS` by itself.
- New sections in the merged document (base sections 1 to 7 stay in place): section 8 "Size budget and records rule", section 9 "Trials before first reliance", section 10 "Decisions for the owner"; base section 8 "Sources" moves to section 11. A grep of `variant-1-original.md` for "section N" and "sec N" (VERIFIED-HERE) finds only two references, to section 4 and section 2, so the renumbering breaks none.
- Everything marked "default" below is a number or rule the owner may change. The marks tell which defaults rest on evidence and which are guesses.

Read-only checks run for this plan on 2026-11-23 (no project, git or GitHub write; scratch repositories under `/tmp` were removed): two scratch-repository tests (results in changes 25, 26 and 28), `orca worktree create --help`, `git --version` (2.47.3), the GitHub REST documentation for the pull-request files endpoint, and a grep for pinned counts in `tests/`.

## Evidence marks used in this plan

| Mark | Meaning |
|------|---------|
| VERIFIED-HERE | I ran or read it for this plan on 2026-11-23 (scratch test, CLI help, fetched documentation, grep). |
| VERIFIED-PROBE | Verified by the invariant probe or by an advocate with read-only commands; recorded in `invariant-probe.md` or `debate-transcript.md`; I did not re-run it. |
| ESTIMATE | Derived from measured data by inference; the inference is stated. |
| GUESS | Chosen for headroom or convenience; no data behind it. |
| UNVERIFIED | Not confirmed; a trial in section "Trials before first reliance" settles it. |

Rule for the merged text: every number or behaviour claim carries one of these marks. Nothing technical enforces any branching rule in this repository (no rulesets, `master` and `integration` unprotected: VERIFIED-PROBE, A4 M7), so the marks are how a reader tells a rule that rests on evidence from one that rests on taste. They replace V4's FROM SOURCE / FROM PRACTICE / MY ADAPTATION / UNSPECIFIED labels, which described GFxAI's text and do not fit a merged document (change 7).

## Planned Changes

### Part A: strengths from non-base variants (changes 1 to 20)

Section references: "sec N" is a section of `variant-1-original.md`; "Q1 to Q9" are its nine answers in sec 4. Diff and assumption ids (C-, X-, A-, U-) are from the Scoring Matrix of `debate-transcript.md`; "R2" is Round 2; the percentage is the matrix confidence.

#### From Variant 4 (GFxAI adapted)

### Change 1: Release line named `release/dash<rel>` (from Variant 4)
- **Source**: Variant 4, rule 1 (`release/dash1.3`).
- **Target**: Base sec 2 table row "Release branch" and every `dash1.3/release` in sec 2 text, sec 3 diagram label and steps 1, 3, 5, Q1 to Q9 and risk 4 (replace).
- **Rationale**: C-001 combined, 72 percent; A2, A3, A4 (R2 70) and A1R2 Q1 all adopt the `release/` folder for the line. Base-selection item 1.
- **Integration point**: Global replace of `dash1.3/release` by `release/dash1.3`. Keep the sec 2 invariant sentence: a branch name may never be the folder part of another branch name, and the bare token `dash1.3` and the bare word `release` are never branches. Redraw the sec 3 diagram label. Add one glossary sentence: the owner's words "integration branch" mean this release line; the repository branch called `integration` is a different thing.
- **Risk**: Medium. About 15 occurrences; a missed one leaves two spellings.

### Change 2: Freeze after the last planned story (from Variant 4)
- **Source**: Variant 4, rule 6 (beta freeze).
- **Target**: Base Q6, new bullet after "A bug in a story already merged..."; and sec 3, new line before step 5 (insert).
- **Rationale**: C-016, unanimous, 90 percent. Base-selection item 2. V1 had no freeze rule (A4-W3).
- **Integration point**: "Freeze starts when the ledger shows the last planned story merged, or when the time box ends (change 14). From freeze until the owner merges, only `dash<rel>-fix<NN>-<slug>` branches enter the line; no new story. While `/sc:pr-submit --monitor 3` runs, nothing enters at all (change 26, INV-005)."
- **Risk**: Low. One refusal rule for the coordinator.

### Change 3: Tag `dash-<rel>` (from Variant 4)
- **Source**: Variant 4, rule 4 (tag `dash-1.3`; the package is 6.1.0, so not `v1.3.0`).
- **Target**: Base sec 2 table row "Marker after landing" and Q7 (replace `dash/1.3`).
- **Rationale**: C-024, 3 of 4, 72 percent; same value without a `dash/` folder. CONTEXT line 15: release numbers are dashboard numbers, not package versions.
- **Integration point**: Replace the row and the Q7 sentence. Replace the base sentence "should not clash; this was not tested (UNVERIFIED)" with: a scratch repository (VERIFIED-HERE, 2026-11-23) holds tag `dash-1.3` next to branches `release/dash1.3`, `release/dash1.105`, `release/dash1.1` and `dash1.3-s04-x` without error. Add the rule: no branch is ever named `dash-<rel>` (a tag and a branch of one name make `git checkout dash-1.3` ambiguous).
- **Risk**: Low.

### Change 4: Explicit deletion, including the remote branch, with a sweep (from Variant 4)
- **Source**: Variant 4, rule 7 (GFxAI left 6 `backup/...` branches and a stale `release/v0.1`).
- **Target**: Base Q7 (append).
- **Rationale**: C-023, unanimous, 92 percent. `delete_branch_on_merge` is false and 170 remote heads exist (INV-014, VERIFIED-PROBE). Base-selection item 4.
- **Integration point**: After the ledger records the merge: delete the story branch and worktree; after the owner merges the release PR and the sync PR is open: delete `release/dash<rel>`, `dash<rel>-records` and the worktrees, local and remote (`git push origin --delete <name>`). Closeout sweep: `git ls-remote --heads origin 'refs/heads/release/dash<rel>*' 'refs/heads/dash<rel>-*'` must print nothing (hyphen-terminated globs, change 28). Branch deletion is part of the authority the owner confirms in chat (decision 1).
- **Risk**: Low. A premature delete loses nothing: the story tip is the second parent of its merge commit.

### Change 5: Release-PR size evidence (from Variant 4)
- **Source**: Variant 4, rule 4 (PR #147: 34 commits, 1,384 files, +242,976 lines, merged "with file-level rejections").
- **Target**: Base Q4 (append), as the reason for the cap in change 25.
- **Rationale**: U-015, keep as size evidence with no precedent weight, 72 percent (A4 asks that GFxAI's pedigree not be weighed). Base-selection item 5.
- **Integration point**: Add a four-row evidence list: GFxAI #147 (1,384 files); in-repo #640 (1,146 files, merged in 43 minutes, one Augment review and one Codex comment), #664 (181 files, 27 minutes), #31 (2,089 files, 0 reviews, 0 comments) (all VERIFIED-PROBE). Sentence: a fast merge shows nothing broke, not that anyone read the diff (A2 N2, A4 point 6).
- **Risk**: Low.

### Change 6: Reduced acceptance gate for the release PR (from Variant 4)
- **Source**: Variant 4, rule 4 (three test tiers, two approvals, UAT sign-off), reduced.
- **Target**: Base Q4 (append) and sec 3 step 5.
- **Rationale**: U-018, keep reduced, 58 percent (A1 and A4 agree on the reduced form; A2 and A3 state no position). The lowest-confidence item in the plan.
- **Integration point**: Gate list, in order: freeze; `master` merged in; the local gate of change 26 (INV-007) green; a green `workflow_dispatch` run on the final tip (necessary, not sufficient: INV-026); then `/sc:pr-submit --monitor 3 --base master`, PR CI and both bots settled; the owner merges with a merge commit. Not carried: GFxAI's three tiers, UAT sign-off, two approvers (no counterpart here, A4-C9).
- **Risk**: Medium. Five gates in a row; the dispatch step needs the owner's CI-minutes nod (decision 6).

### Change 7: Evidence marks on every rule (from Variant 4)
- **Source**: Variant 4 line 5 (provenance marks).
- **Target**: Base sec 1, new paragraph after the first (insert); marks applied in every section.
- **Rationale**: U-014, 78 percent, adopted by A1, A3, A4 (R2 65); S-002 to V4, 60 percent. Nothing enforces the rules, so showing which rest on evidence is substance (A4 M7).
- **Integration point**: Insert the table "Evidence marks used in this plan" (above) as a short legend; apply the marks to numbers and behaviour claims during the merge. Section-level provenance comments are separate (Step 5 tags).
- **Risk**: Low.

### Change 8: Wording of what the owner rule forbids (from Variant 4)
- **Source**: Variant 4, rule 2 ("AI Agent: Merge to Main no" turned into a coordinator rule); U-017.
- **Target**: Base Q2 "Where" bullet and sec 1 (insert).
- **Rationale**: U-017, 72 percent; adopted as wording by A1R2, A3R2, A4R2. Supports the owner's chat confirmation (A-014, QUALIFY 88 percent, unanimous).
- **Integration point**: "The coordinator never merges a pull request and never merges into `master` or `integration`. A local merge of a settled story into the release line is a separate, smaller class: local, unpublished until the forward push, revertable, the same class as the worker contract's child-into-feature merge. It needs the owner's confirmation in chat (CONTEXT line 11: 'to be confirmed'; decision 1)."
- **Risk**: Low. If the owner declines, the design falls to the optional layer of change 16 for every story.

### Change 9: The sync is the price of landing on `master` (from Variant 4)
- **Source**: Variant 4, rule 4 ("then `master` is merged back into `integration`").
- **Target**: Base Q8 (append one sentence).
- **Rationale**: C-019, unanimous, 62 percent. Already in V1 Q8 and step 6; the sentence says why. Who runs the sync today is UNVERIFIED (A-015).
- **Integration point**: "`integration` does not contain the release until the sync pull request lands; that is the price of landing on `master` instead of through `integration`." Head branch and merge method: change 19. Assignment: decision 5.
- **Risk**: Low.

#### From Variant 2 (trunk, dark landing)

### Change 10: Flat story and fix names (from Variant 2, also Variant 3)
- **Source**: Variant 2 sec 2 (`dash1.3-s04-<slug>`); Variant 3 sec 2 (`<release>-fix<NN>-<slug>`).
- **Target**: Base sec 2 table rows "Story branch" and "Fix inside a release", the sort paragraph, the `orca worktree create` command, sec 3 step 2 (replace).
- **Rationale**: C-001, 72 percent; U-004 "drop story folders", 65 percent. Reason, stated honestly: git does not force flat names (`release/dash1.3` plus `dash1.3/story-...` works, CONTEXT line 8). Flat names are insurance against one failure: a worktree created without `--branch` and called `dash1.3` gets the branch `ironbelly/dash1.3` (49 remote branches carry the `ironbelly/` prefix: A2 N5), after which `ironbelly/dash1.3/s04-...` cannot be created ("cannot lock ref"). A flat name is a leaf and cannot become the folder of another branch, with or without the prefix. A1 keeps folders (60); A2, A3, A4 go flat (70).
- **Integration point**: Patterns `dash<rel>-s<NN>-<slug>` and `dash<rel>-fix<NN>-<slug>`. Listing a release: `git branch --list '*dash1.3-*'` (the leading `*` also finds an `ironbelly/` copy). Replace the base creation command with the one in change 28 (the base command lacks `--name`, which the CLI usage requires: VERIFIED-HERE).
- **Risk**: Medium. The owner wrote `dash1.3/story1`; the document must say plainly that the shape changed and why. If trial T1 shows `--branch` always keeps the exact name and refuses a conflicting one, folders become safe again; flat stays the simpler default.

### Change 11: Outside CI per story without a workflow edit (from Variant 2)
- **Source**: Variant 2 Q2 ("CI on every slice runs against the real `integration`") as the goal; the means is `workflow_dispatch`.
- **Target**: Base Q2 (append "Outside gate"), Q4, sec 5 (the cost "No CI and no automatic review until the end").
- **Rationale**: C-007 and C-011, unanimous with qualification, 72 and 68 percent. Evidence: `test.yml` has an unconditional `workflow_dispatch` (VERIFIED-PROBE); two dispatch runs on 2026-11-05 on a branch outside the filter list, both green, 4 min 7 s and 5 min 1 s (A4 M2); median PR run 9.2 minutes, range 7.0 to 12.6 (A4 M3, last 40 runs).
- **Integration point**: Default outside gate: after the forward push of any story merge that touches the shared or risky list (change 13), and always on the final tip, the coordinator dispatches `test.yml` on `release/dash<rel>` (`gh workflow run test.yml --repo IronbellyOrg/IronClaude --ref release/dash<rel>`) and reads the result before the next story that touches the same list merges (a GUESS-level rule: about 9 minutes against a bad line). Caveat carried from INV-026: a dispatch run tests the tip alone and does not run the PR-only workflows.
- **Risk**: Medium. Needs the owner's CI-minutes nod (decision 6); trial T5. Costs about 9 minutes per run (ESTIMATE from the 40-run median).

### Change 12: Third rung of the fallback ladder: dark slices (from Variant 2)
- **Source**: Variant 2 steps 1 and Q5 (slice classification, flags, switch-on slice); U-006 to U-009.
- **Target**: Base Q5 (append the last bullet).
- **Rationale**: C-012 85 percent (no flags in the base); C-022 78 percent (V2 at slice level); U-006 "planning rule only" 60 percent; U-009 "pilot first" 65 percent.
- **Integration point**: "Third rung, not the default: after a pilot on one story, a story that cannot finish inside the time box is sliced into pieces that each land alone (new files nothing imports yet, or behind a flag) as direct pull requests into `master`. Every flag gets a retirement line in the ledger at creation (U-008)." The base sentence "Flags are not used" stays for the base design.
- **Risk**: Low. Fallback text only.

### Change 13: Shared-file list for the coordinator (from Variant 2, extended by the debate and INV-019)
- **Source**: Variant 2 Q2 ("shared files in their own first slice"); the list from A4R2 Q2.
- **Target**: Base Q2(b) (insert).
- **Rationale**: A-001 QUALIFY 88 percent (disjoint paths are necessary, not sufficient). The A4R2 list comes from the #662 stat only; INV-019 (MEDIUM) shows identical edits to a pinned count merge cleanly and give a wrong value (scratch run by the probe: two branches each change `n=47` to `n=48`, merge exits 0, file reads 48, true count 49).
- **Integration point**: List: `CHANGELOG.md`, `CLAUDE.md`, `README.md`, `PROJECT_INDEX.json`, `PROJECT_INDEX.md`, docs index files; `pyproject.toml`, `uv.lock`, `scripts/dependency_baseline.txt` (the CI lint job runs `make verify-deps` against them: VERIFIED-PROBE); every test that pins a count, for example `len(data["commands"]) == 47` in `tests/recommend/test_routing_refresh.py` (VERIFIED-HERE by grep on 2026-11-23; the probe cited line 168, the line is 137 today, so cite the assertion, not the line). Each such file is owned by one story or by a first foundation story that merges before the others start. The probe's two worker-contract counts (13 and 10) were not found by grep here and are not carried. Detection when ownership fails: the full local suite after every merge (change 26, INV-019).
- **Risk**: Low. A list; it grows as releases find new files.

#### From Variant 3 (release train)

### Change 14: Time box with floating scope (from Variant 3)
- **Source**: Variant 3 Q5 ("the scope floats, the time does not"); U-010.
- **Target**: Base Q4 last sentence and Q5 justification (insert; replaces the weaker "Driessen and Fowler only" justification).
- **Rationale**: U-010, unanimous, 95 percent; A1 conceded it is the better justification of a long-lived line (A1R2 item 8). C-013 and X-006, 86 percent.
- **Integration point**: "A release closes at six merged stories or seven days from the cut, whichever comes first (both ESTIMATE, owner sets them: decision 2). A story not merged by then is not in this release: it stays in the ledger as 'carried', keeps its branch and worktree, merges the new line tip into itself when the next release starts (merge, never rebase), and keeps its old `dash<rel>-` name; the ledger records the move." Replace the base sentence "split it if the branch is open longer than about a week" (extrapolated from DORA's one-week batch limit, S6; not a DORA figure for release branches, base text says so; keep that disclosure).
- **Risk**: Low to Medium. The numbers are estimates; the carried-story rule is new text.

### Change 15: Fallback ladder (from Variant 3 and Variant 2)
- **Source**: Variant 3 Q5 ("move toward Proposal 2"); Variant 1 Q5 ("switch to Proposal 3"); C-013, X-006.
- **Target**: Base Q5 last bullet (append; replaces "switch to Proposal 3").
- **Rationale**: C-013, 86 percent unanimous. The base refers to "Proposal 3", a different document; the merged text must stand alone.
- **Integration point**: Rung 0: the line alone. Rung 1: optional review-only story PRs for stories above the size threshold (change 16). Rung 2: a review-only PR for every story, if the time box is missed twice (A3R2 and A4R2 "if missed twice"). Rung 3: dark slices after a pilot (change 12). Delete every "Proposal N" reference in the merged text (the base has the Q5 sentence "switch to Proposal 3" and its title "Proposal 1:"; retitle the merged document, for example "Unified branching proposal").
- **Risk**: Low.

### Change 16: Optional review-only story PR into the line (from Variant 3)
- **Source**: Variant 3 Q2 and A3R2 Q2.
- **Target**: Base Q2 (append "Optional layer") and sec 5 costs.
- **Rationale**: C-004, C-007, C-021, 60 to 72 percent; A-012 ACCEPT 96 percent (Augment and Codex reviewed PRs on the non-default base `346Claude-integration`: #484, #490, #491; CI did not run there). #490 (25 files, +4,636 lines) produced the fix PR #491 the same day (A3 E3).
- **Integration point**: Off by default. When the owner turns it on for stories above a threshold of about 15 files or 1,000 added lines (ESTIMATE from two data points, #484 and #490), the story branch is pushed, its worker session runs `/sc:pr-submit --monitor 3 --base release/dash<rel>` for review only, and the coordinator merges locally with `--no-ff` after pushing the line, so GitHub shows the PR as merged (UNVERIFIED, trial T6). Costs written into the text: no CI on those PRs; `/sc:pr-submit` reports CI as clean when no checks exist (INV-023: read "clean" as "no checks existed"); one top-level session per story; after story A merges locally, story B's open PR has a moved base and pr-submit handles that with one merge commit of the recorded base tip pushed fast-forward.
- **Risk**: Medium. Two UNVERIFIED behaviours; optional, so a failure removes only the layer.

### Change 17: One owner decision list at the end (from Variant 3)
- **Source**: Variant 3 sec 8 ("Open decisions"); U-012.
- **Target**: Base, new sec 10 (insert); sec 8 Sources moves to sec 11.
- **Rationale**: U-012, unanimous, 92 percent.
- **Integration point**: The eight decisions of the last section of this plan, same order, each with its recommended option and the consequence of each answer.
- **Risk**: Low.

### Change 18: Trials before first reliance (from Variant 3)
- **Source**: Variant 3 risk 5 ("check by opening one test pull request first"); U-013.
- **Target**: Base, new sec 9 (insert).
- **Rationale**: U-013, unanimous, 96 percent. Every UNVERIFIED behaviour in the plan points to one trial row.
- **Integration point**: The table "Trials before first reliance" of this plan, copied as sec 9.
- **Risk**: Low.

### Change 19: Sync branch `dash<rel>-sync<N>` as head of the `master` into `integration` PR (from Variant 3, role changed)
- **Source**: Variant 3 sec 2 ("Sync-from-integration branch"); U-011, "reserve only", 70 percent.
- **Target**: Base sec 2 table (new row), step 6 and Q8 (insert).
- **Rationale**: Gap found while checking names: base step 6 and Q8 say the coordinator "opens the `master` into `integration` sync pull request" but name no head branch. The head cannot be `integration`. A head of `master` is not ruled out by GitHub, but the owner rule is no commit on `master`, and a conflict between `master` and Clay's `integration` work needs somewhere to be resolved and committed. This differs from the base-selection recommendation (reserve only, for an `integration` merge-in that nobody now does); the reserve use stays, and the sync-PR use is added. This is the one place the plan departs from base-selection; flagged for the merge executor.
- **Integration point**: Name `dash<rel>-sync<N>`, cut from `origin/integration`, `master` merged in with a merge commit, pushed, `/sc:pr-submit --monitor 3 --base integration` in its own top-level session; the PR body says "Merge this pull request with a merge commit, not squash" (a squash would break the shared history; V2 Q4). A conflict stops the coordinator; a worker resolves it on this branch (CONTEXT line 9). Whether pr-submit accepts `master` as a head is UNVERIFIED and no longer needed.
- **Risk**: Medium. Departure from the base-selection wording; one more branch name.

### Change 20: A release with one story has no line (from Variant 3 and Variant 1)
- **Source**: Variant 3 Q6 ("no train branch for a batch of one"); Variant 1 Q6 already has it.
- **Target**: Base Q6 last sentence (replace "a plain `fix/` or `feat/` branch").
- **Rationale**: C-017 area; INV-016 ADDRESSED. The base name `fix/` or `feat/` breaks the ledger convention (CONTEXT line 14: ledger on the branch being executed) and the name globs.
- **Integration point**: The one story is `dash<rel>-s01-<slug>`, cut from `master`, ledger and `.dev/` records on it, one PR into `master` by `/sc:pr-submit --monitor 3 --base master`, merge commit, tag `dash-<rel>`. `fix/<issue>-<slug>` stays for shipped-code fixes that belong to no dashboard release. The rest of C-017 is change 27.
- **Risk**: Low.

### Part B: debate additions (changes 21 to 24)

These four pieces are not in any variant; the advocates wrote them in Round 2 and all four adopted them.

### Change 21: Forward-only push of the line after each story merge
- **Source**: A1R2 item 1; A4R2 point 8 (debate, no variant).
- **Target**: Base sec 1 sentence "Nothing is pushed for review until the release is complete" and sec 3 step 3 (replace).
- **Rationale**: Conceded in full by A1 (A3-W1, A4-W2): the base leaves one local copy of the release and the coordinator's disk is the only backup. Unanimous (A4R2 section 6 point 8).
- **Integration point**: Step 3 order becomes: path-claim check, `git merge-tree` trial, `--no-ff` merge, local gate (change 26, INV-007), ledger line, then `git push origin release/dash<rel>` (plain push, never `--force`; a rejected push is a stop). The push is a backup, not a review request: no PR is opened until the freeze. Pushing the line and the tag triggers no workflow (INV-002, VERIFIED-PROBE: only `test.yml` has a `push` trigger and it filters on `master` and `integration`). Red gate after the merge: do not push; the unpushed merge is reset to the tip hash the ledger recorded before the merge (local and unpublished, so allowed), the story goes back to its worker (INV-006).
- **Risk**: Low to Medium. The reset is a destructive local act; it is covered by the authority list in decision 1.

### Change 22: Revert the revert first
- **Source**: A1R2 item 3; scratch run in the debate (direct re-merge after `git revert -m 1` stops with `DU s.txt`; reverting the revert first, then merging the fixed branch, is clean); C-005 trap, C-022.
- **Target**: Base Q9 (replace the second bullet's "UNVERIFIED" sentence) and sec 7 risk 5 (replace).
- **Rationale**: The base called it "unverified general git behaviour"; a procedure was missing, not a structure (A1R2 item 3). Unanimous (A4R2 point 10).
- **Integration point**: "To bring back a story or a release that was reverted: first revert the revert commit, then merge the fixed branch. Never merge the old branch directly." Remove risk 5 from sec 7 and put the procedure in Q9.
- **Risk**: Low.

### Change 23: "Merge commit, not squash" sentence plus a two-parent closeout check
- **Source**: A-006 ACCEPT 96 percent (all three merge methods are allowed; nothing technical stops a wrong click; precedent #658 squashed by mistake, reverted by #662, redone as #664); A4 M4 (the closeout script `branch-landed.sh` asserts no merge method).
- **Target**: Base Q4 (insert).
- **Rationale**: INV-009 (MEDIUM). The last 12 merged PRs into `master` all landed as single-parent commits, so the owner's normal click is the wrong one for a release (VERIFIED-PROBE). Q9's story-level revert (`-m 1`) and first-parent bisect need the merge commits to survive.
- **Integration point**: First line of the release PR body and of the sync PR body: "Merge this pull request with a merge commit, not squash." Closeout check (new work, not built; filed as a follow-up outside this proposal): read `mergeCommit` from `gh pr view <n> --json mergeCommit`, then `git cat-file -p <sha>` must show two `parent` lines. The check is detective only. If the wrong method was used: revert PR through pr-submit, redo (the #658 to #662 to #664 path). Repository setting changes are rejected (decision 8).
- **Risk**: Medium. The control is a sentence plus a check that does not exist yet.

### Change 24: First-parent bisect over `--no-ff` story merges
- **Source**: A4 M5 (scratch repository: `git bisect --first-parent` over six story merges names the bad one, "merge s4"; first-parent log 7 entries against 26).
- **Target**: Base Q9 (append).
- **Rationale**: Supports `--no-ff` as the default (C-005, unresolved 50 percent) and gives story-level granularity without squash. Git 2.47.3 here accepts `git bisect start --first-parent` (VERIFIED-HERE).
- **Integration point**: One sentence in Q9: "`git bisect start --first-parent` on the line or on `master` names the story merge that introduced a regression."
- **Risk**: Low.

### Part C: answers the merge must carry (changes 25 to 30)

### Change 25: Size budget, records rule, tooling fallback and over-budget action (answers INV-017, HIGH; also INV-011 and INV-025)
- **Source**: `invariant-probe.md` INV-017, INV-011, INV-025; base-selection item 25. No variant has it. The probe lists no fix and names two options (keep `.dev/` records out of the release PR, or cap files as well as stories); this change takes both and adds the rest.
- **Target**: Base Q4 (insert a pointer and the evidence from change 5), sec 3 steps 3 and 5 (insert the measurement and the stop rules), Q7 `.dev/` bullet (replace), sec 5 and sec 7 (cost and risk 1, update), and the new sec 8.
- **Rationale**: The failure is real and measured. On the 2,089-file PR #31, `gh pr diff` fails with "HTTP 406: the diff exceeded the maximum number of files (300)", `gh pr view --json files` returns 100 files, and `gh api repos/.../pulls/31/files` pages work (page 21 returned 89 files) (VERIFIED-PROBE). The `/sc:auggie-review` skill, whose rubric `/sc:pr-submit` reuses, calls `gh pr view --json files` and `gh pr diff` (probe, skill lines 30, 97, 127). Record-only PRs already sit at the limit: #728 changes 453 files and #730 changes 292 files (VERIFIED-PROBE), so `.dev/` records alone can pass 300 while the base's size control counts stories. Because no human approves plans (owner decision of 2026-11-23, change 29) and the panels and per-task QA are AI reviewers, the release PR is the first place a human reads the result, so this control carries more weight, not less.

**(a) Numbers. Every number is a default the owner may change (decision 2), except the three tool limits, which belong to GitHub.**

| Number | Default | Basis | Mark |
|--------|---------|-------|------|
| `gh pr diff` file limit | 300 files | #31: HTTP 406 above 300 | VERIFIED-PROBE; fixed by the tool |
| `gh pr view --json files` | first 100 files only | #31 returned 100 | VERIFIED-PROBE; fixed by the tool |
| `gh api .../pulls/<n>/files` | 100 per page, at most 3,000 files per PR | GitHub REST documentation fetched 2026-11-23 ("Responses include a maximum of 3000 files"; "max 100" per page); paging worked on #31 | VERIFIED-HERE (docs), VERIFIED-PROBE (paging) |
| Release-PR file budget | 250 files, counted over all paths including `.dev/` | 50 files of headroom under the 300 limit | GUESS (the 300 it sits under is VERIFIED) |
| Stop-adding threshold | 200 files (80 percent of the budget) | headroom for the story in flight | GUESS |
| Story cap | 6 stories | median `master` PR is 37 files, p90 is 334 (A2 N1); 6 x 37 = 222 fits 250, but one p90 story alone does not | ESTIMATE; the file budget, not the story cap, is the binding control |
| Time box | 7 days from the cut | DORA one-week batch limit (S6) extrapolated; base Q4 already says it is not a DORA figure for release branches | ESTIMATE |
| Review-only story PR threshold | about 15 files or 1,000 added lines | #484 (8 files, +217) against #490 (25 files, +4,636, needed fix PR #491) | ESTIMATE from two points |
| Hard stop | 300 files | the `gh pr diff` limit | VERIFIED-PROBE |

What the budget does not prove: that a PR under 250 files is read well. In-repo evidence for "reviewable" is merge speed (#640: 1,146 files, 43 minutes, one Augment review and one Codex comment), which is not review depth (INV-025; depth UNVERIFIED, trial T10). The budget is set by what the tools can read, and it is a ceiling, not a promise of review quality.

**(b) Where `.dev/` records go (rule).**
1. The ledger (`sprint-status.yaml`) and the planning set stay on the release line and land with it, as CONTEXT lines 13 and 14 require. They are never moved out.
2. Every other `.dev/` record (story report folders, panel outputs, QA files) is committed on the story branch, reaches the line at the story merge, and may leave the release PR through a records PR (below).
3. At freeze the coordinator counts: `git diff --name-only origin/master...release/dash<rel> | wc -l`, and the part under `.dev/`. If the total is 250 or less, no records PR: the release PR carries everything. If it is more than 250, the records PR goes first.
4. Records PR mechanics. The coordinator creates `dash<rel>-records` from `origin/master` (`orca worktree create --name dash<rel>-records --branch dash<rel>-records --base-branch origin/master --agent claude`), runs `git checkout release/dash<rel> -- <record paths>` for every `.dev/` path except the ledger and the planning set, commits, and a top-level session runs `/sc:pr-submit --monitor 3 --base master`. The owner merges it (any method; it is record-only, precedent #728 and #730). Then the coordinator merges `master` into the line and recounts.
5. The mechanism is checked: in a scratch repository (VERIFIED-HERE), a line with 400 record files, one code file and a ledger file, after a records branch carrying the 400 files was merged into `master` and `master` was merged into the line, gave `git diff --name-only master...line` of 2 files (the code file and the ledger), 0 of them under the records path. The merge was clean (identical files on both sides).
6. Edge found in the same scratch work (VERIFIED-HERE): if a record file already carried by the records PR is edited again on the line afterwards, the merge of `master` into the line conflicts in that file. Rule: from the moment the records branch is cut until `master` has been merged back in, the coordinator does not edit those record paths on the line; a late record goes into a new file (or into the ledger). Late new files ride the release PR.
7. Expected frequency: most feature releases will trigger it (one record set was 453 files, #728; ESTIMATE). If the rule triggers three releases in a row, the owner may make the records PR the default for feature releases.
8. Cost: one more PR through pr-submit, one more owner click, one more CI run (CI runs for PRs into `master`), an ordering dependency (records merge before the release PR). The records PR can itself exceed 300 files (#728 had 453): the tooling fallback below applies, and the owner reviews it by path class.

**(c) Review-tooling fallback (rule, in the release brief).**

| Need | Do not use above the limit | Use |
|------|---------------------------|-----|
| Count the files | `gh pr view --json files` (first 100 only) | `git diff --name-only origin/master...<head> \| wc -l` locally, or `gh pr view <n> --json changedFiles` |
| List the files | `gh pr view --json files` | `gh api repos/IronbellyOrg/IronClaude/pulls/<n>/files --paginate` (100 per page, 3,000 files at most) |
| Read the diff | `gh pr diff <n>` (fails above 300 files) | local `git diff origin/master...<head>`, or the `patch` field of the paged API |
| Tell a human what is in it | a file list | path classes and the per-story digest in the PR body (ledger lines plus `git log --merges`; U-002, A-009) |

The `/sc:auggie-review` skill and pr-submit's own reads of a PR are not changed by this proposal. Whether pr-submit survives a release PR above 300 files is UNVERIFIED (trial T4). Follow-up work, outside this proposal: an issue for the auggie-review rubric to page the file list.

**(d) What the coordinator does when a release would exceed the budget.** Before every story merge the coordinator predicts the count with `git diff --name-only release/dash<rel>...<story> | wc -l` added to the line's current count, and writes both to the ledger line. Then:

| State | Action |
|-------|--------|
| Predicted total 200 or less | Merge as usual. |
| 201 to 250 | Merge; no new story starts; stories in flight finish (floating scope, change 14). |
| Above 250, records not yet split out | Apply rule (b) first (a records PR may be cut early, before freeze), recount. |
| Still above 250 and this story is not yet merged | The story does not merge. Default: it is carried to the next release (change 14). If it is the release's reason for being, the coordinator asks the owner in chat; the other choice is a planning change that splits the story into two. |
| Still above 250 and everything is merged (one story or late records pushed it over) | Land the release in two PRs. Pick a story-merge commit M_k from the ledger (every merge commit passed the local gate, so each is a green state). `git branch release/dash<rel>-p1 <M_k>`, push it, open PR 1 `release/dash<rel>-p1` into `master` through pr-submit, owner merges (merge commit). Merge `master` into the line. Open PR 2 `release/dash<rel>` into `master`; it carries only the stories after M_k. Tag `dash-<rel>` after PR 2 only. |
| Above 300 and no split is possible | Open no PR. The coordinator stops and asks the owner in chat; the owner may accept the tooling fallback in chat. |

The two-PR landing costs a second owner click, CI and both bots twice, and leaves half a release on `master` between PR 1 and PR 2; the coordinator picks M_k at a story group that is usable alone, and the owner may refuse the split. The split rests on git behaviour (any merge commit of the line is a valid head) and on each M_k having passed the gate; the GitHub side is UNVERIFIED (trial T7).
- **Integration point**: New sec 8 carries (a) to (d) as written above (numbers table, records rule, fallback table, over-budget table). Q4 gets two sentences and a pointer. Step 3 gets the "predict and write to the ledger" line. Step 5 gets the freeze count. Sec 7 risk 1 is updated: "release PR too large to read" is now bounded by a number.
- **Risk**: High. New design with no precedent in any variant; four moving parts; two of them (records PR, two-PR landing) cost an extra owner click. The git side is verified here; the GitHub side and the bot behaviour are not. Rollback: remove sec 8 and revert to the base's story-count cap, which leaves INV-017 open.

### Change 26: Ten MEDIUM invariants, one outcome each
- **Source**: `invariant-probe.md` INV-003, 005, 006, 007, 008, 009, 011, 019, 025, 026; base-selection item 26.
- **Target**: Base sec 3 steps 3 to 5, Q2, Q4, Q7, Q9 and sec 7 (insert one rule per row); the owner-facing outcomes go to sec 9 and sec 10.
- **Rationale**: Each is UNADDRESSED, MEDIUM in the probe, with verified evidence there. Outcome classes: RULE (text the merge adds), OWNER DECISION (the merge asks), TRIAL (a check before first reliance).
- **Integration point**: One row per finding.

| INV | Outcome | What the merged text says |
|-----|---------|---------------------------|
| INV-003 owner latency while the release PR waits | RULE + TRIAL T11 | One open line at a time. While the PR waits, the coordinator does only: monitor and `-fix` handling (change 2), sync-branch preparation (change 19), clean-up prep. No line for release n+1 is cut and planning of n+1 starts only after n merges (CONTEXT line 14). The ledger records PR-opened and PR-merged times for the first two releases. If the wait exceeds one working day (GUESS) in both, the owner decides whether n+1 may be cut from n's tip; it is mechanically cheap because n lands by merge commit (scratch, VERIFIED-HERE: n+1 cut from n's tip; after n landed with a merge commit and `master` was merged in, `git diff --name-only master...n+1` listed only n+1's own file). |
| INV-005 head must stay fixed while `--monitor 3` runs; coordinator shares the release worktree | RULE + TRIAL T3 | Monitor window: from the start of `/sc:pr-submit --monitor 3` until it reports its final state, the release worktree has one writer, pr-submit. The coordinator does no merge, commit, push or branch switch there. A `-fix` waits (ledger: "queued") and enters after the monitor ends; it then starts a new pr-submit run on the new head, because a hand push gets CI but no bot re-review (pr-submit Wave 6: only pr-submit posts the re-trigger comments, probe INV-005). Before starting, `git status` in the worktree is clean with no merge or revert open, or pr-submit halts with `foreign_op_in_progress`. A moved head halts it with `pr_head_mismatch` (both VERIFIED-PROBE from the SKILL text). |
| INV-006 nothing stops a merge into a stale or red line | RULE | Order per story: path-claim check, `git merge-tree` trial (textual clashes only; A-005 QUALIFY), merge, local gate, ledger line, push only if green; red means no push and reset to the ledger's tip hash (change 21). Story N+1 does not merge until story N's gate result is in the ledger. A story that touches the same shared or risky files as a story whose dispatch run is still open waits for that run (GUESS rule). `master` is unprotected and rulesets are empty (VERIFIED-PROBE), so these are rules of the coordinator, not enforcement. |
| INV-007 local tests are not the CI gate | RULE + OWNER DECISION 1 + TRIAL T9 | Define the local gate as the CI list. At release start the coordinator reads `git show origin/master:.github/workflows/test.yml` and copies the exact commands of the `lint` job (the probe lists `ruff check`, `ruff format --check`, `make verify-deps`, `make sync-dev`, `make verify-sync`, `make lint-architecture`) and of the `test` job (`make sync-dev` first, because the `.claude/` mirrors are gitignored) into the first ledger entry (the release brief). The worker contract lets the coordinator run `make sync-dev` or other Makefile targets only when the user's instruction names the step (probe, contract line 234); the brief is that instruction, and decision 1 asks the owner to confirm it. Evidence for the gap: 9 of the last 40 `test.yml` PR runs failed (22.5 percent) and all 6 failed runs opened failed in the lint job (VERIFIED-PROBE). Local run time is unmeasured (A-010): T9. |
| INV-008 Contract #3 heading | RULE | The brief lists the PR-only workflows read from `origin/master` at release start (`test.yml`, `boundary-guard.yml`, `contract3-generator-constraint-lint.yml`). Before opening the PR the coordinator runs `git diff --name-only origin/master...release/dash<rel>` and, if it matches `**/gates.py`, `**/structural_checkers.py` or `**/*_validator.py`, puts `## Generator-Constraint Considered` into the PR body (the workflow also re-runs on `edited`). A dispatch run cannot show this check green (INV-026). |
| INV-009 merge method enforced by a sentence | RULE + OWNER DECISION 8 | Change 23: the sentence in the PR body, the two-parent closeout check (new work), the revert-and-redo recovery. No repository setting change is proposed. |
| INV-011 story cap does not bound file count | RULE | Change 25: file budget counted over all paths; `.dev/` counted. |
| INV-019 identical edits merge cleanly into a wrong value | RULE | Change 13 widens the shared-file list to pinned-count tests and the dependency baseline. The post-merge gate is the full local suite, never a targeted subset: the base says "full local test suite" and this plan rejects V4's "targeted tests" wording (A4R2 Q2). A story that adds a counted item (command, skill, registered entry) names the pinned count in its path claim; two stories that touch the same pinned count are serialised or one owns the count. Detection is the full suite failing, VERIFIED-PROBE (the scratch merge exits 0 with the wrong value; only a test that pins the true count notices). |
| INV-025 no cap number | RULE + OWNER DECISION 2 + TRIAL T10 | Change 25 gives numbers with marks; the owner sets them; bot review depth against PR size is observed in the first release (T10). |
| INV-026 dispatch run is not the PR run | RULE | Final-tip checklist (change 6): green dispatch is necessary, not sufficient. Merge `master` in right before the PR so the PR run tests a merge ref close to the tip (a PR run tests the merge of head and current `master`; `master` moves about 8 PRs a day: INV-012, VERIFIED-PROBE). The PR run is the gate: the owner merges only when `test.yml`, `boundary-guard` and the Contract #3 check are green and both bots have settled. Each pr-submit fix push starts a new PR run (pr-submit allows `max_rounds + 1` pushes, default 2, hard cap 5: probe), so the final state is read after the last push. |

- **Risk**: Medium. Ten rules, three of which (INV-007, INV-009, INV-026) lean on tools or checks that need confirmation. The two with the least evidence are INV-003 (the one-day figure is a GUESS) and INV-006's wait-for-dispatch rule (a GUESS).

### Change 27: Hotfix and special-release handling (answers C-017; decided versus the owner's call)
- **Source**: C-017 (unresolved, 50 percent): A1 and A4 keep 1.1 and 1.105 as ordinary release lines with a one-story skip (A4 asks the owner about test-only); A2 and A3 propose no line for bug-fix and test-only releases (two lanes: small direct PRs into `master`). Base-selection recommendation: V1 and V4's position as the default, owner call for 1.105 only.
- **Target**: Base Q6 (replace the last bullet; insert two bullets).
- **Rationale**: A2 and A3 reached the two-lane view from designs that lost the base question (C-002, C-003). Many direct PRs add owner clicks (A-003: about 5.7 merged PRs a day already). One rule set keeps the ledger convention (C-020: CONTEXT line 14 needs a branch to hold the ledger). A one-story release already skips the line (change 20), so the cost of a line is low exactly when the release is small.
- **Integration point**: Decided in the merged text:
  1. Every dashboard release number, including 1.1 (bug-fix) and 1.105 (test-only), is an ordinary release: line `release/dash1.1`, `release/dash1.105`, story branches `dash1.1-s01-<slug>`, ledger on the line, one PR into `master`, merge commit, tag `dash-1.1`.
  2. A release with exactly one story has no line (change 20).
  3. A bug in shipped code found while a line is open: `fix/<issue>-<slug>` from `master`, PR into `master` through pr-submit, picked up by the next merge-in of `master` into the line. No cherry-pick, no back-port step (C-015, unanimous, 93 percent). A fix that clashes in meaning with dashboard code stops the coordinator at the merge-in; a worker resolves it.
  4. A bug in a story already merged into the line: `dash<rel>-fix<NN>-<slug>` from the line tip, merged locally; after freeze these are the only branches that enter (change 2).
  5. Name hazard: `dash1.1` is a prefix of `dash1.105`; a glob `release/dash1.1*` matched both in a scratch repository (VERIFIED-HERE). Use the exact name or a hyphen-terminated glob (`*dash1.1-*`), and write a future 1.10 as 1.100.
  Left to the owner (decision 7): whether a test-only release of several stories (1.105) may skip the line. Recommended answer: no. Consequence of yes: every test-only story is its own PR into `master` with its own CI, bots and owner click, the ledger has no home for that release, and the coordinator runs a second rule set.
- **Risk**: Low. The default follows the base; the owner's call is narrow.

### Change 28: The ref-name rule and the Orca `--branch` check (answers part d)
- **Source**: CONTEXT lines 8, 12; base sec 2; C-001; A-007, A-011; INV-018, INV-022.
- **Target**: Base sec 2 (replace the table and the invariant paragraph; the base's creation command is replaced).
- **Rationale**: One table, one invariant, one creation command, and a list of what is checked and what is not.
- **Integration point**:

| Kind | Pattern | Example |
|------|---------|---------|
| Release line | `release/dash<rel>` | `release/dash1.3`, `release/dash1.105` |
| Story | `dash<rel>-s<NN>-<slug>` | `dash1.3-s04-token-usage-panel` |
| Fix inside a release | `dash<rel>-fix<NN>-<slug>` | `dash1.3-fix01-empty-state` |
| Sync PR head (change 19) | `dash<rel>-sync<N>` | `dash1.3-sync1` |
| Records PR head (change 25, only when triggered) | `dash<rel>-records` | `dash1.3-records` |
| First half of a two-PR landing (change 25, only when triggered) | `release/dash<rel>-p1` | `release/dash1.3-p1` |
| One-story release (change 20) | `dash<rel>-s01-<slug>` | `dash1.105-s01-add-widget-tests` |
| Shipped-code fix | `fix/<issue>-<slug>` | `fix/731-ledger-path` |
| Marker after landing (a tag, not a branch) | `dash-<rel>` | `dash-1.3` |

Invariants: (1) a branch name is never the folder part of another; the only folders are `release/` and `fix/`, and no branch is named `release` or `fix`; (2) the bare token `dash<rel>` and the tag name `dash-<rel>` are never branch names; (3) release tokens are matched exactly or with a hyphen-terminated glob (`*dash1.1-*`); (4) the worktree name equals the branch leaf (the line's worktree is `dash1.3-release`); (5) after creation the coordinator reads the real name (`git -C <worktree> branch --show-current`) and writes it in the ledger.

Pre-create check: `git check-ref-format --branch <name>` succeeds, `git for-each-ref refs/heads/<name> 'refs/heads/<name>/*'` prints nothing, and for names under `release/` or `fix/` `git rev-parse --verify -q refs/heads/release` (or `fix`) fails.

Creation (replaces the base command, which omits `--name`; the CLI usage line requires it: VERIFIED-HERE):
`orca worktree create --name dash1.3-release --branch release/dash1.3 --base-branch origin/master --agent claude`
`orca worktree create --name dash1.3-s04-token-usage-panel --branch dash1.3-s04-token-usage-panel --base-branch release/dash1.3 --parent-worktree <release worktree selector> --agent claude`

What is verified and what is not:
- VERIFIED-HERE: `orca worktree create --help` prints `--branch <name>  Git branch name to use instead of the prefixed default`, so `--branch` replaces the `ironbelly/` prefix; the usage line requires `--name`. Tag `dash-1.3` coexists with `release/dash1.3`, `release/dash1.105`, `release/dash1.1` and `dash1.3-s04-x` in a scratch repository.
- VERIFIED-PROBE: `git check-ref-format --branch` accepts `release/dash1.3`, `release/dash1.105`, `dash1.3-s04-slug`, `dash1.3-fix01-slug`, `dash-1.3` and `ironbelly/release/dash1.3`; no remote head matches `release/*` or `dash*`.
- UNVERIFIED, trial T1: that `--branch` keeps the exact name in a real run; that "a taken name gets a numeric suffix" (A4 M1, from the CLI help as the advocate read it, not seen by me); what a ref-conflicting name does.
- UNVERIFIED, trial T2: that `worker-start --worktree path:<coordinator-created worktree>` adopts an exact-name worktree (INV-022; CONTEXT line 12 says `worker-start` has no `--branch`).
- UNVERIFIED, trial T8 (low priority): how Orca, pr-submit and the closeout script treat a tag next to similar branch names; the git side is VERIFIED-HERE.
- UNVERIFIED, trial T12 (only for rung 3): whether stacked pull requests and a merge queue are available on this repository's plan. The design does not use either. What replaces stacking, VERIFIED-HERE in a scratch repository: line n+1 cut from line n's tip, n landed with a merge commit, `master` merged into n+1: `git diff --name-only master...n+1` lists only n+1's own file.
- UNVERIFIED, trials T3, T4, T6: how pr-submit and the two bots behave on the release PR with the draft guard (M10), on a PR above 300 files, and on a PR whose base is not `master`. Bots reviewed PRs on the non-default base `346Claude-integration` and CI did not run there (VERIFIED-PROBE, A3 E2 and A4 M8); the rest is not seen.
- **Risk**: Medium. The rule is simple and the facts behind it are checked at the git level; the Orca behaviour is checked at the help-text level only.

### Change 29: Fit with the owner's decisions of 2026-11-23, and the `test.yml` question
- **Source**: the owner's decisions as stated in the team lead's brief; CONTEXT lines 7, 9, 10, 11, 14.
- **Target**: Base sec 1 (insert a short "How this fits" list) and sec 10 (decisions 1 and 6).
- **Rationale**: Each decision must be visible in the merged text as kept, or disclosed as changed.
- **Integration point**:

| Owner decision | How the merged proposal fits | Departure or cost |
|----------------|-----------------------------|-------------------|
| Dashboard releases are integration branches merged to `master` when done | The release line `release/dash<rel>` is that branch; it lands in one PR into `master` by a merge commit; then the next release is cut from `master`. | The line is not called `integration` because the repository already has a branch of that name (change 1 glossary sentence). |
| Stories are sub-branches | Each story is cut from the line and merged back; the link is kept by the Orca parent worktree, the `dash<rel>-` name prefix and the ledger. | Not a folder under the line's name: flat names (change 10); the owner's literal `dash1.3/story1` cannot coexist with `dash1.3`, and the folder form under `release/` is avoided as insurance. |
| No human plan approval; a panel verdict instead | The story pipeline (spec panel, plan, plan review panel, implement, per-task QA) gates on the panel verdict, which the coordinator writes into the ledger line; the coordinator merges a story when the verdicts are PASS, the path claims are disjoint, `git merge-tree` is clean and the local gate is green. | No human sees a story before the release PR. That makes the size budget (change 25) and the bots the only readers; the optional review-only story PR (change 16) exists for this. Humans still decide three things once: local-merge authority, the numbers, and each release PR merge. |
| Two stories in parallel for the first release | Path claims must be disjoint; merges are serial; re-open the design above about four parallel stories (A-004 QUALIFY, 65 percent). | Shared files and pinned counts (change 13) are where two "disjoint" stories collide anyway. |
| Clay's habit of branching from `integration` | Unchanged while a release is built; `integration` is never merged into the line (X-003, 97 percent); `git merge-tree` against `origin/integration` and the path-claim comparison with open `integration` PRs are early warnings (U-001, U-003). After landing, the sync PR (change 19). | Clay's real landing branch is `master` (10 of the last 30 `master` commits are his: VERIFIED-PROBE), so the collisions that matter arrive through the merge-in of `master` (INV-021). `master` is 26 commits ahead of `integration` and `integration` has had no merged PR since 2026-11-19 (VERIFIED-PROBE): decision 5 asks whether it is still in use. |
| PRs only through `/sc:pr-submit --monitor 3`, in its own top-level session | Every PR in the design goes that way: the release PR, the records PR, the sync PR, a revert PR, a two-PR landing, an optional review-only story PR. Each is a separate top-level session in the worktree of its head branch. | About three to four pr-submit sessions per release (records, release, sync, plus any revert), each with an owner click; the coordinator never opens a PR any other way. |
| CI runs only for PRs into `master` and `integration` | The release PR, the records PR and a revert PR get CI. Story merges are local, so they get none; the gap is covered by the local gate and by `workflow_dispatch` (change 11). | See below. |

**The one-line workflow change.** Question: should the proposal ask the owner to add `release/**` to the `pull_request` branch filter of `test.yml` so review-only story PRs get CI? Recommendation: not for the first release; decide after trial T6. Cost of saying yes:
1. A change to `.github/workflows/test.yml`, which also needs the edited file to be the version GitHub reads for a `pull_request` run; where GitHub reads it is UNVERIFIED (A-008; two secondary sources say the merge commit), so the edit may have to be the first commit on the line before any story PR is opened (A3R2 route a), and works only for PRs opened afterwards.
2. CI minutes: median 9.2 minutes per run (A4 M3). With one to three runs per review-only story PR (GUESS: one on open, one per pr-submit fix push) and six stories, about 55 to 165 minutes per release (ESTIMATE; arithmetic on a guess).
3. A wrong pattern leaves story PRs with no CI while everyone assumes they have it (V3 risk 5): if Orca prefixes a branch, `release/**` does not match `ironbelly/release/dash1.3`, so the pattern must be checked against the real branch name (T1).
4. The edit rides in the release PR and changes `test.yml` on `master` permanently.
Cost of saying no: story PRs, if used at all, get bots and no CI; the outside gate is `workflow_dispatch` (change 11), which needs no edit and has precedent (A4 M2). Recommended: no edit in release 1; owner decision 6 asks for dispatch minutes, the review-only layer and the edit together.
- **Risk**: Low. The table restates decisions already taken; the workflow question is an owner decision, not a change to the text.

### Change 30: Seven LOW unaddressed invariants and eight addressed ones
- **Source**: `invariant-probe.md` INV-001, 004, 010, 014, 015, 021, 023 (LOW, UNADDRESSED); INV-002, 012, 013, 016, 018, 020, 022, 024 (ADDRESSED).
- **Target**: Base Q7, Q3, Q6, Q8 and sec 7 (one sentence each).
- **Rationale**: Cheap to close now; leaving them makes the next probe re-find them.
- **Integration point**:

| INV | Outcome | Text |
|-----|---------|------|
| INV-001 one fixed ledger path | RULE | At every line cut the coordinator replaces the contents of `sprint-status.yaml` with the new release's header (release id, `master` tip at the cut). The previous release's final ledger stays in `master` history and under its tag. The first landing creates the file on `master` (VERIFIED-PROBE: absent today). |
| INV-004 do story records reach the story branch | RULE + TRIAL T2 | The worker commits its `.dev/` records on the story branch before reporting done; before merging and before `orca worktree rm` the coordinator checks `git status --short` in the story worktree is empty. Whether child-report directories reach the branch is UNVERIFIED (probe; worker contract lines 236 to 238). |
| INV-010 rebase before PR versus merge | OWNER DECISION 1 (part e) | The line is a published branch after its first push, so CLAUDE.md Pre-PR check 2 (rebase onto `origin/master` before pushing) is replaced for this PR by a merge of `master`, as `/sc:pr-submit` never rewrites a published head. The memory rule already limits rebase to unpublished commits; the owner confirms the exception once. |
| INV-014 branch sprawl | RULE | Change 4 sweep; 170 remote heads today. |
| INV-015 a line with zero merged stories at the time box | RULE | No PR is opened; the line and its worktree are deleted (change 4); the release number is reused at the next cut; the ledger notes "closed empty". The pre-PR failure "No commits between master and branch" is the signal. |
| INV-021 early warning watches `integration`, Clay lands on `master` | OWNER DECISION 5 | Keep the cheap `integration` checks; the merge-in of `master` is the check that matters; decision 5 asks whether `integration` is still in use. |
| INV-023 pr-submit reports CI "clean" with no checks | RULE | Change 16 text: read "clean" on a review-only story PR as "no checks existed"; no CI claim is made for story PRs. |
| INV-002, 012, 013, 016, 018, 020, 022, 024 | ADDRESSED, no change | Carried as stated in the probe: push and tag trigger no workflow; merge-in work for a 7-day line (about 8 `master` PRs a day) is covered; PR volume stays inside the demonstrated peak (26 and 23 merged PRs a day); one-story release skip; token sorting and ref-format checks; a hotfix on `master` is picked up by the merge-in; flat names remove the Orca prefix clash; `worktree_cleanup.py` fails closed. |
- **Risk**: Low. One sentence per row.

## Base weaknesses and who fixes them

| # | Base weakness (where in V1) | Better variant | Fix approach | Change |
|---|-----------------------------|----------------|--------------|--------|
| W1 | Names `dash1.3/release` and `dash1.3/s04-slug`: Orca prefixes a branch `ironbelly/<worktree name>` unless `--branch` is given, and V1 itself rates the prefix UNVERIFIED (sec 2, risk 4) | V4 (`release/` folder), V2 and V3 (flat stories) | `release/dash<rel>` plus flat `dash<rel>-s<NN>-<slug>`; one invariant; read back the real name | 1, 10, 28 |
| W2 | "Nothing is pushed for review until the release is complete" leaves one local copy (sec 1) | none; A1R2 item 1 (debate) | Forward-only push after each merge, as a backup | 21 |
| W3 | No freeze rule | V4 (rule 6) | Freeze after the last planned story; only `-fix` branches | 2 |
| W4 | Revert-then-redo called "unverified general git behaviour" (risk 5, Q9) | none; A1R2 item 3 (debate) | Revert the revert first, then merge | 22 |
| W5 | No outside gate per story; one big review at the end (sec 5, risks 1 and 6) | V2 (dispatch CI), V3 (review-only story PR) | Dispatch run by default; optional review-only PR; cap, digest, time box | 11, 14, 16, 25 |
| W6 | The long-lived line is justified only by Driessen and Fowler (Q5) | V3 (time box) | "The scope floats, the time does not" | 14, 15 |
| W7 | The wrong merge click is possible, and the "closeout checks the merge method" idea does not exist (`branch-landed.sh` asserts no method) | none; A-006, A4 M4 (debate) | PR-body sentence, two-parent check (new work), revert-and-redo recovery | 23 |
| W8 | Size control counts stories, not files; `.dev/` records ride the PR; `gh pr diff` fails above 300 files and `gh pr view --json files` shows 100 (INV-017, INV-011) | no variant | File budget, records PR, paged-API fallback, over-budget table | 25 |
| W9 | Step 6 and Q8 open a `master` into `integration` sync PR with no head branch | V3 (`dash<rel>-sync<N>`) | Name the head; merge-commit sentence in its body | 19 |
| W10 | The creation command omits `--name`, which the CLI usage line requires | none; found by `orca worktree create --help` | Corrected command in change 28 | 28 |
| W11 | The text refers to another document: "switch to Proposal 3" in Q5 (and the title "Proposal 1:"); the merged text must stand alone | none | Replace by the ladder; retitle the document | 15 |
| W12 | Local tests after a merge are not the CI gate (INV-007) | none | Local gate defined as the CI list, named in the release brief | 26 |
| W13 | A one-story release is a plain `fix/` or `feat/` branch, which breaks the ledger convention and the globs | V3, V1 Q6 | Story pattern `dash<rel>-s01-<slug>` | 20 |
| W14 | Only sort caution is "a future 1.10 would sort wrongly"; `dash1.1` is a prefix of `dash1.105` (INV-018) | A4R2 ("write 1.100") | Exact or hyphen-terminated globs; scratch-verified over-match | 27, 28 |

## Changes NOT Being Made (with rationale)

Every omitted requirement-level anchor of a non-base variant is listed with its type, source and the debate evidence. Anchors that are carried (possibly changed) are in the changes above and in "Threshold preservation".

| # | Source variant and section | Anchor type | Anchor | Why the base wins or the anchor is deferred | Debate evidence |
|---|----------------------------|-------------|--------|---------------------------------------------|-----------------|
| R1 | V4, rule 2 | mechanism | Pull request per story from the story branch into `release/dash1.3` | A4 dropped it: the later CI statement contradicts it (X-008) and a PR into a release branch gets no CI under the filter | C-004 72 percent; X-008 85 percent resolved; A4-C1 |
| R2 | V4, rule 3 and Q8 | mechanism | `integration` merged into `release/dash1.3` before the release PR | Puts Clay's unreleased commits in the PR to `master`; scratch test `git diff --stat master...release/dash1.3` listed the `integration` commit's file | X-003 97 percent; A-017 REJECT 97 percent; C-018 96 percent |
| R3 | V4, rule 2 | rule | Squash merge of a story into the line as the default | Not rejected for good: deferred to decision 4. The base default stays `--no-ff` (revert-the-revert remedy verified, first-parent bisect verified, review-only PR needs a merge commit) | C-005, X-004 split 50 percent |
| R4 | V4, rule 2 | rule | Rebase inside a story branch; rebase "to stay current" | Clashes with `/sc:pr-submit` never rewriting a published branch; merge only after the first push | C-009, X-007 82 percent |
| R5 | V4, rule 6 | mechanism | Urgent fix copied into every open release branch by cherry-pick or merge | Merge-in of `master` covers it; cherry-pick duplicates can conflict later | C-015 93 percent; A2 N7 |
| R6 | V4, rule 1 | name | Three-level story name `dash1.3/story/01-widget-grid`, kinds `story`, `bugfix`, `docs`, prefix `hotfix/` | Folders can block with the Orca prefix (A4 M1); flat names group by a glob | C-001 72 percent; U-016 Drop 55 percent |
| R7 | V4, rule 4 | gate | "Tier 1 + Tier 2 + Tier 3" tests, two approvals, UAT sign-off | No counterpart in this repository; reduced gate kept (change 6) | U-018 58 percent; A4-C9 |
| R8 | V4, rule 4 | evidence | GFxAI pedigree as precedent | A4 asks for no weight; kept only as size evidence (change 5) | U-015 72 percent |
| R9 | V4, rule 6 | mechanism | Tech-Lead emergency override | No counterpart here; the source gives no rule either (UNSPECIFIED) | L4 in base-selection |
| R10 | V2, sec 1, 3 | mechanism | `integration` as the trunk and as the base of every slice | `integration` is 26 commits behind `master`, no merged PR since 2026-11-19, none of the owner's 130 recent PRs used it | C-002 95 percent; X-001 95 percent; A2 N1 |
| R11 | V2, Q2, Q5 | mechanism | Slice PRs into `integration` with an owner click each; squash; dark landing and flags as the base design | Heaviest owner load; dark landing unproven here; flags kept as the third rung after a pilot | C-012 85 percent; U-007 to U-009 fallback 60 percent |
| R12 | V2, Q2 (A2R2) | mechanism | A hand-opened draft release PR to get CI on each push | pr-submit has no open-as-draft flag, the owner rule is PRs only through pr-submit, draft behaviour of the bots is unverified | A4R2 section 3, M10 |
| R13 | V2 (A2R2 Q5) | rule | Two lanes: no line for 1.1 and 1.105 | Default rejected; the one open piece (multi-story 1.105) is decision 7 | C-017 50 percent split; A-003 |
| R14 | V2, sec 2 | name | Second PR suffix `-p<N>`; tag `dash/<rel>` | Slices are the third rung only; tag replaced by `dash-<rel>` | U-006 60 percent; C-024 72 percent |
| R15 | V2, Q6 | mechanism | Cherry-pick of fixes into the just-in-time `release/` branch | No back-port step in the base | C-015 93 percent |
| R16 | V3, sec 1 to 3 | mechanism | Train cut from `integration` and landed in `integration`, then promotion to `master` | A3 conceded: the owner's 130 recent PRs did not use the promotion path | C-002, C-003 92 to 95 percent |
| R17 | V3, Q2 | mechanism | Per-story PR into the train as the default; merge authority over GitHub PRs for the coordinator (Open decision A) | Local merge is the default; the PR is an optional layer; no new authority over PR merges is requested | C-004 72 percent; C-006 75 percent; A3-C1 |
| R18 | V3, sec 2 | name | `train/<rel>` | Replaced by `release/<rel>` | C-001 72 percent |
| R19 | V3, Q2 step 3 | mechanism | Stacked story PRs | Nothing is stacked when story merges are local; availability on this plan UNVERIFIED (T12) | C-025, X-010 75 percent moot |
| R20 | V3, sec 5 and decision C | dependency | Edit `test.yml` now so `train/*` PRs get CI | Not a precondition; owner decision 6 only if per-story CI is wanted; where GitHub reads the file is UNVERIFIED | A-008, A-013 split 50 percent |
| R21 | V3, Q8 | rule | BMAD planning of release n+1 starts from `integration` | Planning stays on `master` after n merges | X-009 96 percent; C-020 96 percent |
| R22 | V3, Q3 | mechanism | Merge `origin/integration` into the batch branch, with a sync branch for conflicts | Not adopted; the sync branch is kept as a reserve for that case and used as the sync-PR head (change 19) | U-011 reserve 70 percent; C-008 90 percent |
| R23 | V3, Q7 | rule | Reliance on GitHub deleting head branches on merge | `delete_branch_on_merge` is false | C-023 92 percent |
| R24 | V1 (the base), Q4 | rule | Release size controlled by story count alone | Replaced by the file budget (change 25) | INV-011, INV-017 |
| R25 | Repository setting | mechanism | Restrict allowed merge methods on `master` to merge commits | Would stop the owner's normal squash for every other PR (last 12 merges were single-parent); not proposed; decision 8 | A-006; INV-009 |

## Threshold preservation

Every number inherited from a variant or from the debate, with its disposition. "NEW" marks a number this plan introduces.

| Source | Value | Where it lands | Disposition |
|--------|-------|----------------|-------------|
| V2 (A2R2 Q4) and V3 (Q5), estimate | about six stories | Story cap 6 (changes 14, 25) | preserved-exact; marked ESTIMATE; owner sets it |
| V3 Q5; V1 Q4 ("about a week") | about seven days; one week | Time box 7 days (changes 14, 25) | preserved-exact; the two are merged into one number; marked ESTIMATE |
| V2 (A2R2 Q4) | roughly 300 files, "without `.dev/` records" | Replaced by file budget 250 over all paths (change 25); 300 kept as the hard stop | modified-with-rationale: the PR diff counts `.dev/` (INV-011), and 300 is the `gh pr diff` limit |
| V3 (A3R2 Q2) | about 15 files or 1,000 added lines | Review-only story PR threshold (change 16) | preserved-exact; ESTIMATE from #484 and #490 |
| A4R2 Q2 | re-open the design above about four parallel stories | Change 29 table (two parallel stories) | preserved-exact |
| V4 rule 4 | PR #147: 34 commits, 1,384 files, +242,976 lines | Change 5 | preserved-exact, size evidence only |
| V4 rule 7 | 6 `backup/...` branches; `release/v0.1` 0 ahead, 62 behind | Change 4 reason | preserved-exact |
| V4 rule 4 | three test tiers; two approvals | Change 6 | dropped-with-rationale: no counterpart here (A4-C9, U-018 58 percent) |
| V3 Q5 (S22) | Chrome cycle from four weeks to two | not carried | dropped-with-rationale: V3 itself says the research gives no AI-specific number |
| A4 M3 | CI median 9.2 minutes (min 7.0, max 12.6), last 40 PR runs, 31 succeeded | Changes 11, 29 | preserved-exact |
| A4 M2 | two dispatch runs, 4 min 7 s and 5 min 1 s, 2026-11-05 | Change 11 | preserved-exact |
| A2 N2 and A1R2 | #640 1,146 files 43 minutes; #658 181 files 17 minutes; #664 181 files 27 minutes; #31 2,089 files, 0 reviews | Change 5, 25 | preserved-exact |
| A2 N1 | median 37 files, p90 334 for 155 PRs into `master`; 130 of them the owner's, none through `integration` | Change 25 table, R10 | preserved-exact |
| INV-007 | 9 of the last 40 `test.yml` PR runs failed (22.5 percent) | Change 26 | preserved-exact |
| INV-012, INV-013 | about 8 `master` PRs a day; peak 26 and 23 merged PRs a day | Changes 26, 30 | preserved-exact |
| INV-014 | 170 remote heads | Change 4 | preserved-exact |
| A1R2 new evidence 5; A4 M11 | `master` 26 commits ahead of `integration`; `integration` 2 ahead; newest `integration` commit 2026-11-18 | Changes 29, R10 | preserved-exact |
| INV-017 | 300 files (`gh pr diff`), 100 files (`gh pr view --json files`) | Change 25 | preserved-exact |
| GitHub docs, fetched 2026-11-23 | 3,000 files per PR, 100 per page | Change 25 | NEW (added to the probe's evidence) |
| This plan | file budget 250; stop-adding 200 | Change 25 | NEW; GUESS; owner may change |
| This plan | one working day of owner wait | Change 26 (INV-003) | NEW; GUESS; owner may change |

## Concrete anchors preserved

Carried verbatim into the merged text (names, ids and commands the merge must not paraphrase):
- Systems and files: `/sc:pr-submit --monitor 3 --base master`; `orca worktree create --branch <name> --base-branch <ref> --parent-worktree <selector> --agent claude`; `worker-start` (no `--branch`); `.github/workflows/test.yml`, `boundary-guard.yml`, `contract3-generator-constraint-lint.yml` and its heading `## Generator-Constraint Considered`; `branch-landed.sh`; `scripts/worktree_cleanup.py`; `sprint-status.yaml`; `git merge-tree`; `git revert -m 1`; `git bisect --first-parent`; `workflow_dispatch`; `delete_branch_on_merge` (false).
- Pull requests as evidence: #31, #147 (GFxAI), #484, #490, #491, #640, #658, #662, #664, #728, #730.
- Debate ids: C-001 to C-025, X-001 to X-010, A-001 to A-017, U-001 to U-018 as cited in each change; invariant ids INV-001 to INV-026.
- Constraints: CONTEXT lines 7 to 16 (owner model; ref conflict; worker contract; parallelism; pr-submit rules; `worker-start` and `--branch`; rules; ledger; release numbers; scale); the upstream-repository ban (no variant mentions it; the merged text states it once: PRs use `--repo IronbellyOrg/IronClaude`, nothing goes to `SuperClaude-Org`).
- Rollback bounds: story level `git revert -m 1`, release level revert PR of the release merge commit, "revert the revert first".

Intentionally modified (rationale in the change named): the release-line and story names (1, 10), the tag (3), the "nothing pushed" sentence (21), the one-story branch name (20), the `roughly 300 files without .dev/` cap (25).

Compliance check for the merge: V1 carries no requirement IDs; the anchors above are the equivalent. Any anchor of an accepted change missing from the merged text without a merge-log entry is a merge-execution failure (Step 5, dropped-anchor audit).

## Trials before first reliance

Each trial is throwaway: a disposable worktree or PR, never `master`, removed afterwards. Where a PR is needed, it goes through `/sc:pr-submit --monitor 3 --base <throwaway base branch cut from master>` and is closed unmerged. "Before release 1" trials block the first release; the others run when the feature they check is first used. The plan itself made no GitHub or project write; the trials are for the coordinator, after the owner's go.

| ID | What is checked | Passes when | Settles | When |
|----|-----------------|-------------|---------|------|
| T1 | `orca worktree create --name x --branch dash0-trial-s01-x --base-branch origin/master`; read back `git -C <wt> branch --show-current`; repeat with a name equal to an existing ref and with a name that would make a ref conflict | The branch name is exact and unprefixed; a taken or conflicting name fails loudly or gets a suffix that is visible | Orca prefix with `--branch`; whether flat names stay the default; A-007, A-011; INV-022 | Before release 1 |
| T2 | Coordinator creates the worktree, then `worker-start --worktree path:<it>`; the worker commits a `.dev/` record on the story branch; check `git status --short` is empty and the record is in the branch | The adopted worktree keeps the exact branch; the record is committed before the coordinator merges and removes the worktree | INV-022 adoption; INV-004 | Before release 1 |
| T3 | Release-shaped PR at `--monitor 3` with the draft guard, against a throwaway base: head fixed during the run; `foreign_op_in_progress` and `pr_head_mismatch` seen as the SKILL says | Bots and CI behave as described; a `-fix` after the monitor ends needs a new run | INV-005; M10 draft behaviour; the monitor-window rule | Before release 1 |
| T4 | A throwaway PR with more than 300 changed files: `gh pr diff` HTTP 406, `gh pr view --json files` 100, paged API; what pr-submit's own reads and the two bots do | pr-submit completes or fails in a way the brief can describe | INV-017 tooling; change 25 (c) | Before the first release that may exceed 250 files |
| T5 | `gh workflow run test.yml --ref <pushed throwaway line>`; time it; confirm `boundary-guard` and the Contract #3 workflow do not run | Run starts and finishes; duration recorded; PR-only workflows absent | Change 11 default gate; INV-026 | Before release 1 (owner nods CI minutes: decision 6) |
| T6 | Review-only story PR against a throwaway line: both bots review; local `--no-ff` merge then push; does GitHub show the PR merged; pr-submit report reads CI "clean" with no checks | Bots review; PR shows MERGED; the caveat of INV-023 is real or not | Change 16 optional layer; A-012 on this base | Before the layer is first used |
| T7 | GitHub side of change 25: records PR into a throwaway base; merge it; merge the base into the line; `changedFiles` of the release PR; and the two-PR landing from `release/x-p1` | Counts fall as the scratch test showed; both PRs open and merge | Records rule; two-PR landing; INV-017 | Before the first release whose count exceeds 250 |
| T8 | Tag `dash-0-trial` next to branches `release/dash0-trial` and `dash0-trial-s01-x`: Orca, pr-submit and closeout listing | No tool errors | Names (low risk; git side VERIFIED-HERE) | With T1 |
| T9 | Run the CI-equivalent list on a clean `master` checkout: record minutes and failures; compare with the CI median 9.2 minutes | Duration known; no step missing from the list | INV-007; A-010 (unmeasured) | Before release 1 |
| T10 | In release 1, record per PR: files, bot findings, bot review count, owner minutes | Observation only | INV-025 review depth against size | During release 1 |
| T11 | In releases 1 and 2, record PR opened and PR merged times | Observation only | INV-003 owner latency | During releases 1 and 2 |
| T12 | Whether stacked PRs and a merge queue are available on this plan | Answer recorded | Only rung 3 of the ladder; not used by the design | Only if rung 3 is considered |

Follow-up work outside this proposal (each its own issue, not part of the merge): the two-parent closeout check (change 23); paging the file list in the `/sc:auggie-review` rubric (change 25 (c)).

## Risk Summary

Changes not listed here (2, 3, 4, 5, 7, 8, 9, 12, 13, 15, 17, 18, 20, 22, 24, 27, 29, 30) are Low: additive or one-sentence text; rollback is removing the inserted text.

| Change | Risk | Impact if failed | Rollback |
|--------|------|------------------|----------|
| 1 | Medium | A missed occurrence leaves two spellings of the line name; commands copied from the text would create the wrong branch | Re-run a grep for `dash1.3/release` in the merged text; revert to base sec 2 and Q1 |
| 6 | Medium | Five gates in a row; the dispatch step needs CI minutes the owner may refuse | Drop the dispatch step from the list; the local gate and PR CI remain |
| 10 | Medium | Owner reads the flat names as a departure from `dash1.3/story1` and rejects them | Trial T1 passes: switch stories to `dash<rel>/s<NN>-<slug>` under a line named `release/dash<rel>`; the ref-conflict invariant still holds |
| 11 | Medium | Dispatch on a branch outside the filter list behaves differently than on 2026-11-05; or the owner refuses minutes | Fall back to the local gate only; INV-026 text stays |
| 14 | Low to Medium | Numbers (6 stories, 7 days) are estimates; the carried-story rule is new | Owner changes the numbers; remove the carried-story sentence |
| 16 | Medium | Two UNVERIFIED behaviours (merged-by-push, moved-base handling) | The layer is optional and off by default; remove sec Q2 "Optional layer" |
| 19 | Medium | Departs from the base-selection wording ("reserve only"); one more branch name | Use head `master` for the sync PR if pr-submit accepts it as a head (UNVERIFIED), or fall back to the base-selection wording (reserve only) |
| 21 | Low to Medium | The reset of an unpushed red merge is a destructive local act | Use `git revert -m 1` on the unpushed merge instead; slower, no data loss |
| 23 | Medium | The control is a sentence plus a check that does not exist yet; a wrong click is still possible | Recovery path: revert PR and redo (#658, #662, #664) |
| 25 | High | New design, no precedent; GitHub side and bot behaviour unverified; two of its paths cost an extra owner click | Remove sec 8; INV-017 stays open (accept the owner's explicit risk in chat) |
| 26 | Medium | Ten rules; three lean on tools or checks that need confirmation (INV-007, INV-009, INV-026) | Per row: delete the rule; the finding returns to UNADDRESSED |
| 28 | Medium | Orca behaviour is checked at help-text level only | Trials T1, T2; names stay valid either way (flat, no folder part) |

## Decisions for the owner

Eight decisions, most important first. The merged document carries defaults for all of them, so Step 5 can run before the owner answers; each answer changes the text only as stated. Each lists the recommended option and what every answer does.

**D1. May the coordinator do five things without asking each time?** (a) Merge a settled story into the release line locally with a merge commit. (b) Push the line forward-only after each merge, and reset a merge that failed the gate and was not yet pushed. (c) Run the CI-equivalent commands, including `make sync-dev`, that the release brief names. (d) Delete story, line and records branches and worktrees after the owner's merge. (e) Merge `master` into the line instead of rebasing (an exception to Pre-PR check 2 in CLAUDE.md, because the line is published). Recommended: yes to all five (C-006 75 percent; A-014; CONTEXT line 11 "to be confirmed").
- Yes: the design runs as written; the owner clicks once per release PR (plus a records PR or a sync PR when they apply).
- No to (a): every story goes through a review-only PR (change 16); more owner clicks, bots on every story, no CI without a workflow edit.
- No to (b), (c), (d) or (e): the coordinator asks for each such step; the backup push, the gate, the sweep or the merge-in wait for the owner.

**D2. Size numbers.** Story cap 6, time box 7 days, release-PR file budget 250 over all paths, stop adding at 200, hard stop 300 (the last is GitHub's tool limit). Recommended: accept for release 1, then reset from the ledger's measured counts.
- Accept: as written; unfinished stories ride the next release.
- Looser (for example 400 files): the PR passes the `gh pr diff` limit; reviews use the paged API and the local diff; INV-017 is back for that release.
- Tighter (for example 150 files): more, smaller releases and more owner clicks.

**D3. Records PR when a release is over budget.** Recommended: yes, decided at freeze (change 25 (b)); promote it to the default if it triggers three releases in a row.
- Yes: records land in their own PR first; the release PR stays readable; one extra owner click and CI run.
- Always: same, with no freeze count; one extra PR for every release including small ones.
- Never: records ride the release PR; above 300 files the review tools fail on it and the owner reviews through the local diff.

**D4. Merge method of a story into the line (C-005, unresolved 50 percent).** Recommended: `--no-ff` (merge commit).
- `--no-ff`: story boundaries stay visible (`git revert -m 1`, `git bisect --first-parent`); a reverted story needs "revert the revert" before it returns; the optional review-only PR needs it to show as merged.
- Squash: a plain `git revert` removes a story and nothing needs the revert-the-revert step; the story's own commits are lost from the line.

**D5. Is `integration` still in use, and does the coordinator run the sync?** Facts: `master` is 26 commits ahead; no merged PR into `integration` since 2026-11-19. Recommended: the coordinator runs the `master` into `integration` sync PR (head `dash<rel>-sync<N>`, merge commit) after each landing, and the owner says whether Clay still works from `integration`.
- Still in use, coordinator syncs (A-015 ACCEPT): as written; one more PR per release.
- Still in use, someone else syncs: the merged text names that person; the coordinator opens no sync PR.
- Not in use: the sync PR and the early-warning checks against `integration` come out of the text; whether to retire the branch is a separate question this proposal does not raise.

**D6. How much outside look at a story, and the one-line workflow change.** Three parts. (a) Dispatch runs of `test.yml` on the pushed line, about 9 minutes each, after shared or risky stories and on the final tip. (b) Review-only story PRs for stories above about 15 files or 1,000 added lines. (c) Adding `release/**` to `test.yml`'s `pull_request` filter (one line; cost listed in change 29). Recommended: (a) yes; (b) off until trial T6 passes; (c) no for release 1.
- (a) yes: a CI-clean check on the tip before the PR; no: only the local gate and the PR run.
- (b) on: bots see big stories early, no CI on those PRs; off: the first review is the release PR.
- (c) yes: story PRs get CI; the edit rides the release PR, costs about 55 to 165 CI minutes per release (ESTIMATE) and must be checked against the real branch name; no: story PRs get bots only.

**D7. A test-only release of several stories (1.105): line or direct PRs?** Recommended: a line, like every other release (change 27).
- Line: one rule set, ledger on the line, one PR, one click.
- Direct PRs: each story is a PR into `master` with its own CI, bots and click; the ledger has no home for that release.

**D8. How to guard the merge click on the release PR.** Recommended: the PR-body sentence plus the new two-parent closeout check (detective), and the revert-and-redo recovery.
- Sentence plus check: a wrong click is found after it happens; recovery costs a revert PR and a redo (#658, #662, #664).
- Sentence only: cheaper; a wrong click may go unnoticed until a story revert fails.
- Restrict merge methods on `master` in repository settings: blocks the wrong click, but also the owner's normal squash for every other PR; not recommended.

## Review Status

- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-23 (date only; the plan carries no clock time)
- Open before Step 5: none. The eight decisions have defaults in the merged text.
- Open after Step 5: re-run the invariant gate on the merged text (INV-017 and the ten MEDIUM findings); run trials T1, T2, T3, T5, T9 before release 1.
- Plan author: Step 4 writer, 2026-11-23. Inputs read in full: `base-selection.md`, `variant-1-original.md` to `variant-4-original.md`, `debate-transcript.md` (Round 2, Scoring Matrix, Convergence Assessment), `invariant-probe.md`, `../CONTEXT.md`, the Step 4 sections of the protocol and `refs/artifact-templates.md` Section 4. Round 1 statements were read only through their Round 2 citations.
