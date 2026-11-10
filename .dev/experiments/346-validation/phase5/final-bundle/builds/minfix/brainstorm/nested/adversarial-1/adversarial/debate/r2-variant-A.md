# Round 2 rebuttal: Variant A (opus, architect)

Citation form: `A:NN`, `B:NN`, `C:NN` are lines of variant-1, variant-2, variant-3; `rB:NN`, `rC:NN` are lines of `debate/r1-variant-B.md` and `debate/r1-variant-C.md`; `rA:NN` is my own Round 1 statement.

## Response to criticisms

Each criticism raised against Variant A in the B and C Round 1 statements, with my answer. "Concede" means A's text should change in the merge.

### From B (rB:43-52)

| # | Criticism | Answer |
|---|---|---|
| B1 | The 40/30 class-`B` cap is calibrated on an undercount: 0 of 13 flg-r2 blocking fixes fit 40 words; A's "1-3 escalations" is underived (rB:45) | **Concede.** I already conceded this in Round 1 (rA:100-104): my own rough re-count put every F1-F13 fix between 58 and 164 words. B's independent replication (mean 116, median 126, rB:34) and B's cap replay (B:92-98) agree. A takes 80/120 (MAJOR/CRITICAL). A's 7% growth (A:314) and 2.5 proxy (A:317) assumed compliance with 40 words and are withdrawn as stated. |
| B2 | `open (over budget)` can only raise the metric the bar uses (rB:46) | **Partly contest.** In the experiment a reviser who skips the checker does not produce a counted replicate: A's validity rule V-M2 requires "a ledger and a `fixcheck.json` ... for each cycle", and a failing replicate "is re-run, not counted" (A:308). So the rule does not inflate the measured proxy through non-compliance. Once B's script-side revert is adopted (B:211), over-budget text is reverted before the re-review, so the rule fires only when the reviser also skipped the revert. In that case marking the finding open is the honest record: crediting a fix that broke the budget would hide the breach. I concede B's narrower point that the over-budget text stays in the spec as surface; that is the cost of a non-compliant cycle, and the experiment voids it anyway. |
| B3 | `L` is "never for an `origin=changed` finding", and 89%/100% of new findings are `origin=changed` (AB-REPORT line 30, which I re-read), so the override is effectively cycle-1 only (rB:47) | **Concede in part.** The fact is right. My reason (A:50: "its first remedy is to narrow or revert the change that caused it") still holds as a default, because reverting a cycle-1 site is free under A's rule that removals cost nothing (A:80). But a revert can reopen the parent blocking finding, and A gives no path for that case. Amendment: keep one `L` per report, granted by the reviewer; drop the absolute ban and replace it with a required reason that says why reverting the parent change would reopen a blocking finding. That stays checkable for presence (exit 3 on a missing reason, A:50). |
| B4 | `new sentences` inherits the splitter's semicolon rule; 126 of the draft's boundaries are followed by a lowercase letter (rB:48) | **Concede, verified.** My own count on `spec-v1-draft.md` finds the same 126 lowercase-next boundaries, plus 155 and 172 in the two revisions (New evidence 3). A fix of the form "X; Y" is two sentences and would breach class `B`'s limit of 1. A adopts B's capital-letter lookahead (B:164) and keeps sites only as a soft count; the word caps carry the budget. |
| B5 | Baseline unhashed (rB:49) | **Concede** (as in rA:105). The reviewer records `reviewed_sha256` (B:109) and the checker refuses a mismatch. |
| B6 | Extra authored files against the briefs' ownership clause (rB:50) | **Concede, and the evidence is stronger than B said.** The Arm B R2 reviewer template says "write ONLY your output file; ... no edits to the spec or any other file" (T07 template, New evidence 1). A's reviewer `cp -p` to `-reviewed.md` (A:42) is exactly an "other file" at R2. A's ledger file (A:56) also conflicts with T08's "write ONLY disposition-round2.md". A drops both: the ledger goes into the disposition file (B:134) and the reviewer writes only a hash. |
| B7 | Attribution has no teeth at the re-review: unattributed sites "are not graded blocking" (rB:51) | **Concede.** A named this itself as open question 2 (A:375). With B's revert adopted, unattributed hunks are restored to baseline text by the script before review (B:211), so the question goes away without process-only FAILs. |
| B8 | Anchoring: the report the re-review reads carries the reviser's quoted text and `why_not_narrow` (rB:52) | **Concede** (as in rA:108). The re-review copies only numbers and ids (B:111). |

