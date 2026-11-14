# QA Report: R5 numbers and metrics lens (doc-qualitative, adversarial)

**Topic:** R5 allow-`worktree ps --agent-wait` edit (item 6.3) in `docs/designs/orchestrator-mode.md`
**Date:** 2026-11-09
**Phase:** doc-qualitative, numbers lens (9-agent sizing: this is the domain lens agent)
**Fix cycle:** N/A (first review of this gate)
**fix_authorization:** false (only this report was written)

## Overall Verdict: PASS (with MINOR notes)

Every count the task named recounts correctly from the files on disk. No count is stale in a way that misleads. Five MINOR findings are listed; none fails the gate.

## Recount results (all read from disk this turn)

| Count | Claimed | Recounted | Evidence |
|---|---|---|---|
| `ALLOWED_ORCA` templates | 10 | 10 | DESIGN lines 527-536 hold 10 tuples; the comment at line 537 says `10 templates, 7 verbs` |
| `ALLOWED_ORCA` verbs | 7 | 7 | distinct (group, verb) pairs: run-current, worker-list, worker-show, task-list, ps, list, current |
| `FORBIDDEN_TOKENS` entries | 1 | 1 | line 539: `frozenset({"--include-remote"})`; one definition in the file |
| Template-count labels elsewhere | 10 | 10 | diagram lines 181 and 196, line 555, line 759, NFR-014 row line 815, D10 line 837, line 851, line 895, R5 row line 1047. No label still says 8 or eight as the current count; the only `eight` is D10's "not eight" (line 837) |
| `Total: 10 deviations.` | 10 | 10 | line 839; rows D1 to D10 (lines 828-837) = 10 |
| `Total: 23 open items.` | 23 | 23 | line 1015; rows 1 to 23 (lines 991-1013) = 23; unchanged by R5 |
| `### Fix cycle 3` rows | 5 | 5 | line 1037 heading; rows R3-B1, R3-B2, R3-B3, R4, R5 (lines 1043-1047) |
| Section 1 blocking findings | 3 | 3 | lines 7-11: R3-B1, R3-B2, R3-B3 |
| Em-dash count | 0 | 0 | `grep -c` and `grep -o | wc -l` both 0; en-dash also 0 |
| `agent-wait` hits | 9 lines | 9 lines | DESIGN lines 66, 535, 536, 679, 759, 833, 837, 895, 1047; none forbids the flag |
| SPEC lines that carry `--agent-wait` | D10 lists 9 | 9 | SPEC lines 132, 143, 310, 323, 500, 504, 510, 562, 619; D10 names exactly these (NFR-003 line 132, NFR-014 line 143, and the seven others) |
| SPEC NFR-014 (line 143) | seven verbs, eight templates | confirmed | so D10's "ten, not eight" is a real change, recorded as a deviation |
| `WORKER-CONTRACT.md` line 110 | one `worktree ps --agent-wait` per sweep | confirmed | and research/07 line 117 quotes the same chunk |
| OQ-1 | ten templates, still seven verbs | agrees with DESIGN | `OQ-1-agent-wait-decision.md` line 28 |
| r5-mechanical.md | 12 of 12 | all 12 re-derive | its figures (1047 lines, section 4 at lines 157-222, line 1037, lines 839, 1015, 221, 539, 532/535/536) match what I read |

## Findings

All MINOR.

- **N1 (MINOR), D10 breaks the section 13 intro.** DESIGN line 824 says "Each one comes from the PANEL, FIXREVIEW or the design review". D10's Source cell (line 837) is "Owner decision R5, 2026-11-08", which is none of the three. Smallest fix: add "or an owner decision" to line 824.
- **N2 (MINOR), "each template" is no longer true of step 1.0a.** DESIGN line 914 (capture item 11) and line 1000 (open item 10) speak of "each template" accepting its flags. Line 895 says step 1.0a issues only templates 1 to 8, so the two `--agent-wait` templates are never checked. Smallest fix: in line 914 and line 1000, write "each of templates 1 to 8", and say the two `--agent-wait` templates stay unchecked in Phase 1 (they are not called).
- **N3 (MINOR), r5-mechanical.md Check 1 does not account for all nine hits.** Line 77 sums to eight hits (five allowing, plus GQ-109, R5 and `/sc:sweep`). The ninth is the D6 row (DESIGN line 833), which also names `--agent-wait`. The conclusion holds; the breakdown is incomplete. Smallest fix: add the D6 line to the Check 1 text.
- **N4 (MINOR), OQ-1 lists fewer edited sections than were edited.** `OQ-1-agent-wait-decision.md` line 41 names sections 7.3, 11, 13 and 15.1 plus the GQ-109 row. The DESIGN R5 row (line 1047) lists seven sections (2.2, 4, 7.3, 11, 12, 13, 15.1). Section 4 (lines 181, 196, 221) and section 12 (line 815) were also edited. Smallest fix: update the OQ-1 sentence, or leave it as a plan statement.
- **N5 (MINOR), no test pins the two new templates as not called.** DESIGN lines 535-536 say "not called in Phase 1" and line 679 says `/sc:sweep` does not run the listing. Section 11 (line 759) asserts zero argv only for `worktree list` and `worktree current`. A recorded-argv assertion of zero for the two `--agent-wait` templates would pin the comment. Smallest fix: add that assertion to the `test_probes_allowlist.py` cell.

