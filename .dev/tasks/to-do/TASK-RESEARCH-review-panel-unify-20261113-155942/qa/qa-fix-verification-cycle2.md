# QA Report: Report-Validation Fix Verification (structural), cycle 2

**Topic:** Unified Review Panel investigation
**Date:** 2026-11-14
**Phase:** report-validation (verification)
**Fix cycle:** 2
**Fix authorization:** false (report only; no file edited except this report)
**Inputs:** `qa/qa-consolidated-findings-phase6.md` (`## Cycle 2`: P6-B35-r, P6-B20-r, P6-B5-r), `qa/qa-fix-log.md` (`## Cycle 2`), `RESEARCH-REPORT-review-panel-unification.md` (4283 lines), cycle-1 reports `qa/qa-fix-verification.md` and `qa/qa-fix-verification-qualitative.md`

---

## Overall Verdict: PASS

All three cycle-2 blocking findings are fixed in every place the cycle-1 verifiers named. No new blocking defect was found and none of the 36 findings that cycle 1 verified as fixed has regressed (10 spot-checked against their cycle-1 evidence, the rest by structural script). |F_3| = 0 against |F_2| = 3.

## Cycle-transition checks

| Check | Result | Evidence |
|---|---|---|
| Regression (runs first) | none | The ten spot-checked findings below and the structure scripts show every cycle-1 "Yes" row still holds; the cycle-1 G-skills defect (N-1) is the only item that was not PASS at cycle 1, and it is P6-B35-r. |
| Monotonicity | no halt | |F_2| = 3 (P6-B35-r, P6-B20-r, P6-B5-r), |F_3| = 0 < 3. |
| Hard cap | within cap | Fix cycle 2 of 2; this review is the third review and ends with no open blocking finding. |

## (a) The three cycle-2 findings

