# QA Report: Gate 3 Content Verification (tech-ref-qualitative, fix-cycle 1)

**Status:** Complete
**Document:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md (1,392 lines)
**Date:** 2026-11-20
**Phase:** fix-cycle (tech-ref-qualitative content re-check, report-only, fix_authorization false)
**Fix cycle:** 1

## Per-finding results (content lenses: actionability, domain-accuracy, crossref-chain, code-example-accuracy)

Domain-accuracy lens had 0 blocking findings at review 1 (PASS); the content-lens blocking findings are GD-5 (actionability), GD-6 and GD-7 (crossref-chain), GD-8 and GD-9 (code-example-accuracy). GD-3 and GD-4 (internal-consistency lens) are also checked because the C8 wording and the 12.3 pointer are content. GD-1 and GD-2 (template conformance) are outside this lens; line count was confirmed at 1,392 (`wc -l`), and the 14.2 header was seen with the Severity and Effort to Fix columns.

| ID | Status | Evidence read (document line, then snapshot) |
|---|---|---|
| GD-5 | RESOLVED | Doc 13.1 row D (L1167): step 1 sets the new `CycleResult` field in `Collector.run_once`; step 6 names `keys.py` `_take`/`_take_escape`, the escape decoder finals A and B, and the help-line constants `QUESTIONS_KEYS_LINE`, `QUESTIONS_LINK_KEYS_LINE`, `KEYS_LINE` (view.py:91-118); pitfalls name `test_session.py:339-353` and `:359-393`. Snapshot: `keys.py:176-235` (`_take`, `_take_escape`; only A and B mapped at 227, 233); `view.py:30` `KEY_NAMES`, `view.py:91, 93, 118` constants; `collector.py:248-323` `run_once` builds `CycleResult`; `test_session.py:339-353` pins `r x Z 1` space and backspace as no-ops, `:359-393` pins `e` as the only export key and `q`/Ctrl-C as the only quit keys. All match. The 5.2 convention line (L568) matches. |
| GD-6 | RESOLVED | Doc Section 3 tree (L308) now reads "artifact list in 5.5"; 5.5 holds the 15-step run-folder artifact table (L762-776). 4.2 has no artifact list, so the pointer is correct. |
| GD-7 | RESOLVED | Doc 10.2 new row (L1068), 13.1 scenario F (L1169), 13.2 package row (L1202). Checkout package: `render.py:20-24` (`designs(batch)` merges `DESIGNS` of `layouts.group_a` + `group_b`, or `layouts.agent_focus`), `render.py:127-129` (`--show` does `designs(args.batch)[args.show]`, so a slug of the other batch raises `KeyError`; `--width` is `type=int` with no `choices`), `layouts/agent_focus.py:171-183` (`DESIGNS[slug]` entry keys `name, render, question, omits, tradeoff, data, missing`), `tests/test_designs.py:14-115` (Semantics 10, SafeText 5, Layouts 4 = 19; `test_all_scenarios_widths` asserts 20 designs, widths 160/144/116/80 and `SYNTHETIC`; `test_export_manifest` asserts 10 concepts per batch and needs both `ROOT` and `ROOT/agent-focus`); `tests/test_gallery.cjs` exists (Glob). All match. |
| GD-8 | RESOLVED | Doc L829 now `page.py <run>;  page.py --open;`. Snapshot `skills/agent-work-report/scripts/page.py:381-387`: `sys.argv[1:] == ["--open"]` or `len(sys.argv) == 2`, else `sys.exit(__doc__)`. No `[--open]` form remains in the document (Grep). |
| GD-9 | RESOLVED | Doc skeleton A (L1174-1180): rule contract, `_classification(class_name, rule, evidence, waiting_kind=None, notes=())`, "RULES and CLASSES are tuples, so `+=` raises TypeError", insert before `Rule("fallback", ...)`, add "example" in `CLASSES`, ninth name `C_EXAMPLE` in the unpack, `NEXT_INSPECTION["example"]`. Snapshot: `classify.py:42-51` (eight-name unpack of `CLASSES`), `:130-136` (`_classification` signature), `:156-158` (`Rule` fields), `:345-355` (RULES tuple, `fallback` last), `models.py:50-59` (CLASSES tuple), `report.py:54-69` (`NEXT_INSPECTION`, `_NEXT_DEFAULT`). `C_EXAMPLE` is now defined by the ninth unpack name. Matches. |
| GD-3 | RESOLVED | Full wording "Remediation task not created (read-only brief); flagged for the owner" is in 14.1 D-1 (L1225) and C8-8 (L1228) rows and in 14.5 C8-1 to C8-9 (L1314-1322); 15 lines carry it (Grep count). The 5.2 D-1 bullet (L556) and 5.3 (L636) carry it too. |
| GD-4 | RESOLVED | 12.3 row 2 (L1145) now points to the 5.1 Conventions for the observer and 13.1 B for the sweep; the 5.1 Conventions first bullet (L477) names the template constants, `assert_allowed`, pinned tests and "never remove one". |

