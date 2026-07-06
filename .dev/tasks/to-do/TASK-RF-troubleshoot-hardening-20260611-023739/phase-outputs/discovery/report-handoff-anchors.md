# report-template.md + remediation-handoff.md Anchor Inventory (Step 1.4)

Date: 2026-06-11

Source files (absolute paths):
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening/src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening/src/superclaude/skills/sc-troubleshoot-protocol/refs/remediation-handoff.md`

---

## A. report-template.md anchors

### A.0 — FENCE BACKTICK COUNT: CONFIRMED 4-BACKTICK

The template block IS opened with a FOUR-backtick outer fence (NOT 3-backtick), as required.

- **Open fence** — line 7, verbatim:
  ````
  ````markdown
  ````
  (four backticks + `markdown`)
- **Close fence** — line 203, verbatim: ```` ```` ```` (four backticks, bare)
- Reason confirmed in-body: the template wraps inner three-backtick ```` ```text ```` code blocks (the hard-stop block at lines 160-192 and the Audit block uses ```` ``` ````), so a 4-backtick outer fence is required to nest them. This matches the item's stated expectation.

### A.1 — Heading that opens the fenced template block

- **`## Template`** (line 5). The four-backtick `````markdown` fence opens immediately on line 7, directly under this heading.

### A.2 — Header verdict/status fields inside the template (lines 8-22)

Verbatim field lines (these are the header fields the new hardening fields would attach beside):

- `**Status**: <success|partial>` (line 14) — the gating field FR-12 reconciliation keys off.
- `**Target**: <one-line: the symptom or scope as given>` (line 10)
- `**Type**: <bug|performance|security|build|deployment|test|auto>` (line 11)
- `**Tier reached**: <1|2|3>` (line 12)
- `**Confidence**: <0.0–1.0>` (line 13)
- `**Escalation reason**: <none|low_confidence|multi_domain|forced_by_depth_deep|intermittent|not_reproducible|security_caution>` (line 15)
- `**Test is wrong**: <true|false>` (line 16)
- `**Test file to update**:` (line 17)
- `**Behavior is documented**: <true|false|n/a>` (line 18)
- `**Doc context card**:` (line 19)
- `**Diagnosability audit**: SKIPPED ...` (line 20)
- `**Duration**: <seconds>` (line 21)
- `**Date**: <ISO 8601>` (line 22)

### A.3 — Existing post-template `## ` rule sections (all present, verbatim heading text)

These three sit AFTER the closing four-backtick fence (line 203):

- **`## Rendering rules`** (line 205)
- **`## Test-is-wrong rule`** (line 212)
- **`## Behavior-is-documented rule`** (line 233)

(Also present after the fence, for orientation: the in-template body sections inside the fence include `## Summary`, `## Documentation Context`, `## Diagnosability Context`, `## Diagnosis`, `## Evidence`, `## Proposed Fix`, `## Alternative Fixes Considered`, `## Risk + Rollback`, `## Follow-up tasks`, `## Grounding Gaps`, `## Next Steps`, `## Audit` — but those are template body, NOT post-template rule sections.)

### A.4 — Attachment note: where the new `Pipeline Hardening Closure` section + new header fields should go

- **New header fields** (the `success_with_hardening_*` reconciliation fields for FR-12) should attach inside the template header block, adjacent to `**Status**: <success|partial>` (line 14) — most naturally immediately after the `Status` line so the hardening verdict is read together with the success/partial verdict. They go INSIDE the four-backtick fence (lines 8-22 region).
- **New `## Pipeline Hardening Closure` section**: as a template-body section it belongs INSIDE the four-backtick fence, e.g. after `## Risk + Rollback` (line 112) / `## Follow-up tasks` (line 122) and before `## Audit` (line 196). If instead it is authored as a post-template RULE section (like the three rule sections), it attaches AFTER line 203's closing fence, alongside `## Rendering rules` / `## Test-is-wrong rule` / `## Behavior-is-documented rule`. Authoring guidance: a rendered report SECTION goes inside the fence; a RULE describing when/how to render it goes after the fence.

---

## B. remediation-handoff.md anchors

### B.1 — Line-3 gating note (the REAL precondition) — VERBATIM

- **Line 1 heading**: `# Tier 3 Remediation Handoff (Wave 6)`
- **Line 3, quoted verbatim:**

  > Loaded only when `--fix` is set and Wave 5 produced a `success` (not `partial`) report. Drives the offer + task-builder chain.

  This confirms the precondition is **`success` AND `--fix` set** (both required), NOT `success` alone. FR-12 `success_with_hardening_*` reconciliation must be authored against this exact gate text: the handoff only loads when `--fix` is set AND the report Status is `success`.

### B.2 — The user-offer block

- **Heading**: `## The user offer` (line 5).
- The offer is surfaced verbatim from the fenced block at lines 9-28 (three-backtick bare fence). It opens with:

  > Tier 3 remediation chain is available for this fix.

  and ends with:

  > Proceed with task-builder?  [yes / no]

  Bracketed substitution fields inside the block: `<one-paragraph summary from REPORT.md "Proposed Fix" section>` (line 20), `<bullet list of files from REPORT.md>` (line 23), `Expected task complexity: <generic | complex>` (line 25).

### B.3 — The `BUILD_REQUEST` block

- **Heading**: `## Phase A — Build the task file` (line 38).
- The `BUILD_REQUEST` block is the fenced block at lines 42-56. Verbatim block label / first lines:

  > BUILD_REQUEST:
  >   TEMPLATE: <generic | complex>
  >   GOAL: Apply the fix described in <abs-path-to-REPORT.md>
  >   WHY: <copy the REPORT.md "Summary" section verbatim>
  >   WHERE: <list of files from REPORT.md "Proposed Fix" section>
  >   ACCEPTANCE_CRITERIA:
  >     - <test to verify from REPORT.md, restated as a checkbox criterion>
  >     - The change is limited to the files listed in WHERE
  >     - No new lint or type errors introduced
  >   REFERENCES:
  >     - REPORT.md: <abs-path>
  >     - Audit log: <abs-path>
  >     - Hypothesis card (chosen): <abs-path>

### B.4 — Other structural anchors (orientation)

- `## Decision matrix` (line 30)
- `## Phase B — Pre-execution review` (line 68)
- `## Phase C — Execution gate (always user-initiated)` (line 78)
- `## Phase D — Post-execution validation (optional, user-triggered)` (line 94)
- `## Why this is the only safe handoff` (line 108)
- `## Failure modes` (line 116)

### B.5 — Attachment note: where the new handoff hardening fields should attach

- The new handoff **hardening fields** should attach to the gate on **line 3** (the precondition sentence) and/or the `BUILD_REQUEST` block (lines 42-56). For FR-12 `success_with_hardening_*` reconciliation, the natural attachment is:
  - Augment the **line-3 precondition** so the gate distinguishes plain `success` from `success_with_hardening_*` (i.e. specify which success variants load the handoff). Quote and extend the verbatim line, do not replace its `--fix` AND `success` semantics.
  - Add a hardening-status reference to the **`REFERENCES:`** list in the `BUILD_REQUEST` block (line 52-55 region) so the built task carries the Pipeline Hardening Closure context forward (parallels how `REPORT.md` / `Audit log` / `Hypothesis card` are referenced).
- No existing field in this file is literally named `success_with_hardening_*`; the closest actual gate text is the line-3 sentence quoted in B.1. FR-12 must reconcile against that sentence + the report-template `**Status**: <success|partial>` field (A.2).
