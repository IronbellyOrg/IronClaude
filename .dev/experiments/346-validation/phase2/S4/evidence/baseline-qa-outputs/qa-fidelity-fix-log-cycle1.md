# QA Fidelity Fix Log - Cycle 1 (Gate 4, source-document fidelity)

**Status:** Complete
**Date:** 2026-11-08

---

Target: `.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/RESEARCH-REPORT-bmad-first-use.md`. Input: `qa/qa-fidelity-consolidated-findings.md` (BLOCKING_COUNT 1: row 16). Rows 1-15 and 17-20 are MINOR and were not acted on.

## Finding 16 (IMPORTANT, blocking): deselected-bmad marker "permitted but not pinned"

Source re-read by this agent (read-only):

- `.github/contract-tests/test-startup-boot.sh:2446-2479`: the loop skips only in-profile slugs (2447-2449). For an out-of-profile slug it passes on `[ ! -e "$installed_dir/$slug" ]` (2456-2457) and otherwise `fail "out-of-profile marker PRESENT (should be absent): $slug"` with ledger `UNEXPECTED` (2475-2476). No `bmad` skip there.
- `test-startup-boot.sh:2498-2500` (reprofile loop, `[ "$slug" != bmad ] || continue`) and `2521-2528` (readiness loop, same guard) are the only places that skip `bmad`.
- `startup.sh:1113-1118`: comment at 1114 "BMad is an explicit owner-decision exception: its marker is never touched here"; the condition at 1116-1118 includes `[ "${aidev_cat_slug}" != bmad ]`, so no marker removal for bmad.
- `test-46-catalogue-health.sh:924-933`: fixture pre-seeds the bmad marker; pass requires `bmad.side` present and the bmad marker hash unchanged ("bmad marker untouched").

Edits to the report (all targeted Edits):

1. Section 2.5 live-boot paragraph (report line 430): replaced "It skips `bmad` in the deselected-slug loops (:2482-2528), so a deselected BMad marker is permitted but not pinned" with the code facts above (marker loop does not skip bmad; FAIL at 2475-2476; only :2500 and :2528 skip bmad; default plan never removes the marker per `startup.sh:1116-1118` and `test-46:929-933`). The "both can hold only because the live-boot HOME starts without a bmad marker" statement is labelled `[synthesis inference: ...]`; which profiles CI boots with is stated as UNVERIFIED (not read). The separate open question `sprint-status-orca-gap-closure.yaml:42` stays open.
2. Evidence list (report line 439): added `2446-2479` to the `test-startup-boot.sh` citation.
3. Section 8 Table 5.1 row `test-startup-boot:2446-2479, ...` (report line 1562): replaced "bmad is skipped (`continue`)" and "a deselected-bmad marker is permitted but not pinned" with: bmad is NOT skipped in 2446-2479, FAIL at 2475-2476, only 2500 and 2528 skip; note now "IF 4B: no bmad install marker may exist at boot when bmad is outside the booted profile (2456-2476)".
4. Step 4B.5 (report line 1498): added that the live-boot test pins an absent marker (2475-2476; loop 2446-2479), so no branch may write or keep a bmad install marker at boot, and that a marker-removal branch would contradict `test-46:929-933`; corrected the cite to `startup.sh:1116-1118`.
5. Section 9 row 7 (D-4, D-5, D-11; report line 1697): added to the Impact cell that either answer must keep a bmad install marker off the live-boot HOME when bmad is outside the profile (`test-startup-boot.sh:2456-2476`) and must account for `test-46:929-933`. The question itself and the "no removal by default" Resolution are unchanged; no owner decision was invented; Q1 and Q2 untouched.

Checked and left unchanged because they are true as written: the "marker never removed on deselection (`startup.sh:1116-1117`)" statements at report lines 221, 260, 737, 740, 1018, 1092, 1344, 1349, 1438, 1611 (they describe `startup.sh`, which is correct). Grep after the edits: no remaining "permitted but not pinned" or "bmad is skipped"; the one other "not pinned" hit (line 1405) concerns the markdownlint version and is unrelated. The Feasibility statement, 10-section structure, Table of Contents and all `[synthesis inference: ...]` labels were not touched.

## Not applied (out of scope by the binding scope guard)

- Research file 05 row a7 carries the same error (named in the proposed fix). Research files are read-only evidence for this task, so it was not edited. Report text no longer depends on it.

## Counts

- Blocking findings: 1
- Fixes applied: 1 (finding 16, five places in the report)
- Findings not fixed: 0
- Fixes applied + not fixed = 1 = BLOCKING_COUNT
- MINOR findings acted on: 0
