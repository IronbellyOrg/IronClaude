# Phase 2–5 markdown gate input summary (item 6.1)

**Date:** 2026-09-19
**Worktree (`${WT}` expanded):** `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/`
**Task dir:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/`
**Phase 5 verdict:** PASS (`phase-outputs/plans/phase5-verdict.md`)
**Gate tier:** I19 1500–3000 (task-file sizing; 19 md files + new-ref content; N=15; 5 rf-qa + 5 rf-qa-qualitative)

---

## 19-file markdown manifest (absolute `${WT}` paths)

Copied from `qa-input-manifest-md.md` (item 5.5). These are the Phase 6 reviewed set. `.pre-commit-config.yaml` is the 20th review input, not one of the 19 markdown files.

1. `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` — 653 lines; tracked modified
2. `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md` — 389 lines; tracked modified
3. `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` — 180 lines; tracked modified
4. `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md` — 324 lines; tracked modified
5. `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/triage-checklist.md` — 80 lines; tracked modified
6. `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` — 91 lines; tracked modified
7. `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/hardening-output-contract.md` — 73 lines; tracked modified
8. `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/pipeline-hardening-closure.md` — 63 lines; tracked modified
9. `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/unmask-and-sweep.md` — 52 lines; tracked modified
10. `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/runtime-entrypoint-verification.md` — 47 lines; tracked modified
11. `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/contract-enumeration.md` — 30 lines; tracked modified
12. `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/effective-input-proof.md` — 27 lines; tracked modified
13. `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/primitive-differential.md` — 58 lines; untracked new
14. `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/agent-assertions.md` — 37 lines; untracked new
15. `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/environment-deltas.md` — 16 lines; untracked new
16. `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/probe-packs/read-parse.md` — 10 lines; untracked new
17. `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/agents/confidence-calibrator.md` — 158 lines; tracked modified
18. `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/agents/evidence-validator.md` — 147 lines; tracked modified
19. `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/commands/troubleshoot.md` — 204 lines; tracked modified

Config companion: `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/.pre-commit-config.yaml` — 134 lines.

---

## Seam → item map (Phases 1–4 headers)

Anchor ids are the pre-edit baseline hints from item titles. Source of unique `old_string` needles: `phase-outputs/discovery/insertion-anchors.md`. Binding correction ledger (Phase Gate Findings) supersedes conflicting verbatim checks.

### Phase 1 — new refs + Refs-table rows

| item | file | anchor |
|---|---|---|
| 1.1 | `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/agent-assertions.md` | NEW file (X-1..X-3 + D13) |
| 1.2 | `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/primitive-differential.md` | NEW file (R-05) |
| 1.3 | `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/environment-deltas.md` | NEW file (D9) |
| 1.4 | `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/probe-packs/read-parse.md` | NEW file (v2:336-344) |
| 1.5 | `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` | `## Refs` after `refs/effective-input-proof.md` row (D10) |

### Phase 2 — SKILL.md

| item | file | anchor |
|---|---|---|
| 2.1 | SKILL.md | SKILL:64 fifth token |
| 2.2 | SKILL.md | SKILL:420 Wave 4.5 step 7 |
| 2.3 | SKILL.md | SKILL:444 Wave 5 compose |
| 2.4 | SKILL.md | SKILL:595-600 H0–H5 → HC* |
| 2.5 | SKILL.md | SKILL:444 H0–H5 evidence-card paths |
| 2.6 | SKILL.md | SKILL:414-419 Wave 4.5 six gate steps |
| 2.7 | SKILL.md | SKILL:420 from the H0–H5 statuses |
| 2.8 | SKILL.md | SKILL:410 Wave 4.5 Trigger |
| 2.9 | SKILL.md | SKILL:408 Wave 4.5 Goal |
| 2.10 | SKILL.md | SKILL:104 wave map |
| 2.11 | SKILL.md | SKILL:67-71 Output Contract description cells |
| 2.12 | SKILL.md | SKILL:63-64 H0 classifies / H0–H5 statuses |
| 2.13 | SKILL.md | SKILL:77 execution_locus_card_path |
| 2.14 | SKILL.md | SKILL:73 status: blocked ⇒ halt |
| 2.15 | SKILL.md | SKILL:62 contract_version 1.2.0 |
| 2.16 | SKILL.md | SKILL:43 status enum + blocked |
| 2.17 | SKILL.md | SKILL:582 cosmetic-counter clause (superseded: non-blocking threshold) |
| 2.18 | SKILL.md | SKILL:545 Will Not Do D7 + R-13 |
| 2.19 | SKILL.md | SKILL:266 AND :570 3-round cap |
| 2.20 | SKILL.md | SKILL:529 blocked alternative |
| 2.21 | SKILL.md | SKILL:515 Bash row |
| 2.22 | SKILL.md | SKILL:512 Task row |
| 2.23 | SKILL.md | SKILL:509 Context7 row |
| 2.24 | SKILL.md | SKILL:462 cosmetic_overrun |
| 2.25 | SKILL.md | SKILL:460 split_pending |
| 2.26 | SKILL.md | SKILL:457 status footer (superseded: +failed) |
| 2.27 | SKILL.md | Wave 5 NEW step 3.5 |
| 2.27a | SKILL.md | SKILL:471 TFEP blocked |
| 2.28 | SKILL.md | SKILL:452 A-rule fallback |
| 2.29 | SKILL.md | SKILL:451 validator kwargs |
| 2.30 | SKILL.md | SKILL:451 persist-on-receipt |
| 2.31 | SKILL.md | SKILL:450 headline-confidence |
| 2.32 | SKILL.md | SKILL:439 probe self-consistency |
| 2.33 | SKILL.md | SKILL:381 Wave 4 preconditions |
| 2.34 | SKILL.md | SKILL:372 Wave 3 skip-Wave-4 |
| 2.35 | SKILL.md | SKILL:358 single command |
| 2.36 | SKILL.md | Wave 3 NEW step 4.5 |
| 2.37 | SKILL.md | SKILL:345 calibrator kwargs |
| 2.38 | SKILL.md | SKILL:342 Producers paste |
| 2.39 | SKILL.md | SKILL:336 behaviour-definition |
| 2.40 | SKILL.md | SKILL:282 C-rule fallback |
| 2.41 | SKILL.md | SKILL:281 calibrator kwargs |
| 2.42 | SKILL.md | SKILL:280 runs-in= unread |
| 2.43 | SKILL.md | SKILL:255 discriminator-required |
| 2.44 | SKILL.md | SKILL:248 per-defect counter |
| 2.45 | SKILL.md | SKILL:241 hard-stop bullet |
| 2.46 | SKILL.md | SKILL:240 S1.6.4 discriminator trigger |
| 2.47 | SKILL.md | SKILL:230 S1.6.0b producers |
| 2.48 | SKILL.md | SKILL:168 OBSERVE-VIA |
| 2.49 | SKILL.md | SKILL:167 step 1b locus card |
| 2.50 | SKILL.md | SKILL:106 wave-map hard-stop edge |
| 2.51 | SKILL.md | SKILL:97 Wave 1 label + locus |