### From C (rC:54-62)

| # | Criticism | Answer |
|---|---|---|
| C1 | A detects breaches but does not deny admission: the re-review continues on input error or crash (A:109, A:174) (rC:56) | **Concede for missing or malformed inputs.** 427's own bullet 1 already says "if a named file is unreadable or empty ... stop and say which, and never fall back to a first review" (`spec-panel.md` line 258, re-read). C's fail-closed rule (C:126) is the same house style; A's "continue without it" breaks it. A's own validity rule re-runs such a replicate anyway (A:330), so continuing only spends a review slot on data that is thrown away. I contest one part: "unattributed sites are reviewed normally" stops mattering once the script reverts them (B7). |
| C2 | The trust anchor is editable, and a site matched by k ids splits its words evenly, which can dilute a charge (rC:58) | **Concede both.** The hash answers the first (B5). The second is a real accounting hole that B shares (B:159): a shared site cited for three ids gets three allowances. A adopts C's single-owner rule (C:62, C:88): each hunk is charged to one finding; other ids may be linked but do not add budget. |
| C3 | The 40-word calibration is not settled (rC:60) | **Concede** (B1). |
| C4 | A word ceiling is not a byte ceiling; A labels growth in bytes and computes the 16% bound in words (rC:62) | **Concede the wording.** A:314 derives "about 16%" from added words over 8,148 draft words, under a column labelled bytes. The draft is pure ASCII (New evidence 4), so the word-to-byte ratio is stable on S1, but the claim should say "about 16% in words". The fix costs nothing: A's report already computes `bytes_added` per finding (A:94), so the merged checker can enforce C's byte cycle cap (C:62) alongside the word caps. |

Net: of 12 criticisms I concede 10 fully and 2 in part (B2, B3). None of them touches A's structural core: who acts (no coordinator duty), who grants the override (the reviewer), the seven bullets, no finding ids in the spec, the authoritative re-review run, and the `## Unattended mode` drop. Both B and C endorse most of that core (rB:13-19, rC:9-11, rC:80, rC:150).

## Updated assessment

**B, after its defence.** B's Round 1 statement is the strongest of the three. Its calibration claim now rests on two independent counts (B's tags and B's replication, rB:34; my site re-count, rA:101), and its self-concessions match mine almost point for point: zero minor budget (rB:69), reviewer-granted override only (rB:70), seven bullets (rB:67), the `## Unattended mode` test break (rB:68), an authoritative re-review run (rB:71), the condition-word counter (rB:73) and an optimistic proxy forecast (rB:66). With those taken, B's design and A's converge. What B still has that I would not merge:
- Five subcommands and 20-31 extra calls (B:303, B:436). B itself proposes folding `hash` into `snapshot` and `verify` into `check` (rB:72). I would go further: one `check` with a `--revert` flag that does what `enforce --in-place` does.
- Even budget splitting across two ids (B:159), the same hole C found in A (C2 above).
- Approximate matching (40-character unique substring, 10-word `new` prefix, B:159). C's objection that `enforce` reverts on that basis (rC:70) is fair, but it is a matcher-precision issue that B's replay harness (B:479) measures before any worker runs. I keep `enforce`.
- I withdraw my Round 1 criticism of B's brief substitution (rA:74). The briefs show B's pattern hits exactly the three review briefs (New evidence 5).

**C, after its defence.** C's statement is candid: it concedes the coordinator delivery gap as "a blocking design defect" and prefers A's actor-local placement (rC:80, rC:130, rC:150), withdraws the 1/1 forecast (rC:82) and accepts partial-admission coupling as a required correction (rC:86). Three of its points moved me:
- **Single-owner accounting** (rC:44). It closes a budget-pooling hole in both A and B.
- **Fail closed on missing inputs** (rC:48). It matches 427 bullet 1 word for word.
- **Hard-gate structural validation** (rC:76; C:43). A CRITICAL or FR-8/FR-9 finding must be blocking. That reports the grader inconsistency B:481 would otherwise encode as a minor budget.

