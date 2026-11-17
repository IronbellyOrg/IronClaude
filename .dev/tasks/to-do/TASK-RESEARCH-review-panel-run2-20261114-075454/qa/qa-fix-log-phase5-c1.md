# Gate 2 Fix Log - Cycle 1 (Phase 5)

Task: TASK-RESEARCH-review-panel-run2-20261114-075454, Item 5.28
Input: qa/qa-consolidated-findings-phase5.md (F_0 = 8, table 1a, P5-001 to P5-008). Table 1b (P5-009 and later) is minor and untouched.
Fix agent: single rf-qa instance, fix_authorization: true. Edits limited to synthesis/ and this log.

Status: Complete (all 8 blocking findings P5-001 to P5-008 fixed; verification results at the end)

Finding index: P5-001, P5-002, P5-003, P5-004, P5-005, P5-006, P5-007, P5-008.

## Per-finding log

### P5-001 (false "served model_id" diversity claim) - FIXED

Fact check before editing: `openai_compat.py:467-470` stamps the requested model (R04 lines 62-64, 93-94 carry the code read and the negative grep); `_diversity.py:8-15` counts distinct `worker.model_id`.

| File | Section | Before (one line) | After (one line) |
|---|---|---|---|
| synth-01 | 2.1 table row "Diversity evidence" | `from SERVED worker model_id values (_diversity.py:8-36), vocabulary full / insufficient` | `from the REQUESTED id stamped by the transport (_diversity.py:8-15, openai_compat.py:467-470; the response model field is never read) ...` with a source note that R04 s3.3, s4.1 corrects R06's word "served" |
| synth-01 | 2.1 "Contradictions between research files" (line 156) | `None remain open ... Two were resolved ...` (R04-over-R06 pair absent) | `Three were resolved ...`: new item (1) is the R04-over-R06 served-versus-requested pair; old items renumbered (2), (3) |
| synth-01 | closing "Cross-file contradictions" table | 10 rows, no served-versus-requested row | new row: engine A diversity SERVED or REQUESTED, R04 side used (code read plus negative grep) |
| synth-05 | 6.8 engine table row "Diversity evidence" | `from served model_id values` | `from the requested model id stamped by the transport (WorkerResult.model_id = self._model, openai_compat.py:467-470 ...)` |
| synth-05 | 6.8 option 2 Pros | `... single engine (R06 section 4.4). Diversity stays computed from served ids.` | sentence "Diversity stays computed from served ids." deleted |
| synth-05 | 6.8 option 3 Cons | `Loses ...: diversity measured from served model ids instead of pins (...), headless operation ...` | served-id loss deleted; remaining losses kept (stub lane, fallback ladder, snapshot-grounded children); added that engine A's diversity is over requested ids so no served-model measurement is lost |
| synth-06 | slot C-04 "Why the evidence cannot decide" | `A loses the only code-enforced gate, served-model diversity, headless operation, the ladder` | `A loses headless operation (stub lane), the bounded fallback ladder and the snapshot-grounded children; the fail-closed exit map and atomic write-back live in runner.py and survive either way; engine A's diversity is over REQUESTED ids ...` |
| synth-06 | Table G, 6.12.8, 6.12.10 | RX-1..RX-14; table G 27 rows; total 188; DECIDED 133 | new row RX-15 (R04 over R06, DECIDED-BY-EVIDENCE [CODE-VERIFIED]); 6.12.8 row r06 names RX-15; table G 28 rows, total 189, DECIDED 134; "14" to "15" in the documentation-contradictions row |
| synth-07 | "Contradictions between research files" | C-1..C-18 | new row C-19 (same pair, R04 stronger, points to synth-06 RX-15) |
| synth-09 | file inventory row (line 147) | `diversity from served model ids (_diversity.py:8-36) | R06 s2, s4.4` | `diversity over the REQUESTED model ids stamped by the transport (_diversity.py:8-15, openai_compat.py:467-470) | R06 s2, s4.4; R04 s3.3, s4.1` |

### P5-002 (adjudication markers do not match the 15 routed slots) - FIXED

Slug set of the 15 slots read from synth-06 6.12.9 (C-01 to C-15). All edits in synth-07 except where stated.

