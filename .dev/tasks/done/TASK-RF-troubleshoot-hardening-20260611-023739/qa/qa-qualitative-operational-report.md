# QA Report — Task File Qualitative Review (Operational Correctness Lens)

**Topic:** Pipeline Hardening Closure mode (H0-H5 + waiver/no-re-greening latch) for sc:troubleshoot-protocol
**Date:** 2026-06-11
**Phase:** task-qualitative
**Lens:** operational-correctness
**Fix cycle:** N/A (fix_authorization: false)

---

## Overall Verdict: FAIL

FAIL on 1 IMPORTANT + 2 MINOR operational findings (no severity level is exempt under task-qualitative rules). All findings are localized, evidence-backed, and have concrete remediations. None are blockers to the overall design — the task is operationally sound on its critical path (G1 gate, advisory invariant, schema fidelity, test mapping, sync/lint/pytest gates all verified correct). The IMPORTANT finding (Step 8.15 POST-reflect command uses a non-existent `--task-file` flag and omits the `--diff`/`--task-log` that `--mode post` requires) would cause the penultimate gate to trip a STOP condition rather than run as written.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run (make sync-dev/verify-sync/markdownlint/pytest) | none | PASS | Makefile L109 `sync-dev:` + L166 `verify-sync:` exist; sync-dev syncs skills+agents+commands (`.claude/commands/sc/`); verify-sync checks Skills/Agents/Commands. `.markdownlint.json` present (`default:true` + MD024 siblings_only); markdownlint-cli@0.38.0 matches pre-commit `rev: v0.38.0`. `tests/troubleshoot/` absent → pytest target created by Step 7.1 before Step 7.22 runs. Preconditions satisfied. |
| 2 | SKILL/report/handoff insertion anchors exist as heading text | none | PASS | SKILL.md verbatim: `## Output Contract` (L37), `## Wave Structure` (L77), `### Wave 1.7: Tier 1 — Hypothesis Formation` (L251), `### Wave 2: Confidence Gate` (L271), `### Wave 5: Synthesis + Report` (L385). report-template.md: `## Audit` (L196), `## Rendering rules` (L205), `## Test-is-wrong rule` (L212), `## Behavior-is-documented rule` (L233), `**Status**: <success\|partial>` (L14). remediation-handoff.md: `## The user offer` (L5), `## Phase A — Build the task file` (L38), `BUILD_REQUEST:` (L43), L3 success-gating note. All findable. |
| 3 | 6 new refs + tests/troubleshoot/ genuinely absent (no clobber) | none | PASS | All 6 refs confirmed absent in refs/; `tests/troubleshoot/` confirmed absent. CREATE items will not clobber. |
| 4 | Test items operationally writable (assertions match ref content) | none | PASS | §5.4 truth table verified verbatim (SPEC L388-400): 7 rows, ROW 5 + ROW 6 both emit `advisory` with exact report-language strings the task quotes. `test_verdict_aggregation_from_h_statuses` CAN assert all 7 rows incl. advisory 5/6. REPO_ROOT pattern matches `tests/skills/test_task_builder_merge.py` L20 `parents[2]`. All §8.1 test names match task function names verbatim. |
| 5 | POST-reflect runnable once placeholders resolved | AX-1 | FAIL | `--task-file` NOT a recognized reflect flag (reflect.md L10; sc-reflect-protocol/SKILL.md L68 `--tasklist`, L72 `--task-log`). `--mode post` with no `--diff` AND no `--task-log` is a STOP condition (reflect.md L33, SKILL.md L109). Task supplies neither. `--executor-model` IS valid (SKILL.md L584). Command string as written would not run. See Issue #1. |
| 6 | G1 gate prevents pre-approval edits | none | PASS | Step 1.1 (L173) halts with frontmatter left "🟡 To Do" if G1 not granted; G1 banners L88/L131/L165; no authoring item edits src/.claude before Step 1.1 confirms. Spec §1.2 (L42) + §9 (L586) corroborate. |
| 7 | OI-2/3/5 PENDING markers correctly halt dependents | none | PASS | OI-2 (1.5)→Step 3.2 reads OI-2-PENDING.md, authors `contract_token` OPEN enum. OI-3 (1.6)→Step 3.1 defers cheapest-probe. OI-5 (1.7) blocks `target_release`, distinct from `contract_version`. SPEC §11: OI-2/3=Roadmap M2, OI-5=G1 (open); OI-1/4/6=Resolved (correctly NOT HALT). |
| 8 | TESTING/VALIDATION/QA_GATE requirements reflected as items | none | PASS | 13 unit (12 spec §8.1 + 1 NEW FR-6 G-PRE-1) + 5 integration (§8.2) = 18 across 7 modules. 6 E2E (E1-E5 + Waiver re-green, SPEC §8.3 L573-580). VALIDATION: sync(7.19)/verify(7.20)/markdownlint(7.21)/pytest(7.22). QA_GATE: 7-agent FINAL_ONLY (8.2-8.8). POST-reflect (8.15). All present. |

