# Research Notes: Unified central Review Panel (run 2)

**Date:** 2026-11-14
**Scenario:** A (explicit request: goal, source locations, output shape and constraints all given by the owner)
**Depth Tier:** Deep
**Status:** Complete
**Sufficiency review (A.5), 2026-11-14:** passed in 0 gap-fill rounds. (1) key files have exact paths (section EXISTING_FILES and the 12 slices); (2) 24 research assignments name topic, inputs, open items and output path; (3) the synthesis mapping table links every report section to research files; (4) no ambiguity blocks the builder; (5) solution approaches are listed in SOLUTION_RESEARCH; (6) every [CODE-CONTRADICTED] and [UNVERIFIED] claim is flagged in AMBIGUITIES_FOR_USER.
**Task folder:** `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/`
**Scope-discovery inputs:** 12 slice files in `research/scope/` (all Status: Complete), 6,709 lines in total (`wc -l`, 2026-11-14 08:12)

---

## EXISTING_FILES

Conventions used below: `TD` = the task folder. `HEAD` = this worktree at `50d4d2b9d` (branch `ironbelly/shadow-runs`; the review code equals `origin/master` `d2d8a2d16`, PR #519). `E2-TIP` = `origin/ironbelly/eval-tasklist-review-panel` at `6c0984326cbb8fb06c4a36065de58b171d3f8175` (read only with `git show` / `git ls-tree`; the earlier hand-off commit `4a22d74213f93837d00c2c314075dd967b9a98e3` is its ancestor). Every scope slice is at `TD research/scope/NN-*.md` and holds the exact file:line inventory for its area; Phase 2 agents start from the slice named in each assignment.

### A. Scope slices (the discovery output; every Phase 2 agent reads the slices it is assigned)

| Slice | File (under `TD research/scope/`) | Lines | Covers |
|---|---|---|---|
| 01 | `01-run2-handoff.md` | 563 | E2 run-2 hand-off (543 lines) vs run-1 hand-off (315 lines): 11 form differences, 15 corrections (C1-C15), 12 dropped items (L1-L12), 8 numeric disagreements; code claims checked at HEAD (D1-D13, P1-P7, T1-T2, B-1..B-7 all VERIFIED) |
| 02 | `02-run-comparison-and-notes.md` | 632 | `HANDOFF-run1-vs-run2.md` (67 lines) and the six per-run notes (R1CM 66, R1CP 100, R1TT 13, R2CM 160, R2CP 195, R2TT 137): 16 agreements, 13 disagreements, about 360 coded entries, conflicts C-S1..C-S16, exposures FX-1..FX-22 |
| 03 | `03-e2-study-reports-tools.md` | 576 | E2 study `20261111-a1`: PILOT-REPORT (83), COMBO-REPORT (506), manifest (16), `combos/SPEC.md` (152), `tools/` (3 harness files + 55 tmp-scripts); 17 code claims checked, 10 product defects, 19 harness defects, 20 lessons |
| 04 | `04-e2-study-analysis-audits.md` | 353 | `analysis/` (about 130 files) and audits A-F (only A and D have a `summary.md`); defects found: `fullpkg()` bug in `final-table.py`, batch j1 in no audit; value items V1-V30 |
| 05 | `05-brainstorm-panel-collaboration.md` | 720 | E2 brainstorm `20261113-163248-panel-collaboration/` (58 blobs, 1,055,384 B): seed brief, merged requirements (1,130 lines), 5 variants, enrichment, adversarial run; 47 requirements R-01..R-47, 43 diff points, 33 invariants |
| 06 | `06-brainstorm-process-redesign.md` | 687 | E2 brainstorm `20261113-223124-panel-process-redesign/`: merged requirements (1,254 lines), two redesigns (Sweep Sheet, Recipe Ledger), classes C1-C8, X1-X7, gates G0 and D1-D7 |
| 07 | `07-collab-r1-r2.md` | 440 | E2 `20261113-collab/r1-move-radar` and `r2-idle-shift-sweeper` (design + harness; 138 and 358 claimed passing tests; no quality evidence) |
| 08 | `08-collab-r3-r4-r5.md` | 758 | E2 `r3-axis-flip-challenge`, `r4-flag-and-adjudicate`, `r5-coverage-deflection` (89 + 106 + 108 = 303 claimed tests; engine `lib/` absent from the commit because `.gitignore:13` ignores `lib/`) |
| 09 | `09-review-package-code.md` | 473 | `src/superclaude/cli/review/` (16 modules, 5,086 lines, 19 test modules): v1 loop + v2 reflect kernel; 31 verified defects D-1..D-31 (7 reproduced by a read-only run); K-1..K-15 keep list |
| 10 | `10-reflect-side.md` | 606 | reflect: `sc-reflect-protocol/SKILL.md`, `cli/reflect/` (10 modules), 2 agents, 5 scripts, 38 test files; shadow-exit result `OVERALL: FAIL (shadow runs 13 of 20)`; two Tier-2 implementations; R-01..R-22 constraints |
| 11 | `11-e1-evidence-artifacts.md` | 395 | E1 evidence: 15 pilot shadow dirs + 15 combo dirs, Stage 0a report, troubleshoot report, thresholds T-1..T-10, AI-label check; 22 defects X-1..X-22 |
| 12 | `12-e3-loop-variants-consumers.md` | 506 | E3: shipped #346 loop, 5 installed-only variants (17 files, 4 scripts totalling 7,589 lines), phase-5 bundle, and the consumers (tasklist, workflow, brainstorm, design, pr_submit, auggie-review, rf-qa family) |

### B. E1 (this branch, `ironbelly/shadow-runs`)

| Path | What it is | Size / count (source) |
|---|---|---|
| `src/superclaude/cli/review/` | review package: `findings.py`, `findings_v2.py`, `ledger.py`, `ledger_cmd.py`, `merge_cmd.py`, `cluster.py`, `cluster_cmd.py`, `verify_cmd.py`, `card_convert.py`, `panel.py`, `panel_cmd.py`, `manifest.py`, `manifest_cmd.py`, `telemetry.py`, `telemetry_cmd.py`, `__init__.py` + `data/` | 16 modules / 5,086 lines (slice 09); `panel.py` 707 lines, `panel_cmd.py` 129 at HEAD (slice 02) |
| `src/superclaude/cli/review/data/` | `review-tiers.default.json` (now with a `classes` map), 9 packaged panel templates incl. 6 `reflect-*` templates | slice 09, 12 |
| `tests/review/` | 19 test modules pinning the review package (several pin defects as intended behaviour: D-1, D-2, D-3, D-5, D-6, D-11, D-25, D-26) | slice 09 |
| `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (+ `refs/`) | reflect protocol; Tier 2 panel path and `--t2-engine shadow` exist as prose here | about 2,033 lines; shadow text at `:87, :338-349` (slice 01, 02, 10) |
| `src/superclaude/cli/reflect/` | code-driven Tier 2: `runner.py`, `ensemble.py`, `contract.py`, `panel_lint.py`, `config.py`, `commands.py`, `models.py`, `_diversity`, `fallback.py` (594 lines) | 10 modules (slice 10) |
| `src/superclaude/agents/reflect-reviewer.md`, `confidence-calibrator.md` | read-only reviewer (no Bash) and 6-dimension calibrator | slice 10 |
| `scripts/reflect_*.py` | `reflect_shadow_exit.py`, `reflect_stage0a_replay.py`, `reflect_cluster_pairs.py`, `reflect_verdict_replay.py`, `reflect_consumer_inventory.py` | 5 scripts (slice 10, 11) |
| `tests/cli/reflect/` | reflect tests incl. contract 1.8.0 pins, 36-test verdict matrix | 38 files; 352 passed + 1 xpassed (slice 10) |
| `.dev/reflect/pre-*` and `*shadow*` | 15 pilot shadow run dirs and 91 `pre-*` dirs scanned by Stage 0a | slice 11 |
| `.dev/eval-workspaces/shadow-model-combos/` | 5x3 model-combination experiment: PLAN.md, FINDINGS.md, results.md, combos.json, analysis/, runs/ | 15 combo runs, 3/3 reviewers complete in all (slice 11) |
| `.dev/troubleshoot/shadow-failures-*/` | troubleshoot REPORT.md for the shadow failures | slice 11 |
| `docs/memory/reflect/` | memory files (one untracked at HEAD: `deviation-patterns-brainstorm-reflect-panel.md`) | slice 10, 11 |

### C. E2 (`E2-TIP`, read only through git)

| Path (under `.dev/` unless noted) | What it is |
|---|---|
| `eval-workspaces/tasklist-review-panel/HANDOFF-review-panel-unification.md` (315 lines), `...-run2.md` (543 lines), `HANDOFF-run1-vs-run2.md` (67 lines), `handoff-notes/run1/`, `handoff-notes/run2/` | hand-offs and per-run notes (slices 01, 02) |
| `eval-workspaces/tasklist-review-panel/20261111-a1/` | original study: reports, `combos/` (97 tracked entries), `tools/`, `analysis/`, `audits A-F`, GT; 9,312 files; raw transcripts (1.48 GB, 2,916 files) are off-repo (slices 03, 04) |
| `eval-workspaces/tasklist-review-panel/20261113-collab/r1..r5/` | five collaboration design + harness packages (slices 07, 08) |
| `brainstorms/20261113-163248-panel-collaboration/` | requirements brainstorm and nested adversarial run (slice 05) |
| `brainstorms/20261113-223124-panel-process-redesign/` | process redesign brainstorm and nested adversarial run (slice 06) |

### D. E3 (master #346 loop plus installed-only variants)

| Path | What it is |
|---|---|
| `src/superclaude/commands/spec-panel.md` (`:256-268`) and `src/superclaude/rules/prompts/document_review_loop_prompts.md` (`:31`, `:58-70`) | shipped Review Loop text; rubric with the "Medium" rule |
| `~/.claude/skills/sc-review-ledger/`, `sc-spec-panel-stoprule-protocol/`, `sc-diffgate/`, `sc-fix-audit/`; `~/.claude/agents/finding-grader.md`; `~/.claude/commands/sc/spec-panel-{ledger,stoprule,diffgate,ponytail,armb}.md` | 17 installed-only variant files, byte-identical to the install log (2026-11-08); in the repo only as archives under `.dev/` (slice 12) |
| `.dev/experiments/346-validation/phase5/` | FINAL-REPORT, SNAPSHOT-STATE, `final-bundle/` (7,909 lines of archived tests); "Convergence not proven; no validated winner" (slice 12) |
| `.dev/research/346-review-loop-experiments/` | 6,523 tracked files; NOT read by any slice (slice 12 gap 2) |

### E. Consumers (each has its own review path today; slice 12)

`src/superclaude/skills/sc-workflow-protocol/SKILL.md` (Wave 4 at `:85-89`), `sc-tasklist-protocol/SKILL.md` (Stage 10.5; per-phase post gate near `:1630`), `sc-brainstorm-protocol/`, `src/superclaude/commands/design.md`, `src/superclaude/pr_submit/` (`reviewers.py`, `fsm.py`, `severity_router.py`, `models.py`, `classifier.py` 618, `conflicts.py` 1,659, `merge_guard.py` 605), `src/superclaude/skills/sc-auggie-review-protocol/`, rf-qa family (`src/superclaude/agents/rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md`; slice 12's "185 U2 spawn lines over 7 skills" [CODE-CONTRADICTED: research/13 and a fix-cycle-1 re-run give 175 prose spawn lines over 7 skills, 247 per line-and-agent; use 175], 44 `subagent_type: rf-*` lines over 8 skills in SKILL.md), `src/superclaude/cli/tasklist/`, `cli/roadmap/`, `cli/swarm` (8-lens registry), `sc-implement-protocol/refs/qa.md:11` (forbids panels).

### F. Repository rules that bind the unification (read from `CLAUDE.md`, not from a slice)

`.claude/{skills,commands,agents,hooks,templates}/*` is gitignored sync-dev output of `src/superclaude/` (edit `src/`, then `make sync-dev`, check `make verify-sync`); installed primitives must never name `src/superclaude/...` paths; PRs go only to the fork `IronbellyOrg/IronClaude` through `/sc:pr-submit --monitor 3`; worktrees only through Orca with an agent; uv only for Python.

## PATTERNS_AND_CONVENTIONS

Tags: [CODE-VERIFIED] = a slice read the code; [CODE-CONTRADICTED] = a slice found code that differs from a claim; [UNVERIFIED] = not checked. Evidence is in the cited slice; Phase 2 agents re-verify before the report cites it.

### Structural patterns found across the three efforts

1. **Two disjoint review pipelines inside one package.** v1 (E3: `findings.py` anchor-quote findings, `ledger.py`, `merge_cmd.py`, `telemetry.py`) and v2 (E1: `findings_v2.py` path:line citations, `card_convert.py`, `cluster.py`, `verify_cmd.py`, `manifest.py`). They share only the block container, the `refs_norm` helper, `_ID` and `panel.py`. There is no code path from v2 findings to the ledger (slice 09 D-12) [CODE-VERIFIED].
2. **The shared v1 sites are the same in E1, E2-TIP and master for `findings.py`, `ledger.py`, `merge_cmd.py`** (sha256 identical, slice 08) so E2's evidence about drop-and-warn applies to E1's code. findings-v2 inherits the 200/300-character limits through `_check_flat` (`findings_v2.py:15-22`), so the whole-finding drop (D1) exists in both parsers at HEAD [CODE-VERIFIED, slices 01, 02, 09].
3. **Spec-shaped hard-coding.** Reference-id regex (`findings.py:29` `_REF_TOKEN`, `telemetry.py:23` `_ID_TOKEN`, both checked by the orchestrator against the code on 2026-11-14; neither fits tasklist ids `T01.01`; slice 01 names `telemetry.py:23` as `_REF_TOKEN`, which is wrong), category set (`findings.py:15-22`), brief placeholders, per-target defaults, telemetry strata (sonnet/haiku) (slices 01, 09). Each is a place a shared core must expose, not copy.
4. **Tier/profile data drives panels** (`review-tiers.default.json`, `panel.py` profiles incl. `reflect-*`, `validate_reflect_profile` at `panel.py:80-136`; reflect profile launch limited to sonnet/opus/haiku, max 3 reviewers; gateway env has `launch: {}` "not defined yet" for non-first-slot models; `muse-ember-1.0` absent from the tier data at HEAD) [CODE-VERIFIED, slices 02, 03, 09].
5. **Reflect has two Tier-2 implementations** (prose skill panel with calibrator, evidence validator, executor exclusion, findings-v2; and the Python swarm engine behind `superclaude reflect run`, contract_version "1.0", none of those); only `contract.derive_verdict` is shared (slice 10) [CODE-VERIFIED].
6. **Verdict and ledger models differ per effort**: reviewer-typed verdict (master), script-computed verdict (installed variants, owner ruling in phase 5), reflect's 4-state map, two ledger status machines (`resolved_check` vs `fixed/verified/reopened`), four meanings of "Medium" [CODE-CONTRADICTED: research/12 section 3 and :218 re-derive at least six uses; use six], seven severity vocabularies (slice 12 I1, I3, I4, I6; research/12 counts six label sets plus two orthogonal axes, definition-dependent).
7. **Non-interference is enforced by LLM prose in E1 shadow mode** (7 of 28 counted runs leaked new contract keys; every EV-1/lint failure is a layout or naming failure) (slice 11).
8. **E2's harness shipped without its engine**: `lib/` is gitignored (`.gitignore:13`) so r2 to r5 cannot run from the commit; `runs/` evidence is absent; sandboxes differ (parent commit vs T1-start tree) (slices 07, 08) [CODE-VERIFIED].
9. **Installed-only variants** exist in `~/.claude/` and only as archives in the repo; they shadow nothing and cannot be rebuilt from `src/` (slice 12).
10. **Dispatch by class vs by raw model id**: E1 dispatches by class through the orchestrator's Agent call (collapse to 1 of 3 under tier3, 0 of 12 under tier1b; requested class recorded, not served model); E2 launches `claude -p --model <id>` per reviewer (slices 03, 11).

### Evidence-handling conventions the later phases must keep

- Quote numbers with their unit; the "92 / 80 / 49" merge-drop figures differ by unit (92 findings dropped = all dropped; 80 reviewer-package runs lost findings; 49 blocking) (slices 01, 03, 04, 05) [UNVERIFIED which unit some documents mean].
- Hand-off line cites are exact for `findings.py`, `ledger.py`, `ledger_cmd.py`, `merge_cmd.py`, `telemetry.py`, `telemetry_cmd.py`, reviewer agents; stale for `panel.py` (525 to 707 lines), `panel_cmd.py` (87 to 129), `__init__.py`, `review-tiers.default.json`, reflect `SKILL.md` (+68 lines, cites shifted about +40), workflow `SKILL.md` (Wave 4 now `:85-89`), `MODEL-TIERS.md` (Tier 2b row now `:44`) (slice 02).
- Never cite a number from a slice without the slice's own tag; slice numbers marked [UNVERIFIED] become report claims only after a Phase 2 agent re-derives them.
- Independence: no agent reads `TD/../TASK-RESEARCH-review-panel-unify-*` or `.dev/tasks/to-do/REVIEW-PANEL-UNIFY-RUN2-QUEUED.md`. One slip is on record (slice 03 gap 10): a repo-wide grep printed file NAMES under the run-1 folder; no content was opened or cited.

## SOLUTION_RESEARCH

The goal is a design recommendation, so the report must evaluate approaches. These are the candidates found during discovery. Phase 2 and the synthesis decide among them with evidence; nothing here is a recommendation.

### Decision axes (each becomes a Section 6 option set or a conflict-log entry)

| Axis | Candidates seen in the material | Where the evidence is |
|---|---|---|
| Core shape | (A) v2 kernel as the core: findings-v2 + `cluster` + `verify` + `manifest` + `panel`, with the v1 loop as a thin module; (B) v1 package as the core with reflect as a module; (C) a thin shared contract (finding schema, hashes, run record, eval harness) with per-module engines kept separate; (D) fix the harness and the two parsers only (H1-H4, D1, B-1) and defer unification | slices 01, 02, 09, 10, 12 |
| Finding contract | v1 anchor quotes (E2 R-04), v2 path:line citations with optional `lens`, reflect deviation table, variant ledger rows, E2 `panel-msg/1` with `origin` | slices 05, 07, 08, 09, 10 |
| Limits policy | truncate, reject and re-ask, or keep drop-and-warn (92 findings, 49 blocking lost) | slices 03, 04 |
| Quorum / verdict | one valid reviewer passes (pinned by `tests/review/test_review_ledger.py:376-385`), quorum, or manifest-driven; reviewer-typed vs script-computed vs reflect `derive_verdict` | slices 09, 10, 12 |
| Dispatch | by class through the orchestrator Agent call (E1), raw id per reviewer process (E2), tier alias in the product path | slices 03, 10, 11 |
| Collaboration | none (independent reviewers), static move kit A2 (about +29% elapsed est.; sonnet +59% measured in r5), exchange families F1 axis-flip, F3 move radar, F4 idle-shift sweeper, F6 coverage deflection, F7 flag-and-adjudicate; E2's own spec says a static kit may beat every exchange design and the plan "cannot detect the central estimates of any slot" | slices 05, 07, 08 |
| Process redesign | Sweep Sheet (typed pre-pass items to 2 of 3 reviewers) vs Recipe Ledger (written class recipes by lens), gates G0 and D1-D7, tie to Recipe Ledger | slice 06 |
| Reflect engine | keep both engines, make the swarm engine gain calibrator/validator, or retire it for the skill panel; one convergence threshold (0.75 vs 0.80) and one single-vendor posture | slice 10 |
| Evaluation | shared ground truth (E2 16 defects: 10 GT / 5 blocking on designSpec, alias 4/3, control 2/0), E1 seeded defects (never run), held-out sets; blind judge; audits A-F as a reusable `verify-run` | slices 03, 04, 11 |
| Variants | keep installed-only variants installed, archive them, or fold their ideas (owner counting rule, scoped-PASS coverage statement, fail-closed parsing, provenance of actual model, fix-map per hunk, computed re-review surface) | slice 12 |
| Future modules | PR code review (location type, 18 vs 6 categories, 5 vs 3 severity tiers, cap, third-party reviewers, fork-only rules) and rf-qa replacement (read-write semantics, checklist + confidence gate, 8-lens pack, `/task` lens-gate pattern as a first step) | slice 12 |

### External research planned (web agents, Phase 4)

W1 evidence on multi-model / multi-agent review panels (agreement, position bias, judge reliability, cross-model diversity); W2 Claude Code headless and hook semantics that the collaboration designs and read-only reviewers depend on (`PostToolUse`, `--resume`, `--settings`, subagent tool restrictions, `claude -p` stream output); W3 git branch-name hierarchy (the ref constraint that `feat/review-panel` and `feat/review-panel/<name>` cannot both exist) and stacked-branch/PR practice; W4 finding-schema standards and review-bot practice (SARIF, reviewdog, bot review severity) for the PR-review future use. External findings never override a code-verified fact.

## RECOMMENDED_OUTPUTS

All paths are under `TD` (`.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/`).

| Output | Path | Purpose |
|---|---|---|
| Task file | `TASK-RESEARCH-review-panel-run2-20261114-075454.md` (built by `/task-builder`) | executed by `/task` |
| Build request | `BUILD-REQUEST.md` | input to the builder |
| Scope slices (done) | `research/scope/01..12-*.md` | discovery inventories (feed Phase 2 and the Evidence Trail) |
| Codebase research (18 topic files) | `research/01-overlap-capability-matrix.md`, `02-finding-contract.md`, `03-merge-ledger-verdict.md`, `04-dispatch-identity-tiers.md`, `05-input-delivery-brief.md`, `06-reflect-two-engines.md`, `07-e1-evidence-grading.md`, `08-e2-evidence-grading.md`, `09-collaboration-designs.md`, `10-process-redesign.md`, `11-consumers-tasklist-workflow.md`, `12-consumers-spec-review.md`, `13-future-pr-review-and-rfqa.md`, `14-e3-variants-and-experiments.md`, `15-telemetry-manifest-run-record.md`, `16-eval-governance.md`, `17-defect-register.md`, `18-repo-constraints-and-branching.md` | verified topic findings |
| Value ledgers (6 files) | `research/19-value-ledger-handoffs.md`, `20-value-ledger-e2-study.md`, `21-value-ledger-brainstorms.md`, `22-value-ledger-collab-designs.md`, `23-value-ledger-e1-e3-code.md`, `24-value-ledger-evidence-consumers.md` | every finding, lesson, strategy, defect, script, test, artifact, question from the slices with one destination each (CORE, MODULE-x, EVAL, HARNESS, KNOWLEDGE, DROP with reason); feeds Section 8 and the anti-omission gate |
| Web research (4) | `research/web-01-multi-model-review-evidence.md`, `web-02-claude-code-hooks-headless.md`, `web-03-git-branch-hierarchy-stacked-prs.md`, `web-04-finding-schemas-review-bots.md` | external context |
| Gaps log | `gaps-and-questions.md` | interim gaps and questions from all phases |
| Synthesis (10) | `synthesis/synth-01-problem-current-state.md`, `synth-02-overlap-matrix.md`, `synth-03-target-gaps.md`, `synth-04-external-findings.md`, `synth-05-options.md`, `synth-06-conflict-log.md`, `synth-07-recommendation-architecture.md`, `synth-08-value-inventory.md`, `synth-09-sequence-and-gates.md`, `synth-10-questions-evidence.md` | report sections |
| Conflict debates | `reviews/adversarial/<conflict-slug>/` (one folder per conflict the evidence cannot decide, each with `proposal-a.md`, `proposal-b.md` and the `/sc:adversarial` output) | resolves report conflict log entries |
| QA reports | `qa/*` (per-gate analyst, qa, qualitative, lens, fidelity, anti-omission reports, consolidated findings, fix logs, `final-validation-checklist.md`) | gate evidence |
| Final report | `RESEARCH-REPORT-review-panel-unification-run2.md` | the deliverable; report only, no roadmap |

**Report scope (owner instruction):** report only. It must contain (a) an overlap matrix, (b) a value inventory with a destination for every item, (c) a conflict log (conflicts the evidence cannot decide go through `/sc:adversarial --compare`), (d) a target architecture (shared core plus thin modules), (e) a future-use-case exposure check (PR code review, rf-qa and rf-qa-qualitative replacement, later reviewers). The branch structure, ordering, no-regression gates, PR plan and risk register belong to the later `/sc:workflow` step, so the report records only the constraints and inputs that step needs (Section 8.2 "sequence and gates (inputs for a plan, not a roadmap)").

## SUGGESTED_PHASES

### Rules every Phase 2 / Phase 4 agent receives (embedded in each checklist item)

1. Read your slice(s) first, then verify against code at HEAD and, for E2, against `E2-TIP` through `git show 6c0984326cbb8fb06c4a36065de58b171d3f8175:<path>` or `git ls-tree`. Never check out, switch, pull, stash or write in the repo outside the assigned output file. Python only through `uv run`; no bare `python`; pytest only with `-p no:cacheprovider` and only when the assignment says so.
2. Independence: never read, list, grep into or cite `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/` or `.dev/tasks/to-do/REVIEW-PANEL-UNIFY-RUN2-QUEUED.md`. Exclude `.dev/tasks/` from every repo-wide grep (use `--glob '!.dev/tasks/**'` or a path list) and from `git log` (`-- ':!.dev/tasks'`).
3. Stub-first: create the output file with header and section skeleton, then append section by section; tag every claim [CODE-VERIFIED], [CODE-CONTRADICTED] or [UNVERIFIED]; record every failed search as negative evidence; end with a gaps-and-questions section; return only the file path.
4. Concurrency: the harness refuses more than 20 concurrent subagents. Phase 2 runs as wave 1 (agents 01-18, 18 agents) and wave 2 (value ledgers 19-24, 6 agents) when slots free; Phase 4 runs after Phase 2.

### Phase 1: scope discovery (DONE)

12 slice agents wrote `research/scope/01..12-*.md`; all marked Complete (verified on disk, 2026-11-14 08:12). Gaps carried from the slices are assigned to Phase 2 agents below.

### Phase 2: deep investigation (24 research files)

Each topic agent cross-checks the slices that cover its topic, resolves the open items listed, and writes verified findings with file:line evidence.

| # | Type | Topic | Slices to read / extra material | Open items it must resolve | Output |
|---|---|---|---|---|---|
| 01 | Architecture Analyst | Overlap capability matrix: for each capability (finding schema, ids, identity/hash, merge and dedupe, clustering, citation verification, verdict, ledger and rounds, panel/tier/profile, dispatch, brief, calibration, telemetry/manifest/run record, memory, eval harness, collaboration), who has what in E1, E2, E3 | 01, 02, 09, 10, 12, 03, 08; code at HEAD; `git diff --stat 4a22d7421..6c0984326 -- src tests` on E2 | classify each cell identical / superset / conflicting / unique; check that E2 commits after the hand-off (c2ddeb1b4, fd69a006d, d561461fa, 6c0984326) changed no product code (slice 01 G6); E2 `snap.py` writes into E1's evidence tree | `research/01-overlap-capability-matrix.md` |
| 02 | Code Tracer | Finding contract: v1 anchors, v2 citations, card format, variant ledger rows, E2 `panel-msg/1` and `origin`; limits 200/300; id grammar | 09, 01, 02, 05, 07, 08; `findings.py`, `findings_v2.py` (whole), `card_convert.py`, `cluster.py`, `verify_cmd.py`; tests `tests/review/` | does `findings_v2._check_finding` reject unknown keys such as `origin` (slice 07 Q7, slice 08 gap 5); exact effect of truncate vs reject vs re-ask on the 92 / 49 drop figures; tasklist id grammar `T01.01` | `research/02-finding-contract.md` |
| 03 | Code Tracer | Merge, ledger, verdict semantics: clearing loop (D-1), one valid reviewer passes (D-2), deferred re-open (D-11), quorum, reviewer-typed vs script-computed verdict, two ledgers, stoprule | 09, 12, 10, 01; `ledger.py`, `ledger_cmd.py`, `merge_cmd.py`, `contract.py`, installed `review_ledger.py`, `stoprule.py` (read by ranges), tests pinning them | which pins encode defects as behaviour; relation of installed variant scripts to `cli/review/ledger.py` (slice 09 gap 1, slice 02 gap 9); reproduce D-1, D-2, D-11 read-only | `research/03-merge-ledger-verdict.md` |
| 04 | Integration Mapper | Dispatch, model identity and tiers: class vs raw id, tier JSON and `classes`, gateway `launch` map, ember, served model vs requested, alias tier, `ccsession-models.json` | 03, 10, 11, 02, 09; `review-tiers.default.json`, `panel.py`, `panel_cmd.py`, `MODEL-TIERS.md`, `ccsession-models.json`, `tests/unit/test_ccsession_tiers.py`, `scripts/reflect_*` | whether `muse-ember-1.0` exists anywhere at HEAD (slice 01 Q-F); how the reflect profile validation (`panel.py:80-136`) limits `reflect-*` templates (slice 02 gap 8); what records the served model | `research/04-dispatch-identity-tiers.md` |
| 05 | Code Tracer | Input delivery and brief: source.md, brief placeholders, CB-1..CB-5, B-1..B-7, the reflect brief heading, H1-H4, spec-shape coupling | 03, 05, 06, 01, 09, 10; `document_review_loop_prompts.md`, `spec-panel.md`, reviewer-spec.md, tasklist brief code | what the core must expose per module (placeholders, categories, ref syntax); the claim that the brief never names source.md (slice 02 Q-F) | `research/05-input-delivery-brief.md` |
| 06 | Architecture Analyst | Reflect's two Tier-2 engines and the Stage 2 exit: swarm engine vs skill panel, contract 1.0 vs 1.8.0, convergence 0.75 vs 0.80, EV-1, parity, shadow lint, mechanical vs prose | 10, 11, 01; whole `cli/reflect/`, `fallback.py`, `SKILL.md` ranges NOT read by slice 10 (`L508-L621`, `L872-L935`, `L1047-L1203`, `L1293-L1708`, `L1740-L1849`), `scripts/reflect_shadow_exit.py` | what must stay byte-identical (contract 1.8.0 field lists, `merge_method` values); which EV-1 failures are mechanical and could move into code; run `uv run python scripts/reflect_shadow_exit.py` and the reflect tests with `-p no:cacheprovider` to re-confirm `OVERALL: FAIL (13 of 20)` and 352 passed | `research/06-reflect-two-engines.md` |
| 07 | Pattern Investigator | E1 evidence, graded: 15 pilot + 15 combo runs, Stage 0a, thresholds T-1..T-10, AI-label check, dispatch collapse, orchestrator token share, cluster agreement | 11, 10; `.dev/reflect/`, `.dev/eval-workspaces/shadow-model-combos/`, `.dev/troubleshoot/`, Stage 0 package artifacts | recount key numbers with read-only scripts (15/15 published, 4,119,747 output tokens, 216 clusters of which 7 multi-reviewer, TP 21 FP 4 FN 1 TN 24); grade each finding by strength; list what it does not show | `research/07-e1-evidence-grading.md` |
| 08 | Pattern Investigator | E2 evidence, graded: study results, audits A-F, GT, blind judge, reproducibility | 03, 04, 01, 02; `20261111-a1/` through git only | recompute pilot cells and the `three-way.py` figures; resolve the unit of the "92 / 80 / 49" figures and the 3-vs-4 verdict flips (slice 03 gap 6); decide whether batch j1 invalidates the "not confirmed" decision (slice 04 Q5) | `research/08-e2-evidence-grading.md` |
| 09 | Architecture Analyst | Collaboration designs F1-F7 and r1-r5: mechanisms, measured results, transport requirements, conflicts X1-X17 / C-01..C-19 | 05, 07, 08; r1-r5 DESIGN/IMPLEMENTATION and results via git | what a core must offer (hook points, resume, board path, seal) vs what reflect-reviewer (no Bash) can host; whether H1-H4 should be unconditional core requirements; honest evidence status (single smoke rows only) | `research/09-collaboration-designs.md` |
| 10 | Architecture Analyst | Process redesign: Sweep Sheet, Recipe Ledger, class cards C1-C8, X1-X7, gates, anti-overfitting; relation to ledger-v1, E1 coverage slice, `verify-citations` | 06, 05, 02; E2 brainstorm files via git | name clash `ledger-v1` vs `review-ledger/1`; whether E1 `verify-citations` and coverage already implement item assignment and quote checking | `research/10-process-redesign.md` |
| 11 | Integration Mapper | Consumers: sc:tasklist (Stage 10.5, post gate), sc:workflow Wave 4, reflect UC-1; the E2 tasklist review entry point (DO4) | 12, 10, 01, 02; `sc-tasklist-protocol`, `sc-workflow-protocol`, `cli/tasklist/` | advisory vs blocking tasklist review; where the panel plugs in; the 36-test verdict matrix constraint | `research/11-consumers-tasklist-workflow.md` |
| 12 | Integration Mapper | Consumers for spec review: spec-panel Review Loop, brainstorm, design, rubric text, severity vocabularies, meanings of "Medium" (slice says four; research/12 finds at least six), caps | 12, 09, 05, 06; `spec-panel.md`, `document_review_loop_prompts.md`, `sc-brainstorm-protocol`, `design.md`, plugin mirrors | which severity scale the core carries; plugin mirror differences for `design.md` and `brainstorm.md` (slice 12 gap 9) | `research/12-consumers-spec-review.md` |
| 13 | Integration Mapper | Future uses: PR code review (`pr_submit`, `auggie-review`, severity router, third-party reviewers, fork-only rules) and rf-qa / rf-qa-qualitative / rf-analyst replacement (call-site census, `/task` lens-gate pattern, swarm 8-lens registry) | 12, 10, 01; `src/superclaude/pr_submit/`, `sc-pr-submit-protocol` refs, `sc-auggie-review-protocol`, rf-* agents and SKILL call sites, `cli/swarm` | exact blockers per use case; the minimum shape the core must expose now so neither use case is blocked later; rf-qa behaviour tests (slice 12 gap 5) | `research/13-future-pr-review-and-rfqa.md` |
| 14 | Doc Analyst | E3 variants and experiments: installed-only variants, #346 phase 5, `.dev/research/346-review-loop-experiments/`, install state, personal-over-project shadowing | 12, 03; `.dev/experiments/346-validation/phase5/` (`final-bundle/measurements/*`, `final_report_check.py`), `.dev/research/346-review-loop-experiments/` (FINAL-RESULTS.md, GO-LIVE-RUNBOOK.md, README.md), installed variant files read by ranges | the unread numeric claims (slice 12 gaps 1, 2); is master PR #479 the intended outcome of the refactor spec; value to keep from each variant | `research/14-e3-variants-and-experiments.md` |
| 15 | Code Tracer | Telemetry, manifest, run record, cost, memory policy: `telemetry.py` (no writer, forbids document text), `manifest.py` (lost updates D-23), `model_scores` cost fan-out (D-17), E2 `collab.json` and results rows, memory write policy | 09, 11, 07, 08; `telemetry*.py`, `manifest*.py`, `reflect` run artifacts | one run-record design; whether study telemetry can carry anchors; execute-free reproduction of D-17, D-23 | `research/15-telemetry-manifest-run-record.md` |
| 16 | Doc Analyst | Evaluation governance: shared ground truth, pre-registered decision rule, blind judge, replicates, audits as `verify-run`, held-out sets, AI labels, seeded defects, E1/E2 independence (same designSpec package, sha256 `044809e3...`) | 03, 04, 11, 06, 05; E2 `ground-truth` and judge scripts via git, E1 Stage 0 package | what counts as acceptance evidence for a panel design; who owns harness files (`run-reviewer.sh`, judge scripts); whether E1 and E2 results are independent | `research/16-eval-governance.md` |
| 17 | Code Tracer | Defect register: every defect from the slices (D1-D13, P1-P7, T1-T2, B-1..B-7, D-1..D-31, X-1..X-22, harness H-list, audit-script bugs), de-duplicated, re-verified, each with file:line, reproduction status, fix owner (core / module / eval / drop) | 01, 02, 03, 04, 09, 10, 11 | reproduce with read-only `uv run python`; mark which are pinned by tests as intended behaviour; map the three numbering schemes (slice 02 Q-A) to one | `research/17-defect-register.md` |
| 18 | Integration Mapper | Repository constraints and branching: ref rule (`feat/review-panel` vs `feat/review-panel/<name>`; test in a temporary repo under `/tmp`), package layout, `make sync-dev` / `verify-sync`, installed-path rule for primitives, plugin mirror, contract pins, test layout, fork-only PR flow, Orca worktree rule, `.claude/` staging ban | CLAUDE.md files, `Makefile`, `tests/skills/test_primitive_dual_surface_lookup.py`, `plugins/superclaude/`, `pyproject.toml`, `docs/` | exact constraints a later plan must respect; which hooks and tests fail on a naive layout | `research/18-repo-constraints-and-branching.md` |
| 19 | Pattern Investigator | Value ledger for slices 01 and 02 (hand-offs and notes) | 01, 02 | every item gets `VL-19-nnn`, slice:line source, one-line statement, destination (CORE / MODULE-reflect / MODULE-tasklist / MODULE-spec / EVAL / HARNESS / KNOWLEDGE / DROP + reason), conflict link | `research/19-value-ledger-handoffs.md` |
| 20 | Pattern Investigator | Value ledger for slices 03 and 04 (E2 study and audits) | 03, 04 | same format, `VL-20-nnn` | `research/20-value-ledger-e2-study.md` |
| 21 | Pattern Investigator | Value ledger for slices 05 and 06 (brainstorms) | 05, 06 | same format, `VL-21-nnn` | `research/21-value-ledger-brainstorms.md` |
| 22 | Pattern Investigator | Value ledger for slices 07 and 08 (collaboration packages) | 07, 08 | same format, `VL-22-nnn` | `research/22-value-ledger-collab-designs.md` |
| 23 | Pattern Investigator | Value ledger for slices 09 and 10 (review package and reflect) | 09, 10 | same format, `VL-23-nnn` | `research/23-value-ledger-e1-e3-code.md` |
| 24 | Pattern Investigator | Value ledger for slices 11 and 12 (E1 evidence, E3, consumers) | 11, 12 | same format, `VL-24-nnn` | `research/24-value-ledger-evidence-consumers.md` |

### Phase 3: research completeness gate (full intensity)

2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative, partitioned (more than 6 files), all report-only; serialized fix (consolidate, one fix agent, verify); max 2 fix cycles; halt precedence regression, then monotonicity, then hard cap. Gate focus: every Phase 2 claim has file:line; every slice gap is resolved or logged; no run-1 contamination; every value-ledger row has exactly one destination.

### Phase 4: web research (4 files, after Phase 2)

W1 `research/web-01-multi-model-review-evidence.md`; W2 `research/web-02-claude-code-hooks-headless.md`; W3 `research/web-03-git-branch-hierarchy-stacked-prs.md`; W4 `research/web-04-finding-schemas-review-bots.md` (topics as in SOLUTION_RESEARCH). Tavily first, WebSearch/WebFetch as fallback.

### Phase 5: synthesis, then synthesis QA gate (full), then conflict adjudication

| Synth file | Report sections | Research files that feed it |
|---|---|---|
| `synth-01-problem-current-state.md` | 1 Problem, 2.1-2.8 current state per effort and subsystem | 01-18, scope slices |
| `synth-02-overlap-matrix.md` | 2.9 overlap matrix (a) | 01, 04, 06, 09, 11, 12 |
| `synth-03-target-gaps.md` | 3 Target state, 4 Gap analysis | 01-18 |
| `synth-04-external-findings.md` | 5 External research | web-01..04 |
| `synth-05-options.md` | 6.1-6.x options per decision axis | 01-18, web |
| `synth-06-conflict-log.md` | 6.y conflict log (c), with the list of conflicts the evidence cannot decide | 01-18, 17 |
| `synth-07-recommendation-architecture.md` | 7 Recommendation: 7.1 target architecture (d), 7.2 future-use exposure (e) | 01-18, debates |
| `synth-08-value-inventory.md` | 8.1 value inventory (b) | 19-24 (exhaustive), 17 |
| `synth-09-sequence-and-gates.md` | 8.2 sequence and gates (inputs for a plan, not a roadmap), including the branch-structure constraints | 18, 06, 16, 13 |
| `synth-10-questions-evidence.md` | 9 Open questions, 10 Evidence trail | all gaps, all research paths |

Synthesis QA gate: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative (partition above 4 files), serialized fix, max 2 fix cycles. Then **conflict adjudication (before assembly):** for every conflict in `synth-06` that the evidence cannot decide, write `proposal-a.md` and `proposal-b.md` under `reviews/adversarial/<conflict-slug>/` and run `/sc:adversarial --compare <a>,<b> --depth standard --focus correctness,risk,test-coverage --output <that folder>`; fold winners (and any unaddressed invariants) back into `synth-06` and `synth-07`; conflicts the evidence does decide are decided without a debate. Launch debates in batches that respect the 20-subagent limit.

### Phase 6: assembly and validation (full)

`rf-assembler` builds `RESEARCH-REPORT-review-panel-unification-run2.md`; lens gate (13 lenses; more than 3000 lines means each lens runs as two instances a/b; 3-5 rf-qa + 3-5 rf-qa-qualitative + 3 domain lenses); serialized fix; source-document fidelity gate (4 agents, report against the code and E2 tip); anti-omission gate (4 rf-analyst, exhaustive, by meaning, against research files 01-24 and synthesis); final validation checklist.

### Phase 7: present, record, close

Present the report path and summary; `git add .dev/tasks` (stage only, no commit); record the next step (commit and push without a PR on the owner's instruction, then `/sc:adversarial --compare --merge` on the two reports, then `/sc:workflow ... --depth standard --handoff none`); mark the task Done.

## TEMPLATE_NOTES

Template 02 (Complex Task). The work needs discovery before building (24 verification and value-ledger agents), parallel subagents, five QA gates, a conflict-adjudication step with nested `/sc:adversarial` runs, and a conditional fix loop. QA intensity: **full** (Deep tier default; the owner asked for exhaustive value capture, so no reduction). Report name: `RESEARCH-REPORT-review-panel-unification-run2.md`. Testing requirements: none (documentation only; read-only investigation; the only commands that run are read-only `uv run python` recounts and the reflect/review test suites with `-p no:cacheprovider`).

Builder notes:
- Gate counts and halt rules follow the skill's QA_GATE_REQUIREMENTS for full intensity (Gate 1 research 5 agents, Gate 2 synthesis 5, Gate 3 report 9-13 lens agents, Gate 4 fidelity 2 partitioned to 3-4, Gate 5 anti-omission 2 partitioned to 3-4). Anti-omission coverage is judged by meaning against research files 01-24 (including the six value ledgers) and all synthesis files.
- Phase 2 has 24 agents and the harness limit is 20 concurrent: the builder must create the items so that wave 2 (19-24) starts when slots free, and must not rely on one message spawning all 24.
- The conflict-adjudication step sits between the synthesis QA gate and assembly; its debates use `/sc:adversarial --compare` (never `--merge` here; the merge between the two reports is a later, separate step).
- Report-only: do not create a roadmap, branch plan, PR plan or risk register inside this task.
- Independence rule is embedded in every item (see SUGGESTED_PHASES rules).

## AMBIGUITIES_FOR_USER

Intent is clear from the request and the codebase: produce one independent report on a unified Review Panel, report only. The items below are not ambiguities about intent; they are (1) doc-sourced claims the scope slices marked [CODE-CONTRADICTED] or [UNVERIFIED] (the skill requires them flagged here), and (2) the one outward action the owner's instruction does not cover. Phase 2 agents resolve (1) where the code or git can decide; whatever stays open goes to report Section 9.

### [CODE-CONTRADICTED] claims (do not build on them)

| Claim | Contradicted by | Slice |
|---|---|---|
| E2 run-2 and `HANDOFF-run1-vs-run2.md:22` attribute the `cli/review` changes to #519 + #518 | #518 changes no `cli/review` file (one test file only) | 01 |
| E2 run-1 D14 first half (tasklist review reaches no reflect panel) | `sc-workflow-protocol/SKILL.md:89` and `sc-tasklist-protocol/SKILL.md:1630` | 01 |
| E2 run-2 reflect contrast (5.6) and Q4/Q9 "reflect has no panel/tier code" | reflect has a shadow engine that resolves its panel through the tier JSON (`sc-reflect-protocol/SKILL.md:87, :340-349`) | 01, 02 |
| E2 run-1 "alias GT3 found once" | the finding is alias GT1 (`COMBO-REPORT.md:497`, legend `:401-417`) | 01 |
| `COMBO-REPORT.md:292` "discarded with no error" at merge | merge emits a warning with the first error; `block_ok` exists | 03, 04 |
| `COMBO-REPORT.md:292` "four verdict flips" | audit-D:20 enumerates 3 flips (+5 total-loss merges) | 01, 03, 04 |
| "16 empty terra reviews" | 14 terra + 2 luna | 04 |
| E2 harness brief `unpassable-ac` | rules file and `CATEGORIES` say `unpassable-check`; harness brief typo | 03 |
| E2 run-2 note "T2bModel01 not referenced anywhere in src/ or tests/" | `ccsession-models.json:107`, `README.md:445`, `tests/unit/test_ccsession_tiers.py:72-73,239` (at the base) | 02 |
| E2 hand-off "159 functions" | the table sums to 179 | 02 |
| E2 seed "no missing-task category / no severity levels" | code has `missing-requirement` and CRITICAL/MAJOR/MINOR | 06 |
| E2 `theory.py` HARD set as applied | includes B3/B7, excludes B5/I1/B6 | 05 |
| Memory lesson (memory line 64): "fenced yaml calibration not parsed by cluster" | `cluster_cmd.py:27-34` (installed-CLI version at run time unverified) | 11 (X-16) |

### [UNVERIFIED] claims (carried, not decided)

- The unit behind "92 findings dropped / 80 reviewer-package runs / 49 blocking lost" (slices 01, 03, 04, 05, 06).
- `combos/` size: 106 scored runs vs 96 directories vs 97 tracked entries vs "107 entries" (slices 01, 02, 03); the number of `RESULT.md` files (19 vs 29); quarantine counts 428 vs 417 files; Qwen reviewer count (3 vs 4).
- Whether E2 commits after `4a22d7421` (c2ddeb1b4, fd69a006d, d561461fa, 6c0984326) changed `src/` or `tests/` (slice 01 G6; the E2 branch is described as changing no product code).
- Whether `muse-ember-1.0` exists in the tier data at HEAD (absent in `src tests docs scripts` and `ccsession-models.json` per slice 01; slice 03 reads tier4 = luna, haiku, grok at HEAD).
- All collaboration estimates (reach probabilities, act rates, hook cost about 0.1 s/call, resume 6 s, fresh-start 16 s, +29% static kit est.), the test counts 138 / 358 / 89 / 106 / 108, hooks firing in `claude -p` for gateway ids, `--resume` for gateway ids (slices 05, 07, 08).
- All numeric claims of the #346 phase-5 FINAL-REPORT (slice 12 gap 1) and the contents of `.dev/research/346-review-loop-experiments/` (6,523 tracked files, unread).
- Whether the installed variant scripts re-implement or import `cli/review/ledger.py` (slices 02, 09, 12).
- Whether the pilot stop rule and thresholds T-1..T-10 were ever approved (slice 11 G-4); the per-run causes of shadow parity/EV-1 failures.

### Outward action not covered by the owner's instruction

The owner told the session to commit and push (no PR) after run 1. No instruction covers committing or pushing run 2. At Phase 7 the task only stages `.dev/tasks` (staging is not committing) and records the next step; committing and pushing run 2 waits for the owner's word, unless the owner repeats the run-1 instruction for it.
