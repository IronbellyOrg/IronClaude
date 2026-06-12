# SKILL.md Anchor Inventory (Step 1.3)

Date: 2026-06-11

Source file: `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`

This inventory records the EXACT heading text (verbatim wording, casing, punctuation,
em-dashes) of each anchor heading required by the hardening task, plus the Wave 5
report-composition context and a COMPLETE verbatim enumeration of every existing
Output Contract field (name + type + nullability) for NFR-6 backward-compat collision
avoidance. Anchors are recorded by HEADING TEXT, not line numbers (line numbers drift).

---

## (a) Anchor headings — verbatim

All five expected anchors exist. The Wave numbering and titles match the task's
expected names. Quote everything verbatim (note the EXACT em-dash character `—`
U+2014 used throughout).

| Expected anchor (from task) | ACTUAL heading text in file (verbatim) | Status |
|---|---|---|
| `## Output Contract` | `## Output Contract` | EXACT match |
| `## Wave Structure` | `## Wave Structure` | EXACT match |
| `### Wave 1.7: Tier 1 — Hypothesis Formation` | `### Wave 1.7: Tier 1 — Hypothesis Formation` | EXACT match (em-dash `—` U+2014) |
| `### Wave 2: Confidence Gate` | `### Wave 2: Confidence Gate` | EXACT match |
| `### Wave 5: Synthesis + Report` | `### Wave 5: Synthesis + Report` | EXACT match |

Verbatim heading strings (copy-paste safe):

- `## Output Contract`
- `## Wave Structure`
- `### Wave 1.7: Tier 1 — Hypothesis Formation`
- `### Wave 2: Confidence Gate`
- `### Wave 5: Synthesis + Report`

### Wording / casing / punctuation notes

- The em-dash in `Wave 1.7: Tier 1 — Hypothesis Formation` is a true em-dash
  (`—`, U+2014) with a single space on each side (`Tier 1 — Hypothesis`). The same
  em-dash style appears in the sibling wave headings (`### Wave 1: Tier 1 — Real-Code
  Grounding`, `### Wave 3: Tier 2 — Parallel Hypotheses`, `### Wave 4: Tier 2 —
  Adversarial Fix Debate`). Match this exactly when adding sibling-level content.
- Tiered waves use the pattern `### Wave <N>: <Tier label> — <Title>`; the gate /
  structure waves use `### Wave <N>: <Title>` with NO em-dash and NO "Tier" prefix
  (e.g. `### Wave 2: Confidence Gate`, `### Wave 5: Synthesis + Report`).
- `## Output Contract` and `## Wave Structure` are level-2 (`##`); all individual
  waves are level-3 (`###`).

### Trigger insertion point ("after Tier-1 diagnosis, before report closure")

The actual anchoring heading text for the insertion point is:

- **After Tier-1 diagnosis** = the wave that produces the Tier 1 hypothesis +
  calibration: heading `### Wave 1.7: Tier 1 — Hypothesis Formation`. Its exit
  emits `"Wave 1.7 complete: confidence=<x>"`. The Confidence Gate that consumes it
  is `### Wave 2: Confidence Gate`.
- **Before report closure** = the synthesis/report wave: heading
  `### Wave 5: Synthesis + Report`, specifically before its report-composition
  Step 2 bullet list (see section (b)) and before the audit-log footer Step 4.

So a "Pipeline Hardening Closure" trigger that fires *after Tier-1 diagnosis but
before report closure* is anchored between `### Wave 1.7: Tier 1 — Hypothesis
Formation` (and/or `### Wave 2: Confidence Gate`) and the Step 2 composition bullet
list inside `### Wave 5: Synthesis + Report`.

---

## (b) Wave 5 report-composition bullet list (target for "Pipeline Hardening Closure" bullet)

