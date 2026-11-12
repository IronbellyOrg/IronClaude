# Refactor Plan Review 2 (Step 4)

Abbreviations: A is the folder `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/adversarial/`. TL is the tasklist `TASK-RF-sweep-phase1-20261108-072653.md`. Reviewed file: `A/refactor-plan.md` (revised after review 1). Prior review: `A/refactor-plan-review.md` (B-1, B-2).

## Verdict

PASS. Zero blocking findings. B-1 and B-2 are both fixed as review 1 asked, the counts and the risk table agree with the register rows, and I found no regression from the two edits. Four minor notes are below.

## B-1 check

Result: fixed.

- The either-or is gone. Change 3 now allows exactly two extra commands in step (6): `echo "${XDG_STATE_HOME:-$HOME/.local/state}/ccsession/orca-tabs/"` and `ls -la <printed path>`. It says a literal file read cannot list the tab-map folder, so both commands stay.
- The four texts are edited together, and each citation is right when read against the tasklist:
  - (a) TL:1248 starts "The ONLY commands allowed". Confirmed.
  - (b) TL:1257 holds the Forbidden list and the tab-map folder sentence; TL:1258 holds Action step (6) with the `echo` and the `ls -la`. Confirmed. These are the two commands that conflict with the eight-template rule today.
  - (c) TL:1260 contains the exact phrase "one of the eight templates or a file read", so the proposed replacement has a real target. Confirmed.
  - (d) TL:1314 is the 7.24 lens ("every command in readonly-probe.md is one of the eight ALLOWED_ORCA templates of DESIGN 7.3 or a file read"). Confirmed.
- I searched TL for other copies of the command set ("eight templates", "ONLY commands", "or a file read", "orca-tabs"). The only other hits are TL:1523 (a code-probe lens about `probes.py`, unrelated), TL:1778 (a test fixture builder) and TL:1213. So the plan has not missed a fifth text.
- The sub-fixes carry through: command records on `$ ` lines (so the grep runs over commands, not stdout), `check` added to the TL:1260 grep to match the TL:1257 forbidden list, and the forbidden-list sentence handled.
- Would the fixed 7.16 check pass for a correct run? Yes. A correct run's commands are templates 1 to 8, the `echo`, the `ls -la`, and file reads of `package.json` and the tab-map files. After edits (a) to (d), each is accepted by TL:1248, TL:1260 and the 7.24 lens. None of them contains a forbidden token. Template 1 is `run-current` without `--json`, so it does not hit the `run-current --json` pattern. Stdout is excluded from the grep, so words like "check" in output do not trip it.
- DESIGN:894 ("read the files only") is left unedited. `ls -la` lists a folder rather than reading a file, so a strict reader could still flag it. This is minor (m-3).

## B-2 check

Result: fixed.

- F-10 is LOW in the register row and in the Change 10 heading. The row reads "(probe-sourced, INV-017; no card holds it, not calibrated)". Change 10's Source line repeats "probe-sourced; no card holds it, not calibrated".
- The gap is restated as the HALT-on-CHANGED gap. The register title is "Nothing HALTs when item 1.4 records an anchor as CHANGED". The false claim that item 1.3 does not compare is removed.
- TL:224 does compare. It says "If the HEAD sha does not start with `5dc29d23`, record the actual sha and add a note to `### Phase 1 Findings` that every research anchor must be re-checked against the new base". The live HEAD is `5dc29d23b15eb7db4ead50623bb409f696a0d7d3` (git rev-parse), so the plan's base is right.
- The claim that the HALT gap is real holds. TL:233 (item 1.4 Verification) handles only MOVED and a missing file ("If a file is missing, log the blocker ... and stop"). Nothing handles CHANGED. The debate transcript row for A-007 agrees: "TL:224 is a note, not a HALT".
- The fix is one sentence on TL:233, with the HEAD-compare and anchor re-run instructions deleted. This matches the fix review 1 gave.
- INV-017 in the probe is still MEDIUM, but the plan does not take that value, and its text says why (Change 10 Rationale). That is the labelling the brief asked for.

