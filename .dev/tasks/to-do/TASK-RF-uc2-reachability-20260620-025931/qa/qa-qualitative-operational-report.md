# QA Report — task-qualitative (operational-correctness lens)

**Topic:** FR-RSR UC-2 Runtime-Surface Reachability Escalation
**Date:** 2026-06-20
**Phase:** task-qualitative
**Fix cycle:** N/A
**fix_authorization:** false (REPORT ONLY)
**Task file:** .dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md

---

## Overall Verdict: FAIL (1 IMPORTANT + 2 MINOR; 0 CRITICAL — see full verdict at bottom)

(Findings appended incrementally below.)

---

## Verified Anchors (confirmed against live source — PASS)

All line anchors the edit items rely on were re-Read against the live files. Confirmed accurate:

- pyproject.toml :67-69 `[project.scripts]` = `superclaude`, `ic` — EXACT match (Step 2.1 / degrade-oracle in-repo case). PASS.
- SKILL.md §5.3 table header :386, row 1 :390, row 2 :391, row 8 default :398; D13 pre-filter precedence paragraph :402 (names "1, 2, or the row-8 default" + `--tier 1`/`--depth quick`/`--no-escalate` carve-out). PASS (Steps 4.1/4.2).
- SKILL.md §5.4 tier_decision.yaml header :404, `coverage_degraded` reason field :411. PASS (Step 4.1).
- SKILL.md §6.1 Wave-1A header :453, step 4 `find_referencing_symbols` :463, reuse-auditor step 4a :464, prose region :480-494. PASS (Steps 3.1/3.2).
- SKILL.md §9.1 header :660, `contract_version "1.5.0"` literal at :663; prose "Contract version is v1.5.0" at :804; kill-list invariant test `contract_version == "1.5.0"` at :1772 — ALL THREE gate sites confirmed. PASS (Step 3.3).
- SKILL.md UC-2 block: `verification_skip_reason` :709, Reuse-Miss banner :711 — insertion gap for the 6 fields confirmed. `deviation_count_by_class.{authorized,necessary,drift,regression}` :691-695; `verification_regressions_detected` :708 (FR-4 exit-code-sourced). PASS.
- SKILL.md §9.3 header :851, executor.py TurnLedger rollback row :858 (`deviation_class == regression triggers TurnLedger rollback`), advisory row :862, field-deletion guard :868. PASS (Step 3.3 + key constraint (d)).
- SKILL.md §10.8 Reuse-Miss finding-modifier :1014 (the "NOT a 5th class / maps onto the 4 by evidence" template to mirror), ends :1025, `---` at :1027 — §10.9 insertion point confirmed. §10.6 grounding-gaps reference :1008. PASS (Step 5.1).
- SKILL.md §17.7 kill-list item 6 (5th `unknown` class rejected) :1799. PASS.
- SKILL.md cosmetic site :1641 literal `"skill_version": "1.5.0"` — confirmed stale literal. PASS.
- refs/reviewer-spec.md "exactly these three sections" :23; headings `## T1 card excerpt` :25 / `## Grounding hunks` :31 / `## Coverage slice` :49; FR-4 exemplar :43 (carries the verbatim "NOT a fourth brief section" wording to mirror), FR-RV3-MED.1 :45, D13 :47 — FR-RSR.9 insertion between :47 and :49 inside `## Grounding hunks` confirmed valid. PASS (Step 6.1).
- refs/deviation-taxonomy.md "4 categories" :5, "4 categories, not 5" :117, `## Grounding-gaps parallel artifact` section :115-138. PASS (Step 5.2).
- grader.py `parse_yaml_simple` :58-77 reads ONLY flat top-level non-indented `key: value` (skips `#`/indented) — confirms the flat-key constraint Step 7.1 relies on. `yaml_field` keys `{field, expected}` :336-346; `yaml_field_min` keys `{field, min_value}` :348-361; `regex_absent`/`regex_present` keys `{target, pattern}` :152-169; `yaml_list_contains` uses `field_path`+`value` membership (NOT length) :172-187. PASS — confirms count-invariant is NOT expressible by baseline assertions; precomputed-scalar approach is sound.
- Dual-snapshot mechanism IS implemented: grader.py :422-423 partitions assertions by `with_skill/` vs `old_skill/` target prefix; :448-457 writes separate `with_skill/grading.json` + `old_skill/grading.json`. PASS — `old_skill/` (FAIL-pre) / `with_skill/` (PASS-post) prefixes are real (Steps 7.2/7.7).
- evals.json: 36 existing eval objects (ids 1-36) → new ids 37-41 contiguous; id-2 `post-small-diff-clean` template entry shape confirmed; `case_dir: "cases/post-small-diff-clean/"` confirms cases live under `cases/` NOT `evals/`; falsifier ids 19/20 = `T2-converges-on-wrong`,`T2-judge-class-collision` (these use `case_file`, not `case_dir`); top-level `notes` string present for the codebase-over-doc note. PASS (Step 7.7).
- Template case `cases/post-small-diff-clean/` has `expected.yaml` + `input/diff.patch` + `input/tasklist.md` (3-file layout). PASS (Steps 7.2-7.6).
- skill-snapshot/reflect-v1.md exists (5942 bytes), 0 `runtime_surface` refs — the fail-before baseline. PASS (Step 7.2).
- reflect CLI (`src/superclaude/cli/reflect/commands.py`): `--promote/--no-promote` :90 (default promote), `--depth` :102, `--fix/--no-fix` :128, `--base` :140 (optional), positional TASK path :59-60. Recursion-breaker env `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` (runner.py:53, commands.py:44). PASS — the POST wrapper command (task :362) `superclaude reflect run <abs TASK.md> --depth deep --fix --promote` with the skip-guard is syntactically valid, all flags real, single `;`-joined Bash command (executor-run, not user-pasted). No `--base`/`--reflect`/range present, matching the flat-wrapper contract.
- §0.5d four-field availability contract :242-261 (`backend: none` :246, do-not-re-probe rule :259, fail-open :261); §6.5 fail-open :563-565; `degraded_components` :815; slug precedent `"neighbour-search:auggie_unavailable"` :471. PASS (Step 6.2 FR-RSR.8 wiring).
- QA gate serialization (PG.2-PG.10): PG.2-PG.7 all `fix_authorization: false`; PG.9 spawns EXACTLY ONE `rf-qa` with `fix_authorization: true` ("NO other fix agent concurrently"); PG.10 verification round = 2 agents both `fix_authorization: false`. PASS — no two simultaneous fix authorizations (I20 serialized).
- Research files 01-05 all present and corroborate the anchors; research 04 :300-314 independently flags the count-invariant-needs-precomputed-scalar problem that Step 7.1 resolves. PASS.

