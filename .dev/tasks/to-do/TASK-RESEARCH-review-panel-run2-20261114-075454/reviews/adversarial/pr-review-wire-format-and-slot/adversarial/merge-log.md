# Merge Execution Log

## Metadata
- Base: Variant A (Proposal A, `variant-1-original.md`; default model, default persona), selected by tiebreaker level 1 (`base-selection.md`)
- Executor: merge-executor agent (slot C-10, pr-review-wire-format-and-slot)
- Refactoring plan: `refactor-plan.md` (17 changes plus the "Changes NOT Being Made" table; executed as written, no strategic decisions made)
- Merged output: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/pr-review-wire-format-and-slot/merged-output.md` (473 lines, 13 sections)
- Changes applied: 17 of 17 planned
- Status: success
- Timestamp: 2026-11-14T17:43:44Z (merge date written in the output header)

Executor notes that apply to every change below:
- The merge re-read no source code and ran nothing. Every number, file:line, severity and confidence was copied from the debate files; the tags ([CODE-VERIFIED], [UNVERIFIED], [RELIED]) are carried, not re-earned.
- Inputs read in full: `refactor-plan.md`, `variant-1-original.md`, `round2-advocate-A.md`, `round2-advocate-B.md`, `invariant-probe.md`, `base-selection.md`, `diff-analysis.md`, and `debate-transcript.md` lines 1-287 (Round 1 text, unedited copies of `round1-advocate-A.md` and `round1-advocate-B.md`) and 842-913 (Scoring Matrix, probe summary, Convergence Assessment). `variant-2-original.md` was read for sections 5, 8 and 9 only (to check the tag wording "endangered in a narrow sense" and B's open items O2 to O6 and the "Limits" list); the rest of Variant B reached the merge through the Round files and `diff-analysis.md`, as the plan cites them.
- Structure: the merged document uses Variant A's eight sections, renumbered into 13 sections because the four new sections the plan names are placed where the plan puts them. Mapping from the base: base 1 = merged 1; base 2 = merged 2 (plus the new 3 "Release scope" after it); base 3 = merged 4; base 4 = merged 5; base 5 = merged 6 (plus the new 7 "Contested amendments" after it); base 6 = merged 8; base 7 = merged 9; base 8 = merged 10; the new 11 "Invariants left open by the debate", 12 "Alternatives not adopted (changes not made)" and 13 "Limits and open items" follow. Plan references to "section 2/3.5/4/5/6/8" are to the base numbering and are mapped here.
- Order of execution: the document was assembled in document order, each change integrated at its stated integration point. No change depended on the output of an earlier one, so document order and plan order give the same result.

## Changes Applied

### Change 1: Replace A's converter input (X-001); aggregation contested
- **Status**: Applied
- **Source**: B-R2 sections 1.2, 2 row 2, D1; A-R2 section 3 (e) and section 5 condition 3; diff-analysis X-001; probe INV-012, INV-018
- **Target**: Base sections 2 and 3.5 (replace) -> merged 2.1, 2.2, 4.5
- **Before**: Base 2 said the adapter reads `primary_citation`, `claim`, `blocking_any`, `disputed`, `reviewers` and "the highest member severity" from the cluster record; base 3.5 said the cluster output "already holds what the adapter reads".
- **After**: 2.1 states the cluster and member key lists (no severity, no category) and where path, line, claim and `blocking_any` come from; 2.2 gives the settled inputs (cluster output, same records joined on `(reviewer_id, id)`, `changed_ranges`, severity table, requested ids, head SHA), the join conditions, and the aggregation as contested (A-R2 maximum over joined members versus B-R2 D1 and AM-1, with probe INV-012 beside it); 4.5 points back to 2.1. The two old claims are not carried.
- **Provenance tag**: `<!-- Source: Base (original, modified) — base section 2 shared-core bullets kept; the base bullet on what the cluster record carries for the adapter replaced per Change #1 (X-001, code-contradicted); ... -->` and `<!-- Source: Base (original, modified) — ... inputs and join per Change #1 (B-R2 section 1.2, A-R2 section 3 (e)) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (the aggregation is labelled contested, not settled)