The report-composition bullet list lives under `### Wave 5: Synthesis + Report`,
inside the `**Steps**:` ordered list, at **Step 2** ("Compose `REPORT.md` filling
in:"). The new "Pipeline Hardening Closure" bullet must be added to THIS bullet list.

### Surrounding context (verbatim)

The `**Steps**:` ordered list begins:

> 1. Load `refs/report-template.md` (not before now — lazy load).
> 2. Compose `REPORT.md` filling in:

The Step 2 bullet list (verbatim, in order — these are the sub-bullets indented
under "2. Compose `REPORT.md` filling in:"):

- `Header (target, tier reached, confidence, escalation reason)`
- `Summary (2-4 sentence executive summary)`
- `Documentation Context (≤6-line summary of the Wave 1.5 Documentation Context Card at `<output-dir>/doc-context.md`; omit this section entirely and add a line to Grounding Gaps when `--no-doc-discovery` was set)`
- `Diagnosability Context (≤6-line summary of the Wave 1.6 Diagnosability Context Card at `<output-dir>/diagnosability-context.md`; omit this section entirely and add a line to Grounding Gaps when `--no-diagnosability-audit` was set; when Wave 1.6 hard-stopped, render the section as the hard-stop block from refs/report-template.md instead)`
- `Diagnosis (the chosen hypothesis — from Tier 1 alone, or from the adversarial merge)`
- `Evidence (cited `file:line` and command outputs)`
- `Proposed Fix (the recommended change; if a doc-update + fix bundle was produced in Wave 4, render BOTH the doc file(s) to update and the code change(s) in this section)`
- `Alternative Fixes Considered (Tier 2 only — the losing proposals from the debate, with one-line reason each)`
- `Risk + Rollback (what to watch after applying)`
- `Next Steps (Tier 1: rerun with `--depth deep` if needed; Tier 2 without `--fix`: re-invoke with `--fix` to authorize remediation; Tier 2 with `--fix`: confirm to proceed to Wave 6)`

### Where the new bullet goes

The bullet list above is the canonical report-section enumeration. A new
`Pipeline Hardening Closure` bullet should be appended to this Step 2 list (the
exact position — e.g. after `Next Steps`, or before `Risk + Rollback` — is an
implementation decision for the additive item; this discovery only records that
THIS is the list that must gain the bullet, and that it is the LAST sub-list
before the prose paragraph beginning **"Sprint-failure recovery hint."** and the
two `--no-doc-discovery` / `diagnosability_hard_stop` rendering-conditional
paragraphs that close out Step 2).

After the Step 2 bullet list, Step 2 continues with these prose blocks (verbatim
openers, recorded so the new bullet is not accidentally inserted past them):

- `**Sprint-failure recovery hint.** When the diagnosed target is a `superclaude sprint run` phase that failed on a *subset* of its tasks ...`
- `When `--no-doc-discovery` was set, omit the Documentation Context section entirely AND populate the Grounding Gaps section with: ...`
- `When `diagnosability_hard_stop=true`, replace the Diagnosis section with a "Halted — instrumentation required" prose block ...`

Then Step 3 (`**File:line validation pass (non-negotiable)**` — spawn
`evidence-validator`), Step 4 (audit-log footer), and Step 5 (surface to user in
chat) follow. The `### Wave 5: Synthesis + Report` **Exit criteria** are:
`REPORT.md` written, audit log finalized, user notified; if `--fix` is not set,
return the output contract and STOP.

---

## (c) Existing Output Contract fields — COMPLETE verbatim enumeration

Under heading `## Output Contract`, the contract is introduced by:

> The skill returns a structured dictionary on completion:

followed by a 3-column table (`| Field | Type | Description |`). Below is EVERY
existing field, verbatim field name (column 1) + verbatim type (column 2) +
nullability. **Total existing fields: 19.** NFR-6 backward-compat: any new
additive field MUST NOT reuse any name below.

Nullability legend: "non-null" = no `| null` union in the Type column; "nullable"
= Type column explicitly includes `\| null` (rendered in-table as `string | null`).

| # | Field name (verbatim) | Type (verbatim from Type column) | Nullability |
|---|---|---|---|
| 1 | `status` | `string` | non-null (enum-valued: `success`, `partial`, `failed`) |
| 2 | `tier_reached` | `int` | non-null (1, 2, or 3) |
| 3 | `report_path` | `string` | non-null |
| 4 | `audit_log_path` | `string` | non-null |
| 5 | `confidence` | `float` | non-null (0.0-1.0) |
| 6 | `escalation_reason` | `string` | non-null (string; may describe "If Tier 2 ran...") |
| 7 | `test_is_wrong` | `bool` | non-null |
| 8 | `test_file_path` | `string \| null` | nullable (`null` when `test_is_wrong=false`) |
| 9 | `behavior_is_documented` | `bool` | non-null |
| 10 | `doc_context_card_path` | `string \| null` | nullable (`null` ONLY when `--no-doc-discovery` set) |
| 11 | `hypothesis_cards` | `list[path]` | non-null (list; Tier 2) |
| 12 | `adversarial_artifacts_dir` | `string` | non-null (Tier 2 only, when 2+ fix proposals debated) |
| 13 | `task_file_path` | `string` | non-null (Tier 3 only) |
| 14 | `remediation_offered` | `bool` | non-null |
| 15 | `remediation_accepted` | `bool` | non-null (if offered) |
| 16 | `diagnosability_verdict` | `string` | non-null (enum: `sufficient`, `partial`, `insufficient`, `unknown`; default `unknown`) |
| 17 | `diagnosability_context_card_path` | `string \| null` | nullable (`null` only when `--no-diagnosability-audit` set or Wave 1.6 not reached) |
| 18 | `diagnosability_tasklist_path` | `string \| null` | nullable (`null` for sufficient/unknown/skipped) |
| 19 | `diagnosability_hard_stop` | `bool` | non-null |

### Notes for additive-field collision avoidance (NFR-6)

- The table type vocabulary in use: `string`, `int`, `float`, `bool`,
  `list[path]`, and the nullable-union form `string | null` (written `string \| null`
  with an escaped pipe inside the markdown table cell).
- FOUR fields use the `string \| null` nullable form (#8, #10, #17, #18):
  `test_file_path`, `doc_context_card_path`, `diagnosability_context_card_path`,
  `diagnosability_tasklist_path`.
- Beyond the table, the contract section also defines derivation-rule prose blocks
  for `test_is_wrong` and `behavior_is_documented` (NOT additional fields — they
  govern how fields #7 and #9 are set during Wave 5 synthesis). No field names other
  than the 19 above are introduced anywhere in the `## Output Contract` section.
- A new "Pipeline Hardening Closure" related field (if the additive item adds one)
  must use a name distinct from all 19 above.
