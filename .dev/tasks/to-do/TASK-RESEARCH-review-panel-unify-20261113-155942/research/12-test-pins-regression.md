# Research: Test inventory and pin migration

**Investigation type:** Code Tracer
**Scope:** `tests/review/` (19 test files + fixtures), `tests/cli/reflect/` (12 files), `tests/skills/test_review_severity_mapping.py`, `test_review_severity_rule.py`, `test_review_prompt_overrides.py`, `test_review_brief_placement.py`, `test_review_loop_extension.py`, `tests/skills/test_spec_panel_review_loop.py`
**Status:** Complete
**Date:** 2026-11-14

---

## 0. Collection run (actual command output, 2026-11-14)

Command (repository root, read-only collection; `pyproject.toml:112-113` adds `-v` to `addopts`, so `-qq` was used to get one node id per line):

```
uv run pytest --collect-only -qq tests/review tests/cli/reflect tests/skills/test_review_severity_mapping.py tests/skills/test_review_severity_rule.py tests/skills/test_review_prompt_overrides.py tests/skills/test_review_brief_placement.py tests/skills/test_review_loop_extension.py tests/skills/test_spec_panel_review_loop.py
-> 1182 tests collected in 0.60s
```

Per-area totals from the node-id list: `tests/review` **651** (19 files), `tests/cli/reflect` **353** (37 files), the six `tests/skills` files **178**. 651 + 353 + 178 = 1182.

