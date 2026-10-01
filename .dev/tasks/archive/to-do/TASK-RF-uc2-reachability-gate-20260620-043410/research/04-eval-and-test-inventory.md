# Research 04 — Test & Verification: eval fixture and reflect contract tests

Status: Complete

## Scope

- Eval workspace: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/eval-workspaces/sc-reflect/`
- Reflect tests: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/`
- Focus: eval case/manifest structure, grader assertions, reflect contract fixture/test patterns, and test additions for FR-RH1 UC-2 contracted-sink reachability and oracle-admissibility.

## Findings

### 1. Eval manifest shape is JSON entries with `case_dir`, mode/use_case metadata, `inputs`, `expected`, and assertion objects

- The eval manifest declares the skill name, iteration, scope, and notes that the workspace currently mixes pilot evals, promotion evals, falsifier skeletons, and Serena scaffolds; it explicitly says assertions are defined in `grader.py` and that scaffold entries target future `with_skill/outputs/` artifacts: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/eval-workspaces/sc-reflect/evals/evals.json:1-5`.
- A UC-1 entry uses `case_dir`, `mode`, `use_case`, `spec_ref`, `description`, `inputs`, `expected`, and `assertions`; the assertions include `file_exists`, `matrix_covers_items`, and `regex_present`: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/eval-workspaces/sc-reflect/evals/evals.json:8-39`.
- Existing UC-2 post-mode entries follow the same pattern. `post-small-diff-clean` points to `input/diff.patch` and `input/tasklist.md`, asserts `contract.yaml` fields, and uses `regex_absent` to prevent false deviations: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/eval-workspaces/sc-reflect/evals/evals.json:42-73`.
- `post-large-diff-mixed` shows the richer UC-2 pattern: `yaml_list_contains` against `deviation-ledger.yaml`, `yaml_field` against `contract.yaml`, and `citation_resolves` against `REPORT.md` with fixture-root remapping: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/eval-workspaces/sc-reflect/evals/evals.json:76-114`.

Implication for FR-RH1: add producer-level fixtures as new eval manifest entries rather than inventing a new harness. Suggested names should be explicit, e.g. `uc2-reachability-proxy-oracle-unproven`, `uc2-reachability-telemetry-no-reachability`, and `uc2-reachability-telemetry-missing-inputs`.

### 2. Grader supports enough assertions for the requested reachability/oracle tests, but nested scalar-list checks are limited

- The grader documents the inherited baseline types and the extended semantic types: `file_exists`, `frontmatter_field`, `section_present`, `section_enumerated`, `yaml_field`, `yaml_field_min`, `yaml_substring`, `dir_count`, plus `citation_resolves`, `regex_present`, `regex_absent`, `yaml_list_contains`, `matrix_covers_items`, `checkpoint_logged`, `deviation_class_matches`, `path_exists`, `path_does_not_exist`, and `falsifier_skeleton_present`: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/eval-workspaces/sc-reflect/grader.py:14-19`.
- `parse_yaml_simple` only parses flat top-level scalar YAML for the baseline YAML field checks; the comment states newer nested/list-aware checks use `yaml.safe_load`: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/eval-workspaces/sc-reflect/grader.py:58-65`.
- The dispatcher confirms the available semantic assertion types and that unknown assertion types fail: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/eval-workspaces/sc-reflect/grader.py:386-408`.
- The grading phase splits assertions by `target` prefix into `with_skill/` and `old_skill/` groups, then evaluates each assertion and emits pass/fail totals: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/eval-workspaces/sc-reflect/grader.py:411-449`.

Implication for FR-RH1: for contract fields that are top-level booleans/enums/strings, use `yaml_field`; for evidence buried in nested lists/maps, use `regex_present` unless the implementation adds a scalar-capable nested YAML assertion. Existing manifest comments already use `regex_present` for nested structures when `yaml_list_contains` is not enough.

### 3. Existing telemetry-completeness eval is the closest precedent for field-presence and skip-path assertions