C's exact byte reconstruction remains the strongest integrity invariant, but it should not ask a model for byte offsets. The checker can find each `before` string in the frozen target and compute offsets itself; a unique `before` inside the reviewer's registered target is enough. My Round 1 argument that S1 is full of multibyte characters (rA:86) was wrong for the draft (New evidence 4), so the real cost is absolute positions in a 57 KB file, not encoding. C's coordinator-owned grants and `state.json` still need a coordinator duty that no brief delivers. That is why the override authority stays with the reviewer.

**Where the merge should land (architect's view).** Take A's structure, B's calibration and termination, and C's contract details:
- From A: actor placement (reviewer writes inputs, reviser and re-review run the checker, no coordinator duty); reviewer-only override; seven bullets with bullet 6 rewritten; no ids in the spec; budget constants only in the script; `## Unattended mode` dropped from the repository file; the four causal falsifiers.
- From B: 80/120 caps; script-side revert; ledger in the disposition file; hash plus stale-base refusal; the capital-lookahead splitter; `attacks:`; replay harness first; the 472-line base for the experiment file; the narrow brief substitution.
- From C: exit codes (argparse keeps 2, crash 70); fail closed on missing physical inputs; single-owner charging; hard-gate validation; a byte cycle cap; the fresh-worker valid/invalid probe.

## New evidence

All checks were read-only, run for this round.

1. **The R2 reviewer brief forbids any other file.** `phase2/S1/briefs/templates/T07-R2-reviewer.TEMPLATE.txt`: "Ownership: write ONLY your output file; planning only, no edits to the spec or any other file". The other briefs say:
   - T05 (R1 reviewer): "write ONLY your output file(s)".
   - T09 (R3 reviewer): "write ONLY that file".
   - T06 (R1 reviser): "write ONLY your output file(s)".
   - T08 (R2 reviser): "edit ONLY the spec and write ONLY disposition-round2.md".

   Consequences:
   - A's reviewer-written `-reviewed.md` (A:42) breaks T07.
   - A's reviser-written ledger file (A:56) breaks T08.
   - B's script-written `.fixcheck/` files are a weaker conflict with T08, since the reviser still causes the write. B flags this itself (B:452).
   - The lowest-risk merge has workers write no extra files. The reviewer runs a read-only `hash`. The reviser's ledger lives in the disposition file. The baseline is a script snapshot, and its acceptance by a literal-minded reviser is confirmed in a pilot (B:451).
2. **427 already fails closed on missing inputs.** `src/superclaude/commands/spec-panel.md` bullet 1 (line 258): "if a named file is unreadable or empty, or the prior report has no `review: N of 3` header, stop and say which, and never fall back to a first review". C's rule (C:126) extends existing house style. A's "continue without it" (A:174) and B's "STALE ... and MISSING do not stop the review" (B:110) depart from it.
3. **Splitter counts on S1** (stdlib `re` over the whole text of `exp346-ab-flg-r2/.../specs/history/`):

   | file | A's `(?<=[.!?;])\s+` boundaries | of which next char lowercase | of which after `;` | B's lookahead boundaries |
   |---|---|---|---|---|
   | v1 draft | 564 | 126 | 258 | 349 |
   | v2 after round 1 | 653 | 155 | 301 | 402 |
   | v3 after round 2 | 694 | 172 | 325 | 425 |

   My totals differ from B's 435/288 (rB:38) because I ran the regex over the whole file, so line-end boundaries count too. The lowercase-next figure on the draft (126) matches B exactly. Revised text has more of these splits, so A's `new sentences` and `sites` counts get noisier exactly where they are measured.
4. **Encoding.** `spec-v1-draft.md`: 57,763 bytes, 57,763 characters, 0 non-ASCII. v2: 4 non-ASCII characters (8 extra bytes). v3: 13 (26 extra bytes). B's "pure ASCII" claim for the draft is right (rB:58). My Round 1 claim of common multibyte characters (rA:86) is withdrawn. Byte offsets in cycle 2 would cross a handful of multibyte characters, which is a minor risk.
5. **Brief invocations.** `/sc:spec-panel @.d...` appears once in T05, T07 and T09 (task text and templates) and not in T06, T08 or T10. The R4 briefs outside Arm B's loop (T11, T13, T15, T17) contain prose mentions such as "/sc:spec-panel and", "/sc:spec-panel," and "/sc:spec-panel.". A's `sed` (A:283), applied "in every brief", would rewrite those prose mentions too if those files were ever used. B's `@`-anchored pattern (B:367) touches exactly the three Arm B review briefs. B's is the better choice for S1.
6. **Arm B's review-1 proxy was 16 and 17** (ARMB-REPORT lines 10-16, re-read). This confirms B's own concession that pooling the review-1 proxy at 12 (B:401, B:407) flatters its forecast (rB:66). With 16.5 and B's middle r of 0.50, review 3 comes to about 4.1, not 3.0. Any merged forecast should start from Arm B's 16.5, because the arm uses Arm B's briefs.
7. **Installer rule, re-read.** `src/superclaude/cli/install_skills.py` `_has_corresponding_command` strips only the `sc-` prefix and does not strip `-protocol`. So `fix-budget`, `sc-fixcheck` and `sc-spec-panel-minfix-protocol` all install. My A:151 warning applies only to a bare `sc-spec-panel-minfix`. Folder naming is not a differentiator.

## Updated per-point positions

| id | preferred (A/B/C) | changed since R1? | reason |
|---|---|---|---|
| S-001 | A (tie) | no | Same eight sections in seed order in all three |
| S-002 | A | no | Same content with fewer headings; B's pseudo-headings are harder to navigate |
| S-003 | B | no | Six evidence tables, independently replicated (rB:34, rA:101) |
| S-004 | A | no | Steps grouped by actor (reviewer, reviser, re-review); B also prefers A here (rB:85) |
| S-005 | A | no | A file table, then one H3 per artifact; C agrees (rC:106) |
| S-006 | B | no | Derivation tables let a reader recompute (and correct, New evidence 6) the forecast |
| S-007 | B | no | Detection, mitigation and residual columns per risk |
| C-001 | B | no | Every finding listed with a derived class; lighter than C's JSON. Add C's hard-gate check (see C-015) |
| C-002 | B | no | 80/50 fits the measured blocking fixes; A's 40 is withdrawn (B1) |
| C-003 | B | no | 120/80, consistent with C-002 |
| C-004 | A | no | Zero edits for non-blocking findings; B concedes it (rB:69), C agrees |
| C-005 | C | no | A fixed word and byte cycle cap; it answers C4 too. B's largest-first revert hits CRITICAL fixes first |
| C-006 | B | no | Universal and exec-recipe gates plus A's condition-word counter (B accepts it, rB:73) |
| C-007 | B | no | Ledger inside the disposition file; T08 says "write ONLY disposition-round2.md" (New evidence 1) |
| C-008 | B | yes (amended) | Unit diff with B's lookahead splitter, but charged to one owner per hunk as C does (C2); drop the even split that A and B both use |
| C-009 | B | no | Hash plus stale-base refusal with no coordinator duty; A's reviewer copy breaks T07 (New evidence 1) |
| C-010 | B (tie) | no | All three names install safely (New evidence 7); naming is not a differentiator |
| C-011 | A | no | One `check` invocation, with B's revert as a `--revert` flag rather than a separate subcommand |
| C-012 | C | no | argparse keeps exit 2; crash 70; separate input, hash and output failures |
| C-013 | B | no | Script-side revert of whole failing findings guarantees termination; C's admit-nothing discards good fixes |
| C-014 | A | partly | The reviewer grants it, one per report. The absolute `origin=changed` ban becomes a required reason (B3) |
| C-015 | C | yes | All keep FR-8/FR-9 in the standard class, but C alone validates that a hard-gate or CRITICAL finding is blocking (C:43), as 427 bullet 2 requires. B:481 would budget a minor-graded GAP at minor |
| C-016 | A | no | Seven bullets, bullet 6 rewritten consistently with no id clause; C is close but keeps the id clause (C:167) |
| C-017 | A | no | No ids in the spec; B concedes they are attack surface (B:476) |
| C-018 | A | no | The re-review's own checker run counts, copying only numbers and ids (B's rule); B concedes (rB:71) |
| C-019 | C | yes | Stop on missing or stale physical inputs, as 427 bullet 1 already does (New evidence 2); A's validity rule voids such a replicate anyway (A:330) |
| C-020 | C | no | The fresh-worker valid/invalid probe proves delivery |
| C-021 | B | yes | Verified: B's `@`-anchored pattern hits exactly T05, T07 and T09. A's pattern would also rewrite prose mentions in the R4 briefs (New evidence 5) |
| C-022 | A | no | No coordinator duty; C concedes the gap (rC:80) |
| C-023 | B | no | The 472-line base for the experiment file; the repository file still drops `## Unattended mode` |
| C-024 | B | no | Only derived forecast, but restart it from Arm B's review-1 proxy of 16.5 (New evidence 6), which gives about 4.1 |
| C-025 | B | no | Replay-derived growth; label ceilings by unit. C's 21.3% is the only byte-true bound and should be stated beside it |
| C-026 | A | no | Four causal falsifiers at the seed bar; keep C's spread condition explicit (A states it at A:322) |
| C-027 | B | no | Itemised and most candid |
| C-028 | A | no | One fit assessment per adopter; not designed now (C agrees on separation) |
| C-029 | B | no | Replicated twice; A's per-finding numbers are an undercount |
| C-030 | B | no | Behaviour tests plus the `enforce` property test; add A's derivation pin and C's integrity cases |
| X-001 | A | no | Zero for non-blocking findings; all three advocates now agree |
| X-002 | A | no | Seven bullets with bullet 6 replaced; C is equal on count, B concedes (rB:67) |
| X-003 | A | no | No ids in the spec, consistently; C contradicts itself (C:90 against C:167) |
| X-004 | C | no | The only layout that does not overload argparse's exit 2 |
| X-005 | B | no | The script reverts whole findings; add C's coupled-revert correction (A-002) |
| X-006 | A | no | The reviewer, independent of the reviser, with no unbriefed coordinator |
| X-007 | C | yes | Fail closed on missing or stale inputs (New evidence 2); continuing spends a review slot on a voided replicate |
| X-008 | B | no | Numbers and ids only; A's report leaked `why_not_narrow` (conceded) |
| X-009 | A | no | Free deletions keep delete-first worth doing. Report removed words per cycle (A's M7). B's data: removals run 84-379 words per cycle, so C's cap rarely binds but adds a failure path to the cheapest fix |
| X-010 | B | no | Two independent re-counts support B |
| X-011 | B | no | Size alone does not separate parents (B:87); B's replication shows only a mild lean (rB:35) |
| X-012 | A | no | No coordinator duty; C concedes (rC:150) |
| X-013 | A | no | The fail line is the seed bar; B's 3.5-4.5 "promising" band is a soft escape |
| X-014 | B | no | The 472-line base changes one thing at a time |
| A-001 | B | no (QUALIFY stands, now with numbers) | 126 to 172 lowercase-next splits per file (New evidence 3). Use B's lookahead splitter and word caps that do not depend on boundaries; run the replay harness (B:479) before any worker run |
| A-002 | B | no (QUALIFY) | `enforce` reverts whole findings; add a coupled revert for hunks linked to more than one id (rA:188) and C's demand that coupled changes are kept or dropped together (rC:86). Measure with `attacks:` |
| A-003 | A | no (QUALIFY, mostly holds) | Zero minor budget keeps deferred text `origin=unchanged`, which bullet 5 caps at minor. Report the proxy and 427's blocking count separately (C:302) |
| A-004 | B | no (REJECT as stated) | No evidence of one-retry compliance. `enforce` turns a miss into a recorded escalation; pre-register B's retry at 100/60 (B:424); count carried blockers (A's M9) |

Tally: A 21, B 27, C 7 (55 rows; Round 1 was A 22, B 25, C 4 over 51). Changes since Round 1:
- Moved to C: C-015, C-019, X-007.
- Moved to B: C-021.
- Amended toward C: C-008 (single owner).
- Amended in A's text: C-014 (override reason instead of a ban).

The A rows that remain are the structural and contract points: actor placement, override authority, the Review Loop shape, ids, the re-review's authority and the falsifiers.