| File | Section | Before (one line) | After (one line) |
|---|---|---|---|
| synth-07 | "Choices the evidence cannot decide", markers A-3 to A-14 | 12 markers with their own slugs (`quorum-rule-two-valid-reviewers`, `blocking-rule-typed-vs-computed`, ... none equal to a slot slug) | each marker carries the slot slug verbatim by the Evidence-cell mapping: A-3 `merge-verdict-policy-and-quorum` (C-03), A-4 and A-9 `ledger-clearing-and-verdict-authority` (C-02), A-5 `limits-repair-policy` (C-06), A-6 `panel-resolution-and-tier-source` (C-09), A-7 `dispatch-and-launch-mechanism` (C-07), A-8 `reflect-tier2-engine-composition` (C-04), A-10 `run-record-and-served-model-capture` (C-08), A-11 `eval-acceptance-and-harness-owner` (C-14), A-12 `tasklist-medium-and-fidelity-vocab` (C-15), A-13 `consumer-entry-effect-and-delivery` (C-05), A-14 `pr-review-wire-format-and-slot` (C-10); each marker also names its slot |
| synth-07 | same table | no marker for C-01, C-11, C-12, C-13 and the metric-of-record part of C-14 | new rows A-15 (axis 1, C-01 `core-shape-and-finding-contract`), A-16 (axis 2 unknown keys and `prior`, C-01), A-17 (axis 11 rf-qa first step, C-11 `rfqa-first-step-and-readonly-scope`), A-18 (axis 6, C-12 `collaboration-exchange-capability`), A-19 (axis 7, C-13 `process-redesign-modules`), A-20 (axis 9 metric of record, C-14); each with the evidence for each side taken from synth-06 slots and synth-05, and the recommended default stated |
| synth-07 | axes table rows 6, 7, 9, 11 "Chosen" cells | no pointer to a marker | "PENDING: marker A-18, slot C-12", "A-19, slot C-13", "A-11 and A-20, slot C-14", "A-17, slot C-11" appended |
| synth-07 | intro of the choices table | one sentence | adds the rule (slug = slot slug verbatim, A-n kept, slots shared by A-15/A-16, A-4/A-9, A-11/A-20) and the retirement of A-1 and A-2 (see P5-003) |
| synth-07 | "Adjudication register" | 14 rows, 14 own slugs | 18 rows: slug verbatim from the slot, slot column, default; slot coverage line (all 15 slots) |
| synth-07 | "Rules check" line | `the 14 adjudication markers ... appear once` | `the 18 adjudication markers ... equal to the slug of a synth-06 6.12.9 slot (15 distinct slugs ...)` |

### P5-003 (convergence threshold and single-vendor: three statuses in three files) - FIXED (option a)

Facts re-read before editing: `contract.py:286-288` (single vendor returns `single-vendor` unless `allow_single_vendor`), `contract.py:310-326` (a present score below 0.80 returns `low-convergence`), `tests/cli/reflect/test_verdict_mapping.py` has 36 `def test_`. synth-06 CV-1 and CV-2 were left as they stand (DECIDED-BY-EVIDENCE).

| File | Section | Before (one line) | After (one line) |
|---|---|---|---|
| synth-05 | 6.8 axis status | `UNDECIDABLE-BY-EVIDENCE for the convergence threshold (0.75 versus 0.80) and the single-vendor posture ...` | `DECIDED-BY-EVIDENCE for the convergence threshold (0.80) and the single-vendor posture (degrade unless --allow-single-vendor) ... skill prose is to be reconciled (synth-06 CV-1, CV-2)` |
| synth-05 | 6.8.c table, both Decision-record cells; code cite `contract.py:287-288` | `none found (R06 gap 11, OQ-5)` / `none found (R06 section 5.4)` | `Decided by the code: ...` (CV-1, CV-2) with the skill-prose reconciliation as a follow-up; cite corrected to `contract.py:286-288` and `:310-326` |
| synth-05 | line for 6.8 in the axis-status summary (was line 878) | `UNDECIDABLE-BY-EVIDENCE (threshold, vendor posture, engine choice) ...` | `UNDECIDABLE-BY-EVIDENCE (engine choice); threshold (0.80) and single-vendor posture (degrade) are decided by the code ...` |
| synth-05 | OQ-5 | `which convergence threshold is intended, 0.75 or 0.80` | `whether any decision record exists for the 0.75 in the skill prose (none found); the enforced threshold is 0.80 ...` |
| synth-05 | 6.4 option risk cell and 6.8 option 4 Cons (consequential) | `the 0.75 versus 0.80 threshold conflict is open` / `The threshold, diversity vocabulary, vendor posture and merge_method meaning still need a single decision` | threshold and vendor posture stated as decided by the code; diversity vocabulary and `merge_method` still open |
| synth-07 | choices table | rows A-1 and A-2 with markers | both rows and both markers removed; a "Decided by evidence, so not pending" note after the table states the decision, the code cites, CV-1/CV-2 and the skill-prose follow-up |
| synth-07 | I-2 (line 138 before), defect-table row for DR 133/134, contradiction C-17, coverage row r06 | `(marker A-1)` / `Markers A-1 and A-2` / `Unresolved; ... marker A-1` / `A-1, A-2, A-8` | decided wording, no A-1 or A-2 reference |
| synth-10 | Section 9 row Q-08, Suggested Resolution (consequential) | `Resolve in synth-06 (conflict log) or by owner ruling in Section 9; ...` | prefixed with the statement that threshold and single-vendor posture are decided by the code (CV-1, CV-2) |

