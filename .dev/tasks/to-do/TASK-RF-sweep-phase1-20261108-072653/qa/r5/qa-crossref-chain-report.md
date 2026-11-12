# QA Report: R5 cross-reference chain (agent 7 of 9, rf-qa-qualitative, crossref-chain lens)

**Topic:** `--agent-wait` decision (R5) and INV-005, traced through DESIGN sections 4, 7.3, 11, 12, 13 (D10), 15.1 and 18, the GQ-109 row and the OQ-1 record
**Date:** 2026-11-09
**Phase:** doc-qualitative, cross-reference lens
**Fix cycle:** N/A (first review; `fix_authorization: false`)

DESIGN on disk is `docs/designs/orchestrator-mode.md`, 1047 lines (the task text says 1013 at build time; 1047 matches `r5-mechanical.md`). I read it in chunks of at most 150 lines. I did not trust `r5-mechanical.md`; I re-ran its greps (the same counts and line numbers came back).

## Chain traced

1. SPEC `merged-requirements.md` section 13 (line 477), INV-005 condition 1 (lines 493-504, "`worktree ps` (never with `--agent-wait`)", line 500); NFR-014 (line 143); NFR-015 (line 144).
2. Master `WORKER-CONTRACT.md:110`: "one prompt-wait listing (`worktree ps --agent-wait`)". `research/07:117` quotes it verbatim.
3. `OQ-1-agent-wait-decision.md`: allow, "Allow it, no conditions needed."; run `run_93bfa00cae2b`; messages `msg_d95a87e312e1`, `msg_6ee5998d0874`.
4. Task item 6.3 applies it to DESIGN. Task Execution Log row 2807 records it. `r5-mechanical.md` checks it.
5. DESIGN landing points: line 66 (GQ-109), line 221 (section 4), lines 535-537 (7.3), line 539 (`FORBIDDEN_TOKENS`), line 555 (M3 paragraph), line 759 (section 11), line 815 (section 12), line 837 (D10), line 895 (15.1), line 1047 (Fix cycle 3 R5).

## Items Reviewed

| Link | Result | Evidence |
|---|---|---|
| OQ-1 "SPEC section 13, NFR-014" and "condition 1" | Exists, says what is claimed | SPEC 477, 495-504 (condition 1 forbids `--agent-wait`), 143 (NFR-014 "never carries `--agent-wait`") |
| OQ-1 `WORKER-CONTRACT.md:110` | Exists, matches | `WORKER-CONTRACT.md:110` holds `one prompt-wait listing (\`worktree ps --agent-wait\`)` |
| research/07 line 117 | Exists, matches | `research/07:117` is the second quoted chunk of the `:110` paragraph, character for character |
| research/07 `:151`, `:122` | Match | `WORKER-CONTRACT.md:151` L1 probe row and `:122` S4 `agentWait` row are as quoted |
| OQ-1 "ten templates, still seven verbs" | Matches DESIGN | DESIGN 526-537: 5 orchestration + 5 worktree = 10 templates; verbs run-current, worker-list, worker-show, task-list, ps, list, current = 7 |
| OQ-1 ids vs task file | Match | Task line 984 and Execution Log row 2807 cite both messages; the quote is identical |
| OQ-1 "WORKER-CONTRACT.md:110 is not edited" | True | `git status` shows no change to `WORKER-CONTRACT.md` |
| DESIGN GQ-109 row anchors | Exist | SPEC 562 is the GQ-109 row; SPEC 143 is NFR-014; GAPS 132 is the GQ-109 row |
| D10 cited SPEC lines 132, 143, 310, 323, 500, 504, 510, 562, 619 | All exist and carry `--agent-wait` | A grep of SPEC for `agent-wait` returns exactly these 9 lines (132, 143, 310, 323, 500, 504, 510, 562, 619); none is missing from D10 |
| D10 and R5 row section lists | Match the edits | D10 "2.2, 4, 7.3, 11, 12, 15.1": lines 66, 221, 535, 759, 815, 895. R5 row adds 13 (D10 itself) |
| Section 4 line 221 | Present once | "recorded owner decision (R5, 2026-11-08)" at line 221 |
| `FORBIDDEN_TOKENS` | `{"--include-remote"}` only | line 539 |
| Step 1.0a "templates 1 to 8" | Correct | The first eight tuples at 527-534 are 1 to 8; the `--agent-wait` pair at 535-536 are 9 and 10; line 895 says so |
| Counts | Correct | `Total: 10 deviations.` at 839 (D1 to D10 present); `Total: 23 open items.` at 1015 |
| No sentence still forbids the flag | Confirmed | All 9 DESIGN hits of `agent-wait` (66, 535, 536, 679, 759, 833, 837, 895, 1047) allow it or say `/sc:sweep` does not run it (679, 833, consistent with each other and with D6) |
| No stale "eight" or "seven templates" | Confirmed | Only line 837 says "ten templates, not eight"; line 555 says "seven verbs ... ten templates" |