## Regression scan

- Register counts: rows F-01 to F-03 are HIGH (3), F-04 to F-09 are MEDIUM (6), F-10 to F-23 are LOW (14). Total 23. This matches the Overview line ("HIGH 3, MEDIUM 6, LOW 14") and the revision log.
- Change headings match the register: Changes 1 to 3 HIGH, 4 to 9 MEDIUM, 10 to 23 LOW. The Overview total of 25 holds: 23 findings plus Changes 24 and 25 for the two ledgers.
- Risk table: 25 rows, one per change. Row 3 is Medium and names all four texts (TL:1248, TL:1257-1258, TL:1260, TL:1314), matching Change 3. Row 10 is Low ("A CHANGED anchor is recorded but Phase 1 continues"), matching Change 10. The Overview "Overall risk: Moderate" is still fair.
- Base Weaknesses row for R2-G3 says "Allow the two step (6) discovery commands in all four texts together (Change 3)". Consistent with the new Change 3.
- "Changes NOT Being Made" and the other changes (1, 2, 12, 16 and the ledger changes) were not touched by the two edits. The Change 2 and Change 16 pair on item 8.3 and the Change 1 and Change 6 pair on item 7.4 are unchanged and still cross-referenced.
- No stale text about the removed fix remains: a search of the plan for "preferred option" finds nothing, and "HEAD" and "item 1.3" appear only in the corrected F-10 text and the revision log.

## Blocking findings

None.

## Minor notes

These never fail the review.

- m-1: In Change 3, the sub-bullet about the forbidden-list sentence is still an either-or ("Either add a step that writes the forbidden-list sentence into the probe file, or drop the expectation"). Both options work, but the plan's own Base Weaknesses table says either-or recommendations should become one option. Pick "drop the expectation and say the grep over command records finds nothing".
- m-2: The new check says a grep for `ls` or `echo` finds only the two step (6) commands. An unanchored `ls` can match inside other words. Anchor it to the start of a command record, for example `^\$ (ls|echo)\b`.
- m-3: The `$ ` command-record format is listed under "Also, with the same edit" and not in the (a) to (d) list, and it does not say which text carries it (TL:1258 is the natural one). DESIGN:894 still says "read the files only"; add a one-line note in the 7.24 lens that `ls -la` of that folder is the way to list the entries.
- m-4: Review 1's minor notes M-1 to M-7 were not applied (for example F-21 still cites TL:2677, and Change 1 item 7 still says "four lines everywhere", which conflicts with OQ-8's three lines). They were minor then and stay minor, but the executor of this plan should apply M-6 before editing the 7.22 lens.

## Self-audit

- Tasklist lines I read myself in this pass: 220-239 (items 1.3, 1.4), 1236-1271 (items 7.15 to 7.17), 1296-1316 (7.22 to 7.24), and 1523 (to rule out a fifth command-set text). DESIGN lines read: 884-897. Plan read in full (341 lines) in three chunks. I also read the whole of review 1.
- Commands run: `git rev-parse HEAD` (printed `5dc29d23b15eb7db4ead50623bb409f696a0d7d3`) and a directory listing. Greps over TL, the plan, the invariant probe and the debate transcript.
- Not verified: I did not re-check the other 21 findings' citations; review 1 did that, and these edits did not touch them. I did not run a probe, so "the fixed 7.16 check passes for a correct run" is reasoning from the line text, not an experiment. I did not re-count the 76 + 24 ledger rows.
- Where I looked hardest for a block: (1) a fifth copy of the command allowance in TL (none found), (2) the grep pattern accepting the `echo` and `ls` records (it does, once restricted to command records), (3) whether the F-10 HALT sentence has a real target at TL:233 (it does), (4) count drift between Overview, rows, headings and risk table (none).
- Nothing was staged, committed or edited outside this file.
