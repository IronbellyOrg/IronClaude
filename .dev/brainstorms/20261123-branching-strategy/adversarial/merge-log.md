# Merge Execution Log

## Metadata
- Base: Variant 1 (architect: release line, story branches, local merges)
- Executor: merge-executor agent
- Merged artifact: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261123-branching-strategy/UNIFIED-BRANCHING-PROPOSAL.md` (12 sections, about 585 lines)
- Plan: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261123-branching-strategy/adversarial/refactor-plan.md` (30 changes, 25 rejected alternatives, 8 owner decisions, 12 trials)
- Changes applied: 30 of 30 planned (0 failed, 0 skipped; 5 applied with a recorded note, see "Deviations and notes")
- Status: success, with the invariant gate still to re-run (see Post-Merge Validation)
- Timestamp: 2026-11-23T14:10:06Z (start); completed 2026-11-23 (see end of file)

## Changes Applied

Section numbers below are those of the merged file. "Before" is the base (Variant 1) text. Validation per change is the whole-document result recorded in "Post-Merge Validation" (structure, references and contradiction rescan all pass); a change-specific note is added where one applies. Provenance tags are HTML comments in the merged file; the exact tag text is shortened here.

### Change 1: Release line named `release/dash<rel>` (from Variant 4)
- **Status**: Applied
- **Source**: Variant 4, rule 1
- **Target**: Base sec 2 table, sec 3 diagram and steps, Q1 to Q9, risks; merged sec 2.1, 3.1, 3.2, Q1 to Q9
- **Before**: `dash1.3/release` in about 15 places; tag and story names under the same folder
- **After**: `release/dash<rel>` everywhere; invariant "a branch name is never the folder of another" kept (section 2.2 rule 1); glossary sentence that the owner's "integration branch" means the release line and the repository branch `integration` is a different thing (section 1.2)
- **Provenance tag**: `<!-- Source: Base (original, modified) ... per Changes #1, #10, #28 -->` (sec 2, Q1)
- **Validation**: grep for `dash1.3/release`: 0 hits. Structure pass | References pass | Contradictions pass

### Change 2: Freeze after the last planned story (from Variant 4)
- **Status**: Applied
- **Source**: Variant 4, rule 6
- **Target**: Base Q6 and sec 3 (before step 5); merged Q6 item 3 and section 3.2 step 5
- **Before**: no freeze rule
- **After**: freeze text as planned, including "while pr-submit runs, nothing enters" and the change-14 time-box trigger
- **Provenance tag**: `<!-- Source: Base (original, modified) - Variant 1 Q6; freeze from Variant 4 rule 6 per Change #2 ... -->`
- **Validation**: pass

### Change 3: Tag `dash-<rel>` (from Variant 4)
- **Status**: Applied
- **Source**: Variant 4, rule 4
- **Target**: Base sec 2 tag row and Q7; merged sec 2.1 and 2.5, Q7
- **Before**: tag `dash/1.3`; "should not clash; this was not tested (UNVERIFIED)"
- **After**: tag `dash-1.3`; the scratch-repository coexistence result marked VERIFIED-HERE; rule that no branch is ever named `dash-<rel>`
- **Provenance tag**: `<!-- Source: Variant 4 rule 4 ... merged per Change #3 -->` (sec 2.5)
- **Validation**: grep for `dash/1.3` and `dash/<`: 0 hits. Pass

### Change 4: Explicit deletion with remote branch and sweep (from Variant 4)
- **Status**: Applied
- **Source**: Variant 4, rule 7
- **Target**: Base Q7; merged Q7
- **Before**: delete branches after merge, local wording only
- **After**: local and remote deletion (`git push origin --delete <name>`), the sweep `git ls-remote --heads origin 'refs/heads/release/dash<rel>*' 'refs/heads/dash<rel>-*'`, `delete_branch_on_merge` false, 170 remote heads, GFxAI's 6 `backup/...` branches and `release/v0.1` (0 ahead, 62 behind)
- **Provenance tag**: `<!-- ... explicit remote deletion and sweep from Variant 4 rule 7 per Change #4 ... -->`
- **Validation**: pass (sweep glob checked against names in section 2.1: records and `-p1` branches match)

