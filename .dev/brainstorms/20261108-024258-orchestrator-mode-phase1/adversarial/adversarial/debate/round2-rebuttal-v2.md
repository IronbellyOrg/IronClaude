# Round 2 Rebuttal: Variant 2 (opus, analyzer)

- Variant defended: V2 = `variant-2-opus-analyzer.md`
- Date: 2026-11-08 (from session context)
- Inputs read this round: `round1-advocate-v1.md` lines 1-150, `round1-advocate-v3.md` lines 1-169, `round2-rebuttal-v1.md` (140 lines, all), V2 lines 174-203, my own Round 1 file, and the seed brief read in Round 1. Nothing under `qa/`, no code, no live tool and no git was read or run.
- Citation form: `V1R1:47` = line 47 of `round1-advocate-v1.md`; `V3R1:25` = line 25 of `round1-advocate-v3.md`; `V1R2:22` = line 22 of `round2-rebuttal-v1.md`; `V2R1:138` = line 138 of my Round 1 file; `V2:156` = line 156 of variant 2; `V1:153` = line 153 of variant 1; `Seed:34` = line 34 of the seed brief.
- Method: for each criticism I asked what the defect's cause is in V2's text, whether the cited line shows it, and whether any line in V2 answers it. Where no line answers it, I concede.

## 1. Responses to criticisms of V2

### The idle rule cannot be reached (V1R1:47, V3R1:25)

Conceded in full. I checked the cause, not only the symptom.

- V2:145 says the rules apply in order and the first match wins.
- V2:155 is rule 7, the catch-all, which matches any row no earlier rule took.
- V2:156, the idle row, sits after rule 7. Under V2:145 no row can ever reach it.
- V2:58, the FR-003 AC, expects an idle row to appear. So the intent was a reachable idle class, and the table contradicts V2's own AC.

Root cause: a table-order drafting error, not a design choice. No line in V2 argues for idle after the fallback. The fix is V1's order (V1:153-154): idle is tested before the catch-all, and the catch-all stays last. I also add one AC to the merge: a fixture row that meets the idle condition and no earlier rule must classify as idle. That AC would have caught this defect, and V2:58 alone did not, because it asserts the output, not the rule order.

### From V1 (`round1-advocate-v1.md`)

1. **Null fencing let through on rule 2 (V1R1:46; X-002).** Conceded in Round 1 (V2R1, section 7). No change.
2. **Idle unreachable (V1R1:47; X-007).** See above. Conceded.
3. **WC-14 recommended actions (V1R1:48; X-003).** Conceded in Round 1. No change.
4. **The real-git allowance is session-wide (V1R1:49; X-010).** Conceded, new this round. V2:100 lets any `subprocess.run` with `argv[0] == "git"` through for the whole test session. That weakens the proof that the sweep never runs git outside `_git`, because a stray git call anywhere in a test would pass. The cause is that I wrote the exception at the session level to serve one control test (V2:98). Fix: the real-git exception applies to one marked control test only; every other test patches `subprocess.run` to raise on any call. This keeps V2's control experiment and removes the hole.
5. **Binary name, `orca` against `orca-ide` (V1R1:50; X-009).** Conceded in Round 1. No change.
6. **Extra git verbs (V1R1:51): `git log` per child (V2:200) and `--version` (V2:201).** Conceded. See section 2, C-010 and C-013, for the reasoning. Both verbs leave the allowlist; only `status --porcelain --branch`, one per worktree (V2:199), stays.
7. **No package `unknown` state, so an unreadable ledger falls into unfinished (V1R1:52; V2:164).** Conceded in Round 1 as the C-006 merge. V2:164 has no state for "ledger could not be read", so the only reachable state was unfinished, which states a fact the sweep did not observe. Take V1's `unknown`.

### From V3 (`round1-advocate-v3.md`)

