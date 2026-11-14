# Round 2 Rebuttal: Variant 1 (opus, architect)

- Variant defended: V1 = `variant-1-opus-architect.md`
- Date: 2026-11-08 (from session context)
- Inputs read this round: `round1-advocate-v2.md` (230 lines), `round1-advocate-v3.md` (161 lines), V1 lines 130-157 and 205-249, `../../seed-brief.md` lines 33-38, plus my own Round 1 file. Nothing under `qa/`, no code, no live tool was read or run.
- Citation form: `V2R1:59` = line 59 of `round1-advocate-v2.md`; `V3R1:30` = line 30 of `round1-advocate-v3.md`; `V1:148` = line 148 of variant 1; `Seed:34` = line 34 of the seed brief.

## 1. Responses to criticisms of V1

Most of these criticisms were already conceded in my Round 1 file (section 5). I restate those briefly and spend the space on the ones that are new or that I still contest.

### From V2 (`round1-advocate-v2.md`)

1. **No Shift Brief and no next action (V2R1:59; also V2R1:229).** Conceded in Round 1 (my section 5, items 1 and 2). V1:208 claims the Shift Brief and V1:223-230 omit it; V1:228 has no next-action column. No counter-evidence. The merge takes V3's section list and its "next inspection" column.

2. **Stalled (proved) never appears on a live sweep, and V1 does not say so (V2R1:60).** Partly conceded, partly answered.
   - Counter-evidence: V1 does state the fact. V1:134 says `fenced_evidence` is "always `unreadable` on live rows in Phase 1", and V1:149 labels the `fenced` rule "synthetic fixtures only in Phase 1". So the behaviour is specified, not hidden, and it is the safe direction (Seed:56).
   - Concession: the label sits in the model, not on rule 2 itself (V1:148), and rule 2's note is "fenced evidence not readable" with no mention of Orca's own `exited` verdict. A reader of the report loses the strongest signal Orca gave. Two changes for the merge: (a) rule 2's condition cell adds "reachable only in synthetic fixtures in Phase 1"; (b) the note becomes "Orca: exited; fenced evidence not readable", and the FR-009 AC (V1:59) asserts that the note contains `exited`. This is V2's proposed note text (V2R1:78). It changes C-003 (section 3).

3. **Lock-freedom proved only by intent, and no git version gate (V2R1:61; strength claim at V2R1:46).**
   - The first half is conceded (Round 1, section 5 item 8): V1:82 checks only that the flag is at argv index 1. V2's isolated real-git control test (V2:98) goes into the merge.
   - The second half I still contest. V2R1:46 says that on an old git "the safety flag silently does nothing". That is not what an unknown global option does. A git that predates `--no-optional-locks` rejects the option, prints usage and exits nonzero, so the call fails loudly. (The exact exit code and the first git version with the flag are UNVERIFIED here, since no git was run in this debate.) V1's failure path already handles a failed `_git` call by marking that source unscanned. The environment variable on its own would be ignored silently, but V1 never sends it without the flag (V1:82). So the gate turns a loud failure into a nicer message, at the cost of a third git verb (`--version`). That verb is also outside Seed:34, which names `git status` as the only git input. C-010 stays V1.

