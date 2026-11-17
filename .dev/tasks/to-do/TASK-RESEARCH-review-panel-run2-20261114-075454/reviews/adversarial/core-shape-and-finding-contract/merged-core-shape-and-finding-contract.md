<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant B (opus:architect+qa) -->
<!-- Merge date: 2026-11-14 -->

# Merged position: slot C-01 (core-shape-and-finding-contract)

<!-- Source: Base (original, modified) - title, status and tag convention adjusted for the merged document; [DEBATE-VERIFIED] and [design inference] tags added per the merge brief -->
Status: Complete (merged after debate; convergence BLOCKED_BY_INVARIANTS, see sections 8 and 9)
Position: B (thin shared contract with per-module engines), as narrowed by the debate
Conflicts in scope: C-S1, CO-1, CO-2, CO-3, CO-4, CL-X11 (placement), FX-1, FX-2 (synth-06 6.12.1, 6.12.2, 6.12.5; undecidable-conflicts.md row C-01)
Axis: synth-05 6.1 (core shape, option C) and 6.2 (finding contract, option 1; unknown keys open in both parsers)
Tag convention: [CODE-VERIFIED] = the cited line was read at HEAD 50d4d2b9d by the author of the variant the text comes from, or re-read by the merge executor during this merge; [DEBATE-VERIFIED] = both advocates re-read the fact in code in the debate transcript (Rounds 1 and 2) and the merge executor did not re-read it; [CODE-CONTRADICTED] = the code differs from the stated claim; [UNVERIFIED] = taken from a research or synthesis file and not re-read in code (the file is named); [design inference] = a design step, not a code fact.

## 1. The position in one paragraph

<!-- Source: Base (original, modified) - guard sentence replaced per Change 1, unknown-key clause per Change 3, repair placement per Change 8, stuck-row surfacing per Change 4 -->
The shared core is a thin, versioned contract, not a merged engine. It owns only what is already shared or can be fixed once for every engine: the finding id grammar, the shared limit constants and one repair or itemise step called inside both parsers (the policy is chosen in C-06), the per-module reference-token pattern list (so `T01.02` is fixed once), hashing and identity helpers, panel resolution (`panel.py`, already shared), the run record (location chosen in C-08), and the evaluation harness (X-14). Engines stay per module: the v1 anchor parser, `merge_round` and `review-ledger/1` keep serving spec review as they are; the v2 citation kernel (`findings_v2.py`, `cluster.py`, `verify_cmd.py`, `manifest.py`) serves reflect and PR review; unknown keys stay open in both parsers, as today; and convergence of the two pipelines is deferred until the trigger in section 5.4 fires. The missing locator-agnostic `annotate` is not a crash on the shipped path, because the v1 parser already rejects a line without an anchor before `annotate` runs (E-3); it is deferred, not scheduled now. The one engine-local change C-01 makes is to surface, for each blocking row, whether its anchor was found, missing or ambiguous, in the per-row block that `render_merged_report` prints (section 2.3).

## 2. Design consequence for the shared core and the named modules

### 2.1 What the contract contains (and nothing else)

<!-- Source: Base (original, modified) - "Projection view" row removed per Change 2; "Limit constants and repair step" row edited per Change 8; other rows Base (original) -->
| Contract element | Content | Today | Cost under B |
|---|---|---|---|
| Finding id grammar | `^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$` | one regex; v2 imports it from v1 (`findings_v2.py:15-22`, used at `findings_v2.py:99-100`) [CODE-VERIFIED] | none (already shared) |
| Limit constants and repair step | anchor and quote 12..200, claim at most 300, refs at most 8, citations 1..8; one normalise-or-itemise function called from inside both `parse_block` functions (`findings.py:124`, `findings_v2.py:215`), on each line before the check; it must not invent an anchor for a citation-only line. A repair placed in the callers (for example inside `merge_round`) would miss the other callers and the v2 path (debate N-B3; advocate A agreed in Round 2) | v2 restates the numbers as literals (`findings_v2.py:111,114-120,126,128,132,136`) [CODE-VERIFIED]; v1 has the same numbers at `findings.py:104,108,114,118` [CODE-VERIFIED, re-read in this merge] | one constants module imported by both parsers, names checked against INV-K by running `make lint-architecture`; one repair function (policy: C-06). Qualified by INV-003 (HIGH), INV-004, INV-010, INV-014, INV-022 and INV-024 (section 9): INV-003 shows that a repair policy that rescues over-limit lines and test T1 "every existing pin unmodified" (section 5.1) cannot both hold |
| Reference-token list | per-module pattern list behind `refs_norm`, with `T<PP>.<TT>` added for the tasklist module | `findings.refs_norm` (`findings.py:321-337`) is called by `cluster.annotate` (`cluster.py:141`) [CODE-VERIFIED]; the pattern `_REF_TOKEN` is `findings.py:29` [CODE-VERIFIED, re-read in this merge]; a second copy sits at `telemetry.py:23-27` [UNVERIFIED], research/02:79 | fixed once in `refs_norm`; both clusterers inherit it |
| Hash and identity helpers | `sha256_text`, manifest-frozen input hashes, requested, resolved and observed model | ledger entries keep `report_sha256` and `model` from the resolution only (`ledger.py:144,146`) [CODE-VERIFIED]; manifest side [UNVERIFIED], research/01:110 | helper functions plus a schema id per record |
| Panel resolution | `panel.py`, tier JSON, templates, `resolve_slot` | the one module both pipelines share besides the container, `refs_norm` and `_ID` [UNVERIFIED], research/scope/09:454 | none; C-09 decides the data owner |
| Run record | one adapter that writes the cross-run row from either engine's own state | four formats today [UNVERIFIED], research/01 s5 C-10 | decided in C-08, not here |
| Evaluation harness | tiers S, Q, G and `verify-run` | none in product | decided in X-14, not here |

<!-- Source: Base (original, modified) - the paragraph describing the projection view is removed per Change 2; the item is listed as deferred in 2.4 item 5 -->
The projection view first proposed in this table is not part of the contract; it is deferred until a consumer exists (section 2.4, item 5).

### 2.2 Module by module

