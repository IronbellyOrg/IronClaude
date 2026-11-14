# QA Report: R5 internal-consistency lens (Orca `worktree ps --agent-wait` allow edit)

**Date:** 2026-11-09
**Phase:** fix-cycle gate R5, internal consistency
**fix_authorization:** false (no file edited except this report)
**Target:** `docs/designs/orchestrator-mode.md` (1047 lines at read time)

Method: I read the DESIGN sections named in the brief from disk (sections 4, 7.3, 11, 12, 13, 15.1, 17, the GQ-109 row and `### Fix cycle 3`), plus grep over the whole file for `agent-wait`, `seven`, `eight`, `templates`, `forbidden`, `R5`, `unlikely`. I also read the SPEC lines (132, 143, 301, 310, 323, 500, 504, 510, 562, 619 and section 13), the OQ-1 record, `r5-mechanical.md`, research/07 lines 100-139 and `WORKER-CONTRACT.md` lines 106-113. I did not rely on the mechanical report or earlier QA; its grep claims were re-run.

## Summary of the search for a surviving prohibition

The DESIGN has 9 `agent-wait` hits (grep -c). Each one:

| Line | Text (short) | Forbids it? |
|---|---|---|
| 66 | GQ-109: "`--include-remote` is the only forbidden token ...; `worktree ps --agent-wait` is allowed (R5, owner 2026-11-08)" | No, allows |
| 535, 536 | Two `ALLOWED_ORCA` tuples, comment "allowed by R5 ..., not called in Phase 1" | No, allows |
| 679 | WC-16 text: `/sc:sweep` "does not ... run the `worktree ps --agent-wait` listing" | No. It says `/sc:sweep` does not call it; it does not say the verb is barred |
| 759 | Section 11: "a positive case that both `worktree ps --agent-wait` templates (with and without `--json`) are accepted" | No, allows |
| 833 | D6: "no `--agent-wait` listing" (same WC-16 sentence) | No (same reading as 679) |
| 837 | D10: "`worktree ps` never carries `--agent-wait`" is quoted as the SPEC text being changed | No, it is the SPEC side of the deviation |
| 895 | 15.1: "allowed by R5 but is not run in step 1.0a" | No |
| 1047 | Fix cycle 3 R5 row: RESOLVED, templates added, token removed, D10 | No |

No DESIGN sentence still forbids the flag. The sentences that sound close are 679 and 833, and they are consistent with the allow: WC-16 describes what `/sc:sweep` does (nothing with `--agent-wait`), and master's line 110 sweep keeps its own `worktree ps --agent-wait` listing (WORKER-CONTRACT.md:110, verified; research/07 line 117 quotes it correctly).

Cross-checks of numbers: `ALLOWED_ORCA` has 10 tuples (lines 527-536); the verb set is 7 (run-current, worker-list, worker-show, task-list, ps, list, current), matching the comment at line 537. Diagram lines 181 and 196 say 10. Section 12 NFR-014 row (line 815) says ten. Line 555 says "seven verbs and, since R5 ..., ten templates". Line 851 and 895 say "templates 1 to 8 of the ten": templates 1-8 are exactly the non-`--agent-wait` ones (agent-wait are 9 and 10), so the claim is correct. `FORBIDDEN_TOKENS` (line 539) holds only `--include-remote`, and section 4 line 221 and line 66 say the same. `grep 'eight'` finds only the D10 row (it says "not eight"). D1 to D10 are present and line 839 says "Total: 10 deviations." Line 1015 "Total: 23 open items." matches 23 rows.

## Findings

All are MINOR. None is a contradiction that forbids the flag.

**F1 (MINOR) The "not called in Phase 1" templates are pinned by a zero-argv test for two templates but not for the other two.**
- Evidence: `docs/designs/orchestrator-mode.md:759` ("zero argv for `worktree list` and `worktree current`") against `:535-536` and `:895` (the two `--agent-wait` templates are also "not called in Phase 1"); `:555` gives the zero-argv test as the reason the list/current templates are safe to leave pinned.
- Problem: same status ("pinned, not called"), different test treatment. Nothing fails if a later change starts calling `--agent-wait`, which is the one template whose lock effect the static trace never covered (SPEC:510).
- Smallest fix: add "and zero argv for both `worktree ps --agent-wait` templates" to the line 759 sentence.

**F2 (MINOR) Capture item 11 and open item 10 say "each template", but step 1.0a never runs templates 9 and 10.**
- Evidence: `:914` ("Whether each template accepts its flags as written"), `:1000` (open item 10, same words), against `:895` (1.0a issues only templates 1 to 8).
- Problem: the flag form of the two new templates is unchecked and no open item records that. SPEC:323 says a template that fails the capture is dropped, which cannot happen for these two.
- Smallest fix: reword item 11 and open item 10 to "each template that step 1.0a runs (1 to 8)".

