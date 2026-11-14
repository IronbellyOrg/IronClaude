# Research Notes: Unified Review Panel (reflect Tier 2 + tasklist panel study + #346 review loop)

**Date:** 2026-11-13
**Scenario:** A (explicit request: goal, sources, output shape all given)
**Depth Tier:** Deep (cross-cutting, 3 efforts, ~60+ files, architectural decision)
**QA intensity:** full
**Status:** Complete (sufficiency gate A.5 passed: paths, per-agent assignments, synthesis mapping, solution options and staleness tags present; no blocking ambiguity)

Research question: compare the Review Panel work of three efforts and recommend one unified design and roadmap:
- E1 = this session (branch `ironbelly/shadow-runs`, 3 commits over master `d2d8a2d16`): reflect Tier 2 panel kernel (findings-v2, card_convert, cluster_v2, verify-citations, manifest, panel extensions, reflect templates), shadow mode, Stage 0-2 artifacts, 15 shadow runs, troubleshoot report, 5x3 model-combination experiment.
- E2 = other session (branch `origin/ironbelly/eval-tasklist-review-panel`, hand-off commit `4a22d74213f93837d00c2c314075dd967b9a98e3`): evaluation-only study of reviewer-model panels on `/sc:workflow` tasklists (106 scored runs, 62 sets, 16 product defects D1-D16, harness, ground truth, audits). No product-code change.
- E3 = #346 review loop on master: findings-v1, ledger, `review merge`/`ledger`/`panel`/`telemetry` CLI, spec-panel Review Loop prose, plus experiment variants installed only in `~/.claude/` and the phase-5 bundle.

Purpose: a roadmap to one central Review Panel that serves sc:reflect (Tier 2 shadow then panel), sc:workflow tasklist review, spec review from sc:brainstorm and sc:design, and later PR code review and replacement of rf-qa / rf-qa-qualitative style agents; capture ALL value, dedupe overlap, resolve conflicts, keep future consumers unblocked.

Required report content (from the user): (a) component overlap matrix across E1/E2/E3; (b) value inventory, every item mapped to a destination or an explicit drop with reason; (c) conflict log with options and a recommended resolution with evidence (adversarial debate where evidence does not decide); (d) target architecture: shared core + thin per-use-case modules; (e) future-use-case check for PR code review and rf-qa replacement.

Scope discovery slices (complete, read these first; they hold file:line evidence):
- `research/scope/00-handoff-copy.md` (E2 hand-off, 315 lines)
- `research/scope/01-other-branch-study.md` (E2 study verified; 5 corrections to the hand-off)
- `research/scope/02-review-cli-code.md` (shared `src/superclaude/cli/review/` package; D1-D16 confirmed at current code; 651 tests)
- `research/scope/03-reflect-side.md` (reflect consumer; constraints C1-C16; finding-shape mapping)
- `research/scope/04-this-session-artifacts.md` (E1 findings F-1..F-23, lessons, decisions)
- `research/scope/05-master-loop-and-consumers.md` (E3 loop; future consumers; vocabularies)

**Scope change from the owner (2026-11-13, mid-run):** this run produces the RESEARCH REPORT ONLY. Do NOT run `/sc:workflow` and do NOT build a roadmap in this task. The roadmap is built later, after this report is merged with the other session's second tech-research report through `/sc:adversarial --compare --merge`. Section 8 of the report is therefore a migration and value-capture plan, not a branch roadmap; it must still name branch-structure options and the no-regression gate list so the later roadmap can use them.

---

## EXISTING_FILES

Full per-file tables with line counts and origins are in the scope slices; this is the consolidated map. Paths are repo-relative to this worktree (branch `ironbelly/shadow-runs`) unless prefixed `E2:` (= `git show 4a22d742:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/<path>`).