<!-- Source: Base (original, modified) - spec-loop "Change needed" cell per Change 1 and Change 4; PR "Unknown keys" cell per Change 3; other cells Base (original) -->
| Module | Engine under B | Location type | Unknown keys | Change needed |
|---|---|---|---|---|
| Spec review loop | v1 `findings.py`, `ledger.py`, `merge_cmd.py`, `ledger_cmd.py`, unchanged in shape; fixes for D-1, D-2, D-11, D-13 belong to C-02 and C-03 and land inside this engine | quoted `anchor` (12..200) | open (INV-C) | adopt shared constants and the repair step; surface the anchor status of each blocking row in `render_merged_report` (2.3); no guard is added (2.3) |
| Reflect UC-1 and UC-2 (Tier 2) | v2 kernel inside the existing fail-closed shell (shell choice: C-04) | `citations` | open, as today | adopt shared constants, repair step and `refs_norm` list; no change to contract 1.8.0 names |
| PR code review | v2 citations, a pure adapter to `pr_submit.Finding`, no ledger (wire format: C-10) | `citations[0].line_start` becomes `line` (research/13:176, P1) [UNVERIFIED] | open in the core (E-21); any adapter-side strictness is decided in slot C-10 | module-supplied category, lens and severity sets (M2) in the v2 engine; `Finding`, `Severity` and the FSM untouched |
| rf-qa replacement, first step at the `/task` gate | v2 kernel plus the module's checklist mode; reviewer contract mechanically read-only | module's choice (a task file or phase output is a document; a code review is a path) | module's choice | per-slot lens, checklist output, agent-count rule (research/13 R1 to R3) [UNVERIFIED], all independent of the ledger shape |
| Tasklist and workflow | reached through reflect UC-1 (C-05) | as reflect | as reflect | `T01.02` ref pattern |

### 2.3 No boundary guard; the stuck row is surfaced instead

<!-- Source: Base (original, modified) - the typed LedgerError guard is withdrawn per Change 1 (debate Round 1 and Round 2, both advocates, A-001 REJECT) -->
No guard is added; the boundary already exists in the v1 parser. The typed `LedgerError` guard that the original proposal placed in `merge_round` is withdrawn, because the input it guarded cannot reach that point. `merge_round` takes its findings from `fnd.parse_block` (`ledger.py:128`). `_check_finding` runs `_check_flat(obj.get("anchor"), "anchor", 12, 200)` (`findings.py:104`), which returns "anchor must be a string" when the anchor is absent (`findings.py:80-81`); the line is recorded as an error and never reaches `parsed["findings"]` (`findings.py:188-192`), and `annotate` runs only on parsed findings (`ledger.py:135-136`) [CODE-VERIFIED, re-read in this merge]. The `KeyError` at `findings.py:349` is reachable only by calling `annotate()` directly. C-01 pins today's rejection instead (test 5.2): with one reviewer, the existing refusal "no reviewer produced a valid findings block" and an unchanged ledger; with several reviewers, a warning, `block_ok` false for that reviewer, the line lost, and the same reviewer's other valid lines still merged (`ledger.py:130-157`). The gap the debate named in place of the guard: a citation-only line is lost with only a warning, and a re-find dropped for format reasons cannot hold a `resolved_check` row open (E-19); both are routed to C-02 and C-03.

<!-- Source: Variant A, E11 and T5 (section 3.2, section 6), section 4 FX-2 row - merged per Change 4, with placement from the Variant B advocate's Round 2 (N-B1, N-B2, N-B4) -->
The stuck row (FX-2). A finding whose anchor is not found keeps `span None` (`findings.py:352`); the row is kept `open` and blocking (`test_review_ledger.py:408-417`). `apply_revision` moves a row to `resolved_check` only when a hunk touches its span, and `hunks_touch(None, ...)` is False (`findings.py:446-447`), so a fix map entry naming the row records `named_not_touched` (`ledger.py:331-339`). The only way the row gets a span is a later re-find with a locatable anchor (`ledger.py:226-231`); if the fix worked, nobody re-finds the defect. `anchor_status` and `anchor_ambiguous` are computed (`findings.py:350-351`) and read only by tests (E-20); the row stores neither (`ledger.py:184-202`) [CODE-VERIFIED, re-read in this merge].

The row fails closed, not open: `_brief_ids` keeps every blocking `open` or `regressed` row (`ledger.py:99-104`), `_decision` returns `ESCALATE` at the cap (`ledger.py:93-96`), and the escalation report says "do not start another fix cycle" (`test_review_ledger.py:476-490`) [CODE-VERIFIED, re-read in this merge]. `ledger defer` (`ledger.py:350-360`) is a manual, accepted-risk exit that recomputes the last decision to PASS when no other blocking id remains. The cost is a wasted fix cycle and a human escalation, not a wrong PASS.

The change C-01 makes, agreed by both advocates in Round 2:
1. `render_merged_report` (`ledger.py:408`) prints, for each blocking row, whether its anchor was found, missing or ambiguous, inside that row's `### Lx` block of `## Blocking findings` (`ledger.py:439-466`).
2. It is not printed in the reviser-brief id line: `test_rendered_merged_report` asserts that the reviser brief carries no non-blocking id, with the comment that the Stage 2 harness parses those ids (`test_review_ledger.py:459-467`) [CODE-VERIFIED, re-read in this merge].
3. No prompt-file change: `render_merged_report` is "the merged report the reviser and the next reviewer read" (`ledger.py:411`), so `document_review_loop_prompts.md` and its plugin mirror (INV-N) are untouched.
4. No configuration knobs in C-01. How an unlocated row may clear goes to slot C-02.

Caveats left open (section 9): INV-001 (the source of the status for a row not reported again in the current round is not named; that branch, `ledger.py:457-466`, reads only the row, and the row stores no status) and INV-015 (with empty refs, a re-find carrying the same bad anchor opens a new span-less row every round).

<!-- Source: Debate transcript, Round 2 (advocate A "Stuck-row defect"; advocate B comparison table) and Convergence Assessment - recorded disagreement per Change 4 -->
Recorded disagreement (the debate did not reconcile these two items; the advocate B Round 2 table records DISAGREE on both):

| Item | Advocate A (Round 2) | Advocate B (Round 2) |
|---|---|---|
| Form of the locator policy | Locator policy as data in the v1 engine, `on_missing` and `on_ambiguous`; `spec-loop` default: keep the row and surface the status | Hard-code "keep and surface" now; A's own default gives each knob one used value, which is a configuration value with no consumer; make it data when the engines converge |
| What the next round is asked | "Locate it or say it is gone" | Ask only that the row be re-located (that re-anchors, `ledger.py:226-231`); "say it is gone" can only be a `prior` line, which is inert (`ledger.py:259-272`); route it to C-02 |