8. **Null fencing (V3R1:23).** Same as item 1. Conceded in Round 1.
9. **WC-14 recommendations (V3R1:24).** Same as item 3. Conceded in Round 1.
10. **Rule 7 before idle, and no package unknown (V3R1:25).** Same causes as the idle section and item 7. Conceded.
11. **Rollback removes the ignore line while keeping reports; simultaneous publication is unspecified (V3R1:26).** Conceded in Round 1 (X-013, X-019). With the ignore line gone, kept reports under `.dev/sweeps/` become untracked files that a later `git add .` could stage, so the rollback contradicts itself. V2 has no line that answers it. Take V3's exclusive path reservation and collision suffix and V1's rollback text.
12. **The root method is "unspecified" (V3R1:76).** Contested. V2:203 specifies it: walk up from the current directory to the first `.git` entry with plain path reads, so no git call is needed. See section 2, C-012.

Net: of twelve items, eleven are conceded (two of them, items 4 and 6, new this round) and one is contested (item 12).

## 2. Response to the V1 rebuttal's open disagreements

V1R2:104-111 lists four open items. I now concede three and hold one.

### C-010, the git version gate (V1R2:22). Conceded.

My Round 1 claim (V2R1:46) was that on an old git "the safety flag silently does nothing". V1R2:22 names the flaw in that claim: a git that predates `--no-optional-locks` does not ignore an unknown global option, it rejects it, prints usage and exits nonzero. The failure is loud, and V1's failure path already marks that source unscanned. The silent case needs the environment variable sent without the flag, and neither V1 nor V2 ever does that (V2:176-177). So the gate in V2:180 prevents no unsafe outcome. It only rewords a failure that is already caught, and it costs a third git verb outside Seed:34.

The behaviour of an old git and its exit code are UNVERIFIED: no git was run in this debate, and V2:180 itself marks the first git version with the flag UNVERIFIED.