**F3 (MINOR) D10's list of SPEC lines omits SPEC line 301.**
- Evidence: `:837` lists lines 310, 323, 500, 504, 510, 562, 619 and NFR-003/NFR-014; SPEC:301 says "so there are eight templates".
- Problem: the SPEC statement of the template count that D10 overrides is not in the deviation's citation list.
- Smallest fix: add 301 to the list in D10.

**F4 (MINOR) "R5" now names two different things in the DESIGN.**
- Evidence: routing row R5 at `:719`, `:951`, `:976` against the agent-wait decision at `:66`, `:221`, `:535-536`, `:895`, `:1047`. Line 221 uses a bare "(R5, 2026-11-08)" in section 4, where a reader has not met Fix cycle 3. (The R4 name collision predates this edit.)
- Smallest fix: write "fix cycle 3 R5" at `:66`, `:221`, `:535-536`, or rename the decision.

**F5 (MINOR) The kept lock claim has no sentence tying it to the new templates.**
- Evidence: lock line `:611` and the "version-scoped claim ... are kept" clause at `:1047`; SPEC:510 still says `--agent-wait` "turns on terminal wait-state reads" and was untraced; the 24-call probe is only in `OQ-1-agent-wait-decision.md:34-37`, not in the DESIGN.
- Problem: not a contradiction, since the sweep does not call the flag, but the DESIGN's own text gives no basis for the claim covering the new allowed forms.
- Smallest fix: one sentence in 7.3 citing the owner decision and the OQ-1 probe, or stating that the lock line covers only the verbs `/sc:sweep` calls.

## Checks

| ID | Check | Result |
|---|---|---|
| C1 | Section 4 line 221 extension-point rule is consistent with the allow edit (names R5 as a recorded owner decision) | PASS |
| C2 | Section 4 diagram labels (lines 181, 196) say 10 templates | PASS |
| C3 | 7.3 `ALLOWED_ORCA` contains both `--agent-wait` templates; count 10; 7 verbs; comment on line 537 correct | PASS |
| C4 | 7.3 `FORBIDDEN_TOKENS` holds only `--include-remote`; no conflict with any template | PASS |
| C5 | 7.3 line 555 (seven verbs, ten templates since R5) agrees with the sign-off wording | PASS |
| C6 | Section 11 negatives (line 759) do not include `--agent-wait`; positive case present and matches both templates | PASS |
| C7 | Section 11 exact-set pin says ten templates | PASS |
| C8 | Section 12 NFR-014 row says ten templates | PASS |
| C9 | Section 13 D10 matches 7.3 (ten, `FORBIDDEN_TOKENS` only `--include-remote`); total of 10 deviations correct | PASS |
| C10 | Section 15.1 line 895 and line 851 "templates 1 to 8 of the ten" correct and consistent | PASS |
| C11 | GQ-109 row (line 66) consistent with 7.3 | PASS |
| C12 | WC-16 text (679) and D6 (833) do not forbid the verb, only say `/sc:sweep` does not run it; consistent with WORKER-CONTRACT.md:110 and research/07:117 | PASS |
| C13 | `### Fix cycle 3` R5 row (1047) matches what the file now contains | PASS |
| C14 | No remaining "eight templates" or "never with --agent-wait" claim in the DESIGN outside the quoted SPEC side of D10 | PASS |
| C15 | Test plan covers every allowed-but-not-called template with a zero-argv assertion | FAIL (F1, MINOR) |
| C16 | Capture item 11 and open item 10 match the templates 1.0a actually runs | FAIL (F2, MINOR) |
| C17 | D10's SPEC citation list covers every SPEC statement of the old count/ban | FAIL (F3, MINOR) |
| C18 | Labels unambiguous (R5) | FAIL (F4, MINOR) |
| C19 | Lock claim basis stated for the newly allowed forms | FAIL (F5, MINOR) |
| C20 | OQ-1 record and `r5-mechanical.md` grep results reproduce against the file (9 hits, one `eight` hit, D10 total, line numbers) | PASS |

Confidence: Verified 20/20 | Unverifiable 0 | Unchecked 0 | Confidence: 100.0%
Tool engagement: Read: 12 | Grep: 5 | Glob: 0 | Bash: 4 (read-only awk, wc, grep, git status)

Minor findings F1 to F5 are notes and do not fail the gate.

Verdict: PASS
Blocking count: 0