- The telemetry completeness entry is UC-2 post-mode and describes a holistic sweep over `audit.log` plus the return contract, specifically asserting `<tool>_invoked/_ran` fields and degraded/skip-reason fields on success and degraded paths: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/eval-workspaces/sc-reflect/evals/evals.json:997-1005`.
- Its assertions check `telemetry_fields_present` for success-path fields and use `regex_present` over `audit.log` for skip/degraded-path fields: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/eval-workspaces/sc-reflect/evals/evals.json:1007-1012`.
- The companion expected fixture is a human contract doc whose header says the grader reads `evals/evals.json`; it enumerates success fields, degraded/skip fields, and `both_paths_required: true`: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/eval-workspaces/sc-reflect/cases/serena-telemetry-completeness/expected.yaml:1-23`.

Implication for FR-RH1: UC-2 reachability field presence should extend this pattern using the patched R7 stable field names from `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:162-172`: `reachability_gate_ran`, `reachability_ledger_path`, `reachability_requirements_scanned`, `reachability_unreachable`, `reachability_unproven`, `reachability_real_boot_ran`, and `reachability_skip_reason`. Do NOT use provisional names such as `reachability_ran`, `contracted_sink_reachability`, `oracle_admissibility`, `oracle_boot_mode`, `proxy_oracle_unproven`, or `semantic_fallback_advisory_only` as stable fields unless a later approved spec amends R7. Assertions can target `with_skill/outputs/contract.yaml` and `with_skill/outputs/audit.log`.

### 4. Existing falsifier skeletons are the precedent for producer-level adversarial fixtures

- The `T2-converges-on-wrong` case is a skeleton with `status: skeleton-pending-iteration-3-fixture`, an `expected_grader_emission`, a fixture path, and a canonical assertion expression: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/T2-converges-on-wrong.yaml:1-10`.
- The same skeleton explicitly says promotion to active requires changing `status` to `active` and adding canonical fields `type`, `fixture`, `expected`, and `assertion`: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/T2-converges-on-wrong.yaml:15-18`.

Implication for FR-RH1: the producer-level unproven proxy-oracle fixture should be an active, canonical falsifier-style fixture, not just a prose expected file. The load-bearing assertion should fail if a proxy oracle is treated as proven; use canonical R7 contract fields and ledger assertions, e.g. `reachability_gate_ran: true`, `reachability_unreachable: 0`, `reachability_unproven: 1`, `needs_human_decision: true`, plus a ledger row with `verdict: unproven`, `oracle_match: false`, and `gap_kind: oracle-mismatch`, while proving proxy/oracle evidence alone never satisfies the real-boot Regression proof bar.

### 5. Existing Serena summarize-changes eval is the closest precedent for advisory-only semantic fallback

- The Serena summarize-changes eval is UC-2 post-mode and describes a prompt-based corroboration path where same-session disagreement feeds Drift/Necessary sets, while cross-session `unavailable` leaves the main verdict unchanged: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/eval-workspaces/sc-reflect/evals/evals.json:820-826`.
- Its assertions check `serena_summary_corroboration: disagree`, report surfacing, and a cross-session contract with `serena_summary_corroboration: unavailable`: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/eval-workspaces/sc-reflect/evals/evals.json:844-862`.

Implication for FR-RH1: semantic fallback should mirror this advisory/corroborative posture. Add a fixture where semantic evidence is present but boot/reachability proof is absent, then assert the fallback is recorded in telemetry/audit but does not satisfy the Regression proof bar.

### 6. Reflect contract tests already use fixture YAMLs plus direct `derive_verdict` assertions for contract tolerance and routing

- Contract-version major fail-loud behavior is covered by `test_blocked_unknown_major_version`, which loads `blocked_unknown_major.yaml` and expects `BLOCKED` / exit 2: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_verdict_mapping.py:119-128`.
- Minor-version tolerance is already tested at the 1.x level: `test_tolerant_unknown_field_1x` says `1.9.0 + an unknown top-level field still maps to pass / 0`: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_verdict_mapping.py:131-140`.
- The corresponding fixture has `contract_version: "1.9.0"` and an unrecognized top-level `future_unknown_telemetry_field`: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/fixtures/tolerant_unknown_field.yaml:1-29`.
- Existing tests also pin that advisory/unavailable fields and exempted skips should not degrade: `serena_summary_corroboration: unavailable` maps to PASS, `verification_ran: False` with `verification_skip_reason: read-only-project` maps to PASS, and the unexempted control maps to DEGRADED: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_verdict_mapping.py:143-175`.
- Benign degraded components are tested as exact-membership non-gating tokens: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_verdict_mapping.py:190-201`.

Implication for FR-RH1: add a 1.6.0 fixture (or mutate the loaded pass contract in-test) with reachability/oracle additive fields and assert it remains tolerated by consumers. Also add routing tests for advisory-only semantic fallback and telemetry-only skip reasons so the wrapper does not treat new fields as hard gates unless explicitly specified.

### 7. Mocked E2E runner tests are the precedent for wrapper-level contract production/consumption behavior