What I keep: the unscanned reason must name the git failure with a stable reason code (V3's U-025), so a person can tell "git failed" from "path missing". The isolated real-git control test (V2:98, now one marked test, section 1 item 4) still runs the flag against the host git, so a host git that rejects it fails a test before release.

### C-013 and the `git log` part of X-004 (V1R2:68). Conceded.

V2:200 adds one `git log <branch>..HEAD` per child worktree to count commits ahead. I tested it against its only consumer. Removable is never `yes` in Phase 1, so the count cannot change a verdict; it only decorates a "no". Seed:34 names `git status` of each worktree as the git input, and nothing else. A verb that changes no outcome and sits outside the seed's data model fails the least-surface rule that V2 itself used to cut the Orca allowlist (V2:193).

The one status call already carries part of the signal. The `--branch` header of `status --porcelain --branch` reports ahead and behind against the upstream, at no extra verb. Commits ahead of the feature branch, when there is no upstream, become could not determine with that reason in the note. This also turns C-009 into a merge: status as the only git verb, plus V2's path walk.

### C-023 and X-008, the periodic sweep (V1R2:69). Conceded to V3.

My Round 1 rows (V2R1:140, V2R1:173) cited Seed:36, "runs only when the coordinator calls it", as a reason not to require a periodic duty. V1R2:69 shows there is no conflict: a periodic duty in the coordinator's contract is still the coordinator calling the sweep. Seed:36 forbids a scheduler that runs the sweep without the coordinator, not a duty to call it.

The positive evidence is the owner order in this session's memory index: "keep a cron sweep and idle subscriptions on all peers". I read only the index line, not the memory file, so the order is UNVERIFIED. I take V3's limits with it (V3R1:45): contract text only, no scheduler in Phase 1 and no fixed cadence. Confidence stays modest because the source is an unread memory file.

### C-012, the root walk against `rev-parse` (V1R2:24). Held, with V1's addition.

V3 says the root method is unspecified and prefers one explicit `rev-parse` template (V3R1:76; V3 row C-012 V1, 86). The cause of that criticism is a missed line, not a gap: V2:203 specifies the walk, from the current directory up to the first `.git` entry, with plain path reads and no git call.

Why I still prefer the walk:

- Seed:34 names `git status` as the only git input. A `rev-parse` call is a second git verb, and the arguments that defeated `git log` and `--version` (section 2 above) apply to it equally.
- V1, whose text originally held `rev-parse`, now declines V3's defence of it (V1R2:24). Two of three advocates hold the walk.
- A failed walk has a safe outcome: no `.git` entry found means exit 2 with "no repository root", which the existing error path already covers.

V1R2:24 adds a real fix, and I take it. A linked worktree has a `.git` file, not a `.git` folder, so the walk must accept either. The merge AC: a fixture tree whose root holds a `.git` file resolves to that root, the same as a tree with a `.git` folder. Whether the walk should follow the `gitdir:` line in that file to the main repository is not needed for `--root` and stays out of scope.

### Other items I still hold, outside V1's list

- **X-006, archive-blocked as a named "no" reason.** V1 keeps this merge (V1R2:26); V3 wants V1's original text (V3R1:41). I hold the merge: it changes no verdict, since removable is never `yes`, and adds a reason a person can check.
- **X-001.** Settled across all three advocates (V1R2:111): disk-only exit 0 when Orca is unavailable, exit 2 for a confirmed missing binding. It still needs owner sign-off against the literal Seed:63.

## 3. Changed per-point rows

Old and new are given as "preferred, confidence". Only rows whose preferred position changed are listed.

| Point ID | Old | New | Reason |
|---|---|---|---|
| C-003 | merge V1+V3, 95 | merge V1+V2+V3, 90 | V1 adopted V2's note "Orca: exited; fenced evidence not readable" and a fixture-only label on rule 2 (V1R2:18) |
| C-009 | V2, 70 | merge V1+V2, 85 | `status --porcelain --branch` is the only git verb (V1's position); the root comes from V2's path walk (V2:203). `log` and `--version` leave (section 2) |
| C-010 | V2, 80 | V1, 70 | An old git rejects the unknown option loudly and the source goes unscanned (V1R2:22); the gate adds a verb outside Seed:34. Keep a stable git-failure reason code. Old-git behaviour UNVERIFIED |
| C-013 | V2, 65 | V1, 80 | `git log` per child changes no verdict while removable is never `yes`, and sits outside Seed:34 (V1R2:68) |
| C-021 | V2, 70 | merge V1+V3, 85 | My claim (V2R1:138) that only "apart from the header timestamp" is testable was wrong: with an injected `now` the timestamp is fixed too, so byte-identical report and JSON (V1R1:123; V3R1:85) is testable and stronger |
| C-023 | V1, 60 | V3, 60 | A periodic duty in the coordinator contract does not conflict with Seed:36 (V1R2:69); owner cron order in the memory index, UNVERIFIED; V3's limits apply (V3R1:45) |
| X-004 | V2, 65 | merge V1+V2, 80 | Same as C-009 and C-013: one status call per worktree, no `log`, root by path walk accepting a `.git` file or folder (V1R2:24) |
| X-008 | V1, 60 | V3, 60 | Same as C-023 |
| X-018 | V3 (with V1), 75 | V1, 80 | V1:152 (observed `guard refused:` body is finished) and V1:260 (unreadable contract is could not determine) already say what I credited to V3; V3 now takes V1's text (V3R1:43) |

Rows changed: 9.

Unchanged: all other rows

## 4. Changed A answers

| Point | Old | New | Reason |
|---|---|---|---|
| A-101 | REJECT | QUALIFY | V1R2:137 is right that V1's WC-14 text makes no lock-free claim, and V3 holds QUALIFY with the same named risk (V3R1:150). My REJECT aimed at a claim the merge need not make. Condition: any lock-free sentence in the merge (WC-9, NFR text) is scoped to direct `_git` calls only, and Orca read verbs' indirect git effects stay a named UNVERIFIED risk |
| A-103 | REJECT | QUALIFY | V1:148 already falls to could not determine when fencing is unreadable (V1R2:138), and V3 holds the same (V3R1:152), so REJECT changes no behaviour. Condition: per V1's new A-004 answer (V1R2:133), every live `exited` row keeps Orca's verdict in the note, and stalled (proved) stays fixture-only until a readable source is captured |

All other A answers are unchanged.
