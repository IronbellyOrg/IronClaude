# QA Report: Phase 2 Serialized Corrections

**Topic:** Fourteen consolidated research correction groups  
**Date:** 2026-10-23  
**Status:** Source-backed patches proposed, not applied  
**Phase:** phase-gate fix  
**Lens:** Serialized source-backed corrections only  
**Fix cycle:** 1, application pending  
**Governing template:** Task Standard QA Report Output Format and Serialized Fix Protocol  
**Intended fix-log path:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-phase-2-fix-log.md`

## Overall Verdict

**FAIL**

All 14 findings remain open on disk because higher-priority instructions prohibit this agent from writing research or QA reports. The 62 surgical patches below cover all 14 groups across 13 research files. Their sequential match counts were checked against the actual files through in-memory application; no research target was modified.

This is correction preparation, not independent verification or a gate PASS.

## Items Reviewed

| Finding | Required correction | Result | Verified evidence and proposed treatment |
|---|---|---|---|
| P2-F01 | Partition-a takeaway lists | FAIL, unapplied | Read all five affected targets and the governing research template. Add section-ending lists, preserve existing conclusions and distinguish original source anchors from shifted research-file lines. |
| P2-F02 | Two short screening summaries | FAIL, unapplied | Both existing summaries contain two sentences. Expand each to four sentences using established dispositions and counting limits. |
| P2-F03 | Documentation-case staleness disposition | FAIL, unapplied | The completed documentation case lacks the required section. Add an evidence-bounded statement that no current architectural staleness finding was established. |
| P2-F04 | Partition-b takeaway lists | FAIL, unapplied | Read both cases and both screens completely. Supply missing lists throughout the substantive sections and supplements, without changing historical findings. |
| P2-F05 | Second screening summary | FAIL, unapplied | Expand to four sentences, retaining the separate cannot-verify observation and unchanged-plan control. |
| P2-F06 | Monitor staleness disposition | FAIL, unapplied | Add the missing disposition without converting historical uncertainty into a new documentation defect. |
| P2-F07 | Partition-c takeaway lists | FAIL, unapplied | Convert five monitor prose takeaways, complete its remaining section lists, complete credential lists and convert the screening takeaway paragraph. |
| P2-F08 | Write mislabeled Edit | FAIL, unapplied | Original planning records 544 and 545 establish a successful whole-file Write. Correct the finished screen and its verification qualifier; leave the capture unchanged. |
| P2-F09 | Historical loaded-rule mapping | FAIL, unapplied | Independently decoded both original record-18 Read results and verified both captured-content hashes. Map each version to its actual reviewer and verdict record. |
| P2-F10 | Four retained CI dispositions | FAIL, unapplied | Read both actual plans, revised source, reviewer card, final report and completed probe. Add historical requirements, before/after comparisons, validity, causal classifications and bounded unknowns for all four findings. |
| P2-F11 | Two withdrawn CI claims | FAIL, unapplied | The first reviewer card contains both claims; the final report explicitly withdraws them against revised source instructions. Preserve them as rejected-finding counterevidence, not additional retained findings. |
| P2-F12 | Older-pin discovery history | FAIL, unapplied | Original monitor record 697 already describes older-pin behavior as nonblocking. Record 804 newly demonstrates equal tags and treats the combined problem as a defect. Correct the case and every affected deck classification. |
| P2-F13 | Eight credential observations | FAIL, unapplied | Read the complete third-final response and preserved plan, ledger, acceptance, manpage and sweep evidence. Add all eight dispositions, including the acceptance-record mismatch, without promoting every observation into a delivery defect. |
| P2-F14 | Five monitor reviewer identities | FAIL, unapplied | Verified five identity-bearing dispatch results, continuation targets and all seven verdict identities. Add the complete mapping and deck cross-reference. |

## Summary

- Finding groups source-checked: **14 / 14**.
- Findings resolved on disk: **0 / 14**.
- Findings remaining open on disk: **14**, comprising **6 IMPORTANT and 8 MINOR**.
- Proposed patches: **62**, covering **13 research files**.
- Expected replacement counts: checked successfully in listed order.
- Research, production, historical package, capture, task-checklist and hypothesis-card writes: **0**.
- New agents, gates, tests, investigated executions, Git operations and external publication: **0**.

**Confidence:** Verified: 14/14 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

This measures source-check coverage for the proposed corrections, not successful application or independent acceptance.

**Tool engagement:** Read: 45 | Grep: 0 | Glob: 0 | Bash: 13

Dedicated search tools were unavailable; bounded `rg` and UV-based read-only extraction supplied searches and original-record verification. No external research was performed. One temporary Python input was written solely to validate proposed substitutions in memory; it wrote no research targets or report files.

## Issues Found

All original findings remain open solely because these patches are unapplied. No severity exemption or waiver is proposed.

Historical unknowns remain explicit in the proposed text, including rubric-update authorship, individual reviewer-miss reasons, exact introduction history where unavailable and unobserved runtime outcomes. These unknowns are not filled with invented facts.

One attempted Read used an unavailable original-plan done location; verification recovered through its actual to-do location. The first raw capture-containment check encountered displayed Read line prefixes; removing those prefixes recovered both complete captured texts and confirmed their recorded hashes.

## Actions Taken

- Read the existing fix-log stub, complete consolidated findings, relevant original reports and governing templates.
- Read all 13 affected research targets, including the complete evidence deck.
- Independently verified primary evidence for each factual correction.
- Prepared append-only historical-accounting tables and localized factual, summary, formatting and cross-reference changes.
- Checked all 62 expected match counts through sequential in-memory substitution.
- Changed no research file and populated no report stub.

## Citation Stability and Source Evidence

All original physical JSONL records, source captures, historical plans, reviewer cards, debate artifacts and historical ledgers remain immutable.

The proposed additions use stable headings and explicitly identified source frames. Existing research cross-references use filenames and section names rather than numeric case-file locations. Necessary in-scope cross-references are included below.

Selected **proposed**, not applied, line movements are:

| Research file | Stable heading or boundary | Original → proposed line |
|---|---|---|
| `01-session-ac2cd1fd.md` | Evidence integrity and hashes | 321 → 321 |
| `01-session-ac2cd1fd.md` | Resume traceability supplement | 417 → 425 |
| `02-session-a9b88895.md` | Subsequent outcome and excluded events | 275 → 277 |
| `03-session-6f744b87.md` | Summary and recommended action | 305 → 316 |
| `04-session-43582de1.md` | Final merged finding inventory | 316 → 334 |
| `04-session-43582de1.md` | Resume traceability supplement | 534 → 576 |
| `05-session-e002bed2.md` | Classification of later findings | 107 → 113 |
| `05-session-e002bed2.md` | Separately timed continuation | 289 → 315 |
| `06-session-0690ee9f.md` | Remaining findings versus actual regressions | 260 → 268 |
| `06-session-0690ee9f.md` | Resume traceability supplement | 329 → 349 |
| `scope-rules.md` | Historical Versus Current Rules | 41 → 53 |
| `evidence-deck.md` | Why Earlier Reviews Missed Later Findings | 573 → 579 |

**Out-of-scope downstream follow-up:** Numeric research citations in these existing synthesis files require refresh after application. They were not edited:

- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/synth-01-problem-current-state.md`
- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/synth-02-target-gaps.md`

Original QA reports retain their initial observation locations and verdicts; they must not be rewritten as though they reviewed the corrected files.

## Exact Patches

**Application contract:** Apply in listed order. `literal` means exact string replacement. `regex` uses Python `re.sub` semantics, including `\g<1>` and replacement `\n` escapes. Check `expected_count` immediately before each replacement. Regex matches can be expanded in memory into exact old/new blocks for dedicated editing tools. Stop rather than coerce a count mismatch. These are proposed and unapplied.

```json
[
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-01.md",
    "mode": "literal",
    "needle": "## Observed Sequences and Evidence",
    "repl": "**Key Takeaways**\n\n- Six membership slots retain three selections and three different exclusions.\n\n## Observed Sequences and Evidence",
    "finding_ids": ["P2-F04"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-01.md",
    "mode": "regex",
    "needle": "(?m)^(Three\\ selected\\ sessions\\ represent[^\\n]*)$",
    "repl": "- \\g<1>",
    "finding_ids": ["P2-F04"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-02.md",
    "mode": "literal",
    "needle": "## Observed Sequences and Evidence",
    "repl": "**Key Takeaways**\n\n- All six slots are controls or exclusions, not strict repeated-failure positives.\n\n## Observed Sequences and Evidence",
    "finding_ids": ["P2-F04"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-02.md",
    "mode": "regex",
    "needle": "(?m)^(Zero\\ strict\\ repeated\\-failure\\ chains[^\\n]*)$",
    "repl": "- \\g<1>",
    "finding_ids": ["P2-F04"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-03.md",
    "mode": "literal",
    "needle": "## Observed Sequences and Evidence",
    "repl": "**Key Takeaways**\n\n- Session 15 is selected; session 17 remains a separate bounded-repair control.\n\n## Observed Sequences and Evidence",
    "finding_ids": ["P2-F07"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-03.md",
    "mode": "regex",
    "needle": "(?m)^(Session15\\ supplies[^\\n]*)$",
    "repl": "- \\g<1>",
    "finding_ids": ["P2-F07"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-04.md",
    "mode": "literal",
    "needle": "## Observed Sequences and Evidence",
    "repl": "**Key Takeaways**\n\n- Session 20 is selected; session 19 and four synthetic exclusions remain separate.\n\n## Observed Sequences and Evidence",
    "finding_ids": ["P2-F01"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-04.md",
    "mode": "regex",
    "needle": "(?m)^(Session20\\ is\\ one\\ planning\\ incident[^\\n]*)$",
    "repl": "- \\g<1>",
    "finding_ids": ["P2-F01"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-05.md",
    "mode": "literal",
    "needle": "## Observed Sequences and Evidence",
    "repl": "**Key Takeaways**\n\n- All six slots retain one selection, one unrelated session, one setup-only session and three synthetic exclusions.\n\n## Observed Sequences and Evidence",
    "finding_ids": ["P2-F01"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-05.md",
    "mode": "regex",
    "needle": "(?m)^(One\\ selected\\ strict\\ repeated\\ review\\ failure[^\\n]*)$",
    "repl": "- \\g<1>",
    "finding_ids": ["P2-F01"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-04.md",
    "mode": "literal",
    "needle": "### Separate implementation history must not be back-attributed",
    "repl": "**Key Takeaways**\n\n- The two screening review results are partial; final causal accounting belongs to the dedicated planning case.\n\n### Separate implementation history must not be back-attributed",
    "finding_ids": ["P2-F01"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-04.md",
    "mode": "literal",
    "needle": "544 actual version2 Edit",
    "repl": "544 whole-file Write creating version 2,545 successful Write result",
    "finding_ids": ["P2-F08"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-02.md",
    "mode": "literal",
    "needle": "Screening complete for07-12. Retain successful one-repair case and concurrency controls; exclude all six from strict-positive session count.",
    "repl": "Screening is complete for indexes 07-12. Retain the successful one-repair case and concurrency controls, but exclude all six from the strict-positive session count. Session 10's separate Task 6 cannot-verify observation is not joined to its Task 4 repair. Session 11's parallel reviews concern an unchanged plan, not successive repair rounds.",
    "finding_ids": ["P2-F05"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-04.md",
    "mode": "literal",
    "needle": "Screening complete for19-24: one selected substantive repeated plan-review session, one operational control, four synthetic exclusions. Full exact screening/provenance remains in screening-handoffs-source.txt.",
    "repl": "Screening is complete for indexes 19-24: one selected substantive repeated plan-review session, one operational control and four synthetic exclusions. Session 20 remains one planning incident rather than multiple independent cases. Session 19's nine compliant task reviews do not acquire later Task 12 events from the shared ledger. Full exact screening and provenance remain in screening-handoffs-source.txt.",
    "finding_ids": ["P2-F02"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-05.md",
    "mode": "literal",
    "needle": "Screening complete for25-30: one selected session, one unrelated operational session, one setup-only session, three synthetic exclusions. Full provenance and original event identifiers are in screening-handoffs-source.txt.",
    "repl": "Screening is complete for indexes 25-30: one selected session, one unrelated operational session, one setup-only session and three synthetic exclusions. The oracle case retains the known frozen-fixture finding rather than demonstrating a repair-introduced defect. Opening Task 11 carry-over is not another newly observed incident. Full provenance and original event identifiers remain in screening-handoffs-source.txt.",
    "finding_ids": ["P2-F02"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/01-session-ac2cd1fd.md",
    "mode": "regex",
    "needle": "(?m)^(First\\ and\\ second\\ `input\\-snapshot\\.yaml`\\ files\\ contain[^\\n]*|\\*\\*Historical\\ line\\ convention:\\*\\*\\ Every[^\\n]*|“Fixed”\\ here\\ means[^\\n]*|The\\ reviewed\\ v1\\ contains[^\\n]*|A\\ bounded\\ metadata\\-only\\ extraction\\ from\\ the\\ exact\\ original\\ Session\\ path\\ above\\ verified[^\\n]*)$",
    "repl": "**Key Takeaways**\\n\\n- \\g<1>",
    "finding_ids": ["P2-F01"],
    "expected_count": 5
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/01-session-ac2cd1fd.md",
    "mode": "regex",
    "needle": "\\Z",
    "repl": "\n**Key Takeaways**\n\n- The six transition identifiers retain their original JSONL record numbers, timestamps and UUIDs.\n",
    "finding_ids": ["P2-F01"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/02-session-a9b88895.md",
    "mode": "regex",
    "needle": "(?m)^(Graph\\ coverage\\ reported\\ the\\ investigated\\ worktree\\ paths\\ excluded[^\\n]*|They\\ occurred\\ during\\ initial\\ builder\\ development[^\\n]*|Original\\ event\\ UUIDs\\ and\\ complete\\ timestamps\\ are\\ preserved[^\\n]*)$",
    "repl": "**Key Takeaways**\\n\\n- \\g<1>",
    "finding_ids": ["P2-F01"],
    "expected_count": 3
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/02-session-a9b88895.md",
    "mode": "literal",
    "needle": "Earlier report line anchors are unchanged.",
    "repl": "Original physical JSONL anchors and the preserved capture remain unchanged; formatting corrections can move this research file's lines.",
    "finding_ids": ["P2-F01"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/03-session-6f744b87.md",
    "mode": "literal",
    "needle": "- No production files were edited, no tests were executed, no nested agents were launched, and no remediation task was run.",
    "repl": "**Key Takeaways**\n\n- No real render evidence was established; the historical baseline comparison and unchanged rendering blocker remain distinct.\n- No production files were edited, no tests were executed, no nested agents were launched, and no remediation task was run.",
    "finding_ids": ["P2-F04"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/03-session-6f744b87.md",
    "mode": "literal",
    "needle": "## Summary and recommended action",
    "repl": "## Stale Documentation Found\n\nNo current architectural staleness finding was established within this investigation. The older architectural analysis was used for provenance, not accepted as current implementation proof; the rendering and baseline-provenance findings do not establish a stale-documentation defect.\n\n**Key Takeaways**\n\n- No stale-documentation cause is established by the inspected evidence.\n\n## Summary and recommended action",
    "finding_ids": ["P2-F03"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/03-session-6f744b87.md",
    "mode": "literal",
    "needle": "Earlier case text and line anchors are unchanged; this is traceability completion, not repeated causal analysis.",
    "repl": "The original JSONL records and identifier mapping remain unchanged; later formatting corrections can move research-file lines without changing those source anchors.",
    "finding_ids": ["P2-F04"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/03-session-6f744b87.md",
    "mode": "regex",
    "needle": "\\Z",
    "repl": "\n**Key Takeaways**\n\n- The eight identifiers refer to original physical JSONL records, not this research file's layout.\n",
    "finding_ids": ["P2-F04"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md",
    "mode": "regex",
    "needle": "(?m)^(No\\ implementation\\ run\\ or\\ resulting\\ product\\-code\\ regression\\ was\\ observed\\.[^\\n]*|The\\ knowledge\\ graph\\ explicitly\\ excludes\\ the\\ worktree\\ subtree\\.[^\\n]*|The\\ second\\ debate\\ identified\\ a\\ workable\\ repair[^\\n]*|The\\ record\\ does\\ \\*\\*not\\*\\*\\ establish\\ context\\ exhaustion[^\\n]*|The\\ draft\\ report\\ was\\ first\\ written[^\\n]*|The\\ final\\ report\\ repeats\\ “16\\ original\\ findings\\ fixed[^\\n]*|This\\ also\\ qualifies\\ the\\ earlier\\ bounded\\ description[^\\n]*|These\\ are\\ evidence\\ of\\ defects\\ in\\ proposed\\ remediation\\ instructions\\.[^\\n]*|The\\ return\\ contract\\ also\\ records\\ an\\ input\\-tree\\ hash[^\\n]*|This\\ adds\\ missing\\ finding\\-level\\ accounting\\ to\\ the\\ same\\ CI\\-plan\\ case\\.[^\\n]*|“Final\\ report\\ item”\\ below\\ identifies[^\\n]*|A\\ file\\ can\\ still\\ have\\ exactly\\ one\\ decision\\ line[^\\n]*|The\\ reason\\ an\\ earlier\\ reviewer\\ missed\\ any\\ particular\\ valid\\ example\\ remains\\ unknown[^\\n]*)$",
    "repl": "**Key Takeaways**\\n\\n- \\g<1>",
    "finding_ids": ["P2-F04"],
    "expected_count": 13
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md",
    "mode": "literal",
    "needle": "## 10. Gaps and questions",
    "repl": "**Key Takeaways**\n\n- The regeneration was authorized, but no product-code scope violation or implementation outcome was observed.\n\n## 10. Gaps and questions",
    "finding_ids": ["P2-F04"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md",
    "mode": "literal",
    "needle": "## 2. Post-cutoff timeline and primary session anchors",
    "repl": "**Key Takeaways**\n\n- The completed review is not ready with partial evidence status; partial does not mean it was still running.\n\n## 2. Post-cutoff timeline and primary session anchors",
    "finding_ids": ["P2-F04"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md",
    "mode": "literal",
    "needle": "## 5. New probe concern: half-edited advisory header",
    "repl": "**Key Takeaways**\n\n- Confinement verification was already absent; no wrong-directory repository mutation was observed.\n\n## 5. New probe concern: half-edited advisory header",
    "finding_ids": ["P2-F04"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md",
    "mode": "literal",
    "needle": "## Two previously underexplained retained findings",
    "repl": "**Key Takeaways**\n\n- All eight second-reviewer entries retain their corrected, rejected or deduplicated dispositions.\n\n## Two previously underexplained retained findings",
    "finding_ids": ["P2-F04"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md",
    "mode": "literal",
    "needle": "Original report line anchors are unchanged.",
    "repl": "Original physical JSONL anchors remain unchanged; formatting corrections can move research-file lines.",
    "finding_ids": ["P2-F04"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md",
    "mode": "regex",
    "needle": "\\Z",
    "repl": "\n**Key Takeaways**\n\n- The four transition identifiers refer to immutable original JSONL records.\n\n## Additional retained and withdrawn finding dispositions\n\n**Source frames:** Original plan means `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/tasks/to-do/TASK-WF-spec-20261022-211556/TASK-WF-spec-20261022-211556.md`. Regenerated plan means `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/tasks/done/TASK-WF-specR1-20261023-031725/TASK-WF-specR1-20261023-031725.md`. Revised source is `source.md` in that same regenerated done package. Reviewer card, final report and completed probe mean the primary artifacts under `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-specR1-20261023-031725-20261023032025/` already identified above. These are source-file lines, not research-file lines.\n\n| Retained finding | Historical requirement and validity | Original versus regenerated evidence and causal class | Earlier miss and outcome limits |\n|---|---|---|---|\n| Decision serialization (D-009) | Original source requires recording the chosen input; revised source:69 requires one prefixed decision and :75 defines its consumer. Valid low machine-format ambiguity, not a demonstrated wrong execution. | Original plan:45,49,121,124 leaves a natural-language decision consumed by a later mapping check. Regenerated plan:48,52,145 adds prefix/cardinality and programmatic consumption without a grammar; `files` contains `file`. Preexisting format underspecification retained by an incomplete repair, with newly explicit ambiguous exact-one wording. Reviewer card:65-77; final report:80. This extends the residual already acknowledged in this case, rather than claiming serialization was wholly absent. | The recorded decision-file repair targets position and later appends, not serialization. Why the earlier reviewers did not require a machine grammar is unknown. No parser or incorrect upload was executed in this case. |\n| Failure-message output passes render comparison (D-014) | Source:24,38 requires meaningful before/after rendering and checks that reject wrong results. Valid acceptance weakness: nonempty identical failure text does not prove guarded paths were rendered. | Original plan:84,94 compares renders without requiring actual guarded paths. Regenerated plan:90,100 chooses a known pair and adds nonempty equality, still without requiring the path lines. Completed probe:13 records the historical workflow fallback `(diff unavailable)` and its counterexample; final report:85 retains it. Preexisting render-check weakness surviving a partial strengthening, not a proven repair-introduced regression. | The selected pair worked in the historical probe. No failed rendering run was observed; the issue is what the predicate permits. Why earlier reviewers missed the failure-text counterexample is unknown. `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.github/workflows/boundary-guard.yml:76-82` corroborates the fallback but is not substituted for an original-byte snapshot. |\n| Inconsistent status flags (D-015) | Source:39 requires comparison against the captured baseline, with positive scope evidence. Valid latent false-rejection risk, not an observed out-of-scope edit. | Original plan:34 captures `--porcelain -uall`, while :159 uses default status flags for the positive check. Regenerated plan:37 captures `-uall -z`, while :185 still uses default flags. Both versions can compare individual untracked paths against a collapsed directory entry; regeneration also leaves normalization of its converted NUL-delimited baseline unspecified for this consumer. Preexisting mismatch retained through baseline-parsing repair. Completed probe:15; final report:86. | Probe:15 explicitly reports no such untracked source/test directory at that observation. Actual failure therefore remains unobserved. The earlier-miss mechanism is unknown. |\n| Leftover line reference frame (D-016) | Source:35 and revised source:81 preserve a one-paragraph edit while disclosing remaining text with locations. Valid reference ambiguity, not proof the accepted leftovers are new delivery defects. | Original plan:150,160 requests numeric leftover references without naming a frame. Regenerated plan:174,176,186 still requests them while replacing base lines 7-12, which can move later lines. Inherited frame ambiguity, not a demonstrated new regression. Completed probe:16; final report:87. | The relevant numbers are historical base-file numbers, not guaranteed edited-file locations. No misleading executed leftovers artifact was observed. Why earlier reviewers did not name the frame is unknown. |\n\n| Withdrawn claim | Original substance and historical validity | Final disposition and counting |\n|---|---|---|\n| Prescribed path-filter conclusion (R1-8) | Reviewer card:108-120 objects that Task 9 states a conclusion before Task 3 fetches its quote. As a plan-compliance objection it is not retained: regenerated plan:63,176 follows the revised source:80, which already prescribes that historical planning conclusion and the quote/user-confirmation step. | Final report:89-90 explicitly records withdrawal by both advocates. This verifies the historical withdrawal, not the truth of an external GitHub documentation conclusion; that conclusion was not independently certified here. Not added to the 16 retained merged findings. |\n| Additional README leftover (R1-9) | Reviewer card:122-132 proposes adding base README line 30, about retired modes having no workflow equivalent. Revised source:81 expressly fixes the one-paragraph scope and the requested leftover disclosure; the final adjudication rejects this as an additional plan defect. Whether expanding that disclosure would be useful is separate from historical compliance. | Final report:89-90 explicitly records withdrawal because the plan follows revised source:81. Preserve as rejected-finding counterevidence, not another confirmed omission or a seventeenth finding. |\n\n**Key Takeaways**\n\n- The four retained entries now have individual historical classifications; their possible failure modes are not observed implementation failures.\n- The two withdrawn claims remain counterevidence and do not change the 16-item merged inventory.\n",
    "finding_ids": ["P2-F10", "P2-F11"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/05-session-e002bed2.md",
    "mode": "regex",
    "needle": "(?m)^\\*\\*Key takeaway:\\*\\* ([^\\n]+)$",
    "repl": "**Key Takeaways**\\n\\n- \\g<1>",
    "finding_ids": ["P2-F07"],
    "expected_count": 5
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/05-session-e002bed2.md",
    "mode": "literal",
    "needle": "| Equal tags or an older pin produce a forward range of newer tags. | **Preexisting, missed.** | Original Raw 585, workflow line 475 already used an `awk` walk that consumed the lower bound before checking the upper bound. Raw 804 explicitly states, “Before the fix the output was equally wrong, but no check noticed.” |",
    "repl": "| Older-pin and equal-tag ranges produce newer tags. | **Both preexisting, but with different discovery histories:** older-pin behavior was observed at Raw 697 as nonblocking, remained unrepaired, then was treated as a defect at Raw 804; the equal-tag counterexample was newly demonstrated at Raw 804. | Original Raw 585 contains the range walk. Raw 697, under “Observations (judged, not blocking by the Task 12 text)”, already describes older-pin output. Raw 804 demonstrates equal bounds and repeats older-pin behavior. Its statement “Before the fix the output was equally wrong, but no check noticed” is too broad for older pins: the first reviewer had noticed and judged that path nonblocking. Neither component was introduced by the repair. |",
    "finding_ids": ["P2-F12"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/05-session-e002bed2.md",
    "mode": "literal",
    "needle": "## 7. Final state and evidence limits",
    "repl": "**Key Takeaways**\n\n- Neighboring Tasks 10 and 11 converged after one repair; Task 10 still missed the later integration case.\n\n## 7. Final state and evidence limits",
    "finding_ids": ["P2-F07"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/05-session-e002bed2.md",
    "mode": "literal",
    "needle": "<!-- phase3-correction: monitor-boundary-and-accepted-completion -->",
    "repl": "**Key Takeaways**\n\n- The original prefix ends blocked; its overwritten structural log does not prove complete behavioral coverage.\n\n## Stale Documentation Found\n\nNo stale current-architecture documentation finding was established by this investigation. The changing protocol and overwritten historical structural log are evidence-version limits, not proof that a documented component no longer exists. Historical source claims remain bounded to the cited workflow versions and observations.\n\n**Key Takeaways**\n\n- Historical evidence changes must not be relabeled as a newly verified documentation defect.\n\n<!-- phase3-correction: monitor-boundary-and-accepted-completion -->",
    "finding_ids": ["P2-F06", "P2-F07"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/05-session-e002bed2.md",
    "mode": "literal",
    "needle": "## 2. Source fingerprints at this supplemental observation",
    "repl": "**Key Takeaways**\n\n- Membership selection freezes the population, not session bytes; the original prefix remains rows 1-1247.\n\n## 2. Source fingerprints at this supplemental observation",
    "finding_ids": ["P2-F07"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/05-session-e002bed2.md",
    "mode": "literal",
    "needle": "## 3. Historical ledger evidence versus current ledger",
    "repl": "**Key Takeaways**\n\n- Fingerprints describe the supplemental observation, not a snapshot taken at discovery.\n\n## 3. Historical ledger evidence versus current ledger",
    "finding_ids": ["P2-F07"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/05-session-e002bed2.md",
    "mode": "literal",
    "needle": "## 4. Later human acceptance closed Task 12",
    "repl": "**Key Takeaways**\n\n- Later ledger acceptance cannot be projected backward into the original halt.\n\n## 4. Later human acceptance closed Task 12",
    "finding_ids": ["P2-F07"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/05-session-e002bed2.md",
    "mode": "literal",
    "needle": "## 5. Fresh reviews in the continuation concern Task 13",
    "repl": "**Key Takeaways**\n\n- Task 12 completed through scoped acceptance with its misunderstood verdict unchanged, not an eighth review.\n\n## 5. Fresh reviews in the continuation concern Task 13",
    "finding_ids": ["P2-F07"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/05-session-e002bed2.md",
    "mode": "literal",
    "needle": "## 6. Effect on the original conclusions",
    "repl": "**Key Takeaways**\n\n- Task 13 reviews and its missing checkpoint are separate from Task 12's seven verdicts.\n\n## 6. Effect on the original conclusions",
    "finding_ids": ["P2-F07"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/05-session-e002bed2.md",
    "mode": "literal",
    "needle": "## 8. Summary and recommended action",
    "repl": "**Key Takeaways**\n\n- Later acceptance changes task status, not the established error-trap introduction history or unknown reviewer-miss explanations.\n\n## 8. Summary and recommended action",
    "finding_ids": ["P2-F07"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/05-session-e002bed2.md",
    "mode": "literal",
    "needle": "No earlier case line anchors or historical classifications changed.",
    "repl": "Original physical JSONL anchors remain unchanged; the older-pin discovery classification is corrected separately, and formatting corrections can move research-file lines.",
    "finding_ids": ["P2-F07", "P2-F12"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/05-session-e002bed2.md",
    "mode": "regex",
    "needle": "\\Z",
    "repl": "\n**Key Takeaways**\n\n- Event UUIDs identify messages; the reviewer identities below identify the five reviewing agents.\n\n## Reviewer identity and verdict mapping\n\nAll physical records are in Session S, the original monitor JSONL path defined in Evidence notation. Launch calls and their successful identity-bearing results are separate records. Continuation calls at Raw 797 and 842 both address the first reviewer.\n\n| Reviewer identity | Launch / dispatch-result record | Verdict records and literal results |\n|---|---|---|\n| `abeae1e32b8eb193b` | 685 / 686 | 697 missing; 804 missing; 849 compliant |\n| `a88a1879f45ea420a` | 893 / 894 | 906 missing |\n| `a07df47ab3fd3e05e` | 1009 / 1010 | 1021 missing |\n| `aef3fc4923722198a` | 1131 / 1132 | 1143 missing |\n| `a023d1421085d4e1e` | 1228 / 1229 | 1240 misunderstood |\n\n**Key Takeaways**\n\n- Five reviewer identities produced seven Task 12 verdicts: the reused reviewer produced three, and four fresh reviewers produced one each.\n- Message UUIDs, verdicts and reviewer identities remain different denominators; later acceptance adds no eighth verdict.\n",
    "finding_ids": ["P2-F14"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/06-session-0690ee9f.md",
    "mode": "regex",
    "needle": "(?m)^(The\\ plan\\ and\\ source\\ hashes\\ match\\ their\\ historical[^\\n]*|\\*\\*Root\\ cause:\\*\\*\\ verified\\ temporary\\ proof[^\\n]*|The\\ third\\ reviewer\\ prompt\\ says\\ two\\ earlier\\ attempts[^\\n]*|\\*\\*What\\ cannot\\ be\\ concluded:\\*\\*\\ which\\ actor\\ updated[^\\n]*|This\\ historical\\ content\\ was\\ checked\\ using\\ preserved\\ tree[^\\n]*|Why\\ the\\ first\\ final\\ reviewer\\ missed\\ the\\ already\\ incorrect\\ Task10[^\\n]*)$",
    "repl": "**Key Takeaways**\\n\\n- \\g<1>",
    "finding_ids": ["P2-F07"],
    "expected_count": 6
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/06-session-0690ee9f.md",
    "mode": "literal",
    "needle": "## 8. Supporting reviewer source hashes",
    "repl": "**Key Takeaways**\n\n- Historical follow-up positions are not a current defect inventory; accepted gaps and the missing second FINAL record remain explicit.\n\n## 8. Supporting reviewer source hashes",
    "finding_ids": ["P2-F07"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/06-session-0690ee9f.md",
    "mode": "literal",
    "needle": "<!-- phase3-correction: credential-earlier-miss-uncertainty -->",
    "repl": "**Key Takeaways**\n\n- These fingerprints identify historical nested reviewer transcripts, not current delivery-file contents.\n\n<!-- phase3-correction: credential-earlier-miss-uncertainty -->",
    "finding_ids": ["P2-F07"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/06-session-0690ee9f.md",
    "mode": "literal",
    "needle": "no historical ledger or earlier report line anchor changed.",
    "repl": "the historical ledger and original physical JSONL anchors remain unchanged; formatting corrections can move research-file lines.",
    "finding_ids": ["P2-F07"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/06-session-0690ee9f.md",
    "mode": "regex",
    "needle": "\\Z",
    "repl": "\n**Key Takeaways**\n\n- Original nested evidence preserves the failed FINAL absent from the historical ledger; that ledger remains unmodified.\n\n## Complete third-final eight-observation disposition\n\n**Primary source:** `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-a4bfff371c63a6c39.jsonl`, physical record 155, `2026-10-22T20:37:13.395Z`, message UUID `4209789d-084b-4425-9b19-753e01c8bfa1`. It returns `FINAL: pass` and eight observations labelled MINOR. Source positions below are historical delivery-file positions, not this research file's line numbers.\n\nThe same nested transcript preserves the loaded plan at record 19, ledger at 21, acceptance artifact at 84, manpage evidence at 42 and 87, load-order line at 99, and sweep classification at 121. The two loaded rubric versions remain in `historical-review-rules.json` and this case's Review-policy section. No historical package or ruling ledger was changed for this accounting.\n\n| Observation | Historical meaning and criterion assessment | Causal class and limits |\n|---|---|---|\n| 1. Orphan provider comment | `providers.tf:37` leaves the short fragment “sit on top of the”. The reviewer calls it cosmetic; no separately violated functional criterion is demonstrated. | Cosmetic authoring observation. Exact introducing edit is unknown here; unchanged delivery-state digests exclude the evidence-only FINAL repairs as its cause. Not another failed review or verified runtime defect. |\n| 2. Long README line | `README.md:37` is long after rewrapping. The reviewer expressly says MD013 is disabled and no lint finding results. | Cosmetic observation, not an established literal lint failure. Exact introducing edit and any earlier-miss reason are unknown; not caused by evidence-only corrections. |\n| 3. Refresh comment outside Task 15 spans | `refresh-env:470` lies outside Task 15's named local spans, but the later Task 17 sweep authorizes fixing stale hits in allowed files. Plan record 19, Task 17 body at historical line 190, establishes that broader authority. | Authorized by another task, not extra delivery scope. The third reviewer explicitly accepts it. No final-loop regression is demonstrated. |\n| 4. Loose overwrite wording | Historical `aienv.7:183` says “from this file or any other file”. Source record 27 requires overwriting values set elsewhere; delivered wording appears in original tool results 42 and 87. The reviewer assesses it accurate but loose. | Equivalent historical wording, not an established unmet requirement. No separate behavior claim is revalidated here. Exact wording-introduction time and earlier-miss reason are unknown; no evidence-only repair introduced it. |\n| 5. Missing load-order fan-out clause | Task 2's body at historical plan line 46 explicitly asks the load-order entry to connect all five key names to the gateway key. Tool result 99 shows line 236 says only optional/sourced-last/wins; fan-out is present elsewhere at 171-183. | Valid narrow preexisting task-body omission, not one of the failed FINAL causes and not introduced by evidence repairs. The historical pass is therefore not proof of universal literal instruction completion. Why the final reviewer did not block on this body-level omission is unknown beyond their note that no AC tests it. |\n| 6. Optional file expressed equivalently | `SECURITY.md:434-435` uses “only when created with --file” rather than the literal word “optional” requested by Task 7's AC. The third reviewer expressly judges the meaning equivalent; plan record 19, historical lines 100-103, supplies the requirement. | Accepted equivalent wording, with a literal-token qualification, not a newly proven security defect. Exact introduction and earlier-miss cause are unknown. |\n| 7. Acceptance artifact, no ruling ledger line | The Task 6 lint acceptance exists in `t6-owner-acceptance.md` (original result 84), while original ledger result 21 retains `T6: complete verdict=compliant` and contains no `T6: Ruling:`. The newer loaded rubric permits executor recording of scoped human acceptance but still requires a durable ruling and unchanged noncompliant completion. | Real acceptance-record/protocol mismatch, not missing human consent and not a delivery-code regression. It arose in the post-first-FINAL acceptance sequence, not from later delivery edits. The third reviewer explicitly did not re-litigate it; do not claim their pass proves the ruling schema was satisfied. No historical ledger repair is authorized here. |\n| 8. Retained restart remark | `aidev02-operator.md:528` says old `GH_TOKEN`/`~/.env` needs a restart. Original sweep result 121 labels that exact retained rotation remark ACCURATE; the third reviewer agrees. Task 17 required classifying accurate versus stale hits, not removing every mention. | Retained accurate historical text, not a new stale-documentation or missing-requirement defect. No runtime restart experiment was performed here; the classification is the recorded historical one. No final-loop repair introduced it. |\n\n**Key Takeaways**\n\n- All eight observations are retained with their historical meanings; they are not eight verified delivery defects.\n- The acceptance-record mismatch and narrow task-body omission qualify the observed pass without fabricating another failed FINAL or modifying its historical ledger.\n",
    "finding_ids": ["P2-F13"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-rules.md",
    "mode": "literal",
    "needle": "## Workflow Review Rules",
    "repl": "**Key Takeaways**\n\n- The seven source/installed comparisons describe their observation, not historical execution.\n\n## Workflow Review Rules",
    "finding_ids": ["P2-F01"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-rules.md",
    "mode": "literal",
    "needle": "## Implementation Review and Retry Rules",
    "repl": "**Key Takeaways**\n\n- Generation checks and advisory semantic readiness are separate; later user-authorized plan edits are separate actions.\n\n## Implementation Review and Retry Rules",
    "finding_ids": ["P2-F01"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-rules.md",
    "mode": "literal",
    "needle": "## Historical Versus Current Rules",
    "repl": "**Key Takeaways**\n\n- Per-task QA, retry and managed FINAL have distinct evidence and stopping rules; current source is not historical execution proof.\n\n## Historical Versus Current Rules",
    "finding_ids": ["P2-F01"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-rules.md",
    "mode": "literal",
    "needle": "## Key Takeaways",
    "repl": "**Key Takeaways**\n\n- Current attempt limits do not prove the exact historical rules loaded by a reviewer.\n\n## Recovered historical loaded-rule mapping\n\nThese are observed loads of `/config/.claude/skills/sc-implement-protocol/refs/qa.md`, not versions inferred from the current installed file. Full decoded texts are retained once in `historical-review-rules.json`, records.before and records.after. Removing the Read tool's displayed line-number prefixes from each original result recovers the captured text; hashes below are SHA-256 of that decoded content, not raw JSONL bytes.\n\n| Loaded version and review | Original physical source and load timestamp, UTC | Captured-content SHA-256 | Material historical rule |\n|---|---|---|---|\n| Earlier rubric; credential follow-up second FINAL, result record 116 | `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-acf0a51e6992c50ee.jsonl:18`; `2026-10-22T20:26:30.085Z` | `0b533765d43a7adc90987581892a0bca849cc19a53638b556b6aba62d425d083` | Captured rubric:65 prohibits executor-written rulings and requires an operator-supplied record; :79 makes missing, stale or unverifiable evidence issues. |\n| Later rubric; credential follow-up third FINAL, result record 155 | `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-a4bfff371c63a6c39.jsonl:18`; `2026-10-22T20:32:19.277Z` | `faff03b7b94ca2b70f9b25c35dcefd52636b7df8f7bf9a110c0a956a78d2e7d5` | Captured rubric:66-68 permits executor recording of actual scoped user acceptance, retaining the noncompliant verdict; :82 requires current-file/artifact-log evidence and explicitly rejects moved line numbers alone as issues. |\n\nCase link: `06-session-0690ee9f.md`, Review-policy changed before the final pass and Complete third-final eight-observation disposition. The passing third review follows both evidence corrections and a changed rubric; the updater and each change's independent causal effect remain unknown. Do not assign either recovered version to other historical reviews without their own load evidence. The monitor's separately observed migration is traced in `05-session-e002bed2.md`, A mid-run protocol migration reopened a successful check, using original Raw 42/58 and 874/884/893/902; this mapping does not invent missing hashes or a universal version timeline.\n\n**Key Takeaways**\n\n- Two exact historical rubric loads are available; unobserved versions and update authorship remain unknown.\n\n## Key Takeaways",
    "finding_ids": ["P2-F09"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-rules.md",
    "mode": "literal",
    "needle": "Historical version provenance, actual protocol compliance and finding validity belong to per-session analysts.",
    "repl": "Two recovered historical QA loads are mapped above and linked to the credential case. Historical versions without load evidence, actual protocol compliance and finding validity remain case-specific.",
    "finding_ids": ["P2-F09"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-rules.md",
    "mode": "literal",
    "needle": "**Status:** Complete (current protocol map; historical execution remains case-specific)",
    "repl": "**Status:** Complete (current protocol map and recovered historical loads; execution remains case-specific)",
    "finding_ids": ["P2-F09"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/evidence-deck.md",
    "mode": "literal",
    "needle": "| Equal/older tag range wrong | Preexisting missed range traversal | Original monitor 585, later 804; repair 825 | Reviewer explicitly says original output was equally wrong. Strong. |",
    "repl": "| Older-pin and equal-tag range wrong | Both preexisting, with different discovery histories: older pins observed as nonblocking at 697, unrepaired, then treated as a defect at 804; equal tags newly demonstrated at 804 | Original monitor 585; first review 697; second 804; repair 825 | The broad later “no check noticed” statement is contradicted for older pins by the first review. Neither component is repair-introduced. Strong. |",
    "finding_ids": ["P2-F12"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/evidence-deck.md",
    "mode": "literal",
    "needle": "### Credential finals: evidence errors versus delivery defects",
    "repl": "The five reviewing-agent identities and all seven verdicts are mapped in `05-session-e002bed2.md`, Reviewer identity and verdict mapping. The original reviewer `abeae1e32b8eb193b` produced records 697/804/849; `a88a1879f45ea420a`, `a07df47ab3fd3e05e`, `aef3fc4923722198a` and `a023d1421085d4e1e` produced records 906, 1021, 1143 and 1240 respectively. Identity-bearing dispatch results are original records 686, 894, 1010, 1132 and 1229, not event UUIDs.\n\n### Credential finals: evidence errors versus delivery defects",
    "finding_ids": ["P2-F14"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/evidence-deck.md",
    "mode": "literal",
    "needle": "| Narrow manpage task-body omission remains | Preexisting instruction omission, not failed-round cause | Historical tree checked by case analyst | Fan-out described elsewhere; observed PASS is not universal literal compliance. Strong narrowed finding. |",
    "repl": "| Narrow manpage task-body omission remains | Preexisting instruction omission, not failed-round cause | Historical tree checked by case analyst | Fan-out described elsewhere; observed PASS is not universal literal compliance. Strong narrowed finding. |\n\nThe complete eight-observation accounting is in `06-session-0690ee9f.md`, Complete third-final eight-observation disposition, sourced to nested third-FINAL record 155 and its preserved reads. It also retains observation 4 (accurate but loose overwrite wording), observation 7 (human acceptance exists in an artifact but no required ruling ledger line), and observation 8 (retained restart remark classified accurate by the historical sweep). These are not automatically three additional delivery defects.",
    "finding_ids": ["P2-F13"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/evidence-deck.md",
    "mode": "literal",
    "needle": "The original 18 concerns also received substantial plan-text repairs:",
    "repl": "The four retained low findings about serialization, failure-message rendering, status flags and leftover reference frames have individual before/after and historical-validity dispositions in `04-session-43582de1.md`, Additional retained and withdrawn finding dispositions. That section also accounts for the two withdrawn reviewer claims about the path-filter conclusion and README line 30; both follow the revised source and do not increase the 16 retained merged findings. The external documentation premise is not independently certified here.\n\nThe original 18 concerns also received substantial plan-text repairs:",
    "finding_ids": ["P2-F10", "P2-F11"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/evidence-deck.md",
    "mode": "literal",
    "needle": "| `scope-rules.md` | Current protocol map with historical-version limits. |",
    "repl": "| `scope-rules.md` | Current protocol map, two recovered historical QA loads with hashes and case links, and explicit historical-version limits. |",
    "finding_ids": ["P2-F09"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-04.md",
    "mode": "literal",
    "needle": "Additional screening anchors from the assigned agent, pending direct main-session Read:",
    "repl": "Additional screening anchors from the assigned agent (records 544-545 independently rechecked for operation identity and success; other entries remain navigation leads):",
    "finding_ids": ["P2-F08"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/evidence-deck.md",
    "mode": "literal",
    "needle": "Error-handling repairs leave PR-list substitution failure; preexisting range defect discovered.",
    "repl": "Error-handling repairs leave PR-list substitution failure; the preexisting equal-tag case is newly demonstrated, while older-pin behavior was already observed as nonblocking and is now treated as a defect.",
    "finding_ids": ["P2-F12"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/evidence-deck.md",
    "mode": "literal",
    "needle": "Monitor range, output and summary boundaries; CI search assertions; credential blank pointer",
    "repl": "Monitor equal-tag/absent-upper-tag paths, output and summary boundaries; CI search assertions; credential blank pointer",
    "finding_ids": ["P2-F12"],
    "expected_count": 1
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/evidence-deck.md",
    "mode": "literal",
    "needle": "The appended case supplements retain physical records, timestamps and original message UUIDs without shifting earlier citations.",
    "repl": "The appended case supplements retain original physical JSONL records, timestamps and message UUIDs. Phase 2 formatting corrections can shift research-file lines; the stable supplement headings and original source-record frames remain the citation join.",
    "finding_ids": ["P2-F01", "P2-F04", "P2-F07"],
    "expected_count": 1
  }
]
```

## Recommendations

The parent should persist this fix log at the intended path and apply the 62 patches serially using dedicated editing tools, enforcing every expected count. Then the separately required independent verification must examine all 14 groups and their enumerated subchecks.

The synthesis citation refresh is a recorded downstream follow-up, not permission for this correction context to edit synthesis files.

## QA Complete

| Status | Result |
|---|---|
| DONE | Independently checked the sources and prepared 62 count-validated surgical patches covering all 14 findings. |
| DONE | Preserved original records, captures, historical packages, review artifacts, task state and hypothesis cards. No research targets or reports were written. |
| NEXT | Parent persists `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-phase-2-fix-log.md`, applies the patches and obtains independent verification. |

**Final status: proposals complete and unapplied. Open findings on disk: 14. Gate verdict remains FAIL.**