### P5-004 (core shape and unknown-key policy decided without the options comparison) - FIXED (axes marked pending)

| File | Section | Before (one line) | After (one line) |
|---|---|---|---|
| synth-07 | axis 1 row | options (a) extend kernel, (b) E3i scripts, (c) engine A, (d) E2 scripts; chosen (a) | the four candidates of synth-05 6.1 (A v2 kernel, B v1 package, C thin contract, D fix and defer) listed, the three ruled-out bases named; default A kept, marked PENDING (marker A-15, slot C-01); evidence for the default stated; what the evidence cannot decide (A against B and C; D is an owner scope decision) stated |
| synth-07 | axis 2 row | `unknown keys stay accepted by the core (no whitelist)` as chosen; options without synth-05 6.2 options 1 and 3 | synth-05 6.2 options 1, 2, 3 listed; default option 2 kept; unknown-key policy, `prior` lines and v2-native re-review marked PENDING (marker A-16, slot C-01); one-wire-format question tied to A-14 / C-10; evidence for and against each option added |
| synth-07 | framing sentence before the F-1..F-6 table | `Verified facts that make this ONE design rather than a choice among several` | `Verified facts that bound the design to ONE shape ... they do not decide between the v2 kernel, the v1 package and a thin shared contract (axis 1, slot C-01, marker A-15)` |

No new comparison was invented: every evidence item added is taken from synth-05 6.1 and 6.2, synth-06 C-01 and CO-4, or research/01, 02, 13 as cited in those files.

### P5-005 (design inferences labelled DECIDED-BY-EVIDENCE) - FIXED

| File | Section | Before (one line) | After (one line) |
|---|---|---|---|
| synth-06 | C-S3 decision cell | `The core carries the boolean blocking as the only field that drives verdict, ledger brief and cap; MINOR is never blocking ...; Medium is not a core token ...` (under DECIDED-BY-EVIDENCE) | `Decided by code (verified facts): MINOR is never blocking; two blocking rules are shipped and selected by lens; Medium has no schema value in cli/review. Design inference, NOT decided by evidence (research/12 section 8, Q1 and Q5; synth-10 Q-04 / GQ-159; the owner confirms in Section 9): the core carries blocking as the only field ...` |
| synth-06 | SV-5 decision cell | `The core carries max_fix_cycles = 2 ... and a halt-reason enum ...` | `Decided by code (verified facts): caps agree at 2 ...; outliers ...; test_f ... Design inference, NOT decided by evidence (research/12 section 8, Q1 and Q3; synth-10 Q-04): the core carries max_fix_cycles = 2 ... and a halt-reason enum ...` |
| synth-06 | 6.12.10 "What the evidence decided" rows 1 and 3 | the two rulings stated as decided | rows keep only the verified code facts; a new paragraph "Design inference, not decided by evidence" names the rulings, research/12 Q1, Q3, Q5, synth-10 Q-04 / GQ-159 |
| synth-06 | routing coverage paragraph (end of 6.12.9) and SV-1, SV-2 (consequential) | listed `blocking` boolean and `no Medium token` as decided requirements | restated as design inferences the owner confirms |
| synth-07 | axis 2 "Chosen" and axis 4 "Chosen" | `the blocking boolean is the only field ...` / `cap default max_fix_cycles = 2 (3 reviews), a module may declare an override` | tagged `[DESIGN]` with the research/12 section 8 source, Q1 and Q3, and the pointer to synth-10 Q-04 (Section 9) |
| synth-10 | Section 9 | GQ-159 is already in row Q-04 (`blocking plus CRITICAL/MAJOR/MINOR as the core pair`, GQ-159 in its Source cell) | no new row added; synth-06 and synth-07 point to Q-04 |