---

## Issues Found

### Five-Axis annotations (task-qualitative)

| # | Severity | Axis | Location | Issue | Required Fix |
|---|----------|------|----------|-------|-------------|
| 1 | IMPORTANT | AX-1 (drift) | Task §Key Constraints :136 + Step 3.3 + Step 3.4(PG.2 prompt) — re SKILL.md:1558 | The task asserts a "2 cosmetic refresh sites" claim where one of them (`:1558`) is NOT a literal-version site. Live SKILL.md:1558 reads `"skill_version": "<contract_version from §9.1>"` — a SYMBOLIC reference, not a literal `"1.5.0"`. Step 3.3 instructs "refresh the two cosmetic sites (:1558 skill_version ref ... so they read 1.6.0". An executor following this literally will either no-op (harmless) OR hardcode `"1.6.0"` at :1558, REPLACING the deliberately-symbolic `<contract_version from §9.1>` ref with a literal — a de-parameterizing regression. Research file 02 (the re-anchoring source) documents ONLY 3 contract_version sites (:663/:804/:1772) and never validated :1558 as a refreshable literal; the "2 cosmetic sites" framing is task-introduced drift not grounded in the verified anchors. (:1641 IS a real stale literal `"skill_version": "1.5.0"` and is correctly a refresh target.) | In Step 3.3, Step 3.4, and the PG.2 adversarial prompt, change the :1558 instruction from "refresh so it reads 1.6.0" to "VERIFY :1558 still reads the symbolic `<contract_version from §9.1>` and is LEFT UNCHANGED (it resolves automatically); only :1641 is a literal cosmetic refresh." Reduce the count claim from "3 gate + 2 cosmetic" to "3 gate sites + 1 literal cosmetic (:1641); :1558 is symbolic, no edit." |
| 2 | MINOR | AX-2 (contradictions) | Task Step 3.1/3.2 vs live SKILL.md §6.1 step ordering :463-464 | Step 3.1 says insert 4b' "immediately AFTER step 4 (line 463)" and Step 3.2 inserts 4b after 4b'. But step 4a (reuse-auditor) already occupies :464, between step 4 and step 4.5. The resulting documented order becomes `4, 4b', 4b, 4a` — alphanumerically inverted (4b'/4b precede 4a). The task asserts "4b' coexists with [4a] in correct order" but does not specify whether 4b'/4b land before or after 4a. Dependency-wise either order works (4b'/4b consume step 4's already-fetched `find_referencing_symbols` result at :463, satisfied before both). This is a label-ordering ambiguity, not an execution blocker (the §6.1 chain is a documentation list, not executable code). | Clarify in Step 3.1/3.2 the intended placement relative to existing 4a: recommend inserting 4b'/4b AFTER 4a (giving `4, 4a, 4b', 4b`) to preserve ascending labels, OR explicitly state the chosen order. No functional impact either way. |
| 3 | MINOR | AX-3 (omissions) | Task Step 7.8 / 7.9 — eval execution mechanism | The grader.py contract (`main()` :461-478) takes an `<iteration-dir>` and iterates `eval-*/` subdirs each requiring `eval_metadata.json` (:414, else SKIP); it grades PRE-PRODUCED `with_skill/outputs/*` + `old_skill/outputs/*` files and does NOT run the reflect skill. `make reflect-eval` (:505-508) creates an EMPTY fresh `iterations/<ts>/` and greps nothing. There is NO producer harness in-workspace that materializes `cases/uc2-*/` into `iterations/eval-<name>/` trees, generates `eval_metadata.json`, or runs the v1-snapshot + post-change skill to produce the graded `contract.yaml` outputs. ZERO `eval_metadata.json` and ZERO `with_skill/outputs/` exist anywhere (consistent with evals.json `notes`: existing 36 cases are v1.0 STUBS never run through a producer). Step 7.8 hand-waves "discover the exact invocation from the workspace" and Step 7.9 asserts a byte-identical determinism re-run — but the FAIL-pre/PASS-post + determinism claims require executing the actual (LLM-driven) reflect skill twice per snapshot, a step neither the grader nor `make reflect-eval` performs, and which Step 7.8 does not specify. NOTE: this is consistent with the ESTABLISHED repo pattern (authoring registry + fixtures as scaffolds), so the AUTHORING items 7.1-7.7 are sound; the gap is only in 7.8/7.9's claim that a runnable PASS/FAIL verdict + determinism check is achievable via the documented invocation. | In Step 7.8/7.9, either (a) explicitly scope the deliverable to "author cases + register + materialize the `eval-<name>/` tree with `eval_metadata.json` and produced `with_skill`/`old_skill` outputs, then grade" — naming the producer step that runs the skill; OR (b) acknowledge (matching the existing-36-stub convention) that fixtures+registration are the deliverable and the FAIL-pre/PASS-post + determinism verification is deferred/manual, downgrading 7.8/7.9's "run and confirm green" to "author + register; runtime grading is producer-gated." Do NOT leave Step 7.8 asserting a grader invocation that cannot produce the graded outputs. |

(No CRITICAL issues found. The six SKILL.md edit anchors, all three contract gate sites, the §10.9 insertion point, the refs insertion points, the dual-snapshot grader mechanism, the contract additivity, the counter hygiene plan, the blocker ordering, the POST wrapper command, and the I20 serialization are all operationally correct as written.)

---

## Items Reviewed (operational-correctness checks, 15-item adaptation)

| # | Check (task-qualitative item) | axis | Result | Evidence |
|---|-------------------------------|------|--------|----------|
| 1 | Gate/command dry-run (make verify-sync, reflect wrapper, grader, git) | AX-3 | FAIL | reflect wrapper flags all real (commands.py :90/:102/:128); BUT grader/`make reflect-eval` cannot produce graded outputs for 7.8/7.9 — see Issue #3 |
| 2 | Project convention compliance (src/ SoT, sync, cases/ vs evals/) | none | PASS | every SKILL.md/refs edit item paired with sync+verify-sync; cases under `cases/` confirmed via evals.json id-2 `case_dir`; `.claude/` never staged |
| 3 | Intra-phase execution-order simulation | none | PASS | P1 blocks P2-6; oracle/rootwalk (P2) before UNREACHED (P3 sweep); contract field (P3) before §5.3 pre-filter (P4); evals (P7) terminal — ordering sound |
| 4 | Signature/value verification (all line anchors, contract sites, ports/paths) | AX-1 | FAIL | 3 contract gate sites + :1641 literal verified EXACT; :1558 is symbolic not literal — see Issue #1 |
| 5 | Module context analysis (§6.1 chain, §9.1 block, §10 taxonomy) | AX-2 | FAIL | UC-2 block/banner/counter all confirmed; §6.1 step-ordering label ambiguity vs existing 4a — see Issue #2 |
| 6 | Downstream consumer analysis (6 fields → §5.3/§10.9; executor.py rollback) | none | PASS | §9.3 advisory row + executor.py :858 rollback row confirmed; pre-filter reads `runtime_surface_unreached`, §10.9 reads ledger statuses — consumers wired |
| 7 | Test validity (eval cases test real behavior, real diffs) | none | PASS | Steps 7.2-7.6 mandate REAL git diffs re-enacting FR-S9-04; dual-snapshot FAIL-pre/PASS-post is the falsifiability mechanism (authoring is sound; cf. Issue #3 on execution) |
| 8 | Test coverage of primary use case | none | PASS | headline `uc2-unwired-surface-passes` covers the motivating incident end-to-end; 4 companions cover REACHED/DEGRADE/backend-loss/UNREACHED+count |
| 9 | Error path coverage (fail-open, degrade oracle, kind-resolution failure) | none | PASS | FR-RSR.8 fail-open wired to §0.5d/§6.5; degrade-oracle default-DEGRADE; kind-resolution failure → DEGRADE; backend loss → Grounding Gap never STOP |
| 10 | Runtime failure-path trace (input→sweep→classify→gate→surface) | none | PASS | data flow traced: tagger→sweep(oracle+rootwalk gate)→ledger→§5.3 route→§10.9 classify→reviewer-brief; no UNREACHED emittable without oracle+rootwalk |
| 11 | Completion scope honesty (open questions resolved, no silent skip) | none | PASS | OQ-RSR.1/.2/.3 resolved in P1; codebase-over-doc reconciliations documented not halted; count-invariant OQ resolved in Step 7.1 |
| 12 | Ambient dependency completeness (all touchpoints) | none | PASS | contract 3 gate sites + cosmetic; §9.3 consumer row; deviation-taxonomy xref; evals.json registry + notes; sync after every edit |
| 13 | Kwarg/edit sequencing red flags | none | PASS | no "add kwarg before add param" pattern; sweep's oracle/rootwalk gate authored in P1 BEFORE consumed in P3; field added (P3) before read (P4) |
| 14 | Existence claims grep-verified (NEW runtime-surface.md absent; sites exist) | none | PASS | runtime-surface.md confirmed ABSENT (NEW); all 36 eval ids + falsifier 19/20 + template case + skill-snapshot confirmed present via filesystem |
| 15 | Cross-reference accuracy for templates/refs (§N references) | none | PASS | every §-anchor (5.3/5.4/6.1/6.5/9.1/9.3/10.8/17.7/0.5d + reviewer-spec/deviation-taxonomy) re-Read and confirmed to contain the claimed content |

## Self-Audit (MANDATORY)

1. **How many factual claims independently verified against source?** ~30 distinct anchor/mechanism claims, each via direct Read/Grep of the live file (not via research files alone): pyproject :67-69; SKILL.md §5.3/§5.4/§6.1/§9.1(×3 sites)/§9.3/§10.8/§17.7/§0.5d/§6.5 + cosmetic :1558/:1641; reviewer-spec.md :23/:25/:31/:43/:47/:49; deviation-taxonomy.md :5/:117/:115-138; grader.py parse_yaml_simple + 5 assertion-type signatures + dual-snapshot partition; evals.json count/ids/falsifiers/notes; template case + snapshot via filesystem; reflect CLI flags.
2. **What specific files did I read?** SKILL.md (10 regions), reviewer-spec.md, deviation-taxonomy.md, pyproject.toml, grader.py (4 regions), evals.json, Makefile :505-517, reflect/commands.py (grep), the task file (all 455 lines across 4 reads), research 02/04 (grep corroboration), and filesystem listings of the eval workspace.
3. **If I found issues, why trust the check was thorough?** I did NOT accept the research files' anchors at face value — I re-Read every cited line in the LIVE source and found the :1558 drift specifically BECAUSE I read the actual line (which research never validated). I traced the grader's actual `main()`/`grade_eval` contract rather than assuming `make reflect-eval` works, which surfaced the producer-gap (Issue #3). The 3 confirmed-correct contract gate sites and the dual-snapshot mechanism prove I checked both passing and failing cases.
4. **Web research?** None performed — this review is entirely local-file-bound (task file + source code + eval workspace). No Tavily/WebFetch needed; no Tool-engagement fallback to record.

## Confidence Gate

- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 14 | Grep/Bash-grep: 5 | Glob/Bash-ls: 3 | Bash(total): 4
- Every one of the 15 operational checks was exercised against live source with cited evidence. Tool calls (≈22) exceed the 15-item minimum.
- No UNCHECKED items. No UNVERIFIABLE items.

## Summary

- Checks passed: 12 / 15
- Checks failed: 3 (items 1, 4, 5 — corresponding to Issues #3, #1, #2)
- Critical issues: 0
- Important issues: 1 (Issue #1 — :1558 cosmetic-site drift, risk of de-parameterizing edit)
- Minor issues: 2 (Issue #2 — §6.1 label-order ambiguity; Issue #3 — eval-execution producer gap in 7.8/7.9)
- Issues fixed in-place: 0 (fix_authorization: false — REPORT ONLY)

## Recommendations

1. **Fix Issue #1 (IMPORTANT) before execution.** Correct Step 3.3 / Step 3.4 / PG.2 prompt so :1558 is VERIFY-UNCHANGED (symbolic ref), not "refresh to 1.6.0". Reframe the count as "3 gate sites + 1 literal cosmetic (:1641)". Otherwise an executor risks de-parameterizing the dynamic skill_version reference.
2. **Fix Issue #3 (MINOR but execution-relevant).** Either name the producer step that materializes `eval-<name>/` trees + runs the skill to generate `with_skill`/`old_skill` outputs, OR explicitly scope 7.8/7.9 to author+register (matching the existing-36-stub convention) and mark runtime grading/determinism as producer-gated. As written, Step 7.8's "run the grader and confirm FAIL-pre/PASS-post" is not achievable via the documented `make reflect-eval`/grader path alone.
3. **Optionally clarify Issue #2 (MINOR).** Specify 4b'/4b placement relative to existing 4a (recommend after 4a for ascending labels). No functional impact.

## Overall Verdict: FAIL

Per task-qualitative policy (ANY issue of any severity = FAIL), this gate FAILs on 1 IMPORTANT + 2 MINOR issues. None are CRITICAL — the core mechanism (six edits, contract additivity, counter hygiene, blocker ordering, falsifiability design, POST wrapper, I20 serialization) is operationally correct. The defects are: (#1) a drifted cosmetic-site instruction that risks a wrong de-parameterizing edit; (#2) a step-label ordering ambiguity; (#3) an unspecified eval-execution producer step that makes Step 7.8/7.9's "run-and-confirm" claim unachievable as written. All three are remediable by editing the task file's instructions (no source-code defect). Recommend resolving #1 and #3, then re-gate.

## QA Complete