### Phase 3 — refs + two existing tests

| item | file | anchor |
|---|---|---|
| 3.1 | hardening-output-contract.md | HOC:5 five-token |
| 3.2 | hardening-output-contract.md | HOC:15 schema row |
| 3.3 | report-template.md | RT:223 + RT:315 |
| 3.4 | tests/troubleshoot/test_hardening_verdict.py | :51 five-token |
| 3.5 | pipeline-hardening-closure.md | PHC:13 |
| 3.6 | hardening-output-contract.md | H0..H5 → HC* (keep-verbatim D11) |
| 3.7 | pipeline-hardening-closure.md | H0–H5 headings |
| 3.8 | report-template.md | RT:230-235 + RT:316 |
| 3.9 | unmask-and-sweep.md | UAS HC3 |
| 3.10 | runtime-entrypoint-verification.md | REV HC1 |
| 3.11 | contract-enumeration.md | CE HC2 |
| 3.12 | effective-input-proof.md | EIP HC4 |
| 3.13 | tests/troubleshoot/test_hardening_h1.py | :46 satisfy hc1 |
| 3.14 | (guard command) | D11 GUARD OK |
| 3.15 | hardening-output-contract.md | HOC:13 + :25 1.2.0 |
| 3.16 | report-template.md | RT:161 blocked |
| 3.17 | diagnosability-audit.md | da:284 counter (superseded: repo-root store) |
| 3.17a | diagnosability-audit.md | da:280 Section 7 tasklist order |
| 3.18 | diagnosability-audit.md | da:263 header keys |
| 3.19 | diagnosability-audit.md | da:260-278 Task 6 |
| 3.20 | diagnosability-audit.md | da:255 five task types |
| 3.21 | diagnosability-audit.md | da:247 constraint 5 |
| 3.22 | diagnosability-audit.md | constraint 6 |
| 3.23 | diagnosability-audit.md | da:176 Substituted primitive |
| 3.24 | diagnosability-audit.md | da:150 S14 |
| 3.25 | report-template.md | R-13 timestamp |
| 3.25a | report-template.md | RT:146 hard-stop line |
| 3.25b | report-template.md | RT:208 re-key |
| 3.26 | report-template.md | RT:73 UNDETERMINED |
| 3.27 | report-template.md | RT:67 Diagnosis lead |
| 3.28 | hypothesis-card-template.md | Filling the card |
| 3.29 | hypothesis-card-template.md | HCT:91 producers.md |
| 3.30 | hypothesis-card-template.md | HCT:80-82 discriminator form |
| 3.31 | hypothesis-card-template.md | HCT:44 behaviour-definition |
| 3.32 | hypothesis-card-template.md | HCT:32 runs-in= |
| 3.33 | triage-checklist.md | triage:63 |
| 3.34 | triage-checklist.md | triage:44 Producer citation |
| 3.35 | triage-checklist.md | triage:42 evidence-or-drop |
| 3.36 | triage-checklist.md | triage:33 Substituted primitive |
| 3.37 | escalation-rubric.md | RUB:69 split_pending |