### Change 5: Release-PR size evidence (from Variant 4)
- **Status**: Applied
- **Source**: Variant 4, rule 4 (PR #147)
- **Target**: Base Q4; merged Q4 "Release size" table
- **Before**: size risk stated without numbers
- **After**: four-row table (#147, #640, #664 with #658, #31) and the sentence "a fast merge shows nothing broke, not that anyone read the diff"
- **Provenance tag**: `<!-- ... per Changes #5, #6, #11, #14, #23, #25, #26 -->` (Q4)
- **Validation**: pass; every plan number present (threshold audit below)

### Change 6: Reduced acceptance gate for the release PR (from Variant 4)
- **Status**: Applied
- **Source**: Variant 4, rule 4, reduced
- **Target**: Base Q4 and sec 3 step 5; merged Q4 "gate list" and section 3.2 step 6
- **Before**: no ordered gate
- **After**: six-step list (freeze, `master` merged in, local gate, green dispatch run, pr-submit with PR CI and both bots, owner merges with a merge commit); GFxAI's three tiers, UAT sign-off and two approvers stated as not carried
- **Provenance tag**: same Q4 comment
- **Validation**: pass

### Change 7: Evidence marks on every rule (from Variant 4)
- **Status**: Applied (placement note in "Deviations and notes")
- **Source**: Variant 4 line 5
- **Target**: Base sec 1 new paragraph; merged sec 1.3 plus marks in every section
- **Before**: UNVERIFIED used ad hoc
- **After**: five-mark legend (VERIFIED-HERE, VERIFIED-PROBE, ESTIMATE, GUESS, UNVERIFIED) and marks on numbers and behaviour claims
- **Provenance tag**: `<!-- Source: Variant 4 ... merged per Change #7 -->` (sec 1.3)
- **Validation**: pass

### Change 8: Wording of what the owner rule forbids (from Variant 4)
- **Status**: Applied
- **Source**: Variant 4, rule 2; U-017
- **Target**: Base Q2 "Where" bullet and sec 1; merged sec 1.5 and Q2 "Authority"
- **Before**: coordinator merges without stating the owner rule it relies on
- **After**: coordinator never merges a PR or into `master`/`integration`; local story merge is a smaller class needing the owner's chat confirmation (decision 1); fall-back to review-only PRs if declined
- **Provenance tag**: `<!-- Source: Variant 4, rule 2 ... merged per Change #8 -->`
- **Validation**: pass

### Change 9: The sync is the price of landing on `master` (from Variant 4)
- **Status**: Applied
- **Source**: Variant 4, rule 4
- **Target**: Base Q8; merged Q8
- **Before**: sync mentioned without the reason
- **After**: "`integration` does not contain the release until the sync pull request lands; that is the price of landing on `master`"; who runs it today marked UNVERIFIED
- **Provenance tag**: `<!-- ... price sentence from Variant 4 rule 4 per Change #9 -->` (Q8)
- **Validation**: pass

### Change 10: Flat story and fix names (from Variant 2, also Variant 3)
- **Status**: Applied
- **Source**: Variant 2 sec 2; Variant 3 sec 2
- **Target**: Base sec 2 rows, sort paragraph, create command, step 2; merged sec 2.1 to 2.4, 3.2 step 2
- **Before**: `dash1.3/s04-<slug>` and `dash1.3/fix-<NN>-<slug>`
- **After**: `dash<rel>-s<NN>-<slug>`, `dash<rel>-fix<NN>-<slug>`; `git branch --list '*dash1.3-*'`; section 2.4 states plainly that the owner's `dash1.3/story1` shape changed, why (the `ironbelly/` prefix failure, 49 prefixed remote branches) and that T1 can reverse it
- **Provenance tag**: `<!-- Source: Variant 2 sec 2 and Variant 3 sec 2, merged per Change #10 -->` (sec 2.4)
- **Validation**: pass

### Change 11: Outside CI per story without a workflow edit (from Variant 2)
- **Status**: Applied
- **Source**: Variant 2 Q2, means `workflow_dispatch`
- **Target**: Base Q2, Q4, sec 5; merged Q2 "Outside gate", Q4 gate item 4, section 5, decision 6
- **Before**: no CI before the end
- **After**: dispatch command with `--repo IronbellyOrg/IronClaude`, evidence (unconditional `workflow_dispatch`, two runs on 2026-11-05 of 4 min 7 s and 5 min 1 s, median 9.2 minutes, range 7.0 to 12.6, 40 runs, 31 succeeded), the INV-026 caveat, the owner's CI-minutes nod
- **Provenance tag**: inline `<!-- Source: Variant 2 Q2 goal ... means from Change #11 -->` (Q2)
- **Validation**: pass

### Change 12: Third rung: dark slices (from Variant 2)
- **Status**: Applied
- **Source**: Variant 2 steps 1 and Q5
- **Target**: Base Q5; merged Q5 ladder rung 3
- **Before**: "Flags are not used"
- **After**: that sentence kept for the design; rung 3 added (after a pilot, slices land alone as direct PRs; flag retirement line in the ledger)
- **Provenance tag**: `<!-- ... ladder per Changes #12 and #15 ... -->` (Q5)
- **Validation**: pass

### Change 13: Shared-file list for the coordinator (from Variant 2, extended)
- **Status**: Applied
- **Source**: Variant 2 Q2; debater list; INV-019
- **Target**: Base Q2(b); merged Q2 "Prevention" items 2 and 3
- **Before**: lockfiles, `pyproject.toml`, registries, `__init__` exports
- **After**: the full list (`CHANGELOG.md`, `CLAUDE.md`, `README.md`, `PROJECT_INDEX.json`, `PROJECT_INDEX.md`, docs index files, `pyproject.toml`, `uv.lock`, `scripts/dependency_baseline.txt`, count-pinned tests); cites the assertion `len(data["commands"]) == 47` in `tests/recommend/test_routing_refresh.py`, not a line number; the probe's worker-contract counts (13 and 10) not carried, as the plan says
- **Provenance tag**: Q2 comment (Change #13)
- **Validation**: pass

### Change 14: Time box with floating scope (from Variant 3)
- **Status**: Applied
- **Source**: Variant 3 Q5; U-010
- **Target**: Base Q4 last sentence and Q5 justification; merged Q4 "Time box" and Q5
- **Before**: "split it if the branch is open longer than about a week"
- **After**: six merged stories or seven days (ESTIMATE, owner sets); carried-story rule; the DORA extrapolation disclosure kept
- **Provenance tag**: Q4 and Q5 comments (Change #14)
- **Validation**: pass

### Change 15: Fallback ladder (from Variant 3 and Variant 2)
- **Status**: Applied
- **Source**: Variant 3 Q5; Variant 1 Q5
- **Target**: Base Q5 last bullet and title; merged Q5, document title
- **Before**: "switch to Proposal 3"; title "Proposal 1:"
- **After**: rungs 0 to 3; retitled "Unified branching proposal for dashboard releases"
- **Provenance tag**: Q5 comment
- **Validation**: grep for `Proposal [0-9]`: 0 hits. Pass

### Change 16: Optional review-only story PR into the line (from Variant 3)
- **Status**: Applied
- **Source**: Variant 3 Q2
- **Target**: Base Q2 and sec 5; merged Q2 "Optional layer", section 5
- **Before**: none
- **After**: off by default; threshold about 15 files or 1,000 added lines (ESTIMATE); #484, #490, #491 evidence; `--no-ff` local merge so the PR shows merged (UNVERIFIED, T6); the four costs (no CI, INV-023 "clean" caveat, a session per story, moved base)
- **Provenance tag**: inline Q2 comment (Change #16)
- **Validation**: pass

### Change 17: One owner decision list at the end (from Variant 3)
- **Status**: Applied (note in "Deviations and notes")
- **Source**: Variant 3 sec 8; U-012
- **Target**: new sec 10; Sources moves to sec 11
- **Before**: no list
- **After**: section 10, eight decisions in the plan's order, each with recommendation and what every answer does; Sources is section 11
- **Provenance tag**: `<!-- Source: Variant 3 sec 8 ... merged per Change #17 ... -->`
- **Validation**: pass

### Change 18: Trials before first reliance (from Variant 3)
- **Status**: Applied (note in "Deviations and notes")
- **Source**: Variant 3 risk 5; U-013
- **Target**: new sec 9
- **Before**: none
- **After**: table of T1 to T12, cheapest first, each with settles, exact command or check, disposable target, pass, fail; blocking set (T1, T2, T3, T5, T9) stated
- **Provenance tag**: `<!-- Source: Variant 3, risk 5 ... merged per Change #18 ... -->`
- **Validation**: pass

### Change 19: Sync branch `dash<rel>-sync<N>` as head of the sync PR (from Variant 3, role changed)
- **Status**: Applied
- **Source**: Variant 3 sec 2; U-011
- **Target**: Base sec 2 (new row), step 6, Q8; merged sec 2.1, 3.2 step 8, Q8
- **Before**: sync PR named without a head branch
- **After**: `dash<rel>-sync<N>` cut from `origin/integration`, `master` merged in, `--base integration`, "merge commit, not squash" in the body, conflict stops the coordinator; the departure from the base-selection wording ("reserve only") is stated in the plan and is carried as written
- **Provenance tag**: Q8 comment (Change #19)
- **Validation**: pass

### Change 20: A release with one story has no line (from Variant 3 and Variant 1)
- **Status**: Applied
- **Source**: Variant 3 Q6; Variant 1 Q6
- **Target**: Base Q6 last sentence; merged Q6 item 5
- **Before**: "a plain `fix/` or `feat/` branch"
- **After**: `dash<rel>-s01-<slug>` from `master`, ledger on it, one PR with `--base master`, merge commit, tag; `fix/<issue>-<slug>` kept for shipped-code fixes
- **Provenance tag**: Q6 comment (Change #20)
- **Validation**: pass

### Change 21: Forward-only push after each story merge
- **Status**: Applied
- **Source**: debate (A1R2 item 1; A4R2 point 8)
- **Target**: Base sec 1 sentence and sec 3 step 3; merged sec 1.1, 3.2 step 3, Q9
- **Before**: "Nothing is pushed for review until the release is complete"
- **After**: push order, plain push never `--force`, backup not a review request, INV-002 (no workflow on push or tag), red-gate reset to the ledger's tip hash
- **Provenance tag**: sec 1 and Q9 comments
- **Validation**: pass; one wording conflict found and fixed during validation (see "Contradiction re-scan")

### Change 22: Revert the revert first
- **Status**: Applied
- **Source**: debate (A1R2 item 3; scratch run, `DU s.txt`)
- **Target**: Base Q9 second bullet and risk 5; merged Q9, section 7
- **Before**: re-merge called "unverified general git behaviour"
- **After**: procedure in Q9 marked VERIFIED-PROBE; base risk 5 removed from section 7 (stated in the section's provenance comment)
- **Provenance tag**: Q9 comment (Change #22)
- **Validation**: pass

### Change 23: "Merge commit, not squash" sentence plus a two-parent closeout check
- **Status**: Applied
- **Source**: A-006; A4 M4; INV-009
- **Target**: Base Q4; merged Q4 "The merge click", decision 8
- **Before**: owner merges with a merge commit, method not controlled
- **After**: the PR-body sentence (release and sync PR), `gh pr view <n> --repo IronbellyOrg/IronClaude --json mergeCommit` plus `git cat-file -p <sha>` must show two `parent` lines, labelled new work not built, recovery path #658, #662, #664, no setting change proposed
- **Provenance tag**: Q4 comment (Change #23)
- **Validation**: pass

### Change 24: First-parent bisect over `--no-ff` story merges
- **Status**: Applied
- **Source**: A4 M5
- **Target**: Base Q9; merged Q9
- **Before**: none
- **After**: one bullet, `git bisect start --first-parent`, scratch result (7 entries against 26), git 2.47.3 VERIFIED-HERE
- **Provenance tag**: Q9 comment (Change #24)
- **Validation**: pass

### Change 25: Size budget, records rule, tooling fallback, over-budget action (INV-017, INV-011, INV-025)
- **Status**: Applied (note in "Deviations and notes")
- **Source**: `invariant-probe.md`; base-selection item 25
- **Target**: Base Q4, sec 3 steps 3 and 5, Q7, sec 5, sec 7; new sec 8
- **Before**: size bounded by story count only
- **After**: section 8.1 to 8.5 carry the plan's (a) numbers table, (b) records rule items 1 to 8, (c) fallback table, (d) over-budget table; Q4 gets the pointer and size evidence; section 3.2 gets the predict-and-write and count steps; Q7 and section 7 updated
- **Provenance tag**: `<!-- Source: New section, no variant (merge-plan Change #25) ... -->` and a modified-threshold tag at the 8.2 table
- **Validation**: pass; every number of the plan's table present (250, 200, 300, 100, 3,000, 6, 7 days, about 15 files or 1,000 lines)

### Change 26: Ten MEDIUM invariants, one outcome each
- **Status**: Applied
- **Source**: `invariant-probe.md` INV-003, 005, 006, 007, 008, 009, 011, 019, 025, 026
- **Target**: Base sec 3 steps 3 to 5, Q2, Q4, Q7, Q9, sec 7, and the owner-facing sections
- **Before**: unaddressed
- **After**: INV-003 Q4 "While the PR waits"; INV-005 Q4 "monitor window"; INV-006 and INV-007 Q2 "Order" and "local gate"; INV-008 Q4 "Contract #3"; INV-009 Q4; INV-011 section 8; INV-019 Q2 "Prevention" 3; INV-025 section 8.2 and T10; INV-026 Q4 gate item 4 and 5
- **Provenance tag**: Q2 and Q4 comments (Change #26)
- **Validation**: pass

### Change 27: Hotfix and special-release handling (C-017)
- **Status**: Applied
- **Source**: C-017; base-selection
- **Target**: Base Q6; merged Q6 items 1, 2, 4, 6, 7, decision 7
- **Before**: 1.1 and 1.105 as ordinary releases, one-story skip
- **After**: five decided points (ordinary release for every number including 1.1 and 1.105; one-story release; `fix/<issue>-<slug>` with no cherry-pick; `-fix<NN>` branch inside a line; the `dash1.1` / `dash1.105` prefix hazard, verified); decision 7 left to the owner
- **Provenance tag**: Q6 comment (Change #27)
- **Validation**: pass

### Change 28: The ref-name rule and the Orca `--branch` check
- **Status**: Applied
- **Source**: CONTEXT lines 8, 12; A-007, A-011; INV-018, INV-022
- **Target**: Base sec 2 table, invariant paragraph and creation command; merged sec 2.1 to 2.3, 2.5
- **Before**: one table, a three-line rule, a create command missing `--name`
- **After**: nine-row table, five rules, pre-create check commands, two create commands with `--name` and `--agent claude`, verified and unverified list (T1, T2, T3, T4, T6, T8, T12)
- **Provenance tag**: sec 2 comment (Changes #1, #3, #10, #19, #20, #28)
- **Validation**: pass

### Change 29: Fit with the owner's decisions of 2026-11-23, and the `test.yml` question
- **Status**: Applied (note in "Deviations and notes")
- **Source**: owner decisions as stated in the lead's brief; CONTEXT lines 7, 9, 10, 11, 14
- **Target**: Base sec 1 and sec 10; merged sec 1.4, decision 6
- **Before**: none
- **After**: seven-row fit table with the departure or cost of each; the four costs of editing `test.yml` are in decision 6; recommendation: no edit in release 1
- **Provenance tag**: `<!-- Source: Base (original, modified) - new table per Change #29 ... -->`
- **Validation**: pass

### Change 30: Seven LOW unaddressed invariants and eight addressed ones
- **Status**: Applied
- **Source**: `invariant-probe.md` INV-001, 004, 010, 014, 015, 021, 023 and INV-002, 012, 013, 016, 018, 020, 022, 024
- **Target**: Base Q7, Q3, Q6, Q8, sec 7
- **Before**: unaddressed or implicit
- **After**: INV-001 section 3.2 step 1 and Q7; INV-004 Q2; INV-010 Q3; INV-014 Q7; INV-015 Q5; INV-021 Q3; INV-023 Q2; the eight ADDRESSED rows carried as facts (INV-002 step 3; 012 Q3; 013 section 5; 016 Q6; 018 section 2.2; 020 Q3; 022 T1 and T2; 024 Q7)
- **Provenance tag**: Q3 and Q7 comments (Change #30)
- **Validation**: pass

### Presentation additions made on the lead's brief (no new rule or number)
- Section 1.2 glossary, section 3.3 worked timeline of release 1.3 (illustrative days and file counts, labelled as an illustration), section 6.1 who-does-what table, section 1.5 list of what the coordinator may and may not do, section 12 "How this was produced". Each is built only from rules and facts in the plan.

## Post-Merge Validation

Run on 2026-11-23 against the finished merged file by Grep and Bash (read-only) after all 30 changes were applied.

### Structural Integrity
- Heading hierarchy: pass. One H1 (document title), twelve H2 (sections 1 to 12), H3 under sections 1, 2, 3, 4 (Q1 to Q9), 6, 8; no level gap, no orphaned H3. Section 5, 7, 9, 10, 11, 12 have no H3 by design.
- Section ordering: pass. Summary and words (1), names (2), flow and worked example (3), nine questions (4), costs (5), roles (6), risks (7), size budget (8), trials (9), owner decisions (10), sources (11), production note (12). Prerequisites come before dependents: the glossary and marks precede first use; section 8 precedes the trials that check it.
- Document flow: pass. No `RF_PLACEHOLDER`, TODO or stub marker remains (grep: 0 hits after the stub comment was removed). No em dash or en dash anywhere in the merged file (grep: 0 hits).
- Provenance: pass. 30 `Source:` comments; every change number 1 to 30 is cited at least once; the document header carries the Provenance, Base and Merge date comments.

### Internal References
- Total references: 211 (matches of "section N", "section N.M", "Q1 to Q9", "decision N", "trial T1 to T12" and bare T-ids, counted by one regex; includes the trials table's own ids)
- Resolved: 211
- Broken: 0. Targets checked: sections 1.3, 1.4, 1.5, 2, 2.2, 2.3, 3.2, 8, 8.3, 8.4, 8.5, 9, 10 exist; Q1 to Q9, T1 to T12 and decisions 1 to 8 exist. One reference was wrong during the merge ("section 8 (d)") and was corrected to "section 8.5". "sec N" strings remain only inside HTML provenance comments, where they name sections of the source variants.

### Contradiction Re-Scan
- New contradictions introduced: 0 after two fixes; 2 were found and fixed during the scan.
  1. Found: the freeze step said "no pull request is opened until the freeze", while the optional review-only story PRs (Q2) and an early records PR (section 8.5) are opened earlier. Fixed: sections 1.1 and 3.2 step 3 now say "no pull request for the release", with the two exceptions named.
  2. Found: three runnable `gh pr view` commands (the two-parent check twice, the `changedFiles` count) lacked `--repo IronbellyOrg/IronClaude`. Fixed. All other runnable `gh` commands already carried it.
- Rescan list, each clean:
  - Ref-name rule: every branch pattern in section 2.1 is a flat leaf or a leaf under `release/` or `fix/`; no branch is named `dash<rel>`, `dash-<rel>`, `release` or `fix`. The only folder-form names are the deliberate test inputs of T1 (`dash0-trial`, then `dash0-trial/s01`, to see a refusal) and the conditional fallback in section 2.4 (`dash<rel>/s<NN>-<slug>` under `release/dash<rel>`), which still obeys the rule.
  - CI trigger: `test.yml` runs for pull requests and pushes into `master` and `integration` only (section 1.2, 1.4, Q2, Q4); the release, records, sync and revert PRs get CI; story merges, line pushes and tags do not; a dispatch run tests the tip alone. No section says otherwise.
  - Rebase versus published branch: never rebase the line after the first story branch is cut or after it is pushed (Q2, Q3, 1.5, glossary); the project's pre-PR check 2 is replaced for this PR by a merge of `master`, once, with the owner's confirmation (Q3, decision 1 part e). No step uses a rebase or a force push.
  - `.dev/tasks` staging rule: the merged text does not mention `.dev/tasks` and never says a `.dev/` path is "never staged"; `.dev/` records are committed on the branch where they were made (1.5, Q7). No conflict.
  - Fork-only rule: every pull request goes through `/sc:pr-submit --monitor 3` (1.4, 1.5, Q4, Q8, section 8); `--repo IronbellyOrg/IronClaude` is on every runnable `gh` command.
  - Never push to or open anything on `SuperClaude-Org`: stated once in section 1.5 and once in the role table (6.1); nothing else names it.
  - The coordinator never merges a pull request: section 1.5, 6.1, Q4, Q8 agree; the owner merges the release, records, sync and revert PRs. The one exception the text allows is the trial PRs of T7, which the owner merges into a throwaway base only.
  - Pre-debate guess of the research agent: grep for "researcher", "pre-debate", "likely base": 0 hits. Visible text does not mention it.

### Threshold preservation check (plan table)
- Present in the merged file with exact values: 250 files, 200, 300, 100 per `gh pr view`, 3,000 and 100 per page (REST docs), story cap 6, time box 7 days, about 15 files or 1,000 added lines; #147 (34 commits, 1,384 files, +242,976 lines); #640 (1,146 files, 43 minutes); #658 and #664 (181 files, 17 and 27 minutes); #31 (2,089 files, 0 reviews, 0 comments); CI median 9.2 minutes (7.0 to 12.6, last 40, 31 succeeded); two dispatch runs (4 min 7 s, 5 min 1 s, 2026-11-05); median 37 files and p90 334 for 155 PRs, 130 the owner's; 9 of 40 failed (22.5 percent); about 8 `master` PRs a day, 116 since 2026-11-09, peaks 26 and 23; 170 remote heads; `master` 26 ahead of `integration`; #728 453 files and #730 292; #484 (8 files, +217) and #490 (25 files, +4,636); the 400-file scratch test; git 2.47.3; GFxAI 6 `backup/...` branches, `release/v0.1` 0 ahead and 62 behind.
- Modified with rationale (as the plan says): Variant 2's "roughly 300 files, without `.dev/` records" became the 250 budget over all paths with 300 as hard stop (tag in section 8.2). Preserved-exact otherwise.
- Not carried, as the plan says: the probe's worker-contract counts 13 and 10 (not found by grep), Chrome's four-to-two-week cycle, GFxAI's three test tiers and two approvers.

### Dropped-anchor audit
- Concrete anchors listed in the plan are all present: `/sc:pr-submit --monitor 3 --base master`; `orca worktree create --branch ... --base-branch ... --parent-worktree ... --agent claude`; `worker-start` (no `--branch`); `test.yml`, `boundary-guard.yml`, `contract3-generator-constraint-lint.yml` and the heading `## Generator-Constraint Considered`; `branch-landed.sh`; `scripts/worktree_cleanup.py`; `sprint-status.yaml`; `git merge-tree`; `git revert -m 1`; `git bisect --first-parent`; `workflow_dispatch`; `delete_branch_on_merge`; PRs #31, #147, #484, #490, #491, #640, #658, #662, #664, #728, #730; invariant ids INV-001 to INV-026 (each addressed in a named place); rollback bounds; the upstream ban (stated once).
- Debate ids (C-, X-, A-, U-) are cited in the merged text only where they help the owner (C-005, X-004, C-006, C-015, A-004, A-005, A-007, A-010, A-011, A-012); the rest stay in the plan and in the change numbers of the provenance comments. Decision basis: the lead's brief asks for text a person who has not seen the debate can read. Replacement target: `refactor-plan.md` (every id is traceable there by change number).

### Invariant gate status
- INV-017 (HIGH) is handled by Change 25 (section 8: file budget, records PR, paged-API fallback, over-budget table). The ten MEDIUM and seven LOW findings are each handled by Changes 26 and 30. This merge does not lift `BLOCKED_BY_INVARIANTS`: the orchestrator must re-run the invariant gate on the merged text. Status: INV-017 handled, still to verify.

## Summary

- Total changes planned: 30
- Successfully applied: 30 (5 with a recorded note, below)
- Failed: 0
- Skipped: 0
- Post-merge validation: PASS (structure, 211 of 211 internal references, contradiction re-scan clean after 2 fixes, threshold preservation, dropped-anchor audit). The invariant gate is NOT re-run by this executor: INV-017 handled by Change 25, still to verify.
- Completed: 2026-11-23

### Deviations and notes

1. **Change 7 (placement).** The plan puts the marks table "after the first paragraph of sec 1". The merged section 1 has subsections, so the table is section 1.3, after the glossary. Content and marks are as planned.
2. **Change 17 (extra section).** Decisions are section 10 and Sources is section 11, as planned. The lead's brief also asked for a visible "How this was produced" section at the end, which is section 12 (after Sources). The plan did not number it.
3. **Change 18 (commands).** The plan's trials table gives "what is checked" and "passes when" but not every exact command. The executor composed the commands for T3, T4, T5, T6, T7 and T9 from the plan's wording and the project's documented forms (`gh ... --repo IronbellyOrg/IronClaude`, `/sc:pr-submit --monitor 3 --base ... --head ...`, `git push origin --delete`). The plan's T1 command omitted `--agent`; `--agent claude` was added, because the project rule says every Orca worktree gets an agent and change 28's create commands carry it. T12 has no command (read-only check). The "fails" column is the executor's reading of the plan's risk table and rollbacks, not new design. The coordinator should read these commands before running them, and none was run.
4. **Change 25 (step numbers).** The base had six steps; the merge splits "freeze" and "count, then check" so section 3.2 has eight steps. The plan's "step 3" and "step 5" targets are mapped to steps 3, 5 and 6. Q4 carries more than "two sentences and a pointer" because it also holds the gate list, the monitor window and the size evidence the plan assigns to Changes 5, 6 and 26.
5. **Change 29 (a date).** The plan says "no merged PR into `integration` since 2026-11-19" in Change 29 and "newest `integration` commit 2026-11-18" in its threshold table; base-selection records that the two debate sources differ by a day. The merged text says "since 2026-11-18 or 2026-11-19" and marks it VERIFIED-PROBE (not re-run).
6. **Presentation additions** (glossary, worked example, role table, section 1.5, section 12) came from the lead's brief; they add no rule and no number. The worked example's days and file counts are labelled as an illustration.
7. **Not done on purpose:** the plan's "Follow-up work outside this proposal" (two-parent closeout check, paging in `/sc:auggie-review`) is listed in sections 4 (Q4), 8.4 and 9 and is not built. No GitHub or git write was made; the only files written are the two named in the brief.