- The stub factory writes a selected fixture into `<output_dir>/return-contract.yaml` inside `.wait()`, or writes no contract when `fixture_name=None` / `write_contract=False`: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/conftest.py:98-138`.
- The sequence stub ensures apply launches write no contract and fresh audit contracts are written only by audit steps, matching the post-fix anti-stale-contract pattern: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/conftest.py:141-189`.
- E2E runner tests already cover pass/halted/degraded/blocked verdicts by selecting fixture contracts and asserting exact verdict/exit codes: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_runner_e2e.py:39-114`.
- The fix-loop tests prove exact audit/apply launch arithmetic and fail-closed behavior; for example, convergence uses audit -> apply -> re-audit, non-convergence uses 3 audits + 2 applies, and failed apply never re-audits into a false pass: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_fix_loop.py:35-168`.

Implication for FR-RH1: wrapper/contract tests should use the existing fixture/stub pattern rather than spawning real Claude. Real-boot-only proof-bar behavior belongs in contract fixture(s) plus `derive_verdict`/runner assertions that prove proxy-oracle-only evidence cannot green a Regression proof.

## Recommended task-item breakdown

1. **Add UC-2 reachability eval fixtures and manifest entries**
   - Add case directories under `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/eval-workspaces/sc-reflect/cases/` for:
     - `uc2-reachability-proxy-oracle-unproven`
     - `uc2-reachability-no-reachability-skip`
     - `uc2-reachability-missing-inputs-skip`
     - optionally `uc2-reachability-real-boot-regression-proof`
   - Add entries to `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/eval-workspaces/sc-reflect/evals/evals.json` after the existing UC-2 telemetry/scaffold cases, following the `case_dir` + `inputs` + `expected` + `assertions` pattern.

2. **Use current grader DSL before extending it**
   - Prefer `yaml_field` for top-level scalar contract fields.
   - Prefer `regex_present`/`regex_absent` for nested evidence and audit lines.
   - Use `yaml_list_contains` only for true YAML list fields.
   - Add a new grader type only if the implementation requires nested scalar/list-of-map structural assertions that regex cannot safely pin.

3. **Add producer-level unproven proxy-oracle falsifier**
   - Model it after the falsifier skeleton, but make it active with canonical fields.
   - Assertions should prove proxy/oracle evidence is emitted as unproven/advisory and does not satisfy the real-boot Regression proof bar.

4. **Add contract fixture coverage in `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/fixtures/`**
   - Add a `contract_version: "1.6.0"` fixture with the canonical R7 additive fields: `reachability_gate_ran`, `reachability_ledger_path`, `reachability_requirements_scanned`, `reachability_unreachable`, `reachability_unproven`, `reachability_real_boot_ran`, and `reachability_skip_reason`.
   - Add telemetry-only skip fixtures for `reachability_skip_reason: --no-reachability` and `reachability_skip_reason: spec-and-tasklist-absent`, with zero counters, null ledger path, and no `needs_human_decision`/status effect solely from reachability.
   - Add proxy-oracle-only and semantic-fallback-only fixtures that must not produce a green Regression proof; semantic fallback without explicit `durable_sink:` / `@sink` must remain advisory and must not increment `reachability_unproven`.

5. **Add direct contract tests in `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_verdict_mapping.py`**
   - Assert `contract_version 1.6.0` plus the canonical R7 additive fields is tolerated by the wrapper.
   - Assert `reachability_gate_ran: false` with `reachability_skip_reason: --no-reachability` remains telemetry-only.
   - Assert `reachability_gate_ran: false` with `reachability_skip_reason: spec-and-tasklist-absent` remains telemetry-only.
   - Assert semantic fallback/advisory telemetry does not route to DEGRADED/HALTED by itself and does not create `reachability_unproven` without explicit `durable_sink:` / `@sink`.

6. **Add mocked E2E runner tests only where wrapper integration matters**
   - If the new fields affect wrapper-result/writeback, add tests in `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_runner_e2e.py` using `make_claude_process_stub`.
   - If they affect fix-loop safety, add a focused test in `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_fix_loop.py` proving proxy-oracle-only evidence is never auto-fixed or promoted as proven Regression evidence.

## Gaps and Questions

None blocking after schema normalization. The canonical test/eval schema must use patched R7 fields and patched R2/R3 skip tokens; any provisional field names in earlier drafts are rejected unless a later approved spec amendment adds them.

## Summary

The existing eval workspace already has the right manifest/case/assertion pattern for UC-2 field-presence and telemetry tests, and the grader has enough primitives for most FR-RH1 assertions. The strongest precedents are `post-large-diff-mixed` for UC-2 contract/report assertions, `serena-telemetry-completeness` for success/skip field presence, `T2-converges-on-wrong` for active falsifier shape, and `test_verdict_mapping.py` / `test_runner_e2e.py` for contract-version tolerance and wrapper routing. The main implementation work is to add new reachability/oracle fixtures and a 1.6.0 additive contract fixture using the canonical R7 schema, not to build a new harness.
