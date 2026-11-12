# QA Report: R3-B1 evidence-quality lens

**Topic:** R3-B1 edits (items 2.1 to 2.6) to `docs/designs/orchestrator-mode.md`
**Date:** 2026-11-08
**Phase:** fix-gate review, evidence-quality lens (fix_authorization: false)
**Scope note honoured:** the R3-B2 forward reference "Several matching rows follow the R3-B2 rule below." (DESIGN:496) and the path-B-no-join transcript outcome are item 3.1 work and are not graded here.

## Method

Every Orca claim added by R3-B1 was traced to a research/04 evidence line. Because research/04 reads the bundle statically, I also re-read the cited Orca bundle (`/opt/Orca/resources/app.asar.unpacked/out/main/chunks/orcad-migration-source-retention-B_-OYaBD.js`, 2,654,414 bytes, version `1.4.245-aidev02.780594c521aa`, read-only `grep -b` and `dd`) to test research/04's own claims. That check found one research/04 claim that is wrong (F1).

## Claim-to-evidence map

| # | Claim added by R3-B1 | DESIGN line | research/04 evidence | Bundle re-check (this review) | Status |
|---|---|---|---|---|---|
| 1 | `worker-show` returns a `dispatch` object | 455, 887, 993 | 04:45 (`workerShow` returns `{dispatch: hG(i), ...}`) | `E6e` also returns `dispatch:hG(n)` (offset 1422525), so the context-only path has it too | Supported |
| 2 | `dispatch.dispatchedAt`, `dispatch.completedAt`, `dispatch.status` exist as names | 455, 496, 887, 993 | 04:46 (hG, @1422409, @1422438) | `hG` at 1421905 contains `status:e.status`, `dispatchedAt:e.dispatched_at`, `completedAt:e.completed_at` | Supported statically; live presence UNVERIFIED (04:128) |
| 3 | `dispatchedAt` is SQLite `YYYY-MM-DD HH:MM:SS` UTC | 468, 887 | 04:51 (both inserts `datetime('now')`) | `$nt` and `ert` inserts end `datetime('now')` (1629640 and 1630600 regions) | Supported for `dispatchedAt` only |
| 4 | `completedAt` is SQLite form (the shapes "the static bundle read gives") | 887 | 04:53 says the write was NOT found; 04:51 covers `dispatched_at` only | `completed_at` is written through the lifecycle projection with `new Date().toISOString()` at 12 sites, including `completed`, `failed` and `circuit_broken` (for example 1829430, 1832019, 1845401) | Unsupported and contradicted (F1) |
| 5 | Status values `pending`, `dispatched`, `completed`, `failed`, `circuit_broken`; `pending` and `dispatched` mean "not ended" | 496, 887 | 04:50 (schema), 04:52 | `status IN ('pending','dispatched')` guards at 1626324 and `pY` at 1637813 | Supported |
| 6 | Parser accepts SQLite and ISO forms | 468 | 04:129 | `pY` at 1637813 itself branches on `completed_at.includes('T')` | Supported |
| 7 | Fields are None for a row past the 50-call cap or a `call_failed` show | 455 | 04:54 (worker-show capped at 50); DESIGN:740 (60 rows give 50) | n/a | Supported |
| 8 | Orca version 1.4.245 | 455, 993 | 04:40 | `package.json` reads `1.4.245-aidev02.780594c521aa` | Supported |
| 9 | Python 3.10 `fromisoformat` rejects `Z` | 468 | not Orca; Python docs | n/a | Not an Orca claim; true |
| 10 | Names "confirmed by step 1.0a item 4" | 455, 496 | 04:128 says UNVERIFIED until 1.0a | n/a | Over-stated wording (F2) |
| 11 | `dispatchedAt` precedes the session's first transcript record (premise of the window) | 496 (implicit), 887 (as a capture question) | 04:51 asserts it; 04:131 hedges "worker-start path" | no `dispatched_at` update found, but `$nt` inserts a row for an existing assignee handle, whose session may predate the row | Unmarked premise (F3) |
| 12 | Transcript and Orca clocks agree | 496 (implicit: "compared as UTC instants") | 04:132 UNVERIFIED | n/a | Absent from DESIGN (F3) |

## Findings

### F1. MAJOR. `completedAt` shape claim is unsupported and contradicted

- **Evidence:** `docs/designs/orchestrator-mode.md:887` says the three fields are present "with the shapes the static bundle read gives (SQLite `YYYY-MM-DD HH:MM:SS` UTC)". research/04:51 supports that shape only for `dispatched_at`. research/04:53 states the `dispatch_contexts.completed_at` write was not found and is UNVERIFIED. Re-reading the bundle shows `completed_at` written with `new Date().toISOString()` (form `...T...Z`) at 12 lifecycle sites, including transitions to `completed`, `failed` and `circuit_broken` (for example offsets 1829430, 1832019, 1845401). `pY` at 1637813 branches on `includes('T')`.
- **What is wrong:** The sentence asserts a static-evidence shape for `completedAt` that no research/04 line gives, and the bundle shows ISO. It also sets the wrong expectation for the step 1.0a comparison. research/04:53 is itself wrong about "not found"; its text was carried into DESIGN as an unstated assumption.
- **Smallest fix:** Reword the 887 clause: "`dispatchedAt` in SQLite form `YYYY-MM-DD HH:MM:SS` UTC (static: `datetime('now')` at both inserts); `completedAt` form UNVERIFIED (the static read finds `toISOString()` writes, so both forms are possible and 7.2 accepts both); `status` one of `pending`, `dispatched`, `completed`, `failed`, `circuit_broken`".

### F2. MAJOR. UNVERIFIED marker removed; "confirmed by step 1.0a" reads as already done

