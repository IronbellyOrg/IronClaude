# Research: Reflect merge path and contract constraints

**Investigation type:** Architecture Analyst
**Scope:** `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (§3.1, §4.3a, EV-1, contract consumers, §9.1 contract 1.8.0, `merge_method`, §9.2, testability map); `src/superclaude/cli/reflect/panel_lint.py`; `src/superclaude/cli/reflect/contract.py`; `tests/cli/reflect/` (12 files); `.dev/reflect/pre-*-shadow*/adversarial/merged-verdict.yaml`; `scripts/reflect_shadow_exit.py`; `scripts/reflect_verdict_replay.py`; `~/.claude/skills/sc-adversarial-protocol/SKILL.md` (Mode A); scope slices `research/scope/00-handoff-copy.md` §5.6, `03-reflect-side.md` §1.2/2/4/5/7, `04-this-session-artifacts.md` §0.11-0.15/4
**Status:** Complete
**Date:** 2026-11-13

---

Repository root: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel`, branch `ironbelly/shadow-runs`, HEAD `792cf8c52`. All paths below are relative to that root. Effort tags: [E1] reflect Tier 2 panel kernel / shadow / combo experiment (this branch; kernel itself already on origin/master via #519 per scope slice 03 baseline note); [E2] tasklist review-panel study at `4a22d742`; [E3] #346 review loop on master (findings-v1, ledger, `superclaude review merge/ledger/panel/telemetry`).

## 0. Scope inputs read first (context only, not evidence)

- `research/scope/00-handoff-copy.md` §5.6 (lines 250-259): the E2 hand-off's contrast table says reflect Tier 2 uses 2-3 fixed `reflect-reviewer` agents, a blind calibrator, `sc-adversarial-protocol` Mode A merge then the evidence-validator gate, and that the E2/E3 panel uses a deterministic script merge ("any-blocking => FAIL"). The hand-off itself marks its SKILL.md citations "UNVERIFIED by re-read" (:250). This file re-verifies the reflect side in sections 1-3. [E1][E2][E3]
- `research/scope/03-reflect-side.md` §5 lists constraints C1-C16 (:183-200); §1.2 records a 2026-11-13 run of the exit script (`OVERALL: FAIL (shadow runs 13 of 20)`) (:55-57); §7 notes the HEAD-vs-master risk for C1/C6 (:227). Each constraint is re-checked against code in section 6 below.
- `research/scope/04-this-session-artifacts.md` §0.12 (:123-129): the shadow-failure troubleshoot report root-caused EV-1 failures to file placement (`adversarial/adversarial/merged-verdict.yaml` or `.md` only), not to a missing debate; §0.14 (:143-150): 15 combo runs, no blind quality scoring; §0.15 (:152-167): the earlier exit-script run captured only a tail, so EV-1 counts were UNVERIFIED there; §4.1 (:273-274): the merged-requirements design (MR) kept the debate, kept contract 1.8.0 unchanged through Stage 4, and deferred "E'" (deterministic merge, contract 2.0.0). Those MR decisions are cited second-hand and not re-read here.

Key Takeaways
- Prior slices already list C1-C16; this file re-verifies each against code and answers the merge-path question with recorded run data.
- The deterministic-merge option (E') was deferred to a contract 2.0.0 in the E1 design (per slice 04 §4.1; MR not re-read, [UNVERIFIED] here).

---

## 1. SKILL.md: the reflect merge path and its contract text [E1]

File: `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (2033 lines). SKILL.md is the protocol the orchestrating model executes; its claims about code are tagged, its own rules are reported as "the protocol says" (they are the spec, not a code claim).

### 1.1 §3.1 `--t2-engine` (line 87)

- Values `legacy | shadow`, default `legacy`; read only at the start of Wave 3 and only when the final tier is 2. `panel` is rejected with the literal message `"--t2-engine panel ships in Stage 3; use legacy or shadow."`; any other value STOPs; "With `legacy` the panel code is never called." (:87).
- Code check: there is no Python parser for `--t2-engine` under `src/superclaude/cli/reflect/`; scope slice 04 §0.16 recorded a grep showing `t2_engine|t2-engine` only in `cli/review/manifest.py` and `manifest_cmd.py` (the manifest's `--t2-engine-requested/-effective` options). The flag is therefore a protocol rule executed by the model, not a CLI flag. [CODE-VERIFIED second-hand via slice 04 §0.16 grep; the reject message has no code home]

### 1.2 §4.3a engine selection and shadow steps (lines 309-349)

- Legacy keeps contract 1.8.0 unchanged: "no stable field, `merge_method` value or contract version changes" (:311). Shadow is UC-1 only (Stage 2); "In UC-2 (post-execution) runs the flag is accepted and ignored until Stage 5." (:311).
- Rules D1-D5 (:317-321). D3's floor effects (`t2_floor_unmet` in `degraded_components`, forced `status: partial`, REPORT banner) apply "only when the effective engine is `panel`, which ships in Stage 3" (:319). So Stage 3 already has a written behaviour change that touches stable-adjacent outputs (`status`, `degraded_components` is telemetry).
- Shadow steps 1-10 (:338-349) run next to legacy and "change no verdict, no stable contract field and no `merge_method`" (:338). Step 6: `review cluster` and `review verify-citations` "Neither drops anything and neither feeds the debate"; `cluster_agreement` is "never compared with the convergence thresholds, never routes anything" (:345). Step 7: the debate is "legacy, unchanged"; after it the orchestrator must write `<output>/adversarial/merged-verdict.yaml` (fields `merge_method`, `verdict`, `convergence_score`, `base_variant`, `source_cards`, merged findings; "copy, never invent a value") and confirm it on disk because EV-1 reads exactly that path (:346). Step 7 also records `judge_identity` / `judge_class_collision: unknown` when sc-adversarial's contract names no judge (:346).
- Step 10: contract must record `reviewer_personas` and `reviewer_models` and "no top-level key outside the stable list; every shadow field goes under `telemetry:`" (:349).

### 1.3 Wave 4/5 merge path (lines 679-714, 353-359)

- Delegation table: `sc-adversarial-protocol` (Mode A `--compare`) merges 2-3 cards "via the established debate + scoring + merge pipeline. Reflect does NOT re-implement debate." (:681).
- Invocation: `Skill sc-adversarial-protocol with --compare <output>/reviewer-cards/reviewer-1-card.yaml,... --depth standard --focus correctness,coverage,deviation-classification --output <output>/adversarial/` (:693-699). Under `--unattended` the output goes to `<report-dir>/nested/adversarial-<n>/` and EV-1 reads the child named by that contract's `artifacts_dir` (:701).
- Convergence routing ">=0.75 PASS, >=0.60 PARTIAL, <0.60 FAIL" (:703). Consumer-side rename `artifacts_dir` -> `adversarial_artifacts_dir` (:705).
- Step 5.0 probe and fallbacks (:353-359): F1 retry; F2 "use the highest-calibrated single Tier 2 reviewer verdict ... mark `merge_method: single-reviewer-fallback`"; F3 `adversarial_unavailable: true` + `status: partial`; "loud, never silent: every F-step writes to audit.log".

### 1.4 Contract consumers (lines 707-712)

- Consumers "(sprint, sc-troubleshoot, task) and the §14.5.2 promotion gate" must route on `merge_method` FIRST; `single-reviewer-fallback` makes `convergence_score` inapplicable (:709). Null comparisons are undefined and must be guarded (:710). Promotion gate condition 9: `tier_reached == 2 AND convergence_score == null` blocks promotion (:711). Sprint routing of null: `status: partial` + `next_action: halt-phase-for-review` (:712).
- Code check of the wrapper consumer: see section 3 (`contract.py`). Sprint `executor.py` routing and the promotion gate code were not read in this slice: [UNVERIFIED].

### 1.5 EV-1 (line 714) and the testability map (line 1955)

- EV-1 completion rule (:714): Wave 4 is complete only when EITHER (a) the orchestrator reads disk (Glob/Bash, "NOT a self-written field") and finds `<output>/adversarial/merged-verdict.yaml` with `merge_method: adversarial` AND `<output>/reviewer-cards/` holds at least the resolved `--reviewers` count of blind-calibrated cards (minimum 2), OR (b) a loud fallback fired and is corroborated on disk: `adversarial_unavailable: true` AND an audit.log F-step entry for F2/F3 (and `merge_method == single-reviewer-fallback` when F2).
- On MALFORMED: write a MALFORMED audit.log row, re-run Waves 3-4 up to 2 more times or route to F2/F3, HALT only if still MALFORMED (:714). The STOP explicitly blocks "an illegal `merge_method`" (:714).
- Testability map row (:1955): `file_present + card_count`, same two conditions. Note it only encodes branch (a); the loud-fallback branch (b) is not in the testability row (it is in `panel_lint` L6, section 2.3).

### 1.6 §9.1 stable contract 1.8.0 (lines 724-893) and `merge_method` (line 837)

- `contract_version: "1.8.0"` (:727). The header comment records the history: 1.7.x "EV-1 Wave-4 ORCHESTRATOR-VERIFIES-ON-DISK merge gate + EV-2 merge_method legal-values guard (no stable-field change)" (:727). So EV-1/EV-2 were added without a version bump because they changed semantics, not fields.
- `merge_method: adversarial | single-reviewer-fallback` with "[EV-2] LEGAL VALUES ARE EXACTLY {adversarial, single-reviewer-fallback}: any other value (inline, convergence-inline, an in-context "convergence" of the cards) is MALFORMED -> reject. A non-adversarial merge is legal ONLY via the F2/F3 fallback ... Reflect MUST NOT synthesize its own merge." (:837). The same text is repeated in the §15.1 metrics-export JSON (`"adversarial": {"merge_method": ...}`, :1780) and the metrics label list names `adversarial.merge_method` (:1810).
- Tier 2 artifact fields beside it: `reviewer_cards`, `adversarial_artifacts_dir`, `adversarial_convergence_score`, `adversarial_unavailable`, `t2_model_class_diversity`, `t2_vendor_diversity`, `t2_effective_diversity`, `calibrator_diversity` (:833-841).
- Load-bearing flags: `regression_present`, `unauthorized_deviation_present`, `user_decision_required` ("convergence < threshold AND no auto-route applies"), `needs_human_decision` (:851-858). `user_decision_required` is defined in terms of the debate's convergence score, so a script merge would have to define it anew.
- "Contract version is `v1.8.0`." (:895).

### 1.7 §9.2 telemetry (lines 940-989)

- Non-stable top-level keys (`wave_durations_ms` ... `references_extended_info_used`, :943-968) and a nested `telemetry:` block "Stage 2 panel fields ... nest them here, never at the top level of the contract" (:969) with 19 keys (:970-988), including `cluster_agreement` "telemetry only; never compared with the convergence thresholds" (:979) and `findings_block_compliance_rate` first-parse (:988).
- **Anomaly [STALE DOC candidate]:** the testability map row "Memory write optionality | `yaml_substring` | `telemetry memory_status`" (:1958) expects a `memory_status` telemetry key, but §9.2 lists no `memory_status` (it lists `memory_hits`, `memory_misses`, `memory_retention_actions`, :954-956). Scope slice 04 §0.12 reports shadow07 wrote a top-level `memory_status` that `panel_lint` rejects. So one part of SKILL.md asks for a key another part (and the lint) forbids. Checked against `panel_lint.TELEMETRY_FIELDS` in section 2.

Key Takeaways
- The protocol text forbids reflect from synthesizing its own merge (:837, :1780) and defines Wave 4 completion only by a debate artifact or a loud F2/F3 fallback (:714). A script merge (E2/E3 style `review merge` or an E1 `review cluster`-based merge) is therefore illegal under 1.8.0 for reflect, not merely undocumented. [E1]
- `--t2-engine panel` is reserved for "Stage 3" in text (:87, :319) but has no code; Stage 3 already carries written stable-adjacent effects (D3 `status: partial`) that would apply only then.
- `user_decision_required` and convergence routing (:703, :857) are defined on the debate's `convergence_score`; any merge replacement must supply an equivalent number or bump the contract.
- §9.2 vs testability map disagree on `memory_status` (:954-958 vs :1958).

---

## 2. `src/superclaude/cli/reflect/panel_lint.py` (366 lines) [E1]

Purpose: read-only lint of a panel-run output directory against frozen 1.8.0 (docstring :1-17). Imports `_LOAD_BEARING_BOOL_FIELDS` from `.contract` (:31). Public entry `lint_panel_contract(out_dir, legacy_contract)` (:302) returns failure lines; `ev1_failures(out_dir, contract, use_manifest=True)` (:236) is the EV-1 check reused by the Stage 2 aggregator with `use_manifest=False` (:239-242).

### 2.1 Constants

- `STABLE_FIELDS_1_8_0` (:33-144) and `TELEMETRY_FIELDS` (:146-174) are copied line by line from the SKILL.md §9.1/§9.2 YAML blocks by regex `^([a-z_0-9]+):` (`_KEY_LINE`, :187; `extract_field_list`, :192-197). [CODE-VERIFIED] `TELEMETRY_FIELDS` has no `memory_status`, which confirms the §1.7 anomaly: a contract following the testability map row at SKILL.md:1958 would fail L2.
- `LEGAL_MERGE_METHODS = ("adversarial", "single-reviewer-fallback")` (:184); `CONTRACT_VERSION = "1.8.0"` (:185). [CODE-VERIFIED] matches SKILL.md:837.
- `PARITY_FIELDS` = the four diversity fields + `reviewer_cards` (:177-183).

### 2.2 Assertions (`lint_panel_contract`, :302-366)

| Id | Rule | Lines |
|---|---|---|
| L0 | `return-contract.yaml` missing / unparseable / not a mapping -> single failure, stop | :305-309 |
| L1 | `contract_version != "1.8.0"` | :311-315 |
| L2 | any top-level key outside stable + telemetry + `telemetry`; `telemetry` must be a mapping. The CONTENTS of `telemetry:` are not checked | :316-325 |
| L3 | when Wave 4 ran (`tier_reached` is not the int 1; a missing tier counts as Wave 4), `merge_method` must be a legal value; for tier 1 it may be absent or legal | :326-334 |
| L4 | `adversarial_convergence_score` is a finite float or null | :335-339 |
| L5 | load-bearing bools are real bools; `adversarial_unavailable` and `regression_present` required when Wave 4 | :340-346 |
| L6 | EV-1 on disk (`_ev1`) when Wave 4 | :347-348, :246-299 |
| L7 | parity of the 5 `PARITY_FIELDS` with the matched legacy contract (`reviewer_cards` by basename) | :349-359 |
| B | bump rule: any L2 key violation or L3 failure adds "a new stable key or merge_method value needs a contract version bump, which this plan does not make" | :360-365 |

### 2.3 EV-1 in code (`_ev1`, :246-299) vs the SKILL.md text

- Required card count = `max(2, resolved)` where `resolved` = `len(reviewer_cards)` or, with `use_manifest`, `reviewers_resolved` from `panel/manifest.json` (:249-270). Cards counted by filename `reviewer-<N>-card.(yaml|yml|md)` in `reviewer-cards/` (:188, :219-227).
- Branch (a): `adversarial/merged-verdict.yaml` parses and `merge_method == "adversarial"` -> only the card count is checked (:271-278). [CODE-VERIFIED] matches SKILL.md:714(a).
- Branch (b): otherwise ALL three must hold: `adversarial_unavailable is True`, contract `merge_method == "single-reviewer-fallback"`, and an audit.log row matching `\bF[23]\b` (:282-298).
- **[CODE-CONTRADICTED] vs SKILL.md:714(b):** the protocol requires `merge_method == single-reviewer-fallback` only "when the F2 path was taken"; an F3-only run (`adversarial_unavailable: true`, F3 audit row, no single-reviewer verdict) satisfies the text but fails the lint because :290-291 demand `single-reviewer-fallback` unconditionally. The code is stricter than the doc.
- Limit stated in the docstring: the `--unattended` nested layout (`nested/adversarial-<n>/`, SKILL.md:701) is not covered; L6 reports `merged-verdict: absent` on such runs (:9-12). [CODE-VERIFIED: `_ev1` only reads `out / "adversarial" / "merged-verdict.yaml"`, :271]

Key Takeaways
- The bump rule is mechanical: any new `merge_method` value (e.g. a script-merge value) or new top-level key trips L3/L2 and B. A unified core that changes reflect's merge must ship a new contract version and a new lint constant set, not just new code. [E1]
- L2 does not inspect the nested `telemetry:` block, so all panel-only fields can be added there freely; that is the legal extension point under 1.8.0. [E1]
- The lint is stricter than the protocol on the F3 branch and blind to the `--unattended` layout; both are gaps a shared core must not copy blindly.

---

## 3. `src/superclaude/cli/reflect/contract.py` (420 lines): the wrapper consumer [E1]

Pure module, "the SINGLE place the verdict map, the FR-11 degradation routing, and `contract_version` gating live" (:1-13). `derive_verdict(contract, *, expected_tier, allow_single_vendor, child_rc, promoting=False)` (:138-260) orders blocked -> degraded -> halted -> pass.

- **Version gate:** missing version -> BLOCKED `contract-version-missing` (:179-186); `major != "1"` -> BLOCKED `unknown-major-version` (:187-194). [CODE-VERIFIED] Consequence: a contract 2.0.0 (the deferred "E'" design) blocks every wrapper run until `contract.py` changes; a 1.9.0 passes the version gate unchanged.
- **`merge_method` handling:** only `merge_method == "single-reviewer-fallback"` is read, as degraded trigger 10 (:294-296). There is no legal-values check. An unknown value (for example a hypothetical `script` or `panel`) is NOT rejected by the wrapper; such a run would reach PASS if the convergence score is a float >= 0.80 and no other trigger fires. [CODE-VERIFIED by reading :263-358] So the EV-2 "reject" rule lives only in SKILL.md and `panel_lint` L3, not in the consumer the hand-off treats as authoritative (SKILL.md:709 says consumers route on `merge_method` first; the wrapper does not).
- **Convergence:** T2 with null `adversarial_convergence_score` -> DEGRADED `null-convergence` (:298-300); a present score < 0.80, non-finite or non-numeric -> DEGRADED `low-convergence` (:317-326). This 0.80 floor is stricter than SKILL.md's 0.75 PASS band (:703). A script merge that emits no convergence score (as `review merge` / `review cluster` do not; `cluster_agreement` lives in telemetry) would DEGRADE every T2 run through trigger 11. [CODE-VERIFIED]
- Other degraded triggers that touch Tier 2: chain-critical `degraded_components` `{auggie, env-aliases, evidence-validator}` (:31-33, :274-275); `t2_model_class_diversity != full` (:282-284); `t2_vendor_diversity == single` unless allowed (:287-288); `adversarial_unavailable is True` (:291-292); `adversarial_subrun_status in (partial, failed)` (:306-307).
- **Load-bearing bools** `_LOAD_BEARING_BOOL_FIELDS` (:47-57): `regression_present`, `unauthorized_deviation_present`, `needs_human_decision`, `user_decision_required`, `adversarial_unavailable`, `input_drift_detected`, `verification_ran`; a present non-bool -> BLOCKED (:213-222). `panel_lint` reuses this set (L5).
- **Halted** (:361-382): `status` failed/partial, then `regression_present`, `unauthorized_deviation_present`, `needs_human_decision`, `user_decision_required`, then `deviation_count_by_class.regression > 0` or `drift > 0`. `classify_fix` (:385-420) maps to human-required / auto-fixable.
- **Anomaly:** `_make_result` and `_degraded_reason` read `verification_verified`, `reviewers_verified`, `regression_verified` (:132-134) and `adversarial_subrun_status` (:306), none of which is in `STABLE_FIELDS_1_8_0` or `TELEMETRY_FIELDS` (panel_lint.py:33-174). A producer that wrote them at top level would fail `panel_lint` L2 even though the wrapper reads them. Producer (checked in the Phase 3 fix cycle 1): `ensemble.py` writes all four at top level of its own version-"1.0" contract (`ensemble.py:793`, :814-816), and that contract is never linted; no skill-path producer writes them (section 8a). [CODE-VERIFIED]

Key Takeaways
- The wrapper's real routing inputs from Tier 2 are `adversarial_convergence_score` (float, >= 0.80), `merge_method == single-reviewer-fallback`, `adversarial_unavailable`, diversity enums and the four halting bools. Any replacement merge must produce those fields with the same meaning, or both the wrapper and the contract change. [E1]
- The wrapper does not enforce EV-2; a new `merge_method` value would leak through silently unless the score routing catches it. A unified design adding a value must add the legal-value check to `contract.py` in the same change. [E1]
- Major version 2 is hard-blocked (:187-194); a minor bump is the only bump the wrapper absorbs without code change.

---

## 4. `tests/cli/reflect/`: the pins a unified core must keep or migrate [E1]

Glob of `tests/cli/reflect/*` (2026-11-13) returns 40 entries: 38 `test_*.py` files plus `conftest.py` and `__init__.py`. The task prompt says "the twelve files"; that count does not match the directory. The panel/contract-relevant ones are `test_shadow_skill_contract.py`, `test_panel_contract_lint.py`, `test_shadow_exit_script.py`, `test_verdict_replay_script.py`, `test_reviewer_brief_constraints.py`, `test_reviewer_readonly_tools.py`, `test_reviewer_finding_parity.py`, `test_verdict_mapping.py`, `test_classify_fix.py`, `test_contract_fallback_metadata.py`, `test_contract_status_cli.py`, `test_isolate_reviewers_cli.py` (possibly the "twelve"; this list is my reading of file names, the others concern the wrapper runner, fallback slots, promotion and verify deny-lists). Only the first three were read in full ranges, the fourth by test names.

### 4.1 `test_shadow_skill_contract.py` (307 lines)

| Test | What it pins | Lines | Compares against |
|---|---|---|---|
| `test_stable_contract_block_and_version_are_byte_identical_to_head` | §9.1 YAML block of the working tree == §9.1 block of `git show HEAD:<SKILL.md>`; block contains `contract_version: "1.8.0"` | :42-49 | **HEAD** |
| `test_skill_changes_are_confined_to_the_allowed_sections` | every changed line in `git diff HEAD -U0` lies under `### 3.1 `, `### 4.3a `, `### 5.4 ` or `### 9.2 `; a §3.1 line must contain `--t2-engine`; nothing under §9.1 | :52-75 | **HEAD** (working-tree diff) |
| `test_no_new_src_superclaude_hit_in_the_skill_directory` | line count of `src/superclaude` in the skill dir <= count at HEAD | :78-98 | **HEAD** |
| `test_the_skills_manifest_recipe_runs_as_written` | manifest init/advance recipe of shadow steps runs | :104-140 | CLI |
| `test_the_brief_template_has_exactly_three_sections` | reviewer-spec has exactly `## T1 card excerpt`, `## Grounding hunks`, `## Coverage slice`; the findings-v2 / `reviewer_model_self_report` line sits inside the T1 excerpt; "legacy run's briefs do not carry this line" | :146-165 | text |
| `test_skill_names_the_card_header_fields_and_the_authority_of_the_legacy_path` | needles `persona:`, `model_class:`, `model:`, "unmodified output of `review panel resolve`", "authoritative and unchanged", `manifest advance`, `kept-ids.txt`, `judge_class_collision: unknown` | :168-180 | text |
| `test_the_calibrator_line_is_shadow_only_...` | literal calibrator line appears once; `cluster_cmd._embedded_calibration` parses its example | :183-196 | code [E1 kernel] |
| `test_the_reviewer_brief_line_carries_the_schema_and_its_example_parses` | brief line names every `findings.SEVERITIES`/`CATEGORIES` [E3 findings-v1 constants] and its example parses with `findings_v2.parse_block(lens="reflect-pre")` | :199-218 | code [E3][E1] |
| `test_shadow_steps_pin_the_header_model_the_verdict_file_and_the_first_pass_metric` | needles for step 2, 4, 7, 10 incl. "write `<output>/adversarial/merged-verdict.yaml`" and "every shadow field goes under `telemetry:`" | :221-238 | text |
| fixture parity tests | `recompute_parity` from `panel/resolution.json` + card headers via `panel.load_tiers()["classes"]` | :243-307 | code [E3 panel resolver] |

**C1/C6 HEAD risk [CODE-VERIFIED]:** :43 calls `git("show", f"HEAD:{SKILL_REL}")` and :53 calls `git("diff", "HEAD", ...)`. Both compare the working tree with the current commit. Once a change to §9.1 or to a forbidden section is committed, HEAD contains it and both tests pass again on the next run. They guard only uncommitted edits in one working session, not the contract across commits or branches. Both also `pytest.skip` when git history is absent (:44-45, :54-55), so in an sdist or shallow export they silently skip. The cross-commit guard for the contract's field set is `test_pinned_field_lists_match_skill_md` (section 4.2), which pins the constants to SKILL.md, but SKILL.md and the constants can be changed together in one commit; nothing compares with `master` or `origin/master`. The `merge_method` legal values are pinned only by `test_f2_merge_method_panel_fails` (section 4.2) against the constant, not against the SKILL.md text.

### 4.2 `test_panel_contract_lint.py` (409 lines)

- `test_pinned_field_lists_match_skill_md` (:90-104): `extract_field_list` of §9.1 and §9.2 equals the constants, in order. `test_constant_sizes_and_load_bearing_import` (:107-114): 110 stable, 27 telemetry; `LOAD_BEARING_BOOLS is contract._LOAD_BEARING_BOOL_FIELDS`. [CODE-VERIFIED]
- Pass cases P1-P10 (:120-170): P4 shows arbitrary keys nested under `telemetry:` pass (`panel_engine="shadow"`, :138); P7 null score passes the lint (the wrapper would DEGRADE it, section 3); P8 loud fallback passes (:159-161).
- `test_f1_extra_stable_key_is_named` (:176-181): a top-level `cluster_agreement` fails L2 + B. So moving `cluster_agreement` out of `telemetry:` is a bump.
- `test_f2_merge_method_panel_fails` (:184-190): `merge_method: "panel"` fails L3 + B. This is the pinned answer to "can Stage 3 write `merge_method: panel` under 1.8.0": no.
- `test_f3_f4_contract_version` (:193-201): `1.9.0` fails L1. So a minor bump also breaks the lint; the lint is 1.8.0-only by design.
- F12-F18 (:270-343) pin EV-1 card count, minimum 2, fallback without an audit row fails (F17), and "merged verdict with the fallback method is not enough" (F18).

### 4.3 `test_shadow_exit_script.py` (319 lines)

- Builds synthetic legacy runs from `tests/cli/reflect/fixtures/panel_lint_legacy` and shadow runs with a manifest built by `cli/review/manifest` (`mf.new_manifest`, `mf.advance_stage`, :77-92) [E1 kernel], resolution from `review panel resolve @reflect-pre` (:25-29) [E3 resolver + E1 template].
- Fixture shadow telemetry puts `reviewer_personas`, `reviewer_models`, `executor_class_resolved`, `panel_parity`, `cluster_agreement`, `findings_block_compliance_rate` inside `telemetry:` (:57-69).
- `test_ev1_failures_above_the_legacy_rate_fail` (:228-235): removing `adversarial/` from one of 20 runs gives `shadow 1/20 = 0.050; legacy baseline 0/3 = 0.000` and FAIL.
- `test_a_new_degraded_reason_in_the_verdict_replay_fails` (:238-244): `adversarial_unavailable=True` in a shadow run is a new degraded reason -> FAIL.
- `test_the_current_repository_reports_without_crashing` (:292-299): live-repo test accepts any documented exit code; it no longer asserts PASS. `EXIT == {"PASS": 0, "FAIL": 1, "INSUFFICIENT-RUNS": 3}`, 2 = usage (:302-310).
- `test_report_file_and_no_other_writes` (:313-319): the script writes only `--out`.

### 4.4 `test_verdict_replay_script.py` (190 lines, test names only)

Tests at :38-188 pin self-replay zero diffs, a new degraded reason exits non-zero, `test_derive_arguments_are_the_documented_ones` (:122), a lenient replay that finds reasons hidden behind single-vendor (:130), "writes nothing" (:173), and `test_recorded_runs_replay_against_themselves` (:188, live repo). Bodies not read: [UNVERIFIED] beyond names.

Key Takeaways
- C1 and C6 are HEAD-relative and skip without git history; they are working-session guards, not contract guards. A unified-core migration done in commits passes them trivially. A real guard needs a comparison with a fixed reference (a pinned hash of the §9.1 block in the test, or `git show origin/master:`), which does not exist today. [E1]
- The lint tests explicitly pin that `merge_method: panel` (F2) and `contract_version: 1.9.0` (F3) fail. Any Stage 3 merge replacement must rewrite these tests and the constants together with the contract text. [E1]
- Kernel coupling already exists in tests: reflect tests import `findings` (E3), `findings_v2`, `cluster_cmd`, `manifest` (E1 kernel) and `panel.load_tiers` (E3 resolver extended by E1). A shared core must keep these import paths or update reflect tests in the same change. [E1][E3]

---

## 5. Live Stage 2 exit status: full output of `uv run python scripts/reflect_shadow_exit.py` [E1]

Run on 2026-11-13 from the repository root (read-only; HEAD `792cf8c52`). Exit code **1** (FAIL; expected per the task, not a tool failure). Full output, verbatim:

```text
Stage 2 shadow-exit report

shadow runs counted: 13 of 20 required
  incomplete (not counted): pre-TASK-WF-detachTheCcsessi-20261102-034618-shadow02 (state clustered)
MALFORMED audit.log rows: 0 (must be 0)
EV-1 failure rate (len(reviewer_cards) rule, Wave 4 runs only): shadow 8/13 = 0.615; legacy baseline 3/39 = 0.077 (must be no higher)
parity assertion per run (recomputed):
  pre-TASK-WF-addTheSharedCode-20261111-193909-shadow04: FAILS (card model 'claude-gw-tier1b[1m]' differs from the resolved 'claude-sonnet-5-5')
  pre-TASK-WF-analyzeCodegraph-20261111-193557-shadow15: FAILS (the legacy rotation (reviewer_personas, reviewer_models) is not in the contract)
  pre-TASK-WF-authorizedNarrow-20261106-214325-shadow06: holds
  pre-TASK-WF-designOutput-20261111-193642-shadow14: holds
  pre-TASK-WF-detachTheCcsessi-20261102-034618-shadow03: holds
  pre-TASK-WF-devGuideFenceFix-20261104-204854-shadow12: holds
  pre-TASK-WF-fixIssue412SVeri-20261106-215543-shadow13: holds
  pre-TASK-WF-fixTheScIssueWor-20261104-162205-shadow05: FAILS (card model 'claude-gw-tier1b' differs from the resolved 'claude-sonnet-5-5'); recorded true but recomputed false
  pre-TASK-WF-implementFrOnb1O-20261023-180618-shadow10: holds
  pre-TASK-WF-implementIronbel-20261104-130647-shadow09: FAILS (card model 'claude-gw-tier1b[1m]' differs from the resolved 'claude-sonnet-5-5')
  pre-TASK-WF-implementTheDesi-20261031-182028-shadow11: holds
  pre-TASK-WF-planTheExplicitl-20261110-024937-shadow08: FAILS (card model 'claude-gw-tier1b[1m]' differs from the resolved 'claude-sonnet-5-5')
  pre-TASK-WF-renameTheScIssue-20261104-174359-shadow07: FAILS (the legacy rotation (reviewer_personas, reviewer_models) is not in the contract); recorded true but recomputed false
contract lint and manifest per run:
  pre-TASK-WF-addTheSharedCode-20261111-193909-shadow04: 1 problem(s)
    no contract
  pre-TASK-WF-analyzeCodegraph-20261111-193557-shadow15: 1 problem(s)
    L6 EV-1: reviewer-cards/ holds 0 card(s), fewer than the required 3 (reviewers_resolved from panel/manifest.json)
  pre-TASK-WF-authorizedNarrow-20261106-214325-shadow06: 1 problem(s)
    L6 EV-1: neither a merged adversarial verdict nor a loud fallback is on disk (merged-verdict: absent; fallback missing: adversarial_unavailable: true, merge_method: single-reviewer-fallback, audit.log F2/F3 row)
  pre-TASK-WF-designOutput-20261111-193642-shadow14: clean
  pre-TASK-WF-detachTheCcsessi-20261102-034618-shadow03: 1 problem(s)
    L6 EV-1: neither a merged adversarial verdict nor a loud fallback is on disk (merged-verdict: absent; fallback missing: adversarial_unavailable: true, merge_method: single-reviewer-fallback)
  pre-TASK-WF-devGuideFenceFix-20261104-204854-shadow12: clean
  pre-TASK-WF-fixIssue412SVeri-20261106-215543-shadow13: 2 problem(s)
    L2 stable keys: top-level key 'zero_drop_flag' is not in the 1.8.0 stable field list or the telemetry block
    B bump rule: the contract leaves 1.8.0 (1 stable-key violation(s), 0 EV-2 value violation(s)); a new stable key or merge_method value needs a contract version bump, which this plan does not make
  pre-TASK-WF-fixTheScIssueWor-20261104-162205-shadow05: 1 problem(s)
    L6 EV-1: neither a merged adversarial verdict nor a loud fallback is on disk (merged-verdict: absent; fallback missing: adversarial_unavailable: true, merge_method: single-reviewer-fallback)
  pre-TASK-WF-implementFrOnb1O-20261023-180618-shadow10: clean
  pre-TASK-WF-implementIronbel-20261104-130647-shadow09: 1 problem(s)
    no contract
  pre-TASK-WF-implementTheDesi-20261031-182028-shadow11: clean
  pre-TASK-WF-planTheExplicitl-20261110-024937-shadow08: 1 problem(s)
    no contract
  pre-TASK-WF-renameTheScIssue-20261104-174359-shadow07: 5 problem(s)
    L2 stable keys: top-level key 'memory_status' is not in the 1.8.0 stable field list or the telemetry block
    L2 stable keys: top-level key 'notes' is not in the 1.8.0 stable field list or the telemetry block
    L2 stable keys: top-level key 'zero_drop_flag' is not in the 1.8.0 stable field list or the telemetry block
    L6 EV-1: neither a merged adversarial verdict nor a loud fallback is on disk (merged-verdict: absent; fallback missing: adversarial_unavailable: true, merge_method: single-reviewer-fallback, audit.log F2/F3 row)
    B bump rule: the contract leaves 1.8.0 (3 stable-key violation(s), 0 EV-2 value violation(s)); a new stable key or merge_method value needs a contract version bump, which this plan does not make
verdict replay against the legacy baseline (42 runs): new degraded reasons 0

Stage 2 counts:
  2-of-3 shortfalls: 0
  unknown executor class (executor_class_resolved false): 9
  findings-block compliance rate (mean over 9 run(s)): 0.704
  cluster_agreement (9 run(s)): min 1.000, median 1.000, max 1.000

failure: EV-1 failure rate is higher than the legacy baseline
failure: pre-TASK-WF-addTheSharedCode-20261111-193909-shadow04: parity does not hold
failure: pre-TASK-WF-analyzeCodegraph-20261111-193557-shadow15: parity does not hold
failure: pre-TASK-WF-fixTheScIssueWor-20261104-162205-shadow05: parity does not hold
failure: pre-TASK-WF-implementIronbel-20261104-130647-shadow09: parity does not hold
failure: pre-TASK-WF-planTheExplicitl-20261110-024937-shadow08: parity does not hold
failure: pre-TASK-WF-renameTheScIssue-20261104-174359-shadow07: parity does not hold
failure: pre-TASK-WF-addTheSharedCode-20261111-193909-shadow04: lint or manifest problems
failure: pre-TASK-WF-analyzeCodegraph-20261111-193557-shadow15: lint or manifest problems
failure: pre-TASK-WF-authorizedNarrow-20261106-214325-shadow06: lint or manifest problems
failure: pre-TASK-WF-detachTheCcsessi-20261102-034618-shadow03: lint or manifest problems
failure: pre-TASK-WF-fixIssue412SVeri-20261106-215543-shadow13: lint or manifest problems
failure: pre-TASK-WF-fixTheScIssueWor-20261104-162205-shadow05: lint or manifest problems
failure: pre-TASK-WF-implementIronbel-20261104-130647-shadow09: lint or manifest problems
failure: pre-TASK-WF-planTheExplicitl-20261110-024937-shadow08: lint or manifest problems
failure: pre-TASK-WF-renameTheScIssue-20261104-174359-shadow07: lint or manifest problems
OVERALL: FAIL (shadow runs 13 of 20)
EXIT_CODE=1
```

### 5.1 Reading of the output (question 7)

- **Counted runs:** 13 of 20 required; shadow02 incomplete (manifest state `clustered`); shadow01 not listed at all (scope slice 04 §0.15: no `panel/manifest.json`).
- **Failing criteria (4 of 6):**
  1. EV-1 rate: shadow 8/13 = 0.615 vs legacy 3/39 = 0.077. This is the first time the head of the output (the EV-1 counts) is recorded; slice 04 §0.15 had only the tail.
  2. Parity: 6 runs fail. Four (04, 05, 08, 09) because the card `model:` header holds a gateway alias (`claude-gw-tier1b[1m]` / `claude-gw-tier1b`) rather than the pin `claude-sonnet-5-5`; two (07, 15) because the contract lacks `reviewer_personas`/`reviewer_models`. Both are the defects fixed in skill text by `9874d63fb`/`c2e3347d3` (scope slice 03 §1.1).
  3. Lint/manifest: 9 runs. 3 have no contract at all (04, 08, 09); 4 fail EV-1 placement (03, 05, 06, 07); 1 has zero `reviewer-cards/` (15); 2 carry top-level keys outside 1.8.0 (13: `zero_drop_flag`; 07: `memory_status`, `notes`, `zero_drop_flag`).
  4. (passing) MALFORMED audit rows 0; verdict replay new degraded reasons 0; 2-of-3 shortfalls 0.
- **Clean runs:** 10, 11, 12, 14 (lint clean and parity holds). That is 4 fully clean runs out of 13 counted.
- **Telemetry:** compliance mean 0.704 over 9 runs; `cluster_agreement` 1.000 min/median/max over 9 runs; executor class unknown in all 9 measured.
- Which runs predate the fix commits was not established from timestamps in this slice: [UNVERIFIED]. Run directory names carry the legacy package dates, not the shadow run time.

Key Takeaways
- Stage 2 exit is FAIL on count (13/20) and on three criteria; none of the failures is a merge-quality failure. All observed causes are orchestrator contract-writing or file-placement lapses (missing contract, header copied from the harness, `merged-verdict.yaml` not at the EV-1 path, extra top-level keys). [E1]
- The EV-1 rate jump (0.615 vs 0.077) means the gate catches placement, not debate absence; this matters for question 1 (section 8). [E1]

---

## 6. The two Stage 2 scripts [E1]

### 6.1 `scripts/reflect_shadow_exit.py` (410 lines)

- Imports `panel_lint` (reflect), `cli/review/manifest` and `cli/review/panel` (:50-52) and loads `reflect_verdict_replay.py` by path (:62-71). Reads files only; writes only `--out` (:4-5, :402-405). [CODE-VERIFIED]
- Shadow set: `<runs-root>/pre-*/panel/manifest.json` with `t2_engine_effective == "shadow"`; `published` counted, `failed` fails, others listed incomplete (:209-223). Legacy baseline = `rv.legacy_runs` (1.8.0 contracts without `panel/manifest.json`) (:251).
- `tele()` reads a non-stable field from `telemetry:` or, for older runs, the top level (:90-95). So the aggregator tolerates both placements while the lint (L2) rejects the top-level one for panel-only names.
- Parity recompute (:117-177): needs resolution, card headers whose `model` equals the resolved id (:148-152), and the contract's `reviewer_personas`/`reviewer_models` mapped to classes; a run frozen under another tier file hash is "not proven" (:128-132). Matches the failure reasons seen in section 5.
- Lint is called with the run's own contract as the "matched legacy" contract, so L7 parity is trivially equal (docstring :20-22, call :240). [CODE-VERIFIED] L7 therefore never fires in this aggregator.
- **EV-1 rate detail [CODE-VERIFIED]:** `"ev1_fail": wave4_ev1(run, contract) if contract else True` (:243). A run with no contract counts as an EV-1 failure. In section 5, 3 of the 8 shadow EV-1 failures (04, 08, 09) are "no contract", not a merge-file problem; the remaining 5 are 03, 05, 06, 07 (merged-verdict absent) and 15 (0 reviewer cards). The baseline uses `use_manifest=False` (count from `len(reviewer_cards)`) on both sides (:189-194).
- Overall: FAIL if any failure, else INSUFFICIENT-RUNS if fewer than `--required`, else PASS (:376-381); exit codes 0/1/3, 2 usage (:57, :398-400).

### 6.2 `scripts/reflect_verdict_replay.py` (184 lines)

- Legacy set: `pre-*` dirs with a `"1.8.0"` contract and no `panel/manifest.json` (:89-103). Replays each through `derive_verdict(expected_tier=2, child_rc=0, allow_single_vendor in (False, True))` (:55-59, :78-86).
- `compare` (:106-123): runs are paired by directory name. Shadow runs are named `...-shadowNN`, so in the Stage 2 aggregator they are never paired with a legacy run; a shadow `degraded` verdict counts as "new" only when its reason is absent from the set of reasons any legacy run ever had (:119-122). Blocked/halted shadow verdicts are not "new degraded" (docstring :32-34).
- Consequence: "new degraded reasons 0" (section 5) means shadow runs degrade only for reasons legacy runs also had; it does not show that shadow verdicts equal their legacy twins. A contract 1.9.0 or 2.0.0 run is skipped (:73-74), so a contract bump removes those runs from replay silently (they are listed as skipped, exit code unaffected). [CODE-VERIFIED]

Key Takeaways
- Both scripts are hard-bound to `"1.8.0"` (`VERSION`, `panel_lint.CONTRACT_VERSION`): a contract bump for a script merge needs new scripts or a version parameter; otherwise the Stage 2/3 evidence machinery goes blind to bumped runs. [E1]
- The verdict replay is a reason-set comparison, not a paired verdict comparison; a Stage 3 merge change would need a paired design (same input package, legacy vs panel) to show "no regression". [E1]
- The EV-1 rate counts missing contracts as EV-1 failures, which inflates the "merge gate" failure number; for the merge-path question only 5 of 13 runs fail on the merge artifacts themselves. [E1]

---

## 7. Recorded debate outputs vs `cluster_agreement` (model-behaviour evidence, runs dated 2026-10-23 to 2026-11-13 by directory listing; read 2026-11-13) [E1]

### 7.1 Why three "no contract" runs: unparseable YAML

The exit script reports "no contract" for shadow04, 08, 09, but each has a `return-contract.yaml`. Parsing with PyYAML (`uv run python -I`, read-only) fails in all three with `ParserError ... line 103, column 18, expected ',' or ']', but got '['`. Line 103 of shadow04 is `reviewer_models: [claude-gw-tier1b[1m], claude-gw-tier2[1m], claude-gw-tier1a[1m]]`: the gateway alias suffix `[1m]` inside an unquoted YAML flow list breaks the parse. So the "no contract" failures are one orchestrator YAML-quoting defect caused by gateway alias names, and the aggregator (`_yaml_map(...) or {}`, `reflect_shadow_exit.py:224`) turns them into lint + parity + EV-1 failures at once. This also means the contract consumer `contract.parse_contract` would return None and BLOCK these runs (`contract.py:76-79`).

### 7.2 Placement of `merged-verdict.yaml` and debate artifacts per run

From `ls` of each `adversarial/` dir and its nested `adversarial/adversarial/` (2026-11-13):

| Run | top `merged-verdict.yaml` | nested copy | sc-adversarial artifacts present (where) | contract `adversarial_convergence_score` | telemetry `cluster_agreement` | `judge_identity` (contract telemetry) |
|---|---|---|---|---|---|---|
| shadow01 | yes | - | nested dir (not listed) | 0.80 | null | unknown |
| shadow03 | no | yes | full set, nested | 0.90 | 1.0 | unknown |
| shadow04 | no (`.md` only) | - | full set, top | 1.0 | null | sonnet-class inline orchestrator |
| shadow05 | no (`.md` only) | - | full set + rounds, top | 1.0 | 1.0 | unknown |
| shadow06 | no (`.md` only at top) | yes | full set, nested | 1.0 | 1.0 | unknown |
| shadow07 | no | yes | full set, nested | 0.857 | 1.0 | unknown |
| shadow08 | no (`.md` only) | - | transcript + variants only, top | 1.0 | 1.0 | claude-gw-tier3[1m] |
| shadow09 | yes | - | **none** (only `merged-verdict.yaml`) | 0.93 | 0.933 | sonnet-class inline orchestrator |
| shadow10 | yes | - | full set, top | 1.0 | 1.0 | inline-orchestrator-sonnet |
| shadow11 | yes | yes | full set, top | 1.0 | 1.0 | orchestrator-inline; `debate_skipped_similar: true` |
| shadow12 | yes | - | transcript + base-selection, top | 1.0 | 1.0 | inline-orchestrator-gw-tier3 |
| shadow13 | yes | - | full set (no probe), top | 1.0 | 1.0 | orchestrator-inline |
| shadow14 | yes | - | full set, top | 0.96 | 1.0 | claude-gw-tier3[1m] |
| shadow15 | yes | - | full set nested; `merged-output.md` top | 1.0 | (absent) | unknown (note in verdict file) |

(Values from `grep` of each `return-contract.yaml` and `merged-verdict.yaml`; shadow02 has no contract and is not counted.)

### 7.3 Three `merged-verdict.yaml` files read

- **shadow09** (`.dev/reflect/pre-TASK-WF-implementIronbel-20261104-130647-shadow09/adversarial/merged-verdict.yaml`): `merge_method: adversarial  # inline Mode-A merge per series convention (sc-adversarial return contract names no separate judge)`; `judge_identity: sonnet-class inline orchestrator`; `judge_class_collision: true`; `convergence_score: 0.93  # cluster agreement 0.933; 3/3 unanimity on C1-C3; PASS (>= 0.75)`; five merged findings C1-C5 with `finding_ids` across reviewers, `agreement 3/3` or `2/3`, `calibrated_mean`. No debate transcript, diff analysis or base selection exists in that `adversarial/` dir. The convergence score written into the verdict is the `review cluster` agreement, rounded.
- **shadow12** (`...devGuideFenceFix...-shadow12/adversarial/merged-verdict.yaml`): `merge_method: adversarial`, `convergence_score: 1.0`, `status: success`, `base_variant: reviewer-2 (qa)`, `judge_identity: "inline-orchestrator-gw-tier3 (distinct from all three debater classes ...)"`, `unresolved_conflicts: 0`, `findings: []`.
- **shadow13** (`...fixIssue412SVeri...-shadow13/adversarial/merged-verdict.yaml`): `merge_method: adversarial`, `convergence_score: 1.00`, `base_variant: reviewer-1-card.md (sonnet:analyzer)`, `debate_skipped_similar: false`, findings M-001..M-003 all MINOR with `citations` in findings-v2 shape (`role`, `path`, `line_start`, `line_end`), per-finding `calibrated`, `reviewers`, plus `advisories`. One citation uses `role: evidence`, which is not a findings-v2 role (`findings_v2.py:35` roles per slice 03 §3.2: plan, spec, source, test, diff, artifact).
- shadow11's verdict and contract carry `debate_skipped_similar: true  # FR-006 similarity clause; panel cluster_agreement=1.0`.

### 7.4 What sc-adversarial actually returns (installed `~/.claude/skills/sc-adversarial-protocol/SKILL.md`, 2991 lines, Mode A summary)

- Mode A: `--compare` of 2-10 existing files, copied to `variant-N-original.md` (:55-63). Five steps: diff analysis, debate, hybrid scoring + base selection, refactoring plan, merge (:80-330). Artifacts: `diff-analysis.md`, `debate-transcript.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md`, `return-contract.yaml` (:371-386). `variants_too_similar` (<10% diff) skips the debate (:407-410).
- Return contract (:436-448): `merged_output_path`, `convergence_score`, `artifacts_dir`, `status`, `base_variant`, `unresolved_conflicts`, `fallback_mode`, `failure_stage`, `invocation_method`, `unaddressed_invariants`. **It has no `merge_method` field, no judge identity, and it writes no `merged-verdict.yaml`.** [CODE-VERIFIED against the installed skill text; this is a skill, so "code" here is the installed protocol file]
- Agent delegation names a `debate-orchestrator` agent, `merge-executor` agent and dynamic advocate agents (:467-489). Whether a Skill-tool invocation from inside the reflect session actually spawns these agents or runs the steps in the orchestrator's own context is not stated in the read ranges: [UNVERIFIED]. The recorded `judge_identity` values "inline orchestrator" in 6 of 14 runs (04, 09, 10, 11, 12, 13) show that in practice the reflect orchestrator itself acted as judge.

### 7.5 Consequences for EV-1

- `merged-verdict.yaml` and its `merge_method: adversarial` are written by the reflect orchestrator in shadow step 7 (SKILL.md:346), not by sc-adversarial (whose contract has no such field). EV-1 says the orchestrator must read disk "NOT a self-written field" (SKILL.md:714), but the file it reads is one the same orchestrator writes. EV-1 therefore proves file placement, not that a debate ran. [CODE-VERIFIED by comparing SKILL.md:346, :714 with sc-adversarial :436-448]
- shadow09 is a concrete case: no debate artifacts at all, an inline merge whose convergence is the cluster agreement, and a verdict file saying `merge_method: adversarial`. Had its contract parsed, `panel_lint` L6 would have passed it (branch (a) only checks the verdict field and the card count, `panel_lint.py:271-278`). EV-2 ("an in-context 'convergence' of the cards is MALFORMED", SKILL.md:837) is violated in substance and undetectable by the lint.
- shadow09 and shadow11 also leak `cluster_agreement` into the merge path (as the convergence value, and as the reason to skip the debate), which step 6 forbids ("never compared with the convergence thresholds, never routes anything", SKILL.md:345).

Key Takeaways
- In recorded runs, the debate's `convergence_score` is 1.0 in 9 of 14 runs and `cluster_agreement` is 1.0 in 10 of 11 runs that record it; where they differ (03: 0.90 vs 1.0, 07: 0.857 vs 1.0, 14: 0.96 vs 1.0) the debate is the lower one, and in 09 the debate number is a copy of the cluster number. With this little variance neither number discriminates; the comparison does not show the debate adding verdict information over the script. [E1]
- At least 6 of 14 recorded "adversarial" merges were judged inline by the orchestrator, and 1 (shadow09) had no debate artifacts at all. The debate path is less independent in practice than the contract implies. [E1]
- EV-1 is a placement check on an orchestrator-written file; it cannot tell debate from inline merge. Any unified design that keeps the debate needs sc-adversarial (or a script) to write the verdict file and its `merge_method` itself, or EV-1 stays self-attested. [E1]

---

## 8. UC-2 `reflect-post` readiness (question 6) [E1]

| Piece | State | Evidence |
|---|---|---|
| Panel templates | Exist: `review-panel.reflect-post.json` and `-post-x2.json` in `src/superclaude/cli/review/data/`. `reflect-post` is t1b fixed + t4 random + t1a random, `distinct_across_slots: true`, description "mirrors reflect-pre" | `ls` + file read [CODE-VERIFIED] |
| Template rules | `validate_reflect_profile` applies to any `reflect-*` template: no Fable, no tier0, max 3 reviewers (`_REFLECT_PREFIX = "reflect-"`, `_REFLECT_MAX_REVIEWERS = 3`) | `panel.py:71-73, :80-132, :137-150` [CODE-VERIFIED] |
| Skill path | SKILL.md: "In UC-2 (post-execution) runs the flag is accepted and ignored until Stage 5" | SKILL.md:311 (protocol rule; no code exists to route it) |
| Parser | `findings_v2.check_finding`: lens `reflect-post` requires `deviation_class` in `authorized, necessary, drift, regression, none` (:147-153); `reflect_category: deviation` also needs it (:163-164); with `reflect_category` set, `blocking` must equal `severity != MINOR` (:161-162) | [CODE-VERIFIED] |
| Reviewer brief | the only findings-v2 instruction line (`refs/reviewer-spec.md:39`) hard-codes `lens "reflect-pre"` and is appended only in shadow (UC-1) runs; there is no `reflect-post` brief line | grep of :39 [CODE-VERIFIED] |
| Reviewer output | `reflect-reviewer` returns a markdown Deviations table (`# / Category / Location / What diverged / Evidence (file:line) / Severity`), HIGH/MEDIUM/LOW, Adherence summary, and an advisory "Correctness gaps" table that "NEVER auto-gates" and must not set `regression_present` or force `status: partial` | `agents/reflect-reviewer.md:69-115` [CODE-VERIFIED] |
| Recorded post runs | 48 `.dev/reflect/post-*` dirs; 0 reviewer-card files contain `Findings block` | `ls` / `grep -rl` 2026-11-13 |

Gap between findings-v2 `reflect-post` and what the reviewer returns:
1. No findings-v2 block at all in UC-2; the agent's format is a table, and the brief line is reflect-pre only.
2. Category names: the agent uses `Authorized expansion` / `Necessary deviation` / `Drift` / `Regression` (agent :21-26, :93), findings-v2 needs the lowercase single words; slice 03 §3.3 records that `card_convert` matches only single words, so the two-word labels get no `deviation_class` (and under lens `reflect-post` a line without it is rejected).
3. Severity: HIGH/MEDIUM/LOW vs CRITICAL/MAJOR/MINOR + `blocking`. MEDIUM is "unjustified drift with real impact" (agent :71), which the contract treats as halting (`unauthorized_deviation_present`, `deviation_count_by_class.drift > 0` -> `_halted_reason` "drift", `contract.py:371-381`), but the converter maps MEDIUM to non-blocking MINOR (slice 03 §3.3). A `reflect-post` blocking rule per class (Regression, unjustified Drift blocking; authorized/necessary/none and `channel: advisory` never) is not written anywhere in code.
4. Advisory correctness gaps map to `channel: advisory`, but `check_finding` does not force `blocking: false` for that channel (:184-186 only checks the enum). [CODE-VERIFIED]
5. UC-2 uses further contract fields (`deviation_count_by_class`, `per_task_verdicts[].deviation_class`, reachability, runtime-surface; SKILL.md:753-810, :860-867) that no panel kernel output produces.

Key Takeaways
- UC-2 has data (templates, parser lens) but no producer: no brief line, no reviewer format, no blocking rule, no recorded post card with a findings block. "Templates exist" is not readiness. [E1]
- A unified core's `reflect-post` module needs: a reviewer instruction (or agent change) that emits findings-v2 with `deviation_class`, a per-class blocking rule matching `contract.py`'s halting rules, and a mapping from findings to `deviation_count_by_class` / `per_task_verdicts`. [E1]
- Scope correction (Phase 3 fix cycle 1): the "no producer" finding above holds for the **skill path** only. A code-driven UC-2 producer exists and is what the blocking sc:tasklist post gate runs: `superclaude reflect run` -> `ensemble.py` (section 8a). [E1]

---

## 8a. The code-driven Tier 2 engine behind `superclaude reflect run` (`ensemble.py`): second UC-2 producer, third merge path [E1]

Added in the Phase 3 fix cycle 1 from the gap-fill file `research/13-gap-fill-reflect-ensemble.md` (read in full); every line number below was re-read in source by the fixer on 2026-11-13. Provenance: `ensemble.py`, `runner.py`, `contract.py`, `commands.py` and `config.py` are identical to `origin/master` (file 13 §1.7), so this engine is master-baseline code that predates the E1 shadow work; it is tagged [E1] because it is reflect code, not because E1 wrote it.

**Route.** The CLI accepts only `--depth standard|deep` (`src/superclaude/cli/reflect/commands.py:253-258`). `ReflectRunner._audit_once` sets `expected_tier = 2` for both (`runner.py:538`) and, in production, calls `run_tier2_ensemble(config)` and then `rc = 0` unconditionally (`runner.py:540-545`). So the tasklist post gate (`sc-tasklist-protocol/SKILL.md:1157-1165`, `--depth deep`) never runs the `/sc:reflect` skill, its 1.8.0 contract, `panel_lint` or the shadow kernel. [CODE-VERIFIED]

**Merge path (the third one).** Reviewers are in-process swarm transport calls over the external `T2Model0N` model pool (`ensemble.py:154-182`, :340-348), the swarm "merge" is a verbatim concatenation (`swarm/merge.py:1-29`, per file 13 §5.2), and a `/sc:adversarial` child is run only to obtain `convergence_score`, `report_path` and `status` (`ensemble.py:554-561`). No calibration, evidence validation, clustering or reviewer-card file exists in this engine (file 13 §1.5; `panel_lint|cli.review|executor_model` have 0 matches in `ensemble.py`, Grep 2026-11-13). It shares only the `/sc:adversarial` skill (as a black-box child) and the `contract.py` verdict map with the skill path, and no code with E3's `src/superclaude/cli/review/` (file 13 §5.2). So reflect has three merge paths, not two: (1) skill Mode A debate under contract 1.8.0, (2) E3 `review merge` ledger, (3) this engine. [CODE-VERIFIED]

**`merge_method` and clean defaults.** `merge_method = "adversarial" if reviewer_count >= 2 else "single-reviewer-fallback"` (`ensemble.py:773`) depends only on the number of successful reviewers: it stays `adversarial` when the adversarial child exits non-zero (`ensemble.py:554-555` returns `None`) or writes no contract, and `adversarial_unavailable` is never set by the runner (`runner.py:544` passes no kwarg). The verdict still DEGRADES via `null-convergence` (`contract.py:299-300`), so the label is false but no false PASS follows from it today. The deviation fields default to clean when no seam ran or the child failed (`ensemble.py:442-471`), and the production scorer never fills them (`ensemble.py:557-561` sets only score, report path, status); `status: "success"` is a literal (`ensemble.py:789`). Consequence: no ensemble contract can reach HALTED (exit 10); reviewer findings never reach the verdict (file 13 §3.2, defect D1). [CODE-VERIFIED]

**Contract writer.** `_emit_reflect_contract` (`ensemble.py:886-895`, called at :510) writes `<output>/return-contract.yaml` with `yaml.safe_dump`, version `REFLECT_CONTRACT_VERSION = "1.0"` (`ensemble.py:74`), 33 keys (file 13 §4.2), including `adversarial_subrun_status` (:793), `verification_verified` and `regression_verified` (always `False`, :814, :816) and `reviewers_verified` (:815). This answers the open question of section 3 / Gaps: these four wrapper-read keys (`contract.py:132-134`, :306) are written by ensemble.py, and 11 of its keys are in neither `panel_lint` list (file 13 §4.3). Two incompatible "reflect contracts" (skill 1.8.0, agent-written and linted; engine 1.0, code-written and not linted) share one file name and one reader. [CODE-VERIFIED]

**C1-C16 for this caller** (from file 13 §9.2; this file's table in section 9): C2 and C4 would fail if the skill-path lint were applied (11 extra keys; `t2-adversarial/`, `t2-swarm/` instead of `adversarial/merged-verdict.yaml` and `reviewer-cards/`, `ensemble.py:81-82`); C5 does not describe this path (it is already a UC-2 Tier 2); C11 conflicts (`--reviewers` clamps to 2..4, `config.py:335`); C12 conflicts (the engine launches proxy models directly); C16 is moot (trigger 10 is unreachable for ensemble contracts because trigger 6 `degraded-tier1` fires first at 1 reviewer); C6-C9 and C14 do not apply (no skill text or `reflect-reviewer` involved).

**What a unified Review Panel must keep unchanged for this caller:** the gate command line `superclaude reflect run <phase file> --depth deep --fix --no-promote --base <sha> --output <dir>` (`sc-tasklist-protocol/SKILL.md:1157-1163`); exit codes pass 0 / halted 10 / degraded 11 / blocked 2 (`models.py:39-49`) and the `.reflect-exitcode` sentinel; the output files `<output>/return-contract.yaml`, `<output>/wrapper-result.yaml` and the `reflect_post:` frontmatter block (`runner.py:136-268`); and the contract keys read by `contract.py` (`:113-134`, `:263-382`) and by the gate (`SKILL.md:1171`). File 13 §9.1 lists them.

Key Takeaways
- [E1] The UC-2 producer for the blocking tasklist post gate is `ensemble.py`, not the skill; it is a third, independent merge path that shares only the `/sc:adversarial` child and `contract.py` with the skill path.
- [E1] Its `merge_method` is a reviewer-count label (`ensemble.py:773`) and its deviation flags default to clean (`ensemble.py:442-471`), so the gate can PASS, DEGRADE or BLOCK but never HALT on a found deviation.
- [E1] A unified core that takes over reflect must handle two contract writers (skill 1.8.0, engine 1.0) and resolve the C5/C11/C12 conflicts for this caller.

---

## 9. Constraints C1-C16 re-verified (question 4) [E1 unless tagged]

Constraint list from `research/scope/03-reflect-side.md:183-200`; each re-checked in this slice.

| # | Constraint | Status | What it blocks in a unified design |
|---|---|---|---|
| C1 | §9.1 block byte-identical, `contract_version: "1.8.0"` | CODE-VERIFIED (`test_shadow_skill_contract.py:42-49`), but HEAD-relative (section 4.1) | Any edit to §9.1 in a working tree; does NOT block a committed change |
| C2 | No top-level key outside 110 stable + 27 telemetry; panel fields under `telemetry:` | CODE-VERIFIED (`panel_lint.py:316-325`, `test_panel_contract_lint.py:90-114, :176-181`) | Promoting any panel field (e.g. `cluster_agreement`) to a stable/top-level field without a bump. Nested `telemetry:` contents are unchecked, so that is the free extension point |
| C3 | `merge_method` exactly `adversarial` / `single-reviewer-fallback`; new value = version bump | CODE-VERIFIED in lint (`panel_lint.py:184, :326-334, :360-365`; `test_f2_merge_method_panel_fails` :184-190). NOT enforced in the wrapper (`contract.py` only reads `single-reviewer-fallback`, :294-296) | A script merge labelled honestly; a minor bump also fails the lint (`test_f3_f4`, :193-201); a major bump BLOCKS the wrapper (`contract.py:187-194`) |
| C4 | EV-1 completion: verdict file + cards, or corroborated loud fallback | CODE-VERIFIED (`panel_lint.py:246-299`); lint stricter than text on F3 (section 2.3) | Any merge that does not leave `adversarial/merged-verdict.yaml` with `merge_method: adversarial` at the interactive path |
| C5 | Legacy default and authoritative; panel never called under legacy; shadow UC-1 only until Stage 5 | Protocol rule (SKILL.md:87, :311, :338); no code path exists to violate it ([CODE-VERIFIED by absence]: no `t2-engine` parser in `cli/reflect`, slice 04 §0.16) | Making the shared core authoritative for reflect before Stage 3; any UC-2 panel before Stage 5. Scope: C5 describes the skill path only; the UC-2 Tier 2 that the tasklist post gate runs is the code engine `ensemble.py` (`runner.py:538-545`, section 8a), which C5 does not govern [CODE-VERIFIED] |
| C6 | Working-tree SKILL.md diff only in §3.1 (with `--t2-engine`), §4.3a, §5.4, §9.2 | CODE-VERIFIED (`test_shadow_skill_contract.py:52-75`), HEAD-relative | Uncommitted edits to §7.1, §8, §11.3 etc. A unified design must edit or retire this test in the same change |
| C7 | Brief exactly three sections; shadow line inside T1 excerpt | CODE-VERIFIED (`test_shadow_skill_contract.py:146-165`) | Adding a fourth brief section (e.g. a `{{CANDIDATE}}`/driving-document section from E2/E3) without changing the test [E1][E2] |
| C8 | Shadow text needles pinned | CODE-VERIFIED (`test_shadow_skill_contract.py:168-238`) | Rewording shadow steps 2, 4, 5, 7, 10 in a shared recipe |
| C9 | `reflect-reviewer` mutator-free tools; named in both rotation tables | CODE-VERIFIED by test names (`test_reviewer_readonly_tools.py:69-106`; `test_reviewer_brief_constraints.py:35-58`); bodies not read | Replacing `reflect-reviewer` with a generic reviewer without keeping the allowlist and the two name mentions |
| C10 | Zero new degraded reasons vs legacy; 20 clean shadow runs | CODE-VERIFIED (`reflect_verdict_replay.py:106-123, :180`; `reflect_shadow_exit.py:376-381`); live: 0 new reasons, FAIL 13/20 (section 5) | Stage 3 entry until 20 clean runs; the replay is reason-set only (section 6.2) |
| C11 | Reflect templates: no Fable, no tier0, max 3 reviewers | CODE-VERIFIED (`panel.py:71-150`) | Shared templates that put Fable or tier0 in a reflect slot, or 4+ reviewers [E1][E3] |
| C12 | Only `anthropic-only` can launch; `gateway` has `launch: {}` | CODE-VERIFIED (`review-tiers.default.json:25-35`) | Any gateway-launched reflect panel (all D4 fallback) [E3 tier file] |
| C13 | `src/superclaude/` is source of truth; `.claude/` never staged | Project CLAUDE.md rule (not code) [UNVERIFIED as code; enforced by `make verify-sync` per CLAUDE.md, not read] | Editing installed copies instead of `src/` |
| C14 | No `src/superclaude/...` paths in installed primitives; skill dir gains no new hits | CODE-VERIFIED (`test_shadow_skill_contract.py:78-98`), HEAD-relative | A shared-core recipe that names `src/superclaude/cli/review/...` in reflect's skill dir |
| C15 | Reviewers read-only; no live-exec in briefs | CODE-VERIFIED via C9 tests (names only) and agent text (`reflect-reviewer.md` tools line per slice 03) | A shared reviewer runner that grants Bash/Edit (E2's `claude -p` with Edit/Write disallowed is compatible) [E1][E2] |
| C16 | Consumers route on `merge_method` first (wrapper, sprint, promotion gate) | Partly CONTRADICTED: the wrapper `derive_verdict` routes on `merge_method` only for `single-reviewer-fallback` (trigger 10, `contract.py:294-296`), after diversity and `adversarial_unavailable`; it never checks legal values. For `ensemble.py` contracts trigger 10 is unreachable (1 reviewer sets `tier_reached: 1`, so trigger 6 fires first; `ensemble.py:772-773`, `contract.py:278-279`, section 8a). Sprint and promotion-gate code not read [UNVERIFIED] | Changing `merge_method` values or `convergence_score` semantics without updating `contract.py` triggers 10, 11, 11b |

Key Takeaways
- 12 of 16 constraints are code-backed; C13 is a process rule, C5 is protocol-only (no code exists to break it), C16 is partly contradicted by the wrapper code.
- The constraints that actually decide the merge question are C3 (lint + bump), C4 (EV-1 file), C16 (wrapper's convergence routing) and C10 (Stage 2 exit). C1/C6/C14 are weaker than they look because they compare against HEAD.

---

## 10. Answers to the eight questions

**Q1. Debate merge (sc-adversarial Mode A) vs script merge for reflect Stage 3.** [E1][E3]
- Contract position: under 1.8.0 a script merge is illegal for reflect ("Reflect MUST NOT synthesize its own merge", SKILL.md:837; EV-1 needs `merge_method: adversarial`, :714; lint L3/B, `panel_lint.py:326-334, :360-365`). Keeping the debate needs no bump; replacing it needs a new `merge_method` value and a contract bump (C3).
- Recorded evidence (section 7): convergence 1.0 in 9 of 14 runs, `cluster_agreement` 1.0 in 10 of 11; where they differ the debate is lower by 0.04-0.14 (03, 07, 14); in 09 the debate number is the cluster number. 6 of 14 merges were judged inline by the orchestrator, one with no debate artifacts. No run has ground truth, so neither merge's accuracy is measured (slice 04 §0.14: the combo runs were not scored blind either).
- What this means: the recorded data cannot show that the debate adds verdict information over `review cluster`; it also cannot show the script is as good, because the cluster number never varied. The debate does produce outputs the contract consumes and the script does not: a `convergence_score` routed by the wrapper (<0.80 DEGRADED, `contract.py:317-326`), `base_variant`, and a merged findings list. `review cluster` produces `cluster_agreement` (telemetry only). The E3 deterministic `review merge` (any-blocking => FAIL, per hand-off §5.1; `ledger.py`/`findings.py` lines UNVERIFIED here) produces a PASS/FAIL verdict and a ledger, also with no convergence score.
- Basis for the report (not a decision): (a) Stage 3 "keep the debate as judge; use the shared core for resolution, cards, clustering, citation pre-check and calibration coverage" stays inside 1.8.0 and matches the E1 design decision (MR via slice 04 §4.1, [UNVERIFIED] re-read); (b) a script merge needs a defined replacement for `convergence_score` and `user_decision_required`, new wrapper logic, a new `merge_method` value and a paired (not reason-set) evidence run. Either way, EV-1 should check a file written by the merge step itself, not by the orchestrator (section 7.5).
- Scope: Q1 above compares the two merges of the **skill path** and E3. A third merge path is live in code: `superclaude reflect run` -> `ensemble.py` (swarm fan-out over `T2Model0N` models, verbatim concat, score-only `/sc:adversarial` child, `merge_method` from reviewer count alone at `ensemble.py:773`), which the blocking tasklist post gate uses (section 8a). Any Stage 3 merge decision must state whether it also covers this path. [E1] [CODE-VERIFIED]

**Q2. Legal `merge_method` values and the bump rule (C3).** Exactly `adversarial` and `single-reviewer-fallback` (SKILL.md:837, :1780; `panel_lint.LEGAL_MERGE_METHODS`, :184). Any other value fails L3 and adds the B line "a new stable key or merge_method value needs a contract version bump" (`panel_lint.py:360-365`), pinned by `test_f2_merge_method_panel_fails` with the value `panel` (`test_panel_contract_lint.py:184-190`). The lint also rejects any version other than 1.8.0 (`:311-315`, pinned at `:193-201`), so a bump needs new lint constants. The wrapper accepts any `1.x` (`contract.py:187-194`) and does not check `merge_method` values. History: rule tightening (EV-1, EV-2) was added in 1.7.x with "no stable-field change" (SKILL.md:727); field and value additions have always been bumps.

**Q3. EV-1 completion rule and loud fallback (C4).** Sections 1.5 and 2.3. Text: (a) verdict file with `merge_method: adversarial` + `reviewer-cards/` count >= resolved reviewers (min 2), or (b) `adversarial_unavailable: true` + audit F2/F3 row (+ `single-reviewer-fallback` when F2). On failure: MALFORMED audit row, up to 2 re-runs of Waves 3-4 or F2/F3, HALT only after that (SKILL.md:714). Code: the same, but (b) always demands `single-reviewer-fallback` (stricter on F3), and the `--unattended` nested layout is not covered (`panel_lint.py:9-12, :271`). Loud fallback: F1 retry, F2 single-reviewer verdict, F3 `adversarial_unavailable` + `status: partial`, "loud, never silent" (SKILL.md:353-359); the wrapper DEGRADES both F2 and F3 (`contract.py:291-296`).

**Q4. C1-C16.** Section 9.

**Q5. C1 and C6 compare against HEAD.** CODE-VERIFIED (`test_shadow_skill_contract.py:43`, `:53`). Risk: a unified-core refactor committed in steps passes both pins after each commit; a branch rebased onto master gets no comparison with master; with no git history both skip (`:44-45`, `:54-55`). The only cross-commit contract pin is constants-vs-SKILL.md (`test_pinned_field_lists_match_skill_md`), which a single commit changing both sides also passes. C14 has the same weakness (`:78-98`). A replacement would pin a hash of the §9.1 block, or compare with `origin/master`.

**Q6. UC-2 `reflect-post` readiness.** Section 8: on the skill path, templates and the parser lens exist; the brief line, reviewer output format, blocking rule and recorded data do not. On the code path, a UC-2 producer already runs: `superclaude reflect run` -> `ensemble.py` writes the post contract and `runner.write_reflect_post` writes the `reflect_post:` block (`runner.py:136-204`), but its deviation flags are clean defaults, so it cannot HALT on a found deviation (section 8a). [E1]

**Q7. Stage 2 exit status.** Section 5: FAIL, exit 1, 13 of 20 counted (shadow02 incomplete); EV-1 rate 8/13 = 0.615 vs legacy 3/39 = 0.077; parity fails in 6, lint/manifest in 9; 0 MALFORMED rows; 0 new degraded reasons; compliance 0.704 (9 runs); `cluster_agreement` 1.000 (9 runs); 4 fully clean runs (10, 11, 12, 14). Causes: 3 unparseable contracts (`[1m]` in an unquoted YAML list, section 7.1), header model copied from the harness, `merged-verdict.yaml` at the nested path or only as `.md`, missing `reviewer_personas`/`reviewer_models`, extra top-level keys.

**Q8. What a thin reflect module on a shared core must keep byte-identical (or behaviour-identical) while contract 1.8.0 stands.**
1. The §9.1 YAML block and `contract_version: "1.8.0"` (SKILL.md:724-893), and the 110 + 27 key lists derived from §9.1/§9.2 (`panel_lint.py:33-174`), in order.
2. The `merge_method` legal values and the EV-2 sentence (SKILL.md:837, :1780), and `LEGAL_MERGE_METHODS` (`panel_lint.py:184`).
3. The EV-1 on-disk contract: path `<output>/adversarial/merged-verdict.yaml`, field `merge_method: adversarial`, card names `reviewer-cards/reviewer-<N>-card.(yaml|yml|md)` and the min-2 count (`panel_lint.py:188, :246-299`; SKILL.md:714, :1955).
4. The sc-adversarial call shape and the `artifacts_dir` -> `adversarial_artifacts_dir` rename (SKILL.md:693-705).
5. Wrapper semantics in `contract.py`: the major-`1` version gate, the trigger order in `_degraded_reason` (especially 9, 10, 11 and 11b with the 0.80 floor) and `_halted_reason` (:138-382); `_LOAD_BEARING_BOOL_FIELDS` (:47-57), shared with the lint.
6. Panel-only fields only under `telemetry:` with the §9.2 names (SKILL.md:969-988).
7. The brief template's three sections and the shadow line text (C7, C8); the `reflect-reviewer` tools line and its name in both rotation tables (C9).
8. The reflect template guards in the shared resolver (`panel.py:71-150`) and the `@reflect-*` template ids used by SKILL.md:340 and the tests.
9. For the code-driven caller (`superclaude reflect run`, used by the tasklist post gate): the command line, exit codes 0/10/11/2 (`models.py:39-49`), `<output>/return-contract.yaml`, `<output>/wrapper-result.yaml` and the `reflect_post:` block (`runner.py:136-268`), and the contract keys `contract.py` reads (`:113-134`, `:263-382`), including the four keys only `ensemble.py` writes (`adversarial_subrun_status`, `verification_verified`, `reviewers_verified`, `regression_verified`; `ensemble.py:793`, :814-816). Section 8a.
What can move into a shared core without touching these: resolution, manifest, clustering, citation pre-check and calibration-coverage code (all telemetry under 1.8.0), provided the reflect tests' imports (`findings`, `findings_v2`, `cluster_cmd._embedded_calibration`, `manifest`, `panel.load_tiers`) keep resolving.

Key Takeaways
- Under 1.8.0 the shared core can own everything except the merge decision and the contract writer; the merge is pinned to the debate by text, lint and EV-1. There are two contract writers, not one: the skill's agent-written 1.8.0 contract and `ensemble.py`'s code-written 1.0 contract (`ensemble.py:74`, :886-895), the latter outside the lint (section 8a). [E1]
- The recorded runs do not justify replacing the debate on quality grounds, and they do not show the debate is better; they do show that EV-1 and the debate label are self-attested by the orchestrator.

---

## Gaps and Questions

- [UNVERIFIED] Sprint `executor.py` null-convergence routing and the §14.5.2 promotion-gate code (SKILL.md:707-712); not read.
- [CODE-CONTRADICTED] C16 "consumers route on `merge_method` first" (SKILL.md:709): `contract.derive_verdict` checks diversity and `adversarial_unavailable` first and never validates `merge_method` values (`contract.py:274-296`).
- [CODE-CONTRADICTED] EV-1 branch (b) text accepts an F3 run without `single-reviewer-fallback`; `panel_lint._ev1` requires it (`panel_lint.py:290-291`).
- [CODE-CONTRADICTED] EV-1 claims to read disk, "NOT a self-written field" (SKILL.md:714), but `merged-verdict.yaml` is written by the same orchestrator in shadow step 7 (SKILL.md:346); sc-adversarial's own contract has no `merge_method` (installed SKILL.md:436-448).
- [UNVERIFIED] Whether a Skill-tool call to sc-adversarial spawns the `debate-orchestrator`/advocate agents or runs inline in the reflect session (installed SKILL.md:467-489 names agents; 6 recorded runs say "inline orchestrator").
- [UNVERIFIED] The "twelve files" of `tests/cli/reflect/` named in the task: the directory has 38 test files; my list of twelve relevant ones is by file name.
- [UNVERIFIED] Bodies of `test_verdict_replay_script.py`, `test_reviewer_readonly_tools.py`, `test_reviewer_brief_constraints.py` (names only).
- [UNVERIFIED] Which shadow runs predate the fix commits `9874d63fb`/`c2e3347d3`; directory names carry package dates, not run times.
- [UNVERIFIED] MR decisions (debate kept, contract unchanged through Stage 4, E' deferred to 2.0.0), cited second-hand from scope slice 04 §4.1.
- [UNVERIFIED] E3 `review merge` internals (`ledger.py`, `findings.py` lines), cited from the hand-off §5.1, not re-read here.
- Resolved in the Phase 3 fix cycle 1: `ensemble.py` writes `verification_verified` and `regression_verified` (always `False`, :814, :816), `reviewers_verified` (:815) and `adversarial_subrun_status` (:793) at top level of its version-"1.0" contract; no skill-path producer writes them (section 8a; research/13 §4). [CODE-VERIFIED]
- Open items carried from research/13 Gaps: swarm `reduce_wave3` key list for `t2-swarm/return-contract.yaml` and the score semantics `/sc:adversarial` returns for free-form swarm reviews are [UNVERIFIED]; whether the live `T2Model0N` pool contains the executor's model family (decides whether ignoring `executor_model_class` bites) is [UNVERIFIED].
- [UNVERIFIED] C13 enforcement (`make verify-sync` / pre-commit hook) not read.
- [UNVERIFIED] §1.1: no code home for the `--t2-engine panel` reject message; based on the slice 04 §0.16 grep, not re-run here.
- Question: should EV-1 be rewritten so the merge step (sc-adversarial or a script) writes the verdict file with its own `merge_method`, so the label is not self-attested?
- Question: should the orchestrator write contracts through a YAML serializer? The `[1m]` alias breaks hand-written flow lists (section 7.1); one contract writer is a shared-core candidate.
- Question: is a paired evidence run (same package, legacy vs panel merge, ground truth scored blind) planned before any Stage 3 merge replacement? The current verdict replay cannot show it.
- Question: should `channel: advisory` force `blocking: false` in `findings_v2.check_finding`?

## Stale Documentation Found

- **[STALE DOC]** SKILL.md testability map row "Memory write optionality | `telemetry memory_status`" (:1958) names a telemetry key absent from §9.2 (:940-989) and from `panel_lint.TELEMETRY_FIELDS`; a run following the row (shadow07) fails lint L2.
- **[STALE DOC]** The SKILL.md:714 EV-1 rationale ("a real adversarial merge writes `merged-verdict.yaml`") does not match the installed sc-adversarial artifact list (:371-386: no `merged-verdict.yaml`; the merged output is `<merged-output>.md`). The yaml file exists only because reflect's shadow step 7 tells the orchestrator to write it (:346); no such instruction was found for legacy (non-shadow) runs in the read ranges.
- **[STALE DOC]** The SKILL.md testability row (:1955) covers only EV-1 branch (a); the loud-fallback branch (b) of :714 is missing there.
- **[STALE DOC]** The task prompt describes `tests/cli/reflect/` as twelve files; the directory has 38 test files.
- Scope slice 04 §0.15 left the EV-1 counts UNVERIFIED; this file records them (shadow 8/13, legacy 3/39).
- Scope slice 04 §0.12 says runs 03/06/07 had the nested copy and 04/05 only `.md`. A re-check confirms that and adds 08 (`.md` only), 11 (both copies) and 15 (top copy but 0 reviewer cards).

## Summary

Under reflect's frozen contract 1.8.0, a script merge is not allowed. SKILL.md forbids reflect from building its own merge, and EV-2 allows only `adversarial` and `single-reviewer-fallback`. `panel_lint` turns any new value or new top-level key into a bump failure, and the wrapper `contract.py` blocks major version 2 and degrades any Tier 2 run without a convergence score of at least 0.80. So the shared core can own resolution, cards, clustering, citation checks, calibration coverage and manifests (all telemetry today), but it cannot own reflect's merge decision or contract writer without a contract bump plus wrapper and lint changes. The recorded shadow runs give no quality case either way, because debate convergence and `cluster_agreement` are both near 1.0 everywhere. They also show that the orchestrator judged 6 of 14 "adversarial" merges itself (one with no debate artifacts) and that EV-1 checks a file the orchestrator writes itself. Stage 2 exit is FAIL (exit 1, 13 of 20 runs, EV-1 rate 0.615 vs 0.077, 6 parity and 9 lint/manifest failures). Every failure comes from contract-writing and file-placement mistakes, including three contracts that unquoted `[1m]` alias names made unparseable. C1, C6 and C14 compare only with HEAD, so they do not protect the contract across commits. UC-2 `reflect-post` has templates and a parser lens, but no brief line, reviewer format or blocking rule on the skill path. Everything above is about the skill path: the blocking tasklist post gate runs `superclaude reflect run`, which always takes a third, code-driven merge path (`ensemble.py`, `runner.py:538-545`). That engine writes its own version-"1.0" contract in code (`ensemble.py:886-895`), labels `merge_method: adversarial` from the reviewer count alone (`:773`) even when the adversarial step failed, and defaults every deviation flag to clean (`:442-471`), so it can never HALT on a deviation the reviewers find (section 8a).