## Summary
- Checks passed: 7 / 8
- Checks failed: 1
- Critical issues: 0
- Important issues: 1
- Minor issues: 2
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Step 8.15 (L417) POST-reflect gate | The reflect invocation `/sc:reflect --mode post --depth deep --spec <SPEC> --task-file <TASK> --executor-model {EXECUTOR_CLASS}` uses `--task-file`, which is NOT a recognized reflect flag (skill uses `--tasklist` for the tasklist, `--task-log` for the execution log). Worse, `--mode post` with no `--diff`/`--commit-range`/`--task-log` is an explicit STOP condition (sc-reflect-protocol/SKILL.md L109; reflect.md L33). The literal command would trip the post-mode-needs-completed-work STOP. The item IS framed as a self-run subagent with explicit verification instructions (1)-(5) inline, so the gate intent is achievable, but the literal command string is malformed. (`--executor-model` IS valid per SKILL.md L584, so `{EXECUTOR_CLASS}` is fine.) | Replace `--task-file <TASK>` with `--tasklist <TASK>`, and add a completed-work artifact so post-mode routes to UC-2: `--diff <BASE>..HEAD` (the item already mentions resolving `<BASE>` = merge-base) OR `--task-log <path>`. Wire the already-described `<BASE>` into `--diff <BASE>..HEAD` so post-mode routing (SKILL.md L97) fires. |
| 2 | MINOR | Steps 1.4 (L185) + 6.1 (L257) report-template anchor description | Task describes "the fenced ` ```markdown ` template block" (3-backtick), but the actual fence is a **4-backtick** ` ````markdown ` block (L7, closing L203) — required to wrap inner 3-backtick ` ```text ` blocks (L160). An executor matching on a 3-backtick fence could mis-identify the boundary. Mitigated because Step 6.1 also anchors on heading text (`## Audit`, `## Rendering rules`). | Update Steps 1.4/6.1 to say "the 4-backtick ` ````markdown ` template block (closes after the `## Audit` section)". Note: headings inserted inside the fence are inert to MD025. |
| 3 | MINOR | Step 1.4 (L185) remediation-handoff L3 quote | Task quotes the gating note as "loaded only on `success`", but actual L3 is "Loaded only when `--fix` is set and Wave 5 produced a `success` (not `partial`) report." The quote is a paraphrase. The FR-12 reconciliation (Step 6.2) must reconcile against the REAL gate text (which also requires `--fix`), not the simplified paraphrase. | Quote L3 verbatim in Steps 1.4/6.2; ensure the FR-12 `success_with_hardening_*` reconciliation accounts for the `--fix`-set precondition, not just `success` status. |

