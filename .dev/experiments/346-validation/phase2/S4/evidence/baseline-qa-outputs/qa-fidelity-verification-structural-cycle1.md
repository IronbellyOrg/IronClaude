# QA Report - Gate 4 Fidelity Fix Verification (Structural, Cycle 1)

**Status:** Complete
**Date:** 2026-11-08
**Topic:** BMAD first-use directory creation in a project that never had BMAD
**Phase:** fix-cycle (Gate 4 fidelity), fix_authorization: false
**Inputs:** `qa/qa-fidelity-consolidated-findings.md` (BLOCKING_COUNT 1, row 16), `qa/qa-fidelity-fix-log-cycle1.md`, `RESEARCH-REPORT-bmad-first-use.md`

---

## Check (a): Blocking finding 16 re-verified against the ACTUAL source

Source re-read by me (not taken from the fix log):

| Claim now in the report | Source re-read | Result |
|---|---|---|
| Loop skips only in-profile slugs (:2447-2449) | `test-startup-boot.sh:2446-2449`: `for slug in $all_slugs; case " $profile_slugs " in *" $slug "*) continue` | PASS |
| Out-of-profile slug passes on `[ ! -e "$installed_dir/$slug" ]` (:2456-2457) | lines 2456-2457 | PASS |
| Otherwise FAIL `out-of-profile marker PRESENT (should be absent)` with ledger `UNEXPECTED` (:2475-2476) | lines 2475-2476 verbatim match | PASS |
| `bmad` is in the loop's slug set | line 1968: `all_slugs="claude-code ironclaude bmad mcp-bundle-core orca vibe-kanban test-slug"` | PASS |
| Only reprofile loop (:2498-2500) and readiness loop (:2521-2528) skip `bmad` | lines 2500 and 2528 carry `[ "$slug" != bmad ] \|\| continue`; no other bmad skip in 2446-2535 | PASS |
| `startup.sh:1116-1118` leaves the bmad marker alone; comment at :1114 says "BMad is an explicit owner-decision exception" | `startup.sh:1113-1118`: comment at 1114, condition includes `[ "${aidev_cat_slug}" != bmad ]` | PASS |
| `test-46:929-933` pins "bmad marker untouched" on a fixture that pre-seeds it | `test-46-catalogue-health.sh:922` hashes `${rp_inst}/bmad`; lines 929-933 assert the hash is unchanged and `bmad.side` present | PASS |
| `modules.tf:101-104` link-only removal; line 105 unconditional `rm -rf` of `~/.agents/skills/<s>` (carried in the edited 4B.5 cell) | `modules.tf:98-106` | PASS |

Report places edited by the fix (all re-read in the report file):

| Location | Re-read result |
|---|---|
| Section 2.5 live-boot paragraph, report line 430 | Old "permitted but not pinned" sentence gone; new text states the FAIL at :2475-2476 and the two skip loops, and labels the "both can hold only because" statement `[synthesis inference: ...]` with CI profiles marked UNVERIFIED. PASS |
| Evidence list, report line 439 | Now cites `2446-2479,2482-2528`. PASS |
| Section 8 Table 5.1 row, report line 1562 | States bmad is NOT skipped in 2446-2479, FAIL at 2475-2476, only 2500 and 2528 skip; note "IF 4B: no bmad install marker at boot when out of profile". Row has 5 cells like its neighbours (regex check). PASS |
| Step 4B.5, report line 1498 | Adds the live-boot constraint and the test-46 contradiction for a removal branch; row still has 4 cells (Step / Action / Files / Details). PASS |
| Section 9 row 7, report line 1697 | Impact cell adds the live-boot constraint; row still has 4 cells matching the Question / Impact / Suggested Resolution header; question and resolution unchanged. PASS |

Grep of the whole report for `permitted but not pinned` and `bmad is skipped`: no hits. Remaining `skip bmad` hits (lines 430, 1498, 1562) are the corrected statements. Result for check (a): finding 16 is fixed against the real source.

---

## Check (b): New blocking issues introduced by the fix

