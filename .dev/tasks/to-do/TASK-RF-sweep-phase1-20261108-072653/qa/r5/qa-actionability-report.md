# QA Report: R5 actionability lens (doc-qualitative)

**Topic:** DESIGN `docs/designs/orchestrator-mode.md` as edited by item 6.3 (R5, `worktree ps --agent-wait` allowed)
**Date:** 2026-11-09
**Lens:** actionability. I act as the developer of `probes.py` and of WC-16 (step 1.17), reading DESIGN alone.
**fix_authorization:** false. No file edited except this report.
**Files read:** DESIGN lines 51-74, 157-222, 519-560, 668-710, 745-768 (line 759 is one very long row; I read it through Grep and Read), 800-860, 888-935, 1017-1048; OQ-1-agent-wait-decision.md (all 41 lines); r5-mechanical.md (all 90 lines); research/07 lines 100-135; WORKER-CONTRACT.md lines 106-113; SPEC lines 132, 143, 301, 323 and 487-512.

## Answers to the lens questions

1. Both `--agent-wait` templates are allowlisted by R5 and not called in Phase 1: clear in the code block (DESIGN 535-536, comments), D10 (837) and 15.1 (895). Whether anything stops a Phase 1 call is NOT clear (A1).
2. Step 1.0a runs only templates 1 to 8: stated at 895 and 851. The numbering is never defined in DESIGN (m1), and item 11 of the capture table reads as if it covered all templates (m2).
3. `FORBIDDEN_TOKENS` holds only `--include-remote`: clear and consistent at 539, 66, 837 and 1047. Where it is checked is thin (m5).

## Findings

### A1 (MAJOR): "not called in Phase 1" has no stated enforcement

- Evidence: DESIGN 535-536 say "not called in Phase 1". The same claim for `worktree list` and `worktree current` has a test: line 555 says "The NFR-003 recording test asserts zero argv for both", and line 759 repeats "zero argv for `worktree list` and `worktree current`". Line 759 mentions the agent-wait templates only in a positive case ("both `worktree ps --agent-wait` templates ... are accepted") and in the exact-set pin of ten. The full-sweep recording test checks only that each argv equals one template, so a recorded `worktree ps --agent-wait` would pass.
- Why it blocks: WC-16 (DESIGN 679) tells the person that `/sc:sweep` does not "run the `worktree ps --agent-wait` listing", and D6 (833) repeats it. Nothing in the test plan holds `probes.py` to that. The developer of `probes.py` or of `test_probes_allowlist.py` has to guess whether the recording test must assert zero agent-wait argv. The same developer can add a call and every listed test stays green, while WC-16 becomes false.
- Smallest fix: in 7.3 line 555 and in the section 11 `test_probes_allowlist.py` row, change "zero argv for `worktree list` and `worktree current`" to "zero argv for `worktree list`, `worktree current` and both `--agent-wait` templates".

### m1 (MINOR): "templates 1 to 8" and "9 and 10" are not defined

- Evidence: 7.3 (526-537) is an unnumbered tuple. 15.1 line 895 and the REPORT-difference row at 851 say "templates 1 to 8". The numbering only works as tuple position (1 `run-current`, 2 `worker-list`, 3 `worker-show`, 4 and 5 `task-list`, 6 `ps --json`, 7 `list`, 8 `current`, 9 and 10 the agent-wait pair). The exact-set pin (815) is order-free, so a reorder of the tuple silently changes what step 1.0a may run.
- Fix: in 15.1 line 895, replace "templates 1 to 8 of it" with "the first eight templates in tuple order (everything except the two `--agent-wait` templates)", or add "(listed in this order)" to the 7.3 intro.

### m2 (MINOR): capture item 11 and open item 10 read as covering all ten templates

- Evidence: 914 item 11 "Whether each template accepts its flags as written (exit 0 with parseable output) | NFR-014 pin" and 1000 (open item 10) "Whether each template accepts its flags as written ... A template that fails is dropped only with an owner note". Line 895 says 9 and 10 are not run. A 1.0a runner must guess whether "each template" includes them. Neither is marked UNVERIFIED in DESIGN. The OQ-1 live evidence (24 calls of `worktree ps --agent-wait` on one idle worktree) is not in DESIGN, and it says nothing about `--agent-wait --json`, so template 10 has no evidence at all.
- Fix: write "each of templates 1 to 8" at 914 and 1000, and add "templates 9 and 10 are unverified; they are not called, so no drop rule applies".

### m3 (MINOR): WC-16 (step 1.17) is not tied to D10

