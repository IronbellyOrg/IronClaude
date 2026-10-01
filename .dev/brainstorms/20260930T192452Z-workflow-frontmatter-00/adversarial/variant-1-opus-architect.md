---
variant: 1
author: opus-architect
seed: .dev/brainstorms/20260930T192452Z-workflow-frontmatter-00/seed-brief.md
position: "Switch Wave 2 to render template 00; bump plan schema to workflow-plan/1.1"
---

# SPEC — Route template 00 (frontmatter + builder rules) into /sc:workflow plan.md

## Decision

1. **Q1 — Body shape: switch Wave 2 to render template 00; drop the 03 heading contract.**
   Rationale: 03's phase body is only `- **Goal**:`-style bullets (`03_project_plan_template.md:44-52`), which match no enumerable form (`sc-implement-protocol/SKILL.md:63-65`), so `/sc:implement @plan.md` collapses to T1 = whole document (`SKILL.md:67`). Template 00 uses `## Task N` (`00:32,40`), the one shape `/sc:implement` enumerates, and it carries the frontmatter (`00:1-5`) and the 8 rules (`00:13-20`), so they arrive with no restating. Extending only the frontmatter would add three fields and leave the plan unusable as a task source, and the 8 rules (per-task self-containment, per-task AC) would have no Task to apply to.
   Reconcile the gate: `refs/quality-gates.md:13` stops requiring `## Project Goal / ## Project Context / ## Phases` and requires the 00 shape instead (see Gate changes). 03 itself stays as is. Its other consumer is `rf-team-lead.md:463` (`/rf:project`), which this change does not touch.
2. **Q2 — Fill rules: `created_date` = run date (UTC, `YYYY-MM-DD`); `version` = `"1"`, or the previous integer + 1 when overwriting the same slug; `priority` = the value stated in the source, else `Medium`. No new flag.**
   Rationale: `input-parse.md:13` overwrites the same slug in place with no resume, so `version` only means something as a rewrite counter. The seed constraints forbid new flags unless they are unavoidable (seed-brief.md:31).
3. **Q3 — The new keys are required at schema-min (quick) and at full. Bump `schema: workflow-plan/1.0` to `workflow-plan/1.1`.**
   Rationale: presence and format checks are cheap and the same at every depth (`quality-gates.md:15-19`). The required key set and the body contract both change, and `git grep workflow-plan/1` finds no consumer outside `quality-gates.md:6` and its plugin mirror, so the bump breaks nothing.
4. **Q4 — `return-contract.yaml` stays exactly as it is (`contract_version: "1.0"`).**
   Rationale: the contract carries run and routing state (`return-contract.md:5-15`). Plan metadata already lives in `plan_path`'s frontmatter. Echoing it would duplicate the data and add a way for the two to drift, with no reader that needs it.

## File edits

### 1. `src/superclaude/skills/sc-workflow-protocol/SKILL.md` (Wave 2, lines 40-44)

Current (`SKILL.md:40-44`):

```markdown
## Wave 2 — Synthesize

Write `<run>/plan.md` using headings from `src/superclaude/templates/workflow/03_project_plan_template.md` (`## Project Goal`, `## Project Context`, `## Phases`). Do not copy MDTM 00–02.

If source was an inline prompt, `source.md` MUST already exist from Wave 0.
```

New:

```markdown
## Wave 2 — Synthesize

**Template:** Read `src/superclaude/templates/workflow/00_mdtm_template_simple_task.md`. Obey every rule in its HTML comment while writing, then delete the comment and every unused placeholder. Do not use 01–03.

Write `<run>/plan.md` in that shape:

- Frontmatter: the `refs/quality-gates.md` keys, then the template's `version`, `priority`, `created_date`, filled per `refs/quality-gates.md` § Fill rules.
- `# <title>`, `Source: <source path>`, `Goal: <observable result>`, optional `## Constraints`.
- Each Wave 1 phase → `## Phase N: <outcome>` followed by its `## Task N: <verb + deliverable>` headings. Task numbers run 1..N across the whole plan and are not restarted per phase.
- Phase Inputs → named files and source sections in the task body. Phase Outputs and Checkpoint → that phase's task `Acceptance criteria:` bullets (never a separate verify task). Phase deps → `Depends on: Task K`.

If source was an inline prompt, `source.md` MUST already exist from Wave 0.
```

### 2. `src/superclaude/skills/sc-workflow-protocol/refs/quality-gates.md` (whole file, 31 lines)

Replace lines 3-13 (current):

```markdown
`plan.md` frontmatter MUST include:

```yaml
schema: workflow-plan/1.0
source: <path>
strategy: systematic|agile|enterprise
depth: quick|standard|deep
slug: <slug>
```

Body MUST have headings: `## Project Goal`, `## Project Context`, `## Phases` (same names as `03_project_plan_template.md`). Each phase: Goal, Inputs, Outputs, Checkpoint, deps.
```

with:

```markdown
`plan.md` frontmatter MUST include:

```yaml
schema: workflow-plan/1.1
source: <path>
strategy: systematic|agile|enterprise
depth: quick|standard|deep
slug: <slug>
version: "<integer>"
priority: High|Medium|Low
created_date: "YYYY-MM-DD"
```

Body shape = `00_mdtm_template_simple_task.md`: `# <title>`, `Source:`, `Goal:`, optional `## Constraints`, then `## Phase N: …` group headings, each followed by `## Task N: …` headings.

## Fill rules

- `created_date`: run date in UTC, `YYYY-MM-DD`.
- `version`: `"1"`. If `<run>/plan.md` already exists with an integer `version`, write that value + 1.
- `priority`: the source's own `priority:` frontmatter or `Priority:` line if it is `High|Medium|Low` (case-insensitive, written capitalized); otherwise `Medium`.
```

Replace lines 15-19 (current):

```markdown
## Schema-min (quick)

- frontmatter keys present
- ≥1 phase
- no MDTM checklist dialect (`- [ ]` task items as the phase body)
```

with:

```markdown
## Schema-min (quick)

- all 8 frontmatter keys present; `schema` = `workflow-plan/1.1`; `priority` ∈ `High|Medium|Low`; `created_date` matches `^\d{4}-\d{2}-\d{2}$`; `version` matches `^[1-9]\d*$`
- no unfilled template text: no `<!--`, `[High | Medium | Low]`, `YYYY-MM-DD` literal, `version: ""`, or `[`-bracketed placeholder line
- ≥1 `## Task N:` heading; every Task has an `Acceptance criteria:` block with ≥1 bullet
- no checkbox (`- [ ]`, `- [x]`, `* [ ]`) or numbered-list (`1.` / `1)`) lines anywhere in the body
```

Replace lines 21-28 (current):

```markdown
## Full (standard/deep)

Schema-min plus:

- every phase has Inputs and Checkpoint
- deps acyclic
- phase count within depth cap
- output paths not under `.claude/skills|agents|commands`
```

with:

```markdown
## Full (standard/deep)

Schema-min plus:

- every `## Phase N:` is followed by ≥1 Task before the next Phase
- Task numbers are unique and contiguous from 1; every `Depends on: Task K` names a lower K (so deps are acyclic)
- no plan-wide `## Outputs`, `## Success Criteria`, or `## Verification` heading
- phase count within depth cap
- output paths not under `.claude/skills|agents|commands`
```

Line 30 (`Fail any check → STOP E-GATE …`) is unchanged.

### 3. Plugin mirror: `plugins/superclaude/skills/sc-workflow-protocol/SKILL.md` and `…/refs/quality-gates.md`

These are byte-identical to `src/` today (checked with `diff -r`, no output). Apply edits 1 and 2 verbatim, then confirm with `diff -r src/superclaude/skills/sc-workflow-protocol plugins/superclaude/skills/sc-workflow-protocol`. There is no plugin copy of `templates/` (`plugins/superclaude/templates/` holds only `roadmaps`), so the mirror needs nothing more.

### 4. `tests/commands/test_workflow_command.py`: add one guard (after line 38)

```python
_TPL00 = _REPO / "src" / "superclaude" / "templates" / "workflow" / "00_mdtm_template_simple_task.md"


def test_plan_renders_template_00_with_frontmatter():
    skill = (_SKILL / "SKILL.md").read_text(encoding="utf-8")
    gates = (_SKILL / "refs" / "quality-gates.md").read_text(encoding="utf-8")
    tpl = _TPL00.read_text(encoding="utf-8")
    assert "00_mdtm_template_simple_task.md" in skill
    assert "03_project_plan_template" not in skill + gates
    assert "workflow-plan/1.1" in gates
    for key in ("version:", "priority:", "created_date:"):
        assert key in tpl and key in gates, key