### P5-008 (raw-id lane is not read-only, but the verdicts rest on read-only reviewers) - FIXED

Sources checked: synth-05 6.5 option 2 (`Edit Write NotebookEdit` disallowed only, Bash allowed, `run-reviewer.sh:48`; "Reviewers have Bash"; comparison row "reviewers need a read-only restriction at process level (R13 R1; W02 section 4)"), research/13 R1 (line 195).

| File | Section | Before (one line) | After (one line) |
|---|---|---|---|
| synth-07 | axis 5 "Chosen" | `a raw-id lane covers gateway models; one tier source feeds all lanes` | adds the "Read-only condition on every lane": each lane enforces the read-only reviewer contract at process or tool level; the raw-id lane is not read-only by construction and needs a process-level tool restriction; a lane that cannot is not offered to the PR and rf-qa modules; identity check and tool-restriction check are both acceptance checks (cites synth-05 6.5 option 2, r13 R1, W02 sections 4, 10) |
| synth-07 | A-7 (choices table) | evidence cell silent on read-only; default `Raw-id lane with a transcript identity check beside the Agent class-word lane` | evidence cell adds the not-read-only fact (FX-8, INV-G HIGH); default adds the condition (process-level tool restriction; lane excluded for PR and rf-qa otherwise; both acceptance checks) |
| synth-07 | 7.2.1 verdict (PR code review) | one condition | second condition added: reviewers read-only at process or tool level on every lane; untrusted PR diffs |
| synth-07 | 7.2.2 verdict (rf-qa) | `the final shape does NOT block it (NO). The /task phase gate ...` | adds the Condition (read-only at process or tool level on every lane; raw-id lane excluded unless restricted; synth-05 6.5 option 2, r13 R1) |
| synth-07 | 7.2.4 verdict table, PR and rf-qa rows | conditions without the lane condition | both rows carry the lane condition and cite synth-05 6.5 option 2, r13 R1, marker A-7 |

### P5-007 (VL-23-629 moved from CORE to MODULE-reflect against rule 8.1.1) - FIXED

Rule check: DR-139 is UNVERIFIED, so the ledger destination wins; VL-23-629's ledger destination was CORE (only VL-23-618 is MODULE-reflect). Counterparts VL-23-768 and VL-23-684 (CORE) and the synth-07 axis 8 decision (key allowlist moves into core CLI writers) agree.

