# QA Report: 2.1 allocation page check (check-1)

Status: Complete
Date: 2026-11-13
Verifier: rf-qa, adversarial, report-only, Tier1b, fix_authorization false (run run_c974cafd0eb6)
Object under check: `qa/local-source-allocation.md` topic 2.1 section (lines 38-52)

## Inputs read
Revision: worktree HEAD 933cf3a4f. All reads under 100 lines; metadata via wc -l and targeted greps only (no full source reads).

1. TASK file lines 140-161 (procedure passage, 22 lines) read in full.
2. `qa/local-source-allocation.md` lines 1-60 read (topic 2.1 section is lines 38-52; whole file is 117 lines, measured by wc -l); targeted grep over the whole file for F01-F04, 2.1 and source-slices to find any other topic-2.1 text (lines 3, 11-14, 38-52, 64, 84, 113, 117 only).
3. `qa/input-bindings.md` (32 lines) read in full. It holds only item-1.1 rows; no 2.1 rows are registered yet (consistent with the manifest line 117: pending outputs are registered at dispatch time).
4. Item-2.1 producer spec. LOCATOR DEFECT in the brief: TASK line 213 is an EMPTY line (file is 705 lines, measured). The item-2.1 PRODUCER-ONLY passage is inside the first "Measured-input dispatch barrier" paragraph at TASK line 224 (read from the PRODUCER-ONLY marker to the item's final sentence). The check item itself is TASK line 188. Both read.
5. Metadata verification against the four corpus files: wc -l, function-definition grep, exec-site grep, closing-brace/esac/done grep, option-parser grep, private-profile grep (outputs bounded to under 40 lines each).

## Checks (a)-(f)
Measured endpoints (wc -l): F01 ccsession 1975, F02 ccsession-orca 249, F03 session-start.sh 47, F04 session-name.sh 217. All four match the manifest.

### (a) Range coverage: PASS
Slices 1-3 cover F01 as 1-700, 701-1400, 1401-1975 = 700+700+575 = 1975. No gap, no overlap. F02, F03, F04 are each assigned whole (slice-3 and slice-4). Union complete.

### (b) Counterpart labelling: PASS for the 2.1 section (note on edges, see B3)
The 2.1 section assigns no foreign-file reads. Other topics read F01 ranges (2.2 slice-3: F01 1-120 and 700-1000; 2.4 slice-3: F01 962-1155) and the manifest labels them "counterpart read, charged and attributed"; F01 full coverage stays with 2.1. Labelling is correct.

### (c) Producer-spec obligations to slice aspects: FAIL (B1, B2)
The manifest names only four aspect phrases (line 50): slice-1 "parser/arg handling/prologue"; slice-2 "profile application/selection/export/passthrough"; slice-3 "setup_shim ... and tail exec paths"; slice-4 "hooks and Orca wrapper". Mapping of the obligations in the item-2.1 producer spec:

| Obligation | Aspect phrase that carries it | Where the code is (measured) | Result |
|---|---|---|---|
| parser | slice-1 "parser/arg handling" | option loop is 730-821 (done at 821), in slice-2; slice-1 holds only a pre-parse `case` at 684-727 | MISMATCH (B2) |
| apply_profile | slice-2 "profile application" | 1157-1189, slice-2 | ok |
| apply_tier_selection | slice-2 "selection" | 1191-1233, slice-2 | ok |
| export_selection | slice-2 "export" | 1235-1281, slice-2 | ok |
| setup_shim | slice-3 label (line 50) AND slice-2 per boundary note (line 52) | 962-1155, wholly slice-2 | CONTRADICTORY (B3) |
| all six exec sites | slice-3 "tail exec paths" | 1904, 1906, 1964, 1966, 1971, 1973; all in 1401-1975 | ok |
| passthrough after --claude-args | slice-2 "passthrough" | `--claude-args` handler at 749, slice-2 | ok |
| permissions | none | defaults at 137-141 (slice-1) and the exec flags (slice-3) | UNMAPPED (B1) |
| private-profile rules | none | lines 116 (slice-1), 881 (slice-2), 1833 (slice-3) | UNMAPPED (B1) |
| duplicate model/settings options | none | `--model` 798 and PROFILE_MODEL 849/1175/1226, CC_SETTINGS_ARGS 1150/1259 (slice-2); `--model`/settings in all six exec lines (slice-3) | UNMAPPED (B1) |
| resume | none | resume comment 1298 (slice-2); `--resume "$SESSION_ID"` 1964/1966 (slice-3) | UNMAPPED (B1) |
| immediate callers | none | callers of F01 in F02/F03/F04 (slice-3/4) | UNMAPPED (B1) |
| session-only vs per-request policy, real-client vs fake-client precedence, negative searches | none | spec text, not a code range | UNMAPPED (B1) |

### (d) Lifetime totals <=1000: PASS under the brief's formula, with caveats (see M1)
Formula: source + procedure 22 + brief ~55 + assigned context.
- slice-1: 700+22+55+138 (scope-01) = 915. OK
- slice-2: 700+22+55+142 (scope-02) = 919. OK
- slice-3: 575+249+22+55 = 901 (no context assigned). OK
- slice-4: 47+217+112 (research-notes)+22+55 = 453. OK
Arithmetic re-derived; the manifest's own corrected totals are right. The scope/notes line counts match wc -l (138, 142, 112).

### (e) Output uniqueness: PASS with a note (M3)
The manifest gives the directory `research/source-slices/2.1/`; the check item names `slice-1..4.md`. Four distinct names, no collision. The manifest does not itself list per-slice output paths or consumer IDs for 2.1.

### (f) Producer-before-consumer: PASS
TASK region `local-allocation-checks` is lines 186-198 and `local-source-slices` is lines 202-203 (empty, unemitted). Checks come first; manifest line 113 requires checks before source dispatch; the executor accepts only on PASS.

## Findings
### Blocking
- **B1 (CRITICAL): five producer-spec obligations plus the policy questions have no slice aspect.** Permissions, private-profile rules, duplicate model/settings options, resume and immediate callers appear in no aspect phrase (manifest line 50). Each slice producer would copy the full prompt but be told only a four-phrase aspect, so those obligations have no named owner and their cross-slice pieces (for example private-profile at F01 116/881/1833, resume at 1298 and 1964/1966) belong to nobody. Required fix: list every obligation under a named slice aspect, with the cross-slice pieces split explicitly.
- **B2 (CRITICAL): the "parser" aspect is assigned to the wrong slice.** Slice-1 (1-700) is told "parser/arg handling" but the option loop (`--claude-args` at 749, `--model` at 798, loop end `done` at 821) lies wholly in slice-2 (701-1400). Slice-1 holds only the pre-parse `case` (684-727), the usage/default-flag prologue and helpers. A producer following the aspect would write a parser section from lines that do not contain the parser. Required fix: assign the 730-821 option loop to slice-2's aspect and record the slice-1 case 684-727 to loop 730 entry edge.
- **B3 (CRITICAL): the boundary and edge register is wrong or incomplete.** (i) Slice-3's aspect names `setup_shim` (line 50) while the boundary note (line 52) and the measured range (962-1155) put it wholly in slice-2; the note itself contains a visible self-correction ("Wait: ...") and the line-46 "OVER BUDGET" text is stale, so the page is not a clean directive. (ii) `session_place` is 1358-1406 and straddles the 1400/1401 boundary between slice-2 and slice-3; not declared. (iii) The selection state set in slice-2 (PROFILE_MODEL at 849/1175/1226, CC_SETTINGS_ARGS at 1150/1259, apply_* at 1157-1281) is consumed at the six exec sites in slice-3 (1904-1973); only setup_shim is declared as an attributed edge. Required fix: add these edges with the attribution rule (slice-3 cites slice-2 findings as counterpart evidence, never re-derives).

### Minor / Medium
- **M1 (Medium, follow-up candidate): budget counts are estimates and omit mandatory context.** "brief ~55" is unitemised, not measured; the procedure says missing measurements invalidate admission. Not charged: `qa/input-bindings.md` (32 lines, every emitted paragraph must read it), BUILD-REQUEST.md, the rf-task-researcher role file (564 lines; a pinned passage is needed) and the research template. Headroom is only 85/81/99 lines for slices 1-3, and slice-3 receives no scope or research-notes context at all although item 1.2 says never charge zero for context. Under the brief's own formula this passes, so it does not fail the review.
- **M2 (minor): brief locator is wrong.** The brief and the item name "TASK line 213"; that line is empty. The item-2.1 spec is at line 224; the check item at 188. Does not change any verdict.
- **M3 (minor):** the manifest records no per-slice output paths or consumer IDs for 2.1 (only the directory).
- **M4 (minor, process note):** a stub `check-1.md` already existed with a different layout (created 15:53:36 UTC, about 11 seconds before my first write attempt, not by me). I populated that file in place. If a second verifier of this dispatch is also writing this path, the outputs would collide.

## Self-Audit
Attempted disproof of my own FAIL: (1) Could the missing obligations be covered because every slice reads all its lines? Range coverage is complete (checks a, d pass), but check (c) as the brief states it requires each obligation to map to an assigned aspect, and the manifest's aspect text is the only thing producers receive; unlabelled obligations and a parser label on the wrong range are defects of the page, not of range union. (2) Could the parser be considered slice-1 because of the `case` at 684-727? That `case` is a pre-parse dispatch; the option loop with `--claude-args` and `--model` is 730-821 (grep-verified `done` at 821), so the label is wrong either way. (3) Is `session_place` straddle real? Function opens 1358 and its closing `}` is 1406 (closing-brace grep), boundary is 1400/1401. Yes.
What I confirmed as correct: F01-F04 line counts; contiguous non-overlapping F01 ranges; six exec sites all in slice-3; apply_profile/apply_tier_selection/export_selection/setup_shim wholly inside slice-2; slice totals 915/919/901/453; check-before-source ordering.
Not checked (outside brief): contents of the scope files, 2.2-2.5 pages, whether source behaviour matches the spec beyond these line locations.

Blocking count: 3 (B1, B2, B3). Minor/Medium: 4. Fix authorization was false; no edits made outside this report.

## Recommendation
Do not dispatch any 2.1 source slice. Have the coordinator correct the manifest topic-2.1 section (aspects for all obligations, parser reassigned to slice-2, boundary/edge register incl. session_place and selection-state edges, clean setup_shim ownership, per-slice output paths), then request check-2.

VERDICT: FAIL