4. **`rev-parse` is allowed but not needed (V2R1:62).** Already conceded in Round 1 (C-009, C-012 and X-004 all took V2's root walk). Seed:34 strengthens that concession: the seed's data model lists `git status` of each worktree as the git input and nothing else. V3 now argues the other way and defends V1's original `rev-parse` (V3R1:73, V3R1:76, V3R1:111). I decline that defence, even though it favours my variant: a path walk plus one status call per worktree is the smallest allowlist that matches Seed:34. The walk must accept a `.git` file as well as a `.git` folder, because linked worktrees use a file; that belongs in its AC.

5. **Archive-blocked does not block removal (V2R1:63).** Already conceded in Round 1 as a merge (X-006, merge V1+V2). V3 now backs V1's original reading (V3R1:41, V3R1:113). I keep the merge. Removable is never `yes` in Phase 1 (V1:202), so naming archive-blocked as a "no" reason changes no verdict. It only adds a named reason that a person can check, which costs nothing and follows Seed:27.

6. **No AC that `.dev/tasks/` stays tracked (V2R1:64).** Conceded, new this round. V1's FR-025 (V1:75) checks only the positive case, that `.dev/sweeps/x.md` is ignored. It does not check that the new line leaves `.dev/tasks/` tracked, which is an absolute rule in both CLAUDE.md files. Add V2's negative `git check-ignore` AC (V2:93) to FR-025. This maps to a unique point (U-015), not to an S/C/X row, so no row changes.

### From V3 (`round1-advocate-v3.md`)

7. **Shift Brief, waiting-on and next action missing (V3R1:30).** Same as item 1. Conceded in Round 1.

8. **Exact timestamp name does not establish no-overwrite (V3R1:31).** Conceded in Round 1 (section 5 item 4; X-019 and C-019 to V3). No counter-evidence: V1:210 names the path and nothing else.

9. **WC-14 end condition does not end for rejected results (V3R1:32).** Conceded in Round 1 (section 5 item 6; C-022). V1:240 says "until every Task it created has settled and been admitted", so a rejected result keeps the loop open forever. Take V3's "admission or rejection recorded" (V3:324-325).

10. **Structural tests are not runtime proof (V3R1:33).** Conceded. For git, see item 3. For Orca, no test in any variant can show that an Orca read verb never consumes messages or runs locking git internally. That is A-101, which stays QUALIFY with a named risk, not a release gate (X-016; V3 now drops its gate too, V3R1:42).

Net: of ten criticisms, eight are conceded in full (one of them, item 6, new this round) and two in part (items 2 and 3). The only part I still contest is the git version gate. Separately, I decline V3's defence of V1's original `rev-parse` (item 4).

## 2. Updated assessment of V2 and V3

### V2 after its concessions

V2 conceded its two safety defects and its one scope defect (V2R1:78-80):

- X-002: rule 2 let `consumer_fenced is None` through.
- X-007: idle came after the catch-all, so it could never match.
- X-003 and C-024: WC-14 recommended actions.

It also conceded the binary name (X-009), same-second collisions (X-019), unreadable-as-finished (X-018), the key name and the rollback (X-012, X-013), and several content rows (V2R1:81-90).

With those gone, V2 is no longer a candidate base. It is a strong source of tests and evidence, and every one of these should survive the merge:

- the real-git control experiment (V2:98);
- the negative `check-ignore` AC (V2:93);
- the `rule` plus `evidence` fields (V2:139-141);
- could not determine shown before working rows (V2:211);
- the failure-table columns and rated risks (S-007, S-008);
- OQ IDs (S-010).

V2's own count agrees: of its 30 OWN points, 11 are positions V1 already holds (V2R1:225).

Where V2 still disagrees with me:

- **C-010, the version gate.** See section 1, item 3.
- **C-013 and the `git log` part of X-004.** V2R1:130 and V2R1:169 want one bounded `git log` per child worktree. Seed:34 names `git status` as the git input. Removable is never `yes` (V1:202), so the commit count cannot change a verdict. It would add a verb outside the seed's data model to decorate a "no". I hold V1.
- **C-023 and X-008, the periodic sweep.** V2R1:140 and V2R1:173 now side with V1's "allowed, not required" and cite Seed:36. I conceded this point to V3 in Round 1, and I keep that concession. Seed:36 says the sweep "runs only when the coordinator calls it". A periodic duty written into the coordinator's contract is still the coordinator calling it, so there is no conflict. The owner order recorded in this session's memory index ("keep a cron sweep") favours V3. The memory file itself was not read, so that order is UNVERIFIED. V3 already limits the duty to contract text with no scheduler and no fixed cadence (V3R1:45).

### V3 after its concessions

V3 moved further than V2. It now takes:

- V1's skeleton: modules, typed models and idle order (V3R1:9, V3R1:39);
- V1's non-ready `task-list` read (V3R1:40);
- V1's package `unknown` and interrupted-archive states (V3R1:41);
- V1's pins and the guard-refused finished exception (V3R1:43);
- V2's disk-only exception when Orca is down (V3R1:37), which is V1's FR-019 (V1:69);
- V2's isolated real-git test (V3R1:44).

It also dropped its own two weakest parts:

- the fixed-base comparison (V3R1:38, C-007 and X-005);
- the live release gate (V3R1:42, X-016).

What remains distinctly V3 is the publication layer, and every part of it belongs in the merge:

- exclusive path reservation and collision suffix;
- JSON only after a successful write;
- the "Report complete" footer;
- byte limits;
- window exemptions for open waits;
- next inspection per session;
- the Shift Brief section;
- HTML neutralizing;
- symlink-safe `--output`;
- the WC-14 end condition.

V3's one remaining over-reach is the reverse of V2's. It now defends V1's `rev-parse` more strongly than I do (section 1, item 4).

### Where this leaves the merge

V3 now names V1 as the structural base (V3R1:9, "Prefer V1's structural skeleton"), and V2's steelman calls V1 "the variant most likely to still be correct after three later phases" (V2R1:28). The open disagreements have narrowed to four, none of them a safety defect:

- the git version gate (C-010);
- `git log` (C-013);
- the periodic duty (C-023 and X-008);
- the root walk against `rev-parse` (C-012). On this one, V3 sides with V1's text and I side with V2.

X-001 is now settled. All three advocates hold that an unavailable Orca gives a disk-only exit 0 and a confirmed missing binding gives exit 2. That is V1's FR-019 plus FR-002 (V1:52, V1:69). It still needs owner sign-off against the literal Seed:63 (V2R1:166).

## 3. Changed per-point rows

Old and new are given as "preferred, confidence". One row changes its preference; six change confidence only, because the other advocates moved to V1's position.

| Point ID | Old | New | Reason |
|---|---|---|---|
| C-003 | merge V1+V3, 90 | merge V1+V2+V3, 90 | Add V2's note text "Orca: exited; fenced evidence not readable" and a fixture-only label on rule 2 (V2R1:60, V2R1:78); section 1 item 2 |
| C-015 | V1, 55 | V1, 75 (confidence only) | V3 conceded the disk-only exception (V3R1:37); all three advocates now hold V1's FR-019 (V1:69) |
| X-001 | V1, 55 | V1, 75 (confidence only) | Same as C-015; owner sign-off against the literal Seed:63 is still needed (V2R1:166) |
| X-005 | V1, 80 | V1, 90 (confidence only) | V3 dropped its fixed-base comparison (V3R1:38); V2 holds the same (V2R1:170) |
| X-011 | V1, 80 | V1, 90 (confidence only) | V3 conceded the non-ready `task-list` read (V3R1:40); V2 agrees (V2R1:176) |
| X-016 | V1, 75 | V1, 90 (confidence only) | V3 removed its live release gate (V3R1:42); V2 agrees (V2R1:181) |
| X-018 | V1, 60 | V1, 75 (confidence only) | V3 now takes V1's guard-refused exception (V3R1:43). V2's "V3 (with V1)" (V2R1:183) is what V1 already says: an unreadable contract is could not determine (V1:260), and an observed `guard refused:` body is finished (V1:152) |

Unchanged: all other rows

## 4. Changed A answers

| Point | Old | New | Reason |
|---|---|---|---|
| A-004 | ACCEPT | QUALIFY | The rule is right, but V2R1:193 is also right that it has no live input in Phase 1. No allowlisted read is named as the source of `worker_done_seen`, and V1:134 says fencing is always `unreadable` on live rows. So every live `exited` row is could not determine, and the note must keep Orca's verdict ("Orca: exited; fenced evidence not readable"). Stalled (proved) is reachable only in fixtures until a source is captured (A-103) |

All other A answers are unchanged:

- **A-101 stays QUALIFY.** V2 answers REJECT (V2R1:207). V2's remedy is to name the risk, keep it out of the lock-free claim and test it later. V1's WC-14 text makes no lock-free claim (V1:240), so that remedy is already what QUALIFY does.
- **A-103 stays QUALIFY.** V2 answers REJECT (V2R1:209). V1:148 already falls to could not determine when fencing is unreadable, so a REJECT would change no behaviour.
- **A-107 stays REJECT.** V3 agrees (V3R1:156).
