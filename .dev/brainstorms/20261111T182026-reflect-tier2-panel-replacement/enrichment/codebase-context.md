# Codebase enrichment (Wave 2A)

quality_tier: primary (mcp__litellm__augment_code-augment_code_search ran on branch `master`; the first call without a branch failed with BRANCH_NOT_FOUND and was repeated with `branch: master`).
Checkout: HEAD == origin/master == ec259f1b718ccdb9f08bba0237bfa47b2b7601a2.
Paths are relative to `src/superclaude/` unless they start with `.dev/`. "Read" means read in this session with line numbers; "snippet" means seen only in the search result and not read in full.

## 1. Where reflect T2 lives (two engines)

| Piece | Location | Status |
|---|---|---|
| Agent-session path (interactive skill): reviewers as `reflect-reviewer` agents, brief files, calibrator, `/sc:adversarial --compare`, evidence-validator | skills/sc-reflect-protocol/SKILL.md:587-600, 633-666 (Read); refs/reviewer-spec.md (Read, all) | Read |
| Headless CLI path: swarm fan-out + bounded fallback ladder + Mode-A adversarial scorer + contract builder | cli/reflect/ensemble.py:296-511, 514-561, 722-835 (Read) | Read |
| Swarm lens `reflect-review` (3 workers, suspect=True, T2 models from `T2Model0N` env) | cli/swarm/lenses/reflect_review.py:33-72 (Read) | Read |
| Verdict map from contract to blocked/degraded/halted/pass | cli/reflect/contract.py:138-382 (Read) | Read |
| Diversity helpers | cli/reflect/_diversity.py:8-61 (Read) | Read |
| Fallback ladder | cli/reflect/fallback.py: function list only (Grep), body not read | UNVERIFIED body |
| `reflect_post` frontmatter writer | cli/reflect/runner.py:103-200 (Grep hits only; body not read) | UNVERIFIED body |

Key fact for Q4: the CLI path already uses the swarm engine, and its contract builder emits only a subset of the 1.8.0 fields (no coverage, no per-card calibration, no evidence-validator results: `verification_ran: false`, `citations_dropped: 0` are constants, cli/reflect/ensemble.py:808-817).

## 2. Where the panel lives

