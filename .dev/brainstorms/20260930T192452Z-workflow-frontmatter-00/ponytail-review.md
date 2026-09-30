# Ponytail review of merged-requirements.md

Level: full. Input: `merged-requirements.md` (adversarial merge, convergence 1.00). Output: the edit set below replaces the merged spec's `## File edits`.

| Merged proposal | Verdict | Reason |
|---|---|---|
| Wave 2 renders template 00 | keep, 2 sentences | only path for the fields/rules to reach plan.md; template 00's own comment already says "remove this comment and unused placeholders" — do not restate its rules |
| `## Fill rules` section (3 bullets) | fold into yaml comments | three one-liners, no section needed |
| placeholder-literal list | one clause | `YYYY-MM-DD` / `version: ""` already fail the format checks |
| gate: no plan-wide Outputs/Success/Verification | cut | G50 ruled DO-NOT-ADD (debate/G50.md); template comment already says it; /sc:implement ignores stray sections |
| schema 1.0 → 1.1 | keep | one token; body contract changes |
| mirror assert on 2 named files | `filecmp.cmpfiles` over the whole skill dir | same size, stdlib, also catches refs/* drift |
| test asserts on template keys | cut | gate is the source of truth |
| open issue 1 (Parse/Validate phases) | fix root cause: 1 row in `refs/phase-templates.md` | default `systematic` skeleton would make the writer emit a read-only task and a verify-only task that template 00 forbids (`00:16-17`) and /sc:implement cannot verify (`refs/qa.md:44`); Wave 1 parses, each Task's AC validates |
| return-contract, command, input-parse, overlap-routing | unchanged | as merged spec |

## Final edit set

1. `src/superclaude/skills/sc-workflow-protocol/SKILL.md` — Wave 2 body → template 00 + phase→task mapping (2 sentences).
2. `src/superclaude/skills/sc-workflow-protocol/refs/quality-gates.md` — 8-key frontmatter (fill rules as yaml comments), 00 body shape, schema-min 4 bullets, full 4 bullets.
3. `src/superclaude/skills/sc-workflow-protocol/refs/phase-templates.md` — `systematic` skeleton: `Design boundaries → Build sequential layers → Document`.
4. `plugins/superclaude/skills/sc-workflow-protocol/{SKILL.md,refs/quality-gates.md,refs/phase-templates.md}` — byte copies.
5. `tests/commands/test_workflow_command.py` — `test_plan_uses_template_00` + `test_plugin_mirror_matches_src` (filecmp).

Skipped: fill-rules section, literal residue list, G50 gate, template-key test. Add back if a real plan slips through the gate.
ponytail: "phase count within depth cap" stays a max; the 3-stage systematic skeleton relies on Wave 1 splitting Build layers to reach standard/deep minimums (already how deep works, `phase-templates.md:13`).