Branch state: `git merge-base HEAD origin/master` = `d2d8a2d16` (the reflect Stage 0-2 commit #519 is already on master). The only test changes on this branch (E1, `ironbelly/shadow-runs`) relative to master are `tests/cli/reflect/test_shadow_skill_contract.py` (+42) and `tests/cli/reflect/test_shadow_exit_script.py` (+6/-9) (`git diff --stat d2d8a2d16 HEAD -- tests/...`).

**Correction to the task prompt:** `tests/cli/reflect/` holds **37** test files (plus `conftest.py`, `__init__.py`, `fixtures/`), not 12. Only 4 of them were added by the Stage 0-2 panel commit `d2d8a2d16` (`test_panel_contract_lint.py`, `test_shadow_exit_script.py`, `test_shadow_skill_contract.py`, `test_verdict_replay_script.py`); the other 33 predate the panel work (June-October 2026). [E1]

Key Takeaways
- 1182 tests guard the review surface: 651 package tests, 353 reflect CLI/skill tests, 178 skill-text tests.
- The 651 figure in `tests/review` is confirmed exactly.
- The "12 files" figure for `tests/cli/reflect` is wrong (37 files); 12 is the number of reflect files in `tests/review`.

---

## 1. Inventory: `tests/review/` (651 tests, 19 files)

Stack key: **v1 #346** = findings-v1 / ledger / merge / telemetry / panel (added by merge `9163bd1c7`, 2026-11-11) [E3]; **v2 reflect** = findings-v2 / card_convert / cluster_v2 / manifest / verify-citations / panel exclusion (added by `d2d8a2d16`, 2026-11-12) [E1]. Origin = first-add commit from `git log --diff-filter=A`.

| File | Lines | Collected | Stack | Covers |
|---|---|---|---|---|
| `test_review_findings.py` | 317 | 23 | v1 #346 [E3] | v1 parse, field validation incl. 12/200/300 limits, fixmap, locate, refs_norm, fingerprint, same_defect 3-line rule, cluster determinism |
| `test_review_ledger.py` | 566 | 24 | v1 #346 [E3] | ledger rounds 1-3, membership, status transitions, verdict/decision, no-valid-block refused, one-valid-block-enough (:376), missing anchor kept (:408), atomic save, merged report |
| `test_review_cli.py` | 449 | 13 | v1 #346 [E3], 4 tests added by reflect [E1] | click-level `review panel/merge/ledger/telemetry`; `d2d8a2d16` added `test_panel_resolve_hard_exclude_class_exhausts_the_fixed_anchor`, `..._without_the_new_flags_has_no_extra_keys`, `..._writes_skipped_slots_and_excluded`, `..._unknown_class_is_a_usage_error_listing_known_classes` (9 defs before, 13 after) |
| `test_review_panel.py` | 409 | 41 (26 defs, parametrised) | v1 #346 [E3] | template/tier validation, resolve determinism, env selection |
| `test_review_panel_live7.py` | 244 | 15 | v1 #346 [E3] (edited by `167184c6b`, ccsession tiers #488) | `@live7` shapes per environment |
| `test_review_rules_text.py` | 92 | 5 | v1 #346 [E3] | pins on `document_review_loop_prompts.md` text |
| `test_review_telemetry.py` | 409 | 10 | v1 #346 [E3] | review-telemetry/1 records |
| `test_review_findings_v2.py` | 444 | 92 | v2 reflect [E1] | findings-v2 line/block rules, limits |
| `test_review_card_convert.py` | 723 | 119 | v2 reflect [E1] | 4 card shapes -> findings-v2, fixtures `fixtures/reflect_cards/` |
| `test_review_cluster.py` | 795 | 113 | v2 reflect [E1] | cluster_v2 |
| `test_reflect_cluster_pairs.py` | 522 | 32 | v2 reflect [E1] | labelled pairs for same_defect_v2 |
| `test_review_cluster_cmd.py` | 262 | 15 | v2 reflect [E1] | `review cluster` CLI |
| `test_review_verify_citations.py` | 196 | 8 | v2 reflect [E1] | `review verify-citations` |
| `test_review_manifest.py` | 568 | 40 | v2 reflect [E1] | run manifest |
| `test_review_panel_exclusion.py` | 213 | 32 | v2 reflect [E1] | hard_exclude / strict_distinct; soft distinct repeats a model (:208) |
| `test_review_panel_reflect_profile.py` | 230 | 17 | v2 reflect [E1] | reflect profile rules, packaged-tier golden |
| `test_review_reflect_templates.py` | 161 | 21 | v2 reflect [E1] | six `reflect-*` templates |
| `test_reflect_consumer_inventory.py` | 364 | 14 | v2 reflect [E1] | consumer inventory script |
| `test_reflect_stage0a_replay.py` | 440 | 17 | v2 reflect [E1] | `scripts/reflect_stage0a_replay.py` |

Totals: v1 #346 files = 23+24+13+41+15+5+10 = **131** in 7 files (4 of the 13 in `test_review_cli.py` are reflect additions, so pure #346 = 127); v2 reflect files = **520** in 12 files. Both figures in the task prompt are **confirmed**, with the caveat on `test_review_cli.py`.

Hand-off section 8 (`research/scope/00-handoff-copy.md:303`) said "111 tests in tests/review (cli 9, findings 23, ledger 24, panel 26, panel_live7 14, rules_text 5, telemetry 10)". **[CODE-CONTRADICTED, explained]**: those are `def test_` counts at master before `d2d8a2d16` (`git show d2d8a2d16~1:tests/review/test_review_cli.py` has 9 defs; `test_review_panel.py` has 26 defs that collect as 41 because of parametrisation; live7 has 15 defs both before and after `d2d8a2d16`, not 14). [E2 claim about E3 files]

Fixtures:
- `clean.md`, `seeded.md` (v1 documents): used by `test_review_cli.py:13,374`, `test_review_ledger.py:14-15`, `test_review_telemetry.py:15`. [E3]
- `panel-golden-default-live7.json` (8 keys: `default|live7` x `anthropic-only|gateway` x `first|re-review`), `panel-golden-packaged-tiers.json` (2 keys + `tiers_sha256`), `review-tiers.frozen-1.0.0.json`, `reflect_cards/*` (6 files): all **added by `d2d8a2d16`** [E1] (`git diff --stat d2d8a2d16~1 d2d8a2d16 -- tests/review/fixtures`). Users: `test_review_panel_exclusion.py:23,53`, `test_review_panel_reflect_profile.py:75,89`.

Key Takeaways
- 651 = 131 (v1, 7 files) + 520 (reflect, 12 files) confirmed; 4 of the 131 are reflect tests living in the v1 CLI file.
- Every golden JSON fixture is an E1 artifact that pins E3 panel-resolution output; the v1 stack has no golden of its own.

---

## 2. Inventory: `tests/cli/reflect/` (353 tests, 37 files) and the skill-text tests (178 tests, 6 files)

| File | Lines | Collected | First added | Stack |
|---|---|---|---|---|
| `test_panel_contract_lint.py` | 409 | 38 | `d2d8a2d16` 2026-11-12 | reflect panel [E1] |
| `test_shadow_skill_contract.py` | 307 | 11 | `d2d8a2d16`, +42 lines on this branch | reflect panel [E1] |
| `test_shadow_exit_script.py` | 319 | 20 | `d2d8a2d16`, edited on this branch | reflect panel [E1] |
| `test_verdict_replay_script.py` | 190 | 13 | `d2d8a2d16` | reflect panel [E1] |
| `test_reviewer_readonly_tools.py` | 115 | 5 | `08b1a5f88` 2026-06-25 (#203) | reflect legacy (pre-panel) |
| `test_reviewer_brief_constraints.py` | 70 | 3 | `08b1a5f88` | reflect legacy |
| `test_reviewer_finding_parity.py` | 98 | 5 | `08b1a5f88` | reflect legacy |
| `test_reviewer_isolation_gate.py` | 127 | 4 | `08b1a5f88` | reflect legacy |
| `test_reviewer_swarm_target_grounding.py` | 104 | 2 | `08b1a5f88` | reflect legacy |
| `test_verify_denylist_git_mutations.py` | 76 | 3 | `08b1a5f88` | reflect legacy |
| `test_claudeprocess_reflect_children_restricted.py` | 133 | 5 | `08b1a5f88` | reflect legacy |
| `test_isolate_reviewers_cli.py` | 168 | 7 | `08b1a5f88` | reflect legacy |
| `test_ensemble_unit.py` / `_stub_integration.py` / `_fallback_stub.py` / `_fallback_engage.py` | 628/641/530/237 | 26/15/12/3 | `a589c24e3`, `87c180fb3` (June-July) | reflect Tier 2 headless ensemble + fallback ladder |
| `test_fallback_{classify,config,plan,select,slot_factory}.py` | 66/55/240/143/47 | 6/5/13/10/2 | `87c180fb3` 2026-07-07 | fallback ladder |
| `test_contract_fallback_metadata.py`, `test_contract_status_cli.py`, `test_preflight_phase_complete.py` | 260/292/182 | 8/8/8 | July 2026 | reflect contract |
| `test_verdict_mapping.py` | 637 | 36 | `bcad8852c` 2026-06-10 | reflect wrapper verdict |
| `test_cli_smoke.py`, `test_runner_e2e.py`, `test_fix_loop.py`, `test_writeback.py`, `test_base_precedence.py`, `test_classify_fix.py`, `test_marker_suppression.py`, `test_no_nesting_guard.py`, `test_promote_plumbing.py`, `test_docs_cli_parity.py`, `test_grader_yaml_root.py` | various | 12/10/9/4/6/11/6/6/9/2/1 | June 2026 | reflect auto-fix wrapper |
| `test_remediation_route_table.py`, `test_remediation_source_template.py` | 54/76 | 4/5 | October 2026 | reflect Tier 3 remediation |

All `tests/cli/reflect` files belong to reflect [E1-side], but only the first four rows are panel work; the rest guard legacy reflect behaviour that a unified panel must not regress (C5: legacy stays default and authoritative).

Skill-text tests [E3] (all from the #346 line of work on master):

| File | Lines | Collected (functions per hand-off) | First added | Pins |
|---|---|---|---|---|
| `tests/skills/test_spec_panel_review_loop.py` | 174 | 46 (11) | `95f2c6e43` 2026-11-07 | spec-panel `## Review Loop` bullets, src + plugin copies, HOW-WE-WORK sentence |
| `tests/skills/test_review_loop_extension.py` | 127 | 18 (9) | `5d9a0ae70` 2026-11-09 | P4 provenance / fail-closed / coverage clauses |
| `tests/skills/test_review_severity_mapping.py` | 145 | 14 (8) | `77e0a7029` 2026-11-09 | consequence grading + Medium tier |
| `tests/skills/test_review_severity_rule.py` | 520 | 62 (21) | `80f934de5` 2026-11-02 | minor never fails; 2-fix-cycle cap; rf-qa wording |
| `tests/skills/test_review_prompt_overrides.py` | 283 | 33 (14) | `f90aca51a` 2026-11-09 | banned quota wording in rf-qa etc. |
| `tests/skills/test_review_brief_placement.py` | 140 | 5 (5) | `9163bd1c7` 2026-11-11 | prompt text only in the rules file |

The hand-off section 8 function counts (11, 8, 14, 21, 9) are consistent with these collected totals once parametrisation is counted (178 collected for the six files).

Key Takeaways
- 353 reflect CLI tests, but only 82 (38+11+20+13) are panel/shadow tests; the other 271 guard legacy reflect behaviour.
- 178 skill-text tests pin the spec-panel loop and rf-qa wording; they are pure string pins over `src/` and `plugins/` copies.

---

## 3. Tests that pin current defects as intended behaviour (Q2)

Bodies read 2026-11-14. Each test below passes today **because** the defect exists, so a fix must change it on purpose.

### 3.1 `test_one_valid_block_is_enough_and_the_invalid_reviewer_is_reported` (`tests/review/test_review_ledger.py:376-385`) — pins **D3 and D2** [E3]

```
res = ldg.merge_round(led, new, 2, [rev("t1b-1"), _broken("t2-1")])
assert res["block_ok"] == {"t1b-1": True, "t2-1": False}
assert res["warnings"]
assert status(led)["L1"] == "resolved"
```

- D3: one valid reviewer (`t1b-1`, an empty findings block) plus one broken reviewer (`_broken` at :341-342, no findings block) is merged without error. Code: `ledger.py:150-157` raises only when `not any(block_ok.values())`. [CODE-VERIFIED]
- **D2 as well (new finding; the hand-off and scope slice 2 list D2 as "not covered")**: L1 was `resolved_check` after `apply_revision`; the invalid reviewer `t2-1` could not re-report it, yet the final assertion requires `"resolved"`. Code: `ledger.py:254-258` clears any `resolved_check` row with no cluster, never consulting `block_ok`; the docstring at `ledger.py:112` ("A reviewer with an invalid block is skipped for clearing") is contradicted by the code. [CODE-VERIFIED; docstring CODE-CONTRADICTED]
- `res["warnings"]` is only checked for truthiness, so the single-warning, first-error-only shape of D1 (`ledger.py:130-134`) is not pinned; adding ids/count to warnings will not break this test.

Related tests that stay valid under any D3 fix: `test_round_with_no_valid_block_is_refused_and_changes_nothing` (:345-361) and `test_first_round_with_no_valid_block_is_refused_not_pass` (:364-373) pin the zero-valid case only; CLI twin `test_merge_refuses_a_round_with_no_valid_block_and_writes_nothing` (`test_review_cli.py:425`). [E3]

### 3.2 `test_missing_anchor_is_kept_without_a_span` (`test_review_ledger.py:408-417`) — pins **D5** [E3]

A round-1 blocking finding whose anchor "this text is nowhere in the document" is asserted to become a row with `span is None`, `status == "open"`, `blocking is True`. No assertion on warnings exists, so adding a warning would not break it; dropping or demoting the finding would. Code path: `findings.py` annotate sets `anchor_status "missing"` (scope slice 2, `findings.py:349-358`). [CODE-VERIFIED for the test; findings.py lines from scope slice 2, not re-read here]

### 3.3 `test_soft_distinct_without_exclusion_still_repeats_a_model` (`test_review_panel_exclusion.py:208-213`) — pins **D11** [E1 test of E3 code]

`pnl.resolve(pnl.packaged_panel("live7"), frozen_tiers, "anthropic-only", "r1", "first")` must return 6 x `claude-haiku-5-5`. The comment at :209 says "soft distinctness re-admits Haiku". Also `test_emptied_pool_does_not_readmit_the_excluded_model` (:94-103) asserts the soft case `soft["model"] == "a"` (:97-98) — a second D11 pin. And the **golden byte-identity test** `test_no_exclusion_is_byte_identical_to_golden` (:56-72, 16 parametrised cases) pins the duplicates inside `panel-golden-default-live7.json` (e.g. `live7|anthropic-only|first` holds six haiku reviewers, `default|anthropic-only|first` three haiku; gateway `live7|gateway|first` has `glm-5.3` at both `t3-1` and `t3-2`). A strict-by-default D11 fix therefore breaks 16 + 1 + 1 cases in this file plus the two `panel-golden-packaged-tiers.json` cases (`test_review_panel_reflect_profile.py:75`).

### 3.4 D1 pins (rejection of over-length fields) [E3 + E1]

- v1: `test_field_validation` (`test_review_findings.py:111-122`) asserts `ok is False` for anchor < 12 (:112), anchor 201 (:113), 9 refs (:116), claim 301 (:117); `test_minor_blocking_is_an_error` (:105-108) asserts the finding list is **empty**. These pin "reject", not "drop silently"; a D1 fix that keeps rejection but records dropped ids keeps them green. A fix that **truncates** instead of rejecting breaks :113 and :117.
- v2: `test_review_findings_v2.py` ROWS table (:213+) rows `claim` 300/301 (:241), `refs` 8/9 (:242), `anchor` 12/11 (:243), `anchor2` (:250), `citations count` 8/9 (:251) and `test_citation_quote_optional_and_12_to_200` (:192-208). Same consequence as v1. [E1]
- v2 whole-block invalidation is pinned: `test_prior_lines_are_rejected` (:106-113) and `test_duplicate_id_rejected` (:150-153) assert `state == "invalid"` while still returning the good findings in `r["findings"]` (:111, :153). A D1 fix that makes one bad line not invalidate the block breaks these state assertions.
- legacy cards: `card_convert.py:85-86, 199-201` truncate claims to `MAX_CLAIM - 3` + `...` (truncate, not reject) [CODE-VERIFIED]; the two stacks already disagree on policy.

### 3.5 D8-adjacent: `test_older_pins_still_hold_and_no_source_path` (`test_review_rules_text.py:76-92`) [E3]

**[CODE-CONTRADICTED interpretation]** Scope slice 2 (section 6) lists this as a D8-adjacent pin. Reading the body: the "no source path" assertion is `assert "src/superclaude" not in TEXT` (:92). It forbids a repository path literal (the installed-primitive rule), **not** naming a source document. Adding a `{{SOURCE}}` placeholder to the briefs (the D8 fix) would not break it. What a D8 fix must keep: the three `- <label> brief: "` lines (:90-91) and `test_insertions_a_b_c_follow_their_brief_lines` (:34-42), which requires the findings-block insertion to be the line **immediately after** each brief line — a new source sentence must go inside the brief line, not on a new line between them. The same "no source path" pattern exists in `tests/skills/test_spec_panel_review_loop.py::test_t9_section_names_no_source_path` (see section 6).

### 3.6 Contract-text pins that a contract unification must change [E3]

`test_d_text_is_the_contract_text` (`test_review_rules_text.py:65-73`) pins the literal `findings-v1` info-string sentence, the full example finding line (anchor/anchor2/refs/claim keys), the prior line and the fix-map line. `test_each_insertion_is_present_exactly_once` (:28-31) pins `### Review panel` and the exact `superclaude review panel resolve --run-id <loop id> --kind <first or re-review>` sentence; `test_d_then_fix_map_then_e_come_before_never` (:45-62) pins `superclaude review ledger revise --ledger`. Moving the brief to findings-v2 or renaming the CLI breaks all three.

Key Takeaways
- Four tests pin defects: ledger :376 (D3 **and D2**), ledger :408 (D5), exclusion :208 and :97-98 (D11); the 16-case golden test also pins D11 duplicates.
- D2 is pinned, not uncovered: the hand-off's "D2 not covered" is wrong.
- The "no source path" rules-text test does not block the D8 fix; the adjacency test at :34-42 constrains where the source sentence can go.
- D1 limits are pinned as "reject" in both stacks; only a switch to truncation or per-line (not per-block) validity changes these tests.

### 3.7 Two further pins found while probing (not in the task's list)

- **D15 pinned** [E3]: `test_stratum_tag_is_optional_validated_stored_and_never_pooled` (`test_review_telemetry.py:324-327`) asserts `tel.validate_record(reviewer_record(stratum="gpt"))` is non-empty (rejected). Widening strata beyond `sonnet`/`haiku` must change :327.
- **v1/v2 import coupling pinned** [E1]: `test_module_does_not_import_v1_cluster` (`test_review_cluster.py:784-795`) asserts that `cluster.py` imports exactly `{"refs_norm", "_check_citation"}` from modules whose name contains `findings`. Moving `refs_norm` into a shared contract module (the obvious unification step, and the D7 fix site) breaks :794.
- **D7 neighbours** [E3]: `test_refs_norm` (`test_review_findings.py:201-212`) pins that `SHA-256` is not an id (:210) and lower-case `fr-9` is not an id (:212); `test_refs_norm_reads_claim_tokens_like_v1` (`test_review_cluster.py:221-230`) pins that v2 reads ids from the claim exactly like v1. A widened regex for `T01.02` must keep both green.

---

## 4. Defects with no test (Q3)

Probes run 2026-11-14 (`grep` over `tests/review/*.py` and `tests/cli/reflect/*.py`):

| Defect | Probe | Result | Effort |
|---|---|---|---|
| D1 dropped-id counter | `grep -n warnings` in ledger/cli tests | only `assert res["warnings"]` (`test_review_ledger.py:384`), truthiness only. No test asserts the dropped finding ids, their count, or that the ledger stores them (`ledger.py:141-149` stores only `block_ok`). **Uncovered.** | [E3] (also [E2], which measured 49 lost blocking findings) |
| D2 | see 3.1 | **Pinned, not uncovered** (ledger :376). No test covers the correct behaviour. | [E3] |
| D7 tasklist ids | `grep -n "T01\."` | hits only in `tests/cli/reflect/test_preflight_phase_complete.py:30,80,108,...` (tasklist headings for preflight, unrelated to `refs_norm`). No test feeds `T01.02` to `refs_norm` / `cluster` / `cluster_v2`. Regex at `findings.py:29` and `telemetry.py:23` [CODE-VERIFIED]. **Uncovered.** | [E3], shared by [E1] via `refs_norm` import |
| D12 `T2bModel01` | `grep -rn T2bModel01 tests/review tests/cli/reflect` | no hit. Only `test_panel_resolve_gateway_when_t3model01_is_set` (`test_review_cli.py:83-88`) pins the `T3Model01` key. **Uncovered.** | [E3] |
| D13 `lint_cmd` / `estimate_cmd` | `grep -rn "lint_cmd\|estimate_cmd"` | no hit. `test_review_help_lists_the_subcommands` (`test_review_cli.py:44-49`) checks only `panel, merge, ledger, telemetry` are present; nothing asserts that every registered module loads. **Uncovered.** | [E3] (loader shared by [E1] commands) |
| D16 round 4 / `--cap` on existing ledger | `grep -n cap` | `test_review_ledger.py:136` asserts `cap_reviews == 3` on a new ledger; `test_escalate_still_prints_verdict_fail` (:476-490) stops at round 3; `test_round_cannot_be_merged_twice_or_out_of_order` (:388-393) covers out-of-order, not round 4. **Uncovered.** | [E3] |
| v1/v2 limit equality | `findings.py:104,108,114,118` vs `findings_v2.py:80,111,117,126,132,136` vs `card_convert.py:85-86` [CODE-VERIFIED] | each stack has its own boundary tests (3.4), but **no test asserts the literals are equal** across v1, v2 and `card_convert`. `test_review_findings_v2.py:9` imports `line, report` from the v1 test module and :95-100 compares v1 vs v2 acceptance for one key only (`calibrated_confidence`). **Uncovered.** | [E3]+[E1] |

Hand-off section 8 "NOT covered" claims checked: D11 "not covered" is **[CODE-CONTRADICTED]** (it is pinned, 3.3); D2 "not covered" is **[CODE-CONTRADICTED]** (pinned, 3.1); D7, D12, D13 and D1-id are [CODE-VERIFIED] uncovered.

Key Takeaways
- Six gaps need new tests: D1 id/count recording, D7 tasklist ids, D12 alias check, D13 loader, D16 round cap, and one limit-equality test across v1/v2/card_convert.
- D2 and D11 are not gaps: they are pinned in the wrong direction.

---

## 5. Golden fixtures a contract change would force to regenerate (Q4)

| Fixture | Content | Pinned by | Regenerated when | Effort |
|---|---|---|---|---|
| `tests/review/fixtures/panel-golden-default-live7.json` | 8 serialized resolutions (`json.dumps(res, sort_keys=True, separators=(",", ":"))`) for `default`/`live7` x `anthropic-only`/`gateway` x `first`/`re-review`, run id `golden-run`, taken with the **frozen** tier file; embeds `schema: review-panel-resolution/1`, `template_sha256`, `tiers_sha256 1a2a8ad2...` | `test_no_exclusion_is_byte_identical_to_golden` (`test_review_panel_exclusion.py:56-72`, 16 cases) | (a) any change to the resolution record shape or key set (the test also asserts `skipped_slots`/`excluded` absent, :72); (b) any change to `review-panel.default.json` / `review-panel.live7.json` bytes (template sha); (c) a change of resolution algorithm, including strict-by-default distinctness (D11); (d) a schema id bump. Not affected by packaged tier edits (frozen copy). | [E1] test over [E3] code |
| `tests/review/fixtures/panel-golden-packaged-tiers.json` | 2 resolutions (`default`, `live7`, anthropic-only, first) + `tiers_sha256 a35908fa...` of the **packaged** `review-tiers.default.json` | `test_packaged_tiers_hash_and_resolutions_are_pinned` (`test_review_panel_reflect_profile.py:74-90`) | **any** byte change to `src/superclaude/cli/review/data/review-tiers.default.json` (e.g. adopting the E2 tier-list update, removing Qwen3.8-max, adding `tier0`), plus everything in the row above. The docstring (:3-6) records that this was already regenerated once by design (Task 9 `classes`). | [E1] |
| `tests/review/fixtures/review-tiers.frozen-1.0.0.json` | frozen copy of tier file 1.0.0 | exclusion tests (`:21-23`), `:89-90` asserts its sha differs from packaged | never, unless the frozen baseline itself is retired | [E1] |
| `tests/review/fixtures/reflect_cards/*` (6 files) | legacy reflect card shapes | `test_review_card_convert.py` (119 tests) | when card_convert output (findings-v2 shape, claim truncation, role mapping) changes | [E1] |
| `tests/review/fixtures/clean.md`, `seeded.md` | v1 spec documents | ledger, cli, telemetry tests | only if the v1 anchor model is dropped; the documents themselves are contract-neutral | [E3] |
| `tests/cli/reflect/fixtures/panel_lint_legacy/` | a legacy run directory (return-contract.yaml, adversarial/, reviewer-cards/) | `test_panel_contract_lint.py:15-20, :120-121` (P1) and all `make()` variants | when the contract version or the stable/telemetry key lists change | [E1] |

Non-fixture hard-coded resolution pins that behave like goldens [E3]: `test_review_panel.py:265-281` (default anthropic-only = sonnet + 3 haiku stand-ins), `test_review_panel_live7.py:48-60` (`models[1:] == ["claude-haiku-5-5"] * 6`), `:78-82` (tier2b model list in order), `:92-106` (tier list lengths equal `ccsession-models.json` slot counts — couples the review tier file to `src/superclaude/skills/ccsession-tag/ccsession-models.json`), `:109-125` (gateway live7 for run id `run-a`: t3 pair is exactly `{glm-5.3, Qwen3.8-max}`), `test_review_cli.py:52-80` (reviewer ids `t1b-1,t2-1,t3-1,t3-2`), `test_review_reflect_templates.py:92,99,115-117` (reflect template model lists).

Observation: the frozen golden `live7|gateway|first` holds `glm-5.3` at both `t3-1` and `t3-2` (D11 in gateway), while `test_review_panel_live7.py:123` asserts the two differ for run id `run-a`. Both pass because the draw depends on the run id; the golden is the only test that pins a gateway duplicate.

Key Takeaways
- Two goldens, both E1-owned, pin E3 resolution output; the packaged-tier golden breaks on any tier-file byte change, the frozen one on any template, algorithm or record-shape change.
- A unified panel that changes the resolution record (e.g. adds a duplicate flag or a run-manifest link) must regenerate both and update :72's "no extra keys" assertion.
- The live7 test couples the review tier file to the ccsession models file; a central tier source must keep that check or replace it.

---

## 6. Reflect pins C1, C6, C7, C8, C9, C14 and the `panel_lint` field lists (Q5) [E1]

All in `tests/cli/reflect/test_shadow_skill_contract.py` unless noted (read in full, 307 lines).

| Pin | Test (file:line) | What it asserts | Baseline |
|---|---|---|---|
| C1 | `test_stable_contract_block_and_version_are_byte_identical_to_head` (:42-49) | the yaml block after `### 9.1 Stable contract (contract_version: 1.8.0)` in the working-tree `SKILL.md` equals the same block in `git show HEAD:...`; contains `contract_version: "1.8.0"` | **HEAD** (`git()` helper :23-30). Skips if git is unavailable (:44-45). Once a change is committed, HEAD moves with it, so this guards only uncommitted edits. [CODE-VERIFIED] |
| C6 | `test_skill_changes_are_confined_to_the_allowed_sections` (:52-75) | every hunk of `git diff HEAD -U0 -- SKILL.md` lies under `### 3.1 ` (and the line contains `--t2-engine`), `### 4.3a `, `### 5.4 ` or `### 9.2 `; never `### 9.1 ` | **HEAD**, same caveat: a clean working tree passes trivially. [CODE-VERIFIED] |
| C14 | `test_no_new_src_superclaude_hit_in_the_skill_directory` (:78-98) | count of lines containing `src/superclaude` in the skill directory (working tree) <= the count at HEAD (`git grep -c`) | **HEAD**, also relative. [CODE-VERIFIED] |
| C7 | `test_the_brief_template_has_exactly_three_sections` (:146-165) | between `### Required sections (per brief)` and `### Contract emission` of `refs/reviewer-spec.md`, the `#### \`## ...\`` headings are exactly `T1 card excerpt`, `Grounding hunks`, `Coverage slice`; the T1 excerpt contains `findings-v2`, `reviewer_model_self_report`, `legacy run's briefs do not carry this line` | absolute text [CODE-VERIFIED] |
| C8 | `test_skill_names_the_card_header_fields_and_the_authority_of_the_legacy_path` (:168-180), `test_the_calibrator_line_is_shadow_only_...` (:183-196), `test_the_reviewer_brief_line_carries_the_schema_and_its_example_parses` (:199-218), `test_shadow_steps_pin_the_header_model_the_verdict_file_and_the_first_pass_metric` (:221-238), `test_shadow_card_headers_and_resolution_json_on_a_fixture_run` (:283-299), `test_a_card_header_missing_a_field_is_caught` (:302-307), `test_the_skills_manifest_recipe_runs_as_written` (:104-140) | needles inside the `**Shadow-mode steps` .. `### 4.5 ` slice (`persona:`, `model_class:`, `model:`, "authoritative and unchanged", `kept-ids.txt`, `judge_class_collision: unknown`, `model_observed:`, "valid on this first parse", "before any re-ask", "never edits, remaps or normalizes", `write <output>/adversarial/merged-verdict.yaml`, `` `adversarial/adversarial/` ``, "`reviewer_personas` and `reviewer_models`", "every shadow field goes under `telemetry:`"); the calibrator line occurs exactly once and its example parses with `cluster_cmd._embedded_calibration`; the brief line contains "JSON lines", "never a table", the exact heading phrase, **every `findings.SEVERITIES` and `findings.CATEGORIES` value** (:205-212), and its example parses as findings-v2 with `lens="reflect-pre"` (:213-218); `@reflect-pre --strict-distinct` in anthropic-only resolves to the legacy rotation `analyzer/sonnet, qa/haiku, refactorer/opus` (:243-247, :291-292) | absolute text + live CLI. The two tests at :199 and :221 were **added on this branch** (commits `9874d63fb`, `c2e3347d3`); the rest came with `d2d8a2d16`. [CODE-VERIFIED] |
| C9 | `tests/cli/reflect/test_reviewer_readonly_tools.py:69-115` (5 tests) | `src/superclaude/agents/reflect-reviewer.md` frontmatter `tools:` exists, non-empty, includes Read/Grep/Glob, excludes Bash/Edit/Write/NotebookEdit/Task; the same helper flags the fixture `fixtures/reviewer-personas/reviewer-persona-no-tools.md` | absolute [CODE-VERIFIED] |
| C9 | `tests/cli/reflect/test_reviewer_brief_constraints.py:35-70` (3 tests) | `## Constraints (READ-ONLY)` in reviewer-spec.md (read-only, no shell, git, mutat); "Live-execution prohibition", "MUST NOT embed live-execution instructions", "FR-4 verification-results" in SKILL.md; `reflect-reviewer` in both `### 7.1 Reviewer composition rules` (SKILL.md) and `## Composition` (reviewer-spec.md) (:58-70) | absolute [CODE-VERIFIED] |
| C2 | `tests/cli/reflect/test_panel_contract_lint.py:90-104` `test_pinned_field_lists_match_skill_md` (2 cases) and :107-114 `test_constant_sizes_and_load_bearing_import` | `pl.extract_field_list(SKILL, "### 9.1 Stable contract (contract_version: 1.8.0)")` equals `pl.STABLE_FIELDS_1_8_0` **in order**; same for `### 9.2 Telemetry (non-stable)` vs `pl.TELEMETRY_FIELDS`; sizes 110 and 27; `LOAD_BEARING_BOOLS is contract._LOAD_BEARING_BOOL_FIELDS`; `citations_dropped_extrapolated` in both lists | absolute; constants at `src/superclaude/cli/reflect/panel_lint.py:33` (`STABLE_FIELDS_1_8_0`), `:146` (`TELEMETRY_FIELDS`), `:184` (`LEGAL_MERGE_METHODS = ("adversarial", "single-reviewer-fallback")`) [CODE-VERIFIED] |
| C3 | `test_panel_contract_lint.py:67-71` (`bump()` message) and the F-cases | a new stable key or `merge_method` value is a "B bump rule" violation; message text pinned | `panel_lint.py:333` message [CODE-VERIFIED] |
| C10 | `tests/cli/reflect/test_shadow_exit_script.py` (20 tests) | exit criterion 20 clean shadow runs (`:125-135`, `OVERALL: PASS (shadow runs 20 of 20)`, cluster_agreement min, findings-block compliance); 12 runs insufficient (:147-150); EV-1 rate vs legacy baseline (:228-234); new degraded reason fails (:238); the current-repo test was **rewritten on this branch** from "0 of 20" to "reports without crashing" (:292-299, `git diff d2d8a2d16 HEAD`) | absolute + live `.dev/reflect` |

Cross-stack coupling worth noting: the C8 test at :199-218 imports **both** `findings` (v1 vocab) and `findings_v2` (parser). If the unified contract renames a severity or category in v1, this reflect test fails even though no reflect text changed. [E1]+[E3]

Key Takeaways
- C1, C6 and C14 compare against HEAD, so they protect only the uncommitted diff; they give no protection against a committed change, and they pass on a clean tree. A unified panel PR needs an absolute pin (against a stored hash or master) if those guarantees must survive the commit.
- C6 forbids SKILL.md edits outside §3.1/§4.3a/§5.4/§9.2; any unification that edits §7.1, §8 or §11.3 must change or retire C6 in the same change.
- C2 pins the field lists in order against SKILL.md; adding `merge_method: panel` or any new top-level key requires a contract bump and updating `panel_lint.py:33,146,184` together with the 110/27 sizes.
- C8 pins about 20 exact phrases plus the v1 vocabulary inside the reflect brief line.

---

## 7. Tests pinning spec-panel loop text and rf-qa wording (Q6) [E3]

All are static string pins, most parametrised over the `src/` copy and the `plugins/superclaude/` copy (which is why 63 functions collect as 178 items).

| File (tests) | What is pinned | Unification impact |
|---|---|---|
| `tests/skills/test_spec_panel_review_loop.py` (11 fn / 46 items, read in full) | `## Review Loop` exists once before `## Output Formats` (:75-79); **exactly seven single-line bullets** named Mode, Grading, Verdict, Cap, Re-review output, Reviser contract, Precedence, and no other non-blank line (:32-40, :82-91); cap text imported from `test_review_severity_rule.py` (:15, :94, :118-121); vocabulary `resolved|open|regressed`, `origin=changed|unchanged`, `verdict: PASS/FAIL`, `review: N of 3`, `Reviser brief`, `byte size before and after` (:95-129); rf-qa lookup order "the project `.claude/agents/rf-qa.md` first, else `~/.claude/agents/rf-qa.md`" (:104-138); precedence sentence (:112-153); no `src/superclaude` inside the section (:156-159); HOW-WE-WORK "It only reports." sentence carries `--re-review`, `--baseline`, "save a copy of the PRD" (:162-169); old sentence gone from guides (:172-174) | A unified spec-review module that adds an eighth bullet, or any line that is not one of the seven bullets, breaks :82-91. Replacing rf-qa as the spec-panel reviewer breaks :132-138. |
| `tests/skills/test_review_loop_extension.py` (9 fn / 18 items) | P4 provenance, fail-closed, scoped-pass coverage, reviser byte reporting, precedence clauses (:38-117); **`test_section_adds_no_script_or_parser_requirement` (:120-127) forbids the words `parser`, `script`, `state machine`, `transcript`, `asynchronous` anywhere in the Review Loop section** | Direct conflict with a unified panel: telling spec-panel to call the central panel CLI or a findings parser inside the Review Loop section breaks :126-127. Today the only CLI pointer lives in the rules file (`### Review panel`), not in the command; the unified design must keep CLI wording out of the section or change this test on purpose. |
| `tests/skills/test_review_severity_mapping.py` (8 fn / 14 items) | consequence grading and the Medium tier in spec-panel.md and `src/superclaude/output-styles/pragmatic.md`; Medium follows the untouched S1-S5 (:117); security/data-loss never downgraded by label (:140) | D9 (Medium for `missing-requirement`) touches the same text; a unified severity scale (CRITICAL/MAJOR/MINOR vs Medium vs reflect classes) must keep these or move them. |
| `tests/skills/test_review_severity_rule.py` (21 fn / 62 items) | canonical S1-S3 (and S5) rule bullets copied verbatim into **ten files**: `src/superclaude/agents/rf-qa.md`, `rf-qa-qualitative.md`, two document templates, two MDTM templates, four QA prompts (:181-203); no `(S1)`-style labels (:206-210); `CANONICAL_CAP_TEXT` "at most 2 fix cycles (3 reviews), then escalate ..." and `AT_CAP_CLAUSES` (:215-219) in the style and wherever `fixtures/review_severity_cap_edits.yaml` rows add them (:228-245); no "any severity" wording in tracked primitives (:172) | An rf-qa replacement must carry S1-S3/S5 verbatim or be removed from `S1_S3_FILES` on purpose. The cap text is also imported by the spec-panel test, so one edit breaks both files. |
| `tests/skills/test_review_prompt_overrides.py` (14 fn / 33 items) | brief lint: no "any severity ... FAIL", "assume defects remain", finding quotas, "apply all findings" (:35-50) in the briefs of `document_review_loop_prompts.md` (:61-63, :107-110); QA agents use the independent stance (`rf-qa.md`, `rf-qa-qualitative.md`, `agent_template_qa.md`, :259-264); HOW-WE-WORK and its plugin twin byte-equal (:134); removed quota wording does not return in skills/agents/templates/commands (:172, :217) | Any new panel brief (reflect, tasklist, PR) should be added to `BRIEF_SOURCES` so the same lint guards it; today only the #346 rules file is linted. The reflect `reviewer-spec.md` brief and the E2 eval brief are **not** linted. |
| `tests/skills/test_review_brief_placement.py` (5 fn / 5 items) | all prompt text lives only in the rules file (:38-68, no `src/superclaude` in it); spec-panel carries a one-sentence gate that restates nothing (:73-103); HOW-WE-WORK points at the gate (:106); installer ships the rules file (:119); plugin bundles it (:129-135) | A central brief library must keep "prompt text in one rules file" or retire this test; it is the closest existing precedent for a shared brief location. |

Key Takeaways
- The spec-panel Review Loop is frozen at seven bullets and forbidden to mention a parser or script; a unified panel consumer cannot be wired in through that section without changing two tests on purpose.
- rf-qa wording is pinned in ten files by S1-S3/S5 verbatim copies and the cap text; replacing rf-qa means moving those pins, not deleting them.
- The brief lint covers only the #346 rules file; extending `BRIEF_SOURCES` is the cheapest way to guard the reflect and tasklist briefs too.

---

## 8. Proposed no-regression gate list (Q7, part 1)

Every command is read-only apart from pytest's default cache. Collected counts are from section 0.

| # | Suite | Command | Guards | Items |
|---|---|---|---|---|
| G1 | v1 finding contract | `uv run pytest tests/review/test_review_findings.py` | findings-v1 parse/validate, limits, refs_norm, same_defect, cluster | 23 [E3] |
| G2 | v1 ledger and verdict | `uv run pytest tests/review/test_review_ledger.py tests/review/test_review_cli.py` | ledger statuses, rounds 1-3, verdict/decision, zero-valid refusal, CLI round trip, reflect panel CLI flags | 37 [E3]+[E1] |
| G3 | Panel resolution | `uv run pytest tests/review/test_review_panel.py tests/review/test_review_panel_live7.py tests/review/test_review_panel_exclusion.py tests/review/test_review_panel_reflect_profile.py tests/review/test_review_reflect_templates.py` | templates, tiers, env select, @live7, hard_exclude/strict_distinct, reflect profile, both goldens, ccsession slot-count coupling | 126 [E3]+[E1] |
| G4 | Telemetry | `uv run pytest tests/review/test_review_telemetry.py` | review-telemetry/1, strata | 10 [E3] |
| G5 | findings-v2 and card conversion | `uv run pytest tests/review/test_review_findings_v2.py tests/review/test_review_card_convert.py` | v2 contract, reflect lens rules, legacy card shapes | 211 [E1] |
| G6 | Clustering v2 | `uv run pytest tests/review/test_review_cluster.py tests/review/test_reflect_cluster_pairs.py tests/review/test_review_cluster_cmd.py` | cluster_v2, chain detection, labelled pairs, v1-import coupling | 160 [E1] |
| G7 | Citations, manifest, replays | `uv run pytest tests/review/test_review_verify_citations.py tests/review/test_review_manifest.py tests/review/test_reflect_consumer_inventory.py tests/review/test_reflect_stage0a_replay.py` | verify-citations, run manifest, consumer inventory, Stage 0a replay | 79 [E1] |
| G8 | Reflect contract and shadow | `uv run pytest tests/cli/reflect/test_panel_contract_lint.py tests/cli/reflect/test_shadow_skill_contract.py tests/cli/reflect/test_shadow_exit_script.py tests/cli/reflect/test_verdict_replay_script.py` | C1-C3, C6-C8, C10, C14; 1.8.0 field lists; EV-1/EV-2 | 82 [E1] |
| G9 | Reflect legacy (must not move) | `uv run pytest tests/cli/reflect` (the remaining 33 files) | reviewer isolation (C9, C15), ensemble, fallback ladder, verdict mapping, wrapper, remediation | 271 [E1] |
| G10 | Review-loop and rf-qa text | `uv run pytest tests/skills/test_spec_panel_review_loop.py tests/skills/test_review_loop_extension.py tests/skills/test_review_severity_mapping.py tests/skills/test_review_severity_rule.py tests/skills/test_review_prompt_overrides.py tests/skills/test_review_brief_placement.py` | spec-panel Review Loop, severity rule, cap text, banned brief wording, brief placement | 178 [E3] |
| G11 | Rules text | `uv run pytest tests/review/test_review_rules_text.py` | findings-v1 contract text and CLI sentences in the rules file | 5 [E3] |
| G-all | everything above | `uv run pytest tests/review tests/cli/reflect tests/skills/test_review_severity_mapping.py tests/skills/test_review_severity_rule.py tests/skills/test_review_prompt_overrides.py tests/skills/test_review_brief_placement.py tests/skills/test_review_loop_extension.py tests/skills/test_spec_panel_review_loop.py` | the whole surface | 1182 |
| G-ext | non-test gates | `uv run python scripts/reflect_shadow_exit.py` and `scripts/reflect_verdict_replay.py` (from scope slice 3; arguments UNVERIFIED here); `make verify-sync` | C10 stage exit, zero new degraded reasons; src/.claude sync | n/a [E1]/[E3] |

Note: the HEAD-relative tests in G8 (C1, C6, C14) must be run **before** committing a unification change; after the commit they pass trivially (section 6).

Key Takeaways
- Eleven suites plus one aggregate command cover all 1182 items; G9 (271 legacy reflect tests) is the largest block and should stay unchanged by any unification.
- C1/C6/C14 are only meaningful on an uncommitted working tree; the gate procedure must say so.

---

## 9. Per-fix test migration (Q7, part 2)

"Must change" = the test passes today and will fail after the fix; "add" = new test needed. Replacement assertions are proposals, written so they can be checked against the fix.

| Fix | Tests that must change (file:line) | Replacement assertion | Tests to add | Effort |
|---|---|---|---|---|
| **D1** record dropped findings (ids, count, reason) | none if rejection stays; `test_review_findings.py:113,117` and `test_review_findings_v2.py:241-251` (ROWS) + `:192-208` if the policy becomes truncation; `test_review_findings_v2.py:106-113,150-153` if one bad line no longer invalidates the block | truncation: `parse_block(report(line(claim="x"*301)))["findings"][0]["claim"]` has length 300 and ends with `...`, and a `truncated` field names the field; per-line: `state == "partial"` with the good findings clustered | `merge_round` result and the ledger round entry list `dropped: [{"reviewer_id", "fid", "reason"}]` and the warning carries every error, not only `errors[0]` (`ledger.py:130-134`, `:141-149`); a CLI test that `review merge` prints the count | [E3]+[E1] (measured by [E2]) |
| **D2** invalid reviewer cannot clear a row | `test_review_ledger.py:376-385`, final assertion :385 | `assert status(led)["L1"] == "resolved_check"` and the round result names `t2-1` under a `not_cleared_because_invalid` key (or equivalent) | a test where every reviewer is valid and none re-reports L1 → `resolved` (keeps `test_cleared_after_the_next_round_and_refound_stays_open` :193-217 as the positive case) | [E3] |
| **D3** minimum valid reviewers | `test_review_ledger.py:376-385` (merge would now raise or mark the round degraded) | `with pytest.raises(ldg.LedgerError, match="valid findings block")` when fewer than the quorum are valid, or `res["degraded"] is True` and `res["verdict"] != "PASS"` | quorum boundary test (k-1 valid fails, k valid passes); CLI exit code twin of `test_review_cli.py:425` | [E3] |
| **D4** quorum / calibrated blocking | `test_review_ledger.py:128-129` (`brief_ids == ["L1","L2","L4"]`; L2 and L4 are single-reviewer rows, :121), `test_verdict_and_decision_at_rounds_1_to_3` (:277-304, single reviewer FAIL), `test_capture_export` (:420-429) if the capture gains a support field | `res["brief_ids"] == ["L1"]` under quorum 2, with L2/L4 listed as `disputed`; or keep any-blocking but assert `confidence` is reported per brief id | a test that `confidence`/`support` is consumed by the verdict | [E3]; reflect `cluster_v2` support/disputed [E1] is the candidate mechanism |
| **D5** missing anchor | `test_review_ledger.py:408-417` (:417 `status == "open"` and `blocking is True`) | `res["warnings"]` contains the finding id and "anchor not found"; and either the row is `blocking is False` / `status == "unverified"`, or kept blocking with the warning (then only the warning assertion is added and :417 stays) | — | [E3]; v2 analogue `citations.unresolved` [E1] |
| **D6** chain detection in v1 | v1 same_defect tests `test_review_findings.py` (:235-317) and membership `test_review_ledger.py:139-150` if clusters split | per-cluster `chained` flag equals v2 behaviour; L1 membership unchanged for the two-member case | adopt `test_reflect_cluster_pairs.py` labelled cases for the unified clusterer | [E3]+[E1] |
| **D7** tasklist ids | none (no test feeds `T01.02`) | — | `refs_norm({"claim": "T01.02 breaks AC-3", ...})` contains `T01.02` and `AC-3`; `SHA-256` and `fr-9` stay excluded (`test_review_findings.py:210,212`); same for `telemetry._ID_RE`; `cluster_v2` joins two findings citing `T01.02` | [E3], [E1] via import |
| **D8** brief names the source document | none required if the source sentence is added **inside** the quoted brief lines; `test_review_rules_text.py:34-42` breaks if a new line is inserted between a brief line and its findings-block insertion | — | `{{SOURCE}}` (or equivalent) appears in the placeholder list and in the first-review and re-review briefs; a lint that every shipped brief names its source | [E3]; reflect brief already has a `spec` citation role [E1]; measured by [E2] |
| **D9** missing-requirement severity | `test_review_severity_mapping.py` grading bullets if the rule text moves | — | one test that the brief's per-category rule and `findings.py`'s schema agree | [E3] |
| **D10** `unpassable-check` | none | — | v1 `parse_block` accepts `category: "unpassable-check"` and rejects `unpassable-ac` | [E3] |
| **D11** strict distinctness by default (or a duplicate flag) | `test_review_panel_exclusion.py:208-213` and `:97-98`; golden test `:56-72` (16 cases) + regenerate `panel-golden-default-live7.json`; `test_review_panel_reflect_profile.py:74-90` + regenerate `panel-golden-packaged-tiers.json`; `test_review_panel_live7.py:48-60` (6 haiku); `test_review_panel.py:265-281` (3 haiku); `test_review_cli.py:52-80` (4 reviewer ids) | strict: `pnl.resolve(live7, ..., "anthropic-only", ...)` yields `[sonnet, haiku]` plus `skipped_slots` naming 5 slots; flag-only: `res["duplicates"] == [{"model": HAIKU, "reviewer_ids": [...]}]` and models unchanged (then only the goldens and :72's "no extra keys" change) | gateway duplicate case (`live7|gateway|first` golden has `glm-5.3` twice) asserted explicitly | [E3] code, [E1] tests |
| **D12** tier alias existence | `test_review_cli.py:83-88` only if env detection changes key | — | `T2bModel01` unset with `tier2b` in the template → validation error or explicit warning; positive case with both set | [E3] |
| **D13** loader | `test_review_help_lists_the_subcommands` (`test_review_cli.py:44-49`) if `lint`/`estimate` are added | — | every name in `__init__`'s module list imports; `review --help` lists exactly those commands (catches a silently missing `cluster`, `verify-citations`, `manifest`) | [E3]+[E1] |
| **D14** tasklist review step | none | — | a skill-text test (G10 style) that `sc-workflow-protocol` / `sc-tasklist-protocol` name the review step and its rules file | [E3]/[E2] |
| **D15** strata | `test_review_telemetry.py:327` (`stratum="gpt"` rejected) | `validate_record(reviewer_record(stratum="gpt")) == []` if strata become model classes from the tier file's `classes` map | merge/resolve append a telemetry record | [E3] |
| **D16** cap enforcement | none | — | `merge_round(led, ..., 4, ...)` raises when `cap_reviews == 3`; `--cap` on an existing ledger is an error or is applied | [E3] |
| **Contract unification** (one finding contract, v2 superset) | `test_review_rules_text.py:65-73` (literal `findings-v1` sentence and example line), `:28-31`/`:45-62` if CLI names change; `test_review_findings_v2.py:95-113` (v1/v2 divergence on `calibrated_confidence` and prior lines is pinned as intended); `test_review_cluster.py:784-795` (import set `{refs_norm, _check_citation}`); `test_shadow_skill_contract.py:199-218` (imports v1 `SEVERITIES`/`CATEGORIES`); `test_panel_contract_lint.py:90-114` + `panel_lint.py:33,146,184` if `merge_method` gains a panel value (contract bump); C6 (`test_shadow_skill_contract.py:52-75`) if SKILL.md sections outside the allowed four change; `test_review_loop_extension.py:120-127` if the Review Loop section must name the CLI | rules text pins the new info string and example line; `test_module_does_not_import_v1_cluster` asserts the import comes from the shared contract module; brief-vocabulary test reads the shared contract's enums | one **limit-equality test**: the claim/anchor/anchor2/refs/citation limits used by v1, v2 and `card_convert.MAX_CLAIM`/`MAX_REF_TEXT` come from one constant (or are asserted equal); one v1→v2 round-trip test (same report, info string swapped, same findings) | [E1]+[E3] |

Key Takeaways
- D2, D3, D5 and D11 each have a named test that must flip; D11 alone touches about 25 collected items and both goldens.
- D4's pin is easy to miss: `brief_ids == ["L1","L2","L4"]` (`test_review_ledger.py:129`) encodes "one reviewer's blocking flag decides".
- D7, D10, D12, D13, D14, D16 and the limit-equality check are additions only; no existing test needs to change.

---

## Gaps and Questions

- [UNVERIFIED] `findings.py:349-358` (D5 annotate path) cited from scope slice 2, not re-read in this report.
- [UNVERIFIED] Arguments and exact behaviour of `scripts/reflect_shadow_exit.py` and `scripts/reflect_verdict_replay.py` for gate G-ext; only their tests were read.
- [UNVERIFIED] Bodies of `test_review_card_convert.py`, `test_review_cluster.py` (beyond :218-232, :780-795), `test_review_manifest.py`, `test_reflect_consumer_inventory.py`, `test_reflect_stage0a_replay.py`, and the 33 legacy reflect files: classified by name, first-add commit and collected count only.
- [CODE-CONTRADICTED] Task prompt: `tests/cli/reflect/` has 37 test files, not 12.
- [CODE-CONTRADICTED] Hand-off section 8 (`00-handoff-copy.md:303`) "111 tests in tests/review": these are pre-`d2d8a2d16` function counts; current collection is 651 (131 in the #346 files); `panel_live7` has 15 functions, not 14.
- [CODE-CONTRADICTED] Hand-off section 8 (`:305`) lists D2 and D11 as "NOT covered"; both are pinned in the defect direction (`test_review_ledger.py:376-385`; `test_review_panel_exclusion.py:97-98,208-213` and the golden).
- [CODE-CONTRADICTED] Scope slice 2 section 6 calls `test_older_pins_still_hold_and_no_source_path` D8-adjacent; its "no source path" check is `"src/superclaude" not in TEXT` (`test_review_rules_text.py:92`), unrelated to naming a source document.
- [CODE-CONTRADICTED, minor] Scope slice 2 section 5 says `telemetry.py:22` holds `_ID_TOKEN`; it is at `telemetry.py:23` (the hand-off's :23 was right; `_ID_RE` is :24).
- [CODE-CONTRADICTED] `ledger.py:112` docstring vs `ledger.py:254-258` (D2), restated from scope slice 2 and re-read here.
- Question: should C1/C6/C14 compare against `origin/master` or a stored hash instead of HEAD, so they still guard after a commit?
- Question: is `test_section_adds_no_script_or_parser_requirement` (`test_review_loop_extension.py:120-127`) a deliberate design rule (spec-panel stays prompt-only) that the unified panel must respect, or an artefact of the #346 P4 scope? The owner should decide before a spec-review module is wired in.
- Question: should the reflect `reviewer-spec.md` brief and any tasklist brief be added to the brief lint `BRIEF_SOURCES` (`test_review_prompt_overrides.py:61-63`)?
- Question: the live7 test couples `review-tiers.default.json` list lengths to `src/superclaude/skills/ccsession-tag/ccsession-models.json` (`test_review_panel_live7.py:86-106`); memory notes `ccsession-models.json` is fetched live from master at launch, so a tier-list change needs both files changed in one PR.

## Stale Documentation Found

- **[STALE DOC]** `research/scope/00-handoff-copy.md:303` (hand-off section 8): test counts reflect master before the reflect Stage 0-2 merge (111 vs 651 now).
- **[STALE DOC]** `research/scope/00-handoff-copy.md:305`: "NOT covered" list includes D11 and (implicitly) D2, which are pinned.
- **[STALE DOC]** Task prompt for this report: "tests/cli/reflect/ (12 files)".
- **[STALE DOC]** `tests/cli/reflect/test_shadow_exit_script.py` before this branch asserted "0 of 20" for the current repository; rewritten on this branch (`git diff d2d8a2d16 HEAD`), so any doc quoting the old test name `test_the_current_repository_has_no_shadow_runs` is stale.
- **[STALE DOC]** `src/superclaude/cli/review/ledger.py:112` docstring ("skipped for clearing") does not describe the code.

## Summary

The review surface is guarded by 1182 collected tests: 651 in `tests/review` (131 in the 7 #346 files, 4 of them reflect additions, and 520 in 12 reflect files; both figures confirmed), 353 in 37 `tests/cli/reflect` files (not 12; only 82 are panel/shadow tests) and 178 skill-text pins. Four tests pin defects as intended behaviour: `test_review_ledger.py:376` pins D3 **and D2** (the hand-off called D2 uncovered), `:408` pins D5, and the exclusion tests plus both E1-owned golden fixtures pin D11 duplicates; `test_review_ledger.py:129` also encodes D4 and `test_review_telemetry.py:327` encodes D15. D1 id recording, D7, D10, D12, D13, D14, D16 and v1/v2 limit equality have no test and need additions only. The reflect pins C1, C6 and C14 compare with HEAD and so only guard uncommitted edits, while C2, C7, C8 and C9 are absolute text pins, one of which imports the v1 vocabulary. Two #346 skill tests constrain where a unified panel can plug in: the spec-panel Review Loop is frozen at seven bullets and may not mention a script or parser.