| File | Section | Before (one line) | After (one line) |
|---|---|---|---|
| synth-08 | row VL-23-629 | in MODULE-reflect, Reason `moved from CORE: DR-139 (MODULE-reflect) merges ...` | moved to the CORE section (before VL-23-674); Destination CORE; ledger Reason kept, plus a note that DR-139 is UNVERIFIED so the ledger destinations win and that the legal-key lists (110 + 27 names) stay reflect data while their in-run enforcement is core code |
| synth-08 | row DR-139 (DROP) Reason | `... the ledger destination wins (MODULE-reflect) ...` | `... the ledger destinations win (VL-23-618 MODULE-reflect, VL-23-629 CORE) ...` |
| synth-08 | 8.1.3 P3-012 table row DR-139 | `VL-23-618 and VL-23-629 (MODULE-reflect)`; `VL-23-629 CORE to MODULE-reflect` | `VL-23-618 (MODULE-reflect) and VL-23-629 (CORE)`; `VL-23-629 CORE to CORE (...)` |
| synth-08 | 8.1.3 "Other single-row moves" bullet | `(5): VL-20-067, VL-23-267, VL-23-479, VL-23-629, VL-24-181` | `(4): VL-20-067, VL-23-267, VL-23-479, VL-24-181` |
| synth-08 | 8.1.1 provenance paragraph (moves figure) | `71 rows moved (... ledger 23: 3 ...)` | `70 rows moved (... ledger 23: 2 ...)` |
| synth-08 | 8.1.1 provenance paragraph (checks sentence) | `... two rows from CORE to MODULE-reflect (VL-23-629 with DR-139, and VL-24-181 ...)` | `... one row from CORE to MODULE-reflect (VL-24-181 ...); VL-23-629 stays CORE ...` |
| synth-08 | 8.1.0 table (derived numbers) | CORE 947, MODULE-reflect 280; ledger 23 row 252 / 217 | CORE 948, MODULE-reflect 278 (279 after this finding, 278 after P5-006's DR-147); ledger 23 row 253 / 216; total row updated (see P5-006 for the final table) |

### P5-006 (same defect kept on two inventory rows with two destinations) - FIXED for the pairs with a clear rule outcome

Rule applied (8.1.1): register row UNVERIFIED -> the register row becomes `DROP: duplicate of <kept ledger row>`; register row re-verified (REPRODUCED, TRACED) -> the ledger row becomes `DROP: duplicate of DR-nnn`. The repro status was read from each register row itself, not from the finding text (DR-042 is REPRODUCED by Glob, so the ledger row VL-23-007 became the duplicate, not DR-042).

Rows moved (8; each removed from its old destination section, inserted in the DROP section in ID order; Reason uses the existing pair-row form `DROP[duplicate]: duplicate of <kept>; was <old destination>: ...; item P3-012. <original Reason>`):

| Row | Before | After | Kept row |
|---|---|---|---|
| DR-039 | EVAL | DROP | VL-19-036 (HARNESS; VL-20-345 also HARNESS); register UNVERIFIED |
| DR-098 | EVAL | DROP | VL-20-743 (CORE); register UNVERIFIED |
| DR-103 | EVAL | DROP | VL-20-113 (KNOWLEDGE); register UNVERIFIED |
| DR-147 | MODULE-reflect | DROP | VL-23-518 (EVAL); register UNVERIFIED |
| VL-20-241 | HARNESS | DROP | DR-086 (EVAL); REPRODUCED |
| VL-23-535 | HARNESS | DROP | DR-140 (MODULE-reflect); REPRODUCED by reading |
| VL-23-007 | KNOWLEDGE | DROP | DR-042 (CORE); REPRODUCED by Glob |
| VL-19-351 | EVAL | DROP | DR-073 (CORE); TRACED |

Note on the original Reason text: for the four register rows the original Fix owner and Repro text is kept after the label; only the sentence "Kept row for the defect; ledger rows ... carried as DROP duplicates or notes: ..." was dropped because it is false once the row is the duplicate (the already-converted register rows, for example DR-034, drop it the same way).

Reason texts corrected (no destination change):

| Row | Before (one line) | After (one line) |
|---|---|---|
| VL-19-256 | `[same defect as DR-039 (kept row; register row UNVERIFIED but the ledger rows are all DROP)]` (false: VL-19-036 and VL-20-345 are not DROP) | `[same defect as DR-039 (DR-039 is itself DROP, duplicate of VL-19-036: the register row is UNVERIFIED, so the ledger rows VL-19-036 and VL-20-345 (HARNESS) are the kept rows)]` |
| VL-20-779, VL-20-791, VL-23-626 | `[same defect as DR-098 / DR-103 / DR-147 (kept row; register row UNVERIFIED but the ledger rows are all DROP)]` | each now says the register row is itself DROP, duplicate of the named kept ledger row and gives its destination |
| VL-20-464 | same false note for DR-084 | note states DR-084 stays a kept row but VL-20-077 (CORE), VL-20-076 (EVAL), VL-20-350 (HARNESS) are not DROP and sit in three destinations, so no single kept row: open, see 8.1.4 limit 3b |
| VL-20-471 | `Duplicate of VL-20-241 [...]` (VL-20-241 is now a duplicate itself) | `Duplicate of DR-086 [...; VL-20-241 is also DROP, duplicate of DR-086]` |
| VL-23-619 | `Duplicate of VL-23-535 [...]` (same chain) | `Duplicate of DR-140 [...; VL-23-535 is also DROP, duplicate of DR-140]` |
| DR-086, DR-140, DR-042, DR-073 (kept rows) | twin lists without the new rows | VL-20-241, VL-23-535, VL-23-007, VL-19-351 added |

Tables and prose recomputed (read-only `grep -c` / `awk` on the finished file, before and after):

| Figure | Before | After |
|---|---|---|
| 8.1.0 ledger 19 row (EVAL, DROP) | 96, 500 | 95, 501 |
| 8.1.0 ledger 20 row (HARNESS, DROP) | 138, 309 | 137, 310 |
| 8.1.0 ledger 23 row (CORE, MODULE-reflect, HARNESS, KNOWLEDGE, DROP) | 252, 217, 20, 26, 186 | 253, 216, 19, 25, 188 |
| 8.1.0 register row (MODULE-reflect, EVAL, DROP) | 18, 23, 49 | 17, 20, 53 |
| 8.1.0 total row | CORE 947, MODULE-reflect 280, EVAL 1,369, HARNESS 469, KNOWLEDGE 417, DROP 1,961, total 5,950 | CORE 948, MODULE-reflect 278, EVAL 1,365, HARNESS 467, KNOWLEDGE 416, DROP 1,969, total 5,950 |
| Reconciliation line: ledger rows naming a DR row as kept / register rows naming a ledger row as kept / together | 114 / 39 / 153 | 118 / 43 / 161 |
| DROP by reason: duplicate / obsolete / out of scope / CODE-CONTRADICTED / total | 1,745 / 126 / 86 / 4 / 1,961 | 1,753 / 126 / 86 / 4 / 1,969 |
| 8.1.1 "each defect has one kept row" | claimed for every defect | claimed for the listed pairs; eight further pairs fixed; open pairs listed in new 8.1.4 limit 3b; no new full re-scan claimed |
| 8.1.3 P3-012 table | DR-073, DR-140, DR-147 rows | those three rows updated; rows added for DR-039, DR-086, DR-042, DR-098, DR-103 |

Pairs NOT changed (no single clear rule outcome, per the orchestrator direction; they stay as minor note P5-068 and are listed in 8.1.4 limit 3b): DR-084 (three ledger rows in three destinations), DR-138 (three EVAL ledger rows, absent from the finding's proposed-fix list), DR-135 with VL-23-444, DR-082 with VL-20-195, DR-128 with VL-23-449, DR-154 with VL-23-664, DR-080 with VL-20-309, DR-004 with VL-20-777.

## Post-edit verification (all read-only; results)

| Check | Result |
|---|---|
| `grep -c 'PENDING-ADJUDICATION'` in synth-07 | 18 (lines); 18 occurrences; none in any other synth file |
| marker well-formedness | 18 of 18 match `[PENDING-ADJUDICATION: <kebab-case slug>]`; longest slug 37 characters (limit 40) |
| slug set against synth-06 6.12.9 | every marker slug equals the slug of a slot row C-01 to C-15; all 15 slots covered; shared slots: C-01 (A-15, A-16), C-02 (A-4, A-9), C-14 (A-11, A-20) |
| `ADJUDICATION-FOLD-PENDING` | exactly 1 row, synth-10 line 186, unchanged; 0 in any other synth file |
| synth-08 `grep -c '^| VL-NN-'` per ledger 19, 20, 21, 22, 23, 24 | 886, 868, 1,685, 955, 796, 589 (sum 5,779) |
| synth-08 `grep -c '^| DR-'` | 171 |
| rows in against rows out | 5,779 + 171 = 5,950 in; 5,950 out (sum of the ten destination sections: 948 + 278 + 340 + 69 + 45 + 53 + 1,365 + 467 + 416 + 1,969) |
| duplicate row IDs | none |
| every row under the heading equal to its destination; DROP rows start with `DROP[`; no non-DROP row does | 0 violations (awk over the file) |
| forbidden run-1 paths (`TASK-RESEARCH-review-panel-unify-20261113-155942`, `REVIEW-PANEL-UNIFY-RUN2-QUEUED`) in synthesis/ | 0 mentions in every file |
| files modified after the consolidated findings file | synth-01, 05, 06, 07, 08, 09, 10 and this log; also the task file itself (`TASK-RESEARCH-review-panel-run2-20261114-075454.md`), which this agent did not edit (the orchestrator updates it); no other file under the task folder; no file outside it |

## Findings not fixed

None of the eight blocking findings is left open. Findings of table 1b (P5-009 and later) were not touched, as directed.

## Residual notes for the re-review (not blocking findings)

- P5-002 and P5-004: axes 1 and 2 are now marked pending with the C-01 slug rather than decided; synth-07 keeps the recommended default for both and states which evidence supports it.
- P5-003: the skill-prose reconciliation (0.75 / 0.60 band, warn-only) is stated as a follow-up in synth-05, synth-07 and synth-10 Q-08; it is not an adjudication slot.
- P5-005: no new Section 9 row was added; GQ-159 is already in synth-10 Q-04 and the synth-06 and synth-07 edits point to it.
- Consequential edits outside the finding's named cells (kept minimal): synth-05 6.4 risk cell and 6.8 option 4 Cons; synth-06 SV-1, SV-2, the routing-coverage paragraph and the 6.12.8 and 6.12.10 counts; synth-07 I-2, the defect-table row for DR 133/134 and the r06 coverage row; synth-10 Q-08.

Status: Complete