### Phase 4 — agents + command

| item | file | anchor |
|---|---|---|
| 4.1 | `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/agents/confidence-calibrator.md` | CAL:111-115 Notes |
| 4.2 | confidence-calibrator.md | CAL:108 split_pending |
| 4.3 | confidence-calibrator.md | CAL:88-96 structural_flags |
| 4.4 | confidence-calibrator.md | CAL:62 step 5b |
| 4.5 | confidence-calibrator.md | CAL:51 Inputs |
| 4.6 | `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/agents/evidence-validator.md` | VAL:99-103 blocked |
| 4.7 | evidence-validator.md | VAL:72 suggested status |
| 4.8 | evidence-validator.md | VAL:63-97 Structural assertions |
| 4.9 | evidence-validator.md | VAL:55 2b |
| 4.10 | evidence-validator.md | VAL:44 Inputs |
| 4.11 | `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/commands/troubleshoot.md` | CMD:103 Bash |
| 4.12 | troubleshoot.md | CMD:69 On skill return |

Full unique `old_string` inventory: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/phase-outputs/discovery/insertion-anchors.md`.

---

## Validation evidence (Phase 5)

| check | source | result |
|---|---|---|
| markdownlint | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/phase-outputs/test-results/markdownlint-summary.md` | PASS; hook exit=0; no rewritten/created/deleted nonignored files; 22/22 expected changed paths |
| verify-sync (full) | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/phase-outputs/test-results/verify-sync-output.txt` | GREEN; `✅ All components in sync.`; exit=0 |
| verify-sync (scoped) | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/phase-outputs/test-results/verify-sync-scoped.txt` | GREEN; `TROUBLESHOOT-SCOPE IN SYNC` |
| HC guard | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/phase-outputs/test-results/hc-guard-final.txt` | 0 lines (empty capture) |
| preserve-baseline | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/phase-outputs/test-results/preserve-baseline-check.md` | 67/67 protected entries OK; 19-file sweep 0 hits; scoped exception for pre-existing `artifact_paths` in `refs/doc-discovery.md` (do-not-touch) |
| staging | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/phase-outputs/test-results/git-status-phase5.txt` | `CLEAN: no .claude staged` |
| Phase 5 verdict | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/phase-outputs/plans/phase5-verdict.md` | `PASS` |

Supporting discovery (must stay open for lens agents):

- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/phase-outputs/discovery/naming-ledger.md`
- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/phase-outputs/discovery/insertion-anchors.md`
- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/phase-outputs/discovery/preserve-baseline.md`
- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/phase-outputs/reports/qa-input-manifest-md.md`

Binding correction ledger: task file `### Phase Gate Findings` (supersedes conflicting verbatim strings from Phase 2 items).

---

## Spec sources every lens agent MUST open

1. `${V2}` §(d) R-01..R-19: `/config/workspace/Coder/.claude/worktrees/gh-automation-orca-run/.dev/research/sysbox-retrospective-20260918/merged-report-v2.md` (lines ~151-657)
2. Reconcile (superseding): `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/research/07-gap-fill-reconcile.md`
3. Spec cards: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/research/03-spec-extraction.md`

---

## Glob inventory (item 6.1 Action)

### `phase-outputs/**/*.md`

- `discovery/baseline-summary.md`
- `discovery/naming-ledger.md`
- `discovery/insertion-anchors.md`
- `discovery/preserve-baseline.md`
- `test-results/hc-guard-summary.md`
- `test-results/markdownlint-summary.md`
- `test-results/preserve-baseline-check.md`
- `reports/qa-input-manifest-md.md`
- `reports/phase-md-output-summary.md` (this file)
- `plans/phase5-verdict.md`

### `phase-outputs/test-results/*.txt`

- `hc-guard.txt`
- `markdownlint-output.txt`
- `sync-dev-output.txt`
- `verify-sync-output.txt`
- `verify-sync-scoped.txt`
- `hc-guard-final.txt`
- `git-diff-stat-phase5.txt`
- `git-status-phase5.txt`
- plus discovery captures: `worktree-create.txt`, `baseline-sync-dev.txt`, `baseline-verify-sync.txt`, `baseline-pytest-troubleshoot.txt`, `baseline-pytest-full.txt`, `baseline-h-tokens.txt`, `baseline-markdownlint.txt`

---

## Lens-agent report destinations (`qa/exec-md/`)

- `qa-structural-template-conformance-report.md`
- `qa-structural-internal-consistency-report.md`
- `qa-structural-evidence-quality-report.md`
- `qa-structural-completeness-report.md`
- `qa-structural-hc-rename-lint-report.md`
- `qa-content-actionability-report.md`
- `qa-content-numbers-metrics-report.md`
- `qa-content-crossref-chain-report.md`
- `qa-content-domain-accuracy-report.md`
- `qa-content-mustnot-enum-report.md`

All lens agents: `fix_authorization: false`. Worktree-only reads of the 19 files. Never edit `.claude/`.