**Open blocking findings from review 1: 0 of 9 content-lens items (GD-3 to GD-9 RESOLVED).**

## Re-checks requested (process step 2)

1. **Section 13 extension steps against the real code: still work.** A (sweep class/rule): `CLASSES` tuple and unpack, `RULES` tuple, `report.py:26-27` `CLASSES[5]`/`[7]`, `classify.py:958` (`idle`/`person_active` suffix), `classify.py:976` (`counts[class_name]` KeyError), `NEXT_INSPECTION` keyed by rule name with `_NEXT_DEFAULT`, tests `test_classify.py:277, 351, 375, 379` all read and match. B (probe): `ALLOWED_ORCA` `probes.py:49-60` ("10 templates, 7 verbs (NFR-014)" at :60), `ALLOWED_GIT` :68, `parse_worker_show` :471, tests `test_allowed_orca_is_exactly_the_ten_templates` (:370) and `..._names_seven_verbs` (:375) exist. C (snapshot field): `_TEXT_FIELDS` export.py:25, `_ANY_FIELDS` :46, `_row_dict` :141, `snapshot_dict` :183. D: see GD-5. E (AWR source): `REQUIRED_CHECKS` run.py:204, `sys.exit(__doc__)` run.py:887 and check.py:349, `check.main` :168. F: see GD-7.
2. **C8 candidates.** C8-8 and C8-9 (DEFECT-CANDIDATE) and C8-1 to C8-7 (KNOWN LIMIT) each keep the declaring line, the code evidence and the cited decision or statement ("none found" for the two DEFECT-CANDIDATE rows), and every row ends with the exact words. The 14.1 and 5.2 repeats keep them.
3. **Designed-only described as built: none found.** The orchestrator writer `superclaude orchestrator report-entry`, `/sc:orchestrator`, PR A/B/P and the Orca automations stay tagged DESIGNED or UNVERIFIED in 1, 2.1, 4.1 (e), 5.5 (built-versus-designed table), 8.2 and the glossary; the package is "designed only as a product" (2.5). The two Grep passes over present-tense claims found only the 8.2 and 14.4 rows that say "Reader built" or "unmerged".
4. **No unification recommendation.** Grep for should/recommend-to-unify/merge/consolidate/best-option phrases over the whole document: 0 matches; the "Unification touch points" paragraph (L1186) lists facts and ends "(facts only; no recommendation)".

## Extra check requested by the executor (14.4 C pointer and two dropped glossary rows)

