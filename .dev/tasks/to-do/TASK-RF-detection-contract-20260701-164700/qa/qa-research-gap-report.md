# QA Report — Research Gate

**Topic:** Locked detection contract setup flow task-builder research
**Date:** 2026-07-01
**Phase:** research-gate
**Fix cycle:** N/A

---

## Overall Verdict: FAIL

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory, Status, Summary | FAIL | Bash inventory found four research files plus analyst report. Read verified all four research files have `Status: Complete`, but only `03-validation-tests.md:217` has `## Summary`; `01-file-inventory.md`, `02-patterns-integration.md`, and `04-template-examples.md` lack required Summary sections. Read also verified analyst report is `Verdict: PENDING` at `qa/analyst-cross-validation-report.md:7` and contains no completed checklist content. |
| 2 | Evidence density | PASS | Read all four research files. Bash path existence check verified primary cited source paths exist. Evidence density is Adequate-to-Dense: most code/source claims cite specific absolute paths plus line ranges/symbols, e.g. `01-file-inventory.md:39-45`, `02-patterns-integration.md:21-25`, `03-validation-tests.md:21-38`, `04-template-examples.md:13-17`. |
| 3 | Scope coverage against research-notes EXISTING_FILES | PASS | Read `research-notes.md:10-42` and all research files. Primary design inputs are covered in `01-file-inventory.md:121-138`; core `detection.py`, `classifier.py`, pr-submit skill/command, reflect CLI/command, and tests are covered in `01-file-inventory.md:37-119`, `02-patterns-integration.md:13-84`, and `03-validation-tests.md:17-169`. |
| 4 | Documentation cross-validation tags | FAIL | Bash scan found zero `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, or `[UNVERIFIED]` tags across research. Research contains many doc-sourced/template/design claims, e.g. `04-template-examples.md:13-17` and `02-patterns-integration.md:15-17`, without required tags. Some were independently verified by Read/Bash, but the research files themselves are not compliant. |
| 5 | Contradiction resolution | FAIL | Read found unresolved conflict around the exact no-side-effect halt sentence. Source requirements require `“No monitor was armed. No comments, pushes, retries, resolves, or retriggers were performed.”` at `merged-requirements.md:304`. `03-validation-tests.md:146-147` preserves that sentence, but `02-patterns-integration.md:61-64` recommends different text: `No monitor armed; no poll, push, reply, resolve, retrigger, or resume was started.` No research file resolves which literal the task-builder should encode. |
| 6 | Gap severity | FAIL | `research-notes.md:53-67` lists open decisions and coverage caveats that must be represented. Research files do not include `Gaps and Questions` sections; analyst report is pending. The unresolved exact-halt-text conflict is IMPORTANT because it can cause a tasklist to encode a non-contractual acceptance test. |
| 7 | Depth appropriateness for Deep tier | PASS | Deep-tier end-to-end flow is traced across design and research: `01-file-inventory.md:140-145` identifies package/test/integration targets; `02-patterns-integration.md:13-84` traces pr-submit halt and reflect CLI seams; `03-validation-tests.md:40-169` maps diagnosis → questions → validation → writer → pr-submit/reflect integration tests; `design.md:459-507` independently confirms end-to-end integration sequence. |
| 8 | Integration point coverage | PASS | Read verified integration points are covered: pr-submit Wave 1/for_arming seam in `02-patterns-integration.md:13-25`, no-side-effect boundaries in `02-patterns-integration.md:48-57`, reflect CLI `contract-status` placement in `02-patterns-integration.md:40-46`, source sync in `02-patterns-integration.md:77-84`, and reflect CLI tests in `03-validation-tests.md:153-169`. |
| 9 | Pattern documentation | PASS | Patterns are documented: source-of-truth/sync and `.claude` non-staging in `02-patterns-integration.md:77-84` and `04-template-examples.md:51-57`; B2 checklist/task template conventions in `04-template-examples.md:19-35`; UV validation commands in `03-validation-tests.md:179-215`; writer/no-side-effect patterns in `03-validation-tests.md:123-177`. |
| 10 | Incremental writing compliance | FAIL | No research file contains a findings log or incremental append evidence except `03-validation-tests.md:5` (`## Findings Log`). The other three files have polished one-shot structures and no incremental log/gaps/scratch sections. Given the RF rule, this is a MINOR process failure and raises risk of lost intermediate findings. |