## Findings

No BLOCKING or MAJOR finding. Every cited section, line and condition number exists and says what is claimed. The findings below are MINOR.

**F1 (MINOR). "Not called in Phase 1" is claimed in four places but pinned by no test.**
Evidence: DESIGN 535-536 (`not called in Phase 1`), 679 (WC-16: `/sc:sweep` does not "run the `worktree ps --agent-wait` listing"), 833 (D6), 895 (not run in 1.0a). The test row at 759 asserts "zero argv for `worktree list` and `worktree current`" and a positive acceptance of both `--agent-wait` templates. Line 555 repeats "asserts zero argv for both", where "both" means list and current. Nothing asserts zero `--agent-wait` argv in the full-sweep recording, so the WC-16 sentence (a contract text) is unpinned. The static addendum at SPEC 510 gives the reason `--agent-wait` was forbidden ("turns on terminal wait-state reads").
Smallest fix: at line 759, extend "zero argv for `worktree list` and `worktree current`" to "zero argv for `worktree list`, `worktree current` and both `--agent-wait` templates".

**F2 (MINOR). D10 does not cite SPEC line 301, which still says "eight templates".**
Evidence: SPEC 301 reads "`task-list` has two forms, so there are eight templates." D10 (DESIGN 837) lists the nine `agent-wait` lines and says "ten templates, not eight" for the NFR-014 pin, but line 301 is the only SPEC "eight" that is not on its list. SPEC 143 is covered.
Smallest fix: add "301" to the SPEC line list in D10.

**F3 (MINOR). Capture item 11 and open item 10 say "each template", but step 1.0a runs only templates 1 to 8.**
Evidence: DESIGN 914 ("Whether each template accepts its flags as written ... Feeds NFR-014 pin"), 1000 (open item 10, "Closed by Step 1.0a item 11"), against 895 ("issues only templates 1 to 8"). Templates 9 and 10 are never run, so those two rows cannot close for them.
Smallest fix: at 914 and 1000, write "each of templates 1 to 8; templates 9 and 10 are allowed by R5 and not run in Phase 1".

**F4 (MINOR). The OQ-1 "Applied by" paragraph lists fewer sections than item 6.3 edited.**
Evidence: `OQ-1-agent-wait-decision.md:41` names "DESIGN sections 7.3, 11, 13 and 15.1 plus the GQ-109 row". Task item 6.3 (task line 1000) and the DESIGN also edit section 4 (line 221), section 12 (line 815) and `### Fix cycle 3` (line 1047). The OQ-1 record is not authoritative on the edit list, so no claim is false, but the two lists differ.
Smallest fix: add "4, 12 and the `### Fix cycle 3` table" to line 41 of the OQ-1 record, or say "among others".

**F5 (MINOR). The label "R5" has two referents in DESIGN.**
Evidence: owner decision R5 at 66, 221, 535-536, 555, 837, 895, 1047; routing row R5 (`tests/recommend/test_routing_refresh.py`) at 719, 766, 951, 976. In `### Fix cycle 3` the same collision already exists for R4 (1046 re-anchor, against routing row R4 at 718). The comment `# allowed by R5 (owner 2026-11-08)` at 535-536 is meant to be copied into `probes.py`, where a reader has no way to tell which R5 is meant.
Smallest fix: in the 7.3 code comments write `# allowed by owner decision R5 (2026-11-08), see D10`.

**F6 (MINOR). Task item 6.2 cites `APPROVED.md:71` (G1) as authority, and G1 concerns something else.**
Evidence: task line 991 says the owner's own words are the decision "(APPROVED G1, `.dev/orca-command-refactor/decisions/APPROVED.md:71`)". Line 71 is G1, which is the grant of WC-9 and D4 for a local commit for the AC-1.8 Task, not an allowlist decision. The line exists but does not support the claim as stated. This is outside the listed inputs and is not a DESIGN claim. The real support for R5 is the OQ-1 record plus the relayed messages.
Smallest fix: drop the G1 citation from item 6.2, or rephrase it as "by analogy to G1".

**F7 (MINOR). DESIGN D10 and the R5 row do not point to the OQ-1 record or the relay message ids.**
Evidence: DESIGN 837 and 1047 quote "Allow it, no conditions needed." with the date only. The earlier sign-off in the SPEC records its message ids (SPEC 9, 483). The OQ-1 record (path and `msg_d95a87e312e1`, `msg_6ee5998d0874`) is reachable only from the task folder. This is not a broken link.
Smallest fix: add `(record: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/OQ-1-agent-wait-decision.md)` to the D10 Source cell.