```

If the template is renamed, if SKILL drifts back to 03, or if a key is dropped from either side, this test fails.

## Files unchanged

- `src/superclaude/commands/workflow.md`: it only parses flags and activates the skill (`workflow.md:48-56`). No new flag. "Produces a **phased plan**" (`:12`) still holds.
- `plugins/superclaude/commands/workflow.md`: mirrors the above.
- `refs/return-contract.md`: see Decision 4.
- `refs/input-parse.md`: `E-GATE` "Wave 3 schema/heading fail" (`:26`) still describes the new gate. The slug and overwrite rules (`:9,13`) are what `version` builds on.
- `refs/phase-templates.md`: Wave 1 still produces phases with Goal/Inputs/Outputs/Checkpoint/deps (`:3`). How those map into Tasks lives in Wave 2 (edit 1), not here.
- `refs/overlap-routing.md`: `--handoff implement` already passes `plan.md` to `sc:implement-protocol` (`:5`). It now receives N tasks instead of 1.
- `src/superclaude/templates/workflow/00_…md`: already carries the fields and rules (`:1-21`).
- `src/superclaude/templates/workflow/03_project_plan_template.md`: still used by `/rf:project` (`rf-team-lead.md:463`).
- `.claude/**`: regenerate with `make sync-dev`. Never stage it.

## Fill rules

| Field | Source | Default | Format |
|-------|--------|---------|--------|
| `created_date` | wall-clock run date, UTC | n/a (always set) | `"YYYY-MM-DD"` quoted string |
| `version` | previous `<run>/plan.md` `version` + 1 when the same slug is overwritten (`input-parse.md:13`) | `"1"` | quoted positive integer |
| `priority` | source frontmatter `priority:` or a body `Priority:` line with a value in `High\|Medium\|Low` | `Medium` | one of `High`, `Medium`, `Low` |

The Wave 2 writer (the protocol agent) sets all three before Wave 3. The gate validates them and never repairs them.

## Gate changes

- **Schema-min (quick)**: frontmatter presence plus format for all 8 keys, placeholder residue, ≥1 Task, AC block per Task, and no checkbox or numbered-list lines. These checks keep the plan enumerable by `/sc:implement` and are also enough to catch a template-00 fill that went wrong, which is why the new keys are required at quick depth too.
- **Full (standard/deep)**: adds phase→task grouping, contiguous task ids, `Depends on` pointing backward only, no plan-wide Outputs/Success/Verification heading (`00:20`), plus the two existing checks (depth cap, `.claude/` output paths).
- **Removed**: the `## Project Goal/Context/Phases` heading check and the "each phase: Goal, Inputs, Outputs, Checkpoint, deps" body check (`quality-gates.md:13`). Their content now lives in `Goal:`, the task bodies, and the ACs.
- **STOP**: unchanged. Any failure → `E-GATE` (`quality-gates.md:30`, `SKILL.md:50`). A run dir exists by then, so `return-contract.yaml` is written with `status: failed`, `plan_path: null` (`return-contract.md:18-19`). No partial plan is reported as success.
- **Not mechanically gated**: of the 8 rules, requirement coverage, no fabrication, self-contained tasks, no read-only tasks, and enumerated multi-item work (`00:13-19`) need judgment. They bind the writer through the template comment, not through the gate. The mechanical ones (`00:12,17,20`) are gated.

## /sc:implement compatibility

- A `## Task N: …` heading with body text matches enumerable form 3 (`sc-implement-protocol/SKILL.md:65`), and `Task 3` normalizes to `T3` (`SKILL.md:61`), so ids stay ledger-valid.
- `## Phase N: …` counts as a group heading because it has enumerable children (`SKILL.md:65`), so phases do not become extra tasks.
- `Acceptance criteria:` matches AC QUALIFY rule 1 (`SKILL.md:75`), so each Task's ACs become `Ti.ACk`.
- `## Constraints` becomes a global constraint (`SKILL.md:83`).
- No dialect leaks in: the gate forbids `- [ ]` (which `SKILL.md:63` would enumerate as extra tasks) and `1.` / `1)` lines (which `SKILL.md:64` would enumerate). AC bullets are plain `-`, which `/sc:implement` does not enumerate. `Depends on:` is prose, and the MDTM fields that `SKILL.md:69` ignores are never emitted.
- Result: a plan with N tasks runs as T1..TN with per-task QA. Today it runs as a single T1 (`SKILL.md:67`).

## Risks

1. **"Has enumerable children" is ambiguous for sibling `##` headings.** In template 00, `## Phase 1` and `## Task 1` are both H2 (`00:30,32`), so a strict reader of `SKILL.md:65` could call Phase an empty task. *Mitigation:* Phase headings carry no body text, and `SKILL.md:65` only enumerates headings "with body text". The full gate forces ≥1 Task under every Phase. If this still fails in practice, demote Phase to plain text in a follow-up instead of changing `/sc:implement`.
2. **Installed users may not have `src/superclaude/templates/…`.** Wave 2 reads a `src/` path, which is the same convention the current `SKILL.md:42` already uses for 03. *Mitigation:* no regression versus today. Resolving template paths via the installed `.claude/templates/` (Makefile:148-153 syncs them) is listed out of scope.
3. **Plans get longer and slower to write** (per-task bodies and ACs instead of phase bullets), which is felt most at `deep` (6–12 phases). *Mitigation:* the depth caps are unchanged (`phase-templates.md:13`), and the "no read-only / no verify-only task" rules (`00:16-17`) keep task count close to real change count.
4. **The `version` increment depends on reading the old plan before overwrite.** If a malformed prior `version` exists, the result is ambiguous. *Mitigation:* the fill rule says an integer `version` only; otherwise write `"1"`. The gate regex rejects anything non-integer.
5. **Plugin/src drift.** *Mitigation:* the edits are verbatim, a `diff -r` check is listed, and the new test pins the `src/` side. `make verify-sync` covers `.claude/`.

## Out of scope

- Any Python/runtime code, new CLI flags (e.g. `--priority`), or a new STOP code.
- `return-contract.yaml` fields and its `contract_version`.
- Editing template 00, template 03, or `/rf:project`'s use of 03.
- Changing `/sc:implement` enumeration or AC QUALIFY rules.
- Mechanical enforcement of the 5 judgment rules (coverage, no fabrication, self-contained, no read-only, enumerate items).
- Template path resolution for pip/pipx installs (`.claude/templates/` vs `src/`).
- Staging anything under `.claude/`.