| Piece | Location | Status |
|---|---|---|
| Panel/tier schema, validation, template and tier loading, env selection, deterministic slot resolution | cli/review/panel.py:25-27, 64, 147, 277, 310, 327, 350, 365, 380, 421, 427 (Read, all 525 lines) | Read |
| Findings format, anchors, fingerprints, clustering, diff-mapping | cli/review/findings.py (Read, all 457 lines) | Read |
| Ledger, rounds, merge_round, apply_revision, verdict, capture, merged-report renderer | cli/review/ledger.py:1-200 and 200-495 (Read) | Read |
| `superclaude review merge` | cli/review/merge_cmd.py (Read, all) | Read |
| Telemetry record schema `review-telemetry/1` | cli/review/telemetry.py: constants and function names only (Grep) | partial |
| Data files: default and live7 templates, tier lists | cli/review/data/*.json (Read, all) | Read |
| Operator doc | docs/reference/review-panel-live7.md (Read, all) | Read |

## 3. Consumers of reflect's contract and output

- `sc:workflow` Wave 4 runs `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md`, records only `reflect_status` and `reflect_report_path`, never changes the workflow status, and treats reflect failure as `skipped|failed` (skills/sc-workflow-protocol/SKILL.md:60-64; refs/return-contract.md:16-21). Read.
- `sc-troubleshoot-protocol`, `sc-auggie-review-protocol`: consume `reflect_status` / `reflect_report_path` from workflow, never re-run pre; run `/sc:reflect --mode post --spec ... --tasklist ... --task-log ... --diff ...` before commit (troubleshoot refs/remediation-handoff.md:117-147; auggie-review SKILL.md:348-351). Read via Grep lines only.
- `sc-implement-protocol` does NOT load reflect (SKILL.md:11, refs/qa.md:3, :11). Read via Grep lines.
- Sprint executor and wrapper read: `status`, `tier_reached`, `merge_method`, `adversarial_convergence_score`, `adversarial_unavailable`, diversity fields, `citations_dropped`, `input_drift_detected`, and the four deviation counters (cli/reflect/contract.py:224-382; SKILL.md:925-941).
- Promotion gate condition 9 (SKILL.md:1483).
- NOTE field-name drift: SKILL.md 9.1 names the score `adversarial_convergence_score` (line 787) while prose and the gate use `convergence_score` (lines 659-663, 1483). The wrapper reads `adversarial_convergence_score` (contract.py:299, 317). The design must keep both.

## 4. Recorded evidence of reflect T2 pre-execution runs

Six `return-contract.yaml` files under `.dev/research/346-review-loop-experiments/exp346/.dev/experiments/346-validation/phase5/final-bundle/builds/*/brainstorm/workflow-report/nested/reflect-*/` (field values from grep, sizes from `du -sb`):

| build/run | status | tier | merge_method | convergence | model diversity | vendor | citations total/dropped | artifact bytes | files |
|---|---|---|---|---|---|---|---|---|---|
| diffgate/1 | success | 2 | adversarial | 1.0 | degraded | single | 156/0 | 355,770 | 26 |
| ledger/1 | partial | 2 | adversarial | 1.0 | degraded | single | 62/3 | 371,507 | 28 |
| minfix/1 | partial | 1 | (none) | (none) | (none) | (none) | - | 29,738 | 3 |
| minfix/2 | partial | 2 | adversarial | 1.0 | full | single | 154/1 | 286,284 | 35 |
| ponytail/1 | partial | 2 | adversarial | 1.0 | full | single | 22/0 | 221,405 | 29 |
| stoprule/1 | partial | 2 | adversarial | 0.97 | full | single | 153/1 | 328,506 | 33 |

Reading: convergence was 1.0 in 4 of 5 T2 runs and 0.97 in the fifth, so the debate score separated nothing in this sample; vendor diversity was single in all five; the evidence-validator dropped citations in 3 of 5. Sample is six runs from one phase; it is NOT a measure of review quality.

Snippets (not read in full): a recorded post-execution merged verdict under `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/post/adversarial/merged-verdict.yaml` shows `merge_method: adversarial`, `convergence_score: 0.836`, `reviewers: 3`, `verdict: FAIL`, `judge_class_collision: true`; and a July run recorded a reviewer `proxy_error` with 0 bytes plus a truncated second reviewer (`.dev/tasks/to-do/TASK-RF-t2-fallback-ladder-20260706-050832/reflect/post/d8f84f71a397/t2-adversarial/merged-audit.md`). UNVERIFIED beyond the snippet.

## 5. Token evidence

- PN1 panel on specs: about 408k loop output tokens per run; primary lane 106,357 (Sonnet), parallel Haiku stand-in lane 290,600 (71%), adjudicator 11,359 (Fable, now forbidden) (`.dev/research/346-review-loop-experiments/p17/LEDGER-RESULTS.md:55-68`, Read).
- Brief's figure for first review of 4 reviewers: about 314k (Sonnet 23k + 3 x Haiku 68k-108k); matches the lane table order of magnitude (brief text; consistent with p18/debate/BRIEF.md:55-60).
- Reflect T2 cost profile: 35k-70k Claude tokens (design estimate) against recorded artifacts of 55k-93k tokens (brief) and 221k-372k bytes (six runs above).

## 6. Gaps found while reading (design-relevant)

1. Panel resolve excludes models only inside one panel (`distinct_across_slots`); it has no executor-class input (cli/review/panel.py:380-427, Read). Executor exclusion has no counterpart.
2. findings-v1 requires a 12-200 character anchor quoted from one document and has no file:line field (cli/review/findings.py:90-121, 276, Read).
3. `merge_round` refuses a round in which no reviewer gave a valid findings block, and treats an invalid-block reviewer as non-clearing (cli/review/ledger.py:107-118 snippet, 200-298 Read).
4. The ledger verdict is PASS/FAIL on blocking rows only, with confidence single/overlap; reflect's gate wants a numeric score and a calibrated confidence.
5. `/sc:adversarial` judge model is chosen inside sc-adversarial; recorded runs show `judge_class_collision: true` once (snippet).