Also noted, not graded: the fix-cycle label R4 and R5 collide with the section 9 routing rows R4 and R5 (lines 718-719, 976). This predates R5 for R4, and the context makes each use clear.

## Checks

| ID | Check | Result |
|---|---|---|
| C1 | `ALLOWED_ORCA` holds ten templates (lines 527-536) | PASS |
| C2 | Those ten use seven verbs (comment line 537, recounted) | PASS |
| C3 | Every template-count label (181, 196, 537, 555, 759, 815, 837, 851, 895, 1047) says ten and none says eight as the current count | PASS |
| C4 | `FORBIDDEN_TOKENS` has one entry, and GQ-109 (line 66), D10, M1 and the R5 row agree | PASS |
| C5 | `Total: 10 deviations.` matches D1 to D10 | PASS |
| C6 | `Total: 23 open items.` matches rows 1 to 23 | PASS |
| C7 | `### Fix cycle 3` has five rows: R3-B1, R3-B2, R3-B3, R4, R5 | PASS |
| C8 | Em-dash count is 0 (en-dash also 0) | PASS |
| C9 | Step 1.0a "templates 1 to 8" selects the eight non-`--agent-wait` templates by list position | PASS |
| C10 | D10's nine SPEC line cites (132, 143, 310, 323, 500, 504, 510, 562, 619) are exactly the SPEC lines that carry `--agent-wait` | PASS |
| C11 | `WORKER-CONTRACT.md` line 110 and research/07 line 117 agree with the D6 and WC-16 sweep cadence text and with the allow decision | PASS |
| C12 | OQ-1 and r5-mechanical.md figures (ten, seven, 1047, 839, 1015, 221, 539) match the DESIGN | PASS |
| C13 | Section 13 intro sentence still true after D10 | FAIL (N1, MINOR) |
| C14 | "Each template" wording in items 11 and 10 still true after R5 | FAIL (N2, MINOR) |
| C15 | r5-mechanical.md Check 1 accounts for every hit | FAIL (N3, MINOR) |
| C16 | OQ-1's list of edited sections matches the edits made | FAIL (N4, MINOR) |
| C17 | A test pins the "not called in Phase 1" claim for the two new templates | FAIL (N5, MINOR) |

## Self-Audit

**(a) Reliance list:** no Inherited Structural Verdict was in the spawn prompt, so I relied on no rf-qa PASS and did my own structural counts. I did not trust r5-mechanical.md; I re-derived each of its figures.

**(b) Independent semantic checks:**
- Counted the template tuples, verbs, deviation rows, open-item rows and Fix cycle 3 rows with `awk` and `grep` over the DESIGN and compared them to each `Total:` line.
- Read SPEC lines 130-144 and 485-514 and grepped the SPEC for `agent-wait`, then compared the nine hits to D10's list.
- Read `WORKER-CONTRACT.md` line 110, research/07 lines 105-134 and `OQ-1-agent-wait-decision.md` in full.
- Read DESIGN lines 1-70, 155-230, 496-565, 676-680, 743-1047 in chunks of at most 150 lines (the long lines 498, 759 and 760 are single lines).

**Confidence:** Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 12 | Grep: 2 | Glob: 0 | Bash: 4. No web research was done.

Limits: I did not run `orca`, and made no network call. I only checked the lines the lens named, plus the places a template count could hide, so counts outside those (for example the seven `test_fr010_*` fixtures, which I counted once at seven) were not audited in depth.

Verdict: PASS
Blocking count: 0
