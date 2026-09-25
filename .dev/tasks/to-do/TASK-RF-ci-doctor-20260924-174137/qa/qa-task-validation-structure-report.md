# QA Report — Task Integrity (Phase Structure)

**Topic:** CI doctor-check native install prerequisite
**Date:** 2026-09-24
**Phase:** task-integrity
**Fix cycle:** N/A
**Scope:** Read-only task/workflow review; report output only. No task execution or changes authorized.

---

## Overall Verdict: FAIL

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Template 01 frontmatter and mode | PASS | Task lines 1–51 use template-01 `created_date`, `depends_on`, `spec_path`, and `reflect_post_mode: skill`; template lines 1–61 confirm schema; skill-mode keys `start_commit`/`executor_model_class` are absent as required by task-builder lines 2310–2312. |
| 2 | Phase order and item count | PASS | Task lines 97–135 contain 1 preparation, 1 edit, 3 validation, 3 closeout items in that order; Grep verified all eight `- [ ]` items and four numbered phase headings. |
| 3 | Item-level producer/consumer ordering | PASS | Edit 2.1 precedes tests/diff 3.1–3.3; evidence-producing 3.x precede 4.1 diff capture; 4.1 precedes 4.2 POST; 4.2 precedes 4.3 Done (task lines 103–135). |
| 4 | Authorization and execution boundaries | PASS | Task lines 59, 69, 101 explicitly require separate authorization before execution; task lines 59, 90, 101, 135, 165 prohibit unauthorized commit, push, PR changes. BUILD-REQUEST lines 19–20 require separate execution and POST gate. |
| 5 | PRE gate required when spec resolves | FAIL | BUILD-REQUEST line 13 names an existing spec (Read of `.dev/specs/ccsession-native-install.md`); task lines 18–26 mark PRE `skipped` with empty run_id/report. Task-builder A.10.7 lines 1664–1701 prohibit that. No `reflect/pre/` files matched Glob. |
| 6 | Deterministic PRE sign-off | FAIL | Task lines 20–26 contain `tcs: 0`, no tier/reviewed timestamp and no real PRE run identifier; task-builder lines 1686–1701 explicitly declare zero TCS and empty run_id malformed when a spec exists. |
| 7 | Skill-mode POST runner | FAIL | Task line 131 has a summarized instruction to spawn one runner, not the complete verbatim Agent-tool prompt and hard completion contract in task-builder lines 2217–2233/2310. |
| 8 | POST audit coverage and on-disk verification | FAIL | Task line 127 captures an unstaged workflow.diff; task line 131 passes that file rather than rule-20 `--diff {BASE}..HEAD`, omits `--remediate`, waves-attestation, and EV-3 independent disk verification/retries specified at task-builder lines 2223–2233. |
| 9 | Local validation coverage | PASS | Task lines 113, 117, 121 require existing integration tests, isolated HOME negative/positive doctor sequence, diff/format and `make verify-sync`; workflow lines 213–219 and tests lines 113–151 independently confirm referenced surfaces. Remote check is honestly deferred (task line 165). |
| 10 | Workflow scope and production behavior | PASS | Task lines 63–72, 107, 121 restrict edit to one step in doctor-check; actual workflow lines 213–219 place dependency install immediately before unchanged doctor. Spec FR-1 (lines 97–109) and FR-4 (lines 140–150) support the planned validation. |

## Summary
- Checks passed: 6 / 10; failed: 4.
- Critical issues: 2; important issues: 2; minor issues: 0.
- Issues fixed in-place: 0 (fix authorization false).
- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 13 | Grep: 6 | Glob: 2 | Bash: 1. No external lookups required.
- Unverifiable: none. Unchecked: none. This is a scoped phase-structure review, not an assertion that every item of the general 27-point task-integrity checklist passed.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | Task frontmatter lines 18–26 | Existing explicit spec but `reflect_pre.verdict: skipped`, no report, empty run_id. A.10.7 mandatory PRE cannot be skipped with a resolved spec. | Builder must actually run `sc:reflect-protocol` PRE against this task and spec before presenting it; save the on-disk PRE report and its real run_id/verdict/coverage/tier/review timestamp. If the skill cannot run, surface the hard blocker, not a skip. |
| 2 | IMPORTANT | Task frontmatter lines 19–26 | `tcs: 0` is explicitly malformed, and `depth: quick` is not supported by a recorded deterministic FER computation. Missing `tier_reached` and `reviewed_at` compound the incomplete sign-off. | Compute S1–S6 on the finished task and spec using task-builder TCS FER; record actual nonzero TCS and derived PRE depth, tier and timestamp from the completed run. Independently check required POST depth against the same score. |
| 3 | CRITICAL | Task Step 4.2, line 131 | Skill-mode POST is an abbreviated paraphrase rather than rule-20's complete verbatim dedicated general-purpose Agent prompt. Missing `--remediate`, full tier/wave requirements, return contract with tier/waves attestation, `RUN_INCOMPLETE` hard completion contract, independent EV-3 on-disk artifact verification and bounded retries. Recording only a verdict can falsely complete the gate. | Emit the entire matching Rule 20 skill-mode POST runner form, including exact subagent invocation and full prompt, completion and EV-3 checks; keep it immediately before Done, with no CLI-mode wrapper or executor-model flag. |
| 4 | IMPORTANT | Task Steps 4.1–4.2, lines 127–131 | The specified POST input is an unstaged `workflow.diff`, while the required runner prompt uses `--diff {BASE}..HEAD`. In this task no commit/stage/push is authorized, so a `BASE..HEAD` commit range cannot contain the newly uncommitted YAML change. Neither a shortened custom diff invocation nor a clean pre-change commit range demonstrates a complete compliant POST audit. | Resolve this contract conflict before task execution: obtain an explicitly supported reflect invocation that audits the actual authorized uncommitted change without committing, or stop and seek separate authorization for a different execution/audit sequence. Do not silently mark POST PASS on an audit that missed the workflow edit. |

## Actions Taken
- Read task, BUILD-REQUEST, template, referenced spec, workflow, research notes, test file and task-builder PRE/POST/TCS rules. Searched sign-off and runner requirements and checked the absence of PRE artifacts. Wrote this report only; no task, workflow, commit, push, test execution or PR action.

## Recommendations
- Resolve all four issues before treating the task file as executable or complete. In particular, do not claim PRE skipped with an explicit spec or POST complete from a verdict-only or ungrounded diff review.

## QA Complete
