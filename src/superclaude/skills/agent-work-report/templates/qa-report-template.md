# QA report: {{run}}

**Overview checked:** {{overview}}
**Overview sha256:** {{overview_sha256}} (taken before reading; `run.py gate` accepts this review only for this exact text)
**Reviewer:** a fresh-context reviewer that did not write the overview
**Pass:** {{pass_number}} (reviews repeat after every fix until one passes; the report is never delivered before)

## Verdict

<!-- Start with **PASS.** or **FAIL.** exactly: `run.py gate` reads it. -->
{{RF_PLACEHOLDER:verdict}}

## Script checks

{{script_checks}}

## Reviewer checks

| Check | Result | Evidence |
|---|---|---|
| Every "Needs you" entry states the question, every option with what it does, the key facts, a recommendation with why, what happens after each answer, and links | {{RF_PLACEHOLDER:needs_you_check}} | {{RF_PLACEHOLDER:needs_you_evidence}} |
| Every full entry has all seven parts and says what happened in substance, never "nothing new" | {{RF_PLACEHOLDER:entries_check}} | {{RF_PLACEHOLDER:entries_evidence}} |
| Every statement about an item matches the run folder files (activity.md, compare.json, classified.json) | {{RF_PLACEHOLDER:facts_check}} | {{RF_PLACEHOLDER:facts_evidence}} |
| Every "likely yours" judgment gives a reason drawn from the item's comments or linked work | {{RF_PLACEHOLDER:likely_check}} | {{RF_PLACEHOLDER:likely_evidence}} |
| Plain English: no internal codes, rule numbers or jargon as names | {{RF_PLACEHOLDER:plain_check}} | {{RF_PLACEHOLDER:plain_evidence}} |

## Problems to fix

{{RF_PLACEHOLDER:problems}}

## Self-audit

{{RF_PLACEHOLDER:self_audit}}