This document uses the base approach for the first item (hard-coded keep-and-surface, per the refactoring plan's "Changes NOT being made", row C-008). The second item is not decided here.

### 2.4 What B defers, on purpose

<!-- Source: Base (original, modified) - item 3 reworded per Change 3; item 5 added per Change 2; items 1, 2 and 4 Base (original) -->
1. A v2-native re-review contract that replaces `prior` lines (CO-2). Under B, `prior` lines stay a v1-engine feature (`document_review_loop_prompts.md:61` [CODE-VERIFIED by Grep]); the v2 kernel has no re-review round because reflect has no finding ledger or rounds today [UNVERIFIED], research/01:150.
2. Which clustering the core adopts (CO-3). Both clusterers stay, each with a declared owner. Whether the line-insensitive v2 fingerprint is intended (`cluster.py:119-123` hashes role, path, an empty section, refs and class and never a line number [CODE-VERIFIED]; GQ-023, OQ-25) is answered inside the reflect engine with its own test, not by the core.
3. Any stricter unknown-key policy (CO-4). Unknown keys stay open in both parsers, as today, with no whitelist (E-21); v2 keeps rejecting `calibrated_confidence` (`findings_v2.py:96-97`). Strictness at an adapter has no evidence behind it and is decided in slot C-10.
4. A locator-agnostic ledger. It becomes work only when the trigger in section 5.4 fires.
5. The projection view (a read-only function that turns either engine's finding into one record for telemetry, export and the evaluation harness). Withdrawn from the contract in the debate because no consumer uses it yet (advocate A Round 1 weakness 5; advocate B conceded in Round 1 and Round 2); it is built when a consumer exists.

### 2.5 Answers to the routed rows

<!-- Source: Variant A, section 4 - merged per Change 5, answers updated to the debate result (Round 2 hybrids of both advocates) -->
| Row | Answer as the debate left it | Where |
|---|---|---|
| C-S1 core shape | Thin shared contract now, per-module engines; convergence to one engine only when the trigger fires | 1, 2.1, 5.4 |
| CO-1 location type and ledger path | Pin today's rejection: a citation-only line is rejected by the v1 parser (`findings.py:104`) before `annotate` runs (`ledger.py:135-136`). The locator-agnostic `annotate` and citation-keyed rows are deferred to the trigger | 2.3, 5.2, E-3 |
| CO-2 line grammar versions | `prior` unchanged and inert: v1 accepts it (`findings.py:175-187`), v2 rejects it (`findings_v2.py:279-283`), the ledger only logs a `prior_note` (`ledger.py:259-272`) [CODE-VERIFIED]. What a `prior` line should do goes to C-02. No brief change | 2.4 item 1 |
| CO-3 fingerprint and clustering | Both clusterers stay; the spec loop stays on v1 clustering; `cluster_v2` cannot cluster anchor-only findings (E-18). The convergence precondition is in 5.4 | 2.4 item 2, 5.4, E-18 |
| CO-4 unknown keys | Open in both parsers, no whitelist (E-21); v2 keeps rejecting `calibrated_confidence`; adapter strictness goes to C-10 | 2.2, 2.4 item 3 |
| CL-X11 placement of `origin` | In-line `origin` keeps working at parse time (INV-C). The ledger member record keeps only round, reviewer id, finding id and `blocking` (`ledger.py:172-180`) [CODE-VERIFIED]; storing passthrough keys in the ledger is deferred until a consumer reads provenance from the ledger | 4.1 INV-C |
| FX-1 over-limit whole-line drop | Shared limit constants plus one repair step called inside both `parse_block` functions; the policy is C-06. Qualified by INV-003 (HIGH) and INV-024 | 2.1, section 9 |
| FX-2 exact-substring anchors | Surface the anchor status of each blocking row in the `### Lx` block of `render_merged_report`; no knobs; the row fails closed and `ledger defer` is a manual exit; how an unlocated row may clear goes to C-02. Two disputes recorded | 2.3 |

## 3. Evidence

### 3.1 The two pipelines are disjoint, so a thin contract matches the code that exists

<!-- Source: Base (original, modified) - row E-3 corrected per Change 1 and Change 9; rows E-1, E-2, E-4, E-5 Base (original) -->
| # | Claim | Evidence | Tag |
|---|---|---|---|
| E-1 | No code path leads from v2 findings to the ledger. The v2 modules are imported by exactly six files: `scripts/reflect_cluster_pairs.py`, `scripts/reflect_stage0a_replay.py`, `cli/review/verify_cmd.py`, `cli/review/cluster_cmd.py`, `cli/review/card_convert.py`, `cli/review/cluster.py`. `ledger.py`, `merge_cmd.py` and `ledger_cmd.py` are not among them. | Grep `findings_v2\|cli\.review\.cluster\|from \.cluster\|\.manifest import\|cluster_v2` over `src` and `scripts` `*.py`, files-with-matches | [CODE-VERIFIED] |
| E-2 | The reflect Python package imports nothing from `cli/review`. | Grep `^(import\|from) .*(cli\.review\|\.review\b)` over `src/superclaude/cli/reflect`: no matches. research/01:40 reports the same result for all of `src` outside `cli/review` (one hit, `main.py:568`) | [CODE-VERIFIED] for `cli/reflect`; [UNVERIFIED] for the whole-`src` claim |
| E-3 | Corrected. A citation-only finding does not crash the v1 ledger path. `annotate` does `locate(text, finding["anchor"])` with no `.get` (`findings.py:349`), but `merge_round` calls `fnd.annotate` only for parsed findings (`ledger.py:135-138`), and the v1 parser has already rejected a line without an anchor (`findings.py:104` with `:80-81`; error recorded at `:188-192`). The `KeyError` is reachable only by calling `annotate()` directly. The original E-3 ("crashes the v1 ledger path", from probe P-a in research/01:53) is [CODE-CONTRADICTED] for the shipped path. | Read of `findings.py:79-121,170-196,345-359` and `ledger.py:107-157`; debate Round 1 and Round 2, both advocates (A-001 REJECT) | [CODE-VERIFIED, re-read in this merge] |
| E-4 | The v1 side of the loop is the shipped consumer and is pinned: `review-ledger/1` or `findings-v1` appears 26 times in 10 files: the loop brief in `src/` and `plugins/` (1 each), `findings.py` 6, `findings_v2.py` 3, `ledger.py` 2, and five test files (`test_review_cli.py` 2, `test_review_findings.py` 5, `test_review_findings_v2.py` 1, `test_review_ledger.py` 4, `test_review_rules_text.py` 1). Further static pins of the loop bullets sit in `tests/skills/test_review_severity_mapping.py`, `test_review_brief_placement.py` and `test_spec_panel_review_loop.py`. | Grep `review-ledger/1\|findings-v1` over `src`, `plugins`, `tests`, count mode; the three skill tests: research/12:48-49 | [CODE-VERIFIED] for the 26 / 10; [UNVERIFIED] for the three skill tests |
| E-5 | Both pipelines are two to three days old and each has one commit: `findings.py` and `ledger.py` last changed in `9163bd1c7` (2026-11-11, #498); `findings_v2.py` and `cluster.py` have only `d2d8a2d16` (2026-11-12, #519). There is no history of paying a divergence cost twice, so "B fixes each shared defect twice" is a projection, not a measurement. | `git log --format='%h %ad %s' -- <file>` for the four files | [CODE-VERIFIED]; also re-run by advocate A in Round 1 |

### 3.2 Which defects are shared and which are engine-local (this is what bounds B's duplication)

<!-- Source: Base (original, modified) - row E-11 last cell adjusted per Change 8 (repair placement and the INV-004 caveat); other rows and the result paragraph Base (original) -->
| # | Defect | Where it lives | Fixed once under B? | Tag |
|---|---|---|---|---|
| E-6 | `T01.02` is not a reference token | one function, `findings.refs_norm` (`findings.py:321-337`), called by both `findings.annotate` (`findings.py:357`) and `cluster.annotate` (`cluster.py:141`); the pattern `_REF_TOKEN` at `findings.py:29` | yes | [CODE-VERIFIED] for the functions and call sites; pattern text [UNVERIFIED], research/02:72 |
| E-7 | Whole-line drop at anchor over 200, claim over 300, quote over 200 | literals in both parsers (`findings_v2.py:111,126,132,136`; v1 `findings.py:104,108,118` [UNVERIFIED]) | yes, through a constants module and one pre-parse repair step (the requirement "one policy before `parse_block`" is decided in synth-06 CO-6; the policy itself is C-06) | [CODE-VERIFIED] for v2 lines |
| E-8 | Union-find with a 3-line tolerance and no chain guard | v1 `same_defect` and `cluster` (`findings.py:367-407`, the 3 is an inline literal at `findings.py:377`) | no, engine-local; v2 has `SPAN_TOLERANCE` and a chained flag (`cluster.py:161-181` read; flag at `cluster.py:324,370` [UNVERIFIED]) | [CODE-VERIFIED] for v1 and for `same_defect_v2`; chain flag [UNVERIFIED] |
| E-9 | Fingerprints differ: v1 `sha256("v1\|section\|refs")[:16]` (`findings.py:340-343`); v2 `sha256("v2\|role\|path\|\|refs\|class")` full hex (`cluster.py:119-123`) | engine-local, each consistent with its own location type | no, and no need: a v1 fingerprint depends on a document section and a v2 one has no document text | [CODE-VERIFIED] |
| E-10 | Fail-open ledger: clearing by silence (`ledger.py:254-258`), one valid block of N passes (`ledger.py:150-157`) | v1 ledger only | n/a here: these are C-02 and C-03 and are fixed inside the one multi-reviewer ledger in the product whichever core shape wins; position A would rewrite the same lines | [CODE-VERIFIED] |
| E-11 | One bad line costs one finding in v1 (`ledger.py:135-138` keeps every parsed finding and records `block_ok` only) but one reviewer in v2 clustering (`cluster.py:256-257`) | engine behaviour | the repair step called inside both `parse_block` functions (2.1) is meant to remove the difference for both; INV-004 (section 9) qualifies this: in v2 any recorded error still invalidates the whole block, so the effect depends on whether the repair records an error | [CODE-VERIFIED] for v1; v2 line [UNVERIFIED], research/02:118 |

Result of the table: of six verified cross-engine defects, two (E-6, E-7) and the cost difference of E-11 sit in shared helpers or in a function that runs before both parsers, so they are fixed once under B. E-8 and E-9 are consequences of the two location types, not duplicated bugs. E-10 is fixed once because only one ledger exists. B's real duplication is the second clusterer and the second location type with its own fingerprint, which is the price of keeping two location types.

### 3.3 No measurement says which location type reviewers produce reliably

<!-- Source: Base (original) -->
| # | Fact | Source | Tag |
|---|---|---|---|
| E-12 | Anchor fidelity: luna quotes verbatim in 91.4 percent of anchors (363 of 397), the other models 98 to 100 percent; ember 860 of 878 (97.9 percent). | research/scope/04:155 (audit-B stats), COMBO-REPORT:294 | [UNVERIFIED] |
| E-13 | Citation precheck in E1: 1,047 citations checked, 510 flagged (48.7 percent); 472 of the flags are `not-in-snapshot` (92.5 percent), 7 `out-of-range`, 31 `quote-not-found`. The cause traced in one run is the orchestrator-built snapshot or `--root` argument, not reviewer error; 0 resolved citations in 7 of 15 combo runs. | research/10:194; research/07:49 (E1-F9) | [UNVERIFIED] |
| E-14 | No run compares core shapes; all three of synth-05 options A, B, C need the same verdict fixes and the same locator work; they differ only in where the engine boundary sits. | synth-05:101 | [UNVERIFIED] |

These facts cut both ways and B does not claim them as a win. E-12 says anchors are good but not perfect for one model; E-13 says citations looked bad but for a plumbing reason, so citation reliability is untested, not disproved. What B takes from them: because neither type is shown reliable enough to make the other redundant, B keeps both and lets the target kind choose.

### 3.4 Consumers outside the loop do not need a ledger today

<!-- Source: Base (original) -->
| # | Fact | Source | Tag |
|---|---|---|---|
| E-15 | PR review needs one integer `line` per finding; `pr_submit` drops a finding without one (`is_groundable`, `fsm.py:364-372`); `citations[0].line_start` maps to `line`. The PR path has a pure core around ONE normalised `Finding` and no panel ledger. | research/13:61, 176 (P1) | [UNVERIFIED] |
| E-16 | The `/task` phase gate is already the master-loop shape (read-only lens reviewers, one fix agent, verification round, cap 3 reviews); replacing rf-qa starts by making this gate call a panel core, and the blockers are a mechanically read-only reviewer, a checklist output mode, per-slot lens and an agent-count rule (R1 to R3), none of which is a ledger-shape question. | research/13:145-149, 195-197 | [UNVERIFIED] |
| E-17 | Reflect has no finding ledger or rounds; its per-run state machine is the manifest. | research/01:150 | [UNVERIFIED] |

### 3.5 Facts the debate added

<!-- Source: Debate transcript, Round 2 new evidence N1, N2, N4, N5, N6 (advocate A) and the advocate B verifications (a), (b) - merged per Change 9 -->
| # | Fact | Evidence | Tag |
|---|---|---|---|
| E-18 | `cluster_v2` cannot join anchor-only findings (N1). `cluster.annotate` builds its citations from `finding.get("citations")` only (`cluster.py:128-132`); `primary` is None when there are no citations (`:134`); `fp` is None unless the primary citation is resolved (`:143-147`); `same_defect_v2` has no anchor or span branch (`:161-181`). `test_finding_without_citations_has_no_primary_and_stays_alone` (`test_review_cluster.py:279-293`) asserts two clusters for two identical anchor-only findings. | Read of `cluster.py:126-182` and `test_review_cluster.py:279-293` | [CODE-VERIFIED, re-read in this merge] |
| E-19 | Clearing ignores block validity, and a test pins it as intended (N2). The clearing loop clears a `resolved_check` row that no current cluster matched (`ledger.py:254-258`) and never reads `block_ok`; `test_one_valid_block_is_enough_and_the_invalid_reviewer_is_reported` (`test_review_ledger.py:376-385`) asserts L1 becomes `resolved` while reviewer `t2-1` has a broken block. The docstring "skipped for clearing" (`ledger.py:112`) is not implemented per reviewer. Bound (advocate B): only rows already in `resolved_check` clear this way (`ledger.py:330-336`). Owner: C-02 and C-03. | Read of `ledger.py:107-258,320-339` and `test_review_ledger.py:376-385`; the `block_ok` read sites (`ledger.py:129,147,150,295,423`, `telemetry.py:67`) were found by Grep in the debate | [CODE-VERIFIED, re-read in this merge] for the clearing loop and the test; [DEBATE-VERIFIED] for the complete list of `block_ok` read sites |
| E-20 | `anchor_status` and `anchor_ambiguous` are written only at `findings.py:350-351` and read only by `tests/review/test_review_findings.py:219,223,230` (N4); the ledger row does not store them (`ledger.py:184-202`), and `render_merged_report` prints only claim and anchor for each blocking finding (`ledger.py:447-466`). | Repo Grep excluding `.dev/tasks/` by both advocates; Read of `findings.py:345-359` and `ledger.py:184-202,408-466` | [CODE-VERIFIED, re-read in this merge] for the write site, the row shape and the render; [DEBATE-VERIFIED] for "read only by tests" |
| E-21 | Neither parser has a key whitelist (N5). v1 `_check_finding` (`findings.py:90-121`) checks only id, severity, blocking, category, anchor, anchor2, refs and claim; v2 rejects only `calibrated_confidence` (`findings_v2.py:96-97`). | Read of `findings.py:90-121` and `findings_v2.py:84-140`; `findings_v2.py:141-187` read by advocate A only | [CODE-VERIFIED, re-read in this merge] for v1 and for `findings_v2.py:84-140`; rest of v2 `check_finding` [CODE-VERIFIED] by advocate A |
| E-22 | The limit literals are duplicated (N6): v1 at `findings.py:104` (anchor 12..200), `:108` (anchor2), `:114` (refs at most 8), `:118` (claim at most 300); v2 at `findings_v2.py:111,117,126,132,136` plus the citation quote at `:80`. This makes the shared constants module a real, bounded deduplication. | Read of `findings.py:79-121` and `findings_v2.py:76-140` | [CODE-VERIFIED, re-read in this merge] |

## 4. Invariants

### 4.1 Preserved

<!-- Source: Base (original, modified) - INV-D row rewritten per Change 1 (no guard); other rows Base (original) -->
| Invariant | How B preserves it |
|---|---|
| INV-A (MEDIUM): contract 1.8.0 consumer-read names and the `merge_method` pair, byte-identical | B changes no `cli/reflect` file and no reflect field name. The only edit to the v2 kernel is importing shared constants, the repair step and the `refs_norm` list; none of them is a contract 1.8.0 field. The existing contract tests stay unchanged. |
| INV-B (HIGH in other slots): `derive_verdict` map and the 36-test matrix | `contract.py` and `test_verdict_mapping.py` are not in B's file set. |
| INV-C (HIGH): findings-v1 grammar, `review merge` unchanged, unknown keys accepted | The v1 parser, the merge command and the open unknown-key behaviour are untouched; E2 in-line `origin` keeps working (v1 and v2 accept it: research/02:48-55 [UNVERIFIED], not re-run by me; v2 `check_finding` shows only `calibrated_confidence` rejected in lines 96-97 [CODE-VERIFIED]; lines 174-187 of that function not read). |
| INV-D (HIGH): `review-ledger/1`, the `ledger` command group, exit codes 0/10/11, `merge` exit 0 | Untouched. C-01 adds no guard (2.3): a citation-only line fed to the v1 merge is already rejected by the parser, and when no reviewer has a valid block `merge_round` raises the existing `LedgerError` (`ledger.py:150-157` [CODE-VERIFIED, re-read in this merge]), which the `merge` command turns into exit 1 (`merge_cmd.py:111-112` [DEBATE-VERIFIED]). |
| INV-E (MEDIUM): `pr_submit.Finding`, `Severity`, FSM, no `gh` or `git` in the core | The adapter is pure and lives on the consumer side; nothing in the contract names `gh`, `git` or a repository. |
| INV-F: installed-path rule | The contract is Python package code reached through the `superclaude` CLI; B adds no primitive text that names `src/superclaude/...`. |
| INV-J: S1 to S5 (binary blocking, Medium non-blocking, 2 fix cycles) | B carries no cap or severity rule in the contract. |
| INV-L: shadow mode changes no verdict | Not touched. |
| INV-N: plugin mirror parity | The v1 brief, `spec-panel.md` loop bullets and their mirrors are unchanged. |

### 4.2 Endangered or left open

<!-- Source: Base (original) -->
1. INV-K (MEDIUM): reserved contract-constant names under `cli/`; a duplicate fails `make lint-architecture` Check 11 (synth-05:74, citing research/18 F6 [UNVERIFIED]). A new shared constants module must choose names that do not collide. Watch item for the plan, checked by running the gate.
2. INV-I (HIGH): B does not improve it. The fail-open v1 ledger (E-10) stays as it is until C-02 and C-03 land inside that engine. Under B that work is smaller (one engine, pins already identified in research/03 section 2), but B is not the reason INV-I is fixed.
3. INV-C (HIGH), the repair step: any pre-parse repair changes what reaches `parse_block`. This is not specific to B (A needs the same step), but B must prove byte-equal parser output on already-valid lines. Covered by test 5.1.
4. Engine-count cost: two clusterers, two fingerprints and two location types remain to be maintained, documented and explained to every new module author. This is a cost, not an invariant.

<!-- Source: Base (original, modified) - pointer added per Change 10 -->
The debate's invariant probe (Round 2.5) added 16 items it found unaddressed, one of them HIGH; they are listed in section 9.

## 5. The test or measurement that would show B right or wrong

<!-- Source: Base (original, modified) - subsections 5.1 to 5.3 replaced by the merged test set per Change 7 (Variant A section 6 T1 to T5; Variant B 5.1 to 5.3; debate Round 2 test table of advocate A and the additions of advocate B); 5.4 edited per Change 6; 5.5 added per Change 11 -->
The tests below are the merged set both advocates agreed in Round 2 (score matrix S-005, HYBRID). Original labels are kept in brackets: T1 to T5 from Variant A, 5.1 to 5.3 from the original Variant B.

### 5.1 Pin parity and differential replay (T1; T2 merged with the original 5.1)

<!-- Source: Variant A, section 6 T1 and T2; Base 5.1 (conformance golden set) - merged per Change 7; projection-totality check dropped per Change 2 -->
T1, pin parity (mechanical). Run all modules of `tests/review/` (19 by Variant A's count) and the loop pins in `tests/skills/` (`test_review_brief_placement.py`, `test_spec_panel_review_loop.py`, `test_review_severity_mapping.py`, `test_review_severity_rule.py`) after the constants module and the repair step land, with no test edited except tests that pin a defect owned by C-02 or C-03. Named pins: `test_v1_line_passes_v2_unchanged` (`test_review_findings_v2.py:70-81`), `test_prior_lines` (`test_review_findings.py:132-143`), the fingerprint pins (`test_review_cluster.py:233-241`, `test_review_findings.py:215-224`) [CODE-VERIFIED by Variant A], and, added in the debate, `test_finding_without_citations_has_no_primary_and_stays_alone` (`test_review_cluster.py:279-293`) and `test_rendered_merged_report` (`test_review_ledger.py:442-473`) [CODE-VERIFIED, re-read in this merge]. B is wrong if any other pin must change. Caveats (section 9): INV-003 (HIGH): `test_review_findings.py:113` and `:117` assert `parse_block(...)["ok"] is False` for an anchor of 201 and a claim of 301 characters [CODE-VERIFIED, re-read in this merge], so T1 and a repair policy that rescues those lines cannot both hold; INV-018: `test_review_cluster.py:784-795` pins which names `cluster.py` imports from modules whose name contains "findings", so where the shared module lives matters.

T2 merged with the original 5.1, differential replay and conformance set. A golden set of about 20 finding lines (anchor-only, citation-only, both, a `T01.02` ref, an over-limit anchor, an over-limit claim, an `origin` key, a `calibrated_confidence` key, a 17-character id) plus committed v1 ledger fixtures, run with and without the repair step through the shared constants, `refs_norm` and both parsers. B holds if: the constants are one object imported by both parsers; `refs_norm` output is identical for both engines; on lines that are already valid, parser output with the repair step is byte-equal to output without it; and the ledger file is equal. The original projection-totality condition is dropped with the projection view (2.4 item 5). Caveats (section 9): INV-021 (no committed v1 ledger fixture exists; tests build ledgers in memory, so fixtures must be produced with pre-change code or "ledger equality" is vacuous) and INV-016 (`refs_norm` runs in `annotate`, not in either `parse_block`, so the `T<PP>.<TT>` change passes a parser-output gate while changing fingerprints, clustering and stored row refs).

### 5.2 Rejection pin and stuck-row probe (T4 merged with the original 5.2; T5)

<!-- Source: Variant A, section 6 T4 and T5; Base 5.2 - rewritten as one per Change 1 and Change 7; assertions added by advocate B in Round 2 -->
T4 merged with the original 5.2, rejection pin. Pin today's rejection of a citation-only line in a `findings-v1` block:
- One reviewer: `merge_round` raises `LedgerError` "no reviewer produced a valid findings block" and the ledger is unchanged (the same shape as `test_round_with_no_valid_block_is_refused_and_changes_nothing`, `test_review_ledger.py:345-361` [CODE-VERIFIED, re-read in this merge]).
- Several reviewers: a warning, `block_ok` false for that reviewer, the line lost, the other reviewers merged, and the same reviewer's other valid lines still merged (`ledger.py:130-138`).

T5, stuck-row probe. A finding whose anchor is missing gives a row with `span None` (fixture as in `test_missing_anchor_is_kept_without_a_span`, `test_review_ledger.py:408-417`). Assert that its anchor status is printed in its `### Lx` block of the merged report (2.3); that a fix map entry naming it records `named_not_touched` (`ledger.py:331-339`); and that at the cap the row gives `ESCALATE`, not PASS (`ledger.py:93-96`), which pins the fail-closed property a C-02 change must keep. The clearing assertion is left to C-02. Caveats (section 9): INV-015 (the fixture has refs `["FR-3"]`, so the empty-refs case is untested) and INV-001 (the status source for a row not re-reported in the current round).

### 5.3 Location-type reliability measurement (T3 merged with the original 5.3)

<!-- Source: Base 5.3 (pre-registered rule) and Variant A, section 6 T3 (per-finding record) - merged per Change 7 -->
Same reviewers, same three targets (a spec document, a tasklist with source paths, a code diff). Run only after the E1-F9 snapshot plumbing is fixed and after it is stated how line numbers reach reviewers in the ledger path (A-002, section 5.5). Per arm record: anchor locate rate (`anchor_status == "found"`), anchor ambiguity rate (`anchor_ambiguous`), citation resolved rate (`status == "resolved"`), and blocking findings lost to the parser; per finding: anchor found exactly once, citation path in the snapshot the core built, line range inside the file, quote found inside the range. Pre-register the rule before the first run:
- B is supported if anchors locate at least as often as citations resolve on the document target and citations resolve at least as often as anchors locate on the code target. Per-target locators are then the evidence-supported shape.
- A is supported if citations resolve at least as often as anchors locate on the document target as well, because then one location type serves every target and the v1 anchor engine has no remaining advantage.

### 5.4 Convergence trigger (the condition under which B hands over to A's work)

<!-- Source: Base (original, modified) - item 2 replaced by advocate A's T-c and the precondition added per Change 6 (debate Round 2, both advocates) -->
B is wrong, and the locator-agnostic `annotate` plus citation-keyed rows must be built, when the first of these occurs:
1. (T-a) a module needs re-review rounds over citation-located findings from several reviewers (candidates: an rf-qa replacement over code, the tasklist post gate over source paths);
2. (T-c) a verified defect fix needs a non-helper edit to both `findings._check_finding` and `findings_v2.check_finding`, or to both clusterers, beyond the shared constants and the repair step; this is checked mechanically on the fix's diff;
3. (T-b) test 5.3 shows citations resolve at least as often as anchors locate on the document target.

Item 2 replaces the original "two or more verified defects in one quarter", which had no measured basis (conceded by advocate B in Round 2).

Precondition: before any loop moves to the v2 kernel, give `same_defect_v2` an anchor-span branch, or derive a `spec`-role citation from the located anchor span (E-18). `test_review_cluster.py:279-293` then changes as a planned pin.

### 5.5 Open points (carried, not resolved)

<!-- Source: Variant A, section 9 - merged per Change 11, updated to the debate result (Round 2; A-002; the two disputes of 2.3) -->
1. How line numbers reach reviewers in the ledger path (A-002). Neither variant states it and no measurement exists; it must be stated before test 5.3 runs.
2. Whether the line-insensitive v2 fingerprint is intended (`cluster.py:119-123`; GQ-023).
3. Dispute 1, not reconciled: locator policy as data with `on_missing` and `on_ambiguous` (advocate A) versus hard-coded keep-and-surface (advocate B). See 2.3.
4. Dispute 2, not reconciled: whether the next round is asked to "locate it or say it is gone" (advocate A) or only to re-locate the row (advocate B). See 2.3.
5. The clearing rule: how an unlocated row may clear, and clearing that ignores block validity (E-19). Owners: C-02 and C-03.
6. The share of E1 citation flags caused by orchestrator plumbing is read from one run's notes (E-13), not traced in the skill step text.

## 6. Effect on future PR code review and rf-qa replacement

<!-- Source: Base (original) -->
| Use | Effect under B | Evidence | Tag |
|---|---|---|---|
| PR code review | Works through the v2 engine and a pure adapter to `pr_submit.Finding`; no ledger is needed because `pr_submit` owns remap, verify, route, round cap and push. The blockers that remain are vocabulary, not core shape: module-declared category, lens and severity sets (P2, P3, P4, M2), passthrough fields `in_diff`, `confidence`, `original_line`, `reviewer` (M3), and a "completion" rule for a local panel (research/13 P6). | research/13:176-181, 214-216 | [UNVERIFIED] |
| rf-qa replacement | Starts at the `/task` phase gate with reviewers that are mechanically read-only, a checklist mode with the computed confidence gate (R2), per-slot lens plus an agent-count floor (R3), and a replay oracle built first (R10; the gate has about 23 files of static pins and no behavioural oracle). Re-review rounds in the rf-qa Fix Cycle (steps 1 to 5) can use the v1 ledger when the target is a document. | research/13:195-204, 153-163; `spec-panel.md:262` shows the loop's rf-qa coupling is soft | [UNVERIFIED] |
| Spec review | No change in shape; the loop keeps its pinned bullets and the single multi-reviewer ledger. | E-4 | [CODE-VERIFIED] for the pin count |
| What B costs these uses | If a future PR or rf-qa design needs a multi-reviewer ledger over `file:line` findings, B leaves that to be built later (trigger 5.4). Research/13 M1 asks the core to expose a locator-agnostic `annotate` and citation-keyed rows now because it is cheap before consumers pin it; B accepts the retrofit risk in exchange for not rewriting the pinned v1 path before any consumer needs it. | research/13:214 | [UNVERIFIED] |

## 7. Strongest objection and the answer

<!-- Source: Base (original) -->
Objection (the strongest form of position A's case): B fixes the same class of defect in two places for as long as both engines live, every new module must choose an engine, and the first module that needs both file:line locations and a multi-reviewer re-review ledger (rf-qa on code, tasklist with source paths) forces the locator-agnostic ledger anyway, at a later date when more tests pin the v1 path and more consumers read `anchor`. The core never becomes one pipeline, so unknown-key policy, fingerprint, blocking rule and run record stay four decisions with two answers each. research/13 M1 says the exposure is cheap now and expensive to retrofit.

Answer:

<!-- Source: Base (original) -->
1. The duplicated-defect claim is smaller than it looks. Section 3.2 shows the two defects that appear in both parsers are in shared helpers or in a step that runs before both parsers, so they are fixed once. The differences that remain (fingerprint, tolerance, chain guard) follow from the location type and are not bugs to fix twice. E-5 shows no duplicate cost has been paid yet; the cost is a projection.

<!-- Source: Base (original, modified) - reference to the withdrawn 2.3 guard removed per Change 1; the warning-only loss conceded by advocate B in Round 1 stated -->
2. The forcing function is observable and cheap to detect. B names its trigger (5.4), and item 2 of it (T-c) is checked on the diff of a fix. The typed guard first proposed in 2.3 is withdrawn: the v1 parser already rejects a citation-only line (E-3). That rejection is not loud in every case: with several reviewers the line is lost with only a warning (5.2), which the debate routed to C-02 and C-03 (E-19). Position A pays now for a case no consumer has shown: PR review needs no ledger (E-15), reflect has no ledger (E-17), and the `/task` gate's blockers are not about a ledger (E-16).

<!-- Source: Base (original) -->
3. The retrofit argument is weaker than the rewrite argument. Rewriting `annotate` and the ledger rows now means changing the one path that is shipped, pinned in tests (E-4) and described in the brief, in order to carry a location type no run has shown reliable (E-12, E-13). Deferring leaves the v1 path pinned as it is and adds work only when a consumer pays for it; the pins that exist today (six of eight tests that pin ledger behaviour as intended, research/03:151 [UNVERIFIED]) already have to be rewritten once for C-02 and C-03, and B does not add a second rewrite on top.
4. B does not close A. The contract adopts the shared constants, the repair step and the `refs_norm` list, so a later move of the v1 loop to a profile of the v2 kernel starts from a shared base. What B gives up is an earlier, cheaper start on that move.
5. What B does not answer: it does not say how many module authors must learn two location types, and it does not say who decides, per new module, which engine fits. That is an owner decision, together with the open question whether the v2 fingerprint's line-insensitivity is intended (GQ-023).

## 8. Debate result

<!-- Source: debate-transcript.md (Metadata, Scoring Matrix tally, Convergence Assessment) and base-selection.md (Combined Scoring, Selected Base) - added per the merge brief -->
From `debate-transcript.md`, Metadata:
- "Depth: standard"
- "Rounds completed: 2 (Round 1 parallel statements, Round 2 sequential rebuttals) plus Round 2.5 invariant probe; Round 3 not run (depth standard)"
- "Convergence achieved: 100% of diff points agreed (23 of 23) after Round 2; 78.3% (18 of 23) after Round 1; status BLOCKED_BY_INVARIANTS (see Convergence Assessment)"

From the Scoring Matrix: "Tally of the 23 points: Variant A 2 (S-001, S-004); Variant B 10 (S-002, C-001, C-002, C-003, C-004, C-007, X-001, X-002, X-003, A-003); HYBRID 7 (S-005, C-005, C-006, C-008, C-009, C-010, X-004); NEITHER 4 (S-003, X-005, A-001, A-002)."

From the Convergence Assessment: "Invariant probe gate: BLOCKED (1 HIGH UNADDRESSED: INV-003)"; "Status: BLOCKED_BY_INVARIANTS (agreement 100% >= 80% and taxonomy covered, but a HIGH-severity UNADDRESSED invariant exists)"; and "Two disputes remained between the advocates after Round 2 and are carried in the hybrid" (recorded in 2.3 and 5.5).

From `base-selection.md`: final scores Variant A 0.8760, Variant B 0.8515; "Margin: 2.45 percent (below the 5 percent threshold)"; "Tiebreaker applied: Yes, level 1 (debate performance, points won in Step 2)"; Variant B selected as the base (10 of 23 points won, against 2 for Variant A).

## 9. Invariants the debate left unaddressed

<!-- Source: invariant-probe.md (Round 2.5 fault-finder table and orchestrator gate) - all 16 UNADDRESSED rows copied per Change 10 -->
INV-003 (HIGH) blocks convergence under the protocol's invariant-probe gate; the debate ran at depth standard (no Round 3) and did not resolve it.

| ID | Category | Assumption | Severity | Evidence (one line) |
|---|---|---|---|---|
| INV-001 | state_variables | Anchor status can be surfaced for every blocking row from data render_merged_report already has | MEDIUM | The stuck row is the "open from an earlier review, not reported again" branch (`ledger.py:457-466`), which reads only the row, and the row stores neither `anchor_status` nor `anchor_ambiguous` (`ledger.py:184-202`); the consensus does not name the source of the status. |
| INV-002 | state_variables | Adding T<PP>.<TT> to the shared token list leaves ledgers already on disk behaving the same | MEDIUM | Row fp and refs are frozen at creation (`ledger.py:183-186`), so a later re-find whose only token is T01.02 fails `same_defect` (`findings.py:371-379`), opens a new row, and an old `resolved_check` row is recorded "cleared" instead of "regressed". |
| INV-003 | guard_conditions | A repair step inside both parse_block functions can rescue over-limit lines while T1 keeps every existing pin unmodified | HIGH | `test_review_findings.py:113` and `:117` assert `parse_block(...)["ok"] is False` for an anchor of 201 and a claim of 301 characters, so a rescuing repair and "T1: all pins unmodified" cannot both hold. |
| INV-004 | guard_conditions | The same repair gives the same benefit in the v2 parser | MEDIUM | Any error in a findings-v2 block sets it invalid (`findings_v2.py:299-303`) and `cluster_v2` drops that reviewer (`cluster.py:218-222, 256-257`), so the error-recording choice decides the v2 effect. |
| INV-008 | count_divergence | One constant per limit is safe when equal numbers mean different things, and the consensus literal list is complete | LOW | Anchor max 200 equals quote max 200 (`findings_v2.py:80`) and refs max 8 equals citations max 8 (`findings_v2.py:128`); the consensus list omits `findings_v2.py:128`. |
| INV-009 | count_divergence | The 3-line clustering tolerance means the same thing in both engines, so it can be shared or a spec-role citation can be derived from an anchor span at convergence | MEDIUM | v1 spans are 0-based half-open (`findings.py:377`) and v2 citations 1-based inclusive (`cluster.py:72, 177-178`), so sharing the number or deriving a citation from a span shifts v1 clustering by one line unless the conversion is stated. |
| INV-010 | count_divergence | The two parsers hold the only copies of the limits and the one repair function is the only repair | MEDIUM | `card_convert.py:85-86` re-declares limits, truncates claims (`card_convert.py:199-201`) and calls `findings_v2.check_finding` directly (`card_convert.py:226`), a third copy and a second repair that no detector catches. |
| INV-014 | collection_boundaries | A round whose only reviewer has only a repaired line merges like any other round | MEDIUM | A repair that keeps an error makes the single reviewer's `block_ok` False, so `merge_round` refuses (`ledger.py:150-157`) although a finding was rescued; one that records none breaks T1 (INV-003). |
| INV-015 | collection_boundaries | A stuck row is one row, so surfacing its status once is enough | MEDIUM | A missing anchor gives section "none" (`findings.py:358-359`); with empty refs `same_defect` cannot match, so each re-find with the same bad anchor opens a new span-less row; T5's fixture has refs `["FR-3"]` (`test_review_ledger.py:408-417`). |
| INV-016 | interaction_effects | The merged T2 gate (byte-equal parser output plus ledger equality) catches every shared-contract change | MEDIUM | `refs_norm` runs in `findings.annotate` (`findings.py:357`) and `cluster.annotate` (`cluster.py:141`), not in either `parse_block`, so the token change passes a parser-output gate while changing both fingerprints and stored row refs. |
| INV-017 | interaction_effects | Adding the token "once" in refs_norm updates every reference-token reader | MEDIUM | `telemetry.py:23-27` keeps its own token pattern for counts (`telemetry.py:161-172`), so telemetry would disagree with `refs_norm` on tasklist ids. |
| INV-018 | interaction_effects | The shared helpers can move into a new shared module without touching pinned tests | MEDIUM | `test_review_cluster.py:784-795` asserts `cluster.py` imports exactly `{"refs_norm", "_check_citation"}` from modules whose name contains "findings"; moving `refs_norm` or adding such an import breaks T1. |
| INV-020 | interaction_effects | "No change to cli/reflect" means the reflect pipeline's results do not change | MEDIUM | The reflect shadow steps run `superclaude review cluster` (`cluster_cmd.py:151`) and `verify-citations` (`verify_cmd.py:133`) through `findings_v2.parse_block`, so the repair and token change alter `clusters.json` and `precheck.json`; no v2-side differential test exists. |
| INV-021 | interaction_effects | The merged T2 has committed v1 ledger fixtures to replay | MEDIUM | Grep "review-ledger/1" over `tests/` finds only `test_review_ledger.py:136`; tests build ledgers in memory from `seeded.md` and `clean.md`, so fixtures must be produced with pre-change code. |
| INV-022 | interaction_effects | Whatever repair policy C-06 picks leaves locating and clustering of the rescued line well defined | MEDIUM | A truncated claim can drop ref tokens (`findings.py:323-327`) and a truncated anchor prefix can match several places (`findings.py:349-352`), so `hunks_touch` tests the wrong lines; T2 covers only already-valid lines. |
| INV-024 | sufficiency_challenge | The consensus alone resolves FX-1 and leaves C-06 free to choose the repair policy | MEDIUM | Of three paths that validate a finding line (v1 `parse_block`, v2 `parse_block`, `card_convert.py:226`), the repair inside `parse_block` reaches two, and on those a rescuing policy either breaks T1 pins or is nullified by the validity gate. |

Probe summary (from `invariant-probe.md`): 25 findings, 9 ADDRESSED, 16 UNADDRESSED (HIGH 1: INV-003; MEDIUM 14; LOW 1: INV-008). Gate result: "CONVERGENCE BLOCKED: 1 HIGH-severity UNADDRESSED invariant(s) detected. Blocking items: INV-003."
