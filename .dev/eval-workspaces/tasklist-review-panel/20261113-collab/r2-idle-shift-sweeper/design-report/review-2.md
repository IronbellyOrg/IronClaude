# Review 2 of DESIGN.md (Redesign 2, Idle-Shift Sweeper): re-check of B-1..B-8

Reviewer: independent (did not write the design). Date: 2026-11-14.
Document: `R2/DESIGN.md` (750 lines, read in full this run). Prior review: `design-report/review-1.md` lines 1-70.
Scope: (1) is each of B-1..B-8 fixed; (2) did the edits introduce a new blocking defect or leave a contradicting sentence.
Grading: blocking = wrong behaviour, false claim, missing required deliverable, security or data-loss risk; anything else is a note.

## Prior findings

- B-1 fixed. 2.8 row "No ground truth or other outputs read" (line 393): "Only the **tool inputs** of `assistant` entries are audited (Read `file_path`, Bash `command`, Grep/Glob `path` and `pattern`), never the whole transcript", path patterns `*/ground-truth*.json`, `*/20261111-a1/*`, `*/20261113-collab/*`, `*/.dev/reflect/*`, `SBR/board/*` for reviewers only, and a clean fixture with a hook entry and a "scoring" sandbox file "which must pass". 2.4 sweeper audit (line 263) is now "any sweeper tool input (2.8 rule: tool inputs only)".
- B-2 fixed. 5.2 step 4 (line 538): self-check is `'"origin"[[:space:]]*:|...'`, "Only the key form of `origin` is checked"; `test_anon.py` (line 607): "an anchor quoting "original" passes the self-check".
- B-3 fixed. 2.2 H2 step 2 (line 198): "re-asks once, under the same hang deadline (`timeout <deadline - now>`; exit 124 logs `hang_kill: true` and `slo_breach: true`)"; 6.2 row "Re-ask hangs ... in both switches" (line 634).
- B-4 not fully fixed. The behaviour is fixed: rule 11 (line 244) "the sweeper's posts and the harvested facts together (`from` in `{sw-1, hv-1}`) are at most 2k per package, counted under the board lock", and harvest step 6 (line 292) "under the shared 2k cap". But the requested test of the shared cap is missing and an old sentence survives; see N-2.
- B-5 fixed as written. 5.1 step 0 (line 509): on resume `runid`, `opaque`, `panel`, `panel_collab`, `sweeper_model` are read back, merge/anonymise/judge are skipped when `merged-1.md` / label dir / `score.json` exist; step 1 (line 510) "On a first launch only"; step 4 (line 523) "created once per row in step 1"; test in `test_preflight.py` and 6.2 row "Resume after interruption" (line 636). The fix introduced N-1.
- B-6 fixed. AC-2 (line 674): `find REPO/src EVAL -type f -newer <stamp>` against a stamp created before the tests and smoke runs; "`git status` is not used".
- B-7 fixed. AC-2b (line 675): "Every reviewer meta of every smoke package has `dropped_lines == 0`, and every `.reask.jsonl` that exists parses with `jq -s` and gives `model_ok: true` through the `RR:50-52` filters".
- B-8 fixed. `test_summarize_arm.py` (line 605): "wrong blockers: an arm mean of A1 + 1.01 fails the arm, A1 + 1.0 does not ... flood: facts at the cap with uptake below 0.5 is reported and does not stop the arm"; 6.2 row "Wrong blockers rise" (line 635).

## New blocking findings

### N-1 (blocking): a resumed launch re-runs an incomplete package on the old run id's stale sandbox and board

