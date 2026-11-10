# QA Report - Gate 4 Fidelity Fix Verification (content quality, fix cycle 1)

**Status:** Complete
**Date:** 2026-11-08

---

Scope: the five edited places for blocking finding 16 (report lines 430, 439, 1498, 1562, 1697) against `test-startup-boot.sh:2440-2544`, `startup.sh:1105-1124`, `test-46-catalogue-health.sh:918-958`, and against each other. fix_authorization: false. STOP-AND-RE-SCOPE branch: not applicable (report line 1325 "Stop condition: not triggered"; `## 8. Implementation Plan` at line 1351).

## Check 1: marker statements agree with the test code

| Report place | Claim | Source read | Result |
|---|---|---|---|
| line 430 (Section 2.5) | the out-of-profile loop does not skip bmad; skips only in-profile slugs (:2447-2449) | `test-startup-boot.sh:2446-2449` | AGREES |
| line 430 | passes on `[ ! -e "$installed_dir/$slug" ]` (:2456-2457) | :2456-2457 | AGREES |
| line 430 | otherwise FAIL `out-of-profile marker PRESENT (should be absent): <slug>`, ledger `UNEXPECTED` (:2475-2476) | :2475-2476 (text and ledger string identical) | AGREES |
| line 430 | only the reprofile loop (:2498-2500) and readiness loop (:2521-2528) skip bmad | :2500 `[ "$slug" != bmad ] \|\| continue`; :2528 same guard; no other bmad guard in 2446-2544 | AGREES |
| line 430 | `startup.sh:1116-1118` leaves marker alone; :1114 quote "BMad is an explicit owner-decision exception" | `startup.sh:1113-1118` (`!= bmad` at :1117; comment :1114) | AGREES |
| line 430 | `test-46:929-933` pins "bmad marker untouched" on a pre-seeding fixture | `test-46:922, 929-933` (`rp_bmad` hash taken at :922; `bmad.side` and marker hash checked) | AGREES |
| line 430 | inference: both hold because live-boot HOME starts without a bmad marker | labelled `[synthesis inference]`; consistent with :2456-2476 and the fixture | AGREES (see N1) |
| line 439 | citation list now has `2446-2479` | cited range is the loop | AGREES |
| line 1498 (step 4B.5) | FAIL at :2475-2476, loop 2446-2479, only :2500 and :2528 skip bmad; no branch may write or keep a bmad install marker; removal branch contradicts `test-46:929-933`; cite `startup.sh:1116-1118` | same sources | AGREES (see N3) |
| line 1562 (Table 5.1) | bmad NOT skipped in 2446-2479; FAIL 2475-2476; only 2500 and 2528 skip; "IF 4B: no bmad install marker may exist at boot when bmad is outside the booted profile (2456-2476)" | same sources | AGREES (see N2) |
| line 1697 (Section 9 row 7) | either answer must keep a bmad install marker off the live-boot HOME when bmad is outside the profile (:2456-2476, FAIL :2475-2476) and account for `test-46:929-933` | same sources | AGREES |

Cross-agreement: lines 430, 1498, 1562, 1697 all state the same facts (not skipped in 2446-2479; FAIL 2475-2476; skips only at 2500 and 2528; default build never removes the marker; test-46:929-933 pins it untouched on a pre-seeded fixture). Grep for "permitted but not pinned", "is skipped (`continue`)" and "bmad is skipped": the old wording is gone. The "never removed on deselection (`startup.sh:1116-1117`)" statements at lines 221, 260, 737, 1018, 1092, 1438, 1611 describe `startup.sh` only, which is true (:1117 holds the `!= bmad` test), and none of them claims anything about the live-boot test. No contradiction found.

## Check (a): coherence with Sections 6, 7, 8, 9

The corrected fact changes a constraint on 4B.5 (and on any deselection branch that would touch the bmad marker), not the effort, risk or feasibility of an option: no option writes a bmad install marker at boot (4B writes a skill file; 4C edits the wrapper; 4D edits settings or a drop-in), and the default plan removes nothing. Section 6 option rows (e.g. line 1092) say only that the marker is never removed on deselection, which is true and was not claimed to be permitted by the live-boot test; no Section 6 or Section 7 ranking depended on the old "permitted but not pinned" sentence (Grep: the phrase occurs nowhere now). Section 8 (4B.5, Table 5.1) and Section 9 (row 7) carry the correction. COHERENT.

## Check (b): Feasibility statement and both owner questions