- **UNVERIFIED item classes: all still stated.** 14.4 B is untouched: 9 subject rows covering U-01 to U-40 (every id from 1 to 40 appears; the 40 UNVERIFIED count in 15.1 agrees) plus the no-id row (three Orca wrappers; issue #590). Compared line by line with the pre-fix synthesis (`synthesis/synth-07-conventions-extension-debt.md:210-222`): identical. 14.4 A (contradictions and stale documents), 14.5 (C8) and 14.3 (deferred items) also remain. The removed 14.4 C table was headed "facts; not tagged UNVERIFIED above" (synth-07:224), so it held GAP rows, not UNVERIFIED items.
- **Facts from the removed 14.4 C table are mostly stated where they apply:** G-01/M-1 (2.5, 4.1 a, 5.2 "C8 reachability"), G-02 to G-05 (5.1, 14.1, 14.2), G-06/G-07/G-08 (5.2 gates), G-09 (8.2), G-10 (5.2, 5.6), G-12, G-35 to G-37 (14.5, 14.1), G-15 to G-19 (5.3, 5.4, 8.1, 14.1), G-21 to G-24 (14.2, 5.5, 8.3), G-26 to G-30 (5.2, 5.6, 14.3), G-41 to G-47 (count corrections applied).
- **What was lost (minor, not decision-relevant):** (a) research coverage limits G-11, G-14, G-25, G-28, G-31, G-32, G-34 (which parts of the orchestrator design, sweep internals, observer render internals, adapter tail and AWR `refresh` body the research did not read in full); (b) G-20 (`SKILL.md:194` "never ... starts or messages agents" is broader than `waker.py`, which starts the coordinator session and types into its terminal) and G-39 (CHANGELOG:170 grammar). Why not blocking: the behaviour behind G-20 is stated in 5.5 (writes (3) and 12.1 "Not read-only"); every absence claim about the orchestrator design (never names `/sc:sweep`, WC-16, the observer, `.dev/sweeps`) was made by grep over the whole file (GF-3 section 2), not by partial reading; 8.1 states "about 30 verb forms", not a complete count; no UNVERIFIED class and no C8 label depends on the unread parts. The 14.4 C pointer sentence "their facts are stated where they apply" is therefore not literally true for group (a); see note N3.
- **Glossary:** the dropped rows "Coordinator", "Run, Dispatch" and "Phase 1" are used without definition in Sections 1, 5.1, 5.3, 5.4 and 14. The reader is the owner, who uses these terms; no decision-relevant fact was lost. Note N4.

## New defects introduced by the fixes (process step 3)

None blocking. I read the changed passages and the paragraphs that replaced tables (5.4 exit codes and disk reads, 5.3 phase 1 limits, 12.2) and checked the references that the cuts could have orphaned (Grep for "14.4 C", "assembly map", "in 4.2", "13.1 A to F", status-vocabulary table pointers): every remaining pointer resolves (4.2 has the sweep disk row; 14.4 heading has no C subsection requirement beyond the pointer line; 13.1 A, B and C exist). Spot-checks of facts in condensed paragraphs against `probes.py:87-88` (512 KiB ledger split, 256 KiB transcript tail), `probes.py:1077` (project key by non-alphanumeric replacement) and `sweep/commands.py:279-288` (exit 2 on usage or binding error, exit 1 on publish error or other exception) match.

## Minor notes (not rechecked, do not fail the review)

- N1. 13.1 D and 5.2 (L568) say `_take` and `_take_escape` are "the only places a `Key` is built". `keys.py:165` also builds `Key("escape")` in the lone-Escape timeout path of the read method. Harmless for adding a non-text key.
- N2. 13.1 A / skeleton A: the ninth unpack name must sit at the same position as the new string in `CLASSES` (the unpack is positional); implied by the `CLASSES[5]`/`[7]` pitfall, not stated.
- N3. 14.4 C pointer (L1299): the clause "their facts are stated where they apply" overstates for the research-coverage gaps (G-11, G-14, G-25, G-28, G-31, G-32, G-34). One added sentence naming them would make it accurate.
- N4. Glossary lacks "Coordinator", "Run/Dispatch" and "Phase 1".
- N5. 14.4 intro: "Nine STALE DOC rows ... also CODE-CONTRADICTED" while SD-01, SD-06 and SD-07 are already tagged CODE-CONTRADICTED in their rows; wording only.

## Self-Audit

1. Factual claims independently verified against the snapshot or checkout: about 55 (keys.py 9 `Key(` sites, `_take`/`_take_escape`, `KEY_NAMES`, three help-line constants, `run_once`, two pinned tests, `page.py` usage, classify unpack/RULES/`_classification`/`Rule`, CLASSES, `NEXT_INSPECTION`, `report.py:26-27`, `classify.py:958, 976`, ALLOWED_ORCA/GIT and two test names, export field tuples, run.py/check.py exits, render.py designs/`--show`/`--width`, DESIGNS keys, 19 tests and their classes, sweep exit codes and byte limits).
2. Files read: the assembled document (all 1,392 lines), the consolidated findings, the fix log, `synthesis/synth-07-conventions-extension-debt.md` (14.4 and 14.5), `gaps-and-questions.md` lines 105-144, snapshot `keys.py`, `classify.py`, `models.py`, `report.py`, `collector.py`, `view.py`, `export.py`, `probes.py`, sweep `commands.py`, `page.py`, `run.py`, `check.py`, `tests/observe/test_session.py`, `tests/sweep/*`, and the checkout package `render.py`, `layouts/agent_focus.py`, `tests/test_designs.py`.
3. Reliance (inherited): I did not re-run structural checks (heading numbers, template columns) beyond a line count and the 14.2 header; template conformance GD-1/GD-2 relied on the fix log plus `wc -l`. Independent semantic checks where that was insufficient: GD-5 step text against `keys.py` and both pinned tests; GD-9 skeleton against the real registration and tuple types; GD-7 against the real package test classes and `render.py` `--show` path; the 14.4 C pointer against the original synthesis table and the 52-row gap register.
4. Findings count: 0 blocking, 5 minor. This is not a "0 issues" review: the five notes are real defects, graded minor by the severity rule.
5. Web research: none performed (no Tavily or fallback calls).

## Confidence

Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (items: GD-3, GD-4, GD-5, GD-6, GD-7, GD-8, GD-9, Section 13 steps, C8 candidates, designed-only, no-unification, new defects, UNVERIFIED classes, 14.4 C loss, glossary loss)
Tool engagement: Read: 20 | Grep: 15 | Glob: 1 | Bash: 2

## Overall Verdict: PASS (with notes)

Open blocking findings: 0.