- Where: 5.1 step 0 (line 509) together with 2.1 "Per-run sandbox" (lines 153-161), 2.3 board layout (lines 205-217) and 2.5.1 steps 7 and 9 (lines 317, 319).
- Defect: the B-5 fix keeps `runid` on resume and re-runs a package without `DONE` after moving only `runs/<row>/<pkg>` aside. The sandbox `SBR/sb/<runid>/<pkg>/` and the board `B = SBR/board/<runid>/<pkg>/` are keyed by the same `runid`, so they still hold the interrupted attempt's state: `board.jsonl` facts, `state/<rid>.calls`, `state/<rid>.delivered`, `state/<rid>.sealed`, `finish_sent`, `seq`, `opened.txt`. Before the fix every launch had a new `runid`, so this could not happen.
- Consequence: on the re-run, a receiver whose `delivered` already has k lines gets no fact (step 7); a receiver whose `sealed` exists is not sealed again (step 9), so `B/snap/<rid>.jsonl` is the old session's transcript and the independence evidence is wrong; the call counter starts above 6; old facts are dealt again. In the sandbox, `git commit -qm snap` on an unchanged existing repo exits 1 ("nothing to commit"). The package is silently a different treatment from a first run.
- Fix: when a package without `DONE` is re-run, also move `SBR/sb/<runid>/<pkg>` and `SBR/board/<runid>/<pkg>` to `<same>.incomplete-<UTC>` (quarantine, never delete) before `run-package.sh` rebuilds them, and add that to the 6.2 "Resume after interruption" row: kill during package 1's reviewers, resume, assert a fresh board (no `delivered`/`sealed` from the first attempt) and a new seal hash.

### N-2 (blocking): the shared 2k cap has no test, and a leftover sentence still names a separate "hv cap"

- Where: 6.1 `test_harvest_hook.py` (line 599): "the hv cap holds"; 6.1 `test_validate_msg.py` (line 596): "the 2k+1-th sweeper post (`over_cap`)"; 6.2 "Sweeper floods" (line 622): "fake sweeper posts 3k facts".
- Defect: rule 11 now caps `sw-1` and `hv-1` together, but "the hv cap holds" still describes a cap of the harvested facts alone, and every cap test posts only one source. An implementation with two separate 2k counters (the B-4 defect) passes all listed tests. B-4's own fix asked for "a test where 2k mixed posts fill the cap"; it is absent.
- Consequence: R-18's board-count verification (at most 2k facts per package) is not tested; the original 4k-facts defect can return unnoticed.
- Fix: replace "the hv cap holds" with "harvested facts count toward the shared 2k cap" and add a case to `test_validate_msg.py` (or `test_harvest_hook.py`): k sweeper posts plus k harvested posts fill the cap, and the next post from either `sw-1` or `hv-1` is rejected `over_cap`.

## Notes (minor)

- n-1: 2.8 row "Independent first pass" (line 387) cites "receiver hook step 6" for the seal; the seal is now step 9 (step 6 is only the fail-closed exit). Appendix A R-10 (line 729) "2.5 step 6" and R-19 "steps 5-6" have the same stale numbering.
- n-2: 2.8 says `test_audits` includes the clean hook/"scoring" fixture, but the 6.1 `test_audits.py` row (line 609) does not list it; AC-1 checks "every test in 6.1 and 6.2", so list it there too.
- n-3: 2.8 exempts "the sweeper's calls of its own `B/bin/panel-post`" from `*/20261113-collab/*`, but `B` is under `SBR` (`/tmp/evalsb-collab-r2`), so that exemption never applies. Harmless; reword or drop.
- n-4: AC-2's `find ... -newer <stamp>` over `EVAL` and `src` can fail falsely if another session writes into `EVAL` during the smoke runs, or if importing `superclaude.cli.review.findings` rewrites a stale `.pyc` under `src/.../__pycache__/`. Exclude `__pycache__` (or set `PYTHONDONTWRITEBYTECODE=1`) and run the smoke when no other writer is active.
- n-5: the leftover searches came back clean apart from N-2 and n-1: no "seal on call 6" (line 598 now reads "seal written and hashed in the same call as, and before, the first delivery ... never before call 6", which agrees with step 9), no bare `origin` self-check, no whole-transcript token audit, and no `git status --porcelain -- src EVAL`.

## Verdict

verdict: FAIL

Of the eight prior findings, 7 are fixed and 1 is not fully fixed (B-4: the behaviour is fixed, but its test is missing). There are 2 new blocking findings (N-1 from the B-5 resume fix, N-2 the leftover "hv cap" sentence and the missing test) and 5 notes.

What I checked: all of DESIGN.md (lines 1-750) against review-1.md B-1..B-8 (lines 1-70); a grep of the whole document for leftovers (`hv cap`, `hv-1`, `call 6`, `6th`, `origin|`, `grep -cE`, `git status`, `incomplete`, `whole transcript`, `step 6`/`step 9` cross-references); and how the resume path in 5.1 step 0 interacts with the runid-keyed sandbox and board in 2.1, 2.3 and 2.5.1. I did not re-open MR or the source scripts, because the B-n evidence in review-1 was taken as given.