### Change 2: New pure module, no `REVIEWERS` entry
- **Status**: Applied
- **Source**: A-R2 section 4 row 1 and section 5; B-R1 Concession 4; B-R2 sections 1.1 and 2 row 1; matrix S-003, C-004, C-005, S-002, S-004
- **Target**: Base sections 1 and 2 (keep, add rationale) -> merged 1.1, 2.2
- **Before**: Base 2 named "one new pure module" with no rationale for placement against B.
- **After**: 2.2 "Placement and shape" keeps the module, adds B's concession (slot axis, "size and import fan-in, not on purity"), the zero-token facts (`test_static_grep.py:37-55, :136-147`), the C-003 label (Variant A, 63%), the pin facts (one python fence pinned in four test files; `reviewer_activity` a literal two-key dict, X-002) and records the test-file choice (A-R2 new test file versus B-R2 AM-5 append) as contested and not answered by A.
- **Provenance tag**: `<!-- Source: Base (original, modified) — ... placement rationale added per Change #2 (B-R1 Concession 4, B-R2 section 1.1); ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 3: Strict `incomplete` rule, no quorum helper; extra clauses contested
- **Status**: Applied
- **Source**: A-R2 section 1.1 W5, section 4 row 6, section 5 condition 4; B-R2 section 2 row 6, AM-3, AM-4, D3; X-009, A-013; probe INV-007, INV-008, INV-011
- **Target**: Base section 2 (panel presence bullet) and section 5 C-03 paragraph -> merged 2.3, 6.3
- **Before**: Base 2 and 5 derived `incomplete` from a PR-profile quorum floor and proposed a shared helper (base 5 C-03: "an addition A needs").
- **After**: 2.3 states the strict rule (requested ids minus `complete_reviewers`), withdraws the Round 1 floor with the evidence (0 matches; `evaluate_quorum` wrong shape), and lists the contested clauses (missing ranges, every-cluster-dropped, AM-3, AM-4, D3) with the three HIGH probe findings; 6.3 rewrites the C-03 paragraph for the strict rule. C-006 recorded as content-unresolved.
- **Provenance tag**: `<!-- Source: Variant B (Proposal B), Round 2 B section 2 row 6 and Variant A Round 2 section 1.1 W5, section 4 row 6, section 5 condition 4 — merged per Change #3 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (the quorum floor and B's refusal appear only as withdrawn or non-existent, in paraphrase)