**F8 (MINOR). `r5-mechanical.md` Command 4 records an expectation, not an output.**
Evidence: `r5-mechanical.md:34` reads "(no output expected; grep exit status 1)". The PASS at Check 6 (line 82) therefore rests on no recorded result. I re-ran `grep -nw 'TODO\|TBD'` on the DESIGN and it prints nothing, so the PASS is correct. Check 1 (line 77) groups the 9 hits loosely: "section 13 D10 (1)", while D6 (833) is also in section 13; this does not change the result.
Smallest fix: record the exit status actually seen.

## Checks

MINOR findings never fail the gate; a check is marked FAIL where a MINOR finding attaches.

| Check | Description | Result |
|---|---|---|
| C1 | Sections 4, 7.3, 11, 12, 13, 15.1, 18 and the Fix cycle 3 table exist at the cited places | PASS |
| C2 | Section 4 line 221 holds "recorded owner decision (R5, 2026-11-08)" once | PASS |
| C3 | 7.3: ten templates, seven verbs, `FORBIDDEN_TOKENS` is `--include-remote` only | PASS |
| C4 | GQ-109 row anchors (SPEC 562, NFR-014 line 143, GAPS 132) exist and say what is claimed | PASS |
| C5 | Section 11 test row: ten-template pin, positive `--agent-wait` case, negatives; "not called in Phase 1" pinned (F1) | FAIL (minor) |
| C6 | Section 12 NFR-014 row says ten templates and points to 7.3 | PASS |
| C7 | D10 cited SPEC lines 132, 143, 310, 323, 500, 504, 510, 562, 619 all exist and carry `--agent-wait`; no `agent-wait` line is missed | PASS |
| C8 | D10 covers every SPEC statement of "eight templates" (F2: line 301 missed) | FAIL (minor) |
| C9 | D10 and R5-row section lists match the sections actually edited | PASS |
| C10 | 15.1: "templates 1 to 8" matches 7.3 order; the R5 sentence is present | PASS |
| C11 | 15.1 item 11 and open item 10 agree with "templates 1 to 8 only" (F3) | FAIL (minor) |
| C12 | `Total: 10 deviations.` (D1 to D10) and `Total: 23 open items.` match the tables | PASS |
| C13 | `WORKER-CONTRACT.md:110` text equals the OQ-1, research/07 and D6 and WC-16 quotations | PASS |
| C14 | research/07 line 117, `:151`, `:122` exist and match | PASS |
| C15 | SPEC section 13 INV-005 conditions 1 and 2, NFR-014 (143), NFR-015 (144) exist as cited by OQ-1 | PASS |
| C16 | OQ-1 run id, message ids and quote match the task file (lines 984, 2807) | PASS |
| C17 | OQ-1 "Applied by" section list equals the DESIGN edits (F4) | FAIL (minor) |
| C18 | `r5-mechanical.md` greps reproduce on disk (lines 66, 221, 535, 536, 539, 679, 759, 833, 837, 839, 895, 1015, 1047) | PASS |
| C19 | Label "R5" is unambiguous (F5) | FAIL (minor) |
| C20 | Task item 6.2 citation `APPROVED.md:71` supports the claim (F6) | FAIL (minor) |
| C21 | D10 and R5 row point to the OQ-1 record (F7) | FAIL (minor) |
| C22 | No remaining DESIGN sentence forbids `--agent-wait` or says eight or seven templates | PASS |
| C23 | `WORKER-CONTRACT.md` unedited, as OQ-1 says | PASS |
| C24 | `r5-mechanical.md` Check results are backed by recorded output (F8) | FAIL (minor) |

## Self-audit

Tool engagement: Read 12 chunks (DESIGN 1-230, 515-565, 668-731, 745-890, 886-965, 985-1047; SPEC 125-149, 477-516; OQ-1; r5-mechanical; research/07 105-130; `WORKER-CONTRACT.md` 100-120; task file 980-1024), Grep 3, Bash 3 (read-only grep, sed, git status).
Verified against disk: all nine `agent-wait` hits in the DESIGN and the nine in the SPEC, every line number D10 and the GQ-109 row cite, the contract lines 110, 122 and 151, the task log rows, the GAPS 132 row and `APPROVED.md:71`.
Not verified (no way to do so read-only): the live probe figures in OQ-1 (24 calls, 0 `index.lock` sightings), the relay messages themselves, and the `orca-tabs` and Orca behavior.
Zero BLOCKING and zero MAJOR is credible here because the chain is short and every citation was checked against its file. The eight findings are cross-reference tidiness and one unpinned claim (F1), not broken links.

Verdict: PASS
Blocking count: 0
