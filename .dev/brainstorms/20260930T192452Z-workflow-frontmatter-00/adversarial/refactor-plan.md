# Refactoring Plan

## Overview
- Base variant: V1 `variant-1-opus-architect.md` (opus:architect)
- Incorporated from: V2 `variant-2-sonnet-refactorer.md` (sonnet:refactorer)
- Planned changes: 8 (7 debate-derived + 1 orchestrator-flagged open issue)
- Overall risk: Low (text-level edits to a spec; no structural reorganisation)
- Output: `adversarial/merged-output.md`

## Planned Changes

### Change 1 — `version` is a constant `"1"` (C-001, X-001; 95%)
- Source: V2:16, V2:88, V2:164, V2:216
- Target: V1 Decision 2 (V1:15-16); Wave 2 fill text inside edit 2 `## Fill rules` block (V1:92); `## Fill rules` table row `version` (V1:186); Risk 4 (V1:213); Out of scope (V1:216-224)
- Approach: replace. Decision 2 → "`version` = `"1"` (same-slug runs overwrite in place, no resume — `input-parse.md:13`)". V1:92 → "`version`: `"1"`." Table row → source "constant", default `"1"`. Delete Risk 4 and renumber. Add to Out of scope: "a `version` counter across runs". Keep the gate regex `^[1-9]\d*$` (C-002).
- Risk: Low

### Change 2 — plugin mirror byte-equality in the guard test (C-006; 95%)
- Source: V2:135-142
- Target: V1 edit 4 test (V1:152-165); V1 edit 3 (V1:146-148); Risk 5 (V1:214)
- Approach: append to the V1 test body:
  ```python
      plugin = _REPO / "plugins" / "superclaude" / "skills" / "sc-workflow-protocol"
      for rel in ("SKILL.md", "refs/quality-gates.md"):
          assert (plugin / rel).read_bytes() == (_SKILL / rel).read_bytes(), rel
  ```
  Edit 3: replace the manual-only `diff -r` framing with "copy byte-for-byte; the guard test asserts equality (no make target syncs `plugins/superclaude/`, `Makefile:109,166`)". Risk 5 mitigation → cite the assert.
- Risk: Low

### Change 3 — Checkpoint → the phase's last Task's acceptance criteria (C-003 refinement; 90%)
- Source: V2:43
- Target: V1 edit 1 Wave 2 bullet (V1:48)
- Approach: replace "Phase Outputs and Checkpoint → that phase's task `Acceptance criteria:` bullets (never a separate verify task)" with "Phase Outputs → the task bodies that produce them; Phase Checkpoint → the `Acceptance criteria:` of that phase's last Task (never a separate verify task)". Keep V1's Inputs mapping (Inputs → named files and source sections in the task body).
- Risk: Low

### Change 4 — priority never inferred (U-004)
- Source: V2:88, V2:168
- Target: V1 edit 2 `## Fill rules` `priority` bullet (V1:93); `## Fill rules` table (V1:187)
- Approach: append "Never inferred from tone or urgency (template 00: DO NOT invent, `00:14`)."
- Risk: Low

### Change 5 — placeholder check without the bare `[`-line clause (C-004; 85%)
- Source: V2 advocate critique (debate-transcript.md, V2 weaknesses #4)
- Target: V1 edit 2 schema-min bullet 2 (V1:112)
- Approach: replace "or `[`-bracketed placeholder line" with "or any `[...]` placeholder text copied verbatim from template 00" (literal-match only; markdown links and reference definitions are not flagged).
- Risk: Low

### Change 6 — numbered/checkbox ban covers fenced code (A-001; 95%)
- Source: both advocates REJECT the fence exemption (`sc-implement-protocol/SKILL.md:63-64` has no fence exemption)
- Target: V1 edit 2 schema-min bullet 4 (V1:114); `## Gate changes` (V1:193); `## /sc:implement compatibility` (V1:205)
- Approach: append "including inside fenced code blocks (`/sc:implement` has no fence exemption, `sc-implement-protocol/SKILL.md:63-64`)".
- Risk: Low

### Change 7 — `created_date` source (A-002; 95%)
- Source: both advocates QUALIFY
- Target: V1 Decision 2 (V1:15); edit 2 `## Fill rules` `created_date` bullet (V1:91); `## Fill rules` table (V1:185); `## Files unchanged` `refs/input-parse.md` bullet (V1:174)
- Approach: "`created_date`: today's UTC date from the session's date context — not via Bash (`refs/input-parse.md:30`: 'Bash: mkdir of output dir only', unchanged). Never invent a date; a missing or malformed date fails the Wave 3 date check → `E-GATE`."
- Risk: Low

### Change 8 — open issue flagged by orchestrator (NOT debated)
- Source: orchestrator observation after Round 1 (Round 2.5 invariant probe was skipped at `--depth quick`; this is the kind of interaction effect it would probe)
- Target: new section `## Open issues (not debated)` before `## Out of scope`; qualify the `refs/phase-templates.md` bullet in `## Files unchanged` (V1:175)
- Approach: add: "`refs/phase-templates.md:7-9` skeletons include `Parse`, `Validate` and `Document` phases. Rendered 1:1 as Tasks under the new Wave 2 they become read-only / verify-only tasks that template 00 now forbids (`00:16-17`) and that `/sc:implement` scores `cannot-verify` on an empty diff (`refs/qa.md:44`). Decide during review: fold them into build tasks (e.g. Parse → inputs of the first task; Validate → last task's acceptance criteria), or edit the skeleton table." In `## Files unchanged`, mark the phase-templates bullet "pending open issue 1".
- Risk: Medium (may add a 4th file edit)

## Changes NOT Being Made
| Diff point | Non-base approach | Rationale |
|------------|-------------------|-----------|
| S-001 | One `Fill:` sentence (V2:88) | Tie; V1's `## Fill rules` section kept for findability |
| C-002 | `version` "non-empty" (V2:94) | V2 conceded it accepts non-integers; V1 regex kept |
| C-003 (Inputs part) | Inputs → `Depends on: Task K` (V2:43) | V2 conceded category error; conflicts with `00:15` |
| C-005 | AC-per-Task only at full (V2:112) | V2 conceded; quick plans also reach `/sc:implement` |
| C-007 | Unquoted `created_date` (V2:85) | V2 conceded; template `00:4` quotes it |
| C-008 | ≥1 Phase required at schema-min (V2:95) | V2 conceded; contradicts `00:10` |

## Risk Summary
| Change | Risk | Impact | Rollback |
|--------|------|--------|----------|
| 1-7 | Low | wording/rules inside the spec | revert the section text |
| 8 | Medium | may expand scope to `refs/phase-templates.md` | leave as open issue for downstream review |

## Review Status
- Approval: auto-approved (non-interactive)
- Timestamp: 2026-09-30T19:41:00Z