## Summary
- Checks passed: 5 / 10
- Checks failed: 5
- Critical issues: 1
- Important issues: 3
- Minor issues: 1
- Issues fixed in-place: 0 (fix_authorization: false)

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 10 | Grep: 0 | Glob: 0 | Bash: 6 | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0

Unchecked items: none.

Unverifiable items: none.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/qa/analyst-cross-validation-report.md:7-13` | Completeness verification report is incomplete: verdict is `PENDING` and the file has no actual cross-validation findings. The research gate input explicitly includes the analyst completeness report; a pending stub cannot support synthesis/task-building. | Complete the analyst cross-validation report or replace it with a finished report that verifies coverage and resolves/records findings. |
| 2 | IMPORTANT | `research/01-file-inventory.md`, `research/02-patterns-integration.md`, `research/04-template-examples.md` | Required Summary section is missing in 3 of 4 research files. Status is present, but the research-gate checklist requires both `Status: Complete` and a Summary section. | Add concise `## Summary` sections to each missing file summarizing task-builder-relevant facts and residual caveats. |
| 3 | IMPORTANT | `research/02-patterns-integration.md:61-64` vs `research/03-validation-tests.md:146-147` and `merged-requirements.md:304` | Unresolved contradiction on exact halt text. Requirements mandate: `No monitor was armed. No comments, pushes, retries, resolves, or retriggers were performed.` Research 02 recommends a different sentence that omits `comments` and `retries`, adds `poll`/`resume`, and changes wording from `No monitor was armed` to `No monitor armed`. | Replace or annotate the Research 02 recommendation so the exact required sentence is the normative literal, while any additional explanatory text is clearly non-normative. |
| 4 | IMPORTANT | All research files | Documentation-sourced claims are not tagged with `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, or `[UNVERIFIED]`. This violates the research-gate doc cross-validation contract and makes it harder for the builder to distinguish code-backed facts from template/design assertions. | Add tags to doc-sourced claims. For code-backed claims, add `[CODE-VERIFIED]` after independently verifying the cited source. For template/design-only claims, mark `[UNVERIFIED]` or clearly state they are source requirements rather than observed code. |
| 5 | MINOR | `research/01-file-inventory.md`, `research/02-patterns-integration.md`, `research/04-template-examples.md` | Incremental writing compliance is weak. Only `03-validation-tests.md` has a `## Findings Log`; the other files look one-shotted. | Add a short findings log or revision/collection trail to the affected files, or document why incremental evidence is unavailable. |

## Gap-Detection Notes for Task Builder
- The research does substantially cover the track-specific risk areas: all 16 setup questions (`03-validation-tests.md:66-83`, requirements source `merged-requirements.md:79-150`), omitted surfaces (`03-validation-tests.md:104-113`), cross-PR shape-only behavior (`03-validation-tests.md:118-119`, source `merged-requirements.md:193-194` and `266-268`), safe writer gates (`03-validation-tests.md:123-137`, source `merged-requirements.md:190-203`), and reflect CLI/readiness surface (`02-patterns-integration.md:40-46`, `03-validation-tests.md:153-169`).
- The task-builder must still treat Fork A, Fork B, and live capture timing as human-decision gates because `research-notes.md:53-67` and `design.md:577-586` identify them as open decisions. Do not let the generated tasklist silently default dependent work without a halt/acceptance item.
- The exact no-side-effects sentence is the main builder-blocking content conflict. If left unresolved, the tasklist can pass research coverage while implementing the wrong literal acceptance test.

## Actions Taken
- No research files were modified because `fix_authorization: false`.
- Wrote this QA report to `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/qa/qa-research-gap-report.md`.

## Recommendations
- Resolve all five findings before synthesis/tasklist assembly.
- Prioritize the analyst report completion and exact halt-text contradiction first; these directly affect whether the generated MDTM tasklist encodes the locked setup contract correctly.
- After fixes, rerun a research-gate fix-cycle focused on the five findings above.

## QA Complete

VERDICT: FAIL