### Change 4: `body`, `in_diff`, `confidence`, `original_line`, `reviewer` rules
- **Status**: Applied
- **Source**: A-R2 section 1.1 W2, W3, W6, section 4 rows 3, 5, 7; B-R2 sections 1.3, 1.4, 2 rows 3 to 5, 7; matrix C-002, C-010, C-016, X-010
- **Target**: Base section 2 (adapter owns list) and 3.4 -> merged 2.2, 4.4
- **Before**: Base 2 had the adapter compute `in_diff` and `original_line` "from the diff the pre-step already holds" and set `confidence` "from cluster facts (for example `disputed`)".
- **After**: 2.2 "Fields of each Finding": `body` is the claim verbatim (`fix_key`, `models.py:196-207`), `reviewer = "panel"` set by code, `in_diff` computed by the converter (new code; A's premise [UNVERIFIED]), `confidence` and `original_line` unset with the evidence, keys owned by the converter and no key added to the line. 4.4 keeps the no-producer evidence and adds X-006. The missing-ranges question is labelled contested (Change 7 and 13).
- **Provenance tag**: `<!-- Source: Base (original, modified) — ... field rules per Change #4 ... -->` (4.4) and the 2.2 tag above
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 5: Head-SHA binding and cadence
- **Status**: Applied
- **Source**: A-R2 section 1.1 W7 and section 4 row 11; B-R2 section 2 row 11; A-008; probe INV-001
- **Target**: Base section 4 last bullet and section 2 (sibling field definition) -> merged 5.4, 2.3
- **Before**: Base 4 last bullet: a per-round re-run "needs a cycle id and the cost data first".
- **After**: 5.4 states once per head SHA, SHA in the field, valid only for that SHA, no automatic re-run after a fix push in the first release (GQ-177, OQ-18), with `SKILL.md:103-112` as the model, and records probe INV-001 and probe INV-002; 2.3 defines the sibling field and its SHA.
- **Provenance tag**: `<!-- Source: Variant B (Proposal B), Round 2 B section 2 row 11 and Variant A Round 2 section 1.1 W7, section 4 row 11 — merged per Change #5; replaces the base's statement that a re-run needs a cycle id -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 6: First release report-only; bots-silent and thread-less defaults
- **Status**: Applied
- **Source**: A-R2 section 4 rows 8, 9 and section 5 conditions 1, 7; B-R2 sections 1.5, 2 rows 8, 9, D5; probe INV-014, INV-015
- **Target**: Base, new subsection in section 2 and section 4 -> merged section 3 "Release scope" (3.1 to 3.4)
- **Before**: Base had no release-scope statement and left reply, resolve and bots-silent unaddressed (R-16).
- **After**: 3.1 report-only (`SKILL.md:175-178`), 3.2 thread-less rule on promotion (`fsm.py:1203-1205`, `refs/thread-reply.md:92-99`, INV-K), 3.3 bots-silent and D5/AM-4 (contested) with probe INV-015 and INV-010, 3.4 dedup (A-010) with probe INV-014 in 3.1.
- **Provenance tag**: `<!-- Source: Variant B (Proposal B), Round 2 B sections 1.5, 2 rows 8 and 9 and D5, and Variant A Round 2 section 4 rows 8 and 9 and section 5 conditions 1 and 7 — merged per Change #6 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 7: Per-cluster conversion and dropped list; missing-ranges rule contested
- **Status**: Applied
- **Source**: A-R2 section 3 (c) and section 5 condition 2; B-R2 section 3 row (c), D4, AM-3; probe INV-009
- **Target**: Base section 2 (new bullet) -> merged 2.2 (last paragraph)
- **Before**: Base 2 relied on the existing fail-closed rule and had no per-cluster handling.
- **After**: The bot-gate batch drop (`SKILL.md:118-124, :143-149`), the per-cluster `try`, the drop reasons, B's cluster-id-and-severity addition, the contested missing-ranges clause and probe INV-009 (unit of "dropped").
- **Provenance tag**: covered by the 2.2 tag (Change #1/#2) and the 2.2 "Missing `changed_ranges`: contested" paragraph (labelled in text; no separate tag because it is a paragraph block of 2.2)
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 8: Correct A's factual claims (X-002, X-003, X-004, A-004)
- **Status**: Applied
- **Source**: diff-analysis X-002, X-003, X-004, A-004; A-R1 Concessions 2 and 3; B-R1 strength 8
- **Target**: Base sections 3.3, 6.1, 8 -> merged 4.2, 4.3, 8.1, 10
- **Before**: Base claimed a third name breaks the pins at `test_codex_reviews.py:285-295, :705`, cited 50 test files and 12 `reviewers` lines in 3 files, and said downstream reads only path, line, body, category and the route.
- **After**: 4.3 corrects the pin claim (holds only for a design that edits `reviewer_activity`), the census (47 `test_*.py`, 49 `.py`; 13 occurrences in 4 files; no test pins the `reviewers` row, `test_merge_guard_protocol.py:498-508`) and makes the slot argument semantic (five two-name functions, guards at `reviewers.py:412` and `:420`); 4.2 lists what a `Finding` is also read for (`fsm.py:902-906`, `models.py:196-207`, `fsm.py:1064-1074, :1203-1205`); 10 replaces the "four fields" sentence and the "count in body" suggestion; 8.1 restates the isolation claim.
- **Provenance tag**: `<!-- Source: Base (original, modified) — ... corrected per Change #8 ... -->` on 4.2, 4.3 and section 10
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (old claims absent; see re-scan)

### Change 9: Adopt B's tests and measurements
- **Status**: Applied
- **Source**: B section 6; B-R2 section 6; A-R2 section 5 "Tests and measurements"; probe INV-019
- **Target**: Base section 6 (append and restate) -> merged section 8
- **Before**: Base 6 had seven falsifiable claims and an inconsistency (6.1 no existing test edited versus 6.2 add to the static check).
- **After**: 8.1 to 8.8: isolation claim (inconsistency resolved to a new test file; AM-5 contested), conformance fixtures (CRITICAL in a non-representative member, join miss, empty claim, missing ranges added), T1 parity with probe INV-019, U-001, T3, T4 and groundability, standing and drop tests, measurements M1 to M4, T0 only on promotion. The M-label collision with research/13 is resolved by prefixing the research/13 modules with "r13".
- **Provenance tag**: `<!-- Source: Base (original, modified) — base section 6 kept in shape; restated and extended per Change #9 with Variant B's tests and measurements (B section 6, B-R2 section 6) and A-R2 section 5 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 10: Router facts from B; "CRITICAL never lowered" contested
- **Status**: Applied
- **Source**: diff-analysis U-004, U-008 to U-010; B sections 3.2 item 3b, 3.4, 3.1 item 3; B-R2 D2, AM-2
- **Target**: Base sections 2 and 4 -> merged 2.4 (and 6.2)
- **Before**: Base 2 and 5 stated the table "never lowers a CRITICAL" as a strength.
- **After**: 2.4 gives the default table (A-R2 row 10, 55), the route facts (`severity_router.py:56-58, :203-214`), U-008, U-009, U-010, and states "never lowers a CRITICAL" as contested (B-R2 D2, unanswered by A); 6.2 says the table restates the CRITICAL row only.
- **Provenance tag**: `<!-- Source: Variant A Round 2 section 4 row 10 (default table) and Variant B (Proposal B) sections 3.1 item 3, 3.2 item 3b, 3.4 via diff-analysis U-008 to U-010 — merged per Change #10; the "never lowers a CRITICAL" claim recorded as contested -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 11: Prerequisites owned elsewhere
- **Status**: Applied
- **Source**: A-R2 section 5 condition 5; B-R2 AM-6, D7; diff-analysis A-003; probe INV-005, INV-018
- **Target**: Base section 2 (shared core bullets) -> merged 2.5
- **Before**: Base 2 named FX-5 only as "needed under either position".
- **After**: 2.5: category vocabulary (6 core versus 18 router values, whole-block invalidation), the contested scope (category set only versus category, severity and lens), `snapshot_file_list` as the PR head tree (probe INV-004 addressed, probe INV-003 open), template and C-06 items, probe INV-018 on threading the parameter.
- **Provenance tag**: `<!-- Source: Variant A Round 2 section 3 "found on the way" and section 5 condition 5, Variant B Round 2 section 3 and AM-6 — merged per Change #11; the narrowing to the category set recorded as contested -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 12: Restate the invariant table
- **Status**: Applied
- **Source**: A-R1 and B-R1 "Invariants"; A-R2 section 5; B-R2 section 6
- **Target**: Base section 4 (replace) -> merged 5.1 to 5.5
- **Before**: Base 4 listed "preserved by construction" (INV-E, A, B, C, D, F, I) and "endangered or left open".
- **After**: 5.1 held (INV-E with narrow residual, INV-A, INV-B, INV-C not engaged, INV-D); 5.2 open in both files (INV-G, INV-I, INV-007 (R-C03), INV-003 (R-C01), INV-J, INV-K, INV-F); 5.3 B-R2 only (INV-L, INV-M, contested); 5.4 cadence; 5.5 unmeasured. INV-F moved from preserved to open, as A-R2 grades it. INV-A is restated: the only shared edit is the FX-5 parameters with today's constants as defaults (probe INV-017), where the base said no change to `findings_v2.py`.
- **Provenance tag**: `<!-- Source: Variant B (Proposal B), section 5 invariant table wording ("endangered in a narrow sense") — merged per Change #17 ...; base section 4 "preserved by construction" list restated per Change #12 -->` and `<!-- Source: Variant A Round 2 section 5 ("Invariants it leaves open") and Variant B Round 2 section 6 — merged per Change #12; INV-F moved from preserved to open per A-R2 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (prior-slot ids written INV-003 (R-C01) and INV-007 (R-C03); probe ids prefixed "probe")

### Change 13: Contested items from B's Round 2
- **Status**: Applied
- **Source**: B-R2 section 4 (D1 to D7) and section 6 (AM-1 to AM-6)
- **Target**: Base, new section "Contested amendments" -> merged section 7 (7.1 to 7.8)
- **Before**: Section did not exist.
- **After**: AM-1 to AM-6, D6 and a summary table; each with B's evidence, the amendment, Variant A's position or silence, and the probe findings beside it; every block labelled "not answered by Variant A (standard depth has no Round 3)" or equivalent; AM-5 recorded as either-acceptable.
- **Provenance tag**: `<!-- Source: Variant B (Proposal B), Round 2 B section 4 (D1 to D7) and section 6 (AM-1 to AM-6) — merged per Change #13 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 14: Consistency with C-01, C-02, C-03
- **Status**: Applied
- **Source**: A section 5; B section 2; ADJUDICATION-RESULT files of C-01, C-02, C-03 (as summarised in the base and the debate files; the result files were not opened)
- **Target**: Base section 5 (update) -> merged section 6
- **Before**: Three paragraphs; C-03 proposed a quorum helper.
- **After**: Three paragraphs kept; C-03 updated for the strict rule; B's dependencies added (C-06 over-limit lines, `findings_v2.py:111`; the quorum rule is decided work, not code, at HEAD); A's statement that it does not fire C-01 trigger T-a kept; "requested, not served" kept. The literal quorum-floor expression is paraphrased.
- **Provenance tag**: `<!-- Source: Base (original, modified) — base section 5 paragraphs kept; the C-03 paragraph rewritten for the strict rule (no quorum helper) per Change #14 and Change #3; B's dependencies added from Variant B section 2 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 15: Carry the Round 2.5 findings
- **Status**: Applied (with one note)
- **Source**: `invariant-probe.md` (20 findings: 6 ADDRESSED, 14 UNADDRESSED)
- **Target**: Base, new section "Invariants left open by the debate" -> merged section 11 (11.1 to 11.3)
- **Before**: Section did not exist.
- **After**: 11.1 the five HIGH findings and 11.2 the nine MEDIUM findings, each with assumption, evidence and category quoted from the probe, unresolved; 11.3 the six ADDRESSED findings. Every probe id is written "probe INV-0xx". The probe's "T:" and "V1:" line references are rewritten as `debate-transcript.md:` and `variant-1-original.md:` references.
- **Note**: the plan puts this section "before 'Changes not made'", but the base has no such section and the plan's own list of new sections does not include one. To make the plan's reference resolvable, the merge added section 12 "Alternatives not adopted (changes not made)" from the plan's "Changes NOT Being Made" table (rows copied; the two phrases of the withdrawn quorum rule paraphrased). This is carried content of the plan, not new debate content; flagged for the orchestrator.
- **Provenance tag**: `<!-- Source: Variant B (Proposal B) and Variant A Round 2 debate, Round 2.5 invariant probe (invariant-probe.md) — merged per Change #15; ... -->` and `<!-- Source: Base (original, modified) — new section per Change #15 and Change #17; rows copied from the "Changes NOT Being Made" table of the refactoring plan; ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 16: Winner, conditions, convergence, what would change the outcome
- **Status**: Applied
- **Source**: A-R2 section 5, B-R2 section 6, `debate-transcript.md`, `base-selection.md`
- **Target**: Base section 1 (replace) -> merged section 1 (1.1 to 1.5)
- **Before**: One paragraph stating position A.
- **After**: 1.1 the resolution C10-R (A-R2 naming, confidence 70%) and the one-paragraph statement; 1.2 the winner and base selection (quant A 0.9237 and B 0.9359; qual A 23/30 and B 24/30; combined A 0.8452 and B 0.8679; margin 2.27%; debate points 9 against 6; tiebreaker level 1); 1.3 debate status (49 of 49 by label, 44 of 49 content-adjusted = 0.90, BLOCKED_BY_INVARIANTS, unresolved points C-001, C-002, C-006, S-004, S-008, owner items C-008, A-005, A-006); 1.4 settled versus contested; 1.5 what would change the resolution (A-R2 promotion triggers; B-R2 conditions).
- **Provenance tag**: `<!-- Source: Base (original, modified) — the one-paragraph position of the base replaced by the resolution statement per Change #16; paragraph taken from Variant A Round 2 section 5 (A-R2 section 5) -->` and the four tags of 1.2 to 1.5
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (B's C10-R-B named and recorded as contested)

### Change 17: Form points where the debate named Variant B (S-006, S-009, S-010)
- **Status**: Applied
- **Source**: matrix S-006 (B, 58), S-009 (B, 58), S-010 (B, 55); A-R2 section 7; B-R2 section 8
- **Target**: Base section 4 and a closing "Limits and open items" section -> merged 5.1, 13
- **Before**: Base 4 said "preserved by construction"; no limits section.
- **After**: 5.1 uses B's "endangered in a narrow sense" wording and records that S-006 went to Variant B; section 13 lists what was read only, what is [UNVERIFIED] or [RELIED], scope limits, B's own unread-files list (`variant-2-original.md` section 9), the open owner decisions and B's open items O3 to O6 with where the debate left them.
- **Provenance tag**: `<!-- Source: Variant B (Proposal B), section 9 "Limits of this proposal" and open objections O3 to O6 — merged per Change #17 (S-009 and S-010: ...) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: PASS. 1 H1 (title), 13 H2 (sections 1 to 13), 49 H3, 0 headings of level 4 or deeper. No level gap (every H3 sits under an H2; the file starts with three provenance comments and then the H1). Heading list checked by `grep -n '^#{1,6} '`.
- Section ordering: PASS. Position and resolution first; design before release scope; release scope before evidence; invariants before consistency; contested amendments after the settled design and before the tests; open invariants, alternatives not adopted and limits last.
- Document flow: PASS. Every contested block is labelled in place, then collected in section 7 and section 13.
- Provenance: 33 `<!-- Source: ... -->` tags plus the three-line header (Provenance, Base, Merge date). Every H2 and every significant block carries a tag; paragraph-level blocks inside a tagged section (for example the "Missing `changed_ranges`" and "Per-cluster conversion" paragraphs of 2.2) are covered by the section tag and labelled in text.

### Internal References
- Total references: 68 candidate references to "section N" or "section N.M" matched by pattern; 4 of them cite source documents (for example "A-R2 section 5"), so 64 point into the merged document.
- Resolved: 64
- Broken: 0. Targets checked against the heading list: sections 1, 1.3, 1.5, 2.1 to 2.6, 3.2, 3.3, 4, 4.1 to 4.3, 5, 5.1, 5.2, 6, 7, 7.1, 7.5, 8, 8.2, 8.8, 11.
- Other internal labels (C10-R, AM-1 to AM-6, D1 to D7, INV-A to INV-M, T0 to T4, M1 to M4) are defined where first used or in the header.

### Contradiction Re-Scan
Checked by grep over the merged file; none of the six withdrawn claims survives as a claim.
- A's "cluster output already holds what the adapter reads": absent (three provenance comments that quoted it were reworded; the one remaining "already holds" is A's premise about the diff, tagged [UNVERIFIED]).
- "highest member severity" as a cluster field: absent; the maximum over joined members is stated only as A-R2's aggregation, contested.
- "the 50 files" / "50 test files": absent; the count is 47 `test_*.py` (49 `.py`) and the earlier figure is described as wrong.
- "downstream only reads path, line, body, category and the route": absent as a claim; withdrawn in 4.2 and 10 (the expression "four fields" appears only in the withdrawal).
- `min(2, requested)` as a rule: absent; the withdrawn floor is paraphrased; the only `min(` is `min(group, key=...)` in the representative rule (`cluster.py:338-344`).
- B's "a C-03 quorum refusal" as an existing rule: absent; 2.3 and 6.3 say no such rule exists at HEAD in `cli/review` or `pr_submit` (0 matches).
- New contradictions introduced by the merge: 0.
- Tensions carried from the sources, labelled in the text and not introduced by the merge: (1) A-R2's "no existing test edited" against AM-5 and probe INV-002 (1.1, 5.1, 8.1); (2) the standing rule's "requested" quantity against probe INV-007 (2.3, 11.1); (3) the C-009 evidence line in the matrix ("never lowers a CRITICAL") against B-R2 D2 (2.4, 7.2); (4) INV-I "held as reporting only" against probe INV-015 (5.2, 11.2).
- Other checks: no path or text from the run-1 task folder or the run-1 queued file (grep for both names: 0 matches); no emoji (grep over the emoji ranges: 0 matches); probe ids always carry the "probe" prefix or are the prior-slot ids INV-003 (R-C01), INV-007 (R-C03), INV-006 (R-C03) (checked with a negative-lookbehind grep; after two fixes, no bare probe-set id remains); no leftover work marker (`END-OF-DOCUMENT` count 0).

### Residual items for the orchestrator (none blocks the merge)
1. Section 12 was added to resolve the plan's "before 'Changes not made'" reference (Change 15 note).
2. Citation conflict: the base cited `reviewers.py:75-80` for `reviewer_activity`; X-002 and B-R2 (both read at HEAD) give `:73-78`; the merged text uses `:73-78` and says so in section 13.
3. The base wording "does not go through `review merge`, the ledger or `annotate`" is kept (2.1); `annotate` is also used inside `cluster.py` (`:148-154`) to build each member's `primary_citation`, and the debate files do not say whether R-C01's "locator-agnostic `annotate`" is the same function. Left as written in the sources.
4. The probe's phrase "L3 fix push" (probe INV-001) is quoted as written and is not defined in the debate files.
5. Variant B's original was read only for sections 5, 8 and 9 (see Metadata).

## Summary
- Total changes planned: 17
- Successfully applied: 17
- Failed: 0
- Skipped: 0
- Post-merge validation: PASS