| Test | Evidence | Result |
|---|---|---|
| Broken structure / Table of Contents | Grep of `^#{1,3} ` headings: 10 numbered sections and all subsections still present; ToC (report lines 10-55) matches the headings (re-read lines 10-59) | PASS |
| Broken tables | Regex checks: rows 1498 (4 cells), 1562 (5 cells), 1697 (4 cells) match their table headers (`Step / Action / Files / Details`; Table 5.1 neighbours; `# / Question / Impact / Suggested Resolution`); no stray `\|` inside the edited cells | PASS |
| Placeholders | Grep for TODO, TBD, FIXME, XXX, PLACEHOLDER: only "placeholder trees" (lines 604, 645), a pre-existing technical term; `[...]` hits at 352 and 1579 were not in the edited cells | PASS |
| Contradiction between sections | Grep of "never removed" / "no removal": lines 737, 1018, 1092, 1438, 1611, 1697 describe `startup.sh` (true, re-read at :1113-1118) and none says the live-boot test permits a bmad marker; "permitted" appears only in line 430 as "pinned as absent, not permitted" | PASS |
| Distortion / phantom claim | Every line cite in the five edits was re-read against source (check (a)); the inference sentence is labelled `[synthesis inference: ...]` and states what was not read | PASS |
| Untouched elements | Feasibility statement (Section 7), `[synthesis inference]` labels elsewhere and Q1/Q2 not changed per grep of Section 7 and 9 headings | PASS |

Notes (not blocking, not counted):

- N1: Step 4B.5 says the live-boot test "pins the opposite" of "marker never removed". Looser than the precise wording used at lines 430 and 1562 (a marker on the live-boot HOME for an out-of-profile bmad FAILs); the cell then spells out the exact assertion, so no reader is misled.
- N2: Lines 1018, 1092 and 1611 cite `startup.sh:1116-1117` while the fixed text cites `1116-1118`; both ranges contain the `!= bmad` condition (the condition is on 1117; 1118 is the slug regex), so both are true.
- N3: Research file 05 row a7 still carries the original error. The fix log reports it was not edited under the scope guard and the report no longer depends on it; I did not read research file 05 and mark its current content UNVERIFIED.

---

## Self-Audit

What I actively checked (this run):

- Read in full: `qa-fidelity-consolidated-findings.md` (50 lines) and `qa-fidelity-fix-log-cycle1.md` (40 lines).
- Source files re-read: `test-startup-boot.sh:2436-2535` (loop 2446-2479, reprofile loop 2498-2508, readiness loop 2521-2535); Grep of `test-startup-boot.sh` for `all_slugs=` and `profile_slugs=` (lines 1968, 2016, 2018); `startup.sh:1105-1124`; `test-46-catalogue-health.sh:915-939` plus a Grep of `rp_inst` and `bmad` uses (lines 842, 905, 922, 931-932); `modules.tf:96-107`.
- Report lines re-read: 10-59 (ToC), 337, 430, 1498, 1560-1563 and 1697 in full; Grep with context for every occurrence of `D-5`, `never removed`, `no removal`, `2456`, `2475` and `live-boot`; Grep of all headings; regex cell-count checks on the three edited table rows.
- Searches run: `permitted but not pinned|bmad is skipped|2446-2479|2456-2476|2475-2476|929-933|2482-2528`; `skip(s) bmad|permitted|TODO|TBD|FIXME|XXX|PLACEHOLDER`; `^#{1,3} `.

Why zero blocking findings is credible: the original defect was a false statement about a pinned assertion. I located the exact lines (2446-2479) and confirmed each new clause against them: the loop does not skip bmad, FAIL at 2475-2476, only 2500 and 2528 skip. The one remaining claim that goes beyond code (live-boot HOME starts without a bmad marker) is labelled as an inference and its CI-profile dependency is marked UNVERIFIED rather than asserted. I looked specifically for the failure modes a fix of this kind produces: a stale duplicate of the old wording (none), a plan step that contradicts the corrected facts (4B.5 and row 7 are consistent with 1562), a table broken by an inserted `|` (none), and a ToC change (none). Not done: I did not run any test or read research file 05; I did not re-verify the pre-existing text of the report outside the five edited places or the 19 MINOR findings (out of scope).

Tool engagement: Read: 10 | Grep: 14 | Glob: 0 | Bash: 0. Verified: 14/14 checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%.

---

## Verdict

**VERDICT: PASS**

- Blocking findings from the consolidated list still unfixed: 0 of 1
- New blocking issues introduced by the fix: 0
- Notes: 3 (N1-N3, non-blocking)
- Severity counts: CRITICAL 0, IMPORTANT 0, MINOR 0 (notes excluded)