| Finding ID | Fixed? | Evidence |
|---|---|---|
| P6-B35-r | Yes | Re-ran `grep -rlE 'sc-workflow-protocol\|sc-tasklist-protocol\|sc-brainstorm-protocol' tests/`: 16 files besides `.pyc` caches. The G-skills row (L3858) says 16 and lists them: 13 in the command (the path set in the row equals the 13 I compared, `SAME_SET`) and 3 covered elsewhere. The three are exactly the diff of the grep result against the 13: `tests/review/test_reflect_consumer_inventory.py` (in G7's command, L3852), `tests/cli/reflect/test_remediation_source_template.py` (5 tests; G9 runs `tests/cli/reflect` with four `--ignore` flags, and none of the four ignored files is this one: `test_panel_contract_lint.py`, `test_shadow_skill_contract.py`, `test_shadow_exit_script.py`, `test_verdict_replay_script.py` all exist) and the fixture `tests/skills/fixtures/review_severity_sweep_edits.yaml` (read at `tests/skills/test_review_severity_rule.py:269-278`, a G10 suite). All five files the cycle-1 verifier named as omitted are now in the command (`test_workflow_vs_task_builder_companion.py`, `test_primitive_dual_surface_lookup.py`, `test_tier2_tavily_consistency.py`, `test_cli_install.py`, `test_brainstorm_gaps.py`). `uv run pytest --collect-only -qq -p no:cacheprovider` on the 13 files: `1327 tests collected`; per-file counts 125, 16, 19, 4, 88, 3, 68, 73, 5, 758, 2, 70, 96 equal the row's sum and total 1327 (the report no longer says 1087). The false "file list from `grep -rl`" sentence is replaced by the search actually run. Cites spot-read: `test_workflow_vs_task_builder_companion.py:375-376` (`.claude` copy equals `src` copy), `test_brainstorm_gaps.py:89-91` (makes the directory in a temporary home), `test_cli_install.py:502-506` (`_assert_present`). The row keeps its [UNVERIFIED] note on whether any suite pins the Wave 4 or Stage 10.5 text. |
| P6-B20-r | Yes | M1-04 (L3646) now carries "a `coverage` field in the lens entry (and as a per-slot value in a template), with the values `redundant`, `partitioned` and `per-lens` [proposed, exposure X14 of 7.2 ...]", acceptance "one case per coverage mode (SC-14 (iv))", and X14 in Closes gaps. M1-07 (L3649) states that `quorum = min(2, panel_size)`, `degraded`, `below_quorum` apply to `redundant`, gives the [proposed] per-mode rules (`partitioned`: per slice, one valid block each, a slice without one is `below_quorum`, `support` not computed; `per-lens`: per lens; blocking from the lens predicate, never agreement), leaves the thresholds to Q-60, adds a test per mode (SC-14 (iv)) and lists X14. The M4 Dependencies line (L3706) names M1-04 (`coverage` field, X14) and the M1-07 per-mode rule; M4-07 (L3717) points to the M1-04 field. SC-14 (iv) (L538) is tied to M1-04 and M1-07. The X14 row (L2812) and Q-60 (L4194) agree with M1-04 and M1-07 on the rules (same wording of the per-mode quorum, `degraded`, `support`). `below_quorum` is an existing term (L2776). Gap-coverage rows D3 (L3726) and BL-05 (L3754) note the X14 steps. No number beyond those already in X14 and Q-60 was added. |
| P6-B5-r | Yes | M3-01 (L3693) Details now say the five subcommands `review telemetry`, `ledger defer`, `ledger verdict`, `ledger capture`, `panel validate` are [UNVERIFIED] until Q-58 is answered, only `merge`, `ledger revise` and `panel resolve` are established, and the scope of the wiring and the D14 rating wait on Q-58. SC-12 (L536) carries the same premise mark. Section 9.2 has a new row (L4067) listing Q-58 and Q-61. Q-58 (L4192) is defined once and indexed in 9.1 (L4055). Q-58's sentence "the five subcommands are marked [UNVERIFIED] in the M3 steps" is now true. Q-61's mark exists in C-18 (L2382, "not established [UNVERIFIED]"). |

## (b) Regression spot-check of cycle-1 fixes (grep and script against the current report)

| Finding ID | Still fixed? | Evidence |
|---|---|---|
| P6-B1 | Yes | V-037 row holds "30 findings lost at merge (all dropped findings, not only blocking ones; E2's blocking-lost total is 49)" and points to V-167; `Both versions presented` occurs 0 times. |
| P6-B2 | Yes | L3937 "Under the gap-log rating no gap is Critical ..."; the unqualified "No gap is Critical" occurs 0 times. |
| P6-B3 | Yes | "11 distinct gaps" 4 times; four "Rating basis" Notes cells; Section 4 gap table recounted by script: 145 rows, Critical 15, Important 66, Minor 64 (D 16, BL 23, MS 24, ENS 9, OPEN 2, DOC 71). |
| P6-B6 | Yes | "Of the 41 review call sites among the 43" present once; "32 of 43" and "32 of the 43" occur 0 times. |
| P6-B12 | Yes | SC-18 to SC-23 rows each present once; G-new row names SC-18. |
| P6-B18 | Yes | MS-24 gap row (L650) and its coverage row (L3778), Q-59 (L4193), C-11 route and derivation text (L1921) and rating line (L1923), M2-02 (L3675) present. |
| P6-B19 | Yes | M1-20, M1-21, M1-22 rows present; M4 Dependencies (L3706) names M1-16, M1-20, M1-21 and the C-13 gate. |
| P6-B34 | Yes | `plugins/superclaude/rules/prompts/document_review_loop_prompts.md` and `plugins/superclaude/commands/spec-panel.md` are named in M1-11, M3-01, M3-08 and G10 (one hit each; `plugins/superclaude/skills/sc-workflow-protocol` exists). |
| P6-B36 | Yes | G2 split `:277-298` / `:299-304` present; G1 to G11 rows intact in 8.3 (ids G1-G11, G-pr, G-skills, G-all, G-exit, G-replay, G-sync, G-bench, G-new). |
| P6-B37 | Yes | Persisted-format rule at the head of M1, "13 recorded shadow manifests" 4 times, three `**Rollback (M` lines (M2, M3, M4). |

## (c) Required contents (a) to (e) (BUILD-REQUEST.md L75)

| Content | Present | Evidence |
|---|---|---|
| (a) overlap matrix | Yes | `### 2.6 Current State Summary: component overlap matrix (a)` (L435). |
| (b) value inventory with destination or drop reason per row | Yes | `### 8.1 Value inventory (b)` (L2921); 691 `V-` rows, all 7 columns including Destination and Reason, 691 unique ids. |
| (c) conflict log with options and recommended resolution | Yes | 6.0 conflict index (L1165), C-01 (L1190) to C-19 (L2386), 20 "Recommended resolution" lines. |
| (d) target architecture, shared core and thin modules | Yes | `### 7.1 Target architecture (d)` (L2696). |
| (e) future-use exposure list and blockers | Yes | `### 7.2 Future-use-case exposure list (e)` (L2794, now X1-X14) and 7.3 blockers (L2824). |

## Scripted structural re-checks

| Check | Result | Evidence |
|---|---|---|
| Every Section 8.1 row has 7 columns | PASS | Script: 691 `\| V-` rows, column count {7: 691}, 691 unique ids. |
| All tables keep a constant column count | PASS | Script: 173 table blocks, none with a non-constant unescaped-pipe count (backtick content excluded). |
| Section 4 gap table is one contiguous table | PASS | L586-L732 = 147 lines (header, separator, 145 rows); the other three Section 4 tables (L736, L757, L773) are the separate 4.1 to 4.3 summaries. |
| Table of Contents matches headings | PASS | 72 ToC entries equal the 72 `##` and `###` headings (excluding the ToC) in text and order; 0 anchors without a heading. |
| Ten sections present and ordered | PASS | `##` headings 1 to 10 at L90, 105, 480, 578, 782, 1153, 2624, 2915, 3933, 4197. |
| Section 9.1 lists G-01 to G-94 once and each Q row once | PASS | 94 distinct G ids, no duplicate, none missing, none outside the range; 61 Q rows (Q-01 to Q-61), none missing or duplicated; each of the 61 Q ids has one definition row outside 9.1. |
| Only the allowed `[CONTRADICTION` text | PASS | 13 lines contain the token; the only colon-form `[CONTRADICTION:` is L2777 (Section 7.1.3 Merge and verdict); the other 12 are its echoes (L2911, L2919, V-433, L3633, M1-07, M1-08, M1-16, M3-08, L3891, L3921, L3929, Q-54), all about the core verdict word set. |
| No debate winner changed; four debates `partial` | PASS | `return-contract.yaml` of ledger-model, model-tier-config, panel-size-cost, who-judges-blocking: `status: "partial"`, base variants B, A, variant-2 (B), B; report L2680-2683 give C-03 winner A, C-05 B (Option D), C-13 B, C-14 B; HIGH invariants 10, 2, 3, 11 (`grep -c 'severity: "HIGH"'`) = 26 as stated. |
| E2 at commit 4a22d74213f93837d00c2c314075dd967b9a98e3 only | PASS | Only one 40-hex string occurs (14 times); the short form `4a22d742` occurs 6 times; no other E2 commit named. |
| Report-only: no roadmap, no `/sc:workflow` | PASS | `/sc:workflow` and `sc:workflow` hits are the scope negations (L101, L2917) and the product name (Wave 4 hook rows); every "roadmap" hit is a negation, "the later roadmap", or the `.roadmap-state.json` spec-resolution name at L634. |
| Parsed-sparse figures are counts only | PASS | All hits of "parsed-sparse" and "35 of 39" read "set in 35 of 39 (34 of the 38 Tier 2 runs), decisive in 0 for certain and at most 1" or mark the older "34 by the parsed-sparse pre-filter" wording as superseded (L720, L2059, L2637, L2904, L2910, L3254, L3456, L3495). No causal claim is restored. |
| Placeholder text | PASS | No `TODO`, `TBD`, `PLACEHOLDER` introduced; the report grew by exactly one line (4282 to 4283: the 9.2 row), so cycle-1 line numbers are unchanged below L4067 apart from +1 after it. |

## New blocking defects

None. I looked for a broken table (none), a wrong or stale header and Table of Contents (none), lost required content (none), a new uncited claim (the G-skills file lists and per-file counts reproduce; the X14 rules reuse the text already in 7.2 and Q-60), and a new inconsistency between sections (Section 3 SC-12 and SC-14, 7.2 X14, 8.2 M1-04, M1-07, M3-01, M4 Dependencies, M4-07, 9.2, 9.5 agree).

## New MINOR notes (never fail the gate, never rechecked)

| # | Where | Note |
|---|---|---|
| M1 | 9.2 row L4067 | Says Q-61 is "marked in C-18, M4-06"; C-18 (L2382) carries "[UNVERIFIED]", M4-06 (L3716) conditions the tool set on the Q-61 sample but carries no literal [UNVERIFIED]. |
| M2 | 8.2 M1-04, M1-07 "Closes gaps" | List X14, which is not a gap row; both cells say so ("an exposure added at the report-validation gate, not a gap row"). A strict reader of the column may still stumble. |
| M3 | L2573, L2615 | "X1-X13" remains where the report refers to the exposure count of `research/10`; L2581, 7.2 and M4 say X1-X14. L2573 could say that X14 was added by the report. |
| M4 | 8.3 G-skills | Says whether the suites pin the Wave 4 or Stage 10.5 text was not read [UNVERIFIED]; `tests/commands/test_workflow_command.py:245-261` pins the Wave 4 call string (cycle-1 qualitative minor note N-2). The mark is honest, only unresolved. |
| M5 | `qa/qa-fix-log.md` Cycle 1 row P6-B35 | Still describes G-skills as "nine suites ... 1087 collected"; the Cycle 2 row P6-B35-r supersedes it. Left as history. |

## Confidence and tooling

- **Checks:** 12 (three cycle-2 findings; regression spot-check of ten cycle-1 findings counted as one check; required contents (a) to (e); 8.1 column count; table column counts; Section 4 contiguity; ToC; ten sections; 9.1 ids; `[CONTRADICTION`; debate winners; E2 commit; report-only and parsed-sparse). All 12 examined with tool evidence, all pass.
- **Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% of the examined checks. Limits: I did not re-run the three command reproductions of cycle 1 (`recount_tier_decision.py`, `reflect_shadow_exit.py`, `panel resolve`) because cycle 2 touched none of those sections; the unchanged line numbers (cycle-1 L2106, L3857, L3860 agree) and the 13 `[CONTRADICTION` lines support that. I did not run the 13 G-skills suites (collection only, as the finding requires).
- **Tool engagement:** Read: 12 | Grep: 2 | Glob: 0 | Bash: 9 (two `uv run python` structure scripts, `grep`, `uv run pytest --collect-only`, `sed`, `diff`, `comm`). No Tavily or web calls. Temporary scripts in `/tmp` were deleted. No file was edited except this report.

## Recommendations

1. Close the report-validation gate; no fix cycle 3 is needed.
2. Minor notes M1 to M5 may be fixed when the report is next edited; they are not rechecked.

## QA Complete
