```yaml
contract_version: 1.9.0
status: success
review_verdict: FAIL
finding_counts: {blocking: 1, label_high: 1, medium: 5, note: 3}
mode: pre
tier_reached: 2
confidence_calibrated: 0.81
confidence_source: original selected reviewer card, not merged-report recalibration
citations_total: 21
citations_revalidated: 21
citations_dropped: 0
citations_inferred: 0
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

# Swarm help plan review

## Summary

**Plan verdict: FAIL.** The independent merged review found one Blocking (Missing) input gap in Task 4, five Medium warnings and three Notes. The final task requires comparing public invocations before/after the correction, but its isolated reviewer is not given the earlier commands or baseline identities. Other Task 4 status/content/test-command/report checks remain possible.

The supported two-description correction, behavior boundaries and historical evidence preservation are substantively covered. A plan-only input correction and independent re-review are needed before execution; no correction is made by this review. Full trace: `./adversarial/merged-review.md`, with debate, scoring, probe and merge receipts retained. Convergence was 11/12 points (0.916667); the remaining presentation preference was settled by documented base selection. Original selected-card calibration is 0.81, not a new confidence score for the merged report or product fix.

## Coverage matrix

The independent extraction and deterministic matching receipt is `./coverage-matrix.md`. There are 4 task items, 0 parsed requirement IDs and 12 quote-pinned inferred requirements. Parsed-only coverage is null; literal union coverage is **0.5 (6/12)**, with six literal nonmatches, not an invented 100%. Semantic scope obligations can be present in global Constraints while failing a single-task word-containment rule; the independent Tier 2 review adjudicates substance separately. Sparse source labeling forced Tier 2, with the low initial card calibration (0.68) and density 0.5 independently supporting escalation.

| Planned work | Task |
|---|---|
| Reproduce validate-lenses public help mismatch | Task 1 |
| Reproduce scaffold mismatch and pin unknown-option rejection | Task 2 |
| Correct validate-lenses description without behavioral changes | Task 3 |
| Correct scaffold description; retain repaired outputs and require applied-fix review | Task 4 |

None of those future implementation checks is reported as executed by this review.

## Inferred requirements (Pass 2)

| INF id | Verbatim source quote | Citation | Literal match |
|---|---|---|---|
| INF-001 | Create a checked implementation plan only for issue 568, swarm help advertises unsupported --custom-prompt-dir. | ../../source.md:1 | none; scope in title/Constraints |
| INF-002 | Preserve blocked/partial historical diagnosis and all pending verification requirements. | ../../source.md:1 | none; scope in Constraints and Tasks 2/4 |
| INF-003 | Plan the supported two-help-description correction in src/superclaude/cli/swarm/commands.py using JobSpec custom_prompt_dir with lens custom | ../../source.md:1 | Task 4 |
| INF-004 | reproducing regression tests failing before the edit and passing afterward | ../../source.md:1 | Task 1 |
| INF-005 | corrected public help captures | ../../source.md:1 | Task 2 lexically; Task 4 substantively |
| INF-006 | rejection of unsupported run option | ../../source.md:1 | Task 2 |
| INF-007 | independent review | ../../source.md:1 | Task 4 |
| INF-008 | No new CLI flag, prompt-loading changes, inline-custom-spec changes, injection-guard or metadata changes. | ../../source.md:1 | Task 3 |
| INF-009 | Work only in this isolated checkout. | ../../source.md:1 | none; Constraints |
| INF-010 | Do not replay counter-update.py or change diagnostic counters | ../../source.md:1 | none; Constraints |
| INF-011 | implement product code/tests, run models, commit, push, interact with GitHub or create worktrees | ../../source.md:1 | none; preceding Do not governs prohibition |
| INF-012 | User explicitly requests plan only, no implementation. | ../../source.md:1 | none; Constraints |

These twelve rows are inferred extraction with exact source quotations, not twelve non-load-bearing speculative claims. No source wording or plan text was changed to improve the score.

## Deviations

These are pre-execution findings, not product regressions. Original ids are preserved from the merged card.

### Deviation F1: Task 4 lacks named comparison inputs

- **Label / Grade:** HIGH / Blocking (Missing).
- **Location / mapped task:** `../../TASK-WF-createACheckedIm-20261123-195709.md:76-84`, Task 4 and its global Constraints.
- **Spec section:** governing stand-alone task rule, `/home/coder/.claude/skills/sc-workflow-protocol/refs/00_mdtm_template_simple_task.md:15`.
- **Evidence:** Task 4 says "same three CLI invocations as Task 2" and "after their preserved pre-edit observations", without naming the commands or earlier comparison files. `/home/coder/.claude/skills/sc-implement-protocol/refs/qa.md:9-31` defines task text plus Constraints and task-start diff, not sibling tasks, and restricts external evidence citations.
- **Classification:** drift from the governing template. Required input naming is absent in substance; affected acceptance is before/after invocation identity, not all content/status checking.
- **Default remediation:** a separately authorized plan-only correction must name the three public commands and baseline/red comparison inputs inside Task 4, then undergo independent re-review. Reconstructing only the after invocation does not establish sameness. No correction made here.

### Follow-up candidates: five Medium findings, nonblocking

- **F2, cross-task shorthand:** `../../TASK-WF-createACheckedIm-20261123-195709.md:47-66` delegates symbol/test naming to sibling tasks. The named regression file and behavior descriptions still allow intermediate checks, so not a second blocker. Optional clearer references must not trigger a fix pass.
- **F3, whitespace check:** `../../TASK-WF-createACheckedIm-20261123-195709.md:36-50` requires normalization but does not distinguish collapsing from removing whitespace. Historical `../../../../../troubleshoot/bug-swarm-custom-prompt-help-20261123191427/validate-lenses-help.txt:7-17` shows the target intact and other hyphenated tokens split. Collapsing can yield `--custom- prompt-dir` and miss exact-option absence. Mechanism observed, future target failure unobserved; positive field assertions protect current red reproduction. Optional hardening: remove whitespace or join splits. Source width and raw-capture extension are documented in merged-review, not proof of a repaired-output failure.
- **F5, task-start versus whole-plan diff:** the Task 4 location above describes a final whole-plan diff, although the reviewer input contract above uses a per-task increment. Final verification remains executor-owned. This is a remedy limitation, not another blocker.
- **F6, admissible baseline evidence:** the reviewer citation contract above requires acceptance to require reading outside-touched-set files. Listing paths alone does not prove the comparison inputs will be usable. This is a separate Medium remedy limitation.
- **F7, retained evidence inventory:** Task 4 retains red/green/disposition evidence. The plan range for F2 names the additional green and disposition outputs. Three commands and four baseline paths are not an exhaustive inventory. This is the third distinct Medium remedy limitation.

The independent sufficiency warning overlaps F5-F7 and is not counted again. Its Low wrapping extension folds into F3; the Task 3 interaction concern was addressed. No Medium item authorizes plan/product edits or starts a fix pass.

### Notes: three, nonblocking

- Earlier receipt wording must distinguish observed general wrapping from unobserved future target splitting.
- A fixed independent-review report basename is form, not a missing review: persistence and the review itself are already required.
- `<custom-prompt-dir>/system.txt` is an excluded directory placeholder, not the rejected option or an added help surface.

**Finding counts:** `{blocking: 1, label_high: 1, medium: 5, note: 3}`. Only F1 causes FAIL. The plan and all historical evidence remain unchanged.

## Review scope and limitations

This is pre-execution plan review, not implementation or repaired-state acceptance. Product code/tests, historical diagnostic evidence and the plan are immutable inputs. No pytest, public CLI replay, real model job, GitHub action, commit, push or worktree operation is authorized by this review.

Codegraph readiness was fresh at 2026-11-23T20:08:34Z. Native source Reads confirmed the two help producers, public callback registrations, custom-directory field binding and inline-custom allowance. External semantic retrieval was not used; the local symbol/Read floor supplies this bounded review's evidence. No exhaustive repository or third-party API behavior claim is made.

Model aliases were resolved from the three configured slots. Executor class was not resolvable from a flag, environment value or task log, so executor exclusion cannot be guaranteed. Requested model-class variation is not measured runtime identity. Vendor diversity is not proven for the gateway-routed slot; no claim that bias was eliminated is made.

A new 19-file input snapshot was computed with UV's no-project mode and pinned before this output tree was created. The earlier failed attempt's reported environment bootstrap remains unchanged; this review does not clean it up or treat it as test evidence. The earlier missing review remains a historical failure, not a fabricated prior PASS.

## Inferred-claim audit

- `citations_inferred: 0`. No speculative report finding is presented as established evidence.
- Inferred-fraction is 0 over the independently validated citation count recorded in the header.
- The twelve quote-pinned inferred requirements are source extraction, not speculative report claims. Their exact quotes and the literal coverage calculation are checked separately.
- Requested model diversity and original-card confidence do not establish independence of actual routed models or probability of a successful product fix.

## Recommendations

### Recommendation R-001: Correct Task 4's comparison inputs before execution

- **File:** `../../TASK-WF-createACheckedIm-20261123-195709.md`, Task 4. This review does not edit it in place.
- **Change:** after separate plan-correction authorization, use the registered workflow revision route to make a replacement plan naming `uv run superclaude swarm validate-lenses --help`, `uv run superclaude swarm scaffold --help`, and `uv run superclaude swarm run --custom-prompt-dir <existing temporary directory>`, with the earlier comparison artifacts identified in Task 4. Do not claim merely naming these proves a complete repair; the three Medium remedy limitations remain recorded for the later reviewer.
- **Verifier:** a fresh independent reader given only revised Task 4 plus Constraints can locate its commands and earlier evidence and check the required before/after comparison. Re-review only the blocker/changed scope, not Medium-only warnings.
- **Linked deviation:** F1. **Priority:** P1.

Do not implement the current blocked plan. The five Medium candidates and three Notes are retained in the merged review for follow-up only; no issues were opened, and no Medium-only edit was made. No product test/public CLI replay, model job, commit, push, GitHub action or additional worktree has been authorized. Historical repaired-state blockers remain unproven. Global memory/aggregate writes outside this planning package are skipped to preserve the invocation's scope.