- Evidence: WC-16 text (679) says `/sc:sweep` does not "run the `worktree ps --agent-wait` listing". D10 (837) lists sections 2.2, 4, 7.3, 11, 12, 15.1, not 8. Nothing in section 8 or in the D10 row says this WC-16 sentence stays unchanged after R5, or that contract line 110 is not edited (OQ-1 line 41 says so, but it is in the task package, not DESIGN). The 1.17 developer reads D10 ("allowed") and the WC-16 sentence ("does not run") and has to work out for themselves that the two are consistent: allowlisted, not called.
- Fix: add one sentence to section 8 after the WC-16 text, for example: "R5 allows the listing in the allowlist only; the clause stays because `/sc:sweep` never calls it (7.3). Contract line 110 is not edited." Add "8" to D10's section list.

### m4 (MINOR): D10 omits SPEC line 301

- Evidence: SPEC 301 says "`task-list` has two forms, so there are eight templates". D10 (837) cites 310, 323, 500, 504, 510, 562, 619, 132 and 143, but not 301. A reader who works from the SPEC will see "eight" there with no deviation note.
- Fix: add "301" to the D10 SPEC line list.

### m5 (MINOR): where `FORBIDDEN_TOKENS` is applied is thin

- Evidence: GQ-109 (66) says "checked in every argv". The signature at 383 says `check_orca_argv` raises `ValueError` "unless an exact template match" and does not mention the token check. 384 `check_git_args` has no token mention. With a single token and exact-match templates, the set is redundant for rejection. The developer must guess whether the token check runs first (for a clearer error), whether it also applies to `_git`, and whether a later call of templates 9 and 10 would need the lock claim (NFR-015) revisited. SPEC 510 says `--agent-wait` turns on terminal wait-state reads, and the "unlikely" claim was not probed for it in the SPEC.
- Fix: add to 7.3, one sentence: "`check_orca_argv` tests `FORBIDDEN_TOKENS` first, then the template match; `check_git_args` has no token set."

## Checks

| ID | Check | Result |
|---|---|---|
| C1 | `FORBIDDEN_TOKENS` holds only `--include-remote`, consistent at 183, 539, 66, 837, 1047 | PASS |
| C2 | Both `--agent-wait` templates present in 7.3 and marked allowed by R5 and not called | PASS |
| C3 | "Not called in Phase 1" is backed by a stated test for the two agent-wait templates | FAIL (A1) |
| C4 | Step 1.0a is stated to run only templates 1 to 8, with the two agent-wait templates excluded (851, 895) | PASS |
| C5 | The numbering "1 to 8" and "9, 10" is defined in DESIGN | FAIL (m1) |
| C6 | Capture item 11 and open item 10 agree with 895 on which templates are exercised | FAIL (m2) |
| C7 | Section 4 line 221 extension-point rule names the R5 owner decision as an admission route | PASS |
| C8 | NFR-014 row (815) and D10 (837) both say ten templates, seven verbs, and no "eight" is left (r5-mechanical checks 9 and 12, plus 181 and 196) | PASS |
| C9 | GQ-109 row (66) matches 7.3 | PASS |
| C10 | Fix cycle 3 R5 row (1047) is consistent with the OQ-1 decision (kept pin, kept version-scoped claim) | PASS |
| C11 | Contract line 110 and research/07 line 117 agree with DESIGN's description of master's sweep (the `--agent-wait` listing is master's, not `/sc:sweep`'s) | PASS |
| C12 | A WC-16 developer can tell the "does not run the listing" clause stays after R5 | FAIL (m3) |
| C13 | D10 cites every SPEC line that carries the old rule or the eight-template count | FAIL (m4) |
| C14 | Where `FORBIDDEN_TOKENS` is applied (orca only, order against template match) is stated | FAIL (m5) |
| C15 | SPEC section 13 INV-005 sign-off (487-512) and NFR-014 (143) are recorded as superseded, with owner quote and date, in D10 | PASS |

Checks passed: 9 / 15. Checks failed: 6 (1 MAJOR finding, 5 MINOR findings).

## Self-audit

- Verified by my own reads: DESIGN 535-536, 539, 555, 759 (via grep and read), 837, 895, 914, 1000, 1047; OQ-1 lines 17-41; WORKER-CONTRACT 110; SPEC 132, 143, 301, 323, 500-510. I did not run any `orca` command or any network call.
- r5-mechanical.md reports 12 of 12 PASS, but those checks are grep counts. They cannot catch A1 (a missing test sentence), so I did not rely on them for that.
- The gate folder `qa/r5/` listing printed nothing before this write.

Verdict: FAIL
Blocking count: 1