- **Evidence:** DESIGN:455 ("names read statically from the Orca 1.4.245 bundle and confirmed by step 1.0a item 4, open item 23") and DESIGN:496 ("come from the static bundle read and are confirmed by step 1.0a item 4"). The old 496 sentence quoted at research/04:90 said "UNVERIFIED". `grep` of DESIGN for `UNVERIFIED` returns no hit at lines 455, 468, 496, 887 or 993. research/04:128 requires the live names to stay UNVERIFIED until step 1.0a.
- **What is wrong:** Step 1.0a has not run. The live field names, the live string forms and the live status values are unproved, yet two design sentences state them as confirmed with no UNVERIFIED label, and open item 23 (993) does not use the word. Only the section 17 preface carries the status. Note: the plan text (research/04:87, :90) prescribed this wording, so the defect originates in the plan, but the gate lens treats it as a defect in the edit.
- **Smallest fix:** 455: "names read statically from the Orca 1.4.245 bundle, UNVERIFIED until step 1.0a item 4 (open item 23)". 496: replace "are confirmed by step 1.0a item 4" with "are UNVERIFIED until step 1.0a item 4 confirms them (open item 23)". 993: start the item with "UNVERIFIED:".

### F3. MINOR. Three research/04 section 2.5 premises are not carried into the DESIGN as UNVERIFIED

- **Evidence:** research/04:130 (where and when `completed_at` is written, and its form), :131 (`dispatchedAt` precedes the first transcript record) and :132 (same host clock). DESIGN:887 turns the first two into capture questions, but DESIGN:993 (open item 23) names neither. The same-clock premise appears nowhere in DESIGN; line 496 states "Times are compared as UTC instants" and a skew claim without its premise. The federated-path caveat at 04:128 (`r8e`) is also not carried.
- **Why it matters:** research/04:51 asserts `dispatchedAt` is "before the worker pane runs its session" for both insert paths. `$nt` (offset 1629395) inserts a row for an existing assignee handle, whose session may predate the row, so the window can fail for dispatch-created rows. The design stays safe (no window gives could not determine), so this is not blocking.
- **Smallest fix:** Add to open item 23: "and that `dispatchedAt` is not later than the first transcript record of the session, and that host clocks agree; UNVERIFIED".

### F4. MINOR. The mechanical gate cannot catch F1 or F2

- **Evidence:** `r3-b1-mechanical.md` Checks 1 to 7 test field-name presence, counts, em-dash, TODO and totals only. None tests that UNVERIFIED survives at the claim sites.
- **Smallest fix:** Add a check that lines 455, 496 and 993 contain `UNVERIFIED`.

### F5. MINOR. Fixture realism for the window end

- **Evidence:** DESIGN:741 `test_path_b_terminal_row_without_end_has_no_window` uses status `completed` with `dispatch_ended` None, a state the bundle's lifecycle writes (completed_at set on `completed`, `failed`, `circuit_broken`) make unlikely. `test_path_b_window_inclusive_bounds` uses SQLite-form ends where real ends are ISO with milliseconds.
- **Smallest fix:** Keep the defensive fixture; add one ISO-with-milliseconds end to the bounds fixture.

## Supported claims (no finding)

Items 1, 2, 3, 5, 6, 7 and 8 in the map above are supported by a research/04 line, and the bundle re-check agrees. DESIGN:1013 correctly carries the cycle 2 m2 wording fix, and DESIGN:1023 lists the changes.

## Checks

| ID | Check | Result |
|---|---|---|
| C1 | Read every R3-B1-edited DESIGN region (58-61, 396-398, 447-515, 726-750, 866-901, 965-1023) | PASS |
| C2 | Line 455 field names and nesting trace to research/04 (04:45-46) | PASS |
| C3 | Line 455 "None for a row with no worker-show result" traces to the 50-call cap (04:54, DESIGN:740) | PASS |
| C4 | Line 468 time-parsing forms trace to evidence (04:51, 04:129, bundle) | PASS |
| C5 | Line 887 shape claim for all three fields is supported | FAIL (F1) |
| C6 | Status values and the pending/dispatched "open window" rule trace to evidence (04:50, 04:52) | PASS |
| C7 | Live-only claims stay marked UNVERIFIED at 455, 496, 887, 993 | FAIL (F2) |
| C8 | Every research/04 section 2.5 UNVERIFIED item reaches the DESIGN as UNVERIFIED | FAIL (F3, MINOR) |
| C9 | research/04 evidence offsets and statements re-checked against the bundle | FAIL (04:53 wrong; F1) |
| C10 | Version `1.4.245` claim | PASS |
| C11 | Mechanical result file reliable for evidence quality | FAIL (F4, MINOR; it checks names only) |
| C12 | Section 11 fixtures match supported shapes | PASS with note (F5, MINOR) |
| C13 | Fix cycle 3 row and cycle 2 m2 wording | PASS |
| C14 | R3-B2 forward reference excluded per scope note | PASS |

## Summary

- Findings: 2 MAJOR (F1, F2), 3 MINOR (F3, F4, F5), 0 BLOCKING.
- Confidence: Verified: 14/14 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (every check was done; the FAIL results are findings, not gaps in checking)
- Tool engagement: Read: 10 | Grep: 4 | Glob: 0 | Bash: 3 (read-only bundle inspection: `grep -bo`, `dd`, `ls`)
- Limits: I did not read DESIGN section 6 line 341 (cited by research/04:54 for the 50-call cap); the cap is confirmed through DESIGN:740 instead. Two `completed_at = datetime('now')` hits in the bundle were not attributed to a table, so F1 says "ISO at 12 sites", not "ISO only".

Verdict: FAIL
Blocking count: 2