### Shared review CLI package `src/superclaude/cli/review/` (slice 02 section 1)
- v1 stack (E3, #346, commit 9163bd1c7): `findings.py` 457 (findings-v1/fixmap-v1 parser, `locate`, `refs_norm` :321, `cluster` :382 union-find, `SEVERITIES` :14, `CATEGORIES` :15-22), `ledger.py` 494 (`merge_round` :107, `apply_revision` :301, `verdict` :363), `merge_cmd.py` 118, `ledger_cmd.py` 137 (exit PASS 0 / REVISE 10 / ESCALATE 11), `telemetry.py` 447 (review-telemetry/1, strata :112-115), `telemetry_cmd.py` 98.
- v2 stack (E1, reflect, commit d2d8a2d16 #519): `findings_v2.py` 304 (`LENSES` :36, `DEVIATION_CLASSES` :38, blocking label rule :161-162), `card_convert.py` 517 (`MAX_REF_TEXT=200` :85, `MAX_CLAIM=300` :86), `cluster.py` 487 (`cluster_v2` :381, `clusters_kept` :447), `cluster_cmd.py` 197, `verify_cmd.py` 184, `manifest.py` 534, `manifest_cmd.py` 240.
- Shared: `panel.py` 707 (`resolve` :565-707, `resolve_slot` :500-556, `select_env` :485, reflect profile :76-150), `panel_cmd.py` 129, `__init__.py` 36 (loader lists absent `lint_cmd`, `estimate_cmd`).
- Data: `data/review-panel.{default,live7,reflect-pre,reflect-pre-x2,reflect-post,reflect-post-x2,reflect-enterprise,reflect-lite}.json`, `data/review-tiers.default.json` (38 lines, `classes` map added by reflect).
- Branch-only edits after #519 (E1, commits 9874d63fb, c2e3347d3): `cluster_cmd.py`/`verify_cmd.py` `--coverage`, `findings_v2.coverage_context()`, reflect SKILL.md §4.3a steps and `refs/reviewer-spec.md:39`.

### Reflect consumer (slice 03 section 1)
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md` 2033 (§3.1 :87, §4.3a :309-349, §9.1 contract 1.8.0 :724+, §9.2 :940-989, §11.3 :1240-1262), `refs/reviewer-spec.md` 116, `refs/reflection-rubric.md` 177, `refs/deviation-taxonomy.md`.
- Agents: `src/superclaude/agents/reflect-reviewer.md` 151, `confidence-calibrator.md` 159, `evidence-validator.md` 150.
- `src/superclaude/cli/reflect/panel_lint.py` 366, `src/superclaude/cli/reflect/contract.py` (`derive_verdict`).
- Scripts: `scripts/reflect_cluster_pairs.py` 559, `reflect_consumer_inventory.py` 535, `reflect_stage0a_replay.py` 896, `reflect_verdict_replay.py` 184, `reflect_shadow_exit.py` 410.
- Tests: `tests/cli/reflect/` (12 files incl. `test_shadow_skill_contract.py` 307, `test_panel_contract_lint.py` 409, `test_shadow_exit_script.py` 319) and the reflect files in `tests/review/`; total `tests/review` = 651 tests (131 from #346 in 7 files, 520 from reflect in 12 files) per slice 02 section 6.

### E1 evidence artifacts (slice 04 section 1)
- `.dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md` (625 lines, architecture C).
- `.dev/tasks/done/TASK-WF-implementStages0-20261111-202912/artifacts/`: `pilot-design.md` 257, `stage0a-report.md` 471, `conversion-gate-redefinition.md` 36, `cluster-v2-known-weaknesses.md` 12, `pair-labels/README.md`, `s-id-results.md` 38, `shadow-standalone-evaluation.md` 132, `consumer-inventory.md` 405, `addendum-1.md`, `addendum-2.md`, `final-review-1..7.md`, `cluster-pairs-50.form*.md`, `pair-review/pairs-P*.{simple,detail}.md`.
- `.dev/troubleshoot/shadow-failures-20261113014240/REPORT.md` 45.
- `.dev/eval-workspaces/shadow-model-combos/` (`PLAN.md` 199, `FINDINGS.md` 42, `results.md` 47, `results.jsonl`, `combos.json`, `analysis/extract.py`, `runs/`).
- `.dev/reflect/pre-*-shadow01..15/` (15 shadow runs; exit script: FAIL, 13 of 20 counted).
- GitHub issues #525-#530 (hand labels for 50 cluster pairs; pending).

### E2 study (slice 01 section 1; branch head 4a22d742)
- `E2:../HANDOFF-review-panel-unification.md` 315 (copy: `research/scope/00-handoff-copy.md`), `E2:manifest.md` 16, `E2:PILOT-REPORT.md` 83, `E2:COMBO-REPORT.md` 506 (only :289+ current), `E2:combos/SPEC.md` 152.
- Per package (3): `candidate.md`, `ground-truth.json`, `resolution-*.json`; `source.md` NOT in the tree (copied at run time from the other worktree's `.dev/tasks/done/<pkg>/source.md`, `tools/run-reviewer.sh:10`).
- Harness: `E2:tools/run-reviewer.sh` 87, `E2:tools/tmp-scripts/` (54 scripts incl. `judge-one.sh` 31, `anon-combos.sh` 28), `E2:analysis/final-table.py` 83, `E2:analysis/three-way.py` 63, `E2:analysis/audits/audit-{A..F}/` (only A and D have `summary.md`).

### E3 master loop and experiment variants (slice 05 section 1A)
- `src/superclaude/commands/spec-panel.md` 490 (Review Loop :256-264, gate :266-268), `src/superclaude/rules/prompts/document_review_loop_prompts.md` 74 (CLI wiring :68-70 only).
- Installed-only variants (not in `src/`; also in `.dev/experiments/346-validation/phase5/final-bundle/builds/`): `spec-panel-{armb,diffgate,ledger,ponytail,stoprule}.md`, `sc-review-ledger` (`review_ledger.py` 2668, verify-only, `PROFILES`), `sc-spec-panel-stoprule-protocol` (`stoprule.py` 2050), `sc-diffgate`, `sc-fix-audit`, agent `finding-grader.md` 35. Bundle `SNAPSHOT-STATE.txt`: no valid-success verdict.
- Tests pinning loop and rf-qa text: `tests/skills/test_spec_panel_review_loop.py` 174, `test_review_loop_extension.py` 127, `test_review_severity_mapping.py` 145, `test_review_severity_rule.py` 520, `test_review_prompt_overrides.py` 283, `test_review_brief_placement.py` 140.

### Consumers and future consumers (slice 05 sections 1B-1D)
- `src/superclaude/skills/sc-workflow-protocol/SKILL.md` Wave 4 (:89, reflect `--mode pre`, advisory); `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` Stage 10.5 (:1619-1638) and phase post gate (:1162); `sc-brainstorm-protocol`, `commands/design.md` (no review hook).
- PR review: `src/superclaude/skills/sc-pr-submit-protocol/refs/{finding-verify.md,severity-routing.md}`, `src/superclaude/pr_submit/{models.py,reviewers.py,fsm.py,severity_router.py}`; `sc-auggie-review-protocol` (`auggie-prompts.md`, `severity-rubric.md`).
- rf-qa family: `src/superclaude/agents/rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md`; 19 skill files / 521 lines reference them.

## PATTERNS_AND_CONVENTIONS

- **Two stacks, one package** [CODE-VERIFIED slice 02]: v1 decides (findings -> ledger -> merge/ledger verdict); v2 only flags and records (findings_v2 -> card_convert/cluster -> cluster/verify-citations + manifest). v2 imports private v1 names (`_check_flat`, `_ID`, `_blocks_after`, `_HEAD_FINDINGS`, `refs_norm`, `flat`), so v1 limit and regex changes propagate to v2.
- **Panel data, not code, selects models**: templates (`review-panel/1`, `distinct_across_slots`, `apply_to`) plus tier file (`review-tiers/1`, environments, `classes`). Templates bind slots to tiers, not to reviewer roles or lenses.
- **Prose loops drive the CLI**: spec-panel's Review Loop and reflect §4.3a are orchestrator prose. E1 found the main shadow failures were prose-following lapses (troubleshoot REPORT); E2 found the same class of problem (the brief does not name source.md; 156/665 source-blind runs).
- **Contract pinning by tests**: reflect contract 1.8.0 pinned byte-for-byte (C1, but against HEAD), allowed-section diff test (C6), `panel_lint` field lists; loop and rf-qa wording pinned by `tests/skills/test_review_*`.
- **Reviewer read-only allowlists** (`reflect-reviewer.md` tools line); the E2 runner disallows Edit/Write/NotebookEdit but allows Bash under bypassPermissions.
- **Shadow pattern**: legacy authoritative; the new engine writes side artifacts and telemetry only; exit criteria aggregated by a script (`reflect_shadow_exit.py`).
- **Evaluation pattern (E2)**: fixed GT per package, blind Opus judge over anonymised merged reports, permutation tests, audits as separate passes, observed-model identity from `claude -p` JSON.
- **Severity vocabularies differ** (slice 05 section 4): findings-v1 CRITICAL/MAJOR/MINOR; reflect HIGH/MEDIUM/LOW plus 4 deviation classes; rf-qa CRITICAL/IMPORTANT/MINOR; Auggie/PR Critical/High/Medium/Low/Nit; pragmatic output style blocking/minor/Medium.
- Conventions binding the design: `src/superclaude/` is the source of truth; never stage `.claude/` except settings.json; installed primitives never reference `src/superclaude/...`; uv only; PRs only to IronbellyOrg/IronClaude via `/sc:pr-submit --monitor 3`; worktrees only via Orca with an agent.

## SOLUTION_RESEARCH

This is a design-unification study; candidate solution shapes already exist in the three efforts. Approaches to evaluate in Phase 2 and Section 6:
1. **Finding contract**: (a) findings-v2 as the single contract with v1 as a strict subset; (b) a new superset with pluggable `lens`/`category` namespaces, anchor OR citation OR path+line(+in_diff) locations, and a severity scale with per-consumer mapping; (c) keep both with adapters. Limit policy for D1: reject (today), truncate with a counter (card_convert already truncates claims), or no limits.
2. **Merge and verdict**: (a) #346 re-find ledger (`ledger.py`); (b) find-once verify-only ledger (experiment `review_ledger.py`); (c) sc-adversarial Mode A debate (reflect legacy); (d) script merge plus blind grader (`finding-grader`, stoprule); (e) calibrator-weighted cluster vote. Blocking rule options: single-reviewer veto (D4, current), quorum, calibrator, grader. Evidence: E2's 65 vs 38 and wrong-blocker data; E1's 0/689 numeric calibrations.
3. **Clustering**: anchor union-find (v1, transitive chaining D6, 83 mega-rows) vs path-aware `cluster_v2` ("section always empty" over-merge; AI-labelled precision 0.84 / recall 0.95, human labels pending). Option: one clusterer over anchors, citations and path+line with chain detection and complete-link or size caps.
4. **Panel resolution and identity**: strict distinct by default vs soft; class map from the tier file; observed identity check (E2 runner) vs pinned (`model:` copied from `panel/resolution.json`, E1 fix) vs both; gateway vs anthropic-only environments; role-bound slots (security, architecture, structural QA) for PR review and rf-qa.
5. **Run recording**: `review-panel-manifest/1` (E1) vs review-telemetry/1 (E3) vs E2's meta.json/cost.json/fallback.log; audits A and D (dropped-finding counter, report-sha vs ledger, chain-size flag, identity re-derivation) as built-in checks.
6. **Rollout**: generic shadow harness (E1 `shadow-standalone-evaluation.md:100-123` extraction plan) vs per-consumer flags; E2 GT packages plus judge as a regression benchmark.
Web research (Phase 4) supplies external evidence on multi-reviewer aggregation, severity harmonization, LLM-judge calibration and code-finding fingerprinting.

## RECOMMENDED_OUTPUTS

| Path (under `${TASK_DIR}`) | Purpose |
|---|---|
| `research/01-finding-contract.md` ... `research/12-test-pins-regression.md` | Phase 2 deep research files (one per agent, see SUGGESTED_PHASES) |
| `research/web-01-panel-aggregation.md` ... `research/web-04-finding-fingerprinting.md` | Phase 4 web research files |
| `gaps-and-questions.md` | compiled gaps after Phase 3 |
| `reviews/adversarial/<conflict-slug>/proposal-a.md`, `proposal-b.md` and the `/sc:adversarial` output folder | written proposals and debate results for conflicts the evidence does not decide |
| `synthesis/synth-01-problem-current-state.md` | Report S1 Problem Statement, S2 Current State incl. **(a) component overlap matrix** (rows = components: finding contract, severity scale, parser limits, clustering, merge/ledger, verdict/blocking, calibration, panel templates, tier/class config, identity check, dispatch, brief/input contract, run manifest, telemetry, audits, shadow harness, evaluation harness, tests; columns = E1 / E2 / E3 with same-purpose, same-contract, same-code and divergent-choice flags) |
| `synthesis/synth-02-target-gaps.md` | S3 Target State, S4 Gap Analysis incl. D1-D16 status and **(e) blockers for PR review and rf-qa replacement** |
| `synthesis/synth-03-external-findings.md` | S5 External Research Findings |
| `synthesis/synth-04-options-conflicts.md` | S6 Options Analysis = **(c) conflict log**: every disagreement (finding schema and severities, anchor handling at merge incl. the 200-char drop, model and tier configuration, distinctness, who judges, calibration, run recording, identity, dispatch, brief/input, merge path and contract bump, D1-D16) with options, evidence and recommended resolution; adversarial results embedded where used |
| `synthesis/synth-05-recommendation-architecture.md` | S7 Recommendation = **(d) target architecture** (shared core: finding contract, panel resolution, run manifest, clustering and citation checks, calibration, merge, telemetry; thin modules: reflect, workflow tasklist review, spec review for brainstorm/design, PR code review, rf-qa replacement) and **(e) future-use-case exposure list** (lenses, categories, roles, templates, model-role mapping the core must expose so new consumers need no core change) |
| `synthesis/synth-06-value-migration-plan.md` | S8 Implementation Plan = **(b) value inventory** (every finding, lesson, strategy, defect, script, test and artifact from E1/E2/E3 mapped to a destination in the design or an explicit drop with a reason), migration path for reflect shadow and the tasklist panel onto the core, no-regression gate list (suites, byte-identical contract 1.8.0, ledger and spec-panel behaviour), branch-structure options with the git ref-naming constraint stated, risk register inputs. NO roadmap and NO `/sc:workflow` run |
| `synthesis/synth-07-questions-evidence.md` | S9 Open Questions, S10 Evidence Trail |
| `RESEARCH-REPORT-review-panel-unification.md` | final assembled report |
| `qa/*` | gate reports per the SKILL.md output table |

## SUGGESTED_PHASES

### Phase 2: Deep investigation (12 parallel codebase agents; each reads its named scope slices first, then the files)

| # | Type | Topic | Files / directories | Output |
|---|---|---|---|---|
| 1 | Code Tracer + Integration Mapper | **Finding contract unification**: field-by-field superset of findings-v1, findings-v2, reflect cards (4 shapes), spec-panel ledger rows, `pr_submit/models.py` `Finding`, Auggie schema (`auggie-prompts.md`), rf-qa/rf-qa-qualitative report format; every validator rule that rejects a code-review or rf-qa finding; limit policy for D1 (200/300 literals in `findings.py` and `card_convert.py:85-86`); D5, D9, D10; v1 prior-line and empty-block rules vs v2 | `src/superclaude/cli/review/{findings.py,findings_v2.py,card_convert.py}`, `src/superclaude/pr_submit/models.py`, `src/superclaude/skills/sc-auggie-review-protocol/`, `src/superclaude/agents/{rf-qa.md,rf-qa-qualitative.md,reflect-reviewer.md}`, `src/superclaude/rules/prompts/document_review_loop_prompts.md`; slices 02 s2, 03 s3, 05 s4 | `research/01-finding-contract.md` |
| 2 | Code Tracer | **Ledger, merge and verdict mechanics**: full read of `ledger.py`, `merge_cmd.py`, `ledger_cmd.py`; experiment `review_ledger.py` verify-only and `PROFILES`; stoprule computed verdict; D2, D3, D4, D16 with exact lines; the 49 blocking findings lost at merge and 3 vs 4 verdict flips (E2 audit D); can `merge_round` accept v2 citations | `src/superclaude/cli/review/{ledger.py,merge_cmd.py,ledger_cmd.py}`, `~/.claude/skills/sc-review-ledger/scripts/review_ledger.py`, `~/.claude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py`, `E2:analysis/audits/audit-D/`; slices 01 s2, 02 s5 | `research/02-ledger-merge-verdict.md` |
| 3 | Code Tracer + Pattern Investigator | **Clustering**: `findings.cluster` (union-find, D6 chaining, E2's 83 mega-rows) vs `cluster.cluster_v2` (full read :184-447; support, chained, uncalibrated, `clusters_kept`; "section always empty" over-merge); shared D7 regex vs ids `T01.02`, `AC-...`; E1 pair precision/recall (AI labels) and pending hand labels; design input for one clusterer over anchors, citations and path+line | `src/superclaude/cli/review/{findings.py,cluster.py,cluster_cmd.py,verify_cmd.py}`, `.dev/tasks/done/TASK-WF-implementStages0-20261111-202912/artifacts/{cluster-v2-known-weaknesses.md,pair-labels/,stage0a-report.md}`, `scripts/reflect_cluster_pairs.py`; slices 01, 02 s3, 04 | `research/03-clustering.md` |
| 4 | Architecture Analyst | **Panel resolution, tiers, identity and dispatch**: full read of `panel.py` :137-500; templates; tier file and `classes`; D11 soft distinct, D12 `$T3Model01`; strict distinct vs E2 best panels (2x same model, mixed vendors); gateway `launch: {}` vs anthropic-only; E2 observed-identity check and `expected_model` overwrite bug; E1 dispatch collapse, haiku slot served by gpt-6.1-sol, `model_observed` fix (9874d63fb); role/lens-bound slots for future consumers; date-stamp all model evidence | `src/superclaude/cli/review/{panel.py,panel_cmd.py,data/*.json}`, `E2:tools/run-reviewer.sh`, `src/superclaude/skills/sc-reflect-protocol/SKILL.md` §4.3a/§7.1, `.dev/eval-workspaces/shadow-model-combos/{FINDINGS.md,results.md}`, `.dev/troubleshoot/shadow-failures-20261113014240/REPORT.md`; slices 01 s2-4, 02 s4, 04 | `research/04-panel-resolution-identity.md` |
| 5 | Code Tracer | **Blocking policy per lens and calibration as a panel role**: `cli/reflect/contract.py` `derive_verdict`; deviation taxonomy -> blocking; `card_convert` MEDIUM-drift and two-word label defects; `confidence-calibrator.md` (6-dim troubleshoot rubric) vs reflect 5-dim rubric; class-disjoint rule (§11.3) vs id-based distinctness; 0/689 numeric calibrations; `finding-grader` B1-B3; E2 single-reviewer veto evidence (65 vs 38, wrong blockers); the two blocking rules on master (prose consequence rule vs `findings_v2.py:161-162`) | `src/superclaude/cli/reflect/contract.py`, `src/superclaude/skills/sc-reflect-protocol/{SKILL.md,refs/reflection-rubric.md,refs/deviation-taxonomy.md}`, `src/superclaude/agents/confidence-calibrator.md`, `~/.claude/agents/finding-grader.md`, `src/superclaude/cli/review/{card_convert.py,findings_v2.py,cluster.py}`, `src/superclaude/commands/spec-panel.md`; slices 01, 03 s2-4 | `research/05-blocking-calibration.md` |
| 6 | Doc Analyst + Code Tracer | **Driving-document input contract and briefs**: D8 (brief does not name source.md; 156/665 source-blind runs), E1 W-3 spec:N vs short source.md, parsed-sparse escalation, only the qa persona gets spec hunks, reviewer-spec three-section brief, `{{SOURCE}}` placeholder; one brief template plus grounding-hunk injection shared by reflect, tasklist, spec and PR review; reviewer read-only enforcement (Bash allowed in the E2 runner) | `src/superclaude/rules/prompts/document_review_loop_prompts.md`, `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md`, `E2:tools/run-reviewer.sh`, `E2:<pkg>/candidate.md`, recorded `.dev/reflect/*shadow*/reviewer-briefs/`, `src/superclaude/agents/reflect-reviewer.md`; slices 01, 03, 04 | `research/06-input-contract-briefs.md` |
| 7 | Architecture Analyst | **Reflect merge path and contract constraints**: debate (sc-adversarial Mode A) vs script merge for Stage 3; `merge_method` values and the contract-bump rule (C3); EV-1; constraints C1-C16 with what each blocks; HEAD-relative pins C1/C6; UC-2 `reflect-post` readiness; Stage 2 exit status | `src/superclaude/skills/sc-reflect-protocol/SKILL.md` §9.1-9.2, `src/superclaude/cli/reflect/panel_lint.py`, `tests/cli/reflect/*`, `.dev/reflect/pre-*-shadow*/adversarial/`, `scripts/reflect_shadow_exit.py`; slice 03 s5 | `research/07-reflect-merge-contract.md` |
| 8 | Code Tracer | **Run recording: manifest, telemetry, audits**: `manifest.py` stages/attempts/hashes; `telemetry.py` records, strata (D15), kinds; reflect `telemetry:` block (§9.2); E2 meta/cost/fallback files; audits A and D logic as built-in checks; cost and time per reviewer; combo `extract.py` fields | `src/superclaude/cli/review/{manifest.py,manifest_cmd.py,telemetry.py,telemetry_cmd.py}`, `E2:analysis/audits/audit-{A,D}/`, `.dev/eval-workspaces/shadow-model-combos/analysis/extract.py`, `scripts/reflect_shadow_exit.py`; slices 01 s3, 02 s6-7 | `research/08-run-recording-telemetry.md` |
| 9 | Integration Mapper | **Consumer plug points and CLI surface**: workflow Wave 4 (reflect pre, advisory), tasklist Stage 10.5 and phase post gate, brainstorm and design (no hook; artifact and id convention), spec-panel loop prose and its single CLI paragraph, prose-only fallback without the Python CLI; D13 loader, D14 no in-repo caller of merge/ledger/resolve; whether reflect pre escalates to Tier 2 by default | `src/superclaude/skills/{sc-workflow-protocol,sc-tasklist-protocol,sc-brainstorm-protocol}/SKILL.md`, `src/superclaude/commands/{design.md,spec-panel.md}`, `src/superclaude/cli/review/__init__.py`, `src/superclaude/rules/prompts/document_review_loop_prompts.md`; slice 05 s1B-2 | `research/09-consumer-plugpoints.md` |
| 10 | Integration Mapper | **Future consumers**: PR review seam (`pr_submit` FSM S2-S3, `finding-verify.md`, `severity-routing.md`, `severity_router.py` in_diff tier drop and missing `error-handling` row, Augment/Codex `source` agreement -> ledger confidence); rf-qa / rf-qa-qualitative / rf-analyst call-site census across the 19 skill files (phase, inputs, fix authorization, verdict format; which need in-place fixing a read-only panel cannot do); what the core must expose (lenses, categories, roles, templates, model-role mapping) | `src/superclaude/skills/sc-pr-submit-protocol/refs/*`, `src/superclaude/pr_submit/{fsm.py,reviewers.py,severity_router.py,models.py}`, `src/superclaude/skills/sc-auggie-review-protocol/`, `src/superclaude/agents/rf-*.md`, Grep `rf-qa` over `src/superclaude/skills/`; slice 05 s1C-3 | `research/10-future-consumers.md` |
| 11 | Pattern Investigator + Doc Analyst | **Evaluation harnesses and evidence**: E2 harness as a regression benchmark (GT format, blind judge `judge-one.sh` with no source.md, anonymisation, `final-table.py`, `three-way.py`; about 115k judge tokens per scoring; source.md not committed); E1 shadow harness generalization (`shadow-standalone-evaluation.md:100-123`); Stage 2 failure classification for shadow runs 08-15 after fixes 9874d63fb/c2e3347d3 (run `uv run python scripts/reflect_shadow_exit.py`, read-only); combo study leads (speed, confidence, compliance); E2 headline results (about 2-2.5 of 14 defects found, no panel significantly better, ember + 2x luna default); experiment-bundle verdicts (`.dev/experiments/346-validation/phase5/final-bundle/reports/phase5/`) | `E2:tools/`, `E2:analysis/`, `E2:COMBO-REPORT.md` :289+, `E2:PILOT-REPORT.md`, `.dev/tasks/done/TASK-WF-implementStages0-20261111-202912/artifacts/shadow-standalone-evaluation.md`, `.dev/reflect/*shadow*`, `.dev/eval-workspaces/shadow-model-combos/`, `.dev/experiments/346-validation/phase5/final-bundle/`; slices 01, 04 | `research/11-evaluation-evidence.md` |
| 12 | Code Tracer | **Test inventory and pin migration**: the 651 `tests/review` tests by file and stack; tests pinning defects (D3 `test_review_ledger.py:376`, D5 `:408`, D11 `test_review_panel_exclusion.py:208`); golden fixtures (`panel-golden-*.json`, `review-tiers.frozen-1.0.0.json`); reflect pins C1/C6/C7/C8 and `panel_lint` lists; `tests/skills/test_review_*` and `test_spec_panel_review_loop.py` pins on loop and rf-qa text; proposed no-regression gate list and which tests must change on purpose | `tests/review/`, `tests/cli/reflect/`, `tests/skills/test_review_*.py`, `tests/skills/test_spec_panel_review_loop.py`; slices 02 s6, 03 s5, 05 s1A | `research/12-test-pins-regression.md` |

Every Phase 2 agent: read `research/scope/00-handoff-copy.md` and the slices named in its row before the source files; tag doc-sourced claims [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED]; record for each item which effort (E1/E2/E3) it came from, so the overlap matrix and value inventory can be built by meaning; read E2 files with `git show 4a22d74213f93837d00c2c314075dd967b9a98e3:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/<path>`; modify no file outside its own output path.

### Phase 4: Web research (4 parallel agents)

| # | Topic | Context from codebase | Output |
|---|---|---|---|
| W1 | Multi-reviewer LLM panel aggregation: quorum vs veto vs judge, ensemble code review, LLM juries, duplicate-finding consolidation | D3/D4 single-reviewer veto, E2 65 vs 38 blocking result, reflect debate merge | `research/web-01-panel-aggregation.md` |
| W2 | Severity taxonomies and harmonization: SARIF `level`/`rank`, CodeQL/Semgrep severities, code-review severity conventions, mapping between 3- and 5-level scales | five vocabularies in slice 05 s4 | `research/web-02-severity-harmonization.md` |
| W3 | LLM-as-judge and calibration: self-preference and same-family bias, blind grading, reliability of verbalized confidence | class-disjoint calibrator rule, 0/689 numeric calibrations, E2 blind Opus judge | `research/web-03-judge-calibration.md` |
| W4 | Finding location and fingerprinting across revisions: SARIF `partialFingerprints`, GitHub code scanning alert matching, line drift between commits | anchor vs citation vs path+line clustering for PR review | `research/web-04-finding-fingerprinting.md` |

### Phase 5: Synthesis (7 parallel agents) + adversarial step + synthesis QA gate

| Synth file | Report sections | Source research files |
|---|---|---|
| `synthesis/synth-01-problem-current-state.md` | S1, S2 incl. overlap matrix (a) | research 01-12, scope slices, gaps log |
| `synthesis/synth-02-target-gaps.md` | S3, S4 incl. defect status and future-consumer blockers (e) | research 01-12, web 01-04, gaps log |
| `synthesis/synth-03-external-findings.md` | S5 | web 01-04 |
| `synthesis/synth-04-options-conflicts.md` | S6 conflict log (c) | research 01-12, web 01-04, gaps log, adversarial outputs |
| `synthesis/synth-05-recommendation-architecture.md` | S7 target architecture (d) + exposure list (e) | research 01-12, web 01-04, synth-04 |
| `synthesis/synth-06-value-migration-plan.md` | S8 value inventory (b), migration path, no-regression gates, branch-structure options | research 01-12, scope slices 01-05 (every inventory item), synth-04, synth-05 |
| `synthesis/synth-07-questions-evidence.md` | S9, S10 | all gaps, all research and web file paths |

**Adversarial step (between synth-04 and synth-05, per the owner's request):** for each conflict synth-04 marks `UNDECIDED-BY-EVIDENCE`, write two design proposals to `${TASK_DIR}reviews/adversarial/<conflict-slug>/proposal-a.md` and `proposal-b.md`, then run `/sc:adversarial --compare <proposal-a> <proposal-b> --depth standard --focus correctness,risk,test-coverage --output ${TASK_DIR}reviews/adversarial/<conflict-slug>/` (one item per conflict), and write the result back into synth-04's conflict row before synth-05 runs. If synth-04 marks no conflict undecided, record "no adversarial run needed" with the reason.

## TEMPLATE_NOTES

Template 02 (complex task): discovery, parallel agents, multi-gate QA, conditional adversarial step. QA intensity: full (Deep tier). Phase 3 partitioning applies (12 research files > 6); Phase 5 partitioning applies (7 synth files > 4). Phase 6 Gate 3 full (9-13 lens agents), Gate 4 fidelity with 3-4 agents (source > 1000 lines), Gate 5 anti-omission with 3-4 agents. Phase 7 must NOT run `/sc:workflow` and must NOT suggest a roadmap step; it ends by presenting the report (owner scope change).

## AMBIGUITIES_FOR_USER

None that block this run. Recorded for the report's Open Questions instead of asking now:
- Which installed-only experiment variants (ledger verify-only, stoprule grader, diffgate, fix-audit) to promote; the bundle has no success verdict.
- Target environment for the central panel: anthropic-only (reflect gate) vs gateway (E2 best panels).
- Whether workflow tasklist review stays advisory (reflect pre) or becomes blocking.
- Ownership of `cli/review/` (#346 owners vs reflect work).
- Stage 0 exit depends on hand labels (issues #525-#530), not available yet.
- E2 inputs are taken at 4a22d742; the other session is producing a second report that will be merged later, so differences are expected and resolved in that merge, not here.
- [CODE-CONTRADICTED] items already found in scope discovery: the hand-off says only the bundle holds the experiment variants (they are also installed in `~/.claude/`); audit summaries exist only for A and D; audit D names 3 verdict flips, not 4; the once-found issue is alias GT1 (B6); stale line numbers for D7/D11/D12; `ledger.merge_round` docstring contradicts D2 behaviour.

**Status:** Complete