- Feasibility statement (report lines 1319-1325) is untouched by the five edits and still follows from its cited evidence: yes without a global install, yes without an IronClaude or IronOrca change, "Stop condition: not triggered". Section 9 row 4 restates it consistently.
- Owner Q1 (row 1) and Q2 (row 2) are still unanswered and still list the readings and mechanisms; they match task file lines 163 and 164 (user-level bootstrap artifact; what counts as first use: CLI command, slash skill, session in a project). Row 7's edit adds an Impact sentence only, its Resolution still says "Owner decision; the plan builds no removal by default", so no owner decision was invented. STILL CORRECT.

## Check (c): actionability of the added plan text

Step 4B.5 names the resource ("the same resource"), the files and lines to respect (`test-startup-boot.sh:2446-2479`, `2475-2476`, `startup.sh:1116-1118`, `test-46:929-933`, `modules.tf:101-105`), the default outcome (no removal) and the condition for a cleanup branch (owner answers D-5 "remove"). Table 5.1 row 1562 gives a KEEP verdict and the IF-4B constraint. Row 7 gives the impact and resolution. An implementer can act on all three. ACTIONABLE.

## Notes (MINOR, not blocking, not rechecked)

- N1 (MINOR). Report line 430 and Section 9 leave open which profiles CI boots ("stays UNVERIFIED"). It can be closed from files in the repo: both live-boot workflows boot the default `orca` profile (`coder-ci-validate.yml:259-265, 887`; `coder-ci-orca-boot.yml:186, 257`), and `profiles.yaml:14,18` puts `bmad` in `orca`. So the FAIL at `test-startup-boot.sh:2475-2476` is never reached for bmad in any CI live boot today; the pin is real in code but dormant until a boot with a profile that omits bmad (`minimal`, `profiles.yaml:19-21`) is added. The report's conditional wording ("whenever bmad is outside the booted profile", "IF 4B") is correct, so nothing misleads; it only understates how dormant the row is. Suggested: replace the UNVERIFIED clause with this observation.
- N2 (MINOR). The same loop also pins side markers: `test-startup-boot.sh:2450-2455` FAILs `out-of-profile side marker present: <slug>.*` for every out-of-profile slug, bmad included (`side_markers_absent`, :512-518). The Table 5.1 row 1562 text, step 4B.5 and row 7 say only "marker". No planned branch writes a `bmad.*` side marker, so no step changes; a one-clause mention would make the row complete.
- N3 (MINOR). Step 4B.5 says the live-boot test "pins the opposite" of test-46. They do not conflict (different fixtures: test-46 pre-seeds the marker, the live boot starts with none, as line 430 itself explains). Wording only.
- N4 (MINOR). Line 430 carries the process phrase "re-read in fidelity cycle 1" inside a research report; harmless, but it is pipeline history, not evidence.

## Issue summary

| Severity | Count |
|---|---|
| CRITICAL | 0 |
| IMPORTANT | 0 |
| MINOR (notes) | 4 |

Unresolved or new blocking issues: none. Finding 16 is resolved in all five places.

## Self-Audit

Files and lines read this run: `qa-fidelity-consolidated-findings.md` (all 50 lines); `qa-fidelity-fix-log-cycle1.md` (all 40); `test-startup-boot.sh` 2430-2544 and 508-518 (loop, reprofile, readiness, `side_markers_absent`) plus a Grep for `all_slugs`, `profile_slugs`, `installed_dir`; `startup.sh` 1105-1124; `test-46-catalogue-health.sh` 918-958; `profiles.yaml` 10-24; Grep of `coder-ci-validate.yml` and `coder-ci-orca-boot.yml` for the booted profile; report lines 329, 425-440, 1092, 1318-1328, 1340-1349, 1385-1387, 1425-1427, 1490-1503, 1534-1536, 1555-1568, 1611, 1685-1712; task file lines 160-165. Searches: Grep of the report for "permitted but not pinned", "is skipped", "never removed", "1116-1117/1118", "2446-2479", "2456-2476", "2475-2476", "out-of-profile", "deselect", "live-boot" (every hit classified). Claims reproduced from source: all eleven rows of Check 1 (line numbers, strings, ledger text). I believe the blocking count of zero is right because every statement the fix wrote was compared with the exact test lines and agreed, the old false wording is absent, the five places say the same thing, and the three unedited statements of the same topic (lines 221 to 1611) are about `startup.sh` and true. I do not claim the report is flawless: I found four MINOR notes, including one (N1) that the fix left UNVERIFIED although the repo answers it. Not observed: no test or CI run was executed; research file 05 row a7 (same error, not edited by design) was not read; behaviour of a real boot with `minimal` is UNVERIFIED.

## Verdict

PASS
