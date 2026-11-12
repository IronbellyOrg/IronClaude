---
needs_human_decision: true
status: RESOLVED
---

# Chat summary format

## Question

> "`pragmatic` DONE/NEXT rule has \"No exceptions\" and no exception mechanism (AMBIGUITY 6, F10)"

OQ-6/GQ-63. Source: research GAPS row 86 and `research/09-gap-fill.md` Gap 1. The current style rule at `src/superclaude/output-styles/pragmatic.md:22` says every response includes a DONE / NEXT table, with no exceptions. The report file is written by Python, so this decision affects only the sweep skill's chat reply, not the report file's layout.

## Options

> "(a) no exception: the skill's reply carries the DONE / NEXT table and points to the report path;"

> "(b) add an orchestrator exception, which means editing `pragmatic.md:22`."

Option (a) leaves the output-style source unchanged. Option (b) requires separate design/task revision because the style edit is outside this design. Neither option changes the Python-generated sweep report format.

## No recommendation

No source makes a recommendation. Option (a) is offered as the option that changes no existing file; it is not a recommendation and does NOT authorize adoption.

## Blocked work

Items 8.12 and 11.3 (step 1.5 report format and the sweep skill). Item 7.10 halts while this record is PENDING or Chosen is empty. Selecting option (b) requires the task-builder revision specified by item 7.10 before any output-style edit; this record alone does not authorize that edit.

## Operator decision

OPERATOR DECISION: Choose option (b), an orchestrator exception to the DONE / NEXT chat-table requirement.
Chosen: Add an exception for the sweep skill's coordinator chat reply. The Python-generated report format is unaffected. Exact exception wording and any broader scope require a separate design/task revision before editing the style.
Decided by: Ryan Wiancko, owner, 2026-11-09.
Decision source: In this session's chat-summary question, the owner selected "Add an exception". That option explicitly states that execution stops for a separate design/task revision before editing the output style. This resolves OQ-6/GQ-63 as option (b), not option (a), and does not authorize bypassing task item 7.10's revision stop.