## Adversarial Axes — sweep
- **AX-1 Drift:** Found (Issue #1 — `--task-file` drifted from actual `--tasklist`/`--task-log`; Issues #2/#3 — anchor descriptions drifted from actual file content). GOAL verbatim baseline available (task L114) — drift axis ACTIVE.
- **AX-2 Contradictions:** None. 7-module count, advisory 4-token enum, §5.4 row-count, 18-test total internally consistent across Overview/Objectives/per-phase preambles/per-item acceptance lines (prior fix #5 reconciled module-count prose — verified).
- **AX-3 Omissions:** None material. All §8.1/§8.2 spec tests mapped; FR-6 gap (only `test_h2_empty_ledger_fails` in §8.1) correctly closed by NEW `test_h2_sibling_sweep_required_when_concept_shared`. FR-12↔NFR-4 pairing (spec §10 L596) present (Step 7.9). All 5 §5.6 schemas field-count-accurate.
- **AX-4 Weakened criteria:** None. PASS criteria concrete (sync/verify exit 0; zero markdownlint; 18 tests pass 0 failures; advisory rows explicitly asserted). No or/may/if-applicable softening where spec is unconditional.
- **AX-5 Invented content:** None. Every named artifact traces to SPEC §4.5/§4.6/§8 or research 08. NEW FR-6 test justified by reflect gap G-PRE-1 (closes a real §8.1 coverage hole, not an invention). `--executor-model` confirmed real (SKILL.md L584).

## Self-Audit

**(a) Reliance list — rf-qa A.10 PASS items skipped for structural re-check:**
- Relied on rf-qa PASS for frontmatter schema → did NOT re-verify YAML field shape.
- Relied on rf-qa PASS for phase ordering §4.6 → did NOT re-verify item-sequence numbering structure.
- Relied on rf-qa PASS for "per-function test acceptance lines = 18" → did NOT re-count acceptance-line presence structurally.
- Relied on rf-qa PASS for "7 test modules" → did NOT re-verify module-name list structurally.
- Relied on rf-qa PASS for advisory 4-token enum intact (0 three-token regressions) at the presence level.
- Relied on rf-qa PASS for G1 gate marker presence, OI-2/3/5 HALT markers present, QA gate = 7 agents serialized.

**(b) Independent semantic checks (≥1 required, INV-019):**
- **Advisory invariant — SEMANTIC (rf-qa PASS insufficient):** rf-qa confirms the 4-token enum is *present* with 0 three-token regressions (presence check). I independently Read SPEC L388-400 and verified the §5.4 truth-table SEMANTICS: rows 5 AND 6 specifically emit `advisory` (not just `advisory` appearing somewhere), with exact report-language strings, and that `test_verdict_aggregation_from_h_statuses` (Step 7.8) asserts BOTH advisory rows. Tool evidence: Read SPEC L388-400; grep SPEC L311/385/431; Read task L297-298.
- **Schema field-count fidelity — SEMANTIC:** Read SPEC §5.6 (L441-507), counted every schema against each authoring item's claim (H0=6, H1=11, H2=6, H3=10, H4=8). All match. Tool evidence: Read SPEC L441-507; cross-ref task L205/217/221/225/233.
- **Command-surface operational correctness — SEMANTIC (the FAIL):** rf-qa's structural pass cannot catch that `--task-file` is non-existent or that post-mode needs `--diff`/`--task-log`. grep'd reflect.md + sc-reflect-protocol/SKILL.md for flag surface + STOP conditions. Tool evidence: reflect.md L10/L33; SKILL.md L68/L72/L97/L109/L584.
- **Anchor existence — SEMANTIC:** grep'd the REAL SKILL.md/report-template.md/remediation-handoff.md to confirm each named anchor exists verbatim (found the 4-backtick + paraphrase discrepancies). Tool evidence: grep of all three source files.

## Confidence Gate
- Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement
- Read: 6 | Grep: 9 | Glob: 0 | Bash: 9 (each call directly verified a specific claim)

## Recommendations
- Pre-execution (post-G1): apply Issue #1 to Step 8.15 — `--task-file` → `--tasklist`, add `--diff <BASE>..HEAD`. Only finding that blocks the literal gate from running.
- Apply Issues #2/#3 (anchor-description precision) to reduce executor mis-identification on the report-template fence and the handoff gating note. Low-risk (heading-text anchors mitigate) but descriptions should match real files.
- No CRITICAL findings. The advisory 4-token invariant is correctly and exhaustively guarded across refs, SKILL, report-template, handoff, the verdict test, the domain QA lens (8.8), and the POST-reflect verification instruction (1)-(2). Schema fidelity, test mapping, G1 gate, OI HALT markers, sync/lint/pytest gates all operationally correct.

## QA Complete
**VERDICT: FAIL** (1 IMPORTANT + 2 MINOR; all with concrete remediations; 0 CRITICAL).
